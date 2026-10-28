#!/usr/bin/env python3
"""Starter H4-innleseren (KLAR-ADR-0018) med arkivklarerings testmanus KLAR-MANUS-0002 (H4 i KLAR-PREREG-0001).

Innleseren er en egen modus uten noe resultat: ingen transkripsjon, flagg, poeng, rapport eller eksport vises eller finnes som rute
(`arkivklarering/h4_innlesing.py`). Den bygger på norsk-tales kalibreringsrigg, men bare når riggen står på den låste commiten med de låste
filene (ellers stopper den). Lyd fra innlesingen ligger kun på Vault under /Volumes/Vault/arkivklarering/lyd/h4/ og går aldri i git eller sky
(ADR-0007). `kalibrering/kjor_h4.py --opptak /Volumes/Vault/arkivklarering/lyd/h4` leser opptakene (scripts/kjor_testdel.sh sender det).

    source scripts/miljo.sh && .venv/bin/python scripts/rigg_manus.py          # starter innleseren; åpne URL-en som skrives ut
    .venv/bin/python scripts/rigg_manus.py --tor                                # bare kontroller manus, rigglås og opptaksmappe

Skriptet leser bare teksten som skal leses opp; det kjører ingenting gjennom rørledningen (testmanuset er sperret der til preregistreringen er
registrert). Innlesing til 16 kHz mono wav: `<runde>/opptak/<manus-id>.wav`, med `runde.json` og `opptakslogg.jsonl` (id, tidspunkt, forsøk, grunn).
"""
import glob
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def siste_manus():
    return max(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")), key=lambda p: tuple(int(x) for x in re.search(r"_v(\d+(?:\.\d+)*)_", p).group(1).split(".")))  # versjonssortering


def main(argv=None):
    from arkivklarering import h4_innlesing
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    argv = list(sys.argv[1:] if argv is None else argv)
    if any(a not in ("--tor",) for a in argv):
        sys.exit("bruk: rigg_manus.py [--tor]  (opptaksmappen er fast: " + str(h4_innlesing.H4_ROT) + ")")
    manus = siste_manus()
    try:
        lås = h4_innlesing.kontroller_rigg()
    except h4_innlesing.RiggFeil as e:
        sys.exit(str(e))
    if argv:
        rigg = h4_innlesing.last_rigg()
        rigg.MANUS = pathlib.Path(manus)
        H4Rigg, _ = h4_innlesing.lag_klasser(rigg)
        r = H4Rigg(h4_innlesing.H4_ROT)
        print(f"manus: {manus}\n{len(r.manus)} setninger, {sum(1 for s in r.manus if s['dialektutvalg'])} med dialektutvalg; opptak: {r.rot}\n"
              f"rigg: norsk-tale commit {lås['norsk_tale_commit']}, {len(lås['filer'])} filer verifisert (sha256)\ninstruks: {h4_innlesing.INSTRUKS}")
        return 0
    return h4_innlesing.start(manus)


if __name__ == "__main__":
    sys.exit(main())
