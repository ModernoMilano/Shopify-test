"""Reverso Autumn, versie 2 (23 okt 2026). De eigenaar keurde versie 1 af: "veel te AI, vooral als hij uitblaast", de rits-beweging
klopt niet, aan het einde wegloper met het gilet omgedraaid, in plaats van het uitademen een vertraagde beweging, en het gilet niet
over een reling maar over een stoel bij een Italiaans koffietentje.

Nieuwe opzet (±13 s):
  N1  video 4 s  slow motion, macro: zijn hand trekt de rits van de trui langzaam dicht, gezicht buiten beeld (vervangt S1 + de rits)
  N2  video 4 s  slow motion: aan het kanaal legt hij de kraag van het gilet goed en kijkt het water af (vervangt het uitademen)
  N3  still/video het gilet over een bistrostoel op het terras van een Italiaans koffietentje aan de Navigli, crème kant buiten
  V2  bestaand   van achteren het licht in, gilet crème buiten (job d0da38aa), eindkaart

Regels voor de bewegingsprompts (uit de afkeuring): geen "breathes out", geen geacteerde beats, mond dicht, blik van de camera af,
slow motion voor elke handeling, kleine bewegingen, achtergrond leeft (mist drijft, water rimpelt, voorbijgangers lopen door),
camera handheld-stil of vast, nooit op rails. Geen horloge (merkregel: geen accessoires), dus de "naar zijn horloge kijken"-
beweging is een kraag-en-blik-beweging geworden.

  python3 -I autumn_blu_v2.py images N1a N1b N2a N2b N3a N3b
  python3 -I autumn_blu_v2.py draft <N1|N2|N3> <start_job>
  python3 -I autumn_blu_v2.py final <N1|N2|N3> <start_job> <draft_job>
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autumn_blu import (SET, NO_TEXT, HANDS, REAL, LIGHT, ID_LINE, P, EL, FACES, PRESET_DECLINE, FLAT, MACRO, FRONT, REVERSED)

CAFE = ("the terrace of a small Italian café on the Navigli in Milan: a dark bentwood bistro chair and a small round marble table, "
        "the café's doorway and the misty canal out of focus behind")

SHOTS = {
    "N1": {"person": False, "refs": [MACRO, FRONT],
           "prompt": (f"9:16, 4K close-up at chest height, seen from the front and slightly from his left. {LIGHT} The deep navy "
                      "Milano Mezza Zip knit worn under the open navy reversible gilet, cream showing only inside the gilet's stand "
                      "collar and along its open front edges. The knit's short quarter zip is half open. His right hand, a bare wrist "
                      "with the knit's ribbed cuff just visible, holds the small metal pull of the quarter zip between thumb and "
                      "index finger at mid-chest, about to draw it up. Only the collar, the chest and the hand are in the frame; his "
                      "face is above the top edge of the frame. Fine droplets of mist on the fabric catch the pale light. "
                      "Full-frame digital camera, 100 mm macro, f/4, shallow depth of field.")},
    "N2": {"person": True, "refs": [FRONT, MACRO],
           "prompt": (f"9:16, 4K. {LIGHT} {EL} stands at the stone edge of the canal, seen from his left in a three-quarter view, "
                      "waist-up and off-centre to the right of the frame, the misty water and the far bank behind him. He wears the "
                      "reversible gilet with the deep NAVY side out, hanging open, cream showing only inside the stand collar and "
                      "along the open front edges, over the deep navy Mezza Zip knit, its short quarter zip closed to the top, the "
                      "ribbed mock-neck collar closed at the throat; nothing else shows at his neck. His right hand rests lightly on "
                      "the gilet's open front edge just below the collar, as if about to settle it; his left hand is in his trouser "
                      "pocket. His eyes are down on the water, away from the camera, mouth closed, a quiet unposed moment. "
                      "Full-frame digital camera, 85 mm, f/2. Two or three distant passers-by far along the canal, small and out of "
                      "focus, faces unreadable.")},
    "N3": {"person": False, "refs": [REVERSED, FLAT],
           "prompt": (f"9:16, 4K. {LIGHT} On {CAFE}, the reversible gilet of the set hangs over the back of the bistro chair, the "
                      "CREAM side out and the navy side showing only inside the stand collar and along the open front edges, the "
                      "silver zip open, slightly rumpled as if just taken off, one shoulder hanging lower than the other. The seat of "
                      "the chair is empty and nothing else of the set is in the picture: no knit, no trousers, only the gilet. On the "
                      "marble table an espresso in a small white cup on its saucer, a thread of steam rising in the cold air. Seen "
                      "from slightly above, close, the chair off-centre to the left. Full-frame digital camera, 50 mm, f/2.8. "
                      "Nobody sits at the table; a waiter and a passer-by far in the background, out of focus. No lettering on "
                      "the cup, the café or anywhere.")},
}

MOTION = {
    # Lessen uit de afkeuring (kijkers-workflow wf_2f43d4aa): nooit "breathes out", geen knipperen-en-draaien naar de camera,
    # één fysieke handeling per shot, de camera ademt (handheld), de achtergrond leeft (mist drijft, water rimpelt, mensen lopen
    # echt door), haar en stof bewegen in een briesje, een echte looppas is één stap per ~0,6 s.
    "N1": ("Slow motion at a quarter of real speed. Handheld camera, nearly still, with a slight natural breathing drift. His right "
           "hand draws the small metal pull of the quarter zip slowly upward along the zip, thumb and index finger closed around "
           "the pull the whole way, the zip teeth closing behind the pull as it rises, the knit fabric shifting with the pull, "
           "until the ribbed collar meets at the throat; then the fingers let go and the hand sinks out of the frame. The open "
           "edges of the gilet sway slightly as he moves; behind him the mist drifts over the canal and a far figure walks on. "
           "His face stays above the top edge of the frame. Nothing else happens."),
    "N2": ("Slow motion at a quarter of real speed. Handheld camera, nearly still, with a slight natural breathing drift and a very "
           "slow push-in. One physical thing only: with his right hand he settles the gilet's open front edge, sliding the hand "
           "slowly down the edge from the collar to the chest, while his eyes stay down on the water; his eyes lead a small "
           "turn of the head to follow something on the water, mouth closed the whole time, no blink to the camera, no other "
           "gesture. A light breeze lifts a few strands of his hair and moves the open edges of the gilet. Behind him the mist "
           "drifts over the canal, the water ripples and catches the light, and the distant passers-by keep walking at a real "
           "pace, growing slowly as they come closer."),
    "N3": ("Real-time speed. Handheld camera, nearly still, with a slight natural breathing drift. The thread of steam rises and "
           "curls from the espresso; the mist drifts slowly over the canal behind; the waiter in the far background walks on "
           "and a passer-by crosses far behind, out of focus; the open edges of the gilet stir once in a light breeze. The chair "
           "and the table do not move. Nothing else happens."),
}
SIDE = {"N1": "navy outside, cream only inside the collar and along the open front edges", "N2": "navy outside, cream only inside the collar and along the open front edges",
        "N3": "cream outside, navy only inside the collar and along the open front edges"}


def image_request(sid):
    s = SHOTS[sid]
    parts = [s["prompt"]]
    if s["person"]:
        parts += [P["keep_en"], ID_LINE, P["expression_en"].capitalize() + "."]
    real = REAL if s["person"] else REAL.replace(REAL[REAL.index("Natural healthy skin"):REAL.index("The clothes")], "")
    parts += [SET, HANDS if s["person"] else "His hand and wrist are bare: no watch, no ring, no bracelet.", NO_TEXT, real]
    if sid == "N3":
        parts[-3] = ""
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(p for p in parts if p),
            "medias": [{"value": v, "role": "image_references"} for v in s["refs"]]}


def images(keys):
    return [{"index": i, "sid": k, "params": image_request(k[:2])} for i, k in enumerate(keys)]


def video(clip, start, draft=True, draft_job=None):
    who = ("He is the man in the start frame and in the reference images; use the reference images only for his face and hair. "
           "He keeps the same face, hair and clothes throughout" if SHOTS[clip]["person"] else
           "Everything stays exactly as in the start frame; the clothes keep their shape and colour throughout")
    prompt = (f"{MOTION[clip]} {who}: the sleeveless gilet stays {SIDE[clip]} for the whole shot, over the navy quarter-zip knit. "
              f"{'His wrists bare. ' if clip != 'N3' else ''}{NO_TEXT} Natural motion blur, one continuous take.")
    medias = [{"role": "start_image", "value": start}]
    if SHOTS[clip]["person"]:
        medias += [{"role": "image_references", "value": f} for f in FACES]
    req = {"model": "seedance_2_5", "mode": "omni_reference", "resolution": "480p" if draft else "1080p", "draft": draft,
           "bitrate_mode": "high", "duration": 4, "aspect_ratio": "9:16", "generate_audio": False, "prompt": prompt,
           "medias": medias, "declined_preset_id": PRESET_DECLINE}
    if not draft:
        req["draft_job_id"] = draft_job
    return req


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    out = {"images": lambda: images(args), "draft": lambda: video(args[0], args[1]),
           "final": lambda: video(args[0], args[1], False, args[2])}[cmd]()
    print(json.dumps(out, ensure_ascii=False))
