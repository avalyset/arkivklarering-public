"""Personvernflagg v0: forslag til menneskelig vurdering, aldri en avgjørelse. Ingenting fjernes eller endres.

Motor (KLAR-ADR-0008, KLAR-ADR-0012):
  - Presidio AnalyzerEngine med spaCy-modellen `nb_core_news_md` etter CLEANUP-guiden (Norsk Regnesentral
    og NAV, kap. 7.2), registrert for både `nb` og `nn`. Det finnes ingen egen nynorsk-modell i spaCy; `nn`
    bruker bokmålsmodellen, og det er en kjent svakhet.
  - NB-BERT-base-ner (`NbAiLab/nb-bert-base-ner`) som egen gjenkjenner for personer, steder og organisasjoner.
  - Egne mønstergjenkjennere for datoer, fødselsår, telefonnummer og fødselsnummer (nb og nn).
  - Nøkkelordlister i `vokabular/sensitivt_*.txt` for helse, økonomi, konflikt, religion og politikk.

Recall foran presisjon: standardterskelen er 0, og et falskt flagg koster mindre enn et oversett navn.
Et manglende flagg er likevel ingen garanti. Rålaget (verbatim) er skrevet med små bokstaver uten tegnsetting;
store bokstaver er et viktig signal for navnegjenkjenning, så flagg på rålaget forventes å ha lavere recall enn
på det normaliserte laget (se KLAR-EVAL-0005).

Hvert flagg: (start, stopp, kategori, kilde, score, utdrag). `start` og `stopp` er tegnposisjoner i teksten som
ble analysert; for cuer kommer cuens tidskoder i tillegg.

v0.2: flagg fra rålaget og det normaliserte laget slås sammen til én liste (`slaa_sammen_lag`): samme kategori og
overlappende tid blir ett flagg som beholder begge lagenes utdrag og tidsgrenser, kildelag («ra», «normalisert» eller
«begge») og høyeste score. Et flagg som bare finnes i ett lag beholdes alltid, og ingen terskel filtrerer bort flagg.
"""
from __future__ import annotations

import difflib
import pathlib
import re
from dataclasses import asdict, dataclass, field

VOKABULAR = pathlib.Path(__file__).resolve().parent.parent / "vokabular"
SPRAK = ("nb", "nn")
SPACY_MODELL = "nb_core_news_md"
BERT_MODELL = "NbAiLab/nb-bert-base-ner"

# Presidio-entitet -> kategori i flaggene
KATEGORI = {
    "PERSON": "person", "LOCATION": "sted", "ORGANIZATION": "organisasjon",
    "NB_DATO": "dato", "NB_FODSELSAAR": "fødselsår",
    "NB_TELEFON": "telefon", "NB_FODSELSNUMMER": "fødselsnummer", "EMAIL_ADDRESS": "e-post",
    "SENS_HELSE": "helse", "SENS_OKONOMI": "økonomi", "SENS_KONFLIKT": "konflikt",
    "SENS_RELIGION": "religion", "SENS_POLITIKK": "politikk",
}
ORDLISTER = {"SENS_HELSE": "helse", "SENS_OKONOMI": "okonomi", "SENS_KONFLIKT": "konflikt",
             "SENS_RELIGION": "religion", "SENS_POLITIKK": "politikk"}
# NorNE-/spaCy-/BERT-etiketter -> Presidio-entitet
ETIKETT = {"PER": "PERSON", "LOC": "LOCATION", "GPE_LOC": "LOCATION", "GPE": "LOCATION",
           "ORG": "ORGANIZATION", "GPE_ORG": "ORGANIZATION"}
MANEDER = "januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember"


@dataclass
class Flagg:
    start: int
    stopp: int
    kategori: str
    kilde: str
    score: float
    utdrag: str
    lag: str = ""
    cue_start: float | None = None
    cue_stopp: float | None = None
    ord_start: float | None = None  # ordspennet: tid for første og siste ord flagget dekker (hvis ordtidsstempler finnes)
    ord_stopp: float | None = None

    def som_dict(self) -> dict:
        d = asdict(self)
        d["score"] = round(d["score"], 3)
        return {k: v for k, v in d.items() if v not in ("", None)}


