#!/usr/bin/env bash
# Kildes før hver kjøring: source scripts/miljo.sh
# Alt tungt (evalueringsdata, lyd, modeller, venv for segmentering/talerinndeling, cacher, tmp) ligger under én datarot,
# ARKIVKLARERING_DATA (arkivklarering/miljo.py har samme regel). Er den ikke satt, er standarden /Volumes/Vault/arkivklarering når
# Vault er montert og mappen finnes, ellers ${XDG_DATA_HOME:-~/.local/share}/arkivklarering (opprettes). En satt ARKIVKLARERING_DATA
# som ikke finnes, eller som ligger under et umontert /Volumes/<disk>, gir STOPP (exit 3); den opprettes ikke.
# Cacher og tmp (HF_HOME, HF_DATASETS_CACHE, PIP_CACHE_DIR, TORCH_HOME, KERAS_HOME, XDG_CACHE_HOME, TMPDIR) settes under roten.
_vault_data=/Volumes/Vault/arkivklarering
if [ -z "${ARKIVKLARERING_DATA:-}" ]; then
  if mount | grep -q " on /Volumes/Vault " && [ -d "$_vault_data" ]; then
    ARKIVKLARERING_DATA="$_vault_data"
  else
    ARKIVKLARERING_DATA="${XDG_DATA_HOME:-$HOME/.local/share}/arkivklarering"
    mkdir -p "$ARKIVKLARERING_DATA"
    echo "MERK: /Volumes/Vault er ikke montert; ARKIVKLARERING_DATA=$ARKIVKLARERING_DATA (sett ARKIVKLARERING_DATA for å velge en annen rot)." >&2
  fi
fi
if [ ! -d "$ARKIVKLARERING_DATA" ]; then
  echo "STOPP: ARKIVKLARERING_DATA=$ARKIVKLARERING_DATA finnes ikke (opprettes ikke her)." >&2
  unset _vault_data
  return 3 2>/dev/null || exit 3
fi
case "$ARKIVKLARERING_DATA" in
  /Volumes/*/*|/Volumes/*)
    _disk="/Volumes/$(echo "${ARKIVKLARERING_DATA#/Volumes/}" | cut -d/ -f1)"
    if ! mount | grep -q " on $_disk "; then
      echo "STOPP: $_disk er ikke montert (ARKIVKLARERING_DATA=$ARKIVKLARERING_DATA)." >&2
      unset _vault_data _disk
      return 3 2>/dev/null || exit 3
    fi ;;
esac
export ARKIVKLARERING_DATA
export HF_HOME="$ARKIVKLARERING_DATA/cache/hf"
export HF_DATASETS_CACHE="$ARKIVKLARERING_DATA/cache/hf/datasets"
export PIP_CACHE_DIR="$ARKIVKLARERING_DATA/cache/pip"
export TORCH_HOME="$ARKIVKLARERING_DATA/cache/torch"
export KERAS_HOME="$ARKIVKLARERING_DATA/cache/keras"
export XDG_CACHE_HOME="$ARKIVKLARERING_DATA/cache"   # uv bruker $XDG_CACHE_HOME/uv
export TMPDIR="$ARKIVKLARERING_DATA/tmp"
mkdir -p "$HF_HOME" "$HF_DATASETS_CACHE" "$PIP_CACHE_DIR" "$TORCH_HOME" "$KERAS_HOME" "$XDG_CACHE_HOME/spacy" "$XDG_CACHE_HOME/uv" "$TMPDIR"

# Vakt: alle fire variablene må peke inn i datarota (etter oppløsing av symlinker), ellers avbryter vi.
_rot="$(cd -P "$ARKIVKLARERING_DATA" 2>/dev/null && pwd -P)"
for _v in HF_HOME HF_DATASETS_CACHE TMPDIR XDG_CACHE_HOME; do
  eval "_val=\${$_v:-}"
  _ekte="$(cd -P "$_val" 2>/dev/null && pwd -P)"
  case "$_ekte" in
    "$_rot"|"$_rot"/*) ;;
    *) echo "STOPP: $_v peker utenfor ARKIVKLARERING_DATA=$ARKIVKLARERING_DATA ($_val)." >&2
       unset _v _val _ekte _rot _vault_data _disk
       return 3 2>/dev/null || exit 3 ;;
  esac
done
unset _v _val _ekte _rot _vault_data _disk
