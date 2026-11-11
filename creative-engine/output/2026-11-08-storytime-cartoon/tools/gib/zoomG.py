"""Gezichtsuitsnede uit een clip op gekozen tijden: python3 zoomG.py N02 x0 y0 x1 y1 t1 t2 ... -> clipsG/N02_zoom.jpg"""
import sys, subprocess
from PIL import Image
k = sys.argv[1]; box = [float(v) for v in sys.argv[2:6]]; ts = [float(v) for v in sys.argv[6:]]
ims = []
for t in ts:
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t:.3f}', '-i', f'clipsG/{k}.mp4', '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
    import io
    im = Image.open(io.BytesIO(raw)).convert('RGB'); w, h = im.size
    c = im.crop((int(box[0]*w), int(box[1]*h), int(box[2]*w), int(box[3]*h))); c.thumbnail((360, 360)); ims.append(c)
s = Image.new('RGB', (sum(i.size[0] for i in ims) + 4*(len(ims)-1), max(i.size[1] for i in ims)), (0, 0, 0)); x = 0
for i in ims: s.paste(i, (x, 0)); x += i.size[0] + 4
s.save(f'clipsG/{k}_zoom.jpg', quality=78); print(k, s.size)
