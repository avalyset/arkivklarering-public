#!/usr/bin/env python3
"""Mekanisk kontroll av kilderegisteret `docs/KLAR-KILDE-0001_*.md`.

For hver rad: finn den lagrede kopien under datarota (`$ARKIVKLARERING_DATA/kilder/`, på Vault `/Volumes/Vault/arkivklarering/kilder/`), kontroller sha256, trekk ut tekst
(`pdftotext -layout` for PDF; HTML med lxml, blokkelementer skilles med linjeskift; ren tekst som den er), normaliser BARE
mellomrom og linjeskift (alle blanke tegn → ett mellomrom), og bekreft at sitatet finnes som eksakt delstreng. Utelatelser i
sitatet er markert med «[…]»; hvert fragment mellom dem må finnes, i rekkefølge. Treffer et fragment ikke, blir statusen
«sitat ikke funnet» og påstanden regnes som uverifisert.

Registerets tabell har kolonnene
    påstand-id | påstand | dokument:linje | kilde-URL | kildetype | hentet | sha256 | sitat (side/avsnitt) | tolkning | status
og sitatet står i anførselstegn «…» i sitatcellen, foran «(side/avsnitt)». Kildefilen står i kolonnen «kopi»: kildenøkkelen
(`K01` …) i sha256-cellen peker på en rad i tabellen «Kilder» (nøkkel | URL | type | hentet | fil | sha256 | sider).

    source scripts/miljo.sh && .venv/bin/python scripts/sjekk_kilder.py            # skriver status og brudd, exit 1 ved brudd
    .venv/bin/python scripts/sjekk_kilder.py --uten-vault                           # bare registerstruktur (ingen kopier)

Fra `ground_truth.py`: `from sjekk_kilder import kontroller, urler_uten_rad` (se funksjonene under).
"""
from __future__ import annotations

import glob
import hashlib
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from arkivklarering.miljo import DATA  # noqa: E402

KILDER = DATA / "kilder"
GYLDIGE_STATUS = ("verifisert", "delvis", "ikke funnet", "motsagt")
BLOKK = {"p", "div", "li", "ul", "ol", "br", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "td", "th", "table", "pre", "section", "article",
         "blockquote", "dd", "dt", "dl", "header", "footer", "nav", "main", "aside", "figure", "figcaption", "title", "summary", "details"}


def normaliser(s: str) -> str:
    """Bare mellomrom og linjeskift: alle blanke tegn (også NBSP) blir ett mellomrom."""
    return re.sub(r"\s+", " ", s).strip()


