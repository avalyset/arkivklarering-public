import pytest

from arkivklarering import katalog, personvern
from arkivklarering.transkriber import Cue

CUER = [Cue(0.0, 5.0, "Velkommen til sendinga frå Vinstra. Eg heiter Kari Nordmann."),
        Cue(30.0, 40.0, "Vi skal snakke om jernbana som kom i 1948."),
        Cue(70.0, 80.0, "Torbjørn Stuvstad fortel om garden Bjølstad.")]


def _u(kat, utdrag, a, b):
    f = personvern.Flagg(0, len(utdrag), kat, "k", 0.9, utdrag, "normalisert", a, b)
    return personvern.slaa_sammen_lag({"normalisert": [f], "ra": []})[0]


class Falsk:
    def __init__(self):
        self.kall = 0

    def __call__(self, modell, system, bruker):
        self.kall += 1
        if "sammendrag" in bruker and "Transkripsjon:" in bruker and "personvernflaggene" not in bruker:
            return '{"sammendrag": "Utkast til sammendrag."}'
        return ('{"tittel": "Sending frå Vinstra", "dato": "1948", "talere": ["Kari Nordmann", "Ola Diktet"], '
                '"steder": ["Vinstra", "Roma"], "emneord": ["jernbane", "Jernbane", "lokalhistorie", "gard", "Vinstra"]}')


def test_utkast_og_kontroll_mot_teksten():
    flagg = [_u("person", "Kari Nordmann", 0, 5), _u("person", "Torbjørn Stuvstad", 70, 80), _u("sted", "Vinstra", 0, 5), _u("sted", "Bjølstad", 70, 80)]
    post = katalog.lag_katalogpost(CUER, flagg, modell="test", chat=Falsk())
    assert post.merknad == "utkast – maskinforslag" and post.modell == "test"
    assert post.tittel == "Sending frå Vinstra" and post.dato == "1948"
    assert post.talere == ["Kari Nordmann"]                       # «Ola Diktet» står ikke i teksten
    assert post.steder == ["Bjølstad", "Vinstra"]                 # «Roma» står ikke i teksten, stedene fra flaggene beholdes
    assert 3 <= len(post.emneord) <= 8 and len(set(post.emneord)) == len(post.emneord)
    assert any("Ola Diktet" in f for f in post.forkastet) and any("Roma" in f for f in post.forkastet)
    assert [s["start"] for s in post.segmenter] == [0.0, 70.0] or len(post.segmenter) == 2
    assert all(s["sammendrag"] for s in post.segmenter)


def test_dato_som_ikke_star_i_teksten_forkastes():
    post = katalog.rens_post({"dato": "1999-01-01", "emneord": ["a", "b", "c"]}, "ingen år her", [], [])
    assert post.dato is None and any("dato" in f for f in post.forkastet)


def test_for_faa_emneord_logges_og_for_mange_kuttes():
    assert any("emneord" in f for f in katalog.rens_post({"emneord": ["a"]}, "", [], []).forkastet)
    assert len(katalog.rens_post({"emneord": [f"e{i}" for i in range(20)]}, "", [], []).emneord) == 8


def test_bare_lokal_ollama():
    with pytest.raises(katalog.IkkeLokalt):
        katalog.ollama_chat("m", "s", "b", url="https://api.example.com")
    with pytest.raises(katalog.IkkeLokalt):
        katalog.ollama_chat("m", "s", "b", url="http://10.0.0.5:11434")


def test_json_med_stoy_rundt():
    assert katalog._json('Her er svaret: {"a": 1} ferdig')["a"] == 1
    assert katalog._json("ikke json") == {}


def test_vinduer_grupperer_pa_tid():
    v = katalog.vinduer(CUER, 60)
    assert [(a, b) for a, b, _ in v] == [(0.0, 40.0), (70.0, 80.0)]


def test_emneord_som_ligner_nummer_forkastes():
    post = katalog.rens_post({"emneord": ["sjukdom", "68054567", "arbeiderpartiet", "volda", "01017012345"]}, "tekst", [], [])
    assert post.emneord == ["sjukdom", "arbeiderpartiet", "volda"]
    assert any("68054567" in f for f in post.forkastet) and any("01017012345" in f for f in post.forkastet)
