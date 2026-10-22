"""Eindkaart voor de Reverso Autumn-video: het woordmerk met daaronder REVERSO AUTUMN in kleine kapitalen (Cormorant Garamond
SemiBold, dezelfde crème als het woordmerk, letterafstand 0,27 em, tekstbreedte 86% van het woordmerk). montage.py zet het
bestand als 'logo' op breedte 0,40 van 1080 in het midden over de laatste 2 s.

  python3 -I endcard.py <logo.png> <cormorant.ttf> <uit.png>
Font: https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf (OFL)."""
import sys
from PIL import Image, ImageDraw, ImageFont

logo, font, out = sys.argv[1:4]
TXT, COL = "REVERSO AUTUMN", (224, 221, 222)
lg = Image.open(logo).convert("RGBA")
lg = lg.crop(lg.getbbox())
LW = lg.size[0]


def measure(size, track):
    f = ImageFont.truetype(font, size)
    f.set_variation_by_name("SemiBold")
    return f, sum(f.getlength(c) for c in TXT) + track * (len(TXT) - 1)


size = 96
while True:
    f, w = measure(size, round(size * 0.27))
    if w <= LW * 0.86:
        break
    size -= 2
track, gap = round(size * 0.27), 58
card = Image.new("RGBA", (LW, lg.size[1] + gap + size + 20), (0, 0, 0, 0))
card.alpha_composite(lg, (0, 0))
d, x, y = ImageDraw.Draw(card), (LW - w) / 2, lg.size[1] + gap
for c in TXT:
    d.text((x, y), c, font=f, fill=COL + (255,))
    x += f.getlength(c) + track
card = card.crop(card.getbbox())
card.save(out)
print(out, card.size, "font", size, "track", track)
