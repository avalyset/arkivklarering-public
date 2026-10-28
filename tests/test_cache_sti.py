"""Cachene med `tidslinje` følger segmenteringen (felles.cache_sti): tidslinjer fra inaSpeechSegmenter og inaVAMOS blandes aldri.
Eldre cacher uten suffiks er laget med inaVAMOS og brukes bare med inavamos."""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "eval" / "dev"))
import felles  # noqa: E402

from arkivklarering import segment, transkriber  # noqa: E402


def _seg(monkeypatch, verdi):
    if verdi is None:
        monkeypatch.delenv(segment.MILJOVARIABEL, raising=False)
    else:
        monkeypatch.setenv(segment.MILJOVARIABEL, verdi)


def _skriv(sti, id_="a", label="speech"):
    sti.write_text(json.dumps({"id": id_, "tidslinje": [{"label": label}], "cues": {"normalisert": [{"tekst": str(sti.name)}]}}) + "\n")


@pytest.mark.parametrize("verdi,navn", [(None, "ord_npsc_test_inaseg.jsonl"), ("", "ord_npsc_test_inaseg.jsonl"), ("inaseg", "ord_npsc_test_inaseg.jsonl"),
                                        ("inavamos", "ord_npsc_test_inavamos.jsonl")])
def test_navnet_far_suffiks_etter_segmenteringen(monkeypatch, tmp_path, verdi, navn):
    _seg(monkeypatch, verdi)
    assert felles.cache_sti(tmp_path, "ord_npsc_test") == tmp_path / navn  # ingen filer: ny cache med suffiks


def test_eldre_fil_uten_suffiks_brukes_bare_med_inavamos(monkeypatch, tmp_path):
    _skriv(tmp_path / "ord_npsc_test.jsonl")  # eldre cache, laget med inaVAMOS
    _seg(monkeypatch, "inavamos")
    assert felles.cache_sti(tmp_path, "ord_npsc_test") == tmp_path / "ord_npsc_test.jsonl"
    _seg(monkeypatch, "inaseg")
    assert felles.cache_sti(tmp_path, "ord_npsc_test") == tmp_path / "ord_npsc_test_inaseg.jsonl"
    _seg(monkeypatch, None)
    assert felles.cache_sti(tmp_path, "ord_npsc_test") == tmp_path / "ord_npsc_test_inaseg.jsonl"


def test_inavamos_foretrekker_fil_med_suffiks(monkeypatch, tmp_path):
    _skriv(tmp_path / "deg_original.jsonl")
    _skriv(tmp_path / "deg_original_inavamos.jsonl")
    _seg(monkeypatch, "inavamos")
    assert felles.cache_sti(tmp_path, "deg_original") == tmp_path / "deg_original_inavamos.jsonl"


def test_eksplisitt_segmentering_overstyrer_miljoet(monkeypatch, tmp_path):
    _skriv(tmp_path / "ord_nbsamtale_validation.jsonl")
    _seg(monkeypatch, "inaseg")
    assert felles.cache_sti(tmp_path, "ord_nbsamtale_validation", segmentering="inavamos") == tmp_path / "ord_nbsamtale_validation.jsonl"
    with pytest.raises(segment.SegmenteringFeil):
        felles.cache_sti(tmp_path, "x", segmentering="whisper")


@pytest.mark.parametrize("navn", ["ord_npsc_test", "deg_degradert", "ord_syntetisk_matchet", "h4_torrtest_matchet", "h4_testmanus_nn"])
def test_inaseg_kjoring_leser_aldri_en_inavamos_cache(monkeypatch, tmp_path, navn):
    for fil in (f"{navn}.jsonl", f"{navn}_inavamos.jsonl"):
        _skriv(tmp_path / fil, label="speech+music")  # bare inaVAMOS har speech+music
    _seg(monkeypatch, "inaseg")
    sti = felles.cache_sti(tmp_path, navn)
    assert sti.name == f"{navn}_inaseg.jsonl" and felles.les_jsonl(sti) == {}
    felles.legg_til_jsonl(sti, {"id": "b", "tidslinje": [{"label": "speech"}]})
    assert (tmp_path / f"{navn}.jsonl").read_text().count("\n") == 1  # inaVAMOS-cachene er urørt
    assert set(felles.les_jsonl(felles.cache_sti(tmp_path, navn))) == {"b"}


def test_grunnnavn_er_motsatt_av_cache_sti():
    for fil in ("ord_npsc_test.jsonl", "ord_npsc_test_inaseg.jsonl", "ord_npsc_test_inavamos.jsonl"):
        assert felles.grunnnavn(pathlib.Path("/x") / fil) == "ord_npsc_test"


def _oppsett_norm():
    return transkriber.Oppsett("normalisert", "wcli", "/m.bin", "abc", "nn", False)


def test_gjenbruk_folger_samme_regel(monkeypatch, tmp_path):
    gammel = tmp_path / "gammel"
    gammel.mkdir()
    _skriv(gammel / "ord_npsc_test.jsonl", id_="vamos")  # eldre, inaVAMOS
    monkeypatch.setenv("ARKIVKLARERING_GJENBRUK_NORMALISERT", "1")
    monkeypatch.setenv("ARKIVKLARERING_GJENBRUK_MAPPE", str(gammel))
    logg = []
    _seg(monkeypatch, "inaseg")
    assert felles.gjenbruk_normalisert(felles.cache_sti(tmp_path, "ord_npsc_test"), _oppsett_norm(), logg.append) is None  # aldri inaVAMOS-cuer
    assert "ord_npsc_test_inaseg.jsonl" in logg[-1]
    _skriv(gammel / "ord_npsc_test_inaseg.jsonl", id_="inaseg")
    assert set(felles.gjenbruk_normalisert(felles.cache_sti(tmp_path, "ord_npsc_test"), _oppsett_norm(), logg.append)) == {"inaseg"}
    _seg(monkeypatch, "inavamos")
    assert set(felles.gjenbruk_normalisert(felles.cache_sti(tmp_path, "ord_npsc_test"), _oppsett_norm(), logg.append)) == {"vamos"}


def test_cache_suffiks_miljovariabelen_er_fjernet():
    rot = pathlib.Path(__file__).resolve().parent.parent
    for f in [*rot.glob("eval/**/*.py"), *rot.glob("kalibrering/*.py"), *rot.glob("arkivklarering/*.py"), *rot.glob("scripts/*")]:
        if f.is_file():
            assert "ARKIVKLARERING_CACHE_SUFFIKS" not in f.read_text(encoding="utf-8", errors="replace"), f
