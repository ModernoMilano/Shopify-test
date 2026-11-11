"""Dichte controlestrook: python3 -I dense.py clip.mp4 uit.jpg t0 t1 n [breedte=270] [per_rij=8] [crop=x,y,w,h als fractie]"""
import subprocess, sys
from PIL import Image, ImageDraw
src, out, t0, t1, n = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
W = int(sys.argv[6]) if len(sys.argv) > 6 else 270; per = int(sys.argv[7]) if len(sys.argv) > 7 else 8
crop = [float(v) for v in sys.argv[8].split(',')] if len(sys.argv) > 8 else None
info = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip().split(',')
sw, sh = int(info[0]), int(info[1])
if crop: cx, cy, cw, ch = int(crop[0]*sw), int(crop[1]*sh), int(crop[2]*sw), int(crop[3]*sh)
else: cx, cy, cw, ch = 0, 0, sw, sh
H = int(W * ch / cw) // 2 * 2
def frame(t):
    vf = f'crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}'
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (W, H), raw) if len(raw) == W * H * 3 else Image.new('RGB', (W, H), (90, 0, 0))
ts = [round(t0 + (t1 - t0) * i / max(1, n - 1), 3) for i in range(n)]
rows = (n + per - 1) // per
im = Image.new('RGB', (per * (W + 3), rows * (H + 3)), (0, 0, 0)); d = ImageDraw.Draw(im)
for i, t in enumerate(ts):
    x, y = (i % per) * (W + 3), (i // per) * (H + 3)
    im.paste(frame(t), (x, y)); d.rectangle([x, y, x + 50, y + 13], fill=(0, 0, 0)); d.text((x + 2, y + 1), f'{t:.2f}', fill=(255, 255, 0))
im.save(out, quality=82); print(out, im.size)
