"""Controle: geen ondertitelkaart mag het laatste woord van een regel met het eerste van de volgende regel combineren."""
import json, re, sys
W = json.load(open(sys.argv[1])); cards = [l.rstrip('\n') for l in open(sys.argv[2])][1:]
strip = lambda s: re.sub(r"[.,:!?;]", "", s).upper()
pairs = [(W[i-1]['w'], W[i]['w']) for i in range(1, len(W)) if W[i].get('line_start')]
bad = 0
for a, b in pairs:
    pat = strip(a) + ' ' + strip(b)
    for c in cards:
        if pat in strip(c[18:]) and 'MODERNO' not in pat: print('  kruist:', c); bad += 1
# elke kaart moet minstens 0.2 s staan en kaarten mogen niet overlappen
prev = None
for c in cards:
    t0, t1 = float(c[:6]), float(c[7:13])
    if t1 - t0 < 0.2: print('  flits:', c); bad += 1
    if prev is not None and t0 < prev - 1e-6: print('  overlapt:', c); bad += 1
    prev = t1
print('regelstarts', sum(1 for w in W if w.get('line_start')), 'kaarten', len(cards), 'fouten', bad)
