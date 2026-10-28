"""scripts/kjor_testdel.sh: kjører ikke på urent arbeidstre; skriver kjoring_meta ved siden av resultatet; committer, pusher og speiler etter HVER
testdel før neste starter; stopper på feil og på endrede sporede filer. Testdelene kjøres ikke her: skriptene er stubber i et midlertidig repo
med et lokalt bart repo som origin og en stubb for speil."""
import json
import os
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
STUBB = '''import os, pathlib, sys
navn = pathlib.Path(sys.argv[0]).stem
with open("kjort.log", "a") as f:
    f.write(navn + " " + " ".join(sys.argv[1:]) + "\\n")
with open("segmentering.log", "a") as f:
    f.write(navn + " " + os.environ.get("ARKIVKLARERING_SEGMENTERING", "-") + "\\n")
if os.environ.get("STUBB_OVERSKRIV") == navn:
    pathlib.Path("docs/sporet.md").write_text("endret av kjøringen")
pathlib.Path("docs/KLAR-EVAL-" + navn + "_v1.0_2026-10-27.json").write_text("{}")
sys.exit(3 if os.environ.get("STUBB_FEIL") == navn else 0)
'''
SKRIPT = ["eval/dev/kjor_dev.py", "eval/dev/kjor_flaggoverlevelse_ord.py", "eval/dev/kjor_personvern_dev.py", "kalibrering/kjor_h4.py"]


def git(r, *a):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=r, check=True, capture_output=True, text=True).stdout.strip()


def lag_repo(tmp_path):
    r = tmp_path / "repo"
    for d in ("scripts", "docs", "kalibrering", "eval/dev"):
        (r / d).mkdir(parents=True)
    shutil.copy(REPO / "scripts" / "kjor_testdel.sh", r / "scripts")
    for s in SKRIPT:
        (r / s).write_text(STUBB)
    (r / "scripts" / "speil_stubb.sh").write_text('echo "speil $(git rev-parse --short HEAD) $(git status --porcelain | wc -l | tr -d " ")" >> "$(dirname "$0")/../speil.log"\n')
    (r / ".gitignore").write_text("kjort.log\nspeil.log\nsegmentering.log\n")
    (r / "kalibrering" / "KLAR-MANUS-0002_stubb_v1.2_2026-10-26.tsv").write_text("x\n")
    (r / "docs" / "KLAR-PREREG-0001_stubb_v1.9_2026-10-27.md").write_text("a\n")
    (r / "docs" / "KLAR-PREREG-0001_stubb_v1.10_2026-10-27.md").write_text("b\n")
    (r / "docs" / "sporet.md").write_text("opprinnelig")
    git(r, "init", "-q", "-b", "main")
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "x")
    git(r, "tag", "prereg-v1")
    git(r, "tag", "h4-script-v2")
    git(r, "tag", "testkjoring-v1")
    git(r, "tag", "testkjoring-v2")
    git(r, "tag", "testkjoring-v3")
    git(r, "tag", "testkjoring-v4")
    git(r, "tag", "testkjoring-v5")
    git(r, "tag", "testkjoring-v6")
    git(r, "tag", "testkjoring-v7")
    git(r, "tag", "testkjoring-v8")
    git(r, "tag", "testkjoring-v9")
    git(r, "tag", "testkjoring-v10")
    bart = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(bart)], check=True)
    git(r, "remote", "add", "origin", str(bart))
    return r, bart


def kjor(r, *args, **env):
    return subprocess.run(["bash", "scripts/kjor_testdel.sh", *args], cwd=r, capture_output=True, text=True,
                          env={**os.environ, "KLAR_PY": sys.executable, "KLAR_SPEIL": "scripts/speil_stubb.sh", **env})


def kjort(r):
    f = r / "kjort.log"
    return f.read_text().splitlines() if f.exists() else []


def test_urent_arbeidstre_kjorer_ikke(tmp_path):
    r, _ = lag_repo(tmp_path)
    (r / "uspor.txt").write_text("x")
    p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
    assert p.returncode == 1 and "uspor.txt" in p.stderr
    assert kjort(r) == [] and not list((r / "docs").glob("*kjoring_meta*"))
    (r / "uspor.txt").unlink()
    (r / "docs" / "sporet.md").write_text("endret")  # sporet fil endret
    assert kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001").returncode == 1 and kjort(r) == []


