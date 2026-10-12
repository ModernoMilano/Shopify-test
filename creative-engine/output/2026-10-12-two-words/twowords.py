"""Bouwt de Higgsfield-aanvragen voor de merkfilm "Two Words" (v2, 12 oktober 2026) uit het vastgezette plan (plan.json).

Gebruik (print JSON voor de MCP-tools):
  python3 -I twowords.py images [id ...]          -> generate_image_batch: 4K-startbeelden, 2 varianten per nieuw shot
                                                     (max 12 per batch: geef ids mee, of "images" twee keer met --half 1|2)
  python3 -I twowords.py draft <id> <start_job>    -> generate_video: Seedance 2.5, concept 480p
  python3 -I twowords.py final <id> <start_job> <draft_job>  -> generate_video: 1080p vanuit het concept
  python3 -I twowords.py list                      -> de nieuwe shots met hun referenties

Regels (SKILL.md, model.json): nano_banana_pro 4K 9:16, de element-placeholder als hij in beeld is, alleen eigen
productfoto's en het eigen label als referenties (max 4), geen filmwoorden, de realismeblokken uit model.json. Video:
seedance_2_5, omni_reference, start_image + de twee gezichtsfoto's als zijn gezicht in beeld is, eerst 480p, dan 1080p.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MODEL = json.load(open(os.path.join(ROOT, "creative-engine", "data", "model.json")))
HF, P = MODEL["higgsfield"], MODEL["prompt"]
EL = HF["element_placeholder"]
FACES = [r["upscale_job_id"] for r in HF["face_refs"] if any(r["file"].endswith(f"/{x}.jpg") for x in HF["video_face_refs"])]
PLAN = json.load(open(os.path.join(HERE, "plan.json")))

# Referenties (media-ids, al op Higgsfield; zie higgsfield-media.json, videos4.py en shots100.py)
REFS = {
    "label": ["72a49aff-1436-4dc8-8d02-079409275e78", "18dbf76e-4b08-4247-9451-06dd01d50a3c"],  # necklabel.jpg + script-logo
    "mocha": ["02e95ddd-e359-4a62-a941-71fac89ed20a", "20b8df67-28ef-4573-b678-2e2da7cd3759", "55caff72-82fe-4f91-9b96-e2185fde5641"],
    "antracite": ["31a727e2-62d2-4c9d-a63a-a0d53e6c2372", "e476e5bf-9c42-4d22-9645-e572c44a1ffd", "c5e5fce7-bc65-4c6a-997d-4e2ed9d6c1c4"],
    "nobile": ["1b62527d-d857-4a1c-91e3-8f5899a41e99", "647b6ea6-c23b-4fa4-995e-98e483d1a55d", "dfca0fc8-5302-4b47-a91c-8fc60900a569"],
    "loafer_grigio": ["9de16713-eb94-436b-9edc-61e3796a7f77", "5b91dba6-b39f-42ab-9902-aae2893534d7"],  # zijkant, paar
    "antracite_pietra": ["296c2189-329b-4529-bcef-6552fc227b42", "e9385bb6-6e75-4591-918a-3211ecbb15f8"],  # set, detail
}
NO_TEXT = ("No text, lettering, numbers, logos, signs, brand names, watermarks or borders anywhere in the picture, except "
           "where this prompt names the ModernoMilano neck label.")
HANDS = "Any hands in the picture are his: bare wrists, no watch, no ring, no bracelet."
LENS_ATELIER = "Full-frame digital camera, 100mm macro lens at f/4, soft daylight from one tall north window on the left."
LENS_CITY = "Full-frame digital camera, 35mm lens at f/5.6."
PRESET_DECLINE = "24bae836-2c4a-48e0-89b6-49fcc0b21612"


def shot(sid):
    for s in PLAN["new_shots"]:
        if s["id"] == sid:
            return s
    raise SystemExit(f"onbekend shot {sid}")


# Referenties per shot (controle 12 okt): een macro van stof krijgt hooguit één productfoto, anders tekent het model er
# kledingstukken in. Alleen shots waarin hij als persoon staat (hoofd, nek, rug) krijgen de element-placeholder; bij een
# losse hand zou de placeholder een gezicht kunnen oproepen (les uit de 100-batch van 7 okt).
BORDEAUX_CREMA = ["60115df4-d231-4f40-8e92-13f60ec8adc6", "2532e56d-a5c5-4d95-9a41-db66c744e4e4",
                  "f04007da-5064-4880-a95f-3817eeb7622e", "3115facd-f68d-4eae-b2f3-848b097f9bfc"]  # flat, detail, front, reversed
SHOT_REFS = {
    "V01": REFS["antracite_pietra"] + REFS["loafer_grigio"][:1],      # hij van achteren in de Galleria
    "V02": [REFS["mocha"][1], REFS["antracite_pietra"][1], BORDEAUX_CREMA[0]],  # de stapel: drie kleurfoto's
    "V03": [REFS["antracite_pietra"][1]], "V04": [REFS["antracite_pietra"][1]], "V05": [REFS["antracite_pietra"][1]],
    "V06": [REFS["antracite_pietra"][1]], "V07": [REFS["antracite_pietra"][1]], "V11": [REFS["antracite_pietra"][1]],
    "V08": [BORDEAUX_CREMA[0], BORDEAUX_CREMA[2], BORDEAUX_CREMA[3]],   # beide kanten
    "V09": REFS["label"] + [REFS["mocha"][1]], "S04": REFS["label"] + [REFS["mocha"][1]],
    "V10": [REFS["mocha"][1]], "V12": REFS["antracite_pietra"],
    "S01": [REFS["antracite_pietra"][1]], "S02": [REFS["antracite_pietra"][1]], "S03": [], "S05": [],
}
PERSON = {"V01", "V10", "V12"}  # zijn hoofd, nek of rug in beeld: placeholder + keep_en


def sid(s):
    return s["id"].split()[0]


def refs_for(s):
    return SHOT_REFS.get(sid(s), [])[:4]


def has_model(s):
    return sid(s) in PERSON


def image_request(s):
    prompt = s["start_image_prompt_en"]
    if has_model(s):
        # de placeholder brengt zijn gezicht; nooit zijn gezicht opnieuw beschrijven (SKILL.md)
        prompt = prompt.replace("The model", EL, 1).replace("the model", EL, 1) if "he model" in prompt else f"{EL}: {prompt}"
        prompt += " " + P["keep_en"]
    else:
        prompt = prompt.replace("The model's", "His").replace("the model's", "his").replace("The model", "He").replace("the model", "he")
        prompt += (" The hand in the picture is a man's hand with light warm skin and a faint natural texture. Only his hand "
                   "is in the picture: no face, no second person.")
    parts = [prompt, HANDS, NO_TEXT, P["realism_en"]]
    medias = [{"value": v, "role": "image_references"} for v in refs_for(s)]
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(parts), "medias": medias}


def video_request(s, start, draft=True, draft_job=None):
    face = has_model(s)  # ook van achteren: de gezichtsfoto's dragen zijn haar en nek (ref-4 is driekwart)
    who = ("He is the man in the start frame and in the reference images; use the reference images only for his face and "
           "hair. He keeps the same face, hair and clothes throughout. " if face else "")
    prompt = (f"{s['motion_prompt_en']} Small, natural movement, nothing else moves. {who}{HANDS} {NO_TEXT} Real-time motion "
              "with natural motion blur, one continuous take.")
    medias = [{"role": "start_image", "value": start}]
    if face:
        medias += [{"role": "image_references", "value": f} for f in FACES]
    req = {"model": "seedance_2_5", "mode": "omni_reference", "resolution": "480p" if draft else "1080p", "draft": draft,
           "bitrate_mode": "high", "duration": 4, "aspect_ratio": "9:16", "generate_audio": False, "prompt": prompt,
           "medias": medias, "declined_preset_id": PRESET_DECLINE}
    if not draft:
        req["draft_job_id"] = draft_job
    return req


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "list":
        out = [{"id": s["id"], "kind": s.get("kind", "video"), "refs": refs_for(s), "model": has_model(s)} for s in PLAN["new_shots"]]
    elif cmd == "images":
        half = int(args[args.index("--half") + 1]) if "--half" in args else None
        rest = [a for a in args if a != "--half" and (half is None or a != str(half))]
        ids = rest or [s["id"] for s in PLAN["new_shots"]]
        if half:  # een batch mag 12 aanvragen hebben: 6 shots x 2 varianten
            ids = ids[(half - 1) * 6:half * 6]
        out = [{"index": 2 * n + v, "params": image_request(shot(i))} for n, i in enumerate(ids) for v in range(2)]
    elif cmd == "draft":
        if shot(args[0]).get("kind") == "still":
            raise SystemExit(f"{args[0]} is een levend stilbeeld: geen video, de zoom komt in de montage")
        out = video_request(shot(args[0]), args[1])
    elif cmd == "final":
        out = video_request(shot(args[0]), args[1], draft=False, draft_job=args[2])
    else:
        raise SystemExit(__doc__)
    print(json.dumps(out, ensure_ascii=False))
