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

from autumn_blu import (SET, NO_TEXT, HANDS, REAL, LIGHT, ID_LINE, P, EL, FACES, PRESET_DECLINE, FLAT, MACRO, FRONT, BACK, REVERSED)

LOAFER = "85b7e720-20a8-498c-8992-148b082d584e"  # MILANO SUEDE LOAFER - NAVY, higgsfield-media.json (geïmporteerd 23 okt)
LOAFER_LINE = ("- Milano suede loafers in deep navy, a classic unlined slip-on with an apron toe and a low heel, worn without socks: "
               "a mirrored left and right pair, bare ankles.")
CAFE = ("the terrace of a small Italian café on the Navigli in Milan: a dark bentwood bistro chair and a small round marble table, "
        "the café's doorway and the misty canal out of focus behind")

SHOTS = {
    "N1": {"person": False, "refs": [MACRO, FRONT],
           # N1a had een navy T-shirt onder de trui, N1b een navy onderlaag, glitterdruppels en een navy rits: ronde 2 zonder druppels.
           "prompt": (f"9:16, 4K close-up at chest height, seen from the front and slightly from his left. {LIGHT} The deep navy "
                      "Milano Mezza Zip knit worn under the open navy reversible gilet, cream showing only inside the gilet's stand "
                      "collar and along its open front edges; the gilet's full-length zip is silver metal on both front edges. The "
                      "knit's short quarter zip is half open and inside the opening there is only his bare skin: he wears nothing "
                      "under the knit. His right hand, a bare wrist with the knit's ribbed cuff just visible, holds the small metal "
                      "pull of the quarter zip between thumb and index finger at mid-chest, about to draw it up. Only the collar, "
                      "the chest and the hand are in the frame; his face is above the top edge of the frame. The fabrics are dry and "
                      "matte. Full-frame digital camera, 100 mm macro, f/4, shallow depth of field.")},
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
    "N4": {"person": True, "refs": [FRONT, BACK, LOAFER],
           # Ronde 1 (V2d, volgshot op afstand) las als een loopband. N4a/N4b (23 okt, crème buiten) waren goed, maar de eigenaar
           # wil de wegloper met het gilet NAVY buiten ("de hele bodywarmer moet blauw, alleen de kraag crème"): N4c/N4d.
           "prompt": (f"9:16, 4K. {LIGHT} {EL} seen from behind, full length from the top of his head to the wet stones under his "
                      "feet, off-centre to the left of the frame, caught mid-step walking away from the camera along the stone "
                      "towpath of the canal towards its pale far end, the misty water on his right, the houses and doorways along "
                      "the bank out of focus on the left. He wears the reversible gilet with the deep NAVY side out, the whole back "
                      "and sides of the gilet deep navy, cream showing only as the inner side of the stand collar at the nape, over "
                      "the deep navy Mezza Zip knit with its long sleeves, deep navy trousers and deep navy suede loafers without "
                      "socks; his arms swing lightly, palms toward his thighs; his back and the back of his head to the camera, face "
                      "not visible. A few fallen yellow leaves on the wet stones. Nobody else on the towpath. Full-frame digital "
                      "camera, 35 mm, f/4, at chest height, about three metres behind him.")},
    "N4n": {"person": True, "refs": [BACK, FRONT, LOAFER],
            # 23 okt, derde ronde: de eigenaar wil ook de kraag navy ("de kraag is beige terwijl die gewoon blauw moet zijn").
            # Mijn N4-prompt vroeg zelf om crème bij de nek. Nu: rits dicht, kraag rechtop, één ononderbroken navy zoals productfoto #1.
            "prompt": (f"9:16, 4K. {LIGHT} {EL} seen from behind, full length from the top of his head to the wet stones under his "
                       "feet, off-centre to the left of the frame, caught mid-step walking away from the camera along the stone "
                       "towpath of the canal towards its pale far end, the misty water on his right, the houses and doorways along "
                       "the bank out of focus on the left. He wears the reversible gilet exactly as in reference image #1, the back "
                       "view: the deep NAVY side out, zipped up to the very top, its stand collar standing up straight and close "
                       "around his neck and deep navy all the way round, so that from behind the gilet is one unbroken deep navy "
                       "from the top of the collar to the hem, the cream inner side completely hidden inside. Under it the deep "
                       "navy Mezza Zip knit, only its long navy sleeves showing; deep navy trousers and deep navy suede loafers "
                       "without socks; his arms swing lightly, palms toward his thighs; his back and the back of his head to the "
                       "camera, face not visible. A few fallen yellow leaves on the wet stones. Nobody else on the towpath. "
                       "Full-frame digital camera, 35 mm, f/4, at chest height, about three metres behind him.")},
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
    # Take 2 van de wegloper (23 okt): take 1 met navy buiten (190fb00e) was een halve loopband (stenen schuiven, huizen stil,
    # passen van 10-20 cm). Nu: de camera reist expliciet mee, de gevels links trekken voorbij, lange passen, zes meter in vijf s.
    "N4": ("Real-time speed. A smooth handheld follow: the operator walks behind him at the same unhurried pace, about three "
           "metres back, so the camera travels forward continuously for the whole shot; the wet cobbles stream steadily toward "
           "the bottom edge of the frame and the doorways and shutters on the left pass by one after another behind him, the "
           "far end of the canal drawing nearer. He walks away from the camera with long, easy strides, one step roughly every "
           "0.6 seconds, each heel landing well ahead of the trailing foot, his navy suede loafers and bare ankles visible at "
           "every step, his arms swinging lightly, never turning round; in five seconds he covers about six metres of towpath. "
           "A thin mist drifts slowly over the water on his right; a light breeze moves his hair and the hem of the gilet. The "
           "shot opens exactly on the start frame. Nothing else happens."),
    "N3": ("Real-time speed. Handheld camera, nearly still, with a slight natural breathing drift. The thread of steam rises and "
           "curls from the espresso; the mist drifts slowly over the canal behind; the waiter in the far background walks on "
           "and a passer-by crosses far behind, out of focus; the open edges of the gilet stir once in a light breeze. The chair "
           "and the table do not move. Nothing else happens."),
}
MOTION["N4n"] = MOTION["N4"]
# N4nz: startbeeld met de handen in de broekzakken (N4n-a); de armen zwaaien dan niet, de ellebogen bewegen mee met de pas.
MOTION["N4nz"] = MOTION["N4"].replace("his arms swinging lightly, never turning round;",
                                      "his hands staying in his trouser pockets the whole time, his elbows moving gently with "
                                      "each step, his shoulders easy, never turning round;")
