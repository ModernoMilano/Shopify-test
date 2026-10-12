"""Overzicht van ALLE varianten per shot, met oordeel. python3 allsheet.py verdicts.json uit.jpg
verdicts.json: {"V01": {"title": "...", "vo": "...", "variants": [{"file": "img/V01a.png", "label": "V01a", "ok": true, "chosen": true, "note": "..."}, ...]}}"""
import json, sys
from PIL import Image, ImageDraw, ImageFont
data = json.load(open(sys.argv[1]))
TW, TH, PAD, CAP = 345, 613, 15, 150
W = 1080
def font(p, s, w=None):
    f = ImageFont.truetype(p, s)
    if w: f.set_variation_by_name(w)
    return f
SER = "/home/user/film/f/cormorant.ttf"; SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
fT, fH, fVO, fN, fS = font(SER, 64, "SemiBold"), font(SER, 40, "SemiBold"), font(SER, 30), font(SANS, 19), font(SANSB, 22)
def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
rows = []
for sid, s in data.items():
    n = len(s["variants"]); per = 3
    for i in range(0, n, per): rows.append((sid, s, s["variants"][i:i+per], i == 0))
H = 150 + sum((70 if first else 0) + TH + CAP + PAD for _, _, _, first in rows) + 40
img = Image.new("RGB", (W, H), (246, 242, 235)); d = ImageDraw.Draw(img)
PLAN_TITLE = json.load(open("plan.json"))["title"]
d.text((40, 36), PLAN_TITLE + " · alle startbeelden", font=fT, fill=(28, 24, 20))
d.text((42, 112), "groen = goedgekeurd door beide controleurs · rood = afgekeurd (reden eronder) · ster = gekozen voor de film", font=fN, fill=(110, 100, 90))
y = 150
for sid, s, vs, first in rows:
    if first:
        d.line((40, y, W - 40, y), fill=(214, 206, 194), width=2)
        head = s["title"]  # de titel bevat het shot-id al
        avail = W - 80 - d.textlength(s["vo"], font=fVO) - 30
        while d.textlength(head, font=fH) > avail and len(head) > 8: head = head[:-2].rstrip() + "…"
        d.text((40, y + 10), head, font=fH, fill=(28, 24, 20))
        d.text((W - 40 - d.textlength(s["vo"], font=fVO), y + 18), s["vo"], font=fVO, fill=(150, 112, 52))
        y += 70
    for k, v in enumerate(vs):
        x = 40 + k * (TW + PAD)
        im = Image.open(v["file"]).convert("RGB"); im.thumbnail((TW, TH), Image.LANCZOS); img.paste(im, (x, y))
        col = (40, 130, 70) if v["ok"] else (170, 40, 40)
        d.rectangle((x, y, x + im.width - 1, y + im.height - 1), outline=col, width=5)
        tag = ("★ " if v.get("chosen") else "") + v["label"] + (" · goed" if v["ok"] else " · afgekeurd")
        d.text((x, y + TH + 8), tag, font=fS, fill=col)
        yy = y + TH + 38
        for ln in wrap(d, v.get("note", ""), fN, TW)[:5]:
            d.text((x, yy), ln, font=fN, fill=(80, 72, 64)); yy += 23
    y += TH + CAP + PAD
img.save(sys.argv[2], quality=86, optimize=True); print(sys.argv[2], img.size)
