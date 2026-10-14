"""Knipt een doorlopende VO-opname van het hele script 'You Will Look Twice' in de 24 zinnen (draait in de sandbox).

Gebruik: python3 split_read_v3.py <opname.mp3> <uit-map>
Zoals split_read.py (11 okt), maar de woorden van whisper worden met difflib aan het script gekoppeld, zodat een
verkeerd gehoord woord of een gesplitst woord de knippunten niet verschuift.
"""
import difflib, os, re, subprocess, sys, wave
import numpy as np
from faster_whisper import WhisperModel

SR = 48000
LINES = ["You will look twice.", "Nothing on him says a word.", "And still, you look.", "He never asked you to.",
         "So where does that come from.", "From the elegance of Milan... to the precision of the atelier.",
         "A line in chalk.", "Straight at the shoulder.", "Cut once.", "Room to breathe.", "Thread... until it holds.",
         "Pressed flat... until the seam forgets it was two.", "Worn, until it forgets it was new.",
         "One piece. ... Two sides.", "The same man.", "Two words.", "Not an address.", "Moderno is the man.",
         "Milano is the measure.", "Worn together.", "The name comes last.", "Inside. ... Against the neck.",
         "You wear it. ... Nobody reads it.", "Moderno Milano."]


def read(path):
    with wave.open(path) as f:
        return np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").reshape(-1, f.getnchannels()).astype(np.float64) / 32768


def write(path, x):
    with wave.open(path, "wb") as f:
        f.setnchannels(x.shape[1]); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def main(src, out):
    os.makedirs(out, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    full = f"{out}/full_p.wav"
    subprocess.run(["bash", f"{here}/vochain.sh", src, full], check=True)
    x = read(full)
    h = int(0.005 * SR)
    m = np.abs(x).max(1)
    k = len(m) // h
    e = 20 * np.log10(np.sqrt((m[:k * h].reshape(k, h) ** 2).mean(1)) + 1e-9)
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(full, beam_size=5, language="en", word_timestamps=True)
    words = [w for s in segs for w in s.words]
    print("gehoord:", " ".join(w.word.strip() for w in words))
    hidx = [i for i, w in enumerate(words) if norm(w.word)]
    heard = [norm(words[i].word) for i in hidx]
    script = [(n, norm(t)) for n, l in enumerate(LINES) for t in l.split() if norm(t)]
    sm = difflib.SequenceMatcher(None, [s[1] for s in script], heard, autojunk=False)
    link = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for d in range(i2 - i1):
                link[i1 + d] = hidx[j1 + d]
    print(f"script {len(script)} woorden, whisper {len(heard)}, gekoppeld {len(link)}")
    first, last = {}, {}
    for si, (n, _) in enumerate(script):
        if si in link:
            first.setdefault(n, link[si]); last[n] = link[si]
    for n in range(len(LINES)):   # een zin zonder gekoppeld woord krijgt de woorden tussen zijn buren
        if n not in first and n + 1 in first:
            last[n] = first[n + 1] - 1; first[n] = last.get(n - 1, -1) + 1
        if n not in first and n - 1 in last:
            first[n] = last[n - 1] + 1; last[n] = first.get(n + 1, len(words)) - 1
    missing = [n + 1 for n in range(len(LINES)) if n not in first or last[n] < first[n]]
    if missing:
        print("FOUT: geen woorden voor zin", missing); sys.exit(1)
    cuts = [0]
    for n in range(len(LINES) - 1):
        a = words[last[n]].start + 0.15
        b = max(words[first[n + 1]].start, a + 0.05)
        b = min(b + 0.15, len(e) * h / SR)
        fa, fb = int(a * SR / h), int(b * SR / h)
        j = fa + int(np.argmin(e[fa:fb]))
        cuts.append(j * h)
    cuts.append(len(x))
    f = int(0.01 * SR)
    for n in range(len(LINES)):
        y = x[cuts[n]:cuts[n + 1]]
        ym = np.abs(y).max(1)
        on = np.flatnonzero(ym > 10 ** (-50 / 20))
        y = y[max(0, on[0] - int(0.02 * SR)):on[-1] + int(0.08 * SR)].copy()
        y[:f] *= (np.sin(np.linspace(0, np.pi / 2, f)) ** 2)[:, None]
        y[-f:] *= (np.cos(np.linspace(0, np.pi / 2, f)) ** 2)[:, None]
        write(f"{out}/L{n + 1}_p.wav", y)
        segs2, _ = model.transcribe(f"{out}/L{n + 1}_p.wav", beam_size=5, language="en")
        heard2 = " ".join(s.text.strip() for s in segs2)
        print(f"L{n + 1:<2} {len(y) / SR:5.2f} s | {heard2}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
