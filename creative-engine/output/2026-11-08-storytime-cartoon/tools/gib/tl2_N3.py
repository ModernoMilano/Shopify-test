"""Woordtijdlijn versie 2 voor take N3. Drie metingen op de geisoleerde zang:
1. spraakherkenning met woordtijden (timeline_words_N3_asr.json, uit tl_N3.py): geeft de woorden, maar zet het eerste woord
   na een stilte tot 0,6 s te vroeg en de laatste "Moderno Milano" 0,6 s te laat;
2. de bekende tekst met een akoestisch model op de zang gelegd (fa_words_N3.json, uit fa_N3.py): starttijd per woord;
3. de luidheid van het zangspoor: waar na een stilte de stem weer begint en waar hij ophoudt.
Regel: start = meting 2 min 0,04 s; volgt het woord op een stilte, dan het begin van de stem uit meting 3.
Einde = start van het volgende woord, of het einde van de stem als er een stilte volgt.
Schrijft timeline_words_N3.json en timeline_lines_N3.json en drukt de verschillen met versie 1 af."""
import json, os, wave, numpy as np
R = os.path.expanduser('~/tb/rnb')
A = json.load(open('timeline_words_N3_asr.json')); F = json.load(open(f'{R}/fa_words_N3.json')); assert len(A) == len(F)
w = wave.open(f'{R}/N3_vocals.wav'); sr = w.getframerate(); ch = w.getnchannels()
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768; x = x.reshape(-1, ch).mean(axis=1)
hop = int(sr * 0.01); n = len(x) // hop
db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(axis=1)) + 1e-7)
loud = db > -35.0
# stiltes van minstens 0,25 s: (begin, einde); einde = eerste hoorbare moment dat minstens 60 ms aanhoudt
sil = []; i = 0
while i < n:
    if not loud[i]:
        j = i
        while j < n and not (loud[j] and loud[j:j + 6].all()): j += 1
        if (j - i) * 0.01 >= 0.25: sil.append((round(i * 0.01, 2), round(j * 0.01, 2)))
        i = j
    else: i += 1
W = []
for a, f in zip(A, F):
    d = dict(w=a['w'], t0=round(f['t0'] - 0.04, 2), asr=a['t0'], fa=f['t0'], sc=f['score'])
    if a.get('line_start'): d['line_start'] = True
    W.append(d)
W[0]['t0'] = max(0.0, W[0]['t0'])
# eerste woord na een stilte: begin van de stem (als dat hooguit 0,35 s voor de akoestische meting ligt)
snapped = []
for (s0, s1) in sil:
    cand = [k for k, d in enumerate(W) if s1 - 0.10 <= d['fa'] <= s1 + 0.35]
    if cand and (cand[0] == 0 or W[cand[0] - 1]['fa'] < s1 - 0.10):
        k = cand[0]; snapped.append((W[k]['w'], W[k]['t0'], s1)); W[k]['t0'] = s1
for a, b in zip(W, W[1:]):
    if b['t0'] < a['t0'] + 0.06: b['t0'] = round(a['t0'] + 0.06, 2)
for k, d in enumerate(W):
    nxt = W[k + 1]['t0'] if k + 1 < len(W) else None
    gap = [s for s in sil if s[0] > d['t0'] and (nxt is None or s[0] < nxt)]
    d['t1'] = round(max(d['t0'] + 0.12, gap[0][0]) if gap else (nxt if nxt is not None else d['t0'] + 0.5), 2)
    if nxt is not None: d['t1'] = min(d['t1'], nxt) if not gap else min(d['t1'], nxt)
assert all(b['t0'] >= a['t0'] for a, b in zip(W, W[1:])) and all(d['t1'] > d['t0'] for d in W)
assert sum(1 for d in W if d.get('line_start')) == 30 and len(W) == 182
out = [{k: v for k, v in d.items() if k in ('w', 't0', 't1', 'line_start')} for d in W]
json.dump(out, open('timeline_words_N3.json', 'w'), indent=0)
L = []; cur = None
LINES = [l['text'] for l in json.load(open('timeline_lines_N3_asr.json'))]
for d in out:
    if d.get('line_start'): cur = dict(n=len(L) + 1, t0=d['t0'], t1=d['t1'], text=LINES[len(L)]); L.append(cur)
    cur['t1'] = d['t1']
json.dump(L, open('timeline_lines_N3.json', 'w'), indent=1)
print('stiltes in de zang (s):', sil)
print('eerste woord na stilte gelegd op het begin van de stem:', snapped)
OLD = json.load(open('timeline_lines_N3_asr.json'))
print('regel  v1-start  v2-start  verschil   einde')
for o, l in zip(OLD, L): print(f"  {l['n']:2d}  {o['t0']:7.2f}  {l['t0']:7.2f}  {l['t0'] - o['t0']:+.2f}  {l['t1']:7.2f}  {l['text']}")
dd = np.array([b['t0'] - a['t0'] for a, b in zip(A, out)]); print('woorden: |verschil| > 0,15 s:', int((abs(dd) > 0.15).sum()), 'van', len(dd), ' grootste', round(float(abs(dd).max()), 2))
