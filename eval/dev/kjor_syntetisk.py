#!/usr/bin/env python3
"""SYNTETISK – kjede og flagglogikk, ikke talekvalitet. Kjører justeringsmanuset KLAR-MANUS-0001 gjennom hele rørledningen.

TTS (`say -v Nora`, bokmålsstemme; det finnes ingen nynorskstemme på maskinen) -> 16 kHz mono wav under
$ARKIVKLARERING_DATA/lyd/syntetisk/ -> segmentering -> rålag og normalisert lag (ordtidsstempler) -> personvernflagg -> union.
Scoring (vendor-score.py fra norsk-tale, KLAR-ADR-0014) per målelement og kategori:
  tekst_treff   elementet står i laget sin transkripsjon (tall normaliseres: tallord -> sifre)
  flagg_treff   et flagg i samme kategori har et utdrag som dekker elementet (per lag og i union)
Målformfeil (nb-markører i nynorsk eller omvendt) rapporteres separat og feller aldri et element.
To konfigurasjoner: matchet (nb -> no, nn -> nn) og nn (-l nn for alle, slik rørledningen kjører).

    source scripts/miljo.sh && .venv/bin/python eval/dev/kjor_syntetisk.py [--fase lyd|kjor|evaluer|alle]
"""
import argparse
import collections
import datetime
import glob
import json
import pathlib
import subprocess
import sys
import time

HER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HER))
import felles  # noqa: E402
from felles import REPO, dict_til_cue, legg_til_jsonl, les_jsonl  # noqa: E402

from arkivklarering import evaldata, kalibrering, miljo, personvern, transkriber  # noqa: E402

DATO = datetime.date.today().isoformat()
LYD = miljo.DATA / "lyd" / "syntetisk"
CACHE = miljo.EVAL_DATA
STEMME = "Nora"


def lag_lyd(manus):
    LYD.mkdir(parents=True, exist_ok=True)
    for r in manus:
        wav = LYD / f"{r['id']}.wav"
        if wav.exists():
            continue
        aiff = LYD / f"{r['id']}.aiff"
        subprocess.run(["say", "-v", STEMME, "-o", str(aiff), r["setning"]], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(aiff), "-ar", "16000", "-ac", "1", str(wav)], check=True)
        aiff.unlink()


