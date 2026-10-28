"""Tester av eksportformatene. Skjemavalidering der det finnes et skjema: OHMS (ohms.xsd), MMIF (mmif-python mot MMIF-skjemaet),
IIIF Presentation 3 (iiif-prezi3). WebVTT har bare en parserkontroll."""
import json
import pathlib

import pytest

from arkivklarering import eksport, miljo
from arkivklarering.segment import Segment
from arkivklarering.transkriber import Cue

POST = {"tittel": "Utkast: Sending fra Vinstra", "dato": "1965-11-03", "talere": ["Kari Nordmann"], "steder": ["Vinstra"],
        "emneord": ["lokalhistorie", "jernbane", "Gudbrandsdalen"], "modell": "test", "merknad": "utkast – maskinforslag",
        "segmenter": [{"start": 0.0, "stopp": 4.0, "sammendrag": "Innledning om jernbanen."},
                      {"start": 4.0, "stopp": 9.5, "sammendrag": "Intervju om oppveksten på Vinstra."}]}
CUER = [Cue(0.0, 3.5, "Velkommen til sendinga frå Vinstra."), Cue(4.2, 9.0, "Kari Nordmann fortel om oppveksten.")]
TL = [Segment("speech", 0.0, 4.0, "transkriber"), Segment("music", 4.0, 5.0, "foreslått klipp"), Segment("speech", 5.0, 9.5, "transkriber")]
OHMS_XSD = eksport.OHMS_XSD
IIIF_RECEPT = miljo.EVAL_DATA / "iiif" / "recept_0219_manifest.json"


# ------------------------------------------------------------ WebVTT
def test_vtt_gyldig_og_ugyldig(tmp_path):
    sti = eksport.skriv_vtt(CUER, tmp_path / "a.vtt", "normalisert")
    assert eksport.valider_vtt(sti.read_text(encoding="utf-8")) == []
    assert eksport.valider_vtt("ikke vtt") != []
    assert eksport.valider_vtt("WEBVTT\n\n00:00:05.000 --> 00:00:01.000\ntekst\n") != []


def test_versjonen_i_vtt_hodet_er_pakkeversjonen(tmp_path):
    """VTT-hodet og `__version__` følger versjonen i pyproject.toml (1.0.0), ikke en hardkodet streng."""
    import re
    import arkivklarering
    pyproj = (pathlib.Path(__file__).resolve().parent.parent / "pyproject.toml").read_text(encoding="utf-8")
    assert arkivklarering.__version__ == re.search(r'^version = "([^"]+)"', pyproj, re.M).group(1) == "1.0.0"
    hode = eksport.skriv_vtt(CUER, tmp_path / "a.vtt", "ra").read_text(encoding="utf-8").splitlines()[0]
    assert hode == "WEBVTT - arkivklarering v1.0.0 - ra"


# ------------------------------------------------------------ OHMS
@pytest.mark.skipif(not OHMS_XSD.is_file(), reason=f"ohms.xsd finnes ikke ({OHMS_XSD}; ligger under ARKIVKLARERING_DATA/eval-data/ohms, eller sett ARKIVKLARERING_OHMS_XSD)")
def test_ohms_xml_er_gyldig_mot_xsd():
    xml = eksport.bygg_ohms_xml(POST, CUER, "lyd/sending.wav", 9.5)
    assert eksport.valider_ohms(xml) == []
    assert b"<userestrict>1</userestrict>" in xml and "utkast".encode() in xml


@pytest.mark.skipif(not OHMS_XSD.is_file(), reason=f"ohms.xsd finnes ikke ({OHMS_XSD}; ligger under ARKIVKLARERING_DATA/eval-data/ohms, eller sett ARKIVKLARERING_OHMS_XSD)")
def test_ohms_xml_ugyldig_avvises():
    from lxml import etree
    xml = eksport.bygg_ohms_xml(POST, CUER, "lyd/sending.wav", 9.5)
    ns = "{%s}" % eksport.OHMS_NS
    rot = etree.fromstring(xml)
    rec = rot.find(ns + "record")
    rec.remove(rec.find(ns + "title"))  # title er påkrevd
    assert eksport.valider_ohms(etree.tostring(rot)) != []
    rot = etree.fromstring(xml)
    rec = rot.find(ns + "record")
    rec.insert(0, rec.find(ns + "title"))  # rekkefølgen er en del av skjemaet
    assert eksport.valider_ohms(etree.tostring(rot)) != []


def test_ohms_mangler_skjema(tmp_path):
    with pytest.raises(FileNotFoundError):
        eksport.valider_ohms(b"<x/>", tmp_path / "finnes_ikke.xsd")


# ------------------------------------------------------------ IIIF
def _manifest():
    return eksport.bygg_iiif_manifest(POST, {"ra": CUER, "normalisert": CUER}, {"ra": "sending.ra.vtt", "normalisert": "sending.normalisert.vtt"},
                                      "https://example.org/lyd/sending.wav", 9.5)


def test_iiif_manifest_er_gyldig_og_bruker_supplementing():
    m = _manifest()
    assert eksport.valider_iiif(m) == []
    annotasjoner = [a for side in m["items"][0]["annotations"] for a in side["items"]]
    assert annotasjoner and all(a["motivation"] == "supplementing" for a in annotasjoner)
    assert any(a["body"].get("format") == "text/vtt" for a in annotasjoner)
    assert any(a["target"].endswith("#t=4.200,9.000") for a in annotasjoner)
    assert m["items"][0]["items"][0]["items"][0]["motivation"] == "painting"
    json.dumps(m)


def test_iiif_ugyldig_avvises():
    m = _manifest()
    m["type"] = "Collection"
    assert eksport.valider_iiif(m) != []


@pytest.mark.skipif(not IIIF_RECEPT.is_file(), reason=f"IIIF-oppskrift 0219 finnes ikke ({IIIF_RECEPT}; ligger under ARKIVKLARERING_DATA/eval-data/iiif)")
def test_iiif_validatoren_godtar_den_offisielle_oppskriften():
    t = IIIF_RECEPT.read_text(encoding="utf-8").replace("{{ id.url }}", "https://example.org/m/1/manifest").replace("{{ id.path }}", "https://example.org/m/1")
    assert eksport.valider_iiif(json.loads(t)) == []


# ------------------------------------------------------------ MMIF
def test_mmif_er_gyldig_og_har_dokument_og_visninger(tmp_path):
    lyd = tmp_path / "sending.wav"
    lyd.write_bytes(b"RIFF")
    m = eksport.bygg_mmif(str(lyd), TL, {"ra": CUER, "normalisert": CUER})
    s = m.serialize(pretty=True)
    assert eksport.valider_mmif(s) == []
    d = json.loads(s)
    assert d["documents"][0]["@type"].endswith("AudioDocument/v2") and len(d["views"]) == 3
    typer = {t for v in d["views"] for t in v["metadata"]["contains"]}
    assert any(t.endswith("TimeFrame/v6") for t in typer) and any("TextDocument" in t for t in typer) and any("Alignment" in t for t in typer)
    assert [a["properties"]["label"] for a in d["views"][0]["annotations"]] == ["speech", "music", "speech"]


def test_mmif_ugyldig_avvises():
    assert eksport.valider_mmif("{}") != []
    assert eksport.valider_mmif('{"metadata": {"mmif": "http://mmif.clams.ai/1.2.0"}, "documents": 5, "views": []}') != []
