"""Segmentering med inaSpeechSegmenter (INA): standard segmentør i arkivklarering (KLAR-ADR-0019 v1.1, AV-25); inaVAMOS er et valgfritt tillegg.

Samme grensesnitt som `segment.segmenter`: `segmenter(lydfil, enhet="cpu") -> [(etikett, start, stopp)]`, med etikettene arkivklarering bruker
(`speech`, `music`, `other`), slik at `segment.bygg_tidslinje`, `felles.py` og `kalibrering/kjor_h4.py` kan bruke den uten andre endringer
(se `segment.segmenter`, som bruker denne kjøreren som standard; ARKIVKLARERING_SEGMENTERING=inavamos velger i stedet inaVAMOS for H1/H2).

inaSpeechSegmenter kjører i et eget venv via `_inaseg_runner.py` (TensorFlow bare der), som pyannote i `diarisering.py`. `segmenter` bruker én
vedvarende runner-prosess (modellen lastes én gang; JSON-linjer inn og ut), `segmenter_flere` én runner per kall med en jobbfil.

Etikettkart: speech, male og female → speech; music → music; noise og noEnergy → other. inaSpeechSegmenter har **ingen klasse for tale over
musikk**, så `speech+music` blir aldri produsert og flagget «musikk under tale – vurder rettigheter» faller bort (se KLAR-ADR-0019).
`enhet` tas imot for samme signatur som `segment.segmenter`, men brukes ikke (TensorFlow på CPU).
"""
from __future__ import annotations

import atexit
import datetime
import json
import os
import pathlib
import subprocess
import sys
import tempfile

from .miljo import DATA

VENV_PYTHON = pathlib.Path(os.environ.get("ARKIVKLARERING_INASEG_PYTHON") or DATA / "venv-inaseg" / "bin" / "python")
RUNNER = pathlib.Path(__file__).resolve().parent / "_inaseg_runner.py"

ETIKETTKART = {"speech": "speech", "male": "speech", "female": "speech", "music": "music", "noise": "other", "noEnergy": "other"}


INASEG_VERSJON = "0.8.0"  # låst i requirements-inaseg.lock
LOGG_MILJOVARIABEL = "ARKIVKLARERING_SEGMENTERING_LOGG"
_KALL = {"antall": 0, "registrert": False}


class InasegFeil(RuntimeError):
    pass


def _skriv_logg(objekt: dict) -> None:
    sti = os.environ.get(LOGG_MILJOVARIABEL)
    if sti:
        with open(sti, "a", encoding="utf-8") as f:
            f.write(json.dumps(objekt, ensure_ascii=False) + "\n")


def _sammendrag() -> None:
    _skriv_logg({"sammendrag": True, "tid": datetime.datetime.now().isoformat(timespec="seconds"), "kjorer": f"inaSpeechSegmenter {INASEG_VERSJON}",
                 "antall_kall": _KALL["antall"], "inavamos_importert": "inavamos" in sys.modules})


def _logg_kall(lyd, segmenter_ut) -> None:
    """Én linje per segmentert fil i loggen (miljøvariabelen ARKIVKLARERING_SEGMENTERING_LOGG), og et sammendrag når prosessen avslutter:
    antall kall og om inaVAMOS er importert (skal være false). Dokumenterer at segmenteringen faktisk kjørte med inaSpeechSegmenter."""
    _KALL["antall"] += 1
    if not _KALL["registrert"]:
        _KALL["registrert"] = True
        atexit.register(_sammendrag)
    _skriv_logg({"tid": datetime.datetime.now().isoformat(timespec="seconds"), "lyd": str(lyd), "n_segmenter": len(segmenter_ut)})


def _miljo() -> dict:
    """Miljø for runner-prosessen: modellvektene (hdf5) lagres under ARKIVKLARERING_DATA (KERAS_HOME), ikke i ~/.keras, og TensorFlow er stille."""
    env = dict(os.environ)
    env.setdefault("KERAS_HOME", str(DATA / "cache" / "keras"))
    env.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    return env


