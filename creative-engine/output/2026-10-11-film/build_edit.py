"""Schrijft film-edit.json (met ondertitels) en film-edit-clean.json (zonder) voor film.py (draait in de sandbox).

Gebruik: python3 build_edit.py <vo-map> <uit-map>

- Elke gekozen VO-opname krijgt een fade van 10 ms aan beide kanten, en de bekende klik in L2 gaat eraf (eindcontrole
  11 okt: een mondklik van -22,6 dBFS na "about clothes." viel recht in digitale stilte). Mogelijke andere klikjes worden
  gemeld, niet automatisch geknipt.
- De ondertitelkaarten wisselen op de echte pauzes in de stem. Whisper rekt een woord uit over de stilte die erop volgt;
  daarom wordt de wissel op de stilte gelegd die het dichtst bij de woordgrens van whisper ligt (eindcontrole 11 okt: "do
  the dressing." kwam 0,65 s te vroeg). Een kaart blijft 0,25 s na het laatste geluid staan (brief, hoofdstuk 6).
"""
import json, os, sys, wave
import numpy as np
from faster_whisper import WhisperModel

SR = 48000
SM = "/home/user/film/sm"
SRC = {"RAIN": f"{SM}/rain.mp4", "PIANO": f"{SM}/piano2.mp4", "TBA": f"{SM}/tbA.mp4", "TBB": f"{SM}/tbB.mp4",
       "LA": f"{SM}/lagoA.mp4", "LC": f"{SM}/lagoC.mp4", "LB": f"{SM}/lagoB.mp4", "SC": f"{SM}/seraC.mp4",
       "SD": f"{SM}/seraD.mp4", "SA": f"{SM}/seraA.mp4", "SB": f"{SM}/seraB.mp4", "LOGO": "/home/user/film/assets/logo.png"}
# Beeld (48,2 s): een dag, van de regen in Milaan tot het blauwe uur thuis. Zie FILM.md.
# TBB 4,8 -> 3,7 s: het einde stond ruim 2 s bijna stil, net na het sterkste moment (eindcontrole 11 okt).
CUTS = [{"src": "RAIN", "from": 0.0, "dur": 3.9},           # 0,0
        {"src": "PIANO", "from": 0.0, "dur": 10.0},         # 3,9
        {"src": "TBA", "from": 0.2, "dur": 4.6},            # 13,9
        {"src": "TBB", "from": 0.2, "dur": 3.7, "crop": [0.0134, 0.0027, 0.9866, 0.976]},  # 18,5; rand uit de reel van 8 okt
        {"src": "LA", "from": 0.0, "dur": 4.0},             # 22,2
        {"src": "LC", "from": 0.6, "dur": 3.2},             # 26,2
        {"src": "LB", "from": 0.0, "dur": 5.0},             # 29,4
        {"src": "SC", "from": 0.4, "dur": 3.0, "gain": 0.74},  # 34,4; belichting zoals in Sera (9 okt)
        {"src": "SD", "from": 1.0, "dur": 2.6},             # 37,4
        {"src": "SA", "from": 0.8, "dur": 3.2},             # 40,0
        {"src": "SB", "from": 0.0, "dur": 5.0}]             # 43,2 tot 48,2; logo vanaf 45,2
# Gekozen opnames (ElevenLabs v4, stem Gideon): a = gewone lezing, b = met geschreven pauze. Keuze op tempo, dalend
# einde en een woordelijk kloppende transcriptie (voqa.py). Kaarten splitsen waar de stem een pauze houdt.
LINES = [("b/L1", 0.8, ["My father", "never owned an umbrella."]),
         ("a/L2", 4.3, ["He had one rule", "about clothes."]),
         ("b/L3", 7.0, ["Let the day", "do the dressing."]),
         ("a/L4", 12.3, ["I was eight."]),
         ("b/L5", 14.6, ["I thought", "he meant the rain."]),
         ("a/L6", 19.2, ["Some afternoons want", "the other side of me."]),
         ("a/L7", 22.9, ["For years, I was dressed", "for the evening by breakfast."]),
         ("b/L8", 29.8, ["Turns out,", "his rule was permission."]),
         # 2,7 s na "permission." in plaats van 4,4 s: de zin loopt door over de snede naar huis (verhaalcontrole)
         ("b/L9", 35.4, ["To stop being early", "for my own life."]),
         ("a/L10", 43.3, ["On time."]),   # landt op de snede naar de fauteuil (43,2)
         ("a/L11", 45.5, [])]             # de naam: geen kaart, het logo staat er al
