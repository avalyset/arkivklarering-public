---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0007: All prosessering lokalt; lyd forlater ikke institusjonen

Versjon 1.1, 2026-10-27 (v1.1: modellene som lastes ned, rettet etter koden: inaVAMOS er ikke lenger standard (KLAR-ADR-0019, AV-26), og NB-BERT-base-ner, inaSpeechSegmenters vekter og pyannote-modellen lastes ned første gang de brukes; Whisper-modellene og katalogmodellen lastes separat; beslutningen om lokal behandling er uendret; v1.0: første versjon).

## Kontekst

Opptakene inneholder personopplysninger og rettighetsbelagt musikk som ikke er klarert.

## Beslutning

All behandling (segmentering, transkripsjon, flagging, katalogutkast, talerinndeling) kjører lokalt. Lyd sendes ikke til skytjenester eller GitHub. Katalogutkastet går bare til en lokal ollama på loopback (`arkivklarering/katalog.py`: andre adresser avvises).

**Modeller (v1.1).** Det som lastes ned, er modellfiler; ingen lyd eller tekst sendes ut:

- **NB-BERT-base-ner** (personvernflaggene) hentes av `transformers` fra Hugging Face første gang (`arkivklarering/personvern.py`, `pipeline("token-classification", model=…)`) og lagres i `HF_HOME` under datarota (KLAR-ADR-0015).
- **inaSpeechSegmenters vekter** (standard segmentering) lastes ned fra GitHub-releases første gang og lagres under `$KERAS_HOME/inaSpeechSegmenter` (`arkivklarering/segment_inaseg.py`; `requirements-inaseg.lock`).
- **pyannote/speaker-diarization-community-1** (bare den valgfrie talerinndelingen, `--taler`) hentes fra Hugging Face av runneren (`arkivklarering/_diarisering_runner.py`, `Pipeline.from_pretrained` med `HF_TOKEN`; modellen er gated, og vilkårene godtas av brukeren på Hugging Face).
- **Katalogmodellen** (`hf.co/NbAiLab/borealis-open-4b-gguf:Q4_K_M`) lastes ned av brukeren med `ollama pull` (README «Installasjon»); koden laster den ikke ned.
- **Whisper-modellene** (`NbAiLab/nb-whisper-large-verbatim` og `NbAiLab/nb-whisper-large`, ggml) lastes ned separat av brukeren; koden laster dem ikke ned, men kontrollerer sha256 mot `modeller.lock.json` før bruk (`arkivklarering/transkriber.py`).
- **inaVAMOS** brukes ikke som standard. Den er bare det valgfrie tillegget `reproduksjon-h1h2` for å reprodusere H1 og H2 (KLAR-ADR-0019); med den lastes inaVAMOS' to modeller (ca. 80 MB) ned én gang.

## Konsekvenser

Krever maskinvare lokalt og begrenser modellvalg til det som kan kjøres der. Lyd fra museet kommer aldri inn i git. Første oppsett og første kjøring trenger nettverk for modellnedlasting (listen over).

## Alternativer som ble vurdert

- Skytranskripsjon: forkastet; lyden ville forlate institusjonen.
- Institusjonens egen tjeneste: ikke vurdert videre.
