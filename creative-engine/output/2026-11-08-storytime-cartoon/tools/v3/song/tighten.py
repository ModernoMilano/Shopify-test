"""Haal lange instrumentale gaten tussen gezongen regels weg, op de maat. Gebruik:
python3 tighten.py <in.wav> <words.json> <out.wav> <bpm> [max_gap=1.6] [keep=1.0]
Een gat (einde laatste woord -> begin volgende woord) langer dan max_gap wordt ingekort tot ~keep seconden,
waarbij een geheel aantal tellen wordt weggeknipt (zodat de beat doorloopt), met een korte crossfade.
Schrijft ook <out>.cuts.json met de weggehaalde stukken (in de tijd van het origineel) voor de woordtijdlijn."""
import sys, json, numpy as np, soundfile as sf
inp, wordsf, out, bpm = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
max_gap = float(sys.argv[5]) if len(sys.argv) > 5 else 1.6
keep = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
y, sr = sf.read(inp, always_2d=True); beat = 60.0 / bpm
W = json.load(open(wordsf)); cuts = []
for a, b in zip(W, W[1:]):
    gap = b['t0'] - a['t1']
    if gap > max_gap:
        n_beats = int((gap - keep) // beat)
        if n_beats >= 1:
            cut_len = n_beats * beat; start = a['t1'] + keep * 0.5
            cuts.append((start, start + cut_len))
pieces = []; pos = 0.0; xf = int(0.03 * sr)
for s, e in cuts:
    seg = y[int(pos * sr):int(s * sr)]
    pieces.append(seg); pos = e
pieces.append(y[int(pos * sr):])
outy = pieces[0]
for seg in pieces[1:]:
    a = outy[-xf:] * np.linspace(1, 0, xf)[:, None]; b = seg[:xf] * np.linspace(0, 1, xf)[:, None]
    outy = np.concatenate([outy[:-xf], a + b, seg[xf:]])
sf.write(out, outy, sr)
json.dump([{"start": round(s, 3), "end": round(e, 3)} for s, e in cuts], open(out + '.cuts.json', 'w'))
print('cuts', [(round(s, 2), round(e - s, 2)) for s, e in cuts], 'new length', round(len(outy) / sr, 2))
