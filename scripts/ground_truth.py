#!/usr/bin/env python3
"""Genererer docs/KLAR-GT-0001_arkivklarering_ground-truth_v<auto>_<dato>.md fra disk.

Tilstand påstås aldri fra minne eller chat. Skriptet leser git, GitHub, modellfilene, pytest, docs/,
eval/ og Vault, og legger inn den håndførte seksjonen docs/gt_fast.md uendret. Versjonen økes
automatisk (minor) fra den eksisterende GT-fila, som erstattes (den gamle ligger i git-historikken).
Regenereres som siste steg i hver CC-kjøring, før scripts/speil.sh.

    .venv/bin/python scripts/ground_truth.py
"""
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
GH_REPO = "avalyset/arkivklarering"
GUARD = pathlib.Path.home() / "dev/norpref/scripts/gh_token_guard.sh"
sys.path.insert(0, str(REPO))
from arkivklarering import miljo, transkriber  # noqa: E402

VAULT = miljo.VAULT

GH_ENV = {**os.environ, "GITHUB_TOKEN": "", "GH_TOKEN": ""}  # token-vakt: gh skal bruke keyring


def kjor(argv, env=None, cwd=REPO):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, cwd=cwd, env=env, timeout=900)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:  # noqa: BLE001
        return 99, f"{type(e).__name__}: {e}"


def git(*a):
    rc, ut = kjor(["git", *a])
    return ut if rc == 0 else f"(feil: {ut})"


def seksjon_git():
    rc, vakt = kjor(["bash", str(GUARD)], env=GH_ENV)
    rc2, vis = kjor(["gh", "repo", "view", GH_REPO, "--json", "visibility,url,defaultBranchRef",
                     "--jq", '.visibility+" "+.url+" "+.defaultBranchRef.name'], env=GH_ENV)
    status = git("status", "--porcelain")
    return [
        f"- HEAD: `{git('rev-parse', 'HEAD')}` ({git('log', '-1', '--format=%s')})",
        f"- gren: `{git('rev-parse', '--abbrev-ref', 'HEAD')}`",
        f"- remote: `{git('remote', 'get-url', 'origin')}`",
        f"- origin/main: `{git('rev-parse', 'origin/main')}`",
        f"- visibility (gh repo view): `{vis}`" + ("" if rc2 == 0 else " **(feilet)**"),
        f"- token-vakt: {'OK' if rc == 0 else 'FEILET'}: {vakt.splitlines()[-1].removeprefix('OK: ') if vakt else ''}",
        f"- arbeidstre: {'rent' if not status else 'ikke rent (' + str(len(status.splitlines())) + ' endrede/uspora filer)'}",
    ]


def seksjon_modeller():
    lock = json.loads((REPO / "modeller.lock.json").read_text(encoding="utf-8"))
    ut = []
    for lag in transkriber.LAG:
        l = lock[lag]
        sti = pathlib.Path(os.environ.get(f"ARKIVKLARERING_MODELL_{lag.upper()}") or transkriber.standard_modellsti(lag))
        repo_lenke = REPO / "modeller" / sti.name
        if sti.is_file():
            sha = transkriber.sha256_fil(sti)
            ok = "stemmer med lock" if sha == l["sha256"] else f"**AVVIK mot lock ({l['sha256']})**"
            ut.append(f"- {lag}: `{sti}` ({sti.stat().st_size} byte), sha256 `{sha}`, {ok}")
        else:
            ut.append(f"- {lag}: `{sti}` **finnes ikke**; lock forventer sha256 `{l['sha256']}`")
        if repo_lenke.exists() or repo_lenke.is_symlink():
            ut.append(f"  - repo-symlink: `{repo_lenke}` -> `{os.path.realpath(repo_lenke)}`")
    return ut


def seksjon_pytest():
    py = REPO / ".venv/bin/python"
    rc, ut = kjor([str(py if py.exists() else sys.executable), "-m", "pytest", "-q"])
    sist = ut.splitlines()[-1] if ut else "(ingen utdata)"
    return [f"- `pytest -q` (rask del, `-m 'not tung'`): {sist}" + ("" if rc == 0 else f" **(exit {rc})**")]


