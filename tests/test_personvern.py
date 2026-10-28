"""Raske tester av personvern.py som ikke laster NLP-modeller (mønstre og ordlister), og en tung motortest."""
import pytest

from arkivklarering import personvern as p


def _treff(gjenkjenner, tekst):
    return [(tekst[r.start:r.end], r.entity_type) for r in gjenkjenner.analyze(tekst, [gjenkjenner.supported_entities[0]])]


def _gj(entitet, sprak="nn"):
    return next(r for r in p.monster_gjenkjennere(sprak) if r.supported_entities[0] == entitet)


def test_dato_nb_og_nn():
    g = _gj("NB_DATO")
    assert _treff(g, "Han vart fødd 3. november 1965 i Volda.") == [("3. november 1965", "NB_DATO")]
    assert _treff(g, "Møtet var 15.03.1999.")[0][0] == "15.03.1999"


def test_fodselsaar_krever_fodt_konteks():
    g = _gj("NB_FODSELSAAR")
    assert _treff(g, "Ho vart fødd i 1972 i Volda.") == [("1972", "NB_FODSELSAAR")]
    assert _treff(g, "Han er født 1965.") == [("1965", "NB_FODSELSAAR")]
    assert _treff(g, "Boka kom ut i 1972.") == []


def test_telefon_og_fodselsnummer():
    t = _gj("NB_TELEFON")
    assert _treff(t, "Ring 68054567 i dag.")[0][0] == "68054567"
    assert _treff(t, "Ring 68 05 45 67.")[0][0] == "68 05 45 67"
    assert _treff(t, "Året 1972 er ikke et nummer.") == []
    f = _gj("NB_FODSELSNUMMER")
    assert _treff(f, "Fødselsnummeret er 01016512345.")[0][0] == "01016512345"


def test_nokkelord_er_hele_ord_og_ikke_case_folsomme():
    h = _gj("SENS_HELSE")
    assert [x[0] for x in _treff(h, "Han var Syk og lå på sykehuset.")] == ["Syk", "sykehuset"]  # bestemt form tillates
    assert _treff(h, "Det er sykt bra") == []  # «sykt» er ikke i lista


@pytest.mark.parametrize("navn", ["helse", "okonomi", "konflikt", "religion", "politikk"])
def test_ordlistene_har_ingen_personnavn_og_er_smaa_bokstaver(navn):
    ord_ = p.les_ordliste(navn)
    assert len(ord_) > 10
    for o in ord_:
        assert o == o.lower(), f"{navn}: «{o}» har store bokstaver (personnavn?)"
        assert not any(c.isdigit() for c in o)
    assert len(ord_) == len(set(ord_))


def test_ukjent_sprak():
    with pytest.raises(ValueError):
        p.flagg_tekst("x", "en", motor=object())


@pytest.mark.tung
def test_motor_flagger_navn_sted_dato_og_nokkelord():
    m = p.lag_motor()
    f = p.flagg_tekst("Ho heitte Kari Nordmann og vart fødd i 1972 i Volda. Ho var sjuk.", "nn", m)
    typer = {(x.kategori, x.utdrag) for x in f}
    assert ("person", "Kari Nordmann") in typer and ("sted", "Volda") in typer
    assert ("fødselsår", "1972") in typer and ("helse", "sjuk") in typer


def _f(kat, utdrag, a, b, lag="ra", score=0.6):
    return p.Flagg(0, len(utdrag), kat, "k", score, utdrag, lag, a, b)


def test_union_slaar_sammen_samme_kategori_og_overlappende_tid():
    ra = [_f("person", "karin", 20.0, 30.0, "ra", 0.497)]
    nor = [_f("person", "Kari Nordmann", 20.5, 22.0, "normalisert", 1.0)]
    u = p.slaa_sammen_lag({"ra": ra, "normalisert": nor})
    assert len(u) == 1 and u[0].lag == "begge" and u[0].score == 1.0
    assert (u[0].start, u[0].stopp) == (20.0, 30.0)
    assert u[0].per_lag["ra"]["utdrag"] == "karin" and u[0].per_lag["normalisert"]["utdrag"] == "Kari Nordmann"
    assert u[0].per_lag["ra"]["cue_start"] == 20.0 and u[0].per_lag["normalisert"]["cue_stopp"] == 22.0


def test_union_beholder_flagg_som_bare_finnes_i_ett_lag():
    ra = [_f("helse", "sjuk", 1, 5, "ra"), _f("person", "ola", 1, 5, "ra", 0.2)]
    nor = [_f("sted", "Volda", 1, 5, "normalisert", 0.99)]
    u = p.slaa_sammen_lag({"ra": ra, "normalisert": nor})
    assert sorted((x.kategori, x.lag) for x in u) == [("helse", "ra"), ("person", "ra"), ("sted", "normalisert")]


def test_union_krever_overlappende_tid_og_lik_kategori():
    u = p.slaa_sammen_lag({"ra": [_f("person", "Ola", 0, 2, "ra")], "normalisert": [_f("person", "Ola", 5, 7, "normalisert")]})
    assert [x.lag for x in u] == ["ra", "normalisert"]
    u = p.slaa_sammen_lag({"ra": [_f("person", "Ola", 0, 2, "ra")], "normalisert": [_f("sted", "Ola", 0, 2, "normalisert")]})
    assert len(u) == 2


