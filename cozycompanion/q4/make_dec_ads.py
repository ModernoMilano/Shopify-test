"""December 2026 Meta ad creatives ("The Cozy Season", light look) from the APPROVED December calendar photos.
Layout: photo on top (never covered), cream panel below with rose eyebrow, charcoal Cormorant headline, a Jost line and a
small CTA pill. 4:5 = 1080x1350; 9:16 = 1080x1920 with all text between y 1240 and 1560 (Reels/Stories UI safe zones:
nothing in the top 250 px or bottom 340 px). No prices.
  python3 q4/make_dec_ads.py            -> renders q4/out/ad_<id>_45.jpg / _916.jpg
  python3 q4/make_dec_ads.py --upload   -> also uploads each as Shopify file q4_ad_<id>_45 / _916 (sequential)"""
import os, sys, io, json, ssl, subprocess, urllib.request
from PIL import Image, ImageDraw, ImageFont
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, S)
from lib import DOMAIN
F = os.path.join(S, "ads", "fonts"); OUT = os.path.join(S, "q4", "out"); os.makedirs(OUT, exist_ok=True)
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
CREAM, CHAR, ROSE, SAND = (245, 241, 237), (26, 26, 26), (183, 110, 121), (235, 227, 218)
reg = json.load(open(os.path.join(S, "files.json")))
def font(n, s): return ImageFont.truetype(os.path.join(F, n + ".ttf"), s)

_cache = {}
def photo(name):
    if name not in _cache:
        u = reg[name]["url"].split("?")[0]
        _cache[name] = Image.open(io.BytesIO(urllib.request.urlopen(f"https://{DOMAIN}/cdn/shop/files/" + u.split("/files/")[-1], context=CTX).read())).convert("RGB")
    return _cache[name]

# id: eyebrow, headline, line, cta, 4:5 photo (+focus y), 9:16 photo (+focus y)
ADS = {
    "D1":  ("THE COZY SEASON", "Gifts for the dog\nwho has everything.", None, "Shop the gift guide", ("f_2026-12-02_1_raw", .62), ("st_2026-12-02_raw", .52)),
    "D1b": ("ORDER BY DEC 5", "Gifts for the dog\nwho has everything.", "for the best chance of delivery before Christmas", "Shop the gift guide", ("f_2026-12-02_1_raw", .62), ("st_2026-12-02_raw", .52)),
    "D2":  ("THE COZY SEASON", "Gifts for the cat\nwho rules the house.", None, "Shop the gift guide", ("f_2026-12-03_0_raw", .60), ("st_2026-12-03_raw", .62)),
    "D2b": ("ORDER BY DEC 5", "Gifts for the cat\nwho rules the house.", "for the best chance of delivery before Christmas", "Shop the gift guide", ("f_2026-12-03_0_raw", .60), ("st_2026-12-03_raw", .62)),
    "D3":  ("COMPLETE THE SET", "The Cozy Nap Set.", "20% off automatically when you buy the set", "Shop the set", ("f_2026-12-12_0_raw", .64), ("st_2026-12-12_raw", .66)),
    "D4":  ("LAST-MINUTE GIFTING", "Too late to ship?\nGive a gift card.", "Delivered instantly by email", "Shop gift cards", ("f_2026-12-17_0_raw", .42), ("st_2026-12-17_v2_raw", .38)),
}
NEEDS_APPROVAL = {"D4": "gift card product not created yet (gift cards must be activated in Shopify admin first)"}

def cover(im, w, h, fy):
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = int(min(max(im.height * fy - h / 2, 0), im.height - h))
    return im.crop((x, y, x + w, y + h))

def spaced(d, text, f, y, fill, sp, W):
    tw = sum(d.textlength(c, font=f) for c in text) + sp * (len(text) - 1); x = (W - tw) / 2
    for c in text: d.text((x, y), c, font=f, fill=fill); x += d.textlength(c, font=f) + sp

def wrap(d, text, f, maxw):
    if "\n" in text: return text.split("\n")
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def render(aid, fmt):
    eyebrow, head, line, cta, p45, p916 = ADS[aid]
    W, H = (1080, 1350) if fmt == "45" else (1080, 1920)
    ph_h = 880 if fmt == "45" else 1180
    name, fy = p45 if fmt == "45" else p916
    canvas = Image.new("RGB", (W, H), CREAM)
    canvas.paste(cover(photo(name), W, ph_h, fy), (0, 0))
    d = ImageDraw.Draw(canvas)
    d.line([(0, ph_h), (W, ph_h)], fill=SAND, width=2)
    fe, fh, fl, fc = font("Jost-500", 24), font("Cormorant-600", 66), font("Jost-400", 29), font("Jost-500", 22)
    hl = wrap(d, head, fh, W - 160)
    block = 24 + 22 + len(hl) * 76 + (14 + 38 if line else 0) + 30 + 58
    top = ph_h + 44 if fmt == "45" else 1240 + max(0, (320 - block) // 2)
    y = top
    spaced(d, eyebrow, fe, y, ROSE, 5, W); y += 24 + 22
    for t in hl:
        d.text(((W - d.textlength(t, font=fh)) / 2, y), t, font=fh, fill=CHAR); y += 76
    if line:
        y += 14; d.text(((W - d.textlength(line, font=fl)) / 2, y), line, font=fl, fill=(80, 74, 70)); y += 38
    y += 30
    lab = cta.upper()
    cw = sum(d.textlength(c, font=fc) for c in lab) + 3 * (len(lab) - 1) + 64
    x0 = (W - cw) / 2; d.rectangle([x0, y, x0 + cw, y + 58], fill=CHAR)
    spaced(d, lab, fc, y + 17, CREAM, 3, W)
    if fmt == "45":
        logo = Image.open(os.path.join(S, "logo", "logo-dark.png")).convert("RGBA"); logo = logo.crop(logo.getbbox())
        lw = 150; logo = logo.resize((lw, round(lw * logo.height / logo.width)), Image.LANCZOS)
        canvas.paste(logo, ((W - lw) // 2, H - logo.height - 26), logo)
    if fmt == "916":
        assert y + 58 <= 1580, f"{aid} 9:16 text leaves the safe zone ({y + 58})"
    out = os.path.join(OUT, f"ad_{aid}_{fmt}.jpg"); canvas.save(out, quality=92)
    return out

if __name__ == "__main__":
    done = {}
    for aid in ADS:
        for fmt in ("45", "916"):
            p = render(aid, fmt); done[f"{aid}_{fmt}"] = p
            if "--upload" in sys.argv:
                subprocess.run([sys.executable, "-I", os.path.join(S, "staged_one.py"), p, f"q4_ad_{aid}_{fmt}",
                                f"CozyCompanion December ad {aid}"], check=True, capture_output=True)
    meta = {k: {"local": v, "url": (json.load(open(os.path.join(S, "files.json"))).get(f"q4_ad_{k}", {}).get("url", "").split("?")[0] or None),
                "needs_owner_approval": NEEDS_APPROVAL.get(k.split("_")[0])} for k, v in done.items()}
    json.dump(meta, open(os.path.join(S, "q4", "dec_ads.json"), "w"), indent=1)
    print("rendered", len(done))
