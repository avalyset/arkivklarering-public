"""H4-innleseren (KLAR-ADR-0018): rigglås, ingen resultatvisning, Vault-sti, instruks vist og omtakslogg. Ingen mikrofon, ingen Whisper, ingen testdel."""
import http.client
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import threading
import wave

import pytest

from arkivklarering import h4_innlesing as h4

REPO = pathlib.Path(__file__).resolve().parent.parent
pytestmark = pytest.mark.skipif(not (h4.NORSK_TALE / "kalibrering" / "rigg.py").is_file() or not shutil.which("ffmpeg"), reason="norsk-tale eller ffmpeg mangler")
FORBUDT_I_SIDEN = ("transkri", "wer", "rapport", "resultat", "poeng", "flagg", "eksport", "bidrag", "selvtest", "hopp over", "slett")


def wav_bytes(sek=0.3):
    b = io.BytesIO()
    with wave.open(b, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(b"\x10\x00" * int(16000 * sek))
    return b.getvalue()


@pytest.fixture
def server(tmp_path):
    rigg = h4.last_rigg()
    rigg.MANUS = next(iter(sorted((REPO / "kalibrering").glob("KLAR-MANUS-0002_*.tsv"))))
    H4Rigg, H4Handler = h4.lag_klasser(rigg)
    r = H4Rigg(tmp_path / "h4")
    r.rot.mkdir(parents=True, exist_ok=True)
    H4Handler.rigg = r
    srv = rigg.Server(("127.0.0.1", 0), H4Handler)
    r.port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield r
    srv.shutdown()
    srv.server_close()


def kall(r, metode, sti, kropp=b"", ctype="application/json", med_token=True):
    c = http.client.HTTPConnection("127.0.0.1", r.port, timeout=30)
    url = sti + (("&" if "?" in sti else "?") + "token=" + r.token if med_token else "")
    c.request(metode, url, body=kropp if metode == "POST" else None,
              headers={"Content-Type": ctype, "Origin": f"http://127.0.0.1:{r.port}"} if metode == "POST" else {})
    svar = c.getresponse()
    data = svar.read()
    c.close()
    return svar.status, data


def ny_runde(r, **ekstra):
    d = {"modus": "fullt", "rom_og_mikrofon": "kontor, innebygd mikrofon", "instruks_lest": True, **ekstra}
    st, data = kall(r, "POST", "/api/runde", json.dumps(d).encode())
    return st, json.loads(data)


def test_riggen_er_laast_til_commit_og_filer(tmp_path):
    assert h4.kontroller_rigg()["norsk_tale_commit"] == h4.RIGG_COMMIT
    falsk = tmp_path / "norsk-tale"
    for rel in h4.RIGG_FILER:
        (falsk / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(h4.NORSK_TALE / rel, falsk / rel)
    assert h4.kontroller_rigg(falsk)  # uendrede filer, ingen .git: bare filhashene sjekkes
    (falsk / "kalibrering" / "rigg.py").write_text("# endret\n")
    with pytest.raises(h4.RiggFeil, match="rigg.py"):
        h4.kontroller_rigg(falsk)
    (falsk / "kalibrering" / "rigg.py").unlink()
    with pytest.raises(h4.RiggFeil, match="finnes ikke"):
        h4.kontroller_rigg(falsk)


def test_ingen_resultatvisning_ruter_og_side(server):
    for sti in ("/api/transkriber", "/api/resultat?runde=x", "/api/rapport?runde=x", "/api/bidrag?runde=x", "/api/selvtest", "/api/ukjent"):
        assert kall(server, "GET", sti)[0] == 404, sti
    for sti in ("/api/transkriber", "/api/slett", "/api/hopp", "/api/bidrag", "/api/selvtest/start", "/api/selvtest/lagre", "/api/selvtest/opptak"):
        assert kall(server, "POST", sti, b"{}")[0] == 404, sti
    assert kall(server, "GET", "/api/oppsett")[0] == 200 and kall(server, "GET", "/", med_token=False)[0] == 404  # token kreves
    st, side = kall(server, "GET", "/")
    tekst = side.decode("utf-8").lower()
    assert st == 200 and not [w for w in FORBUDT_I_SIDEN if w in tekst], [w for w in FORBUDT_I_SIDEN if w in tekst]
    for tom in ("/api/oppsett",):
        assert "modellvalg" not in kall(server, "GET", tom)[1].decode()


def test_instruksen_vises_for_start_og_ved_innlesing(server):
    assert h4.INSTRUKS == "Les i naturlig tempo og på din vanlige dialekt. Ikke legg ekstra trykk på navn, tall eller fremmedord."
    assert json.loads(kall(server, "GET", "/api/oppsett")[1])["instruks"] == h4.INSTRUKS
    side = h4.SIDE.read_text(encoding="utf-8")
    assert 'id="instruks"' in side and 'id="instruks2"' in side and "OPPSETT.instruks" in side
    assert re.search(r'class="kort instruks" id="instruks"', side) and 'id="kortOppsett"' in side  # synlig øverst, før oppsettet
    assert 'id="lest"' in side and "instruks_lest" in side  # må bekreftes lest før runden starter
    st, d = ny_runde(server, instruks_lest=False)
    assert st == 400 and "instruksen" in d["feil"].lower()


def test_rom_og_mikrofon_foeres_en_gang_per_runde(server):
    st, d = ny_runde(server, rom_og_mikrofon="  ")
    assert st == 400
    st, d = ny_runde(server)
    assert st == 200 and d["rom_og_mikrofon"] == "kontor, innebygd mikrofon" and d["instruks"] == h4.INSTRUKS
    assert d["h4_innlesing"]["norsk_tale_commit"] == h4.RIGG_COMMIT
    lagret = json.loads((server.rot / d["id"] / "runde.json").read_text(encoding="utf-8"))
    assert lagret["rom_og_mikrofon"] == "kontor, innebygd mikrofon" and lagret["modus"] == "fullt"


def test_vault_sti_og_aldri_i_repoet():
    assert h4.H4_ROT == pathlib.Path("/Volumes/Vault/arkivklarering/lyd/h4")  # fast i den låste innleseren (h4-rigg-v3), ikke ARKIVKLARERING_DATA
    assert REPO not in h4.H4_ROT.parents
    p = subprocess.run([sys.executable, str(REPO / "scripts" / "rigg_manus.py"), "--opptak", "/tmp/x"], capture_output=True, text=True)
    assert p.returncode != 0 and "opptaksmappen er fast" in (p.stderr + p.stdout)  # ingen annen opptaksmappe kan velges
    if not os.path.ismount("/Volumes/Vault"):
        pytest.skip("rigg_manus.py --tor åpner den faste opptaksmappen på Vault (h4-rigg-v3); /Volumes/Vault er ikke montert")
    p = subprocess.run([sys.executable, str(REPO / "scripts" / "rigg_manus.py"), "--tor"], capture_output=True, text=True)
    assert p.returncode == 0 and "opptak: /Volumes/Vault/arkivklarering/lyd/h4" in p.stdout and h4.INSTRUKS in p.stdout


def test_omtakslogg_og_ta_om_bare_ved_feillesing(server):
    st, runde = ny_runde(server)
    rid = runde["id"]
    manus_id = server.manus[0]["id"]
    sti = f"/api/opptak?runde={rid}&id={manus_id}"
    st, d = kall(server, "POST", sti + "&grunn=feil+ord", wav_bytes(), "audio/wav")
    assert st == 400 and "første" in d.decode().lower()  # første forsøk har ingen grunn
    st, d = kall(server, "POST", sti, wav_bytes(), "audio/wav")
    assert st == 200 and json.loads(d)["forsok"] == 1
    st, d = kall(server, "POST", sti, wav_bytes(), "audio/wav")
    assert st == 400 and "feillesing" in d.decode()  # omtak uten grunn nektes
    st, d = kall(server, "POST", sti + "&grunn=d%C3%A5rlig+resultat", wav_bytes(), "audio/wav")
    assert st == 400  # grunn som ikke er feillesing (f.eks. maskinens resultat) nektes
    st, d = kall(server, "POST", sti + "&grunn=st%C3%B8y", wav_bytes(1.0), "audio/wav")
    assert st == 200 and json.loads(d)["forsok"] == 2
    logg = [json.loads(l) for l in (server.rot / rid / "opptakslogg.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [(r["id"], r["forsok"], r["grunn_omtak"]) for r in logg] == [(manus_id, 1, None), (manus_id, 2, "støy")]
    assert all(r["tidspunkt"] and r["runde"] == rid and len(r["wav_sha256"]) == 64 for r in logg)
    assert (server.rot / rid / "forkastet" / f"{manus_id}_forsok1.wav").is_file()
    wav = server.rot / rid / "opptak" / f"{manus_id}.wav"  # gjeldende opptak = siste forsøk, 16 kHz mono wav (formatet kjor_h4.py leser)
    with wave.open(str(wav)) as w:
        assert (w.getframerate(), w.getnchannels(), w.getsampwidth()) == (16000, 1, 2) and w.getnframes() > 12000
    assert [p.name for p in (server.rot / rid / "opptak").glob("*")] == [f"{manus_id}.wav"]
    st, status = kall(server, "GET", f"/api/runde?runde={rid}")
    assert json.loads(status)["rader"][0]["opptak"] is True
    st, lyd = kall(server, "GET", sti)  # avspilling av eget opptak er tillatt
    assert st == 200 and lyd[:4] == b"RIFF"


def test_opptakene_kan_leses_av_kjor_h4_finn_opptak(server):
    import importlib.util
    spec = importlib.util.spec_from_file_location("kjor_h4_t", REPO / "kalibrering" / "kjor_h4.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["kjor_h4_t"] = m
    spec.loader.exec_module(m)
    st, runde = ny_runde(server, dialektregion="Østlandet", dialektkilde="morsmål", malform="nb")
    assert st == 200
    manus_id = server.manus[0]["id"]
    assert kall(server, "POST", f"/api/opptak?runde={runde['id']}&id={manus_id}", wav_bytes(), "audio/wav")[0] == 200
    funnet = m.finn_opptak(server.rot, [])
    assert len(funnet) == 1 and funnet[0][0] == runde["id"] and list(funnet[0][2]) == [manus_id]
    assert funnet[0][1]["dialektregion"] == "Østlandet" and funnet[0][1]["malform"] == "nb"  # feltene kjor_h4.py bruker


# ---- h4-fiks (ADR-0018 v1.1): ingen testopptak, banner, statuslinje, bekreftelse ved avslutning, hendelseslogg

def test_mikrofonsjekken_har_ingen_testopptak_og_siden_har_banner_uten_runde():
    side = h4.SIDE.read_text(encoding="utf-8")
    for borte in ("testOpp", "testStopp", "testSpill", "testBlob", "Ta opp testsetning"):
        assert borte not in side, borte
    assert 'id="mikStart"' in side and 'id="nivaa"' in side and "getUserMedia" in side  # tillatelse og nivåmåler er beholdt
    assert re.search(r'<div id="banner" class="banner">Ingen runde startet – ingenting lagres\. Fyll ut og trykk Start ny runde\.</div>', side)  # synlig fra start
    assert side.index('id="banner"') < side.index('id="instruks"')  # øverst
    assert "Runde ${RUNDE.id} – lagret ${antallLagret()} av ${RADER.length}" in side and 'id="statuslinje"' in side
    ut = side[side.index("async function lagreOpptak"):]
    assert ut.index("await post(") < ut.index("visStatus()")  # statuslinja oppdateres bare etter serversvar
    assert side.count("visStatus()") == 3  # definisjon, åpne runde, etter lagret opptak


def test_avslutt_krever_bekreftelse_med_antall_lagret():
    side = h4.SIDE.read_text(encoding="utf-8")
    kode = side[side.index('$("avslutt").onclick'):]
    assert "Avslutte innleseren? ${antallLagret()} av ${RADER.length} opptak er lagret i denne runden. Du kan fortsette senere." in kode
    assert '"Avslutte? Ingen runde er startet."' in kode
    assert kode.index("confirm(melding)") < kode.index('post("avslutt")') and "return;" in kode[:kode.index('post("avslutt")')]


class _Port:
    def __init__(self, port, token):
        self.port, self.token = port, token


def test_hendelseslogg_ende_til_ende_mot_server_i_prosess(tmp_path):
    manus = next(iter(sorted((REPO / "kalibrering").glob("KLAR-MANUS-0002_*.tsv"))))
    rot = tmp_path / "h4"  # aldri lyd/h4/
    ut = []
    t = threading.Thread(target=h4.start, args=(manus,), kwargs={"rot": rot, "melding": ut.append}, daemon=True)
    t.start()
    for _ in range(100):
        if ut:
            break
        threading.Event().wait(0.1)
    klar = json.loads(ut[0])
    assert klar["type"] == "klar" and klar["opptak"] == str(rot)
    port, token = re.search(r":(\d+)/\?token=(\S+)", klar["url"]).groups()
    r = _Port(int(port), token)
    st, d = ny_runde(r, rom_og_mikrofon="  ")  # avvist
    assert st == 400
    st, runde = ny_runde(r)
    assert st == 200
    mid = json.loads(kall(r, "GET", f"/api/runde?runde={runde['id']}")[1])["rader"][0]["id"]
    sti = f"/api/opptak?runde={runde['id']}&id={mid}"
    assert kall(r, "POST", sti, wav_bytes(), "audio/wav")[0] == 200
    assert kall(r, "POST", sti + "&grunn=feil+ord", wav_bytes(1.0), "audio/wav")[0] == 200  # omtak
    assert (rot / runde["id"] / "opptak" / f"{mid}.wav").is_file()
    assert kall(r, "POST", "/api/avslutt", b"{}")[0] == 200
    t.join(timeout=15)
    assert not t.is_alive() and json.loads(ut[-1]) == {"type": "stoppet"}
    logg = [json.loads(l) for l in (rot / h4.LOGG_NAVN).read_text(encoding="utf-8").splitlines()]
    assert [x["type"] for x in logg] == ["oppstart", "runde_ny", "runde_ny", "opptak_lagret", "opptak_lagret", "omtak", "avslutt", "stoppet"]
    assert [x["type"] for x in logg if x["type"] in ("oppstart", "runde_ny", "opptak_lagret", "avslutt", "stoppet")][:1] == ["oppstart"]
    assert logg[1]["ok"] is False and "Beskriv rom" in logg[1]["grunn"] and logg[1]["status"] == 400
    assert logg[2]["ok"] is True and logg[2]["runde"] == runde["id"]
    assert [(x["id"], x["forsok"]) for x in logg[3:5]] == [(mid, 1), (mid, 2)] and logg[5]["grunn"] == "feil ord"
    assert logg[0]["norsk_tale_commit"] == h4.RIGG_COMMIT and logg[0]["arkivklarering_commit"] == h4._git("rev-parse", "HEAD")
    assert logg[-1]["via"] == "avslutt" and all(x["tidspunkt"] for x in logg)
    forbudt = {"lyd", "wav", "data", "tekst", "transkripsjon", "blob"}
    assert not [k for x in logg for k in x if k in forbudt]  # ingen lyd, ingen tekst fra opptak


def test_loggfila_i_opptaksroten_forstyrrer_ikke_h4_skriptets_listing(server):
    import importlib.util
    spec = importlib.util.spec_from_file_location("kjor_h4_t2", REPO / "kalibrering" / "kjor_h4.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["kjor_h4_t2"] = m
    spec.loader.exec_module(m)
    st, runde = ny_runde(server)
    mid = server.manus[0]["id"]
    assert kall(server, "POST", f"/api/opptak?runde={runde['id']}&id={mid}", wav_bytes(), "audio/wav")[0] == 200
    assert (server.rot / h4.LOGG_NAVN).is_file()  # loggfila ligger ved siden av rundemappen
    funnet = m.finn_opptak(server.rot, [])
    assert [f[0] for f in funnet] == [runde["id"]] and list(funnet[0][2]) == [mid]
    assert [r["id"] for r in server.runder()] == [runde["id"]]  # riggens rundeliste teller heller ikke loggfila


def test_oppstartsinfo_viser_tagg_og_at_riggfilene_er_identiske_etter_en_tidsstempelcommit(tmp_path, monkeypatch):
    rep = tmp_path / "rep"
    for rel in h4.RIGGFILER_REPO:
        (rep / rel).parent.mkdir(parents=True, exist_ok=True)
        (rep / rel).write_text("x\n")
    def g(*a):
        subprocess.run(["git", "-C", str(rep), "-c", "user.name=t", "-c", "user.email=t@t", *a], check=True, capture_output=True)
    subprocess.run(["git", "init", "-q", str(rep)], check=True)
    g("add", "."); g("commit", "-qm", "kode"); g("tag", "h4-rigg-v3")
    monkeypatch.setattr(h4, "REPO", rep)
    i = h4.oppstartsinfo()
    assert i["tagger_paa_HEAD"] == ["h4-rigg-v3"] and i["rigg_tag"]["navn"] == "h4-rigg-v3" and i["rigg_tag"]["riggfiler_identiske_med_HEAD"] is True
    (rep / "stempel.ots").write_text("ots\n")
    g("add", "."); g("commit", "-qm", "stempel")
    i = h4.oppstartsinfo()
    assert i["tagger_paa_HEAD"] == [] and i["rigg_tag"]["commit"] == h4._git("rev-parse", "h4-rigg-v3")
    assert i["rigg_tag"]["riggfiler_identiske_med_HEAD"] is True and i["riggfiler_uendret_siden_commit"] is True
    (rep / "arkivklarering" / "h4_side.html").write_text("endret\n")
    i = h4.oppstartsinfo()
    assert i["rigg_tag"]["riggfiler_identiske_med_HEAD"] is True and i["riggfiler_uendret_siden_commit"] is False  # uforpliktet endring synes
