"""Contactblad van de gekozen nieuwe beelden: 3 kolommen, 540x960 per beeld, met shot-id en de tekst erbij. python3 contact.py chosen.json uit.jpg"""
import json, sys
from PIL import Image, ImageDraw, ImageFont
chosen = json.load(open(sys.argv[1]))  # {"V01": {"file": "img/V01a.png", "title": "...", "vo": "..."}}
plan = json.load(open("plan.json"))
F = ImageFont.truetype("/home/user/film/f/cormorant.ttf", 34); F.set_variation_by_name("SemiBold")
S = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
ids = list(chosen.keys()); cols, cw, ch, pad, cap = 3, 540, 960, 24, 110
rows = (len(ids) + cols - 1) // cols
W = cols * cw + (cols + 1) * pad; H = rows * (ch + cap + pad) + pad + 120
img = Image.new("RGB", (W, H), (246, 242, 235)); d = ImageDraw.Draw(img)
T = ImageFont.truetype("/home/user/film/f/cormorant.ttf", 64); T.set_variation_by_name("SemiBold")
d.text((pad, 30), plan["title"] + f" · de {len(ids)} nieuwe beelden", font=T, fill=(28, 24, 20))
for n, k in enumerate(ids):
    r, c = divmod(n, cols); x = pad + c * (cw + pad); y = 120 + pad + r * (ch + cap + pad)
    im = Image.open(chosen[k]["file"]).convert("RGB"); im.thumbnail((cw, ch), Image.LANCZOS); img.paste(im, (x, y))
    txt = chosen[k]["title"]  # de titel bevat het shot-id al
    f = F
    for size in (34, 30, 27, 24, 22):
        f = ImageFont.truetype("/home/user/film/f/cormorant.ttf", size); f.set_variation_by_name("SemiBold")
        if d.textlength(txt, font=f) <= cw - 6: break
    while d.textlength(txt, font=f) > cw - 6 and len(txt) > 8: txt = txt[:-2].rstrip() + "…"
    d.text((x, y + ch + 10), txt, font=f, fill=(28, 24, 20))
    d.text((x, y + ch + 56), chosen[k]["vo"][:60], font=S, fill=(110, 100, 90))
img.save(sys.argv[2], quality=86, optimize=True); print(sys.argv[2], img.size)
