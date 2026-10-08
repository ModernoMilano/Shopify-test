"""25 foto's en 5 video's met het vaste model (8 okt 2026).

Gebruik: python3 -I shots.py <ids...>  -> print de requests (JSON) voor generate_image_batch.
Productfoto's en specs komen uit de eerdere series (R, SPEC, MEDIA); het model en de vaste
Engelse blokken uit creative-engine/data/model.json. Geen MEN, geen filmwoorden.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-07-100-gevarieerd"))
import shots100 as base  # noqa: E402  (alleen R, SPEC, MEDIA, B, LABEL, LABEL_IDS)

R, SPEC, MEDIA, B = base.R, base.SPEC, base.MEDIA, base.B
MODEL = json.load(open(os.path.join(ROOT, "creative-engine", "data", "model.json")))
P = MODEL["prompt"]
EL = MODEL["higgsfield"]["element_placeholder"]
SOUL = MODEL["higgsfield"]["soul_id"]

HANDS = "His hands and wrists are bare: no watch, no ring, no bracelet, no glasses, no bag."
FEET = {
    "loafers": "Loafers are worn without socks, ankles bare.",
    "none": "His feet are not in the picture.",
}
NOTEXT = "No text, no logos, no badges, no film borders, no frame."


def spec(k):
    return SPEC[k].replace(" Smooth matte fabric, no labels.", " Smooth matte fabric.").replace(" No labels.", "")


def refs(keys, cap=4):
    """Productfoto's in volgorde, maximaal `cap`, eerlijk verdeeld over de stukken."""
    medias, lines = [], []
    per = max(1, cap // len(keys))
    for k in keys:
        files = R[k][:per] if sum(len(R[x]) for x in keys) > cap else R[k]
        for f in files:
            medias.append({"value": MEDIA[B + f], "role": "image_references"})
        lines.append(f"- {spec(k)}")
    return medias[:cap], lines


def person(s):
    medias, lines = refs(s["keys"])
    parts = [
        s["scene"].replace("{M}", EL),
        s["light"],
        f"Expression: {P['expression_en']}.",
        P["keep_en"],
        "He wears only these ModernoMilano pieces, reproduced exactly as in the product reference images:\n" + "\n".join(lines),
        f"How they are worn: {s['worn']}",
        f"{HANDS} {FEET[s['feet']]} He is the only person near the camera.",
    ]
    if s.get("public"):
        parts.append(P["public_places_en"][0].upper() + P["public_places_en"][1:] + ".")
    parts += [P["realism_en"], f"Full-frame digital camera, {s['lens']}."]
    ar = s.get("ar", "4:5")
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": ar, "prompt": "\n\n".join(parts), "medias": medias}


def detail(s):
    """Macro/still life: kleding zonder gezicht (hooguit handen of kin van het model)."""
    medias, lines = refs(s["keys"], cap=s.get("cap", 4))
    parts = [s["scene"], s["light"],
             "The only clothing in the picture is these ModernoMilano pieces, reproduced exactly as in the product reference images:\n" + "\n".join(lines)]
    if s.get("arranged"):
        parts.append(f"How they are arranged: {s['arranged']}")
    if s.get("label"):
        n = len(medias)
        for v in base.LABEL_IDS:
            medias.append({"value": v, "role": "image_references"})
        parts.append(base.LABEL.format(a=n + 1, b=n + 2).replace("The label is sharp and clearly legible.", "The label is small, curving with the collar, partly shaded, and legible."))
        parts.append("The only text anywhere in the picture is the 'ModernoMilano' wordmark on the neck label, spelled exactly like that. No other logos, labels or text.")
    parts.append(s.get("people", "There are no people in the picture."))
    parts += [P["realism_en"], f"{s['lens']}."]
    if not s.get("label"):
        parts.append(NOTEXT)
    return {"model": "nano_banana_pro", "resolution": "4k", "aspect_ratio": s.get("ar", "4:5"), "prompt": "\n\n".join(parts), "medias": medias}


def mood(s):
    parts = [s["scene"], s["light"], "There are no people and no clothing in the picture, apart from any distant passers-by named above.",
             "An unretouched photograph with real optics, natural colour, muted and soft in contrast; no HDR.", f"{s['lens']}.", NOTEXT]
    return {"model": "nano_banana_pro", "resolution": "2k", "aspect_ratio": "4:5", "prompt": "\n\n".join(parts), "medias": []}


L85 = "85mm lens at f/2"
S = {
    # ---------- M: Luca ----------
    "M01": dict(kind="p", title="Brera op een grijze ochtend", keys=["reverso_nero", "loafer_nero"], feet="loafers", public=True, lens=L85,
                scene="A grey morning on a narrow cobbled street in Brera, Milan: {M} walks past an ochre palazzo facade with green shutters, seen from the side, mid-step, glancing down the street ahead of him. Three-quarter length, framed off-centre to the left, with the soft edge of an open shutter in the foreground.",
                light="Soft, even overcast daylight from the open street on his right; a faint real shadow under him on the cobbles; muted warm colour, soft contrast.",
                worn="The black gilet zipped halfway over the white T-shirt; black trousers; black suede loafers."),
    "M02": dict(kind="p", title="Blauw uur aan de Navigli", keys=["lounge_navy"], feet="none", public=True, lens="85mm lens at f/1.8",
                scene="Blue hour on the Naviglio Grande in Milan: {M} leans with his forearms on the iron railing of the canal, seen from behind and slightly to the side, looking along the water while the warm lights of the old houses reflect in it. Waist-up, off-centre to the right, the railing soft in the foreground.",
                light="His face and shoulder are lit only by the warm glow of a cafe window on his left; the cool blue dusk behind him; muted colour, soft contrast, no HDR.",
                worn="The navy cashmere zip jacket zipped halfway; the joggers below, out of frame from the hips down."),
    "M03": dict(kind="p", title="Tegen de oude Spider", keys=["imperial_green", "loafer_moro"], feet="loafers", public=True, lens="50mm lens at f/2",
                scene="Morning in a quiet side street in Milan: {M} leans against the rear wing of a cream 1960s Italian two-seater convertible with chrome bumpers and no badges, emblems or number plates, his arms loosely folded, looking down the street past the camera. Three-quarter length, framed off-centre, a curve of chrome soft in the foreground.",
                light="Low morning sun from the left rakes along the facades and puts a warm rim on his hair and shoulder while his face sits in soft open shade; real shadows on the car and the cobbles.",
                worn="The olive-green zip jacket zipped up to the chest; matching trousers; dark brown suede loafers."),
    "M04": dict(kind="p", title="Op de achtersteven in Varenna", keys=["supremo_set"], feet="loafers", public=True, lens=L85,
                scene="Late afternoon on Lake Como: {M} sits on the varnished mahogany stern of an old wooden runabout moored at a stone jetty in Varenna, one arm resting along the gunwale, looking out over the water. Three-quarter, seen from the side, a coiled rope soft in the foreground. The boat has no badges, lettering or numbers.",
                light="Warm side light from the low sun on his right; reflections of the water dance on the varnish; his face in soft light; the colourful houses behind out of focus.",
                worn="The sleeveless beige knit gilet zipped over the beige long-sleeve knit polo; beige trousers; sand suede loafers."),
    "M05": dict(kind="p", title="Espresso op het dak", keys=["camicia_grafite", "tee"], feet="none", lens=L85, soul_main="camicia_grafite",
                scene="A grey morning on a Milan rooftop terrace among chimneys and terracotta roofs: {M} stands at the parapet holding a small espresso cup, looking out over the city. Waist-up, seen from the side, off-centre.",
                light="Soft grey daylight from the open sky on his left; the city behind a stop darker and out of focus; cool muted colour, soft contrast.",
                worn="The charcoal knitted overshirt open over the white T-shirt."),
    "M06": dict(kind="p", title="Bij het hoge raam", keys=["lido_avena", "sart_charcoal"], feet="none", lens="50mm lens at f/2",
                scene="Morning in an old Milan apartment with herringbone parquet: {M} sits sideways in a worn leather armchair by a tall window, a closed book with a plain cover on his knee, looking out of the window. From mid-thigh up, seen from the side, the window frame soft in the foreground.",
                light="Soft morning daylight from the tall window on his left lights the side of his face; the room behind him falls into warm shadow.",
                worn="The oatmeal knit polo with the top button open; charcoal tailored trousers."),
    "M07": dict(kind="p", title="Onder de koepel van de Galleria", keys=["onyx", "loafer_nero"], feet="loafers", public=True, lens="50mm lens at f/2",
                scene="Early morning under the glass dome of the Galleria Vittorio Emanuele II in Milan: {M} walks across the mosaic floor, seen from the side and slightly behind, his head turned towards the arcade. Three-quarter length, off-centre, a column soft in the foreground. The shop fronts are far away and blurred, with no readable signs.",
                light="Soft daylight falls from the glass roof above him; gentle shadows; muted warm colour.",
                worn="The black zip jacket zipped halfway over the white T-shirt; black joggers; black suede loafers."),
    "M08": dict(kind="p", title="Wachten op de tram", keys=["mocha_set", "loafer_moro"], feet="loafers", public=True, lens=L85,
                scene="An overcast morning at a tram stop in central Milan: {M} stands on the kerb with his hands in his jacket pockets while an old orange tram slides past behind him, slightly motion-blurred. Three-quarter length, off-centre to the left, seen from the side. The tram shows no readable numbers or lettering.",
                light="Even grey daylight; a soft shadow under him; muted warm colour against the orange of the tram.",
                worn="The dark mocha knit zip jacket zipped up, the cream stripes down the sleeves visible; matching joggers with the side stripe; dark brown suede loafers."),
    "M09": dict(kind="p", title="Aan de zinken bar", keys=["verona_navy", "tee"], feet="none", lens="50mm lens at f/1.8",
                scene="Morning at the zinc counter of an old Milan coffee bar: {M} stands at the bar with one elbow on the counter and a small espresso cup, looking towards the street door. Waist-up, seen from the side, off-centre, a glass sugar jar soft in the foreground. Nobody stands behind the bar; the bottles and signs behind are blurred and unreadable.",
                light="Daylight from the open street door on his left lights his face; the bar behind him is in warm shadow.",
                worn="The navy zip jacket with its pointed collar zipped halfway over the white T-shirt."),
    "M10": dict(kind="p", title="De trappen van Bellagio", keys=["oliva_set", "loafer_moro"], feet="loafers", lens="35mm lens at f/2.8",
                scene="A narrow stepped lane in Bellagio with flower pots and old shutters: {M} climbs the stone steps away from the camera and looks back over his shoulder towards the lake below. Full length, seen from behind and slightly below, off-centre.",
                light="Soft open shade in the lane, warm sunlight on the walls above him; muted colour.",
                worn="The olive gilet zipped up over the white long-sleeve T-shirt; olive trousers; dark brown suede loafers."),
    "M11": dict(kind="p", title="Laatste licht op de brug", keys=["lido_notte"], feet="none", lens="85mm lens at f/1.8", soul_main="lido_notte",
                scene="Late afternoon on a footbridge over the Navigli in Milan: a close portrait of {M} from the chest up, looking down the canal, off-centre.",
                light=P["light_default_en"],
                worn="The dark navy knit polo with the top button open."),
    "M12": dict(kind="p", title="Villaterras met cipressen", keys=["bellagio_green", "atelier_beige"], feet="none", lens=L85,
                scene="Morning on the terrace of a lakeside villa on Lake Como: {M} stands at a stone balustrade with tall cypresses behind him, one hand resting on the stone, looking out over the lake. From mid-thigh up, seen from the side, off-centre, a terracotta urn soft in the foreground.",
                light="Morning sun from behind him to the right puts a warm rim on his hair and shoulder while his face sits in soft shade; the lake hazy and out of focus.",
                worn="The forest-green cardigan zipped up; beige trousers."),
    "M13": dict(kind="p", title="Avond in Brera", keys=["midnight"], feet="none", public=True, lens="50mm lens at f/1.8",
                scene="Evening on a narrow street in Brera: {M} stands by the lit window of a small bakery, looking down the street, his hands in his jacket pockets. Waist-up, seen from the side, off-centre; the street behind him dark with a few warm lights.",
                light="His face is lit only by the warm bakery window on his left; the rest of the street is in deep blue-black shadow.",
                worn="The black hooded zip jacket open over the black gilet with its thin white edges and a white T-shirt."),
    # ---------- D: macro ----------
    "D01": dict(kind="d", title="Streep op de mouw", keys=["twotone_navy"], lens="100mm macro lens at f/4",
                scene="Macro detail: a man's hand adjusts the ribbed cuff of a navy cashmere zip jacket, the cream-and-white stripe running down the sleeve; only his forearm, hand and part of the jacket front are in frame.",
                light="Soft window light from the left; real knit stitch visible; muted warm colour.",
                people="Only his hand and wrist are visible, bare, with no ring, watch or bracelet; no face in the picture."),
    "D02": dict(kind="d", title="Kraag en knopen", keys=["lido_avena"], lens="100mm macro lens at f/4",
                scene="Macro detail of the pointed collar and three-button placket of an oatmeal knit polo as worn by a man; the top of the frame cuts off just below his chin, so only the faint stubble of his jawline shows at the edge.",
                light="Morning window light from the left raking across the knit, every stitch visible.",
                people="No face in the picture."),
    "D03": dict(kind="d", title="De rits omhoog", keys=["imperial_green"], lens="100mm macro lens at f/4",
                scene="Macro detail: a man's fingers pull up the silver zip of an olive-green jacket towards its pointed collar; only his hand and the jacket front are in frame.",
                light="Soft daylight from the right; the smooth matte fabric and the zip teeth sharp.",
                people="Only his bare hand is visible, no ring or watch; no face in the picture."),
    "D04": dict(kind="d", title="Suede op de kasseien", keys=["loafer_sabbia_hero", "atelier_beige"], lens="100mm macro lens at f/4",
                scene="Macro at ankle height on a Milan cobbled street: a man mid-step in sand suede loafers without socks, his bare ankles and the hem of his beige trousers in frame; a mirrored left and right pair.",
                light="Low morning sun from behind, long shadows on the cobbles, the suede nap visible.",
                people="Only his ankles and feet are visible."),
    "D05": dict(kind="d", title="Label in de kraag", keys=["lounge_gray"], cap=3, label=True, lens="100mm macro lens at f/4",
                scene="Close-up still life: the grey cashmere zip jacket lies folded on white bed linen with the collar open, the inside of the back neck towards the camera.",
                light="Soft morning light from a window on the left."),
    "D06": dict(kind="d", title="Champagne op linnen", keys=["champagne_set"], lens="100mm macro lens at f/4",
                scene="Macro still life: the champagne cashmere knit, slightly rumpled, not pressed, one sleeve falling loose, next to a small espresso cup on a linen tablecloth.",
                light="Morning light from a window on the right; the soft knit texture visible.",
                arranged="The hooded knit jacket folded loosely with the drawstring of the joggers just visible beneath."),
    # ---------- A: sfeer ----------
    "A01": dict(kind="a", title="Houten boot bij Varenna", lens="35mm lens at f/4",
                scene="Morning on Lake Como: an old varnished mahogany runabout with cream leather seats moored at a stone jetty in Varenna, seen from slightly above, the water clear and green. The boat has no badges, lettering or numbers.",
                light="Soft low morning sun from the left; gentle reflections; the far shore hazy."),
    "A02": dict(kind="a", title="Oude Cinquecento in de straat", lens="35mm lens at f/2.8",
                scene="A small pale blue 1960s Italian city car with no badges, emblems or readable number plates parked on a cobbled street in Milan, ochre facades and green shutters behind it, an old bicycle leaning against the wall.",
                light="Overcast morning, soft even light, the cobbles slightly damp."),
    "A03": dict(kind="a", title="Espresso op zink", lens="100mm lens at f/2.8",
                scene="Close-up of a small white espresso cup with crema and a spoon on the worn zinc counter of an old Milan bar.",
                light="Morning daylight from the open street door on the left; the bar behind in warm shadow."),
    "A04": dict(kind="a", title="Torre Velasca op een grijze ochtend", lens="50mm lens at f/4",
                scene="The Torre Velasca in Milan seen from a quiet street below, a plane-tree branch soft in the foreground.",
                light="A grey morning, soft even light, muted colour."),
    "A05": dict(kind="a", title="Fietsen aan de Navigli", lens="35mm lens at f/2.8",
                scene="Early morning on the Naviglio Grande: two old bicycles lean against the iron railing, the canal still, the pastel houses soft behind; two distant passers-by small and out of focus, faces unreadable.",
                light="Soft early sun from the left, mist on the water."),
    "A06": dict(kind="d", title="Tabacco op het balkon", keys=["tabacco_set"], lens="50mm lens at f/2.8",
                scene="On a small iron balcony with red geraniums above a Brera street: the dark chocolate hooded jacket and the dark brown trousers lie on a rattan chair, the cream knit polo folded on top.",
                light="Morning sun from the left, real shadows of the railing on the clothes.",
                arranged="Slightly rumpled, not pressed, one sleeve falling loose over the armrest."),
}

# ---------- V: startbeelden voor de video's (9:16) ----------
V = {
    "V01": dict(kind="p", title="Aan het stuur op het Comomeer", keys=["sorrento_ottanio", "atelier_beige"], feet="none", lens="50mm lens at f/2", ar="9:16",
                scene="Lake Como in the late morning: {M} stands at the slim wooden steering wheel of an old varnished mahogany runabout gliding slowly across the water, the wind lifting his hair, looking ahead towards the shore. Waist-up, seen from the side, off-centre. The boat has no badges, lettering or numbers.",
                light="Bright soft sun from the left, light reflected from the water on his face; the mountains hazy behind.",
                worn="The teal knit polo with cream tipping; beige trousers.",
                motion="The boat glides slowly forward; the wind moves his hair and the knit; he keeps one hand on the wheel and glances towards the shore, then back ahead. Gentle handheld camera from the deck."),
    "V02": dict(kind="p", title="Bij de oude auto", keys=["tabacco_set", "loafer_moro"], feet="loafers", public=True, lens="50mm lens at f/2", ar="9:16",
                scene="Morning in a cobbled Milan side street: {M} walks up beside a cream 1960s Italian convertible with no badges, emblems or number plates and rests one hand on the top of its door, looking down the street. Three-quarter length, off-centre.",
                light="Low morning sun from behind him to the left, a warm rim on his hair and shoulder, his face in soft open shade.",
                worn="The dark chocolate hooded jacket open over the cream knit polo; dark brown trousers; dark brown suede loafers.",
                motion="He takes two slow steps along the car, lets his hand slide along the top of the door and stops, looking down the street. The camera drifts slowly beside him."),
    "V03": dict(kind="p", title="Espresso aan de bar", keys=["morbido_beige"], feet="none", lens="50mm lens at f/1.8", ar="9:16",
                scene="Morning at the zinc counter of an old Milan coffee bar: {M} stands at the bar holding a small espresso cup, looking towards the street door. Waist-up, seen from the side, off-centre. Nobody stands behind the bar; bottles and signs blurred and unreadable.",
                light="Daylight from the open street door on his left lights his face; the bar behind is in warm shadow.",
                worn="The oatmeal hooded knit jacket zipped halfway, hood down.",
                motion="He lifts the cup slightly, pauses, then sets it down on the saucer and glances towards the door. Very small natural movement, locked-off camera."),
    "V04": dict(kind="p", title="Rits omhoog, hoofd buiten beeld", keys=["twotone_navy", "loafer_notte"], feet="loafers", public=True, lens="50mm lens at f/2.8", ar="9:16", headless=True,
                scene="A Brera street on an overcast morning: {M} walks slowly along the pavement, seen from the front and slightly to the side. The frame runs from just below his chin down to his feet: the top of the frame cuts off his head just below the chin, so the focus is entirely on the clothes.",
                light="Even grey daylight; soft shadows; muted warm colour.",
                worn="The navy cashmere zip jacket with the cream-and-white sleeve stripes, open over his chest; matching navy joggers with the side stripe; navy suede loafers.",
                motion="As he walks he pulls the zip of the jacket up to his chest with one hand; the knit moves with each step. The camera tracks backwards at walking pace and keeps his head out of frame."),
    "V05": dict(kind="p", title="De trap af, hoofd buiten beeld", keys=["imperial_brown", "loafer_moro"], feet="loafers", lens="35mm lens at f/2.8", ar="9:16", headless=True,
                scene="Wide stone steps between old Milan palazzi in soft afternoon light: {M} walks slowly down the steps towards the camera at an angle. The frame runs from his shoulders down to his feet: the top of the frame cuts off his head at the neck, so the focus is entirely on the clothes.",
                light="Soft side light from the right; real shadows on the steps.",
                worn="The dark chocolate zip jacket with the pointed collar zipped halfway; matching trousers; dark brown suede loafers.",
                motion="He comes down three steps, one hand brushing the stone balustrade, the trousers moving naturally; the camera stays at chest height and keeps his head out of frame."),
}


def build(i):
    s = {**S, **V}[i]
    if s["kind"] == "p":
        r = person(s)
        if s.get("headless"):
            r["prompt"] = (r["prompt"].replace(P["keep_en"], "Keep his build, jaw line and skin exactly as in the reference images; his face is not in the picture.")
                           .replace(f"Expression: {P['expression_en']}.\n\n", ""))
        return r
    return detail(s) if s["kind"] == "d" else mood(s)


if __name__ == "__main__":
    ids = sys.argv[1:] or list(S)
    print(json.dumps([{"index": k + 1, "params": build(i)} for k, i in enumerate(ids)], ensure_ascii=False))
