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
    "loafers": "Loafers are worn without socks, ankles bare. Both loafers are one mirrored pair in exactly the reference style: a plain vamp with moc-toe apron stitching and a small side tab, no penny strap or saddle band; both feet sit fully inside the shoes, heels in the heel cups.",
    "none": "His feet are not in the picture.",
}
NOTEXT = "No text, no logos, no badges, no film borders, no frame."
RES = "4k"
# Na batch 2 (8 okt): het gezicht dreef af in haarlengte, haarkleur en oogkleur.
# Na batch 4: "kort in de nek" gaf soms een strakke fade of pompadour; nu dichter bij model.md.
ID_LINE = ("He is in his mid-twenties, with only a faint stubble shadow (never dense stubble or a beard), dark warm brown eyes "
           "(never blue or grey) and warm chestnut-brown hair (not espresso, not near-black), full and swept back with soft natural "
           "volume, the sides combed back over the tops of his ears; no fringe falling forward, no fade, no shaved sides, no pompadour.")


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
        ID_LINE,
        "He wears only these ModernoMilano pieces, reproduced exactly as in the product reference images:\n" + "\n".join(lines),
        f"How they are worn: {s['worn']}",
        f"{HANDS} {FEET[s['feet']]} He is the only person near the camera.",
    ]
    if s.get("public"):
        parts.append(P["public_places_en"][0].upper() + P["public_places_en"][1:] + ".")
    if s.get("fix"):
        parts.append(s["fix"])
    parts += [P["realism_en"], f"Full-frame digital camera, {s['lens']}."]
    ar = s.get("ar", "4:5")
    return {"model": "nano_banana_pro", "resolution": RES, "aspect_ratio": ar, "prompt": "\n\n".join(parts), "medias": medias}


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
    if s.get("fix"):
        parts.append(s["fix"])
    parts += [P["realism_en"], f"{s['lens']}."]
    if not s.get("label"):
        parts.append(NOTEXT)
    return {"model": "nano_banana_pro", "resolution": RES, "aspect_ratio": s.get("ar", "4:5"), "prompt": "\n\n".join(parts), "medias": medias}


