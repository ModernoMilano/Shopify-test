"""Bouwt film-edit-<stem>.json voor film3.py uit plan.json (tijdlijn) en vo_script.json (draait in de sandbox).

Gebruik: python3 build_edit_v3.py <stem> [look]      stem: grady of holden (map ~/film/vo/<stem> uit split_read_v3.py)

- De tijdlijn komt uit plan.json: elke rij is een snede (NEW-shot of bestaande clip, clip_in, lengte). Stills (kind
  "still") krijgen de push-in uit de shotregel ("N percent"); een still die twee keer voorkomt (V09) zoomt de tweede keer
  verder door. Clips komen gladgemaakt uit vid/s/ (smooth.py); seraB blijft ruw (twinkelende lichten).
- Het beeld volgt de stem: een zin begint op zijn geplande tijd, maar nooit eerder dan GAP na het einde van de vorige zin.
  Loopt de stem daardoor achter op het beeld, dan worden de shots tussen de vorige zin en deze zin zo veel langer als
  hun bron toelaat (stills tot 2 s, clips tot hun einde), zodat elke zin op zijn eigen beeld blijft vallen. Het laatste
  shot gaat onder het logo naar zwart en mag zo nodig op zijn laatste frame blijven staan.
- Ondertitelkaarten op de echte pauzes in de stem (zoals build_edit.py van 11 okt), met de whisper-woorden via difflib
  aan de kaarttekst gekoppeld, zodat een verkeerd gehoord woord de wissel niet verschuift. Een kaart die volgens de
  kolom subtitle_cards van het plan op een later beeld hoort, begint nooit voor dat beeld: de still ervoor wordt korter
  (tot 1,0 s) of de zin begint later.
- Geluidslagen per scène (Galleria, atelier, villa, meer, thuis, binnenplaats, het label in stilte), als J-cut 0,3 s voor
  het beeld; één lage klap onder het logo. Geen muziek: die komt er bij het posten bij.
"""
import difflib, json, os, re, subprocess, sys, wave
import numpy as np
from faster_whisper import WhisperModel

TW = os.path.expanduser("~/tw")
VO = os.path.expanduser("~/film/vo")
SR = 48000
GAP = 0.3           # minste stilte tussen twee zinnen
STILL_EXTRA = 2.0   # een still mag zo veel langer staan
EXIST = {"PIANO": "piano2", "LB": "lagoB", "SA": "seraA", "SD": "seraD", "TBB": "tbB_fix", "LA": "lagoA", "SB": "seraB"}
# tbB_fix: de binnenplaatsclip met colorbalance=gm=0.08:gs=0.04:gh=0.02 voor de look (controle 14 okt: onder Portra liep
# de zuil naar roze-mauve; G lag 13 onder het gemiddelde van R en B, bij alle andere clips 0 tot -3)
CROP = {"TBB": [0.0134, 0.0027, 0.9866, 0.976],   # rand uit de reel van 8 okt
        "H05": [0.0, 0.08, 0.76, 0.92]}           # rechterrand met de groep voorbijgangers eruit (controle 14 okt: 5-6 figuren, de regel zegt 2-3)
CLIP_ZOOM = {("TBB", 2.0): [1.0, 1.02]}  # rij 30: de laatste 0,8 s staat hij stil; een lichte push-in houdt het beeld levend
NO_SMOOTH = {"SB"}
VOICE_DB = {"grady": 1.8, "holden": 0.3}
SCENE = {"H01": "galleria", "H02": "galleria", "H03": "galleria", "H04": "galleria", "H05": "galleria", "V01": "galleria",
         "S05": "galleria", "V02": "atelier", "S01": "atelier", "V03": "atelier", "V12": "atelier", "PIANO": "villa",
         "S02": "atelier", "V04": "atelier", "LB": "lake", "S03": "atelier", "V06": "atelier", "V07": "atelier",
         "V11": "atelier", "SA": "home", "SD": "home", "V08": "atelier", "TBB": "courtyard", "S04": "quiet",
         "V09": "quiet", "LA": "boat", "V05": "atelier", "SB": "home", "V10": "home"}
BEDS = {"galleria": [{"gen": "air", "db": -43, "lp": 7000, "fade": [0.3, 0.6]}],
        "atelier": [{"gen": "room", "db": -46, "fade": [0.3, 0.5]}],
        "villa": [{"gen": "air", "db": -44, "fade": [0.4, 0.6]}, {"gen": "surf", "db": -42, "fade": [0.6, 0.5]}],
        "lake": [{"gen": "lake", "db": -38, "fade": [0.3, 0.6]}],
        "boat": [{"gen": "lake", "db": -38, "fade": [0.3, 0.6]}, {"gen": "city_night", "db": -46, "fade": [0.4, 0.6]}],
        "home": [{"gen": "rain_window", "db": -47, "fade": [0.5, 0.8], "duck": 2}],
        "courtyard": [{"gen": "air", "db": -43, "fade": [0.3, 0.5]}],
        "quiet": [{"gen": "room", "db": -52, "fade": [0.2, 0.4]}]}


