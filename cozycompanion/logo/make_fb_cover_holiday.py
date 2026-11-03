"""Holiday (December) Facebook page cover, 1640x624; usage: make_fb_cover_holiday.py q4_W6. Based on make_fb_cover.py:
1640x624 (2x of Facebook's 820x312). Copy sits in the centre so it survives the mobile
crop (sides cut) and stays clear of the profile picture (bottom-left). Background: a Nano Banana interior photo
(files.json name passed as argv[1]) with the products at the far left and right."""
import os, sys, io, json, ssl, urllib.request
S = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(S))
from lib import DOMAIN
from PIL import Image, ImageDraw, ImageFont
W, H = 1640, 624
F = os.path.join(S, "..", "ads", "fonts")
reg = json.load(open(os.path.join(S, "..", "files.json")))
u = f"https://{DOMAIN}/cdn/shop/files/" + reg[sys.argv[1]]["url"].split("/files/")[-1].split("?")[0]
im = Image.open(io.BytesIO(urllib.request.urlopen(u, context=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")).read())).convert("RGB")
s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
x, y = (im.width - W) // 2, (im.height - H) // 2; im = im.crop((x, y, x + W, y + H)).convert("RGBA")
# soft cream glow behind the copy: a blurred ellipse over the full canvas, so it has no visible edges
from PIL import ImageFilter
glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).ellipse((W // 2 - 500, 110, W // 2 + 500, 410), fill=215)
glow = glow.filter(ImageFilter.GaussianBlur(90))
halo = Image.new("RGBA", (W, H), (245, 241, 237, 0)); halo.putalpha(glow); im.alpha_composite(halo)
d = ImageDraw.Draw(im)
def spaced(text, font, y, fill, sp):
    tw = sum(d.textlength(c, font=font) for c in text) + sp * (len(text) - 1); x = (W - tw) / 2
    for c in text: d.text((x, y), c, font=font, fill=fill); x += d.textlength(c, font=font) + sp
logo = Image.open(os.path.join(S, "logo-dark.png")).convert("RGBA"); logo = logo.crop(logo.getbbox())
lw = 300; logo = logo.resize((lw, round(lw * logo.height / logo.width)), Image.LANCZOS)
im.alpha_composite(logo, ((W - lw) // 2, 150))
spaced("THE COZY SEASON", ImageFont.truetype(os.path.join(F, "Jost-500.ttf"), 17), 218, (183, 110, 121, 255), 4)
f = ImageFont.truetype(os.path.join(F, "Cormorant-600.ttf"), 54); t = "Gifts for every pet, and their people."
d.text(((W - d.textlength(t, font=f)) / 2, 252), t, font=f, fill=(26, 26, 26, 255))
spaced("COZYCOMPANION.US", ImageFont.truetype(os.path.join(F, "Jost-400.ttf"), 18), 352, (26, 26, 26, 200), 5)
im.convert("RGB").save(os.path.join(S, "facebook-cover-holiday-1640x624.png"))
print("ok")
