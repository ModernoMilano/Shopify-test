# Herstelt samengeperste woordtijden uit de whisper-uitlijning (woorden < 0,08 s) door een run van korte woorden,
# samen met een te lange buur (> 0,45 s, die de tijd had opgeslokt), opnieuw te verdelen naar woordlengte.
# Gebruik: python3 retime_words.py timeline_words.json timeline_words_v2.json
import json, sys
W = json.load(open(sys.argv[1])); n = len(W); i = 0; changed = []
while i < n:
    if W[i]['t1'] - W[i]['t0'] < 0.08:
        j = i
        while j + 1 < n and W[j+1]['t1'] - W[j+1]['t0'] < 0.08: j += 1
        a, b = i, j
        if a > 0 and W[a-1]['t1'] - W[a-1]['t0'] > 0.45: a -= 1
        if b + 1 < n and W[b+1]['t1'] - W[b+1]['t0'] > 0.4: b += 1
        if a == i and b == j: a = max(0, i - 1); b = min(n - 1, j + 1)
        t0 = W[a]['t0']; t1 = W[b]['t1']
        ws = [max(2, len([c for c in w['w'] if c.isalpha()])) for w in W[a:b+1]]; tot = sum(ws); t = t0
        for k, w in zip(range(a, b + 1), ws):
            d = (t1 - t0) * w / tot; W[k]['t0'] = round(t, 3); W[k]['t1'] = round(t + d, 3); t += d
        changed.append((a, b, [W[k]['w'] for k in range(a, b + 1)], round(t0, 2), round(t1, 2)))
        i = b + 1
    else: i += 1
json.dump(W, open(sys.argv[2], 'w'), ensure_ascii=False)
for c in changed: print(c)
