#!/bin/bash
#
# kjor_testdel.sh: kjører testdelene (H1–H4) én og én utenfra, og etter HVER del committer den resultat og kjøringsmetadata, pusher (privat)
# og kjører scripts/speil.sh før neste del starter. Analysekoden er uendret; skriptet bare starter den.
#
#   source scripts/miljo.sh && scripts/kjor_testdel.sh [--tor] <H1|H2|H3|H4|alle> --prereg-id KLAR-PREREG-0001 [-- ekstra argumenter]
#
#   H1  eval/dev/kjor_dev.py --splitt test --per-dialekt 60 ... --eval-nr KLAR-EVAL-0013   (NB Samtale test; PREREG: opptil 60 per dialektområde)
#   H2  eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --mal-person 300 --mal-sted 200 --maks-timer 4 ... --eval-nr KLAR-EVAL-0014   (PREREG: doble mål)
#   H3  eval/dev/kjor_personvern_dev.py --splitt test ... --eval-nr KLAR-EVAL-0015      (NorNE test)
#   H4  kalibrering/kjor_h4.py --opptak /Volumes/Vault/arkivklarering/lyd/h4          (menneskeinnlest testmanus, innlest med scripts/rigg_manus.py; skriver docs/KLAR-EVAL-0009_...)
#   Segmentering (KLAR-ADR-0019 v1.1, AV-25): standarden i koden er inaSpeechSegmenter, men de preregistrerte H1 og H2 brukte inaVAMOS. H1 og H2
#       startes derfor uendret, men med ARKIVKLARERING_SEGMENTERING=inavamos satt eksplisitt (krever tillegget reproduksjon-h1h2; uten det feiler
#       delen med en melding om installasjon og lisens). H3 segmenterer ikke og kjøres uendret, med kallerens miljø. H4 kjøres med
#       ARKIVKLARERING_SEGMENTERING=inaseg (inaSpeechSegmenter; inaVAMOS brukes ikke); segmenteringsloggen eval/test/h4_segmenteringslogg_<tid>.jsonl
#       og et sammendrag føres i kjoring_meta. Verdien for hver del føres i kjoring_meta («segmentering.miljovariabel»).
#   H1–H3 skriver til eval/test/ med --etikett TEST (merknad «TEST – preregistrert (OSF hc83q)»).
#   alle = H1, H2, H3, H4 i den rekkefølgen (H4 til sist: opptakene må være innlest og scoret først, se PREREG).
#
# Før hver del: (1) `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1); (2) koden må være uendret siden
# taggen `testkjoring-v12` (`git diff --quiet testkjoring-v12 -- arkivklarering kalibrering tests scripts` og alle .py-filer under eval/), ellers kjøres
# ingenting (exit 5; mangler taggen, er det også exit 5). Kravet er IKKE at HEAD er taggen: resultat-commitene (docs/, eval/test/) er tillatt. Etter hver del skrives
# <resultat>_kjoring_meta.json (commit-SHA ved start, tom porcelain, kommando, tider, returkode, resultatfiler, SHA-ene til taggene og sha256 for PREREG-
# og MANUS-fila). Så: commit av resultat og metafil, push, speil. Stopper hele kjøringen (ingen neste del) hvis en del feiler, hvis en SPORET fil er
# endret av kjøringen (da committes ingenting, exit 4; fjerner ikke noe), eller hvis commit, push eller speil feiler. Feilede deler committes (med
# returkoden i metafila) og stopper deretter. --tor skriver bare hva som ville blitt kjørt.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
PY="${KLAR_PY:-.venv/bin/python}"
SPEIL="${KLAR_SPEIL:-scripts/speil.sh}"
REMOTE="${KLAR_REMOTE:-origin}"
TOR=0; DEL=""; ID=""; EKSTRA=()
while [ $# -gt 0 ]; do
  case "$1" in
    --tor) TOR=1 ;;
    --prereg-id) ID="${2:?mangler verdi til --prereg-id}"; shift ;;
    --) shift; EKSTRA=("$@"); break ;;
    H1|H2|H3|H4|alle) DEL="$1" ;;
    *) echo "ukjent argument: $1" >&2; exit 2 ;;
  esac
  shift
done
[ -n "$DEL" ] && [ -n "$ID" ] || { echo "bruk: kjor_testdel.sh [--tor] <H1|H2|H3|H4|alle> --prereg-id KLAR-PREREG-<NNNN> [-- ekstra]" >&2; exit 2; }
if [ "$DEL" = alle ]; then DELER=(H1 H2 H3 H4); else DELER=("$DEL"); fi
# kallerens segmenteringsmiljø, så H3 kjøres med det uendret også etter H1/H2 i «alle»
SEG_KALLER_SATT="${ARKIVKLARERING_SEGMENTERING+1}"; SEG_KALLER="${ARKIVKLARERING_SEGMENTERING-}"
LOGG_KALLER_SATT="${ARKIVKLARERING_SEGMENTERING_LOGG+1}"; LOGG_KALLER="${ARKIVKLARERING_SEGMENTERING_LOGG-}"

