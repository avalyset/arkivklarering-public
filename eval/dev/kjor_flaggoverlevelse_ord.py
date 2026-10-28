#!/usr/bin/env python3
"""DEV-måling (IKKE pilot): flaggoverlevelse med ordtidsstempler i unionen.

  --datasett nbsamtale  de samme 60 NB Samtale validation-segmentene som KLAR-EVAL-0006 (KLAR-EVAL-0003). Rålaget og det
                        normaliserte laget kjøres på nytt med DTW-ordtidsstempler (`-l nn`, som primærmålingen i 0006).
  --datasett npsc       NPSC validation (`eval/`), utvalg med fast seed, stort nok til minst 150 person- og 100 stedsreferanseflagg
                        per målform eller til lydgrensen er nådd. Språk etter transkripsjonens målform (nb -> no, nn -> nn).

Samme metode som KLAR-EVAL-0006: referanse = personvernmotoren på den menneskelige transkripsjonen, rørledning = union av
flagg fra rålaget og det normaliserte laget (nå paret på tidsoverlapp mellom ordspenn, likhet bare til å velge mellom flere
tidstreff). Overlevelse (a): referanseflagget har et rørledningsflagg i samme kategori i samme segment. Streng (b): i tillegg
delt ord eller inneholdt utdrag. Ekstra: rørledningsflagg uten referanseflagg i samme kategori i samme segment.

Fase: velg (bare NPSC), kjor (Whisper; gjenopptar fra cache), evaluer. test-delen er sperret (arkivklarering/evaldata.py).

    source scripts/miljo.sh && .venv/bin/python eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc
"""
import argparse
import collections
import datetime
import json
import os
import pathlib
import random
import sys
import tarfile
import time

HER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HER))
import felles  # noqa: E402
from felles import REPO, dict_til_cue, legg_til_jsonl, les_jsonl  # noqa: E402
from kjor_flaggoverlevelse_dev import omtaler, streng_treff, wilson  # noqa: E402

from arkivklarering import evaldata, miljo, personvern, transkriber  # noqa: E402

DATO = datetime.date.today().isoformat()
EVALDATA = miljo.EVAL_DATA  # $ARKIVKLARERING_DATA/eval-data
NBS = EVALDATA / "nb_samtale"
NPSC = EVALDATA / "npsc"
KATEGORIER = ["person", "sted", "organisasjon", "dato", "fødselsår", "telefon", "fødselsnummer", "e-post",
              "helse", "økonomi", "konflikt", "religion", "politikk"]
MALT = ["person", "sted"]  # overlevelse måles bare for disse; resten er «ikke målt – krever eget testmateriale»
IKKE_MALT = ["helse", "økonomi", "konflikt", "religion", "politikk", "dato", "fødselsår", "telefon", "fødselsnummer", "e-post"]


