"""Clips ophalen en controlestroken maken over het deel dat de montage gebruikt.
python3 getclips.py <werkmap> N03=<url> N04=<url> ...   (of alleen sleutels om de stroken opnieuw te maken)
Schrijft <werkmap>/clipsG/Nxx.mp4 (de vorige versie gaat naar clipsG/old/) en <werkmap>/qaclips/Nxx_a.jpg en Nxx_b.jpg:
tien beelden, gelijk verdeeld over het gebruikte deel van de clip, met de tijd in de hoek."""
import os, re, shutil, subprocess, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gib_shots.py'), encoding='utf-8').read()
m = re.search(r"CUTS = \[(.*?)\]\n", src, flags=re.S)
USED = {k: float(b) - float(a) for k, a, b in re.findall(r"\('(\w+)',\s*([\d.]+),\s*([\d.]+)\)", m.group(1))}
work = sys.argv[1]; os.makedirs(f'{work}/clipsG/old', exist_ok=True); os.makedirs(f'{work}/qaclips', exist_ok=True)
W = 300; H = W * 16 // 9
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout or 0)
def frame(p, t):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t:.3f}', '-i', p, '-frames:v', '1', '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (W, H), raw) if len(raw) == W * H * 3 else Image.new('RGB', (W, H), (90, 0, 0))
for a in sys.argv[2:]:
    k, _, url = a.partition('='); p = f'{work}/clipsG/{k}.mp4'
    if url:
        if os.path.exists(p):
            n = 1
            while os.path.exists(f'{work}/clipsG/old/{k}_v{n}.mp4'): n += 1
            shutil.move(p, f'{work}/clipsG/old/{k}_v{n}.mp4')
        subprocess.run(['curl', '-sS', '-o', p, url], check=True)
    d = dur(p); used = min(USED.get(k, d), d - 0.04); ts = [round(used * i / 9, 2) for i in range(10)]
    for part, g in (('a', ts[:5]), ('b', ts[5:])):
        im = Image.new('RGB', (W * 5 + 16, H), (0, 0, 0)); dr = ImageDraw.Draw(im)
        for j, t in enumerate(g):
            im.paste(frame(p, t), (j * (W + 4), 0)); dr.rectangle([j * (W + 4), 0, j * (W + 4) + 62, 16], fill=(0, 0, 0)); dr.text((j * (W + 4) + 3, 2), f'{t:.2f}s', fill=(255, 255, 0))
        im.save(f'{work}/qaclips/{k}_{part}.jpg', quality=80)
    print(k, 'clip', round(d, 2), 's, gebruikt', round(USED.get(k, d), 2), 's')
