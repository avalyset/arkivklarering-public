#!/usr/bin/env python3
"""Lager røyktestfila lyd/rokytest.wav: 20 s syntetisk musikk + 20 s norsk tale (16 kHz, mono).

Musikken er en egenprodusert arpeggio med overtoner og slag (ingen opphavsrett til andre).
Talen er macOS-stemmen Nora (nb_NO) som leser en kort nynorsk tekst. Stemmen er bokmålsstemme,
så uttalen av nynorske former er ufullkommen; fila tester rørledningen, ikke talegjenkjenningen.
"""
import pathlib
import subprocess
import sys
import tempfile
import wave

import numpy as np

SR = 16000
TEKST_PERSONVERN = ("Ho heitte Kari Nordmann og vart fødd i 1972 i Volda. Ho var sjuk og gjekk i Arbeiderpartiet. "
                    "Ring nummeret 68 05 45 67.")
TEKST = ("Ho gjekk heim frå skulen og kjøpte brød i butikken. "
         "Me høyrer på radio kvar dag, og ingen av oss hugsar kva dei sa i går. "
         "Gardane ligg langt frå vegen.")


def musikk(sek=20.0):
    t = np.arange(int(SR * sek)) / SR
    akkorder = [(220.00, 261.63, 329.63), (174.61, 220.00, 261.63),
                (196.00, 246.94, 293.66), (164.81, 207.65, 246.94)]
    sig = np.zeros_like(t)
    steg = 0.25
    for i in range(int(sek / steg)):
        a, b = i * steg, (i + 1) * steg
        idx = (t >= a) & (t < b)
        akk = akkorder[(i // 8) % len(akkorder)]
        f = akk[i % 3] * (2 if i % 4 == 3 else 1)
        lokal = t[idx] - a
        env = np.exp(-lokal * 7)
        tone = sum(np.sin(2 * np.pi * f * k * lokal) / k for k in (1, 2, 3, 4))
        sig[idx] += 0.25 * env * tone
        # basstone på første slag i hver takt
        if i % 4 == 0:
            sig[idx] += 0.3 * np.exp(-lokal * 3) * np.sin(2 * np.pi * (akk[0] / 2) * lokal)
        # hi-hat-aktig støy på annenhvert slag
        if i % 2 == 1:
            rng = np.random.default_rng(i)
            sig[idx] += 0.05 * np.exp(-lokal * 40) * rng.standard_normal(idx.sum())
    return (0.8 * sig / np.max(np.abs(sig))).astype(np.float32)


def tale(sek=20.0, tekst=None):
    with tempfile.TemporaryDirectory() as d:
        aiff = pathlib.Path(d) / "tale.aiff"
        wav = pathlib.Path(d) / "tale.wav"
        subprocess.run(["say", "-v", "Nora", "-o", str(aiff), tekst or TEKST], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(aiff), "-ar", str(SR), "-ac", "1", str(wav)], check=True)
        with wave.open(str(wav)) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    n = int(SR * sek)
    if len(x) > n:
        sys.exit(f"Talen er {len(x)/SR:.1f} s, lengre enn {sek} s. Kort ned TEKST.")
    return np.concatenate([x, np.zeros(n - len(x), dtype=np.float32)])


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()  # avbryter hvis cacher og tmp ikke ligger under ARKIVKLARERING_DATA
    """lag_testlyd.py [utfil] [--personvern]: --personvern bruker en tekst med navn, sted, fødselsår, sykdom, parti og telefon."""
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pers = "--personvern" in sys.argv
    ut = pathlib.Path(args[0] if args else ("lyd/rokytest_personvern.wav" if pers else "lyd/rokytest.wav"))
    ut.parent.mkdir(parents=True, exist_ok=True)
    x = np.concatenate([musikk(), tale(tekst=TEKST_PERSONVERN if pers else None)])
    with wave.open(str(ut), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    print(f"{ut}: {len(x)/SR:.1f} s")


if __name__ == "__main__":
    main()