def test_tor_kjorer_ikke_og_skriver_ingenting(tmp_path):
    r, _ = lag_repo(tmp_path)
    p = kjor(r, "--tor", "alle", "--prereg-id", "KLAR-PREREG-0001")
    assert p.returncode == 0 and p.stdout.count("ville kjørt") == 4 and "--mal-person 300 --mal-sted 200 --maks-timer 4" in p.stdout
    assert kjort(r) == [] and git(r, "status", "--porcelain") == ""


def test_en_del_committer_pusher_og_speiler_med_meta_ved_siden_av_resultatet(tmp_path):
    r, bart = lag_repo(tmp_path)
    start = git(r, "rev-parse", "HEAD")
    p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
    assert p.returncode == 0, p.stderr
    assert kjort(r) == ["kjor_h4 --prereg-id KLAR-PREREG-0001 --opptak /Volumes/Vault/arkivklarering/lyd/h4"]
    d = json.loads((r / "docs" / "KLAR-EVAL-kjor_h4_v1.0_2026-10-27_kjoring_meta.json").read_text())
    assert d["commit"] == start and d["git_status_porcelain_ved_start"] == [] and d["returkode"] == 0 and d["del"] == "H4"
    assert d["tag_testkjoring"] == {"navn": "testkjoring-v10", "commit": start} and d["tag_testkjoring_v1"] == start and d["kode_uendret_siden_tagg"] is True
    assert d["tag_prereg_v1"] == start == d["tag_h4_script_v2"] and d["preregistrering"]["fil"].endswith("_v1.10_2026-10-27.md")  # versjonssortering
    assert d["resultatfil"] == "docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27.json"
    assert git(r, "status", "--porcelain") == "" and git(r, "rev-parse", "HEAD") != start
    assert git(bart, "rev-parse", "main") == git(r, "rev-parse", "HEAD")  # pushet
    assert (r / "speil.log").read_text().splitlines() == [f"speil {git(r, 'rev-parse', '--short', 'HEAD')} 0"]  # speilet etter commit, rent tre
    assert set(git(r, "show", "--name-only", "--format=", "HEAD").split()) == {"docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27.json", "docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27_kjoring_meta.json"}


def test_to_kjoringer_etter_hverandre_hver_med_egen_commit_push_og_speil(tmp_path):
    r, bart = lag_repo(tmp_path)
    start = git(r, "rev-parse", "HEAD")
    p = kjor(r, "alle", "--prereg-id", "KLAR-PREREG-0001")
    assert p.returncode == 0, p.stderr
    assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord", "kjor_personvern_dev", "kjor_h4"]
    assert "--datasett npsc --splitt test --prereg-id KLAR-PREREG-0001 --mal-person 300 --mal-sted 200 --maks-timer 4 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0014" in kjort(r)[1]
    assert kjort(r)[0].endswith("--per-dialekt 60 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0013")
    assert kjort(r)[2].endswith("--ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015") and kjort(r)[3].endswith("kjor_h4 --prereg-id KLAR-PREREG-0001 --opptak /Volumes/Vault/arkivklarering/lyd/h4")
    log = git(r, "log", "--format=%H %s", f"{start}..HEAD").splitlines()[::-1]
    assert [l.split(" ", 1)[1][:10] for l in log] == [f"Testdel H{i}" for i in (1, 2, 3, 4)]
    metas = [json.loads(p_.read_text()) for p_ in sorted((r / "docs").glob("*kjoring_meta.json"))]
    shas = {m["del"]: m["commit"] for m in metas}
    hashes = [l.split()[0] for l in log]
    assert [shas[f"H{i}"] for i in (1, 2, 3, 4)] == [start] + hashes[:3]  # hver del startet på forrige dels commit
    assert all(m["git_status_porcelain_ved_start"] == [] for m in metas)
    assert git(bart, "rev-parse", "main") == hashes[-1]
    assert [l.split()[1] for l in (r / "speil.log").read_text().splitlines()] == [git(r, "rev-parse", "--short", h) for h in hashes]  # speil etter hver commit
    assert all(l.endswith(" 0") for l in (r / "speil.log").read_text().splitlines())


