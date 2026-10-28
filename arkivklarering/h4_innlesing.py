"""H4-innlesing (KLAR-ADR-0018): innleseren for KLAR-MANUS-0002, i en egen modus uten noe resultat.

Bygger på norsk-tales kalibreringsrigg (`kalibrering/rigg.py`, lokal nettleserserver), men som en **innlesings-modus**: bare oppsett, mikrofonsjekk,
innlesing, avspilling, ta om (med påkrevd grunn) og navigasjon. Alt som kan vise eller beregne et resultat er borte (transkripsjon, rapport, eksport,
bidrag, sletting, selvtest): rutene finnes ikke (404), og siden (`h4_side.html`) har ingen slike elementer. Den som leser inn skal ikke se noe om
hvordan maskinen leser opptaket.

Riggversjonen er låst: norsk-tale må stå på commit `RIGG_COMMIT`, og hver rigg-fil som lastes må ha sha256 som i `RIGG_FILER`, ellers stopper
innlesingen før serveren starter. Opptakene ligger KUN under `H4_ROT` (Vault), aldri i git eller sky; én runde = `<runde>/opptak/<manus-id>.wav`
(16 kHz mono wav, som `kalibrering/kjor_h4.py --opptak` leser) + `runde.json`. Per opptak føres `opptakslogg.jsonl` (id, tidspunkt, forsøk, grunn).
Serveren fører i tillegg en hendelseslogg, `<H4_ROT>/serverlogg.jsonl` (oppstart, runde_ny, opptak_lagret, omtak, avslutt, stoppet; aldri lyd eller tekst).
Loggfila ligger i opptaksroten, ikke i en runde: `kjor_h4.finn_opptak` leser bare mapper som heter `runde-*` (kalibrering/kjor_h4.py:96) og riggens
`runder()` bare mapper med `runde.json` (norsk-tale kalibrering/rigg.py:146-152), så loggen kan ikke tolkes som en runde. Mikrofonsjekken tar ikke opp noe.
"""
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import threading
import time

NORSK_TALE = pathlib.Path(os.environ.get("NORSK_TALE", "~/dev/norsk-tale")).expanduser()
RIGG_COMMIT = "bcfef63d1be49ac239956dfb67784c002cecf310"
RIGG_FILER = {  # relativt til NORSK_TALE
    "kalibrering/rigg.py": "d79d692658235dd4a53877a25e933a689fd26ced896661c11b67a6bc1d480d68",
    "kalibrering/aggreger.py": "08e315e85dc5e820013fdca9f6ae56a56b150b3b09a89f70ba2c95d534c9b73d",
    "kalibrering/score.py": "90859617b4d1d59c88d0b2d95466f6c3f6b3626c4cff787ed835f36088aebfec",
    "kalibrering/norm.py": "70826a80cdb8b02810e1f70ad57509c1675f2a004fb114342d4bee917bbe6283",
    "kjerne/kjerne.py": "962e691c47824a4160bbd8fd208330abac5a7d4fd85ab803bedfaa17fb528a24",
    "kjerne/korriger.py": "335bc6ac2454ee1744556f411c2f7cf6a44fcd02579b07ba9d201e863752cc68",
}
H4_ROT = pathlib.Path("/Volumes/Vault/arkivklarering/lyd/h4")
SIDE = pathlib.Path(__file__).resolve().parent / "h4_side.html"
INSTRUKS = "Les i naturlig tempo og på din vanlige dialekt. Ikke legg ekstra trykk på navn, tall eller fremmedord."
GRUNNER = ("feil ord", "avbrudd", "støy")  # ta om bare ved feillesing; aldri på grunn av maskinens resultat
TILLATT_GET = ("/", "/api/oppsett", "/api/runde", "/api/opptak")
TILLATT_POST = ("/api/runde", "/api/opptak", "/api/avslutt")
REPO = pathlib.Path(__file__).resolve().parent.parent
LOGG_NAVN = "serverlogg.jsonl"
RIGGFILER_REPO = ("arkivklarering/h4_innlesing.py", "arkivklarering/h4_side.html", "scripts/rigg_manus.py")  # filene som utgjør innleseren


