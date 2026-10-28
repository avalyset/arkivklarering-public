"""Segmentering: tale, musikk, (tale+musikk) og annet, med en utskiftbar segmentør, og tidslinje med disposisjon.

Segmentøren velges med miljøvariabelen ARKIVKLARERING_SEGMENTERING (KLAR-ADR-0019 v1.1, AV-25):

  inaseg    (standard) inaSpeechSegmenter (INA, MIT), i eget venv via `segment_inaseg` (requirements-inaseg.lock)
  inavamos  (valgfritt) inaVAMOS (INA), bare for å reprodusere de preregistrerte kjøringene H1 og H2; tillegget
            `reproduksjon-h1h2`. Pantagruel Research-only License: bare forskning, art. 3 forbyr bruk i kommersiell aktivitet.

Begge gir (etikett, start, stopp) med etikettene `speech`, `music` og `other`. Bare inaVAMOS har en klasse for tale over
musikk (`speech+music`); med inaSpeechSegmenter produseres den aldri, og flagget «musikk under tale – vurder rettigheter»
faller da bort (KLAR-ADR-0019).

Tidslinjen får en disposisjon per segment. Disposisjonen er et forslag til en menneskelig
vurdering, ikke en avgjørelse:

  speech        -> «transkriber»
  speech+music  -> «transkriber», med flagget «musikk under tale – vurder rettigheter» (bare inaVAMOS)
  music         -> «foreslått klipp»   (aldri til Whisper)
  other         -> «ingen handling»    (aldri til Whisper)

Kort støy midt i tale gir ellers mange bittesmå segmenter. Tale-segmenter (speech og
speech+music) som bare er skilt av `other` med samlet varighet på høyst `bro_s` slås derfor
sammen. Et gap som inneholder ren musikk broes aldri. Et sammenslått segment beholder
tidsintervallene der musikk lå under talen (`musikk_under_tale`). Tale kortere enn `min_s`
blir ikke transkribert, men sendt til menneskelig vurdering.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

TRANSKRIBER = "transkriber"
FORESLATT_KLIPP = "foreslått klipp"
MENNESKELIG_VURDERING = "menneskelig vurdering"
INGEN_HANDLING = "ingen handling"

FLAGG_MUSIKK_UNDER_TALE = "musikk under tale – vurder rettigheter"

TALE_ETIKETTER = {"speech", "speech+music"}
ALDRI_TIL_WHISPER = {"music", "other"}
_DISPOSISJON = {
    "speech": TRANSKRIBER,
    "speech+music": TRANSKRIBER,
    "music": FORESLATT_KLIPP,
    "other": INGEN_HANDLING,
}
_BROBARE = {"other"}


@dataclass
class Segment:
    label: str
    start: float
    stop: float
    disposisjon: str = ""
    merknad: str = ""
    flagg: list[str] = field(default_factory=list)
    musikk_under_tale: list[tuple[float, float]] = field(default_factory=list)

    @property
    def varighet(self) -> float:
        return self.stop - self.start


MILJOVARIABEL = "ARKIVKLARERING_SEGMENTERING"
STANDARD_SEGMENTERING = "inaseg"
SEGMENTERINGER = ("inaseg", "inavamos")

INAVAMOS_MANGLER = (
    "ARKIVKLARERING_SEGMENTERING=inavamos er valgt, men inaVAMOS er ikke installert. inaVAMOS er et valgfritt tillegg, bare for å "
    "reprodusere de preregistrerte kjøringene H1 og H2 (KLAR-ADR-0019 v1.1). Installer tillegget med\n"
    "    source scripts/miljo.sh && VIRTUAL_ENV=$PWD/.venv uv pip install -e '.[reproduksjon-h1h2]'\n"
    "Lisens: inaVAMOS har Pantagruel Research-only License og kan bare brukes til forskning; art. 3 forbyr bruk i kommersiell "
    "aktivitet. Standard segmentering er inaSpeechSegmenter (fjern miljøvariabelen eller sett ARKIVKLARERING_SEGMENTERING=inaseg)."
)


class SegmenteringFeil(RuntimeError):
    """Ukjent verdi i ARKIVKLARERING_SEGMENTERING, eller inaVAMOS valgt uten at tillegget er installert."""


def valgt_segmentering() -> str:
    """Segmentøren som er valgt med ARKIVKLARERING_SEGMENTERING: «inaseg» (standard; også når variabelen mangler eller er tom)
    eller «inavamos». Andre verdier gir SegmenteringFeil."""
    verdi = os.environ.get(MILJOVARIABEL, "").strip()
    if not verdi:
        return STANDARD_SEGMENTERING
    if verdi not in SEGMENTERINGER:
        raise SegmenteringFeil(f"ukjent verdi {MILJOVARIABEL}={verdi!r}; gyldige verdier er «inaseg» (standard, inaSpeechSegmenter) "
                               "og «inavamos» (valgfritt tillegg reproduksjon-h1h2, bare for å reprodusere H1 og H2; KLAR-ADR-0019)")
    return verdi


_SEGMENTERER: dict = {}


def segmenter(lydfil, enhet: str = "cpu") -> list[tuple[str, float, float]]:
    """Segmenterer hele fila og returnerer (etikett, start, stopp), med segmentøren valgt i ARKIVKLARERING_SEGMENTERING.

    Standard er inaSpeechSegmenter (`segment_inaseg.segmenter`, eget venv; `enhet` brukes ikke, TensorFlow på CPU). Med
    «inavamos» kjøres inaVAMOS på torch-enheten `enhet` (modellene, ca. 80 MB, lastes ned fra Hugging Face første gang og ligger
    i cache etter det). inaVAMOS importeres bare da; mangler tillegget, gis en feilmelding med installasjon og lisens.
    """
    if valgt_segmentering() == "inaseg":  # KLAR-ADR-0019 v1.1: standard
        from . import segment_inaseg

        return segment_inaseg.segmenter(lydfil, enhet)
    try:
        from inavamos import Segmenter  # bare når «inavamos» er valgt; importeres sent: torch er tungt
    except ImportError as e:
        if getattr(e, "name", None) not in (None, "inavamos"):
            raise  # inaVAMOS finnes, men en av avhengighetene mangler: vis den ekte feilen
        raise SegmenteringFeil(INAVAMOS_MANGLER) from e

    if enhet not in _SEGMENTERER:  # modellene lastes én gang per prosess
        _SEGMENTERER[enhet] = Segmenter(device=enhet)
    seg = _SEGMENTERER[enhet]
    return [(str(l), float(a), float(b)) for l, a, b in seg(str(lydfil))]


def bygg_tidslinje(raa, bro_s: float = 1.0, min_s: float = 0.5) -> list[Segment]:
    """Gjør segmentørens utdata (etikett, start, stopp) om til en tidslinje med disposisjon, og slår sammen tale over korte gap.

    Leverandørnøytral: tar utdata fra `segmenter` uansett segmentør. `speech+music` (og dermed flagget «musikk under tale») finnes
    bare i utdata fra inaVAMOS; inaSpeechSegmenter gir bare speech, music og other (KLAR-ADR-0019)."""
    deler = [Segment(l, a, b) for l, a, b in raa]
    tale = [i for i, s in enumerate(deler) if s.label in TALE_ETIKETTER]
    grupper: list[list[int]] = []
    for i in tale:
        if grupper:
            forrige = grupper[-1][-1]
            gap = deler[forrige + 1:i]
            if (not gap or all(g.label in _BROBARE for g in gap)) and sum(g.varighet for g in gap) <= bro_s:
                grupper[-1].append(i)
                continue
        grupper.append([i])
    ut: list[Segment] = []
    i = 0
    start_av = {g[0]: g for g in grupper}
    while i < len(deler):
        if i in start_av:
            g = start_av[i]
            medlemmer = [deler[k] for k in g]
            mus = [(m.start, m.stop) for m in medlemmer if m.label == "speech+music"]
            s = Segment("speech+music" if mus else "speech", deler[g[0]].start, deler[g[-1]].stop,
                        musikk_under_tale=mus)
            if mus:
                s.flagg.append(FLAGG_MUSIKK_UNDER_TALE)
            if len(g) > 1:
                s.merknad = f"slått sammen av {len(g)} tale-segmenter (gap ≤ {bro_s} s)"
            if s.varighet < min_s:
                s.disposisjon = MENNESKELIG_VURDERING
                s.merknad = (s.merknad + "; " if s.merknad else "") + f"tale kortere enn {min_s} s, ikke transkribert"
            else:
                s.disposisjon = TRANSKRIBER
            ut.append(s)
            i = g[-1] + 1
        else:
            s = deler[i]
            s.disposisjon = _DISPOSISJON.get(s.label, MENNESKELIG_VURDERING)
            if s.label not in _DISPOSISJON:
                s.merknad = f"ukjent etikett «{s.label}»"
            ut.append(s)
            i += 1
    return ut
