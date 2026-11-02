"""ModernoMilano Black Week 2026: shotlijst en prompts voor de 5 betaalde video's (2 hooks elk).

Bron: de brief van de eigenaar van 2 nov 2026 (README.md). Geen gezichten, alleen handen en silhouetten; alleen de
Milano Cashmere Lounge Set (beige, gray, black, navy) plus het witte T-shirt eronder; tekst, prijzen en logo's komen er
in de nabewerking op (bw_build.py), nooit in het beeld zelf.

Gebruik:  python3 -I blackweek.py images <shot> [<shot>...]   -> generate_image_batch-requests (JSON)
          python3 -I blackweek.py draft <shot> <start_job_id>   -> generate_video-params (480p-concept)
          python3 -I blackweek.py final <shot> <start_job_id> <draft_job_id>
          python3 -I blackweek.py list
"""
import json
import sys

# Productfoto's (Shopify) op Higgsfield, media_import_url 2 nov 2026
BEIGE, GRAY, BLACK, NAVY = ("209f2622-0938-495a-a1db-70fe080cd7e8", "0d1b11da-2fde-4671-80ce-c6b013abd751",
                            "453f3b1b-363b-45c5-86c4-b6dcbb66e0ae", "7be3d17b-b000-4cd6-ac45-f25fa41a480f")
COLOUR = {BEIGE: "oatmeal beige", GRAY: "mid heather grey", BLACK: "black", NAVY: "deep navy"}
PRESET_DECLINE = "24bae836-2c4a-48e0-89b6-49fcc0b21612"

LOOK = ("Warm, quiet luxury in a muted palette of beige, cream, brown and black with a touch of gold. One real light "
        "source with a direction. Full-frame digital camera, shallow depth of field, slight lens softness at the edges. "
        "Every object rests with its weight on its surface; nothing floats.")
NO_TEXT = ("No text, lettering, numbers, logos, labels, tags, prints, embroidery, brand names or signs anywhere in the "
           "picture: not on the garments, not on the box, the ribbon, the envelope, the socks or the background.")
HANDS = ("The hands are a man's: natural, well-groomed, bare, with exactly five fingers on each hand, no ring, no watch, no "
         "bracelet, no nail polish; only bare hands and bare forearms enter the frame, no sleeves, no other clothing.")
NO_FACE = "No face and no head anywhere in the picture."
REAL = ("An unretouched photograph: the knit with its real stitch structure and soft natural creases, satin with real "
        "sheen and folds, matte paper and card, real skin texture on the hands with no beauty glow and no airbrushing. "
        "No HDR, no teal-and-orange grade, no film borders.")


def set_line(ref_no, colour, folded=True):
    fold = ("folded neatly, the jacket on top with its ribbed stand-up collar and its full-length silver zip facing up, "
            "its matching knit drawstring trousers folded underneath with the two silver aglet tips of the drawstring "
            "showing" if folded else "")
    return (f"the Milano Cashmere Lounge Set in {colour}, exactly as in reference image #{ref_no}: a cashmere-blend knit "
            f"jacket with a ribbed stand-up collar, a full-length silver zip with a small silver pull, ribbed cuffs and "
            f"hem, and matching knit drawstring trousers with silver aglet tips, plain, no print, no label; {fold}")


BOX = ("a matte black rigid gift box with a separate lid, lined with black tissue paper, with a wide cream satin ribbon")
ENVELOPE = "a sealed matte black envelope with a plain round cream wax seal, blank, without letters or symbols"
SOCKS = "a pair of plain cream ribbed wool socks rolled into a roll and tied with natural twine, no logo, no pattern, no tag"
STACK5 = ("a tall neat stack of five folded Milano Cashmere Lounge Sets, from the bottom up: oatmeal beige (reference "
          "image #1), deep navy (#2), mid heather grey (#3), black (#4) and oatmeal beige again on top; each set is the "
          "folded jacket with its ribbed stand-up collar and silver zip facing the camera, the folded trousers underneath")

# Dezelfde man als altijd: geen gezicht in beeld, dus geen element; zijn handen en silhouet worden beschreven.
SIL = ("a slim man of about 1.83 m in his mid-twenties with full, swept-back hair, seen only as a pure backlit silhouette: "
       "no face, no features, no readable clothing")

