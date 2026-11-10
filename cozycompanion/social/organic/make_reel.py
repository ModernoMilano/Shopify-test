"""Vertical interaction reels from still images (no generation credits).
render(segments, out_mp4, audio_src): Ken-Burns zoom/pan per image, 0.4 s crossfades, timed text blocks (fade in),
1080x1920 H.264 yuv420p 30 fps + AAC 48 kHz stereo, moov first (+faststart) so Instagram accepts it.
segment = {"img": path, "dur": s, "zoom": (z0, z1), "pan": ((x0, y0), (x1, y1)), "texts": [{"block": RGBA, "y": px,
           "t0": s, "t1": s|None}]}  (pan = focus fractions of the oversized image; t0/t1 relative to the segment)"""
import subprocess, os
from PIL import Image
from common import W, H, cover

FPS, XF = 30, 0.4
STILL = os.environ.get("CC_REEL_STILL") == "1"   # no Ken-Burns motion (owner: "rare inzoom effect ... helemaal eruit")

def _prep(seg):
    base = cover(Image.open(seg["img"]), int(W * 1.22), int(H * 1.22), seg.get("focus", (0.5, 0.5)))
    return base

def _frame(seg, base, t):
    d = seg["dur"]; k = min(1.0, max(0.0, t / d))
    k = k * k * (3 - 2 * k)  # ease in-out
    z0, z1 = seg.get("zoom", (1.0, 1.08)); z = z0 + (z1 - z0) * k
    (x0, y0), (x1, y1) = seg.get("pan", ((0.5, 0.5), (0.5, 0.5)))
    cx, cy = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    if STILL:  # owner 2026-11-10: no zoom/pan at all; hold the segment's widest framing
        z, (cx, cy) = (z1, (x1, y1)) if z1 < z0 else (z0, (x0, y0))
    # the base is 1.22x the frame; at z=1 we show base/1.12 (leaves room to pan), zooming in shrinks the window
    cw, ch = base.width / (z * 1.12), base.height / (z * 1.12)
    left = max(0, min(base.width - cw, cx * base.width - cw / 2))
    top = max(0, min(base.height - ch, cy * base.height - ch / 2))
    im = base.crop((int(left), int(top), int(left + cw), int(top + ch))).resize((W, H), Image.BILINEAR).convert("RGBA")
    for tx in seg.get("texts", []):
        t0 = tx.get("t0", 0.0); t1 = tx.get("t1")
        if t < t0 or (t1 is not None and t > t1): continue
        a = min(1.0, (t - t0) / 0.25) if t0 > 0 else 1.0
        if t1 is not None: a = min(a, max(0.0, (t1 - t) / 0.2))
        b = tx["block"]
        if a < 1.0:
            b = b.copy(); b.putalpha(b.split()[3].point(lambda v: int(v * a)))
        x = tx.get("x", (W - b.width) // 2)
        im.alpha_composite(b, (int(x), int(tx["y"])))
    return im.convert("RGB")

def render(segments, out_mp4, audio_src):
    total = sum(s["dur"] for s in segments) - XF * (len(segments) - 1)
    bases = [_prep(s) for s in segments]
    aud = out_mp4 + ".wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", audio_src, "-t", f"{total:.2f}", "-vn",
                    "-af", f"volume=4.0,afade=t=in:d=0.6,afade=t=out:st={max(0, total - 0.9):.2f}:d=0.9", "-ar", "48000", "-ac", "2", aud], check=True)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", aud, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
                          "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-shortest", out_mp4],
                         stdin=subprocess.PIPE)
    starts, acc = [], 0.0
    for s in segments:
        starts.append(acc); acc += s["dur"] - XF
    n = int(round(total * FPS))
    for f in range(n):
        t = f / FPS
        i = max(j for j in range(len(segments)) if starts[j] <= t + 1e-9)
        fr = _frame(segments[i], bases[i], t - starts[i])
        # crossfade into the next segment during its first XF seconds
        if i > 0 and t - starts[i] < XF:
            prev = _frame(segments[i - 1], bases[i - 1], t - starts[i - 1])
            fr = Image.blend(prev, fr, (t - starts[i]) / XF)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait(); os.remove(aud)
    if p.returncode: raise SystemExit(f"ffmpeg failed for {out_mp4}")
    return out_mp4
