"""Meet elke VO-opname in een map (Claude kan niet luisteren): lengte na de keten, toonhoogte (Praat), bereik in halve
tonen, het einde van de zin ten opzichte van de mediaan (< 1 is dalend), piek, en een transcriptie (faster-whisper).
Gebruik: python3 voqa.py <map met L1.mp3, L2.mp3, ...>"""
import sys, glob, os, subprocess, numpy as np, parselmouth
from faster_whisper import WhisperModel

m = WhisperModel("small", device="cpu", compute_type="int8")
d = sys.argv[1]
for f in sorted(glob.glob(d + "/L*.mp3"), key=lambda x: int(os.path.basename(x)[1:].split('.')[0].rstrip('ab'))):
    w = f[:-4] + "_p.wav"
    subprocess.run(["bash", os.path.join(os.path.dirname(os.path.abspath(__file__)), "vochain.sh"), f, w], check=True)
    snd = parselmouth.Sound(w).convert_to_mono()
    dur = snd.get_total_duration()
    p = snd.to_pitch_ac(time_step=0.01, pitch_floor=50, pitch_ceiling=300)
    f0 = p.selected_array["frequency"]
    t = p.xs()
    v = f0 > 0
    f0v, tv = f0[v], t[v]
    last = f0v[tv > tv.max() - 0.35]
    mid = np.median(f0v)
    peak = 20 * np.log10(np.abs(snd.values[0]).max() + 1e-9)
    segs, _ = m.transcribe(w, beam_size=5, language="en")
    text = " ".join(s.text.strip() for s in segs)
    rng = 12 * np.log2(np.percentile(f0v, 90) / np.percentile(f0v, 10))
    print(f"{os.path.basename(f):8s} dur {dur:4.2f}s f0 {mid:5.0f}Hz range {rng:4.1f}st end {np.median(last) / mid:4.2f}x "
          f"peak {peak:5.1f}dB | {text}", flush=True)
