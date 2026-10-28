#!/usr/bin/env python3
"""Slår opp hvert ord i KLAR-MANUS-0002 mot Nynorskordboka (nn-setninger) og Bokmålsordboka (nb-setninger) via det offisielle
API-et (https://ord.uib.no, dokumentasjon: https://ord.uib.no/ord_2_API.html).

Oppslag: `GET /api/articles?w=<ord>&dict=<nn|bm>&scope=ei`: `e` = oppslagsord, `i` = bøyde former, så en bøyd form gir treff
på artikkelen til lemmaet. Søket skiller ikke mellom store og små bokstaver. Ord uten treff listes (og forslag fra `/api/suggest`
med `include=s` hentes til manuell vurdering). Hoppes over: egennavn (ord i målelementene av typen person og sted), tall og
e-postadresser. Intet rettes av skriptet; det rapporterer bare. Resultatet skrives til `eval/dev/ordbokkontroll_manus0002_<dato>.json`
sammen med sha256 av manusfila som ble kontrollert.

    source scripts/miljo.sh && .venv/bin/python scripts/ordbokkontroll.py
"""
import datetime
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
API = "https://ord.uib.no/api"
ORDBOK = {"nn": "Nynorskordboka", "nb": "Bokmålsordboka"}
DICT = {"nn": "nn", "nb": "bm"}


def hent(url, forsok=3):
    for i in range(forsok):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                return json.load(r)
        except Exception:  # noqa: BLE001  nettverksfeil: prøv igjen
            if i == forsok - 1:
                raise
            time.sleep(1.5 * (i + 1))


def tokens(setning):
    ut = []
    for t in setning.split():
        t = t.strip(".,;:!?()«»\"'")
        if t:
            ut.append(t)
    return ut


def main():
    import glob
    from arkivklarering import evaldata, kalibrering
    manus = evaldata.siste_versjon(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))
    sha = hashlib.sha256(pathlib.Path(manus).read_bytes()).hexdigest()
    rader = kalibrering.les_manus(manus, kun_struktur=True)
    cache = {}
    slag = {}
    ingen_treff = {}
    for r in rader:
        mf = r["malform"]
        navn = {w.lower() for e in r["elementer"] if e["type"] in ("person", "sted") for f in e["former"] for w in f.split()}
        funn = []
        for i, t in enumerate(tokens(r["setning"])):
            lo = t.lower()
            if re.search(r"\d", t) or "@" in t:
                funn.append({"ord": t, "status": "hoppet over (tall eller e-post)"})
                continue
            if lo in navn:
                funn.append({"ord": t, "status": "hoppet over (egennavn)"})
                continue
            nokkel = (mf, lo)
            if nokkel not in cache:
                q = urllib.parse.urlencode({"w": lo, "dict": DICT[mf], "scope": "ei"})
                svar = hent(f"{API}/articles?{q}")
                ider = svar.get("articles", {}).get(DICT[mf], [])
                cache[nokkel] = {"artikler": ider}
                if not ider:
                    s = hent(f"{API}/suggest?" + urllib.parse.urlencode({"q": lo, "n": 5, "dict": DICT[mf], "include": "s"}))
                    cache[nokkel]["forslag"] = [x[0] for x in s.get("a", {}).get("similar", [])]
                time.sleep(0.15)
            c = cache[nokkel]
            funn.append({"ord": t, "status": "treff" if c["artikler"] else "ingen treff", **({"artikler": c["artikler"]} if c["artikler"] else {"forslag": c.get("forslag", [])})})
        slag[r["id"]] = funn
        for f in funn:
            if f["status"] == "ingen treff":
                ingen_treff.setdefault((mf, f["ord"].lower()), []).append(r["id"])
    ut = {"ordbok": ORDBOK, "api": API, "oppslag": "articles?w=<ord>&dict=<nn|bm>&scope=ei", "dato": datetime.date.today().isoformat(),
          "manus": pathlib.Path(manus).name, "manus_sha256": sha, "unike_oppslag": len(cache),
          "ingen_treff": [{"malform": m, "ord": o, "setninger": ids, "forslag": cache[(m, o)].get("forslag", [])} for (m, o), ids in sorted(ingen_treff.items())],
          "setninger": slag}
    sti = REPO / "eval" / "dev" / f"ordbokkontroll_manus0002_{ut['dato']}.json"
    sti.write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(sti.relative_to(REPO), f"{len(cache)} unike oppslag, {len(ingen_treff)} ord uten treff")
    for x in ut["ingen_treff"]:
        print(f"  {x['malform']}: {x['ord']!r} i {', '.join(x['setninger'])}  forslag: {', '.join(x['forslag'])}")
    return 0


if __name__ == "__main__":
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    sys.exit(main())
