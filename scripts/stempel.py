#!/usr/bin/env python3
"""Uavhengig tidsstempel (OpenTimestamps) av docs/ og HEAD-commiten.

  1. Med --head: `git rev-parse HEAD` skrives til docs/stempler/HEAD_<sha12>.txt og stemples.
  2. Hver fil i docs/ (unntatt docs/stempler/) stemples hvis det ikke finnes et stempel for akkurat
     denne sha256-en: docs/stempler/<filnavn>.<sha12>.ots. Endret innhold gir nytt stempel; gamle
     stempler beholdes.
  3. `ots upgrade` kjøres på alle eksisterende .ots-filer som ikke er Bitcoin-bekreftet ennå. Det er
     ufarlig å gjenta; så lenge kalenderne ikke har fått bekreftelse i en blokk ligger stempelet urørt.
  4. docs/stempler/KLAR-LOG-0002_arkivklarering_tidsstempler_v<maj>.<min>_<dato>.md føres: ett rad per
     stempling og per Bitcoin-bekreftelse. Versjonen i filnavnet økes når det kommer nye rader.

`ots stamp` sender bare sha256-sammendraget til offentlige kalendertjenester, ikke innholdet.
Stempelet beviser at filen fantes senest da Bitcoin-blokken ble funnet; det beviser ikke forfatterskap.
Verifiser: `ots verify -f docs/<fil> docs/stempler/<fil>.<sha12>.ots`.

    .venv/bin/python scripts/stempel.py           # docs/ + upgrade (det speil.sh kjører)
    .venv/bin/python scripts/stempel.py --head    # i tillegg HEAD-commiten (kjøres av hånd, før commit av stemplene)
"""
import datetime
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
ST = DOCS / "stempler"
OTS = REPO / ".venv/bin/ots"
LOGG_GLOB = "KLAR-LOG-0002_arkivklarering_tidsstempler_v*_*.md"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while b := f.read(1 << 20):
            h.update(b)
    return h.hexdigest()


def kjor(argv):
    r = subprocess.run(argv, capture_output=True, text=True, timeout=300)
    return r.returncode, (r.stdout + r.stderr)


def bitcoin_bekreftet(ots_fil):
    rc, ut = kjor([str(OTS), "info", str(ots_fil)])
    return "BitcoinBlockHeaderAttestation" in ut


def les_logg():
    fil = sorted(ST.glob(LOGG_GLOB))
    stempler, bekreftelser, v = [], [], (1, -1)
    for p in fil:
        m = re.search(r"_v(\d+)\.(\d+)_", p.name)
        v = max(v, (int(m[1]), int(m[2])))
        sek = None
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.startswith("## Stemplinger"):
                sek = stempler
            elif l.startswith("## Bitcoin-bekreftelser"):
                sek = bekreftelser
            elif l.startswith("| 20") and sek is not None:
                sek.append([c.strip() for c in l.strip("|").split("|")])
    return fil, stempler, bekreftelser, v


