"""Talerinndeling (speaker diarization) med pyannote, standardløsningen (KLAR-ADR-0016).

Modellen er den samme som WhisperX bruker som standard: `pyannote/speaker-diarization-community-1`. Den kjører i et eget venv via
`_diarisering_runner.py` (pyannote.audio med egen torch), så det låste analysemiljøet ikke berøres. Talere merkes anonymt, TALER_1,
TALER_2 … i den rekkefølgen de først snakker. Det gjøres **ingen** identifisering og ingen stemmegjenkjenning mot kjente personer, og
etikettene gjelder bare innenfor én sending (TALER_1 i én fil er ikke samme person som TALER_1 i en annen).
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import tempfile
from dataclasses import dataclass

from .miljo import DATA

MODELL = "pyannote/speaker-diarization-community-1"
VENV_PYTHON = pathlib.Path(os.environ.get("ARKIVKLARERING_DIARISERING_PYTHON") or DATA / "venv-diarisering" / "bin" / "python")
RUNNER = pathlib.Path(__file__).resolve().parent / "_diarisering_runner.py"
MERKNAD = ("Anonyme talermerker (TALER_1, TALER_2 …) fra pyannote; forslag til menneskelig vurdering. Ingen identifisering og ingen "
           "stemmegjenkjenning mot kjente personer. Merkene gjelder bare innenfor denne sendingen.")


@dataclass(frozen=True)
class Tur:
    start: float
    stopp: float
    taler: str  # TALER_n


class DiariseringFeil(RuntimeError):
    pass


def navngi_talere(rå_turer) -> list[Tur]:
    """[{start, stopp, etikett}] → [Tur] med TALER_n i rekkefølgen etikettene først snakker."""
    navn: dict[str, str] = {}
    ut = []
    for t in sorted(rå_turer, key=lambda x: (x["start"], x["stopp"])):  # nummereringen følger første opptreden i tid
        navn.setdefault(t["etikett"], f"TALER_{len(navn) + 1}")
        ut.append(Tur(float(t["start"]), float(t["stopp"]), navn[t["etikett"]]))
    return ut


def taler_for_tidsrom(turer: list[Tur], start: float, stopp: float) -> str | None:
    """Taleren med mest overlapp med [start, stopp]; None når ingen tur overlapper. Likt overlapp: den som snakket først."""
    best, best_o = None, 0.0
    for t in turer:
        o = min(stopp, t.stopp) - max(start, t.start)
        if o > best_o + 1e-9:
            best, best_o = t.taler, o
    return best


def tildel_cuer(cues, turer: list[Tur]) -> list[str | None]:
    """En taler (eller None) per cue, parallelt med `cues`."""
    return [taler_for_tidsrom(turer, c.start, c.stop) for c in cues]


def kjor(lyd, enhet: str = "cpu", antall_talere: int | None = None) -> list[Tur]:
    """Kjører pyannote på lydfila (via runner i eget venv). Modellen er gated: HF_TOKEN må finnes i miljøet eller i .env."""
    return kjor_flere([lyd], enhet, antall_talere)[0]


def kjor_flere(lydfiler, enhet: str = "cpu", antall_talere: int | None = None, modell: str = MODELL):
    """Én runner-prosess for flere filer (modellen lastes én gang). Returnerer [list[Tur]] i samme rekkefølge."""
    if not VENV_PYTHON.is_file():
        raise DiariseringFeil(f"fant ikke {VENV_PYTHON}: opprett venv-diarisering (requirements-diarisering.lock)")
    with tempfile.TemporaryDirectory(prefix="diarisering-") as tmp:
        tmp = pathlib.Path(tmp)
        filer = [{"lyd": str(pathlib.Path(l).resolve()), "ut": str(tmp / f"{i}.json")} for i, l in enumerate(lydfiler)]
        jobb = tmp / "jobb.json"
        jobb.write_text(json.dumps({"filer": filer, "modell": modell, "enhet": enhet, "antall_talere": antall_talere}), encoding="utf-8")
        r = subprocess.run([str(VENV_PYTHON), str(RUNNER), str(jobb)], capture_output=True, text=True)
        if r.returncode != 0:
            raise DiariseringFeil((r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else f"runner rc={r.returncode}")
        return [navngi_talere(json.loads(pathlib.Path(f["ut"]).read_text(encoding="utf-8"))["tur"]) for f in filer]
