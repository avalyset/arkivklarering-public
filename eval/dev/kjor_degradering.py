#!/usr/bin/env python3
"""SIMULERT DEGRADERING (DEV, ikke pilot): WER for rålaget (målform matchet) og flaggoverlevelse før og etter båndlyd-lignende degradering
av de 60 NB Samtale validation-segmentene (KLAR-EVAL-0003).

«Før» og «etter» kjøres her med samme oppsett og samme kode (språk etter målform, begge lag med DTW-ordtidsstempler, union paret på
ordspenn), slik at forskjellen bare skyldes lyden. Degraderingen lages av `eval/dev/degrader_lyd.py` (audiomentations og ffmpeg, eget
venv). Skriver `docs/KLAR-EVAL-0010_arkivklarering_degradering-dev_v1.0_<dato>.json` og tallene i `.md`; tolkningen skrives for hånd.

    source scripts/miljo.sh && $ARKIVKLARERING_DATA/venv-degradering/bin/python eval/dev/degrader_lyd.py
    .venv/bin/python eval/dev/kjor_degradering.py
"""
import argparse
import datetime
import json
import pathlib
import random
import re
import sys
import time

HER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HER))
import felles  # noqa: E402
import kjor_flaggoverlevelse_ord as fo  # noqa: E402
from felles import legg_til_jsonl, les_jsonl  # noqa: E402

import jiwer  # noqa: E402

from arkivklarering import miljo, personvern, transkriber  # noqa: E402

REPO = HER.parent.parent
DATO = datetime.date.today().isoformat()
CACHE = miljo.EVAL_DATA
DEGRADERT = miljo.DATA / "lyd" / "degradert" / "nbsamtale_validation"
SPRAK = {"nb": "no", "nn": "nn"}
SEED = 20261026
MERKE = "**SIMULERT DEGRADERING (DEV, ikke pilot): båndlyd-lignende støy lagt på ren NB Samtale-lyd. Ikke ekte båndlyd.**"


