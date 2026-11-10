"""Frames uit de eindmontage voor de controle: elke 4 s een frame, 4 per strook. Gebruik: python3 frames_v3.py video2_v3.mp4 qa3"""
import sys, subprocess, os
from PIL import Image
vid, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',vid],capture_output=True,text=True).stdout)
ts = [t for t in [1.0 + 4.0*i for i in range(200)] if t < dur - 0.5]
frames = []
for t in ts:
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',f'{t:.2f}','-i',vid,'-frames:v','1','-vf','scale=270:-1',f'/tmp/q.jpg'],check=True)
    frames.append((t, Image.open('/tmp/q.jpg').convert('RGB')))
n = 0
for i in range(0, len(frames), 4):
    grp = frames[i:i+4]; w = sum(f.size[0] for _, f in grp); h = grp[0][1].size[1]
    im = Image.new('RGB', (w, h)); x = 0
    for _, f in grp: im.paste(f, (x, 0)); x += f.size[0]
    n += 1; im.save(f'{out}/strip{n:02d}_{grp[0][0]:.0f}s-{grp[-1][0]:.0f}s.jpg', quality=78)
print('frames', len(frames), 'strips', n, 'dur', round(dur,1))
