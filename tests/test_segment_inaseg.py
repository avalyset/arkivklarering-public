import json
import pathlib
import sys

import pytest

from arkivklarering import segment, segment_inaseg

STUB = '''
import json, pathlib, sys
SVAR = [["noEnergy", 0.0, 0.4], ["female", 0.4, 2.0], ["male", 2.0, 3.0], ["music", 3.0, 5.0], ["noise", 5.0, 6.0]]
if sys.argv[1:] == ["--server"]:
    for linje in sys.stdin:
        lyd = json.loads(linje)["lyd"]
        if lyd.endswith("feil.wav"):
            print(json.dumps({"ok": False, "feil": "ValueError: ødelagt lyd"}), flush=True)
        else:
            print(json.dumps({"ok": True, "segmenter": SVAR}), flush=True)
else:
    jobb = json.loads(pathlib.Path(sys.argv[1]).read_text())
    assert jobb["vad_engine"] == "smn"
    for f in jobb["filer"]:
        pathlib.Path(f["ut"]).write_text(json.dumps({"segmenter": SVAR}))
'''


@pytest.fixture
def stub(tmp_path, monkeypatch):
    r = tmp_path / "stub_runner.py"
    r.write_text(STUB, encoding="utf-8")
    monkeypatch.setattr(segment_inaseg, "VENV_PYTHON", pathlib.Path(sys.executable))
    monkeypatch.setattr(segment_inaseg, "RUNNER", r)
    monkeypatch.setattr(segment_inaseg, "_SERVER", None)
    yield r
    segment_inaseg.lukk()


def test_etikettkart_og_sammenslaing_av_male_female():
    raa = [("noEnergy", 0, 0.4), ("female", 0.4, 2.0), ("male", 2.0, 3.0), ("music", 3.0, 5.0), ("noise", 5.0, 6.0), ("noEnergy", 6.0, 7.0)]
    assert segment_inaseg.kart_etiketter(raa) == [("other", 0, 0.4), ("speech", 0.4, 3.0), ("music", 3.0, 5.0), ("other", 5.0, 7.0)]


def test_speech_pluss_music_produseres_aldri():
    raa = [(e, i, i + 1) for i, e in enumerate(segment_inaseg.ETIKETTKART)]
    assert "speech+music" not in {e for e, _, _ in segment_inaseg.kart_etiketter(raa)}


def test_samme_etikett_med_gap_slas_ikke_sammen():
    assert segment_inaseg.kart_etiketter([("male", 0, 1), ("female", 1.5, 2)]) == [("speech", 0, 1), ("speech", 1.5, 2)]


def test_ukjent_etikett_beholdes_og_gar_til_menneskelig_vurdering():
    ut = segment_inaseg.kart_etiketter([("ny_klasse", 0, 2)])
    tl = segment.bygg_tidslinje(ut)
    assert tl[0].disposisjon == segment.MENNESKELIG_VURDERING and "ukjent etikett" in tl[0].merknad


def test_kartet_gir_tidslinje_etter_adr_0004():
    tl = segment.bygg_tidslinje(segment_inaseg.kart_etiketter(
        [("noEnergy", 0, 0.4), ("female", 0.4, 2.0), ("male", 2.0, 3.0), ("music", 3.0, 5.0), ("noise", 5.0, 6.0)]))
    assert [(s.label, s.disposisjon) for s in tl] == [("other", "ingen handling"), ("speech", "transkriber"), ("music", "foreslått klipp"),
                                                       ("other", "ingen handling")]
    assert all(not s.flagg for s in tl)  # ingen «musikk under tale»-flagg: kjøreren har ingen speech+music-klasse


def test_segmenter_via_vedvarende_runner(stub):
    a = segment_inaseg.segmenter("a.wav")
    b = segment_inaseg.segmenter("b.wav")
    assert a == b == [("other", 0.0, 0.4), ("speech", 0.4, 3.0), ("music", 3.0, 5.0), ("other", 5.0, 6.0)]
    assert segment_inaseg._SERVER is not None