kommando() {  # skriver skriptet og argumentene for en del, ett ord per linje
  case "$1" in
    H1) printf '%s\n' eval/dev/kjor_dev.py --splitt test --prereg-id "$ID" --per-dialekt 60 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0013 ;;
    H2) printf '%s\n' eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --prereg-id "$ID" --mal-person 300 --mal-sted 200 --maks-timer 4 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0014 ;;
    H3) printf '%s\n' eval/dev/kjor_personvern_dev.py --splitt test --prereg-id "$ID" --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015 ;;
    # H4: fast sti, den samme som H4_ROT i den låste innleseren (arkivklarering/h4_innlesing.py, h4-rigg-v3); følger ikke ARKIVKLARERING_DATA
    H4) printf '%s\n' kalibrering/kjor_h4.py --prereg-id "$ID" --opptak /Volumes/Vault/arkivklarering/lyd/h4 ;;
  esac
}

segmentering_for() {  # ARKIVKLARERING_SEGMENTERING for en del (tom = kallerens miljø, uendret)
  case "$1" in
    H1|H2) echo inavamos ;;   # preregistrert med inaVAMOS; standarden i koden er nå inaseg
    H4) echo inaseg ;;
    *) echo "" ;;
  esac
}

sett_segmentering() {  # setter miljøet for del $1 og tidsstempel $2
  case "$1" in
    H1|H2) export ARKIVKLARERING_SEGMENTERING=inavamos; unset ARKIVKLARERING_SEGMENTERING_LOGG ;;
    H4) export ARKIVKLARERING_SEGMENTERING=inaseg ARKIVKLARERING_SEGMENTERING_LOGG="eval/test/h4_segmenteringslogg_$2.jsonl" ;;
    *)
      if [ -n "$SEG_KALLER_SATT" ]; then export ARKIVKLARERING_SEGMENTERING="$SEG_KALLER"; else unset ARKIVKLARERING_SEGMENTERING; fi
      if [ -n "$LOGG_KALLER_SATT" ]; then export ARKIVKLARERING_SEGMENTERING_LOGG="$LOGG_KALLER"; else unset ARKIVKLARERING_SEGMENTERING_LOGG; fi ;;
  esac
}

rent_eller_stopp() {
  local p; p="$(git status --porcelain)"
  if [ -n "$p" ]; then
    echo "FEIL: arbeidstreet er ikke rent; kjører ikke. git status --porcelain:" >&2
    echo "$p" >&2
    exit 1
  fi
}

kode_uendret_eller_stopp() {
  local TAGG="${KLAR_KODETAGG:-testkjoring-v12}"
  if ! git rev-parse -q --verify "refs/tags/$TAGG^{commit}" >/dev/null; then
    echo "FEIL: taggen $TAGG finnes ikke; kan ikke vise at koden er uendret. Kjører ikke." >&2
    exit 5
  fi
  if ! git diff --quiet "$TAGG" -- arkivklarering kalibrering tests scripts ':(glob)eval/**/*.py'; then
    echo "FEIL: koden er endret siden taggen $TAGG; kjører ikke. Endrede filer:" >&2
    git diff --name-only "$TAGG" -- arkivklarering kalibrering tests scripts ':(glob)eval/**/*.py' >&2
    exit 5
  fi
}

rent_eller_stopp
kode_uendret_eller_stopp
if [ "$TOR" -eq 1 ]; then
  for d in "${DELER[@]}"; do
    K=(); while IFS= read -r l; do K+=("$l"); done < <(kommando "$d")
    S="$(segmentering_for "$d")"
    echo "(--tor) $d ville kjørt på $(git rev-parse HEAD): ${S:+ARKIVKLARERING_SEGMENTERING=$S }$PY ${K[*]} ${EKSTRA[*]:-}"
  done
  exit 0
fi

