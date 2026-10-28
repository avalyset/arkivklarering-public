#!/usr/bin/env python3
"""95 %-intervaller for testdelene, regnet fra resultat-JSON. Leser bare filer; analysekoden (eval/dev, kalibrering) er ikke berørt.

Metoden følger KLAR-PREREG-0001 («Statistical models & analysis plan»): korpus-WER med **clusterbootstrap over taler** (NB Samtale `speaker_id`),
2000 gjentak, seed 20261026; K1 (rålag mot normalisert lag, matchet) med **parret** clusterbootstrap (samme trukne talere for begge lag); proporsjoner
(H2, H3, H4) med **Wilson-95 %** (z = 1,96). Intervalltypen var ikke spesifisert i PREREG og er låst her før noen testdel er åpnet (KLAR-LOG-0001,
KLAR-PREREG-0001 «Avvik etter registrering»): **persentilintervall** av de sorterte bootstrap-verdiene, nedre = element int(0,025·B), øvre =
element int(0,975·B) − 1 (0-indeksert), B = 2000. Per gjentak trekkes like mange talere som det finnes (med tilbakelegging), og alle segmentene til de
trukne talerne tas med; WER = sum av feil / sum av referanseord (som jiwer.wer på hele korpuset).

    .venv/bin/python scripts/rapporter_intervaller.py wer    <resultat-json> <utvalg-json> [--ut <fil.md>]
    .venv/bin/python scripts/rapporter_intervaller.py flagg  <resultat-json>            (KLAR-EVAL-0007/-0006-format: overlevelse per kategori)
    .venv/bin/python scripts/rapporter_intervaller.py h4     <resultat-json>            (kjor_h4.py-format: flaggtreff per kategori)
    .venv/bin/python scripts/rapporter_intervaller.py norne  <resultat-json> [<setninger-json>]   (KLAR-EVAL-0005-format: recall og presisjon)

NorNE (H3): Wilson fra de aggregerte tellerne, og med <setninger-json> (tellere per setning, `<resultat>.setninger.json` fra `kjor_personvern_dev.py`)
også **bootstrap over setninger** (PREREG: «NorNE: bootstrap over setninger»): per gruppe (målform, type, motor, variant) trekkes like mange setninger som det
finnes, med tilbakelegging, B = 2000, `numpy.random.default_rng(20261026)` brukt i rekkefølgen av sorterte gruppenøkler; recall = Σ treff / Σ gull og
presisjon = Σ treff / Σ predikert over de trukne setningene; samme persentilregel som for WER.
"""
import argparse
import json
import math
import pathlib
import random
import re
import sys

B = 2000
SEED = 20261026
KOLONNER = ("ra/nn", "ra/matchet", "normalisert/nn", "normalisert/matchet")


