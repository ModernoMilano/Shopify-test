"""TikTok week Nov 9-15, 2026: 35 posts (5 a day) = 25 vertical videos + 10 photo carousels, all from approved
CozyCompanion visuals already in Shopify Files (no generation credits). Nothing is posted: TikTok posts need the owner's
tap in the publish form.
Sources: social/organic/src/tt/<files.json name>.jpg (st_/f_ raw calendar images, z_ gallery lifestyle, bfcm_P clean photos)
and social/organic/src/tt/reels/<r_..._ig>.mp4 (approved Seedance product reels).
  python3 social/organic/build_tiktok.py [--only 2026-11-09_3,...]   render into social/organic/out/tt/ + QA sheets + posts.json
Slots (NL time): 1 15:00 · 2 18:00 · 3 21:00 · 4 00:00 · 5 02:00 (= 9 am, noon, 3 pm, 6 pm, 8 pm New York)."""
import os, sys, json, subprocess, collections, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw
from common import W, H, SAFE_TOP, SAFE_BOTTOM, CREAM, CHAR, ROSE, font, text_block, cover, wordmark, draw_text, text_width
from build_week import reels as org_reels, OUT as ORG_OUT
import make_reel
from make_reel import render

SRC = os.path.join(HERE, "src", "tt"); REELS = os.path.join(SRC, "reels")
OUT = os.path.join(HERE, "out", "tt"); os.makedirs(OUT, exist_ok=True)
AMB = [os.path.join(HERE, "src", "amb26.mp4"), os.path.join(HERE, "src", "amb06.mp4")]
TIMES = {1: "15:00", 2: "18:00", 3: "21:00", 4: "00:00", 5: "02:00"}
DARK = (26, 26, 26, 165)
HOOK = font("Cormorant-600.ttf", 92); HOOK_S = font("Cormorant-600.ttf", 80); BIG = font("Cormorant-600.ttf", 104)
SUB = font("Jost-500.ttf", 46); LABEL = font("Jost-500.ttf", 46); SMALL = font("Jost-500.ttf", 36)
RIGHT_RAIL = 110            # TikTok like/comment/share icons on the right edge

def T(k): return os.path.join(SRC, k + ".jpg")

# ---------- text blocks ----------
def hook(t, sub=None, f=HOOK):
    return text_block([(t, f, CREAM, 0)] + ([(sub, SUB, CREAM, 0)] if sub else []), max_w=900, bg=DARK)
def label(t):
    return text_block([(t, LABEL, CREAM, 1)], max_w=860, pad=(40, 24), radius=30, bg=DARK)
def cta(t):
    return text_block([(t, SUB, CHAR, 0)], max_w=880, pad=(46, 30), radius=34, bg=(245, 241, 237, 238))
def soft(t):
    return text_block([(t, font("Cormorant-600.ttf", 96), CREAM, 0)], max_w=880, bg=(26, 26, 26, 110), pad=(50, 30))
def num(n):
    d = 300; im = Image.new("RGBA", (d, d), (0, 0, 0, 0)); g = ImageDraw.Draw(im)
    g.ellipse((0, 0, d - 1, d - 1), fill=(245, 241, 237, 240)); f = font("Cormorant-600.ttf", 230)
    tw = g.textlength(str(n), font=f); g.text(((d - tw) / 2, -12), str(n), font=f, fill=CHAR); return im
