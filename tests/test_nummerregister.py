import importlib.util
import pathlib

import pytest

SKRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "ground_truth.py"


@pytest.fixture
def gt(tmp_path):
    spec = importlib.util.spec_from_file_location("ground_truth_test", SKRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    (tmp_path / "docs").mkdir()
    (tmp_path / "eval").mkdir()
    m.REPO, m.DOCS = tmp_path, tmp_path / "docs"
    for n, slug in (("0001", "arkitektur"), ("0002", "navnekonvensjon")):  # grunnlaget som alle tilstander forutsetter
        (m.DOCS / f"KLAR-ARK-{n}_arkivklarering_{slug}_v1.0_2026-10-26.md").write_text("x")
    return m


def _fil(gt, navn):
    (gt.DOCS / navn).write_text("x")


def _reg(gt, *rader):
    rader = (("KLAR-ARK-0001", "arkitektur", "i bruk"), ("KLAR-ARK-0002", "navnekonvensjon", "i bruk"),
             ("KLAR-ARK-0003", "nummerregister", "i bruk")) + rader  # registerfila selv ligger på disk og må stå i registeret
    tab = "| nøkkel | slug | status | sted | brukt av |\n|---|---|---|---|---|\n" + "\n".join(
        f"| {n} | {s} | {st} | `docs/` | x |" for n, s, st in rader)
    (gt.DOCS / "KLAR-ARK-0003_arkivklarering_nummerregister_v1.0_2026-10-26.md").write_text(tab)


def test_ren_tilstand_gir_ingen_varsler(gt):
    _fil(gt, "KLAR-ADR-0001_arkivklarering_a_v1.0_2026-10-26.md")
    _fil(gt, "KLAR-ADR-0001_arkivklarering_a_v1.1_2026-10-27.md")  # ny versjon, samme slug
    _reg(gt, ("KLAR-ADR-0001", "a", "i bruk"))
    assert gt.nummerregister()[1] == []


def test_dobbel_bruk_to_slugger_samme_nummer(gt):
    _fil(gt, "KLAR-ADR-0001_arkivklarering_a_v1.0_2026-10-26.md")
    _fil(gt, "KLAR-ADR-0001_arkivklarering_b_v1.0_2026-10-26.md")
    _reg(gt, ("KLAR-ADR-0001", "a", "i bruk"))
    assert any("DOBBEL BRUK" in v for v in gt.nummerregister()[1])


def test_hull(gt):
    _fil(gt, "KLAR-ADR-0001_arkivklarering_a_v1.0_2026-10-26.md")
    _fil(gt, "KLAR-ADR-0003_arkivklarering_c_v1.0_2026-10-26.md")
    _reg(gt, ("KLAR-ADR-0001", "a", "i bruk"), ("KLAR-ADR-0003", "c", "i bruk"))
    assert any(v.startswith("HULL") and "0002" in v for v in gt.nummerregister()[1])


def test_reservert_teller_ikke_som_hull(gt):
    _fil(gt, "KLAR-ADR-0001_arkivklarering_a_v1.0_2026-10-26.md")
    _reg(gt, ("KLAR-ADR-0001", "a", "i bruk"), ("KLAR-ADR-0002", "r", "reservert"), ("KLAR-ADR-0003", "c", "reservert"))
    assert gt.nummerregister()[1] == []


def test_ikke_i_registeret_og_registrert_men_mangler(gt):
    _fil(gt, "KLAR-ADR-0001_arkivklarering_a_v1.0_2026-10-26.md")
    _reg(gt, ("KLAR-ADR-0002", "b", "i bruk"))
    v = gt.nummerregister()[1]
    assert any("IKKE I REGISTERET" in x for x in v) and any("MEN IKKE PÅ DISK" in x for x in v)


def test_reservert_men_i_bruk_og_slug_avviker(gt):
    _fil(gt, "KLAR-ADR-0001_arkivklarering_a_v1.0_2026-10-26.md")
    _reg(gt, ("KLAR-ADR-0001", "annen", "reservert"))
    v = gt.nummerregister()[1]
    assert any("RESERVERT, MEN I BRUK" in x for x in v) and any("SLUG AVVIKER" in x for x in v)


def test_ots_filer_telles_ikke(gt):
    _fil(gt, "KLAR-ADR-0001_arkivklarering_a_v1.0_2026-10-26.md")
    _fil(gt, "KLAR-ADR-0001_arkivklarering_a_v1.0_2026-10-26.md.abc123def456.ots")
    _reg(gt, ("KLAR-ADR-0001", "a", "i bruk"))
    assert gt.nummerregister()[1] == []


def test_manglende_register(gt):
    _fil(gt, "KLAR-ADR-0001_arkivklarering_a_v1.0_2026-10-26.md")
    assert any("REGISTER MANGLER" in x for x in gt.nummerregister()[1])
