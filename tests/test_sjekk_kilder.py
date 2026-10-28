import importlib.util
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("sjekk_kilder", REPO / "scripts" / "sjekk_kilder.py")
sk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sk)


def test_normaliser_bare_mellomrom_og_linjeskift():
    assert sk.normaliser("a  b\n\n c\t d e") == "a b c d e"
    assert sk.normaliser("Å—ø") == "Å—ø"  # ingen andre tegn endres


def test_sitat_med_utelatelser_i_rekkefolge():
    t = sk.normaliser("Først kommer A. Så kommer B og C. Til slutt D.")
    assert sk.finn_sitat(t, "Først kommer A. […] Til slutt D.")
    assert sk.finn_sitat(t, "Så kommer B […] D.")
    assert not sk.finn_sitat(t, "Til slutt D. […] Først kommer A.")  # feil rekkefølge
    assert not sk.finn_sitat(t, "Først kommer a.")  # forskjellig bokstavstørrelse
    assert not sk.finn_sitat(t, "")


def test_html_til_tekst_skiller_blokker_og_beholder_inline(tmp_path):
    f = tmp_path / "s.html"
    f.write_text("<html><head><style>x{}</style></head><body><p>Hei <em>verden</em>, her.</p><p>Neste</p><script>var a=1;</script></body></html>", encoding="utf-8")
    t = sk.normaliser(sk.tekst_fra_kopi(f))
    assert t == "Hei verden, her. Neste"


REG = """# KLAR-KILDE-0001: test

## Kilder

| nøkkel | URL | type | hentet | fil | sha256 | sider |
|---|---|---|---|---|---|---|
| K01 | https://example.org/a | primær | 2026-10-26 | `a.txt` (test) | `{sha}` | – |

## Påstander

| påstand-id | påstand ordrett | dokument:linje | kilde-URL | kildetype | hentet | kilde | sitat (side/avsnitt) | tolkning | status |
|---|---|---|---|---|---|---|---|---|---|
| T-01 | p | d.md:1 | https://example.org/a | primær | 2026-10-26 | K01 | «Først kommer A.» (rå fil) | | verifisert |
| T-02 | p | d.md:2 | https://example.org/a | primær | 2026-10-26 | K01 | «Finnes ikke i kilden.» (rå fil) | | verifisert |
| T-03 | p | d.md:3 | – | primær | 2026-10-26 | – | – | ingen kilde | ikke funnet |
"""


def _lag(tmp_path, monkeypatch):
    k = tmp_path / "kilder"
    k.mkdir()
    (k / "a.txt").write_text("Først kommer A.\nSå B.", encoding="utf-8")
    reg = tmp_path / "reg.md"
    reg.write_text(REG.format(sha=sk.sha256_fil(k / "a.txt")), encoding="utf-8")
    monkeypatch.setattr(sk, "KILDER", k)
    return reg, k


def test_kontroller_finner_sitat_som_ikke_er_delstreng(tmp_path, monkeypatch):
    reg, _ = _lag(tmp_path, monkeypatch)
    telling, brudd = sk.kontroller(reg)
    assert telling == {"verifisert": 1, "sitat ikke funnet": 1, "ikke funnet": 1}
    assert [b["id"] for b in brudd] == ["T-02"]


def test_kontroller_avviser_endret_kopi(tmp_path, monkeypatch):
    reg, k = _lag(tmp_path, monkeypatch)
    (k / "a.txt").write_text("Først kommer A. Endret.", encoding="utf-8")
    telling, brudd = sk.kontroller(reg)
    assert "sha256" in brudd[0]["grunn"] and telling.get("verifisert", 0) == 0


def test_urler_uten_rad(tmp_path, monkeypatch):
    reg, _ = _lag(tmp_path, monkeypatch)
    d = tmp_path / "KLAR-ARK-9999_x.md"
    d.write_text("Se https://example.org/a og http://example.org/a/ og https://ukjent.example/side og <https://x.org/<ord>>.\nOSF https://osf.io/abcde/.", encoding="utf-8")
    monkeypatch.setattr(sk, "REPO", tmp_path)
    ut = sk.urler_uten_rad([d], reg)
    assert [u for _, u in ut] == ["https://ukjent.example/side"]


def test_kopier_i_undermapper_og_ikke_utenfor_kildemappen(tmp_path, monkeypatch):
    k = tmp_path / "kilder"
    (k / "pyannote_hf" / "a__b").mkdir(parents=True)
    f = k / "pyannote_hf" / "a__b" / "README.md"
    f.write_text("---\nlicense: mit\n---\n", encoding="utf-8")
    monkeypatch.setattr(sk, "KILDER", k)
    reg = tmp_path / "reg.md"
    reg.write_text(REG.format(sha=sk.sha256_fil(f)).replace("`a.txt` (test)", "`pyannote_hf/a__b/README.md` (test)")
                   .replace("«Først kommer A.»", "«license: mit»").replace("«Finnes ikke i kilden.»", "«license: mit»"), encoding="utf-8")
    telling, brudd = sk.kontroller(reg)
    assert telling.get("verifisert") == 2 and not brudd
    reg.write_text(reg.read_text(encoding="utf-8").replace("`pyannote_hf/a__b/README.md`", "`../utenfor.txt`"), encoding="utf-8")
    telling, brudd = sk.kontroller(reg)
    assert any("utenfor kildemappen" in b["grunn"] for b in brudd)


def test_registerfil_velger_nyeste_versjon_etter_versjonsnummer(tmp_path):
    for v in ("1.0", "1.7", "1.9", "1.10"):
        (tmp_path / f"KLAR-KILDE-0001_arkivklarering_kilderegister_v{v}_2026-10-27.md").write_text("x\n", encoding="utf-8")
    assert sk.registerfil(tmp_path).name == "KLAR-KILDE-0001_arkivklarering_kilderegister_v1.10_2026-10-27.md"  # ikke v1.9 (leksikografisk)
