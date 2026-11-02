"""BFCM "Black Velvet Edit" creatives: offer overlays on the QA-approved Nano Banana photos.

Renders into bfcm/out/:
- ads in 4:5 (1080x1350) and 9:16 (1080x1920);
- the feed posts that carry text;
- 33 stories (1080x1920).

Text is always drawn here with PIL, never generated. Copy follows bfcm/BRIEF.md (exact tiers, no fake scarcity).
Safe zones for 9:16: no text in the top 250 px or the bottom 340 px.
usage: python3 bfcm/make_overlays.py            (renders everything; prints the output list)
"""
import os, io, json, ssl, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(S, "bfcm", "out"); os.makedirs(OUT, exist_ok=True)
CACHE = "/tmp/claude-0/-home-user-Shopify-test/7ae2a11e-4ae5-5a99-ac75-b7957d6a039d/scratchpad/bfcm"
os.makedirs(CACHE, exist_ok=True)
F = os.path.join(S, "ads", "fonts")
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
DOMAIN = os.environ["COZY_SHOPIFY_DOMAIN"]
REG = json.load(open(os.path.join(S, "files.json")))

CREAM = (245, 241, 237); CHAR = (26, 26, 26); ROSE = (183, 110, 121)
EYEBROW = "BLACK FRIDAY WEEK"
HEAD = "Black Friday, the cozy way."
TIER1 = "Save 10% · 15% · 20%"
TIER2 = "on orders $75 · $150 · $250+"
SMALL = "Applied automatically · cozycompanion.us"

# which QA-approved photo is used for each asset id
CLEAN = {"A1_45": "bfcm_A1_45", "A1_916": "bfcm_A1_916", "A2_45": "bfcm_A2_45", "A2_916": "bfcm_A2_916",
         "A3_45": "bfcm_A3_45", "A3_916": "bfcm_A3_916", "A4_45": "bfcm_A4_45_v2", "A4_916": "bfcm_A4_916_v2",
         "P1": "bfcm_P1", "P3a": "bfcm_P3a_v2", "P3b": "bfcm_P3b", "P3c": "bfcm_P3c_v2", "P4a": "bfcm_P4a_v2",
         "P4b": "bfcm_P4b", "P4c": "bfcm_P4c", "P5": "bfcm_P5", "P6a": "bfcm_P6a", "P6b": "bfcm_P6b", "P6c": "bfcm_P6c",
         "P7": "bfcm_P7", "P8": "bfcm_P8", "P9": "bfcm_P9", "P10": "bfcm_P10",
         "SB1": "bfcm_SB1", "SB2": "bfcm_SB2", "SB3": "bfcm_SB3", "SB4": "bfcm_SB4", "SB5": "bfcm_SB5", "SB6": "bfcm_SB6",
         "W1": "bfcm_W1", "W2": "bfcm_W2", "W3": "bfcm_W3"}

def font(name, size): return ImageFont.truetype(os.path.join(F, name + ".ttf"), size)

def photo(asset):
    name = CLEAN[asset]; path = os.path.join(CACHE, name + ".png")
    if not os.path.exists(path):
        f = REG[name]["url"].split("/files/")[-1].split("?")[0]
        open(path, "wb").write(urllib.request.urlopen(f"https://{DOMAIN}/cdn/shop/files/{f}", context=CTX).read())
    return Image.open(path).convert("RGB")

def cover(im, W, H, fy=0.5):
    s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H))

def shade(im, y0, y1, a0, a1):
    """charcoal gradient band from alpha a0 at y0 to a1 at y1 (and a1 beyond y1 in that direction)"""
    W, H = im.size; ov = Image.new("L", (W, H), 0); d = ImageDraw.Draw(ov)
    step = 1 if y1 >= y0 else -1
    for y in range(y0, y1, step):
        t = (y - y0) / (y1 - y0); d.line([(0, y), (W, y)], fill=int(a0 + (a1 - a0) * t))
    if step == 1: d.rectangle([0, y1, W, H], fill=a1)
    else: d.rectangle([0, 0, W, y1], fill=a1)
    layer = Image.new("RGBA", (W, H), CHAR + (0,)); layer.putalpha(ov)
    base = im.convert("RGBA"); base.alpha_composite(layer)
    return base

