#!/usr/bin/env python3
"""DEV-måling (IKKE pilot): arkivklarering-rørledningen på et lagdelt utvalg fra nb_samtale (validation).

Ingen konklusjoner om pilotkvalitet. Utvalget trekkes før noen kjøring, med fast seed, og ID-ene
lagres. Fasit er feltet `orthographic`. WER regnes med jiwer etter enkel normalisering
(små bokstaver, tegnsetting fjernes). Hver rad i tabellen er korpus-WER (summerte feil over summerte
ord), ikke gjennomsnitt av segment-WER.

Konfigurasjoner per lag:
  nn      -l nn for alle segmenter (slik rørledningen kjører)
  matchet -l etter fasitens skriftform (bm -> no, nn -> nn)
Dialektene og skriftformen henger sammen i dette utvalget (sw/w er mest nynorsk, e/n mest bokmål);
`nn`-kolonnene straffer bokmålsfasit, og dialektforskjellene er derfor sammenblandet med skriftform.

    .venv/bin/python eval/dev/kjor_dev.py [--utvalg-bare]
"""
import argparse
import dataclasses
import collections
import datetime
import json
import os
import pathlib
import random
import re
import sys
import tarfile
import tempfile
import time

import jiwer

HER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HER.parent.parent))
from arkivklarering import evaldata, miljo, segment, transkriber  # noqa: E402

DATA = pathlib.Path(os.environ.get("ARKIVKLARERING_EVALDATA") or miljo.EVAL_DATA / "nb_samtale")
SPLITT = "validation"  # settes av --splitt; test-delen er sperret (arkivklarering/evaldata.py)
PREREG_ID = None
SEED = 20261026
PER_DIALEKT = 12  # settes av --per-dialekt (standard 12 = DEV-utvalget)
UT_MAPPE = None  # settes av --ut-mappe (standard: denne mappen)
ETIKETT = "DEV"  # settes av --etikett (DEV eller TEST)
EVAL_NR = None  # settes av --eval-nr (standard: KLAR-EVAL-0002 og -0003, dagens DEV-filnavn)
ETIKETT_TEST = os.environ.get("ARKIVKLARERING_ETIKETT_TEST", "TEST – preregistrert (OSF hc83q)")  # overstyres bare av sensitivitetskjøringen (KLAR-ADR-0019)
DIALEKTER = ["e", "n", "sw", "t", "w"]
DATO = datetime.date.today().isoformat()
SPRAK_FRA_SKRIFTFORM = {"bm": "no", "nn": "nn"}


def trekk_utvalg():
    rader = [json.loads(l) for l in open(evaldata.metadata_sti(DATA, SPLITT, PREREG_ID), encoding="utf-8")]
    kandidater = [r for r in rader if not r["overlap_previous"] and not r["overlap_next"]
                  and 2 <= r["duration"] <= 12 and len(r["orthographic"].split()) >= 3]
    rng = random.Random(SEED)
    valg = []
    for d in DIALEKTER:
        pool = sorted((r for r in kandidater if r["dialect"] == d), key=lambda r: (r["source_file_id"], r["segment_id"]))
        valg += rng.sample(pool, min(PER_DIALEKT, len(pool)))  # har et område færre kvalifiserte, tas alle (PREREG, Study design); gir samme trekk som før når poolen er stor nok
    return valg, len(kandidater)


def pakk_ut(valg, mappe):
    for form in ("bm", "nn"):
        onsket = {pathlib.PurePosixPath(r["file_name"]).as_posix(): r for r in valg if r["orthography"] == form}
        if not onsket:
            continue
        with tarfile.open(evaldata.tar_sti(DATA, SPLITT, form, PREREG_ID)) as t:
            for m in t:
                if m.name in onsket:  # filnavn i tar følger data/<splitt>/<form>/
                    t.extract(m, mappe, filter="data")


