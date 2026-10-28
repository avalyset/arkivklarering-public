# KLAR-ARK-0004: Modellkort for arkivklarering-rørledningen

Versjon 1.8, 2026-10-28 (v1.8: kodetaggen er `testkjoring-v10` (AV-33); v1.7: v1.6-notatet under sa at pekere til versjoner som ikke er i treet var rettet eller merket; det holdt ikke for KLAR-ADR-0019 v1.2 (:15, :26, :53, :63, :131), KLAR-ARK-0006 v1.8 (:135) og flere, som nå er merket. pekere til versjoner som ikke er i treet er merket «(i git-historikken)», og pekere med linjenummer til forrige versjon av et dokument med ny versjon viser til den nye versjonen, samme linje; kontrollert med `scripts/sjekk_pekere.py`, 0 brudd (KLAR-LOG-0005, restfunn etter kontrollen); v1.6: AV-32 tar med GT-generatoren; pekere til versjoner som ikke er i treet er rettet til gjeldende versjon eller merket «(i git-historikken)» (porten, runde 3 (KLAR-LOG-0005), funn 6 og 8); v1.5: repo-statusen viser til nyeste KLAR-GT-0001 (v1.34:13) og KLAR-ARK-0008 v1.8; rettelsen av standarden i koden viser til KLAR-ADR-0019 v1.5:16 (samme linje som i v1.4); rekkefølgen i «Type» er den `arkivklarering/cli.py` kjører (talerinndeling før personvernflagg); innledningen nevner DEV-sammenligningen av segmentørene, som ikke er et KLAR-EVAL-dokument; NPSC-merknaden under kjente begrensninger sier at kortet lister NPSC i metadata og at tallene kan være optimistiske; kodetagg `testkjoring-v9` (AV-32) i «Dato og versjon»; v1.4: tittelen uten «(v0.4)» (kortet gjelder pakkeversjon 1.0.0); repo-status med kilde i KLAR-GT-0001 v1.32; kodetagg `testkjoring-v8` (`0224d6d`; AV-30) i «Dato og versjon»; NOTICE-linjene for talerinndelingsmodellen (L14–16) og NB-BERT-base-ner (L18–20) rettet; øvrig tekst uendret; v1.3: merkene for A2 og A3 erstattet med Eiriks beslutninger 2026-10-27: egen kode er AGPL-3.0-or-later med kommersiell lisens som tillegg, og hele historikken publiseres med lisenserklæring (KLAR-ADR-0020, `LICENSING-HISTORY.md`); pakkeversjon 1.0.0 og kodetagg `testkjoring-v6` (AV-28) i «Dato og versjon»; datarota `ARKIVKLARERING_DATA` i «Ethical Considerations»; øvrig tekst uendret; v1.2: merkene for A1 erstattet med Eiriks beslutning 2026-10-27: H4 gjennomføres ikke i v1.0 (AV-27), blindtesten på NB Tale modul 3 er planlagt som v1.1 (KLAR-PREREG-0003); merkene for A2 og A3 står; øvrig tekst uendret; v1.1: segmenteringen er inaSpeechSegmenter 0.8.0 og inaVAMOS bare et valgfritt tillegg for reproduksjon av H1 og H2 (KLAR-ADR-0019, AV-25), med DEV-sammenligningen; talerinndelingen er bygget (KLAR-ADR-0016); målte testresultater H1–H3 med intervaller og primærintervall (KLAR-EVAL-0013 v1.2, -0014 v1.3, -0015 v1.4); kjente begrensninger; katalogutkastet er ikke validert og ligger utenfor v1.0; H4 eller blindtest merket som ventende på A1; v1.0: første versjon, 2026-10-26). Forfatter: Eirik Botten Nicolaysen, EcoDeco AS. Malen er seksjonene i Mitchell mfl. (2019), «Model Cards for Model Reporting» (<https://arxiv.org/abs/1810.03993>). Rørledningen er satt sammen av tredjepartsmodeller; arkivklarering har ikke trent noen modell. Kortet gjelder derfor rørledningen som helhet, med én tabell for delene. **Det inneholder ingen kvalitetspåstander utover tallene i KLAR-EVAL-dokumentene og i DEV-sammenligningen av segmentørene (`eval/dev/inaseg_sammenligning_dev_2026-10-27.json`, ikke et KLAR-EVAL-dokument; se «Segmentering, inaSpeechSegmenter mot inaVAMOS»); tallene under er kopiert derfra med fil og linje.** Ting vi ikke har målt er merket «ikke målt».

## Model Details

- **Utvikler:** EcoDeco AS (Eirik Botten Nicolaysen). Repo: `avalyset/arkivklarering`, privat til publiseringen (KLAR-GT-0001, nyeste versjon v1.34:13, «PRIVATE»; gjøres offentlig i frys-steget D4, KLAR-ARK-0008 v1.9 (i git-historikken)). Egen kode er lisensiert AGPL-3.0-or-later, med kommersiell lisens fra rettighetshaveren som tillegg (Eiriks beslutning A2 2026-10-27; `LICENSE`, `NOTICE` L4–5, `pyproject.toml:11–12`; KLAR-ADR-0020). Hele git-historikken publiseres, med lisenserklæring for de tidligere commitene med Apache-2.0 eller uten lisensfil (A3; `LICENSING-HISTORY.md`). Modellene og tredjepartskomponentene beholder sine egne lisenser (`NOTICE`).
- **Dato og versjon:** 2026-10-28, pakkeversjon 1.0.0 (`pyproject.toml:7`), kodetagg `testkjoring-v10` (commit efce3f443ecbd27ecf72e067ffc71bb0c3391ae1; AV-33: mekanisk pekersjekk med test, og kodetaggen i kjøreskriptet), den siste kodetaggen før frysen; `testkjoring-v9` (`951091e`, AV-32), `testkjoring-v6` (`57dedaf`, AV-28), `testkjoring-v7` (`9ded8d8`) og `testkjoring-v8` (`0224d6d`, AV-30) er beholdt.
- **Type:** lokal rørledning, ikke én modell: segmentering (tale/musikk) → transkripsjon i to lag → valgfri talerinndeling → personvernflagg → katalogutkast → eksport (rekkefølgen i `arkivklarering/cli.py:83–107`; KLAR-ARK-0001 § 2). Alt kjører lokalt (KLAR-ADR-0007).
- **Delene** (versjoner fra låsefilene og `modeller.lock.json`; opphav og vilkår i `KLAR-KILDE-0001`):

| del | rolle | identitet i repoet |
|---|---|---|
| inaSpeechSegmenter 0.8.0 (**standard**) | segmentering: `speech`, `music`, `other`; ingen klasse for tale over musikk | `requirements-inaseg.lock:525`, eget venv; `arkivklarering/segment.py:66` (`STANDARD_SEGMENTERING = "inaseg"`); KLAR-ADR-0019 |
| vektfila `keras_speech_music_noise_cnn.hdf5` | den eneste vektfila som lastes (`detect_gender=False`, `vad_engine="smn"`, `arkivklarering/_inaseg_runner.py:22–25`) | sha256 `f04b5e3c…`, cache på Vault (KLAR-ADR-0019 v1.2:31 (i git-historikken)) |
| inaVAMOS 0.1.1 (**valgfritt tillegg** `reproduksjon-h1h2`) | segmenteringen i de preregistrerte kjøringene H1 og H2; bare for å reprodusere dem (`ARKIVKLARERING_SEGMENTERING=inavamos`) | `pyproject.toml:24–26`, `requirements.lock:547` |
| NB-Whisper large verbatim (ggml) | rålag | `NbAiLab/nb-whisper-large-verbatim`, sha256 `0227866e…` |
| NB-Whisper large (ggml) | normalisert lag | `NbAiLab/nb-whisper-large`, sha256 `0f2f66f2…` |
| whisper.cpp med DTW-ordtidsstempler | kjøring av begge lag; rålaget med `-nt` (KLAR-ADR-0017) | `-nfa -dtw large.v3` (KLAR-LOG-0001) |
| Presidio 2.2.362 med spaCy 3.8.16 og `nb_core_news_md` 3.8.0 | navnegjenkjenning og mønstre | `requirements.lock:1445`, `:2399`; KLAR-ADR-0008 |
| `NbAiLab/nb-bert-base-ner` | navnegjenkjenning (person, sted, organisasjon) | `personvern.py` |
| mønstre og ordlister | dato, fødselsår, telefon, fødselsnummer, e-post, nøkkelord | `personvern.py`, `vokabular/` |
| `pyannote/speaker-diarization-community-1` via pyannote.audio 4.0.7 | valgfri talerinndeling (`--taler`), anonyme `TALER_n` | `requirements-diarisering.lock:1770`, eget venv; KLAR-ADR-0016 |
| `hf.co/NbAiLab/borealis-open-4b-gguf:Q4_K_M` via ollama | katalogutkast, **ikke validert** (se «Caveats») | `arkivklarering/katalog.py:21`; KLAR-ADR-0013 |

- **Vilkår for delene:** inaSpeechSegmenter har MIT-lisens for koden (KILDE IS-01); lisensen for vektene er uklar, og ingen kilde oppgir NC- eller forskningsvilkår (KLAR-ADR-0019 v1.2:20–25). inaVAMOS har Pantagruel Research-only License (art. 1 begrenser hvem som kan være lisenstaker, art. 3 forbyr bruk i kommersiell aktivitet); EcoDecos dekning er uavklart, og den brukes ikke i verktøyet fra 2026-10-27 (AV-25, `KLAR-LOG-0003` v1.9:31 (i git-historikken)). Talerinndelingsmodellen er CC BY 4.0 (KLAR-ADR-0016:15, `NOTICE` L14–16). NB-BERT-base-ner er CC BY 4.0 (KILDE NB-02, `NOTICE` L18–20). Borealis-open oppgir lisensen `gemma`; vilkårene er ikke gjennomgått (KLAR-ADR-0013:32, KILDE LI-15).
- **Merknad om dokumentene:** KLAR-ADR-0019 v1.2:16 (i git-historikken) sier at standard i koden fortsatt er inaVAMOS uten miljøvariabelen; det gjaldt før commit `076bb8d` (`testkjoring-v5`), som gjorde inaSpeechSegmenter til standard (`segment.py:66`). KLAR-ARK-0001 v1.5 (i git-historikken) (:26, :53) nevner fortsatt inaVAMOS som segmentering. Begge er rettet i KLAR-ADR-0019 v1.3:16 (gjeldende versjon v1.6:16) og KLAR-ARK-0001 v1.6 (:26, :53) (AV-26, commit `721261c`); KLAR-ARK-0001 v1.6:92 (i git-historikken) sier fortsatt «inaVAMOS, fire etiketter» om `segment.py`. Dette kortet følger koden.
- **Treningsalgoritmer, parametere, fairness-begrensninger:** ikke våre; vi har ikke trent eller finjustert noe. Unionen av begge lags flagg bruker ingen terskel (KLAR-ADR-0012).
- **Mer informasjon:** `README.md`, `KLAR-ARK-0001` (arkitektur), ADR-ene i `docs/adr/`, datablad `KLAR-ARK-0005` v1.2 (i git-historikken).
- **Sitering:** `CITATION.cff`. Spørsmål: eirik@ecodeco.no.

## Intended Use

- **Primær bruk:** å foreslå for et menneske hva som bør vurderes før et norsk lydarkiv publiseres: personopplysninger (navn, steder, dato, fødselsår, telefon, fødselsnummer, e-post, sensitive temaer) og at musikk ikke blir transkribert. Alt er forslag («utkast – maskinforslag»); **mennesket avgjør** (KLAR-ADR-0002).
- **Primære brukere:** arkivansatte og forskere som klarerer lokalradio- og fortellerarkiv.
- **Utenfor bruksområdet:** automatisk publisering eller sladding uten gjennomlytting; juridisk klarering; talergjenkjenning mot kjente personer (bygges ikke); lyd som ikke er norsk; bruk av flaggenes fravær som bevis for at noe er trygt; bruk av katalogutkastet som katalogpost (ikke validert, utenfor v1.0); kommersiell bruk av inaVAMOS-tillegget (lisensen, AV-25).

## Factors

- **Relevante faktorer:** målform (bokmål, nynorsk), dialekt og region, talestil (samtale, opplesning, tale i forsamling, spontantale), lydkvalitet (båndlyd, støy, musikk under tale), overlappende tale.
- **Faktorer i evalueringene så langt:** målform og skriftform (alle EVAL-er); dialektområde (e, n, sw, t, w) i NB Samtale, på DEV (KLAR-EVAL-0002) og test (KLAR-EVAL-0013 v1.2:28 (i git-historikken), uten intervaller); talestil bare som samtaleopptak (NB Samtale), stortingstale (NPSC) og skrevet tekst (NorNE). Simulert degradering er målt på DEV (KLAR-EVAL-0010). Ekte båndlyd, kjønn, alder og overlappende tale er **ikke målt**; H1-utvalget har bare segmenter uten overlapp (KLAR-EVAL-0013 v1.2:65 (i git-historikken)). Tale over musikk er bare sett i DEV (to intervaller) og i syntetisk røyktest (se «Quantitative Analyses»).

## Metrics

- WER (jiwer, `norm.normaliser` fra norsk-tale) for transkripsjon; recall og presisjon (overlapp og nøyaktig span) for navnegjenkjenning; overlevelse (andel referanseflagg som har et rørledningsflagg i samme kategori i samme segment) og «ekstra flagg» for flaggkjeden; flagg-treff per målelement for manusene; enighet per sekund mellom segmenterere.
- **Beslutningsterskler:** ingen i verktøyet. Flaggene er en union uten terskel (recall foran presisjon, KLAR-ADR-0012). Tersklene i KLAR-PREREG-0001 er evalueringsterskler, ikke driftsterskler.
- **Usikkerhet og primærintervall:** H1: clusterbootstrap over `speaker_id`, B = 2000, seed 20261026, persentilintervall (KLAR-EVAL-0013 v1.2:91 (i git-historikken), AV-13). H2: Wilson 95 % over referanseflagg, ingen bootstrap (KLAR-EVAL-0014 v1.3:73 (i git-historikken)); flaggene er klynget i segmenter og talere, så intervallene er trolig for smale (:57). H3: Wilson 95 % er primær, bootstrap over setninger er sensitivitetsanalyse, besluttet av eier etter at resultatene var kjent (AV-24, `KLAR-LOG-0003` v1.9:30; KLAR-EVAL-0015 v1.4:39–43 (i git-historikken)). «Klart bekreftet» krever at grensen til primærintervallet også er på riktig side av terskelen. DEV-tallene har Wilson-intervaller som er for smale fordi segmenter fra samme taler ikke er uavhengige.

## Evaluation Data

- **DEV (validation):** NB Samtale validation, 60 segmenter (KLAR-EVAL-0002, -0003, -0004); NorNE validation (KLAR-EVAL-0005); NPSC validation, 934 segmenter (KLAR-EVAL-0007); syntetisk TTS-lyd av justeringsmanuset (KLAR-EVAL-0008); DEV-sammenligning av segmenterere på NB Samtale validation og røyktestlyd (`eval/dev/inaseg_sammenligning_dev_2026-10-27.json`).
- **Test (preregistrert, OSF hc83q), kjørt én gang hver 2026-10-27 via `scripts/kjor_testdel.sh`** (`KLAR-LOG-0003` v1.9:3): NB Samtale test, revisjon `1c70281`, 252 segmenter fra 51 talere (H1; KLAR-EVAL-0013 v1.2:3, :9 (i git-historikken)); NPSC test, revisjon `e906435`, 1 995 segmenter fra fire møtedager, 14 216 s (H2; KLAR-EVAL-0014 v1.3:3, :9 (i git-historikken)); NorNE test, revisjon `1ca12d4`, 3 450 setninger (H3; KLAR-EVAL-0015 v1.4:3 (i git-historikken)). sha256 for de 13 testdatafilene står i KLAR-ARK-0007 og ble ført etter at H1 startet (AV-23). Datasettene er beskrevet i datablad `KLAR-ARK-0005` v1.2 (i git-historikken).
- **Segmentering i testkjøringene:** H1 og H2 er kjørt med inaVAMOS og står som preregistrert; H3 bruker ingen segmentering (KLAR-ADR-0019 v1.2:15 (i git-historikken)). Testtallene gjelder altså rørledningen med inaVAMOS, ikke standardoppsettet med inaSpeechSegmenter. Forskjellen mellom de to er bare målt på DEV og røyktest.
- **Testmanuset (H4):** `KLAR-MANUS-0002` er ikke lest inn; ingen opptak finnes (`/Volumes/Vault/arkivklarering/lyd/h4/serverlogg.jsonl` har ingen `opptak_lagret`; AV-19, AV-22). H4 gjennomføres ikke i v1.0 (AV-27); blindtesten på NB Tale modul 3 er planlagt som v1.1 (KLAR-PREREG-0003); Eiriks beslutning A1 2026-10-27.
- **Motivasjon og forbehold:** offentlige datasett med åpne lisenser; ingen av dem er lokalradio eller ekte arkivlyd.

## Training Data

Ikke våre data. Hva tredjepartsmodellene er trent på står i modellkortene deres (se `KLAR-KILDE-0001`). Det som gjelder tolkningen av våre tall:

- **NB-Whisper:** modellkortet oppgir stortingstaler transkribert av Språkbanken som treningsdata (OL-01) og lister `NbAiLab/NPSC` i metadata uten å si hvilke splitter (OL-02). Artikkelen trener på Stortinget Speech Corpus (SSC), oppgitt uten splitter (OL-06, OL-07), og nevner verken NPSC, NB Tale eller NB Samtale (OL-09). Ifølge Språkbanken ligger NPSCs eval- og testmøter i SSCs eval- og testsplitt (OL-16); om NB-Whisper bare brukte SSCs treningssplitt, er ikke avgjørbart fra kildene (OL-16). Om NB Samtale test ble holdt utenfor, er ikke opplyst (KLAR-EVAL-0013 v1.2:55 (i git-historikken)). Sammendrag med sitater: KLAR-EVAL-0013 v1.2:49–57 (i git-historikken) og KLAR-EVAL-0014 v1.3:61–69 (i git-historikken).
- **NB-BERT-base-ner** er finjustert på NorNE (KILDE NB-04, NB-05); om NorNE test var med i finjusteringen, er ikke kontrollert. H3-tallene kan derfor være optimistiske.
- **inaSpeechSegmenter:** treningsdata er ikke omtalt for de tre Keras-modellene; README sier bare at kjønnsmodellene (ikke brukt) er trent på franske talere (KLAR-ADR-0019 v1.2:20, :24 (i git-historikken)).

## Quantitative Analyses

Tallene er kopiert fra evalueringsdokumentene; der står oppsett, utvalg og forbehold.

**H1, NB Samtale test (WER, korpus-WER; primærintervall clusterbootstrap over taler).** Kilde: KLAR-EVAL-0013 v1.2:36–41 (i git-historikken).

| id | utfall | terskel | test | 95 %-intervall | utfall |
|---|---|---|---|---|---|
| **H1a (primær)** | rålag, språk etter målform | ≤ 0,25 | **0,127** | 0,112–0,144 | bekreftet, klart |
| H1b | normalisert lag, språk etter målform | ≤ 0,45 | 0,337 | 0,305–0,373 | bekreftet, klart |
| H1d | rålag, `-l nn` | ≤ 0,35 | 0,254 | 0,221–0,285 | bekreftet, klart |
| H1e | normalisert lag, `-l nn` | ≤ 0,60 | 0,464 | 0,428–0,507 | bekreftet, klart |

K1 (kontrollsjekk): normalisert minus rålag 0,209, 95 % 0,176–0,248. Det normaliserte laget måler normalisering og rettskrivning, ikke gjenkjenning (KLAR-EVAL-0013 v1.2:43 (i git-historikken)).

**H2, NPSC test (flaggoverlevelse, union; primærintervall Wilson over referanseflagg).** Kilde: KLAR-EVAL-0014 v1.3:17–22 (i git-historikken).

| id | gruppe | terskel | test | Wilson 95 % | utfall |
|---|---|---|---|---|---|
| **H2a** | person, begge målformer | ≥ 0,85 | **0,913** (346/379) | 0,880–0,937 | bekreftet, klart |
| **H2b** | sted, begge målformer | ≥ 0,80 | **0,856** (172/201) | 0,8005–0,898 | bekreftet; klart med 0,0005 |
| **H2c** | person, bokmål | ≥ 0,90 | **0,935** (145/155) | 0,885–0,965 | bekreftet, ikke klart |
| **H2d** | sted, bokmål | ≥ 0,80 | **0,871** (121/139) | 0,805–0,916 | bekreftet, klart |
| **H2e** | person, nynorsk | ≥ 0,75 | **0,897** (201/224) | 0,851–0,931 | bekreftet, klart |
| H2f | sted, nynorsk | ingen | 0,823 (51/62) | 0,710–0,898 | ingen vurdering |

H2 måler bare person og sted. De andre kategoriene (dato, fødselsår, telefon, fødselsnummer, e-post, sensitive temaer) er ikke målt på test.

**H3, NorNE test (navnegjenkjenning, hele motoren, original tekst; sekundær; primærintervall Wilson, bootstrap over setninger som sensitivitet, AV-24).** Kilde: KLAR-EVAL-0015 v1.4:15–25 (i git-historikken).

| id | gruppe | recall | Wilson 95 % | utfall recall | presisjon | Wilson 95 % | utfall presisjon |
|---|---|---|---|---|---|---|---|
| H3a | bokmål, person | 1,000 | 0,993–1,000 | klart | 0,904 | 0,878–0,924 | klart |
| H3b | bokmål, sted | 0,975 | 0,953–0,987 | klart | 0,811 | 0,771–0,844 | ikke klart |
| H3c | nynorsk, person | 0,982 | 0,964–0,991 | klart | 0,733 | 0,694–0,769 | ikke klart |
| H3d | nynorsk, sted | 0,976 | 0,949–0,989 | ikke klart (bootstrap-grensen 0,956 ligger over terskelen, som sensitivitet) | 0,769 | 0,720–0,812 | klart |

Alle åtte terskler er oppfylt av punktestimatet; fem er klart bekreftet. K3: recall faller 0,281–0,478 på små bokstaver uten tegnsetting (KLAR-EVAL-0015 v1.4:31 (i git-historikken)).

**H4 (manus, sekundær): ikke målt.** Ingen opptak finnes (se «Evaluation Data»). H4 gjennomføres ikke i v1.0 (AV-27); blindtesten på NB Tale modul 3 er planlagt som v1.1 (KLAR-PREREG-0003). Kortet kan derfor ikke si noe om flaggkjeden på menneskelig tale med kjente målelementer, heller ikke om kategoriene H2 ikke dekker: kategoriene uten naturlige forekomster i H1–H3 er ikke målt på tale i v1.0. Fra DEV finnes bare syntetisk TTS-lyd (KLAR-EVAL-0008: kjede og flagglogikk, ikke talekvalitet).

**Segmentering, inaSpeechSegmenter mot inaVAMOS (DEV og røyktest, ikke test; inaVAMOS ble ikke kjørt på nytt, gamle utdata er lest fra disk).** Kilde: `eval/dev/inaseg_sammenligning_dev_2026-10-27.json`, linjenumre i parentes.

- NB Samtale validation, 60 filer, 396,92 s (:3–4): enighet per sekund 0,9291 streng og 0,9434 når `speech+music` regnes som `speech` (:5–6).
- inaVAMOS' `speech` (363,04 s) → ny `speech` 0,9993 (:9, :16); `speech+music` (5,66 s) → 100 % `speech` (:24–28); `music` (0,72 s) → `speech` (:39–43); `other` (27,5 s) → `speech` 0,7818, `other` 0,2182 (:54–63).
- Transkribert tid: 0 filer der den ene transkriberer og den andre ikke; 15 filer med minst 0,5 s forskjell; 0,78 s transkriberes bare med inaVAMOS og 22,22 s bare med ny kjører; 0 segmenter transkriberes av bare én av dem (:70–75).
- Røyktest (TTS med musikk under tale, to filer, hver 39,98 s): inaVAMOS' `speech+music`, 8,58 s og 9,96 s, ble 100 % `speech` i ny kjører (:618–628, :863–873), og transkriberes fortsatt. Flagget «musikk under tale» faller bort.

Ikke målt: katalogutkastet; segmentering og transkripsjon på ekte arkivlyd; intersectional-analyser (målform × dialekt × lydkvalitet).

## Ethical Considerations

- Rørledningen behandler personopplysninger og kan behandle særlige kategorier (helse, religion, politisk syn). All prosessering er lokal; ingen lyd eller tekst forlater maskinen (KLAR-ADR-0007). Tunge data ligger under datarota `ARKIVKLARERING_DATA`, hos eieren den eksterne Vault-disken (KLAR-ADR-0015; AV-28).
- Flagg er forslag. En mulig skade er at fravær av flagg tas for klarering. Derfor er alt merket som utkast, og ingenting regnes som klarert før et menneske har lyttet.
- Katalogutkastet kan gjengi navn og tall som flaggene har markert (KLAR-ADR-0013:33).
- Talerinndeling (anonyme `TALER_n`, valgfri) er bygget; den avslører ikke hvem noen er, men gjør det mulig å følge én stemme gjennom en sending. Ingen stemmegjenkjenning mot kjente personer, ingen taleravtrykk lagres (KLAR-ADR-0016:17, :26).
- Data fra museet er ikke brukt (ikke samtykke, `docs/gt_fast.md`). Data til Språkbanken først etter klarering (KLAR-ADR-0011).

## Caveats and Recommendations

- **Kjente begrensninger:**
  1. **Mulig overlapp mellom testdata og treningsdata** (NB-Whisper, NB-BERT; se «Training Data»). Det er en begrensning, ikke et funn om at overlapp finnes (KLAR-EVAL-0013 v1.2:49 (i git-historikken), KLAR-EVAL-0014 v1.3:61 (i git-historikken)). NB-Whisper-kortet lister NPSC i metadata (OL-02, se «Training Data»); H2-tallene kan derfor være optimistiske for talegjenkjenningen (KLAR-EVAL-0014 v1.3:11 (i git-historikken)).
  2. **Referansene startet som automatisk talegjenkjenning.** NB Samtale ble transkribert automatisk med et norsk ASR-system fra NBs KI-lab og deretter rettet og gjennomgått manuelt (OL-19, OL-20); NPSC ble først transkribert automatisk og så sjekket og korrigert manuelt (OL-18). Det kan gi en skjevhet i NB-Whispers favør; størrelsen er ikke målt (KLAR-EVAL-0013 v1.2:57 (i git-historikken), KLAR-EVAL-0014 v1.3:69 (i git-historikken)). H2-referansen er dessuten motorens egen utgang på den menneskelige transkripsjonen, ikke manuelt merket fasit (KLAR-EVAL-0014 v1.3:57 (i git-historikken)).
  3. **Én leser i H4** (forfatteren, som kjenner målelementene; AV-14). Gjelder ikke v1.0, fordi H4 ikke gjennomføres (AV-27); begrensningen er en del av grunnen.
  4. **Utenfor ekte arkivlyd.** Alle tall gjelder offentlige datasett (samtaleopptak med utvalgt lyd på 2–12 s uten overlapp, stortingstale, skrevet tekst) eller DEV, ikke lokalradio eller fortellerarkiv (KLAR-EVAL-0013 v1.2:43 (i git-historikken)).
  5. **H1 og H2 er kjørt med inaVAMOS**, mens verktøyet nå bruker inaSpeechSegmenter (AV-25). Forskjellen er bare målt på DEV og røyktest (over).
  6. **Ingen klasse for tale over musikk.** Med standard segmentering produseres `speech+music` aldri, og flagget «musikk under tale – vurder rettigheter» faller bort (KLAR-ADR-0019 v1.2:41–43, :58 (i git-historikken); `segment.py:17`). Tale over musikk transkriberes bare hvis modellen kaller den `speech`; tale merket `music` blir ikke transkribert og må fanges av menneskelig vurdering. Det er ikke målt på ekte arkivlyd med musikk (KLAR-ADR-0019 v1.2:57 (i git-historikken)). Alternativ B og C er ikke implementert (:44–45).
  7. **Intervallene for H2 er trolig for smale**, og klassifiseringen av H2b (margin 0,0005) er følsom for det (KLAR-EVAL-0014 v1.3:57 (i git-historikken)).
  8. **Presisjonen er hovedsvakheten i H3**, særlig på nynorsk (person 0,733, sted 0,769): motoren flagger mer enn gullet (KLAR-EVAL-0015 v1.4:27 (i git-historikken)). NorNE er skrevet tekst, ikke tale (:35).
  9. Fra DEV: rålaget (små bokstaver uten tegnsetting) gir svakere navnegjenkjenning enn det normaliserte laget; nynorsk er svakere enn bokmål; unionen ga ingen gevinst over det normaliserte laget for steder på NPSC validation; talte e-postadresser blir ikke skrevet som adresser (KLAR-EVAL-0005, -0007, -0008). På NPSC test løftet unionen overlevelsen over hvert enkeltlag i alle seks kombinasjoner av kategori og målform (KLAR-EVAL-0014 v1.3:55 (i git-historikken)).
- **Katalogutkastet er ikke validert og ligger utenfor v1.0.** Modellen (`borealis-open-4b`) er valgt mekanisk på fire DEV-utdrag; språkkvaliteten er ikke vurdert av et menneske, utkastet er ikke målt mot noe gullsett og er ikke preregistrert (KLAR-ADR-0013:17, :30). Gemma-vilkårene er ikke gjennomgått (:32). Vurderingen står under «Etter v1.0» i veikartet (KLAR-ARK-0006 v1.8:59 (i git-historikken)).
- **Ikke målt:** kvalitet på arkivlyd; musikkdeteksjon på ekte lyd; katalogutkastets språkkvalitet; H4 (gjennomføres ikke i v1.0, AV-27) og blindtesten på NB Tale modul 3 (planlagt som v1.1, KLAR-PREREG-0003).
- **Anbefaling:** bruk rørledningen som en lesehjelp, ikke som en sladdemaskin. Mål på eget materiale (pilot, `KLAR-PREREG-0002`, reservert) før noen tall brukes til å spare lyttetid.