# Een doorlopende bodem, zodat het nergens digitaal stil wordt; elke laag begint even voor zijn beeld (J-cut).
BEDS = [{"gen": "rain", "from": 0.0, "to": 4.1, "db": -31, "fade": [0.05, 0.8], "duck": 7},  # zachter onder zin 1
        {"gen": "air", "from": 3.8, "to": 9.0, "db": -44, "fade": [0.4, 1.0]},                 # binnen in de villa
        {"gen": "surf", "from": 3.9, "to": 8.9, "db": -42, "fade": [0.8, 0.5]},                # de zee, nog ver
        {"gen": "surf", "from": 8.6, "to": 14.2, "db": -38, "fade": [1.5, 0.5]},               # bij het glas
        {"gen": "air", "from": 13.7, "to": 22.4, "db": -42, "fade": [0.4, 0.5]},               # binnenplaats
        {"gen": "birds", "from": 13.5, "to": 14.6, "db": -42, "fade": [0.2, 0.3], "lp": 6000, "verb": 0.5},
        {"gen": "birds", "from": 17.0, "to": 19.2, "db": -45, "fade": [0.2, 0.3], "lp": 6000, "verb": 0.5},
        {"gen": "lake", "from": 21.9, "to": 34.6, "db": -38, "fade": [0.3, 0.8]},
        {"gen": "room", "from": 34.2, "to": 48.2, "db": -48, "fade": [0.5, 1.0]}]
HITS = [{"gen": "thump", "at": 45.2, "len": 2.5, "db": -28}]


def read(path):
    with wave.open(path) as f:
        x = np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").reshape(-1, f.getnchannels()).astype(np.float64) / 32768
    return x


def write(path, x):
    with wave.open(path, "wb") as f:
        f.setnchannels(x.shape[1])
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def rms_db(x, ms=5):
    h = int(SR * ms / 1000)
    m = x.max(1) if x.ndim > 1 else x
    k = len(m) // h
    return 20 * np.log10(np.sqrt((m[:k * h].reshape(k, h) ** 2).mean(1)) + 1e-9), h


# Met de hand gevonden klikjes (eindcontrole 11 okt): in L2 zit 2,185-2,212 s een mondklik na "clothes.". Niet automatisch
# knippen: een losse t aan het eind ("eight", "out", "breakfast") ziet er in de meting net zo uit.
TRIM_END = {"a/L2": 2.180}


def declick(key, src, dst):
    """Knipt de bekende klikjes weg, meldt mogelijke andere (kort geluid na minstens 20 ms stilte aan het eind), en zet
    een fade van 10 ms aan beide kanten (15 ms aan een geknipt eind)."""
    x = read(src)
    e, h = rms_db(x)
    on = e > e.max() - 40
    idx = np.flatnonzero(on)
    a, b = idx[0], idx[-1]
    j = b
    while j > a and on[j]:
        j -= 1
    gap = j
    while gap > a and not on[gap]:
        gap -= 1
    if (b - j) * h < 0.03 * SR and (j - gap) * h >= 0.02 * SR:
        print(f"  {key}: kort geluid na stilte aan het eind, {(j + 1) * h / SR:.3f}-{(b + 1) * h / SR:.3f} s (nakijken)")
    y = x[: int(TRIM_END[key] * SR)].copy() if key in TRIM_END else x.copy()
    f = int(0.01 * SR)
    fo = int(0.015 * SR) if key in TRIM_END else f
    y[:f] *= (np.sin(np.linspace(0, np.pi / 2, f)) ** 2)[:, None]
    y[-fo:] *= (np.cos(np.linspace(0, np.pi / 2, fo)) ** 2)[:, None]
    write(dst, y)
    return 0.0


