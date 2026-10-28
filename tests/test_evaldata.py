import pytest

from arkivklarering import evaldata


def test_train_og_validation_er_fri(tmp_path):
    assert evaldata.sjekk_splitt("validation", docs=tmp_path) == "validation"
    assert evaldata.sjekk_splitt("train", docs=tmp_path) == "train"


def test_test_uten_prereg_id_sperres(tmp_path):
    with pytest.raises(evaldata.TestdelSperret):
        evaldata.sjekk_splitt("test", docs=tmp_path)
    with pytest.raises(evaldata.TestdelSperret):
        evaldata.sjekk_splitt("test", "bare-noe", docs=tmp_path)


def test_test_med_id_uten_fil_sperres(tmp_path):
    with pytest.raises(evaldata.TestdelSperret):
        evaldata.sjekk_splitt("test", "KLAR-PREREG-0001", docs=tmp_path)


def test_test_med_id_og_fil_slippes_gjennom(tmp_path):
    (tmp_path / "KLAR-PREREG-0001_arkivklarering_testdeler_v1.0_2026-11-01.md").write_text("Status: registrert https://osf.io/abcde/\n")
    assert evaldata.sjekk_splitt("test", "KLAR-PREREG-0001", docs=tmp_path) == "test"


def test_stiene_gar_gjennom_sperren(tmp_path):
    with pytest.raises(evaldata.TestdelSperret):
        evaldata.metadata_sti(tmp_path, "test")
    with pytest.raises(evaldata.TestdelSperret):
        evaldata.tar_sti(tmp_path, "test", "bm")
    assert evaldata.metadata_sti(tmp_path, "validation").name == "validation_metadata.jsonl"


def test_ukjent_splitt():
    with pytest.raises(ValueError):
        evaldata.sjekk_splitt("dev")


def test_norne_test_er_sperret(tmp_path):
    with pytest.raises(evaldata.TestdelSperret):
        evaldata.norne_sti(tmp_path, "bokmaal", "test")
    assert evaldata.norne_sti(tmp_path, "nynorsk", "validation").name == "validation-00000-of-00001.parquet"
    with pytest.raises(ValueError):
        evaldata.norne_sti(tmp_path, "annet", "validation")


def test_npsc_test_er_sperret_og_validation_ligger_i_eval(tmp_path):
    with pytest.raises(evaldata.TestdelSperret):
        evaldata.npsc_mappe(tmp_path, "test")
    assert evaldata.npsc_mappe(tmp_path, "validation").name == "eval"


def test_utkast_apner_ikke_testdelen(tmp_path, monkeypatch):
    monkeypatch.setattr(evaldata, "DOCS", tmp_path)  # testen leser ikke repoets ekte PREREG (som er registrert)
    f = tmp_path / "KLAR-PREREG-0001_arkivklarering_testdeler_v1.0_2026-11-01.md"
    f.write_text("Status: UTKAST (ikke sendt inn)\n")
    with pytest.raises(evaldata.TestdelSperret):
        evaldata.sjekk_splitt("test", "KLAR-PREREG-0001", docs=tmp_path)
    with pytest.raises(evaldata.TestdelSperret):
        evaldata.metadata_sti(tmp_path, "test", "KLAR-PREREG-0001")
    f.write_text("tekst\nStatus: registrert https://osf.io/abcde/\n")
    assert evaldata.sjekk_splitt("test", "KLAR-PREREG-0001", docs=tmp_path) == "test"


def test_versjonssortering_ikke_leksikografisk(tmp_path):
    """v1.10 er nyere enn v1.9 (leksikografisk sorteres `v1.10` før `v1.9`); den nyeste fila avgjør statuslinjen."""
    eldre = tmp_path / "KLAR-PREREG-0001_arkivklarering_testdeler_v1.9_2026-11-01.md"
    nyere = tmp_path / "KLAR-PREREG-0001_arkivklarering_testdeler_v1.10_2026-11-02.md"
    eldre.write_text("Status: UTKAST\n")
    nyere.write_text("Status: registrert https://osf.io/abcde/\n")
    assert evaldata.siste_versjon([eldre, nyere]) == nyere
    assert evaldata.siste_versjon([nyere, eldre]) == nyere
    assert evaldata.sjekk_splitt("test", "KLAR-PREREG-0001", docs=tmp_path) == "test"
    eldre.write_text("Status: registrert https://osf.io/abcde/\n")
    nyere.write_text("Status: UTKAST\n")
    with pytest.raises(evaldata.TestdelSperret):
        evaldata.sjekk_splitt("test", "KLAR-PREREG-0001", docs=tmp_path)