def sha256_fil(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _html_til_tekst(data: bytes) -> str:
    import lxml.html
    m = re.search(rb"charset=[\"']?([A-Za-z0-9_-]+)", data[:4096], re.I)
    kode = m.group(1).decode("ascii") if m else "utf-8"
    try:
        tekst = data.decode(kode)
    except (LookupError, UnicodeDecodeError):
        tekst = data.decode("utf-8", errors="replace")
    tekst = re.sub(r"^\s*<\?xml[^>]*\?>", "", tekst)
    doc = lxml.html.fromstring(tekst)
    for el in doc.xpath("//script|//style|//noscript|//template"):
        el.getparent().remove(el)
    for el in doc.iter():
        if not isinstance(el.tag, str):
            continue
        if el.tag in BLOKK:
            el.text = "\n" + (el.text or "")
            el.tail = "\n" + (el.tail or "")
    return doc.text_content()


def tekst_fra_kopi(sti) -> str:
    """Ren tekst fra den lagrede kopien (ikke normalisert)."""
    sti = pathlib.Path(sti)
    suf = sti.suffix.lower()
    if suf == ".pdf":
        r = subprocess.run(["pdftotext", "-layout", str(sti), "-"], capture_output=True, check=True)
        return r.stdout.decode("utf-8", errors="replace")
    data = sti.read_bytes()
    if suf in (".html", ".htm"):
        return _html_til_tekst(data)
    return data.decode("utf-8", errors="replace")


def sider_i_pdf(sti) -> list[str]:
    """Teksten per side (form feed skiller sidene i pdftotext), for å oppgi sidetall."""
    return tekst_fra_kopi(sti).split("\f")


def finn_sitat(tekst_norm: str, sitat: str) -> bool:
    """Sitatet (med «[…]» for utelatelser) finnes som eksakte delstrenger i rekkefølge i den normaliserte teksten."""
    fragmenter = [normaliser(f) for f in re.split(r"\[…\]|\[\.\.\.\]", sitat)]
    fragmenter = [f for f in fragmenter if f]
    if not fragmenter:
        return False
    pos = 0
    for f in fragmenter:
        i = tekst_norm.find(f, pos)
        if i < 0:
            return False
        pos = i + len(f)
    return True


# ----------------------------------------------------------------------------------------------------------------- register
def _versjon(sti) -> tuple[int, int]:
    """(major, minor) fra `_v<maj>.<min>_` i filnavnet; v1.10 kommer etter v1.9 (ikke leksikografisk)."""
    m = re.search(r"_v(\d+)\.(\d+)_", pathlib.Path(sti).name)
    return (int(m.group(1)), int(m.group(2))) if m else (-1, -1)


def registerfil(docs=None) -> pathlib.Path | None:
    f = sorted(glob.glob(str(pathlib.Path(docs or REPO / "docs") / "KLAR-KILDE-0001_*.md")), key=_versjon)
    return pathlib.Path(f[-1]) if f else None


def _celler(linje: str) -> list[str]:
    s = linje.strip().strip("|")
    ut, cur, i = [], "", 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur += "|"
            i += 2
            continue
        if s[i] == "|":
            ut.append(cur.strip())
            cur = ""
        else:
            cur += s[i]
        i += 1
    ut.append(cur.strip())
    return ut


def les_register(sti=None):
    """(kilder, paastander). kilder: {nokkel: {...}}; paastander: [{id, paastand, dok, url, kildetype, hentet, kilde, sitat_celle, sitat, tolkning, status}]."""
    sti = pathlib.Path(sti) if sti else registerfil()
    if not sti or not sti.exists():
        return {}, []
    kilder, pst = {}, []
    modus = None
    for linje in sti.read_text(encoding="utf-8").splitlines():
        if linje.startswith("## "):
            tittel = linje[3:].strip().lower()
            modus = "kilder" if tittel == "kilder" else ("pst" if tittel.startswith("påstander") else None)
            continue
        if not linje.startswith("|") or modus is None:
            continue
        c = _celler(linje)
        if c[0] in ("nøkkel", "påstand-id") or set(c[0]) <= {"-", " ", ":"}:
            continue
        if modus == "kilder" and len(c) >= 7:
            kilder[c[0]] = {"nokkel": c[0], "url": c[1], "kildetype": c[2], "hentet": c[3], "fil": (re.search(r"`([^`]+)`", c[4]) or re.search(r"(.+)", c[4])).group(1), "sha256": c[5].strip("`"), "sider": c[6]}
        elif modus == "pst" and len(c) >= 10:
            m = re.search(r"«(.*)»", c[7], re.S)
            pst.append({"id": c[0], "paastand": c[1], "dok": c[2], "url": c[3], "kildetype": c[4], "hentet": c[5], "kilde": c[6],
                        "sitat_celle": c[7], "sitat": (m.group(1) if m else ""), "tolkning": c[8], "status": c[9]})
    return kilder, pst


def kontroller(sti=None, vault: bool = True):
    """Returnerer (antall per status, brudd). Brudd er dicts {id, grunn}. Status etter mekanisk kontroll:
    verifisert / delvis / ikke funnet / motsagt (som ført) og «sitat ikke funnet» (uverifisert) når sitatet ikke er en delstreng
    av den lagrede kopien, eller når kopien mangler / har feil sha256 / registerrader mangler felter."""
    kilder, pst = les_register(sti)
    brudd, telling = [], {}
    cache = {}
    for p in pst:
        status = p["status"].strip().lower()
        if status not in GYLDIGE_STATUS:
            brudd.append({"id": p["id"], "grunn": f"ugyldig status «{p['status']}»"})
            status = "ugyldig"
        k = kilder.get(p["kilde"])
        if status in ("ikke funnet",) and not p["sitat"]:
            telling[status] = telling.get(status, 0) + 1
            continue
        if k is None:
            brudd.append({"id": p["id"], "grunn": f"kilde «{p['kilde']}» finnes ikke i tabellen «Kilder»"})
            status = "sitat ikke funnet"
        elif not p["sitat"]:
            brudd.append({"id": p["id"], "grunn": "tomt sitat"})
            status = "sitat ikke funnet"
        elif vault:
            fil = (KILDER / k["fil"]).resolve()
            if KILDER.resolve() not in fil.parents:
                brudd.append({"id": p["id"], "grunn": f"kopien {k['fil']} ligger utenfor kildemappen"})
                status = "sitat ikke funnet"
            elif not fil.exists():
                brudd.append({"id": p["id"], "grunn": f"kopien {k['fil']} finnes ikke på Vault"})
                status = "sitat ikke funnet"
            else:
                if k["nokkel"] not in cache:
                    sha = sha256_fil(fil)
                    cache[k["nokkel"]] = (sha, normaliser(tekst_fra_kopi(fil)))
                sha, tekst = cache[k["nokkel"]]
                if sha != k["sha256"]:
                    brudd.append({"id": p["id"], "grunn": f"sha256 av {k['fil']} er {sha[:12]}…, registeret har {k['sha256'][:12]}…"})
                    status = "sitat ikke funnet"
                elif not finn_sitat(tekst, p["sitat"]):
                    brudd.append({"id": p["id"], "grunn": f"sitatet er ikke en delstreng av {k['fil']}"})
                    status = "sitat ikke funnet"
        telling[status] = telling.get(status, 0) + 1
    return telling, brudd


URL_RE = re.compile(r"https?://[^\s)>\]`\"'|]+")
# URL-er som ikke er faktakilder, men egne artefakter (OSF-registreringen, eget repo, malens skjema)
HOPP_OVER = ("osf.io/", "api.osf.io/", "github.com/avalyset/", "creativecommons.org/publicdomain/zero/1.0/\n")


def _norm_url(u: str) -> str:
    """Skjema og avsluttende skråstrek teller ikke (http = https)."""
    return re.sub(r"^https?://", "", u.split("#")[0]).rstrip("/").rstrip(".,;:")


def urler_uten_rad(dokumenter=None, sti=None):
    """Kildelenker (http-URL-er) i KLAR-dokumenter, README og ADR-er som ikke står i registeret (verken som påstandens URL eller som
    kildens URL). Returnerer [(dokument:linje, url)]. Egne artefakter (OSF-registreringen, eget GitHub-repo) hoppes over."""
    kilder, pst = les_register(sti)
    kjente = {u.rstrip("/.,;") for u in [k["url"] for k in kilder.values()] + [p["url"] for p in pst]}
    kjente_norm = {_norm_url(u) for u in kjente}
    if dokumenter is None:
        dokumenter = [REPO / "README.md"] + sorted((REPO / "docs").glob("KLAR-*.md")) + sorted((REPO / "docs" / "adr").glob("KLAR-*.md"))
    ut = []
    for d in dokumenter:
        d = pathlib.Path(d)
        if d.name.startswith("KLAR-KILDE-") or d.name.startswith("KLAR-GT-"):
            continue
        for n, linje in enumerate(d.read_text(encoding="utf-8").splitlines(), 1):
            for u in URL_RE.findall(linje):
                u = u.rstrip(".,;:")
                if any(h in u for h in HOPP_OVER) or "<" in u or "{" in u:
                    continue
                if _norm_url(u) not in kjente_norm:
                    ut.append((f"{d.relative_to(REPO)}:{n}", u))
    return ut


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    vault = "--uten-vault" not in argv
    telling, brudd = kontroller(vault=vault)
    mangler = urler_uten_rad()
    print("påstander per status:", ", ".join(f"{k}: {v}" for k, v in sorted(telling.items())) or "ingen rader")
    for b in brudd:
        print(f"  BRUDD {b['id']}: {b['grunn']}")
    for d, u in mangler:
        print(f"  URL UTEN RAD {d}: {u}")
    return 1 if (brudd or mangler) else 0


if __name__ == "__main__":
    sys.exit(main())
