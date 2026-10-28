# arkivklarering [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23723666.svg)](https://doi.org/10.5281/zenodo.23723666)

Klarering **før** publisering av norske lokalradio- og fortellerarkiv: verktøyet foreslår hva et menneske må vurdere (personopplysninger, musikkrettigheter) før et opptak publiseres. **Mennesket avgjør alt; verktøyet foreslår.** Søkbarhet er en bieffekt, ikke målet. Alt kjører lokalt, og lyd forlater ikke maskinen. Privat repo; metoden og prioriteten er registrert på OSF: <https://osf.io/fbme7/> (under embargo til 2027-10-26; status sett i innlogget OSF-økt 2026-10-27, kan ikke etterprøves offentlig før embargoen oppheves).

Utdata er **utkast og maskinforslag**, ikke en klarering. Verktøyet fjerner og endrer ingenting.

## Behov: hvem trenger hva

Norske lokalradio- og fortellerarkiv kan ikke publiseres før hvert opptak er klarert for personopplysninger og tredjeparts musikkrettigheter. Klareringen gjøres i dag ved at ansatte og frivillige lytter gjennom hver time, og for arkiv på tusenvis av timer er lyttingen flaskehalsen, ikke digitalisering eller transkripsjon ([KLAR-ARK-0001](docs/KLAR-ARK-0001_arkivklarering_arkitektur_v1.10_2026-10-28.md) § 1).

arkivklarering er for dem som klarerer slike opptak (arkiv, museer og frivillige som lytter gjennom). Det kjører på egen maskin og lager forslag med tidskode til hva et menneske bør lytte på og vurdere: hvor det er tale og musikk, en transkripsjon i to lag, personvernflagg og et utkast til katalogpost, eksportert til arkivformater (WebVTT, OHMS XML, IIIF, MMIF). **Forholdet til annet arbeid** (sitat og lagret kopi for hver kilde i [KLAR-KILDE-0001](docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.20_2026-10-28.md), kilde-ID og rad i parentes): Beslektede arkivprosjekter bruker talegjenkjenning på radio- og TV-samlinger for søk eller berikelse: Kungliga bibliotekets Mediesök lar brukerne søke i KI-transkribert tekst fra radiosamlingene (K71, RG-01), et prosjekt ved Det Kgl. Bibliotek tar sikte på ASR for tekstsøk i radio- og TV-arkivet (K72, RG-02a), og NISVs samling berikes med ASR-transkripsjoner (K73, RG-02b, sekundærkilde). arkivklarering tar steget før: om noe kan publiseres i det hele tatt. Den nærmeste åpne plattformen er CLAMS, utviklet ved Brandeis University i samarbeid med GBH Archives og åpen kildekode (K09, CL-01 og CL-05b); MMIF, formatet CLAMS-apper overfører analyseresultater i (K10, CL-04), skrives her som eksport, men komponentene er ikke CLAMS-apper og utveksler ennå ikke data via MMIF ([KLAR-ADR-0003](docs/adr/KLAR-ADR-0003_arkivklarering_mmif-internt-format_v1.2_2026-10-27.md)). AMP kombinerer automatiske mekanismer med menneskelig arbeid (K05, AM-01); her skal hvert menneskelig steg bli et eksplisitt godkjenningspunkt, men godkjenningsflaten er ikke bygget. Nunn Centers SpeakEZ lager råtranskript med Whisper og utkast til OHMS-indeks, men er et lukket, internt system (K16, NU-01 og NU-03); arkivklarering bruker det som modell, ikke som komponent, og eksporterer OHMS XML. FIX IT+ er en crowdsourcing-plattform der brukere retter maskingenererte transkripsjoner linje for linje mens de lytter (K17, AA-01); arkivklarering har ennå ingen rette- eller godkjenningsflate. Personvernflaggene bygger på Presidio (K27, PR-01) med bokmålsoppsettet fra CLEANUP-guiden til NR og NAV (K26, PR-03; K28, PR-05 og PR-06) og på NB-BERT-base-ner, som er finjustert på NorNE (K23, NB-01). Det arkivklarering legger til, er klareringslogikken rundt disse komponentene (flagg på begge transkripsjonslag, slått sammen uten terskel, og disposisjon per segment) og den preregistrerte målingen av den (se «Resultater»).

- **Det er:** et lokalt verktøy som gir maskinforslag til menneskelig vurdering ([KLAR-ADR-0002](docs/adr/KLAR-ADR-0002_arkivklarering_klarering-foer-publisering_v1.0_2026-10-26.md), [KLAR-ADR-0007](docs/adr/KLAR-ADR-0007_arkivklarering_lokal-prosessering_v1.1_2026-10-27.md)).
- **Det er ikke:** en klarering. Det avgjør ikke at noe er klarert eller fritt for personopplysninger, og et manglende flagg er ikke en garanti ([KLAR-ARK-0001](docs/KLAR-ARK-0001_arkivklarering_arkitektur_v1.10_2026-10-28.md) § 3.2). Det har ennå ingen menneskelig godkjenningsflate og ingen alias-tabell ([KLAR-ARK-0006](docs/KLAR-ARK-0006_arkivklarering_veikart_v1.13_2026-10-28.md), «Etter v1.0»), og det er ikke målt på ekte arkivlyd (se «Resultater»).

## Hva verktøyet gjør

1. **Segmentering** (standard: inaSpeechSegmenter 0.8.0; valgfritt: inaVAMOS, bare for å reprodusere H1 og H2): `speech`, `music` og `other` (bare inaVAMOS gir i tillegg `speech+music`). Bare `speech` og `speech+music` transkriberes; `music` merkes «foreslått klipp» og går aldri til Whisper ([KLAR-ADR-0004](docs/adr/KLAR-ADR-0004_arkivklarering_segmentregel_v1.5_2026-10-28.md), [KLAR-ADR-0019](docs/adr/KLAR-ADR-0019_arkivklarering_inaseg-erstatning_v1.6_2026-10-28.md)).
2. **Transkripsjon i to lag** (NB-Whisper large via whisper.cpp): rålag (verbatim, kjørt med `-nt`) og normalisert lag, begge med DTW-ordtidsstempler ([KLAR-ADR-0005](docs/adr/KLAR-ADR-0005_arkivklarering_to-lag-nb-whisper-large_v1.3_2026-10-28.md), [KLAR-ADR-0017](docs/adr/KLAR-ADR-0017_arkivklarering_nt-for-raalaget_v1.1_2026-10-28.md)).
3. **Personvernflagg** (Presidio med spaCy `nb_core_news_md`, NB-BERT-base-ner, mønstre og nøkkelordlister i `vokabular/`), på begge lag, slått sammen til én liste (union) uten terskel ([KLAR-ADR-0008](docs/adr/KLAR-ADR-0008_arkivklarering_personvernflagg-presidio-nbbert_v1.3_2026-10-27.md), [KLAR-ADR-0012](docs/adr/KLAR-ADR-0012_arkivklarering_recall-foran-presisjon_v1.4_2026-10-28.md)).
4. **Katalogutkast** per sending (lokal ollama; tittel, dato hvis den nevnes, talere, steder, 3–8 emneord, sammendrag per segment med tidskode), merket «utkast – maskinforslag» ([KLAR-ADR-0013](docs/adr/KLAR-ADR-0013_arkivklarering_katalogmodell_v1.1_2026-10-28.md)). Forslag som ikke står i teksten forkastes og logges. Ikke validert (se «Begrensninger»).
5. **Eksport:** WebVTT per lag, `segments.json`, OHMS XML (validert i testene, ikke ved kjøring, mot den arkiverte `ohms.xsd` v5.4 fra Wayback Machine; eksempelfilene vi har (`ohms_xml_samples.zip`, opphav ikke dokumentert) validerer ikke mot den XSD-en; den nyeste versjonen på Wayback er 6.0 (fra juli 2025), og vi validerer mot 5.4), IIIF Presentation 3-manifest (transkripsjon som `supplementing`-merknader, IIIF Cookbook 0231/0219) og MMIF (`mmif-python`). Hvert format har en test; WebVTT har bare en parserkontroll, siden det ikke finnes noe skjema.

