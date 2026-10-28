"""Delt hjelpekode for DEV-målingene som kjører Whisper: ressurssjekk (minnevakt) og kjøring av hele rørledningen på en lydfil."""
import json
import os
import pathlib
import subprocess
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))
from arkivklarering import miljo, segment, transkriber  # noqa: E402

MIN_LEDIG_PROSENT = 38  # 38 % av 16 GB er ca. 6 GB
ANNEN_VAKT = "src/f0/vakt.sh"  # det andre sporets minnevakt (SES-S1)
DISK_MIN_GIB = 8        # Whisper avbrytes/venter hvis df -h / viser under så mye ledig
SWAP_MAKS_MB = 6656     # ... eller hvis swap er over 6,5 GB brukt
MAKS_VENTETID_S = 3 * 3600  # ventet så lenge sammenhengende: feil ut i stedet for å henge uten at noen ser det


def grunn_for(disk_ledig_gib, swap_brukt_mb, ledig_prosent_=None, annen_vakt=False, bare_kjoring=False):
    """Årsaken til at Whisper ikke skal kjøre (eller avbrytes), eller None. `bare_kjoring` hopper over minne- og
    vaktkravene som bare gjelder før start."""
    if disk_ledig_gib < DISK_MIN_GIB:
        return f"intern disk: {disk_ledig_gib:.1f} GiB ledig (< {DISK_MIN_GIB})"
    if swap_brukt_mb > SWAP_MAKS_MB:
        return f"swap: {swap_brukt_mb:.0f} MB brukt (> {SWAP_MAKS_MB})"
    if not bare_kjoring:
        if annen_vakt:
            return "det andre sporets minnevakt er aktiv"
        if ledig_prosent_ is not None and ledig_prosent_ < MIN_LEDIG_PROSENT:
            return f"ledig minne {ledig_prosent_} % (< {MIN_LEDIG_PROSENT})"
    return None


def disk_ledig_gib() -> float:
    import shutil
    return shutil.disk_usage("/").free / 2**30


def swap_brukt_mb() -> float:
    ut = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout
    for del_ in ut.replace("=", " ").split():
        pass
    tokens = ut.replace("=", " ").split()
    return float(tokens[tokens.index("used") + 1].rstrip("M"))


def ledig_prosent() -> int:
    ut = subprocess.run(["memory_pressure", "-Q"], capture_output=True, text=True).stdout
    for linje in ut.splitlines():
        if "free percentage" in linje:
            return int(linje.split(":")[1].strip().rstrip("%"))
    return 0


def vakt_under_kjoring():
    """Kalles av whisper_flere mens Whisper kjører: avbryter ved lite disk eller mye swap."""
    return grunn_for(disk_ledig_gib(), swap_brukt_mb(), bare_kjoring=True)


def vent_pa_ressurser(logg=print):
    """Venter til Whisper kan kjøre: ledig minne minst 6 GB, det andre sporets minnevakt ikke aktiv, minst 8 GiB ledig på
    den interne disken og swap høyst 6,5 GB brukt. Én Whisper-kjøring om gangen. Gir opp (RuntimeError) etter 3 t venting."""
    ventet = 0
    while True:
        vakt = subprocess.run(["pgrep", "-f", ANNEN_VAKT], capture_output=True).returncode == 0
        grunn = grunn_for(disk_ledig_gib(), swap_brukt_mb(), ledig_prosent(), vakt)
        if grunn is None:
            if ventet:
                logg(f"  ressurser frie igjen etter {ventet} s")
            return
        if ventet % 300 == 0:
            logg(f"  venter: {grunn}")
        if ventet >= MAKS_VENTETID_S:
            raise RuntimeError(f"ressursvakten har ventet i {ventet} s: {grunn}")
        time.sleep(30)
        ventet += 30


def cue_til_dict(c):
    return {"start": c.start, "stop": c.stop, "tekst": c.tekst, "ord": [list(o) for o in c.ord]}


def dict_til_cue(d):
    return transkriber.Cue(d["start"], d["stop"], d["tekst"], [tuple(o) for o in d["ord"]])