SHOTS = {
    # ---------------- V1 · P1_ListSignup ----------------
    "V1HA": {"video": "V1", "part": "hookA", "seconds": 4, "refs": [BEIGE],
             "image": (f"9:16, 4K macro. {LOOK} Soft window light from the left. On a rumpled cream linen sheet lies "
                       f"{set_line(1, 'oatmeal beige')}. On top of the folded jacket rests {ENVELOPE}, the wax seal catching "
                       "the light. A man's right hand has already taken the envelope's near corner between thumb and "
                       "fingers, about to lift it; the hand enters from the bottom right. Only the envelope, the folded set, "
                       f"the linen and the hand are in the frame. {HANDS} {NO_FACE} Full-frame digital camera, 90 mm macro, "
                       f"f/4, slightly above the bed. {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. Handheld camera, nearly still, with a slight natural breathing drift. The hand "
                        "lifts the envelope about ten centimetres toward the camera in one calm, continuous movement, the "
                        "envelope tilting slightly so the cream wax seal catches the window light; the linen under it "
                        "stays put, the folded set does not move. The hand keeps exactly five fingers and never covers "
                        "the seal. The shot opens exactly on the start frame. Nothing else happens.")},
    "V1HB": {"video": "V1", "part": "hookB", "seconds": 4, "refs": [BEIGE],
             "image": (f"9:16, 4K extreme macro. {LOOK} Golden side light from the right, low and warm. The surface of "
                       f"{set_line(1, 'oatmeal beige', folded=False)} fills the frame: the ribbed knit at the collar, each "
                       "stitch and fibre visible. A man's index fingertip rests on the knit at the centre of the frame, "
                       f"just touching it, the skin texture visible. {HANDS} {NO_FACE} Full-frame digital camera, 100 mm "
                       f"macro, f/2.8, extremely shallow depth of field. {NO_TEXT} {REAL}"),
             "motion": ("Half speed. Camera locked on a tripod with a barely visible drift. The fingertip sinks slowly "
                        "into the soft knit, the fibres compressing around it, then lifts a little and the knit recovers; "
                        "the golden light rakes across the fibres. Nothing else moves. The shot opens exactly on the start "
                        "frame. Nothing else happens.")},
    "V1B": {"video": "V1", "part": "body", "seconds": 5, "refs": [BEIGE],
            "image": (f"9:16, 4K. {LOOK} Morning window light from the left. On a cream linen bed stands {BOX}, open: the "
                      "lid lies beside it, the black tissue folded back over the edges, and inside lies "
                      f"{set_line(1, 'oatmeal beige')}. Both of a man's hands rest on the box, the right hand's fingers "
                      "just touching the folded jacket, about to press into it; the hands enter from the bottom of the "
                      f"frame. The box is centred in the frame, seen from slightly above. {HANDS} {NO_FACE} Full-frame "
                      f"digital camera, 50 mm, f/2.8. {NO_TEXT} {REAL}"),
            "motion": ("Real-time speed. A slow, steady push-in of the camera toward the box for the whole shot. The "
                       "right hand presses gently into the folded beige jacket, the knit compressing under the fingers "
                       "and slowly recovering as the hand lifts a little; the left hand rests on the box edge. The box, "
                       "the lid and the tissue do not move; the set keeps its colour and its fold. The shot opens exactly "
                       "on the start frame. Nothing else happens.")},
    "V1E": {"video": "V1", "part": "endcard", "still": True, "refs": [],
            "image": (f"9:16, 2K. {LOOK} A plain cream linen sheet fills the whole frame, softly rumpled, lit by morning "
                      "window light from the left with gentle folds and shadows; nothing else in the picture. Full-frame "
                      f"digital camera, 50 mm, f/4, seen from above. {NO_TEXT} {REAL}")},
    # ---------------- V2 · P2_BlackWeek ----------------
    "V2HA": {"video": "V2", "part": "hookA", "seconds": 4, "refs": [],
             "image": (f"9:16, 4K. {LOOK} Warm afternoon light from the left on a warm plaster wall. On a travertine ledge "
                       "stand two matte black rigid gift boxes with wide cream satin bows, a small one on the left and a "
                       "medium one in the middle, with an empty place on the right; a man's hands hold a third, larger "
                       "black gift box with a cream bow just above that empty place, about to set it down; the hands "
                       f"enter from the right. {HANDS} {NO_FACE} Full-frame digital camera, 50 mm, f/4, at ledge height. "
                       f"{NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. Handheld camera, nearly still, with a slight natural breathing drift. The hands "
                        "lower the large box onto the ledge in one calm movement, it settles with weight, the bow sways "
                        "once, and the hands withdraw to the right out of the frame. The two other boxes do not move. The "
                        "shot opens exactly on the start frame. Nothing else happens.")},
    "V2HB": {"video": "V2", "part": "hookB", "seconds": 4, "refs": [],
             "image": (f"9:16, 4K. {LOOK} A rainy evening: on a cream linen bed lies {BOX}, its lid resting half on, "
                       "askew; behind it, out of focus, a tall window with rain running down the glass and the warm "
                       "lights of the city as soft bokeh; a bedside lamp on the right is the only light. A man's right "
                       "hand has entered from the bottom of the frame and hovers a hand's width from the box, fingers "
                       f"slightly open. {HANDS} {NO_FACE} Full-frame digital camera, 50 mm, f/2. {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. Handheld camera, nearly still, with a slight natural breathing drift. The hand "
                        "moves slowly toward the box, hesitates halfway with a small pause, the fingers curling slightly, "
                        "and stops just short of the lid. Rain keeps running down the window behind; the bokeh lights "
                        "shimmer. The box does not move. The shot opens exactly on the start frame. Nothing else happens.")},
    "V2B": {"video": "V2", "part": "body", "seconds": 5, "refs": [BEIGE],
            "image": (f"9:16, 4K, seen straight down from above. {LOOK} Window light from the top of the frame on an oak "
                      f"table. {BOX} stands open in the centre: the lid lies at the top of the frame, the cream ribbon lies "
                      "loose and untied beside the box, the black tissue is folded back, and inside lies "
                      f"{set_line(1, 'oatmeal beige')} with {SOCKS} resting on top of the folded jacket. A man's two hands "
                      "have taken hold of the roll of socks from both sides, about to lift it out; the hands enter from "
                      f"the bottom of the frame. {HANDS} {NO_FACE} Full-frame digital camera, 35 mm, f/4. {NO_TEXT} {REAL}"),
            "motion": ("Real-time speed. Camera straight down, nearly still, with a slight natural breathing drift. The "
                       "two hands lift the roll of socks out of the box about fifteen centimetres toward the camera and "
                       "hold it there, revealing the folded beige jacket and its silver zip beneath; the twine stays tied. "
                       "The box, the lid, the ribbon and the set do not move. The shot opens exactly on the start frame. "
                       "Nothing else happens.")},
    # ---------------- V3 · P3_BlackFriday_BigStack ----------------
    "V3HA": {"video": "V3", "part": "hookA", "seconds": 4, "refs": [BEIGE, NAVY, GRAY, BLACK],
             "image": (f"9:16, 4K. A dark charcoal studio. On a black marble plinth stands {STACK5}. One warm spotlight from "
                       "the upper left is the only light, a narrow beam with fine dust drifting in it; the rest of the "
                       "studio falls into darkness. The stack is centred, seen from slightly below plinth height. "
                       f"Full-frame digital camera, 50 mm, f/2.8, shallow depth of field. {NO_FACE} {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. The camera on a tripod with a very slow push-in. Fine dust drifts slowly through "
                        "the beam of the spotlight; the light breathes very slightly. The stack does not move: five sets, "
                        "same colours, same order, same folds for the whole shot. The shot opens exactly on the start "
                        "frame. Nothing else happens.")},
    "V3HB": {"video": "V3", "part": "hookB", "seconds": 4, "refs": [BEIGE, NAVY, GRAY, BLACK],
             "image": (f"9:16, 4K. A dark charcoal studio, near darkness. On a black marble plinth stands {STACK5}; beside "
                       "it, on the right, a single cream candle burnt low in a small black holder, its flame the only "
                       "light, warm and small, lighting the near side of the stack and leaving the rest in shadow. "
                       f"Full-frame digital camera, 50 mm, f/2, shallow depth of field. {NO_FACE} {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. Camera locked on a tripod. The candle flame flickers and leans in a faint draught, "
                        "the light on the stack trembling with it; a thin thread of smoke rises. The stack does not move: "
                        "five sets, same colours, same order for the whole shot. The shot opens exactly on the start "
                        "frame. Nothing else happens.")},
    "V3B1": {"video": "V3", "part": "body1", "seconds": 5, "refs": [BEIGE, NAVY, GRAY, BLACK],
             "image": (f"9:16, 4K. A dark charcoal studio. On a black marble plinth stands {STACK5}, lit by one warm "
                       "spotlight from the upper left with fine dust in the beam, the background in darkness. Seen from a "
                       "three-quarter angle at plinth height, the stack a little left of centre. Full-frame digital "
                       f"camera, 50 mm, f/2.8. {NO_FACE} {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. A slow, smooth orbit of the camera around the stack, about twenty degrees to the "
                        "right over the whole shot, the plinth turning gently in perspective, the spotlight staying "
                        "fixed, dust drifting in the beam. The stack is rigid: five sets, same colours, same order, same "
                        "folds. The shot opens exactly on the start frame. Nothing else happens.")},
    "V3B2": {"video": "V3", "part": "body2", "seconds": 5, "refs": [BEIGE, GRAY, BLACK, NAVY],
             "image": (f"9:16, 4K, seen straight down from above. {LOOK} One warm light from the top left on beige linen. "
                       "Four folded Milano Cashmere Lounge Sets lie in a vertical column with a small gap between them, "
                       "from the top: oatmeal beige (reference image #1), mid heather grey (#2), black (#3), deep navy "
                       "(#4), each the folded jacket with its ribbed stand-up collar and silver zip facing up; below the "
                       "navy set an empty place on the linen. A man's two hands hold a fifth folded set, oatmeal beige, "
                       "just above that empty place, about to lay it down; the hands enter from the bottom of the frame. "
                       f"{HANDS} {NO_FACE} Full-frame digital camera, 35 mm, f/4. {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. Camera straight down, nearly still, with a slight natural breathing drift. The "
                        "hands lay the fifth folded set down into its place at the bottom of the column in one calm "
                        "movement, it settles with weight, and the hands withdraw downward out of the frame. The four "
                        "other sets do not move and keep their colours and order. The shot opens exactly on the start "
                        "frame. Nothing else happens.")},
    # ---------------- V4 · P4_MilanoStack ----------------
    "V4HA": {"video": "V4", "part": "hookA", "seconds": 4, "refs": [BEIGE, NAVY, GRAY, BLACK],
             "image": (f"9:16, 4K. An elegant Milan apartment at dusk: herringbone parquet, a tall window through which the "
                       "spires of the Duomo glow in the falling snow, a decorated Christmas tree with warm lights out of "
                       "focus on the left. In the foreground, on a Calacatta marble side table by the window, stands "
                       f"{STACK5}, lit by the warm lamplight of the room and the cold dusk from the window. The stack is "
                       "centred in the lower half of the frame, the window above it. Full-frame digital camera, 35 mm, "
                       f"f/2.8. {NO_FACE} {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. A slow, smooth pull-back of the camera for the whole shot, the stack growing a "
                        "little smaller in the frame and more of the room appearing at the edges; snow falls steadily "
                        "past the window over the glowing Duomo; the tree lights twinkle softly. The stack does not move: "
                        "five sets, same colours, same order. The shot opens exactly on the start frame. Nothing else "
                        "happens.")},
    "V4HB": {"video": "V4", "part": "hookB", "seconds": 4, "refs": [],
             "image": (f"9:16, 4K close-up. {LOOK} An elegant Milan apartment at night: under a decorated Christmas tree "
                       "with warm lights lie five plain matte black gift boxes tied with wide cream satin ribbons, "
                       "different sizes, on herringbone parquet; the tree lights and one warm lamp on the right light "
                       "the scene softly. Nobody in the picture. Full-frame digital camera, 50 mm, f/2, shallow depth of "
                       f"field. {NO_FACE} {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. Camera locked on a tripod with a barely visible drift. The tree lights twinkle "
                        "softly and the lamp light stays warm; the ribbons and boxes do not move. The shot opens exactly "
                        "on the start frame. Nothing else happens.")},
    "V4B1": {"video": "V4", "part": "body1", "seconds": 5, "refs": [BLACK, BEIGE, GRAY, NAVY],
             "image": (f"9:16, 4K, seen straight down from above. {LOOK} Warm lamplight from the top left on a walnut "
                       "parquet floor. A large open matte black gift box lined with black tissue lies in the centre; "
                       "inside, on the left, a folded black Milano Cashmere Lounge Set jacket (reference image #1) with "
                       "folded mid heather grey knit drawstring trousers (reference image #3) beside it, and on the right a "
                       "folded mid heather grey jacket; a man's two hands hold folded oatmeal beige knit drawstring "
                       "trousers (reference image #2) with silver aglet tips just above the empty place beside the black "
                       f"jacket, about to lay them in; the hands enter from the bottom of the frame. {HANDS} {NO_FACE} "
                       f"Full-frame digital camera, 35 mm, f/4. {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. Camera straight down, nearly still, with a slight natural breathing drift. The "
                        "hands lay the folded beige trousers into the box beside the black jacket in one calm movement "
                        "and withdraw downward out of the frame. The box, the tissue and the other garments do not move "
                        "and keep their colours. The shot opens exactly on the start frame. Nothing else happens.")},
    "V4B2": {"video": "V4", "part": "body2", "seconds": 5, "refs": [BEIGE, GRAY, BLACK, NAVY],
             "image": (f"9:16, 4K. {LOOK} An elegant Milan apartment at night, the warm lights of a decorated Christmas "
                       "tree above. Under the tree, on herringbone parquet, lie five folded Milano Cashmere Lounge Sets "
                       "tied like presents with wide cream satin ribbons: oatmeal beige (reference image #1), mid heather "
                       "grey (#2), black (#3), deep navy (#4) and oatmeal beige, side by side. A man's right hand has "
                       "taken hold of the beige set at the front, fingers under its ribbon, about to slide it out toward "
                       f"the camera; the hand enters from the bottom right. {HANDS} {NO_FACE} Full-frame digital camera, "
                       f"50 mm, f/2.8, at floor height. {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. Handheld camera, nearly still, with a slight natural breathing drift. The hand "
                        "slides the beige set out from under the tree toward the camera about twenty centimetres in one "
                        "calm movement, the ribbon staying tied, and rests. The other four sets do not move and keep their "
                        "colours; the tree lights twinkle softly. The shot opens exactly on the start frame. Nothing else "
                        "happens.")},
    # ---------------- V5 · P5_WinterDrop ----------------
    "V5HA": {"video": "V5", "part": "hookA", "seconds": 4, "refs": [],
             "image": (f"9:16, 4K. Night on a snowy Milan terrace: on a wide stone balustrade, under a thin layer of fresh "
                       "snow, stands a closed matte black rigid gift box, snow falling softly, the city lights out of "
                       "focus far behind. A man's bare right hand has already taken the lid at its near edge, about to "
                       "lift it; from the thin gap under the lid a warm golden light spills onto the snow. The contents "
                       f"stay hidden. {HANDS} {NO_FACE} Full-frame digital camera, 50 mm, f/2, shallow depth of field. "
                       f"{NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. Handheld camera, nearly still, with a slight natural breathing drift. The hand "
                        "lifts the lid a few centimetres and holds it there; the warm golden light from inside the box "
                        "spills out wider, lighting the falling snowflakes and the snow on the balustrade; the inside of "
                        "the box stays hidden by the lid. Snow keeps falling at a natural speed. The shot opens exactly on "
                        "the start frame. Nothing else happens.")},
    "V5HB": {"video": "V5", "part": "hookB", "seconds": 5, "refs": [],
             "image": (f"9:16, 4K. The Galleria Vittorio Emanuele II in Milan at night in heavy snow blowing in through the "
                       "arcade, seen along its length toward the far arch: the great glass-and-iron vault above, the far "
                       f"arch flooded with white light. In the middle distance {SIL} walks toward the camera, backlit by "
                       "the far arch, a pure dark silhouette against the light. The shopfronts on both sides are in deep "
                       "shadow, dark and empty, with no signs; snow swirls in the light. Nobody else. Full-frame digital "
                       f"camera, 85 mm, f/2. {NO_FACE} {NO_TEXT} {REAL}"),
             "motion": ("Real-time speed. The camera on a tripod, still. The silhouette walks toward the camera with long, "
                        "natural strides, growing larger, staying a pure dark shape against the far light; snow blows "
                        "through the arcade and swirls in the backlight. The shopfronts stay dark. The shot opens exactly "
                        "on the start frame. Nothing else happens.")},
    "V5B": {"video": "V5", "part": "body", "seconds": 5, "refs": [],
            "image": (f"9:16, 4K. Blue hour on a snowy rooftop terrace in Milan, the spires and the golden Madonnina of "
                      "the Duomo rising in the distance under a deep blue sky with light snow falling. In the foreground, "
                      f"seen from behind, two figures stand side by side looking at the Duomo: on the left {SIL}; on the "
                      "right a slender woman, slightly shorter, long hair, also only a pure dark silhouette, no face, no "
                      "readable clothing. They are in the lower half of the frame, the Duomo above them. Full-frame "
                      f"digital camera, 50 mm, f/2.8. {NO_FACE} {NO_TEXT} {REAL}"),
            "motion": ("Real-time speed. A slow, smooth rise of the camera over the whole shot, the rooftop edge sinking "
                       "and more of the Duomo and the sky appearing above the two silhouettes, who stand still, their "
                       "shoulders moving only with their breathing; light snow falls. The shot opens exactly on the start "
                       "frame. Nothing else happens.")},
}