def cards(path, at, texts, model):
    """Kaarttijden voor één zin (in filmtijd)."""
    if not texts:
        return []
    x = read(path)
    e, h = rms_db(x, 10)
    on = e > e.max() - 30
    idx = np.flatnonzero(on)
    t0, t1 = idx[0] * h / SR, (idx[-1] + 1) * h / SR
    # stiltes van minstens 0,15 s binnen de zin
    gaps, k = [], idx[0]
    while k < idx[-1]:
        if not on[k]:
            j = k
            while j < idx[-1] and not on[j]:
                j += 1
            if (j - k) * h >= 0.15 * SR:
                gaps.append((k * h / SR, j * h / SR))
            k = j
        else:
            k += 1
    segs, _ = model.transcribe(path, beam_size=5, language="en", word_timestamps=True)
    words = [w for s in segs for w in s.words]
    out, i, start = [], 0, t0 - 0.05
    for c in range(len(texts) - 1):
        i += len(texts[c].split())
        tb = words[i].start
        # alleen een stilte NA het begin van het laatste woord van deze kaart, en voor het woord na het eerste van de
        # volgende kaart (hercontrole 11 okt: bij L7 greep de wissel de pauze na "For years," en liep de kaart voor)
        lo = words[i - 1].start
        hi = words[i + 1].start if i + 1 < len(words) else tb + 0.9
        near = [g for g in gaps if lo < (g[0] + g[1]) / 2 < hi]
        if near:
            g = min(near, key=lambda g: abs((g[0] + g[1]) / 2 - tb))
            end, nxt = min(g[0] + 0.15, g[1] - 0.07), g[1] - 0.03
        else:
            end, nxt = tb - 0.04, tb
        out.append([at + start, at + end, texts[c]])
        start = nxt
    out.append([at + start, at + t1 + 0.25, texts[-1]])
    return out


def main(vo_dir, out_dir):
    model = WhisperModel("small", device="cpu", compute_type="int8")
    vo, subs = [], []
    for f, at, texts in LINES:
        src, dst = f"{vo_dir}/{f}_p.wav", f"{vo_dir}/{f}_f.wav"
        shift = declick(f, src, dst)
        vo.append({"file": dst, "at": round(at + shift, 3), "rms": -20})
        subs += [{"t": [round(a, 2), round(b, 2)], "text": t} for a, b, t in cards(dst, at + shift, texts, model)]
    # geen kaart die net over een snede doorloopt of net ervoor begint (hercontrole 11 okt: 3 frames over het detail van
    # de hand, en 2 frames voor de snede naar de knie)
    cuts, t = [], 0.0
    for c in CUTS:
        t += c["dur"]
        cuts.append(round(t, 3))
    for sb in subs:
        for c in cuts:
            if c < sb["t"][1] < c + 0.35 and sb["t"][1] - 0.35 > sb["t"][0]:
                sb["t"][1] = round(c - 0.04, 2)
            if c - 0.15 < sb["t"][0] < c:
                sb["t"][0] = round(c + 0.005, 3)
    for a, b in zip(subs, subs[1:]):  # nooit twee kaarten tegelijk
        a["t"][1] = min(a["t"][1], round(b["t"][0] - 0.04, 2))
    base = {"src": SRC, "cuts": CUTS,
            "logo": {"src": "LOGO", "width": 0.28, "seconds": 3.0, "y": 0.44, "fade": 0.6},
            "audio": {"vo": vo, "beds": BEDS, "hits": HITS, "duck": 4.0, "lufs": -14.0, "tp": -1.5}}
    json.dump(base, open(f"{out_dir}/film-edit-clean.json", "w"), indent=1)
    base["subs"] = {"font": "/home/user/film/f/cormorant.ttf", "weight": "SemiBold", "size": 52, "y": 0.605,
                    "lines": subs}
    json.dump(base, open(f"{out_dir}/film-edit.json", "w"), indent=1)
    for s in subs:
        print(s)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
