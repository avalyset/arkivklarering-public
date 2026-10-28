"""Kommandolinje: lydfil inn; WebVTT per lag, segments.json (med personvernflagg), OHMS XML, IIIF-manifest og MMIF ut.

    arkivklarering lyd/rokytest.wav -o ut/
    python -m arkivklarering.cli lyd/rokytest.wav -o ut/

Kjører segmentering og deretter to transkripsjonslag (ra, normalisert), ett pass om gangen (16 GB RAM).
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import time

from . import eksport, katalog, segment, segment_inaseg, transkriber


def _varighet(lyd, tidslinje) -> float:
    """Lydens varighet i sekunder (ffprobe), ellers slutten av siste segment."""
    import subprocess

    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(lyd)],
                           capture_output=True, text=True, timeout=60)
        return float(r.stdout.strip())
    except (ValueError, OSError, subprocess.SubprocessError):
        return max((s.stop for s in tidslinje), default=0.0)


def main(argv=None) -> int:
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()  # avbryter hvis cacher og tmp ikke ligger under ARKIVKLARERING_DATA
    ap = argparse.ArgumentParser(prog="arkivklarering", description=__doc__.splitlines()[0])
    ap.add_argument("lydfil")
    ap.add_argument("-o", "--ut", default="ut", help="utkatalog (standard: ut/)")
    ap.add_argument("--sprak", default="nn", help="whisper-språk for begge lag (standard: nn)")
    ap.add_argument("--enhet", default="cpu", help="torch-enhet; gjelder bare ARKIVKLARERING_SEGMENTERING=inavamos (valgfritt tillegg reproduksjon-h1h2). Standard segmentering (inaSpeechSegmenter) kjører på CPU og bruker den ikke (standard: cpu)")
    ap.add_argument("--bro-s", type=float, default=1.0, help="slå sammen tale over gap på høyst så mange s")
    ap.add_argument("--min-s", type=float, default=0.5, help="tale kortere enn dette transkriberes ikke")
    ap.add_argument("--whisper", help="sti til whisper-cli")
    ap.add_argument("--modell-ra", help="ggml for rålaget (verbatim)")
    ap.add_argument("--modell-normalisert", help="ggml for normalisert lag")
    ap.add_argument("--ingen-personvern", action="store_true", help="hopp over personvernflagg")
    ap.add_argument("--taler", action="store_true", help="talerinndeling med pyannote (TALER_1, TALER_2 …; krever HF_TOKEN og venv-diarisering, KLAR-ADR-0016)")
    ap.add_argument("--ingen-katalog", action="store_true", help="hopp over katalogutkastet (lokal ollama)")
    ap.add_argument("--katalogmodell", default=katalog.STANDARD_MODELL, help="ollama-modell for katalogutkastet (KLAR-ADR-0013)")
    ap.add_argument("--ingen-ordtider", action="store_true", help="ikke be om DTW-ordtidsstempler (-nfa -dtw large.v3 -ojf); cuene får da whisper.cpps segmenttider, og union parer på cuenes tidsrom")
    a = ap.parse_args(argv)

    lyd = pathlib.Path(a.lydfil)
    if not lyd.is_file():
        print(f"Fant ikke {lyd}", file=sys.stderr)
        return 2
    try:
        segmentor = segment.valgt_segmentering()  # ARKIVKLARERING_SEGMENTERING: inaseg (standard) eller inavamos (KLAR-ADR-0019)
    except segment.SegmenteringFeil as e:
        print(f"Oppsett: {e}", file=sys.stderr)
        return 2
    try:
        oppsett = {lag: transkriber.finn_oppsett(lag, a.whisper, m, a.sprak)
                   for lag, m in (("ra", a.modell_ra), ("normalisert", a.modell_normalisert))}
    except transkriber.OppsettFeil as e:
        print(f"Oppsett: {e}", file=sys.stderr)
        return 2
    for lag, o in oppsett.items():
        print(f"{lag}: {pathlib.Path(o.modell).name} sha256={o.sha256}", file=sys.stderr)

    ut = pathlib.Path(a.ut)
    ut.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    try:
        raa = segment.segmenter(lyd, a.enhet)
    except (segment.SegmenteringFeil, segment_inaseg.InasegFeil) as e:  # inavamos uten tillegget, eller venv-inaseg mangler
        print(f"Oppsett: {e}", file=sys.stderr)
        return 2
    tidslinje = segment.bygg_tidslinje(raa, a.bro_s, a.min_s)
    print(f"segmentering ({segmentor}): {len(raa)} råsegmenter -> {len(tidslinje)} ({time.time() - t0:.1f} s)", file=sys.stderr)

    cues = {}
    for lag in transkriber.LAG:  # ett pass om gangen
        t1 = time.time()
        cues[lag] = transkriber.transkriber(lyd, tidslinje, oppsett[lag], ordtider=not a.ingen_ordtider)
        print(f"{lag}: {len(cues[lag])} cuer ({time.time() - t1:.1f} s)", file=sys.stderr)
        if not a.taler:
            print(eksport.skriv_vtt(cues[lag], ut / f"{lyd.stem}.{lag}.vtt", lag))
    taler = taler_info = None
    if a.taler:  # én pyannote-kjøring, etter Whisper (én tung prosess om gangen)
        from . import diarisering
        t4 = time.time()
        turer = diarisering.kjor(lyd, a.enhet)
        taler = {lag: diarisering.tildel_cuer(cues[lag], turer) for lag in cues}
        taler_info = {"modell": diarisering.MODELL, "merknad": diarisering.MERKNAD, "antall_talere": len({t.taler for t in turer}),
                      "turer": [{"start": round(t.start, 3), "stopp": round(t.stopp, 3), "taler": t.taler} for t in turer]}
        print(f"talerinndeling: {taler_info['antall_talere']} talere, {len(turer)} turer ({time.time() - t4:.1f} s)", file=sys.stderr)
        for lag in cues:
            print(eksport.skriv_vtt(cues[lag], ut / f"{lyd.stem}.{lag}.vtt", lag, taler=taler[lag]))
    flagg = None
    if not a.ingen_personvern:
        from . import personvern  # laster spaCy og NB-BERT; importeres bare når flagg skal lages
        t2 = time.time()
        motor = personvern.lag_motor()
        sprak = "nn" if a.sprak == "nn" else "nb"
        flagg = {lag: personvern.flagg_cues(cues[lag], lag, sprak, motor) for lag in transkriber.LAG}
        union = personvern.slaa_sammen_lag(flagg)
        print("personvern: " + ", ".join(f"{lag} {len(f)} flagg" for lag, f in flagg.items()) +
              f"; union {len(union)} flagg ({time.time() - t2:.1f} s)", file=sys.stderr)
    else:
        union = None
    print(eksport.skriv_segments_json(tidslinje, cues, ut / f"{lyd.stem}.segments.json", lyd, oppsett, flagg, union, taler, taler_info))

    # katalogutkast (lokal ollama) og de øvrige eksportformatene; alt er utkast, ikke klarering
    varighet = _varighet(lyd, tidslinje)
    post = katalog.Katalogpost(tittel="(uten tittel) – utkast", modell="", segmenter=[])
    if not a.ingen_katalog:
        try:
            t3 = time.time()
            post = katalog.lag_katalogpost(cues["normalisert"], union or [], a.katalogmodell)
            print(f"katalog: {len(post.segmenter)} segmentsammendrag, {len(post.forkastet)} forkastede forslag ({time.time() - t3:.1f} s)", file=sys.stderr)
        except Exception as e:  # noqa: BLE001  ollama kjører ikke, modellen mangler osv.: eksporten gjøres uten katalogtekst
            print(f"katalog: hoppet over ({type(e).__name__}: {e})", file=sys.stderr)
    pd = post.som_dict()
    print(eksport.skriv_ohms_xml(ut / f"{lyd.stem}.ohms.xml", pd, cues["normalisert"], lyd, varighet, "nno" if a.sprak == "nn" else "nob", taler=taler["normalisert"] if taler else None))
    print(eksport.skriv_iiif_manifest(ut / f"{lyd.stem}.iiif.json", pd, cues, {lag: f"{lyd.stem}.{lag}.vtt" for lag in cues},
                                      f"file:///{lyd.name}", varighet, sprak="nn" if a.sprak == "nn" else "no"))
    print(eksport.skriv_mmif(ut / f"{lyd.stem}.mmif.json", str(lyd), tidslinje, cues, None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
