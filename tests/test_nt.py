"""-nt (ingen tidsstempeltokens) bare for rålaget (KLAR-ADR-0017, KLAR-EVAL-0011)."""
import copy
import json
import pathlib
import re

import pytest

from arkivklarering import personvern, transkriber
from arkivklarering.segment import Segment

FIX = pathlib.Path(__file__).resolve().parent / "fixtures" / "nt_normalisert_nb12.json"


def _oppsett(lag, **kw):
    return transkriber.Oppsett(lag, "wcli", "/m.bin", "x", "no", **kw)


@pytest.fixture
def falske_modeller(monkeypatch, tmp_path):
    """finn_oppsett uten de ekte modellene (3 GB hver) og uten whisper-cli: tomme modellfiler, ingen sha256-kontroll."""
    for lag in transkriber.LAG:
        (tmp_path / f"{lag}.bin").write_bytes(b"")
        monkeypatch.setenv(f"ARKIVKLARERING_MODELL_{lag.upper()}", str(tmp_path / f"{lag}.bin"))
    monkeypatch.setattr(transkriber, "finn_whisper", lambda whisper=None: "wcli")
    return lambda lag: transkriber.finn_oppsett(lag, verifiser=False)


def test_standard_er_nt_for_raalaget_og_ikke_for_normalisert(monkeypatch, falske_modeller):
    monkeypatch.delenv("ARKIVKLARERING_MED_TIDSSTEMPELTOKENS", raising=False)
    assert falske_modeller("ra").uten_tidsstempeltokens is True
    assert falske_modeller("normalisert").uten_tidsstempeltokens is False


def test_miljovariabel_slaar_av_nt_for_aa_gjenskape_for_nt_tall(monkeypatch, falske_modeller):
    monkeypatch.setenv("ARKIVKLARERING_MED_TIDSSTEMPELTOKENS", "1")
    assert falske_modeller("ra").uten_tidsstempeltokens is False


def test_standard_modellsti_er_relativ_til_datarota(tmp_path):
    import json
    lock = json.loads(transkriber.LOCK.read_text(encoding="utf-8"))
    for lag in transkriber.LAG:
        assert not pathlib.Path(lock[lag]["standardsti"]).is_absolute()
        assert transkriber.standard_modellsti(lag, tmp_path) == tmp_path / lock[lag]["standardsti"]
        assert transkriber.standard_modellsti(lag) == transkriber.DATA / "modeller" / pathlib.Path(lock[lag]["standardsti"]).name


def test_whisper_direkte_gir_nt_bare_naar_oppsettet_sier_det(monkeypatch, tmp_path):
    sett = []

    def falsk(argv, **kw):
        sett.append(argv)
        pathlib.Path(f"{tmp_path / 'x'}.json").write_text('{"transcription": []}', encoding="utf-8")

        class R:
            returncode = 0
            stderr = ""
        return R()

    monkeypatch.setattr(transkriber.subprocess, "run", falsk)
    transkriber.whisper_direkte(tmp_path / "a.wav", tmp_path / "x", _oppsett("ra", uten_tidsstempeltokens=True), ordtider=True)
    transkriber.whisper_direkte(tmp_path / "a.wav", tmp_path / "x", _oppsett("normalisert"), ordtider=True)
    assert "-nt" in sett[0] and "-dtw" in sett[0]  # DTW beholdes sammen med -nt
    assert "-nt" not in sett[1] and "-dtw" in sett[1]


def test_whisper_flere_gir_nt_bare_for_raalaget_ogsaa_uten_dtw(monkeypatch, tmp_path):
    sett = []

    def falsk(argv, timeout, vakt=None):
        sett.append(argv)
        for i, a in enumerate(argv):
            if a == "-f":
                pathlib.Path(f"{argv[i + 1]}.json").write_text('{"transcription": []}', encoding="utf-8")

        class R:
            returncode = 0
        return R()

    monkeypatch.setattr(transkriber, "kjor_prosess", falsk)
    w = tmp_path / "a.wav"
    transkriber.whisper_flere([w], _oppsett("ra", uten_tidsstempeltokens=True), ordtider=True)
    transkriber.whisper_flere([w], _oppsett("normalisert"), ordtider=True)
    assert "-nt" in sett[0] and "-nt" not in sett[1]
    assert sett[0][sett[0].index("-l") + 1] == "no"