def les_ordliste(navn: str) -> list[str]:
    """Leser vokabular/sensitivt_<navn>.txt (kommentarlinjer med # hoppes over)."""
    sti = VOKABULAR / f"sensitivt_{navn}.txt"
    return [l.strip() for l in sti.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


# Bøyningsendelser som tillates på nøkkelord med minst fire bokstaver (bestemt form, flertall, preteritum og partisipp, nb og nn)
ENDELSER = "en|et|a|e|er|ar|ane|ene|te|t|de|d"
SIFFERKANDIDAT = r"(?<![\d+])(?:\+47[ -]?|0047[ -]?)?\d(?:\d|[ ,.\-]{1,2}(?=\d)){6,20}(?!\d)"


def _siffer(tekst: str) -> str:
    return re.sub(r"\D", "", tekst)


def _aar_liste_eller_dato(tekst: str) -> bool:
    """Treff som egentlig er en dato (dd.mm.åååå) eller en liste med årstall, ikke et nummer."""
    if re.fullmatch(r"\d{1,2}[.]\d{1,2}[.]\d{2,4}", tekst.strip()):
        return True
    grupper = re.findall(r"\d+", tekst)
    return len(grupper) >= 2 and all(re.fullmatch(r"(?:19|20)\d{2}", g) for g in grupper)


def _nokkelord_monster(ord_: str) -> str:
    """Regex for ett nøkkelord: hele ord, uten stor/liten bokstav; ord på fire bokstaver eller mer får bøyningsendelser.
    Flerordsuttrykk matches ordrett."""
    e = re.escape(ord_)
    return rf"(?<!\w){e}(?:{ENDELSER})?(?!\w)" if len(ord_) >= 4 and " " not in ord_ else rf"(?<!\w){e}(?!\w)"


def monster_gjenkjennere(sprak: str):
    """Mønstergjenkjennere for datoer, fødselsår, telefon, fødselsnummer og nøkkelord, for ett språk. Krever ikke NLP-motor.

    Telefonnumre og fødselsnumre tillater skilletegn mellom sifrene, fordi Whisper skriver talte tall som «68, 05, 45, 67» eller
    «150 575 45 615» (funn i den syntetiske kjedekalibreringen, KLAR-EVAL-0008). Treffet godtas når sifrene har riktig antall
    og form (8 siffer som begynner på 2–9, eventuelt med +47/0047; 11 siffer med plausibel dato) og ikke er en dato eller en
    liste med årstall."""
    from presidio_analyzer import Pattern, PatternRecognizer

    class _Telefon(PatternRecognizer):
        def validate_result(self, pattern_text):
            if _aar_liste_eller_dato(pattern_text):
                return False
            d = _siffer(pattern_text)
            d = d[2:] if d.startswith("47") and len(d) == 10 else d[4:] if d.startswith("0047") and len(d) == 12 else d
            return None if len(d) == 8 and d[0] in "23456789" else False

    class _Fodselsnummer(PatternRecognizer):
        def validate_result(self, pattern_text):
            d = _siffer(pattern_text)
            if len(d) != 11 or _aar_liste_eller_dato(pattern_text):
                return False
            return None if 1 <= int(d[:2]) <= 31 and 1 <= int(d[2:4]) <= 12 else False

    dato = [
        Pattern("dato_dag_maaned_aar", rf"\b(?:[1-9]|0[1-9]|[12][0-9]|3[01])\.\s+(?:{MANEDER})\s+(?:(?:18|19|20)[0-9]{{2}}|[0-9]{{2}})\b", 0.8),
        Pattern("dato_dag_maaned_aar_tall", r"\b(?:1[0-9]|2[0-9]|3[01]|0?[1-9])\.(?:1[0-2]|0?[1-9])\.(?:(?:18|19|20)[0-9]{2}|[0-9]{2})\b", 0.5),
        Pattern("dato_maaned_aar", rf"\b(?:{MANEDER})\s+(?:18|19|20)[0-9]{{2}}\b", 0.4),
    ]
    fodt = [
        Pattern("fodselsaar_i_ar", r"(?<=\b(?:født|fødd|fødde)\s+(?:i\s+|(?:den\s+)?(?:\d{1,2}\.\s*)?(?:" + MANEDER + r")\s+)?)(?:18|19|20)[0-9]{2}\b", 0.6),
        Pattern("fodselsaar_f_punktum", r"(?<=\bf\.\s*)(?:18|19|20)[0-9]{2}\b", 0.5),
    ]
    ut = [
        _Telefon(supported_entity="NB_TELEFON", supported_language=sprak, patterns=[Pattern("telefon_siffer", SIFFERKANDIDAT, 0.5)],
                 name="NorskTelefonGjenkjenner"),
        _Fodselsnummer(supported_entity="NB_FODSELSNUMMER", supported_language=sprak, patterns=[Pattern("fodselsnummer_siffer", SIFFERKANDIDAT, 0.6)],
                       name="NorskFodselsnummerGjenkjenner"),
        PatternRecognizer(supported_entity="NB_DATO", supported_language=sprak, patterns=dato, name="NorskDatoGjenkjenner"),
        PatternRecognizer(supported_entity="NB_FODSELSAAR", supported_language=sprak, patterns=fodt, name="NorskFodselsaarGjenkjenner"),
    ]
    for entitet, navn in ORDLISTER.items():
        ut.append(PatternRecognizer(supported_entity=entitet, supported_language=sprak, name=f"Nokkelord_{navn}",
                                    patterns=[Pattern(f"nokkelord_{navn}", "|".join(_nokkelord_monster(o) for o in les_ordliste(navn)), 0.6)],
                                    global_regex_flags=re.IGNORECASE | re.DOTALL | re.MULTILINE))
    return ut


class NbBertGjenkjenner:
    """Presidio-gjenkjenner rundt NB-BERT-base-ner. Lages via `lag_bert_gjenkjenner` (importerer Presidio sent)."""


def lag_bert_gjenkjenner(sprak: str, rorledning=None, enhet: str = "cpu"):
    from presidio_analyzer import EntityRecognizer, RecognizerResult

    if rorledning is None:
        rorledning = lag_bert_rorledning(enhet)

    class _Gjenkjenner(EntityRecognizer):
        def load(self):  # modellen er allerede lastet
            pass

        def analyze(self, text, entities, nlp_artifacts=None):
            ut = []
            for e in rorledning(text):
                presidio = ETIKETT.get(e["entity_group"])
                if presidio and (not entities or presidio in entities):
                    ut.append(RecognizerResult(entity_type=presidio, start=int(e["start"]), end=int(e["end"]),
                                               score=float(e["score"]),
                                               recognition_metadata={RecognizerResult.RECOGNIZER_NAME_KEY: self.name,
                                                                     RecognizerResult.RECOGNIZER_IDENTIFIER_KEY: self.id}))
            return ut

    return _Gjenkjenner(supported_entities=["PERSON", "LOCATION", "ORGANIZATION"], supported_language=sprak,
                        name="NbBertNerGjenkjenner")


def lag_bert_rorledning(enhet: str = "cpu"):
    from transformers import pipeline

    return pipeline("token-classification", model=BERT_MODELL, aggregation_strategy="first", device=enhet)


def lag_motor(kilder=("spacy", "bert", "monster"), enhet: str = "cpu", nlp_motor=None, bert_rorledning=None):
    """Bygger en Presidio AnalyzerEngine. `kilder` velger gjenkjennere ("spacy", "bert", "monster"); standard er alle."""
    from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
    from presidio_analyzer.nlp_engine import NerModelConfiguration, SpacyNlpEngine

    if nlp_motor is None:
        modeller = [{"lang_code": s, "model_name": SPACY_MODELL} for s in SPRAK]
        ner = NerModelConfiguration(default_score=0.6, model_to_presidio_entity_mapping=dict(ETIKETT))
        nlp_motor = SpacyNlpEngine(models=modeller, ner_model_configuration=ner)
        nlp_motor.load()
    register = RecognizerRegistry(supported_languages=list(SPRAK))
    if "spacy" in kilder:
        register.load_predefined_recognizers(nlp_engine=nlp_motor, languages=list(SPRAK))
        # behold bare spaCy-gjenkjenneren og e-postgjenkjenneren (telefon er norsk mønster; Presidios PhoneRecognizer kjenner ikke norske nummer); resten er engelsk- eller land-spesifikke
        beholdt = {"SpacyRecognizer", "EmailRecognizer"}
        for r in list(register.recognizers):
            if r.name not in beholdt:
                register.remove_recognizer(r.name)
    for s in SPRAK:
        if "monster" in kilder:
            for r in monster_gjenkjennere(s):
                register.add_recognizer(r)
        if "bert" in kilder:
            if bert_rorledning is None:
                bert_rorledning = lag_bert_rorledning(enhet)
            register.add_recognizer(lag_bert_gjenkjenner(s, bert_rorledning))
    return AnalyzerEngine(nlp_engine=nlp_motor, registry=register, supported_languages=list(SPRAK))


def flagg_tekst(tekst: str, sprak: str = "nn", motor=None, terskel: float = 0.0) -> list[Flagg]:
    """Flagger kandidater til personopplysninger i en tekst. `sprak` er `nb` eller `nn`."""
    if sprak not in SPRAK:
        raise ValueError(f"Ukjent språk «{sprak}». Gyldige: {', '.join(SPRAK)}")
    motor = motor or lag_motor()
    resultater = motor.analyze(text=tekst, language=sprak, entities=list(KATEGORI), score_threshold=terskel)
    ut = []
    for r in resultater:
        kilde = (r.recognition_metadata or {}).get("recognizer_name", "")
        ut.append(Flagg(r.start, r.end, KATEGORI.get(r.entity_type, r.entity_type), kilde, float(r.score), tekst[r.start:r.end]))
    return sorted(ut, key=lambda f: (f.start, f.stopp, f.kategori, f.kilde))


def flagg_cues(cues, lag: str, sprak: str = "nn", motor=None, terskel: float = 0.0) -> list[Flagg]:
    """Flagger hver cue fra `transkriber.transkriber()`. Cuens tidskoder følger med i flaggene."""
    motor = motor or lag_motor()
    ut = []
    for c in cues:
        for f in flagg_tekst(c.tekst, sprak, motor, terskel):
            f.lag, f.cue_start, f.cue_stopp = lag, round(c.start, 3), round(c.stop, 3)
            tid = c.ord_tidsrom(f.start, f.stopp) if getattr(c, "ord", None) else None
            if tid:
                f.ord_start, f.ord_stopp = round(tid[0], 3), round(tid[1], 3)
            ut.append(f)
    return ut


@dataclass
class UnionFlagg:
    """Ett flagg etter sammenslåing av lagene. `start`/`stopp` er tidsgrensene (sek) som dekker begge lagenes cuer;
    hvert lags egne tegnposisjoner, utdrag, kilde, score og tidsgrenser ligger i `per_lag`."""
    kategori: str
    start: float
    stopp: float
    lag: str  # «ra», «normalisert» eller «begge»
    score: float  # høyeste score
    per_lag: dict = field(default_factory=dict)

    def som_dict(self) -> dict:
        return {"kategori": self.kategori, "start": round(self.start, 3), "stopp": round(self.stopp, 3),
                "lag": self.lag, "score": round(self.score, 3),
                "per_lag": {l: {k: (round(v, 3) if isinstance(v, float) else v) for k, v in d.items()}
                            for l, d in self.per_lag.items()}}


def _lag_info(f: Flagg) -> dict:
    d = {"utdrag": f.utdrag, "start": f.start, "stopp": f.stopp, "kilde": f.kilde, "score": f.score,
         "cue_start": f.cue_start, "cue_stopp": f.cue_stopp}
    if f.ord_start is not None:
        d["ord_start"], d["ord_stopp"] = f.ord_start, f.ord_stopp
    return d


TIDSTOLERANSE_S = 0.5  # DTW-tidsstempler fra to modeller stemmer ikke helt; ordgrensene kan avvike så mye


def _tidsrom(f: Flagg, ordtider: bool):
    if ordtider:
        return f.ord_start, f.ord_stopp
    return f.cue_start, f.cue_stopp


def _tid_overlapper(a: Flagg, b: Flagg) -> bool:
    """Ordspennene overlapper (med toleranse) når begge flagg har ordtidsstempler; ellers cuenes tidsrom."""
    ordtider = a.ord_start is not None and b.ord_start is not None
    (a0, a1), (b0, b1) = _tidsrom(a, ordtider), _tidsrom(b, ordtider)
    tol = TIDSTOLERANSE_S if ordtider else 0.0
    return a0 < b1 + tol and b0 < a1 + tol


def slaa_sammen_lag(flagg_per_lag: dict) -> list[UnionFlagg]:
    """Union av flagg fra lagene `ra` og `normalisert` (`{lag: [Flagg]}`).

    Samme kategori og overlappende tid parres til ett flagg, én-til-én. Tiden er flaggets **ordspenn** i hvert lag
    (fra DTW-ordtidsstempler, med en toleranse på 0,5 s); mangler ordtidsstempler brukes cuenes tidsrom. Likheten mellom
    utdragene brukes bare til å velge når flere flagg overlapper i tid (grådig, høyest likhet først). Ingen
    likhetsterskel og ingen terskel som fjerner flagg: et flagg uten partner beholdes som flagg for det ene laget.
    Med ordtidsstempler slås to ulike personer i samme segment ikke sammen, fordi de ikke overlapper i tid."""
    ra, nor = flagg_per_lag.get("ra", []), flagg_per_lag.get("normalisert", [])
    kandidater = []
    for i, a in enumerate(ra):
        for j, b in enumerate(nor):
            if a.kategori == b.kategori and _tid_overlapper(a, b):
                lik = difflib.SequenceMatcher(None, a.utdrag.lower(), b.utdrag.lower()).ratio()
                ordtider = a.ord_start is not None and b.ord_start is not None
                (a0, a1), (b0, b1) = _tidsrom(a, ordtider), _tidsrom(b, ordtider)
                kandidater.append((lik, -(abs(a0 - b0) + abs(a1 - b1)), i, j))
    brukt_a, brukt_b, par = set(), set(), []
    for lik, _, i, j in sorted(kandidater, reverse=True):
        if i not in brukt_a and j not in brukt_b:
            brukt_a.add(i); brukt_b.add(j); par.append((i, j))

    def union_tid(*fl):
        ordtider = all(f.ord_start is not None for f in fl)
        t = [_tidsrom(f, ordtider) for f in fl]
        return min(x[0] for x in t), max(x[1] for x in t)

    ut = []
    for i, j in par:
        a, b = ra[i], nor[j]
        t0, t1 = union_tid(a, b)
        ut.append(UnionFlagg(a.kategori, t0, t1, "begge", max(a.score, b.score), {"ra": _lag_info(a), "normalisert": _lag_info(b)}))
    for i, a in enumerate(ra):
        if i not in brukt_a:
            ut.append(UnionFlagg(a.kategori, *union_tid(a), "ra", a.score, {"ra": _lag_info(a)}))
    for j, b in enumerate(nor):
        if j not in brukt_b:
            ut.append(UnionFlagg(b.kategori, *union_tid(b), "normalisert", b.score, {"normalisert": _lag_info(b)}))
    return sorted(ut, key=lambda u: (u.start, u.stopp, u.kategori, u.lag))
