#!/usr/bin/env python3
"""DEV-måling (IKKE pilot): hvor mange personvernflagg overlever talegjenkjenningen?

Samme 60 NB Samtale validation-segmenter som DEV-målingen av WER (KLAR-EVAL-0002/0003). Whisper kjøres IKKE på nytt:
hypotesene hentes fra den lagrede DEV-utdataen. Referanse: personvernmotoren på den menneskelige ortografiske
transkripsjonen (`fasit`). Rørledning: flagg på rålaget (ra) og det normaliserte laget for samme segment, og union av dem
(`personvern.slaa_sammen_lag`). Ingen terskel.

Treff, per kategori:
  (a) overlevelse: referanseflagget har minst ett rørledningsflagg i samme kategori i samme segment
  (b) streng: i tillegg deler flaggene minst ett ord (små bokstaver, uten tegnsetting) eller det ene utdraget inneholder det andre
Ekstra flagg: rørledningsflagg uten referanseflagg i samme kategori i samme segment, (a) og (b) som over.
Flagg i samme lag og kategori med overlappende tegnspenn telles som ett treff (en omtale).

    source scripts/miljo.sh && .venv/bin/python eval/dev/kjor_flaggoverlevelse_dev.py
"""
import collections
import datetime
import difflib  # noqa: F401
import json
import math
import pathlib
import re
import sys

HER = pathlib.Path(__file__).resolve().parent
REPO = HER.parent.parent
sys.path.insert(0, str(REPO))
from arkivklarering import personvern  # noqa: E402

DEV = sorted(HER.glob("KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_*.json"))[-1]  # siste kjøring (nyeste dato)
DATO = datetime.date.today().isoformat()
KONFIGER = {"nn": "ra/nn", "matchet": "ra/matchet"}  # lagnavn -> nøkkel for rålaget; normalisert utledes
SPRAK = {"bm": "nb", "nn": "nn"}


def omtaler(flagg):
    """Slår sammen flagg med samme kategori og overlappende tegnspenn til omtaler."""
    ut = []
    for f in sorted(flagg, key=lambda f: (f.kategori, f.start, f.stopp)):
        if ut and ut[-1].kategori == f.kategori and f.start < ut[-1].stopp:
            sist = ut[-1]
            if f.stopp > sist.stopp:
                sist.utdrag = sist.utdrag + f.utdrag[sist.stopp - f.start:] if f.start <= sist.stopp else sist.utdrag
                sist.stopp = f.stopp
            sist.score = max(sist.score, f.score)
        else:
            ut.append(personvern.Flagg(f.start, f.stopp, f.kategori, f.kilde, f.score, f.utdrag))
    return ut


def ord_(s):
    return {w for w in re.sub(r"[^\w\s]", " ", s.lower()).split() if len(w) > 1}


def streng_treff(a, b):
    la, lb = a.lower().strip(), b.lower().strip()
    return bool(ord_(a) & ord_(b)) or (la and lb and (la in lb or lb in la))


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()  # avbryter hvis cacher og tmp ikke ligger under ARKIVKLARERING_DATA
    dev = json.loads(DEV.read_text(encoding="utf-8"))
    motor = personvern.lag_motor()
    kat = sorted({v for v in personvern.KATEGORI.values()})
    # c[(konfig, kilde)][kategori] -> tellere; kilde: ra, normalisert, union
    c = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    ref_antall = collections.Counter()
    segm_med_ref = collections.Counter()
    for s in dev["segmenter"]:
        sprak = SPRAK[s["orthography"]]
        ref = omtaler(personvern.flagg_tekst(s["fasit"], sprak, motor))
        for r in ref:
            pass
        per_kat_ref = collections.defaultdict(list)
        for r in ref:
            per_kat_ref[r.kategori].append(r)
        for k, v in per_kat_ref.items():
            ref_antall[k] += len(v)
            segm_med_ref[k] += 1
        for navn, ra_nokkel in KONFIGER.items():
            nor_nokkel = ra_nokkel.replace("ra/", "normalisert/")
            lagflagg = {}
            for lag, nokkel in (("ra", ra_nokkel), ("normalisert", nor_nokkel)):
                fl = omtaler(personvern.flagg_tekst(s["hyp"][nokkel], sprak, motor)) if s["hyp"][nokkel].strip() else []
                for f in fl:
                    f.lag, f.cue_start, f.cue_stopp = lag, 0.0, float(s["duration"])
                lagflagg[lag] = fl
            union = personvern.slaa_sammen_lag(lagflagg)
            kilder = {"ra": [(f.kategori, [f.utdrag]) for f in lagflagg["ra"]],
                      "normalisert": [(f.kategori, [f.utdrag]) for f in lagflagg["normalisert"]],
                      "union": [(u.kategori, [x["utdrag"] for x in u.per_lag.values()]) for u in union]}
            for kilde, pf in kilder.items():
                t = c[(navn, kilde)]
                for k in kat:
                    refs = per_kat_ref.get(k, [])
                    pfk = [u for kk, u in pf if kk == k]
                    t[k]["ref"] += len(refs)
                    t[k]["ref_a"] += sum(1 for _ in refs if pfk)
                    t[k]["ref_b"] += sum(1 for r in refs if any(streng_treff(r.utdrag, x) for u in pfk for x in u))
                    t[k]["pred"] += len(pfk)
                    t[k]["ekstra_a"] += len(pfk) if not refs else 0
                    t[k]["ekstra_b"] += sum(1 for u in pfk if not any(streng_treff(r.utdrag, x) for r in refs for x in u))
    ut = {"merknad": "DEV, ikke pilot", "datasett": "Sprakbanken/nb_samtale, validation, 60 segmenter (KLAR-EVAL-0003)",
          "referanseflagg": dict(ref_antall), "segmenter_med_referanseflagg": dict(segm_med_ref), "resultat": {}}
    for (navn, kilde), t in c.items():
        for k in kat:
            x = t[k]
            if x["ref"] == 0 and x["pred"] == 0:
                continue
            ut["resultat"][f"{navn}|{kilde}|{k}"] = {
                "ref": x["ref"], "overlevd_a": x["ref_a"], "overlevelse_a": None if not x["ref"] else round(x["ref_a"] / x["ref"], 3),
                "overlevelse_a_ki95": wilson(x["ref_a"], x["ref"]),
                "overlevd_b": x["ref_b"], "overlevelse_b": None if not x["ref"] else round(x["ref_b"] / x["ref"], 3),
                "pipeline": x["pred"], "ekstra_a": x["ekstra_a"], "ekstra_andel_a": None if not x["pred"] else round(x["ekstra_a"] / x["pred"], 3),
                "ekstra_b": x["ekstra_b"], "ekstra_andel_b": None if not x["pred"] else round(x["ekstra_b"] / x["pred"], 3)}
    sti = REPO / "docs" / f"KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.0_{DATO}.json"
    sti.write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(sti)


if __name__ == "__main__":
    main()