class RiggFeil(Exception):
    pass


def sha256_fil(sti) -> str:
    return hashlib.sha256(pathlib.Path(sti).read_bytes()).hexdigest()


def kontroller_rigg(rot=None) -> dict:
    """Stopper (RiggFeil) hvis norsk-tale ikke er på låst commit eller en rigg-fil avviker. Returnerer det som skal føres i runde.json."""
    rot = pathlib.Path(rot or NORSK_TALE)
    avvik = []
    for rel, forventet in RIGG_FILER.items():
        f = rot / rel
        if not f.is_file():
            avvik.append(f"{rel}: finnes ikke")
        elif sha256_fil(f) != forventet:
            avvik.append(f"{rel}: sha256 {sha256_fil(f)[:12]}… ≠ låst {forventet[:12]}…")
    commit = None
    if (rot / ".git").exists():
        p = subprocess.run(["git", "-C", str(rot), "rev-parse", "HEAD"], capture_output=True, text=True)
        commit = p.stdout.strip() or None
        if commit != RIGG_COMMIT:
            avvik.append(f"commit {commit} ≠ låst {RIGG_COMMIT}")
    if avvik:
        raise RiggFeil("Riggen er ikke den låste versjonen (KLAR-ADR-0018); stopper før innlesing:\n  " + "\n  ".join(avvik))
    return {"norsk_tale_commit": commit or RIGG_COMMIT, "filer": dict(RIGG_FILER)}


def last_rigg(rot=None):
    """Kontrollerer låsen og importerer riggen (modulen `rigg` fra norsk-tale)."""
    rot = pathlib.Path(rot or NORSK_TALE)
    kontroller_rigg(rot)
    for d in ("kalibrering", "kjerne", "lytter"):
        sys.path.insert(0, str(rot / d))
    import rigg  # noqa: E402  (norsk-tale/kalibrering/rigg.py, verifisert over)
    return rigg


def _git(*args):
    p = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else None


def oppstartsinfo():
    """Hva riggen kjører fra: arkivklarering-commit, tagger på HEAD, nærmeste `h4-rigg-v*`-tagg som er forfar til HEAD og om de tre riggfilene er
    identiske med den, og om riggfilene er uendret siden commiten. (Etter at taggen er satt kan HEAD ha flyttet seg til en commit som bare legger
    til tidsstempelfiler; da viser `rigg_tag.riggfiler_identiske_med_HEAD` at koden er den samme.)"""
    commit = _git("rev-parse", "HEAD")
    rigg_tag = None
    for t in (_git("tag", "-l", "--sort=-v:refname", "h4-rigg-v*") or "").split():
        sha = _git("rev-parse", f"{t}^{{commit}}")
        if sha and subprocess.run(["git", "-C", str(REPO), "merge-base", "--is-ancestor", sha, "HEAD"]).returncode == 0:
            ident = subprocess.run(["git", "-C", str(REPO), "diff", "--quiet", t, "HEAD", "--", *RIGGFILER_REPO]).returncode == 0
            rigg_tag = {"navn": t, "commit": sha, "riggfiler_identiske_med_HEAD": ident}
            break
    uendret = subprocess.run(["git", "-C", str(REPO), "diff", "--quiet", "HEAD", "--", *RIGGFILER_REPO]).returncode == 0 if commit else None
    return {"arkivklarering_commit": commit, "tagger_paa_HEAD": (_git("tag", "--points-at", "HEAD") or "").split(), "rigg_tag": rigg_tag,
            "riggfiler_uendret_siden_commit": uendret, "norsk_tale_commit": RIGG_COMMIT}


