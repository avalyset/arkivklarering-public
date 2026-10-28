#!/usr/bin/env python3
"""H4 i KLAR-PREREG-0001: flaggkjeden på menneskeinnleste opptak av testmanuset (KLAR-MANUS-0002).

Leser innleste opptak fra norsk-tales rigg (`<rot>/<runde>/opptak/<manus-id>.wav` + `<rot>/<runde>/runde.json`), kjører begge lag
(rålag og normalisert lag, DTW-ordtidsstempler) og union gjennom rørledningen, og scorer målelementene per kategori med vendor-
`score.py` (`kalibrering.score_flagg`): andel `flagg_treff`, n per kategori, og bokmål og nynorsk hver for seg. Skriver
`docs/KLAR-EVAL-0009_arkivklarering_h4-testmanus_v1.0_<dato>.{json,md}` med tersklene fra PREREG-0001 og bestått / ikke bestått.

Oppsett: språk etter målform (`-l no` for bokmål, `-l nn` for nynorsk; «matchet», grunnlaget for tersklene i PREREG-0001).
`--oppsett nn` kjører `-l nn` for alle som sekundært utfall.

Sperret: uten `--torrtest` leser skriptet KLAR-MANUS-0002 (`kalibrering.les_manus`), og det avvises til KLAR-PREREG-0001 har
statuslinjen `Status: registrert <OSF-URL>`; sha256 av manusfila må være den som står i preregistreringen.

TØRRTEST: `--torrtest` kjører justeringsmanuset KLAR-MANUS-0001 på de SYNTETISKE (TTS) filene i
$ARKIVKLARERING_DATA/lyd/syntetisk/ og skriver til `eval/dev/h4_torrtest_justeringsmanus_<dato>.{json,md}`, merket
«tørrtest på justeringsmanus». Det er ingen H4-måling.

    source scripts/miljo.sh
    .venv/bin/python kalibrering/kjor_h4.py --torrtest
    .venv/bin/python kalibrering/kjor_h4.py --prereg-id KLAR-PREREG-0001 [--runde runde-...] [--oppsett matchet|nn]
"""
import argparse
import datetime
import glob
import hashlib
import json
import math
import pathlib
import re
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "eval" / "dev"))
import felles  # noqa: E402
import kjor_syntetisk  # noqa: E402  (evaluer: scoring av cache mot manus)
from felles import legg_til_jsonl, les_jsonl  # noqa: E402

from arkivklarering import evaldata, kalibrering, miljo, personvern, transkriber  # noqa: E402

DATO = datetime.date.today().isoformat()
OPPTAKSROT = miljo.DATA / "lyd" / "menneske"
SYNTETISK = miljo.DATA / "lyd" / "syntetisk"
CACHE = miljo.EVAL_DATA
KATEGORIER = ["person", "sted", "dato", "fødselsår", "telefon", "fødselsnummer", "e-post", "helse", "økonomi", "konflikt", "religion", "politikk"]
OPPSETT = {"matchet": lambda r: "no" if r["malform"] == "nb" else "nn", "nn": lambda r: "nn"}


