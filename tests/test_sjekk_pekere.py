import importlib.util
import os
import pathlib
import subprocess

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("sjekk_pekere", REPO / "scripts" / "sjekk_pekere.py")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)

pytestmark = pytest.mark.skipif(not (REPO / ".git").exists(), reason="krever git-repoet")
IDENTITET = {"GIT_AUTHOR_NAME": "Eirik Botten Nicolaysen", "GIT_AUTHOR_EMAIL": "eirik@ecodeco.no",
             "GIT_COMMITTER_NAME": "Eirik Botten Nicolaysen", "GIT_COMMITTER_EMAIL": "eirik@ecodeco.no"}


def tøm_cacher():
    for f in (sp.tre, sp.historikk, sp.har_historikk, sp.indeks, sp.linjer):
        f.cache_clear()


def git(r, *a):
    return subprocess.run(["git", *a], cwd=r, check=True, capture_output=True, text=True, env={**os.environ, **IDENTITET}).stdout


def test_ingen_brudd_i_repoet():
    tøm_cacher()
    assert sp.sjekk() == []


@pytest.fixture
def lite_repo(tmp_path, monkeypatch):
    r = tmp_path / "r"
    (r / "docs").mkdir(parents=True)
    git(r, "init", "-q", "-b", "main")
    gammel = r / "docs" / "KLAR-ARK-0001_x_arkitektur_v1.0_2026-10-26.md"
    gammel.write_text("# A\n\nlinje 3\nlinje 4\n")
    git(r, "add", "-A"); git(r, "commit", "-q", "-m", "v1.0")
    git(r, "mv", str(gammel), str(r / "docs" / "KLAR-ARK-0001_x_arkitektur_v1.1_2026-10-27.md"))
    git(r, "commit", "-q", "-m", "v1.1")
    monkeypatch.setattr(sp, "REPO", r)
    monkeypatch.setattr(sp, "BUNDLE_COMMIT", git(r, "rev-parse", "HEAD~1").strip())  # «privat historikk» = første commit
    tøm_cacher()
    yield r
    tøm_cacher()


def skriv(r, tekst):
    (r / "docs" / "KLAR-ARK-0005_x_datablad_v1.0_2026-10-27.md").write_text(tekst)
    git(r, "add", "-A")


def test_peker_til_versjon_i_historikken_maa_merkes(lite_repo):
    skriv(lite_repo, "# B\n\nSe KLAR-ARK-0001 v1.0:3.\n")
    assert [b.split(": ", 1)[1] for b in sp.sjekk()] == ["ikke i treet og ikke merket (i git-historikken): KLAR-ARK-0001 v1.0"]
    tøm_cacher()
    skriv(lite_repo, "# B\n\nSe KLAR-ARK-0001 v1.0:3 (i git-historikken). Gjeldende er KLAR-ARK-0001 v1.1:4.\n")
    assert sp.sjekk() == []


def test_skrivefeil_og_linje_som_ikke_finnes(lite_repo):
    skriv(lite_repo, "# B\n\nSe KLAR-ARK-0001 v1.7 (i git-historikken). Og KLAR-ARK-0001 v1.1:9.\n")
    b = [x.split(": ", 1)[1] for x in sp.sjekk()]
    assert b[0] == "finnes verken i treet eller i git-historikken: KLAR-ARK-0001 v1.7"
    assert b[1].startswith("linje 9 finnes ikke i docs/KLAR-ARK-0001_x_arkitektur_v1.1_2026-10-27.md (5 linjer)")


def test_versjonsnotat_og_kodeblokk_er_unntatt(lite_repo):
    skriv(lite_repo, "# B\n\nVersjon 1.0, 2026-10-27 (v1.0: bygger på KLAR-ARK-0001 v1.0).\n\n```\nKLAR-ARK-0001 v1.0\n```\n\n## C\n")
    assert sp.sjekk() == []


def test_uten_den_private_historikken_proves_bare_merking_og_linjer_i_treet(lite_repo, monkeypatch):
    """Som i det offentlige repoet: egne commits, men ikke bundle-commiten. Merkede henvisninger godtas, umerkede er fortsatt brudd."""
    monkeypatch.setattr(sp, "BUNDLE_COMMIT", "0" * 40)
    tøm_cacher()
    skriv(lite_repo, "# B\n\nSe KLAR-ARK-0001 v1.7:99 (i git-historikken). Gjeldende er KLAR-ARK-0001 v1.1:4.\n")
    assert sp.har_historikk() is False and sp.sjekk() == []
    tøm_cacher()
    skriv(lite_repo, "# B\n\nSe KLAR-ARK-0001 v1.0:3.\n")
    assert [b.split(": ", 1)[1] for b in sp.sjekk()] == ["ikke i treet og ikke merket (i git-historikken): KLAR-ARK-0001 v1.0"]


def test_det_private_repoet_har_bundle_commiten():
    tøm_cacher()
    assert sp.har_historikk() is True