def mood(s):
    parts = [s["scene"], s["light"], "There are no people and no clothing in the picture, apart from any distant passers-by named above."] + ([s["fix"]] if s.get("fix") else []) + [
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
                scene="Blue hour on the Naviglio Grande in Milan: {M} leans with his forearms on the iron railing of the canal, seen from behind over his left shoulder, looking along the water while the warm lights of the old houses reflect in it. Waist-up, off-centre to the right, the railing soft in the foreground.",
                light="His face and shoulder are lit only by the warm glow of a cafe window on his left; the cool blue dusk behind him; muted colour, soft contrast, no HDR.",
                worn="The navy cashmere zip jacket zipped halfway; the joggers below, out of frame from the hips down."),
    "M03": dict(kind="p", title="Tegen de oude Spider", keys=["imperial_green", "loafer_moro"], feet="loafers", public=True, lens="50mm lens at f/2",
                scene="Morning in a quiet side street in Milan: {M} leans against the rear wing of a cream 1960s Italian two-seater convertible with chrome bumpers and no badges, emblems or number plates, his arms loosely folded, looking down the street past the camera. Three-quarter length, framed off-centre, a curve of chrome soft in the foreground.",
                light="Low morning sun from the left rakes along the facades and puts a warm rim on his hair and shoulder while his face sits in soft open shade; real shadows on the car and the cobbles.",
                worn="The olive-green zip jacket zipped up to the chest; matching trousers; dark brown suede loafers."),
    "M04": dict(kind="p", title="Op de achtersteven in Varenna", keys=["supremo_set"], feet="none", public=True, lens=L85,
                scene="Late afternoon on Lake Como: {M} sits on the varnished mahogany stern of an old wooden runabout moored at a stone jetty in Varenna, one arm resting along the gunwale, looking out over the water. Framed from the knees up, seen from the side, a coiled rope soft in the foreground. The boat has no badges, lettering or numbers.",
                light="Warm side light from the low sun on his right; reflections of the water dance on the varnish; his face in soft light; the colourful houses behind out of focus.",
                worn="The sleeveless beige knit gilet zipped over the beige long-sleeve knit polo; the beige knit trousers."),
    "M05": dict(kind="p", title="Espresso op het dak", keys=["camicia_grafite", "tee"], feet="none", lens=L85, soul_main="camicia_grafite",
                scene="A grey morning on a Milan rooftop terrace among chimneys and terracotta roofs: {M} stands at the parapet holding a small espresso cup, looking out over the city. Waist-up, seen in three-quarter view from his left, off-centre.",
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
                scene="An overcast morning at a tram stop in central Milan: {M} stands on the kerb with his hands in his jacket pockets, seen from the side and turned away from the camera, looking down the street, while an old orange tram slides past on the far track behind him, motion-blurred. Three-quarter length, off-centre to the left.",
                light="Even grey daylight; a soft shadow under him; muted warm colour against the orange of the tram.",
                worn="The dark mocha knit zip jacket zipped up, the cream stripes down the sleeves visible; matching joggers with the side stripe; dark brown suede loafers."),
    "M09": dict(kind="p", title="Aan de zinken bar", keys=["verona_navy", "tee"], feet="none", lens="50mm lens at f/1.8",
                scene="Morning at the zinc counter of an old Milan coffee bar: {M} stands at the bar with one elbow on the counter and a small espresso cup, looking towards the street door. Waist-up, seen from the side, off-centre, a glass sugar jar soft in the foreground. Nobody stands behind the bar; behind it only plain wooden shelves with unlabelled bottles, softly out of focus.",
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

# Correcties na de controle van batch 1 (8 okt): komen als extra zin in de prompt.
FIXES = {
    "M01": "He is seen in profile from the side as he walks past along the facade, not walking towards the camera. The gilet and trousers are true jet black, not navy; the gilet is zipped halfway and shows its slanted welt side pockets.",
    "M02": "The navy cashmere zip jacket has a completely plain front body with no pockets of any kind, only the stand collar, the zip, ribbed cuffs and ribbed hem; the crop ends at his hips.",
    "M03": "The car has no number plate, no plate holder and no plate frame anywhere; its rear panel is smooth. Both of his wrists are completely bare, with no bracelet, cord or band.",
    "M04": "He sits with both feet flat on the deck in front of him, both feet fully inside their sand suede loafers, the legs clearly separate; the sleeveless gilet is zipped up over the polo.",
    "M05": "He is clearly the young man of the reference images, about twenty-five, clean-shaven apart from a faint shadow, with no forehead lines.",
    "D04": "The trousers are the pale light-stone ecru beige of the reference chino, clearly lighter and less saturated than the sand loafers, with a plain unrolled hem.",
    "A01": "The cream leather seats are completely plain with no stitched or embossed emblem, and the mahogany hull has only plain chrome trim with no script, nameplate or badge; the cushions are smooth and intact.",
    "A06": "The trousers have a single elasticated drawstring waistband draped over the chair back; the folded legs on the seat end in two plain hems, with no second waistband.",
}
FIXES.update({
    "M13": "The black gilet has a smooth, flat matte shell with no quilting or horizontal channels and a thin white edge at the collar and armholes; the hooded jacket is black inside and out.",
    "D02": "Only his chin and jaw edge show at the very top of the frame; no mouth or nose.",
    "D03": "Only one bare hand with five natural fingers; no ring, watch or bracelet.",
    "A05": "The bicycles are plain and old, with no brand names, logos or stickers anywhere.",
    "M12": "The cardigan is zipped up to its own ribbed stand collar; no shirt collar or other garment shows above it.",
})
# Correcties na de controle van batch 2 (8 okt): vervangen de eerdere zin.
FIXES.update({
    "M02": "His back and left shoulder face the camera, so the front of the jacket is not in the picture; the navy jacket is completely plain, with no pockets, and the frame ends at his waist.",
    "M03": "His hair is short and neat at the back, the nape of his neck clearly visible and nothing touching the jacket collar; his face is lean with a sharply defined square jaw.",
    "M04": "The trousers are the reference heathered light-oatmeal knit trousers with a drawstring waist and a stitched centre crease, not chinos; the gilet has a fine heathered knit and a ribbed stand collar.",
    "M05": "He has only a very faint stubble shadow, no visible beard; his hair is short at the back and sides above the collar, with the nape visible.",
    "M08": "The tram is plain orange with blank dark windows: no route number, no destination board and no lettering anywhere on it; the shopfronts carry no signage.",
    "M09": "There are no signs, posters or labels anywhere in the bar; the wall behind the counter is plain.",
    "M10": "His eyes are dark warm brown, never blue or grey; his hair is short and neat at the nape, well above the collar of the gilet.",
    "A01": "The mahogany hull sides are smooth, unbroken varnished wood with only a thin plain chrome rub rail: no script, lettering, oval plate or nameplate anywhere on the boat; nothing intrudes at the edges of the frame.",
    "A06": "The cream knit polo has a closed three-button placket with dark buttons; the dark chocolate jacket is a smooth shell zip blouson whose hood is lined in light beige, with no drawstrings; the trousers end in plain hems with no turn-ups.",
})
for _k, _v in FIXES.items():
    S[_k]["fix"] = _v

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
                scene="Morning at the zinc counter of an old Milan coffee bar: {M} stands at the bar holding a small espresso cup, looking towards the street door. Waist-up, seen from the side, off-centre. Nobody stands behind the bar; behind it only plain wooden shelves with unlabelled bottles, softly out of focus.",
                light="Daylight from the open street door on his left lights his face; the bar behind is in warm shadow.",
                worn="The oatmeal hooded knit jacket zipped halfway, hood down.",
                motion="He lifts the cup slightly, pauses, then lowers it to the counter and glances towards the door. Locked-off camera."),
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