Valgfritt: anonym talerinndeling (TALER_1, TALER_2 …) med pyannote ([KLAR-ADR-0016](docs/adr/KLAR-ADR-0016_arkivklarering_talerinndeling-pyannote_v1.1_2026-10-28.md)). Ingen identifisering og ingen stemmegjenkjenning mot kjente personer.

### Moduler

Hver modul i tabellen har en docstring som beskriver hva den gjør; tabellen er en oversikt.

| modul | hva den gjør | beslutning |
|---|---|---|
| `arkivklarering/cli.py` | Kommandolinjen: lydfil inn, segmentering, to transkripsjonslag ett pass om gangen, personvernflagg, katalogutkast og eksport ut | – |
| `arkivklarering/segment.py` | Velger segmentør med `ARKIVKLARERING_SEGMENTERING` (`inaseg` standard, `inavamos` valgfritt); `bygg_tidslinje` gir hvert segment en disposisjon («transkriber», «foreslått klipp», «ingen handling», «menneskelig vurdering»), slår sammen tale over gap på høyst `--bro-s` og sender tale kortere enn `--min-s` til menneskelig vurdering | ADR-0004, ADR-0019 |
| `arkivklarering/segment_inaseg.py`, `_inaseg_runner.py` | inaSpeechSegmenter i eget venv som subprosess (JSON inn og ut); etikettkart `speech`/`male`/`female` → `speech`, `music` → `music`, `noise`/`noEnergy` → `other` | ADR-0019 |
| `arkivklarering/transkriber.py` | whisper.cpp med to NB-Whisper-modeller, sha256-kontroll mot `modeller.lock.json`; sender bare tale til Whisper | ADR-0005, ADR-0017 |
| `arkivklarering/personvern.py` | Presidio (`nb`/`nn`) med spaCy, NB-BERT-base-ner, mønstre (dato, fødselsår, telefon, fødselsnummer) og `vokabular/sensitivt_*.txt`; flagg per lag og union på tvers av lag | ADR-0008, ADR-0012 |
| `arkivklarering/katalog.py` | Katalogutkast via lokal ollama (standard `hf.co/NbAiLab/borealis-open-4b-gguf:Q4_K_M`); forkaster forslag som ikke står i teksten | ADR-0013 |
| `arkivklarering/diarisering.py`, `_diarisering_runner.py` | Talerinndeling med `pyannote/speaker-diarization-community-1` i eget venv (`--taler`) | ADR-0016 |
| `arkivklarering/eksport.py` | Skriver og validerer WebVTT, `segments.json`, OHMS XML, IIIF Presentation 3 og MMIF | ADR-0003, ADR-0009 |
| `arkivklarering/evaldata.py` | Sperre for testdelene av evalueringsdataene: åpnes bare med `--prereg-id KLAR-PREREG-<NNNN>` for en registrert preregistrering | PREREG-0001 |
| `arkivklarering/miljo.py` | Datarota `ARKIVKLARERING_DATA` (standard Vault når montert, ellers `~/.local/share/arkivklarering`); setter manglende cache- og tmp-variabler under rota og avbryter hvis de peker utenfor | ADR-0015 |
| `arkivklarering/kalibrering.py` | Scoring av flagg mot et manus (justeringsmanus; testmanuset er sperret) | ADR-0014 |
| `arkivklarering/h4_innlesing.py`, `h4_side.html` | Innleser for H4 (låst rigg, ingen visning av resultater) | ADR-0018 |
| `arkivklarering/entiteter.py` | Stubb: deterministisk alias-tabell er planlagt, ikke bygget | ADR-0006 |
| `arkivklarering/_vendor/norsk_tale/` | Uendret kopi av `norm.py` og `score.py` fra norsk-tale (opphav i `ORIGIN.txt`) | ADR-0014 |

## Avhengigheter