def evaluer(manus, cache, motor):
    ut = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    malformfeil = collections.defaultdict(collections.Counter)
    bom = []
    for r in manus:
        c = cache.get(r["id"])
        if not c:
            continue
        sprak = r["malform"]
        tekst = {lag: " ".join(x["tekst"] for x in c["cues"].get(lag, [])) for lag in transkriber.LAG}
        flagg = {lag: personvern.flagg_cues([dict_til_cue(x) for x in c["cues"].get(lag, [])], lag, sprak, motor) for lag in transkriber.LAG}
        union = personvern.slaa_sammen_lag(flagg)
        kilder = {"ra": [{"kategori": f.kategori, "utdrag": f.utdrag} for f in flagg["ra"]],
                  "normalisert": [{"kategori": f.kategori, "utdrag": f.utdrag} for f in flagg["normalisert"]],
                  "union": [{"kategori": u.kategori, "utdrag": x["utdrag"]} for u in union for x in u.per_lag.values()]}
        for kilde, fl in kilder.items():
            lagtekst = tekst["normalisert"] if kilde == "union" else tekst[kilde]
            if kilde == "union":  # tekst-treff i union: elementet står i minst ett av lagene
                s_ra = kalibrering.score_flagg(r, tekst["ra"], fl)
                s_no = kalibrering.score_flagg(r, tekst["normalisert"], fl)
                elementer = [{**a, "tekst_treff": a["tekst_treff"] or b["tekst_treff"]} for a, b in zip(s_ra["elementer"], s_no["elementer"])]
                mf = s_no["malformfeil"]
            else:
                s = kalibrering.score_flagg(r, lagtekst, fl)
                elementer, mf = s["elementer"], s["malformfeil"]
            for e in elementer:
                for grp in (e["type"], "alle"):
                    t = ut[(kilde, r["malform"])][grp]
                    t["n"] += 1
                    t["tekst"] += e["tekst_treff"]
                    t["flagg"] += e["flagg_treff"]
                    t["flagg_gitt_tekst"] += (e["flagg_treff"] and e["tekst_treff"])
                    t["tekst_n_for_flagg"] += e["tekst_treff"]
                if kilde == "union" and not e["flagg_treff"]:
                    bom.append({"id": r["id"], "klasse": r["klasse"], "type": e["type"], "tekst_treff": e["tekst_treff"]})
            if kilde != "union":
                malformfeil[(kilde, r["malform"])]["n"] += 1
                malformfeil[(kilde, r["malform"])]["feil"] += bool(mf)
    res = {}
    for (kilde, mf), d in ut.items():
        res[f"{kilde}|{mf}"] = {g: dict(t) for g, t in d.items()}
    return res, {f"{k}|{m}": dict(v) for (k, m), v in malformfeil.items()}, bom


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    ap = argparse.ArgumentParser()
    ap.add_argument("--fase", default="alle", choices=["lyd", "kjor", "evaluer", "alle"])
    a = ap.parse_args()
    manus_sti = evaldata.siste_versjon(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0001_*.tsv")))
    manus = kalibrering.les_manus(manus_sti)
    if a.fase in ("lyd", "alle"):
        lag_lyd(manus)
        print(f"lyd: {len(list(LYD.glob('*.wav')))} filer i {LYD}", flush=True)
    konfiger = {"matchet": lambda r: "no" if r["malform"] == "nb" else "nn", "nn": lambda r: "nn"}
    if a.fase in ("kjor", "alle"):
        oppsett = {lag: transkriber.finn_oppsett(lag) for lag in transkriber.LAG}
        for navn, spr in konfiger.items():
            sti = felles.cache_sti(CACHE, f"ord_syntetisk_{navn}")  # følger segmenteringen (felles.cache_sti)
            cache = les_jsonl(sti)
            igjen = [{"id": r["id"], "lyd": str(LYD / f"{r['id']}.wav"), "whisper_sprak": spr(r)} for r in manus if r["id"] not in cache]
            gb = felles.gjenbruk_normalisert(sti, oppsett["normalisert"], lambda *x: print(*x, flush=True))
            print(f"{navn}: {len(igjen)} av {len(manus)} gjenstår", flush=True)
            t0 = time.time()
            for i0 in range(0, len(igjen), 40):
                ut = felles.kjor_batch(igjen[i0:i0 + 40], oppsett, ordtider=True, logg=lambda *x: print(*x, flush=True), gjenbruk=gb)
                for it in igjen[i0:i0 + 40]:
                    legg_til_jsonl(sti, ut[it["id"]])
                print(f"  {min(i0 + 40, len(igjen))}/{len(igjen)} ({time.time() - t0:.0f} s)", flush=True)
    if a.fase in ("evaluer", "alle"):
        motor = personvern.lag_motor()
        resultat = {}
        for navn in konfiger:
            cache = les_jsonl(felles.cache_sti(CACHE, f"ord_syntetisk_{navn}"))
            res, mf, bom = evaluer(manus, cache, motor)
            resultat[navn] = {"elementer": res, "malformfeil": mf, "bom_i_union": bom, "segmenter": len(cache)}
        ut = {"merknad": "SYNTETISK – kjede og flagglogikk, ikke talekvalitet", "stemme": STEMME + " (nb_NO; ingen nynorskstemme tilgjengelig)",
              "manus": pathlib.Path(manus_sti).name, "resultat": resultat}
        sti = REPO / "docs" / f"KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.1_{DATO}.json"
        sti.write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(sti)


if __name__ == "__main__":
    main()
