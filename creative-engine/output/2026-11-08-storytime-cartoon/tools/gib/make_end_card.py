"""Eindkaart voor 9:16 (1080x1920), midden in beeld zodat de knoppen en de tekstbalk van Reels en TikTok er niet overheen vallen:
een donkere band met MODERNO MILANO en modernomilano.com. python3 make_end_card.py fonts/Montserrat-VF.ttf end_card_mid.png"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
font_path, out = sys.argv[1], sys.argv[2]
W, H = 1080, 1920
Y0, Y1, Y2, Y3, AMAX = 930, 1040, 1300, 1420, 175      # band: infaden 930-1040, vol 1040-1300, uitfaden 1300-1420
a = np.zeros((H, W), np.float32)
for y in range(H):
    if Y0 <= y < Y1: v = (y - Y0) / (Y1 - Y0)
    elif Y1 <= y < Y2: v = 1.0
    elif Y2 <= y < Y3: v = 1.0 - (y - Y2) / (Y3 - Y2)
    else: v = 0.0
    a[y, :] = AMAX * (v * v * (3 - 2 * v))               # zachte overgang
im = Image.fromarray(np.dstack([np.zeros((H, W, 3), np.uint8), a.astype(np.uint8)]), 'RGBA')
d = ImageDraw.Draw(im)
big = ImageFont.truetype(font_path, 84); big.set_variation_by_name('Black')
small = ImageFont.truetype(font_path, 40); small.set_variation_by_name('Medium')
t1, t2 = 'MODERNO MILANO', 'modernomilano.com'
x1 = (W - d.textlength(t1, font=big)) / 2; x2 = (W - d.textlength(t2, font=small)) / 2
d.text((x1, 1100), t1, font=big, fill=(255, 255, 255, 255))
d.text((x2, 1212), t2, font=small, fill=(235, 235, 235, 255))
im.save(out); print(out, 'merknaam breed', round(d.textlength(t1, font=big)), 'px; band', Y0, '-', Y3)
