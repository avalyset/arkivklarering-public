#!/usr/bin/env python3
"""DER-måling (DEV) av talerinndelingen på NB Samtale validation (CC0, `speaker_id` per ytring; KLAR-EVAL-0004).

KJØRES I venv-diarisering (pyannote.audio 4 og pyannote.metrics):
    source scripts/miljo.sh && $ARKIVKLARERING_DATA/venv-diarisering/bin/python eval/dev/kjor_der.py [--enhet cpu|mps]

Materialet er ytringer (segmenter) fra 35 opptak, ikke hele opptak: for hvert opptak ligger bare 2 til 13 minutter tale spredt utover
15 til 145 minutter. **Hver kilde settes derfor sammen av sine ytringer i tidsrekkefølge** (opprinnelig pause mellom ytringene,
begrenset til 0,2–2,0 s; null for overlappende naboer), og referansen er `speaker_id` for hver ytring. Det er en konstruert
sammenstilling, ikke en opptaksrekonstruksjon: ingen overlappende tale (ytringene legges etter hverandre) og andre pausemønstre enn i
samtalen. DER her er derfor ikke sammenlignbar med DER på hele opptak. Standard DER (pyannote.metrics): missed speech + false alarm +
speaker confusion, delt på total referansetale; collar 0,25 s (standard i litteraturen) og 0 s; overlappende tale i referansen
telles med (`skip_overlap=False`; referansen har ingen overlapp i denne sammenstillingen). Antall talere er ukjent for modellen.
Skriver `docs/KLAR-EVAL-0012_arkivklarering_talerinndeling-der-dev_v1.0_<dato>.{json,md}` (tallene; tolkningen skrives for hånd).
"""
import argparse
import collections
import datetime
import json
import pathlib
import sys
import tarfile
import time
import wave

import numpy as np

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))
from arkivklarering import miljo  # noqa: E402  (bare standardbiblioteket; virker også i venv-diarisering)

DATA = miljo.EVAL_DATA / "nb_samtale"
ALLE = DATA / "alle_validation"
ARB = miljo.DATA / "tmp" / "der"
DATO = datetime.date.today().isoformat()
SR = 16000
MODELL = "pyannote/speaker-diarization-community-1"


def pakk_ut():
    ALLE.mkdir(exist_ok=True)
    for form in ("bm", "nn"):
        t = DATA / f"validation_{form}_1.tar.gz"
        if (ALLE / f".ferdig_{form}").exists():
            continue
        with tarfile.open(t) as tf:
            tf.extractall(ALLE, filter="data")
        (ALLE / f".ferdig_{form}").write_text("ok")


def les_wav(p):
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1 and w.getsampwidth() == 2, (p, w.getparams())
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)


def bygg_kilde(kid, rader):
    """Setter sammen ytringene i tidsrekkefølge. Returnerer (wav-sti, referanse [(start, stopp, taler)])."""
    ms = lambda r: tuple(int(x) for x in r["segment_id"].split("-"))  # noqa: E731
    rader = sorted(rader, key=ms)
    deler, ref, t, forrige_slutt = [], [], 0.0, None
    for r in rader:
        a, b = ms(r)
        gap = 0.0 if forrige_slutt is None else min(2.0, max(0.2, (a - forrige_slutt) / 1000))
        if gap and deler:
            deler.append(np.zeros(int(gap * SR), dtype=np.int16))
            t += gap
        x = les_wav(ALLE / pathlib.PurePosixPath(r["file_name"]))
        ref.append((round(t, 3), round(t + len(x) / SR, 3), r["speaker_id"]))
        deler.append(x)
        t += len(x) / SR
        forrige_slutt = b
    sti = ARB / f"{kid}.wav"
    with wave.open(str(sti), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.concatenate(deler).tobytes())
    return sti, ref


