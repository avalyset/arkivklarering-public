#!/usr/bin/env python3
"""DEV-måling (IKKE pilot): recall og presisjon for personer (PER) og steder (LOC, GPE_LOC) på NorNE.

Datasett: NbAiLab/norne (revisjon 1ca12d43…), configene `bokmaal` og `nynorsk`, KUN validation-delen.
test-delen er sperret (arkivklarering/evaldata.py) og krever --prereg-id KLAR-PREREG-<NNNN>.
Ingen setninger skrives ut eller lagres; resultatene er bare tall (lisensen dekker annotasjonene, ikke
gjenpublisering av originaltekstene, se KLAR-EVAL-0005).

Gull: PER -> person. LOC og GPE_LOC -> sted (GPE_ORG regnes som organisasjon og evalueres ikke).
Prediksjon: flagg med kategori «person» og «sted». Overlappende prediksjoner av samme type slås sammen.
  recall (overlapp):  andel gullentiteter som overlappes av minst én prediksjon av samme type (hovedmål)
  recall (nøyaktig):  andel gullentiteter med prediksjon med identisk start og slutt og samme type
  presisjon (overlapp / nøyaktig): tilsvarende for prediksjonene
Konfigurasjoner: kombinert (hele motoren), bert (bare NB-BERT-base-ner), spacy (bare spaCy-modellen).
Tekstformer: original (setningen slik NorNE har den) og små bokstaver uten tegnsetting (som rålaget).

    source scripts/miljo.sh && .venv/bin/python eval/dev/kjor_personvern_dev.py
"""
import argparse
import collections
import datetime
import json
import math
import pathlib
import sys
import time

import pyarrow.parquet as pq

HER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HER.parent.parent))
from arkivklarering import evaldata, miljo, personvern  # noqa: E402

DATA = miljo.EVAL_DATA / "norne"
REVISJON = "1ca12d437b84f65a34c454d339317d39d35c8149"
MALFORM = {"bokmaal": "nb", "nynorsk": "nn"}
GULL_TYPE = {"PER": "person", "LOC": "sted", "GPE_LOC": "sted"}
ETIKETTER = ['O', 'B-PER', 'I-PER', 'B-ORG', 'I-ORG', 'B-GPE_LOC', 'I-GPE_LOC', 'B-PROD', 'I-PROD', 'B-LOC', 'I-LOC',
             'B-GPE_ORG', 'I-GPE_ORG', 'B-DRV', 'I-DRV', 'B-EVT', 'I-EVT', 'B-MISC', 'I-MISC']
DATO = datetime.date.today().isoformat()


def gull_spenn(tokens, tags):
    """Token-intervaller (i, j, type) for PER/LOC/GPE_LOC fra BIO-etiketter."""
    ut, i = [], 0
    while i < len(tokens):
        e = ETIKETTER[tags[i]]
        if e.startswith("B-") and e[2:] in GULL_TYPE:
            j = i + 1
            while j < len(tokens) and ETIKETTER[tags[j]] == "I-" + e[2:]:
                j += 1
            ut.append((i, j, GULL_TYPE[e[2:]]))
            i = j
        else:
            i += 1
    return ut


def original_variant(text, tokens):
    """Tegnposisjoner for hvert token i originalteksten; None hvis et token ikke finnes i rekkefølge."""
    pos, ut = 0, []
    for t in tokens:
        k = text.find(t, pos)
        if k < 0:
            return None
        ut.append((k, k + len(t)))
        pos = k + len(t)
    return ut


def smaa_variant(tokens):
    """Små bokstaver, uten tokens som bare er tegnsetting, ett mellomrom mellom. Returnerer (tekst, spenn per token|None)."""
    deler, spenn, pos = [], [], 0
    for t in tokens:
        if not any(c.isalnum() for c in t):
            spenn.append(None)
            continue
        if deler:
            pos += 1
        spenn.append((pos, pos + len(t)))
        deler.append(t.lower())
        pos += len(t)
    return " ".join(deler), spenn


def slaa_sammen(spenn):
    ut = []
    for a, b, t in sorted(spenn):
        if ut and ut[-1][2] == t and a < ut[-1][1]:
            ut[-1] = (ut[-1][0], max(b, ut[-1][1]), t)
        else:
            ut.append((a, b, t))
    return ut


def overlapper(a, b):
    return a[2] == b[2] and a[0] < b[1] and b[0] < a[1]


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


