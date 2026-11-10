"""Silent copies of the TikTok videos (owner 2026-11-10 via the Metricool session: "zorg dat de videos zonder geluiden worden gepost").
Video stream copied unchanged, audio replaced by a silent 48 kHz stereo AAC track (TikTok wants an audio stream).
Uploaded as tt_<date>_<slot>_mute; social/tiktok_plan.json "url" -> silent version, old one kept as "url_with_audio"."""
import os, sys, json, subprocess, re
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, S); sys.path.insert(0, HERE)
from upload_week import up_video
MEDIA = os.path.join(S, "social", "organic", "out", "tt"); OUT = os.path.join(MEDIA, "mute"); os.makedirs(OUT, exist_ok=True)
P = os.path.join(S, "social", "tiktok_plan.json"); plan = json.load(open(P))
def probe(f, what):
    return json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", what, "-of", "json", f], capture_output=True, text=True, check=True).stdout)
done = []
for e in plan:
    if e["type"] != "video": continue
    base = f"tt_{e['date']}_{e['slot']}"; src = os.path.join(MEDIA, base + ".mp4"); dst = os.path.join(OUT, base + "_mute.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", dst], check=True)
    a, b = probe(src, "format=duration:stream=codec_type,width,height,r_frame_rate,nb_frames"), probe(dst, "format=duration:stream=codec_type,width,height,r_frame_rate,nb_frames,sample_rate")
    va = [s for s in a["streams"] if s["codec_type"] == "video"][0]; vb = [s for s in b["streams"] if s["codec_type"] == "video"][0]
    ab = [s for s in b["streams"] if s["codec_type"] == "audio"]
    assert (va["width"], va["height"], va["r_frame_rate"], va["nb_frames"]) == (vb["width"], vb["height"], vb["r_frame_rate"], vb["nb_frames"]), base
    assert abs(float(a["format"]["duration"]) - float(b["format"]["duration"])) < 0.1 and ab and ab[0]["sample_rate"] == "48000", base
    vd = subprocess.run(["ffmpeg", "-i", dst, "-map", "0:a", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    mx = re.search(r"max_volume: (-?[\d.]+|-inf) dB", vd).group(1)
    assert mx == "-inf" or float(mx) <= -91, (base, mx)
    if "url_with_audio" not in e: e["url_with_audio"] = e["url"]
    up = up_video(dst, base + "_mute", f"CozyCompanion TikTok {e['date']} slot {e['slot']} (no audio)")
    e["url"] = "https://cozycompanion.us/cdn/shop/files/" + up.split("/files/")[-1]
    json.dump(plan, open(P, "w"), indent=1, ensure_ascii=False)
    done.append((f"{e['date']}_{e['slot']}", e["url"], mx, round(float(b["format"]["duration"]), 2)))
    print(done[-1], flush=True)
print("muted:", len(done))
