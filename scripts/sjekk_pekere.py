#!/usr/bin/env python3
"""Kontrollerer henvisninger til arkivnøkler og fil:linje-pekere (regelen i KLAR-ARK-0002 v1.5:25).

Omfang: `README.md`, `CITATION.cff`, `.zenodo.json`, `paper.bib` og `paper/` (hvis mappen finnes), og alle tekstfiler under `docs/` i treet.
Unntak: filer i LOG-serien (`KLAR-LOG-*`), `CHANGELOG.md`, versjonsnotatene i dokumenthodene (parentesen etter «Versjon X.Y, dato» og
«UTKAST vX.Y, dato» før første overskrift på nivå 2) og kodeblokker (```). Regel 1 gjelder ikke for tekst som ikke kan endres: JSON-rådata
fra kjøringer, eldre versjoner som står ved siden av nyere etter unntaket i KLAR-ARK-0002, og den registrerte teksten i KLAR-PREREG-0001 (før
«Avvik etter registrering»). KLAR-GT-0001 er et generert og stemplet øyeblikksbilde av arbeidstreet ved sin commit; der gjelder bare regel 3.

Regler:
  1. En henvisning til en versjon (`KLAR-TYPE-NNNN vX.Y`, kortformen `TYPE-NNNN vX.Y`, `PREREG vX.Y`, `KILDE vX.Y`, `GT vX.Y`, et filnavn
     `KLAR-…_vX.Y_dato….ext`, eller et nakent `vX.Y:linje` etter en slik henvisning i samme setning) skal finnes som fil i treet, eller stå
     i samme setning som «(i git-historikken)».
  2. Hver slik henvisning, merket eller ikke, skal finnes i treet eller i git-historikken (`git log --all`); ellers er den en skrivefeil.
  3. En fil:linje-peker skal vise til en linje som finnes i den fila (i treet, eller ved siste commit der fila fantes).

    python3 scripts/sjekk_pekere.py      # skriver ett brudd per linje; avslutter med 1 hvis det finnes brudd
"""
import functools
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
MERKE = "(i git-historikken)"
TYPER = "ARK|ADR|EVAL|LOG|KILDE|PREREG|MANUS|REG|GT"
LANG = re.compile(r"KLAR-[A-Z]+-\d{4}_[a-z0-9_-]+?_v(\d+\.\d+)_\d{4}-\d{2}-\d{2}(?:_[a-z_]+)?(?:\.[a-z0-9]+)+")
ELIDERT = re.compile(r"KLAR-([A-Z]+)-(\d{4})_…_v(\d+\.\d+)_\d{4}-\d{2}-\d{2}(?:_[a-z_]+)?(?:\.[a-z0-9]+)+")  # «KLAR-ADR-0019_…_v1.5_….md»
KORT = re.compile(rf"(?<![\w-])`?(?:KLAR-)?({TYPER})-(\d{{4}})`? v(\d+\.\d+)(?![\d.]*\d)")
BARE_TYPE = re.compile(r"(?<![\w-])(PREREG|KILDE|GT|LOG) v(\d+\.\d+)(?![\d.]*\d)")  # LOG = KLAR-LOG-0001
KJEDE = re.compile(r"(?:,? og |, | eller |\(og |\(i | \()v(\d+\.\d+)(?=[:\s),;])")
NAKEN = re.compile(r"(?<![\w.-])v(\d+\.\d+):(\d+)")
LINJE = re.compile(r"`?\)?:(\d+)(?:[–-](\d+))?")
LINJEKJEDE = re.compile(r"(?:,| og) :(\d+)(?:[–-](\d+))?")
FILPEKER = re.compile(r"`?((?:[\w.-]+/)*[\w.-]+\.(?:md|py|sh|toml|cff|json|bib|txt|tsv|lock|xsd|yml|yaml|cfg|ini))`?:(\d+)(?:[–-](\d+))?")
SETNING = re.compile(r"(?<=[.!?»])\s+(?=[A-ZÆØÅ«*\[`])|\s\|\s")


def git(*a):
    return subprocess.run(["git", *a], cwd=REPO, check=True, capture_output=True, text=True).stdout


@functools.lru_cache(None)
def tre():
    return set(git("ls-files").split("\n")) - {""}


@functools.lru_cache(None)
def har_historikk():
    """Uten historikk (ett commit, som i det offentlige repoet fra et rent tre) kan regel 2 og regel 3 for historiske filer ikke prøves;
    historikken ligger da i den tilgangsstyrte deponeringen, og bare regel 1 og regel 3 for filer i treet gjelder."""
    return int(git("rev-list", "--count", "--all").strip() or 0) > 1


@functools.lru_cache(None)
def historikk():
    return set(git("log", "--all", "--no-renames", "--name-only", "--format=").split("\n")) - {""}


def nokkel(navn):
    m = re.match(r"(KLAR-[A-Z]+-\d{4})_.*?_v(\d+\.\d+)_", pathlib.Path(navn).name)
    return (m[1], m[2]) if m else None


