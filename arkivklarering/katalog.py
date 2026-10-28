"""Utkast til katalogpost per sending, etter samme modell som Nunn Centers OHMSifier (utkast til OHMS-indeks).

ALT her er «utkast – maskinforslag» til menneskelig retting, ikke katalogisering. Modellen kjører lokalt via ollama
(http://127.0.0.1:11434); en annen adresse enn loopback avvises, så ingenting går til skyen. Modellvalget og begrunnelsen
står i KLAR-ADR-0013.

Utdata (`Katalogpost`): tittel, dato (bare hvis den nevnes), talere, steder, 3–8 emneord og et sammendrag per segment med
tidskode. Modellen er ikke til å stole på for navn, steder og datoer: alt den foreslår der sjekkes mot transkripsjonen og
personvernflaggene, og forslag som ikke står i teksten forkastes og logges i `forkastet`.
"""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field

MERKNAD = "utkast – maskinforslag"
OLLAMA_URL = "http://127.0.0.1:11434"
STANDARD_MODELL = "hf.co/NbAiLab/borealis-open-4b-gguf:Q4_K_M"  # KLAR-ADR-0013
VINDU_S = 60.0
MIN_EMNEORD, MAKS_EMNEORD = 3, 8


@dataclass
class Katalogpost:
    """Utkast til katalogpost for én sending. `segmenter`: [{start, stopp, sammendrag}] i sekunder."""
    tittel: str = ""
    dato: str | None = None  # bare hvis den nevnes i sendingen (ÅÅÅÅ-MM-DD eller ÅÅÅÅ)
    talere: list[str] = field(default_factory=list)
    steder: list[str] = field(default_factory=list)
    emneord: list[str] = field(default_factory=list)
    segmenter: list[dict] = field(default_factory=list)
    modell: str = ""
    merknad: str = MERKNAD
    forkastet: list[str] = field(default_factory=list)  # modellforslag som ikke sto i teksten

    def som_dict(self) -> dict:
        return asdict(self)


class IkkeLokalt(ValueError):
    """Ollama-adressen er ikke loopback; ingenting skal gå til skyen."""


def _sjekk_lokal(url: str) -> None:
    v = urllib.parse.urlparse(url).hostname
    if v not in ("127.0.0.1", "localhost", "::1"):
        raise IkkeLokalt(f"{url}: bare lokal ollama er tillatt")


def ollama_chat(modell: str, system: str, bruker: str, url: str = OLLAMA_URL, tidsgrense_s: int = 600) -> str:
    """Ett kall til lokal ollama med temperatur 0 og fast seed (gjentakbart), JSON-modus."""
    _sjekk_lokal(url)
    kropp = json.dumps({"model": modell, "stream": False, "format": "json", "options": {"temperature": 0, "seed": 20261026},
                        "messages": [{"role": "system", "content": system}, {"role": "user", "content": bruker}]}).encode()
    req = urllib.request.Request(url + "/api/chat", data=kropp, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=tidsgrense_s) as r:
        return json.load(r)["message"]["content"]


SYSTEM = ("Du hjelper et norsk lokalradio- og lydarkiv med å lage UTKAST til katalogposter. Svar alltid med gyldig JSON. "
          "Skriv på samme målform (bokmål eller nynorsk) som teksten du får. Ikke finn på navn, steder eller datoer: "
          "bruk bare det som står i teksten. Er du usikker, la feltet stå tomt.")


def _json(tekst: str) -> dict:
    try:
        d = json.loads(tekst)
        return d if isinstance(d, dict) else {}
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", tekst, re.S)
        try:
            return json.loads(m.group(0)) if m else {}
        except json.JSONDecodeError:
            return {}


def _mmss(sek: float) -> str:
    return f"{int(sek) // 60:02d}:{int(sek) % 60:02d}"


def vinduer(cues, vindu_s: float = VINDU_S):
    """Grupperer cuene i tidsvinduer på omtrent `vindu_s` sekunder: [(start, stopp, [cuer])]."""
    ut, gjeldende = [], []
    for c in sorted(cues, key=lambda c: c.start):
        if gjeldende and c.start - gjeldende[0].start >= vindu_s:
            ut.append((gjeldende[0].start, gjeldende[-1].stop, gjeldende))
            gjeldende = []
        gjeldende.append(c)
    if gjeldende:
        ut.append((gjeldende[0].start, gjeldende[-1].stop, gjeldende))
    return ut


def _finnes_i(tekst: str, navn: str) -> bool:
    n = re.sub(r"\s+", " ", navn.strip().lower())
    return bool(n) and n in re.sub(r"\s+", " ", tekst.lower())


