import collections
import glob
import hashlib
import pathlib
import re

import pytest

from arkivklarering import kalibrering, personvern

REPO = pathlib.Path(__file__).resolve().parent.parent
MANUS = sorted(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0001_*.tsv")))[-1]  # justeringsmanuset
TESTMANUS = sorted(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))[-1]  # urørt testmateriale (H4)
BEGGE = [MANUS, TESTMANUS]


def _les(sti):
    return kalibrering.les_manus(sti, kun_struktur=True)  # formatkontroll; ingen rørledning, mønstre eller ordlister
KLASSER = {"person", "sted", "dato", "fødselsår", "telefon", "fødselsnummer", "e-post", "helse", "økonomi", "konflikt",
           "religion", "politikk", "kombinert"}


@pytest.mark.parametrize("manus", BEGGE)
def test_manus_struktur(manus):
    rader = _les(manus)
    assert len({r["id"] for r in rader}) == len(rader)
    per = collections.Counter((r["klasse"], r["malform"]) for r in rader)
    assert {k for k, _ in per} == KLASSER
    assert all(n == 6 for n in per.values())  # seks setninger per klasse og målform
    assert sorted(r["malform"] for r in rader).count("nb") == sorted(r["malform"] for r in rader).count("nn")


@pytest.mark.parametrize("manus", BEGGE)
def test_elementene_star_i_setningen_og_kategoriene_finnes(manus):
    for r in _les(manus):
        assert r["elementer"], r["id"]
        for el in r["elementer"]:
            assert el["type"] in personvern.KATEGORI.values(), (r["id"], el["type"])
            norm_setning = kalibrering.score.normaliser(r["setning"])
            assert any(kalibrering.score._inneholder(norm_setning, kalibrering.score.normaliser(f)) for f in el["former"]), (r["id"], el)


@pytest.mark.parametrize("manus", BEGGE)
def test_fodselsnumre_er_ugyldige_og_ikke_ekte(manus):
    def gyldig(n):
        d = [int(c) for c in n]
        k1 = (11 - sum(a * b for a, b in zip(d[:9], (3, 7, 6, 1, 8, 9, 4, 5, 2))) % 11) % 11
        k2 = (11 - sum(a * b for a, b in zip(d[:10], (5, 4, 3, 2, 7, 6, 5, 4, 3, 2))) % 11) % 11
        return k1 == d[9] and k2 == d[10]
    n = 0
    for r in _les(manus):
        for el in r["elementer"]:
            if el["type"] == "fødselsnummer":
                n += 1
                assert len(el["former"][0]) == 11 and not gyldig(el["former"][0]), r["id"]
    assert n == 12


def test_score_flagg_treff_og_bom():
    fasit = {"id": "x", "malform": "nn", "klasse": "person", "setning": "Takk til Halvor Brekkebu.",
             "elementer": [{"type": "person", "former": ["Halvor Brekkebu"]}]}
    s = kalibrering.score_flagg(fasit, "takk til halvor brekkebu", [{"kategori": "person", "utdrag": "halvor brekkebu"}])
    assert s["elementer"][0]["tekst_treff"] and s["elementer"][0]["flagg_treff"]
    s = kalibrering.score_flagg(fasit, "takk til halvor brekkebu", [{"kategori": "sted", "utdrag": "halvor brekkebu"}])
    assert s["elementer"][0]["tekst_treff"] and not s["elementer"][0]["flagg_treff"]
    s = kalibrering.score_flagg(fasit, "takk til halvor", [{"kategori": "person", "utdrag": "halvor"}])
    assert not s["elementer"][0]["tekst_treff"]


def _ord_av_type(manus, typer):
    ut = set()
    for r in _les(manus):
        for el in r["elementer"]:
            if el["type"] in typer:
                ut.update(el["former"])
    return ut


def test_testmanuset_er_nytt_materiale():
    """MANUS-0002 deler ingen setning, ingen personnavn, ingen steder og ingen tall med justeringsmanuset (ren strengsammenligning)."""
    a, b = _les(MANUS), _les(TESTMANUS)
    assert not {r["setning"] for r in a} & {r["setning"] for r in b}
    assert not {r["id"] for r in a} - {r["id"] for r in b}  # samme id-system, ikke samme innhold
    for typer in ({"person"}, {"sted"}, {"telefon"}, {"fødselsnummer"}, {"e-post"}, {"dato"}):
        assert not _ord_av_type(MANUS, typer) & _ord_av_type(TESTMANUS, typer), typer