def wilson(k, n, z=1.96):
    if not n:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def sha256_fil(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def les_terskler(prereg):
    """Tersklene for H4 fra tabellen «terskel (på menneskeinnlest …)» i PREREG-0001: {kategori: (operator, verdi)}."""
    tekst = pathlib.Path(prereg).read_text(encoding="utf-8")
    del_ = tekst[tekst.index("terskel (på menneskeinnlest"):]
    ut = {}
    for linje in del_.splitlines()[2:]:
        if not linje.startswith("|"):
            break
        celler = [c.strip() for c in linje.strip().strip("|").split("|")]
        m = re.search(r"(≥|≤)\s*(\d),(\d+)", celler[-1])
        if celler[0] in KATEGORIER and m:
            ut[celler[0]] = (m.group(1), float(f"{m.group(2)}.{m.group(3)}"))
    mangler = [k for k in KATEGORIER if k not in ut]
    if mangler:
        raise ValueError(f"fant ikke terskel for {mangler} i {prereg}")
    return ut


def vurder(op, terskel, k, n):
    """bestått / ikke bestått på punktestimatet; «klart» når også 95 %-intervallgrensen er på riktig side."""
    if not n:
        return "ingen data", False
    lo, hi = wilson(k, n)
    p = k / n
    ok = p >= terskel if op == "≥" else p <= terskel
    klart = (lo >= terskel) if op == "≥" else (hi <= terskel)
    return ("bestått" if ok else "ikke bestått"), bool(ok and klart)


def finn_opptak(rot, runder):
    """[(runde, runde.json, {manus_id: wav})] for ferdige runder i riggens mappe."""
    ut = []
    for d in sorted(pathlib.Path(rot).glob("runde-*")):
        if runder and d.name not in runder:
            continue
        rj = d / "runde.json"
        if not rj.is_file():
            continue
        runde = json.loads(rj.read_text(encoding="utf-8"))
        wavs = {w.stem: w for w in sorted((d / "opptak").glob("*.wav"))}
        ut.append((d.name, runde, wavs))
    return ut


def utvid_manus(manus, opptak):
    """En rad per opptak: id = «<runde>:<manus-id>», med rundens region og kilde."""
    rader, meta = [], {}
    by_id = {r["id"]: r for r in manus}
    for runde_id, runde, wavs in opptak:
        for mid, wav in wavs.items():
            if mid not in by_id:
                continue
            rad = dict(by_id[mid])
            rad["id"] = f"{runde_id}:{mid}"
            rader.append(rad)
            meta[rad["id"]] = {"runde": runde_id, "manus_id": mid, "lyd": str(wav), "lyd_sha256": sha256_fil(wav),
                               "region": runde.get("dialektregion"), "kilde": runde.get("dialektkilde")}
    return rader, meta


def kjor(rader, meta, oppsett_navn, cache_sti):
    cache = les_jsonl(cache_sti)
    spr = OPPSETT[oppsett_navn]
    igjen = [{"id": r["id"], "lyd": meta[r["id"]]["lyd"], "whisper_sprak": spr(r)} for r in rader
             if r["id"] not in cache or cache[r["id"]].get("lyd_sha256") != meta[r["id"]]["lyd_sha256"]]
    print(f"{oppsett_navn}: {len(igjen)} av {len(rader)} opptak gjenstår", flush=True)
    oppsett = {lag: transkriber.finn_oppsett(lag) for lag in transkriber.LAG}
    gb = felles.gjenbruk_normalisert(cache_sti, oppsett["normalisert"], lambda *x: print(*x, flush=True))
    t0 = time.time()
    for i0 in range(0, len(igjen), 40):
        ut = felles.kjor_batch(igjen[i0:i0 + 40], oppsett, ordtider=True, logg=lambda *x: print(*x, flush=True), gjenbruk=gb)
        for it in igjen[i0:i0 + 40]:
            ut[it["id"]]["lyd_sha256"] = meta[it["id"]]["lyd_sha256"]
            legg_til_jsonl(cache_sti, ut[it["id"]])
        print(f"  {min(i0 + 40, len(igjen))}/{len(igjen)} ({time.time() - t0:.0f} s)", flush=True)
    return les_jsonl(cache_sti)


def tabell(res, terskler, tellere=True):
    """res = evaluer()-resultatet for union; samlet over målformer per kategori."""
    rader = []
    for kat in KATEGORIER:
        n = k = 0
        per_mf = {}
        for nokkel, d in res.items():
            kilde, mf = nokkel.split("|")
            if kilde != "union" or kat not in d:
                continue
            per_mf[mf] = (d[kat]["flagg"], d[kat]["n"])
            n += d[kat]["n"]
            k += d[kat]["flagg"]
        op, t = terskler[kat]
        dom, klart = vurder(op, t, k, n)
        lo, hi = wilson(k, n)
        rader.append({"kategori": kat, "n": n, "flagg_treff": k, "andel": (k / n if n else None), "ki95": [lo, hi],
                      "terskel": f"{op} {t:.2f}", "vurdering": dom, "klart": klart,
                      "bokmal": per_mf.get("nb"), "nynorsk": per_mf.get("nn")})
    return rader


def f(x):
    return "–" if x is None else f"{x:.3f}".replace(".", ",")


def skriv_md(sti, tittel, merke, meta_ut, rader_union, lagtall):
    L = [f"# {tittel}", "", merke, "", f"Generert {DATO} av `kalibrering/kjor_h4.py`. {meta_ut['beskrivelse']}", "",
         "## Union per kategori (flagg-treff / n; terskel fra KLAR-PREREG-0001)", "",
         "| kategori | n | flagg-treff | andel | 95 %-int. (Wilson) | terskel | vurdering | bokmål | nynorsk |", "|---|---|---|---|---|---|---|---|---|"]
    for r in rader_union:
        mf = lambda x: "–" if not x else f"{x[0]}/{x[1]}"  # noqa: E731
        L.append(f"| {r['kategori']} | {r['n']} | {r['flagg_treff']} | {f(r['andel'])} | {f(r['ki95'][0])}–{f(r['ki95'][1])} | {r['terskel']} | "
                 f"{r['vurdering']}{' (klart)' if r['klart'] else ''} | {mf(r['bokmal'])} | {mf(r['nynorsk'])} |")
    L += ["", "«Bestått» gjelder punktestimatet; «klart» betyr at også 95 %-intervallgrensen er på riktig side av terskelen. "
          "Intervallene antar uavhengige målelementer, og elementer i samme setning, fra samme leser og fra samme opptak er ikke uavhengige.",
          "", "## Per lag (rålag, normalisert lag og union; flagg-treff / n)", "",
          "| lag og målform | " + " | ".join(KATEGORIER) + " |", "|---|" + "---|" * len(KATEGORIER)]
    for nokkel, d in sorted(lagtall.items()):
        L.append(f"| {nokkel} | " + " | ".join((f"{d[k]['flagg']}/{d[k]['n']}" if k in d else "–") for k in KATEGORIER) + " |")
    L += ["", f"Opptak: {meta_ut['opptak']}; segmenter i cachen: {meta_ut['segmenter']}.", ""]
    sti.write_text("\n".join(L), encoding="utf-8")


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    ap = argparse.ArgumentParser()
    ap.add_argument("--torrtest", action="store_true", help="tørrtest på justeringsmanuset (syntetiske filer); ingen H4-måling")
    ap.add_argument("--prereg-id", default=None)
    ap.add_argument("--opptak", default=str(OPPTAKSROT), help="riggens opptaksmappe")
    ap.add_argument("--runde", action="append", default=[], help="bare disse rundene (standard: alle)")
    ap.add_argument("--oppsett", default="matchet", choices=list(OPPSETT))
    a = ap.parse_args()

    prereg = evaldata.siste_versjon(glob.glob(str(REPO / "docs" / "KLAR-PREREG-0001_*.md")))
    terskler = les_terskler(prereg)
    if a.torrtest:
        manus_sti = evaldata.siste_versjon(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0001_*.tsv")))
        manus = kalibrering.les_manus(manus_sti)
        opptak = [("syntetisk", {"dialektregion": None, "dialektkilde": None}, {r["id"]: SYNTETISK / f"{r['id']}.wav" for r in manus
                                                                                  if (SYNTETISK / f"{r['id']}.wav").is_file()})]
        merke = "**TØRRTEST PÅ JUSTERINGSMANUS (SYNTETISK, TTS). Ingen H4-måling: justeringsmanuset er brukt til å justere mønstrene og tersklene, og lyden er syntetisk.**"
        tittel = "H4-skriptet: tørrtest på justeringsmanus"
        stub = REPO / "eval" / "dev" / f"h4_torrtest_justeringsmanus_{DATO}"
        cache_sti = felles.cache_sti(CACHE, f"h4_torrtest_{a.oppsett}")  # følger segmenteringen (felles.cache_sti)
    else:
        if not a.prereg_id:
            sys.exit("H4 på testmanuset krever --prereg-id KLAR-PREREG-0001 (og at preregistreringen er registrert)")
        evaldata.sjekk_splitt("test", a.prereg_id)
        manus_sti = evaldata.siste_versjon(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))
        manus = kalibrering.les_manus(manus_sti, prereg_id=a.prereg_id)
        sha = sha256_fil(manus_sti)
        if sha not in pathlib.Path(prereg).read_text(encoding="utf-8"):
            sys.exit(f"sha256 av {pathlib.Path(manus_sti).name} ({sha}) står ikke i {pathlib.Path(prereg).name}: manuset er endret etter låsing")
        opptak = finn_opptak(a.opptak, a.runde)
        merke = "H4 (sekundært utfall) på menneskeinnlest KLAR-MANUS-0002. Tersklene er forhåndsregistrert i KLAR-PREREG-0001."
        tittel = "KLAR-EVAL-0009: H4, flaggkjeden på menneskeinnlest testmanus"
        stub = REPO / "docs" / f"KLAR-EVAL-0009_arkivklarering_h4-testmanus_v1.0_{DATO}"
        cache_sti = felles.cache_sti(CACHE, f"h4_testmanus_{a.oppsett}")  # H4 kjøres med inaseg: h4_testmanus_<oppsett>_inaseg.jsonl

    rader, meta = utvid_manus(manus, opptak)
    if not rader:
        sys.exit("ingen opptak å score")
    print(f"{len(rader)} opptak fra {len(opptak)} runde(r)", flush=True)
    cache = kjor(rader, meta, a.oppsett, cache_sti)
    motor = personvern.lag_motor()
    res, malformfeil, bom = kjor_syntetisk.evaluer(rader, {k: v for k, v in cache.items() if k in meta}, motor)
    union = tabell(res, terskler)
    ut = {"merknad": merke.replace("*", ""), "manus": pathlib.Path(manus_sti).name, "manus_sha256": sha256_fil(manus_sti),
          "preregistrering": pathlib.Path(prereg).name, "oppsett": a.oppsett, "runder": {r[0]: {k: r[1].get(k) for k in ("modus", "dialektregion", "dialektkilde", "malform")} for r in opptak},
          "opptak": len(rader), "segmenter": len(cache), "union": union, "per_lag_og_malform": res, "malformfeil": malformfeil, "bom_i_union": bom}
    pathlib.Path(str(stub) + ".json").write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    skriv_md(pathlib.Path(str(stub) + ".md"), tittel, merke,
             {"beskrivelse": f"Manus: `{ut['manus']}` (sha256 `{ut['manus_sha256']}`). Oppsett: {a.oppsett}. Preregistrering: `{ut['preregistrering']}`.",
              "opptak": len(rader), "segmenter": len(cache)},
             union, {k: v for k, v in res.items()})
    print(str(stub) + ".md")
    for r in union:
        print(f"  {r['kategori']:14s} {r['flagg_treff']:3d}/{r['n']:<3d} {f(r['andel'])}  {r['terskel']:8s} {r['vurdering']}{' (klart)' if r['klart'] else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
