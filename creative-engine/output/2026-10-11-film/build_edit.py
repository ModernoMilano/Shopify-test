"""Schrijft film-edit.json (met ondertitels) en film-edit-clean.json (zonder) voor film.py (draait in de sandbox).

Gebruik: python3 build_edit.py <vo-map> <uit-map>
De ondertitelkaarten worden getimed op de woorden in de gekozen opname (faster-whisper, woordtijden): een kaart komt op
bij zijn eerste woord en blijft 0,25 s na het laatste woord staan (brief, hoofdstuk 6), zonder over de volgende kaart heen.
"""
import json, os, sys
from faster_whisper import WhisperModel

SM = "/home/user/film/sm"
SRC = {"RAIN": f"{SM}/rain.mp4", "PIANO": f"{SM}/piano2.mp4", "TBA": f"{SM}/tbA.mp4", "TBB": f"{SM}/tbB.mp4",
       "LA": f"{SM}/lagoA.mp4", "LC": f"{SM}/lagoC.mp4", "LB": f"{SM}/lagoB.mp4", "SC": f"{SM}/seraC.mp4",
       "SD": f"{SM}/seraD.mp4", "SA": f"{SM}/seraA.mp4", "SB": f"{SM}/seraB.mp4", "LOGO": "/home/user/film/assets/logo.png"}
# Beeld (49,3 s): een dag, van de regen in Milaan tot het blauwe uur thuis. Zie FILM.md.
CUTS = [{"src": "RAIN", "from": 0.0, "dur": 3.9},
        {"src": "PIANO", "from": 0.0, "dur": 10.0},
        {"src": "TBA", "from": 0.2, "dur": 4.6},
        {"src": "TBB", "from": 0.2, "dur": 4.8, "crop": [0.0134, 0.0027, 0.9866, 0.976]},  # rand uit de reel van 8 okt
        {"src": "LA", "from": 0.0, "dur": 4.0},
        {"src": "LC", "from": 0.6, "dur": 3.2},
        {"src": "LB", "from": 0.0, "dur": 5.0},
        {"src": "SC", "from": 0.4, "dur": 3.0, "gain": 0.74},  # belichting zoals in Sera (9 okt)
        {"src": "SD", "from": 1.0, "dur": 2.6},
        {"src": "SA", "from": 0.8, "dur": 3.2},
        {"src": "SB", "from": 0.0, "dur": 5.0}]
# Gekozen opnames (ElevenLabs v4, stem Gideon): a = gewone lezing, b = met geschreven pauze. Keuze op tempo, dalend
# einde en een woordelijk kloppende transcriptie (voqa.py).
LINES = [("b/L1", 0.8, ["My father never", "owned an umbrella."]),
         ("a/L2", 4.3, ["He had one rule", "about clothes."]),
         ("b/L3", 7.0, ["Let the day", "do the dressing."]),
         ("a/L4", 12.3, ["I was eight."]),
         ("b/L5", 14.6, ["I thought he meant", "the rain."]),
         ("a/L6", 19.2, ["Some afternoons want", "the other side of me."]),
         ("a/L7", 24.0, ["For years, I was dressed", "for the evening by breakfast."]),  # 0,6 s-kaart samengevoegd
         ("b/L8", 30.9, ["Turns out,", "his rule was permission."]),
         ("b/L9", 38.2, ["To stop being early", "for my own life."]),
         ("a/L10", 44.4, ["On time."]),
         ("a/L11", 46.6, [])]  # de naam: geen kaart, het logo staat er al
BEDS = [{"gen": "rain", "from": 0.0, "to": 4.4, "db": -31, "fade": [0.05, 0.6]},
        {"gen": "surf", "from": 8.6, "to": 14.2, "db": -38, "fade": [1.5, 0.5]},   # de zee achter het glas
        {"gen": "birds", "from": 13.6, "to": 23.6, "db": -42, "fade": [0.3, 0.6]},  # 0,3 s voor het beeld (J-cut)
        {"gen": "lake", "from": 23.0, "to": 35.7, "db": -32, "fade": [0.3, 0.8]},
        {"gen": "room", "from": 35.3, "to": 49.3, "db": -54, "fade": [0.5, 1.0]}]
HITS = [{"gen": "thump", "at": 46.3, "len": 2.5, "db": -26}]


def cards(path, at, texts, model):
    if not texts:
        return []
    segs, _ = model.transcribe(path, beam_size=5, language="en", word_timestamps=True)
    words = [w for s in segs for w in s.words]
    out, i = [], 0
    for c in texts:
        n = len(c.split())
        ws = words[i:i + n]
        i += n
        out.append([at + ws[0].start - 0.05, at + ws[-1].end + 0.25, c])
    for a, b in zip(out, out[1:]):  # nooit twee kaarten tegelijk
        a[1] = min(a[1], b[0] - 0.04)
    return out


def main(vo_dir, out_dir):
    model = WhisperModel("small", device="cpu", compute_type="int8")
    vo, subs = [], []
    for f, at, texts in LINES:
        p = f"{vo_dir}/{f}_p.wav"
        vo.append({"file": p, "at": at, "rms": -20})
        subs += [{"t": [round(a, 2), round(b, 2)], "text": t} for a, b, t in cards(p, at, texts, model)]
    base = {"src": SRC, "cuts": CUTS,
            "logo": {"src": "LOGO", "width": 0.28, "seconds": 3.0, "y": 0.44, "fade": 0.6},
            "audio": {"vo": vo, "beds": BEDS, "hits": HITS, "duck": 4.0, "lufs": -14.0, "tp": -1.5}}
    json.dump(base, open(f"{out_dir}/film-edit-clean.json", "w"), indent=1)
    base["subs"] = {"font": "/home/user/film/f/cormorant.ttf", "weight": "Medium", "size": 46, "y": 0.605, "lines": subs}
    json.dump(base, open(f"{out_dir}/film-edit.json", "w"), indent=1)
    for s in subs:
        print(s)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