def lag_klasser(rigg):
    """H4Rigg og H4Handler som underklasser av norsk-tales Rigg og Handler. Ingen rute utover TILLATT_* svarer."""

    class H4Rigg(rigg.Rigg):
        def __init__(self, opptaksrot, inaktiv_s=1800):
            super().__init__(opptaksrot, {"modellvalg": None, "modell": None, "whisper": None}, inaktiv_s)
            self.logg_las = threading.Lock()
            self.avsluttet_via_knapp = False

        # ---- hendelseslogg (forespørselslaget; ikke lyd, ikke tekst fra opptak)
        def hend(self, type_, **felt):
            rad = {"tidspunkt": datetime.datetime.now().astimezone().isoformat(timespec="milliseconds"), "type": type_, **felt}
            try:
                with self.logg_las, open(self.rot / LOGG_NAVN, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rad, ensure_ascii=False) + "\n")
            except OSError as e:  # en loggfeil skal ikke velte et opptak, men synes i terminalen
                print(f"ADVARSEL: kunne ikke skrive {LOGG_NAVN}: {e}", file=sys.stderr, flush=True)

        # ---- runde: rom og mikrofon noteres én gang (fritekst), instruksen må være lest
        def ny_runde(self, data):
            rom = (data.get("rom_og_mikrofon") or "").strip()
            if not rom:
                raise rigg.Feil(400, "Beskriv rom og mikrofon (fritekst) før runden starter.")
            if not data.get("instruks_lest"):
                raise rigg.Feil(400, "Bekreft at instruksen er lest.")
            runde = super().ny_runde(data)
            runde["rom_og_mikrofon"] = rom[:2000]
            runde["instruks"] = INSTRUKS
            runde["h4_innlesing"] = {"norsk_tale_commit": RIGG_COMMIT, "rigg_filer_sha256": dict(RIGG_FILER)}
            self.skriv_runde(runde)
            return runde

        # ---- logg per opptak
        def _logg_sti(self, runde_id):
            return self.runde_dir(runde_id) / "opptakslogg.jsonl"

        def logg(self, runde_id):
            f = self._logg_sti(runde_id)
            return [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()] if f.is_file() else []

        def lagre_opptak(self, runde_id, manus_id, data, ctype, grunn=None):
            mal = self.wav(runde_id, manus_id)
            with self.logg_las:
                finnes = mal.is_file()
                if finnes and grunn not in GRUNNER:
                    raise rigg.Feil(400, "Ta om bare ved feillesing: velg feil ord, avbrudd eller støy.")
                if not finnes and grunn:
                    raise rigg.Feil(400, "Første forsøk har ingen omtaksgrunn.")
                forsok = sum(1 for r in self.logg(runde_id) if r["id"] == manus_id) + 1
                forkastet = None
                if finnes:  # det gamle opptaket beholdes for etterprøving, utenfor opptak/ (som H4-skriptet leser)
                    d = self.runde_dir(runde_id) / "forkastet"
                    d.mkdir(exist_ok=True)
                    forkastet = d / f"{manus_id}_forsok{forsok - 1}.wav"
                    mal.replace(forkastet)
                ut = super().lagre_opptak(runde_id, manus_id, data, ctype)
                rad = {"id": manus_id, "runde": runde_id, "tidspunkt": datetime.datetime.now().isoformat(timespec="seconds"), "forsok": forsok,
                       "grunn_omtak": grunn, "bytes": ut["bytes"], "wav_sha256": sha256_fil(mal),
                       "forkastet_fil": forkastet.name if forkastet else None}
                with open(self._logg_sti(runde_id), "a", encoding="utf-8") as f:
                    f.write(json.dumps(rad, ensure_ascii=False) + "\n")
            return {"ok": True, "bytes": ut["bytes"], "forsok": forsok}

    class H4Handler(rigg.Handler):
        def do_GET(self):
            try:
                sti, q = self._vakt("GET")
                if sti not in TILLATT_GET:
                    raise rigg.Feil(404, "Ikke funnet.")
                r = self.rigg
                if sti == "/":
                    return self._svar(200, SIDE.read_text(encoding="utf-8"), "text/html; charset=utf-8")
                if sti == "/api/oppsett":
                    return self._svar(200, {
                        "manus": [{k: s[k] for k in ("id", "malform", "klasse", "setning", "dialektutvalg")} for s in r.manus],
                        "regioner": rigg.REGIONER, "kilder": rigg.KILDER, "malformer": rigg.MALFORMER, "testsetning": rigg.TESTSETNING,
                        "runder": r.runder(), "opptaksrot": str(r.rot), "instruks": INSTRUKS, "grunner": list(GRUNNER)})
                return super().do_GET()
            except rigg.Feil as e:
                self._svar(e.status, {"feil": str(e)})
            except Exception as e:
                self._svar(500, {"feil": f"{type(e).__name__}: {e}"})

        def do_POST(self):
            try:
                sti, q = self._vakt("POST")
                if sti not in TILLATT_POST:
                    self._les()
                    raise rigg.Feil(404, "Ikke funnet.")
                if sti == "/api/runde":
                    data = self._json(self._les())
                    try:
                        runde = self.rigg.ny_runde(data)
                    except Exception as e:  # avvist (400) eller feil: føres med grunn, så svares det som før
                        self.rigg.hend("runde_ny", ok=False, grunn=str(e), status=getattr(e, "status", 500))
                        raise
                    self.rigg.hend("runde_ny", ok=True, runde=runde["id"], modus=runde["modus"], antall_manus=len(self.rigg.ider(runde)))
                    return self._svar(200, runde)
                if sti == "/api/opptak":
                    data = self._les()
                    if not data:
                        raise rigg.Feil(400, "Tomt opptak.")
                    grunn = q.get("grunn") or None
                    svar = self.rigg.lagre_opptak(q.get("runde"), q.get("id"), data, self.headers.get("Content-Type", ""), grunn)
                    self.rigg.hend("opptak_lagret", runde=q.get("runde"), id=q.get("id"), forsok=svar["forsok"])
                    if grunn:
                        self.rigg.hend("omtak", runde=q.get("runde"), id=q.get("id"), grunn=grunn, forsok=svar["forsok"])
                    return self._svar(200, svar)
                if sti == "/api/avslutt":
                    self.rigg.avsluttet_via_knapp = True
                    self.rigg.hend("avslutt")
                return super().do_POST()
            except rigg.Feil as e:
                self._svar(e.status, {"feil": str(e)})
            except Exception as e:
                self._svar(500, {"feil": f"{type(e).__name__}: {e}"})

    return H4Rigg, H4Handler