def test_feil_fra_runner_gir_inasegfeil_og_serveren_lever(stub):
    with pytest.raises(segment_inaseg.InasegFeil, match="ødelagt lyd"):
        segment_inaseg.segmenter("feil.wav")
    assert segment_inaseg.segmenter("ok.wav")[1][0] == "speech"


def test_segmenter_flere_via_jobbfil(stub, tmp_path):
    ut = segment_inaseg.segmenter_flere([tmp_path / "a.wav", tmp_path / "b.wav"])
    assert len(ut) == 2 and ut[0] == ut[1] and ut[0][1] == ("speech", 0.4, 3.0)


def test_manglende_venv_gir_tydelig_feil(monkeypatch, tmp_path):
    monkeypatch.setattr(segment_inaseg, "VENV_PYTHON", tmp_path / "finnes_ikke")
    monkeypatch.setattr(segment_inaseg, "_SERVER", None)
    with pytest.raises(segment_inaseg.InasegFeil, match="venv-inaseg"):
        segment_inaseg.segmenter("a.wav")
    with pytest.raises(segment_inaseg.InasegFeil, match="venv-inaseg"):
        segment_inaseg.segmenter_flere(["a.wav"])


def test_segment_segmenter_velger_inaseg_med_miljovariabel(monkeypatch):
    kall = []
    monkeypatch.setenv("ARKIVKLARERING_SEGMENTERING", "inaseg")
    monkeypatch.setattr(segment_inaseg, "segmenter", lambda lyd, enhet="cpu": kall.append((lyd, enhet)) or [("speech", 0.0, 1.0)])
    assert segment.segmenter("x.wav", "cpu") == [("speech", 0.0, 1.0)] and kall == [("x.wav", "cpu")]


def _sperr_inavamos(monkeypatch, nadd):
    """Samme builtins.__import__-sperre som før: importen av inavamos registreres og avvises (inaVAMOS kjøres aldri i testene)."""
    import builtins
    ekte = builtins.__import__

    def sperr(navn, *a, **k):
        if navn == "inavamos" or navn.startswith("inavamos."):
            nadd.append(navn)
            raise ModuleNotFoundError("No module named 'inavamos'", name="inavamos")  # som når tillegget ikke er installert
        return ekte(navn, *a, **k)
    monkeypatch.setattr(builtins, "__import__", sperr)


@pytest.mark.parametrize("verdi", [None, "", "  ", "inaseg"])
def test_standard_er_inaseg_og_inavamos_importeres_ikke(monkeypatch, verdi):
    if verdi is None:
        monkeypatch.delenv("ARKIVKLARERING_SEGMENTERING", raising=False)
    else:
        monkeypatch.setenv("ARKIVKLARERING_SEGMENTERING", verdi)
    kall, nadd = [], []
    monkeypatch.setattr(segment_inaseg, "segmenter", lambda lyd, enhet="cpu": kall.append((lyd, enhet)) or [("speech", 0.0, 1.0)])
    monkeypatch.delitem(sys.modules, "inavamos", raising=False)
    _sperr_inavamos(monkeypatch, nadd)
    assert segment.valgt_segmentering() == "inaseg"
    assert segment.segmenter("x.wav") == [("speech", 0.0, 1.0)] and kall == [("x.wav", "cpu")]
    assert nadd == [] and "inavamos" not in sys.modules


def test_inavamos_uten_installert_tillegg_gir_feil_med_installasjon_og_lisens(monkeypatch):
    monkeypatch.setenv("ARKIVKLARERING_SEGMENTERING", "inavamos")
    monkeypatch.setattr(segment_inaseg, "segmenter", lambda *a, **k: pytest.fail("inaseg skal ikke velges når inavamos er valgt"))
    monkeypatch.delitem(sys.modules, "inavamos", raising=False)
    nadd = []
    _sperr_inavamos(monkeypatch, nadd)
    with pytest.raises(segment.SegmenteringFeil) as e:
        segment.segmenter("x.wav")
    assert nadd == ["inavamos"]  # importen nås bare når inavamos er valgt
    for ord_ in ("reproduksjon-h1h2", "Pantagruel", "art. 3", "kommersiell", "forskning", "H1 og H2"):
        assert ord_ in str(e.value), ord_


