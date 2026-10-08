"""Reel 1 "One gilet. Two looks." (Milano Reverso Set Bordeaux & Crema), proef van 8 okt 2026.

Gebruik:
  python3 -I reel1.py still <id...>            -> requests (JSON) voor generate_image_batch
  python3 -I reel1.py reverse <job A>          -> request voor startbeeld B (zelfde foto, gilet omgekeerd)
  python3 -I reel1.py draft <A|B> <start_job>  -> params voor generate_video (Seedance 2.5, concept 480p)
  python3 -I reel1.py final <A|B> <start_job> <draft_job> -> params om dat concept af te maken in 1080p

Stills: A1/A2 (startbeeld, bordeaux kant buiten), B (dezelfde foto, gilet omgekeerd, via reverse),
MAC (macro van de kraag) en FLAT (flat-lay). Zie PLAN.md voor de montage.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MODEL = json.load(open(os.path.join(ROOT, "creative-engine", "data", "model.json")))
P, HF = MODEL["prompt"], MODEL["higgsfield"]
EL = HF["element_placeholder"]

# Productfoto's van MILANO REVERSO SET BORDEAUX & CREMA (higgsfield-media.json).
FLAT, DETAIL, FRONT, REVERSED = ("60115df4-d231-4f40-8e92-13f60ec8adc6", "2532e56d-a5c5-4d95-9a41-db66c744e4e4",
                                 "f04007da-5064-4880-a95f-3817eeb7622e", "3115facd-f68d-4eae-b2f3-848b097f9bfc")

ID_LINE = ("He is in his mid-twenties, with only a faint stubble shadow (never dense stubble or a beard), dark warm brown eyes "
           "(never blue or grey) and warm chestnut-brown hair (not espresso, not near-black), full and swept back with soft natural "
           "volume, the sides combed back over the tops of his ears; no fringe falling forward, no fade, no shaved sides, no pompadour.")
HANDS = "His hands and wrists are bare: no watch, no ring, no bracelet, no glasses, no bag."
NOTEXT = "No text, no logos, no badges, no film borders, no frame."
# realism_en noemt breisel; deze set is glad technisch weefsel met een katoenen tee.
REAL = P["realism_en"].replace("The clothes are real fabric with visible knit stitch and soft creases at the elbows and waist.",
                               "The clothes are real fabric with soft natural creases at the waist and where the gilet folds.")
STILL_REAL = ("An unretouched photograph of real fabric with soft natural creases and fine surface texture; real optics, shallow "
              "depth of field, slight lens softness at the edges.")

GILET = ("a lightweight, unpadded, fully reversible sleeveless gilet in a smooth matte technical fabric with a soft peached surface "
         "(no quilting, no puffiness): one side deep bordeaux (a dark wine red), the other side cream; a stand collar, a full-length "
         "silver zip, two slanted side pockets and an elasticated hem")
SET = ("MILANO REVERSO SET BORDEAUX & CREMA, three pieces:\n"
       f"- {GILET[0].upper() + GILET[1:]}.\n"
       "- A plain cream crew-neck T-shirt in smooth mercerised cotton with a subtle sheen, short sleeves, no print.\n"
       "- Deep bordeaux trousers in the same smooth matte fabric as the gilet: an elasticated waistband with belt loops, slanted side "
       "pockets, a slim tapered leg.")

COURTYARD = ("A quiet morning in an old stone courtyard in Brera, Milan: ochre plaster walls, a colonnade of grey stone arches, "
             "a few potted lemon trees. Nobody else is in the courtyard.")
LIGHT = ("Soft open daylight from the courtyard on his left falls on his face and the front of the gilet; the arcade behind him is a "
         "stop darker and out of focus; muted warm colour, lifted blacks, soft contrast; no HDR.")

S = {
    "A1": dict(
        scene=(f"{COURTYARD} {EL} stands just inside the shade of a stone arch, his body turned three-quarters to the camera, his right "
               "hand in his trouser pocket, looking out into the courtyard past the camera on his left. Framed vertically from just "
               "above his head to mid-thigh, off-centre to the right, the edge of the stone arch soft in the foreground on the left."),
        worn=("The gilet with the BORDEAUX side out, zipped halfway up the chest, so the cream T-shirt shows above the zip and the cream "
              "inside of the gilet shows along the open edges of the zip and inside the stand collar; the bordeaux trousers."),
        refs=[FRONT, FLAT, DETAIL]),
    "A2": dict(
        scene=(f"{COURTYARD} {EL} leans one shoulder lightly against a stone column of the colonnade, seen from his right side in "
               "three-quarter view, his left hand in his trouser pocket, looking down the arcade away from the camera. Framed "
               "vertically from just above his head to mid-thigh, off-centre to the left, the soft curve of the next column in the "
               "foreground on the right."),
        worn=("The gilet with the BORDEAUX side out, zipped halfway up the chest, so the cream T-shirt shows above the zip and the cream "
              "inside of the gilet shows along the open edges of the zip and inside the stand collar; the bordeaux trousers."),
        refs=[FRONT, FLAT, DETAIL]),
}


def person(i):
    s = S[i]
    parts = [s["scene"], LIGHT, f"Expression: {P['expression_en']}.", P["keep_en"], ID_LINE,
             "He wears only these ModernoMilano pieces, reproduced exactly as in the product reference images:\n" + SET,
             f"How they are worn: {s['worn']}",
             f"{HANDS} His feet are not in the picture. He is the only person in the picture.",
             REAL, "Full-frame digital camera, 50mm lens at f/2."]
    medias = [{"value": v, "role": "image_references"} for v in s["refs"]]
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(parts), "medias": medias}


def reversed_take(job_a):
    """Dezelfde foto als A, met het gilet binnenstebuiten: de crème kant buiten (productfoto 'reversed')."""
    parts = [
        f"The same photograph as reference image #1, a moment later: the same man ({EL}), the same courtyard, the same pose, light, "
        "lens and framing. Only one thing changes: he now wears the gilet REVERSED, with the CREAM side out, exactly as in reference "
        "image #2. The bordeaux side is now the inside: it shows only inside the stand collar and along the open front edges. "
        "The gilet is open or zipped exactly as far as in reference image #1, over the same cream T-shirt; the bordeaux trousers stay "
        "exactly the same.",
        P["keep_en"], ID_LINE,
        "The pieces are these ModernoMilano pieces, reproduced exactly as in the reference images:\n" + SET,
        f"{HANDS} His feet are not in the picture. He is the only person in the picture.",
        REAL, "Full-frame digital camera, 50mm lens at f/2."]
    medias = [{"value": job_a, "role": "image_references"}, {"value": REVERSED, "role": "image_references"},
              {"value": DETAIL, "role": "image_references"}]
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(parts), "medias": medias}


def mac():
    # Ronde 1 (8 okt): zonder uitsnede verzon het model een ronde naad naast de rits en een platte zoom. Nu alleen de kraag.
    parts = [
        "A close-up still life, seen from slightly above: the top of the gilet lies flat on a cream linen sheet on an old oak "
        "table near a window, front facing up. The frame shows only the stand collar and the top 20 centimetres of the silver "
        "zip: the zip is open at the top and the stand collar falls open so its cream inside faces the camera, next to the deep "
        "bordeaux outside. Slightly rumpled, not pressed.",
        "Soft window light from the left rakes across the fabric and shows its fine peached surface; shallow depth of field; "
        "muted warm colour, soft contrast.",
        "The only clothing in the picture is this ModernoMilano piece, reproduced exactly as in the product reference images "
        "(reference image #1 shows this exact detail): " + GILET + ".",
        "The front of the gilet is one smooth panel on each side of the zip: no extra seams, panels, piping or pockets near the "
        "zip. The collar is a plain stand collar with the same fabric on both sides, bordeaux outside and cream inside.",
        "There are no people and no hands in the picture.", STILL_REAL, "100mm macro lens at f/4.", NOTEXT]
    return {"model": "nano_banana_pro", "resolution": "2k", "aspect_ratio": "9:16", "prompt": "\n\n".join(parts),
            "medias": [{"value": DETAIL, "role": "image_references"}, {"value": FLAT, "role": "image_references"}]}


def flat():
    parts = [
        "An overhead flat-lay on a pale oak herringbone floor in morning window light, with the soft shadows of the window bars "
        "falling across it. The three pieces are laid out loosely, slightly rumpled, not pressed: the gilet with the bordeaux side "
        "up and the zip half open so the cream inside shows at the collar; the cream T-shirt half under it, one sleeve falling "
        "loose; the bordeaux trousers folded once below them. Some bare floor shows around the pieces.",
        "One light source: the window at the top of the frame; muted warm colour, soft contrast.",
        "The only clothing in the picture is these ModernoMilano pieces, reproduced exactly as in the product reference images:\n" + SET,
        "There are no people and no hands in the picture.", STILL_REAL, "35mm lens at f/5.6, shot straight down.", NOTEXT]
    return {"model": "nano_banana_pro", "resolution": "2k", "aspect_ratio": "9:16", "prompt": "\n\n".join(parts),
            "medias": [{"value": FLAT, "role": "image_references"}, {"value": DETAIL, "role": "image_references"}]}


# ---------- Video (Seedance 2.5, model.json rules.video) ----------
MOTION = {
    # Startbeelden A2 en B: hij leunt met een schouder tegen een zuil, beide handen in de broekzakken.
    "A": ("He keeps leaning lightly with his shoulder against the stone column, both hands in his trouser pockets. He takes a "
          "slow breath, lifts his gaze from the arcade floor and turns his head a little further towards the courtyard, then "
          "settles. The open front of the gilet moves slightly as he breathes. The camera, handheld, drifts a few centimetres closer."),
    "B": ("He keeps leaning lightly with his shoulder against the stone column, both hands in his trouser pockets. He shifts his "
          "weight a little, raises his eyes towards the arches across the courtyard and holds them there. The camera, handheld, "
          "holds still with a faint natural sway."),
}


def video(clip, start_job):
    faces = [r["upscale_job_id"] for r in HF["face_refs"] if any(r["file"].endswith(f"/{x}.jpg") for x in HF["video_face_refs"])]
    prompt = (f"{MOTION[clip]} Small, natural movement. He is the man in the start frame and in the reference images; use the "
              "reference images only for his face and hair. Keep exactly the same man, with the same face, hair and clothes: the "
              "gilet keeps the same side out for the whole shot and nothing about the clothes changes. No head turn of more than 45 "
              "degrees, nothing passes in front of his face. No new objects, no accessories, no text, no new people. Real-time "
              "motion with natural motion blur, one continuous shot, no cuts, no zoom effects.")
    medias = [{"role": "start_image", "value": start_job}] + [{"role": "image_references", "value": f} for f in faces]
    return {"model": "seedance_2_5", "mode": "omni_reference", "resolution": "480p", "draft": True, "bitrate_mode": "high",
            "duration": 4, "aspect_ratio": "9:16", "generate_audio": False, "prompt": prompt, "medias": medias}


def final(clip, start_job, draft_job):
    """Hetzelfde verzoek als het concept, nu in 1080p met draft_job_id (eerst get_cost; boven 50 credits toestemming)."""
    p = video(clip, start_job)
    p.update(resolution="1080p", draft=False, draft_job_id=draft_job)
    return p


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "still":
        build = {"MAC": mac, "FLAT": flat}
        out = [{"index": n, "params": (build[i]() if i in build else person(i))} for n, i in enumerate(args)]
    elif cmd == "reverse":
        out = reversed_take(args[0])
    elif cmd == "draft":
        out = video(args[0], args[1])
    elif cmd == "final":
        out = final(args[0], args[1], args[2])
    else:
        raise SystemExit(__doc__)
    print(json.dumps(out, ensure_ascii=False, indent=1))
