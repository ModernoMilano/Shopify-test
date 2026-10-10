"""Video "Il pianoforte" (10 okt 2026): MILANO REVERSO SET ANTRACITE & PIETRA met de MILANO SUEDE LOAFER - GRIGIO.

Wens van de eigenaar: niet slow motion zoals de vorige video's. Een luxe huis met een mooie vleugel. Het shot begint dichtbij
op zijn hand met een vinger op een toets (hand en onderarm, de focus op kleding en kwaliteit), dan steeds verder uitzoomen
terwijl hij wegloopt naar een groot raam en naar buiten kijkt; aan het eind de hele outfit van opzij. Eerst start- en
eindbeeld ter goedkeuring.

Opzet: één doorlopende shot met Seedance 2.5, start_image + end_image. Het eindbeeld (hele outfit, raam, vleugel op de
voorgrond) wordt eerst gemaakt; het startbeeld is daar een bewerking van, zodat kamer, licht en kleding gelijk blijven.

Gebruik:
  python3 -I piano.py end                 -> 2 varianten van het eindbeeld (generate_image_batch)
  python3 -I piano.py start <job eind>    -> 2 varianten van het startbeeld, als bewerking van het gekozen eindbeeld
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


def start_frame(job_end):
    parts = [
        "A close detail from the same room as reference image #1, a few seconds earlier: the same man, the same black "
        "lacquered grand piano, the same daylight and the same clothes. He stands beside the grand piano, close to the "
        "keyboard, his right arm hanging relaxed and his index finger resting on one white key, pressing it softly. The camera "
        "is very close beside the keyboard at key height and frames his right arm from the shoulder down to his hand on the "
        "keys: at the top, the deep armhole of the anthracite gilet with the short sleeve of the light pietra "
        "T-shirt coming out of it; below, his bare forearm; at the bottom, his relaxed hand on the black and white keys, the "
        "black lacquer softly reflecting it. His face is not in the picture. The bright window and the room behind are soft "
        "and out of focus.",
        "Soft late-morning daylight from the window on his left rakes across the fabric of the gilet and the T-shirt and "
        "shows their texture; the lacquer and the keys catch the light; muted natural colour, soft contrast, no HDR.",
        "The pieces are these ModernoMilano pieces, reproduced exactly as in the reference images:\n" + SET["text"],
        sleeveless("dark anthracite grey", "light pietra stone", 2),
        PIANO, f"{HANDS} Natural hand with real skin texture and relaxed fingers.", REAL_SMOOTH,
        "Full-frame digital camera, 85mm lens at f/2."]
    return req(parts, [job_end, SET_FRONT, SET_DETAIL])


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "end":
        out = [{"index": 80 + v, "params": end_frame()} for v in range(2)]
    elif cmd == "start":
        out = [{"index": 82 + v, "params": start_frame(args[0])} for v in range(2)]
    else:
        raise SystemExit(__doc__)
    print(json.dumps(out, ensure_ascii=False))