- **Systemprogrammer:** `ffmpeg` (med `ffprobe`), `whisper-cli` ([whisper.cpp](https://github.com/ggml-org/whisper.cpp)) og, for katalogutkastet, en lokal [ollama](https://ollama.com).
- **Modeller (lastes separat, ligger aldri i repoet):** to ggml-modeller, `NbAiLab/nb-whisper-large-verbatim` og `NbAiLab/nb-whisper-large`, med forventet sha256 og stier i `modeller.lock.json` (koden laster ikke ned Whisper-modellene); spaCy-modellen `nb_core_news_md` 3.8.0; NB-BERT-base-ner hentes av `transformers` fra Hugging Face; inaSpeechSegmenters vektfil lastes ned fra GitHub-releases første gang og lagres under `$KERAS_HOME/inaSpeechSegmenter` (`requirements-inaseg.lock`, linje 4); pyannote-modellen er gated på Hugging Face og krever `HF_TOKEN` i `.env`. `.gitignore` holder `modeller/`, `lyd/`, `ut/`, `eval/data/` og lydfiler utenfor git.
- **Python:** `requires-python = ">=3.11"` (`pyproject.toml`); venvene på Vault er bygd med Python 3.13 (`requirements.lock` linje 1, `requirements-inaseg.lock` linje 2).
- **Kjerne og tillegg (`pyproject.toml`):** kjernen har ingen påkrevde pakker (`dependencies = []`). Tilleggene er `test` (pytest), `eval` (jiwer), `tidsstempel` (opentimestamps-client), `eksport` (lxml, mmif-python, iiif-prezi3, webvtt-py), `personvern` (presidio-analyzer, spacy, transformers, torch, pyarrow) og `reproduksjon-h1h2` (inaVAMOS, bare for å reprodusere H1 og H2; se «Begrensninger»). En full kjøring av `arkivklarering` trenger i praksis `eksport` (OHMS, IIIF og MMIF skrives alltid) og `personvern` (med mindre `--ingen-personvern`).
- **Egne venv (TensorFlow og pyannote holdes utenfor analysemiljøet):** inaSpeechSegmenter 0.8.0 med TensorFlow i `$ARKIVKLARERING_DATA/venv-inaseg` (`requirements-inaseg.lock`); pyannote.audio i `$ARKIVKLARERING_DATA/venv-diarisering` (`requirements-diarisering.lock`). Degraderingssteget i DEV-evalueringen har sitt eget (`requirements-degradering.lock`).
- **Låste miljøer:** alle `requirements*.lock` har sha256 for hver distribusjon. `requirements.lock` er analysemiljøet som H1 og H2 ble kjørt i, og inneholder `inavamos==0.1.1` (linje 547).

## Installasjon

Alt tungt (venv, cacher, modeller, evalueringsdata, lyd) ligger under én datarot, `ARKIVKLARERING_DATA` ([KLAR-ADR-0015](docs/adr/KLAR-ADR-0015_arkivklarering_tunge-data-kun-paa-vault_v1.1_2026-10-27.md); `arkivklarering/miljo.py`, `scripts/miljo.sh`). Er variabelen ikke satt, er standarden `/Volumes/Vault/arkivklarering` når Vault er montert og mappen finnes, ellers `${XDG_DATA_HOME:-~/.local/share}/arkivklarering`, som opprettes. En satt `ARKIVKLARERING_DATA` som ikke finnes, eller som ligger under et umontert `/Volumes/<disk>`, gir stopp (exit 3) og opprettes ikke. `source scripts/miljo.sh` setter de avledede variablene under rota, `HF_HOME` (`cache/hf`), `HF_DATASETS_CACHE` (`cache/hf/datasets`), `PIP_CACHE_DIR` (`cache/pip`), `TORCH_HOME` (`cache/torch`), `KERAS_HOME` (`cache/keras`), `XDG_CACHE_HOME` (`cache`) og `TMPDIR` (`tmp`), og stopper hvis `HF_HOME`, `HF_DATASETS_CACHE`, `TMPDIR` eller `XDG_CACHE_HOME` peker utenfor rota. Python-skriptene og testene gjør det samme selv (`krev_miljo()`). Evalueringsdataene ligger i `$ARKIVKLARERING_DATA/eval-data`; `ARKIVKLARERING_EVAL_DATA` overstyrer bare den (brukes av `scripts/reproduser.sh --uten-cache`).

```bash
source scripts/miljo.sh                                   # datarot og cacher/tmp under ARKIVKLARERING_DATA, avbryter ellers
uv venv --python 3.13 "$ARKIVKLARERING_DATA/venv" && ln -s "$ARKIVKLARERING_DATA/venv" .venv
VIRTUAL_ENV=$PWD/.venv uv pip install -e ".[test,eval,personvern,eksport,tidsstempel]" \
  "nb_core_news_md @ https://github.com/explosion/spacy-models/releases/download/nb_core_news_md-3.8.0/nb_core_news_md-3.8.0-py3-none-any.whl"

# standard segmentering (inaSpeechSegmenter) i eget venv; kommandoene står i toppen av låsfila
uv venv --python 3.13 "$ARKIVKLARERING_DATA/venv-inaseg"
VIRTUAL_ENV="$ARKIVKLARERING_DATA/venv-inaseg" uv pip install --require-hashes --no-deps -r requirements-inaseg.lock

# formattestene: OHMS-skjemaet (KLAR-KILDE-0001 K34) og IIIF-oppskrift 0219 (K33) under datarota; uten dem hoppes fire tester over
curl -fL --create-dirs -o "$ARKIVKLARERING_DATA/eval-data/ohms/ohms.xsd" https://web.archive.org/web/20240830153336id_/https://www.weareavp.com/nunncenter/ohms/ohms.xsd
echo "78e7fe404d7eed05027f165339663a0595f49609f3998ac2e8357c6f0bf9385c  $ARKIVKLARERING_DATA/eval-data/ohms/ohms.xsd" | shasum -a 256 -c
git clone --depth 1 https://github.com/IIIF/cookbook-recipes "$ARKIVKLARERING_DATA/tmp/cookbook-recipes"
mkdir -p "$ARKIVKLARERING_DATA/eval-data/iiif" && cp "$ARKIVKLARERING_DATA/tmp/cookbook-recipes/recipe/0219-using-caption-file/manifest.json" "$ARKIVKLARERING_DATA/eval-data/iiif/recept_0219_manifest.json"
ollama pull hf.co/NbAiLab/borealis-open-4b-gguf:Q4_K_M         # katalogmodellen (arkivklarering/katalog.py:21); uten den hoppes katalogutkastet over
```

Låst analysemiljø i stedet for tilleggene: `uv pip install --require-hashes --no-deps -r requirements.lock` i et venv under `$ARKIVKLARERING_DATA`; spaCy-modellen og repoet selv (`pip install -e .`) ligger utenfor låsen (`requirements.lock`, linje 1–3). Talerinndelingen: `uv pip install --require-hashes --no-deps -r requirements-diarisering.lock` i `$ARKIVKLARERING_DATA/venv-diarisering` (linje 1–2 i låsfila). Whisper-modellene ligger i `$ARKIVKLARERING_DATA/modeller/` (`standardsti` i `modeller.lock.json` er relativ til rota). Koden laster dem ikke ned: hent `fil` (`ggml-model.bin`) fra hvert av Hugging Face-repoene som står som `repo` i `modeller.lock.json` (`NbAiLab/nb-whisper-large-verbatim` for rålaget og `NbAiLab/nb-whisper-large` for det normaliserte laget) og legg filene på `standardsti`; de kontrolleres mot `sha256` i samme fil før bruk. `ffmpeg`, `whisper-cli` og ollama installeres separat (se «Avhengigheter»); kommandoene over installerer Python-miljøene, henter skjemaet og oppskriften formattestene leser og katalogmodellen. Testene leser `ohms.xsd` fra `$ARKIVKLARERING_DATA/eval-data/ohms/` (eller `ARKIVKLARERING_OHMS_XSD`) og oppskriften fra `$ARKIVKLARERING_DATA/eval-data/iiif/` (`arkivklarering/eksport.py:114`, `tests/test_eksport_formater.py:19`; `ARKIVKLARERING_EVAL_DATA` overstyrer `eval-data`). Fila fra `cookbook-recipes` har malfeltene `{{ id.url }}` og `{{ id.path }}`, som testen fyller ut; kopien testene er kjørt med på Vault har sha256 `746e7561…`, og repoet kan ha endret seg siden.

Miljøvariabler:

| variabel | verdi | kilde |
|---|---|---|
| `ARKIVKLARERING_DATA` | Datarota for alt tungt; standard `/Volumes/Vault/arkivklarering` når Vault er montert og mappen finnes, ellers `${XDG_DATA_HOME:-~/.local/share}/arkivklarering` | `arkivklarering/miljo.py:40–53`, `scripts/miljo.sh:9–17` |
| `ARKIVKLARERING_EVAL_DATA` | Evalueringsdata og cacher; standard `$ARKIVKLARERING_DATA/eval-data` | `arkivklarering/miljo.py:57` |
| `ARKIVKLARERING_SEGMENTERING` | `inaseg` (standard, også når variabelen mangler) eller `inavamos` (valgfritt, bare for å reprodusere H1 og H2; krever tillegget `reproduksjon-h1h2`). Andre verdier gir feil. | `arkivklarering/segment.py:65–67`, `:82–91` |
| `ARKIVKLARERING_INASEG_PYTHON` | Python i inaseg-venvet; standard `$ARKIVKLARERING_DATA/venv-inaseg/bin/python` | `arkivklarering/segment_inaseg.py:27` |
| `KERAS_HOME` | Hvor inaSpeechSegmenters vekter lagres; settes til `$ARKIVKLARERING_DATA/cache/keras` for runner-prosessen hvis den ikke er satt | `arkivklarering/segment_inaseg.py:64–67` |
| `ARKIVKLARERING_WHISPER` | Sti til `whisper-cli` når `--whisper` ikke er gitt (`--whisper` går foran); ellers `whisper-cli` på PATH eller `~/whisper.cpp/build/bin/whisper-cli` | `arkivklarering/transkriber.py:107–113` |
| `ARKIVKLARERING_DIARISERING_PYTHON` | Python i pyannote-venvet; standard `$ARKIVKLARERING_DATA/venv-diarisering/bin/python` | `arkivklarering/diarisering.py:20` |

Cacher med tidslinje (segmenteringen lagret sammen med Whisper-utdata, under `$ARKIVKLARERING_DATA/eval-data`) får navn etter segmentøren: `<navn>_inaseg.jsonl` eller `<navn>_inavamos.jsonl`, så tidslinjer fra de to aldri blandes. Eldre cacher uten suffiks (`<navn>.jsonl`, alle fra før 27.10.2026) er laget med inaVAMOS og leses bare når `ARKIVKLARERING_SEGMENTERING=inavamos` og `_inavamos`-fila mangler; med `inaseg` leses de aldri (`eval/dev/felles.py:182–200`).

`scripts/kjor_testdel.sh` setter selv `ARKIVKLARERING_SEGMENTERING=inavamos` for H1 og H2 og `inaseg` for H4.

## Bruk

```bash
source scripts/miljo.sh
.venv/bin/python scripts/lag_testlyd.py                   # lager lyd/rokytest.wav: 20 s syntetisk musikk + 20 s norsk TTS-tale; krever macOS (`say -v Nora`)
.venv/bin/arkivklarering lyd/rokytest.wav -o ut/rokytest/
.venv/bin/arkivklarering lyd/rokytest.wav -o ut/rokytest_enkel/ --ingen-katalog --ingen-personvern   # uten ollama og uten flagg, egen utkatalog
```

`scripts/lag_testlyd.py --personvern` lager `lyd/rokytest_personvern.wav` med en tekst som har navn, sted, fødselsår, sykdom, parti og telefonnummer. Begge lydfilene lages med `say -v Nora` og krever macOS med den norske stemmen. `lyd/` og `ut/` er ikke i git.

Flagg (`.venv/bin/python -m arkivklarering --help`): `-o/--ut` (utkatalog, standard `ut`), `--sprak` (whisper-språk for begge lag, standard `nn`), `--enhet` (torch-enhet; gjelder bare `inavamos`), `--bro-s` (standard 1,0 s), `--min-s` (standard 0,5 s), `--whisper`, `--modell-ra`, `--modell-normalisert`, `--ingen-personvern`, `--taler` (pyannote; krever `HF_TOKEN` og `venv-diarisering`), `--ingen-katalog`, `--katalogmodell` og `--ingen-ordtider`.

Utdata per lydfil `<navn>` (`arkivklarering/cli.py:86–126`): `<navn>.ra.vtt`, `<navn>.normalisert.vtt`, `<navn>.segments.json`, `<navn>.ohms.xml`, `<navn>.iiif.json` og `<navn>.mmif.json`. Alle seks ble laget i hver av tre kjøringer (de to over og `rokytest_personvern.wav`) i en ren klon av `9ded8d8` 2026-10-27 (inaSpeechSegmenter). De 15 filene i WebVTT, OHMS XML, IIIF og MMIF validerte med repoets validatorer (`eksport.valider_vtt`, `valider_ohms`, `valider_iiif` og `valider_mmif` i `arkivklarering/eksport.py`); de tre `segments.json` fikk en egen feltkontroll av feltene under (det finnes ingen validator for dem), med 2 OK og 1 med ventet avvik: i kjøringen med `--ingen-personvern` mangler `personvern`, som det skal ([KLAR-LOG-0001](docs/KLAR-LOG-0001_arkivklarering_avvik-og-hendelser_v1.53_2026-10-28.md), «Verifikasjon av installasjon, funksjon og ytelse fra ren klon»). Utdrag av `rokytest_personvern.ra.vtt` fra den kjøringen, med NOTE-linjen slik koden skriver den fra `testkjoring-v8` (på `9ded8d8` sto det «Tale med musikk under er transkribert og flagget.», som ikke stemmer med inaSpeechSegmenter; KLAR-ADR-0019):

```text
WEBVTT - arkivklarering v1.0.0 - ra

NOTE Maskinforslag til menneskelig vurdering. Ikke en klarering. Ren musikk og annet er ikke transkribert; «foreslått klipp» er ikke utført. Tale med musikk under transkriberes bare når segmenteringen merker den som tale; flagget «musikk under tale» lages bare med inaVAMOS (ADR-0019).

1
00:00:20.180 --> 00:00:28.420
ho heite kari nordmann og vart fødd i 1972 i volda ho var sjuk og gjekk i arbeiderpartiet ring nummeret 68
```

`segments.json` har på toppnivå `versjon`, `kilde`, `merknad`, `lag` (modell, sha256 og språk per lag) og `segmenter`, og `personvern` når personvern kjøres (ikke med `--ingen-personvern`; `arkivklarering/eksport.py:81`). Hvert segment har `label`, `start`, `stopp` og `disposisjon` (`music` → «foreslått klipp», `other` → «ingen handling»); transkriberte segmenter har i tillegg `tekst` og, når personvern kjøres, `personvern` per lag og `personvern_union`.

## Tester

```bash
source scripts/miljo.sh
.venv/bin/python -m pytest -q -m 'not tung'               # raske tester (standard i pyproject.toml);  -m tung  for testene som kjører Whisper
```

Dagens tall (2026-10-28, målt på koden i `testkjoring-v10` (`efce3f4`); utgivelsescommiten endrer bare dokumenter): innsamling (`.venv/bin/python -m pytest -m 'not tung' --co -q`) gir 216 av 219 tester, 3 merket `tung`. Med en tom `ARKIVKLARERING_DATA`: 212 bestått, 4 hoppet over (OHMS-skjemaet og IIIF-oppskrift 0219 mangler under en tom datarot) og 3 utvalgt bort (`tung`). Med stegene for formattestene i «Installasjon» (`ohms.xsd`, oppskrift 0219, katalogmodellen) kjørt i en ny, tom datarot kjører de fire: `tests/test_eksport_formater.py` og `tests/test_diarisering.py` ga 12 bestått og 4 hoppet over før stegene og 16 bestått etter ([KLAR-LOG-0001](docs/KLAR-LOG-0001_arkivklarering_avvik-og-hendelser_v1.53_2026-10-28.md), «F11: installasjonsstegene for formattestene i en ny datarot»). Med datarota på Vault: 216 bestått, 3 utvalgt bort. Ren installasjon fra en ny klon av `9ded8d8` (`testkjoring-v7`) med kommandoene i «Installasjon» (med nett; `venv` og `venv-inaseg` under en ny datarot, Whisper-modellene kontrollert mot sha256 i `modeller.lock.json`): med en tom `ARKIVKLARERING_DATA` 206 bestått, 4 hoppet over og 3 utvalgt bort (`testkjoring-v8` har én test til); `-m tung` med datarota gir 3 bestått ([KLAR-LOG-0001](docs/KLAR-LOG-0001_arkivklarering_avvik-og-hendelser_v1.53_2026-10-28.md), «Verifikasjon av installasjon, funksjon og ytelse fra ren klon»). Testene går i et rent miljø: `tests/conftest.py` kaller `krev_miljo()`, som setter cacher og tmp under datarota, og tester som trenger data under rota (evalueringsdata, modeller, `venv-inaseg`), nett eller Vault hoppes over med en grunn. Det er ingen CI i repoet; testene kjøres lokalt.

## Resultater

### Testdelene (preregistrert, OSF hc83q)

Kjørt én gang hver via `scripts/kjor_testdel.sh` 2026-10-27. Testdelene er offentlige datasett, ikke arkivlyd. Tallene er de preregistrerte målingene fra testkjøringene (kodetagg `testkjoring-v2`; H1 og H2 segmentert med inaVAMOS, H3 er tekst uten segmentering). De er gjenberegnet fra de lagrede utdataene i `eval/test/` med `scripts/rapporter_intervaller.py` på `9ded8d8` 2026-10-27 og stemmer (KLAR-LOG-0001, oppføringen «Verifikasjon …» fra v1.44, nyeste v1.48, F13). H1 og H2 kan ikke kjøres på nytt med standardsegmentøren (inaSpeechSegmenter) uten å bli en annen måling, og det er ingen påstand her om at rørledningen i v1.0 gir disse tallene.

| hypotese | resultat | dokument |
|---|---|---|
| H1, NB Samtale test (252 segmenter, 51 talere) | H1a (primær) rålag/matchet WER **0,127** (95 % 0,112–0,144) mot terskel ≤ 0,25: bekreftet, klart. H1b, H1d og H1e (sekundære) bekreftet, klart. | [KLAR-EVAL-0013](eval/test/KLAR-EVAL-0013_arkivklarering_test-nbsamtale-wer_v1.3_2026-10-27.md) |
| H2, NPSC test (flaggoverlevelse, union) | H2a–H2e (primære) alle bekreftet av punktestimatet; H2c (person, bokmål, 0,935) er ikke klar (nedre Wilson-grense 0,885 < 0,90), og H2b (sted, 0,856) er klar med 0,0005. | [KLAR-EVAL-0014](eval/test/KLAR-EVAL-0014_arkivklarering_test-flaggoverlevelse-npsc_v1.4_2026-10-27.md) |
| H3, NorNE test (navnegjenkjenning, sekundær) | Alle åtte terskler bekreftet av punktestimatet; fem klart etter Wilson, tre ikke klart (H3d recall og presisjonen i H3b og H3c). | [KLAR-EVAL-0015](eval/test/KLAR-EVAL-0015_arkivklarering_personvern-test_v1.5_2026-10-28.md) |
| H4, menneskeinnlest testmanus | Gjennomføres ikke i v1.0 (AV-27; Eiriks beslutning 2026-10-27; veikartet steg 13–14 utgår). Blindtesten på NB Tale modul 3 er planlagt som v1.1 (KLAR-PREREG-0003). | [KLAR-ARK-0006](docs/KLAR-ARK-0006_arkivklarering_veikart_v1.13_2026-10-28.md) |

Avvik fra planen står i [KLAR-LOG-0003](docs/KLAR-LOG-0003_arkivklarering_avvikstabell_v1.22_2026-10-28.md) (AV-01–AV-34) og i [KLAR-PREREG-0001](docs/KLAR-PREREG-0001_arkivklarering_testdeler_v1.33_2026-10-28.md) («Avvik etter registrering»).

### Utviklingsresultater (DEV, ikke pilot)

DEV-målinger på valideringsdeler av offentlige datasett (og én syntetisk kalibrering). De sier ikke noe om kvalitet på arkivlyd. Les dokumentene for oppsett, intervaller og forbehold. Tallene er fra nyeste versjon (etter at rålaget fikk `-nt`); oppsett og begrensninger står i versjonen før. Tallene er målinger fra utviklingsarbeidet (segmentering inaVAMOS), ikke fra rørledningen i v1.0; tallene for WER, navnegjenkjenning og flaggoverlevelse er gjenberegnet fra de lagrede utdataene med `scripts/rapporter_intervaller.py` på `9ded8d8` 2026-10-27 og stemmer, og 198 av 244 i den syntetiske kjeden er summert fra JSON-fila (skriptet har ikke det formatet) (KLAR-LOG-0001, oppføringen «Verifikasjon …» fra v1.44, nyeste v1.48).

| måling | resultat | dokument |
|---|---|---|
| WER, NB Samtale validation, 60 segmenter | korpus-WER totalt: rålag 0,135 (språk etter målform) og 0,248 (`-l nn`); normalisert lag 0,348 og 0,463 | [KLAR-EVAL-0002](eval/dev/KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.1_2026-10-27.md) |
| Navnegjenkjenning, NorNE validation (hele motoren, original tekst) | recall (overlapp): bokmål person 0,997, sted 0,970; nynorsk person 0,954, sted 0,986. Med små bokstaver uten tegnsetting: 0,715, 0,739, 0,599, 0,504 | [KLAR-EVAL-0005](docs/KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_2026-10-26.md) |
| Flaggoverlevelse, NB Samtale validation (60 segmenter) | union: person 14 av 17, sted 14 av 14 (n er liten) | [KLAR-EVAL-0006](docs/KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.2_2026-10-27.md) |
| Flaggoverlevelse, NPSC validation (934 segmenter, 1,97 t) | union, begge målformer: person 139 av 150 (0,927), sted 92 av 102 (0,902); nynorsk sted bare 22 referanseflagg | [KLAR-EVAL-0007](docs/KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.1_2026-10-27.md) |
| **SYNTETISK – kjede og flagglogikk, ikke talekvalitet** (TTS, 156 setninger) | flagg-treff i union 198 av 244 elementer før `-nt` (v1.1); etter `-nt` endret bare enkeltelementer; e-post 0 av 12 | [KLAR-EVAL-0008](docs/KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.5_2026-10-28.md) |
| Whisper på stillhet, støy og musikk (syntetisk lyd) | ingen prosa; begge lag skrev spesialtokenet `<\|nocaptions\|>` (før `-nt` skrev rålaget «.») | [KLAR-EVAL-0001](docs/KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v1.5_2026-10-28.md) |

## Begrensninger

Kort, med henvisning til kontrollpunktene:

- **inaVAMOS brukes ikke lenger.** inaVAMOS har Pantagruel Research-only License (art. 1 begrenser lisenstakere, art. 3 forbyr bruk i kommersiell aktivitet) og ble brukt i H1, H2 og DEV-arbeidet; EcoDecos dekning under lisensen er uavklart. Fra 2026-10-27 brukes den ikke; den er bare et valgfritt tillegg (`reproduksjon-h1h2`) for å reprodusere H1 og H2, som står som preregistrert (AV-25 og AV-26 i [KLAR-LOG-0003](docs/KLAR-LOG-0003_arkivklarering_avvikstabell_v1.22_2026-10-28.md)). `requirements.lock` inneholder den (se «Avhengigheter»).
- **Vektlisensen til inaSpeechSegmenter er uklar.** Koden er MIT; ingen kilde oppgir en egen lisens for vektene, og den er ikke avklart med INA ([KLAR-ADR-0019](docs/adr/KLAR-ADR-0019_arkivklarering_inaseg-erstatning_v1.6_2026-10-28.md), «Vektlisensen» og «Åpne punkter»).
- **«Musikk under tale» bortfaller.** inaSpeechSegmenter har ingen klasse for tale over musikk; med alternativ A blir den `speech` eller `music`, og flagget «musikk under tale – vurder rettigheter» produseres ikke. Tale som merkes `music`, transkriberes ikke og må fanges av menneskelig vurdering. Alternativ B og C står åpne etter v1.0 ([KLAR-ADR-0019](docs/adr/KLAR-ADR-0019_arkivklarering_inaseg-erstatning_v1.6_2026-10-28.md), «Tale over musikk» og «Hva det betyr for ADR-0004»).
- **Mulig overlapp mellom testdata og NB-Whispers treningsdata,** og mulig skjevhet i referansen; ikke kontrollert ([KLAR-EVAL-0013](eval/test/KLAR-EVAL-0013_arkivklarering_test-nbsamtale-wer_v1.3_2026-10-27.md) «Begrensninger» (2); [KLAR-EVAL-0014](eval/test/KLAR-EVAL-0014_arkivklarering_test-flaggoverlevelse-npsc_v1.4_2026-10-27.md) «Begrensninger» (1) og (6)).
- **Katalogutkastet er ikke validert** og ligger utenfor v1.0. Standardmodellen `borealis-open-4b` er Gemma 3-basert med lisensen `gemma`, og vilkårene er ikke gjennomgått ([KLAR-ADR-0013](docs/adr/KLAR-ADR-0013_arkivklarering_katalogmodell_v1.1_2026-10-28.md) «Lisens»; [KLAR-ARK-0006](docs/KLAR-ARK-0006_arkivklarering_veikart_v1.13_2026-10-28.md) «Etter v1.0»).
- **H4 gjennomføres ikke i v1.0.** Testmanuset og mønstrene i personvernmotoren er laget av samme forfatter, og målingen ville hatt én leser, som er forfatter og kjenner målelementene (AV-14), så den ville ikke gitt ekstern gyldighet. Kategoriene uten naturlige forekomster i H1–H3 er derfor ikke målt på tale i v1.0. Blindtesten på NB Tale modul 3 er planlagt som v1.1 (KLAR-PREREG-0003) ([KLAR-PREREG-0001](docs/KLAR-PREREG-0001_arkivklarering_testdeler_v1.33_2026-10-28.md), «Avvik etter registrering» punkt 8 og 20; AV-14, AV-27).
- **Foreknowledge-feltet på OSF er satt feil.** Avvikspunkt 1 i [KLAR-PREREG-0001](docs/KLAR-PREREG-0001_arkivklarering_testdeler_v1.33_2026-10-28.md), ordrett:

> **Foreknowledge på OSF ble satt til ‹Authors have observed the data, but have not performed the proposed analyses›. Det riktige er: testdelene (NB Samtale, NorNE, NPSC test) er ikke lastet inn eller observert (sperret i koden). Testmanuset er skrevet av forfatterne, men ingen opptak finnes. DEV-dataene (validation) er observert.** Valget på OSF er ikke endret.

Ordrett fra beslutningene og eval-dokumentene (lenket til versjonen sitatet står i):

> **Regelen fjerner ikke risikoen Koenecke m.fl. beskriver.** Pauser inne i tale ligger i `speech`-segmenter (og tale slås sammen over gap på høyst 1 s), og oppdiktet tekst der er ikke utelukket. Alle transkripsjoner må derfor vurderes av et menneske, og en måling på ekte arkivlyd med pauser er ikke gjort.
> — [KLAR-ADR-0004](docs/adr/KLAR-ADR-0004_arkivklarering_segmentregel_v1.5_2026-10-28.md)

> Den avgjør ikke at noe er klarert. Den avgjør ikke at noe er fritt for personopplysninger. Et manglende flagg er ikke en garanti.
> — [KLAR-ARK-0001](docs/KLAR-ARK-0001_arkivklarering_arkitektur_v1.10_2026-10-28.md)

> Utdata er forslag til en menneskelig vurdering og skal ikke leses som en klarering.
> — [KLAR-ARK-0001](docs/KLAR-ARK-0001_arkivklarering_arkitektur_v1.10_2026-10-28.md)

> **Dette er skrevet tekst, ikke tale.** NorNE er avis-, blogg-, stortings- og rapporttekst. Talespråk og dialekt, og transkripsjonsfeil i navn (ASR skriver «Kari» som «Karin»), er ikke med. Recall på transkripsjoner vil være lavere enn tallene her.
> — [KLAR-EVAL-0005](docs/KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_2026-10-26.md)

> **Overlapp med treningsdata er ikke kontrollert.** NB-BERT-base-ner er finjustert på NorNE (modellkortet), og spaCys norske pipeline er ikke sjekket her. Validation er ikke testdelen, men tallene er sannsynligvis optimistiske for tekst av denne typen.
> — [KLAR-EVAL-0005](docs/KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_2026-10-26.md)

> Rålaget (verbatim) har små bokstaver uten tegnsetting, og store bokstaver er et sterkt signal for navnegjenkjenning. Flagg lages derfor på begge lag, og rålagets recall forventes lavere (målt i KLAR-EVAL-0005).
> — [KLAR-ADR-0012](docs/adr/KLAR-ADR-0012_arkivklarering_recall-foran-presisjon_v1.4_2026-10-28.md)

> **n er fortsatt for liten** (person 17, sted 14, organisasjon 3) til å si mer enn dette. Se `KLAR-EVAL-0007` (NPSC, større n).
> — [KLAR-EVAL-0006](docs/KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.1_2026-10-26.md)

> **Optimisme.** NB-Whisper-kortet oppgir stortingstaler fra Språkbanken som treningsdata og sier ikke hvilke deler; validation-delen av NPSC kan ligge i treningsdataene. Tallene sier derfor lite om hvordan talegjenkjenningen vil gjøre det på arkivlyd, og de kan ikke sammenlignes med `KLAR-EVAL-0006` (annet materiale, annet språkvalg).
> — [KLAR-EVAL-0007](docs/KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_2026-10-26.md)

> **Referansen er ikke fasit.** Den er samme motor på riktig tekst, med recall under 1 (`KLAR-EVAL-0005`). «Overlevelse» sier hvor mye av det motoren finner i riktig tekst den også finner i transkripsjonen.
> — [KLAR-EVAL-0007](docs/KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_2026-10-26.md)

> **e-post: 0 av 12.** Whisper skriver ikke talte e-postadresser som adresser (teksten har ikke tegnet @), så ingen e-postgjenkjenning kan treffe. Dette er en kjent begrensning og står i preregistreringen som forventet negativt.
> — [KLAR-EVAL-0008](docs/KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.5_2026-10-28.md)

## Kilder

Kontrollert 2026-10-26 (resultat per kilde i [KLAR-ARK-0001_arkivklarering_arkitektur_v1.10_2026-10-28.md](docs/KLAR-ARK-0001_arkivklarering_arkitektur_v1.10_2026-10-28.md) § 6); hver faktapåstand med sitat, lagret kopi og sha256 står i [KLAR-KILDE-0001](docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.20_2026-10-28.md):

- <https://clams.ai/home/>
- <https://mmif.clams.ai/>
- <https://hdl.handle.net/2022/21982>
- <https://research.uky.edu/news/making-history-accessible-doug-boyds-curate-research>
- <https://blog.americanarchive.org/2020/06/05/how-to-fix-it-and-why-crowdsourcing-to-save-public-media/>
- <https://pypi.org/project/inaVAMOS/>
- <https://github.com/ina-foss/inaVAMOS>
- <https://arxiv.org/abs/2402.08021>
- <https://huggingface.co/NbAiLab/nb-whisper-large-verbatim>
- <https://huggingface.co/NbAiLab/nb-whisper-large>
- <https://github.com/NbAiLab/nb-whisper>
- <https://presidio.dataprivacystack.org/>
- <https://data.nav.no/fortelling/cleanup-guide>
- <https://huggingface.co/NbAiLab/nb-bert-base-ner>
- <https://www.w3.org/TR/webvtt1/>
- <https://iiif.io/api/presentation/3.0/>

Tillagt etter at kildekontrollen ble gjort: OHMS XML-skjemaet (<https://www.weareavp.com/nunncenter/ohms/ohms.xsd>, tidligere avpreserve.com-adressen, som svarer med en bot-sjekk (HTTP 403, Cloudflare); kopien er Wayback Machines snapshot av 2024-08-30, sha256 `78e7fe40…`), IIIF Cookbook-oppskriftene 0231 og 0219 (<https://github.com/IIIF/cookbook-recipes>), `mmif-python` og NorNE (<https://github.com/ltgoslo/norne>), NPSC (<https://huggingface.co/datasets/NbAiLab/NPSC>) og NB Samtale (<https://huggingface.co/datasets/Sprakbanken/nb_samtale>).

Tillagt 2026-10-27: inaSpeechSegmenters lisens ved tagg v0.8.0 (<https://github.com/ina-foss/inaSpeechSegmenter/blob/v0.8.0/LICENSE>) og talerinndelingsmodellen (<https://huggingface.co/pyannote/speaker-diarization-community-1>).

Tillagt 2026-10-27 (lisensbyttet): lisensteksten GNU Affero General Public License v3 (<https://www.gnu.org/licenses/agpl-3.0.txt>) og Open Source Initiatives side for lisensen (<https://opensource.org/license/agpl-3.0>).

## Dokumenter og beslutninger

**Veikart:** [KLAR-ARK-0006](docs/KLAR-ARK-0006_arkivklarering_veikart_v1.13_2026-10-28.md) (stegene til v1.0 med status, og det som kommer etter).

Dokumentene bærer arkivnøkler, `KLAR-<TYPE>-<NNNN>_arkivklarering_<slug>_v<maj>.<min>_<dato>` ([KLAR-ARK-0002](docs/KLAR-ARK-0002_arkivklarering_navnekonvensjon_v1.6_2026-10-28.md)), med numrene registrert i [KLAR-ARK-0003](docs/KLAR-ARK-0003_arkivklarering_nummerregister_v1.27_2026-10-28.md). Beslutningene (MADR) ligger i `docs/adr/` (0001–0020). Preregistreringen: [KLAR-PREREG-0001](docs/KLAR-PREREG-0001_arkivklarering_testdeler_v1.33_2026-10-28.md) (registrert, <https://osf.io/hc83q/>, embargo til 2027-10-26); metoderegistreringen: [KLAR-REG-0001](docs/KLAR-REG-0001_arkivklarering_osf-metode_v1.2_2026-10-27.md). Avvik: [KLAR-LOG-0003](docs/KLAR-LOG-0003_arkivklarering_avvikstabell_v1.22_2026-10-28.md) (tabell) og [KLAR-LOG-0001](docs/KLAR-LOG-0001_arkivklarering_avvik-og-hendelser_v1.53_2026-10-28.md) (fortløpende logg). Avklaringene før frys: [KLAR-ARK-0008](docs/KLAR-ARK-0008_arkivklarering_avklaringer-foer-frys_v1.16_2026-10-28.md); artikkelutkastet til JOSS (ikke sendt inn): [KLAR-ARK-0009](docs/KLAR-ARK-0009_arkivklarering_artikkelutkast-joss_v0.15_2026-10-28.md), med referansene som BibTeX i [paper.bib](paper.bib). Museumspiloten får en egen preregistrering, KLAR-PREREG-0002 (reservert). Tilstanden leses fra den genererte `docs/KLAR-GT-0001_*`, ikke fra dette dokumentet. `scripts/speil.sh` speiler til Vault og Master Dok. og sammenligner sha256; `scripts/stempel.py` tidsstempler dokumentene med OpenTimestamps (`docs/stempler/`). Manus: `kalibrering/KLAR-MANUS-0001_*` er justeringsmanuset (brukt til mønsterjustering, ikke til testing), `kalibrering/KLAR-MANUS-0002_*` er urørt testmateriale for H4 (156 setninger hver; innlesing av testmanuset med `scripts/rigg_manus.py`). Bidrag: [CONTRIBUTING.md](CONTRIBUTING.md); endringer: [CHANGELOG.md](CHANGELOG.md).

## Lisens

Programvaren er tilgjengelig under GNU Affero General Public License v3.0 eller senere, en lisens godkjent av Open Source Initiative (godkjent 3. mars 2008, SPDX `AGPL-3.0`; <https://opensource.org/license/agpl-3.0>, KLAR-KILDE-0001 OI-01). For bruk som ikke er forenlig med AGPL, tilbyr rettighetshaveren kommersiell lisens: eirik@ecodeco.no.

Rettighetshaver: Copyright 2026 Eirik Botten Nicolaysen, EcoDeco AS ([NOTICE](NOTICE)). SPDX-identifikator `AGPL-3.0-or-later` (`pyproject.toml`, `CITATION.cff`, `.zenodo.json`); [LICENSE](LICENSE) er lisensteksten ordrett fra <https://www.gnu.org/licenses/agpl-3.0.txt> (byte-lik den lagrede kopien, KLAR-KILDE-0001 K123). Det offentlige repoet (`avalyset/arkivklarering-public`) har én commit med treet ved utgivelsen. Hele git-historikken er lisensiert AGPL-3.0-or-later og deponert med begrenset tilgang og tilgang på forespørsel på Zenodo (DOI 10.5281/zenodo.23723450); commit-SHA-ene som preregistreringen, `kjoring_meta`-filene, kodetaggene og stemplene viser til, finnes der. KLAR-MANUS-0002 v1.2 (i git-historikken), som OSF-registreringen låser med sha256, kan etterprøves der. Commitene før lisensbyttet hadde en LICENSE-fil med Apache-2.0 eller ingen lisensfil ([LICENSING-HISTORY.md](LICENSING-HISTORY.md)). Beslutning og begrunnelse: [KLAR-ADR-0020](docs/adr/KLAR-ADR-0020_arkivklarering_lisens-agpl_v1.4_2026-10-28.md).

Tredjepartskomponenter og modeller beholder sine egne lisenser og står i [NOTICE](NOTICE); lisenskildene er ført i [KLAR-KILDE-0001](docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.20_2026-10-28.md):

- `arkivklarering/_vendor/norsk_tale/` er en uendret kopi fra norsk-tale, Apache-2.0, med egen `LICENSE` og opphav i `ORIGIN.txt` ([KLAR-ADR-0014](docs/adr/KLAR-ADR-0014_arkivklarering_vendor-fra-norsk-tale_v1.1_2026-10-27.md)).
- NB-Whisper large og large-verbatim (lastes ned separat, `modeller.lock.json`): Apache-2.0 (NW-05, NW-15, NW-16).
- To modeller er lisensiert CC BY 4.0 (<https://creativecommons.org/licenses/by/4.0/>) og krediteres her og i NOTICE: NB-BERT-base-ner (NbAiLab/nb-bert-base-ner, <https://huggingface.co/NbAiLab/nb-bert-base-ner>, NbAiLab (NB AI-Lab)), brukt i personvernflaggene, og pyannote/speaker-diarization-community-1 (<https://huggingface.co/pyannote/speaker-diarization-community-1>, pyannote), brukt i den valgfrie talerinndelingen. Ingen av dem er endret av oss eller ligger i repoet; pyannote-modellen lastes ned av brukeren etter at vilkårene er godtatt på Hugging Face.
- Standardmodellen for katalogutkastet, `borealis-open-4b` (lastes ned separat via ollama), er Gemma 3-basert, og Hugging Face-kortet oppgir lisensen `gemma` (egne vilkår); vilkårene er ikke gjennomgått (LI-15; [KLAR-ADR-0013](docs/adr/KLAR-ADR-0013_arkivklarering_katalogmodell_v1.1_2026-10-28.md) «Lisens»).
- inaSpeechSegmenter 0.8.0 (standard segmentering, eget venv): MIT for koden; lisensen for vektene er uklar (IS-01; [KLAR-ADR-0019](docs/adr/KLAR-ADR-0019_arkivklarering_inaseg-erstatning_v1.6_2026-10-28.md)).
- inaVAMOS (bare det valgfrie tillegget `reproduksjon-h1h2`): Pantagruel Research-only License, bare for forskning; art. 3 forbyr bruk i kommersiell aktivitet (PG-01, PG-02). Den ligger ikke i repoet og er ikke en del av standardinstallasjonen.

## Sitering

Siter med [CITATION.cff](CITATION.cff); `.zenodo.json` har de samme metadataene (tittel, versjon 1.0.0, forfatter, lisens, nøkkelord, OSF-registreringene). DOI settes etter arkivering på Zenodo. Forfatter: Eirik Botten Nicolaysen, EcoDeco AS (ORCID 0009-0001-9188-6788).

---

## English (short)

**arkivklarering** helps Norwegian local-radio and oral-history archives with *clearance before publication* (personal data and third-party music rights). Archives cannot publish until every recording is cleared, and today that means staff and volunteers listening through every hour. Everything runs **locally**; audio never leaves the machine. A human decides everything: the tool only **proposes**, and its output is a draft, not a clearance. Pipeline: speech/music segmentation (inaSpeechSegmenter by default; inaVAMOS only as an optional extra to reproduce the preregistered runs H1 and H2) → transcription in two layers with NB-Whisper large via whisper.cpp (verbatim and standard, with DTW word timestamps) → personal-data flags (Presidio with spaCy, NB-BERT-base-ner, patterns, keyword lists; union of both layers, no threshold) → draft catalogue record (local ollama; not validated) → export to WebVTT, OHMS XML, IIIF Presentation 3 and MMIF.

Install, usage and tests: see the commands above (everything heavy lives under one data root, `ARKIVKLARERING_DATA`, by default `/Volumes/Vault/arkivklarering` when mounted and `~/.local/share/arkivklarering` otherwise; scripts abort if caches or tmp point outside it; the tests run in a clean environment; run the fast tests with `pytest -q -m 'not tung'`). The preregistered test splits H1–H3 (NB Samtale, NPSC, NorNE) have been run once and reported; the figures are the preregistered measurements from those runs (code tag `testkjoring-v2`; H1 and H2 segmented with inaVAMOS, H3 is text and was not segmented), recomputed from the stored outputs with `scripts/rapporter_intervaller.py` on `9ded8d8` and matching, and H1 and H2 cannot be re-run with the default segmenter (inaSpeechSegmenter) without becoming a different measurement, so no claim is made that the v1.0 pipeline produces these figures; H4 is not carried out in v1.0 (deviation AV-27), and a blind test on NB Tale module 3 is planned as v1.1 (KLAR-PREREG-0003). Other results are **development (DEV) measurements** on validation splits of public datasets and one synthetic calibration; none of them say anything about quality on archive audio. Known limitations (in Norwegian above): inaVAMOS is research-only and no longer used, the licence of the inaSpeechSegmenter weights is unclear, the "music under speech" flag is no longer produced, test data may overlap NB-Whisper's training data, the catalogue draft is not validated, H4 is not carried out in v1.0 (so categories without natural occurrences in H1–H3 are not measured on speech), and the foreknowledge field on OSF was set incorrectly. Licence: the software is available under the GNU Affero General Public License v3.0 or later; for uses that are not compatible with the AGPL, the rights holder offers a commercial licence: eirik@ecodeco.no. Third-party components and models keep their own licences (`NOTICE`), and the licence history of the earlier commits is in `LICENSING-HISTORY.md`. Contributing: `CONTRIBUTING.md`. Cite via `CITATION.cff`. Method registration: <https://osf.io/fbme7/> (under embargo until 2027-10-26).
