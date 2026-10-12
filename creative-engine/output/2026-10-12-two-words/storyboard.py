"""Maakt een overzicht (storyboard) van de film als één lange JPEG, om op een telefoon door te scrollen (draait in de sandbox).

Gebruik: python3 storyboard.py <rows.json> <uit.jpg>
rows.json: [{"t": "0,0-4,0", "vo": "From the elegance of Milan.", "nl": "wat je ziet", "tag": "NIEUW", "img": "<pad of null>"}, ...]
Bestaande shots krijgen een echt frame; nieuwe shots zonder beeld krijgen een kaart met de beschrijving. Zodra de
startbeelden er zijn, komt hun pad in "img" en wordt het overzicht opnieuw gemaakt.
"""
import json, sys
from PIL import Image, ImageDraw, ImageFont

W, ROW, TW, TH = 1080, 330, 168, 299
BG, INK, MUTED, GOLD, CARD = (246, 242, 235), (28, 24, 20), (110, 100, 90), (150, 112, 52), (226, 219, 207)
SERIF = "/home/user/film/f/cormorant.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight:
        f.set_variation_by_name(weight)
    return f


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def thumb(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    s = max(TW / w, TH / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    x, y = (im.width - TW) // 2, (im.height - TH) // 2
    return im.crop((x, y, x + TW, y + TH))


def main(rows_path, out):
    rows = json.load(open(rows_path))
    head = 210
    img = Image.new("RGB", (W, head + ROW * len(rows) + 60), BG)
    d = ImageDraw.Draw(img)
    d.text((48, 52), "Two Words", font=font(SERIF, 72, "SemiBold"), fill=INK)
    d.text((50, 140), "Storyboard · ModernoMilano · alle beelden op volgorde, met de tekst die in beeld komt",
           font=font(SANS, 22), fill=MUTED)
    f_vo, f_nl, f_t, f_tag = font(SERIF, 42, "SemiBold"), font(SANS, 23), font(SANS, 22), font(SANS, 19)
    for i, r in enumerate(rows):
        y = head + i * ROW
        d.line((48, y, W - 48, y), fill=(214, 206, 194), width=2)
        x0, y0 = 48, y + 16
        if r.get("img"):
            img.paste(thumb(r["img"]), (x0, y0))
        else:
            d.rectangle((x0, y0, x0 + TW, y0 + TH), fill=CARD)
            d.text((x0 + 18, y0 + 18), "NIEUW", font=font(SANS, 22), fill=GOLD)
            d.text((x0 + 18, y0 + 50), "beeld volgt", font=font(SANS, 18), fill=MUTED)
            d.text((x0 + 18, y0 + 74), "na de credits", font=font(SANS, 18), fill=MUTED)
        tx = x0 + TW + 34
        tw = W - 48 - tx
        d.text((tx, y0 + 2), f"{r['t']} s", font=f_t, fill=MUTED)
        tag = r.get("tag", "")
        d.text((tx + 170, y0 + 4), tag, font=f_tag, fill=GOLD if tag.startswith("NIEUW") else MUTED)
        yy = y0 + 40
        for ln in wrap(d, r["vo"], f_vo, tw):
            d.text((tx, yy), ln, font=f_vo, fill=INK)
            yy += 48
        yy += 8
        for ln in wrap(d, r["nl"], f_nl, tw)[:6]:
            d.text((tx, yy), ln, font=f_nl, fill=MUTED)
            yy += 31
    img.save(out, quality=88, optimize=True)
    print(out, img.size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
