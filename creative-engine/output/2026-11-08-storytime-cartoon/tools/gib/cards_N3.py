"""Ondertitelkaarten met de hand ingedeeld: captions_N3.txt geeft per regel de stukjes (gescheiden door /), de tijden komen uit
de woordtijdlijn. Zo staan dezelfde refreinregels elke keer hetzelfde in beeld en breekt een kaart nooit midden in een zinsdeel.
python3 cards_N3.py timeline_words_N3.json captions_N3.txt cards_N3.json [fonts/Montserrat-VF.ttf]
Regels: een kaart blijft staan tot de volgende kaart van dezelfde regel begint; de laatste kaart van een regel tot hooguit 0,3 s
na het einde van de zang en nooit over het begin van de volgende regel. Controle: elk woord precies een keer en in volgorde,
geen kaart korter dan 0,33 s in beeld, geen kaart breder dan het beeld."""
import json, re, sys
words = json.load(open(sys.argv[1])); lines = [l.strip() for l in open(sys.argv[2], encoding='utf-8') if l.strip()]
font_path = sys.argv[4] if len(sys.argv) > 4 else None
def toks(s): return re.findall(r"[A-Za-z0-9'’\-]+[.,:!?;]*", s)
def norm(s): return re.sub(r"[^a-z0-9]", '', s.lower())
cards = []; i = 0; errs = []
for n, line in enumerate(lines, 1):
    chunks = [c.strip() for c in line.split('/')]; lc = []
    for c in chunks:
        tk = toks(c); seg = words[i:i + len(tk)]
        if [norm(t) for t in tk] != [norm(w['w']) for w in seg]: errs.append(f'regel {n}: "{c}" past niet op de tijdlijn ({[w["w"] for w in seg]})')
        if seg and not (seg[0].get('line_start') == (c is chunks[0]) or (not seg[0].get('line_start') and c is not chunks[0])): errs.append(f'regel {n}: regelstart klopt niet bij "{c}"')
        big = norm(c) == 'modernomilano'
        lc.append(dict(t0=seg[0]['t0'], t1=seg[-1]['t1'], text=c.upper().replace('’', "'"), big=big, line=n)); i += len(tk)
    cards += lc
if i != len(words): errs.append(f'woorden over: {len(words) - i}')
for k, c in enumerate(cards):
    nxt = cards[k + 1] if k + 1 < len(cards) else None
    if nxt is None: c['end'] = c['t1']
    elif nxt['line'] == c['line']: c['end'] = nxt['t0']
    else: c['end'] = min(nxt['t0'], c['t1'] + 0.3)
    c['vis'] = round(c['end'] - c['t0'], 2)
    if c['vis'] < 0.33: errs.append(f"regel {c['line']}: \"{c['text']}\" staat maar {c['vis']} s")
if font_path:
    from PIL import ImageFont
    f = ImageFont.truetype(font_path, int(0.03 * 1920 / 0.72)); f.set_variation_by_name('Black')
    b = ImageFont.truetype(font_path, int(0.052 * 1920 / 0.72)); b.set_variation_by_name('Black')
    for c in cards:
        wpx = (b if c['big'] else f).getlength(c['text']); c['px'] = round(wpx)
        if wpx > 0.9 * 1080 and not c['big']: errs.append(f"regel {c['line']}: \"{c['text']}\" is {round(wpx)} px breed en breekt in twee regels")
json.dump([[round(c['t0'], 2), round(c['end'], 2), c['text'], c['big']] for c in cards], open(sys.argv[3], 'w'), indent=0)
for c in cards: print('%6.2f-%6.2f %s%-20s %.2f s%s' % (c['t0'], c['end'], 'BIG ' if c['big'] else '    ', c['text'], c['vis'], ('  %d px' % c['px']) if 'px' in c else ''))
print('kaarten', len(cards), 'regels', len(lines), 'fouten', len(errs))
for e in errs: print('  !!', e)
