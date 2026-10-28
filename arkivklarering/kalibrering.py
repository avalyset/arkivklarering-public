"""Kalibrering av personvernflaggene mot et manus (justeringsmanuset KLAR-MANUS-0001; testmanuset KLAR-MANUS-0002 er sperret): scoring og lesing av manus.

Tallnormalisering og scoring (`score.py`, `norm.py`) er en vendor-kopi fra norsk-tale (arkivklarering/_vendor/norsk_tale,
KLAR-ADR-0014). Her legges bare til det som er spesifikt for flaggene: et element regnes som «flagget» når en flaggtreff i
samme kategori har et utdrag som dekker elementets skriveform.
"""
from __future__ import annotations

import pathlib
import sys

from . import evaldata

_V = pathlib.Path(__file__).resolve().parent / "_vendor" / "norsk_tale"
if str(_V) not in sys.path:
    sys.path.insert(0, str(_V))
import norm  # noqa: E402  (vendor)
import score  # noqa: E402  (vendor)


def les_manus(sti, prereg_id=None, kun_struktur=False):
    """TSV med id, malform, klasse, setning, elementer (JSON), dialektutvalg.

    KLAR-MANUS-0002 er testmateriale for H4 og kan ikke leses av rørledningen før preregistreringen er registrert
    (samme sperre som testdelene, `evaldata.sjekk_splitt`). `kun_struktur=True` er for formatkontrollene i `tests/test_manus.py`
    (kolonner, antall, at målelementene står i setningen); de kjører ingen rørledning, mønstre eller ordlister."""
    if pathlib.Path(sti).name.startswith("KLAR-MANUS-0002_") and not kun_struktur:
        evaldata.sjekk_splitt("test", prereg_id)
    return score.les_setninger(sti)


def _dekker(utdrag: str, form: str) -> bool:
    """Utdraget og skriveformen overlapper etter normalisering (tall: tallord og mellomrom i sifre håndteres av score.py)."""
    u, f = score.normaliser(utdrag), score.normaliser(form)
    return bool(u and f and (score._inneholder(u, f) or score._inneholder(f, u)))


def score_flagg(fasit: dict, tekst: str, flagg: list[dict]) -> dict:
    """Scorer ett segment.

    fasit: en manusrad (`les_manus`). tekst: transkripsjonen (ett lag eller union-tekst). flagg: [{kategori, utdrag}], flagg
    fra personvernmotoren for samme segment.
    Per målelement: `tekst_treff` (elementet står i transkripsjonen, vendor score) og `flagg_treff` (et flagg i samme
    kategori har et utdrag som dekker en av skriveformene). Målformfeil rapporteres separat og feller aldri segmentet.
    """
    s = score.score_setning(fasit, tekst)
    elementer = []
    for el, e in zip(fasit["elementer"], s["elementer"]):
        treff = any(f["kategori"] == el["type"] and any(_dekker(f["utdrag"], form) for form in el["former"]) for f in flagg)
        elementer.append({"type": el["type"], "former": el["former"], "tekst_treff": e["treff"], "flagg_treff": treff})
    return {"id": fasit["id"], "klasse": fasit["klasse"], "malform": fasit["malform"], "elementer": elementer,
            "malformfeil": s["malform"]["funn"], "malform_utdata": s["malform"]["utdata"], "wer": s["wer"]}