for d in "${DELER[@]}"; do
  rent_eller_stopp   # etter forrige dels commit skal treet være rent igjen
  kode_uendret_eller_stopp   # og koden fortsatt som i taggen (bare resultat-commiter er kommet til)
  K=(); while IFS= read -r l; do K+=("$l"); done < <(kommando "$d")
  SHA="$(git rev-parse HEAD)"
  KMD="$PY ${K[*]} ${EKSTRA[*]:-}"
  PRE="$(ls docs/${ID}_*.md | sort -V | tail -1)"
  MAN="$(ls kalibrering/KLAR-MANUS-0002_*.tsv | sort -V | tail -1)"
  TID="$(date +%Y%m%d-%H%M%S)"
  START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  sett_segmentering "$d" "$TID"
  echo "== $d ($KMD; ARKIVKLARERING_SEGMENTERING=${ARKIVKLARERING_SEGMENTERING:-<ikke satt>}) på $SHA"
  set +e
  "$PY" "${K[@]}" "${EKSTRA[@]+"${EKSTRA[@]}"}"
  RC=$?
  set -e
  SLUTT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  ENDRET="$(git status --porcelain --untracked-files=no)"
  if [ -n "$ENDRET" ]; then
    echo "STOPP: kjøringen endret sporede filer; ingenting committet, ingen neste del. Sjekk med git diff (ingenting er fjernet eller tilbakestilt):" >&2
    echo "$ENDRET" >&2
    exit 4
  fi
  NYE="$(git status --porcelain --untracked-files=all | sed 's/^?? //' | sort)"
  RES="$(echo "$NYE" | grep -E '^(docs|eval/dev|eval/test)/KLAR-EVAL.*\.json$' | grep -v '\.utvalg\.json$' | head -1 || true)"
  [ -n "$RES" ] || RES="$(echo "$NYE" | grep -E '\.json$' | head -1 || true)"
  if [ -n "$RES" ]; then META="${RES%.json}_kjoring_meta.json"; else META="docs/kjoring_meta_${d}_$TID.json"; fi
  export META SHA START SLUTT RC KMD PRE MAN RES DEL_NAVN="$d" NYE
  export TAG_PREREG="$(git rev-parse -q --verify 'refs/tags/prereg-v1^{commit}' || echo mangler)"
  export TAG_H4="$(git rev-parse -q --verify 'refs/tags/h4-script-v2^{commit}' || echo mangler)"
  export TAG_KODE="$(git rev-parse -q --verify "refs/tags/${KLAR_KODETAGG:-testkjoring-v12}^{commit}" || echo mangler)"
  export TAG_KODE_NAVN="${KLAR_KODETAGG:-testkjoring-v12}"
  export TAG_KODE_V1="$(git rev-parse -q --verify 'refs/tags/testkjoring-v1^{commit}' || echo mangler)"
  export SHA_PRE="$(shasum -a 256 "$PRE" | cut -d' ' -f1)" SHA_MAN="$(shasum -a 256 "$MAN" | cut -d' ' -f1)"
  "$PY" - <<'PYEOF'
import json, os
e = os.environ
ut = {"del": e["DEL_NAVN"], "commit": e["SHA"], "git_status_porcelain_ved_start": [], "kommando": e["KMD"], "start_utc": e["START"], "slutt_utc": e["SLUTT"],
      "returkode": int(e["RC"]), "resultatfil": e["RES"] or None, "nye_filer": [x for x in e["NYE"].split("\n") if x],
      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"], "tag_testkjoring": {"navn": e["TAG_KODE_NAVN"], "commit": e["TAG_KODE"]}, "tag_testkjoring_v1": e["TAG_KODE_V1"], "kode_uendret_siden_tagg": True,
      "preregistrering": {"fil": e["PRE"], "sha256": e["SHA_PRE"]}, "manus": {"fil": e["MAN"], "sha256": e["SHA_MAN"]}}
seg = {"miljovariabel": e.get("ARKIVKLARERING_SEGMENTERING"), "logg": e.get("ARKIVKLARERING_SEGMENTERING_LOGG")}
if seg["logg"] and os.path.exists(seg["logg"]):
    linjer = [json.loads(l) for l in open(seg["logg"], encoding="utf-8") if l.strip()]
    seg["antall_loggede_kall"] = sum(1 for l in linjer if not l.get("sammendrag"))
    seg["sammendrag"] = next((l for l in reversed(linjer) if l.get("sammendrag")), None)
ut["segmentering"] = seg
open(e["META"], "w", encoding="utf-8").write(json.dumps(ut, ensure_ascii=False, indent=2) + "\n")
print(e["META"])
PYEOF
  git add -A
  git commit -q -m "Testdel $d: resultat og kjøringsmetadata (returkode $RC, start på ${SHA:0:7})"
  git push -q "$REMOTE" HEAD
  bash "$SPEIL"
  if [ "$RC" -ne 0 ]; then echo "STOPP: $d feilet (returkode $RC); resultat og metafil er committet, pushet og speilet. Ingen neste del." >&2; exit "$RC"; fi
done