def kart_etiketter(raa, toleranse: float = 1e-3) -> list[tuple[str, float, float]]:
    """[(inaSpeechSegmenter-etikett, start, stopp)] → [(arkivklarering-etikett, start, stopp)].

    Naboer som får samme etikett og henger sammen (gap ≤ `toleranse` s) slås sammen, så «male» rett etter «female» blir ett `speech`-segment.
    Ukjente etiketter beholdes uendret; `segment.bygg_tidslinje` sender dem til menneskelig vurdering.
    """
    ut: list[tuple[str, float, float]] = []
    for etikett, a, b in raa:
        ny = ETIKETTKART.get(etikett, etikett)
        if ut and ut[-1][0] == ny and a - ut[-1][2] <= toleranse:
            ut[-1] = (ny, ut[-1][1], max(ut[-1][2], float(b)))
        else:
            ut.append((ny, float(a), float(b)))
    return ut


def _sjekk_oppsett():
    if not VENV_PYTHON.is_file():
        raise InasegFeil(f"fant ikke {VENV_PYTHON}: opprett venv-inaseg (requirements-inaseg.lock)")


class _Server:
    """Én vedvarende runner-prosess (modellen lastes én gang)."""

    def __init__(self):
        _sjekk_oppsett()
        self.p = subprocess.Popen([str(VENV_PYTHON), str(RUNNER), "--server"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, bufsize=1, env=_miljo())

    def segmenter(self, lyd) -> list:
        if self.p.poll() is not None:
            raise InasegFeil(f"runner er stoppet (rc={self.p.returncode})")
        self.p.stdin.write(json.dumps({"lyd": str(pathlib.Path(lyd).resolve())}) + "\n")
        self.p.stdin.flush()
        linje = self.p.stdout.readline()
        while linje and not linje.lstrip().startswith("{"):  # tåler støy på stdout fra biblioteker
            linje = self.p.stdout.readline()
        if not linje:
            raise InasegFeil(f"runner ga ingen svar (rc={self.p.poll()})")
        svar = json.loads(linje)
        if not svar.get("ok"):
            raise InasegFeil(svar.get("feil", "ukjent feil"))
        return svar["segmenter"]

    def lukk(self):
        if self.p.poll() is None:
            try:
                self.p.stdin.close()
                self.p.wait(timeout=10)
            except Exception:  # noqa: BLE001
                self.p.kill()


_SERVER: _Server | None = None


def segmenter(lydfil, enhet: str = "cpu") -> list[tuple[str, float, float]]:
    """Samme signatur og returtype som `segment.segmenter`, men med inaSpeechSegmenter og arkivklareringens etiketter."""
    global _SERVER
    if _SERVER is None or _SERVER.p.poll() is not None:
        _SERVER = _Server()
    ut = kart_etiketter(_SERVER.segmenter(lydfil))
    _logg_kall(lydfil, ut)
    return ut


def lukk() -> None:
    global _SERVER
    if _SERVER is not None:
        _SERVER.lukk()
        _SERVER = None


def segmenter_flere(lydfiler, enhet: str = "cpu") -> list[list[tuple[str, float, float]]]:
    """Én runner-prosess for flere filer (modellen lastes én gang). Returnerer en liste per fil, i samme rekkefølge."""
    _sjekk_oppsett()
    with tempfile.TemporaryDirectory(prefix="inaseg-") as tmp:
        tmp = pathlib.Path(tmp)
        filer = [{"lyd": str(pathlib.Path(l).resolve()), "ut": str(tmp / f"{i}.json")} for i, l in enumerate(lydfiler)]
        jobb = tmp / "jobb.json"
        jobb.write_text(json.dumps({"filer": filer, "vad_engine": "smn"}), encoding="utf-8")
        r = subprocess.run([str(VENV_PYTHON), str(RUNNER), str(jobb)], capture_output=True, text=True, env=_miljo())
        if r.returncode != 0:
            siste = (r.stderr or r.stdout).strip().splitlines()
            raise InasegFeil(siste[-1] if siste else f"runner rc={r.returncode}")
        ut = [kart_etiketter(json.loads(pathlib.Path(f["ut"]).read_text(encoding="utf-8"))["segmenter"]) for f in filer]
        for f, u in zip(filer, ut):
            _logg_kall(f["lyd"], u)
        return ut
