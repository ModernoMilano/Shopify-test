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
  python3 -I piano.py end3 <job start>    -> 2 varianten van het eindbeeld, ronde 3: villa aan zee, van achteren (2k)
  python3 -I piano.py video <job eind> [draft|720p|<concept job>] [seconden]  -> Seedance 2.5 van startbeeld 87 naar het
                                                                    eindbeeld
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-reels-focus"))
from videos4 import EL, HANDS, HF, ID_LINE, P, PRESET_DECLINE, REAL_SMOOTH, person, req, reverso, sleeveless  # noqa: E402

# Productfoto's (higgsfield-media.json): de set aan het model, voorkant (4da40a85) en detail van kraag en rits (d0bad191);
# de loafer van opzij (08_45_00) en het paar schuin (08_45_36). Geen flat-lay: daar zijn de armsgaten in de binnenkleur.
SET_FRONT, SET_DETAIL = "296c2189-329b-4529-bcef-6552fc227b42", "e9385bb6-6e75-4591-918a-3211ecbb15f8"
LOAFER_SIDE, LOAFER_PAIR = "9de16713-eb94-436b-9edc-61e3796a7f77", "5b91dba6-b39f-42ab-9902-aae2893534d7"
START_JOB = "928c365c-4920-4184-a043-8e9a9e801112"  # goedgekeurd startbeeld 87 (ronde 3 van het startbeeld)

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


# Eindbeeld ronde 3 (wens eigenaar, 10 okt). Het startbeeld 87 blijft, maar:
# - de villa wordt groot, met uitzicht over zee, strand en natuur in Italië;
# - het beeld eindigt achter hem, terwijl hij vanaf het raam naar het uitzicht kijkt.
# Gekozen kust: Sardinië. Een stille baai met licht zand, turquoise water en macchia en pijnbomen op de rotsen.
# Vooraf door 4 critici nagelopen (workflow, 10 okt). De belangrijkste aanpassingen:
# - Referentie #2 is de achterkant van de set zonder hoofd (78276004): het productmodel heeft kort, bijna zwart haar.
#   Ook zonder schoenen, want daar draagt het penny loafers.
# - Referentie #4 is de loafer van achteren (c899ef9b): van achteren zie je alleen de hielen.
# - Het kader moet bereikbaar zijn vanuit het startbeeld. De ramen staan rechts en lopen de diepte in; hij draait naar
#   zijn rechterhand en loopt naar het raam in de hoek. De vleugel zit niet in het eindbeeld, dus er kunnen geen foute
#   toetsen in komen.
# - Direct achter het glas staan een terras en bomen, net als in het startbeeld, met de baai daarachter. Anders moet de
#   video een tuin in zee laten overvloeien.
# - 50mm op f/8, zodat het uitzicht leesbaar blijft. Geen hand in zijn zak: dat beweegt slecht in video.
SET_BACK = "78276004-55b2-4e58-8bab-0bd295330338"
LOAFER_REAR = "c899ef9b-3a34-4e8d-83cf-1d83804a6f07"


