"""Swap TikTok videos for the no-zoom renders (owner 2026-11-10: "rare inzoom effect ... helemaal eruit").
Render first with CC_REEL_STILL=1 python3 build_tiktok.py --only <keys>; this makes the silent copy (as mute_tiktok.py),
uploads it as tt_<date>_<slot>_still and points social/tiktok_plan.json "url" at it (old zoom url kept as "url_zoom").
Usage: python3 social/organic/still_tiktok.py 2026-11-11_5,2026-11-12_2,..."""
import os, sys, json, subprocess, re
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, S); sys.path.insert(0, HERE)
from upload_week import up_video
MEDIA = os.path.join(S, "social", "organic", "out", "tt"); OUT = os.path.join(MEDIA, "still"); os.makedirs(OUT, exist_ok=True)
P = os.path.join(S, "social", "tiktok_plan.json"); plan = json.load(open(P))
keys = sys.argv[1].split(",")
for e in plan:
    k = f"{e['date']}_{e['slot']}"
    if e["type"] != "video" or k not in keys: continue
    src = os.path.join(MEDIA, f"tt_{k}.mp4"); dst = os.path.join(OUT, f"tt_{k}_still.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", dst], check=True)
    vd = subprocess.run(["ffmpeg", "-i", dst, "-map", "0:a", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    mx = re.search(r"max_volume: (-?[\d.]+|-inf) dB", vd).group(1); assert mx == "-inf" or float(mx) <= -91, (k, mx)
    up = up_video(dst, f"tt_{k}_still", f"CozyCompanion TikTok {k} (no zoom, no audio)")
    if "url_zoom" not in e: e["url_zoom"] = e["url"]
    e["url"] = "https://cozycompanion.us/cdn/shop/files/" + up.split("/files/")[-1]
    json.dump(plan, open(P, "w"), indent=1, ensure_ascii=False)
    print(k, e["url"], flush=True)