def rens_post(rå: dict, tekst: str, flagg_person: list[str], flagg_sted: list[str]) -> Katalogpost:
    """Sjekker modellens forslag mot teksten. Personer og steder må stå i teksten (eller i flaggene), en dato må stå i teksten,
    emneord begrenses til 3–8 stykker. Det som forkastes, logges i `forkastet`."""
    post = Katalogpost(tittel=str(rå.get("tittel", "")).strip(), modell=str(rå.get("_modell", "")))
    forkastet = []
    for navn in [str(x).strip() for x in rå.get("talere", []) if str(x).strip()]:
        if _finnes_i(tekst, navn) or any(_finnes_i(f, navn) or _finnes_i(navn, f) for f in flagg_person):
            post.talere.append(navn)
        else:
            forkastet.append(f"taler «{navn}» står ikke i teksten")
    steder = [str(x).strip() for x in rå.get("steder", []) if str(x).strip()]
    for navn in flagg_sted + steder:  # stedene kommer fra personvernflaggene; modellens tillegg må stå i teksten
        if navn in post.steder:
            continue
        if navn in flagg_sted or _finnes_i(tekst, navn):
            post.steder.append(navn)
        else:
            forkastet.append(f"sted «{navn}» står ikke i teksten")
    d = str(rå.get("dato") or "").strip()
    if d:
        ar = re.search(r"(18|19|20)\d{2}", d)
        if ar and ar.group(0) in tekst:
            post.dato = d
        else:
            forkastet.append(f"dato «{d}» står ikke i teksten")
    ord_ = []
    for e in rå.get("emneord", []):
        e = str(e).strip().lower()
        if re.search(r"\d(?:\D{0,2}\d){5,}", e):  # telefonnummer, personnummer og lignende er ikke emneord
            forkastet.append(f"emneord «{e}» ligner et nummer")
            continue
        if e and e not in ord_:
            ord_.append(e)
    post.emneord = ord_[:MAKS_EMNEORD]
    if len(post.emneord) < MIN_EMNEORD:
        forkastet.append(f"færre enn {MIN_EMNEORD} emneord ({len(post.emneord)})")
    post.forkastet = forkastet
    return post


def lag_katalogpost(cues, union_flagg=(), modell: str = STANDARD_MODELL, chat=ollama_chat, vindu_s: float = VINDU_S) -> Katalogpost:
    """Lager utkastet fra cuene (normalisert lag) og unionsflaggene (`personvern.slaa_sammen_lag`).

    `chat(modell, system, bruker)` kan byttes ut i tester. Tittel, emneord, talere og dato spørres i ett kall på hele teksten;
    sammendraget lages per tidsvindu."""
    cues = list(cues)
    tekst = "\n".join(f"[{_mmss(c.start)}] {c.tekst}" for c in cues)
    person = sorted({(u.per_lag.get("normalisert") or next(iter(u.per_lag.values())))["utdrag"] for u in union_flagg if u.kategori == "person"})
    sted = sorted({(u.per_lag.get("normalisert") or next(iter(u.per_lag.values())))["utdrag"] for u in union_flagg if u.kategori == "sted"})
    bruker = (f"Transkripsjon (maskinlagd, kan ha feil):\n{tekst}\n\nPersonnavn funnet av personvernflaggene: {person or 'ingen'}\n"
              f"Steder funnet av personvernflaggene: {sted or 'ingen'}\n\nSvar med JSON: "
              '{"tittel": "kort tittel", "dato": "ÅÅÅÅ-MM-DD eller ÅÅÅÅ, bare hvis den nevnes, ellers tom streng", '
              '"talere": ["navn på de som snakker, bare fra listen over personnavn"], "steder": ["steder som nevnes"], '
              f'"emneord": ["{MIN_EMNEORD} til {MAKS_EMNEORD} emneord"]}}')
    rå = _json(chat(modell, SYSTEM, bruker))
    rå["_modell"] = modell
    post = rens_post(rå, " ".join(c.tekst for c in cues), person, sted)
    post.modell = modell
    for a, b, gruppe in vinduer(cues, vindu_s):
        v = "\n".join(c.tekst for c in gruppe)
        s = _json(chat(modell, SYSTEM, f"Transkripsjon:\n{v}\n\nSvar med JSON: " + '{"sammendrag": "ett til to setninger om hva som blir sagt"}'))
        post.segmenter.append({"start": round(a, 3), "stopp": round(b, 3), "sammendrag": str(s.get("sammendrag", "")).strip()})
    return post
