"""Sample week Nov 9-15, 2026: one interaction reel per day (extra 15:13 ET slot) + 3 reply-prompt stories per day.
All from already-approved CozyCompanion visuals (st_<date>_raw clean 9:16 photos in social/organic/src/), no credits.
  python3 social/organic/build_week.py            render reels + stories into social/organic/out/ and QA sheets
  python3 social/organic/build_week.py --upload   also upload to Shopify Files and write social/organic_plan.json"""
import os, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw
from common import (W, H, SAFE_TOP, SAFE_BOTTOM, CREAM, CHAR, ROSE, font, text_block, shadowed, cover, wordmark, draw_text,
                    text_width)
from make_reel import render

SRC = os.path.join(HERE, "src"); OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
AUD = os.path.join(SRC, "amb26.mp4")
src = lambda d: os.path.join(SRC, f"{d}.jpg")

HOOK = font("Cormorant-600.ttf", 96); HOOK_S = font("Cormorant-600.ttf", 80)
SUB = font("Jost-500.ttf", 50); LABEL = font("Jost-500.ttf", 46); EYEBROW = font("Jost-500.ttf", 30)
DARK = (26, 26, 26, 160)

def hook(text, sub=None, f=HOOK):
    spec = [(text, f, CREAM, 0)] + ([(sub, SUB, CREAM, 0)] if sub else [])
    return text_block(spec, max_w=960, bg=DARK)

def label(text):
    return text_block([(text, LABEL, CREAM, 1)], max_w=900, pad=(40, 24), radius=30, bg=DARK)

def cta(text):
    return text_block([(text, SUB, CHAR, 0)], max_w=960, pad=(48, 30), radius=34, bg=(245, 241, 237, 235))

def at_bottom(b, margin=30):
    return SAFE_BOTTOM - b.height - margin