def test_inavamos_med_manglende_avhengighet_viser_den_ekte_feilen(monkeypatch):
    monkeypatch.setenv("ARKIVKLARERING_SEGMENTERING", "inavamos")
    monkeypatch.delitem(sys.modules, "inavamos", raising=False)
    import builtins
    ekte = builtins.__import__

    def sperr(navn, *a, **k):
        if navn == "inavamos":
            raise ModuleNotFoundError("No module named 'torch'", name="torch")  # inaVAMOS finnes, torch mangler
        return ekte(navn, *a, **k)
    monkeypatch.setattr(builtins, "__import__", sperr)
    with pytest.raises(ModuleNotFoundError, match="torch"):
        segment.segmenter("x.wav")


@pytest.mark.parametrize("verdi", ["inaVAMOS", "INASEG", "whisper", "inavamos,inaseg"])
def test_ukjent_verdi_gir_tydelig_feil(monkeypatch, verdi):
    monkeypatch.setenv("ARKIVKLARERING_SEGMENTERING", verdi)
    monkeypatch.setattr(segment_inaseg, "segmenter", lambda *a, **k: pytest.fail("ukjent verdi skal ikke kjøre noen segmentør"))
    nadd = []
    _sperr_inavamos(monkeypatch, nadd)
    with pytest.raises(segment.SegmenteringFeil, match="ukjent verdi") as e:
        segment.segmenter("x.wav")
    assert repr(verdi) in str(e.value) and "inaseg" in str(e.value) and "inavamos" in str(e.value) and nadd == []


def test_cli_gir_feilkode_2_for_ukjent_segmentering_for_noe_kjores(monkeypatch, tmp_path, capsys):
    from arkivklarering import cli, miljo
    monkeypatch.setattr(miljo, "krev_vault_miljo", lambda: None)
    monkeypatch.setenv("ARKIVKLARERING_SEGMENTERING", "feil")
    monkeypatch.setattr(segment, "segmenter", lambda *a, **k: pytest.fail("segmentering skal ikke starte"))
    lyd = tmp_path / "a.wav"
    lyd.write_bytes(b"")
    assert cli.main([str(lyd), "-o", str(tmp_path / "ut")]) == 2
    assert "ukjent verdi" in capsys.readouterr().err


@pytest.mark.tung
def test_ekte_runner_pa_rokytest():
    kandidater = [pathlib.Path(__file__).resolve().parent.parent / "lyd" / "rokytest.wav", pathlib.Path.home() / "dev/arkivklarering/lyd/rokytest.wav"]
    lyd = next((k for k in kandidater if k.is_file()), None)
    if lyd is None:
        pytest.skip("lyd/rokytest.wav finnes ikke (ligger utenfor git)")
    r = segment_inaseg.segmenter(lyd)
    segment_inaseg.lukk()
    assert r and {e for e, _, _ in r} <= {"speech", "music", "other"}
    assert r[0][1] == 0.0 and r[-1][2] > 1.0


def test_logg_har_en_linje_per_kall_og_sammendrag_uten_inavamos(stub, tmp_path, monkeypatch):
    logg = tmp_path / "seg.jsonl"
    monkeypatch.setenv(segment_inaseg.LOGG_MILJOVARIABEL, str(logg))
    monkeypatch.setitem(segment_inaseg._KALL, "antall", 0)
    segment_inaseg.segmenter("a.wav")
    segment_inaseg.segmenter_flere(["b.wav", "c.wav"])
    segment_inaseg._sammendrag()
    linjer = [json.loads(l) for l in logg.read_text().splitlines()]
    assert [l.get("lyd", "").rsplit("/", 1)[-1] for l in linjer[:3]] == ["a.wav", "b.wav", "c.wav"]
    assert linjer[3] == {**linjer[3], "sammendrag": True, "antall_kall": 3, "inavamos_importert": False, "kjorer": "inaSpeechSegmenter 0.8.0"}
