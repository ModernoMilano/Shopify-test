"""Schrijft rows.json voor storyboard.py uit plan.json (draait in de sandbox, waar de frames staan).

Gebruik: python3 rows.py <plan.json> <frames-map> <uit rows.json> [images.json]
- Bestaande stukken: een frame uit de clip op clip_in + 0,5 s (ffmpeg), uit ~/film/sm/<key>.mp4.
- Nieuwe shots: het gekozen startbeeld uit images.json ({"V01 ...": "<pad>"}) als dat er is, anders een kaart.
"""
import json, os, subprocess, sys

CLIPS = {"RAIN": "rain", "PIANO": "piano2", "TBA": "tbA", "TBB": "tbB", "LA": "lagoA", "LC": "lagoC", "LB": "lagoB",
         "SC": "seraC", "SD": "seraD", "SA": "seraA", "SB": "seraB"}
NAMES = {"RAIN": "Regen in Milaan", "PIANO": "Il pianoforte", "TBA": "Total Bordeaux", "TBB": "Total Bordeaux (omgekeerd)",
         "LA": "Il lago", "LC": "Il lago (hand)", "LB": "Il lago (profiel)", "SC": "Sera (band)", "SD": "Sera (strepen)",
         "SA": "Sera (hand)", "SB": "Sera (fauteuil)"}


def main(plan_path, frames, out, images_path=None):
    plan = json.load(open(plan_path))
    images = json.load(open(images_path)) if images_path and os.path.exists(images_path) else {}
    os.makedirs(frames, exist_ok=True)
    rows = []
    for i, t in enumerate(plan["timeline"]):
        key = (t.get("existing_clip") or "").strip().upper()
        vo = t["vo"].split(" (")[0].strip()  # de tijden tussen haakjes niet
        if key in CLIPS:
            at = float(t.get("clip_in") or 0) + 0.5
            img = f"{frames}/{key}_{at:.1f}.jpg"
            if not os.path.exists(img):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(at), "-i", os.path.expanduser(f"~/film/sm/{CLIPS[key]}.mp4"),
                                "-frames:v", "1", "-q:v", "3", img], check=True)
            tag = f"BESTAAND · {NAMES[key]}"
        else:
            sid = t["shot"].replace("NEW ", "").split(" 0.0")[0].split(" (")[0].strip()
            sid = sid.split(",")[0].strip() if sid[:1] in "VSH" else sid  # "V01 GALLERIA", "H02 THE CHEST"
            match = next((k for k in images if k.startswith(sid.split(",")[0].split()[0])), None)
            img = images.get(match) if match else None
            kind = "stil" if sid.startswith("S") or "living still" in t["shot"] else "video"
            tag = f"NIEUW · {sid.split(',')[0]} · {kind}"
        rows.append({"t": f"{t['t_start']:.1f}-{t['t_end']:.1f}".replace(".", ","), "tag": tag, "vo": vo or "(geen stem)",
                     "nl": t.get("nl", ""), "img": img})
    json.dump({"title": plan["title"], "sub": "Storyboard · ModernoMilano · 32 beelden in 65 s, elk op de tekst die erbij klinkt",
               "rows": rows}, open(out, "w"), indent=1, ensure_ascii=False)
    print(len(rows), "rijen;", sum(1 for r in rows if r["img"]), "met beeld")


if __name__ == "__main__":
    main(*sys.argv[1:])