def norm(t):
    t = t.lower()
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def wer_gruppe(par):
    if not par:
        return None
    return jiwer.wer([r for r, _ in par], [h if h else "" for _, h in par])


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()  # avbryter hvis cacher og tmp ikke ligger under ARKIVKLARERING_DATA
    ap = argparse.ArgumentParser()
    ap.add_argument("--utvalg-bare", action="store_true")
    ap.add_argument("--splitt", default="validation", choices=evaldata.SPLITT,
                    help="datasettdel (standard: validation). test krever --prereg-id")
    ap.add_argument("--prereg-id", help="KLAR-PREREG-<NNNN>; kreves for --splitt test")
    ap.add_argument("--per-dialekt", type=int, default=12, help="segmenter per dialektområde (standard 12 = DEV-utvalget; PREREG H1: 60)")
    ap.add_argument("--ut-mappe", default=str(HER), help="mappe for utdata (standard: eval/dev)")
    ap.add_argument("--etikett", default="DEV", choices=["DEV", "TEST"], help="DEV (standard) eller TEST (overskrift «TEST – preregistrert (OSF hc83q)»)")
    ap.add_argument("--eval-nr", help="KLAR-EVAL-<NNNN> for utdatafilene (standard: -0002 for resultatet og -0003 for utvalget, som i DEV)")
    a = ap.parse_args()
    global SPLITT, PREREG_ID, PER_DIALEKT, UT_MAPPE, ETIKETT, EVAL_NR
    SPLITT, PREREG_ID, PER_DIALEKT, UT_MAPPE, ETIKETT, EVAL_NR = a.splitt, a.prereg_id, a.per_dialekt, pathlib.Path(a.ut_mappe), a.etikett, a.eval_nr
    evaldata.sjekk_splitt(SPLITT, PREREG_ID)  # hard sperre før noe leses

    valg, n_kand = trekk_utvalg()
    UT_MAPPE.mkdir(parents=True, exist_ok=True)
    if ETIKETT == "DEV" and EVAL_NR is None:
        utvalg_sti = UT_MAPPE / f"KLAR-EVAL-0003_arkivklarering_dev-utvalg_v1.0_{DATO}.json"
        stamme = UT_MAPPE / f"KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_{DATO}"
    else:
        nr = EVAL_NR or "KLAR-EVAL-0002"
        utvalg_sti = UT_MAPPE / f"{nr}_arkivklarering_{ETIKETT.lower()}-nbsamtale-wer_v1.0_{DATO}.utvalg.json"
        stamme = UT_MAPPE / f"{nr}_arkivklarering_{ETIKETT.lower()}-nbsamtale-wer_v1.0_{DATO}"
    merknad = "DEV, ikke pilot" if ETIKETT == "DEV" else ETIKETT_TEST
    utvalg_sti.write_text(json.dumps({
        "merknad": f"DEV, ikke pilot. Lagdelt utvalg fra Sprakbanken/nb_samtale ({SPLITT}), fast seed." if ETIKETT == "DEV" else f"{ETIKETT_TEST}. Lagdelt utvalg fra Sprakbanken/nb_samtale ({SPLITT}), fast seed.",
        "datasett_revisjon": "1c7028101858b854d3d568761778d8f63bb7e33f", "splitt": SPLITT,
        "seed": SEED, "per_dialekt": PER_DIALEKT,
        "filter": "ingen overlapp mot forrige/neste, 2–12 s, minst 3 ord i fasiten",
        "kandidater_etter_filter": n_kand,
        "utvalg": [{k: r[k] for k in ("source_file_id", "segment_id", "dialect", "orthography", "duration",
                                      "speaker_id", "gender", "source_type", "file_name", "orthographic")}
                   for r in valg]}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(utvalg_sti)
    if a.utvalg_bare:
        return

    mappe = DATA / f"valg_{SPLITT}"
    mappe.mkdir(exist_ok=True)
    pakk_ut(valg, mappe)
    lyd = {r["segment_id"]: mappe / pathlib.PurePosixPath(r["file_name"]) for r in valg}
    # segment_id er ikke unik på tvers av kildefiler; bruk kilde+segment
    nokkel = lambda r: f'{r["source_file_id"]}_{r["segment_id"]}'  # noqa: E731
    lyd = {nokkel(r): mappe / pathlib.PurePosixPath(r["file_name"]) for r in valg}
    mangler = [k for k, v in lyd.items() if not v.is_file()]
    assert not mangler, mangler

    t0 = time.time()
    tidslinjer = {}
    for r in valg:
        tidslinjer[nokkel(r)] = segment.bygg_tidslinje(segment.segmenter(lyd[nokkel(r)]))
    print(f"segmentering {len(valg)} filer: {time.time() - t0:.0f} s", flush=True)

    oppsett = {lag: transkriber.finn_oppsett(lag) for lag in transkriber.LAG}
    res = {}  # (lag, konfig) -> {nokkel: tekst}
    # Gjenbruk av det normaliserte lagets lagrede utdata fra forrige versjon av denne målingen (KLAR-ADR-0017): modellen (låst sha256) og alle
    # parametere er uendret, og laget kjøres uten -nt. Aktivert av ARKIVKLARERING_GJENBRUK_NORMALISERT=1.
    gammel = None
    if os.environ.get("ARKIVKLARERING_GJENBRUK_NORMALISERT") == "1":
        assert not oppsett["normalisert"].uten_tidsstempeltokens
        kand = sorted(HER.glob("KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_*.json"))
        if kand:
            gammel = {x["id"]: x["hyp"] for x in json.loads(kand[-1].read_text(encoding="utf-8"))["segmenter"]}
            print(f"gjenbruk: normalisert lag fra {kand[-1].name} ({len(gammel)} segmenter); modell sha256 {oppsett['normalisert'].sha256[:12]}… (låst), parametere uendret (uten -nt)", flush=True)
    for lag in transkriber.LAG:            # ett lag om gangen, ett segment om gangen
        for konfig in ("nn", "matchet"):
            t1 = time.time()
            ut = {}
            if lag == "normalisert" and gammel and all(nokkel(r) in gammel and f"{lag}/{konfig}" in gammel[nokkel(r)] for r in valg):
                res[(lag, konfig)] = {nokkel(r): gammel[nokkel(r)][f"{lag}/{konfig}"] for r in valg}
                print(f"{lag}/{konfig}: gjenbrukt fra lagret utdata", flush=True)
                continue
            for r in valg:
                o = oppsett[lag]
                sprak = "nn" if konfig == "nn" else SPRAK_FRA_SKRIFTFORM[r["orthography"]]
                o = dataclasses.replace(o, sprak=sprak)
                cues = transkriber.transkriber(lyd[nokkel(r)], tidslinjer[nokkel(r)], o)
                ut[nokkel(r)] = " ".join(c.tekst for c in cues)
            res[(lag, konfig)] = ut
            print(f"{lag}/{konfig}: {time.time() - t1:.0f} s", flush=True)

    # resultater
    per_segment = []
    for r in valg:
        k = nokkel(r)
        tl = tidslinjer[k]
        dekket = sum(s.varighet for s in tl if s.disposisjon == segment.TRANSKRIBER)
        per_segment.append({"id": k, "dialect": r["dialect"], "orthography": r["orthography"],
                            "duration": r["duration"], "dekket_av_tale_s": round(dekket, 2),
                            "flagg": sorted({f for s in tl for f in s.flagg}),
                            "fasit": r["orthographic"],
                            "hyp": {f"{lag}/{konfig}": res[(lag, konfig)][k] for lag, konfig in res}})
    tabell = {}
    for kol in (f"{lag}/{konfig}" for lag, konfig in res):
        tabell[kol] = {}
        for grp in DIALEKTER + ["totalt"] + ["skrift:bm", "skrift:nn"]:
            def i_gruppe(s):
                return (grp == "totalt" or s["dialect"] == grp or grp == f'skrift:{s["orthography"]}')
            par = [(norm(s["fasit"]), norm(s["hyp"][kol])) for s in per_segment if i_gruppe(s)]
            w = wer_gruppe(par)
            tabell[kol][grp] = None if w is None else round(w, 4)
            tabell[kol][grp + "_n"] = len(par)
    modeller = {lag: {"modell": pathlib.Path(o.modell).name, "sha256": o.sha256} for lag, o in oppsett.items()}
    pathlib.Path(str(stamme) + ".json").write_text(json.dumps(
        {"merknad": merknad, "seed": SEED, "modeller": modeller, "wer": tabell,
         "segmenter": per_segment}, ensure_ascii=False, indent=2), encoding="utf-8")

    kols = list(tabell)
    if ETIKETT == "DEV":
        topp = [f"# DEV-måling ({DATO}): WER på nb_samtale ({SPLITT}), 60 segmenter", "",
                "**DEV, ikke pilot. Ingen konklusjoner om pilotkvalitet.** 12 segmenter per dialektområde "
                f"(e, n, sw, t, w), seed {SEED}. Fasit: `orthographic`. Korpus-WER etter normalisering (små bokstaver, "
                "tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.", ""]
    else:
        topp = [f"# {ETIKETT_TEST} ({DATO}): WER på nb_samtale ({SPLITT}), {len(valg)} segmenter", "",
                f"**{ETIKETT_TEST}.** Opptil {PER_DIALEKT} segmenter per dialektområde (e, n, sw, t, w), seed {SEED}; har et område færre kvalifiserte segmenter, tas alle. "
                "Antall per område: " + ", ".join(f"{d} {sum(1 for r in valg if r['dialect'] == d)}" for d in DIALEKTER) + ". Fasit: `orthographic`. "
                "Korpus-WER etter normalisering (små bokstaver, tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.", ""]
    md = [*topp,
          "`ra` = NB-Whisper large verbatim, `normalisert` = NB-Whisper large (ikke verbatim). "
          "`nn` = `-l nn` for alle; `matchet` = språk etter fasitens skriftform. "
          "Rålaget skriver ut nøling og omtrent som sagt og scores likevel mot ortografisk fasit, så ra-tallene "
          "er ikke likestilt med normalisert lag.", "",
          "| gruppe (n) | " + " | ".join(kols) + " |", "|---|" + "---|" * len(kols)]
    for grp in DIALEKTER + ["totalt", "skrift:bm", "skrift:nn"]:
        n = tabell[kols[0]][grp + "_n"]
        md.append(f"| {grp} ({n}) | " + " | ".join("–" if tabell[k][grp] is None else f"{tabell[k][grp]:.3f}" for k in kols) + " |")
    ingen = {k: sum(1 for s in per_segment if not s["hyp"][k].strip()) for k in kols}
    md += ["", f"Segmenter uten noen tekst (tom hypotese), av {len(per_segment)}: " + ", ".join(f"{k}: {v}" for k, v in ingen.items()), "",
           "Modeller: " + "; ".join(f"{l}: `{m['modell']}` sha256 `{m['sha256']}`" for l, m in modeller.items())]
    pathlib.Path(str(stamme) + ".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