def _ra_fra_normalisert():
    """Rålagets utdata har samme form som det normaliserte, men med små bokstaver og uten tegnsetting."""
    j = copy.deepcopy(json.loads(FIX.read_text(encoding="utf-8")))
    for t in j["transcription"]:
        t["text"] = re.sub(r"[^\w\s]", "", t["text"].lower())
        for tok in t["tokens"]:
            tok["text"] = re.sub(r"[^\w\s]", "", tok["text"].lower())
    return j


def test_begge_lag_har_ordspenn_med_nt_og_unionen_parer_dem_via_dtw():
    seg = Segment("speech", 0.0, 3.6, "transkriber")
    cuer = {"normalisert": transkriber.json_til_cues(json.loads(FIX.read_text(encoding="utf-8")), seg, True),
            "ra": transkriber.json_til_cues(_ra_fra_normalisert(), seg, True)}
    for lag, cs in cuer.items():
        assert cs and all(c.ord for c in cs), f"{lag}: cue uten ordtidsstempler"
        starter = [o[2] for c in cs for o in c.ord]  # ord = (tegn_fra, tegn_til, start_s, slutt_s)
        assert starter == sorted(starter) and all(0.0 <= s <= 3.6 for s in starter)
    # unionen: et flagg på samme ord i begge lag blir ett unionflagg via ordspennet
    fl = {}
    for lag, cs in cuer.items():
        o = cs[0].ord[1]  # andre ord
        fl[lag] = [personvern.Flagg(o[0], o[1], "sted", "test", 1.0, cs[0].tekst[o[0]:o[1]], lag, cs[0].start, cs[0].stop, o[2], o[3])]
    union = personvern.slaa_sammen_lag(fl)
    assert len(union) == 1 and set(union[0].per_lag) == {"ra", "normalisert"}


def test_gjenbruk_av_normalisert_bruker_lagrede_cuer_og_kjorer_bare_raalaget(monkeypatch, tmp_path):
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "eval" / "dev"))
    import felles
    kjort = []
    monkeypatch.setattr(felles, "vent_pa_ressurser", lambda *a, **k: None)
    monkeypatch.setattr(felles.segment, "segmenter", lambda lyd: [])
    monkeypatch.setattr(felles.segment, "bygg_tidslinje", lambda raa: [Segment("speech", 0.0, 3.0, "transkriber")])
    monkeypatch.setattr(felles.transkriber, "sjekk_segment", lambda s: None)
    monkeypatch.setattr(felles.transkriber, "_kutt", lambda lyd, a, b, w: pathlib.Path(w).write_bytes(b""))

    def falsk_flere(wavs, o, ordtider, logg, vakt=None):
        kjort.append(o.lag)
        return [{"transcription": []} for _ in wavs]

    monkeypatch.setattr(felles.transkriber, "whisper_flere", falsk_flere)
    gammel = {"s1": {"id": "s1", "cues": {"normalisert": [{"start": 0, "stop": 1, "tekst": "lagret", "ord": []}], "ra": []}}}
    o = {"ra": _oppsett("ra", uten_tidsstempeltokens=True), "normalisert": _oppsett("normalisert")}
    ut = felles.kjor_batch([{"id": "s1", "lyd": "x.wav", "whisper_sprak": "no"}], o, gjenbruk=gammel)
    assert kjort == ["ra"] and ut["s1"]["cues"]["normalisert"][0]["tekst"] == "lagret" and ut["s1"]["gjenbrukt"] == ["normalisert"]
