"""Video "Il pianoforte" (10 okt 2026): MILANO REVERSO SET ANTRACITE & PIETRA met de MILANO SUEDE LOAFER - GRIGIO.

Wens van de eigenaar: niet slow motion zoals de vorige video's. Een luxe huis met een mooie vleugel. Het shot begint dichtbij
op zijn hand met een vinger op een toets (hand en onderarm, de focus op kleding en kwaliteit), dan steeds verder uitzoomen
terwijl hij wegloopt naar een groot raam en naar buiten kijkt; aan het eind de hele outfit van opzij. Eerst start- en
eindbeeld ter goedkeuring.

Opzet: één doorlopende shot met Seedance 2.5, start_image + end_image. Het eindbeeld (hele outfit, raam, vleugel op de
voorgrond) wordt eerst gemaakt; het startbeeld is daar een bewerking van, zodat kamer, licht en kleding gelijk blijven.

Gebruik:
  python3 -I piano.py end                 -> 2 varianten van het eindbeeld (generate_image_batch)
  python3 -I piano.py start <job eind> [eerste index]  -> 2 varianten van het startbeeld, als bewerking van het gekozen
                                                         eindbeeld (standaard index 82)
  python3 -I piano.py shoes <job eind>    -> 2 varianten van het eindbeeld met alleen andere schoenen (2k)
  python3 -I piano.py end2 <job start>    -> 2 varianten van het eindbeeld, ronde 2, met het startbeeld als kamer (2k)
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-reels-focus"))
from videos4 import EL, HANDS, ID_LINE, P, REAL_SMOOTH, person, req, reverso, sleeveless  # noqa: E402

# Productfoto's (higgsfield-media.json): de set aan het model, voorkant (4da40a85) en detail van kraag en rits (d0bad191);
# de loafer van opzij (08_45_00) en het paar schuin (08_45_36). Geen flat-lay: daar zijn de armsgaten in de binnenkleur.
SET_FRONT, SET_DETAIL = "296c2189-329b-4529-bcef-6552fc227b42", "e9385bb6-6e75-4591-918a-3211ecbb15f8"
LOAFER_SIDE, LOAFER_PAIR = "9de16713-eb94-436b-9edc-61e3796a7f77", "5b91dba6-b39f-42ab-9902-aae2893534d7"

SET = reverso("ANTRACITE & PIETRA", "dark anthracite grey", "light pietra stone", "light pietra stone", "dark anthracite grey",
              [SET_FRONT, SET_DETAIL])
LOAFER = ("- MILANO SUEDE LOAFER - GRIGIO, exactly as in reference images #3 and #4: mid-grey suede slip-on loafers with a "
          "stitched moc-toe apron and a flat off-white rubber sole, worn on bare feet without socks, a mirrored left and right "
          "pair.")
PIANO = ("The grand piano is a plain black lacquered grand with no brand name, no logo and no lettering anywhere, on the "
         "fallboard or elsewhere.")
ROOM = ("a luxurious 1950s Milanese residence on a quiet morning: a large, calm living room with a pale travertine floor, warm "
        "grey stone walls, ivory linen curtains, a black lacquered grand piano, and a tall floor-to-ceiling window with thin "
        "bronze frames looking out over a green garden and the soft rooftops of Milan beyond, out of focus")
LIGHT = ("Soft, bright late-morning daylight from the tall window falls along his profile and the front of the clothes; the "
         "room behind him is a stop darker; muted natural colour, soft contrast, no HDR.")


def end_frame():
    return req(person(
        scene=(f"Late morning in {ROOM}. Nobody else is there. " + EL + " stands at the tall window, his body in profile to "
               "the camera, facing the right of the frame, looking out of the window at the garden; his weight on one leg, his "
               "left hand in his trouser pocket and his right arm relaxed at his side. The camera stands in the room at hip "
               "height beside the end of the grand piano's keyboard, which is soft and out of focus in the lower-left "
               "foreground. Framed vertically from just above his head to his feet on the travertine floor: the whole man "
               "and his loafers are in the picture, standing off-centre to the right, the bright window beside him."),
        light=LIGHT, product={"text": SET["text"] + "\n" + LOAFER},
        worn=("the gilet with the dark ANTHRACITE side out, hanging open over the light pietra T-shirt; the anthracite "
              "trousers, slim and tapered, ending just above the ankle bone; the grey suede loafers on bare feet."),
        extra=[sleeveless("dark anthracite grey", "light pietra stone", 1), PIANO],
        real=REAL_SMOOTH, lens="Full-frame digital camera, 35mm lens at f/2.8."),
        [SET_FRONT, SET_DETAIL, LOAFER_SIDE, LOAFER_PAIR])


# Eindbeeld ronde 2. Eindbeeld 80 is afgekeurd om drie redenen:
# - penny loafers, overgenomen van de setfoto aan het model;
# - een toetsenbord op de voorgrond met zwarte toetsen in een gelijkmatige rij;
# - haar dat te donker en te koel is.
# Daarom wordt de setfoto boven de enkels afgesneden (3de9e4be). Het goedgekeurde startbeeld 87 is referentie #1 voor de
# kamer. Er staan geen toetsen in beeld en de haarkleur wordt met name genoemd.
SET_FRONT_NOSHOES = "3de9e4be-64af-4156-a409-759a5eb6eb3d"
HAIR = ("His hair is warm chestnut brown, with warm reddish-brown light where the daylight touches it; not espresso, not "
        "dark ash brown.")
LOAFER_PLAIN = ("The loafers have a smooth plain vamp with only a stitched moc-toe apron seam around the toe: no strap, no "
                "saddle and no penny slot across the vamp.")


def end_frame2(job_start):
    return req(person(
        scene=("Late morning in the same room as reference image #1, a few seconds later: the same black lacquered grand "
               "piano, the same ivory linen curtains, the same tall window with thin bronze frames looking out over a green "
               "garden and soft rooftops, and a pale travertine floor. Nobody else is there. " + EL + " stands at the tall "
               "window, his body in profile to the camera, facing the right of the frame, looking out of the window at the "
               "garden; his weight on one leg, his right hand in his trouser pocket. The camera has stepped back into the "
               "room, at hip height: the curved black lacquered side of the grand piano is soft and out of focus at the left "
               "edge of the frame, and no piano keys are visible. Framed vertically from just above his head to his feet on "
               "the travertine floor: the whole man and his loafers are in the picture, standing off-centre to the right, "
               "the bright window beside him, with a soft shadow where he stands."),
        light=LIGHT, product={"text": SET["text"] + "\n" + LOAFER},
        worn=("the gilet with the dark ANTHRACITE side out, hanging open over the light pietra T-shirt; the anthracite "
              "trousers, slim and tapered, ending just above the ankle bone; the grey suede loafers on bare feet."),
        extra=[sleeveless("dark anthracite grey", "light pietra stone", 2), LOAFER_PLAIN, HAIR, PIANO],
        real=REAL_SMOOTH, lens="Full-frame digital camera, 35mm lens at f/2.8."),
        [job_start, SET_FRONT_NOSHOES, LOAFER_SIDE, LOAFER_PAIR])


def start_frame(job_end):
    parts = [
        "A close detail from the same room as reference image #1, a few seconds earlier: the same man, the same black "
        "lacquered grand piano, the same daylight and the same clothes. He stands beside the grand piano, close to the "
        "keyboard, his left arm hanging relaxed and the index finger of his left hand resting on one white key, pressing it "
        "softly. The camera is very close beside the keyboard at key height and frames his left arm from the shoulder down "
        "to his hand on the keys: at the top, the deep armhole of the anthracite gilet with the short sleeve of the light "
        "pietra T-shirt coming out of it; below, his bare forearm; at the bottom, his relaxed hand on the black and white "
        "keys, the black lacquer softly reflecting it. His face is not in the picture. The bright window and the room "
        "behind are soft and out of focus.",
        # Ronde 1 (82, 83) afgekeurd: een tweede hand op de toetsen, een in tweeën geknipt toetsenbord, voorover leunen.
        # Ronde 2 (84, 85) afgekeurd: weer losse vingers aan de rand van het beeld (zijn andere hand) en gouden letters op de
        # klep. Daarom zijn andere hand uit beeld en maar één octaaf in beeld.
        "He stands upright beside the keyboard and does not lean over it; his right hand hangs at his far side, hidden "
        "behind his body and out of the picture. Only about one octave of the keyboard is visible, one continuous straight "
        "row of keys under his hand with the black keys in groups of two and three; the rest of the keyboard is outside the "
        "frame. His left hand is the only hand in the picture: no other fingers or hands anywhere, also not at the edges of "
        "the frame or in the reflections in the black lacquer. The fallboard is plain black lacquer with no name, no logo "
        "and no gold lettering.",
        "Soft late-morning daylight from the tall window on the right of the frame rakes across the fabric of the gilet and "
        "the T-shirt and shows their texture; the lacquer and the keys catch the light; muted natural colour, soft "
        "contrast, no HDR.",
        "The pieces are these ModernoMilano pieces, reproduced exactly as in the reference images:\n" + SET["text"],
        sleeveless("dark anthracite grey", "light pietra stone", 2),
        PIANO, f"{HANDS} Natural hand with real skin texture and relaxed fingers.", REAL_SMOOTH,
        "Full-frame digital camera, 85mm lens at f/2."]
    return req(parts, [job_end, SET_FRONT, SET_DETAIL])


def shoes_fix(job_end):
    """Eindbeeld 80 had penny loafers (een riempje met sleuf over de wreef, overgenomen van de setfoto aan het model); de
    Grigio heeft een glad voorblad met alleen de moc-toe-naad. Bewerking van het eindbeeld die alleen de schoenen
    verandert."""
    return req([
        "The same photograph as reference image #1, unchanged in every way: the same man, face, hair, pose, clothes, room, "
        "grand piano, daylight and framing. Change only his shoes.",
        "His shoes are the MILANO SUEDE LOAFER - GRIGIO, exactly as in reference images #2 and #3: mid-grey suede slip-on "
        "loafers with a smooth plain vamp and only a stitched moc-toe apron seam around the toe; there is no strap, no "
        "saddle and no penny slot across the vamp; a flat off-white rubber sole. Worn on bare feet without socks, with bare "
        "skin at the ankles, a mirrored left and right pair.",
        "No film borders, no frame, no text, no logos."], [job_end, LOAFER_SIDE, LOAFER_PAIR])


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "end":
        out = [{"index": 80 + v, "params": end_frame()} for v in range(2)]
    elif cmd == "start":
        base = int(args[1]) if len(args) > 1 else 82
        out = [{"index": base + v, "params": start_frame(args[0])} for v in range(2)]
    elif cmd == "end2":
        out = [{"index": 90 + v, "params": {**end_frame2(args[0]), "resolution": "2k"}} for v in range(2)]
    elif cmd == "shoes":
        # 2k: genoeg voor een video-eindbeeld (1080p) en 2 credits in plaats van 4 (10 okt)
        out = [{"index": 88 + v, "params": {**shoes_fix(args[0]), "resolution": "2k"}} for v in range(2)]
    else:
        raise SystemExit(__doc__)
    print(json.dumps(out, ensure_ascii=False))
