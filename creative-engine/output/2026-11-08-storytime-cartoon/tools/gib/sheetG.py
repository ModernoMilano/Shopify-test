"""Contactblad van keyframes: python3 sheetG.py uit.jpg N01 N02 ... (elk 300 px breed)"""
import sys
from PIL import Image, ImageDraw
out, names = sys.argv[1], sys.argv[2:]
W = 300; ims = []
for n in names:
    im = Image.open(f'kfG/{n}.png').convert('RGB'); w, h = im.size
    im = im.resize((W, int(h * W / w))); ImageDraw.Draw(im).text((6, 6), n, fill=(255, 255, 0)); ims.append(im)
s = Image.new('RGB', (W * len(ims) + 4 * (len(ims) - 1), ims[0].size[1]), (0, 0, 0))
for i, im in enumerate(ims): s.paste(im, (i * (W + 4), 0))
s.save(out, quality=70, optimize=True); print(out, s.size)