def kjor_rorledning(lyd, oppsett_per_lag, ordtider=True):
    """Segmentering og ett Whisper-pass per lag (rålag, normalisert lag), ett om gangen. Returnerer en dict som kan lagres.

    Segmentøren er `segment.segmenter`: inaSpeechSegmenter som standard, inaVAMOS med ARKIVKLARERING_SEGMENTERING=inavamos (tillegget
    reproduksjon-h1h2; KLAR-ADR-0019 v1.1). DEV-resultatene og cachene fra før 27.10.2026 er laget med inaVAMOS: reproduksjon av dem
    (scripts/verifiser_uendret.py, scripts/reproduser.sh, H1/H2 i scripts/kjor_testdel.sh) setter inavamos eksplisitt."""
    tl = segment.bygg_tidslinje(segment.segmenter(lyd))
    ut = {"tidslinje": [{"label": s.label, "start": round(s.start, 3), "stopp": round(s.stop, 3), "disposisjon": s.disposisjon,
                         "flagg": s.flagg} for s in tl], "cues": {}}
    for lag, o in oppsett_per_lag.items():
        vent_pa_ressurser()
        ut["cues"][lag] = [cue_til_dict(c) for c in transkriber.transkriber(lyd, tl, o, ordtider=ordtider)]
    return ut


def kjor_batch(items, oppsett_per_lag, ordtider=True, logg=print, gjenbruk=None):
    """Som kjor_rorledning (samme segmentørvalg), men for en gruppe segmenter: segmentering per fil, så ett Whisper-kall per lag og språk med alle
    talesegmentene (modellen lastes én gang). items: [{id, lyd, whisper_sprak}]. Returnerer {id: {tidslinje, cues}}.

    `gjenbruk`: valgfri {id: lagret record} (se `gjenbruk_normalisert`). Det normaliserte lagets cuer tas da fra den lagrede recorden i stedet
    for å kjøre Whisper på nytt; bare rålaget kjøres. Brukes etter innføringen av `-nt` for rålaget (KLAR-ADR-0017), der det normaliserte
    lagets modell og parametere er uendret."""
    import dataclasses
    import tempfile

    tl = {it["id"]: segment.bygg_tidslinje(segment.segmenter(it["lyd"])) for it in items}
    ut = {it["id"]: {"id": it["id"], "tidslinje": [{"label": s.label, "start": round(s.start, 3), "stopp": round(s.stop, 3),
                                                  "disposisjon": s.disposisjon, "flagg": s.flagg} for s in tl[it["id"]]],
                     "cues": {lag: [] for lag in oppsett_per_lag}} for it in items}
    with tempfile.TemporaryDirectory(prefix="batch-", dir=None) as tmp:
        tmp = pathlib.Path(tmp)
        jobber = []  # (id, språk, seg, wav)
        for it in items:
            for k, seg in enumerate(tl[it["id"]]):
                if seg.disposisjon != segment.TRANSKRIBER:
                    continue
                transkriber.sjekk_segment(seg)
                wav = tmp / f'{len(jobber):05d}.wav'
                transkriber._kutt(it["lyd"], seg.start, seg.stop, wav)
                jobber.append((it["id"], it["whisper_sprak"], seg, wav))
        gjenbrukt = {i for i in (gjenbruk or {}) if i in ut and (gjenbruk[i].get("cues") or {}).get("normalisert") is not None}
        for lag, o in oppsett_per_lag.items():
            if lag == "normalisert":
                for i in gjenbrukt:
                    ut[i]["cues"]["normalisert"] = list(gjenbruk[i]["cues"]["normalisert"])
                    ut[i]["gjenbrukt"] = ["normalisert"]
            for sprak in sorted({j[1] for j in jobber}):
                gruppe = [j for j in jobber if j[1] == sprak and not (lag == "normalisert" and j[0] in gjenbrukt)]
                if not gruppe:
                    continue
                while True:
                    vent_pa_ressurser(logg)
                    try:
                        jsoner = transkriber.whisper_flere([j[3] for j in gruppe], dataclasses.replace(o, sprak=sprak), ordtider, logg,
                                                           vakt=vakt_under_kjoring)
                        break
                    except transkriber.Avbrutt as e:
                        logg(f"  Whisper avbrutt av ressursvakten ({e}); venter og prøver igjen")
                for (id_, _, seg, _), js in zip(gruppe, jsoner):
                    if js.get("feil"):
                        ut[id_].setdefault("feil", []).append(f"{lag}: {js['feil']}")
                    if js.get("uten_dtw"):
                        ut[id_].setdefault("uten_dtw", []).append(lag)
                    ut[id_]["cues"][lag].extend(cue_til_dict(c) for c in transkriber.json_til_cues(js, seg, ordtider and not js.get("uten_dtw")))
    return ut