def cx(b): return max(30, (W - RIGHT_RAIL - b.width) // 2 + 30)
def top(b): return SAFE_TOP + 40
def bottom(b, m=30): return SAFE_BOTTOM - b.height - m
def tx(b, y, t0=0.0, t1=None): return dict(block=b, x=cx(b), y=y, t0=t0, t1=t1)

def seg(k, dur, texts=(), zoom=(1.0, 1.08), pan=((0.5, 0.5), (0.5, 0.5)), focus=(0.5, 0.5)):
    return dict(img=T(k), key=k, dur=dur, zoom=zoom, pan=pan, focus=focus, texts=list(texts))

def seq(segs): return dict(kind="seq", segs=segs)

def list_video(hk, items, end):
    """3 numbered tips; hook on the first slide, save prompt on the last."""
    s = []
    for i, (k, t) in enumerate(items):
        texts = [tx(label(f"{i + 1} · {t}"), 0, 0.35)]
        if i == 0: texts.insert(0, tx(hook(hk, f=HOOK_S), top(None)))
        if i == len(items) - 1: texts.append(tx(cta(end), 0, 1.1))
        s.append(seg(k, 3.9 if i < len(items) - 1 else 4.6, texts, zoom=(1.0, 1.07)))
    for sg in s:                                     # stack label (+ CTA) from the bottom of the safe zone
        for t in sg["texts"]:
            if t["y"] == 0: t["y"] = None
        labs = [t for t in sg["texts"] if t["y"] is None]
        y = SAFE_BOTTOM - 30
        for t in reversed(labs):
            y -= t["block"].height; t["y"] = y; y -= 18
    return seq(s)

def product(reel, hk, stills, end, name):
    """Approved Seedance reel (6 s) with a hook, then two stills with the product facts, then a comment prompt."""
    (k1, f1, *y1), (k2, f2) = stills                  # optional y for the first label when the product sits low in the photo
    lab_end = label(f"{name} · link in bio")
    return dict(kind="product", reel=os.path.join(REELS, reel + ".mp4"), reel_key=reel, hook=hook(hk, f=HOOK_S), segs=[
        seg(k1, 3.0, [tx(label(f1), y1[0] if y1 else bottom(label(f1)), 0.35)], zoom=(1.0, 1.08)),
        seg(k2, 4.2, [tx(label(f2), bottom(label(f2)) - 0, 0.35, 1.6), tx(cta(end), bottom(lab_end) - 18 - cta(end).height, 1.6),
                      tx(lab_end, bottom(lab_end), 1.6)], zoom=(1.0, 1.06))])

# ---------- carousel slides (1080x1920 JPEG, TikTok photo mode) ----------
def bg(k, focus=(0.5, 0.5)):
    im = cover(Image.open(T(k)), W, H, focus).convert("RGBA")
    sh = Image.new("L", (1, H))
    for y in range(H):
        sh.putpixel((0, y), int(70 * max(0, (520 - y) / 520) + 120 * max(0, (y - 1050) / 870) ** 1.3))
    lay = Image.new("RGBA", (W, H), CHAR + (0,)); lay.putalpha(sh.resize((W, H))); im.alpha_composite(lay); return im

def put(im, b, y): im.alpha_composite(b, (cx(b), int(y)))

def badge(im, t, xy=(60, SAFE_TOP + 20)):
    f = font("Jost-500.ttf", 54); d = ImageDraw.Draw(im); r = 52; x, y = xy
    d.ellipse((x, y, x + 2 * r, y + 2 * r), fill=(245, 241, 237, 240)); tw = text_width(t, f)
    draw_text(im, (x + r - tw / 2, y + 18), t, f, CHAR)

def slide_cover(k, title, sub, focus=(0.5, 0.5)):
    im = bg(k, focus); put(im, text_block([(title, BIG, CREAM, 0)], max_w=900, bg=DARK, pad=(56, 40)), SAFE_TOP + 50)
    s = text_block([(sub, SMALL, CHAR, 1)], max_w=860, pad=(36, 20), radius=26, bg=(245, 241, 237, 235))
    wm = wordmark(240); pill = Image.new("RGBA", (wm.width + 56, wm.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(pill).rounded_rectangle((0, 0, pill.width - 1, pill.height - 1), pill.height // 2, fill=(26, 26, 26, 150))
    pill.alpha_composite(wm, (28, 15))
    put(im, pill, SAFE_BOTTOM - pill.height - 30); put(im, s, SAFE_BOTTOM - pill.height - 50 - s.height)
    return im

def slide(k, text, n=None, end=None, focus=(0.5, 0.5), head=None):
    im = bg(k, focus)
    if head: put(im, hook(head, f=HOOK_S), SAFE_TOP + (150 if n is not None else 40))
    if n is not None: badge(im, str(n))
    y = SAFE_BOTTOM - 30
    blocks = ([label(text)] if text else []) + ([cta(end)] if end else [])
    for b in reversed(blocks):
        y -= b.height; put(im, b, y); y -= 18
    return im

def slide_ab(a, b, q, end=None):
    im = Image.new("RGB", (W, H), CREAM); hw = W // 2 - 3
    im.paste(cover(Image.open(T(a)), hw, H), (0, 0)); im.paste(cover(Image.open(T(b)), hw, H), (W // 2 + 3, 0))
    im = im.convert("RGBA"); f = font("Jost-500.ttf", 76); d = ImageDraw.Draw(im); r = 66
    for i, t in enumerate(("A", "B")):
        c = (W // 4 + i * (W // 2), int(H * 0.53))
        d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=(245, 241, 237, 240)); tw = d.textlength(t, font=f)
        d.text((c[0] - tw / 2, c[1] - 50), t, font=f, fill=CHAR)
    put(im, text_block([(q, HOOK_S, CHAR, 0)], max_w=880, bg=(245, 241, 237, 238), pad=(50, 32)), SAFE_TOP + 40)
    if end: c = cta(end); put(im, c, SAFE_BOTTOM - c.height - 30)
    return im

def photo(slides, keys): return dict(kind="photo", slides=slides, keys=keys)

# ---------- the week ----------
def week():
    P = {}
    O = org_reels()
    # TikTok has no 'featured in our story': the caption contest prize becomes a pinned comment
    O["2026-11-13"]["segs"][1]["texts"][1]["block"] = __import__("build_week").cta("Best caption gets pinned 📌👇")
    for d, r in O.items():
        P[(d, 4)] = dict(kind="org", segs=r["segs"], format=f"Interaction · {r['format']}", type="video")

    def add(d, s, fmt, spec, title, desc):
        if (d, s) in P: spec = {**P[(d, s)], **spec}
        spec.update(title=title, description=desc, type="photo" if spec["kind"] == "photo" else "video")
        if fmt: spec["format"] = fmt
        P[(d, s)] = spec

    BOTH = "#petsoftiktok #dogsoftiktok #catsoftiktok"
    CAT = "#catsoftiktok #cattok #petsoftiktok"; DOG = "#dogsoftiktok #dogtok #petsoftiktok"
    # ---------------- Mon 9 Nov ----------------
    d = "2026-11-09"
    k = ["z_dapper_dog", "z_dream_dog", "z_bloom_cat", "f_2026-11-20_0_v2_raw", "z_riddle_dog", "z_glide_dog", "z_buddy_life"]
    add(d, 1, "Carousel · Pet awards", photo([
        slide_cover(k[0], "Pets who understood the assignment 🏆", "Swipe →"),
        slide(k[1], "🏆 Best napper"), slide(k[2], "🏆 Head of security", focus=(0.35, 0.5)), slide(k[3], "🏆 Most dramatic"),
        slide(k[4], "🏆 Snack detective"), slide(k[5], "🏆 Best athlete"),
        slide(k[6], "🏆 Best friends", end="Which award does your pet win? 👇")], k),
        "Pets who understood the assignment 🏆",
        f"Pets who understood the assignment 🏆 Which award does your pet win? Comment below 👇\n\n{BOTH} #petawards #funnypets")
    add(d, 2, "POV · Breakfast alarm", seq([
        seg("st_2026-11-30_raw", 3.8, [tx(hook("POV: it's 6 am and they've decided it's breakfast ⏰", f=HOOK_S), top(None))], zoom=(1.0, 1.1), pan=((0.5, 0.6), (0.55, 0.62))),
        seg("z_cove_cat", 3.2, [tx(hook("…and they will not be taking questions", f=HOOK_S), top(None))], zoom=(1.0, 1.08)),
        seg("z_slate_cat", 3.8, [tx(hook("Breakfast: served. Peace: restored. 🙏", f=HOOK_S), top(None)),
                                 tx(cta("Who runs the schedule at your house? 👇"), bottom(cta("Who runs the schedule at your house? 👇")), 1.0)])]),
        "POV: it's 6 am and they've decided it's breakfast ⏰",
        f"POV: it's 6 am and they've decided it's breakfast ⏰ Who runs the schedule at your house? 👇\n\n{CAT} #breakfasttime #relatable")
    add(d, 3, "Product · Haven Pet Den", product("r_2026-11-06_v2_ig", "When the cat moves into the den, you just live there now 🏠",
        [("st_2026-12-31_raw", "Bed and den in one"), ("f_2026-12-20_0_raw", "Quiet, scratch-resistant felt")],
        "Would your cat claim this spot? 👇", "Haven Pet Den"),
        "When the cat moves into the den, you just live there now 🏠😼",
        f"When the cat moves into the den, you just live there now 🏠😼 Would your cat claim this spot? 👇 Haven Pet Den: bed and den in one, link in bio.\n\n{CAT} #catbed #cozycat")
    add(d, 4, None, {}, "Which nap spot wins? 1 or 2? 🛏️",
        f"Which nap spot wins? 1 = the round snuggle bed, 2 = the plush sofa bed. Comment 1 or 2 👇\n\n{BOTH} #thisorthat #dogbed #cozyhome")
    add(d, 5, "Stitch bait · Where does your pet sleep", seq([
        seg("z_orbit_sleep", 3.4, [tx(hook("Show me where YOUR pet sleeps 👇", f=HOOK_S), top(None)), tx(label("Ours: in the donut"), bottom(label("x")), 0.8)]),
        seg("z_burrow_cat", 2.8, [tx(label("…or the plush bed"), bottom(label("x")), 0.35)]),
        seg("z_billow_dog", 4.2, [tx(label("…or wherever the sun is ☀️"), bottom(label("x")), 0.35, 1.7),
                                  tx(cta("Stitch this with your pet's spot 🎬👇"), bottom(cta("Stitch this with your pet's spot 🎬👇")), 1.7)])]),
        "Show me where YOUR pet sleeps 👇",
        f"Show me where YOUR pet sleeps 👇 Stitch this with their favorite spot 🎬\n\n{BOTH} #sleepingpets #stitch")
    # ---------------- Tue 10 Nov ----------------
    d = "2026-11-10"
    k = ["z_fold_cat", "z_perch_cats", "z_wiggle_cat", "z_chaise_cat", "z_orbit_kitten", "z_nook_cat", "z_purr_cat"]
    names = ["The supervisor", "The hunter", "The diva", "The hider", "The sunbather", "The food critic"]
    add(d, 1, "Carousel · Which one is your cat", photo(
        [slide_cover(k[0], "Which one is your cat? 1–6 🐱", "Swipe, then comment the number →")] +
        [slide(k[i + 1], names[i], n=i + 1, end="Which one is yours? Comment 1–6 👇" if i == 5 else None) for i in range(6)], k),
        "Which one is your cat? 1–6 🐱", f"Which one is your cat? 1–6 🐱 Comment the number 👇\n\n{CAT} #catpersonality #catmom")
    add(d, 2, "Cozy aesthetic · Cozy season", seq([
        seg("st_2026-12-13_raw", 3.6, [tx(soft("cozy season starts now 🕯️"), top(None))], zoom=(1.0, 1.06)),
        seg("f_2026-12-19_0_raw", 3.3, [], zoom=(1.04, 1.0), pan=((0.5, 0.5), (0.52, 0.5))),
        seg("st_2026-12-21_raw", 3.3, [], zoom=(1.0, 1.06)),
        seg("st_2026-12-20_raw", 3.8, [tx(cta("Save this for the next slow evening 🤎"), bottom(cta("Save this for the next slow evening 🤎")), 0.6)], zoom=(1.0, 1.05))]),
        "Cozy season starts now 🕯️",
        f"Cozy season starts now 🕯️ Save this for the next slow evening 🤎 Would your pet pick the fireplace or the window? 👇\n\n{BOTH} #cozyseason #cozyvibes")
    add(d, 3, "Product · Forage Snuffle Mat", product("r_2026-11-17_v1_ig", "Dinner, but make it a treasure hunt 🔎",
        [("z_forage_dog", "Sniff-and-find enrichment"), ("z_forage_detail", "Machine washable")],
        "10 seconds or 10 minutes for your dog? 👇", "Forage Snuffle Mat"),
        "Dinner, but make it a treasure hunt 🔎",
        f"Dinner, but make it a treasure hunt 🔎 Would your dog figure it out in 10 seconds or 10 minutes? 👇 Forage Snuffle Mat, link in bio.\n\n{DOG} #snufflemat #dogenrichment")
    add(d, 4, None, {}, "Rate this nap from 1 to 10 👇",
        f"Rate this nap from 1 to 10 👇 Fireplace on, best friend next to you, zero plans. We're saying 11.\n\n{BOTH} #rateit #cozyvibes")
    k = ["z_gnaw_puppy", "z_chester_dog", "z_lift_sofa", "z_drizzle_walk", "z_ride_dog", "z_quest_dog", "z_stride_walk"]
    lines = ["The dog has nicer furniture than you", "Dog hair is part of every outfit now", "Rain? The walk still happens",
             "The front seat is theirs now", "Dinner is a puzzle now", "You spell out W-A-L-K"]
    add(d, 5, "Carousel · Tell me you're a dog parent", photo(
        [slide_cover(k[0], "Tell me you're a dog parent without telling me 🐶", "Swipe →")] +
        [slide(k[i + 1], lines[i], end="Add yours in the comments 👇" if i == 5 else None) for i in range(6)], k),
        "Tell me you're a dog parent without telling me 🐶",
        f"Tell me you're a dog parent without telling me 🐶 Add yours in the comments 👇\n\n{DOG} #dogparent #dogmom")
    # ---------------- Wed 11 Nov ----------------
    d = "2026-11-11"
    k = ["z_mistle_dog", "st_2026-11-19_raw", "st_2026-12-14_raw", "st_2026-12-01_raw", "z_chirp_kitten", "f_2026-11-03_0_raw", "z_beacon_walk"]
    tips = ["A warm bed away from drafty doors and windows", "Wipe paws after walks on salted sidewalks", "An extra blanket for nap time",
            "Indoor play for cold, dark days", "Fresh water, refilled every day", "A light-up collar for dark evening walks"]
    add(d, 1, "Carousel · Cozy winter checklist", photo(
        [slide_cover(k[0], "Cozy winter checklist for pets ❄️", "Save this for later 📌")] +
        [slide(k[i + 1], f"{i + 1} · {tips[i]}", end="What would you add? 👇" if i == 5 else None) for i in range(6)], k),
        "Cozy winter checklist for pets ❄️",
        f"Cozy winter checklist for pets ❄️ Save this for the first cold night 📌 What would you add? 👇\n\n{BOTH} #wintertips #petparents")
    add(d, 2, "Stitch bait · Most dramatic nap", seq([
        seg("z_cloud_cat", 3.4, [tx(hook("Stitch this with your pet's most dramatic nap 😴", f=HOOK_S), top(None))]),
        seg("z_doze_dog", 3.0, [tx(label("Exhibit A"), bottom(label("x")), 0.35)], zoom=(1.0, 1.1), pan=((0.5, 0.55), (0.55, 0.55))),
        seg("f_2026-12-21_0_raw", 4.0, [tx(label("Exhibit B"), bottom(label("x")), 0.35, 1.6),
                                        tx(cta("Your turn: stitch it 🎬👇"), bottom(cta("Your turn: stitch it 🎬👇")), 1.6)])]),
        "Stitch this with your pet's most dramatic nap 😴",
        f"Stitch this with your pet's most dramatic nap 😴🎬 We need to see it 👇\n\n{BOTH} #sleepingpets #stitch")
    add(d, 3, "Product · Wiggle Window Cat Teaser", product("r_2026-11-13_v1_ig", "The window is now their favorite channel 📺",
        [("z_wiggle_cat", "Sticks to windows and walls"), ("z_wiggle_detail", "Light sensor starts and stops it")],
        "Would your cat be obsessed? 👇", "Wiggle Window Cat Teaser"),
        "The window is now their favorite channel 📺",
        f"The window is now their favorite channel 📺 Would your cat be obsessed? 👇 Wiggle Window Cat Teaser, link in bio.\n\n{CAT} #cattoys #indoorcat")
    add(d, 4, None, {}, "POV: the comfiest bed in the house… and they chose the box 📦",
        f"POV: you got them the comfiest bed in the house… and they chose the box 📦😹 Tag someone whose pet does this 👇\n\n{CAT} #catsandboxes #funnypets")
    q = "Dog or cat under the blanket? 🐶🐱"
    add(d, 5, "Quiz · Who's under the blanket", seq([
        seg("z_snug_dog", 5.6, [tx(hook(q, f=HOOK_S), top(None)), dict(block=num(3), x=(W - 300) // 2, y=1050, t0=1.6, t1=2.8),
                                dict(block=num(2), x=(W - 300) // 2, y=1050, t0=2.8, t1=4.0), dict(block=num(1), x=(W - 300) // 2, y=1050, t0=4.0, t1=5.2)],
            zoom=(2.8, 2.9), pan=((0.72, 0.45), (0.73, 0.45))),
        seg("z_snug_dog", 4.4, [tx(hook("A very sleepy puppy 🐶", f=HOOK_S), top(None), 0.5),
                                tx(cta("Did you guess right? 👇"), bottom(cta("Did you guess right? 👇")), 1.3)], zoom=(2.2, 1.0), pan=((0.72, 0.45), (0.5, 0.5)))]),
        "Dog or cat under the blanket? 🐶🐱",
        f"Dog or cat under the blanket? 🐶🐱 Guess before the reveal and comment 👇\n\n{BOTH} #guess #cozyvibes")
    # ---------------- Thu 12 Nov ----------------
    d = "2026-11-12"
    k = ["z_lounge_cat", "st_2026-11-09_raw", "z_cloud_cat", "f_2026-12-22_0_raw", "z_chaise_cat", "z_peak_cat"]
    signs = ["They have the best view in the house", "Your blanket is now their blanket", "Their nap schedule is non-negotiable",
             "They have their own sofa (and use yours)", "They have a designer scratcher"]
    add(d, 1, "Carousel · Signs your cat owns the house", photo(
        [slide_cover(k[0], "5 signs your cat owns the house 😼", "Swipe →")] +
        [slide(k[i + 1], f"{i + 1} · {signs[i]}", end="How many does your cat check? 1–5 👇" if i == 4 else None) for i in range(5)], k),
        "5 signs your cat owns the house 😼",
        f"5 signs your cat owns the house 😼 How many does your cat check? Comment 1–5 👇\n\n{CAT} #catlife #catmom")
    add(d, 2, "List · 3 habits your cat will love", list_video("3 tiny habits your cat will love 🐱",
        [("z_slate_cat", "Fresh water, every single day"), ("z_chase_cat", "Rotate toys so they stay exciting"),
         ("z_perch_cats", "A high spot by the window")], "Save this 📌 Which one do you already do?"),
        "3 tiny habits your cat will love 🐱",
        f"3 tiny habits your cat will love 🐱 Save this 📌 Which one do you already do? 👇\n\n{CAT} #cattips #catcare")
    add(d, 3, "Product · Brook Pet Fountain", product("r_2026-11-03_v2_ig", "Fresh, flowing water all day 💧",
        [("u_brook", "304 stainless steel", 1000), ("st_2026-11-03_raw", "Ultra-quiet (under 20 dB)")],
        "Does your cat prefer running water? 👇", "Brook Pet Fountain"),
        "Fresh, flowing water all day 💧",
        f"Fresh, flowing water all day 💧 Does your cat prefer running water? 👇 Brook Stainless Pet Fountain, link in bio.\n\n{CAT} #petfountain #catlife")
    add(d, 4, None, {}, "Every pet has a sleeping style. Which one is yours?",
        f"Every pet has a sleeping style. Which one is yours? 1 the burrito, 2 the donut, 3 the cuddler, 4 the couch potato 👇\n\n{BOTH} #sleepingpets #petpersonality")
    k = ["z_knot_play", "z_savor_dog", "z_lounge_dog", "z_zoom_play", "bfcm_P6a", "z_wander_walk"]
    ll = ["Snacks", "Quality time on the sofa", "Playtime", "Cuddles under a blanket", "Adventures outside"]
    add(d, 5, "Carousel · Pet love language", photo(
        [slide_cover(k[0], "What's your pet's love language? 🤎", "Swipe →")] +
        [slide(k[i + 1], ll[i], n=i + 1, end="Comment your pet's number 👇" if i == 4 else None) for i in range(5)], k),
        "What's your pet's love language? 1–5 🤎",
        f"What's your pet's love language? 1–5 🤎 Comment the number 👇\n\n{BOTH} #lovelanguage #petparents")
    # ---------------- Fri 13 Nov ----------------
    d = "2026-11-13"
    k = ["st_2026-11-15_raw", "st_2026-12-20_raw", "z_nook_crate", "z_lounge_dog", "f_2026-12-19_1_raw", "z_billow_dog"]
    add(d, 1, "Carousel · Rate these nap spots", photo(
        [slide_cover(k[0], "Rate these nap spots 1–10 🛏️", "Swipe →")] +
        [slide(k[i + 1], f"Nap spot #{i + 1}", end="Comment your scores, like 8-10-7-9-10 👇" if i == 4 else None) for i in range(5)], k),
        "Rate these nap spots 1–10 🛏️",
        f"Rate these nap spots 1–10 🛏️ Comment your scores like 8-10-7-9-10 👇\n\n{BOTH} #napspot #rateit")
    add(d, 2, "POV · Whose bed is it", seq([
        seg("z_dream_dog", 3.8, [tx(hook("You: “the dog sleeps in HIS bed.”", f=HOOK_S), top(None))], zoom=(1.0, 1.08)),
        seg("z_cloud_dog", 4.6, [tx(hook("The dog at 2 am: 🙃", f=HOOK_S), top(None)),
                                 tx(cta("Whose bed is it really? Tag a co-sleeper 👇"), bottom(cta("Whose bed is it really? Tag a co-sleeper 👇")), 1.4)],
            zoom=(1.0, 1.1), pan=((0.5, 0.5), (0.52, 0.55)))]),
        "You: the dog sleeps in HIS bed. The dog at 2 am: 🙃",
        f"You: the dog sleeps in HIS bed. The dog at 2 am: 🙃 Whose bed is it really? Tag a co-sleeper 👇\n\n{DOG} #relatable #dogmom")
    add(d, 3, "Product · Chester Tufted Dog Sofa", product("r_2026-11-08_v1_ig", "Big dog. Even bigger sofa energy 🛋️",
        [("z_chester_dog", "Raised off the floor, thick padding"), ("z_chester_detail", "Removable, washable cover")],
        "Would your dog share it with you? 👇", "Chester Tufted Dog Sofa"),
        "Big dog. Even bigger sofa energy 🛋️",
        f"Big dog. Even bigger sofa energy 🛋️ Would your dog share it with you? 👇 Chester Tufted Dog Sofa, link in bio.\n\n{DOG} #dogsofa #bigdogs")
    add(d, 4, None, {}, "Caption this 😂👇",
        f"Caption this 😂👇 The best caption gets pinned 📌\n\n{CAT} #captionthis #funnycats")
    add(d, 5, "Cozy aesthetic · Friday night", seq([
        seg("z_nook_cat", 3.6, [tx(soft("Friday night plans: absolutely none 🤎"), top(None))], zoom=(1.0, 1.06)),
        seg("st_2026-11-19_raw", 3.2, [], zoom=(1.05, 1.0)),
        seg("f_2026-12-22_0_raw", 3.2, [], zoom=(1.0, 1.06)),
        seg("f_2026-11-19_1_raw", 3.8, [tx(cta("Who's staying in tonight? 👇"), bottom(cta("Who's staying in tonight? 👇")), 0.6)], zoom=(1.0, 1.05))]),
        "Friday night plans: absolutely none 🤎",
        f"Friday night plans: absolutely none 🤎 Who's staying in with their pet tonight? 👇\n\n{BOTH} #cozynight #fridaynight")
    # ---------------- Sat 14 Nov ----------------
    d = "2026-11-14"
    k = ["z_knit_poodle", "z_maze_dog", "st_2026-11-08_raw", "z_trail_run", "z_splash_dog", "z_fetch_dog", "z_cocoon_dog"]
    names = ["The snack detective", "The couch prince", "The adventurer", "The drama queen", "The athlete", "The professional napper"]
    add(d, 1, "Carousel · Which one is your dog", photo(
        [slide_cover(k[0], "Which one is your dog? 1–6 🐶", "Swipe, then comment the number →")] +
        [slide(k[i + 1], names[i], n=i + 1, end="Which one is yours? Comment 1–6 👇" if i == 5 else None) for i in range(6)], k),
        "Which one is your dog? 1–6 🐶", f"Which one is your dog? 1–6 🐶 Comment the number 👇\n\n{DOG} #dogpersonality #dogmom")
    add(d, 2, "POV · The warm spot", seq([
        seg("z_lounge_cat", 3.8, [tx(hook("When you finally sit down after a long day…", f=HOOK_S), top(None))], zoom=(1.0, 1.08)),
        seg("z_chester_dog", 4.6, [tx(hook("…and someone already claimed the warm spot 🙃", f=HOOK_S), top(None)),
                                   tx(cta("Does your pet steal your seat? 👇"), bottom(cta("Does your pet steal your seat? 👇")), 1.4)], zoom=(1.0, 1.1))]),
        "When you finally sit down… and someone already claimed the warm spot 🙃",
        f"When you finally sit down… and someone already claimed the warm spot 🙃 Does your pet steal your seat? 👇\n\n{BOTH} #relatable #couchpotato")
    add(d, 3, "Product · Burrow Plush Pet Bed", product("r_2026-11-26_v1_ig", "Best friends, one bed 🤎",
        [("z_burrow_cat", "Plush bolster sides"), ("z_burrow_detail", "Thick, warm cushion")],
        "Do your pets share or fight over it? 👇", "Burrow Plush Pet Bed"),
        "Best friends, one bed 🤎",
        f"Best friends, one bed 🤎 Do your pets share or fight over it? 👇 Burrow Plush Pet Bed, link in bio.\n\n{BOTH} #dogandcat #petbed")
    add(d, 4, None, {}, "Guess what this is for 🤔",
        f"Guess what this is for 🤔 Watch till the end and comment your guess 👇\n\n{DOG} #dachshund #guess")
    k = ["z_chomp_dog", "z_riddle_dog", "z_tidy_dog", "st_2026-11-25_raw", "st_2026-11-06_raw", "z_plume_play", "z_knot_play",
         "z_frost_snow", "z_puddle_walk", "st_2026-12-13_raw", "z_nook_cat"]
    qs = ["Breakfast", "Nap", "Play", "Walk", "Evening"]
    add(d, 5, "Carousel · Build your pet's dream day (A/B)", photo(
        [slide_cover(k[0], "Build your pet's dream day 🅰️🅱️", "Pick A or B on every slide →")] +
        [slide_ab(k[1 + 2 * i], k[2 + 2 * i], qs[i], end="Comment your combo, like ABBAB 👇" if i == 4 else None) for i in range(5)], k),
        "Build your pet's dream day: A or B? 🅰️🅱️",
        f"Build your pet's dream day: A or B? 🅰️🅱️ Comment your combo, like ABBAB 👇\n\n{BOTH} #thisorthat #dreamday")
    # ---------------- Sun 15 Nov ----------------
    d = "2026-11-15"
    k = ["f_2026-11-02_0_raw", "st_2026-11-29_raw", "st_2026-11-17_raw", "z_chomp_dog", "f_2026-11-28_0_raw", "z_pounce_cat", "z_gnaw_puppy"]
    add(d, 1, "Carousel · Sunday photo dump", photo(
        [slide(k[0], None, n=1, head="Sunday photo dump 🤎")] +
        [slide(k[i], None, n=i + 1, end="Which one is your favorite? 1–7 👇" if i == 6 else None) for i in range(1, 7)], k),
        "Sunday photo dump 🤎", f"Sunday photo dump 🤎 Which one is your favorite? Comment 1–7 👇\n\n{BOTH} #photodump #sundayvibes")
    add(d, 2, "List · Calm on a noisy night", list_video("3 ways to help your pet feel calm on a noisy night 🎆",
        [("st_2026-12-31_raw", "A covered, quiet spot to retreat to"), ("z_snug_dog", "A blanket that smells like home"),
         ("z_tidy_dog", "Meals and walks at the usual times")], "Save this for the next fireworks night 📌"),
        "3 ways to help your pet feel calm on a noisy night 🎆",
        f"3 ways to help your pet feel calm on a noisy night 🎆 Save this for the next fireworks night 📌 What helps your pet? 👇\n\n{BOTH} #pettips #petparents")
    add(d, 3, "Product · Cocoon Deep Sleep Bed", product("r_2026-11-15_v1_ig", "Sunday mode: activated 😴",
        [("z_cocoon_dog", "Thick, raised round bolster"), ("z_cocoon_detail", "Removable, washable cover")],
        "Would your pup curl up in this? 👇", "Cocoon Deep Sleep Bed"),
        "Sunday mode: activated 😴",
        f"Sunday mode: activated 😴 Would your pup curl up in this? 👇 Cocoon Deep Sleep Bed, link in bio.\n\n{DOG} #puppy #dogbed")
    add(d, 4, None, {}, "Team dog or team cat? 🐶🐱",
        f"The big question: team dog or team cat? 🐶🐱 Comment your team 👇\n\n{BOTH} #teamdog #teamcat")
    q = "What's inside the donut? 🍩"
    add(d, 5, "Quiz · What's inside the donut", seq([
        seg("z_orbit_kitten", 5.6, [tx(hook(q, f=HOOK_S), top(None)), dict(block=num(3), x=(W - 300) // 2, y=1150, t0=1.6, t1=2.8),
                                    dict(block=num(2), x=(W - 300) // 2, y=1150, t0=2.8, t1=4.0), dict(block=num(1), x=(W - 300) // 2, y=1150, t0=4.0, t1=5.2)],
            zoom=(2.9, 3.0), pan=((0.4, 0.42), (0.42, 0.42))),
        seg("z_orbit_kitten", 4.4, [tx(hook("A tiny tenant 🐱", f=HOOK_S), top(None), 0.6),
                                    tx(cta("Did you guess it? 👇"), bottom(cta("Did you guess it? 👇")), 1.3)], zoom=(2.2, 1.05), pan=((0.42, 0.45), (0.5, 0.58)))]),
        "What's inside the donut? 🍩",
        f"What's inside the donut? 🍩 Guess before the reveal 👇\n\n{CAT} #kitten #guess")
    return P

ORG_KEYS = {"2026-11-09": ["11-15", "11-19"], "2026-11-10": ["11-14"], "2026-11-11": ["11-02", "12-05"],
            "2026-11-12": ["12-01", "12-20", "11-26", "11-25"], "2026-11-13": ["11-13"], "2026-11-14": ["11-22"], "2026-11-15": ["11-21", "11-06"]}

def keys_of(d, s, p):
    if p["kind"] == "org": return [f"st_2026-{x}_raw" for x in ORG_KEYS[d]]
    if p["kind"] == "photo": return p["keys"]
    return [sg["key"] for sg in p["segs"]]

def check_usage(P):
    tot = collections.Counter(); bad = []
    for d in sorted({d for d, _ in P}):
        day = collections.Counter()
        for s in range(1, 6):
            ks = set(keys_of(d, s, P[(d, s)])); day.update(ks); tot.update(ks)
        bad += [f"{d}: {k} twice" for k, n in day.items() if n > 1]
    bad += [f"{k} used {n}x" for k, n in tot.items() if n > 3]
    return tot, bad

def render_product(p, out):
    part = out[:-4] + "_b.mp4"; render(p["segs"], part, AMB[0])
    hk = Image.new("RGBA", (W, H), (0, 0, 0, 0)); b = p["hook"]; hk.alpha_composite(b, (cx(b), SAFE_TOP + 40))
    png = out[:-4] + "_hook.png"; hk.save(png)
    rd = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p["reel"]]))
    bd = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", part]))
    XF = 0.4; total = rd + bd - XF; wav = out[:-4] + ".wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", AMB[1], "-t", f"{total:.2f}", "-vn",
                    "-af", f"volume=4.0,afade=t=in:d=0.6,afade=t=out:st={total - 0.9:.2f}:d=0.9", "-ar", "48000", "-ac", "2", wav], check=True)
    fc = (f"[0:v]scale={W}:{H}:flags=lanczos,fps=30,setsar=1,format=rgba[s];[1:v]format=rgba,fade=t=in:st=0.25:d=0.3:alpha=1[h];"
          f"[s][h]overlay=0:0:shortest=1,format=yuv420p,settb=AVTB[a];[2:v]fps=30,setsar=1,format=yuv420p,settb=AVTB[b];"
          f"[a][b]xfade=transition=fade:duration={XF}:offset={rd - XF:.3f},format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", p["reel"], "-loop", "1", "-t", f"{rd:.3f}", "-framerate", "30", "-i", png,
                    "-i", part, "-i", wav, "-filter_complex", fc, "-map", "[v]", "-map", "3:a", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
                    "-movflags", "+faststart", "-shortest", out], check=True)
    for f in (part, png, wav): os.remove(f)

def job(args):
    name, p = args
    if p["kind"] == "photo":
        outs = []
        for i, im in enumerate(p["slides"]):
            f = os.path.join(OUT, f"{name}_s{i + 1}.jpg"); im.convert("RGB").save(f, quality=90); outs.append(f)
        sheet = Image.new("RGB", (270 * len(outs), 480), CREAM)
        for i, f in enumerate(outs): sheet.paste(Image.open(f).resize((270, 480)), (270 * i, 0))
        sheet.save(os.path.join(OUT, f"_qa_{name}.jpg"), quality=85)
        return name, outs
    out = os.path.join(OUT, name + ".mp4")
    if p["kind"] == "product": render_product(p, out)
    else: render(p["segs"], out, AMB[0])
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]))
    frames = []
    for i, t in enumerate((0.5, dur / 2, dur - 0.4)):
        f = os.path.join(OUT, f"_f{i}_{name}.jpg")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", out, "-frames:v", "1", "-vf", "scale=360:-1", f], check=True)
        frames.append(f)
    sheet = Image.new("RGB", (360 * 3, 640), CREAM)
    for i, f in enumerate(frames): sheet.paste(Image.open(f), (360 * i, 0)); os.remove(f)
    sheet.save(os.path.join(OUT, f"_qa_{name}.jpg"), quality=85)
    return name, [out]

def probe(f):
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,avg_frame_rate,sample_rate,pix_fmt:format=duration",
                                            "-of", "json", f]))
    v = next(s for s in j["streams"] if s["codec_type"] == "video"); a = next(s for s in j["streams"] if s["codec_type"] == "audio")
    head = open(f, "rb").read(200000); moov, mdat = head.find(b"moov"), head.find(b"mdat")
    return dict(dur=round(float(j["format"]["duration"]), 2), fps=v["avg_frame_rate"], size=f'{v["width"]}x{v["height"]}', pix=v["pix_fmt"],
                codec=v["codec_name"], ar=a["sample_rate"], faststart=0 <= moov < mdat or (moov >= 0 and mdat < 0))

