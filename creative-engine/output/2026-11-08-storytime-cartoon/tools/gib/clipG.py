"""Clips ophalen en controlestroken maken.
python3 clipG.py N01=<bestandsdeel.mp4> ...   -> clipsG/N01.mp4 + clipsG/N01_strip.jpg (5 beelden: begin, 25%, midden, 75%, eind)"""
import sys, os, shutil, subprocess
from PIL import Image
B = 'https://d8j0ntlcm91z4.cloudfront.net/user_3EYCP9eOPYPhvDZtzEySAqbjgsC/'
os.makedirs('clipsG/old', exist_ok=True)
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout or 0)
def strip(k):
    p = f'clipsG/{k}.mp4'; d = dur(p); ims = []
    for f in (0.0, 0.25, 0.5, 0.75, 0.97):
        t = max(0.0, d * f - (0.02 if f > 0.9 else 0))
        raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t:.3f}', '-i', p, '-frames:v', '1', '-vf', 'scale=216:384', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        if len(raw) == 216 * 384 * 3: ims.append(Image.frombytes('RGB', (216, 384), raw))
    s = Image.new('RGB', (216 * len(ims) + 4 * (len(ims) - 1), 384), (0, 0, 0))
    for i, im in enumerate(ims): s.paste(im, (i * 220, 0))
    s.save(f'clipsG/{k}_strip.jpg', quality=72, optimize=True); return d, len(ims)
for a in sys.argv[1:]:
    if '=' in a:
        k, part = a.split('=', 1); dst = f'clipsG/{k}.mp4'
        if os.path.exists(dst):
            n = 1
            while os.path.exists(f'clipsG/old/{k}_v{n}.mp4'): n += 1
            shutil.move(dst, f'clipsG/old/{k}_v{n}.mp4')
        subprocess.run(['curl', '-sS', '-o', dst, B + part], check=True)
    else: k = a
    d, n = strip(k); print(k, round(d, 2), 's', n, 'beelden', os.path.getsize(f'clipsG/{k}.mp4') // 1024, 'kB')
