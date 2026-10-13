"""python3 strip.py <sid> -> qa/vid/<sid>_strip.jpg : zes frames (0, 0.8, 1.6, 2.4, 3.2, laatste) naast elkaar, elk 300 px breed."""
import sys, subprocess, json
from PIL import Image, ImageDraw
sid = sys.argv[1]; src = f"vid/{sid}.mp4"
dur = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", src], capture_output=True, text=True).stdout)["format"]["duration"])
ts = [0.0, 0.8, 1.6, 2.4, 3.2, max(0.0, dur - 0.05)]
frames = []
for i, t in enumerate(ts):
    f = f"qa/vid/_{sid}_{i}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", "-q:v", "2", f], check=True)
    im = Image.open(f); im = im.resize((300, int(im.height * 300 / im.width)), Image.LANCZOS); frames.append((t, im))
h = max(im.height for _, im in frames)
sheet = Image.new("RGB", (len(frames) * 306, h + 26), (30, 30, 30)); d = ImageDraw.Draw(sheet)
for i, (t, im) in enumerate(frames):
    sheet.paste(im, (i * 306, 26)); d.text((i * 306 + 4, 6), f"{sid} {t:.1f}s", fill=(230, 220, 200))
out = f"qa/vid/{sid}_strip.jpg"; sheet.save(out, quality=80); print(out, sheet.size, f"duur {dur:.2f}s")
