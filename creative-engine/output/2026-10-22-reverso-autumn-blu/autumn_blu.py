"""Cinematic video "Reverso Autumn" met de MILANO REVERSO AUTUMN SET – TOTAL BLU · QUARTER ZIP (scenario 2, "Het eerste koude
licht", gekozen door de eigenaar op 22 okt 2026). Navigli in de ochtendmist, 13 s:

  S1  levende still  2,5 s  macro van de ribkraag en de rits van de navy Mezza Zip, druppels op de stof
  V1  video          4 s    hij trekt de rits dicht tot aan de hals en kijkt het water over (gilet navy buiten)
  S2  levende still  2,5 s  het gilet over de reling aan het kanaal, crème kant buiten, één blad erop
  V2  video          4 s    van achteren: hij loopt het licht in langs het kanaal, gilet crème buiten; logo + REVERSO AUTUMN de laatste 2 s

Gebruik:
  python3 -I autumn_blu.py images                 -> requests voor generate_image_batch (2 varianten per shot, 8 beelden)
  python3 -I autumn_blu.py draft <V1|V2> <start>  -> Seedance 2.5, concept 480p, 4 s
  python3 -I autumn_blu.py final <V1|V2> <start> <draft_job> -> 1080p
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MODEL = json.load(open(os.path.join(ROOT, "creative-engine", "data", "model.json")))
P, HF = MODEL["prompt"], MODEL["higgsfield"]
EL = HF["element_placeholder"]
FACES = [r["upscale_job_id"] for r in HF["face_refs"] if any(r["file"].endswith(f"/{x}.jpg") for x in HF["video_face_refs"])]
PRESET_DECLINE = "24bae836-2c4a-48e0-89b6-49fcc0b21612"

# Productfoto's van de set (geïmporteerd 22 okt, higgsfield-media.json)
FLAT, MACRO, FRONT, BACK, REVERSED = ("ce23488f-08c8-477d-bf35-f1cee928cef8", "c7a36d73-a64a-4af4-a84d-9484a9ec4767",
                                      "fd656a7d-cc0f-4844-8360-37eb3f5ee697", "fc7f8070-b1e0-4ceb-b131-5cdc03294c97",
                                      "42ddc2fd-9c4d-424f-b981-22d3c28b536e")

SET = ("MILANO REVERSO AUTUMN SET TOTAL BLU, three pieces, reproduced exactly as in the reference images:\n"
       "- A lightweight, unpadded, fully reversible sleeveless gilet in a smooth matte technical fabric with a soft peached surface "
       "(no quilting, no puffiness): one side deep navy, the other side cream; a stand collar, a full-length silver zip, two slanted "
       "side pockets and an elasticated hem. The inner colour shows only inside the stand collar and along the open front edges, "
       "never at the armholes or the hem.\n"
       "- The Milano Mezza Zip: a fine-gauge knit in the same deep navy with a ribbed stand-up mock-neck collar, a short quarter zip "
       "with a small metal pull at the neck, long sleeves with ribbed cuffs and a ribbed hem; no print, no logo.\n"
       "- Deep navy trousers in the same smooth matte fabric as the gilet's navy side: an elasticated waistband with belt loops, "
       "slanted side pockets, a slim tapered leg.")
NO_TEXT = ("No text, lettering, numbers, logos, labels, tags, signs, brand names, watermarks or borders anywhere in the picture; "
           "nothing is printed or sewn on the outside of any garment.")
HANDS = "His hands and wrists are bare: no watch, no ring, no bracelet, no glasses, no bag."
REAL = P["realism_en"].replace("The clothes are real fabric with visible knit stitch and soft creases at the elbows and waist.",
                               "The clothes are real fabric: the knit with a fine visible stitch, the gilet and trousers smooth and matte "
                               "with soft natural creases at the waist and where the gilet folds.")
LIGHT = ("Early morning on the Navigli in Milan, late October: a thin mist over the canal, the pale low sun coming through the mist "
         "from the left as the only light source, soft and cold, the far bank and the houses along the water out of focus and a stop "
         "darker; muted colour, lifted blacks, soft contrast; no HDR, no teal-and-orange grade.")
PUBLIC = P["public_places_en"]
ID_LINE = ("He is in his mid-twenties, with only a faint stubble shadow (never dense stubble or a beard), dark warm brown eyes "
           "(never blue or grey) and warm chestnut-brown hair (not espresso, not near-black), full and swept back with soft natural "
           "volume, the sides combed back over the tops of his ears; no fringe falling forward, no fade, no shaved sides, no pompadour.")

SHOTS = {
    "S1": {"kind": "still", "seconds": 2.5, "zoom": [1.0, 1.04], "refs": [MACRO, FRONT], "person": False,
           "prompt": (f"9:16, 4K macro at chest height, seen from the front. {LIGHT} The ribbed stand-up mock-neck collar of the "
                      "deep navy Milano Mezza Zip, its short quarter zip closed to the top with the small metal pull at the throat, "
                      "worn by a man whose face is above the top edge of the frame: only the collar, the top of the chest and the "
                      "open stand collar of the navy gilet around it, cream showing only inside the gilet's collar. Fine droplets "
                      "of mist sit on the knit and the gilet, catching the pale light. Full-frame digital camera, 100 mm macro, "
                      "f/4, shallow depth of field. Nobody else is in the picture; no face in the picture.")},
    "V1": {"kind": "video", "seconds": 4, "refs": [FRONT, MACRO], "person": True,
           "prompt": (f"9:16, 4K. {LIGHT} {EL} stands at the stone edge of the canal, seen from his left in a three-quarter view, "
                      "waist-up and off-centre to the right of the frame, the misty water and the far bank behind him. He wears the "
                      "reversible gilet with the deep NAVY side out, hanging open, cream showing only inside the stand collar and "
                      "along the open front edges, over the deep navy Mezza Zip knit whose quarter zip is still half open; his "
                      "right hand holds the small metal pull of the quarter zip at his chest, about to draw it up; his left hand "
                      "is in his trouser pocket. His eyes are on the water, away from the camera, mouth closed; a faint breath of "
                      "mist in the cold air. Full-frame digital camera, 85 mm, f/2. Two or three distant passers-by far along the "
                      "canal, small and out of focus, faces unreadable.")},
    "S2": {"kind": "still", "seconds": 2.5, "zoom": [1.0, 1.03], "refs": [REVERSED, FLAT], "person": False,
           "prompt": (f"9:16, 4K. {LIGHT} The reversible gilet of the set laid over the dark iron railing at the edge of the canal, "
                      "seen from slightly above and close, the CREAM side out and the navy side showing only inside the stand "
                      "collar and along the open front edges, the silver zip open; one single yellow autumn leaf has landed on "
                      "the cream fabric. Behind and below, out of focus, the misty water of the canal. Full-frame digital camera, "
                      "50 mm, f/2.8. Nobody is in the picture.")},
    "V2": {"kind": "video", "seconds": 4, "refs": [REVERSED, BACK], "person": True,
           "prompt": (f"9:16, 4K. {LIGHT} {EL} seen from behind, full length but off-centre to the left of the frame, walking away "
                      "from the camera along the stone towpath of the canal towards the pale light, the misty water on his "
                      "right, the houses along the bank out of focus on the left. He now wears the reversible gilet with the "
                      "CREAM side out, navy showing only inside the stand collar, over the deep navy Mezza Zip knit with its "
                      "long sleeves, deep navy trousers, both hands loose at his sides; his back and the back of his head to "
                      "the camera, face not visible. Fallen yellow leaves on the wet stones catch the light. Full-frame digital "
                      "camera, 50 mm, f/2.8. Two or three distant passers-by far ahead along the canal, small and out of focus.")},
}
MOTION = {
    "V1": ("The camera is locked off on a tripod and stays perfectly still. He slowly draws the quarter zip up to his throat with "
           "his right hand, lets the hand drop to his side, breathes out once (a faint breath of mist in the cold air) and keeps "
           "looking out over the water, calm and still, until the end of the shot. Small, natural movement; nothing else moves "
           "except the mist drifting slowly over the canal."),
    "V2": ("The camera is locked off on a tripod and stays perfectly still. He walks slowly and evenly away from the camera "
           "along the towpath, a natural unhurried pace, his back to the camera the whole time, never turning round, until the "
           "end of the shot; the mist drifts slowly over the water. Small, natural movement; nothing else moves."),
}


def image_request(sid):
    s = SHOTS[sid]
    parts = [s["prompt"]]
    if s["person"]:
        parts += [P["keep_en"], ID_LINE, P["expression_en"].capitalize() + "."]
    parts += [SET, HANDS if s["person"] else "", NO_TEXT, REAL]
    medias = [{"value": v, "role": "image_references"} for v in s["refs"]]
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(p for p in parts if p),
            "medias": medias}


def images():
    out, i = [], 0
    for sid in ["S1", "V1", "S2", "V2"]:
        for v in "ab":
            out.append({"index": i, "sid": f"{sid}{v}", "params": image_request(sid)})
            i += 1
    return out


def video(clip, start, draft=True, draft_job=None):
    side = {"V1": "navy outside, cream only inside the collar and along the open front edges",
            "V2": "cream outside, navy only inside the collar"}[clip]
    prompt = (f"{MOTION[clip]} He is the man in the start frame and in the reference images; use the reference images only for "
              f"his face and hair. He keeps the same face, hair and clothes throughout: the sleeveless gilet stays {side} for the "
              f"whole shot, over the navy quarter-zip knit. His wrists bare. {NO_TEXT} Real-time motion with natural motion "
              "blur, one continuous take from the fixed camera.")
    medias = [{"role": "start_image", "value": start}] + [{"role": "image_references", "value": f} for f in FACES]
    req = {"model": "seedance_2_5", "mode": "omni_reference", "resolution": "480p" if draft else "1080p", "draft": draft,
           "bitrate_mode": "high", "duration": 4, "aspect_ratio": "9:16", "generate_audio": False, "prompt": prompt,
           "medias": medias, "declined_preset_id": PRESET_DECLINE}
    if not draft:
        req["draft_job_id"] = draft_job
    return req


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    out = {"images": lambda: images(), "draft": lambda: video(args[0], args[1]),
           "final": lambda: video(args[0], args[1], False, args[2])}[cmd]()
    print(json.dumps(out, ensure_ascii=False))