def norm(t):
    t = re.sub(r"[^\w\s]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def tekst_lag(c, lag):
    return " ".join(x["tekst"] for x in c["cues"].get(lag, []))


def wer(par):
    return jiwer.wer([r for r, _ in par], [h or "" for _, h in par]) if par else None


def wer_ki(par, n=2000):
    rng = random.Random(SEED)
    verdier = sorted(wer([par[rng.randrange(len(par))] for _ in par]) for _ in range(n))
    return [round(verdier[int(0.025 * n)], 3), round(verdier[int(0.975 * n) - 1], 3)]


def kjor(items, cache_sti):
    cache = les_jsonl(cache_sti)
    igjen = [i for i in items if i["id"] not in cache]
    print(f"{cache_sti.name}: {len(igjen)} av {len(items)} gjenstår", flush=True)
    oppsett = {lag: transkriber.finn_oppsett(lag) for lag in transkriber.LAG}
    gb = felles.gjenbruk_normalisert(cache_sti, oppsett["normalisert"], lambda *x: print(*x, flush=True))
    t0 = time.time()
    for i0 in range(0, len(igjen), 40):
        ut = felles.kjor_batch(igjen[i0:i0 + 40], oppsett, ordtider=True, logg=lambda *x: print(*x, flush=True), gjenbruk=gb)
        for it in igjen[i0:i0 + 40]:
            legg_til_jsonl(cache_sti, ut[it["id"]])
        print(f"  {min(i0 + 40, len(igjen))}/{len(igjen)} ({time.time() - t0:.0f} s)", flush=True)
    return les_jsonl(cache_sti)


def wer_tabell(items, cache):
    ut = {}
    for lag in ("ra", "normalisert"):
        for g in ("nb", "nn", "samlet"):
            par = [(norm(i["ref"]), norm(tekst_lag(cache[i["id"]], lag))) for i in items if i["id"] in cache and (g == "samlet" or i["gruppe"] == g)]
            ut[f"{lag}|{g}"] = {"n": len(par), "wer": round(wer(par), 3) if par else None, "ki95_segmentbootstrap": wer_ki(par) if par else None}
    return ut


def overlevelse(res):
    """Union, rålag og normalisert lag for person og sted, per målform og samlet: {nøkkel: (overlevd, n)}."""
    ut = {}
    for kilde in ("ra", "normalisert", "union"):
        for k in fo.MALT:
            tot_o = tot_n = 0
            for g in ("nb", "nn"):
                x = res.get(g, {}).get("kategorier", {}).get(f"{kilde}|{k}")
                o, n = (x["overlevd_a"], x["ref"]) if x else (0, 0)
                ut[f"{kilde}|{k}|{g}"] = (o, n)
                tot_o += o
                tot_n += n
            ut[f"{kilde}|{k}|samlet"] = (tot_o, tot_n)
    return ut


def f3(x):
    return "–" if x is None else f"{x:.3f}".replace(".", ",")


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    argparse.ArgumentParser().parse_args()
    base = fo.items_nbsamtale()
    for i in base:
        i["whisper_sprak"] = SPRAK[i["gruppe"]]
    if len(list(DEGRADERT.glob("*.wav"))) != len(base):
        sys.exit("kjør eval/dev/degrader_lyd.py først")
    deg = [{**i, "id": i["id"], "lyd": str(DEGRADERT / f"{i['id']}.wav")} for i in base]
    c_for = kjor(base, felles.cache_sti(CACHE, "deg_original"))  # følger segmenteringen (felles.cache_sti)
    c_etter = kjor(deg, felles.cache_sti(CACHE, "deg_degradert"))
    motor = personvern.lag_motor()
    res_for, res_etter = fo.evaluer(base, c_for, motor), fo.evaluer(deg, c_etter, motor)
    w_for, w_etter = wer_tabell(base, c_for), wer_tabell(deg, c_etter)
    o_for, o_etter = overlevelse(res_for), overlevelse(res_etter)
    param = json.loads((DEGRADERT.parent / "degradert_nbsamtale_validation.sha256.json").read_text(encoding="utf-8"))["parametre"]
    ut = {"merknad": "SIMULERT DEGRADERING (DEV, ikke pilot)", "datasett": "Sprakbanken/nb_samtale, validation, 60 segmenter (KLAR-EVAL-0003)",
          "degradering": param, "oppsett": "språk etter målform; rålag og normalisert lag med DTW-ordtidsstempler; union paret på ordspenn",
          "wer": {"for": w_for, "etter": w_etter}, "overlevelse_a": {"for": res_for, "etter": res_etter}}
    stub = REPO / "docs" / f"KLAR-EVAL-0010_arkivklarering_degradering-dev_v1.0_{DATO}"
    pathlib.Path(str(stub) + ".json").write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    L = ["# KLAR-EVAL-0010: Robusthet for båndlyd (simulert degradering, DEV)", "", MERKE, "",
         f"Versjon 1.0, {DATO}. DEV, ikke pilot. Tall generert av `eval/dev/kjor_degradering.py`; tolkning skrevet for hånd (under «Vurdering»).", "",
         "## Oppsett", "",
         "- **Materiale:** de samme 60 NB Samtale validation-segmentene som KLAR-EVAL-0002, -0003 og -0006 (CC0, se KLAR-EVAL-0004). Referanse for WER: `orthographic`; referanse for flaggene: personvernmotoren på referanseteksten.",
         "- **Degradering** (`eval/dev/degrader_lyd.py`, audiomentations 0.43.1 og ffmpeg, eget venv): " + "; ".join(f"{k}: {v}" for k, v in param.items() if k != "samplingsfrekvens") + ". Fast seed per segment. Parametrene er valgt for å ligne smalbånds båndlyd, ikke målt mot noen ekte båndmaskin.",
         "- **Rørledning:** som i KLAR-EVAL-0006 v1.1, men **språk etter målform** (bokmål `-l no`, nynorsk `-l nn`, «matchet»). «Før» er kjørt på nytt her med samme kode som «etter», og er derfor ikke bitidentisk med KLAR-EVAL-0002 (rålag/matchet 0,250 der).",
         "- **WER:** korpus-WER (jiwer), små bokstaver og tegnsetting fjernet; 95 %-intervall fra bootstrap over segmenter (2000 gjentak, seed 20261026). Intervallene er for smale: segmentene kommer fra få talere og er ikke uavhengige.",
         "- **Flaggoverlevelse (a):** andelen referanseflagg i kategorien som har minst ett rørledningsflagg i samme kategori i samme segment. Bare person og sted måles (n er lite: se tabellen).", "",
         "## WER (korpus, 60 segmenter)", "", "| lag | målform | n | før | 95 %-int. | etter | 95 %-int. |", "|---|---|---|---|---|---|---|"]
    for k in w_for:
        lag, g = k.split("|")
        a, b = w_for[k], w_etter[k]
        L.append(f"| {'rålag (hovedutfall)' if lag == 'ra' else 'normalisert'} | {g} | {a['n']} | {f3(a['wer'])} | {a['ki95_segmentbootstrap'][0]}–{a['ki95_segmentbootstrap'][1]} | {f3(b['wer'])} | {b['ki95_segmentbootstrap'][0]}–{b['ki95_segmentbootstrap'][1]} |".replace(".", ",").replace("–", "–"))
    L += ["", "## Flaggoverlevelse (a): overlevd / referanseflagg", "", "| kategori | lag | målform | før | etter |", "|---|---|---|---|---|"]
    for k in o_for:
        kilde, kat, g = k.split("|")
        a, b = o_for[k], o_etter[k]
        if not a[1] and not b[1]:
            continue
        L.append(f"| {kat} | {kilde} | {g} | {a[0]}/{a[1]} ({f3(a[0] / a[1]) if a[1] else '–'}) | {b[0]}/{b[1]} ({f3(b[0] / b[1]) if b[1] else '–'}) |")
    L += ["", "Rådata: `" + pathlib.Path(str(stub) + ".json").name + "` (bare tall).", ""]
    pathlib.Path(str(stub) + ".md").write_text("\n".join(L), encoding="utf-8")
    print(str(stub) + ".md")
    for k in ("ra|samlet", "normalisert|samlet"):
        print(k, "WER før", w_for[k]["wer"], "etter", w_etter[k]["wer"])
    for k in ("union|person|samlet", "union|sted|samlet"):
        print(k, "før", o_for[k], "etter", o_etter[k])


if __name__ == "__main__":
    main()