SHA_MANUS_0002_V12 = "9a3d12d1e2438b09f9fcb6aa43300ace406888732d058e3cbabf70cb0ad963b1"  # registrert v1.2, ført i KLAR-PREREG-0001
SHA_MANUS_0002_V13 = "d71b5b138279f19b116f6f207cb0d1e586b1354d31c2ccb0fe044aaa03ff3003"  # v1.3 (AV-29): alle sju telefonnumre byttet til 68 05


def test_testmanusets_sha256_staar_i_preregistreringen():
    """Sha256 av den registrerte KLAR-MANUS-0002 v1.2 er ført ordrett i KLAR-PREREG-0001. v1.3 (AV-29) bytter alle sju telefonnumrene
    til Nkoms serie for TV- og filmproduksjon (68 05 00 00–68 05 99 99), og erstatter v1.2 i arbeidstreet (v1.2 ligger i git-historikken); H4
    gjennomføres ikke i v1.0 (AV-27). v1.3 er låst til sha256 over: en ny endring i fila bryter testen."""
    from arkivklarering import evaldata
    prereg = evaldata.siste_versjon(glob.glob(str(REPO / "docs" / "KLAR-PREREG-0001_*.md")))
    assert SHA_MANUS_0002_V12 in pathlib.Path(prereg).read_text(encoding="utf-8"), "sha256 av testmanuset v1.2 mangler i PREREG-0001"
    assert pathlib.Path(TESTMANUS).name == "KLAR-MANUS-0002_arkivklarering_testmanus_v1.3_2026-10-27.tsv"
    assert hashlib.sha256(pathlib.Path(TESTMANUS).read_bytes()).hexdigest() == SHA_MANUS_0002_V13


SHA_MANUS_0001_V12 = "085e72c9f38b189eb5d66101660ea96f9ee75937d20a93b749a2bdccad443a66"  # v1.2 (AV-29): alle telefonnumre byttet til 68 05


def test_justeringsmanusets_sha256_er_laast():
    """KLAR-MANUS-0001 v1.2 (AV-29) er låst til sha256 over; en endring i fila er en ny versjon."""
    assert pathlib.Path(MANUS).name == "KLAR-MANUS-0001_arkivklarering_justeringsmanus_v1.2_2026-10-27.tsv"
    assert hashlib.sha256(pathlib.Path(MANUS).read_bytes()).hexdigest() == SHA_MANUS_0001_V12


@pytest.mark.parametrize("manus", BEGGE)
def test_telefonnumrene_ligger_i_nkoms_fiktivserie(manus):
    """Alle telefonnumre i manusene ligger i Nkoms serie for TV- og filmproduksjon, 68 05 00 00–68 05 99 99 (KLAR-KILDE-0001, NK-02,
    NK-03; AV-29), og ingen andre 8-sifrede tall står i setningene."""
    n = 0
    for r in _les(manus):
        for el in r["elementer"]:
            if el["type"] == "telefon":
                n += 1
                assert re.fullmatch(r"6805\d{4}", el["former"][0]), (r["id"], el)
        for m in re.finditer(r"(?<!\d)\d{2}(?: ?\d{2}){3}(?!\d)", r["setning"]):
            assert re.sub(r"\D", "", m.group(0)).startswith("6805"), (r["id"], m.group(0))
    assert n == 14


def test_testmanuset_er_sperret_for_roerledningen_foer_registrering(tmp_path, monkeypatch):
    """les_manus uten kun_struktur avviser MANUS-0002 uten registrert preregistrering; justeringsmanuset er åpent."""
    import pytest
    from arkivklarering import evaldata
    (tmp_path / "KLAR-PREREG-0001_arkivklarering_testdeler_v1.0_2026-11-01.md").write_text("Status: UTKAST (ikke sendt inn)\n")
    monkeypatch.setattr(evaldata, "DOCS", tmp_path)  # et utkast i en egen mappe, ikke repoets ekte (registrerte) PREREG
    assert kalibrering.les_manus(MANUS)
    with pytest.raises(evaldata.TestdelSperret):
        kalibrering.les_manus(TESTMANUS)
    with pytest.raises(evaldata.TestdelSperret):
        kalibrering.les_manus(TESTMANUS, prereg_id="KLAR-PREREG-0001")  # utkastet i tmp_path
