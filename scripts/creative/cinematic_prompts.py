# Filmische serie (stijl Zegna / moodboard van de eigenaar): per shot de definitieve prompt + referentielijst.
# Een shot heeft een scene_prompt (cameraman-brief), handles uit de garderobe (leeg = sfeerbeeld van Milaan zonder kleding)
# en optioneel ref_keys per handle (bv. ["primary", "back"]). Voorbeeld: creative-engine/output/2026-10-06-zegna-stijl/shots.json
# Gebruik: python3 -I scripts/creative/cinematic_prompts.py shots.json built.json [face_media_id]
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = {i["handle"]: i for i in json.load(open(f"{ROOT}/creative-engine/data/wardrobe.json"))["items"]}
MEDIA = json.load(open(f"{ROOT}/creative-engine/data/higgsfield-media.json"))["media"]

FACE = ("a composed Mediterranean man in his early fifties, swept-back silver-grey hair, short grey beard, "
        "tall and lean, weathered handsome face, natural skin with real pores and lines")

def describe(item):
    labels = " + ".join(p["label"] for p in item["pieces"])
    return f'{item["title"]} ({labels})'

def refs_for(item, hero, keys=None):
    imgs = item["images"]
    if keys:
        return [imgs[k] for k in keys if imgs.get(k)]
    urls = [imgs["primary"]]
    if hero:
        for k in ("detail", "model"):
            if imgs.get(k) and imgs[k] not in urls:
                urls.append(imgs[k]); break
    return urls

def build(shot, face_media=None):
    handles = shot["handles"]
    items = [W[h] for h in handles]
    hero = shot["framing"] in ("detail", "still-life") or len(items) <= 2
    refs, lines = [], []
    for it in items:
        nums = []
        for u in refs_for(it, hero, shot.get("ref_keys", {}).get(it["handle"])):
            refs.append({"url": u, "label": it["title"], "media_id": MEDIA.get(u)})
            nums.append(f"#{len(refs)}")
        lines.append(f'- {describe(it)}, exactly as in reference image {" and ".join(nums)}')
    person = shot["people"] == 1
    if not items:
        tail = "There are no people and no clothing in the picture. No logos, signs, labels or readable text anywhere. Photographic, not CGI: real optics, real grain."
        return {"n": shot["n"], "title": shot["title_nl"], "handles": [], "people": 0, "framing": shot["framing"],
                "prompt": shot["scene_prompt"].strip() + "\n\n" + tail, "refs": []}
    has_shoes = any(p["slot"] == "shoes" for it in items for p in it["pieces"])
    parts = [shot["scene_prompt"].strip()]
    if person:
        if shot["framing"] != "detail":
            parts.append(f"The man: {FACE}.")
        if face_media:
            refs.append({"url": None, "label": "face", "media_id": face_media})
            parts.append(f"His face, hair and beard are exactly those of the man in reference image #{len(refs)}; ignore that image's clothing, light and setting.")
        parts.append("He wears only these ModernoMilano pieces and nothing else:\n" + "\n".join(lines))
    else:
        parts.append("The only clothing in the picture is these ModernoMilano pieces:\n" + "\n".join(lines))
    parts.append(f'How they are worn or arranged: {shot["worn_notes"].strip()}')
    parts.append("Reproduce every piece exactly as in its reference: same colour and shade, same knit or weave, same collar, "
                 "same buttons or zip, same pockets, same length and fit. Do not redesign anything.")
    if person:
        rules = ["His hands and wrists are bare."]
        if has_shoes:
            rules.append("The loafers are worn without socks, ankles bare.")
        elif shot["framing"] in ("full-body",):
            raise SystemExit(f'{shot["n"]}: full-body without loafers')
        else:
            rules.append("His feet are not in the picture.")
        rules.append("He is the only person in the picture.")
        parts.append(" ".join(rules))
    parts.append("No logos, labels, badges or readable text anywhere in the picture. Photographic, not CGI: real optics, real grain.")
    return {"n": shot["n"], "title": shot["title_nl"], "handles": handles, "people": shot["people"],
            "framing": shot["framing"], "prompt": "\n\n".join(parts), "refs": refs}

if __name__ == "__main__":
    final = json.load(open(sys.argv[1]))
    shots = final["final"]["shots"] if "final" in final else final["shots"]
    face = sys.argv[3] if len(sys.argv) > 3 else None
    out = [build(s, face) for s in shots]
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    for o in out:
        missing = [r["url"] for r in o["refs"] if r["url"] and not r["media_id"]]
        print(o["n"], o["title"], len(o["refs"]), "refs", len(missing), "to import", len(o["prompt"].split()), "words")