@functools.lru_cache(None)
def indeks():
    """(nøkkel, versjon) -> stier, og filnavn -> stier, for treet og historikken."""
    i_tre, i_hist, navn_tre, navn_hist = {}, {}, {}, {}
    for kilde, nk, nv in ((tre(), i_tre, navn_tre), (historikk(), i_hist, navn_hist)):
        for p in kilde:
            k = nokkel(p)
            if k and not p.startswith("docs/stempler/"):  # stempelfilene (.ots) bærer dokumentnavnet, men er ikke dokumentet
                nk.setdefault(k, []).append(p)
            nv.setdefault(pathlib.Path(p).name, []).append(p)
    return i_tre, i_hist, navn_tre, navn_hist


@functools.lru_cache(None)
def linjer(sti):
    """Antall linjer i fila: i treet hvis den finnes der, ellers ved siste commit der den fantes."""
    if sti in tre():
        return len((REPO / sti).read_text(encoding="utf-8", errors="replace").split("\n"))
    for sha in git("log", "--all", "--no-renames", "--format=%H", "--", sti).split():
        for kandidat in (sha, sha + "^"):
            r = subprocess.run(["git", "show", f"{kandidat}:{sti}"], cwd=REPO, capture_output=True)
            if r.returncode == 0:
                return len(r.stdout.decode("utf-8", "replace").split("\n"))
    return None


def velg(stier):
    stier = sorted(stier)
    return next((s for s in stier if s.endswith(".md")), stier[0])


def nyeste(sti):
    """Er fila nyeste versjon av sin arkivnøkkel i treet (eller uten arkivnøkkel)?"""
    k = nokkel(sti)
    if not k:
        return True
    tall = lambda v: tuple(int(x) for x in v.split("."))
    andre = [nokkel(s)[1] for s in tre() if nokkel(s) and nokkel(s)[0] == k[0] and not s.startswith("docs/stempler/")]
    return tall(k[1]) == max(map(tall, andre))


def finn_fil(navn, fra):
    """Sti for en fil:linje-peker uten arkivnøkkel: relativt til repoet, til dokumentet, eller et entydig filnavn."""
    _, _, navn_tre, navn_hist = indeks()
    for kandidat in (navn, str((fra.parent / navn).resolve().relative_to(REPO)) if (fra.parent / navn).resolve().is_relative_to(REPO) else None):
        if kandidat and (kandidat in tre() or kandidat in historikk()):
            return kandidat
    treff = navn_tre.get(pathlib.Path(navn).name) or navn_hist.get(pathlib.Path(navn).name) or []
    treff = sorted(set(treff))
    return treff[0] if len(treff) == 1 else None


def omfang():
    filer = [p for p in ("README.md", "CITATION.cff", ".zenodo.json", "paper.bib") if p in tre()]
    filer += sorted(p for p in tre() if p.startswith("paper/") or p.startswith("docs/"))
    ut = []
    for p in filer:
        navn = pathlib.Path(p).name
        if navn.startswith("KLAR-LOG-") or navn == "CHANGELOG.md" or not navn.endswith((".md", ".json", ".txt", ".cff", ".bib")):
            continue
        ut.append(p)
    return ut


def fjern_versjonsnotater(tekst):
    """Erstatter versjonsnotatene i hodet (før første «## ») med mellomrom, så linjenumre og posisjoner står."""
    slutt = next((m.start() for m in re.finditer(r"(?m)^## ", tekst)), len(tekst))
    hode = list(tekst[:slutt])
    for m in re.finditer(r"(?:Versjon|UTKAST) v?\d+\.\d+, \d{4}-\d{2}-\d{2} \(", tekst[:slutt]):
        dybde, i = 1, m.end()
        while i < slutt and dybde:
            dybde += {"(": 1, ")": -1}.get(tekst[i], 0)
            i += 1
        for j in range(m.end(), i):
            if hode[j] != "\n":
                hode[j] = " "
    return "".join(hode) + tekst[slutt:]