def skriv_logg(fil, stempler, bekreftelser, v, nå):
    ny = (v[0], v[1] + 1)
    ut = ST / f"KLAR-LOG-0002_arkivklarering_tidsstempler_v{ny[0]}.{ny[1]}_{nå.date().isoformat()}.md"
    t = ["# KLAR-LOG-0002: Tidsstempler (OpenTimestamps)", "",
         f"Versjon {ny[0]}.{ny[1]}, {nå.date().isoformat()}. Ført av `scripts/stempel.py`; ikke rediger for hånd.", "",
         "Stempelet beviser at en fil med denne sha256-en fantes senest da Bitcoin-blokken ble funnet, uavhengig av GitHub, Vault og Master Dok. "
         "Det beviser ikke forfatterskap. Bare sha256-sammendraget er sendt til kalendertjenestene. Et stempel er «ventende» til en kalender har "
         "fått det inn i en Bitcoin-blokk (vanligvis noen timer); `ots upgrade` kjøres av `scripts/speil.sh` hver gang og fører bekreftelsen under.",
         "Verifiser: `ots verify -f docs/<fil> docs/stempler/<ots-fil>`.", "",
         "## Stemplinger", "", "| tidspunkt (UTC) | fil | sha256 | .ots-fil |", "|---|---|---|---|"]
    t += ["| " + " | ".join(r) + " |" for r in stempler]
    t += ["", "## Bitcoin-bekreftelser", "", "| tidspunkt (UTC) | .ots-fil | merknad |", "|---|---|---|"]
    t += ["| " + " | ".join(r) + " |" for r in bekreftelser]
    ut.write_text("\n".join(t) + "\n", encoding="utf-8")
    for g in fil:
        if g != ut:
            if subprocess.run(["git", "ls-files", "--error-unmatch", str(g)], cwd=REPO, capture_output=True).returncode == 0:
                subprocess.run(["git", "rm", "-q", "-f", str(g)], cwd=REPO)
            else:
                g.unlink()
    return ut


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()  # avbryter hvis cacher og tmp ikke ligger under ARKIVKLARERING_DATA
    if not OTS.exists():
        sys.exit("ots mangler. Installer: VIRTUAL_ENV=$PWD/.venv uv pip install opentimestamps-client")
    ST.mkdir(exist_ok=True)
    nå = datetime.datetime.now(datetime.timezone.utc)
    ts = nå.strftime("%Y-%m-%d %H:%M:%S")
    fil, stempler, bekreftelser, v = les_logg()
    nye_stempler, nye_bekreftelser, feil = [], [], []

    # 1. HEAD (bare med --head: speil.sh kjører etter commit, og et HEAD-stempel per kjøring ville aldri bli ferdig committet)
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    head = ST / f"HEAD_{sha[:12]}.txt"
    if "--head" in sys.argv and not (ST / f"{head.name}.ots").exists():
        head.write_text(sha + "\n", encoding="utf-8")
        rc, ut = kjor([str(OTS), "stamp", str(head)])
        if rc == 0 and (ST / f"{head.name}.ots").exists():
            nye_stempler.append([ts, f"{head.name} (git HEAD {sha[:7]})", sha256(head), f"{head.name}.ots"])
        else:
            feil.append((head.name, ut[-300:]))

    # 2. docs/
    for p in sorted(DOCS.rglob("*")):
        if not p.is_file() or ST in p.parents or p.name == ".DS_Store":
            continue
        h = sha256(p)
        navn = f"{p.name}.{h[:12]}.ots"
        if (ST / navn).exists():
            continue
        with tempfile.TemporaryDirectory() as tmp:
            kopi = pathlib.Path(tmp) / p.name
            shutil.copyfile(p, kopi)
            rc, ut = kjor([str(OTS), "stamp", str(kopi)])
            if rc == 0 and pathlib.Path(f"{kopi}.ots").exists():
                shutil.copyfile(f"{kopi}.ots", ST / navn)
                nye_stempler.append([ts, str(p.relative_to(REPO)), h, navn])
            else:
                feil.append((str(p.relative_to(REPO)), ut[-300:]))

    # 3. upgrade
    ventende = bekreftet_nå = 0
    alt_bekreftet = {r[1] for r in bekreftelser}
    for o in sorted(ST.glob("*.ots")):
        if o.name in alt_bekreftet or bitcoin_bekreftet(o):
            if o.name not in alt_bekreftet:
                nye_bekreftelser.append([ts, o.name, "allerede bekreftet ved første sjekk"])
            continue
        rc, ut = kjor([str(OTS), "upgrade", str(o)])
        if bitcoin_bekreftet(o):
            bekreftet_nå += 1
            nye_bekreftelser.append([ts, o.name, "bekreftet i Bitcoin-blokk"])
        else:
            ventende += 1
        bak = pathlib.Path(f"{o}.bak")
        if bak.exists() and bitcoin_bekreftet(o) is False:
            bak.unlink()  # uendret stempel; ingen grunn til å beholde sikkerhetskopien

    # 4. logg
    if nye_stempler or nye_bekreftelser:
        ut = skriv_logg(fil, stempler + nye_stempler, bekreftelser + nye_bekreftelser, v, nå)
        print("logg:", ut.relative_to(REPO))
    alle = len(list(ST.glob("*.ots")))
    print(f"stemplet nå: {len(nye_stempler)}; .ots-filer totalt: {alle}; Bitcoin-bekreftet nå: {bekreftet_nå}; "
          f"nye bekreftelser ført: {len(nye_bekreftelser)}; ventende: {ventende}")
    for n, m in feil:
        print(f"FEIL ved stempling av {n}: {m}", file=sys.stderr)
    sys.exit(1 if feil else 0)


if __name__ == "__main__":
    main()
