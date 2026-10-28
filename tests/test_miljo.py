import os
import pathlib
import subprocess
import sys

import pytest

from arkivklarering import miljo

REPO = pathlib.Path(__file__).resolve().parent.parent


def _env(rot, **avvik):
    e = {v: str(rot / v.lower()) for v in miljo.KREVDE}
    for v in miljo.KREVDE:
        os.makedirs(e[v], exist_ok=True)
    e.update(avvik)
    return e


def test_ok_naar_alt_ligger_under_roten(tmp_path):
    assert miljo.sjekk(_env(tmp_path), tmp_path, krev_montert=False) == []


@pytest.mark.parametrize("variabel", miljo.KREVDE)
def test_avbryter_naar_en_variabel_peker_utenfor(tmp_path, variabel):
    vault = tmp_path / "vault"
    vault.mkdir()
    utenfor = tmp_path / "intern"
    utenfor.mkdir()
    e = _env(vault, **{variabel: str(utenfor)})
    feil = miljo.sjekk(e, vault, krev_montert=False)
    assert len(feil) == 1 and variabel in feil[0]
    with pytest.raises(SystemExit) as ut:
        miljo.krev_vault_miljo(e, vault, krev_montert=False)  # gammelt navn = krev_miljo
    assert ut.value.code == 3


@pytest.mark.parametrize("variabel", miljo.KREVDE)
def test_avbryter_naar_variabel_mangler(tmp_path, variabel):
    e = _env(tmp_path)
    del e[variabel]
    assert any(variabel in f and "ikke satt" in f for f in miljo.sjekk(e, tmp_path, krev_montert=False))