def seksjon_dokumenter():
    ut = []
    for p in sorted(DOCS.rglob("KLAR-*.md")) + sorted((REPO / "eval").rglob("KLAR-*.md")):
        if p.name.startswith("KLAR-GT-0001_"):  # forrige GT erstattes av denne fila; den listes ikke (se linja under)
            continue
        m = re.match(r"KLAR-([A-Z]+)-(\d{4})_arkivklarering_(.+)_v(\d+\.\d+)_(\d{4}-\d{2}-\d{2})\.md$", p.name)
        ut.append(f"- {p.relative_to(REPO)}: " + (f"{m[1]}-{m[2]}, v{m[4]}, {m[5]}" if m else "**navnet følger ikke konvensjonen**"))
    ut.append("- KLAR-GT-0001: denne fila (generert av scripts/ground_truth.py; forrige versjon ligger i git-historikken)")
    return ut


def seksjon_eval():
    ut = []
    for p in sorted((REPO / "eval").rglob("KLAR-EVAL-*wer*.json")):
        if p.name.endswith((".utvalg.json", "_kjoring_meta.json")):  # utvalgs- og metafiler har ikke «wer»-nøkkelen; bare resultatfilene leses
            continue
        try:
            j = json.loads(p.read_text(encoding="utf-8"))
            tot = {k: v.get("totalt") for k, v in j["wer"].items()}
            ut.append(f"- {p.relative_to(REPO)} ({j.get('merknad', '')}): korpus-WER totalt " +
                      ", ".join(f"{k} {v:.3f}" for k, v in tot.items() if v is not None))
        except Exception as e:  # noqa: BLE001
            ut.append(f"- {p.relative_to(REPO)}: kunne ikke leses ({e})")
    if not ut:
        ut.append("- ingen WER-resultater i eval/")
    for p in sorted(DOCS.glob("KLAR-EVAL-*.md")):
        ut.append(f"- {p.relative_to(REPO)}")
    return ut


def seksjon_vault():
    montert = os.path.ismount(VAULT)
    ut = [f"- Vault montert: **{'ja' if montert else 'NEI'}** ({VAULT})", f"- datarot (ARKIVKLARERING_DATA): `{miljo.DATA}`"]
    if miljo.DATA.is_dir():
        for d in ("repo-bundle", "modeller", "lyd", "eval-data"):
            p = miljo.DATA / d
            n = sum(1 for _ in p.rglob("*")) if p.is_dir() else None
            ut.append(f"  - arkivklarering/{d}: " + ("finnes, " + str(n) + " oppføringer" if n is not None else "**mangler**"))
    return ut


NOKKEL = re.compile(r"^KLAR-([A-Z]+)-(\d{4})_arkivklarering_(.+?)_v\d+\.\d+_\d{4}-\d{2}-\d{2}\.(?:md|json|ots|txt|tsv)", re.I)


