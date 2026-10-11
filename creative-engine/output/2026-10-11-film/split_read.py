"""Knipt één doorlopende VO-opname van het hele script in de 11 zinnen (draait in de sandbox).

Gebruik: python3 split_read.py <opname.mp3> <uit-map>
Schrijft <uit-map>/L1_p.wav ... L11_p.wav: elke zin door de VO-keten (vochain.sh), geknipt op het stilste punt tussen het
laatste woord van de ene zin en het eerste woord van de volgende (whisper-woordtijden plus een rms-spoor van 5 ms), met
stilte ervoor en erna eraf. Zo kost een tweede stem één opname in plaats van elf (de laatste 2,62 credits, 11 okt).
"""
import os, subprocess, sys, wave
import numpy as np
from faster_whisper import WhisperModel

SR = 48000
LINES = ["My father never owned an umbrella.", "He had one rule about clothes.", "Let the day do the dressing.",
         "I was eight.", "I thought he meant the rain.", "Some afternoons want the other side of me.",
         "For years, I was dressed for the evening by breakfast.", "Turns out, his rule was permission.",
         "To stop being early for my own life.", "On time.", "Moderno Milano."]


def read(path):
    with wave.open(path) as f:
        return np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").reshape(-1, f.getnchannels()).astype(np.float64) / 32768


def write(path, x):
    with wave.open(path, "wb") as f:
        f.setnchannels(x.shape[1])
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


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
    counts = [len(l.split()) for l in LINES]
    if len(words) != sum(counts):
        print("LET OP: whisper hoort", len(words), "woorden, het script heeft er", sum(counts))
        print(" ".join(w.word for w in words))
    cuts, i = [0], 0
    for c in counts[:-1]:
        i += c
        a = words[i - 1].start + 0.15        # na het begin van het laatste woord van deze zin
        b = max(words[i].start, a + 0.05)    # tot het begin (volgens whisper) van de volgende zin
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
        heard = " ".join(s.text.strip() for s in segs2)
        print(f"L{n + 1:<2} {len(y) / SR:5.2f} s | {heard}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
