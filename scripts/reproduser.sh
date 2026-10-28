#!/bin/bash
#
# reproduser.sh — kjører alle EVAL-ene i rekkefølge fra rådata (datasettene og lyden under ARKIVKLARERING_DATA, på Vault) og skriver sha256 for hvert resultat.
#
#   source scripts/miljo.sh && scripts/reproduser.sh [--tor] [--bare 1,5,7] [--uten-cache] [--med-h4 KLAR-PREREG-0001] [--tillat-urent]
#
# Hvordan: skriptet lager en frittstående git-worktree av HEAD under $ARKIVKLARERING_DATA/reproduksjon/<tid>/tre og kjører
# eval-skriptene der, så de committede resultatfilene aldri overskrives. Resultatene (nye filer og endrede filer i worktreet)
# kopieres til <ut>/resultater/, og sha256 for hver skrives til <ut>/sha256.txt sammen med sha256 av den committede filen med samme
# EVAL-nøkkel (til informasjon: Whisper-kjøring i batcher er ikke bitidentisk, så ulik sha256 betyr ikke automatisk ulike tall;
# sammenlign tallene i JSON-filene).
#
# Cache: Whisper-utdata fra tidligere kjøringer ligger i $ARKIVKLARERING_DATA/eval-data/*.jsonl og gjenbrukes som standard. Cachene følger
# segmenteringen (eval/dev/felles.cache_sti: <navn>_inavamos.jsonl, eller en eldre <navn>.jsonl uten suffiks, som er laget med inaVAMOS).
# --uten-cache setter ARKIVKLARERING_EVAL_DATA til en ny mappe med symlinker til rådataene (datasettene) men uten cachene, slik at
# alt Whisper-arbeid gjøres på nytt (timer). Ingenting i den ekte eval-data-mappen endres eller slettes.
#
# Vakter: miljo.sh avbryter hvis cacher og tmp peker utenfor ARKIVKLARERING_DATA. Før hvert steg kalles eval/dev/felles.vent_pa_ressurser() (minst 6 GB
# ledig minne, det andre sporets vakt ikke aktiv, minst 8 GiB ledig intern disk, swap høyst 6,5 GB), samme som i selve skriptene.
#
# EVAL-0004 (lisensen for NB Samtale) er ført for hånd og kjøres ikke; sha256 av fila skrives. EVAL-0009 (H4) kjøres bare med
# --med-h4 <prereg-id> og krever at preregistreringen er registrert og at opptak finnes; C-målingen (EVAL-0010, simulert degradering) har eget steg
# når de finnes i registeret (se STEG under).
#
# Segmentering: de committede DEV-resultatene og cachene er laget med inaVAMOS, mens standarden nå er inaSpeechSegmenter (KLAR-ADR-0019 v1.1).
# Alle steg kjøres derfor med ARKIVKLARERING_SEGMENTERING=inavamos (krever tillegget reproduksjon-h1h2), unntatt steg 9 (H4), som er
# preregistrert med inaSpeechSegmenter og kjøres med ARKIVKLARERING_SEGMENTERING=inaseg. Valget skrives i sha256.txt.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
TOR=0; BARE=""; UTEN_CACHE=1; GJENBRUK=1; H4=""; URENT=0
while [ $# -gt 0 ]; do
  case "$1" in
    --tor) TOR=1 ;;
    --bare) BARE="$2"; shift ;;
    --uten-cache) UTEN_CACHE=1 ;;
    --med-cache) UTEN_CACHE=0 ;;       # gjenbruk også rålagets gamle cache (gir da tall uten -nt)
    --uten-gjenbruk) GJENBRUK=0 ;;    # kjør også det normaliserte laget på nytt
    --med-h4) H4="$2"; shift ;;
    --tillat-urent) URENT=1 ;;
    -h|--help) sed -n '2,26p' "$0"; exit 0 ;;
    *) echo "ukjent argument: $1" >&2; exit 2 ;;
  esac
  shift
done

# 1. miljøet må være satt av miljo.sh: ARKIVKLARERING_DATA, og cacher og tmp under den
PY=".venv/bin/python"
DATA="${ARKIVKLARERING_DATA:-}"
if [ -z "$DATA" ] || ! "$PY" -c 'import sys; from arkivklarering import miljo; sys.exit(1 if miljo.sjekk() else 0)' 2>/dev/null; then
  echo "FEIL: kjør 'source scripts/miljo.sh' først (ARKIVKLARERING_DATA, og cacher og tmp under den)." >&2; exit 1
