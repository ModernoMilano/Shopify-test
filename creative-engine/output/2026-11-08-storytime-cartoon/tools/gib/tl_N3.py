"""Woordtijdlijn voor take N3: de gezongen woorden (ASR op de geisoleerde zang, words_voc_N3.json) gekoppeld aan de tekstregels.
Afwijkingen van het tekstblad die in de take zelf zitten:
- regel 7 ("I zipped it up to my chin"): in de take klinkt alleen "(to) my chin" (15,4-16,0 s); de ondertitel volgt wat er klinkt.
- de ASR hoort na het slot "Thank you very much" in stilte (zangspoor is daar -55 dB): weggelaten.
Schrijft timeline_words_N3_asr.json (w, t0, t1, line_start) en timeline_lines_N3_asr.json: de eerste meting.
De tijdlijn die de video gebruikt komt uit tl2_N3.py (na fa_N3.py), die de starttijden bijstelt met een tweede en derde meting."""
import json, re, os, difflib
R = os.path.expanduser('~/tb/rnb')
A = json.load(open(f'{R}/words_voc_N3.json'))
A = [dict(w=x['w'].strip(), t0=x['t0'], t1=x['t1']) for x in A]
# 1) hallucinatie aan het eind weg
while A and A[-1]['t0'] > 84.0: A.pop()
# 2) samengevoegde woorden
out = []
i = 0
while i < len(A):
    a = A[i]; nxt = A[i+1] if i + 1 < len(A) else None
    lw = re.sub(r'[^a-z\-]', '', a['w'].lower())
    if nxt is not None:
        ln = re.sub(r'[^a-z\-]', '', nxt['w'].lower())
        if lw == 'candle' and ln == 'light': out.append(dict(w='candlelight', t0=a['t0'], t1=nxt['t1'])); i += 2; continue
        if lw == 't' and ln == '-shirt': out.append(dict(w='T-shirt', t0=a['t0'], t1=nxt['t1'])); i += 2; continue
    out.append(a); i += 1
A = out
# 3) "to" voor "my chin" (de mix-ASR hoort het op 15,36 s)
for k, a in enumerate(A):
    if a['w'].lower() == 'my' and abs(a['t0'] - 15.44) < 0.05 and A[k+1]['w'].lower().startswith('chin'):
        A[k-1]['t1'] = 15.38; A.insert(k, dict(w='To', t0=15.38, t1=15.50)); A[k+1]['t0'] = 15.50; break
else: raise SystemExit('my chin niet gevonden')
LINES = """I'm not giving it back
It's soft, it's you, that's that
Sleeves too long, collar high
Hold out your hand, nice try
One cold night, my navy knit was gone
Round your shoulders once, you kept it on
To my chin
So warm, all sleeves and a grin
Wore it making tea
Wore it watching TV
My grey hoodies? Nobody stole those
You stole my knit: first praise for my clothes
One empty hanger, box at the door
My flatmate's eyebrow rises: one more?
I bought another, date two, candlelight
Your hand on my sleeve, it's gone tonight
I'm not giving it back
That's two, are you keeping track?
Sleeves too long, collar high
Hold out your hand, nice try
You wave from the tram in knit number two
I laugh on the platform, turning blue
Two knits down, in a T-shirt, you win, I'm fine
At your door you turn the collar, read the line
It says Moderno Milano
But I say mine
I'm not giving it back
Sleeves too long, collar high
Hold out your hand, nice try
Moderno Milano""".split('\n')
def toks(s): return re.findall(r"[A-Za-z0-9'’\-]+[.,:!?;]*", s)
def norm(s): return re.sub(r"[^a-z0-9]", '', s.lower())
W = []; L = []; i = 0; odd = []
for n, line in enumerate(LINES, 1):
    tk = toks(line); seg = A[i:i+len(tk)]
    if len(seg) != len(tk): raise SystemExit(f'regel {n} past niet: {line} ({len(seg)} vs {len(tk)})')
    for k, (t, a) in enumerate(zip(tk, seg)):
        d = dict(w=t, t0=round(a['t0'], 2), t1=round(a['t1'], 2))
        if k == 0: d['line_start'] = True
        W.append(d)
        r = difflib.SequenceMatcher(None, norm(t), norm(a['w'])).ratio()
        if r < 0.6: odd.append((n, t, a['w'], a['t0']))
    L.append(dict(n=n, t0=round(seg[0]['t0'], 2), t1=round(seg[-1]['t1'], 2), text=line)); i += len(tk)
assert i == len(A), (i, len(A))
for a, b in zip(W, W[1:]):
    if b['t0'] < a['t1']: b['t0'] = a['t1']
    if b['t1'] < b['t0'] + 0.12: b['t1'] = round(b['t0'] + 0.12, 2)
assert all(b['t0'] >= a['t0'] for a, b in zip(W, W[1:])), 'niet oplopend'
assert sum(1 for w in W if w.get('line_start')) == len(LINES) == 30
json.dump(W, open('timeline_words_N3_asr.json', 'w'), indent=0); json.dump(L, open('timeline_lines_N3_asr.json', 'w'), indent=1)
print('woorden', len(W), 'regels', len(L), 'regelstarts', sum(1 for w in W if w.get('line_start')))
for l in L: print(f"{l['t0']:6.2f}-{l['t1']:6.2f}  {l['text']}")
print('tekstwoord wijkt af van wat de ASR hoorde (alleen ter controle):')
for o in odd: print('  regel', o[0], repr(o[1]), '<- ASR', repr(o[2]), 'op', o[3])
