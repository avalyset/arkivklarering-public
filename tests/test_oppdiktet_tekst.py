"""Vern mot oppdiktet tekst: rene music- og other-segmenter (musikk, stillhet, støy) gir ingen tekst.

Del 1 (rask, ingen modeller): selv om tidslinjen bare har music/other, kalles Whisper aldri, og
direkte kall på et slikt segment avvises.
Del 2 (tung, krever modeller; kjøres med `pytest -m tung`): ekte lyd av musikk, stillhet og støy
går gjennom hele rørledningen (standard segmentør -> to lag), og ingen cue havner i music/other-segmenter. Segmentøren er
standarden (inaSpeechSegmenter, KLAR-ADR-0019 v1.1): testen sammenligner ikke med lagrede inaVAMOS-resultater, men sjekker
regelen for den rørledningen som faktisk brukes (ARKIVKLARERING_SEGMENTERING=inavamos tester inaVAMOS-varianten).
"""
import pathlib
import stat
import sys
import wave

import numpy as np
import pytest

from arkivklarering import segment, transkriber
from arkivklarering.segment import Segment

SR = 16000


@pytest.fixture
def falsk_whisper(tmp_path):
    """En whisper-cli som skriver en markør og feiler hvis den noen gang kalles."""
    markor = tmp_path / "kalt"
    sti = tmp_path / "whisper-cli"
    sti.write_text(f"#!/bin/sh\ntouch {markor}\nexit 1\n")
    sti.chmod(sti.stat().st_mode | stat.S_IXUSR)
    return sti, markor


def test_ren_music_og_other_sendes_aldri_til_whisper(falsk_whisper, tmp_path):
    sti, markor = falsk_whisper
    t = segment.bygg_tidslinje([("music", 0, 10), ("other", 10, 20), ("music", 20, 25), ("other", 25, 30)])
    o = transkriber.Oppsett("ra", str(sti), "/dev/null", "", "nn")
    assert transkriber.transkriber(tmp_path / "finnes_ikke.wav", t, o) == []
    assert not markor.exists()


@pytest.mark.parametrize("label", ["music", "other"])
def test_direkte_kall_pa_music_eller_other_avvises(label, falsk_whisper, tmp_path):
    sti, markor = falsk_whisper
    o = transkriber.Oppsett("ra", str(sti), "/dev/null", "", "nn")
    seg = Segment(label, 0, 5, disposisjon=segment.TRANSKRIBER)  # selv om noen setter feil disposisjon
    with pytest.raises(ValueError):
        transkriber.transkriber_segment(tmp_path / "x.wav", seg, o, tmp_path)
    assert not markor.exists()


def _skriv(x, sti):
    with wave.open(str(sti), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


@pytest.mark.tung
def test_musikk_stillhet_og_stoy_gjennom_hele_rorledningen(tmp_path):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
    import lag_testlyd
    rng = np.random.default_rng(1)
    stille = np.zeros(SR * 20, dtype=np.float32)
    stoy = (0.2 * rng.standard_normal(SR * 20)).astype(np.float32)
    x = np.concatenate([lag_testlyd.musikk(20), stille, stoy])
    lyd = tmp_path / "ikke_tale.wav"
    _skriv(x, lyd)
    tidslinje = segment.bygg_tidslinje(segment.segmenter(lyd))
    til_whisper = [s for s in tidslinje if s.disposisjon == segment.TRANSKRIBER]
    for lag in transkriber.LAG:
        cues = transkriber.transkriber(lyd, tidslinje, transkriber.finn_oppsett(lag))
        for c in cues:
            mid = (c.start + c.stop) / 2
            assert any(s.start <= mid <= s.stop for s in til_whisper), f"{lag}: tekst utenfor tale: {c}"
    # ingen cue kan ligge i music/other; hvis segmentøren fant tale i støyen, er det segmentørens funn
    # og rapporteres i stedet for å skjules
    assert all(s.label in segment.TALE_ETIKETTER for s in til_whisper)