def test_feil_i_en_del_committer_den_og_stopper(tmp_path):
    r, bart = lag_repo(tmp_path)
    p = kjor(r, "alle", "--prereg-id", "KLAR-PREREG-0001", STUBB_FEIL="kjor_flaggoverlevelse_ord")
    assert p.returncode == 3 and "H2 feilet" in p.stderr
    assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord"]  # H3 og H4 startet ikke
    m = json.loads(next((r / "docs").glob("*flaggoverlevelse_ord*kjoring_meta.json")).read_text())
    assert m["returkode"] == 3 and git(r, "status", "--porcelain") == "" and git(bart, "rev-parse", "main") == git(r, "rev-parse", "HEAD")


def test_endret_sporet_fil_gir_ingen_commit_og_stopper(tmp_path):
    r, bart = lag_repo(tmp_path)
    start = git(r, "rev-parse", "HEAD")
    p = kjor(r, "H1", "--prereg-id", "KLAR-PREREG-0001", STUBB_OVERSKRIV="kjor_dev")
    assert p.returncode == 4 and "endret sporede filer" in p.stderr
    assert git(r, "rev-parse", "HEAD") == start and (r / "docs" / "sporet.md").read_text() == "endret av kjøringen"  # ingenting tilbakestilt
    assert subprocess.run(["git", "rev-parse", "-q", "--verify", "main"], cwd=bart, capture_output=True).returncode != 0  # ingenting pushet
    assert not (r / "speil.log").exists()


def endre_og_commit(r, sti, innhold):
    (r / sti).write_text(innhold)
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "endret kode")


def test_endret_kode_siden_taggen_stopper_for_hver_kodemappe(tmp_path):
    for sti in ("scripts/ny.sh", "kalibrering/ny.py", "arkivklarering/ny.py", "tests/test_ny.py", "eval/dev/kjor_ny.py", "eval/dyp/under/ny.py"):
        r, bart = lag_repo(tmp_path / sti.replace("/", "_"))
        (r / sti).parent.mkdir(parents=True, exist_ok=True)
        endre_og_commit(r, sti, "x = 1\n")
        p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
        assert p.returncode == 5 and sti in p.stderr, (sti, p.stderr)
        assert kjort(r) == [] and not (r / "speil.log").exists()


def test_resultatfiler_og_andre_filtyper_under_eval_tillates(tmp_path):
    r, bart = lag_repo(tmp_path)
    (r / "eval" / "test").mkdir()
    endre_og_commit(r, "eval/test/KLAR-EVAL-0099_resultat.json", "{}")  # ikke .py: ikke kode
    endre_og_commit(r, "docs/notat.md", "x")
    p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
    assert p.returncode == 0, p.stderr  # HEAD er ikke taggen, men koden er uendret


def test_manglende_tagg_stopper(tmp_path):
    r, bart = lag_repo(tmp_path)
    git(r, "tag", "-d", "testkjoring-v10")
    p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
    assert p.returncode == 5 and "testkjoring-v10" in p.stderr and "finnes ikke" in p.stderr and kjort(r) == []  # v1–v9 finnes, men teller ikke


def test_to_testdeler_etter_hverandre_med_kodesjekk_for_hver(tmp_path):
    r, bart = lag_repo(tmp_path)
    p1 = kjor(r, "H1", "--prereg-id", "KLAR-PREREG-0001")
    assert p1.returncode == 0, p1.stderr
    assert git(r, "rev-parse", "HEAD") != git(r, "rev-parse", "testkjoring-v10")  # HEAD har flyttet seg (resultat-commit), koden ikke
    p2 = kjor(r, "H2", "--prereg-id", "KLAR-PREREG-0001")
    assert p2.returncode == 0, p2.stderr
    assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord"]
    # kode endres mellom to deler: den andre nektes
    r2, _ = lag_repo(tmp_path / "b")
    assert kjor(r2, "H1", "--prereg-id", "KLAR-PREREG-0001").returncode == 0
    endre_og_commit(r2, "scripts/endret.sh", "echo hei\n")
    p = kjor(r2, "H2", "--prereg-id", "KLAR-PREREG-0001")
    assert p.returncode == 5 and "scripts/endret.sh" in p.stderr
    assert [x.split()[0] for x in kjort(r2)] == ["kjor_dev"] and len(git(r2, "log", "--format=%s").splitlines()) == 3  # x, Testdel H1, endret kode: ingen H2


