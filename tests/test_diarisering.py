import json

import pytest

from arkivklarering import diarisering, eksport
from arkivklarering.segment import Segment
from arkivklarering.transkriber import Cue


def test_taler_navngis_i_rekkefolgen_de_forst_snakker():
    rå = [{"start": 5.0, "stopp": 8.0, "etikett": "SPEAKER_01"}, {"start": 0.0, "stopp": 4.0, "etikett": "SPEAKER_00"},
          {"start": 9.0, "stopp": 10.0, "etikett": "SPEAKER_01"}]
    t = diarisering.navngi_talere(rå)
    assert [(x.start, x.taler) for x in t] == [(0.0, "TALER_1"), (5.0, "TALER_2"), (9.0, "TALER_2")]


def test_cue_faar_taleren_med_mest_overlapp():
    t = [diarisering.Tur(0, 4, "TALER_1"), diarisering.Tur(4, 10, "TALER_2")]
    c = [Cue(1, 3, "a"), Cue(3, 8, "b"), Cue(11, 12, "c")]
    assert diarisering.tildel_cuer(c, t) == ["TALER_1", "TALER_2", None]


def test_vtt_med_taler_er_gyldig_og_har_voice_span(tmp_path):
    c = [Cue(0, 2, "hei"), Cue(2, 4, "på deg")]
    sti = eksport.skriv_vtt(c, tmp_path / "x.vtt", "ra", taler=["TALER_1", None])
    tekst = sti.read_text(encoding="utf-8")
    assert "<v TALER_1>hei" in tekst and "\npå deg\n" in tekst and eksport.valider_vtt(tekst) == []


def test_ohms_transcript_har_talermerke_og_validerer():
    c = [Cue(0, 2, "hei"), Cue(2, 4, "på deg")]
    xml = eksport.bygg_ohms_xml({"tittel": "t", "emneord": [], "talere": [], "segmenter": []}, c, "x.wav", 4.0, taler=["TALER_1", "TALER_2"])
    assert b"TALER_1: hei" in xml and b"TALER_2: p\xc3\xa5 deg" in xml
    if not eksport.OHMS_XSD.is_file():
        pytest.skip(f"ohms.xsd finnes ikke ({eksport.OHMS_XSD}; ligger under ARKIVKLARERING_DATA/eval-data/ohms, eller sett ARKIVKLARERING_OHMS_XSD)")
    assert eksport.valider_ohms(xml) == []


def test_segments_json_har_taler_per_cue_og_info(tmp_path):
    from arkivklarering.transkriber import Oppsett
    tl = [Segment("speech", 0.0, 10.0, "transkriber")]
    cues = {"ra": [Cue(1, 3, "a"), Cue(4, 6, "b")]}
    o = {"ra": Oppsett("ra", "wcli", "/m/ra.bin", "x", "nn")}
    sti = eksport.skriv_segments_json(tl, cues, tmp_path / "s.json", "x.wav", o, taler_per_lag={"ra": ["TALER_1", "TALER_2"]},
                                      taler_info={"modell": "m", "antall_talere": 2, "turer": []})
    d = json.loads(sti.read_text(encoding="utf-8"))
    assert d["segmenter"][0]["taler"] == {"ra": ["TALER_1", "TALER_2"]} and d["talerinndeling"]["antall_talere"] == 2


def test_uten_taler_er_utdata_uendret(tmp_path):
    c = [Cue(0, 2, "hei")]
    t = eksport.skriv_vtt(c, tmp_path / "x.vtt").read_text(encoding="utf-8")
    assert "<v " not in t and "TALER" not in t
