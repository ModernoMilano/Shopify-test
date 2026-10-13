"""python3 vframe.py <sid> <t> [x y w h]  -> qa/vid/<sid>_<t>s[_crop].jpg : een frame uit vid/<sid>.mp4 op tijd t (s), optioneel een uitsnede op 100% (fracties 0-1)."""
import sys, subprocess
from PIL import Image
sid, t = sys.argv[1], float(sys.argv[2])
out = f"qa/vid/{sid}_{t:.1f}s.jpg"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", f"vid/{sid}.mp4", "-frames:v", "1", "-q:v", "2", out], check=True)
if len(sys.argv) > 3:
    x, y, w, h = map(float, sys.argv[3:7]); im = Image.open(out); W, H = im.size
    c = im.crop((int(x*W), int(y*H), int((x+w)*W), int((y+h)*H)))
    if c.width > 1000: c = c.resize((1000, int(c.height*1000/c.width)), Image.LANCZOS)
    out = out.replace(".jpg", "_crop.jpg"); c.save(out, quality=85)
print(out, Image.open(out).size)
