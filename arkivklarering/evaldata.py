"""Hard sperre for testdelen av evalueringsdata (NB Samtale).

`train` og `validation` brukes til utvikling (DEV). `test` er reservert for piloten og kan ikke
lastes uten en preregistrering: `--prereg-id KLAR-PREREG-<NNNN>` må oppgis, `docs/KLAR-PREREG-<NNNN>_*.md` må finnes, og
fila må ha statuslinjen `Status: registrert <OSF-URL>` (et utkast har `Status: UTKAST` og åpner ingenting). Alt som leser
datasettet går gjennom denne modulen.
"""
from __future__ import annotations

import pathlib
import re

SPLITT = ("train", "validation", "test")
_PREREG = re.compile(r"^KLAR-PREREG-\d{4}$")
DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"


class TestdelSperret(PermissionError):
    """Testdelen er sperret uten preregistrering."""

    __test__ = False  # ikke en pytest-klasse


def versjonsnokkel(sti) -> tuple:
    """Sorteringsnøkkel etter versjonsnummeret i filnavnet (`..._v1.10_...` er nyere enn `..._v1.9_...`), ikke leksikografisk."""
    m = re.search(r"_v(\d+(?:\.\d+)*)_", pathlib.Path(sti).name)
    return (tuple(int(x) for x in m.group(1).split(".")) if m else (), pathlib.Path(sti).name)


def siste_versjon(filer):
    """Den nyeste filen etter versjonsnummer (versjonssortering). Tom liste gir IndexError, som `sorted(...)[-1]`."""
    return sorted(filer, key=versjonsnokkel)[-1]


def sjekk_splitt(splitt: str, prereg_id: str | None = None, docs: pathlib.Path | None = None) -> str:
    if splitt not in SPLITT:
        raise ValueError(f"Ukjent splitt «{splitt}». Gyldige: {', '.join(SPLITT)}")
    if splitt != "test":
        return splitt
    if not prereg_id or not _PREREG.match(prereg_id):
        raise TestdelSperret("test-delen kan ikke lastes uten --prereg-id KLAR-PREREG-<NNNN>")
    docs = DOCS if docs is None else docs  # leses ved kall, slik at tester kan peke DOCS til en egen mappe
    filer = sorted(pathlib.Path(docs).glob(f"{prereg_id}_*.md"), key=versjonsnokkel)
    if not filer:
        raise TestdelSperret(f"{prereg_id}: fant ingen docs/{prereg_id}_*.md. "
                             "Preregistreringen må ligge i repoet før testdelen åpnes.")
    if not re.search(r"^Status:\s*registrert\b", filer[-1].read_text(encoding="utf-8"), re.I | re.M):
        raise TestdelSperret(f"{filer[-1].name} er ikke registrert (statuslinjen må være «Status: registrert <OSF-URL>»; "
                             "et utkast åpner ikke testdelen).")
    return splitt


def metadata_sti(data: pathlib.Path, splitt: str, prereg_id: str | None = None) -> pathlib.Path:
    return pathlib.Path(data) / f"{sjekk_splitt(splitt, prereg_id)}_metadata.jsonl"


def tar_sti(data: pathlib.Path, splitt: str, form: str, prereg_id: str | None = None) -> pathlib.Path:
    return pathlib.Path(data) / f"{sjekk_splitt(splitt, prereg_id)}_{form}_1.tar.gz"


def norne_sti(data: pathlib.Path, config: str, splitt: str, prereg_id: str | None = None) -> pathlib.Path:
    """NorNE (NbAiLab/norne): `config` er `bokmaal` eller `nynorsk`. test-delen er sperret."""
    if config not in ("bokmaal", "nynorsk"):
        raise ValueError(f"Ukjent NorNE-config «{config}»")
    return pathlib.Path(data) / config / f"{sjekk_splitt(splitt, prereg_id)}-00000-of-00001.parquet"


NPSC_MAPPE = {"train": "train", "validation": "eval", "test": "test"}  # NbAiLab/NPSC kaller valideringsdelen «eval»


def npsc_mappe(data: pathlib.Path, splitt: str, prereg_id: str | None = None) -> pathlib.Path:
    """NPSC (NbAiLab/NPSC): mappen med skjøtene for en datasettdel. `validation` ligger i `eval/`. test-delen er sperret."""
    return pathlib.Path(data) / NPSC_MAPPE[sjekk_splitt(splitt, prereg_id)]
