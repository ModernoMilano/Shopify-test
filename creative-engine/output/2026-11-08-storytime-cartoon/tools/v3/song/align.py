"""Lijn de echte lyrics uit op de whisper-woordtijden (difflib), zodat de ondertitels de juiste woorden tonen op de gezongen
tijden. Gebruik: python3 align.py <part> <lyrics.txt> -> schrijft words_<part>.json [{w,t0,t1}] in de tijd van het DEEL."""
import json, re, sys, difflib
part, lyr = sys.argv[1], sys.argv[2]
tr = json.load(open('transcripts.json'))[part]['words']
def norm(w): return re.sub(r"[^a-z0-9']", '', w.lower())
truth = [w for w in re.findall(r"[A-Za-z0-9'’]+[.,:!?]*", open(lyr).read()) if not w.startswith('[')]
truth = [w for w in truth if norm(w)]
hw = [norm(w['w']) for w in tr]; tw = [norm(w) for w in truth]
sm = difflib.SequenceMatcher(a=tw, b=hw, autojunk=False)
times = [None] * len(truth)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1): times[i1 + k] = (tr[j1 + k]['t0'], tr[j1 + k]['t1'])
    elif tag == 'replace' and (i2 - i1) == (j2 - j1):
        for k in range(i2 - i1): times[i1 + k] = (tr[j1 + k]['t0'], tr[j1 + k]['t1'])
    elif tag == 'replace':
        # spread the heard span over the true words
        a, b = tr[j1]['t0'], tr[j2 - 1]['t1']; n = i2 - i1
        for k in range(n): times[i1 + k] = (a + (b - a) * k / n, a + (b - a) * (k + 1) / n)
# interpolate the rest (deleted words) between neighbours
for i, t in enumerate(times):
    if t is None:
        l = next((times[j] for j in range(i - 1, -1, -1) if times[j]), None)
        r = next((times[j] for j in range(i + 1, len(times)) if times[j]), None)
        if l and r:
            gap_words = 1 + sum(1 for j in range(i + 1, len(times)) if times[j] is None and j < len(times) and all(times[m] is None for m in range(i, j + 1)))
            times[i] = (l[1], min(r[0], l[1] + 0.35))
        elif l: times[i] = (l[1], l[1] + 0.3)
        elif r: times[i] = (max(0, r[0] - 0.3), r[0])
words = [{"w": w, "t0": round(t[0], 2), "t1": round(t[1], 2)} for w, t in zip(truth, times)]
matched = sum(1 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag == 'equal' for _ in range(i2 - i1))
print(part, 'true words', len(truth), 'heard', len(hw), 'exact matches', matched)
json.dump(words, open(f'words_{part}.json', 'w'), indent=0)
