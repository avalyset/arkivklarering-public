#!/usr/bin/env python3
"""Kontrollerer etternavnene i KLAR-MANUS-0002 mot SSBs navnesøk (https://www.ssb.no/befolkning/navn/statistikk/navn).

Søket kaller tjenesten som siden selv bruker: `GET https://www.ssb.no/_/service/mimir/nameSearch?name=<navn>`; svaret har
`response.numFound` og per treff `type` (family, middleandfamily, firstgiven, onlygiven) og `count`. Krav (Eirik, 2026-10-26): hver
person som står i samme setning som helse, økonomi, konflikt, religion eller politikk skal ha et etternavn uten bærere. SSB oppgir at
«alle navn med mer enn tre navnebærere gir treff i navnesøket»: «ingen treff» betyr derfor 0 til 3 bærere, ikke nødvendigvis 0.
Resultatet skrives til `eval/dev/navnesjekk_manus0002_<dato>.json`.

    source scripts/miljo.sh && .venv/bin/python scripts/navnesjekk.py
"""
import datetime
import glob
import hashlib
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
SENSITIVE = {"helse", "økonomi", "konflikt", "religion", "politikk"}
URL = "https://www.ssb.no/_/service/mimir/nameSearch?name="


def sok(navn):
    for i in range(3):
        try:
            with urllib.request.urlopen(URL + urllib.parse.quote(navn), timeout=20) as r:
                svar = json.load(r)
            return svar["response"]["numFound"], [{"type": d["type"], "count": d["count"]} for d in svar["response"]["docs"]]
        except Exception:  # noqa: BLE001
            if i == 2:
                raise
            time.sleep(1.5)


def main():
    from arkivklarering import evaldata, kalibrering
    manus = evaldata.siste_versjon(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))
    rader = kalibrering.les_manus(manus, kun_struktur=True)
    funn, sett = [], {}
    for r in rader:
        typer = {e["type"] for e in r["elementer"]}
        for e in r["elementer"]:
            if e["type"] != "person":
                continue
            for form in e["former"]:
                etternavn = form.split()[-1]
                sensitiv = bool(typer & SENSITIVE)
                if etternavn not in sett:
                    sett[etternavn] = sok(etternavn)
                    time.sleep(0.3)
                n, docs = sett[etternavn]
                funn.append({"id": r["id"], "navn": form, "etternavn": etternavn, "i_setning_med_sensitiv_kategori": sensitiv,
                             "treff": n, "bærere": docs})
    krav = [f for f in funn if f["i_setning_med_sensitiv_kategori"]]
    ut = {"kilde": URL, "regel": "alle navn med mer enn tre bærere gir treff; ingen treff = 0–3 bærere", "dato": datetime.date.today().isoformat(),
          "manus": pathlib.Path(manus).name, "manus_sha256": hashlib.sha256(pathlib.Path(manus).read_bytes()).hexdigest(),
          "sensitive_setninger_med_person": len(krav), "av_dem_med_treff": sum(1 for f in krav if f["treff"]), "oppslag": funn}
    sti = REPO / "eval" / "dev" / f"navnesjekk_manus0002_{ut['dato']}.json"
    sti.write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(sti.relative_to(REPO), f"{len(krav)} personer i sensitive setninger, {ut['av_dem_med_treff']} med treff")
    for f in sorted({(x['etternavn'], x['treff']) for x in krav}):
        print("  ", f)
    return 1 if ut["av_dem_med_treff"] else 0


if __name__ == "__main__":
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    sys.exit(main())
