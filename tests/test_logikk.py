from arkivklarering.eksport import vtt_tid
from arkivklarering.segment import (FLAGG_MUSIKK_UNDER_TALE, FORESLATT_KLIPP, INGEN_HANDLING,
                                    MENNESKELIG_VURDERING, TRANSKRIBER, bygg_tidslinje)
from arkivklarering.transkriber import er_lydmerke


def test_vtt_tid():
    assert vtt_tid(0) == "00:00:00.000"
    assert vtt_tid(3661.5) == "01:01:01.500"


def test_tale_broes_over_kort_stoy_men_ikke_over_musikk():
    raa = [("speech", 0, 2), ("other", 2, 2.4), ("speech", 2.4, 5),
           ("music", 5, 6), ("speech", 6, 9)]
    t = bygg_tidslinje(raa)
    assert [(s.label, s.start, s.stop, s.disposisjon) for s in t] == [
        ("speech", 0, 5, TRANSKRIBER), ("music", 5, 6, FORESLATT_KLIPP), ("speech", 6, 9, TRANSKRIBER)]


def test_speech_plus_music_transkriberes_og_flagges():
    t = bygg_tidslinje([("speech+music", 0, 4)])
    assert (t[0].label, t[0].disposisjon) == ("speech+music", TRANSKRIBER)
    assert t[0].flagg == [FLAGG_MUSIKK_UNDER_TALE]
    assert t[0].musikk_under_tale == [(0, 4)]


def test_sammenslaing_beholder_intervallene_med_musikk_under_tale():
    t = bygg_tidslinje([("speech", 0, 2), ("speech+music", 2, 2.3), ("speech", 2.3, 6)])
    assert len(t) == 1 and t[0].disposisjon == TRANSKRIBER
    assert t[0].label == "speech+music" and t[0].musikk_under_tale == [(2, 2.3)]
    assert t[0].flagg == [FLAGG_MUSIKK_UNDER_TALE]


def test_ren_tale_har_ingen_flagg():
    t = bygg_tidslinje([("speech", 0, 4)])
    assert t[0].flagg == [] and t[0].musikk_under_tale == []


def test_music_og_other_far_aldri_transkriber():
    t = bygg_tidslinje([("music", 0, 5), ("other", 5, 9), ("music", 9, 12)])
    assert [s.disposisjon for s in t] == [FORESLATT_KLIPP, INGEN_HANDLING, FORESLATT_KLIPP]


def test_lang_gap_broes_ikke():
    t = bygg_tidslinje([("speech", 0, 2), ("other", 2, 4), ("speech", 4, 6)])
    assert [s.label for s in t] == ["speech", "other", "speech"]


def test_kort_tale_gar_til_menneskelig_vurdering():
    t = bygg_tidslinje([("other", 0, 1), ("speech", 1, 1.2)])
    assert t[1].disposisjon == MENNESKELIG_VURDERING


def test_lydmerker():
    assert er_lydmerke("[MUSIC]") and er_lydmerke(" ♪ ") and er_lydmerke("(musikk)")
    assert er_lydmerke("<|nocaptions|>") and er_lydmerke(".")
    assert not er_lydmerke("Ho gjekk heim") and not er_lydmerke("(Ja) det stemmer")


def test_cuer_begrenses_til_segmentet(monkeypatch, tmp_path):
    from arkivklarering import transkriber
    from arkivklarering.segment import Segment
    monkeypatch.setattr(transkriber, "_kutt", lambda *a, **k: None)
    monkeypatch.setattr(transkriber, "whisper_direkte", lambda *a, **k: {"transcription": [
        {"offsets": {"from": 0, "to": 30000}, "text": " heim frå skulen"},
        {"offsets": {"from": 31000, "to": 33000}, "text": " utenfor"}]})
    seg = Segment("speech", 20.48, 22.84, disposisjon=TRANSKRIBER)
    o = transkriber.Oppsett("ra", "x", "y", "", "nn")
    cues = transkriber.transkriber_segment(tmp_path / "x.wav", seg, o, tmp_path)
    assert [(c.start, c.stop) for c in cues] == [(20.48, 22.84), (22.84, 22.84)]


def test_ordtidsstempler_fra_dtw_gir_cuer_med_ordspenn():
    from arkivklarering import transkriber
    from arkivklarering.segment import Segment
    seg = Segment("speech", 10.0, 16.0, disposisjon=TRANSKRIBER)
    tok = lambda t, d: {"text": t, "t_dtw": d, "offsets": {"from": 0, "to": 0}}  # noqa: E731
    json_ = [{"tokens": [tok("[_BEG_]", -1), tok(" ho", 6), tok(" he", 19), tok("ite", 41), tok(" kari", 67), tok(" .", 120),
                         tok(" og", 300), tok(" ola", 330), tok("<|nocaptions|>", -1)]}]
    ord_ = transkriber._ord_fra_dtw(json_, seg)
    assert [w[0].strip() for w in ord_] == ["ho", "heite", "kari.", "og", "ola"]
    assert ord_[0][1] == 10.06 and ord_[1][2] == 10.67  # slutten er neste ords start
    assert ord_[-1][2] == 11.8 or ord_[-1][2] <= 16.0     # siste ord begrenses
    cuer = transkriber._ord_til_cuer(json_, seg)
    assert [c.tekst for c in cuer] == ["ho heite kari.", "og ola"]  # setningsslutt og pause deler cuene
    assert cuer[0].ord_tidsrom(0, 2) == (10.06, 10.19)  # «ho»
    assert cuer[0].ord_tidsrom(3, 8) == (10.19, 10.67)  # «heite»


def test_eget_mellomromstoken_gir_nytt_ord_for_tall():
    from arkivklarering import transkriber
    from arkivklarering.segment import Segment
    seg = Segment("speech", 0.0, 3.0, disposisjon=TRANSKRIBER)
    tok = lambda t, d: {"text": t, "t_dtw": d, "offsets": {"from": 0, "to": 0}}  # noqa: E731
    json_ = [{"tokens": [tok(" i", 54), tok(" ", 56), tok("19", 74), tok("17", 106)]}]
    assert [w[0].strip() for w in transkriber._ord_fra_dtw(json_, seg)] == ["i", "1917"]