def start(manus_sti, rot=None, inaktiv_s=1800, melding=None):
    """Starter innlesingen. `rot` er alltid H4_ROT i bruk (tester sender en egen mappe). `melding` tar linjene «klar» og «stoppet» (standard: skrives til stdout)."""
    melding = melding or (lambda s: print(s, flush=True))
    rigg = last_rigg()
    rigg.MANUS = pathlib.Path(manus_sti)
    H4Rigg, H4Handler = lag_klasser(rigg)
    r = H4Rigg(rot or H4_ROT, inaktiv_s)
    r.rot.mkdir(parents=True, exist_ok=True)
    H4Handler.rigg = r
    server = rigg.Server(("127.0.0.1", 0), H4Handler)
    r.port = server.server_address[1]
    r.hend("oppstart", port=r.port, opptaksrot=str(r.rot), **oppstartsinfo())
    threading.Thread(target=rigg.vakt_inaktivitet, args=(server, r), daemon=True).start()
    melding(json.dumps({"type": "klar", "url": f"http://127.0.0.1:{r.port}/?token={r.token}", "opptak": str(r.rot)}))
    try:
        server.serve_forever()
    finally:
        server.server_close()
        via = "avslutt" if r.avsluttet_via_knapp else "tidsavbrudd" if time.monotonic() - r.sist > r.inaktiv_s else "avbrutt"
        r.hend("stoppet", via=via)
        melding(json.dumps({"type": "stoppet"}))
    return 0
