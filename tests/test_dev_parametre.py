"""Parametrene som er lagt til i DEV-skriptene (--per-dialekt, --ut-mappe, --etikett, --eval-nr) og intervallskriptet. Ingen Whisper, ingen testdel."""
import importlib.util
import json
import pathlib
import random
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DEV = REPO / "eval" / "dev"
sys.path.insert(0, str(REPO / "scripts"))


def last(navn, sti):
    spec = importlib.util.spec_from_file_location(navn, sti)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(DEV))
    sys.modules[navn] = m
    spec.loader.exec_module(m)
    return m


def lag_metadata(tmp_path, antall):
    rader = []
    for d, n in antall.items():
        for i in range(n):
            rader.append({"overlap_previous": False, "overlap_next": False, "duration": 3.0, "orthographic": "a b c d", "dialect": d,
                          "source_file_id": f"nb-{i % 4}", "segment_id": f"{i:07d}-{i + 1:07d}"})
    (tmp_path / "validation_metadata.jsonl").write_text("\n".join(json.dumps(r) for r in rader) + "\n", encoding="utf-8")


def test_per_dialekt_standard_gir_samme_trekk_som_for(tmp_path):
    kd = last("kjor_dev_t1", DEV / "kjor_dev.py")
    lag_metadata(tmp_path, {d: 40 for d in kd.DIALEKTER})
    kd.DATA, kd.SPLITT = tmp_path, "validation"
    assert kd.PER_DIALEKT == 12
    valg, _ = kd.trekk_utvalg()
    rader = [json.loads(l) for l in open(tmp_path / "validation_metadata.jsonl", encoding="utf-8")]
    rng, forventet = random.Random(kd.SEED), []
    for d in kd.DIALEKTER:  # den gamle logikken, ordrett
        pool = sorted((r for r in rader if r["dialect"] == d), key=lambda r: (r["source_file_id"], r["segment_id"]))
        forventet += rng.sample(pool, 12)
    assert valg == forventet and len(valg) == 60


def test_per_dialekt_60_tar_alle_i_omrader_med_faerre(tmp_path):
    kd = last("kjor_dev_t2", DEV / "kjor_dev.py")
    lag_metadata(tmp_path, {"e": 100, "n": 80, "sw": 5, "t": 60, "w": 61})
    kd.DATA, kd.SPLITT, kd.PER_DIALEKT = tmp_path, "validation", 60
    valg, _ = kd.trekk_utvalg()
    per = {d: sum(1 for r in valg if r["dialect"] == d) for d in kd.DIALEKTER}
    assert per == {"e": 60, "n": 60, "sw": 5, "t": 60, "w": 60}


def test_alle_tre_skript_har_de_nye_parametrene_med_dev_som_standard():
    for s in ("kjor_dev.py", "kjor_flaggoverlevelse_ord.py", "kjor_personvern_dev.py"):
        t = (DEV / s).read_text(encoding="utf-8")
        for flagg in ("--ut-mappe", "--etikett", "--eval-nr"):
            assert flagg in t, (s, flagg)
        assert 'default="DEV"' in t and "TEST – preregistrert (OSF hc83q)" in t


def test_wilson_og_persentil():
    import rapporter_intervaller as ri
    assert ri.wilson(0, 0) == (None, None)
    assert ri.wilson(5, 10) == (0.237, 0.763)
    assert ri.persentil(list(range(2000))) == (50, 1949)  # int(0,025·2000) = 50, int(0,975·2000) − 1 = 1949


def test_wer_clusterbootstrap_pa_dev_er_deterministisk_og_gir_samme_wer():
    import rapporter_intervaller as ri
    res = json.loads(sorted(REPO.glob("eval/dev/KLAR-EVAL-0002_*v1.1_*.json"))[-1].read_text(encoding="utf-8"))
    utv = json.loads(sorted(REPO.glob("eval/dev/KLAR-EVAL-0003_*.json"))[-1].read_text(encoding="utf-8"))["utvalg"]
    a, k1a = ri.wer_intervaller(res, utv, b=300)
    b, k1b = ri.wer_intervaller(res, utv, b=300)
    assert a == b and k1a == k1b  # fast seed
    for (kol, g), v in a.items():
        assert v["ki95"][0] <= v["wer"] <= v["ki95"][1], (kol, g)
        if g == "totalt":
            assert abs(v["wer"] - res["wer"][kol]["totalt"]) < 5e-5
    assert a[("ra/matchet", "totalt")]["n_talere"] == 33 and k1a["utelukker_0"] is True


def _setninger():
    rng = random.Random(7)
    rader = []
    for config in ("bokmaal", "nynorsk"):
        for i in range(200):
            g = rng.randint(0, 3)
            go = rng.randint(0, g)
            p = rng.randint(0, 3)
            po = rng.randint(0, p)
            rader.append([config, i, str(i), "original", "kombinert", "person", g, go, go, p, po, po])
    return {"kolonner": ["config", "rad", "idx", "variant", "motor", "type", "gull", "gull_overlapp", "gull_noyaktig", "pred", "pred_overlapp", "pred_noyaktig"], "rader": rader}


def test_norne_bootstrap_over_setninger_er_deterministisk_og_punktestimatet_er_summen():
    import rapporter_intervaller as ri
    s = _setninger()
    a, b = ri.norne_bootstrap(s, b=300), ri.norne_bootstrap(s, b=300)
    assert a == b  # fast seed
    for sprak, config in (("nb", "bokmaal"), ("nn", "nynorsk")):
        rs = [r for r in s["rader"] if r[0] == config]
        v = a[(sprak, "person", "kombinert", "original")]
        assert v["n_setninger"] == 200
        assert abs(v["recall"][0] - sum(r[7] for r in rs) / sum(r[6] for r in rs)) < 1e-12
        assert abs(v["presisjon"][0] - sum(r[10] for r in rs) / sum(r[9] for r in rs)) < 1e-12
        assert v["recall"][1] <= v["recall"][0] <= v["recall"][2] and v["presisjon"][1] <= v["presisjon"][0] <= v["presisjon"][2]


def test_personvern_skriptet_skriver_tellere_per_setning_og_aggregatene_er_summen():
    t = (DEV / "kjor_personvern_dev.py").read_text(encoding="utf-8")
    assert "per_setning.append(" in t and ".setninger.json" in t
    assert "for k, v in d.items():\n                            c[k] += v" in t  # aggregatene summeres fra de samme tallene som skrives per setning