def read(path):
    with wave.open(path) as f:
        return np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").reshape(-1, f.getnchannels()).astype(np.float64) / 32768


def write(path, x):
    with wave.open(path, "wb") as f:
        f.setnchannels(x.shape[1]); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def rms_db(x, ms=5):
    h = int(SR * ms / 1000)
    m = x.max(1) if x.ndim > 1 else x
    k = len(m) // h
    return 20 * np.log10(np.sqrt((m[:k * h].reshape(k, h) ** 2).mean(1)) + 1e-9), h


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def clip_len(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def declick(src, dst):
    """Fade van 10 ms aan beide kanten; meldt een kort geluid na stilte aan het eind (mogelijke mondklik)."""
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
        print(f"  {os.path.basename(src)}: kort geluid na stilte aan het eind, {(j + 1) * h / SR:.3f}-{(b + 1) * h / SR:.3f} s (nakijken)")
    y = x.copy()
    f = int(0.01 * SR)
    y[:f] *= (np.sin(np.linspace(0, np.pi / 2, f)) ** 2)[:, None]
    y[-f:] *= (np.cos(np.linspace(0, np.pi / 2, f)) ** 2)[:, None]
    write(dst, y)
    return len(y) / SR


def cards(path, at, texts, model):
    """Kaarttijden voor één zin (in filmtijd): de wissel ligt op de stilte die het dichtst bij de woordgrens ligt."""
    if not texts:
        return []
    x = read(path)
    e, h = rms_db(x, 10)
    on = e > e.max() - 30
    idx = np.flatnonzero(on)
    t0, t1 = idx[0] * h / SR, (idx[-1] + 1) * h / SR
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
    sw = [(c, norm(t)) for c, txt in enumerate(texts) for t in txt.split() if norm(t)]
    hidx = [i for i, w in enumerate(words) if norm(w.word)]
    sm = difflib.SequenceMatcher(None, [s[1] for s in sw], [norm(words[i].word) for i in hidx], autojunk=False)
    link = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for d in range(i2 - i1):
                link[i1 + d] = hidx[j1 + d]
    out, start = [], t0 - 0.05
    for c in range(1, len(texts)):
        fs = next(si for si, (cc, _) in enumerate(sw) if cc == c)
        fi, li = link.get(fs), link.get(fs - 1)
        if fi is None and li is not None:
            fi = li + 1
        if li is None and fi is not None:
            li = fi - 1
        if fi is None or fi >= len(words):
            tb = t0 + (t1 - t0) * fs / len(sw)
            lo, hi = tb - 0.5, tb + 0.5
            print(f"  kaart {c} van '{texts[c]}' niet aan whisper gekoppeld; naar rato geplaatst")
        else:
            tb = words[fi].start
            lo = words[li].start if 0 <= li < len(words) else tb - 0.6
            hi = words[fi + 1].start if fi + 1 < len(words) else tb + 0.9
        near = [g for g in gaps if lo < (g[0] + g[1]) / 2 < hi]
        if near:
            g = min(near, key=lambda g: abs((g[0] + g[1]) / 2 - tb))
            end, nxt = min(g[0] + 0.15, g[1] - 0.07), g[1] - 0.03
        else:
            end, nxt = tb - 0.04, tb
        out.append([at + start, at + end, texts[c - 1]])
        start = nxt
    out.append([at + start, at + t1 + 0.25, texts[-1]])
    return out


def card_row(plan_rows, l, text):
    """De rij uit plan.json waar deze kaart volgens de kolom subtitle_cards op hoort (None als het plan er niets over zegt)."""
    nc = norm(text)
    for i, r in enumerate(plan_rows):
        nr = "".join(norm(x) for x in r.get("subtitle_cards", []))
        if nc and nr and (nc in nr or nr in nc) and r["t_start"] - 8 <= l["at"] <= r["t_end"] + 8:
            return i
    return None


def src_path(key):
    name = EXIST.get(key, key)
    cands = [f"{TW}/vid/s/{name}.mp4", f"{TW}/vid/final/{name}.mp4", f"{TW}/vid/{name}.mp4", f"{TW}/vid/sm/{name}_raw.mp4"]
    if key in NO_SMOOTH:
        cands = cands[1:]
    for p in cands:
        if os.path.exists(p) and os.path.getsize(p) > 0:
            return p
    raise SystemExit("geen bron voor " + key)


def main(stem, look=None):
    plan = json.load(open(f"{TW}/plan.json"))
    chosen = json.load(open(f"{TW}/chosen.json"))
    kinds = {s["id"].split()[0]: s.get("kind", "video") for s in plan["new_shots"]}
    rows, zoom_seen = [], {}
    for r in plan["timeline"]:
        m = re.match(r"^NEW ([HVS]\d\d)", r["shot"])
        key = m.group(1) if m else r["existing_clip"]
        kind = "still" if (m and kinds[key] == "still") else "clip"
        row = {"key": key, "kind": kind, "from": float(r["clip_in"]), "dur": round(r["t_end"] - r["t_start"], 3),
               "plan": [r["t_start"], r["t_end"]], "nl": r["nl"]}
        if kind == "still":
            pm = re.search(r"(\d+) percent", r["shot"])
            z = int(pm.group(1)) / 100 if pm else 0.03
            z0 = zoom_seen.get(key, 1.0)
            row["zoom"] = [z0, round(z0 + z, 3)]
            zoom_seen[key] = round(z0 + z, 3)
            row["path"] = f"{TW}/{chosen[key]['file']}"
            row["slack"] = STILL_EXTRA
        else:
            row["path"] = src_path(key)
            row["slack"] = max(0.0, clip_len(row["path"]) - row["from"] - row["dur"] - 0.05)
        if key in CROP:
            row["crop"] = CROP[key]
        if (key, row["from"]) in CLIP_ZOOM:
            row["zoom"] = CLIP_ZOOM[(key, row["from"])]
        rows.append(row)
    for i, row in enumerate(rows):   # niet doorlopen in een stuk van dezelfde clip dat later nog komt
        if row["kind"] == "clip":
            later = [r["from"] for r in rows[i + 1:] if r["key"] == row["key"] and r["from"] > row["from"]]
            if later:
                row["slack"] = max(0.0, min(row["slack"], min(later) - row["from"] - row["dur"]))
    rows[-1]["slack"] = 3.0   # onder het logo naar zwart: het laatste frame mag blijven staan

    vo = json.load(open(f"{TW}/vo_script.json"))
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    for l in vo:
        src, dst = f"{VO}/{stem}/L{l['n']}_p.wav", f"{VO}/{stem}/L{l['n']}_f.wav"
        l["len"] = declick(src, dst)
        l["file"] = dst
        l["row"] = next(i for i, r in enumerate(rows) if r["plan"][0] <= l["at"] < r["plan"][1])
        l["lead"] = round(l["at"] - rows[l["row"]]["plan"][0], 3)
        l["offs"] = cards(dst, 0.0, l["cards"], model)   # kaarttijden t.o.v. het begin van de zin
        l["card_row"] = [card_row(plan["timeline"], l, ct) for _, _, ct in l["offs"]]

    def start_of(i):
        return round(sum(r["dur"] for r in rows[:i]), 3)

    prev_end = -9.0
    for n, l in enumerate(vo):
        i = l["row"]
        at = max(start_of(i) + l["lead"], prev_end + GAP)
        late = at - (start_of(i) + l["lead"])
        if late > 0.001 and n > 0:
            rest = late
            for j in range(vo[n - 1]["row"], i):
                use = min(rest, rows[j]["slack"])
                rows[j]["dur"] = round(rows[j]["dur"] + use, 3)
                rows[j]["slack"] -= use
                rest -= use
                if rest <= 0.001:
                    break
            at = max(start_of(i) + l["lead"], prev_end + GAP)
        # een kaart die volgens het plan op een later beeld hoort: dat beeld mag niet na de kaart beginnen. Eerst de
        # stills ertussen inkorten (tot 1,0 s), anders de zin later laten beginnen (14 okt: "until the seam" begon
        # 0,5 s voor de snede naar de naad, "it was new." 0,2 s voor de knie)
        for k, (cs, ce, ct) in enumerate(l["offs"]):
            rho = l["card_row"][k]
            if rho is None or rho <= i:
                continue
            early = start_of(rho) - (at + cs)
            if early <= 0.05:
                continue
            for j in range(rho - 1, i - 1, -1):
                if rows[j]["kind"] == "still" and early > 0.05:
                    cut = min(early, max(0.0, rows[j]["dur"] - 1.0))
                    rows[j]["dur"] = round(rows[j]["dur"] - cut, 3)
                    rows[j]["slack"] += cut
                    early -= cut
            if early > 0.05:
                at += early
        l["at_final"] = round(at, 3)
        prev_end = at + l["len"]
    total = start_of(len(rows))
    need = vo[-1]["at_final"] + vo[-1]["len"] + 0.6
    if need > total:
        rows[-1]["dur"] = round(rows[-1]["dur"] + need - total, 3)
        total = start_of(len(rows))

    src, cuts = {}, []
    for row in rows:
        src[row["key"]] = row["path"]
        c = {"src": row["key"], "from": row["from"], "dur": row["dur"]}
        if "zoom" in row:
            c["zoom"] = row["zoom"]
        if "crop" in row:
            c["crop"] = row["crop"]
        cuts.append(c)
    src["LOGO"] = f"{TW}/refs/logo.png"
    lstart = start_of(len(rows) - 1) + 0.2
    logo = {"src": "LOGO", "width": 0.28, "seconds": round(total - lstart, 3), "y": 0.44, "fade": 0.6, "black": 1.8}

    voice, subs = [], []
    for l in vo:
        voice.append({"file": l["file"], "at": l["at_final"], "rms": -20, "db": VOICE_DB.get(stem, 0.0)})
        subs += [{"t": [round(l["at_final"] + a, 2), round(l["at_final"] + b, 2)], "text": t} for a, b, t in l["offs"]]
    bounds = [start_of(i) for i in range(1, len(rows))]
    last = start_of(len(rows) - 1)
    for sb in subs:   # geen kaart tot in het slotbeeld met het woordmerk
        if sb["t"][0] < last < sb["t"][1]:
            sb["t"][1] = round(last - 0.04, 2)
    for sb in subs:   # geen kaart die net over een snede doorloopt of net ervoor begint
        for c in bounds:
            if c < sb["t"][1] < c + 0.35 and sb["t"][1] - 0.35 > sb["t"][0]:
                sb["t"][1] = round(c - 0.04, 2)
            if c - 0.15 < sb["t"][0] < c:
                sb["t"][0] = round(c + 0.005, 3)
    for a, b in zip(subs, subs[1:]):
        a["t"][1] = min(a["t"][1], round(b["t"][0] - 0.04, 2))

    beds, hits = [], [{"gen": "thump", "at": 0.05, "len": 0.6, "db": -33}, {"gen": "thump", "at": round(lstart, 3), "len": 2.5, "db": -28}]
    i, seen_courtyard = 0, False
    while i < len(rows):
        sc = SCENE[rows[i]["key"]]
        j = i
        while j + 1 < len(rows) and SCENE[rows[j + 1]["key"]] == sc:
            j += 1
        a, b = max(0.0, start_of(i) - 0.3), min(total, start_of(j + 1) + 0.3)
        if j == len(rows) - 1:
            b = total
        for bed in BEDS[sc]:
            beds.append({**bed, "from": round(a, 3), "to": round(b, 3)})
        if sc == "courtyard" and not seen_courtyard:
            beds.append({"gen": "birds", "db": -46, "lp": 6000, "verb": 0.5, "fade": [0.2, 0.3], "from": round(a, 3), "to": round(b, 3)})
            seen_courtyard = True
        i = j + 1

    cfg = {"src": src, "cuts": cuts, "logo": logo,
           "audio": {"vo": voice, "beds": beds, "hits": hits, "duck": 4.0, "lufs": -14.0, "tp": -1.5},
           "subs": {"font": f"{TW}/cormorant.ttf", "weight": "SemiBold", "size": 52, "y": 0.605, "lines": subs}}
    if look:
        sys.path.insert(0, TW)
        import looks_defs
        cfg["look"] = looks_defs.LOOKS[look][2]
    tag = f"-{stem}" + (f"-{look}" if look else "")
    out = os.path.expanduser("~/film/out")
    os.makedirs(out, exist_ok=True)
    json.dump(cfg, open(f"{out}/film-edit{tag}.json", "w"), indent=1)
    timing = {"total": total, "rows": [{"key": r["key"], "start": start_of(i), "dur": r["dur"], "plan": r["plan"]} for i, r in enumerate(rows)],
              "lines": [{"n": l["n"], "at": l["at_final"], "plan": l["at"], "len": round(l["len"], 2), "text": l["text"]} for l in vo],
              "subs": subs}
    json.dump(timing, open(f"{out}/timing{tag}.json", "w"), indent=1)
    print(f"film {total:.2f} s, {len(cuts)} snedes, {len(subs)} kaarten")
    for i, r in enumerate(rows):
        d = r["dur"] - (r["plan"][1] - r["plan"][0])
        print(f"  {i:2d} {r['key']:<6} {start_of(i):6.2f} +{r['dur']:.2f}" + (f"  (+{d:.2f} s)" if d > 0.001 else ""))
    for l in vo:
        print(f"  L{l['n']:<2} {l['at_final']:6.2f} (plan {l['at']:5.1f}, +{l['at_final'] - l['at']:.2f}) {l['len']:.2f} s  {l['text']}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
