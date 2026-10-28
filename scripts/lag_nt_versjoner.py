#!/usr/bin/env python3
"""Lager før/etter-tabeller (før -nt / etter -nt for rålaget, KLAR-ADR-0017) for de berørte EVAL-ene fra to sett resultatfiler.

    .venv/bin/python scripts/lag_nt_versjoner.py <ny-mappe> [--ut <mappe>]

`<ny-mappe>` er `resultater/` fra `scripts/reproduser.sh`. «Før» leses fra de committede filene (versjonene før -nt). Skriver
Markdown-tabeller til stdout/`--ut` og ingen kvalitetspåstander: bare tall. Tolkning skrives for hånd i EVAL-dokumentene.
"""
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent


def f3(x):
    return "–" if x is None else f"{x:.3f}".replace(".", ",")


def siste(mønster, rot=REPO, som=-1):
    fs = sorted(pathlib.Path(rot).glob(mønster))
    return fs[som] if fs else None


def les(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def t_eval0002(for_, etter):
    """WER totalt og per skriftform for de fire oppsettene."""
    rader = ["| oppsett | gruppe | n | før -nt | etter -nt |", "|---|---|---|---|---|"]
    for kol in ("ra/matchet", "ra/nn", "normalisert/matchet", "normalisert/nn"):
        for g in ("totalt", "skrift:bm", "skrift:nn"):
            rader.append(f"| {kol} | {g} | {for_['wer'][kol][g + '_n']} | {f3(for_['wer'][kol][g])} | {f3(etter['wer'][kol][g])} |")
    return "\n".join(rader)


def _surv(res):
    ut = {}
    for g, d in res.items():
        for k, v in d["kategorier"].items():
            ut[(g, k)] = (v["overlevd_a"], v["ref"])
    return ut


def t_overlevelse(for_, etter):
    """Overlevelse (a) per målform, kategori og kilde (rålag/normalisert/union), samlet over målformer."""
    a, b = _surv(for_["resultat"]), _surv(etter["resultat"])
    rader = ["| kategori | lag | målform | før -nt | etter -nt |", "|---|---|---|---|---|"]
    for kat in ("person", "sted"):
        for kilde in ("ra", "normalisert", "union"):
            tot_a = [0, 0]
            tot_b = [0, 0]
            for g in ("nb", "nn"):
                x, y = a.get((g, f"{kilde}|{kat}"), (0, 0)), b.get((g, f"{kilde}|{kat}"), (0, 0))
                rader.append(f"| {kat} | {kilde} | {'bokmål' if g == 'nb' else 'nynorsk'} | {x[0]}/{x[1]} ({f3(x[0] / x[1]) if x[1] else '–'}) | {y[0]}/{y[1]} ({f3(y[0] / y[1]) if y[1] else '–'}) |")
                tot_a[0] += x[0]; tot_a[1] += x[1]; tot_b[0] += y[0]; tot_b[1] += y[1]
            rader.append(f"| {kat} | {kilde} | **samlet** | {tot_a[0]}/{tot_a[1]} ({f3(tot_a[0] / tot_a[1]) if tot_a[1] else '–'}) | {tot_b[0]}/{tot_b[1]} ({f3(tot_b[0] / tot_b[1]) if tot_b[1] else '–'}) |")
    return "\n".join(rader)


def t_eval0008(for_, etter):
    """Flagg-treff (union, begge målformer) per klasse, konfigurasjon matchet og nn."""
    rader = ["| konfigurasjon | kategori | før -nt | etter -nt |", "|---|---|---|---|"]
    kats = ["person", "sted", "dato", "fødselsår", "telefon", "fødselsnummer", "e-post", "helse", "økonomi", "konflikt", "religion", "politikk"]
    for konf in ("matchet", "nn"):
        for k in kats:
            def sum_(j):
                n = fl = 0
                for mf in ("nb", "nn"):
                    d = j["resultat"][konf]["elementer"].get(f"union|{mf}", {}).get(k)
                    if d:
                        n += d["n"]; fl += d["flagg"]
                return fl, n
            x, y = sum_(for_), sum_(etter)
            rader.append(f"| {konf} | {k} | {x[0]}/{x[1]} | {y[0]}/{y[1]} |")
    return "\n".join(rader)


def t_eval0010(for_, etter):
    rader = ["| lag | målform | betingelse | n | før -nt (EVAL-0010 v1.1) | etter -nt |", "|---|---|---|---|---|---|"]
    for cond in ("for", "etter"):
        for k in for_["wer"][cond]:
            lag, g = k.split("|")
            rader.append(f"| {lag} | {g} | {'ren lyd' if cond == 'for' else 'degradert'} | {for_['wer'][cond][k]['n']} | {f3(for_['wer'][cond][k]['wer'])} | {f3(etter['wer'][cond][k]['wer'])} |")
    return "\n".join(rader)


def t_h4(for_, etter):
    rader = ["| kategori | før -nt | etter -nt | terskel | vurdering etter -nt |", "|---|---|---|---|---|"]
    ef = {r["kategori"]: r for r in etter["union"]}
    for r in for_["union"]:
        e = ef[r["kategori"]]
        rader.append(f"| {r['kategori']} | {r['flagg_treff']}/{r['n']} | {e['flagg_treff']}/{e['n']} | {r['terskel']} | {e['vurdering']} |")
    return "\n".join(rader)


def main():
    ny = pathlib.Path(sys.argv[1])
    ut = {}
    p = siste("eval/dev/KLAR-EVAL-0002*v1.0_*.json")
    q = siste("eval/dev/KLAR-EVAL-0002*v1.0_*.json", ny)
    if p and q:
        ut["EVAL-0002"] = t_eval0002(les(p), les(q))
    p = siste("docs/KLAR-EVAL-0006*v1.1_*.json")
    q = siste("docs/KLAR-EVAL-0006*v1.1_*.json", ny)
    if p and q:
        ut["EVAL-0006 v1.1 (ordtider)"] = t_overlevelse(les(p), les(q))
    p = siste("docs/KLAR-EVAL-0007*v1.0_*.json")
    q = siste("docs/KLAR-EVAL-0007*v1.0_*.json", ny)
    if p and q:
        ut["EVAL-0007"] = t_overlevelse(les(p), les(q))
    p = siste("docs/KLAR-EVAL-0008*v1.1_*.json")
    q = siste("docs/KLAR-EVAL-0008*v1.1_*.json", ny)
    if p and q:
        ut["EVAL-0008"] = t_eval0008(les(p), les(q))
    p = siste("docs/KLAR-EVAL-0010*v1.0_*.json")
    q = siste("docs/KLAR-EVAL-0010*v1.0_*.json", ny)
    if p and q:
        ut["EVAL-0010"] = t_eval0010(les(p), les(q))
    p = siste("eval/dev/h4_torrtest_justeringsmanus_*.json")
    q = siste("eval/dev/h4_torrtest_justeringsmanus_*.json", ny)
    if p and q:
        ut["H4-tørrtest"] = t_h4(les(p), les(q))
    for k, v in ut.items():
        print(f"## {k}\n\n{v}\n")


if __name__ == "__main__":
    main()