assert MOTION["N4nz"] != MOTION["N4"]
# N4nz2 (23 okt): concept N4nz-a (ecf0699e) was weer een loopband (gevels stil, grond schuift, 72 passen/min, camera gladde glijvlucht).
# Nu de parallax expliciet: deuren en luiken links worden groter en verlaten het kader, nieuwe komen uit het verdwijnpunt, bollards
# rechts trekken voorbij, hij blijft even groot; 100 passen per minuut; een lichte pas-synchrone deining van de drager.
MOTION["N4nz2"] = (
    "Real-time speed. The camera is carried by an operator walking behind him at exactly his pace, about three metres back, "
    "so for the full five seconds the whole scene streams past the camera in perspective: the wet cobbles flow down and out of "
    "the bottom of the frame, the doorway and the dark shutters on the left grow larger, slide past the left edge of the frame "
    "and leave the picture while new doorways emerge from the far end to take their place, the stone bollards along the canal "
    "edge on the right pass by one after another, and the pale far end of the canal draws nearer; he stays the same size in the "
    "frame because the camera moves with him, and the frame sways very slightly with each step the operator takes. He walks away "
    "from the camera at a brisk natural walking pace, about a hundred steps a minute, each step about seventy centimetres, each "
    "heel landing well ahead of the trailing foot, his navy suede loafers and bare ankles visible at every step, his hands "
    "staying in his trouser pockets the whole time, his elbows moving gently with each step, his shoulders easy, never turning "
    "round; in five seconds he covers about six metres of towpath. A thin mist drifts slowly over the water on his right; a "
    "light breeze moves his hair and the hem of the gilet. The shot opens exactly on the start frame. Nothing else happens.")