def henvisninger(setning):
    """(start, slutt, (nøkkel, versjon) eller filnavn, tekst) for hver henvisning i setningen; slutt tar med linjepekerne etter."""
    ut = []
    for m in LANG.finditer(setning):
        ut.append([m.start(), m.end(), ("fil", m[0]), m[0]])
    for m in ELIDERT.finditer(setning):
        ut.append([m.start(), m.end(), (f"KLAR-{m[1]}-{m[2]}", m[3]), m[0]])
    brukt = [(a, b) for a, b, _, _ in ut]
    for m in KORT.finditer(setning):
        if not any(a <= m.start() < b for a, b in brukt):
            ut.append([m.start(), m.end(), (f"KLAR-{m[1]}-{m[2]}", m[3]), m[0]])
    for m in BARE_TYPE.finditer(setning):
        if not any(a <= m.start() < b for a, b, _, _ in ut):
            ut.append([m.start(), m.end(), (f"KLAR-{m[1]}-0001", m[2]), m[0]])
    ut.sort()
    # kjeder av nakne versjoner etter en kortform («KLAR-EVAL-0013 v1.2:5 (og v1.3:5)»)
    flere = []
    for h in ut:
        if h[2][0] == "fil":
            continue
        pos = h[1]
        while True:
            lm = LINJE.match(setning, pos)
            pos = lm.end() if lm and lm[0].strip("`)") else pos
            while (k := LINJEKJEDE.match(setning, pos)):
                pos = k.end()
            k = KJEDE.match(setning, pos)
            if not k:
                break
            flere.append([k.start(1) - 1, k.end(), (h[2][0], k[1]), k[0].strip()])
            pos = k.end()
    ut += flere
    ut.sort()
    # nakne «vX.Y:linje» som ikke er del av en henvisning: hører til siste nøkkel før i setningen
    for m in NAKEN.finditer(setning):
        if any(a <= m.start() < b for a, b, _, _ in ut):
            continue
        foran = [h for h in ut if h[0] < m.start() and h[2][0] != "fil"]
        if foran:
            ut.append([m.start(), m.start() + len("v" + m[1]), (foran[-1][2][0], m[1]), m[0]])
    ut.sort()
    return ut


def linjepekere(setning, pos):
    """Linjenumrene (største i hvert område) som følger rett etter posisjonen."""
    ut = []
    lm = LINJE.match(setning, pos)
    if lm and lm[1]:
        ut.append(int(lm[2] or lm[1]))
        pos = lm.end()
        while (k := LINJEKJEDE.match(setning, pos)):
            ut.append(int(k[2] or k[1]))
            pos = k.end()
    return ut


def sjekk():
    i_tre, i_hist, navn_tre, navn_hist = indeks()
    brudd = []
    for p in omfang():
        gt = pathlib.Path(p).name.startswith("KLAR-GT-0001_")  # generert øyeblikksbilde av treet ved sin commit: regel 1 gjelder ikke
        frosset = p.endswith(".json") or not nyeste(p)  # rådata fra kjøringer og eldre versjoner som står etter unntaket: regel 1 gjelder ikke
        registrert_slutt = 0
        rå = (REPO / p).read_text(encoding="utf-8", errors="replace")
        if pathlib.Path(p).name.startswith("KLAR-PREREG-0001_"):  # den registrerte teksten (før avviksseksjonen) er låst på OSF
            registrert_slutt = next((i for i, l in enumerate(rå.split("\n"), 1) if l.startswith("## Avvik etter registrering")), 0)
        tekst = fjern_versjonsnotater(rå)
        i_kode = False
        for nr, linje in enumerate(tekst.split("\n"), 1):
            if linje.lstrip().startswith("```"):  # kodeblokker er kode og utdata, ikke henvisninger
                i_kode = not i_kode
                continue
            if i_kode:
                continue
            for setning in SETNING.split(linje):
                merket = MERKE in setning
                for a, b, k, vis in henvisninger(setning):
                    if k[0] == "fil":
                        navn = k[1]
                        stier_tre, stier_hist = navn_tre.get(navn, []), navn_hist.get(navn, [])
                    else:
                        stier_tre, stier_hist = i_tre.get(k, []), i_hist.get(k, [])
                    if not stier_tre and not stier_hist:
                        if gt:
                            continue
                        if har_historikk():
                            brudd.append(f"{p}:{nr}: finnes verken i treet eller i git-historikken: {vis}")
                        elif not merket and not frosset and nr >= registrert_slutt:
                            brudd.append(f"{p}:{nr}: ikke i treet og ikke merket {MERKE}: {vis}")
                        continue
                    if not stier_tre and not merket and not gt and not frosset and nr >= registrert_slutt:
                        brudd.append(f"{p}:{nr}: ikke i treet og ikke merket {MERKE}: {vis}")
                    sti = velg(stier_tre or stier_hist)
                    n = linjer(sti)
                    for ln in linjepekere(setning, b):
                        if n is not None and not 1 <= ln <= n:
                            brudd.append(f"{p}:{nr}: linje {ln} finnes ikke i {sti} ({n} linjer): {vis}")
                for m in FILPEKER.finditer(setning):
                    navn = m[1]
                    if pathlib.Path(navn).name.startswith("KLAR-") or navn.startswith("/") or setning[max(0, m.start() - 1):m.start()] == "…":
                        continue
                    sti = finn_fil(navn, REPO / p)
                    if sti is None:
                        if not har_historikk():
                            continue
                        brudd.append(f"{p}:{nr}: fila finnes ikke i treet eller historikken: {navn}:{m[2]}")
                        continue
                    n = linjer(sti)
                    ln = int(m[3] or m[2])
                    if n is not None and not 1 <= ln <= n:
                        brudd.append(f"{p}:{nr}: linje {ln} finnes ikke i {sti} ({n} linjer)")
    return brudd


def main():
    brudd = sjekk()
    for b in brudd:
        print(b)
    print(f"{len(brudd)} brudd i {len(omfang())} filer", file=sys.stderr)
    return 1 if brudd else 0


if __name__ == "__main__":
    sys.exit(main())