def end_frame3(job_start):
    return req([
        ("Late morning, a few seconds later in the same room as reference image #1, seen from a little further back, "
         "slightly higher and turned a little to the right: the large living room of a grand Italian villa high on a green "
         "hillside above the sea on the north-east coast of Sardinia, Italy, with a pale polished travertine floor, warm "
         "plaster walls and ivory linen curtains drawn back to the sides of the windows. The wall of tall floor-to-ceiling "
         "glass panels in the same slim bronze frames as in reference image #1, which is behind him on the right of "
         "reference image #1, is still on the right side of the picture, running into the depth of the room; at the far "
         "end of the room it turns the corner into a second wall of the same tall glass panels facing the camera, with "
         "large clear panes and a low threshold at the floor. Just outside the glass lie a pale stone terrace, the "
         "terracotta-tiled roof edge of the villa's lower terrace and the tops of the garden's umbrella pines and olive "
         "trees, the same greenery as glimpsed through the windows in reference image #1; beyond and far below them, a "
         "wide view over a quiet bay a few hundred metres away: a crescent of pale sand, small with the distance, clear "
         "water that is soft turquoise near the shore and deep blue further out, smooth pink-grey granite rocks, green "
         "Mediterranean scrub of juniper and myrtle and Italian umbrella pines on the two headlands that frame the bay, and "
         "the open sea running out to the horizon under a clear soft-blue sky with a light haze only along the horizon. "
         "The beach is empty and untouched, the sea is empty, and the green hillsides are wild, with no other buildings. "
         "Nobody else is in the room."),
        (EL + " stands close to the far windows, a little right of centre, about four to five metres from the camera, seen "
         "straight from behind with his back to the camera, looking out over the bay; his weight on one leg, both arms "
         "hanging relaxed at his sides. His head is straight and level, turned fully towards the window like his "
         "shoulders: from the camera only the back of his head, his hair, the back of his neck and the backs of his ears "
         "are seen, with no part of his cheek, nose or eye in view. He stands in front of one wide clear pane, so his body "
         "does not cover the view: the curved pale beach, the turquoise water and a pine-covered headland are plainly "
         "visible in the glass beside him, and the sea horizon is one straight, level line at the same height on both "
         "sides of him, crossing behind his upper back; the thin bronze frames are to his left and right, not behind his "
         "head or spine. The glass is clean and clear, with no reflection of him or of the room in it."),
        ("The camera is at chest height and held perfectly level, so the vertical window frames stay vertical and "
         "parallel. Framed vertically, he fills a little over half the height of the frame, standing in its lower part "
         "with his loafers near the bottom edge and a stretch of polished floor between him and the camera; the tall glass "
         "panels rise far above his head and run on past the top of the frame, so the height of the room and the size of "
         "the windows are obvious."),
        ("Soft late-morning daylight; the sun is high and behind the house, out of view, so the bay is lit from the front "
         "with clear, gentle colour, there is no glare or sparkle on the water, and no sunbeams or bright sun patches fall "
         "into the room. The only light in the room is this daylight coming through the glass, soft and even as in "
         "reference image #1. The view is the brightest part of the picture but keeps its colour and detail; the room and "
         "his back are in soft open daylight about one and a half stops darker, clearly readable. The polished travertine "
         "in front of him carries a soft, blurred reflection of the bright window, and under his loafers there is only a "
         "faint, diffuse contact shadow. Against the bright window the gilet and trousers still read clearly as dark "
         "anthracite grey, not black, with their matte peached texture visible, and the T-shirt sleeves and hem read as "
         "light pietra stone. Muted natural colour, soft contrast, no HDR, not a silhouette."),
        ("He is the man introduced above, seen from behind. Reference image #2 shows only the clothing; the man wearing it "
         "there is a different person, so his head, hair, neck and skin are not copied. From behind, his hair is warm "
         "chestnut brown with lighter golden-brown strands where the daylight catches it (not espresso, not near-black), "
         "full and swept back with soft natural volume, longer on top, the sides combed back over the tops of his ears and "
         "tapered neatly at the nape; the same build, shoulders and posture."),
        ("He wears only these ModernoMilano pieces, reproduced exactly as in the product reference images:\n" + SET["text"]
         + "\n- MILANO SUEDE LOAFER - GRIGIO, exactly as in reference images #3 (from the side) and #4 (from behind): "
         "mid-grey suede slip-on loafers with a flat off-white rubber sole, worn on bare feet without socks, a mirrored "
         "left and right pair."),
        ("How they are worn, seen from behind: the gilet with the dark ANTHRACITE side out. The zip and the two welt "
         "pockets are on the front and are not visible from behind; the back panel is one plain piece of anthracite "
         "fabric with no zip, pocket, label or logo, exactly as in reference image #2, ending in the elasticated hem, and "
         "the back of the stand collar stands up plain anthracite at the back of his neck. The short sleeves of the light "
         "pietra T-shirt come out of the deep armholes, and the T-shirt hem hangs loose a few centimetres below the gilet "
         "hem, untucked all the way round, covering the waistband. The anthracite trousers are slim and tapered, with a "
         "plain, clean seat with no back pockets and no labels, exactly as in reference image #2, ending just above the "
         "ankle bone; there is no belt."),
        ("The gilet is a SLEEVELESS bodywarmer, cut like the gilet in reference image #2. Seen from behind, it shows only "
         "its dark anthracite outside: the back panel, the outside of the stand collar, the armhole edges and the "
         "elasticated hem are all anthracite, and no light pietra stone shows anywhere on the gilet in this picture. The "
         "armholes are cut deep and sit clearly inward of his shoulder points, so on both sides the T-shirt's shoulder "
         "seam and the top of its short sleeve are plainly visible outside the gilet. The gilet is a matte, peached, "
         "slightly thicker fabric whose armhole edges lie flat on the T-shirt; the T-shirt is a thinner jersey with a "
         "subtle sheen, so the two layers are easy to tell apart. The T-shirt sleeve ends in its own hemmed edge on the "
         "upper arm."),
        ("Seen from behind, his feet point away from the camera towards the window. The loafers are exactly as in "
         "reference image #4: plain rounded grey suede heels with a single fine centre-back seam, no heel tab, no pull "
         "loop, no logo and no contrast patch; the low suede topline sits just below his bare heels, with bare skin at the "
         "backs of both ankles and no socks; the flat off-white rubber sole is slightly thicker at the heel. Their fronts, "
         "hidden from the camera, have a smooth plain vamp with only a stitched moc-toe seam: no strap, no saddle and no "
         "penny slot."),
        f"{HANDS} He is the only person in the picture.",
        ("An unretouched photograph. The visible skin of his neck, forearms and hands has fine real texture, matte, with "
         "no glow and no airbrushing. The clothes are real fabric with soft natural creases at the waist and where the "
         "gilet folds. Real optics: full-frame digital camera, natural depth of field, slight lens softness at the far "
         "edges: he is sharp, and the bay beyond the glass is a little softer with distance and haze but clearly readable. "
         "No borders, no frame, no text, no logos."),
        "Full-frame digital camera, 50mm lens at f/8."], [job_start, SET_BACK, LOAFER_SIDE, LOAFER_REAR])