def image_request(key):
    s = SHOTS[key]
    return {"model": "nano_banana_pro", "resolution": "2k" if s.get("still") else "4k", "aspect_ratio": "9:16",
            "prompt": s["image"], "medias": [{"value": v, "role": "image_references"} for v in s["refs"]]}


def images(keys):
    """keys als 'V1HA-a', 'V1HA-b': de letter is de variant."""
    return [{"index": i, "sid": k, "params": image_request(k.split("-")[0])} for i, k in enumerate(keys)]


STABLE = ("The garments keep their colour, their folds and their number for the whole shot; nothing is added and nothing "
          "disappears.")


def video(key, start, draft=True, draft_job=None):
    s = SHOTS[key.split("-")[0]]
    prompt = f"{s['motion']} {STABLE} {NO_FACE} {NO_TEXT} Natural motion blur, one continuous take."
    req = {"model": "seedance_2_5", "mode": "omni_reference", "resolution": "480p" if draft else "1080p", "draft": draft,
           "bitrate_mode": "high", "duration": s["seconds"], "aspect_ratio": "9:16", "generate_audio": False,
           "prompt": prompt, "medias": [{"role": "start_image", "value": start}], "declined_preset_id": PRESET_DECLINE}
    if not draft:
        req["draft_job_id"] = draft_job
    return req


