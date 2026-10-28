#!/usr/bin/env python3
"""DEV: sammenligner installerte ollama-modeller for katalogutkastet (KLAR-ADR-0013). Ingen sky; bare lokal ollama.

Inndata er sammenhengende utdrag av menneskelig transkripsjon fra NPSC validation (CC0): fire «sendinger» på 45 setninger (tre
bokmål, én nynorsk), trukket med fast seed. Det isolerer modellens norsk fra Whispers feil. Målene er enkle og mekaniske:
  gyldig JSON ved første forsøk, andel norske stoppord i sammendragene (og ingen engelske), forslag som ikke står i teksten
  (forkastet av `katalog.rens_post`), antall emneord etter rens, tid. Språkkvaliteten er IKKE vurdert av et menneske.
En kandidat må ha minst 90 % gyldig JSON og norsk språk (>= 25 % norske og < 2 % engelske stoppord) for å komme i betraktning;
blant dem velges den med færrest forkastede forslag per sending, så den raskeste.

    source scripts/miljo.sh && .venv/bin/python eval/dev/velg_katalogmodell.py
"""
import glob
import json
import pathlib
import random
import re
import subprocess
import sys
import time

HER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HER))
from felles import REPO  # noqa: E402

from arkivklarering import evaldata, katalog, miljo, personvern  # noqa: E402
from arkivklarering.transkriber import Cue  # noqa: E402

KANDIDATER = ["nb-llama-3.1-8b-instruct-cardtmpl:latest", "normistral-7b-warm-instruct-cardtmpl:latest",
              "hf.co/NbAiLab/borealis-open-4b-gguf:Q4_K_M", "hf.co/NbAiLab/borealis-4b-gguf:Q4_K_M"]
NO = set("og i det som på til er en av for med at ikke har de den var om et fra så men også eg ein ho han vi vart dei som kva med å".split())
EN = set("the and of to is in that it was for with as on are this".split())


def sendinger(n=45, seed=20261026):
    mappe = evaldata.npsc_mappe(miljo.EVAL_DATA / "npsc", "validation")
    rader = []
    for f in sorted(mappe.glob("*.json")):
        rader += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    rng = random.Random(seed)
    ut = []
    for sprak, antall in (("nb-NO", 3), ("nn-NO", 1)):
        kand = [r for r in rader if r["sentence_language_code"] == sprak]
        kand.sort(key=lambda r: (r["meeting_date"], r["sentence_id"]))
        for _ in range(antall):
            i = rng.randrange(0, len(kand) - n)
            run = kand[i:i + n]
            t0 = run[0]["start_time"]
            ut.append((sprak, [Cue((r["start_time"] - t0) / 1000, (r["end_time"] - t0) / 1000, r["normsentence_text"]) for r in run]))
    return ut


def norsk_andel(tekst):
    ord_ = re.findall(r"[a-zæøåA-ZÆØÅ]+", tekst.lower())
    return (sum(w in NO for w in ord_) / len(ord_), sum(w in EN for w in ord_) / len(ord_)) if ord_ else (0.0, 0.0)


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    kun = [a for a in sys.argv[1:] if not a.startswith("--")]
    kandidater = kun or KANDIDATER
    motor = personvern.lag_motor()
    data = sendinger()
    tilsvar = []
    for sprak, cues in data:
        g = "nn" if sprak == "nn-NO" else "nb"
        fl = personvern.flagg_cues(cues, "normalisert", g, motor)
        tilsvar.append((cues, personvern.slaa_sammen_lag({"normalisert": fl, "ra": []})))
    res = {}
    for modell in kandidater:
        tall = {"kall": 0, "ugyldig_json": 0, "forkastet": 0, "emneord_ok": 0, "tittel_ok": 0, "sammendrag": 0, "sammendrag_tomt": 0, "tid_s": 0.0,
                "no_andel": [], "en_andel": []}

        def chat(m, system, bruker, _t=tall):
            t0 = time.time()
            raa = katalog.ollama_chat(m, system, bruker)
            _t["tid_s"] += time.time() - t0
            _t["kall"] += 1
            _t["ugyldig_json"] += not _json_ok(raa)
            return raa

        try:
            for cues, union in tilsvar:
                p = katalog.lag_katalogpost(cues, union, modell, chat=chat)
                tall["forkastet"] += sum(1 for f in p.forkastet if "emneord" not in f)
                tall["emneord_ok"] += katalog.MIN_EMNEORD <= len(p.emneord) <= katalog.MAKS_EMNEORD
                tall["tittel_ok"] += 0 < len(p.tittel) <= 120
                for s in p.segmenter:
                    tall["sammendrag"] += 1
                    tall["sammendrag_tomt"] += not s["sammendrag"]
                    if s["sammendrag"]:
                        no, en = norsk_andel(s["sammendrag"])
                        tall["no_andel"].append(no)
                        tall["en_andel"].append(en)
        except Exception as e:  # noqa: BLE001
            tall["feil"] = f"{type(e).__name__}: {e}"
        subprocess.run(["ollama", "stop", modell], capture_output=True)
        n = len(tilsvar)
        res[modell] = {"kall": tall["kall"], "ugyldig_json_andel": round(tall["ugyldig_json"] / max(tall["kall"], 1), 3),
                       "forkastede_forslag_per_sending": round(tall["forkastet"] / n, 2), "emneord_ok": f"{tall['emneord_ok']}/{n}",
                       "tittel_ok": f"{tall['tittel_ok']}/{n}", "sammendrag_tomme": f"{tall['sammendrag_tomt']}/{tall['sammendrag']}",
                       "norske_stoppord_andel": round(sum(tall["no_andel"]) / max(len(tall["no_andel"]), 1), 3),
                       "engelske_stoppord_andel": round(sum(tall["en_andel"]) / max(len(tall["en_andel"]), 1), 3),
                       "tid_per_sending_s": round(tall["tid_s"] / n, 1), **({"feil": tall["feil"]} if "feil" in tall else {})}
        print(modell, json.dumps(res[modell], ensure_ascii=False), flush=True)
    ut = REPO / "eval" / "dev" / ("katalogmodell_valg_2026-10-26.json" if not kun else "katalogmodell_omkjoring_2026-10-26.json")
    ut.write_text(json.dumps({"merknad": "DEV: modellvalg for katalogutkast (KLAR-ADR-0013)", "sendinger": len(data), "resultat": res}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _json_ok(tekst):
    try:
        return isinstance(json.loads(tekst), dict)
    except json.JSONDecodeError:
        return False


if __name__ == "__main__":
    main()
