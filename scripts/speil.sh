#!/usr/bin/env bash
# speil.sh: tre kopier av arkivklarering.
#   (1) GitHub (privat), (2) Vault /Volumes/Vault/arkivklarering/ (eller $ARKIVKLARERING_DATA hvis satt), (3) ~/Desktop/Master Dok./Arkivklarering/
# Gjør (2) og (3) og sammenligner sha256 for docs/ på tvers av arbeidstre, GitHub, Vault-bundle og Master Dok.
# Kjøres til slutt i hver CC-kjøring, etter scripts/ground_truth.py, og etter at commit er pushet.
#
# Ikke montert Vault (når (2) ligger på Vault) eller manglende mappe for (2) = STOPP (exit 3), ingen stille hopp.
# Desktop er iCloud-synket: aldri `>` mot Desktop. Nye filer opprettes med ditto, eksisterende overskrives med tee.
# MASTER og POINTER lages ikke her (versjoneres med ~/bin/bump-master.sh) og committes aldri; speil.sh sjekker dem bare.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
VAULT=/Volumes/Vault
VA="${ARKIVKLARERING_DATA:-$VAULT/arkivklarering}"   # (2): datarota hvis satt, ellers Vault
export ARKIVKLARERING_DATA="$VA"   # miljo.sh setter cacher og tmp under samme rot
MD="$HOME/Desktop/Master Dok./Arkivklarering"
GH_REPO=avalyset/arkivklarering
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cd "$REPO"
source "$REPO/scripts/miljo.sh" || exit 3   # alt tungt på Vault; avbryter hvis miljøet peker utenfor