COST = {"image4k": 4, "image2k": 2, "draft4": 12, "draft5": 15, "final4": 64, "final5": 80}


def estimate():
    clips = [k for k, s in SHOTS.items() if not s.get("still")]
    stills = [k for k, s in SHOTS.items() if s.get("still")]
    img = len(clips) * 3 * COST["image4k"] + len(stills) * 2 * COST["image2k"]
    drafts = sum(COST["draft4"] if SHOTS[k]["seconds"] == 4 else COST["draft5"] for k in clips)
    finals = sum(COST["final4"] if SHOTS[k]["seconds"] == 4 else COST["final5"] for k in clips)
    base = img + drafts + finals
    return {"clips": len(clips), "stills": len(stills), "start_images_3_per_shot": img, "drafts": drafts, "finals": finals,
            "base": base, "with_40pct_retakes": round(base * 1.4)}


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "list":
        for k, s in SHOTS.items():
            print(k, s["video"], s["part"], s.get("seconds", "still"), len(s["refs"]), "refs")
        print(json.dumps(estimate(), indent=1))
    else:
        out = {"images": lambda: images(args), "draft": lambda: video(args[0], args[1]),
               "final": lambda: video(args[0], args[1], False, args[2])}[cmd]()
        print(json.dumps(out, ensure_ascii=False))