def logg(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- utvalg
def items_nbsamtale():
    utv = json.loads((REPO / "eval/dev/KLAR-EVAL-0003_arkivklarering_dev-utvalg_v1.0_2026-10-26.json").read_text(encoding="utf-8"))
    ut = []
    for r in utv["utvalg"]:
        ut.append({"id": f'{r["source_file_id"]}_{r["segment_id"]}', "gruppe": {"bm": "nb", "nn": "nn"}[r["orthography"]],
                   "lyd": str(NBS / "valg_validation" / pathlib.PurePosixPath(r["file_name"])), "ref": r["orthographic"],
                   "varighet": r["duration"], "whisper_sprak": "nn"})
    return ut


def velg_npsc(splitt, prereg, seed, maks_timer, mal_person, mal_sted, sti):
    mappe = evaldata.npsc_mappe(NPSC, splitt, prereg)
    rader = []
    for f in sorted(mappe.glob("*.json")):
        rader += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    def ok(r):
        d = (r["end_time"] - r["start_time"]) / 1000
        return 1.5 <= d <= 25 and r["normsentence_text"].strip()
    kand = {"nb": [r for r in rader if ok(r) and r["sentence_language_code"] == "nb-NO"],
            "nn": [r for r in rader if ok(r) and r["sentence_language_code"] == "nn-NO"]}
    motor = personvern.lag_motor()
    rng = random.Random(seed)
    valgt, brukt_s = [], 0.0
    totalt_s = maks_timer * 3600
    lister = {}
    for sprak in ("nb", "nn"):
        liste = sorted(kand[sprak], key=lambda r: (r["meeting_date"], r["sentence_id"]))
        rng.shuffle(liste)
        lister[sprak] = iter(liste)
    tell = {"nb": collections.Counter(), "nn": collections.Counter()}
    # vektet rundtur, to bokmålssegmenter per nynorsksegment (nynorsk er ca. 13 % av segmentene, men gir ellers for lite nynorsk).
    # Utvalget utvides gradvis til de samlede målene er nådd (person og sted, begge målformer sammen) eller lydgrensen er nådd.
    rekke = ["nb", "nb", "nn"]
    tom = set()
    while brukt_s < totalt_s and len(tom) < 2:
        if sum(t["person"] for t in tell.values()) >= mal_person and sum(t["sted"] for t in tell.values()) >= mal_sted:
            break
        for sprak in rekke:
            if sprak in tom:
                continue
            r = next(lister[sprak], None)
            if r is None:
                tom.add(sprak)
                continue
            d = (r["end_time"] - r["start_time"]) / 1000
            if brukt_s + d > totalt_s:
                continue
            ref = omtaler(personvern.flagg_tekst(r["normsentence_text"], sprak, motor))
            for f in ref:
                tell[sprak][f.kategori] += 1
            valgt.append({"id": f'{r["meeting_date"]}_{r["sentence_id"]}', "path": r["path"], "gruppe": sprak, "ref": r["normsentence_text"],
                          "varighet": d, "whisper_sprak": "no" if sprak == "nb" else "nn", "dato": r["meeting_date"]})
            brukt_s += d
    for sprak in ("nb", "nn"):
        logg(f"{sprak}: {sum(1 for v in valgt if v['gruppe'] == sprak)} segmenter, referanseflagg person {tell[sprak]['person']}, sted {tell[sprak]['sted']}")
    logg(f"samlet: person {sum(t['person'] for t in tell.values())}, sted {sum(t['sted'] for t in tell.values())}, lyd {brukt_s / 3600:.2f} t")
    sti.write_text(json.dumps({"seed": seed, "splitt": splitt, "valgt": valgt, "lyd_sek": brukt_s}, ensure_ascii=False, indent=1), encoding="utf-8")
    return valgt


def pakk_ut_npsc(valgt, splitt, prereg):
    mappe = evaldata.npsc_mappe(NPSC, splitt, prereg)
    ut = NPSC / f"valg_{splitt}"
    ut.mkdir(exist_ok=True)
    for dato in sorted({v["dato"] for v in valgt}):
        onsket = {v["path"] + ".mp3" for v in valgt if v["dato"] == dato}
        with tarfile.open(mappe / f"{dato}_16K_mp3.tar.gz") as t:
            for m in t:
                if m.name in onsket and not (ut / m.name).exists():
                    t.extract(m, ut, filter="data")
    for v in valgt:
        v["lyd"] = str(ut / (v["path"] + ".mp3"))
    return valgt


# ---------------------------------------------------------------- evaluering
def finn_prefiks(items, mal_person, mal_sted, sti, splitt, seed):
    """Stoppregel uten å se utfall: det minste prefikset av utvalget (i seed-rekkefølgen) som gir minst `mal_person` personflagg og
    `mal_sted` stedsflagg i REFERANSEN (personvernmotoren på den menneskelige transkripsjonen). Ingen Whisper, ingen rørledningsutfall."""
    motor = personvern.lag_motor()
    tell = collections.Counter()
    per_sprak = {"nb": collections.Counter(), "nn": collections.Counter()}
    k = None
    kum = []
    for n, it in enumerate(items, 1):
        for f in omtaler(personvern.flagg_tekst(it["ref"], it["gruppe"], motor)):
            tell[f.kategori] += 1
            per_sprak[it["gruppe"]][f.kategori] += 1
        kum.append((n, tell["person"], tell["sted"]))
        if k is None and tell["person"] >= mal_person and tell["sted"] >= mal_sted:
            k = n
            ved_k = {"person": tell["person"], "sted": tell["sted"], "per_malform": {g: dict(c) for g, c in per_sprak.items()},
                     "lyd_sek": round(sum(i["varighet"] for i in items[:n]), 1), "nb": sum(1 for i in items[:n] if i["gruppe"] == "nb"),
                     "nn": sum(1 for i in items[:n] if i["gruppe"] == "nn")}
    ut = {"regel": f"minste prefiks i seed-rekkefølgen med minst {mal_person} personflagg og {mal_sted} stedsflagg i referansen",
          "seed": seed, "splitt": splitt, "utvalg_lengde": len(items), "prefiks_lengde": k, "ved_prefiks": ved_k if k else None,
          "referanse_hele_utvalget": {"person": tell["person"], "sted": tell["sted"]},
          "logget": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
          "fastsatt": "før rørledningsutfallet for NPSC ble lest (bare antall ferdige segmenter i cachen var kjent)"}
    sti.write_text(json.dumps(ut, ensure_ascii=False, indent=2), encoding="utf-8")
    return ut


def evaluer(items, cache, motor, navn_tillegg=""):
    tell = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    ref_antall = collections.defaultdict(collections.Counter)
    seg_med_ref = collections.defaultdict(collections.Counter)
    n_seg = collections.Counter()
    for it in items:
        c = cache.get(it["id"])
        if not c:
            continue
        g = it["gruppe"]
        n_seg[g] += 1
        ref = omtaler(personvern.flagg_tekst(it["ref"], g, motor))
        per_kat = collections.defaultdict(list)
        for r in ref:
            per_kat[r.kategori].append(r)
        for k, v in per_kat.items():
            ref_antall[g][k] += len(v)
            seg_med_ref[g][k] += 1
        lagflagg = {lag: personvern.flagg_cues([dict_til_cue(x) for x in c["cues"].get(lag, [])], lag, g, motor)
                    for lag in transkriber.LAG}
        union = personvern.slaa_sammen_lag(lagflagg)
        kilder = {"ra": [(f.kategori, [f.utdrag]) for f in lagflagg["ra"]],
                  "normalisert": [(f.kategori, [f.utdrag]) for f in lagflagg["normalisert"]],
                  "union": [(u.kategori, [x["utdrag"] for x in u.per_lag.values()]) for u in union]}
        antall_union = collections.Counter(u.lag for u in union)
        tell[g]["_union_lag"].update(antall_union)
        for kilde, pf in kilder.items():
            for k in MALT:
                refs = per_kat.get(k, [])
                pfk = [u for kk, u in pf if kk == k]
                t = tell[g][(kilde, k)]
                t["ref"] += len(refs)
                t["ref_a"] += sum(1 for _ in refs if pfk)
                t["ref_b"] += sum(1 for r in refs if any(streng_treff(r.utdrag, x) for u in pfk for x in u))
                t["pred"] += len(pfk)
                t["ekstra_a"] += len(pfk) if not refs else 0
                t["ekstra_b"] += sum(1 for u in pfk if not any(streng_treff(r.utdrag, x) for r in refs for x in u))
    res = {}
    for g, d in tell.items():
        res[g] = {"segmenter": n_seg[g], "referanseflagg": dict(ref_antall[g]), "segmenter_med_referanseflagg": dict(seg_med_ref[g]),
                  "union_per_kildelag": dict(d["_union_lag"]), "kategorier": {}}
        for (kilde, k), x in ((kk, v) for kk, v in d.items() if kk != "_union_lag"):
            if x["ref"] == 0 and x["pred"] == 0:
                continue
            res[g]["kategorier"][f"{kilde}|{k}"] = {
                "ref": x["ref"], "overlevd_a": x["ref_a"], "overlevelse_a": None if not x["ref"] else round(x["ref_a"] / x["ref"], 3),
                "overlevelse_a_ki95": wilson(x["ref_a"], x["ref"]), "overlevd_b": x["ref_b"],
                "overlevelse_b": None if not x["ref"] else round(x["ref_b"] / x["ref"], 3),
                "overlevelse_b_ki95": wilson(x["ref_b"], x["ref"]),
                "pipeline": x["pred"], "ekstra_a": x["ekstra_a"], "ekstra_andel_a": None if not x["pred"] else round(x["ekstra_a"] / x["pred"], 3),
                "ekstra_b": x["ekstra_b"], "ekstra_andel_b": None if not x["pred"] else round(x["ekstra_b"] / x["pred"], 3)}
    return res


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()  # avbryter hvis cacher og tmp ikke ligger under ARKIVKLARERING_DATA
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasett", choices=["nbsamtale", "npsc"], required=True)
    ap.add_argument("--splitt", default="validation", choices=evaldata.SPLITT)
    ap.add_argument("--prereg-id")
    ap.add_argument("--fase", default="alle", choices=["velg", "prefiks", "kjor", "evaluer", "alle"])
    ap.add_argument("--seed", type=int, default=20261026)
    ap.add_argument("--maks-timer", type=float, default=2.0)
    ap.add_argument("--mal-person", type=int, default=150)
    ap.add_argument("--mal-sted", type=int, default=100)
    ap.add_argument("--ut-mappe", default=str(REPO / "docs"), help="mappe for resultatfila (standard: docs)")
    ap.add_argument("--etikett", default="DEV", choices=["DEV", "TEST"], help="DEV (standard) eller TEST («TEST – preregistrert (OSF hc83q)» i merknaden)")
    ap.add_argument("--eval-nr", help="KLAR-EVAL-<NNNN> for resultatfila (standard: -0006 for nbsamtale og -0007 for npsc, som i DEV)")
    a = ap.parse_args()
    evaldata.sjekk_splitt(a.splitt, a.prereg_id)  # hard sperre før noe leses
    if a.datasett == "nbsamtale" and a.splitt != "validation":
        sys.exit("nbsamtale-utvalget er trukket fra validation")
    valg_sti = EVALDATA / f"valg_{a.datasett}_{a.splitt}.json"
    # cachen (med tidslinjen) følger segmenteringen: ord_<datasett>_<splitt>_inaseg.jsonl eller _inavamos.jsonl; med inavamos brukes en eldre
    # fil uten suffiks (laget med inaVAMOS) hvis _inavamos-fila ikke finnes (felles.cache_sti)
    cache_sti = felles.cache_sti(EVALDATA, f"ord_{a.datasett}_{a.splitt}")

    if a.datasett == "nbsamtale":
        items = items_nbsamtale()
    else:
        if a.fase in ("velg", "alle") or not valg_sti.exists():
            valgt = velg_npsc(a.splitt, a.prereg_id, a.seed, a.maks_timer, a.mal_person, a.mal_sted, valg_sti)
        else:
            valgt = json.loads(valg_sti.read_text(encoding="utf-8"))["valgt"]
        items = pakk_ut_npsc(valgt, a.splitt, a.prereg_id)
        logg(f"utvalg: {len(items)} segmenter, {sum(i['varighet'] for i in items) / 3600:.2f} t lyd")
    if a.fase == "velg":
        return
    prefiks_sti = EVALDATA / f"prefiks_{a.datasett}_{a.splitt}.json"
    if a.datasett == "npsc":
        if a.fase == "prefiks":
            logg(json.dumps(finn_prefiks(items, a.mal_person, a.mal_sted, prefiks_sti, a.splitt, a.seed), ensure_ascii=False))
            return
        if prefiks_sti.exists():  # stoppregelen er fastsatt uten å se rørledningsutfall: bare prefikset kjøres og evalueres
            pf = json.loads(prefiks_sti.read_text(encoding="utf-8"))
            items = items[:pf["prefiks_lengde"]]
            logg(f"prefiks: {pf['prefiks_lengde']} av {pf['utvalg_lengde']} segmenter (regel fra {pf['logget']})")

    cache = les_jsonl(cache_sti)
    if a.fase in ("kjor", "alle"):
        oppsett = {lag: transkriber.finn_oppsett(lag) for lag in transkriber.LAG}
        gb = felles.gjenbruk_normalisert(cache_sti, oppsett["normalisert"], logg)
        t0 = time.time()
        igjen = [i for i in items if i["id"] not in cache]
        logg(f"Whisper: {len(igjen)} av {len(items)} segmenter gjenstår")
        for i0 in range(0, len(igjen), 40):
            gruppe = igjen[i0:i0 + 40]
            o = {lag: x for lag, x in oppsett.items()}
            ut = felles.kjor_batch(gruppe, o, ordtider=True, logg=logg, gjenbruk=gb)
            for it in gruppe:
                legg_til_jsonl(cache_sti, ut[it["id"]])
                cache[it["id"]] = ut[it["id"]]
            logg(f"  {min(i0 + 40, len(igjen))}/{len(igjen)} ({time.time() - t0:.0f} s)")
    if a.fase in ("evaluer", "alle"):
        motor = personvern.lag_motor()
        res = evaluer(items, cache, motor)
        meta = {"merknad": "DEV, ikke pilot" if a.etikett == "DEV" else os.environ.get("ARKIVKLARERING_ETIKETT_TEST", "TEST – preregistrert (OSF hc83q)"), "datasett": a.datasett, "splitt": a.splitt, "seed": a.seed,
                "lyd_sek": round(sum(i["varighet"] for i in items if i["id"] in cache)), "segmenter": len([i for i in items if i["id"] in cache]),
                "ikke_malt": IKKE_MALT, "ordtider": "DTW (-nfa -dtw large.v3), paring på ordspenn med toleranse "
                + f"{personvern.TIDSTOLERANSE_S} s", "resultat": res}
        if a.datasett == "npsc" and prefiks_sti.exists():
            meta["prefiks"] = json.loads(prefiks_sti.read_text(encoding="utf-8"))
        ut_mappe = pathlib.Path(a.ut_mappe)
        ut_mappe.mkdir(parents=True, exist_ok=True)
        if a.datasett == "nbsamtale":
            sti = ut_mappe / f"KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.1_{DATO}.json"
        else:
            meta["segment_ider"] = [i["id"] for i in items if i["id"] in cache]
            sti = ut_mappe / f"KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_{DATO}.json"
        if a.etikett == "TEST" or a.eval_nr:
            sti = ut_mappe / f"{a.eval_nr or sti.name.split('_')[0]}_arkivklarering_{a.etikett.lower()}-flaggoverlevelse-{a.datasett}_v1.0_{DATO}.json"
        sti.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        logg(sti)


if __name__ == "__main__":
    main()
