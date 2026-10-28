import pathlib
import sys
import time

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "eval" / "dev"))
import felles  # noqa: E402

from arkivklarering import transkriber  # noqa: E402


def test_for_lite_disk_stopper():
    assert "disk" in felles.grunn_for(7.9, 1000, 80, False)
    assert felles.grunn_for(8.0, 1000, 80, False) is None


def test_mye_swap_stopper():
    assert "swap" in felles.grunn_for(20, 6657, 80, False)
    assert felles.grunn_for(20, 6656, 80, False) is None


def test_minne_og_annen_vakt_gjelder_bare_for_start():
    assert "minnevakt" in felles.grunn_for(20, 1000, 80, True)
    assert "minne" in felles.grunn_for(20, 1000, 37, False)
    assert felles.grunn_for(20, 1000, 37, True, bare_kjoring=True) is None
    assert "disk" in felles.grunn_for(5, 1000, 37, True, bare_kjoring=True)


def test_vakt_dreper_prosessen_og_reiser_avbrutt():
    start = time.time()
    with pytest.raises(transkriber.Avbrutt) as e:
        transkriber.kjor_prosess(["sleep", "60"], 120, vakt=lambda: "test: for lite disk")
    assert "for lite disk" in str(e.value) and time.time() - start < 20


def test_prosess_uten_avbrudd_gir_utdata():
    r = transkriber.kjor_prosess(["echo", "hei"], 30, vakt=lambda: None)
    assert r.returncode == 0 and r.stdout.strip() == "hei"
