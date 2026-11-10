"""Maak per clip een strook van 3 frames (begin, midden, eind) om te controleren. Gebruik: python3 strip.py clips2/K01.mp4 [...]"""
import sys, subprocess, os
from PIL import Image
for path in sys.argv[1:]:
    dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',path],capture_output=True,text=True).stdout or 0)
    frames = []
    for t in (0.05, dur/2, max(0.0, dur-0.15)):
        out = '/tmp/f.jpg'
        subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',f'{t:.2f}','-i',path,'-frames:v','1','-vf','scale=300:-1',out],check=True)
        frames.append(Image.open(out).convert('RGB'))
    w = sum(f.size[0] for f in frames); h = max(f.size[1] for f in frames)
    strip = Image.new('RGB',(w,h),(0,0,0)); x=0
    for f in frames: strip.paste(f,(x,0)); x+=f.size[0]
    o = os.path.splitext(path)[0] + '_strip.jpg'; strip.save(o, quality=78); print(o, round(dur,2), os.path.getsize(o))