def test_h4_kjores_med_inaseg_og_meta_forer_segmenteringen_mens_h1_h3_er_uendret(tmp_path):
    r, _ = lag_repo(tmp_path)
    assert kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001").returncode == 0
    d = json.loads((r / "docs" / "KLAR-EVAL-kjor_h4_v1.0_2026-10-27_kjoring_meta.json").read_text())
    assert d["segmentering"]["miljovariabel"] == "inaseg" and d["segmentering"]["logg"].startswith("eval/test/h4_segmenteringslogg_")
    assert (r / "segmentering.log").read_text().splitlines() == ["kjor_h4 inaseg"]


def test_h1_og_h2_kjores_med_inavamos_eksplisitt_og_meta_forer_det(tmp_path):
    r, _ = lag_repo(tmp_path)
    for d in ("H1", "H2"):  # også når kallerens miljø sier noe annet (standarden i koden er inaseg)
        assert kjor(r, d, "--prereg-id", "KLAR-PREREG-0001", ARKIVKLARERING_SEGMENTERING="inaseg",
                    ARKIVKLARERING_SEGMENTERING_LOGG="kaller.jsonl").returncode == 0
    assert (r / "segmentering.log").read_text().splitlines() == ["kjor_dev inavamos", "kjor_flaggoverlevelse_ord inavamos"]
    for navn in ("kjor_dev", "kjor_flaggoverlevelse_ord"):
        m = json.loads((r / "docs" / f"KLAR-EVAL-{navn}_v1.0_2026-10-27_kjoring_meta.json").read_text())
        assert m["segmentering"] == {"miljovariabel": "inavamos", "logg": None}
        assert "ARKIVKLARERING" not in m["kommando"]  # kommandoen startes uendret; valget står i miljøet og i meta


def test_alle_setter_segmentering_per_del_og_h3_far_kallerens_miljo(tmp_path):
    r, _ = lag_repo(tmp_path)
    env = {k: v for k, v in os.environ.items() if not k.startswith("ARKIVKLARERING_SEGMENTERING")}
    p = subprocess.run(["bash", "scripts/kjor_testdel.sh", "alle", "--prereg-id", "KLAR-PREREG-0001"], cwd=r, capture_output=True, text=True,
                       env={**env, "KLAR_PY": sys.executable, "KLAR_SPEIL": "scripts/speil_stubb.sh"})
    assert p.returncode == 0, p.stderr
    assert (r / "segmentering.log").read_text().splitlines() == ["kjor_dev inavamos", "kjor_flaggoverlevelse_ord inavamos",
                                                                 "kjor_personvern_dev -", "kjor_h4 inaseg"]  # H3: ikke arvet fra H1/H2
    metas = {m["del"]: m for m in (json.loads(f.read_text()) for f in (r / "docs").glob("*kjoring_meta.json"))}
    assert [metas[d]["segmentering"]["miljovariabel"] for d in ("H1", "H2", "H3", "H4")] == ["inavamos", "inavamos", None, "inaseg"]


def test_tor_viser_segmenteringen_per_del(tmp_path):
    r, _ = lag_repo(tmp_path)
    p = kjor(r, "--tor", "alle", "--prereg-id", "KLAR-PREREG-0001")
    linjer = [l for l in p.stdout.splitlines() if "ville kjørt" in l]
    assert ["ARKIVKLARERING_SEGMENTERING=inavamos" in linjer[0], "ARKIVKLARERING_SEGMENTERING=inavamos" in linjer[1],
            "ARKIVKLARERING_SEGMENTERING" in linjer[2], "ARKIVKLARERING_SEGMENTERING=inaseg" in linjer[3]] == [True, True, False, True]


def test_h3_kjores_med_kallerens_segmenteringsmiljo(tmp_path):
    r, _ = lag_repo(tmp_path)
    assert kjor(r, "H3", "--prereg-id", "KLAR-PREREG-0001", ARKIVKLARERING_SEGMENTERING="").returncode == 0
    assert (r / "segmentering.log").read_text().splitlines() == ["kjor_personvern_dev "]