V["V01"]["fix"] = "The boat, its seats and the steering wheel have no badges, emblems, lettering or numbers."
V["V02"]["fix"] = "The car has no badges, emblems, number plate, plate holder or plate frame anywhere."
V["V04"]["fix"] = "The navy jacket has the cream-and-white stripe down the outer length of each sleeve and the joggers have the same stripe down each side."
V["V05"]["fix"] = "Both of his wrists are bare, with no bracelet or band."


# ---------- Na de controle van batch 3 (8 okt) ----------
# M02 en M04 hadden drie pogingen: nieuwe opzet. V02 krijgt een eenvoudiger outfit (de Tabacco-set kwam
# twee keer als gebreide hoodie terug). Bar-scènes zonder flessen, tramstraat zonder winkels.
S["M02"].update(keys=["bellagio_burgundy", "tee"],
                worn="The burgundy cashmere cardigan zipped halfway over the white T-shirt.",
                fix="The frame ends at his waist; nothing below the cardigan hem is visible.")
S["M04"].update(title="Op de achtersteven in Varenna",
                scene="Late afternoon on Lake Como: {M} sits on the varnished mahogany stern of an old wooden runabout moored at a stone jetty in Varenna, one arm resting along the gunwale, looking out over the water. Framed from the waist up, seen from the side, a coiled rope soft in the foreground. The boat has no badges, lettering or numbers.",
                worn="The sleeveless beige knit gilet zipped over the beige long-sleeve knit polo.",
                fix="The frame ends at his waist, so his trousers and feet are not visible; the gilet has a fine heathered knit and a ribbed stand collar.")
S["M08"].update(scene="An overcast morning at a tram stop in central Milan: {M} stands on the kerb with his hands in his jacket pockets, seen from the side and turned away from the camera, looking down the street, while an old orange tram slides past on the far track behind him, motion-blurred. Across the street only the plain ochre wall of an old palazzo with closed green shutters, no shops. Three-quarter length, off-centre to the left.",
                fix="The tram is plain orange with blank dark windows and no route number, destination board or lettering; the joggers have the cream stripe running the full length of each outer leg, exactly as in the product photo.")
_BAR = "Nobody stands behind the bar; behind it only plain shelves with stacked white cups and saucers, softly out of focus, no bottles."
S["M09"].update(scene=S["M09"]["scene"].replace("Nobody stands behind the bar; behind it only plain wooden shelves with unlabelled bottles, softly out of focus.", _BAR),
                fix="The navy jacket has a flat, pointed shirt collar with two collar points lying open on his chest, not a stand-up collar, and a tonal navy zip.")
V["V02"].update(keys=["bergamo_bordeaux", "sart_charcoal", "loafer_nero"],
                worn="The deep bordeaux long-sleeve knit polo with the top button open; the charcoal tailored trousers; black suede loafers.")
V["V03"].update(scene=V["V03"]["scene"].replace("Nobody stands behind the bar; behind it only plain wooden shelves with unlabelled bottles, softly out of focus.", _BAR),
                fix="The oatmeal hooded jacket has a dark gunmetal zip on a dark tape, exactly as in the product photo.")
V["V04"].update(keys=["twotone_navy", "tee", "loafer_notte"],
                scene="A Brera street on an overcast morning: {M} walks slowly along the pavement, seen from the front and slightly to the side. The top edge of the frame falls at the base of his neck, well below the chin, so no part of his mouth, chin or jaw is visible; the frame runs from there down to his feet, so the focus is entirely on the clothes.",
                worn="The navy cashmere zip jacket with the cream-and-white sleeve stripes, zipped up to the middle of his chest over the white T-shirt; matching navy joggers with the side stripe; navy suede loafers.")
