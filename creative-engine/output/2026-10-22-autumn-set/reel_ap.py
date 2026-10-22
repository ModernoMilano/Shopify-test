"""Reel "Autumn Set Antracite & Pietra": dezelfde video als Total Bordeaux (8 okt), met de MILANO REVERSO AUTUMN SET
ANTRACITE & PIETRA · QUARTER ZIP (wens van de eigenaar, 22 okt 2026).

Zelfde binnenplaats in Brera, zelfde pose, licht en camerabeweging als het goedgekeurde startbeeld van Total Bordeaux
(Y0, 66db5823). Shot A: het gilet antraciet buiten, over de lichtgrijze Mezza Zip; snede op de beweging naar shot B, waarin
hij verder gaat waar A eindigt, met het gilet omgekeerd (pietra buiten). Geen tekst, alleen het logo de laatste 2 s.

Gebruik:
  python3 -I reel_ap.py startA                          -> requests voor generate_image_batch (2 varianten van startbeeld A)
  python3 -I reel_ap.py startB <media laatste frame A>  -> request voor startbeeld B (zelfde frame, gilet omgekeerd)
  python3 -I reel_ap.py draft <A|B> <start>             -> Seedance 2.5, concept 480p, 5 s
  python3 -I reel_ap.py final <A|B> <start> <draft_job> -> afmaken in 1080p
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MODEL = json.load(open(os.path.join(ROOT, "creative-engine", "data", "model.json")))
P, HF = MODEL["prompt"], MODEL["higgsfield"]
EL = HF["element_placeholder"]

# Productfoto's van MILANO REVERSO AUTUMN SET – ANTRACITE & PIETRA · QUARTER ZIP (geïmporteerd 22 okt, higgsfield-media.json).
FLAT, MACRO, FRONT, BACK, REVERSED = ("7fc22639-b017-4f6c-98be-cfc86c97617e", "ea50c54f-0f1a-483d-8587-fada31aaf697",
                                      "8762fe28-b46e-4e0b-a7e0-da2f25367718", "74d2f154-841b-470b-af28-dd10e26e0ea5",
                                      "f568e105-1876-45f9-bd2f-0933f215bc1a")
# Goedgekeurd startbeeld A van Total Bordeaux (Y0, ronde 4, "perfect zo"): zelfde man, plek, pose, licht en kader.
Y0 = "66db5823-11ca-4cb1-a1dc-b23e82aff434"
PRESET_DECLINE = "24bae836-2c4a-48e0-89b6-49fcc0b21612"

ID_LINE = ("He is in his mid-twenties, with only a faint stubble shadow (never dense stubble or a beard), dark warm brown eyes "
           "(never blue or grey) and warm chestnut-brown hair (not espresso, not near-black), full and swept back with soft natural "
           "volume, the sides combed back over the tops of his ears; no fringe falling forward, no fade, no shaved sides, no pompadour.")
HANDS = "His hands and wrists are bare: no watch, no ring, no bracelet, no glasses, no bag."
REAL = P["realism_en"].replace("The clothes are real fabric with visible knit stitch and soft creases at the elbows and waist.",
                               "The clothes are real fabric: the knit with a fine visible stitch, the gilet and trousers smooth and matte "
                               "with soft natural creases at the waist and where the gilet folds.")
SET = ("MILANO REVERSO AUTUMN SET ANTRACITE & PIETRA, three pieces:\n"
       "- A lightweight, unpadded, fully reversible sleeveless gilet in a smooth matte technical fabric with a soft peached surface "
       "(no quilting, no puffiness): one side anthracite (a deep charcoal grey), the other side pietra (a pale warm stone, almost "
       "off-white); a stand collar, a full-length silver zip, two slanted side pockets and an elasticated hem.\n"
       "- The Milano Mezza Zip: a fine-gauge knit in light grey melange with a ribbed stand-up mock-neck collar, a short quarter zip "
       "with a small metal pull at the neck, long sleeves with ribbed cuffs and a ribbed hem; no print, no logo.\n"
       "- Anthracite trousers in the same smooth matte charcoal fabric as the gilet's outside: an elasticated waistband with belt "
       "loops, slanted side pockets, a slim tapered leg.")
# Les van Total Bordeaux (8 okt): de binnenkleur alleen binnen in de kraag en langs de open voorkant, NIET bij de armsgaten.
# Hier is het makkelijker dan bordeaux op bordeaux: de lange lichtgrijze mouwen van de trui komen uit de armsgaten.
SLEEVELESS = ("The gilet is a SLEEVELESS bodywarmer, cut exactly like the gilet in reference image #2. Its armholes are finished "
              "in the same colour as its outside, exactly like the armhole edge in reference image #2: no inner colour shows at the "
              "armholes at all. The inner colour shows only inside the stand collar and along the open front edges. The long light "
              "grey knit sleeves of the Mezza Zip come out from under the armholes, so the gilet reads unmistakably as a sleeveless "
              "bodywarmer over a long-sleeved knit. The gilet's two slanted welt pockets sit on its lower front panels. Above the "
              "gilet's open collar the ribbed light grey mock-neck collar of the knit is visible, with its short quarter zip closed "
              "to the top and its small metal pull at the throat.")
TAIL = [P["keep_en"], ID_LINE, "The pieces are these ModernoMilano pieces, reproduced exactly as in the reference images:\n" + SET,
        f"{HANDS} His feet are not in the picture. He is the only person in the picture.", REAL,
        "Full-frame digital camera, 50mm lens at f/2."]


def start_a():
    parts = [
        f"The same photograph as reference image #1: the same man ({EL}), the same courtyard, the same pose, light, lens and framing. "
        "Only his clothes change: he now wears the ModernoMilano Autumn Set exactly as in reference image #2: the reversible gilet "
        "with the ANTHRACITE side out, hanging open as far as in reference image #1, pale stone (pietra) showing only inside the "
        "stand collar and along the open front edges; under it the light grey melange Mezza Zip knit with its ribbed mock-neck "
        "collar and closed quarter zip; anthracite trousers in the same matte charcoal as the gilet. The knit hangs loose over "
        "the trousers so no waistband is visible.",
        SLEEVELESS] + TAIL
    medias = [{"value": Y0, "role": "image_references"}, {"value": FRONT, "role": "image_references"},
              {"value": MACRO, "role": "image_references"}]
    req = {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(parts), "medias": medias}
    return [{"index": 0, "params": req}, {"index": 1, "params": dict(req)}]


def start_b(last_frame):
    parts = [
        f"The same photograph as reference image #1: the same man ({EL}), the same courtyard, the same pose, the same direction of "
        "his head and eyes, the same light, lens and framing. Only one thing changes: he now wears the gilet REVERSED, with the "
        "pale stone PIETRA side out, exactly as in reference image #2. The anthracite side is now the inside: it shows only inside "
        "the stand collar and along the open front edges. The gilet is open exactly as far as in reference image #1, over the same "
        "light grey melange Mezza Zip knit with its ribbed mock-neck collar and closed quarter zip; the anthracite trousers stay "
        "exactly the same.",
        "The knit hangs loose over the trousers exactly as in reference image #1, at exactly the same length: its ribbed hem fully "
        "covers the waistband of the trousers, so no waistband is visible. Everything except the gilet is identical to reference "
        "image #1.",
        "The gilet is clearly a sleeveless bodywarmer: its armholes are finished in pietra like the rest of the outside, with no "
        "anthracite at the armholes; anthracite shows only inside the stand collar and along the open front edges. The long light "
        "grey sleeves of the knit come out from under the armholes."] + TAIL
    medias = [{"value": last_frame, "role": "image_references"}, {"value": REVERSED, "role": "image_references"}]
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(parts), "medias": medias}


# ---------- Video (Seedance 2.5): dezelfde bewegingen als Total Bordeaux (lessen in 2026-10-08-reels-focus/README.md) ----------
MOTION = {
    "A": ("He keeps leaning lightly with his left shoulder against the stone column on the right of the frame, both hands in "
          "his trouser pockets. He takes a slow breath and slowly lifts his chin and eyes from the paving to look out into the "
          "courtyard past the left edge of the frame, then holds that look, calm and still, until the end of the shot. The "
          "open front of the gilet moves slightly as he breathes. The handheld camera drifts a few centimetres closer, then "
          "settles."),
    "B": ("The shot opens exactly on the start frame, with the same framing, background, head angle and closed lips. The "
          "camera is locked off on a tripod and stays perfectly still for the whole shot. He keeps leaning lightly with his "
          "left shoulder against the stone column on the right of the frame, both hands in his trouser pockets, his gaze out "
          "over the courtyard past the left edge of the frame. With a slow breath he gently lowers his chin and eyes a little "
          "to the paving ahead of him on the left, his face still turned to the left, and by the third second he has settled "
          "against the column; for the last two seconds he stays calm and still, only breathing softly."),
}
TAKE = {"A": "one continuous handheld take.", "B": "one continuous take from the fixed camera."}
KNIT = {"A": "over the light grey quarter-zip knit with its ribbed mock-neck collar.",
        "B": "over the light grey quarter-zip knit, which hangs loose at the same length throughout."}
SIDE = {"A": "anthracite outside, pale stone only inside the collar and along the open front edges",
        "B": "pale stone outside, anthracite only inside the collar and along the open front edges"}


def video(clip, start):
    faces = [r["upscale_job_id"] for r in HF["face_refs"] if any(r["file"].endswith(f"/{x}.jpg") for x in HF["video_face_refs"])]
    prompt = (f"{MOTION[clip]} Small, natural movement. He is the man in the start frame and in the reference images; use the "
              "reference images only for his face and hair. He keeps the same face, hair and clothes throughout: the sleeveless "
              f"gilet stays {SIDE[clip]} for the whole shot, {KNIT[clip]} His face stays clear, his wrists bare. The "
              "courtyard stays quiet and still around him. No text, lettering, logos or labels anywhere; nothing is printed or "
              "sewn on the outside of any garment. Real-time motion with natural motion blur, " + TAKE[clip])
    medias = [{"role": "start_image", "value": start}] + [{"role": "image_references", "value": f} for f in faces]
    return {"model": "seedance_2_5", "mode": "omni_reference", "resolution": "480p", "draft": True, "bitrate_mode": "high",
            "duration": 5, "aspect_ratio": "9:16", "generate_audio": False, "prompt": prompt, "medias": medias,
            "declined_preset_id": PRESET_DECLINE}


def final(clip, start, draft_job):
    p = video(clip, start)
    p.update(resolution="1080p", draft=False, draft_job_id=draft_job)
    return p


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    out = {"startA": lambda: start_a(), "startB": lambda: start_b(args[0]), "draft": lambda: video(args[0], args[1]),
           "final": lambda: final(args[0], args[1], args[2])}[cmd]()
    print(json.dumps(out, ensure_ascii=False))
