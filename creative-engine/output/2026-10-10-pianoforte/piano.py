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
  python3 -I piano.py video [draft|720p|<concept job>] [seconden]  -> Seedance 2.5 van startbeeld 87 naar eindbeeld 90
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-08-reels-focus"))
from videos4 import EL, HANDS, HF, ID_LINE, P, PRESET_DECLINE, REAL_SMOOTH, person, req, reverso, sleeveless  # noqa: E402

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


# Eindbeeld ronde 3 (wens eigenaar, 10 okt). Het startbeeld 87 blijft, maar:
# - de villa wordt groot, met uitzicht over zee, strand en natuur in Italië;
# - het beeld eindigt achter hem, terwijl hij vanaf het raam naar het uitzicht kijkt.
# Gekozen kust: Sardinië. Een stille baai met licht zand, turquoise water en macchia en pijnbomen op de rotsen.
# De achterkant-foto van de set is boven de enkels afgesneden (ce8e5038), want ook daar draagt het model penny loafers.
SET_BACK_NOSHOES = "ce8e5038-0802-44f9-bd0d-66473adf7828"
VIEW = ("a wide view over a quiet bay on the coast of Sardinia below: a curved beach of pale sand, clear turquoise water "
        "turning deep blue further out, green Mediterranean scrub and umbrella pines on the rocky headlands, and the open sea "
        "to the horizon under a soft, slightly hazy sky; no buildings, no boats close by and no people on the beach")
ID_BACK = ("He is the same man as in the reference images, seen from behind: warm chestnut-brown hair (not espresso, not "
           "near-black), full and swept back with soft natural volume, the sides combed back over the tops of his ears and "
           "tapered neatly at the nape; the same build, shoulders and posture.")


def end_frame3(job_start):
    return req([
        ("Late morning, a few seconds later in the same room as reference image #1: the large living room of a grand villa "
         "high above the sea on the coast of Sardinia, with high ceilings, a pale travertine floor, warm stone walls, ivory "
         "linen curtains, the same black lacquered grand piano and a wall of tall floor-to-ceiling windows with thin bronze "
         f"frames. Through the tall windows, {VIEW}. Nobody else is in the room. " + EL + " stands at the tall window, seen "
         "from behind with his back to the camera, looking out over the bay; his weight on one leg, his right hand in his "
         "trouser pocket and his left arm relaxed at his side, his head level and facing the view, so his face is not "
         "visible. The camera stands a few metres behind him in the room at chest height, a little off-centre; at the left "
         "edge of the frame the curved black lacquered tail of the grand piano is soft and out of focus, and no piano keys "
         "are visible. Framed vertically from just above his head to his feet on the travertine floor: the whole man and his "
         "loafers are in the picture, with the bright bay filling the window around him."),
        ("Soft late-morning daylight from the tall windows. The view outside is bright and slightly hazy but keeps its colour "
         "and detail. The room and his back are softly lit by daylight bouncing off the pale travertine floor, a stop darker "
         "than the view, with a soft shadow on the floor behind his feet. Muted natural colour, soft contrast, no HDR, not a "
         "silhouette."),
        ID_BACK,
        "He wears only these ModernoMilano pieces, reproduced exactly as in the product reference images:\n" + SET["text"]
        + "\n" + LOAFER,
        ("How they are worn, seen from behind: the gilet with the dark ANTHRACITE side out, its plain back panel and "
         "elasticated hem, the stand collar standing up at the back of his neck; the short sleeves of the light pietra "
         "T-shirt coming out of the deep armholes, and its hem hanging loose below the gilet hem; the anthracite trousers, "
         "slim and tapered, ending just above the ankle bone; the grey suede loafers on bare feet, with bare skin visible at "
         "both ankles."),
        sleeveless("dark anthracite grey", "light pietra stone", 2), LOAFER_PLAIN, PIANO,
        f"{HANDS} He is the only person in the picture.", REAL_SMOOTH,
        "Full-frame digital camera, 35mm lens at f/2.8."], [job_start, SET_BACK_NOSHOES, LOAFER_SIDE, LOAFER_PAIR])


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


