#!/usr/bin/env python3
"""Beviser at utregningen i DEV-skriptene er uendret etter at parametre (--per-dialekt, --ut-mappe, --etikett, --eval-nr) ble lagt til.

Kjører DEV-skriptene med STANDARDVERDIER uten Whisper og sammenligner med de committede resultatene; kravet er identiske tall:

  KLAR-EVAL-0002 v1.1  eval/dev/kjor_dev.py: Whisper-kallet byttes med de lagrede hypotesene (samme segmentering, samme trekk, samme WER-kode)
  KLAR-EVAL-0006 v1.2  eval/dev/kjor_flaggoverlevelse_ord.py --datasett nbsamtale --fase evaluer (lagrede hypoteser fra reproduksjonen 27.10)
  KLAR-EVAL-0007 v1.1  samme skript, --datasett npsc --fase evaluer
  KLAR-EVAL-0005       eval/dev/kjor_personvern_dev.py (ingen Whisper; NorNE-modeller), `--bare 5`; sjekker også at tellerne per setning (ny utdatafil)
                       summerer til de aggregerte tellene

    source scripts/miljo.sh && .venv/bin/python scripts/verifiser_uendret.py [--bare 2,6,7,5] [--repro <eval-data-mappe>]

Skriver en tabell (identisk ja/nei per EVAL, med første avvik) til stdout og et exit-nummer ulik 0 hvis noe er ulikt. Skriver ingenting i repoet.

Segmentering: de lagrede resultatene er laget med inaVAMOS. Standarden er nå inaSpeechSegmenter (KLAR-ADR-0019 v1.1), så skriptet setter
ARKIVKLARERING_SEGMENTERING=inavamos eksplisitt (også for underprosesser) og krever tillegget reproduksjon-h1h2. Bare KLAR-EVAL-0002 segmenterer
(kjor_dev.py kaller segment.segmenter på de 60 filene); 0006/0007 (--fase evaluer) og 0005 segmenterer ikke, men får samme miljø.
"""
import argparse
import importlib.util
import json
import pathlib
import sys
import tempfile
import types

REPO = pathlib.Path(__file__).resolve().parent.parent
DEV = REPO / "eval" / "dev"
SPRAK = {"bokmaal": "nb", "nynorsk": "nn"}
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(DEV))
from arkivklarering import miljo  # noqa: E402

REPRO = miljo.DATA / "reproduksjon" / "20261027-003846" / "eval-data"  # cachene herfra er laget med inaVAMOS (uten suffiks)