echo "== (2) Vault ($VA)"
case "$VA" in
  "$VAULT"|"$VAULT"/*)
    if ! mount | grep -q " on $VAULT "; then
      echo "STOPP: Vault er ikke montert ($VAULT). Speiling til Vault og sammenligning er ikke gjort." >&2
      exit 3
    fi ;;
esac
if [ ! -d "$VA" ]; then
  echo "STOPP: $VA finnes ikke. Speiling og sammenligning er ikke gjort." >&2
  exit 3
fi
mkdir -p "$VA/repo-bundle" "$VA/modeller" "$VA/lyd" "$VA/eval-data"

# modeller: skal ligge under $VA og stemme med modeller.lock.json («standardsti» er relativ til datarota); repoet har bare en symlink
python3 - "$REPO" "$VA" <<'PY'
import hashlib, json, os, pathlib, sys
repo, va = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
lock = json.loads((repo / "modeller.lock.json").read_text())
feil = 0
for lag in ("ra", "normalisert"):
    l = lock[lag]; p = pathlib.Path(l["standardsti"]); p = p if p.is_absolute() else va / p
    if not p.is_file() or va not in p.parents:
        print(f"  modell {lag}: FEIL, {p} ligger ikke under {va}"); feil += 1; continue
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while b := f.read(1 << 24): h.update(b)
    ok = h.hexdigest() == l["sha256"]
    print(f"  modell {lag}: {p.name} sha256 {'OK' if ok else 'AVVIK'} {h.hexdigest()}"); feil += (not ok)
lenke = repo / "modeller"
if not (lenke.is_symlink() and os.path.realpath(lenke) == os.path.realpath(va / "modeller")):
    print(f"  repo/modeller er ikke symlink til {va / 'modeller'}"); feil += 1
sys.exit(1 if feil else 0)
PY

# lyd og eval-data: lyd/ speiles hvis den er en ekte mappe; eval-data ligger allerede i Vault (symlink eval/data)
if [ -d lyd ] && [ ! -L lyd ]; then rsync -a lyd/ "$VA/lyd/"; echo "  lyd/ -> $VA/lyd/"; fi
[ -e "$VA/eval-data/nb_samtale" ] && echo "  eval-data/nb_samtale finnes" || echo "  ADVARSEL: eval-data/nb_samtale mangler"

echo "== tidsstempler (OpenTimestamps)"
if [ -x .venv/bin/ots ]; then
  .venv/bin/python scripts/stempel.py || echo "  ADVARSEL: stempel.py rapporterte feil (se over)"
  [ -z "$(git status --porcelain docs/stempler)" ] || echo "  NB: nye eller endrede stempler er ikke committet; commit og push, og kjør speil.sh på nytt"
else
  echo "  ADVARSEL: ots mangler i .venv; stempling og upgrade er hoppet over"
fi
mkdir -p "$VA/stempler"
rsync -a --delete --exclude '*.bak' docs/stempler/ "$VA/stempler/"
echo "  docs/stempler/ -> $VA/stempler/ ($(ls "$VA/stempler" | wc -l | tr -d ' ') filer)"

# git bundle
[ -z "$(git status --porcelain)" ] || echo "  ADVARSEL: arbeidstreet er ikke rent; bundlen inneholder bare det som er committet"
SHA="$(git rev-parse --short HEAD)"
B="$VA/repo-bundle/arkivklarering_$(date +%Y-%m-%d)_${SHA}.bundle"
[ -e "$B" ] || git bundle create "$B" --all >/dev/null 2>&1
git bundle verify "$B" >/dev/null 2>&1 && echo "  bundle OK: $B ($(stat -f %z "$B") byte)" || { echo "FEIL: git bundle verify feilet for $B" >&2; exit 1; }
git clone -q "$B" "$TMP/bundle" 2>/dev/null
# bundlen har alle grener; sjekk ut main ved HEAD
git -C "$TMP/bundle" checkout -q "$(git rev-parse HEAD)" 2>/dev/null

echo "== (3) Master Dok."
kopier() {  # kopier <kilde> <mål>: ditto for nye filer, tee for å overskrive; hopp over like filer
  local src="$1" dst="$2"
  if [ -e "$dst" ]; then
    if [ "$(shasum -a 256 < "$src" | cut -d' ' -f1)" != "$(shasum -a 256 < "$dst" | cut -d' ' -f1)" ]; then
      tee "$dst" < "$src" >/dev/null
    fi
  else
    ditto --noextattr --noacl --noqtn "$src" "$dst"
  fi
}
if [ ! -d "$MD/arkiv" ]; then
  echo "  ADVARSEL: $MD/arkiv finnes ikke ennå (MASTER og POINTER opprettes av CC-kjøringen første gang)"
fi
while IFS= read -r -d '' f; do
  kopier "$f" "$MD/docs/${f#docs/}"
done < <(find docs -type f -not -name '.DS_Store' -not -name '*.bak' -print0)
# filer som ikke lenger finnes i repoets docs/ (omdøpt eller erstattet versjon) fjernes fra speilet, én og én sti
if [ -d "$MD/docs" ]; then
  while IFS= read -r -d '' g; do
    rel="${g#"$MD/docs/"}"
    if [ ! -e "docs/$rel" ]; then
      rm -f "$g" && echo "  fjernet utdatert: docs/$rel" || echo "  ADVARSEL: kunne ikke fjerne $g (ekstern blokk?)"
    fi
  done < <(find "$MD/docs" -type f -not -name '.DS_Store' -print0)
fi
n0=$(find "$MD" -type f -size 0 2>/dev/null | wc -l | tr -d ' ')
echo "  filer med 0 byte under Master Dok./Arkivklarering: $n0"
[ "$n0" = 0 ] || { echo "FEIL: 0-byte-filer (iCloud-placeholder?)" >&2; exit 1; }
if [ -f "$MD/arkiv/POINTER.txt" ]; then
  T="$(tr -d '\n' < "$MD/arkiv/POINTER.txt")"
  [ -f "$MD/arkiv/$T" ] && echo "  POINTER -> $T (finnes)" || { echo "FEIL: POINTER peker på $T som ikke finnes" >&2; exit 1; }
fi

# stempler i Vault sammenlignes med arbeidstreet
if diff -rq --exclude "*.bak" docs/stempler "$VA/stempler" >/dev/null; then echo "  Vault/stempler: sha256-match med arbeidstreet = ja"; else echo "  Vault/stempler: NEI"; diff -rq --exclude "*.bak" docs/stempler "$VA/stempler" | head -5; fi

echo "== sha256 for docs/ på tvers av arbeidstre, GitHub, Vault-bundle og Master Dok."
GITHUB_TOKEN= GH_TOKEN= python3 - "$REPO" "$TMP/bundle" "$MD" "$GH_REPO" <<'PY'
import hashlib, os, pathlib, subprocess, sys
repo, bundle, md, gh = (pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), sys.argv[4])
def sha(b): return hashlib.sha256(b).hexdigest()
def tre(rot):
    d = rot / "docs"
    return {str(p.relative_to(rot)): sha(p.read_bytes()) for p in sorted(d.rglob("*")) if p.is_file() and p.name != ".DS_Store" and not p.name.endswith(".bak")} if d.is_dir() else {}
arb, bun = tre(repo), tre(bundle)
des = {k: v for k, v in tre(md.parent / md.name).items()} if (md / "docs").is_dir() else {}
dd = {}
if (md / "docs").is_dir():
    dd = {"docs/" + str(p.relative_to(md / "docs")): sha(p.read_bytes()) for p in sorted((md / "docs").rglob("*")) if p.is_file() and p.name != ".DS_Store" and not p.name.endswith(".bak")}
env = {**os.environ, "GITHUB_TOKEN": "", "GH_TOKEN": ""}
git = {}
for k in arb:
    r = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw", f"repos/{gh}/contents/{k}?ref=main"],
                       capture_output=True, env=env)
    git[k] = sha(r.stdout) if r.returncode == 0 else None
alle = sorted(set(arb) | set(bun) | set(dd))
kopier = {"GitHub": git, "Vault-bundle": bun, "Master Dok.": dd}
avvik = {n: [] for n in kopier}
for k in alle:
    for n, d in kopier.items():
        if d.get(k) != arb.get(k):
            avvik[n].append((k, "mangler" if d.get(k) is None else "annen sha256"))
print(f"  filer i arbeidstreets docs/: {len(arb)}")
rc = 0
for n in kopier:
    ok = not avvik[n]
    print(f"  {n}: sha256-match med arbeidstreet = {'ja' if ok else 'NEI'} ({len(arb) - len([a for a in avvik[n] if a[0] in arb])}/{len(arb)} like" + (f", {len([a for a in avvik[n] if a[0] not in arb])} ekstra" if any(a[0] not in arb for a in avvik[n]) else "") + ")")
    for k, why in avvik[n]:
        print(f"     {why}: {k}")
    rc |= (not ok)
sys.exit(1 if rc else 0)
PY
