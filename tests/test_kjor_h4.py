import glob
import importlib.util
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent


def _last():
    spec = importlib.util.spec_from_file_location("kjor_h4", REPO / "kalibrering" / "kjor_h4.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


h4 = _last()


def test_terskler_leses_fra_preregistreringen():
    from arkivklarering import evaldata
    prereg = evaldata.siste_versjon(glob.glob(str(REPO / "docs" / "KLAR-PREREG-0001_*.md")))
    t = h4.les_terskler(prereg)
    assert set(t) == set(h4.KATEGORIER)
    assert t["person"] == ("≥", 0.60) and t["fødselsnummer"] == ("≥", 0.50) and t["e-post"] == ("≤", 0.10) and t["helse"] == ("≥", 0.75)


def test_vurdering_punktestimat_og_klart():
    assert h4.vurder("≥", 0.60, 9, 12)[0] == "bestått"
    assert h4.vurder("≥", 0.60, 5, 12) == ("ikke bestått", False)
    assert h4.vurder("≥", 0.60, 120, 150) == ("bestått", True)  # 0,80; nedre grense over 0,60
    assert h4.vurder("≤", 0.10, 0, 12)[0] == "bestått" and h4.vurder("≤", 0.10, 6, 12)[0] == "ikke bestått"
    assert h4.vurder("≥", 0.5, 0, 0) == ("ingen data", False)


def test_wilson_stemmer_med_kjent_verdi():
    lo, hi = h4.wilson(67, 85)  # KLAR-EVAL-0007: 0,690–0,862
    assert round(lo, 3) == 0.690 and round(hi, 3) == 0.862


def test_utvid_manus_en_rad_per_opptak(tmp_path):
    manus = [{"id": "per01nb", "malform": "nb", "klasse": "person", "setning": "x", "elementer": [], "dialektutvalg": False}]
    w = tmp_path / "a.wav"
    w.write_bytes(b"RIFFxxxx")
    rader, meta = h4.utvid_manus(manus, [("runde-1", {"dialektregion": "t", "dialektkilde": "morsmål"}, {"per01nb": w, "ukjent": w})])
    assert [r["id"] for r in rader] == ["runde-1:per01nb"] and meta["runde-1:per01nb"]["region"] == "t"


def test_testmanus_kan_ikke_scores_for_preregistreringen_er_registrert(monkeypatch, tmp_path):
    from arkivklarering import evaldata
    (tmp_path / "KLAR-PREREG-0001_arkivklarering_testdeler_v1.0_2026-11-01.md").write_text("Status: UTKAST (ikke sendt inn)\n")
    monkeypatch.setattr(evaldata, "DOCS", tmp_path)  # et utkast i en egen mappe, ikke repoets ekte (registrerte) PREREG
    monkeypatch.setattr(sys, "argv", ["kjor_h4.py", "--prereg-id", "KLAR-PREREG-0001"])
    with pytest.raises(evaldata.TestdelSperret):
        h4.main()