SIDE = {"N1": "navy outside, cream only inside the collar and along the open front edges", "N2": "navy outside, cream only inside the collar and along the open front edges",
        "N3": "cream outside, navy only inside the collar and along the open front edges",
        "N4": "navy outside, cream only inside the collar at the nape",
        "N4n": "navy outside everywhere, zipped to the top, the stand collar standing up and deep navy all the way round, the cream inner side hidden",
        "N4nz": "navy outside everywhere, zipped to the top, the stand collar standing up and deep navy all the way round, the cream inner side hidden",
        "N4nz2": "navy outside everywhere, zipped to the top, the stand collar standing up and deep navy all the way round, the cream inner side hidden",
        "N2t2": "navy outside, cream only inside the collar and along the open front edges"}


def image_request(sid):
    s = SHOTS[sid]
    parts = [s["prompt"]]
    if s["person"]:
        parts += [P["keep_en"], ID_LINE, P["expression_en"].capitalize() + "."]
    real = REAL if s["person"] else REAL.replace(REAL[REAL.index("Natural healthy skin"):REAL.index("The clothes")], "")
    set_ = SET + ("\n" + LOAFER_LINE if sid in ("N4", "N4n") else "")
    if sid == "N4n":
        set_ = set_.replace("The inner colour shows only inside the stand collar and along the open front edges, never at the "
                            "armholes or the hem.", "Zipped up with the stand collar standing, the inner colour is completely hidden: "
                            "seen from behind the gilet, collar included, is one deep navy.")
        assert "completely hidden" in set_
    parts += [set_, HANDS if s["person"] else "His hand and wrist are bare: no watch, no ring, no bracelet.", NO_TEXT, real]
    if sid == "N3":
        parts[-3] = ""
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(p for p in parts if p),
            "medias": [{"value": v, "role": "image_references"} for v in s["refs"]]}


def images(keys):
    return [{"index": i, "sid": k, "params": image_request(k.split("-")[0] if "-" in k else k[:2])} for i, k in enumerate(keys)]


def video(clip, start, draft=True, draft_job=None):
    shot = SHOTS[{"N2t2": "N2", "N4nz": "N4n", "N4nz2": "N4n"}.get(clip, clip)]
    who = ("He is the man in the start frame and in the reference images; use the reference images only for his face and hair. "
           "He keeps the same face, hair and clothes throughout" if shot["person"] else
           "Everything stays exactly as in the start frame; the clothes keep their shape and colour throughout")
    knit = "" if clip == "N3" else ", over the navy quarter-zip knit"
    prompt = (f"{MOTION[clip]} {who}: the sleeveless gilet stays {SIDE[clip]} for the whole shot{knit}. "
              f"{'His wrists bare. ' if clip != 'N3' else ''}{NO_TEXT} Natural motion blur, one continuous take.")
    medias = [{"role": "start_image", "value": start}]
    if shot["person"]:
        medias += [{"role": "image_references", "value": f} for f in FACES]
    req = {"model": "seedance_2_5", "mode": "omni_reference", "resolution": "480p" if draft else "1080p", "draft": draft,
           "bitrate_mode": "high", "duration": 4, "aspect_ratio": "9:16", "generate_audio": False, "prompt": prompt,
           "medias": medias, "declined_preset_id": PRESET_DECLINE}
    if clip in ("N4", "N4n", "N4nz", "N4nz2"):
        req["duration"] = 5
    if not draft:
        req["draft_job_id"] = draft_job
    return req


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    out = {"images": lambda: images(args), "draft": lambda: video(args[0], args[1]),
           "final": lambda: video(args[0], args[1], False, args[2])}[cmd]()
    print(json.dumps(out, ensure_ascii=False))
