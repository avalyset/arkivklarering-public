"""scripts/ground_truth.py leser WER bare fra resultatfiler; utvalgs- og metafiler (…utvalg.json, …_kjoring_meta.json) hoppes over uten leseadvarsel."""
import importlib.util
import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent


def last_gt():
    spec = importlib.util.spec_from_file_location("ground_truth", REPO / "scripts" / "ground_truth.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_utvalgs_og_metafiler_gir_ingen_leseadvarsel(tmp_path, monkeypatch):
    gt = last_gt()
    d = tmp_path / "eval" / "test"
    d.mkdir(parents=True)
    stamme = "KLAR-EVAL-0099_arkivklarering_test-nbsamtale-wer_v1.0_2026-10-27"
    (d / f"{stamme}.json").write_text(json.dumps({"merknad": "x", "wer": {"ra/matchet": {"totalt": 0.1275}}}), encoding="utf-8")
    (d / f"{stamme}.utvalg.json").write_text(json.dumps({"utvalg": []}), encoding="utf-8")
    (d / f"{stamme}_kjoring_meta.json").write_text(json.dumps({"del": "H1"}), encoding="utf-8")
    (tmp_path / "docs").mkdir()
    monkeypatch.setattr(gt, "REPO", tmp_path)
    monkeypatch.setattr(gt, "DOCS", tmp_path / "docs")
    ut = gt.seksjon_eval()
    assert not any("kunne ikke leses" in l for l in ut)
    assert len([l for l in ut if "korpus-WER totalt" in l]) == 1  # bare resultatfila gir en WER-linje


def test_resultatfil_som_mangler_wer_gir_fortsatt_advarsel(tmp_path, monkeypatch):
    gt = last_gt()
    d = tmp_path / "eval"
    d.mkdir()
    (d / "KLAR-EVAL-0098_arkivklarering_test-nbsamtale-wer_v1.0_2026-10-27.json").write_text("{}", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    monkeypatch.setattr(gt, "REPO", tmp_path)
    monkeypatch.setattr(gt, "DOCS", tmp_path / "docs")
    assert any("kunne ikke leses" in l for l in gt.seksjon_eval())


def test_dokumentlista_viser_ikke_forrige_gt_men_denne_fila(tmp_path, monkeypatch):
    gt = last_gt()
    d = tmp_path / "docs"
    d.mkdir()
    (d / "KLAR-GT-0001_arkivklarering_ground-truth_v1.1_2026-10-28.md").write_text("x", encoding="utf-8")
    (d / "KLAR-ARK-0001_arkivklarering_arkitektur_v1.0_2026-10-28.md").write_text("x", encoding="utf-8")
    (tmp_path / "eval").mkdir()
    monkeypatch.setattr(gt, "REPO", tmp_path)
    monkeypatch.setattr(gt, "DOCS", d)
    ut = gt.seksjon_dokumenter()
    assert not any("ground-truth_v1.1" in l for l in ut)
    assert any(l.startswith("- KLAR-GT-0001: denne fila") for l in ut) and any("ARK-0001" in l for l in ut)
