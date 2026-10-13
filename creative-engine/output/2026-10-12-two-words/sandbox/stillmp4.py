"""python3 stillmp4.py <sid> <img.png> [seconds=4] [push=0.03] [w=540] -> vid/<sid>.mp4 : levende still met een langzame push-in (24 fps)."""
import sys, subprocess
sid, img = sys.argv[1], sys.argv[2]
sec = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
push = float(sys.argv[4]) if len(sys.argv) > 4 else 0.03
w = int(sys.argv[5]) if len(sys.argv) > 5 else 540
h = w * 16 // 9
n = int(round(sec * 24))
vf = (f"scale={w*2}:{h*2}:force_original_aspect_ratio=increase,crop={w*2}:{h*2},"
      f"zoompan=z='1+{push}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={w}x{h}:fps=24,format=yuv420p")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", img, "-vf", vf, "-frames:v", str(n), "-r", "24",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", f"vid/{sid}.mp4"], check=True)
print(f"vid/{sid}.mp4", n, "frames")