TELLERE = ("gull", "gull_overlapp", "gull_noyaktig", "pred", "pred_overlapp", "pred_noyaktig")


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()  # avbryter hvis cacher og tmp ikke ligger under ARKIVKLARERING_DATA
    ap = argparse.ArgumentParser()
    ap.add_argument("--splitt", default="validation", choices=evaldata.SPLITT)
    ap.add_argument("--prereg-id")
    ap.add_argument("--ut-mappe", default=str(HER.parent.parent / "docs"), help="mappe for resultatfila (standard: docs)")
    ap.add_argument("--etikett", default="DEV", choices=["DEV", "TEST"], help="DEV (standard) eller TEST («TEST – preregistrert (OSF hc83q)» i merknaden)")
    ap.add_argument("--eval-nr", help="KLAR-EVAL-<NNNN> for resultatfila (standard: KLAR-EVAL-0005, som i DEV)")
    ap.add_argument("--maks", type=int, default=0, help="bare de første N setningene per målform (røyktest)")
    a = ap.parse_args()
    evaldata.sjekk_splitt(a.splitt, a.prereg_id)

    t0 = time.time()
    from presidio_analyzer.nlp_engine import NerModelConfiguration, SpacyNlpEngine
    ner = NerModelConfiguration(default_score=0.6, model_to_presidio_entity_mapping=dict(personvern.ETIKETT))
    nlp = SpacyNlpEngine(models=[{"lang_code": s, "model_name": personvern.SPACY_MODELL} for s in personvern.SPRAK],
                         ner_model_configuration=ner)
    nlp.load()
    bert = personvern.lag_bert_rorledning()
    motorer = {"kombinert": personvern.lag_motor(("spacy", "bert", "monster"), nlp_motor=nlp, bert_rorledning=bert),
               "bert": personvern.lag_motor(("bert",), nlp_motor=nlp, bert_rorledning=bert),
               "spacy": personvern.lag_motor(("spacy",), nlp_motor=nlp)}
    print(f"motorer klare: {time.time() - t0:.0f} s", flush=True)

    tell = collections.defaultdict(lambda: collections.Counter())
    hoppet = collections.Counter()
    per_setning = []  # tellere per setning (egen utdatafil `.setninger.json`); de aggregerte tellene under er summen av disse
    for config, sprak in MALFORM.items():
        tab = pq.read_table(evaldata.norne_sti(DATA, config, a.splitt, a.prereg_id)).to_pylist()
        if a.maks:
            tab = tab[:a.maks]
        for rad_nr, rad in enumerate(tab):
            tokens, tags = rad["tokens"], rad["ner_tags"]
            gull = gull_spenn(tokens, tags)
            for variant in ("original", "små"):
                if variant == "original":
                    tekst = rad["text"]
                    pos = original_variant(tekst, tokens)
                    if pos is None:
                        hoppet[(config, variant)] += 1
                        continue
                else:
                    tekst, pos = smaa_variant(tokens)
                gs = []
                for i, j, typ in gull:
                    deler = [p for p in pos[i:j] if p]
                    if deler:
                        gs.append((deler[0][0], deler[-1][1], typ))
                for navn, motor in motorer.items():
                    pred = [(f.start, f.stopp, f.kategori) for f in personvern.flagg_tekst(tekst, sprak, motor)
                            if f.kategori in ("person", "sted")]
                    pred = slaa_sammen(pred)
                    for typ in ("person", "sted"):
                        g = [x for x in gs if x[2] == typ]
                        pp = [x for x in pred if x[2] == typ]
                        c = tell[(sprak, typ, navn, variant)]
                        d = {"gull": len(g), "gull_overlapp": sum(any(overlapper(x, y) for y in pp) for x in g),
                             "gull_noyaktig": sum(any(x == y for y in pp) for x in g), "pred": len(pp),
                             "pred_overlapp": sum(any(overlapper(x, y) for y in g) for x in pp),
                             "pred_noyaktig": sum(any(x == y for y in g) for x in pp)}
                        for k, v in d.items():
                            c[k] += v
                        per_setning.append([config, rad_nr, str(rad.get("idx", "")), variant, navn, typ, *(d[k] for k in TELLERE)])
        print(f"{config}: {len(tab)} setninger, {time.time() - t0:.0f} s", flush=True)

    resultat = {}
    for (sprak, typ, navn, variant), c in sorted(tell.items()):
        def r(k, n):
            return None if n == 0 else round(k / n, 3)
        lo, hi = wilson(c["gull_overlapp"], c["gull"])
        resultat[f"{sprak}|{typ}|{navn}|{variant}"] = {
            "gull": c["gull"], "predikert": c["pred"],
            "recall_overlapp": r(c["gull_overlapp"], c["gull"]), "recall_overlapp_ki95": [lo, hi],
            "recall_noyaktig": r(c["gull_noyaktig"], c["gull"]),
            "presisjon_overlapp": r(c["pred_overlapp"], c["pred"]), "presisjon_noyaktig": r(c["pred_noyaktig"], c["pred"])}
    ut = {"merknad": "DEV, ikke pilot" if a.etikett == "DEV" else "TEST – preregistrert (OSF hc83q)", "datasett": "NbAiLab/norne", "revisjon": REVISJON, "splitt": a.splitt,
          "motor": {"spacy": personvern.SPACY_MODELL, "bert": personvern.BERT_MODELL, "terskel": 0.0},
          "setninger_hoppet_over_pga_tokenjustering": {f"{k[0]}|{k[1]}": v for k, v in hoppet.items()},
          "resultat": resultat, "sekunder": round(time.time() - t0)}
    ut_mappe = pathlib.Path(a.ut_mappe)
    ut_mappe.mkdir(parents=True, exist_ok=True)
    if a.etikett == "DEV" and not a.eval_nr:
        sti = ut_mappe / f"KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_{DATO}.json"
    else:
        sti = ut_mappe / f"{a.eval_nr or 'KLAR-EVAL-0005'}_arkivklarering_personvern-{a.etikett.lower()}_v1.0_{DATO}.json"
    sti.write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(sti, flush=True)
    sti_s = sti.with_name(sti.stem + ".setninger.json")  # ikke et KLAR-dokument i nummerregisteret (navnet slutter ikke på .json rett etter datoen)
    sti_s.write_text(json.dumps({"merknad": ut["merknad"], "splitt": a.splitt, "revisjon": REVISJON,
                                 "kolonner": ["config", "rad", "idx", "variant", "motor", "type", *TELLERE], "rader": per_setning},
                                ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(sti_s, flush=True)


if __name__ == "__main__":
    main()
