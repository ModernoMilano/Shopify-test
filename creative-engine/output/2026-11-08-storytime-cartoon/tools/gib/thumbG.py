"""Maak controlebeelden (540 px breed, JPEG) van keyframes. Gebruik: python3 thumbG.py N01 N02 ..."""
import sys
from PIL import Image
for n in sys.argv[1:]:
    im = Image.open(f'kfG/{n}.png').convert('RGB'); w, h = im.size
    im.resize((540, int(h * 540 / w))).save(f'kfG/{n}_t.jpg', quality=72, optimize=True)
    print(n, w, h)
