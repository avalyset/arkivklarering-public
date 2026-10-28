#!/usr/bin/env python3
"""Måler hva whisper.cpp skriver når stillhet, støy og musikk sendes DIREKTE til modellen,
utenom segmentregelen. Dokumentasjon på hvorfor regelen «aldri music/other til Whisper» finnes.

Lyden er syntetisk (digital stillhet, hvit støy på to nivåer, rosa støy, egenprodusert arpeggio), ikke
arkivmateriale. Resultatet sier hva disse modellene gjør på akkurat denne lyden, ikke hvor ofte
det skjer i et arkiv. Én kjøring per modell og lyd, ett pass om gangen.

    .venv/bin/python scripts/mal_oppdiktet_tekst.py docs/KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v<maj>.<min>_<dato>.md
"""
import datetime
import json
import pathlib
import sys
import tempfile
import time
import wave

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import lag_testlyd  # noqa: E402
from arkivklarering import transkriber  # noqa: E402

SR = 16000


def skriv(x, sti):
    with wave.open(str(sti), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def rosa_stoy(n, rng, topp=0.5):
    """Rosa støy (1/f i effekt): hvit støy formet i frekvensdomenet, normalisert til gitt toppverdi."""
    spekter = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    f[0] = f[1]
    x = np.fft.irfft(spekter / np.sqrt(f), n)
    return (topp * x / np.max(np.abs(x))).astype(np.float32)


def lyder():
    rng = np.random.default_rng(1)
    n = SR * 20
    return {
        "stillhet (digital nuller)": np.zeros(n, dtype=np.float32),
        "svak hvit støy (amplitude 0,01)": (0.01 * rng.standard_normal(n)).astype(np.float32),
        "hvit støy (amplitude 0,2)": (0.2 * rng.standard_normal(n)).astype(np.float32),
        "rosa støy (1/f, toppverdi 0,5)": rosa_stoy(n, np.random.default_rng(2)),
        "syntetisk musikk (arpeggio)": lag_testlyd.musikk(20),
    }


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()  # avbryter hvis cacher og tmp ikke ligger under ARKIVKLARERING_DATA
    ut = pathlib.Path(sys.argv[1])
    resultater = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        for lag in transkriber.LAG:
            o = transkriber.finn_oppsett(lag)
            for navn, x in lyder().items():
                wav = tmp / "x.wav"
                skriv(x, wav)
                t0 = time.time()
                j = transkriber.whisper_direkte(wav, tmp / "x", o)
                cues = [(t["offsets"]["from"] / 1000, t["offsets"]["to"] / 1000, t["text"].strip())
                        for t in j.get("transcription", [])]
                resultater.append({"lag": lag, "modell": pathlib.Path(o.modell).name, "sha256": o.sha256,
                                   "lyd": navn, "cuer": cues, "sek": round(time.time() - t0, 1)})
                print(lag, navn, cues, flush=True)
    dato = datetime.date.today().isoformat()
    md = [f"# Oppdiktet tekst: whisper.cpp direkte på stillhet, støy og musikk ({dato})", "",
          "Dokumentasjon på hvorfor rørledningen aldri sender `music` eller `other` til Whisper. "
          "Syntetisk lyd (20 s hver), `-l nn`, whisper.cpp med standardinnstillinger, én kjøring per "
          "modell og lyd. Sier hva modellene gjør på akkurat denne lyden, ikke hvor ofte det skjer i et "
          "arkiv. Generert av `scripts/mal_oppdiktet_tekst.py`.", ""]
    for r in resultater:
        md.append(f"## {r['lag']} · {r['lyd']}")
        md.append(f"Modell `{r['modell']}`, sha256 `{r['sha256']}`, {r['sek']} s.")
        md.append("")
        if r["cuer"]:
            md += [f"- {a:.2f}–{b:.2f} s: «{t}»" for a, b, t in r["cuer"]]
        else:
            md.append("- (ingen tekst)")
        md.append("")
    ut.write_text("\n".join(md), encoding="utf-8")
    ut.with_suffix(".json").write_text(json.dumps(resultater, ensure_ascii=False, indent=2), encoding="utf-8")
    print(ut)


if __name__ == "__main__":
    main()