def nummerregister():
    """Leser KLAR-numre fra disken og fra KLAR-ARK-0003. Returnerer (linjer, varsler)."""
    disk = {}
    for rot in (DOCS, REPO / "eval", REPO / "kalibrering"):
        for p in sorted(rot.rglob("KLAR-*")):
            if not p.is_file() or p.name.endswith((".ots", ".bak")):  # .ots-filene (og sikkerhetskopiene .ots.bak fra ots upgrade) bærer navnet til dokumentet de stempler
                continue
            m = NOKKEL.match(p.name)
            if m:
                disk.setdefault((m[1].upper(), m[2]), {}).setdefault(m[3], []).append(p.name)
    varsler = []
    for k, slugs in disk.items():
        if len(slugs) > 1:
            varsler.append(f"DOBBEL BRUK: KLAR-{k[0]}-{k[1]} brukes med flere slugger: {', '.join(sorted(slugs))}")
    reg = {}
    regfil = sorted(DOCS.glob("KLAR-ARK-0003_arkivklarering_nummerregister_v*_*.md"))
    if not regfil:
        varsler.append("REGISTER MANGLER: docs/KLAR-ARK-0003_arkivklarering_nummerregister_v*.md finnes ikke")
    else:
        for l in regfil[-1].read_text(encoding="utf-8").splitlines():
            c = [x.strip().strip("`") for x in l.strip().strip("|").split("|")]
            m = re.match(r"^KLAR-([A-Z]+)-(\d{4})$", c[0]) if c else None
            if m and len(c) >= 3:
                if (m[1], m[2]) in reg:
                    varsler.append(f"DOBBEL BRUK i registeret: KLAR-{m[1]}-{m[2]}")
                reg[(m[1], m[2])] = (c[1], c[2])
    for k, slugs in sorted(disk.items()):
        if k not in reg:
            varsler.append(f"IKKE I REGISTERET: KLAR-{k[0]}-{k[1]} ({', '.join(slugs)}) finnes på disk")
        elif list(slugs)[0] != reg[k][0]:
            varsler.append(f"SLUG AVVIKER: KLAR-{k[0]}-{k[1]} har slug «{list(slugs)[0]}» på disk og «{reg[k][0]}» i registeret")
    for k, (slug, status) in sorted(reg.items()):
        if k not in disk and status != "reservert":
            varsler.append(f"I REGISTERET, MEN IKKE PÅ DISK: KLAR-{k[0]}-{k[1]} ({slug}), status «{status}»")
        if k in disk and status == "reservert":
            varsler.append(f"RESERVERT, MEN I BRUK: KLAR-{k[0]}-{k[1]}")
    brukt = set(disk) | {k for k, v in reg.items() if v[1] == "reservert"}
    for typ in sorted({k[0] for k in brukt}):
        nr = sorted(int(k[1]) for k in brukt if k[0] == typ)
        hull = [n for n in range(1, nr[-1] + 1) if n not in nr]
        if hull:
            varsler.append(f"HULL: KLAR-{typ} mangler " + ", ".join(f"{n:04d}" for n in hull))
    linjer = []
    for typ in sorted({k[0] for k in brukt}):
        nr = sorted(k[1] for k in brukt if k[0] == typ)
        linjer.append(f"- {typ}: " + ", ".join(nr) + (" (reservert: " + ", ".join(k[1] for k in sorted(brukt) if k[0] == typ and k not in disk) + ")" if any(k[0] == typ and k not in disk for k in brukt) else ""))
    linjer.append(f"- register: {regfil[-1].relative_to(REPO) if regfil else 'mangler'}; {len(reg)} nøkler i registeret, {len(disk)} på disk")
    return linjer, varsler


def seksjon_stempler():
    st = DOCS / "stempler"
    ots = sorted(st.glob("*.ots")) if st.is_dir() else []
    if not ots:
        return ["- ingen .ots-filer i docs/stempler/"]
    prog = REPO / ".venv/bin/ots"
    bekreftet = 0
    for o in ots:
        rc, ut = kjor([str(prog), "info", str(o)])
        bekreftet += "BitcoinBlockHeaderAttestation" in ut
    logg = sorted(st.glob("KLAR-LOG-0002_*.md"))
    return [f"- .ots-filer: {len(ots)}, Bitcoin-bekreftet: {bekreftet}, ventende: {len(ots) - bekreftet}",
            f"- logg: {logg[-1].relative_to(REPO) if logg else 'mangler'}"]


def neste_versjon():
    gamle = sorted(DOCS.glob("KLAR-GT-0001_arkivklarering_ground-truth_v*_*.md"))
    mx = (1, -1)
    for p in gamle:
        m = re.search(r"_v(\d+)\.(\d+)_", p.name)
        if m:
            mx = max(mx, (int(m[1]), int(m[2])))
    return gamle, f"{mx[0]}.{mx[1] + 1}"


