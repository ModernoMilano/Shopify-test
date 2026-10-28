"""Branded explainer photos for every product page (2:3, 1600x2400), in the house style:
  i_why_<handle>  'Why you'll love it': our packshot + the three highlights
  i_det_<handle>  'The details': our lifestyle shot + description bullets + spec line
  i_promise       one shared card: shipping, returns, checkout, COZY15
Text comes from the product itself (highlight metafields + description), so nothing is claimed that isn't on the page.
Usage: python3 -I infographics.py [--preview] [handle ...]   (no handles = every product in gallery.GALLERIES)
"""
import sys, os, io, re, ast, json, html, ssl, subprocess, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, S)
from lib import gql, DOMAIN

CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
F = lambda n, s: ImageFont.truetype(os.path.join(S, "ads", "fonts", n), s)
CREAM, SAND, CHAR, ROSE, WHITE = (245, 241, 237), (235, 227, 218), (26, 26, 26), (183, 110, 121), (255, 255, 255)
W, H = 1600, 2400
OUT = os.path.join(S, "infographics_out"); os.makedirs(OUT, exist_ok=True)
reg = json.load(open(os.path.join(S, "files.json")))
src = open(os.path.join(S, "gallery.py")).read()
GALLERIES = ast.literal_eval(src[src.index("GALLERIES = {") + len("GALLERIES = "): src.index("\n}\n", src.index("GALLERIES = {")) + 2])
LOGO = Image.open(os.path.join(S, "logo", "logo-dark.png")).convert("RGBA"); LOGO = LOGO.crop(LOGO.getbbox())
LOGO_LIGHT = Image.open(os.path.join(S, "logo", "logo-light.png")).convert("RGBA"); LOGO_LIGHT = LOGO_LIGHT.crop(LOGO_LIGHT.getbbox())

def fetch(name, width=1600):
    u = f"https://{DOMAIN}/cdn/shop/files/" + reg[name]["url"].split("/files/")[-1].split("?")[0] + f"?width={width}"
    return Image.open(io.BytesIO(urllib.request.urlopen(u, context=CTX).read())).convert("RGB")