fi

# STEG: nr | beskrivelse | kommando (kjøres i worktreet) | EVAL-nøkler som lages
STEG=(
  "1|KLAR-EVAL-0001 oppdiktet tekst (Whisper på stillhet, støy og musikk)|scripts/mal_oppdiktet_tekst.py docs/KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v9.9_REPRO.md|KLAR-EVAL-0001"
  "2|KLAR-EVAL-0002 og 0003 WER og utvalg, NB Samtale validation|eval/dev/kjor_dev.py|KLAR-EVAL-0002 KLAR-EVAL-0003"
  "4|KLAR-EVAL-0004 lisens NB Samtale (ført for hånd, ikke kjørt)||KLAR-EVAL-0004"
  "5|KLAR-EVAL-0005 navnegjenkjenning NorNE validation|eval/dev/kjor_personvern_dev.py|KLAR-EVAL-0005"
  "6|KLAR-EVAL-0006 v1.0 flaggoverlevelse NB Samtale (fra cache av WER-kjøringen)|eval/dev/kjor_flaggoverlevelse_dev.py|KLAR-EVAL-0006"
  "61|KLAR-EVAL-0006 v1.1 flaggoverlevelse NB Samtale med ordtider|eval/dev/kjor_flaggoverlevelse_ord.py --datasett nbsamtale|KLAR-EVAL-0006"
  "7|KLAR-EVAL-0007 flaggoverlevelse NPSC validation|eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc|KLAR-EVAL-0007"
  "8|KLAR-EVAL-0008 syntetisk kjede (justeringsmanus, TTS)|eval/dev/kjor_syntetisk.py|KLAR-EVAL-0008"
  "9t|H4-skriptets tørrtest på justeringsmanuset (SYNTETISK, ingen H4-måling)|kalibrering/kjor_h4.py --torrtest|h4_torrtest"
)
if [ -n "$H4" ]; then
  STEG+=("9|KLAR-EVAL-0009 H4 på menneskeinnlest testmanus|kalibrering/kjor_h4.py --prereg-id $H4|KLAR-EVAL-0009")
fi
[ -f eval/dev/kjor_degradering.py ] && STEG+=("10a|degradert lyd for EVAL-0010 (audiomentations, eget venv; deterministisk)|DEGPY eval/dev/degrader_lyd.py|degradert" "10|KLAR-EVAL-0010 simulert degradering (DEV)|eval/dev/kjor_degradering.py|KLAR-EVAL-0010")

VELG() { [ -z "$BARE" ] && return 0; case ",$BARE," in *",$1,"*) return 0 ;; esac; return 1; }  # --bare tar stegnumrene (1,2,4,5,6,61,7,8,9t,10a,10)

