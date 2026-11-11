"""Controlestroken uit een video: python3 strips.py video.mp4 uitmap [stap=2.0] [per_strook=5] [breedte=300]
Of op gekozen tijden: python3 strips.py video.mp4 uitmap t 0.4 3.0 5.5 ...
Elke strook is een rij beelden met de tijd in de hoek."""
import os, subprocess, sys
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
if len(sys.argv) > 3 and sys.argv[3] == 't':
    times = [float(v) for v in sys.argv[4:]]; per = 5; W = 300
else:
    step = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0; per = int(sys.argv[4]) if len(sys.argv) > 4 else 5; W = int(sys.argv[5]) if len(sys.argv) > 5 else 300
    times = []; t = step / 2
    while t < dur - 0.05: times.append(round(t, 2)); t += step
H = W * 16 // 9
def frame(t):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (W, H), raw) if len(raw) == W * H * 3 else Image.new('RGB', (W, H), (90, 0, 0))
for s in range(0, len(times), per):
    g = times[s:s + per]; im = Image.new('RGB', (W * len(g) + 4 * (len(g) - 1), H), (0, 0, 0)); d = ImageDraw.Draw(im)
    for j, t in enumerate(g):
        im.paste(frame(t), (j * (W + 4), 0)); d.rectangle([j * (W + 4), 0, j * (W + 4) + 62, 16], fill=(0, 0, 0)); d.text((j * (W + 4) + 3, 2), f'{t:.2f}s', fill=(255, 255, 0))
    name = f'{out}/strip{s // per + 1:02d}_{g[0]:.1f}-{g[-1]:.1f}.jpg'; im.save(name, quality=80); print(name)
print('beelden', len(times), 'duur', round(dur, 2))