# Eindbeeld ronde 3, controle (6 controleurs en een eindoordeel, 10 okt):
# - 92 is afgekeurd: een spookfiguur in het rechterraam leest als een tweede persoon.
# - 93 is goedgekeurd met aantekeningen. De ruimte leest niet als "echt een dikke villa": een gewoon plafond van ongeveer
#   2,5 m en een lege kamer.
# Daarom twee pogingen voor meer grandeur:
# - 93 bewerken: alleen het interieur en het terras worden luxer (infinity pool, meubels, balkenplafond);
# - een nieuwe variant met een kamer van dubbele hoogte, op 35 mm, met hem verder weg.
END_93 = "417707cb-0aa8-4aa5-8ccc-8ba5d3cfdee2"
GRAND_TERRACE = ("On the pale stone terrace just outside the glass lies a long infinity pool of still, clear water whose far edge "
                 "seems to run straight into the sea, with two low linen sun loungers beside it; beyond it the umbrella pines "
                 "and the bay.")
GRAND_ROOM = ("Inside, the room is furnished sparingly like the living room of a very large luxury villa: the soft corner of a "
              "long, low ivory linen sofa and a low travertine table at the left edge of the frame, a large pale handmade "
              "ceramic vase with an olive branch, and a ceiling of dark wooden beams on white plaster. None of it has any "
              "logo, label or lettering.")


def end_grand_edit(job_end=END_93):
    return req([
        ("The same photograph as reference image #1, unchanged in every way: the same man in the same pose, seen from "
         "behind, with the same hair, the same clothes and the same loafers; the same camera position and framing, the same "
         "glass corner with its slim bronze frames, the same light and the same view over the bay. Change only the room "
         "and the terrace, so that it is clearly a very large, luxurious villa."),
        GRAND_TERRACE, GRAND_ROOM,
        ("He is the only person in the picture; the pool, the terrace and the beach are empty. The glass is clean and clear, "
         "with no reflection of him or of anyone in it."),
        "No borders, no frame, no text, no logos."], [job_end])


def end_frame4(job_start):
    """Ronde 3 met meer grandeur: een kamer van dubbele hoogte, 35mm en hem verder weg. Verder de nagelopen prompt van
    end_frame3."""
    p = end_frame3(job_start)
    t = p["prompt"]
    swaps = [
        ("the large living room of a grand Italian villa", "the vast double-height living room of a grand Italian villa"),
        ("with a pale polished travertine floor, warm plaster walls and ivory linen curtains drawn back to the sides of the "
         "windows.",
         "about six metres high, with a pale polished travertine floor, warm plaster walls and ivory linen curtains drawn "
         "back to the sides of the windows. " + GRAND_ROOM),
        ("Just outside the glass lie a pale stone terrace,", GRAND_TERRACE.replace("beyond it the umbrella pines and the bay.",
         "beside the terrace lie") ),
        ("stands close to the far windows, a little right of centre, about four to five metres from the camera,",
         "stands close to the far windows, a little right of centre, about six metres from the camera,"),
        ("Framed vertically, he fills a little over half the height of the frame, standing in its lower part with his "
         "loafers near the bottom edge and a stretch of polished floor between him and the camera; the tall glass panels "
         "rise far above his head and run on past the top of the frame, so the height of the room and the size of the "
         "windows are obvious.",
         "Framed vertically, he fills a little under half the height of the frame, standing in its lower half on the "
         "polished floor; the double-height glass walls rise far above him, more than three times his height, to the "
         "beamed ceiling at the top of the frame, so the size of the room and of the windows is obvious."),
        ("Full-frame digital camera, 50mm lens at f/8.", "Full-frame digital camera, 35mm lens at f/8."),
    ]
    for a, b in swaps:
        assert a in t, a[:50]
        t = t.replace(a, b)
    p["prompt"] = t
    return p


# Concepten 1 en 2 (10 okt) zijn afgekeurd. Rond 3 à 3,5 s springt het beeld (concept 1: snede) of vloeit het over
# (concept 2: dubbele belichting), van de kamer met gazon in 87 naar de villa van 94. Seedance kan twee verschillende
# ruimtes niet als één kamer verbinden. Daarom krijgt het startbeeld dezelfde villa: alleen de achtergrond door de
# ramen en de afwerking van de kamer worden die van 94. Hand, arm, kleding, vleugel en kader blijven gelijk.
def start_villa_edit(job_start=START_JOB, job_end="4d7fdf1b-1093-4b13-aea5-e685537506af"):
    return req([
        ("The same photograph as reference image #1, unchanged in every way: the same man, the same arm and hand with the "
         "same fingers in the same position on the keys, the same clothes, the same black grand piano, the same camera "
         "angle, framing and depth of field. Change only what is seen through the tall windows on the right and the finish "
         "of the room, so that it is the same villa room as in reference image #2: outside the glass, soft and out of "
         "focus, the pale stone terrace with the long infinity pool, the umbrella pines and the turquoise bay with the "
         "open sea beyond; the window frames are the same slim bronze frames as in reference image #2, the walls are warm "
         "white plaster and the floor is pale travertine, as in reference image #2."),
        ("The soft daylight still comes from the tall windows on the right, as in reference image #1. Nobody else is in "
         "the picture and the terrace is empty. His hands and wrists are bare."),
        "No borders, no frame, no text, no logos."], [job_start, job_end])


