"""Tweede meting van de woordtijden: de bekende tekst wordt met een akoestisch model (wav2vec2, CTC) op de geisoleerde zang gelegd
(forced alignment). Gebruik: env -u PYTHONPATH python3 fa_N3.py  -> fa_words_N3.json (per woord t0, t1, score)."""
import json, re, wave, numpy as np, torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
LINES = [l.strip() for l in open('lyr_sung_N3.txt', encoding='utf-8') if l.strip()]
w = wave.open('N3_voc16.wav'); sr = w.getframerate(); assert sr == 16000, sr
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
if w.getnchannels() > 1: x = x.reshape(-1, w.getnchannels()).mean(axis=1)
proc = Wav2Vec2Processor.from_pretrained('facebook/wav2vec2-base-960h'); model = Wav2Vec2ForCTC.from_pretrained('facebook/wav2vec2-base-960h').eval()
vocab = proc.tokenizer.get_vocab(); blank = vocab['<pad>']; sep = vocab['|']
# emissies in stukken van 30 s met 2 s overlap (geheugen), daarna aan elkaar
hop = 320; CH = 30 * sr; OV = 2 * sr; ems = []; pos = 0
while pos < len(x):
    seg = x[max(0, pos - OV): pos + CH + OV]
    with torch.no_grad():
        lg = model(torch.tensor((seg - seg.mean()) / (seg.std() + 1e-7)).unsqueeze(0)).logits[0]
    lp = torch.log_softmax(lg, dim=-1).numpy()
    a = (pos - max(0, pos - OV)) // hop; b = a + min(CH, len(x) - pos) // hop
    ems.append(lp[a:b]); pos += CH
E = np.concatenate(ems); T = len(E); print('frames', T, 'sec/frame', len(x) / sr / T)
# tokens: woorden gescheiden door |, alleen letters en apostrof
def norm(wd): return re.sub(r"[^A-Z']", '', wd.upper().replace('’', "'"))
words = []
for n, line in enumerate(LINES):
    for k, wd in enumerate(re.findall(r"[A-Za-z0-9'’\-]+", line)):
        parts = [p for p in wd.split('-') if p]          # T-shirt -> T, SHIRT (later weer samen)
        words.append(dict(w=wd, line=n + 1, first=(k == 0), toks=[norm(p) for p in parts]))
seq = []; owner = []
for i, wd in enumerate(words):
    for p in wd['toks']:
        for ch in p: seq.append(vocab[ch]); owner.append(i)
        seq.append(sep); owner.append(-1)
seq = seq[:-1]; owner = owner[:-1]; S = len(seq)
# Viterbi over (frame, positie) met blanks
ext = [blank]; eo = [-1]
for t, o in zip(seq, owner): ext += [t, blank]; eo += [o, -1]
L = len(ext); NEG = -1e30
dp = np.full((T, L), NEG, np.float32); bp = np.zeros((T, L), np.int8)
dp[0, 0] = E[0, ext[0]]; dp[0, 1] = E[0, ext[1]]
ok2 = np.array([j >= 2 and ext[j] != blank and ext[j] != ext[j-2] for j in range(L)])
ext = np.array(ext)
for t in range(1, T):
    stay = dp[t-1]; s1 = np.concatenate(([NEG], dp[t-1, :-1])); s2 = np.concatenate(([NEG, NEG], dp[t-1, :-2]))
    s2 = np.where(ok2, s2, NEG)
    best = np.maximum(np.maximum(stay, s1), s2); bp[t] = np.where(best == stay, 0, np.where(best == s1, 1, 2))
    dp[t] = best + E[t, ext]
j = L - 1 if dp[T-1, L-1] >= dp[T-1, L-2] else L - 2; path = np.zeros(T, np.int32)
for t in range(T - 1, -1, -1):
    path[t] = j; j -= int(bp[t, j])
spf = len(x) / sr / T; span = {}
for t in range(T):
    o = eo[path[t]]
    if o >= 0:
        a = span.setdefault(o, [t, t, []]); a[1] = t; a[2].append(float(E[t, ext[path[t]]]))
out = []
for i, wd in enumerate(words):
    a = span.get(i)
    out.append(dict(w=wd['w'], line=wd['line'], first=wd['first'], t0=round(a[0] * spf, 2) if a else None, t1=round((a[1] + 1) * spf, 2) if a else None,
                    score=round(float(np.exp(np.mean(a[2]))), 2) if a else 0.0))
json.dump(out, open('fa_words_N3.json', 'w'), indent=0)
print('woorden', len(out), 'zonder plek', sum(1 for o in out if o['t0'] is None))
