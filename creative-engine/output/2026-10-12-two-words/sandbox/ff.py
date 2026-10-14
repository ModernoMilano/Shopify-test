"""python3 ff.py <film.mp4> <t> [x y w h] -> qa/film/f_<t>s[_crop].jpg : een frame uit de film op tijd t (s), optioneel een uitsnede op 100% (fracties 0-1)."""
import os, subprocess, sys
from PIL import Image
film, t = sys.argv[1], float(sys.argv[2])
os.makedirs("qa/film", exist_ok=True)
out = f"qa/film/f_{t:.2f}s.jpg"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", film, "-frames:v", "1", "-q:v", "2", out], check=True)
if len(sys.argv) > 3:
    x, y, w, h = map(float, sys.argv[3:7]); im = Image.open(out); W, H = im.size
    c = im.crop((int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)))
    if c.width > 1000: c = c.resize((1000, int(c.height * 1000 / c.width)), Image.LANCZOS)
    out = out.replace(".jpg", "_crop.jpg"); c.save(out, quality=85)
else:
    im = Image.open(out)
    if im.width > 720: im.resize((720, int(im.height * 720 / im.width)), Image.LANCZOS).save(out, quality=85)
print(out, Image.open(out).size)