if __name__ == "__main__":
    P = week()
    tot, bad = check_usage(P)
    if bad: sys.exit("image usage: " + "; ".join(bad))
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    jobs = [(f"tt_{d}_{s}", p) for (d, s), p in sorted(P.items()) if not only or f"{d}_{s}" in only]
    res = {}
    with cf.ProcessPoolExecutor(4) as ex:
        for name, outs in ex.map(job, jobs):
            res[name] = outs; print("done", name, flush=True)
    meta_path = os.path.join(OUT, "posts.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    for (d, s), p in sorted(P.items()):
        name = f"tt_{d}_{s}"
        if name not in res: continue
        m = dict(date=d, slot=s, type=p["type"], format=p["format"], title=p["title"], description=p["description"],
                 recommended_post_time_nl=TIMES[s], files=[os.path.relpath(f, OUT) for f in res[name]])
        if p["type"] == "video":
            m["probe"] = probe(res[name][0]); pr = m["probe"]
            assert pr["fps"] == "30/1" and pr["ar"] == "48000" and pr["faststart"] and pr["size"] == "1080x1920" and 7 <= pr["dur"] <= 15.5, (name, pr)
        assert len(p["title"]) <= 150 and len(p["description"]) <= 2200, name
        meta[name] = m
    json.dump(meta, open(meta_path, "w"), indent=1, ensure_ascii=False)
    print("posts:", len(meta), "| images used:", len(tot), "| max per image:", max(tot.values()))
