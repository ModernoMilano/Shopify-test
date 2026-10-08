"""Serie "Una giornata": vier video's in de stijl van reel Total Bordeaux (8 okt 2026). Luca in elke video, geen tekst,
het logo de laatste 2 s. Het draaiboek staat in VIDEOS4.md.

Producten (eigenaar): Reverso Total Antracite, Reverso Blu & Crema, Nobile Set (op een oude boot op het Comomeer) en
Knitted Two-Tone Cashmere Set Dark Mocha. Eerst alle startbeelden ter goedkeuring (eigenaar, 8 okt).

Gebruik:
  python3 -I videos4.py starts                    -> ronde 1: requests voor generate_image_batch (2 varianten per beeld)
  python3 -I videos4.py como_b <job como_a> [left|right]  -> ronde 2: shot B op de boot, dichterbij (bewerking van como_a)
  python3 -I videos4.py mocha_a <job mocha_b>     -> ronde 2: shot A van Dark Mocha, het detail (bewerking van mocha_b)
  python3 -I videos4.py reverse <antracite|blu> <media laatste frame A>  -> startbeeld B van een Reverso-video
  python3 -I videos4.py draft <shot> [start]     -> Seedance 2.5, concept 480p (shot: como_a, como_b, antracite_a, ...)
  python3 -I videos4.py final <shot> <start> <draft_job>  -> afmaken in 1080p
  python3 -I videos4.py prompts                   -> alle Seedance-requests, voor de voorcontrole

Lessen uit reel_tb.py (README): een vaste camera voor een shot met logo of een snede op de beweging; de binnenkleur van
een Reverso-gilet alleen in de kraag en langs de open voorkant, niet bij de armsgaten; diepe armsgaten zodat een gilet in
dezelfde kleur als de tee toch een bodywarmer blijft; de flat-lay van een Reverso-set niet als referentie (daar zijn de
armsgaten wel in de binnenkleur afgewerkt).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MODEL = json.load(open(os.path.join(ROOT, "creative-engine", "data", "model.json")))
P, HF = MODEL["prompt"], MODEL["higgsfield"]
EL = HF["element_placeholder"]

ID_LINE = ("He is in his mid-twenties, with only a faint stubble shadow (never dense stubble or a beard), dark warm brown eyes "
           "(never blue or grey) and warm chestnut-brown hair (not espresso, not near-black), full and swept back with soft natural "
           "volume, the sides combed back over the tops of his ears; no fringe falling forward, no fade, no shaved sides, no pompadour.")
HANDS = "His hands and wrists are bare: no watch, no ring, no bracelet, no glasses, no bag."
REAL = P["realism_en"]  # met "visible knit stitch": goed voor de cashmere van Nobile en Dark Mocha
REAL_SMOOTH = REAL.replace("The clothes are real fabric with visible knit stitch and soft creases at the elbows and waist.",
                           "The clothes are real fabric with soft natural creases at the waist and where the gilet folds.")
# Controle 8 okt (como_a-8): een geëtst merkteken met letters op het glas van de voorruit.
NO_BADGES = ("The boat has no badges, emblems, lettering or numbers anywhere; the glass of its windscreen is completely "
             "clean and clear, with no etched marks or lettering.")

# ---------- Producten (media-ids uit higgsfield-media.json, productfoto's bekeken op 8 okt) ----------
NOBILE = dict(refs=["1b62527d-d857-4a1c-91e3-8f5899a41e99", "647b6ea6-c23b-4fa4-995e-98e483d1a55d",
                    "dfca0fc8-5302-4b47-a91c-8fc60900a569"],  # flat-lay, detail, aan het model
              text="MILANO NOBILE SET, all black:\n"
                   "- MILANO CASHMERE PIENO GILET - NERO: a sleeveless black 100% cashmere knit gilet with a ribbed stand "
                   "collar whose inside is dark charcoal grey, a full-length dark silver zip, two vertical welt pockets, ribbed "
                   "armholes and a ribbed hem.\n"
                   "- MILANO CASHMERE LIDO - NERO: a black long-sleeve 100% cashmere knit polo with a pointed collar, a "
                   "three-button placket with grey buttons, ribbed cuffs and hem.\n"
                   "- MILANO CLASSICO PANTS - BLACK: black trousers with a mid-rise elastic waistband, a black drawstring with "
                   "silver tips and a straight leg with a pressed crease.")
# flat-lay met witte tee (dark_mocha.png), jas gevouwen (16.45.40), broek (16.45.52). Niet 16.46.06: dat is een stapel
# in vier kleuren (grijs, navy, mokka, zwart); in ronde 1 ging die per ongeluk mee en werd de jas grijs.
MOCHA = dict(refs=["02e95ddd-e359-4a62-a941-71fac89ed20a", "20b8df67-28ef-4573-b678-2e2da7cd3759",
                   "55caff72-82fe-4f91-9b96-e2185fde5641"],
             # Ronde 1 (8 okt): de jas werd grijs en kreeg koordjes aan de capuchon die het product niet heeft.
             text="MILANO KNITTED TWO-TONE CASHMERE SET - DARK MOCHA, in a soft cashmere knit in a warm dark mocha brown, "
                  "the deep coffee brown of reference images #1 and #2: clearly brown, never grey or taupe:\n"
                  "- A full-zip hooded knit jacket with a dark silver zip; the opening of the hood is edged with a cream band "
                  "that runs down to the top of the zip; the hood has no drawstrings and no cords; two thin cream stripes run "
                  "down the outer side of each sleeve from the shoulder to the cuff; ribbed cuffs and a ribbed hem.\n"
                  "- Matching knit trousers with a drawstring waist and a wide and a thin cream stripe down the outer side of "
                  "each leg.\n"
                  "- Under the jacket, the PURO SUPIMA MERCER TEE - WHITE: a plain white crew-neck T-shirt in smooth "
                  "mercerised Supima cotton, as in reference image #1.")


def reverso(name, outside, inside, tee, trousers, refs):
    return dict(refs=refs, outside=outside, inside=inside, text=(
        f"MILANO REVERSO SET {name}, three pieces:\n"
        "- A lightweight, unpadded, fully reversible sleeveless gilet in a smooth matte technical fabric with a soft peached "
        f"surface (no quilting, no puffiness): one side {outside}, the other side {inside}; a stand collar, a full-length silver "
        "zip, two slanted welt pockets on the lower front panels and an elasticated hem.\n"
        f"- A plain {tee} crew-neck T-shirt in smooth mercerised cotton with a subtle sheen, short sleeves, no print.\n"
        f"- {trousers[0].upper() + trousers[1:]} trousers in the same smooth matte fabric as the gilet: an elasticated "
        "waistband with belt loops, slanted side pockets, a slim tapered leg."))


# refs: aan het model met de buitenkant (voorkant), detail van kraag en rits, "reversed". Geen flat-lay (zie docstring).
ANTRACITE = reverso("TOTAL ANTRACITE", "dark anthracite grey", "light pearl grey", "dark anthracite grey", "dark anthracite grey",
                    ["31a727e2-62d2-4c9d-a63a-a0d53e6c2372", "e476e5bf-9c42-4d22-9645-e572c44a1ffd",
                     "c5e5fce7-bc65-4c6a-997d-4e2ed9d6c1c4"])
BLU = reverso("BLU & CREMA", "deep navy blue", "cream", "cream", "deep navy blue",
              ["a9e4ee85-c230-4928-b64e-d9b13e374f8b", "eaaca997-31d2-44f3-bed3-d69d9054f6f2",
               "288e4e34-8aab-431b-a34a-fff860a2f909"])


def sleeveless(outside, inside, ref_n):
    """Regel van de eigenaar (8 okt): binnenkleur alleen in de kraag en langs de open voorkant, niet bij de armsgaten."""
    return (f"The gilet is a SLEEVELESS bodywarmer, cut like the gilet in reference image #{ref_n}. Its armholes are finished "
            f"in {outside}, the same colour as its outside: no {inside} shows at the armholes at all; the {inside} inside "
            "shows only inside the stand collar and along the open front edges. It reads unmistakably as a sleeveless "
            "bodywarmer: the armholes are cut deep and sit clearly inward of his shoulder points, so on both sides the "
            "T-shirt's shoulder seam and the top of its short sleeve are plainly visible outside the gilet, with a soft shadow "
            "line where the gilet's armhole edge lies over the T-shirt. The gilet is a matte, peached, slightly thicker fabric "
            "that stands a little away from the body at the armhole; the T-shirt is a thinner jersey with a subtle sheen, so "
            "the two layers are easy to tell apart. The T-shirt sleeve ends in its own hemmed edge on the upper arm. The "
            "T-shirt hangs loose and untucked over the trousers and covers the waistband.")


def req(parts, medias):
    m = [{"value": v, "role": "image_references"} for v in medias]
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": "9:16", "prompt": "\n\n".join(parts), "medias": m}


def person(scene, light, product, worn, extra, real, lens):
    """Licht, uitsnede en uitdrukking vooraan; de kledingregels erachter (SKILL.md, "Echt, niet AI")."""
    return [scene, light, f"Expression: {P['expression_en']}.", P["keep_en"], ID_LINE,
            "He wears only these ModernoMilano pieces, reproduced exactly as in the product reference images:\n" + product["text"],
            f"How they are worn: {worn}"] + extra + [f"{HANDS} He is the only person in the picture.", real, lens]


START = {
    # 1. "Il lago", late middag: de Nobile Set op een oude houten motorboot die over het Comomeer glijdt (wens eigenaar).
    #    Shot A: de camera vaart naast de boot mee. Shot B (como_b): dichterbij, op de boot zelf.
    "como_a": lambda: req(person(
        scene=("Late afternoon on Lake Como, near Varenna. An old varnished mahogany motor launch from the 1960s, with cream "
               "leather seats, a low chrome-framed windscreen and a thin wooden steering wheel, glides slowly across the calm "
               "lake, a soft white wave folding away from its bow. " + EL + " sits alone at the wheel, his left hand resting "
               "on the thin wooden steering wheel, his right forearm resting along the varnished side of the boat, looking "
               "ahead along the lake past the camera on his left; the breeze of the boat's slow speed lifts his hair a little. "
               "The camera travels alongside on another boat at the same speed, slightly ahead of him and just above the "
               "water. Framed vertically from just above his head down to the varnished hull and the water streaming past it; "
               "he and the boat fill the lower two thirds of the frame, the blue-grey mountains and the faint colours of the "
               "village far behind across the water, soft and out of focus. The lake around the boat is empty."),
        light=("Warm low sun from behind him on the right puts a soft warm rim on his hair and shoulders and glitters on the "
               "water; his face is in soft light reflected from the lake; the mountains behind are a stop darker in a soft "
               "haze; muted warm colour, soft contrast, no HDR."),
        product=NOBILE,
        worn=("the black Pieno gilet zipped halfway up over the black Lido polo, the polo's pointed collar lying flat inside "
              "the gilet's stand collar with its top button open, the polo's long sleeves down to the ribbed cuffs; the black "
              "trousers. His feet are not in the picture."),
        # Ronde 1 (8 okt): zwart op zwart las het gilet als een jasje; de geribde armsgaten moeten zichtbaar zijn.
        extra=["The gilet is clearly sleeveless: its ribbed armholes sit just inside his shoulders and the polo's long knit "
               "sleeves come out of them; the gilet's thicker knit and the polo's finer knit are easy to tell apart, and the "
               "low sun catches the ribbed edge of each armhole.", NO_BADGES],
        real=REAL, lens="Full-frame digital camera, 50mm lens at f/2.8."), NOBILE["refs"]),

    # 2. "Pioggia", grijze ochtend: Total Antracite onder de arcade van een rationalistisch gebouw in Milaan, regen erachter.
    #    Shot A: de camera schuift van achter een zuil vandaan en laat hem zien. Snede op de beweging naar het lichtgrijze gilet.
    "antracite_a": lambda: req(person(
        scene=("A rainy grey morning in Milan, under the arcade of a 1930s rationalist building: tall square pillars clad in "
               "pale grey stone and a smooth grey stone floor, dry under the arcade. Beyond the arcade a steady rain falls in "
               "fine silver lines on the empty wet street and the dark facades opposite, soft and out of focus. " + EL + " "
               "stands at the edge of the arcade, just out of the rain, his body turned three-quarters to the camera, his "
               "weight on one leg, both hands in his trouser pockets, his head turned to the street, looking out at the rain "
               "past the camera on his left. The camera stands a few metres away inside the arcade at chest height, the soft "
               "grey edge of a pillar in the foreground covering the right edge of the frame. Framed vertically from just "
               "above his head to mid-thigh, off-centre to the left."),
        light=("Soft grey daylight from the open street falls on his face and the front of the gilet; the arcade behind him "
               "is a stop darker; cool, muted grey colour with soft contrast, no HDR."),
        product=ANTRACITE,
        worn=("the gilet with the dark ANTHRACITE side out, hanging open; the dark anthracite T-shirt; the dark anthracite "
              "trousers."),
        extra=[sleeveless("dark anthracite grey", "light pearl grey", 1)], real=REAL_SMOOTH,
        lens="Full-frame digital camera, 50mm lens at f/2."), ANTRACITE["refs"][:2]),

    # 3. "Giardino", late ochtend: Blu & Crema aan het zwembad van een villa uit de jaren dertig in Milaan. Shot A: hij
    #    trekt de rits van het navy gilet op van zijn middel tot halverwege de borst. Snede op de beweging naar crème.
    "blu_a": lambda: req(person(
        scene=("Late morning in the garden of a 1930s Milanese villa: a long rectangular swimming pool with pale travertine "
               "edges, clipped box hedges, old magnolia trees, and behind them the villa's pale facade with tall dark green "
               "shutters, soft and out of focus. Nobody else is there. " + EL + " stands at the end of the pool on the "
               "travertine edge, his body turned three-quarters to the camera, looking down the length of the pool past the "
               "camera on his left. The gilet is zipped up only to his waist: his right hand holds the small silver zip pull "
               "just above his waist, about to pull it up; his left hand is in his trouser pocket. The camera stands low at "
               "the side of the pool, the calm water in the lower part of the frame, a few magnolia leaves soft in the "
               "foreground on the left. Framed vertically from just above his head to mid-thigh, off-centre."),
        light=("Soft late-morning sun filtered by the magnolias falls from the left on his face and the front of the gilet; "
               "faint reflections from the water play on the travertine; the garden behind him lies in the soft shade of the "
               "trees, a stop darker; muted fresh colour, soft contrast, no HDR."),
        product=BLU,
        worn=("the gilet with the deep NAVY side out, zipped up only to his waist, so its front stands open above the zip "
              "over the cream T-shirt; the navy trousers."),
        extra=[sleeveless("deep navy blue", "cream", 1)], real=REAL_SMOOTH,
        lens="Full-frame digital camera, 50mm lens at f/2."), BLU["refs"][:2]),

    # 4. "Sera", blauw uur: Dark Mocha in een leren fauteuil bij het raam van een oud appartement in Milaan.
    #    Dit is shot B (met gezicht, logo). Shot A, het detail van de mouw, is een bewerking hiervan (mocha_a).
    "mocha_b": lambda: req(person(
        scene=("Evening in an old Milan apartment at the blue hour: walnut panelling, a herringbone parquet floor, a warm "
               "brass floor lamp, and on the right of the frame a tall window with thin dark frames, the deep blue dusk and "
               "the small warm lights of the city far behind the glass, out of focus. Nobody else is there. " + EL + " sits "
               "back in a worn cognac leather armchair beside the window, his body turned three-quarters to the camera, his "
               "right forearm resting along the armrest with the hand hanging relaxed over its end, his left hand resting on "
               "his thigh, his head turned towards the window, looking out past the camera on his right. The camera is close, "
               "about two metres from him: framed vertically from just above his head to his knees, his face large in the "
               "frame, off-centre to the left, the soft edge of a linen curtain in the foreground on the right."),
        light=("Lit only by the warm floor lamp on his left: a soft warm glow on his face and on the knit, which glows a warm "
               "coffee brown and shows every stitch; the cool blue dusk in the window is a few stops darker; muted warm "
               "colour, soft contrast, no HDR."),
        product=MOCHA,
        worn=("the hooded knit jacket zipped up to the middle of his chest over the white T-shirt, the hood lying flat at "
              "the back of his neck, its cream edge framing his neck; the cream stripes running down both sleeves; the "
              "matching trousers with the stripes down each leg. His feet are not in the picture."),
        extra=[], real=REAL, lens="Full-frame digital camera, 50mm lens at f/2."), MOCHA["refs"]),
}


def como_b(job_a, side="right"):
    """side: de kant van het beeld waar hij in como_a naar kijkt, zodat de kijkrichting over de snede gelijk blijft."""
    parts = [
        f"The same scene as reference image #1, a moment later, seen from a second camera: the same man ({EL}), the same old "
        "mahogany motor launch gliding across Lake Como, the same late-afternoon light and the same clothes. The camera is now "
        "on the boat itself, fixed on the deck beside the windscreen, and frames him from just above his head to the middle "
        f"of his chest; his face is in three-quarter profile turned to the {side} of the frame, looking ahead over the lake. "
        "Behind him the water glitters in the low sun and the far mountains are soft and out of focus.",
        "The same light as reference image #1: the warm low sun behind him puts a soft warm rim on his hair and shoulder, his "
        "face is in soft light reflected from the lake; muted warm colour, soft contrast, no HDR.",
        f"Expression: {P['expression_en']}.", P["keep_en"], ID_LINE,
        "He wears only these ModernoMilano pieces, exactly as in reference image #1 and the product reference images:\n"
        + NOBILE["text"],
        "How they are worn: exactly as in reference image #1: the gilet zipped halfway up over the polo, the polo's pointed "
        "collar lying flat inside the gilet's stand collar.",
        NO_BADGES, f"{HANDS} He is the only person in the picture.", REAL, "Full-frame digital camera, 85mm lens at f/2."]
    return req(parts, [job_a] + NOBILE["refs"][1:])


def mocha_a(job_b):
    parts = [
        "A close detail from the same scene as reference image #1: the same armchair, the same warm lamp light, the same "
        "clothes. The camera is close beside the armchair and frames only his right forearm and his relaxed bare hand resting "
        "on his thigh, as in reference image #1: the sleeve of the dark mocha knit jacket with its cream stripes running down "
        "to the plain ribbed cuff, the side of the jacket and the knit trousers beside it, the cognac leather of the armchair "
        "soft behind. His face is not in the picture. "
        "The warm lamp light rakes across the knit and shows every stitch and the soft halo of the cashmere fibres; behind, "
        "the dark window with the blurred warm lights of the city.",
        "The pieces are these ModernoMilano pieces, reproduced exactly as in the reference images:\n" + MOCHA["text"],
        f"{HANDS} Natural hand with real skin texture and relaxed fingers.", REAL,
        "Full-frame digital camera, 100mm macro lens at f/2.8."]
    return req(parts, [job_b] + MOCHA["refs"][1:])


def reverse(video, last_frame):
    prod = {"antracite": ANTRACITE, "blu": BLU}[video]
    o, i = prod["outside"], prod["inside"]
    parts = [
        f"The same photograph as reference image #1: the same man ({EL}), the same place, the same pose, the same direction of "
        "his head and eyes, the same light, lens and framing. Only one thing changes: he now wears the gilet REVERSED, with "
        f"the {i.upper()} side out, exactly as in reference image #2. The {o} side is now the inside: it shows only inside the "
        "stand collar and along the open front edges. The gilet is zipped or open exactly as far as in reference image #1.",
        "The T-shirt hangs loose and untucked over the trousers exactly as in reference image #1, at exactly the same length: "
        "its hem fully covers the waistband of the trousers. Everything except the gilet is identical to reference image #1.",
        f"The gilet is clearly a sleeveless bodywarmer: its armholes are finished in {i} like the rest of the outside, with no "
        f"{o} at the armholes; the short sleeves of the T-shirt come out from under the armholes.",
        P["keep_en"], ID_LINE,
        "The pieces are these ModernoMilano pieces, reproduced exactly as in the reference images:\n" + prod["text"],
        f"{HANDS} He is the only person in the picture.", REAL_SMOOTH, "Full-frame digital camera, 50mm lens at f/2."]
    return req(parts, [last_frame, prod["refs"][2]])


# ---------- Video (Seedance 2.5, model.json rules.video; lessen in README.md) ----------
PRESET_DECLINE = "24bae836-2c4a-48e0-89b6-49fcc0b21612"
# Goedgekeurde startbeelden (controle 8 okt). Como A is een bijsnede van job afc686cd (zonder het merkteken op de ruit).
START_IMG = {
    "como_a": "304515f9-5388-4a7b-a8c2-5f06eb77a44d",
    "como_b": "7292b98e-3543-489b-88e2-727ac10f9835",
    "antracite_a": "6f98f485-59f7-4e29-a5a0-baf6c7789207",
    "blu_a": "b3851105-101c-41c6-9e16-ad4e5ad5abf2",
    "mocha_a": "98e8323c-ebb0-4e04-82cc-1d0391ab05e7",  # detail 2 (detail 1 afgekeurd: broek zonder streep)
    "mocha_b": None,  # bijsnede van job 7782c3c1
}
LOCKED = ("The shot opens exactly on the start frame, with the same framing, background, head angle and closed lips. ")
SHOT = {
    # 1. Il lago. A: meevaren naast de boot. B: camera vast op de boot, logo de laatste 2 s.
    "como_a": dict(dur=4, face=True, take="one continuous take from the camera boat.",
        motion=("The old mahogany motor launch glides slowly forward to the right across the calm lake. The camera travels "
                "alongside on a second boat at the same speed, so he and the chrome windscreen frame at the lower right stay in "
                "the same place in the frame, while the lake water behind him streams slowly to the left and the far shore and "
                "the village drift slowly to the left. He stands at "
                "the windscreen, the forearm nearest the right of the frame resting on its chrome frame and his other hand in "
                "his trouser pocket, "
                "looking ahead along the lake to the right of the frame; the breeze gently lifts a few strands of his hair. "
                "He takes one slow breath and keeps looking ahead, calm, until the end of the shot."),
        clothes=("the black sleeveless knit gilet stays zipped halfway over the black long-sleeve knit polo for the whole "
                 "shot, its ribbed armholes at his shoulders, with the black trousers"),
        still="The lake stays calm around the boat."),
    "como_b": dict(dur=5, face=True, take="one continuous take from the camera fixed on the boat.",
        motion=(LOCKED + "The boat glides slowly forward to the right. The camera is rigidly fixed to the boat beside the "
                "windscreen, so he, the chrome windscreen frame and the wooden steering wheel at the lower right stay exactly "
                "in place in the frame for the whole shot; only the glittering water behind him streams slowly from right to "
                "left, while the distant mountains barely drift. He keeps looking ahead over "
                "the water to the right of the frame, and the breeze moves his hair a little. With a slow breath he lowers "
                "his eyes slightly towards the water, and by the third second he is still; for the last two seconds he "
                "stays calm, only breathing softly."),
        clothes=("the black sleeveless knit gilet stays zipped halfway over the black long-sleeve knit polo for the whole "
                 "shot, its ribbed armholes at his shoulders"),
        still="The lake stays calm and empty around the boat."),
    # 2. Pioggia. A: de camera schuift iets naar links, de zuil glijdt verder uit beeld. B: vaste camera, gilet omgekeerd.
    "antracite_a": dict(dur=4, face=True, take="one continuous take on a slow dolly.",
        motion=("The camera glides slowly a little to the left, so the soft pillar at the right edge of the frame slides "
                "further out of the picture, and the camera settles by the third second. He stands at the edge of the arcade "
                "with both hands in his trouser pockets, looking out at the rain over the street past the right edge of the "
                "frame; a steady rain falls in fine silver lines beyond the arcade onto the wet street. He slowly lifts his "
                "chin and eyes a little towards the falling rain, his face still turned to the right, then holds that look, "
                "calm and still, until the end of the shot."),
        clothes=("the sleeveless gilet stays dark anthracite outside, light pearl grey only inside the collar and along the "
                 "open front edges for the whole shot, over the dark anthracite T-shirt, with the dark anthracite trousers"),
        still=("Far across the street, the few small blurred figures under umbrellas stay small and soft in the distance. "
               "The arcade stays empty and quiet around him.")),
    "antracite_b": dict(dur=5, face=True, take="one continuous take from the fixed camera.",
        motion=(LOCKED + "The camera is locked off on a tripod and stays perfectly still for the whole shot. He keeps "
                "standing at the edge of the arcade with both hands in his trouser pockets, his gaze on the rain over the "
                "street past the right edge of the frame. With a slow breath he gently lowers his chin and eyes a little to "
                "the wet street, his face still turned to the right, and by the third second he is still; for the last two "
                "seconds he stays calm, only breathing softly. The rain keeps falling steadily beyond the arcade."),
        clothes=("the sleeveless gilet stays light pearl grey outside, dark anthracite only inside the collar and along the "
                 "open front edges for the whole shot, over the dark anthracite T-shirt, which hangs loose and untucked at the "
                 "same length throughout, with the dark anthracite trousers"),
        still=("Far across the street, the few small blurred figures under umbrellas stay small and soft in the distance. "
               "The arcade stays empty and quiet around him.")),
    # 3. Giardino. A: hij trekt de rits een stukje verder op en steekt de hand in zijn zak. B: vaste camera, crème buiten.
    "blu_a": dict(dur=4, face=True, take="one continuous take on a slow dolly.",
        motion=("With his right hand, which already holds the small silver zip pull at his chest, he slowly draws the zip "
                "of the navy gilet up in one smooth movement to just below his collarbone, while his left hand stays in his "
                "trouser pocket; the stand collar stays open with its cream inside. Then he lets go and slides his right hand "
                "into his right trouser pocket, his gaze staying past the left edge of the frame, as in the start frame. The "
                "camera pushes in slowly a few centimetres and settles by the third second; for the last second he holds "
                "still, calm."),
        clothes=("the sleeveless gilet stays deep navy outside, cream only inside the collar and along the open front "
                 "edges for the whole shot, over the cream T-shirt, with the deep navy trousers"),
        still="The garden stays quiet; the water of the pool barely moves."),
    "blu_b": dict(dur=5, face=True, take="one continuous take from the fixed camera.",
        motion=(LOCKED + "The camera is locked off on a tripod and stays perfectly still for the whole shot. He keeps "
                "standing at the end of the pool with both hands in his trouser pockets, looking off to the left of the frame "
                "past the camera. A light breeze stirs the magnolia leaves and soft reflections ripple on the water. With a "
                "slow breath he lifts his chin slightly, his face still turned to the left, and by the third second he is "
                "still; for the last two seconds he stays calm, only breathing softly."),
        clothes=("the sleeveless gilet stays cream outside, zipped up to just below his collarbone exactly as in the start "
                 "frame, deep navy only inside the collar and along the open front edges above the zip for the whole shot, "
                 "over the cream T-shirt, which hangs loose and untucked at the same length throughout, with the deep navy "
                 "trousers"),
        still="The garden stays quiet around him."),
    # 4. Sera. A: macro van mouw en hand, zonder gezicht. B: vaste camera in de fauteuil, logo de laatste 2 s.
    "mocha_a": dict(dur=4, face=False, take="one continuous take with a macro lens.",
        motion=("A close detail shot of his hand resting on his thigh, the knit sleeve and ribbed cuff beside the cognac "
                "leather armrest. The camera pushes in very slowly towards his hand and the cuff, then settles, while the warm "
                "lamp light rakes across the knit. His fingers relax and move slightly once, then rest. The frame stays on "
                "his hand, the sleeve and the knit for the whole shot."),
        clothes=("the dark mocha brown knit sleeve keeps its cream stripes exactly as in the start frame, straight and "
                 "continuous down to the ribbed cuff"),
        still="The city lights stay soft and blurred behind the glass."),
    "mocha_b": dict(dur=5, face=True, take="one continuous take from the fixed camera.",
        motion=(LOCKED + "The camera is locked off on a tripod and stays perfectly still for the whole shot. He sits back "
                "in the cognac leather armchair, his right hand resting on his thigh, his face in profile turned to the right "
                "of the frame. With a slow breath he lifts his chin slightly, his face still turned to the right, and by the "
                "third second he is still; for the last two seconds he stays calm, only breathing softly. The small city "
                "lights twinkle softly far behind the glass."),
        clothes=("the dark mocha brown hooded knit jacket stays open and unzipped over the white T-shirt exactly as in the "
                 "start frame, its hood lying flat behind his neck with the opening edged only by the plain cream band, its "
                 "cream stripes running down the sleeves, with the matching dark mocha trousers and their cream side stripes"),
        still="The room stays quiet and still around him."),
}


def video(shot, start=None):
    c = SHOT[shot]
    start = start or START_IMG.get(shot)
    faces = [r["upscale_job_id"] for r in HF["face_refs"] if any(r["file"].endswith(f"/{x}.jpg") for x in HF["video_face_refs"])]
    who = ("He is the man in the start frame and in the reference images; use the reference images only for his face and "
           "hair. He keeps the same face, hair and clothes throughout: " if c["face"] else
           "He keeps the same clothes throughout: ")
    prompt = (f"{c['motion']} Small, natural movement. {who}{c['clothes']}. "
              + ("His face stays clear, his wrists bare. " if c["face"] else "His hand and wrist stay bare. ")
              + f"{c['still']} Real-time motion with natural motion blur, {c['take']}")
    medias = [{"role": "start_image", "value": start}]
    if c["face"]:
        medias += [{"role": "image_references", "value": f} for f in faces]
    return {"model": "seedance_2_5", "mode": "omni_reference", "resolution": "480p", "draft": True, "bitrate_mode": "high",
            "duration": c["dur"], "aspect_ratio": "9:16", "generate_audio": False, "prompt": prompt, "medias": medias,
            "declined_preset_id": PRESET_DECLINE}


def final(shot, start, draft_job):
    p = video(shot, start)
    p.update(resolution="1080p", draft=False, draft_job_id=draft_job)
    return p


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "starts":
        out = [{"index": 2 * n + v, "params": START[k]()} for n, k in enumerate(START) for v in range(2)]
    elif cmd in ("como_b", "mocha_a"):
        f = {"como_b": como_b, "mocha_a": mocha_a}[cmd]
        out = [{"index": v, "params": f(*args)} for v in range(2)]
    elif cmd == "reverse":
        out = reverse(args[0], args[1])
    elif cmd == "draft":
        out = video(*args)
    elif cmd == "final":
        out = final(*args)
    elif cmd == "prompts":
        out = {k: video(k, START_IMG.get(k) or "<start>") for k in SHOT}
    else:
        raise SystemExit(__doc__)
    print(json.dumps(out, ensure_ascii=False))