def split(a, b, labels=("1", "2"), out=None):
    """Side-by-side composite (oversized like make_reel expects) with round number badges."""
    ww, hh = int(W * 1.22), int(H * 1.22)
    im = Image.new("RGB", (ww, hh), CREAM)
    im.paste(cover(Image.open(a), ww // 2 - 4, hh), (0, 0)); im.paste(cover(Image.open(b), ww // 2 - 4, hh), (ww // 2 + 4, 0))
    im = im.convert("RGBA"); d = ImageDraw.Draw(im); r = 70; f = font("Jost-500.ttf", 84)
    for i, t in enumerate(labels):
        cx, cy = (ww // 4) + i * (ww // 2), int(hh * 0.62)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(245, 241, 237, 240))
        tw = text_width(t, f); draw_text(im, (cx - tw / 2, cy - 56), t, f, CHAR)
    out = out or os.path.join(OUT, f"_split_{os.path.basename(a)[:5]}_{os.path.basename(b)[:5]}.jpg")
    im.convert("RGB").save(out, quality=92); return out

def grid(paths, labels, out):
    ww, hh = int(W * 1.22), int(H * 1.22); im = Image.new("RGB", (ww, hh), CREAM)
    cw, ch = ww // 2, hh // 2
    for i, p in enumerate(paths):
        im.paste(cover(Image.open(p), cw - 4, ch - 4), ((i % 2) * cw + 2, (i // 2) * ch + 2))
    im = im.convert("RGBA")
    for i, t in enumerate(labels):
        b = label(t); im.alpha_composite(b, ((i % 2) * cw + (cw - b.width) // 2, (i // 2) * ch + ch - b.height - 40))
    im.convert("RGB").save(out, quality=92); return out

# ---------------- reels ----------------
def reels():
    R = {}
    s9 = split(src("11-15"), src("11-19"))
    R["2026-11-09"] = dict(format="This or that", segs=[
        dict(img=s9, dur=2.8, zoom=(1.0, 1.05), texts=[dict(block=hook("Which nap spot wins?"), y=SAFE_TOP + 40)]),
        dict(img=src("11-15"), dur=2.4, zoom=(1.0, 1.08), pan=((0.5, 0.55), (0.5, 0.5)), texts=[dict(block=label("1 · the round snuggle bed"), y=at_bottom(label("x")) - 40, t0=0.45)]),
        dict(img=src("11-19"), dur=2.4, zoom=(1.0, 1.08), pan=((0.5, 0.5), (0.52, 0.55)), texts=[dict(block=label("2 · the plush sofa bed"), y=at_bottom(label("x")) - 40, t0=0.45)]),
        dict(img=s9, dur=3.0, zoom=(1.05, 1.0), texts=[dict(block=cta("1 or 2? Comment your pick 👇"), y=at_bottom(cta("x")), t0=0.45)])],
        ig="Be honest: which nap spot would your pet pick? 🛏️\n\n1 = the round snuggle bed\n2 = the plush sofa bed\n\nComment 1 or 2 👇 and tag a friend who needs to vote.\n\n#dogsofinstagram #catsofinstagram #petsofinstagram #thisorthat #dogbed #catbed #cozyhome #napspot",
        fb="Which nap spot would your pet pick? 🛏️ 1 = the round snuggle bed, 2 = the plush sofa bed. Comment 1 or 2 👇")
    R["2026-11-10"] = dict(format="Rate this nap", segs=[
        dict(img=src("11-14"), dur=4.2, zoom=(1.0, 1.1), pan=((0.5, 0.55), (0.48, 0.58)), texts=[dict(block=hook("Rate this nap", "1 to 10"), y=SAFE_TOP + 40)]),
        dict(img=src("11-14"), dur=4.0, zoom=(1.12, 1.2), pan=((0.48, 0.58), (0.5, 0.6)), texts=[dict(block=cta("Comment your score 👇"), y=at_bottom(cta("x")), t0=0.45)])],
        ig="Rate this nap from 1 to 10 👇\n\nFireplace on, best friend next to you, zero plans. We're saying 11.\n\nSave this for the next cold evening. 🔥\n\n#dogsofinstagram #catsofinstagram #petsofinstagram #dogandcat #bestfriends #napgoals #cozyvibes #rateit",
        fb="Rate this nap from 1 to 10 👇 Fireplace on, best friend next to you, zero plans. We're saying 11. 🔥")
    R["2026-11-11"] = dict(format="POV", segs=[
        dict(img=src("11-02"), dur=3.4, zoom=(1.0, 1.07), pan=((0.5, 0.55), (0.5, 0.52)), texts=[dict(block=hook("POV: you got them the comfiest bed in the house", f=HOOK_S), y=SAFE_TOP + 40)]),
        dict(img=src("12-05"), dur=3.2, zoom=(1.0, 1.1), pan=((0.5, 0.55), (0.55, 0.6)), texts=[dict(block=hook("…and they chose the box 📦", f=HOOK_S), y=SAFE_TOP + 40)]),
        dict(img=src("12-05"), dur=2.8, zoom=(1.1, 1.16), pan=((0.55, 0.6), (0.56, 0.62)), texts=[dict(block=hook("…and they chose the box 📦", f=HOOK_S), y=SAFE_TOP + 40), dict(block=cta("Tag someone whose pet does this 👇"), y=at_bottom(cta("Tag someone whose pet does this 👇")), t0=0.45)])],
        ig="POV: you got them the comfiest bed in the house… and they chose the box. 📦😹\n\nTag someone whose pet does this 👇\n\n#catsofinstagram #dogsofinstagram #petsofinstagram #catsandboxes #funnypets #petlife #relatable #cozyhome",
        fb="POV: you got them the comfiest bed in the house… and they chose the box. 📦😹 Tag someone whose pet does this!")
    g12 = grid([src("12-01"), src("12-20"), src("11-26"), src("11-25")], ["1 · the burrito", "2 · the donut", "3 · the cuddler", "4 · the couch potato"], os.path.join(OUT, "_grid_12.jpg"))
    R["2026-11-12"] = dict(format="Which one is your pet", segs=[
        dict(img=src("12-01"), dur=2.4, zoom=(1.0, 1.06), texts=[dict(block=hook("Which one is your pet?", f=HOOK_S), y=SAFE_TOP + 40), dict(block=label("1 · the burrito"), y=at_bottom(label("x")) - 40, t0=0.45)]),
        dict(img=src("12-20"), dur=2.0, zoom=(1.0, 1.06), pan=((0.55, 0.55), (0.55, 0.55)), texts=[dict(block=label("2 · the donut"), y=at_bottom(label("x")) - 40, t0=0.45)]),
        dict(img=src("11-26"), dur=2.0, zoom=(1.0, 1.06), texts=[dict(block=label("3 · the cuddler"), y=at_bottom(label("x")) - 40, t0=0.45)]),
        dict(img=src("11-25"), dur=2.0, zoom=(1.0, 1.06), pan=((0.45, 0.6), (0.45, 0.6)), texts=[dict(block=label("4 · the couch potato"), y=at_bottom(label("x")) - 40, t0=0.45)]),
        dict(img=g12, dur=3.0, zoom=(1.04, 1.0), texts=[dict(block=cta("Which one is yours? Comment 1–4 👇"), y=SAFE_TOP + 40, t0=0.45)])],
        ig="Every pet has a sleeping style. Which one is yours? 👇\n\n1 · the burrito\n2 · the donut\n3 · the cuddler\n4 · the couch potato\n\nComment the number (bonus points for a photo in our DMs). 📸\n\n#dogsofinstagram #catsofinstagram #petsofinstagram #sleepingpets #whichoneareyou #petpersonality #cozyhome",
        fb="Every pet has a sleeping style. Which one is yours? 1 the burrito, 2 the donut, 3 the cuddler, 4 the couch potato 👇")
    R["2026-11-13"] = dict(format="Caption this", segs=[
        dict(img=src("11-13"), dur=4.0, zoom=(1.0, 1.08), pan=((0.5, 0.6), (0.52, 0.62)), texts=[dict(block=hook("Caption this 😂"), y=SAFE_TOP + 40)]),
        dict(img=src("11-13"), dur=4.0, zoom=(1.15, 1.25), pan=((0.52, 0.62), (0.5, 0.6)), texts=[dict(block=hook("Caption this 😂"), y=SAFE_TOP + 40), dict(block=cta("Best caption gets featured in our story 👇"), y=at_bottom(cta("Best caption gets featured in our story 👇")), t0=0.45)])],
        ig="Caption this. 😂👇\n\nThe best caption gets featured in our story this weekend.\n\n#catsofinstagram #petsofinstagram #captionthis #funnycats #catlife #indoorcat #catmom",
        fb="Caption this 😂 The best caption gets featured in our story this weekend 👇")
    R["2026-11-14"] = dict(format="Guess", segs=[
        dict(img=src("11-22"), dur=3.2, zoom=(1.75, 1.85), pan=((0.38, 0.8), (0.4, 0.82)), texts=[dict(block=hook("Guess what this is for 🤔", f=HOOK_S), y=SAFE_TOP + 40)]),
        dict(img=src("11-22"), dur=3.4, zoom=(1.6, 1.0), pan=((0.4, 0.82), (0.5, 0.55)), texts=[dict(block=cta("Comment your guess 👇"), y=at_bottom(cta("x")), t0=0.45)]),
        dict(img=src("11-22"), dur=2.8, zoom=(1.0, 1.05), pan=((0.5, 0.55), (0.5, 0.52)), texts=[dict(block=hook("Little legs, big bed? Problem solved.", f=HOOK_S), y=SAFE_TOP + 40), dict(block=label("Ascend Pet Stairs"), y=at_bottom(label("x")) - 40, t0=0.45)])],
        ig="Did you guess it? 🤔\n\nAscend gives little legs (and senior joints) an easy way up to the bed or sofa. No more jumping.\n\nTag a dachshund parent who needs this 👇\n\n#dogsofinstagram #dachshund #seniordog #petsofinstagram #guessit #dogstairs #smalldogs #cozyhome",
        fb="Did you guess it? 🤔 Ascend gives little legs (and senior joints) an easy way up to the bed or sofa: https://cozycompanion.us/products/ascend-acacia-pet-stairs-ramp")
    s15 = split(src("11-21"), src("11-06"), labels=("🐶", "🐱"), out=os.path.join(OUT, "_split_15.jpg"))
    R["2026-11-15"] = dict(format="Team dog or team cat", segs=[
        dict(img=s15, dur=2.8, zoom=(1.0, 1.05), texts=[dict(block=hook("Team dog or team cat?", f=HOOK_S), y=SAFE_TOP + 40)]),
        dict(img=src("11-21"), dur=2.3, zoom=(1.0, 1.08), texts=[dict(block=label("Team 🐶"), y=at_bottom(label("x")) - 40, t0=0.45)]),
        dict(img=src("11-06"), dur=2.3, zoom=(1.0, 1.08), pan=((0.5, 0.6), (0.5, 0.6)), texts=[dict(block=label("Team 🐱"), y=at_bottom(label("x")) - 40, t0=0.45)]),
        dict(img=s15, dur=3.0, zoom=(1.05, 1.0), texts=[dict(block=cta("Comment 🐶 or 🐱 👇"), y=at_bottom(cta("x")), t0=0.45)])],
        ig="The big question: team dog or team cat? 🐶🐱\n\nComment your team 👇 (both is allowed, we won't judge).\n\n#dogsofinstagram #catsofinstagram #petsofinstagram #teamdog #teamcat #dogsandcats #petlovers #cozyhome",
        fb="The big question: team dog or team cat? 🐶🐱 Comment your team 👇")
    return R

# ---------------- stories ----------------
def put_wm(im, w):
    """Light wordmark on a small dark pill so it reads on bright photos too."""
    wm = wordmark(w); pw, ph = wm.width + 56, wm.height + 30
    pill = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle((0, 0, pw - 1, ph - 1), ph // 2, fill=(26, 26, 26, 150))
    pill.alpha_composite(wm, (28, 15)); im.alpha_composite(pill, ((W - pw) // 2, SAFE_TOP - ph - 30))

def story_bg(p, focus=(0.5, 0.5)):
    im = cover(Image.open(p), W, H, focus).convert("RGBA")
    shade = Image.new("L", (1, H))
    for y in range(H):
        shade.putpixel((0, y), int(150 * max(0, (y - 900) / 1020) ** 1.2 + 60 * max(0, (500 - y) / 500)))
    sh = Image.new("RGBA", (W, H), CHAR + (0,)); sh.putalpha(shade.resize((W, H))); im.alpha_composite(sh)
    put_wm(im, 260)
    return im

def story_q(p, eyebrow, q, reply, focus=(0.5, 0.5)):
    im = story_bg(p, focus)
    b = text_block([(eyebrow, EYEBROW, ROSE, 5), (q, font("Cormorant-600.ttf", 76), CHAR, 0), (reply, font("Jost-500.ttf", 44), CHAR, 1)],
                   max_w=900, bg=(245, 241, 237, 238), pad=(56, 44), gap=18)
    im.alpha_composite(b, ((W - b.width) // 2, SAFE_BOTTOM - b.height - 40))
    return im.convert("RGB")

def story_rate(p, what, focus=(0.5, 0.5)):
    im = story_bg(p, focus)
    b = text_block([("RATE IT", EYEBROW, ROSE, 5), (what, font("Cormorant-600.ttf", 76), CHAR, 0)], max_w=900, bg=(245, 241, 237, 238), pad=(56, 40))
    nums = Image.new("RGBA", (b.width, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(nums); f = font("Jost-500.ttf", 40)
    n = 10; cw = (b.width - 60) / n
    for i in range(n):
        cx = 30 + cw * i + cw / 2; d.ellipse((cx - 38, 22, cx + 38, 98), fill=(26, 26, 26, 215))
        t = str(i + 1); tw = d.textlength(t, font=f); d.text((cx - tw / 2, 34), t, font=f, fill=CREAM)
    r = text_block([("Reply with your number 👇", font("Jost-500.ttf", 44), CREAM, 1)], bg=(26, 26, 26, 170), pad=(44, 26))
    y = SAFE_BOTTOM - 40 - r.height - 20 - nums.height - 20 - b.height
    im.alpha_composite(b, ((W - b.width) // 2, y)); im.alpha_composite(nums, ((W - nums.width) // 2, y + b.height + 20))
    im.alpha_composite(r, ((W - r.width) // 2, y + b.height + 20 + nums.height + 20))
    return im.convert("RGB")

def story_lr(a, b, q):
    im = Image.new("RGB", (W, H), CREAM); im.paste(cover(Image.open(a), W // 2 - 3, H), (0, 0)); im.paste(cover(Image.open(b), W // 2 - 3, H), (W // 2 + 3, 0))
    im = im.convert("RGBA"); d = ImageDraw.Draw(im); f = font("Jost-500.ttf", 72); r = 62
    for i, t in enumerate(("L", "R")):
        cx, cy = W // 4 + i * (W // 2), int(H * 0.52)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(245, 241, 237, 240)); tw = d.textlength(t, font=f); d.text((cx - tw / 2, cy - 48), t, font=f, fill=CHAR)
    top = text_block([(q, font("Cormorant-600.ttf", 80), CHAR, 0)], max_w=900, bg=(245, 241, 237, 238), pad=(56, 36))
    im.alpha_composite(top, ((W - top.width) // 2, SAFE_TOP + 40))
    rep = text_block([("Reply L or R 👇", font("Jost-500.ttf", 48), CREAM, 1)], bg=(26, 26, 26, 175), pad=(48, 28))
    im.alpha_composite(rep, ((W - rep.width) // 2, SAFE_BOTTOM - rep.height - 40))
    put_wm(im, 220)
    return im.convert("RGB")

STORIES = {
    "2026-11-09": [("q", "12-26", "QUESTION OF THE DAY", "What's your pet's weirdest sleeping spot?", "Reply and tell us 👇"),
                   ("rate", "11-09", "Rate this cat tree setup"),
                   ("lr", "12-06", "11-25", "Which sofa would your pet steal?")],
    "2026-11-10": [("q", "11-08", "BE HONEST", "Does your dog steal your spot on the couch?", "Reply 🔥 if yes"),
                   ("rate", "12-10", "Rate this breakfast setup"),
                   ("lr", "11-17", "12-27", "Snuffle mat or puzzle feeder?")],
    "2026-11-11": [("q", "11-03", "QUICK QUESTION", "Does your cat drink more from running water?", "Reply YES or NO 👇"),
                   ("rate", "11-12", "Rate this feeding station"),
                   ("lr", "11-05", "11-20", "Snow walk or bath day?")],
    "2026-11-12": [("q", "12-24", "SAY HI", "What's your pet's name?", "Reply 👇 we'll say hi"),
                   ("rate", "11-27", "Rate this play session"),
                   ("lr", "12-02", "12-16", "Back seat or front seat co-pilot?")],
    "2026-11-13": [("q", "12-18", "RELATABLE?", "Does your cat attack the toy like this?", "Reply 🔥 if yours does too"),
                   ("rate", "12-30", "Rate this spa day"),
                   ("lr", "12-09", "12-31", "Sofa or den?")],
    "2026-11-14": [("q", "11-11", "YOUR TURN", "Describe your pet today in one emoji", "Reply with it 👇"),
                   ("rate", "12-14", "Rate this winter outfit"),
                   ("lr", "12-22", "12-21", "Which bed would they pick?")],
    "2026-11-15": [("q", "12-07", "SUNDAY QUESTION", "What's your pet's favorite treat?", "Reply 👇 we're taking notes"),
                   ("rate", "12-04", "Rate this snow day"),
                   ("lr", "11-28", "11-14", "City walk or fireplace nap?")],
}

def stories():
    out = {}
    for day, items in STORIES.items():
        for slot, it in zip(("am", "mid", "pm"), items):
            p = os.path.join(OUT, f"org_st_{day}_{slot}.jpg")
            if it[0] == "q": im = story_q(src(it[1]), it[2], it[3], it[4])
            elif it[0] == "rate": im = story_rate(src(it[1]), it[2])
            else: im = story_lr(src(it[1]), src(it[2]), it[3])
            im.save(p, quality=90); out[(day, slot)] = (p, it)
    return out

if __name__ == "__main__":
    R = reels(); S = stories()
    for day, r in R.items():
        mp4 = os.path.join(OUT, f"org_reel_{day}.mp4"); render(r["segs"], mp4, AUD)
        still = os.path.join(OUT, f"org_still_{day}.jpg")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.2", "-i", mp4, "-frames:v", "1", "-q:v", "2", still], check=True)
        sheet = os.path.join(OUT, f"_qa_{day}.jpg")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-vf", "fps=1,scale=270:-1,tile=6x2", "-frames:v", "1", sheet], check=False)
        print("reel", day, r["format"])
    json.dump({d: {k: v for k, v in r.items() if k != "segs"} for d, r in R.items()}, open(os.path.join(OUT, "captions.json"), "w"), indent=1, ensure_ascii=False)
    print("stories", len(S))
