"""python3 rough.py <uit.mp4> -> ruwe montage van de hele film op 540x960 uit plan.json: nieuwe shots uit vid/<sid>.mp4 (vanaf clip_in),
bestaande clips uit ~/film/sm/<clip>.mp4 (vanaf clip_in); per rij de duur uit het plan; de tekst van de rij als label onderin."""
import sys, json, subprocess, os
CLIPS = {"RAIN": "rain", "PIANO": "piano2", "TBA": "tbA", "TBB": "tbB", "LA": "lagoA", "LC": "lagoC", "LB": "lagoB",
         "SC": "seraC", "SD": "seraD", "SA": "seraA", "SB": "seraB"}
plan = json.load(open("plan.json")); out = sys.argv[1]; parts = []
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def esc(s): return s.replace("\\", "\\\\").replace("'", "’").replace(":", "\\:").replace("%", "\\%")
for n, t in enumerate(plan["timeline"]):
    key = (t.get("existing_clip") or "").strip().upper(); dur = float(t["t_end"]) - float(t["t_start"]); cin = float(t.get("clip_in") or 0)
    if key in CLIPS: src = os.path.expanduser(f"~/film/sm/{CLIPS[key]}.mp4"); tag = key
    else:
        sid = t["shot"].replace("NEW ", "").split()[0]; src = f"vid/{sid}.mp4"; tag = sid
    vo = t["vo"].split(" (")[0].strip()
    label = f"{t['t_start']:.1f}s  {tag}   {vo}" if vo else f"{t['t_start']:.1f}s  {tag}"
    p = f"vid/_r_{n:02d}.mp4"
    vf = ("scale=540:960:force_original_aspect_ratio=increase,crop=540:960,"
          f"drawtext=fontfile={FONT}:text='{esc(label)}':fontsize=20:fontcolor=white:box=1:boxcolor=black@0.45:boxborderw=8:x=14:y=h-56")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{cin:.2f}", "-i", src, "-t", f"{dur:.3f}", "-vf", vf, "-r", "24", "-an",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-video_track_timescale", "24000", p], check=True)
    parts.append(p)
open("vid/_r_list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "vid/_r_list.txt", "-c", "copy", out], check=True)
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
print(out, os.path.getsize(out) // 1000, "kB", d, "s")
