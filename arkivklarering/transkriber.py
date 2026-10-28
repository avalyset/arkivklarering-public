"""Transkripsjon med NB-Whisper via whisper.cpp, to lag, kun på tale-segmenter.

Whisper får aldri `music` eller `other`: der er det ikke tale å transkribere, og utdata kan forveksles med
innhold (begrunnelse i KLAR-ADR-0004 v1.1; Koenecke m.fl. 2024 gjelder pauser i tale). Måling: docs/KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v1.1_2026-10-26.md. Segmenter med
`speech` og `speech+music` transkriberes; `speech+music` får i tillegg flagget
«musikk under tale – vurder rettigheter» (se segment.py).

To lag, hvert som eget pass over de samme segmentene (én whisper-cli-prosess om gangen):
  ra          NB-Whisper large VERBATIM (NbAiLab/nb-whisper-large-verbatim)
  normalisert NB-Whisper large, ikke verbatim (NbAiLab/nb-whisper-large)
Begge med `-l nn` som standard.

Modellfilene ligger utenfor repoet (modeller.lock.json har forventet sha256 og standardsti, relativt til ARKIVKLARERING_DATA).
sha256 sjekkes før kjøring; avvik stopper. Modeller lastes ikke ned av koden.

whisper-cli: --whisper, ARKIVKLARERING_WHISPER, `whisper-cli` på PATH eller ~/whisper.cpp/build/bin/whisper-cli.
Modell: --modell-ra/--modell-normalisert eller ARKIVKLARERING_MODELL_RA/_NORMALISERT.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field

from .miljo import DATA
from .segment import ALDRI_TIL_WHISPER, TRANSKRIBER, Segment

LAG = ("ra", "normalisert")
LOCK = pathlib.Path(__file__).resolve().parent.parent / "modeller.lock.json"
TIDSGRENSE_S = 1800
# Whisper skriver av og til lydmerker som «[MUSIC]» eller «(musikk)» i stedet for tekst.
# whisper.cpp skriver også spesialtokens som «<|nocaptions|>» når modellen ikke finner tale.
_LYDMERKE = re.compile(r"<\|[^|<>]*\|>|[\[\(]\s*(musikk|music|applaus|applause|latter|laughter|støy|noise|stillhet|silence|lyd)\s*[\]\)]",
                       re.IGNORECASE)


class OppsettFeil(RuntimeError):
    pass


class Avbrutt(RuntimeError):
    """Whisper-prosessen ble drept av en ressursvakt (lite disk, mye swap). Kjøringen kan tas opp igjen senere."""


def kjor_prosess(argv, timeout, vakt=None):
    """subprocess.run med valgfri vakt. `vakt()` kalles hvert 3. sekund og returnerer en årsak (tekst) når prosessen skal
    avbrytes, ellers None. Da drepes prosessen og `Avbrutt(årsak)` reises."""
    if vakt is None:
        return subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    start = time.time()
    while True:
        try:
            ut, feil = p.communicate(timeout=3)
            return subprocess.CompletedProcess(argv, p.returncode, ut, feil)
        except subprocess.TimeoutExpired:
            grunn = vakt()
            if grunn:
                p.kill()
                p.communicate()
                raise Avbrutt(grunn)
            if time.time() - start > timeout:
                p.kill()
                p.communicate()
                raise


@dataclass
class Oppsett:
    lag: str
    whisper_cli: str
    modell: str
    sha256: str
    sprak: str = "nn"
    uten_tidsstempeltokens: bool = False  # whisper-cli -nt; settes av finn_oppsett (rålaget), se KLAR-ADR-0017 og KLAR-EVAL-0011


@dataclass
class Cue:
    start: float
    stop: float
    tekst: str
    # ordtidsstempler: (tegn_start, tegn_slutt, tid_start, tid_slutt) per ord, tegnposisjoner i `tekst`
    ord: list = field(default_factory=list)

    def ord_tidsrom(self, a: int, b: int):
        """Tidsrommet (start, slutt) for ordene som overlapper tegnspennet [a, b), eller None uten ordtidsstempler."""
        treff = [(t0, t1) for ca, cb, t0, t1 in self.ord if ca < b and a < cb]
        return (min(t[0] for t in treff), max(t[1] for t in treff)) if treff else None


def sha256_fil(sti, blokk=1 << 24) -> str:
    h = hashlib.sha256()
    with open(sti, "rb") as f:
        while b := f.read(blokk):
            h.update(b)
    return h.hexdigest()


def finn_whisper(whisper=None) -> str:
    cli = whisper or os.environ.get("ARKIVKLARERING_WHISPER") or shutil.which("whisper-cli")
    if not cli:
        kandidat = pathlib.Path.home() / "whisper.cpp/build/bin/whisper-cli"
        cli = str(kandidat) if kandidat.exists() else None
    if not cli or not (shutil.which(cli) or pathlib.Path(cli).exists()):
        raise OppsettFeil("Fant ikke whisper-cli. Sett --whisper eller ARKIVKLARERING_WHISPER.")
    return cli


def standard_modellsti(lag: str, rot=None) -> pathlib.Path:
    """Standardstien til modellfila for laget: `standardsti` i modeller.lock.json, relativt til datarota (ARKIVKLARERING_DATA)."""
    sti = pathlib.Path(json.loads(LOCK.read_text(encoding="utf-8"))[lag]["standardsti"])
    return sti if sti.is_absolute() else pathlib.Path(rot or DATA) / sti


def finn_oppsett(lag: str, whisper=None, modell=None, sprak="nn", verifiser=True, uten_tidsstempeltokens: bool | None = None) -> Oppsett:
    """Finner whisper-cli og modellfila for laget og sjekker sha256 mot modeller.lock.json.

    `uten_tidsstempeltokens` (whisper-cli `-nt`): standard er på for rålaget og av for det normaliserte laget (KLAR-ADR-0017). Rålaget
    mister ellers teksten når verbatim-modellen avslutter et vindu med EOT uten avsluttende tidsstempeltoken (KLAR-EVAL-0011).
    Miljøvariabelen ARKIVKLARERING_MED_TIDSSTEMPELTOKENS=1 slår `-nt` av for alle lag, så tallene «før -nt» kan gjenskapes."""
    if lag not in LAG:
        raise OppsettFeil(f"Ukjent lag «{lag}». Gyldige: {', '.join(LAG)}")
    lock = json.loads(LOCK.read_text(encoding="utf-8"))[lag]
    m = modell or os.environ.get(f"ARKIVKLARERING_MODELL_{lag.upper()}") or str(standard_modellsti(lag))
    if not pathlib.Path(m).is_file():
        raise OppsettFeil(f"Fant ikke modellfila for laget «{lag}»: {m}. Standardstien er ARKIVKLARERING_DATA/{lock['standardsti']} "
                          f"(Vault må være montert hvis roten ligger der). Fila er {lock['repo']}/{lock['fil']}; den lastes ikke ned av koden.")
    sha = sha256_fil(m) if verifiser else ""
    if verifiser and sha != lock["sha256"]:
        raise OppsettFeil(f"sha256 for {m} er {sha}, forventet {lock['sha256']}. Stopper.")
    if uten_tidsstempeltokens is None:
        uten_tidsstempeltokens = lag == "ra" and os.environ.get("ARKIVKLARERING_MED_TIDSSTEMPELTOKENS") != "1"
    return Oppsett(lag, finn_whisper(whisper), str(m), sha, sprak, uten_tidsstempeltokens)


def _kutt(lydfil, start, stop, wav):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{stop - start:.3f}",
                    "-i", str(lydfil), "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(wav)],
                   check=True, timeout=TIDSGRENSE_S)


def whisper_direkte(wav, base, o: Oppsett, ordtider: bool = False):
    """Kjører whisper-cli på en wav-fil og returnerer JSON. Brukes av transkriber_segment og av
    målingen av oppdiktet tekst (som bevisst går utenom segmentregelen).

    ordtider: DTW-tidsstempler på tokennivå (`-nfa -dtw large.v3 -ojf`; flash-attention må være av). `--dtw`-forhåndsvalget
    `large.v3` er valgt fordi NB-Whisper large har samme arkitektur som whisper-large-v3 (128 mel-bånd, 32 dekoderlag).
    `-ml 1 -sow` (ord-for-ord via token-tidsstempler) ble forkastet: for verbatim-modellen klumpet sene ord seg i
    segmentets slutt (alle ord etter de første fikk tidskoden til segmentslutten)."""
    ekstra = ["-nfa", "-dtw", "large.v3", "-ojf"] if ordtider else []
    if o.uten_tidsstempeltokens:
        ekstra = ekstra + ["-nt"]
    r = subprocess.run([o.whisper_cli, "-l", o.sprak, "-m", o.modell, "-f", str(wav),
                        "-oj", "-of", str(base), "-np", *ekstra],
                       capture_output=True, text=True, timeout=TIDSGRENSE_S)
    if r.returncode != 0:
        raise RuntimeError(f"whisper-cli feilet ({r.returncode}): {r.stderr[-500:]}")
    return json.loads(pathlib.Path(f"{base}.json").read_text(encoding="utf-8"))


def whisper_flere(wavs, o: Oppsett, ordtider: bool = False, logg=None, vakt=None):
    """Én whisper-cli-prosess på flere wav-filer (modellen lastes én gang). Utdata skrives ved siden av hver fil
    (`<fil>.json`). NB: gjentatte kjøringer i samme prosess er ikke bitidentiske med én prosess per fil (funn i
    norsk-tale), så dette brukes bare i DEV-målinger der kjøretid veier tyngre enn bitvis gjenskaping.

    whisper-cli krasjer av og til (SIGABRT) med DTW på verbatim-modellen, uten feilmelding. Da deles gruppen i to og kjøres
    på nytt (halvering) til den krasjende filen er isolert; den kjøres så uten DTW (tekst uten ordtidsstempler, merket
    `uten_dtw`). Krasjer den også uten DTW, får den tomt resultat med feltet `feil`. Ingen fil droppes stille.
    `vakt` (se kjor_prosess) kan avbryte kjøringen med `Avbrutt`; den er ikke en krasj og fører ikke til halvering."""
    ekstra = ["-nfa", "-dtw", "large.v3", "-ojf"] if ordtider else []
    nt = ["-nt"] if o.uten_tidsstempeltokens else []  # også i reservekjøringen uten DTW

    def kjor(filer, med_dtw=True):
        argv = [o.whisper_cli, "-l", o.sprak, "-m", o.modell, "-oj", "-np", *(ekstra if med_dtw else []), *nt]
        for w in filer:
            argv += ["-f", str(w)]
        for w in filer:
            pathlib.Path(f"{w}.json").unlink(missing_ok=True)
        return kjor_prosess(argv, TIDSGRENSE_S * 4, vakt)

    def les(w):
        return json.loads(pathlib.Path(f"{w}.json").read_text(encoding="utf-8"))

    def gruppe(filer):
        r = kjor(filer)
        if r.returncode == 0 and all(pathlib.Path(f"{w}.json").exists() for w in filer):
            return [les(w) for w in filer]
        if len(filer) > 1:
            if logg:
                logg(f"  whisper-cli krasjet ({r.returncode}) på {len(filer)} filer; halverer")
            m = len(filer) // 2
            return gruppe(filer[:m]) + gruppe(filer[m:])
        w = filer[0]
        if ordtider:
            r2 = kjor([w], med_dtw=False)
            if r2.returncode == 0 and pathlib.Path(f"{w}.json").exists():
                if logg:
                    logg(f"  {pathlib.Path(w).name} krasjer med DTW; kjørt uten DTW (ingen ordtidsstempler)")
                ut = les(w)
                ut["uten_dtw"] = True
                return [ut]
        if logg:
            logg(f"  FEIL: {pathlib.Path(w).name} krasjet også uten DTW ({r.returncode})")
        return [{"transcription": [], "feil": f"whisper-cli {r.returncode}"}]

    return gruppe(list(wavs))


def er_lydmerke(tekst: str) -> bool:
    """Sant når cuen bare består av et lydmerke eller symboler (♪, *) uten ord."""
    rest = _LYDMERKE.sub("", tekst)
    return not re.search(r"\w", rest)


MAKS_PAUSE_S = 0.7   # ny cue ved pause mellom ord på minst så lenge
MAKS_CUE_S = 8.0     # eller når cuen har vart så lenge
_SPESIAL = re.compile(r"<\|[^|<>]*\|>")


def _ord_fra_dtw(segmenter, seg: Segment):
    """Ord med (tekst, start, slutt) fra whisper.cpps JSON med `t_dtw` per token. Et token som begynner med mellomrom
    starter et nytt ord; ren tegnsetting festes til ordet foran. Ordets slutt er neste ords start."""
    ord_ = []  # [tekst, start, slutt|None]
    nytt_ord = False  # et eget mellomromstoken (« ») foran tall som «19»+«17» betyr at neste token starter et ord
    for sg in segmenter:
        for t in sg.get("tokens", []):
            tekst = t["text"]
            if tekst.startswith("[_") or _SPESIAL.search(tekst):
                continue
            if not tekst.strip():
                nytt_ord = True
                continue
            tid = t.get("t_dtw", -1)
            start = (tid / 100 if tid is not None and tid >= 0 else t["offsets"]["from"] / 1000)
            if ord_ and not tekst.startswith(" ") and not nytt_ord:  # fortsettelse av ordet foran (delt i flere tokens)
                ord_[-1][0] += tekst
            elif ord_ and not re.search(r"\w", tekst):  # ren tegnsetting: festes til ordet foran
                ord_[-1][0] += tekst.strip()
            else:
                ord_.append([" " + tekst.strip(), start, None])
            nytt_ord = False
    ut, forrige = [], seg.start
    for k, w in enumerate(ord_):
        a = min(max(seg.start + w[1], forrige), seg.stop)  # ikke-avtagende og innenfor segmentet
        ut.append([w[0], a, None])
        forrige = a
    for k, w in enumerate(ut):
        neste = ut[k + 1][1] if k + 1 < len(ut) else min(seg.stop, w[1] + 1.5)
        w[2] = min(max(neste, w[1]), seg.stop)
    return [(w[0], w[1], w[2]) for w in ut]


def _ord_til_cuer(segmenter, seg: Segment) -> list[Cue]:
    """Slår ord med tidsstempler sammen til cuer (ny cue ved pause, setningsslutt eller lang cue)."""
    ord_ = _ord_fra_dtw(segmenter, seg)
    cuer, gjeldende = [], []
    for k, (tekst, a, b) in enumerate(ord_):
        if gjeldende and (a - gjeldende[-1][2] >= MAKS_PAUSE_S or a - gjeldende[0][1] >= MAKS_CUE_S
                          or gjeldende[-1][0].rstrip()[-1:] in ".!?"):
            cuer.append(gjeldende)
            gjeldende = []
        gjeldende.append((tekst, a, b))
    if gjeldende:
        cuer.append(gjeldende)
    ut = []
    for gruppe in cuer:
        tekst, ord_info = "", []
        for w, a, b in gruppe:
            ord_tekst = w.strip()
            if tekst:
                tekst += " "
            ord_info.append((len(tekst), len(tekst) + len(ord_tekst), a, b))
            tekst += ord_tekst
        if er_lydmerke(tekst):
            continue
        ut.append(Cue(gruppe[0][1], gruppe[-1][2], tekst, ord_info))
    return ut


def sjekk_segment(seg: Segment):
    if seg.label in ALDRI_TIL_WHISPER or seg.disposisjon != TRANSKRIBER:
        raise ValueError(f"Segment {seg.label} {seg.start:.2f}–{seg.stop:.2f} skal ikke til Whisper")


def transkriber_segment(lydfil, seg: Segment, o: Oppsett, tmp, ordtider: bool = False) -> list[Cue]:
    sjekk_segment(seg)
    tmp = pathlib.Path(tmp)
    wav = tmp / "segment.wav"
    _kutt(lydfil, seg.start, seg.stop, wav)
    ut = whisper_direkte(wav, tmp / "segment", o, ordtider)
    return json_til_cues(ut, seg, ordtider)


def json_til_cues(ut: dict, seg: Segment, ordtider: bool = False) -> list[Cue]:
    """Gjør whisper.cpps JSON for ett segment om til cuer (med ordtidsstempler hvis `ordtider`)."""
    if ordtider:
        return _ord_til_cuer(ut.get("transcription", []), seg)
    cues = []
    for t in ut.get("transcription", []):
        tekst = t["text"].strip()
        if er_lydmerke(tekst):
            continue
        # Verbatim-modellen gir ofte én cue som dekker hele 30 s-vinduet til whisper.cpp. Tidskodene
        # begrenses til segmentet, ellers havner cuen utenfor segmentet og i feil tidsrom i VTT.
        a = min(max(seg.start + t["offsets"]["from"] / 1000, seg.start), seg.stop)
        b = min(max(seg.start + t["offsets"]["to"] / 1000, a), seg.stop)
        cues.append(Cue(a, b, tekst))
    return cues


def transkriber(lydfil, tidslinje: list[Segment], o: Oppsett, ordtider: bool = False) -> list[Cue]:
    """Ett pass: transkriberer bare segmenter med disposisjon «transkriber», ett om gangen.
    Med `ordtider` får cuene ordtidsstempler (`Cue.ord`) og grupperes etter pauser og setningsslutt."""
    cues: list[Cue] = []
    with tempfile.TemporaryDirectory(prefix="arkivklarering-") as tmp:
        for seg in tidslinje:
            if seg.disposisjon == TRANSKRIBER:
                cues.extend(transkriber_segment(lydfil, seg, o, tmp, ordtider))
    return cues
