"""Brand line on the gift-card feed images: soft bottom gradient + CozyCompanion wordmark + 'GIFT CARD' (Jost, spaced).
giftcard.py <key>  -> re-uploads as <key>_gc and points results.json at it."""
import json, os, sys, subprocess
D = os.path.dirname(os.path.abspath(__file__)); SOC = os.path.dirname(D); S = os.path.dirname(SOC)
sys.path.insert(0, SOC); sys.path.insert(0, S)
import social_post as sp
from PIL import Image, ImageDraw, ImageFont
res = json.load(open(os.path.join(D, "results.json"))); k = sys.argv[1]; r = res[k]
im = Image.open(r["preview"]).convert("RGBA"); W, H = im.size
g = Image.new("L", (1, H)); [g.putpixel((0, y), int(185 * max(0, (y - H * 0.62) / (H * 0.38)) ** 1.3)) for y in range(H)]
sh = Image.new("RGBA", (W, H), sp.CHAR + (0,)); sh.putalpha(g.resize((W, H))); im = Image.alpha_composite(im, sh)
logo = Image.open(os.path.join(S, "logo", "logo-light.png")).convert("RGBA"); logo = logo.crop(logo.getbbox())
logo = Image.merge("RGBA", (*[Image.new("L", logo.size, v) for v in sp.CREAM], logo.getchannel("A")))
lw = 420; logo = logo.resize((lw, round(lw * logo.height / logo.width)), Image.LANCZOS)
im.alpha_composite(logo, ((W - lw) // 2, H - 250))
d = ImageDraw.Draw(im); f = ImageFont.truetype(os.path.join(sp.FONT, "Jost-500.ttf"), 30); t = "GIFT CARD"; sp_ = 9
tw = sum(d.textlength(c, font=f) for c in t) + sp_ * (len(t) - 1); x = (W - tw) / 2; y = H - 250 + logo.height + 26
for c in t: d.text((x, y), c, font=f, fill=sp.ROSE + (255,)); x += d.textlength(c, font=f) + sp_
out = r["preview"].replace(".jpg", "_gc.jpg"); im.convert("RGB").save(out, "JPEG", quality=90)
name = k + "_gc"
subprocess.run([sys.executable, "-I", os.path.join(S, "staged_one.py"), out, name, f"CozyCompanion gift card {k}"], check=True, capture_output=True)
r["url"] = sp.reg()[name]["url"].split("?")[0]; r["preview"] = out
json.dump(res, open(os.path.join(D, "results.json"), "w"), indent=1); print(k, out, r["url"])