def test_union_parer_etter_likhet_nar_ra_dekker_hele_segmentet():
    ra = [_f("person", "kari", 0, 30, "ra"), _f("person", "ola", 0, 30, "ra")]
    nor = [_f("person", "Ola", 5, 6, "normalisert"), _f("person", "Kari", 1, 2, "normalisert")]
    u = p.slaa_sammen_lag({"ra": ra, "normalisert": nor})
    assert len(u) == 2 and all(x.lag == "begge" for x in u)
    par = {x.per_lag["ra"]["utdrag"]: x.per_lag["normalisert"]["utdrag"] for x in u}
    assert par == {"kari": "Kari", "ola": "Ola"}


def test_union_tom():
    assert p.slaa_sammen_lag({"ra": [], "normalisert": []}) == []


def _fo(kat, utdrag, ord0, ord1, lag, cue=(0.0, 30.0), score=0.6):
    f = p.Flagg(0, len(utdrag), kat, "k", score, utdrag, lag, cue[0], cue[1])
    f.ord_start, f.ord_stopp = ord0, ord1
    return f


def test_union_med_ordtider_slar_ikke_sammen_to_ulike_personer():
    # rålaget har én cue over hele segmentet; to ulike personer med ulik tid skal forbli to flagg
    ra = [_fo("person", "kari", 1.0, 1.4, "ra"), _fo("person", "ola", 5.0, 5.4, "ra")]
    nor = [_fo("person", "Kari", 1.1, 1.5, "normalisert", (0.0, 8.0))]
    u = p.slaa_sammen_lag({"ra": ra, "normalisert": nor})
    assert sorted((x.lag, x.per_lag.get("ra", {}).get("utdrag")) for x in u) == [("begge", "kari"), ("ra", "ola")]
    # to flagg som hver er alene i sitt lag, men i ulik tid, parres ikke selv om cuene overlapper helt
    u = p.slaa_sammen_lag({"ra": [_fo("person", "kari", 1.0, 1.4, "ra")], "normalisert": [_fo("person", "Ola", 5.0, 5.5, "normalisert")]})
    assert sorted(x.lag for x in u) == ["normalisert", "ra"]


def test_union_med_ordtider_parer_pa_tid_selv_med_lav_likhet():
    ra = [_fo("person", "karin", 20.3, 21.7, "ra")]
    nor = [_fo("person", "Kari Nordmann", 20.2, 21.7, "normalisert")]
    u = p.slaa_sammen_lag({"ra": ra, "normalisert": nor})
    assert len(u) == 1 and u[0].lag == "begge" and (u[0].start, u[0].stopp) == (20.2, 21.7)
    assert u[0].per_lag["ra"]["ord_start"] == 20.3 and u[0].per_lag["normalisert"]["ord_stopp"] == 21.7


def test_union_likhet_skiller_flere_tidstreff():
    ra = [_fo("person", "kari", 1.0, 1.4, "ra"), _fo("person", "ola", 1.1, 1.5, "ra")]
    nor = [_fo("person", "Ola", 1.0, 1.5, "normalisert"), _fo("person", "Kari", 1.0, 1.5, "normalisert")]
    u = p.slaa_sammen_lag({"ra": ra, "normalisert": nor})
    par = {x.per_lag["ra"]["utdrag"]: x.per_lag["normalisert"]["utdrag"] for x in u}
    assert par == {"kari": "Kari", "ola": "Ola"}


def test_flagg_cues_setter_ordspenn_fra_ordtider():
    from arkivklarering.transkriber import Cue

    class Motor:
        def analyze(self, text, language, entities, score_threshold):
            from presidio_analyzer import RecognizerResult
            return [RecognizerResult("PERSON", text.index("Kari"), text.index("Kari") + 4, 0.9)]

    c = Cue(10.0, 12.0, "hei Kari Nordmann", [(0, 3, 10.0, 10.3), (4, 8, 10.4, 10.9), (9, 17, 11.0, 12.0)])
    f = p.flagg_cues([c], "ra", "nn", Motor())
    assert (f[0].ord_start, f[0].ord_stopp) == (10.4, 10.9)


def test_telefon_og_fodselsnummer_med_skilletegn_fra_whisper():
    t, f = _gj("NB_TELEFON"), _gj("NB_FODSELSNUMMER")
    assert _treff(t, "Ring oss på 68, 05, 45, 67 hvis du vet mer.")[0][0] == "68, 05, 45, 67"
    assert _treff(t, "Mobil 68, 05, 34, 56 etter fire.")[0][0] == "68, 05, 34, 56"
    assert _treff(t, "Ring +47 68 05 45 67.")[0][0].startswith("+47")
    assert _treff(f, "Oppgi fødselsnummer 150 575 45 615 i skjemaet.")[0][0] == "150 575 45 615"
    assert _treff(f, "nummer 230 248 78 913.")[0][0] == "230 248 78 913"


def test_siffer_som_ikke_er_nummer_avvises():
    t, f = _gj("NB_TELEFON"), _gj("NB_FODSELSNUMMER")
    for tekst in ("Brevet er datert 28.05.1972.", "Årene 2010, 2012 var gode.", "I 1965, 1972 og 1980.", "Det var 1234567 kroner.", "Tallet 12345678."):
        assert _treff(t, tekst) == [] and _treff(f, tekst) == [], tekst
    assert _treff(f, "Nummeret 99999999999 er ikke en dato.") == []


def test_nokkelord_boyning_og_ordgrenser():
    k = _gj("SENS_KONFLIKT")
    assert [x[0] for x in _treff(k, "Hun anmeldte mobbingen, og rettssaken startet.")] == ["anmeldte", "mobbingen", "rettssaken"]
    h = _gj("SENS_HELSE")
    assert _treff(h, "Han kjøpte en sykkel.") == [] and _treff(h, "Det er sykt bra") == []