def foil(size_wh, draw_fn):
    """rose-gold foil: text mask filled with a soft vertical gradient"""
    w, h = size_wh; mask = Image.new("L", (w, h), 0); draw_fn(ImageDraw.Draw(mask))
    grad = Image.new("RGB", (w, h)); gd = ImageDraw.Draw(grad)
    for y in range(h):
        t = (y % 80) / 80; c1, c2 = (226, 170, 178), (168, 98, 109)
        c = tuple(int(c1[i] + (c2[i] - c1[i]) * abs(1 - 2 * t)) for i in range(3)); gd.line([(0, y), (w, y)], fill=c)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0)); layer.paste(grad, (0, 0), mask); return layer

def spaced_w(d, text, f, sp): return sum(d.textlength(c, font=f) for c in text) + sp * (len(text) - 1)

def draw_spaced(d, text, f, cx, y, fill, sp):
    x = cx - spaced_w(d, text, f, sp) / 2
    for c in text: d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + sp

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def block(im, y, items, maxw=940):
    """items: list of (kind, text). Draws centred, returns bottom y."""
    W = im.width; cx = W / 2; d = ImageDraw.Draw(im)
    for kind, text in items:
        if kind == "eyebrow":
            f = font("Jost-500", 26); lay = foil(im.size, lambda dd: draw_spaced(dd, text, f, cx, y, 255, 7))
            im.alpha_composite(lay); y += 54
        elif kind == "head":
            f = font("Cormorant-600", 78)
            for line in wrap(d, text, f, maxw):
                d.text((cx - d.textlength(line, font=f) / 2, y), line, font=f, fill=CREAM); y += 84
            y += 14
        elif kind == "headbig":
            f = font("Cormorant-600", 104)
            for line in wrap(d, text, f, maxw):
                d.text((cx - d.textlength(line, font=f) / 2, y), line, font=f, fill=CREAM); y += 108
            y += 16
        elif kind == "tier":
            f = font("Jost-500", 36); lay = foil(im.size, lambda dd: dd.text((cx - dd.textlength(text, font=f) / 2, y), text, font=f, fill=255))
            im.alpha_composite(lay); y += 50
        elif kind == "line":
            f = font("Jost-400", 32)
            for line in wrap(d, text, f, maxw):
                d.text((cx - d.textlength(line, font=f) / 2, y), line, font=f, fill=CREAM); y += 44
            y += 6
        elif kind == "small":
            f = font("Jost-400", 24); draw_spaced(d, text, f, cx, y, CREAM + (200,), 2); y += 40
        elif kind == "rule":
            d.line([(cx - 40, y + 6), (cx + 40, y + 6)], fill=ROSE, width=2); y += 30
        elif kind == "gap":
            y += int(text)
    return y