def seksjon_kilder():
    """Kilderegisteret (KLAR-KILDE-0001) mekanisk kontrollert mot de lagrede kopiene på Vault (`scripts/sjekk_kilder.py`).
    Returnerer (linjer, varsler): varsler ved sitat som ikke er en delstreng av kopien, manglende kopi eller sha256-avvik,
    og ved påstander i KLAR-dokumenter, README og ADR-er med kildelenke (http-URL) uten rad i registeret."""
    sys.path.insert(0, str(REPO / "scripts"))
    import sjekk_kilder
    if sjekk_kilder.registerfil() is None:
        return ["Kilderegisteret `docs/KLAR-KILDE-0001_*.md` finnes ikke."], ["KILDEREGISTER MANGLER: docs/KLAR-KILDE-0001_*.md"]
    telling, brudd = sjekk_kilder.kontroller()
    mangler = sjekk_kilder.urler_uten_rad()
    linjer = [f"- register: {sjekk_kilder.registerfil().relative_to(REPO)}; {sum(telling.values())} påstander",
              "- status etter mekanisk kontroll (sitat som eksakt delstreng av lagret kopi): " + ", ".join(f"{k} {v}" for k, v in sorted(telling.items())),
              f"- brudd (sitat ikke funnet, manglende kopi eller sha256-avvik): {len(brudd)}",
              f"- kildelenker i KLAR-dokumenter, README og ADR-er uten rad i registeret: {len(mangler)}"]
    varsler = [f"KILDE {b['id']}: {b['grunn']}" for b in brudd]
    varsler += [f"KILDELENKE UTEN RAD: {d} {u}" for d, u in mangler]
    uverifisert = {k: v for k, v in telling.items() if k in ("sitat ikke funnet", "ugyldig")}
    if uverifisert:
        varsler.append(f"UVERIFISERTE PÅSTANDER i kilderegisteret: {uverifisert}")
    return linjer, varsler


def main():
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()  # avbryter hvis cacher og tmp ikke ligger under ARKIVKLARERING_DATA
    gamle, v = neste_versjon()
    nå = datetime.datetime.now().astimezone()
    fast = (DOCS / "gt_fast.md").read_text(encoding="utf-8").rstrip("\n")
    reg_linjer, reg_varsler = nummerregister()
    kilde_linjer, kilde_varsler = seksjon_kilder()
    reg_varsler = reg_varsler + kilde_varsler
    varselblokk = (["## VARSLER", "", *[f"- **{v}**" for v in reg_varsler], ""] if reg_varsler else [])
    deler = [
        f"# KLAR-GT-0001: Ground truth (generert fra disk)",
        "",
        "**Tilstand påstås aldri fra minne eller chat. Les denne fila eller disken.**",
        "",
        f"Versjon {v}. Generert {nå.isoformat(timespec='seconds')} av `scripts/ground_truth.py`. "
        "Alt utenom «Håndført» er lest fra disk ved generering. HEAD under er commiten som var utsjekket da "
        "fila ble generert; GT-fila selv committes etterpå.",
        "",
        *varselblokk,
        "## Git og GitHub", "", *seksjon_git(), "",
        "## Modellfiler", "", *seksjon_modeller(), "",
        "## Tester", "", *seksjon_pytest(), "",
        "## KLAR-dokumenter", "", *seksjon_dokumenter(), "",
        "## Nummerregister (KLAR-ARK-0003 mot disken)", "", *reg_linjer, "", ("Varsler: ingen." if not reg_varsler else f"Varsler: {len(reg_varsler)} (se VARSLER øverst)."), "",
        "## Kilderegister (KLAR-KILDE-0001 mot lagrede kopier på Vault)", "", *kilde_linjer, "",
        "## Siste eval-resultater", "", *seksjon_eval(), "",
        "## Vault", "", *seksjon_vault(), "",
        "## Tidsstempler (OpenTimestamps)", "", *seksjon_stempler(), "",
        "## Håndført (fra docs/gt_fast.md, ikke generert)", "", fast, "",
    ]
    ut = DOCS / f"KLAR-GT-0001_arkivklarering_ground-truth_v{v}_{nå.date().isoformat()}.md"
    ut.write_text("\n".join(deler), encoding="utf-8")
    for g in gamle:
        if g != ut:
            if kjor(["git", "ls-files", "--error-unmatch", str(g)])[0] == 0:
                kjor(["git", "rm", "-q", "-f", str(g)])
            else:
                g.unlink()
    print(ut)
    for v in reg_varsler:
        print("VARSEL:", v, file=sys.stderr)


if __name__ == "__main__":
    main()
