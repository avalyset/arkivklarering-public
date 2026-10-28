"""Datarot og miljøvakt: alt tungt (evalueringsdata, lyd, modeller, venv for segmentering og talerinndeling, cacher, tmp) ligger under
én rot, ARKIVKLARERING_DATA.

Roten (`DATA`) er miljøvariabelen ARKIVKLARERING_DATA. Mangler den, er standarden `/Volumes/Vault/arkivklarering` når Vault er montert og
mappen finnes (Eiriks oppsett, uendret), ellers `$XDG_DATA_HOME/arkivklarering` (`~/.local/share/arkivklarering` når XDG_DATA_HOME mangler).
`EVAL_DATA` er `DATA/eval-data` (evalueringsdata og cacher); miljøvariabelen ARKIVKLARERING_EVAL_DATA overstyrer bare den (brukes av
`scripts/reproduser.sh --uten-cache`).

`krev_miljo()` (alias `krev_vault_miljo()`, navnet fra før) kalles først i alle Python-skript og i `tests/conftest.py`. Den
  1. setter HF_HOME, HF_DATASETS_CACHE, XDG_CACHE_HOME, PIP_CACHE_DIR, TORCH_HOME og KERAS_HOME til standardstier under roten når de mangler,
     og TMPDIR til `DATA/tmp` når den mangler eller er systemets standard (macOS' /var/folders/…/T, /tmp, /var/tmp);
  2. avbryter (exit 3) hvis roten ikke finnes (en satt ARKIVKLARERING_DATA opprettes ikke; standardroten under ~/.local/share opprettes),
     hvis roten ligger under et umontert /Volumes/<disk>, eller hvis HF_HOME, HF_DATASETS_CACHE, TMPDIR eller XDG_CACHE_HOME peker utenfor
     roten (etter oppløsing av symlinker).
Shell-skript kilder `scripts/miljo.sh`, som setter de samme variablene ut fra ARKIVKLARERING_DATA og gjør samme kontroll.
"""
from __future__ import annotations

import os
import pathlib
import sys
import tempfile

VAULT = pathlib.Path("/Volumes/Vault")
VAULT_DATA = VAULT / "arkivklarering"
MILJOVARIABEL = "ARKIVKLARERING_DATA"
EVAL_MILJOVARIABEL = "ARKIVKLARERING_EVAL_DATA"
KREVDE = ("HF_HOME", "HF_DATASETS_CACHE", "TMPDIR", "XDG_CACHE_HOME")
_UNDER_ROTEN = {  # standardstier relativt til roten (samme som scripts/miljo.sh)
    "HF_HOME": "cache/hf",
    "HF_DATASETS_CACHE": "cache/hf/datasets",
    "XDG_CACHE_HOME": "cache",
    "TMPDIR": "tmp",
    "PIP_CACHE_DIR": "cache/pip",
    "TORCH_HOME": "cache/torch",
    "KERAS_HOME": "cache/keras",
}


def standard_data(env=None) -> pathlib.Path:
    """Standardroten når ARKIVKLARERING_DATA mangler: Vault hvis montert og `arkivklarering/` finnes der, ellers XDG_DATA_HOME/arkivklarering."""
    env = os.environ if env is None else env
    if os.path.ismount(VAULT) and VAULT_DATA.is_dir():
        return VAULT_DATA
    xdg = env.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")
    return pathlib.Path(xdg) / "arkivklarering"


def data_rot(env=None) -> pathlib.Path:
    """Roten for tunge data: ARKIVKLARERING_DATA, ellers `standard_data()`."""
    env = os.environ if env is None else env
    verdi = env.get(MILJOVARIABEL, "").strip()
    return pathlib.Path(verdi).expanduser() if verdi else standard_data(env)


DATA = data_rot()
EVAL_DATA = pathlib.Path(os.environ.get(EVAL_MILJOVARIABEL, "").strip() or DATA / "eval-data")


def standardmiljo(rot=None) -> dict:
    """Miljøvariablene for cacher og tmp under roten (det `scripts/miljo.sh` setter)."""
    rot = pathlib.Path(rot or DATA)
    return {v: str(rot / rel) for v, rel in _UNDER_ROTEN.items()}