# Versie 2 van de video (eigenaar, 10 okt).
# Fout in versie 1: hij loopt door de glazen wand en staat dan opeens in een andere ruimte (screenshot rond 4 s). Oorzaak:
# het eindbeeld 94 (een glazen hoek) komt in het startbeeld nergens voor, dus Seedance moet de ruimte daartussen
# verzinnen. Wens erbij: de video iets langer, en aan het eind kijkt hij rustig naar rechts, zodat je zijn gezicht een
# beetje van opzij ziet.
# Oplossing: een eindbeeld van dezelfde kamer als startbeeld 97, van verder weg op dezelfde lijn. Links op de
# voorgrond de vleugel, rechts de raamwand met gordijnen die de diepte in loopt, achterin de glazen hoek van 94. Hij
# staat binnen voor het achterste raam en draait zijn hoofd ongeveer 45 graden naar rechts (modelregel: hooguit 45).
START_VILLA = "ce72c67f-805a-411f-bf9a-4b71b2bdb17e"


def end_frame5(job_start=START_VILLA, job_far="4d7fdf1b-1093-4b13-aea5-e685537506af"):
    return req([
        ("A wider view of the same villa living room as in reference images #1 and #2, a few seconds later, taken from "
         "where the camera of reference image #1 has pulled back: about three metres further back along the same line "
         "and a little higher, at chest height, held level, looking straight into the depth of the room. In the left "
         "foreground stands the same black lacquered grand piano as in reference image #1, seen from the end of its "
         "keyboard, soft and slightly out of focus and cut off by the left and bottom edges of the frame. On the right, "
         "the same wall of tall floor-to-ceiling glass panels in slim bronze frames, with the same ivory linen curtains "
         "as in reference image #1, runs straight into the depth of the room, with the pale stone terrace, the infinity "
         "pool and the umbrella pines outside it. At the far end of the room, about five metres from the camera, is the "
         "glass corner of reference image #2: a second wall of the same tall glass panels facing the camera, with the "
         "long low linen sofa, the travertine table and the pale vase with the olive tree in front of it, and beyond the "
         "glass the infinity pool, the umbrella pines and the bay with its crescent of pale sand, its granite rocks, the "
         "turquoise water and the open sea to the horizon. A ceiling of dark wooden beams on white plaster, a pale "
         "polished travertine floor. It is all one room; nobody else is in it."),
        (EL + " stands inside the room on the travertine floor, at the far end, about half a metre in front of the far "
         "glass wall and well away from the glass wall on the right, seen from behind with his back to the camera; his "
         "weight on one leg, his arms relaxed at his sides. His body faces the far glass, and he has calmly turned his "
         "head about forty-five degrees to his right to look out along the glass towards the pines and the sea, so his "
         "face is seen a little from the side: the line of his right cheek, his nose, his eye and his jaw in soft "
         "profile, his mouth closed and his expression calm. He fills about half the height of the frame, standing "
         "slightly right of centre, his loafers on the floor in the lower part of the frame."),
        ("Soft late-morning daylight; the sun is high and behind the house, out of view, so there is no glare on the "
         "water and no sunbeams in the room. The only light is the daylight coming through the glass walls, soft and "
         "even as in reference image #1. The view is the brightest part of the picture but keeps its colour and detail; "
         "the room and his back are about one and a half stops darker, clearly readable, and the gilet and trousers read "
         "as dark anthracite grey, not black. Muted natural colour, soft contrast, no HDR, not a silhouette."),
        "His face is the face of the man introduced above. " + ID_LINE,
        ("He wears only these ModernoMilano pieces, exactly as in reference image #2 and the product reference images:\n"
         + SET["text"] + "\n- MILANO SUEDE LOAFER - GRIGIO, as in reference image #4 (from behind): mid-grey suede "
         "slip-on loafers with a smooth plain vamp, no strap and no penny slot, a flat off-white rubber sole, on bare "
         "feet without socks, a mirrored left and right pair."),
        ("Seen from behind: the gilet with the dark ANTHRACITE side out, its plain back panel with no zip, pocket, label "
         "or logo, exactly as in reference image #3, ending in the elasticated hem, and the stand collar plain "
         "anthracite at the back of his neck; no light pietra stone shows anywhere on the gilet from behind, and the "
         "armhole edges are dark anthracite. The short sleeves of the light pietra T-shirt come out of the deep "
         "armholes, and its hem hangs loose a few centimetres below the gilet hem, untucked all the way round. The slim "
         "anthracite trousers have a plain seat with no back pockets and no belt, ending just above the ankle bone; bare "
         "skin shows at the backs of both ankles above the loafers."),
        ("Reference image #3 shows only the clothing; the man wearing it there is a different person, so his head and "
         "hair are not copied."),
        PIANO, f"{HANDS} He is the only person in the picture.",
        ("An unretouched photograph. Fine real skin texture, matte, with no glow and no airbrushing. The clothes are "
         "real fabric with soft natural creases. Real optics: full-frame digital camera, natural depth of field: he and "
         "the far end of the room are sharp, the view beyond the glass is a little softer with distance and haze, the "
         "piano in the foreground is soft. No borders, no frame, no text, no logos."),
        "Full-frame digital camera, 50mm lens at f/8."], [job_start, job_far, SET_BACK, LOAFER_REAR])


