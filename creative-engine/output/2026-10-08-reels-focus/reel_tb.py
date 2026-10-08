"""Reel "Total Bordeaux": één snede, geen tekst, logo de laatste 2 seconden (wens van de eigenaar, 8 okt 2026).

Hetzelfde als de proefreel (binnenplaats in Brera, zelfde pose en camerabeweging), maar in de MILANO REVERSO SET TOTAL
BORDEAUX en met maar één snede: shot A met het gilet bordeaux buiten, dan een snede op de beweging naar shot B, waarin hij
precies verder gaat waar A eindigt, met het gilet omgekeerd (crème buiten).

Gebruik:
  python3 -I reel_tb.py startA                     -> requests voor generate_image_batch (2 varianten van startbeeld A)
  python3 -I reel_tb.py startB <media laatste frame A>  -> request voor startbeeld B (zelfde frame, gilet omgekeerd)
  python3 -I reel_tb.py draft <A|B> <start>        -> Seedance 2.5, concept 480p, 5 s
  python3 -I reel_tb.py final <A|B> <start> <draft_job>  -> afmaken in 1080p
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MODEL = json.load(open(os.path.join(ROOT, "creative-engine", "data", "model.json")))
P, HF = MODEL["prompt"], MODEL["higgsfield"]
EL = HF["element_placeholder"]

# Productfoto's van MILANO REVERSO SET TOTAL BORDEAUX (higgsfield-media.json).
FLAT, DETAIL, FRONT, REVERSED = ("fe534f99-7f8e-4d67-a6f3-8738c71de906", "58b7b005-71e8-4fce-85c1-34bfadc3eca4",
                                 "132e8e87-bd19-416e-b097-6775262996e7", "597a8547-9c1f-4a93-846c-e33f35707ca4")
# Goedgekeurd startbeeld A2 van de proefreel (Bordeaux & Crema): zelfde man, plek, pose en licht; alleen de tee wordt bordeaux.
A2 = "152dd083-0cc3-4090-8a01-32f57da326dc"
PRESET_DECLINE = "24bae836-2c4a-48e0-89b6-49fcc0b21612"

ID_LINE = ("He is in his mid-twenties, with only a faint stubble shadow (never dense stubble or a beard), dark warm brown eyes "
           "(never blue or grey) and warm chestnut-brown hair (not espresso, not near-black), full and swept back with soft natural "
           "volume, the sides combed back over the tops of his ears; no fringe falling forward, no fade, no shaved sides, no pompadour.")
HANDS = "His hands and wrists are bare: no watch, no ring, no bracelet, no glasses, no bag."
REAL = P["realism_en"].replace("The clothes are real fabric with visible knit stitch and soft creases at the elbows and waist.",
                               "The clothes are real fabric with soft natural creases at the waist and where the gilet folds.")
SET = ("MILANO REVERSO SET TOTAL BORDEAUX, three pieces:\n"
       "- A lightweight, unpadded, fully reversible sleeveless gilet in a smooth matte technical fabric with a soft peached surface "
       "(no quilting, no puffiness): one side deep bordeaux (a dark wine red), the other side cream; a stand collar, a full-length "
       "silver zip, two slanted side pockets and an elasticated hem.\n"
       "- A plain deep bordeaux crew-neck T-shirt in smooth mercerised cotton with a subtle sheen, short sleeves, no print, the same "
       "bordeaux as the trousers.\n"
       "- Deep bordeaux trousers in the same smooth matte fabric as the gilet: an elasticated waistband with belt loops, slanted side "
       "pockets, a slim tapered leg.")
# Ronde 2 en 3 (8 okt): een crème bies of band bij de armsgaten las als een streep of mouwnaad. De eigenaar: crème alleen
# binnen in de kraag (en langs de open voorkant), NIET bij de armen, en toch duidelijk een bodywarmer. Dus: diepe armsgaten
# binnen het schouderpunt, de schouder en mouw van de tee zichtbaar, schaduw en stofverschil in plaats van kleur.
SLEEVELESS = ("The gilet is a SLEEVELESS bodywarmer, cut like the gilet in reference image #2. Its armholes are finished in "
              "bordeaux, the same colour as its outside, exactly like the armhole edge in reference image #3: no cream shows at "
              "the armholes at all. Cream shows only inside the stand collar and along the open front edges. It still reads "
              "unmistakably as a sleeveless bodywarmer: the armholes are cut deep and sit clearly inward of his shoulder points, "
              "so on both sides the T-shirt's shoulder seam and the top of its short sleeve are plainly visible outside the "
              "gilet, with a soft shadow line where the gilet's armhole edge lies over the T-shirt. The gilet is a matte, "
              "peached, slightly thicker fabric that stands a little away from the body at the armhole; the T-shirt is a thinner "
              "jersey with a subtle sheen, so the two layers are easy to tell apart. The T-shirt sleeve ends in its own hemmed "
              "edge on the upper arm. The gilet's two slanted welt pockets sit on its lower front panels.")
TAIL = [P["keep_en"], ID_LINE, "The pieces are these ModernoMilano pieces, reproduced exactly as in the reference images:\n" + SET,
        f"{HANDS} His feet are not in the picture. He is the only person in the picture.", REAL,
        "Full-frame digital camera, 50mm lens at f/2."]


def start_a():
    parts = [
        f"The same photograph as reference image #1: the same man ({EL}), the same courtyard, the same pose, light, lens and framing. "
        "Only one thing changes: his crew-neck T-shirt is now deep bordeaux, the same bordeaux as his trousers and the outside of "
        "the gilet, exactly as in reference image #2, so the whole outfit is bordeaux. The gilet hangs open as in reference "
        "image #1, bordeaux side out, cream inside the stand collar and along the open front edges.",
        # Ronde 1 (8 okt): met een tee in dezelfde kleur liep het armsgat over in de mouw en leek het gilet een jasje met korte
        # mouwen. Het gilet is mouwloos; de crème binnenkant geeft een smalle rand langs de armsgaten (zie de flat-lay).
        SLEEVELESS] + TAIL
    medias = [{"value": A2, "role": "image_references"}, {"value": FRONT, "role": "image_references"},
              {"value": DETAIL, "role": "image_references"}]
    req = {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(parts), "medias": medias}
    return [{"index": 0, "params": req}, {"index": 1, "params": dict(req)}]


def start_b(last_frame):
    parts = [
        f"The same photograph as reference image #1: the same man ({EL}), the same courtyard, the same pose, the same direction of "
        "his head and eyes, the same light, lens and framing. Only one thing changes: he now wears the gilet REVERSED, with the "
        "CREAM side out, exactly as in reference image #2. The bordeaux side is now the inside: it shows only inside the stand "
        "collar and along the open front edges. The gilet is open exactly as far as in reference image #1, over the same deep "
        "bordeaux T-shirt; the bordeaux trousers stay exactly the same.", "The gilet is clearly a sleeveless bodywarmer: its armholes are finished in cream like the rest of the outside, "
        "with no bordeaux at the armholes; bordeaux shows only inside the stand collar and along the open front edges. The "
        "short sleeves of the bordeaux T-shirt come out from under the armholes."] + TAIL
    medias = [{"value": last_frame, "role": "image_references"}, {"value": REVERSED, "role": "image_references"},
              {"value": DETAIL, "role": "image_references"}]
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(parts), "medias": medias}


# ---------- Video (Seedance 2.5, model.json rules.video; lessen van de proefreel in README.md) ----------
MOTION = {
    # Zelfde beweging als de goedgekeurde clip A van de proefreel, nu over 5 seconden. Voorcontrole 8 okt: de blik en de
    # camera moeten tot stilstand komen, want het laatste frame wordt het startbeeld van B.
    "A": ("He keeps leaning lightly with his left shoulder against the stone column on the right of the frame, both hands in "
          "his trouser pockets. He takes a slow breath and slowly lifts his chin and eyes from the paving to look out into the "
          "courtyard past the left edge of the frame, then holds that look, calm and still, until the end of the shot. The "
          "open front of the gilet moves slightly as he breathes. The handheld camera drifts a few centimetres closer, then "
          "settles."),
    # B begint waar A eindigt (startbeeld = laatste frame van A, gilet omgekeerd): blik nog omhoog, dan rustig weer omlaag.
    "B": ("He keeps leaning lightly with his left shoulder against the stone column on the right of the frame, both hands in "
          "his trouser pockets. He holds his gaze out over the courtyard for a moment, takes a slow breath, then slowly lowers "
          "his eyes back to the paving and settles against the column, calm and still until the end of the shot. The handheld "
          "camera holds still with a faint natural sway."),
}
SIDE = {"A": "bordeaux outside, cream only inside the collar and along the open front edges",
        "B": "cream outside, bordeaux only inside the collar and along the open front edges"}


def video(clip, start):
    faces = [r["upscale_job_id"] for r in HF["face_refs"] if any(r["file"].endswith(f"/{x}.jpg") for x in HF["video_face_refs"])]
    prompt = (f"{MOTION[clip]} Small, natural movement. He is the man in the start frame and in the reference images; use the "
              "reference images only for his face and hair. He keeps the same face, hair and clothes throughout: the sleeveless "
              f"gilet stays {SIDE[clip]} for the whole shot, over the deep bordeaux T-shirt. His face stays clear, his wrists bare. The "
              "courtyard stays quiet and still around him. Real-time motion with natural motion blur, one continuous handheld take.")
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