for _k in ("M02", "M04", "M08", "M09"):
    FIXES[_k] = S[_k]["fix"]


# ---------- Na de controle van batch 4 (8 okt) ----------
V["V02"]["fix"] = ("The car has no badges, emblems, number plate, plate holder or plate frame anywhere. The charcoal trousers are pull-on "
                   "trousers with an elasticated drawstring waist and no zip fly, a straight relaxed leg and a plain hem with no turn-ups. "
                   "His left hand rests flat on the top edge of the car door.")
V["V03"]["fix"] = ("The oatmeal hooded jacket has a dark gunmetal zip, exactly as in the product photo. His fingers are completely bare, "
                   "with no ring on any finger. The espresso cup is plain, fully opaque white porcelain.")
V["V05"].update(keys=["imperial_brown", "tee", "loafer_moro"],
                scene="Wide stone steps between old Milan palazzi in soft afternoon light: {M} walks slowly down the last steps towards the camera at an angle. The top edge of the frame falls at his collarbones, so his chin, mouth and face are never in the picture; the frame runs from there down to his feet, so the focus is entirely on the clothes.",
                worn="The dark chocolate zip jacket with the pointed collar zipped halfway over the white T-shirt; matching trousers; dark brown suede loafers.",
                motion="He walks slowly down the last three steps towards the camera, one hand brushing the stone balustrade; the camera glides backwards at chest height and keeps the same framing from his collarbones to his feet; the staircase and balustrade stay the same from the first frame to the last.",
                fix="Both of his wrists are bare. Under the jacket only the plain white crew-neck T-shirt shows.")
S["M11"].update(scene="Late afternoon on a footbridge over the Navigli in Milan: a close portrait of {M} from the chest up, seen in three-quarter view from his left, looking away down the canal, off-centre.",
                fix="He looks away down the canal, not at the camera, his mouth relaxed and closed.")
S["M13"]["fix"] += " He has only a faint stubble shadow, and his hair is soft and swept back, not a sculpted pompadour, with no shaved or tapered sides."
S["D03"]["fix"] = ("Only one bare hand with five natural fingers; no ring, watch or bracelet. The zip is one continuous polished silver zip, "
                   "the same metal above and below the slider, with a flat rectangular silver pull tab like the product photo.")
# Les uit video 1: een grote hoofddraai laat het haar vervormen. Daarom blijft zijn hoofd in video 3 dezelfde kant op kijken.
V["V03"]["motion"] = ("He lifts the cup slightly, pauses, then lowers it to the counter, still looking out towards the street door; "
                      "his head stays turned the same way the whole time. Locked-off camera.")
# V04: het startbeeld is bijgesneden (bovenste 200 px eraf, 9:16 behouden) en als media geüpload: 81fdbca0-ec61-41d7-9d67-83ae2ba1ee39.
V["V04"]["motion"] = ("As he walks, he pulls the zip of the jacket up from mid-chest towards the collar with one hand; the knit moves with each step. "
                      "The camera tracks backwards at walking pace at chest height and keeps the same framing, from the T-shirt collar down to his feet.")
for _k in ("M11", "M13", "D03"):
    FIXES[_k] = S[_k]["fix"]


# ---------- Na de controle van batch 5 (8 okt): laatste ronde ----------
# Wat het model steeds verkeerd tekende (Sartoriale-broek met gulp en omslag, Imperial-jack als trainingsjack,
# de dubbele laag van de Midnight-set, de Tabacco-set) is vervangen door stukken die het betrouwbaar goed maakt.
V["V02"].update(keys=["bergamo_bordeaux", "sig_trousers_grey", "loafer_nero"],
                worn="The deep bordeaux long-sleeve knit polo with the top button open; the light grey trousers; black suede loafers.",
                fix="The car has no badges, emblems, number plate, plate holder or plate frame anywhere. The light grey trousers have a plain hem with no turn-ups. His left hand rests flat on the top edge of the car door.")
V["V05"].update(keys=["onyx", "loafer_nero"],
                worn="The black cashmere zip jacket with the ribbed stand collar zipped halfway over the white T-shirt; the black cashmere joggers; black suede loafers.",
                fix="Both of his wrists are bare. Under the jacket only the plain white crew-neck T-shirt shows; there is no hood.")
S["M13"].update(keys=["vest_black", "tee"],
                worn="The black fine-knit zip cardigan zipped halfway over the white T-shirt, the beige lining of its stand collar just visible.",
                fix="He has only a faint stubble shadow, and his hair is soft and swept back, not a sculpted pompadour, with no shaved or tapered sides.")
