"""Per regel: hoeveel woorden van de ware tekst zijn letterlijk gehoord (difflib tegen whisper). Gebruik: python3 linecheck.py <part> <lyrics.txt>"""
import json, re, sys, difflib
part, lyr = sys.argv[1], sys.argv[2]
tr = json.load(open('transcripts.json'))[part]['words']
def norm(w): return re.sub(r"[^a-z0-9']", '', w.lower())
lines = [l for l in open(lyr).read().splitlines() if l.strip()]
truth = []; owner = []
for i, l in enumerate(lines):
    for t in re.findall(r"[A-Za-z0-9'’]+[.,:!?]*", l):
        if norm(t): truth.append(norm(t)); owner.append(i)
hw = [norm(w['w']) for w in tr]
sm = difflib.SequenceMatcher(a=truth, b=hw, autojunk=False)
hit = [False] * len(truth)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i1, i2): hit[k] = True
for i, l in enumerate(lines):
    idx = [k for k, o in enumerate(owner) if o == i]
    pct = sum(hit[k] for k in idx) / max(1, len(idx))
    flag = '  ' if pct >= 0.75 else ('!!' if pct < 0.5 else ' !')
    print(f"{flag} {pct:4.0%}  {l}")