def test_symlink_ut_av_vault_avvises(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    intern = tmp_path / "intern"
    intern.mkdir()
    (vault / "hf").symlink_to(intern)
    e = _env(vault, HF_HOME=str(vault / "hf"))
    feil = miljo.sjekk(e, vault, krev_montert=False)
    assert any("HF_HOME" in f and "utenfor" in f for f in feil)


def test_prefiks_som_ligner_er_ikke_inni_roten(tmp_path):
    vault = tmp_path / "Vault"
    vault.mkdir()
    lignende = tmp_path / "VaultKopi"
    lignende.mkdir()
    e = _env(vault, TMPDIR=str(lignende))
    assert any("TMPDIR" in f for f in miljo.sjekk(e, vault, krev_montert=False))


def test_umontert_rot_avvises(tmp_path):
    assert any("ikke montert" in f for f in miljo.sjekk(_env(tmp_path), tmp_path, krev_montert=True))


# ------------------------------------------------------------ ARKIVKLARERING_DATA
def test_datarot_fra_miljovariabelen(tmp_path):
    assert miljo.data_rot({"ARKIVKLARERING_DATA": str(tmp_path)}) == tmp_path


def test_standard_er_vault_naar_montert_ellers_xdg(tmp_path, monkeypatch):
    monkeypatch.setattr(miljo, "VAULT", tmp_path / "ikke_montert")
    monkeypatch.setattr(miljo, "VAULT_DATA", tmp_path / "ikke_montert" / "arkivklarering")
    assert miljo.data_rot({"XDG_DATA_HOME": str(tmp_path)}) == tmp_path / "arkivklarering"
    assert miljo.data_rot({}) == pathlib.Path(os.path.expanduser("~")) / ".local" / "share" / "arkivklarering"
    vault_data = tmp_path / "Vault" / "arkivklarering"
    vault_data.mkdir(parents=True)
    monkeypatch.setattr(miljo, "VAULT", pathlib.Path("/"))  # et monteringspunkt som alltid finnes
    monkeypatch.setattr(miljo, "VAULT_DATA", vault_data)
    assert miljo.data_rot({"XDG_DATA_HOME": str(tmp_path)}) == vault_data  # Eiriks oppsett uendret


def test_krev_miljo_setter_manglende_variabler_under_roten(tmp_path):
    rot = tmp_path / "data"
    rot.mkdir()
    env = {"ARKIVKLARERING_DATA": str(rot)}
    assert miljo.krev_miljo(env) == rot
    for v, rel in (("HF_HOME", "cache/hf"), ("HF_DATASETS_CACHE", "cache/hf/datasets"), ("XDG_CACHE_HOME", "cache"), ("TMPDIR", "tmp"),
                   ("TORCH_HOME", "cache/torch"), ("KERAS_HOME", "cache/keras"), ("PIP_CACHE_DIR", "cache/pip")):
        assert env[v] == str(rot / rel) and (rot / rel).is_dir()


def test_systemets_tmpdir_byttes_ut_men_ikke_en_valgt(tmp_path):
    rot = tmp_path / "data"
    rot.mkdir()
    env = {"ARKIVKLARERING_DATA": str(rot), "TMPDIR": "/tmp"}
    miljo.krev_miljo(env)
    assert env["TMPDIR"] == str(rot / "tmp")
    if sys.platform == "darwin":
        assert miljo.er_systemets_tmp(subprocess.run(["getconf", "DARWIN_USER_TEMP_DIR"], capture_output=True, text=True).stdout.strip())
    valgt = tmp_path / "egen_tmp"
    valgt.mkdir()
    env = {"ARKIVKLARERING_DATA": str(rot), "TMPDIR": str(valgt)}
    with pytest.raises(SystemExit):
        miljo.krev_miljo(env)  # valgt utenfor roten: STOPP, ikke stille overstyring
    assert env["TMPDIR"] == str(valgt)


def test_satt_datarot_som_ikke_finnes_opprettes_ikke(tmp_path):
    env = {"ARKIVKLARERING_DATA": str(tmp_path / "finnes_ikke")}
    with pytest.raises(SystemExit) as ut:
        miljo.krev_miljo(env)
    assert ut.value.code == 3 and not (tmp_path / "finnes_ikke").exists()


def test_rot_under_umontert_volum_avvises(tmp_path):
    feil = miljo.sjekk(_env(tmp_path), pathlib.Path("/Volumes/FinnesIkke_arkivklarering/data"))
    assert any("/Volumes/FinnesIkke_arkivklarering er ikke montert" in f for f in feil)


def test_standardroten_opprettes_naar_variabelen_mangler(tmp_path, monkeypatch):
    monkeypatch.setattr(miljo, "VAULT", tmp_path / "ikke_montert")
    env = {"XDG_DATA_HOME": str(tmp_path / "xdg")}
    assert miljo.krev_miljo(env) == tmp_path / "xdg" / "arkivklarering"
    assert (tmp_path / "xdg" / "arkivklarering" / "tmp").is_dir()


def _miljo_sh(env, *ekstra):
    kmd = f'source "{REPO / "scripts" / "miljo.sh"}" && echo "DATA=$ARKIVKLARERING_DATA" && echo "HF=$HF_HOME" && echo "TMP=$TMPDIR" && echo "XDG=$XDG_CACHE_HOME"'
    return subprocess.run(["bash", "-c", kmd], capture_output=True, text=True, env={"PATH": os.environ["PATH"], **env})


def test_miljo_sh_utleder_alt_fra_datarota(tmp_path):
    rot = tmp_path / "data"
    rot.mkdir()
    p = _miljo_sh({"ARKIVKLARERING_DATA": str(rot), "HOME": str(tmp_path), "HF_HOME": "/annet/sted"})
    assert p.returncode == 0, p.stderr
    assert p.stdout.splitlines() == [f"DATA={rot}", f"HF={rot}/cache/hf", f"TMP={rot}/tmp", f"XDG={rot}/cache"]
    assert (rot / "cache" / "hf" / "datasets").is_dir() and (rot / "cache" / "keras").is_dir()


def test_miljo_sh_stopper_naar_satt_datarot_mangler(tmp_path):
    p = _miljo_sh({"ARKIVKLARERING_DATA": str(tmp_path / "borte"), "HOME": str(tmp_path)})
    assert p.returncode == 3 and "finnes ikke" in p.stderr and not (tmp_path / "borte").exists()