def norm(t):
    t = re.sub(r"[^\w\s]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


def persentil(verdier, b=B):
    v = sorted(verdier)
    return (v[int(0.025 * b)], v[int(0.975 * b) - 1])


def feil_og_ord(ref, hyp):
    import jiwer
    o = jiwer.process_words(norm(ref), norm(hyp))
    return o.substitutions + o.deletions + o.insertions, len(norm(ref).split())


def wer_intervaller(res, utvalg, b=B, seed=SEED):
    """{(kolonne, gruppe): {wer, ki95, n_segmenter, n_talere}} og K1 {differanse, ki95, utelukker_0}. Clusterbootstrap over speaker_id."""
    tal = {f'{r["source_file_id"]}_{r["segment_id"]}': r["speaker_id"] for r in utvalg}
    seg = res["segmenter"]
    talere = sorted({tal[s["id"]] for s in seg})
    gr = {"totalt": lambda s: True, "skrift:bm": lambda s: s["orthography"] == "bm", "skrift:nn": lambda s: s["orthography"] == "nn"}
    tellere = {}  # (kolonne, gruppe) -> {taler: [feil, ord]}
    for kol in KOLONNER:
        for g, f in gr.items():
            d = {t: [0, 0] for t in talere}
            for s in seg:
                if f(s):
                    e, n = feil_og_ord(s["fasit"], s["hyp"][kol])
                    d[tal[s["id"]]][0] += e
                    d[tal[s["id"]]][1] += n
            tellere[(kol, g)] = d
    rng = random.Random(seed)
    trekk = [[talere[rng.randrange(len(talere))] for _ in talere] for _ in range(b)]  # samme trekk brukes for alle kolonner og grupper (parret)
    ut = {}
    for (kol, g), d in tellere.items():
        e, n = sum(v[0] for v in d.values()), sum(v[1] for v in d.values())
        vs = [sum(d[t][0] for t in tr) / max(1, sum(d[t][1] for t in tr)) for tr in trekk]
        ut[(kol, g)] = {"wer": e / n, "ki95": persentil(vs, b), "n_segmenter": sum(1 for s in seg if gr[g](s)), "n_talere": sum(1 for v in d.values() if v[1])}
    a, c = tellere[("normalisert/matchet", "totalt")], tellere[("ra/matchet", "totalt")]
    diff = [(sum(a[t][0] for t in tr) / sum(a[t][1] for t in tr)) - (sum(c[t][0] for t in tr) / sum(c[t][1] for t in tr)) for tr in trekk]
    pe = (sum(v[0] for v in a.values()) / sum(v[1] for v in a.values())) - (sum(v[0] for v in c.values()) / sum(v[1] for v in c.values()))
    lo, hi = persentil(diff, b)
    return ut, {"differanse_normalisert_minus_ra": pe, "ki95": (lo, hi), "utelukker_0": lo > 0 or hi < 0}


def f3(x):
    return "–" if x is None else f"{x:.3f}".replace(".", ",")


def md_wer(ut, k1):
    r = ["| kolonne | gruppe | WER | 95 %-intervall (clusterbootstrap, taler) | segmenter | talere |", "|---|---|---|---|---|---|"]
    for (kol, g), v in ut.items():
        r.append(f"| {kol} | {g} | {f3(v['wer'])} | {f3(v['ki95'][0])}–{f3(v['ki95'][1])} | {v['n_segmenter']} | {v['n_talere']} |")
    r += ["", f"K1 (normalisert/matchet minus ra/matchet, totalt, parret): {f3(k1['differanse_normalisert_minus_ra'])}, 95 %-intervall {f3(k1['ki95'][0])}–{f3(k1['ki95'][1])}; utelukker 0: {'ja' if k1['utelukker_0'] else 'nei'}."]
    return "\n".join(r)


def flagg_tabell(res):
    r = ["| kategori | lag | målform | overlevd/ref | andel | Wilson 95 % |", "|---|---|---|---|---|---|"]
    tot = {}
    for g in ("nb", "nn"):
        for nokkel, v in res["resultat"][g]["kategorier"].items():
            t = tot.setdefault(nokkel, [0, 0])
            t[0] += v["overlevd_a"]; t[1] += v["ref"]
            lo, hi = wilson(v["overlevd_a"], v["ref"])
            r.append(f"| {nokkel.split('|')[1]} | {nokkel.split('|')[0]} | {g} | {v['overlevd_a']}/{v['ref']} | {f3(v['overlevd_a'] / v['ref']) if v['ref'] else '–'} | {f3(lo)}–{f3(hi)} |")
    for nokkel, (k, n) in tot.items():
        lo, hi = wilson(k, n)
        r.append(f"| {nokkel.split('|')[1]} | {nokkel.split('|')[0]} | samlet | {k}/{n} | {f3(k / n) if n else '–'} | {f3(lo)}–{f3(hi)} |")
    return "\n".join(r)


def h4_tabell(res):
    r = ["| kategori | treff/n | andel | Wilson 95 % | terskel | vurdering |", "|---|---|---|---|---|---|"]
    for x in res["union"]:
        lo, hi = wilson(x["flagg_treff"], x["n"])
        r.append(f"| {x['kategori']} | {x['flagg_treff']}/{x['n']} | {f3(x['flagg_treff'] / x['n']) if x['n'] else '–'} | {f3(lo)}–{f3(hi)} | {x['terskel']} | {x['vurdering']} |")
    return "\n".join(r)


SPRAK = {"bokmaal": "nb", "nynorsk": "nn"}


def norne_bootstrap(setn, b=B, seed=SEED):
    """{(målform, type, motor, variant): {recall: (punkt, lo, hi), presisjon: (...), n_setninger}} fra tellere per setning."""
    import numpy as np
    k = setn["kolonner"]
    grupper = {}
    for rad in setn["rader"]:
        r = dict(zip(k, rad))
        grupper.setdefault((SPRAK[r["config"]], r["type"], r["motor"], r["variant"]), []).append(r)
    rng = np.random.default_rng(seed)
    ut = {}
    for nokkel in sorted(grupper):
        rs = grupper[nokkel]
        n = len(rs)
        a = {x: np.array([r[x] for r in rs]) for x in ("gull", "gull_overlapp", "pred", "pred_overlapp")}
        idx = rng.integers(0, n, size=(b, n))
        ut[nokkel] = {"n_setninger": n}
        for navn, teller, nevner in (("recall", "gull_overlapp", "gull"), ("presisjon", "pred_overlapp", "pred")):
            punkt = a[teller].sum() / a[nevner].sum() if a[nevner].sum() else None
            if punkt is None:
                ut[nokkel][navn] = (None, None, None)
                continue
            nev = a[nevner][idx].sum(axis=1)
            verdier = np.sort(a[teller][idx].sum(axis=1)[nev > 0] / nev[nev > 0]).tolist()
            lo, hi = (verdier[int(0.025 * len(verdier))], verdier[int(0.975 * len(verdier)) - 1])
            ut[nokkel][navn] = (float(punkt), lo, hi)
    return ut


def norne_tabell(res, setn=None):
    bs = norne_bootstrap(setn) if setn else {}
    kol = "| målform|type|motor|variant | recall (overlapp) | Wilson 95 % | presisjon (overlapp) | Wilson 95 % |" + (" bootstrap recall (setninger) | bootstrap presisjon (setninger) |" if setn else "")
    r = [kol, "|---|---|---|---|---|" + ("---|---|" if setn else "")]
    for nokkel, v in res["resultat"].items():
        kr = round(v["recall_overlapp"] * v["gull"]) if v["recall_overlapp"] is not None else 0
        kp = round(v["presisjon_overlapp"] * v["predikert"]) if v["presisjon_overlapp"] is not None else 0
        a, b_ = wilson(kr, v["gull"]), wilson(kp, v["predikert"])
        rad = f"| {nokkel} | {f3(v['recall_overlapp'])} | {f3(a[0])}–{f3(a[1])} | {f3(v['presisjon_overlapp'])} | {f3(b_[0])}–{f3(b_[1])} |"
        if setn:
            x = bs[tuple(nokkel.split("|"))]
            rad += f" {f3(x['recall'][1])}–{f3(x['recall'][2])} | {f3(x['presisjon'][1])}–{f3(x['presisjon'][2])} |"
        r.append(rad)
    return "\n".join(r)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("hva", choices=["wer", "flagg", "h4", "norne"])
    ap.add_argument("resultat")
    ap.add_argument("utvalg", nargs="?")
    ap.add_argument("--ut")
    a = ap.parse_args(argv)
    res = json.loads(pathlib.Path(a.resultat).read_text(encoding="utf-8"))
    if a.hva == "wer":
        utv = json.loads(pathlib.Path(a.utvalg).read_text(encoding="utf-8"))["utvalg"]
        ut, k1 = wer_intervaller(res, utv)
        for (kol, g), v in ut.items():
            if g == "totalt" and abs(v["wer"] - res["wer"][kol]["totalt"]) > 5e-5:
                sys.exit(f"avvik mot resultat-JSON for {kol}: {v['wer']} mot {res['wer'][kol]['totalt']}")
        tekst = md_wer(ut, k1)
    else:
        if a.hva == "norne":
            tekst = norne_tabell(res, json.loads(pathlib.Path(a.utvalg).read_text(encoding="utf-8")) if a.utvalg else None)
        else:
            tekst = {"flagg": flagg_tabell, "h4": h4_tabell}[a.hva](res)
    print(tekst)
    if a.ut:
        pathlib.Path(a.ut).write_text(tekst + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
