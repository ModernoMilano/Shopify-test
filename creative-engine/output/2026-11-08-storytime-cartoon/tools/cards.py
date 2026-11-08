"""Verdeel de woorden van elke zin over de gemeten duur (evenredig met woordlengte) en groepeer ze in kaarten van 1-2 woorden,
zoals het voorbeeld (gemiddeld ~0,6 s per kaart). Geeft per zin een lijst (t0, t1, TEXT) relatief aan de start van de zin."""
import re
def cards(sentence, dur, max_words=2):
    words = re.findall(r"[A-Za-z'’]+[.,:!?\"”]*", sentence)
    weights = [len(re.sub(r'\W', '', w)) + 1.2 for w in words]
    total = sum(weights); t = 0.0; out = []; i = 0
    while i < len(words):
        k = 1 if len(words[i]) >= 7 else max_words
        grp = words[i:i + k]; wsum = sum(weights[i:i + k]); d = dur * wsum / total
        txt = ' '.join(grp).upper().strip('"“”')
        txt = re.sub(r'[“”"]', '', txt)
        out.append((round(t, 2), round(t + d, 2), txt)); t += d; i += k
    return out