# Video: één doorlopende take van startbeeld 87 naar eindbeeld 90. Niet slow motion (wens eigenaar): het tempo wordt
# in de prompt uitgeschreven, want Seedance maakt uit zichzelf trage beweging.
START_JOB, END_JOB = "928c365c-4920-4184-a043-8e9a9e801112", "3cb9512a-2879-4588-8944-e52ed9384978"
VIDEO_MOTION = (
    "One continuous take in real time, at a normal, natural pace; not slow motion. It opens exactly on the start frame: a "
    "close detail of his left hand resting on the white keys of the black lacquered grand piano, his bare forearm and the "
    "short sleeve of the light pietra T-shirt coming out of the deep armhole of the anthracite gilet. In the first second "
    "he presses one key softly, lifts his hand from the keys and turns away from the piano towards the tall window on the "
    "right. He walks to the window with a few relaxed steps at a normal walking pace while the camera pulls back smoothly "
    "and steadily at hip height, so that more and more of him and the room comes into view: his arm and the gilet, then "
    "the trousers, then the grey suede loafers on bare feet, until the whole man stands in profile at the window. There he "
    "stops, slides his right hand into his trouser pocket and looks out at the garden, exactly as in the end frame; for "
    "the last second he stands still, breathing softly.")
VIDEO_CLOTHES = (
    "the sleeveless gilet stays dark anthracite outside, light pietra stone only inside the collar and along the open front "
    "edges, hanging open over the light pietra T-shirt, which hangs loose and untucked at the same length throughout, with "
    "the slim anthracite trousers and the plain grey suede loafers on bare feet")


def video(draft=True, resolution="480p", duration=8, draft_job=None):
    faces = [r["upscale_job_id"] for r in HF["face_refs"] if any(r["file"].endswith(f"/{x}.jpg") for x in HF["video_face_refs"])]
    prompt = (f"{VIDEO_MOTION} He is the man in the start and end frames and in the reference images; use the reference "
              f"images only for his face and hair. He keeps the same face, hair and clothes throughout: {VIDEO_CLOTHES}. "
              "His face stays clear, his hands and wrists bare. The room stays quiet; the garden beyond the window barely "
              "moves. Real-time motion with natural motion blur, one continuous take on a smooth dolly.")
    medias = ([{"role": "start_image", "value": START_JOB}, {"role": "end_image", "value": END_JOB}]
              + [{"role": "image_references", "value": f} for f in faces])
    p = {"model": "seedance_2_5", "mode": "omni_reference", "resolution": resolution, "draft": draft,
         "bitrate_mode": "high", "duration": duration, "aspect_ratio": "9:16", "generate_audio": False, "prompt": prompt,
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
    elif cmd == "end3":
        out = [{"index": 92 + v, "params": {**end_frame3(args[0]), "resolution": "2k"}} for v in range(2)]
    elif cmd == "end2":
        out = [{"index": 90 + v, "params": {**end_frame2(args[0]), "resolution": "2k"}} for v in range(2)]
    elif cmd == "video":
        # video [draft|720p|<draft job>] [seconden]
        mode, dur = (args + ["draft"])[0], int((args + ["draft", "8"])[1])
        if mode == "draft":
            params = video(duration=dur)
        elif mode == "720p":
            params = video(draft=False, resolution="720p", duration=dur)
        else:
            params = video(duration=dur, draft_job=mode)
        out = [{"index": 0, "params": params}]
    elif cmd == "shoes":
        # 2k: genoeg voor een video-eindbeeld (1080p) en 2 credits in plaats van 4 (10 okt)
        out = [{"index": 88 + v, "params": {**shoes_fix(args[0]), "resolution": "2k"}} for v in range(2)]
    else:
        raise SystemExit(__doc__)
    print(json.dumps(out, ensure_ascii=False))