def er_systemets_tmp(verdi: str) -> bool:
    """Sann når TMPDIR er operativsystemets standard (ikke valgt for arkivklarering): /tmp, /var/tmp eller macOS' /var/folders/…/T
    (`getconf DARWIN_USER_TEMP_DIR`)."""
    ekte = os.path.realpath(verdi)
    if ekte in {os.path.realpath("/tmp"), os.path.realpath("/var/tmp")}:
        return True
    deler = pathlib.PurePath(ekte).parts  # macOS: /private/var/folders/<xx>/<id>/T
    return len(deler) == 7 and deler[1:4] == ("private", "var", "folders") and deler[6] == "T"


def _under(sti: str, rot_ekte: str) -> bool:
    ekte = os.path.realpath(sti)
    return ekte == rot_ekte or ekte.startswith(rot_ekte + os.sep)


def sjekk(env=None, rot=None, krev_montert: bool = False) -> list[str]:
    """Returnerer en liste med feil (tom = OK). `krev_montert`: roten selv må være et monteringspunkt."""
    env = os.environ if env is None else env
    rot = pathlib.Path(rot) if rot is not None else data_rot(env)
    feil = []
    if not rot.is_dir():
        feil.append(f"datarot {rot} finnes ikke ({MILJOVARIABEL}; opprett mappen eller sett {MILJOVARIABEL})")
    deler = rot.parts
    if len(deler) >= 3 and deler[1] == "Volumes" and not os.path.ismount(os.path.join(os.sep, deler[1], deler[2])):
        feil.append(f"/Volumes/{deler[2]} er ikke montert (datarot {rot})")
    if krev_montert and not os.path.ismount(rot):
        feil.append(f"{rot} er ikke montert")
    rot_ekte = os.path.realpath(rot)
    for v in KREVDE:
        verdi = env.get(v, "")
        if not verdi:
            feil.append(f"{v} er ikke satt (kjør `source scripts/miljo.sh` eller kall krev_miljo())")
            continue
        if not _under(verdi, rot_ekte):
            ekte = os.path.realpath(verdi)
            feil.append(f"{v} peker utenfor {rot}: {verdi}" + (f" (-> {ekte})" if ekte != verdi.rstrip(os.sep) else ""))
    return feil


def sett_standardmiljo(env=None, rot=None) -> list[str]:
    """Setter manglende variabler (og TMPDIR når den er systemets standard) til stier under roten og oppretter mappene. Variabler som
    allerede er satt til noe annet, endres ikke (sjekk() avviser dem hvis de peker utenfor roten). Returnerer navnene som ble satt."""
    env = os.environ if env is None else env
    rot = pathlib.Path(rot) if rot is not None else data_rot(env)
    satt = []
    for v, sti in standardmiljo(rot).items():
        verdi = env.get(v, "")
        if not verdi or (v == "TMPDIR" and er_systemets_tmp(verdi) and not _under(verdi, os.path.realpath(rot))):
            env[v] = sti
            satt.append(v)
        if rot.is_dir() and _under(env[v], os.path.realpath(rot)):
            os.makedirs(env[v], exist_ok=True)
    if "TMPDIR" in satt and env is os.environ:
        tempfile.tempdir = None  # tempfile leser TMPDIR på nytt
    return satt


def krev_miljo(env=None, rot=None, krev_montert: bool = False, sett_standard: bool = True) -> pathlib.Path:
    """Sørger for at tunge data og cacher ligger under roten (se modulteksten); avbryter med exit 3 ellers. Returnerer roten."""
    env = os.environ if env is None else env
    eksplisitt = rot is not None or bool(env.get(MILJOVARIABEL, "").strip())
    rot = pathlib.Path(rot) if rot is not None else data_rot(env)
    if not eksplisitt and not rot.exists() and rot != VAULT_DATA:
        os.makedirs(rot, exist_ok=True)  # standardroten under XDG_DATA_HOME opprettes; en satt ARKIVKLARERING_DATA gjør det ikke
    if sett_standard:
        sett_standardmiljo(env, rot)
    feil = sjekk(env, rot, krev_montert)
    if feil:
        print(f"STOPP: tunge data og cacher ligger ikke under datarot {rot} ({MILJOVARIABEL}).", file=sys.stderr)
        for f in feil:
            print(f"  - {f}", file=sys.stderr)
        raise SystemExit(3)
    return rot


krev_vault_miljo = krev_miljo  # gammelt navn; alle skript kaller det fortsatt