S["A06"].update(title="Ivoor op het balkon", keys=["bellagio_ivory"],
                scene="On a small iron balcony with red geraniums above a Brera street: the ivory cashmere zip cardigan lies folded over the back of a rattan chair.",
                arranged="Slightly rumpled, not pressed, one sleeve falling loose over the armrest.", fix="")
S["D03"].update(keys=["verona_navy"],
                scene="Macro detail: a man's fingers pull up the silver zip of a navy knit cardigan towards its pointed shirt collar; only his hand and the cardigan front are in frame, and the frame ends just below the collar.",
                light="Soft daylight from the right; the knit stitch and the zip teeth sharp.",
                people="Only his bare hand is visible, with no ring or watch; no face, chin or neck in the picture.",
                fix="The cuff is the ribbed knit cuff of the product photo, and the zip is one continuous silver zip.")
S["A07"] = dict(kind="a", title="Chroom en achterlicht", lens="85mm lens at f/2.8",
                scene="Close detail of the chrome rear bumper and round tail light of a cream 1960s Italian convertible parked on a cobbled Milan side street, an ochre wall soft and out of focus behind it.",
                light="Low morning sun from the left, a warm highlight along the chrome.",
                fix="The car has no badge, emblem, script, number plate or plate holder anywhere.")
S["D07"] = dict(kind="d", title="Loafers aan dek", keys=["loafer_tabacco_hero"], lens="100mm macro lens at f/4",
                scene="Still life on the varnished mahogany deck of an old wooden runabout on Lake Como: a pair of cognac suede loafers stands next to a coiled cream rope, the water soft and out of focus behind.",
                light="Late afternoon sun from the left, warm reflections on the varnish.",
                arranged="A mirrored left and right pair, side by side, slightly angled.",
                fix="The loafers have the moccasin seam across the toe and thick white rubber soles, no penny strap; the boat has no badges or lettering.")
for _k in ("M13", "D03"):
    FIXES[_k] = S[_k]["fix"]


# Na de laatste controle: de Onyx-jogger kreeg een gulp.
V["V05"]["fix"] = ("Both of his wrists are bare. Under the jacket only the plain white crew-neck T-shirt shows; there is no hood. "
                   "The black cashmere joggers have an elasticated waistband with a black drawstring tied at the front, no fly and no front seam, and ribbed ankle cuffs.")


def video(i, start_job):
    """Kling 3.0 image-to-video vanaf een goedgekeurd 9:16-startbeeld (model.json rules.video)."""
    v = V[i]
    keep = ("His head stays out of the frame for the whole shot; the camera never tilts up to his face. "
            "The clothes stay exactly as in the start frame." if v.get("headless") else
            "He stays exactly the same man as in the start frame, with the same face, hair and clothes; no full head turn, nothing passes in front of his face.")
    m = v["motion"]
    # Zonder gezicht geen element: dat zou het model naar zijn gezicht trekken.
    lead = m if v.get("headless") else (EL + " " + m[3:] if m.startswith("He ") else f"The man is {EL}. {m}")
    prompt = (f"{lead} Small, natural movement. {keep} Any distant passers-by keep walking, small and out of focus. "
              "Real camera, natural motion blur, no text, no logos.")
    return {"model": "kling3_0", "mode": "pro", "duration": 5, "aspect_ratio": "9:16", "sound": "off",
            "prompt": prompt, "medias": [{"role": "start_image", "value": start_job}]}


def build(i):
    s = {**S, **V}[i]
    if s["kind"] == "p":
        r = person(s)
        if s.get("headless"):
            r["prompt"] = (r["prompt"].replace(P["keep_en"], "Keep his build and skin exactly as in the reference images; his head, chin and mouth are not in the picture.")
                           .replace(f"Expression: {P['expression_en']}.\n\n", "").replace(ID_LINE + "\n\n", ""))
        return r
    return detail(s) if s["kind"] == "d" else mood(s)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--video"]:  # --video V01=<job_id> ...
        pairs = [a.split("=") for a in sys.argv[2:]]
        print(json.dumps([{"index": k + 1, "params": video(i, j)} for k, (i, j) in enumerate(pairs)], ensure_ascii=False))
        sys.exit(0)
    if sys.argv[1:2] == ["--2k"]:
        RES = "2k"
        sys.argv.pop(1)
    ids = sys.argv[1:] or list(S)
    print(json.dumps([{"index": k + 1, "params": build(i)} for k, i in enumerate(ids)], ensure_ascii=False))