def gjenbruk_normalisert(sti, oppsett_norm, logg=print):
    """Lagrede utdata for det normaliserte laget fra en tidligere kjøring (før -nt for rålaget), når modellens sha256 og alle parametere er uendret:
    modellen er den låste (`finn_oppsett` har kontrollert sha256 mot `modeller.lock.json`), laget kjøres uten `-nt` og med de samme
    DTW-argumentene som før. Returnerer {id: record} eller None (miljøvariabelen ARKIVKLARERING_GJENBRUK_NORMALISERT må være «1», og
    den gamle fila må finnes i ARKIVKLARERING_GJENBRUK_MAPPE, standard `EVAL_DATA`). Logger hva som gjenbrukes. Ingen krav om bitidentitet.

    Den gamle fila finnes med samme regel som `cache_sti` for gjeldende segmentering: `<navn>_inaseg.jsonl` med inaseg (aldri en fil uten
    suffiks eller med `_inavamos`), `<navn>_inavamos.jsonl` eller eldre `<navn>.jsonl` med inavamos. Lagrede cuer fra én segmentør brukes
    derfor aldri i en kjøring med den andre."""
    if os.environ.get("ARKIVKLARERING_GJENBRUK_NORMALISERT") != "1":
        return None
    if oppsett_norm.uten_tidsstempeltokens or oppsett_norm.lag != "normalisert":
        raise RuntimeError("gjenbruk er bare gyldig når normalisert lag kjøres uten -nt")
    mappe = pathlib.Path(os.environ.get("ARKIVKLARERING_GJENBRUK_MAPPE") or miljo.EVAL_DATA)
    gammel = cache_sti(mappe, grunnnavn(sti))  # `sti`: denne kjøringens cache (fra cache_sti)
    if not gammel.is_file():
        logg(f"gjenbruk: ingen lagret fil {gammel.name}; normalisert lag kjøres på nytt")
        return None
    rec = les_jsonl(gammel)
    logg(f"gjenbruk: normalisert lag tas fra {gammel.name} ({len(rec)} segmenter); modell sha256 {oppsett_norm.sha256[:12]}… (låst), "
         f"parametere uendret (DTW, uten -nt)")
    return rec


CACHE_SUFFIKS = {s: f"_{s}" for s in segment.SEGMENTERINGER}  # «_inaseg», «_inavamos»


def cache_sti(mappe, navn, segmentering=None) -> pathlib.Path:
    """Stien til en cache som lagrer `tidslinje` (segmenteringen) sammen med Whisper-utdata, for gjeldende segmentering.

    Navnet får suffiks etter segmentøren (`segment.valgt_segmentering()`, eller `segmentering` når den er gitt): `<mappe>/<navn>_inaseg.jsonl`
    eller `<mappe>/<navn>_inavamos.jsonl`, så tidslinjer fra inaSpeechSegmenter og inaVAMOS aldri blandes i samme fil.

    Bakoverkompatibilitet: eldre cacher uten suffiks er laget med inaVAMOS (alle cachene fra før 27.10.2026). Med inavamos brukes derfor
    `<navn>_inavamos.jsonl` hvis den finnes, ellers den eldre `<navn>.jsonl` hvis den finnes; finnes ingen av dem, er stien
    `<navn>_inavamos.jsonl` (ny cache). Med inaseg er stien alltid `<navn>_inaseg.jsonl`: en fil uten suffiks leses aldri."""
    mappe = pathlib.Path(mappe)
    seg = segmentering or segment.valgt_segmentering()
    if seg not in CACHE_SUFFIKS:
        raise segment.SegmenteringFeil(f"ukjent segmentering {seg!r}")
    ny = mappe / f"{navn}{CACHE_SUFFIKS[seg]}.jsonl"
    if seg == "inavamos" and not ny.exists():
        eldre = mappe / f"{navn}.jsonl"  # eldre cacher uten suffiks er laget med inaVAMOS
        if eldre.exists():
            return eldre
    return ny


def grunnnavn(sti) -> str:
    """Navnet uten segmenteringssuffiks og `.jsonl` (motsatt av `cache_sti`): `ord_npsc_test_inaseg.jsonl` → `ord_npsc_test`."""
    stamme = pathlib.Path(sti).name.removesuffix(".jsonl")
    for suffiks in CACHE_SUFFIKS.values():
        if stamme.endswith(suffiks):
            return stamme.removesuffix(suffiks)
    return stamme


def les_jsonl(sti):
    sti = pathlib.Path(sti)
    return {} if not sti.exists() else {j["id"]: j for j in (json.loads(l) for l in sti.read_text(encoding="utf-8").splitlines() if l.strip())}


def legg_til_jsonl(sti, objekt):
    with open(sti, "a", encoding="utf-8") as f:
        f.write(json.dumps(objekt, ensure_ascii=False) + "\n")