def last_modul(navn):
    spec = importlib.util.spec_from_file_location(navn, DEV / f"{navn}.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[navn] = m
    spec.loader.exec_module(m)
    return m


def les(sti):
    return json.loads(pathlib.Path(sti).read_text(encoding="utf-8"))


def siste(mønster):
    return sorted(REPO.glob(mønster))[-1]


def diff(a, b, sti="", ut=None, maks=8):
    """Eksakt sammenligning (floats bit for bit); første avvikene som liste av (sti, a, b)."""
    ut = [] if ut is None else ut
    if len(ut) >= maks:
        return ut
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                ut.append((f"{sti}/{k}", "mangler" if k not in a else "finnes", "mangler" if k not in b else "finnes"))
            else:
                diff(a[k], b[k], f"{sti}/{k}", ut, maks)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            ut.append((f"{sti}[]", f"lengde {len(a)}", f"lengde {len(b)}"))
        for i, (x, y) in enumerate(zip(a, b)):
            diff(x, y, f"{sti}[{i}]", ut, maks)
    elif a != b or type(a) is not type(b):
        ut.append((sti, a, b))
    return ut


def eval0002(tmp):
    kd = last_modul("kjor_dev")
    lagret = les(siste("eval/dev/KLAR-EVAL-0002_*v1.1_*.json"))
    utv = les(siste("eval/dev/KLAR-EVAL-0003_*.json"))["utvalg"]
    fil_til_nokkel = {pathlib.PurePosixPath(r["file_name"]).name: f'{r["source_file_id"]}_{r["segment_id"]}' for r in utv}
    assert len(fil_til_nokkel) == len(utv)
    hyp = {s["id"]: s["hyp"] for s in lagret["segmenter"]}
    antall = {}
    n = len(utv)

    def falsk(lyd_sti, tidslinje, o):
        lag = "ra" if "verbatim" in pathlib.Path(o.modell).name else "normalisert"
        i = antall[lag] = antall.get(lag, -1) + 1
        konfig = ("nn", "matchet")[i // n]
        return [types.SimpleNamespace(tekst=hyp[fil_til_nokkel[pathlib.Path(lyd_sti).name]][f"{lag}/{konfig}"])]

    kd.transkriber.transkriber = falsk
    sys.argv = ["kjor_dev.py", "--ut-mappe", str(tmp)]  # alt annet er standardverdier
    kd.main()
    ny = les(next(pathlib.Path(tmp).glob("KLAR-EVAL-0002_*.json")))
    ny_utv = les(next(pathlib.Path(tmp).glob("KLAR-EVAL-0003_*.json")))["utvalg"]
    return diff({"wer": lagret["wer"], "segmenter": lagret["segmenter"], "seed": lagret["seed"], "modeller": lagret["modeller"], "utvalg": utv},
                {"wer": ny["wer"], "segmenter": ny["segmenter"], "seed": ny["seed"], "modeller": ny["modeller"], "utvalg": ny_utv}), len(ny["segmenter"])


def flagg(tmp, datasett, lagret_sti, repro):
    fo = last_modul("kjor_flaggoverlevelse_ord")
    fo.EVALDATA = repro
    sys.argv = ["kjor_flaggoverlevelse_ord.py", "--datasett", datasett, "--fase", "evaluer", "--ut-mappe", str(tmp)]  # standardverdier ellers
    fo.main()
    ny = les(next(pathlib.Path(tmp).glob("KLAR-EVAL-000*.json")))
    lagret = les(lagret_sti)
    return diff(lagret, ny), ny.get("segmenter")


def eval0005(tmp):
    import subprocess
    p = subprocess.run([sys.executable, str(DEV / "kjor_personvern_dev.py"), "--ut-mappe", str(tmp)], cwd=REPO, capture_output=True, text=True)
    if p.returncode:
        return [("kjøring", f"returkode {p.returncode}", p.stderr[-300:])], None
    ny = les(next(f for f in sorted(pathlib.Path(tmp).glob("KLAR-EVAL-0005_*.json")) if not f.name.endswith(".setninger.json")))
    lagret = les(siste("docs/KLAR-EVAL-0005_*.json"))
    for d in (ny, lagret):
        d.pop("sekunder", None)  # kjøretid er ikke et tall i utregningen
    avvik = diff(lagret, ny)
    # tellerne per setning (ny utdatafil) skal summere til de aggregerte tellene
    s = les(next(pathlib.Path(tmp).glob("KLAR-EVAL-0005_*.setninger.json")))
    k = s["kolonner"]
    sum_ = {}
    for rad in s["rader"]:
        r = dict(zip(k, rad))
        nokkel = (SPRAK[r["config"]], r["type"], r["motor"], r["variant"])
        t = sum_.setdefault(nokkel, [0] * 6)
        for i, navn in enumerate(("gull", "gull_overlapp", "gull_noyaktig", "pred", "pred_overlapp", "pred_noyaktig")):
            t[i] += r[navn]
    for (sprak, typ, motor, variant), (gull, go, gn, pred, po, pn) in sum_.items():
        v = ny["resultat"][f"{sprak}|{typ}|{motor}|{variant}"]
        if (gull, pred) != (v["gull"], v["predikert"]):
            avvik.append((f"setninger/{sprak}|{typ}|{motor}|{variant}", (gull, pred), (v["gull"], v["predikert"])))
        for navn, k_, n in (("recall_overlapp", go, gull), ("recall_noyaktig", gn, gull), ("presisjon_overlapp", po, pred), ("presisjon_noyaktig", pn, pred)):
            if v[navn] != (None if n == 0 else round(k_ / n, 3)):
                avvik.append((f"setninger/{sprak}|{typ}|{motor}|{variant}/{navn}", v[navn], round(k_ / n, 3) if n else None))
    if len(sum_) != len(ny["resultat"]):
        avvik.append(("setninger/antall nøkler", len(sum_), len(ny["resultat"])))
    return avvik, f'{len(ny["resultat"])} nøkler, {len(s["rader"])} setningsrader'


SEGMENTERING_LAGRET = "inavamos"  # segmentøren de lagrede resultatene er laget med (sammenligningen krever samme)


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    import os
    os.environ["ARKIVKLARERING_SEGMENTERING"] = SEGMENTERING_LAGRET  # eksplisitt, uavhengig av kallerens miljø (se docstringen)
    ap = argparse.ArgumentParser()
    ap.add_argument("--bare", default="2,6,7,5")
    ap.add_argument("--repro", default=str(REPRO))
    a = ap.parse_args()
    valgt = set(a.bare.split(","))
    rader, feil = [], 0
    jobber = [("2", "KLAR-EVAL-0002 v1.1", lambda t: eval0002(t)),
              ("6", "KLAR-EVAL-0006 v1.2", lambda t: flagg(t, "nbsamtale", siste("docs/KLAR-EVAL-0006_*v1.2_*.json"), pathlib.Path(a.repro))),
              ("7", "KLAR-EVAL-0007 v1.1", lambda t: flagg(t, "npsc", siste("docs/KLAR-EVAL-0007_*v1.1_*.json"), pathlib.Path(a.repro))),
              ("5", "KLAR-EVAL-0005 (NorNE)", lambda t: eval0005(t))]
    for nr, navn, f in jobber:
        if nr not in valgt:
            continue
        with tempfile.TemporaryDirectory(dir=miljo.DATA / "tmp") as tmp:
            d, n = f(tmp)
        rader.append(f"| {navn} | {'JA' if not d else 'NEI'} | {n if n is not None else '–'} | " + ("–" if not d else "; ".join(f"{s}: {x!r} ≠ {y!r}" for s, x, y in d)[:600]) + " |")
        feil += bool(d)
        print(rader[-1], flush=True)
    print("\n| EVAL | identiske tall | enheter | første avvik |\n|---|---|---|---|\n" + "\n".join(rader))
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