def main():
    sys.path.insert(0, str(REPO))
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    ap = argparse.ArgumentParser()
    ap.add_argument("--enhet", default="cpu")
    a = ap.parse_args()
    from pyannote.core import Annotation, Segment
    from pyannote.metrics.diarization import DiarizationErrorRate

    ARB.mkdir(parents=True, exist_ok=True)
    pakk_ut()
    rader = [json.loads(l) for l in open(DATA / "validation_metadata.jsonl", encoding="utf-8")]
    per_kilde = collections.defaultdict(list)
    for r in rader:
        per_kilde[r["source_file_id"]].append(r)
    kilder = {}
    for kid in sorted(per_kilde):
        kilder[kid] = bygg_kilde(kid, per_kilde[kid])
    tot_s = sum(ref[-1][1] for _, ref in kilder.values())
    print(f"{len(kilder)} kilder, {tot_s / 60:.1f} min sammenstilt lyd", flush=True)

    sys.path.insert(0, str(REPO / "arkivklarering"))
    import _diarisering_runner as runner  # noqa: E402  (samme runner som rørledningen bruker)
    import torch
    from pyannote.audio import Pipeline

    pipe = Pipeline.from_pretrained(MODELL, token=runner.les_token())
    pipe.to(torch.device(a.enhet))
    resultat, t0 = {}, time.time()
    cache = ARB / f"hyp_{a.enhet}"
    cache.mkdir(exist_ok=True)
    for kid, (wav, ref) in kilder.items():
        c = cache / f"{kid}.json"
        if not c.exists():
            ut = pipe(str(wav))
            full = getattr(ut, "speaker_diarization", ut)
            c.write_text(json.dumps([[round(t.start, 3), round(t.end, 3), str(l)] for t, _, l in full.itertracks(yield_label=True)]), encoding="utf-8")
        print(f"  {kid} ({time.time() - t0:.0f} s)", flush=True)
    for kid, (wav, ref) in kilder.items():
        R, H = Annotation(), Annotation()
        for s, e, sp in ref:
            R[Segment(s, e)] = sp
        for s, e, sp in json.loads((cache / f"{kid}.json").read_text(encoding="utf-8")):
            H[Segment(s, e)] = sp
        resultat[kid] = {"lengde_s": round(ref[-1][1], 1), "talere_referanse": len({sp for _, _, sp in ref}), "talere_estimert": len(H.labels()), "ytringer": len(ref)}
        for collar in (0.25, 0.0):
            m = DiarizationErrorRate(collar=collar, skip_overlap=False)
            d = m(R, H, detailed=True)
            resultat[kid][f"collar_{collar}"] = {"der": round(d["diarization error rate"], 4), "total": round(d["total"], 2), "missed": round(d["missed detection"], 2),
                                                 "false_alarm": round(d["false alarm"], 2), "confusion": round(d["confusion"], 2)}
    samlet = {}
    for collar in (0.25, 0.0):
        k = f"collar_{collar}"
        tot = sum(v[k]["total"] for v in resultat.values())
        part = {x: sum(v[k][x] for v in resultat.values()) for x in ("missed", "false_alarm", "confusion")}
        samlet[k] = {"der": round(sum(part.values()) / tot, 4), "total_s": round(tot, 1), **{x: round(y / tot, 4) for x, y in part.items()}}
    antall = [(v["talere_referanse"], v["talere_estimert"]) for v in resultat.values()]
    ut = {"merknad": "DEV, ikke pilot. Konstruert sammenstilling av ytringer (ikke hele opptak).", "modell": MODELL, "enhet": a.enhet, "datasett": "Sprakbanken/nb_samtale, validation (CC0)",
          "kilder": len(kilder), "lengde_min": round(tot_s / 60, 1), "kjoretid_s": round(time.time() - t0), "samlet": samlet,
          "talerantall": {"riktig": sum(1 for r, e in antall if r == e), "for_mange": sum(1 for r, e in antall if e > r), "for_faa": sum(1 for r, e in antall if e < r), "n": len(antall)},
          "per_kilde": resultat}
    stub = REPO / "docs" / f"KLAR-EVAL-0012_arkivklarering_talerinndeling-der-dev_v1.0_{DATO}"
    pathlib.Path(str(stub) + ".json").write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    L = ["# KLAR-EVAL-0012: Talerinndeling, DER på NB Samtale validation (DEV)", "",
         "**DEV, ikke pilot. Konstruert sammenstilling av ytringer (hver kilde = ytringene i tidsrekkefølge), ikke hele opptak.**", "",
         f"Versjon 1.0, {DATO}. Tall generert av `eval/dev/kjor_der.py`; tolkning skrevet for hånd (under «Vurdering»).", "",
         "## Oppsett", "",
         f"- **Modell:** `{MODELL}` (pyannote.audio, samme standardmodell som WhisperX), antall talere ukjent for modellen, enhet {a.enhet}.",
         "- **Materiale:** NB Samtale validation (1194 ytringer, 35 kilder; CC0, KLAR-EVAL-0004). Se `eval/dev/kjor_der.py` for sammenstillingen: ytringer i tidsrekkefølge, pause mellom dem fra originalen begrenset til 0,2–2,0 s, ingen overlapp.",
         "- **Mål:** DER = (missed speech + false alarm + speaker confusion) / total referansetale (pyannote.metrics), collar 0,25 s og 0 s. Referanse: `speaker_id` per ytring.", "",
         "## Samlet", "", "| collar | DER | missed | false alarm | confusion | total referansetale (s) |", "|---|---|---|---|---|---|"]
    for k, v in samlet.items():
        L.append(f"| {k.split('_')[1]} s | {v['der']:.3f} | {v['missed']:.3f} | {v['false_alarm']:.3f} | {v['confusion']:.3f} | {v['total_s']} |".replace(".", ","))
    L += ["", f"Antall talere: riktig {ut['talerantall']['riktig']} av {ut['talerantall']['n']} kilder, for mange {ut['talerantall']['for_mange']}, for få {ut['talerantall']['for_faa']}.", "",
          "## Per kilde (collar 0,25 s)", "", "| kilde | lengde (s) | ytringer | talere ref/est | DER | missed | false alarm | confusion |", "|---|---|---|---|---|---|---|---|"]
    for kid, v in resultat.items():
        d = v["collar_0.25"]
        t = d["total"] or 1
        L.append(f"| {kid} | {v['lengde_s']} | {v['ytringer']} | {v['talere_referanse']}/{v['talere_estimert']} | {d['der']:.3f} | {d['missed'] / t:.3f} | {d['false_alarm'] / t:.3f} | {d['confusion'] / t:.3f} |".replace(".", ","))
    L += ["", f"Rådata: `{pathlib.Path(str(stub) + '.json').name}` (bare tall).", ""]
    pathlib.Path(str(stub) + ".md").write_text("\n".join(L), encoding="utf-8")
    print(str(stub) + ".md")
    print(json.dumps(samlet))


if __name__ == "__main__":
    main()