# end_frame5 is niet gegenereerd. Drie critici vonden dat ook die kamer niet bestaat in startbeeld 97 (10 okt). Daar
# staan één schuine glazen wand rechts, ongeveer 1,2 m achter hem, een witte gestucte muur achter de vleugel en een vlak
# wit plafond, zonder gordijnen en zonder glazen hoek. Een glazen hoek met bank moet Seedance dus verzinnen, en dan
# loopt hij door het glas.
# end_frame6 is daarom precies die kamer, 2 m verder terug op dezelfde lijn. Hij draait zich naar het raam dat al
# achter hem staat en blijft binnen, ongeveer 60 cm ervoor. Lichaam 30 graden en hoofd 40 graden verder naar rechts:
# zijn gezicht in een zacht verloren profiel, zonder dat de nek meer dan 45 graden draait. 35mm, zoals het startbeeld
# ongeveer heeft. Het oude eindbeeld gaat niet als referentie mee: het trekt de glazen hoek terug.
def end_frame6(job_start=START_VILLA):
    return req([
        ("The same villa living room as in reference image #1, a few seconds later and seen wider: the camera of "
         "reference image #1 has moved straight back about two metres along its own line and risen a little, to chest "
         "height, held level and still pointing in exactly the same direction as in reference image #1, so every wall "
         "and line keeps the angle it has there. The picture shows only the room that reference image #1 already shows, "
         "seen from further back. In the left part of the frame stands the same black lacquered grand piano, exactly as "
         "placed in reference image #1: seen from the end of its keyboard, the keyboard running away from the camera "
         "towards the glass, its curved black body cut off by the left edge of the frame and filling no more than the "
         "left third of the frame, so his whole figure down to both loafers stands clear of it. Behind the piano, at the "
         "far end of the room, is the same plain white plaster wall as in reference image #1, under the same flat white "
         "plaster ceiling. On the right is the same single wall of bare, clear floor-to-ceiling glass panels in slim "
         "bronze frames as in reference image #1, at the same angle as there: nearest to the camera at the right edge of "
         "the frame, it recedes diagonally towards the left and meets the white plaster wall in a plain vertical corner "
         "deep in the room. Beyond the glass, as in reference image #1: the pale stone terrace, the edge of the infinity "
         "pool, the umbrella pines and the turquoise sea to the horizon. A pale polished travertine floor. This one glass "
         "wall is the only glass in the room; it is all one room, and nobody else is in it. The glass is clean and clear "
         "and the bright view shows straight through it, with no reflection of him or of the room in it."),
        (EL + " stands inside the room on the travertine floor, a couple of steps from where he stood in reference "
         "image #1: just past the end of the piano keyboard, with the piano to his left, about sixty centimetres in front "
         "of the glass wall, on the room side of its bronze floor track, with a clear strip of travertine floor between "
         "his loafers and the foot of the glass, about three and a half metres from the camera. He is seen from behind, "
         "his back mostly to the camera: his shoulders and hips are turned about thirty degrees to his right, towards the "
         "glass, his weight on one leg, his arms relaxed at his sides. He has calmly turned his head about forty degrees "
         "further to his right to look out through the glass towards the pines and the sea; the turn comes easily from "
         "his neck and upper back together, his chin level, his neck relaxed, his head upright. From the camera his face "
         "is seen from behind and to the side, in a soft lost profile: his right ear, the side of his hair, the curve of "
         "his right cheekbone and his jawline down to his chin, the outer corner of his right eye with its lashes, the "
         "end of his brow and the tip of his nose beyond his cheek. He fills a little over half the height of the frame, "
         "standing right of centre."),
        ("Soft late-morning daylight; the sun is high and behind the house, out of view, so there is no glare on the "
         "water and no sunbeams in the room. The only light is the daylight coming through that one glass wall, soft and "
         "even as in reference image #1, falling gently on the right side of his face. The view is the brightest part of "
         "the picture but keeps its colour and detail; the room and his back are about one and a half stops darker, "
         "clearly readable, and the gilet and trousers read as dark anthracite grey, not black. Muted natural colour, "
         "soft contrast, no HDR, not a silhouette."),
        ("His face is the face of the man introduced above: the same young man in his mid-twenties, seen from behind and "
         "to the side. His hair is the clearest sign of him: warm chestnut-brown (not espresso, not near-black) with "
         "lighter warm strands where the daylight catches it, full and swept back with soft natural volume, the sides "
         "combed back over the tops of his ears and the back tapered naturally with scissors to just above his collar; "
         "no fringe falling forward, no fade, no shaved sides, no pompadour. A strong, straight brow; a clean, defined "
         "jaw with only a faint stubble shadow along it (never dense stubble or a beard); dark warm brown eyes (never "
         "blue or grey). His face is exactly as sharp, as softly lit and as finely textured as his ear and neck at that "
         "distance, not brighter, smoother or sharper than the rest of him."),
        ("He wears only these ModernoMilano pieces, reproduced exactly as in the product reference images:\n"
         + SET["text"] + "\n- MILANO SUEDE LOAFER - GRIGIO, exactly as in reference images #3 (from behind) and #4 "
         "(from the side): mid-grey suede slip-on loafers with a smooth vamp and only a stitched moc-toe seam, no strap, "
         "no saddle and no penny slot, a flat off-white rubber sole, worn on bare feet without socks, a mirrored left and "
         "right pair."),
        ("Seen from behind: the gilet with the dark ANTHRACITE side out. The zip and the two welt pockets are on the "
         "front and are not visible from behind; the back panel is one plain piece of anthracite fabric with no zip, "
         "pocket, label or logo, exactly as in reference image #2, ending in the elasticated hem, and the stand collar is "
         "plain anthracite at the back and the right side of his neck, beside his turned jaw. No light pietra stone shows "
         "anywhere on the gilet from behind, and the armhole edges are dark anthracite. The short sleeves of the light "
         "pietra T-shirt come out of the deep armholes, and its hem hangs loose a few centimetres below the gilet hem, "
         "untucked all the way round. The slim anthracite trousers have a plain seat with no back pockets and no belt, "
         "ending just above the ankle bone; bare skin shows at the backs of both ankles. From behind, the loafers show "
         "plain rounded grey suede heels with a single fine centre-back seam, no heel tab, no pull loop and no logo, the "
         "low topline just below his bare heels."),
        ("The gilet is a SLEEVELESS bodywarmer, cut like the gilet in reference image #2: its armholes are cut deep and "
         "sit clearly inward of his shoulder points, so on both sides the T-shirt's shoulder seam and the top of its "
         "short sleeve are plainly visible outside the gilet, and the dark anthracite armhole edges lie flat on the "
         "T-shirt."),
        ("Reference image #2 shows only the clothing; the man wearing it there is a different person, so his head and "
         "hair are not copied."),
        PIANO, f"{HANDS} He is the only person in the picture.",
        ("An unretouched photograph. Fine real skin texture, matte, with no glow and no airbrushing. The clothes are "
         "real fabric with soft natural creases. Real optics: full-frame digital camera, natural depth of field: he, the "
         "piano and the room are sharp; the view beyond the glass is a little softer with distance and haze. No "
         "borders, no frame, no text, no logos."),
        "Full-frame digital camera, 35mm lens at f/8."], [job_start, SET_BACK, LOAFER_REAR, LOAFER_SIDE])