def wordmark(im, y, w=300):
    lg = Image.open(os.path.join(S, "logo", "logo-light.png")).convert("RGBA"); lg = lg.crop(lg.getbbox())
    lg = lg.resize((w, round(w * lg.height / lg.width)), Image.LANCZOS); im.alpha_composite(lg, ((im.width - w) // 2, y))
    return y + lg.height

OFFER = [("eyebrow", EYEBROW), ("head", HEAD), ("tier", TIER1), ("tier", TIER2), ("gap", "6"), ("small", SMALL)]

def save(im, name):
    p = os.path.join(OUT, name + ".jpg"); im.convert("RGB").save(p, quality=92, optimize=True); return p

def ad45(asset, fy=0.5):
    im = cover(photo(asset), 1080, 1350, fy); im = shade(im, 760, 1010, 0, 225)
    block(im, 1020, OFFER); return save(im, f"ad_{asset}")

def ad916(asset, fy=0.5):
    im = cover(photo(asset), 1080, 1920, fy); im = shade(im, 820, 470, 0, 215)
    block(im, 285, OFFER); return save(im, f"ad_{asset}")

def feed_bottom(asset, items, name, fy=0.5, top=980):
    im = cover(photo(asset), 1080, 1350, fy); im = shade(im, top - 260, top - 20, 0, 220)
    block(im, top, items); return save(im, name)

def feed_top(asset, items, name, fy=0.5, start=110, fade_to=560):
    im = cover(photo(asset), 1080, 1350, fy); im = shade(im, fade_to, fade_to - 260, 0, 215)
    y = wordmark(im, start, 240) + 34; block(im, y, items); return save(im, name)

def story_bg(asset, items, name, fy=0.5):
    im = cover(photo(asset), 1080, 1920, fy); im = shade(im, 1150, 820, 0, 150)
    y = wordmark(im, 300, 300) + 70; block(im, y, items); return save(im, name)

def story_card(asset, items, name, fy=0.5):
    im = Image.new("RGBA", (1080, 1920), CHAR + (255,))
    y = block(im, 290, items)
    card = cover(photo(asset), 960, 1200, fy); top = max(y + 20, 540)
    im.alpha_composite(card.convert("RGBA"), (60, top)); return save(im, name)

TIERS_EXPLAIN = [("eyebrow", "HOW IT WORKS"), ("head", "Black Friday Week"), ("rule", ""),
                 ("tier", "10% off orders $75+"), ("tier", "15% off orders $150+"), ("tier", "20% off orders $250+"),
                 ("gap", "10"), ("line", "Applied automatically at checkout. No code needed."), ("small", "Nov 23 – 30 · cozycompanion.us")]
TIERS_SHORT = [("tier", TIER1), ("tier", TIER2)]

def product_story(asset, guide, product, name):
    return story_card(asset, [("eyebrow", guide), ("head", product), ("small", "Shop via link in bio")], name)

STORIES = [
    ("2026-11-20", "am", lambda n: story_bg("SB1", [("eyebrow", EYEBROW), ("headbig", "Starts in 3 days."), ("line", "Monday, November 23.")], n)),
    ("2026-11-20", "mid", lambda n: story_card("A3_916", [("eyebrow", "COMING MONDAY"), ("head", "Black Friday, the cozy way.")], n, 0.62)),
    ("2026-11-20", "pm", lambda n: story_bg("SB2", [("eyebrow", "SAVE THE DATE"), ("headbig", "Nov 23 – 30"), ("line", "Up to 20% off, applied automatically.")], n)),
    ("2026-11-21", "am", lambda n: story_card("P1", [("eyebrow", EYEBROW), ("headbig", "2 days to go.")], n)),
    ("2026-11-21", "mid", lambda n: story_bg("SB3", [("eyebrow", "STARTS MONDAY"), ("head", "Save up to 20% on the things they love most.")], n)),
    ("2026-11-21", "pm", lambda n: story_card("P4b", [("eyebrow", "START YOUR WISHLIST"), ("head", "Haven Pet Den"), ("small", "Shop via link in bio")], n)),
    ("2026-11-22", "am", lambda n: story_bg("SB4", [("eyebrow", EYEBROW), ("headbig", "Tomorrow.")], n)),
    ("2026-11-22", "mid", lambda n: story_bg("SB5", [("eyebrow", "STARTS TOMORROW"), ("head", "How it works"), ("rule", ""),
                                                     ("tier", "10% off orders $75+"), ("tier", "15% off orders $150+"), ("tier", "20% off orders $250+"),
                                                     ("line", "Applied automatically. No code needed.")], n)),
    ("2026-11-22", "pm", lambda n: product_story("A3_916", "ON YOUR WISHLIST?", "Chester Tufted Dog Sofa", n)),
    ("2026-11-23", "am", lambda n: story_bg("SB1", [("eyebrow", "IT'S HERE"), ("head", HEAD)] + TIERS_SHORT + [("small", "Applied automatically")], n)),
    ("2026-11-23", "mid", lambda n: story_card("A1_916", [("eyebrow", EYEBROW), ("head", "They stole your spot. Make it official.")], n, 0.62)),
    ("2026-11-23", "pm", lambda n: story_bg("SB5", TIERS_EXPLAIN, n)),
    ("2026-11-24", "am", lambda n: product_story("A2_916", EYEBROW, "Dine Automatic Feeder", n)),
    ("2026-11-24", "mid", lambda n: product_story("A1_916", EYEBROW, "Nestle Heated Pet Pad", n)),
    ("2026-11-24", "pm", lambda n: story_bg("SB2", TIERS_EXPLAIN, n)),
    ("2026-11-25", "am", lambda n: product_story("P3a", "GIFT GUIDE · FOR THE DOG", "Chester Tufted Dog Sofa", n)),
    ("2026-11-25", "mid", lambda n: product_story("P3b", "GIFT GUIDE · FOR THE DOG", "Dream Memory Foam Dog Bed", n)),
    ("2026-11-25", "pm", lambda n: product_story("P4a", "GIFT GUIDE · FOR THE CAT", "Perch Modern Cat Tree", n)),
    ("2026-11-26", "am", lambda n: story_bg("SB6", [("eyebrow", "HAPPY THANKSGIVING"), ("head", "From our pack to yours.")], n)),
    ("2026-11-26", "mid", lambda n: story_card("P9", [("eyebrow", "THANKFUL FOR"), ("head", "Naps like these.")], n, 0.7)),
    ("2026-11-26", "pm", lambda n: story_bg("SB3", [("eyebrow", EYEBROW), ("head", "Still on through Monday.")] + TIERS_SHORT, n)),
    ("2026-11-27", "am", lambda n: story_card("P5", [("eyebrow", EYEBROW), ("headbig", "Black Friday is here.")], n, 0.7)),
    ("2026-11-27", "mid", lambda n: product_story("P4c", "GIFT GUIDE · FOR THE CAT", "Pounce Automatic Feather Cat Toy", n)),
    ("2026-11-27", "pm", lambda n: story_bg("SB5", TIERS_EXPLAIN, n)),
    ("2026-11-28", "am", lambda n: product_story("P6a", "LITTLE LUXURIES", "Snug Sherpa Pet Blanket", n)),
    ("2026-11-28", "mid", lambda n: product_story("P6b", "LITTLE LUXURIES", "Nestle Heated Pet Pad", n)),
    ("2026-11-28", "pm", lambda n: product_story("P6c", "LITTLE LUXURIES", "Peak Triangle Cat Scratcher", n)),
    ("2026-11-29", "am", lambda n: story_card("P7", [("eyebrow", "FINAL DAYS"), ("head", "Black Friday Week ends Monday.")], n)),
    ("2026-11-29", "mid", lambda n: product_story("A4_916", EYEBROW, "Perch Modern Cat Tree", n)),
    ("2026-11-29", "pm", lambda n: story_card("P8", [("eyebrow", "ENDS MONDAY"), ("head", "11:59 pm ET.")], n, 0.7)),
    ("2026-11-30", "am", lambda n: story_card("P9", [("eyebrow", "CYBER MONDAY"), ("headbig", "Last chance.")], n, 0.7)),
    ("2026-11-30", "mid", lambda n: story_bg("SB2", TIERS_EXPLAIN, n)),
    ("2026-11-30", "pm", lambda n: story_bg("SB4", [("eyebrow", "CYBER MONDAY"), ("headbig", "Ends tonight."), ("line", "11:59 pm ET.")] + TIERS_SHORT, n)),
]

def render_all():
    out = {}
    for a in ("A1", "A2", "A3", "A4"):
        out[f"{a}_45"] = ad45(f"{a}_45")
        out[f"{a}_916"] = ad916(f"{a}_916")
    out["P1"] = feed_bottom("P1", [("eyebrow", EYEBROW), ("head", "Starts Monday, November 23.")], "feed_P1")
    # P2a: typographic launch slide on the velvet-and-gifts photo (gifts in the lower third, copy above)
    im = cover(photo("P10"), 1080, 1350, 0.5); im = shade(im, 860, 600, 0, 140)
    y = wordmark(im, 120, 260) + 50
    block(im, y, [("eyebrow", "BLACK FRIDAY WEEK · NOV 23–30"), ("head", HEAD), ("rule", ""),
                  ("tier", "10% off orders $75+"), ("tier", "15% off orders $150+"), ("tier", "20% off orders $250+"),
                  ("gap", "8"), ("line", "Applied automatically at checkout. No code needed.")])
    out["P2a"] = save(im, "feed_P2a")
    out["P5"] = feed_top("P5", [("eyebrow", EYEBROW), ("headbig", "Black Friday is here.")] + TIERS_SHORT, "feed_P5", fade_to=640)
    out["P8"] = feed_top("P8", [("eyebrow", "BLACK FRIDAY WEEK ENDS"), ("headbig", "Monday, 11:59 pm ET.")] + TIERS_SHORT, "feed_P8", fade_to=640)
    out["P9"] = feed_top("P9", [("eyebrow", "CYBER MONDAY"), ("headbig", "Last chance.")] + TIERS_SHORT, "feed_P9", fade_to=620)
    out["P10"] = feed_top("SB2", [("eyebrow", "CYBER MONDAY"), ("headbig", "Ends tonight."), ("line", "Black Friday Week ends at 11:59 pm ET.")] + TIERS_SHORT, "feed_P10", fade_to=700)
    stories = []
    for date, slot, fn in STORIES:
        n = f"story_{date[5:]}_{slot}"; stories.append({"date": date, "slot": slot, "path": fn(n)})
    out["stories"] = stories
    return out

if __name__ == "__main__":
    r = render_all(); print(json.dumps({k: v for k, v in r.items() if k != "stories"}, indent=1)); print(len(r["stories"]), "stories")