def cover(im, w, h, focus_y=0.5):
    s = max(w / im.width, h / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = round((im.height - h) * focus_y)
    return im.crop((x, y, x + w, y + h))

def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = word
    return lines + ([cur] if cur else [])

def spaced(d, xy, text, font, fill, sp=5, center_w=None):
    ws = [d.textlength(ch, font=font) for ch in text]; total = sum(ws) + sp * (len(text) - 1)
    x, y = xy
    if center_w is not None: x = x + (center_w - total) / 2
    for ch, w in zip(text, ws): d.text((x, y), ch, font=font, fill=fill); x += w + sp

def check_icon(d, x, y, s, fill=ROSE):
    d.ellipse((x, y, x + s, y + s), fill=fill)
    d.line([(x + s * .27, y + s * .52), (x + s * .44, y + s * .68), (x + s * .74, y + s * .34)], fill=WHITE, width=max(3, s // 12), joint="curve")

def logo(im, cx, y, width, light=False):
    lg = LOGO_LIGHT if light else LOGO
    lg = lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)
    im.paste(lg, (round(cx - width / 2), y), lg)

def product(handle):
    p = gql("""query($h:String!){productByHandle(handle:$h){title descriptionHtml
      h1:metafield(namespace:"custom",key:"highlight_1"){value} h2:metafield(namespace:"custom",key:"highlight_2"){value}
      h3:metafield(namespace:"custom",key:"highlight_3"){value}}}""", {"h": handle})["productByHandle"]
    clean = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    bullets = [clean(b) for b in re.findall(r"<li>(.*?)</li>", p["descriptionHtml"], re.S)]
    spec = clean((re.findall(r"<small>(.*?)</small>", p["descriptionHtml"], re.S) or [""])[0])
    lead = clean((re.findall(r"<p>(.*?)</p>", p["descriptionHtml"], re.S) or [""])[0])
    highs = [m["value"] for m in (p["h1"], p["h2"], p["h3"]) if m] or bullets[:3]
    return {"title": p["title"], "bullets": bullets[:4], "spec": spec, "lead": lead, "highs": highs[:3]}

def why_card(handle, info):
    im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
    # the full packshot as a framed 2:3 print on sand, so nothing is ever cropped
    d.rectangle((0, 0, W, 1420), fill=SAND)
    fw, fh = 880, 1320; pack = cover(fetch(GALLERIES[handle][0]), fw, fh, 0.5)
    sh = Image.new("RGBA", (fw + 80, fh + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((40, 50, fw + 40, fh + 50), fill=(0, 0, 0, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(18)); im.paste(sh, ((W - fw) // 2 - 40, 50 - 40), sh)
    im.paste(pack, ((W - fw) // 2, 50))
    y = 1480
    spaced(d, (120, y), "WHY YOU'LL LOVE IT", F("Jost-500.ttf", 36), ROSE, 7); y += 66
    ft = F("Cormorant-600.ttf", 92)
    tl = wrap(d, info["title"], ft, W - 240)[:2]
    for line in tl: d.text((120, y), line, font=ft, fill=CHAR); y += 98
    y += 30; fb = F("Jost-400.ttf", 50 if len(tl) == 1 else 46)
    for h in info["highs"]:
        lines = wrap(d, h, fb, W - 240 - 96)[:2]
        check_icon(d, 120, y + 6, 56)
        for k, line in enumerate(lines): d.text((120 + 96, y + k * 62), line, font=fb, fill=CHAR)
        y += 62 * len(lines) + 34
    logo(im, W / 2, H - 112, 420)
    return im

def details_card(handle, info):
    im = Image.new("RGB", (W, H), SAND); d = ImageDraw.Draw(im)
    life = GALLERIES[handle][1] if len(GALLERIES[handle]) > 1 else GALLERIES[handle][0]
    im.paste(cover(fetch(life), W, 1240, 0.35), (0, 0))
    y = 1320
    spaced(d, (120, y), "THE DETAILS", F("Jost-500.ttf", 34), ROSE, 6); y += 74
    if info["lead"]:
        fl = F("Cormorant-500.ttf", 72)
        for line in wrap(d, info["lead"], fl, W - 240)[:3]: d.text((120, y), line, font=fl, fill=CHAR); y += 82
        y += 30
    fb = F("Jost-400.ttf", 48)
    for b in info["bullets"]:
        lines = wrap(d, b, fb, W - 240 - 60)[:2]
        if y + 62 * len(lines) > H - 420: break
        d.rectangle((120, y + 30, 150, y + 34), fill=ROSE)
        for k, line in enumerate(lines): d.text((180, y + k * 62), line, font=fb, fill=CHAR)
        y += 62 * len(lines) + 28
    if info["spec"]:
        fs = F("Jost-400.ttf", 42); lines = wrap(d, info["spec"], fs, W - 340)[:3]
        bh = 90 + 50 * len(lines); top = max(y + 20, H - 200 - bh)
        d.rectangle((120, top, W - 120, top + bh), outline=CHAR, width=2)
        spaced(d, (160, top + 26), "SPECS", F("Jost-600.ttf", 28), ROSE, 5)
        for k, line in enumerate(lines): d.text((160, top + 72 + k * 50), line, font=fs, fill=CHAR)
    logo(im, W / 2, H - 112, 420)
    return im

def promise_card():
    im = Image.new("RGB", (W, H), CHAR); d = ImageDraw.Draw(im)
    logo(im, W / 2, 330, 1100, light=True)
    spaced(d, (0, 560), "THE COZYCOMPANION PROMISE", F("Jost-500.ttf", 40), ROSE, 8, center_w=W)
    rows = [("Free tracked shipping", "on orders over $150, with tracking all the way to your door"),
            ("30-day happiness guarantee", "not in love? return it unused within 30 days"),
            ("Secure checkout", "encrypted payment with PayPal and all major cards"),
            ("15% off your first order", "join the Cozy Circle and use code COZY15")]
    y = 820; ft, fs = F("Cormorant-600.ttf", 78), F("Jost-400.ttf", 40)
    for t, s in rows:
        check_icon(d, 170, y + 14, 70)
        d.text((290, y), t, font=ft, fill=CREAM)
        for k, line in enumerate(wrap(d, s, fs, W - 290 - 170)[:2]): d.text((290, y + 100 + k * 52), line, font=fs, fill=(205, 198, 190))
        y += 300
    d.line((170, H - 230, W - 170, H - 230), fill=(70, 66, 62), width=2)
    spaced(d, (0, H - 180), "CONSIDERED ESSENTIALS FOR DOGS & CATS", F("Jost-400.ttf", 32), (205, 198, 190), 6, center_w=W)
    return im

def upload(im, name, alt):
    path = os.path.join(OUT, name + ".jpg"); im.save(path, quality=90)
    r = subprocess.run([sys.executable, "-I", os.path.join(S, "staged_one.py"), path, name, alt], capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr)

if __name__ == "__main__":
    preview = "--preview" in sys.argv
    handles = [a for a in sys.argv[1:] if not a.startswith("--")] or list(GALLERIES)
    if not preview and "i_promise" not in reg:
        upload(promise_card(), "i_promise", "The CozyCompanion promise: free tracked shipping over $150, 30-day guarantee, secure checkout")
    if preview: promise_card().save(os.path.join(OUT, "i_promise.jpg"), quality=90)
    for h in handles:
        if h not in GALLERIES: print("skip (no gallery):", h); continue
        info = product(h)
        a, b = why_card(h, info), details_card(h, info)
        if preview:
            a.save(os.path.join(OUT, f"i_why_{h}.jpg"), quality=90); b.save(os.path.join(OUT, f"i_det_{h}.jpg"), quality=90)
        else:
            upload(a, f"i_why_{h}", f"{info['title']}: why you'll love it")
            upload(b, f"i_det_{h}", f"{info['title']}: the details")
        print("ok:", h)