# Startbeeld 87, alleen de toetsen (controle echtheid, 10 okt): de zwarte toetsen staan in een gelijkmatige rij, zonder
# groepjes van 2 en 3, en dat is op telefoongrootte te zien. De eigenaar heeft 87 goedgekeurd, dus alleen deze correctie.
def keys_fix(job_start=START_JOB):
    return req([
        ("The same photograph as reference image #1, unchanged in every way: the same man, the same arm and hand with the "
         "same fingers in the same position, the same clothes, the same grand piano, the same window, the same light, the "
         "same angle, framing and blur. Correct only the piano keyboard so that it is a real piano keyboard: the black keys "
         "are in alternating groups of two and three, with a clearly wider gap between the groups where two white keys meet "
         "with no black key between them, exactly as on every real piano. The white keys, the red felt strip and the black "
         "lacquer stay as they are."),
        "No borders, no frame, no text, no logos."], [job_start])


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


# Video: één doorlopende take van startbeeld 87 naar het eindbeeld (ronde 3: villa aan zee, van achteren).
# - Niet slow motion (wens eigenaar): tempo en tijdstippen staan uitgeschreven, want Seedance maakt uit zichzelf trage
#   beweging.
# - Camerapad (critici, 10 okt): hij draait naar zijn rechterhand, met zijn rug naar de camera. De camera trekt terug,
#   stijgt van heuphoogte naar borsthoogte en draait een kwartslag naar rechts, met een zachte start en een zacht einde.
# - Geen gezichtsreferenties: zijn gezicht komt nooit in beeld en gezichtsreferenties trekken het hoofd naar de camera.
# - Geen hand in de zak.
VIDEO_PROMPT = (
    "One single unbroken shot in real time, at a normal, natural pace, not slow motion, with a single smooth camera move "
    "that starts gently and ends gently: no cut, no dissolve, no fade and no change of scene; it is the same villa room "
    "from the first frame to the last, with the same terrace, infinity pool and sea outside the same bronze-framed "
    "windows. It opens exactly on the start frame: a vertical shot from his shoulders to his shins, "
    "his head above the top of the frame, as he stands at the end of the keyboard of the black lacquered grand piano "
    "facing it, his left side to the camera and his left hand on the white keys, with the tall bronze-framed windows "
    "behind him on the right. For the first second the camera is almost still while his index finger presses one key "
    "softly. Then he lifts his hand from the keys, turns to his right, away from the camera, until his back is to the "
    "camera, and walks with four relaxed steps at a normal walking pace away from the camera, along the window wall on "
    "the right, to the glass corner at the far end of the same room, where he stops close to the glass and looks out over the bay, exactly as "
    "in the end frame, by about the sixth second. As he turns, the camera starts one steady, continuous move at an even "
    "speed: it pulls back on a smooth dolly, rising gently from hip height to chest height and turning slowly a little to "
    "the right to keep him in the picture, so that the piano leaves the picture on the left and more and more of him, the "
    "tall windows and the room come into view, and the soft view of the terrace, the pool and the sea outside the glass "
    "becomes sharper and wider. His head comes into view from behind; his face stays turned away from the camera the whole "
    "time, and at the glass his head stays turned towards the sea in the same lost profile, never further towards the "
    "camera. The grand piano and the curtained window bay of the start frame pass out of the picture on the left early "
    "in the turn; they do not fade or change into the glass walls or the furniture. Only after the piano has left the "
    "picture do the soft corner of the linen sofa and the travertine table come into the left foreground. The glass "
    "corner, the pale vase with the olive tree, the sofa and the table are standing in the room all along: they slide "
    "into view from the edges of the picture as the camera moves, solid and opaque, and never fade in, appear out of "
    "nothing or show through the glass. The window panes stay clear glass with no transparent overlay. He stops just "
    "beside the pale ceramic vase with the olive tree, his right hand hanging close to it without touching the leaves. "
    "Over the last two seconds the camera slows smoothly and comes to rest behind him, exactly on the end frame, while "
    "he stands relaxed at the glass with his arms at his sides. The terrace, the beach and the bay stay empty: no people "
    "and no boats appear. He is the same man in the same "
    "clothes from the first frame to the last, in the same colours: the sleeveless gilet stays dark anthracite outside, "
    "and its armhole edges "
    "stay dark anthracite with no light pietra showing at the armholes, also when his arms swing as he walks; it hangs "
    "open over the light pietra T-shirt, which stays loose and untucked at the same length, with the slim anthracite "
    "trousers and the mid-grey suede slip-on loafers with a plain vamp and an off-white sole on bare feet; his hands and "
    "wrists stay bare. Soft daylight from the windows, natural motion blur.")