if [ "$URENT" -eq 0 ] && [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  echo "FEIL: arbeidstreet har ucommittede endringer; worktreet inneholder bare HEAD. Commit først, eller bruk --tillat-urent." >&2
  exit 1
fi

TID="$(date +%Y%m%d-%H%M%S)"
UT="$DATA/reproduksjon/$TID"
echo "== reproduser: HEAD $(git rev-parse --short HEAD), ut: $UT"
for s in "${STEG[@]}"; do IFS='|' read -r nr besk kmd nok <<<"$s"; VELG "$nr" && echo "   steg $nr: $besk"; done
[ "$TOR" -eq 1 ] && { echo "(--tor: ingenting kjørt)"; exit 0; }

mkdir -p "$UT/resultater"
git worktree add --detach "$UT/tre" HEAD >/dev/null 2>&1
ln -s "$REPO/modeller" "$UT/tre/modeller"
[ -e "$REPO/vokabular" ] && [ ! -e "$UT/tre/vokabular" ] && ln -s "$REPO/vokabular" "$UT/tre/vokabular" || true
if [ "$UTEN_CACHE" -eq 1 ]; then
  ED="$UT/eval-data"; mkdir -p "$ED"
  for e in "${ARKIVKLARERING_EVAL_DATA:-$DATA/eval-data}"/*; do
    case "$e" in *.jsonl) continue ;; esac
    ln -s "$e" "$ED/$(basename "$e")"
  done
  export ARKIVKLARERING_EVAL_DATA="$ED"   # arkivklarering/miljo.py: EVAL_DATA for alle steg
  echo "   --uten-cache: cache i $ED (rådata lenket inn, ingen .jsonl-cache)"
fi

SHA="$UT/sha256.txt"; : > "$SHA"
echo "# reproduser.sh $TID, HEAD $(git rev-parse HEAD)$([ "$UTEN_CACHE" -eq 1 ] && echo ', uten cache')" >> "$SHA"
echo "# sha256 | resultatfil | sha256 av committet fil med samme EVAL-nøkkel (til informasjon) " >> "$SHA"
FEIL=0
echo "   segmentering: ARKIVKLARERING_SEGMENTERING=inavamos for alle steg (lagrede resultater er laget med inaVAMOS), inaseg for steg 9 (H4)" | tee -a "$SHA"
if [ "$GJENBRUK" -eq 1 ]; then
  export ARKIVKLARERING_GJENBRUK_NORMALISERT=1 ARKIVKLARERING_GJENBRUK_MAPPE="$DATA/eval-data"
  echo "   gjenbruk av lagrede utdata for det normaliserte laget er PÅ (modell-sha256 låst, parametere uendret, uten -nt); rålaget kjøres på nytt med -nt" | tee -a "$SHA"
else
  unset ARKIVKLARERING_GJENBRUK_NORMALISERT
fi
if [ "$UTEN_CACHE" -eq 0 ]; then echo "   ADVARSEL: --med-cache gjenbruker også rålagets gamle cacher (uten -nt)" | tee -a "$SHA"; fi
cd "$UT/tre"
for s in "${STEG[@]}"; do
  IFS='|' read -r nr besk kmd nok <<<"$s"
  VELG "$nr" || continue
  echo "== steg $nr: $besk"
  if [ -n "$kmd" ]; then
    PYTHONPATH="$UT/tre" "$REPO/$PY" -c "import sys; sys.path.insert(0,'eval/dev'); import felles; felles.vent_pa_ressurser()"
    before="$(find docs eval kalibrering -type f \( -name '*.json' -o -name '*.md' \) -print0 | xargs -0 shasum -a 256 | sort)"
    interp="$REPO/$PY"
    case "$kmd" in DEGPY\ *) interp="$DATA/venv-degradering/bin/python"; kmd="${kmd#DEGPY }" ;; esac
    SEG=inavamos; [ "$nr" = 9 ] && SEG=inaseg   # se «Segmentering» øverst
    # shellcheck disable=SC2086
    if ! ARKIVKLARERING_SEGMENTERING="$SEG" PYTHONPATH="$UT/tre" "$interp" $kmd; then echo "   FEIL i steg $nr (fortsetter)" >&2; FEIL=1; fi
    after="$(find docs eval kalibrering -type f \( -name '*.json' -o -name '*.md' \) -print0 | xargs -0 shasum -a 256 | sort)"
    ny="$(comm -13 <(echo "$before") <(echo "$after") | awk '{print $2}')"
  else
    ny="$(ls eval/dev/KLAR-EVAL-0004_* 2>/dev/null || true)"
  fi
  for f in $ny; do
    mkdir -p "$UT/resultater/$(dirname "$f")"; cp "$f" "$UT/resultater/$f"
    h="$(shasum -a 256 "$f" | cut -d' ' -f1)"
    key="$(basename "$f" | grep -o '^KLAR-[A-Z]*-[0-9]*' || true)"
    c=""; if [ -n "$key" ]; then c="$(git -C "$REPO" ls-files "docs/${key}_*" "eval/dev/${key}_*" | grep "$(basename "$f" | sed 's/.*\.//')\$" | tail -1)"; fi
    ch=""; [ -n "$c" ] && ch="$(shasum -a 256 "$REPO/$c" | cut -d' ' -f1) ($c)"
    echo "$h  $f  | $ch" | tee -a "$SHA"
  done
done
cd "$REPO"
echo "== ferdig. Resultater: $UT/resultater  sha256: $SHA  (fjern worktreet med: git worktree remove --force '$UT/tre')"
exit "$FEIL"