# Gekozen eindbeeld (controle 10 okt): 94, de bewerking van 93 met infinity pool, meubels en balkenplafond.
END_JOB = "4d7fdf1b-1093-4b13-aea5-e685537506af"


# Startbeeld voor de video: 97, de bewerking van 87 met de villa (zwembad, pijnbomen, zee) achter het raam.
VIDEO_START = "ce72c67f-805a-411f-bf9a-4b71b2bdb17e"


def video(end_job=END_JOB, draft=True, resolution="480p", duration=8, draft_job=None, start_job=VIDEO_START):
    medias = [{"role": "start_image", "value": start_job}, {"role": "end_image", "value": end_job}]
    p = {"model": "seedance_2_5", "mode": "omni_reference", "resolution": resolution, "draft": draft,
         "bitrate_mode": "high", "duration": duration, "aspect_ratio": "9:16", "generate_audio": False,
         "prompt": VIDEO_PROMPT, "medias": medias, "declined_preset_id": PRESET_DECLINE}
    if draft_job:
        p.update(resolution="1080p", draft=False, draft_job_id=draft_job)
    return p


# Video versie 2 (10 s): startbeeld 97 en het eindbeeld van end_frame5, één kamer. Een rechte camerabeweging terug
# langs dezelfde lijn. Hij loopt recht de diepte in, met de glazen wand steeds rechts op afstand, en draait aan het
# eind zijn hoofd ongeveer 45 graden naar rechts. Zijn gezicht komt nu in beeld, dus de gezichtsreferenties gaan weer
# mee.
VIDEO2_PROMPT = (
    "One single unbroken shot in real time, at a normal, natural pace, not slow motion: one slow, steady dolly move "
    "straight back with a gentle rise and no pan, which starts gently and ends gently, with no cut, no dissolve, no fade "
    "and no change of scene. It is one and the same room from the first frame to the last: the black grand piano, the "
    "plain white plaster wall behind it, the flat white ceiling and the single wall of bare bronze-framed glass on the "
    "right stay exactly where they are and keep their shape; nothing new appears in the room. It opens exactly on the "
    "start frame: a close shot of his left arm and hand on the white keys at the end of the keyboard, the glass wall "
    "behind him on the right. In the first second his index finger presses one key softly. Then he lifts his hand from "
    "the keys and turns calmly to his right, away from the camera, towards the glass wall that is behind him, and takes "
    "two or three unhurried steps to it at a normal walking pace; he stops on the travertine floor about sixty "
    "centimetres in front of the glass, on the room side of its bronze floor track, with a clear strip of floor between "
    "his loafers and the glass. He never touches or passes through the glass and stays inside the room. All the while "
    "the camera dollies straight back about two metres along its own line and rises from hip height to chest height, so "
    "the piano stays in view on the left and more and more of the same room and of him comes into view, until his whole "
    "figure is in the picture. By about the sixth second he stands still, his back mostly to the camera and his "
    "shoulders turned a little towards the glass, his arms relaxed at his sides. Then, over about two seconds, he calmly "
    "turns his head to his right to look out through the glass at the pines and the sea, so his face is seen softly "
    "from behind and to the side: his ear, his cheekbone, his jaw and the tip of his nose; his body stays still and his "
    "neck relaxed. For the last second the camera comes to rest exactly on the end frame and he holds the pose, "
    "breathing softly. He is the man in the start and end frames and in the reference images; use the reference images "
    "only for his face and hair. He keeps the same face, hair and clothes throughout, in the same colours: the "
    "sleeveless gilet stays dark anthracite outside, its armhole edges stay dark anthracite with no light pietra showing "
    "at the armholes, also when his arms move; it hangs open over the light pietra T-shirt, which stays loose and "
    "untucked at the same length, with the slim anthracite trousers and the mid-grey suede slip-on loafers with a plain "
    "vamp and an off-white sole on bare feet; his hands and wrists stay bare. The terrace, the pool and the sea stay "
    "empty: no people and no boats appear, and the glass stays clear with no reflection of him or of anyone. Soft "
    "daylight from the glass wall, natural motion blur.")


def video2(end_job, draft=True, duration=10, draft_job=None, start_job=START_VILLA):
    faces = [r["upscale_job_id"] for r in HF["face_refs"] if any(r["file"].endswith(f"/{x}.jpg") for x in HF["video_face_refs"])]
    medias = ([{"role": "start_image", "value": start_job}, {"role": "end_image", "value": end_job}]
              + [{"role": "image_references", "value": f} for f in faces])
    p = {"model": "seedance_2_5", "mode": "omni_reference", "resolution": "480p", "draft": draft, "bitrate_mode": "high",
         "duration": duration, "aspect_ratio": "9:16", "generate_audio": False, "prompt": VIDEO2_PROMPT,
         "medias": medias, "declined_preset_id": PRESET_DECLINE}
    if draft_job:
        p.update(resolution="1080p", draft=False, draft_job_id=draft_job)
    return p


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "end":
        out = [{"index": 80 + v, "params": end_frame()} for v in range(2)]
    elif cmd == "start":
        base = int(args[1]) if len(args) > 1 else 82
        out = [{"index": base + v, "params": start_frame(args[0])} for v in range(2)]
    elif cmd == "video2":
        # video2 <job eindbeeld> [<concept job> voor 1080p]
        out = [{"index": 0, "params": video2(args[0], draft_job=args[1] if len(args) > 1 else None)}]
    elif cmd == "end6":
        out = [{"index": 110 + v, "params": {**end_frame6(), "resolution": "2k"}} for v in range(int(args[0]) if args else 3)]
    elif cmd == "end5":
        out = [{"index": 100 + v, "params": {**end_frame5(), "resolution": "2k"}} for v in range(int(args[0]) if args else 2)]
    elif cmd == "startvilla":
        out = [{"index": 97 + v, "params": {**start_villa_edit(), "resolution": "2k"}} for v in range(2)]
    elif cmd == "grand":
        # 3 beelden op 2k: 93 bewerkt, een nieuwe variant met dubbele hoogte, en de toetsen van 87
        out = [{"index": 94, "params": {**end_grand_edit(), "resolution": "2k"}},
               {"index": 95, "params": {**end_frame4(START_JOB), "resolution": "2k"}},
               {"index": 96, "params": {**keys_fix(), "resolution": "2k"}}]
    elif cmd == "end3":
        out = [{"index": 92 + v, "params": {**end_frame3(args[0]), "resolution": "2k"}} for v in range(2)]
    elif cmd == "end2":
        out = [{"index": 90 + v, "params": {**end_frame2(args[0]), "resolution": "2k"}} for v in range(2)]
    elif cmd == "video":
        # video <job eindbeeld> [draft|720p|<concept job>] [seconden]
        end_job, mode, dur = args[0], (args[1:] + ["draft"])[0], int((args[1:] + ["draft", "8"])[1])
        if mode == "draft":
            params = video(end_job, duration=dur)
        elif mode == "720p":
            params = video(end_job, draft=False, resolution="720p", duration=dur)
        else:
            params = video(end_job, duration=dur, draft_job=mode)
        out = [{"index": 0, "params": params}]
    elif cmd == "shoes":
        # 2k: genoeg voor een video-eindbeeld (1080p) en 2 credits in plaats van 4 (10 okt)
        out = [{"index": 88 + v, "params": {**shoes_fix(args[0]), "resolution": "2k"}} for v in range(2)]
    else:
        raise SystemExit(__doc__)
    print(json.dumps(out, ensure_ascii=False))
