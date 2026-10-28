# KLAR-EVAL-0014: H2, NPSC test (flaggoverlevelse), med 95 %-intervaller og terskelvurdering

Versjon 1.4, 2026-10-27 (v1.4: under begrensning (6) ett nytt avsnitt med sitat og URL om at referansen i NB Samtale (H1) startet som automatisk talegjenkjenning fra NBs KI-lab (OL-19, OL-20; B12 i KLAR-ARK-0008), sitatene kopiert fra sitatfeltet i `docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.4_2026-10-27.md`; perioden SSC dekker stod allerede i (6); ingen ny beregning og ingen endring i tall, tabeller, klassifisering eller resultatfiler; v1.0: resultatfila `…_v1.0_2026-10-27.json` fra skriptet, uendret; v1.1: intervaller og terskelvurdering; v1.2: én setning om klyngede flagg under begrensninger, ingen ny beregning og ingen endring i tall eller klassifisering; v1.3: to nye begrensninger, (5) inaVAMOS-lisensen og (6) mulig overlapp mellom testdata og NB-Whispers treningsdata (sitater fra KLAR-KILDE-0001 v1.1), ingen ny beregning og ingen endring i tall, tabeller, klassifisering eller resultatfiler). Datasett: `NbAiLab/NPSC`, del `test`, 16 kHz mp3, revisjon `e906435cc445e38961d86f3ebf53a7b38603b903`. Kjørt én gang via `scripts/kjor_testdel.sh H2` med de forhåndsregistrerte parametrene `--mal-person 300 --mal-sted 200 --maks-timer 4`.

**Foreknowledge (avvik 1 i PREREG, ordrett):** «Foreknowledge på OSF ble satt til ‹Authors have observed the data, but have not performed the proposed analyses›. Det riktige er: testdelene (NB Samtale, NorNE, NPSC test) er ikke lastet inn eller observert (sperret i koden). Testmanuset er skrevet av forfatterne, men ingen opptak finnes. DEV-dataene (validation) er observert.» Valget på OSF er ikke endret.

## Utvalget

1 995 segmenter (bokmål 1 330, nynorsk 665) fra de fire testdagene (20170207, 20171122, 20171219, 20180530), 14 216 s lyd (3,95 timer; taket er 4 timer). Referanseflagg i prefikset: person 379 (bokmål 155, nynorsk 224) og sted 201 (bokmål 139, nynorsk 62). Målene 300 person- og 200 stedsflagg er nådd; fire-timerstaket ble ikke nådd. Referansen er personvernmotoren på `normsentence_text`; overlevelse (a) = andelen referanseflagg i kategorien som har minst ett rørledningsflagg i samme kategori i samme segment.

**NB-Whisper er trent på NPSC; overlevelsestallene er optimistiske for talegjenkjenningen** (PREREG).

## Terskler (PREREG, UNION, overlevelse (a); punktestimat; «klart bekreftet» krever at Wilson-grensen også er på riktig side)

| id | gruppe | DEV | terskel | test | Wilson 95 % | utfall |
|---|---|---|---|---|---|---|
| **H2a (primær)** | person, begge målformer | 0,927 (139/150) | ≥ 0,85 | **0,913** (346/379) | 0,880–0,937 | bekreftet, klart |
| **H2b (primær)** | sted, begge målformer | 0,902 (92/102) | ≥ 0,80 | **0,856** (172/201) | 0,8005–0,898 | bekreftet; klart med 0,0005 (nedre grense 0,80047, avrundet 0,800) |
| **H2c (primær)** | person, bokmål | 0,976 (83/85) | ≥ 0,90 | **0,935** (145/155) | 0,885–0,965 | bekreftet, ikke klart (nedre grense 0,885 < 0,90) |
| **H2d (primær)** | sted, bokmål | 0,925 (74/80) | ≥ 0,80 | **0,871** (121/139) | 0,805–0,916 | bekreftet, klart |
| **H2e (primær)** | person, nynorsk | 0,862 (56/65) | ≥ 0,75 | **0,897** (201/224) | 0,851–0,931 | bekreftet, klart |
| H2f (rapporteres) | sted, nynorsk | 0,818 (18/22) | ingen terskel | 0,823 (51/62) | 0,710–0,898 | ingen vurdering |

Alle fem H2-terskler (H2a–H2e) er oppfylt av punktestimatet. Fire av fem er klart bekreftet; H2c er bekreftet uten å være klar, og H2b er klar med en margin på 0,0005 som ikke bør tolkes som mer enn «på grensen».

## Alle lag (overlevelse (a), Wilson 95 %)

| kategori | lag | målform | overlevd/ref | andel | Wilson 95 % |
|---|---|---|---|---|---|
| person | ra | nb | 115/155 | 0,742 | 0,668–0,804 |
| sted | ra | nb | 96/139 | 0,691 | 0,610–0,761 |
| person | normalisert | nb | 139/155 | 0,897 | 0,839–0,935 |
| sted | normalisert | nb | 115/139 | 0,827 | 0,756–0,881 |
| person | union | nb | 145/155 | 0,935 | 0,885–0,965 |
| sted | union | nb | 121/139 | 0,871 | 0,805–0,916 |
| person | ra | nn | 169/224 | 0,754 | 0,694–0,806 |
| sted | ra | nn | 26/62 | 0,419 | 0,305–0,543 |
| person | normalisert | nn | 191/224 | 0,853 | 0,800–0,893 |
| sted | normalisert | nn | 46/62 | 0,742 | 0,621–0,834 |
| person | union | nn | 201/224 | 0,897 | 0,851–0,931 |
| sted | union | nn | 51/62 | 0,823 | 0,710–0,898 |
| person | ra | samlet | 284/379 | 0,749 | 0,703–0,790 |
| sted | ra | samlet | 122/201 | 0,607 | 0,538–0,672 |
| person | normalisert | samlet | 330/379 | 0,871 | 0,833–0,901 |
| sted | normalisert | samlet | 161/201 | 0,801 | 0,740–0,850 |
| person | union | samlet | 346/379 | 0,913 | 0,880–0,937 |
| sted | union | samlet | 172/201 | 0,856 | 0,800–0,898 |

Streng overlevelse (b, delt ord eller inneholdt utdrag) for unionen står i resultatfila (`overlevelse_b`): bokmål person 130/155 (0,839), sted 118/139 (0,849); nynorsk person 188/224 (0,839), sted 50/62 (0,806).

**K2 (kontrollsjekk, ikke hypotese):** rålaget alene har lavere overlevelse enn det normaliserte laget for både person og sted, samlet: person 0,749 mot 0,871, sted 0,607 mot 0,801 (DEV: 0,740 mot 0,880 og 0,549 mot 0,902). Kriteriet (punktestimat rå < normalisert for begge) er oppfylt.

## Tolkning (for hånd)

Unionen løfter overlevelsen over hvert enkeltlag i alle seks kombinasjoner av kategori og målform, og forklarer hvorfor PREREG bruker unionen som primærutfall. Sted på nynorsk er svakest (rålag 0,419; union 0,823 på bare 62 referanseflagg). Testtallene ligger lavere enn DEV for fire av fem terskelgrupper (H2a–H2d), og H2e (nynorsk person) ligger høyere (0,897 mot 0,862). Rapporterte «ekstra» rørledningsflagg uten referanse (union, `ekstra_andel_a`): bokmål person 0,087, sted 0,124; nynorsk person 0,112, sted 0,175; unionen flagger altså også mer enn referansen.

Begrensninger: (1) NB-Whisper er trent på NPSC, så tallene er optimistiske for talegjenkjenningen. (2) Wilson-intervallene behandler hvert referanseflagg som uavhengig; flagg fra samme taler og samme segment henger sammen, så intervallene er sannsynligvis for smale. PREREG krever ikke clusterbootstrap for H2 (clusterbootstrap over `speaker_id` er spesifisert for WER). Den avviker ikke, men leseren bør vite det. (3) Referansen er motorens egen utgang på menneskelig transkripsjon, ikke manuelt merket fasit. (4) Intervallene er Wilson over flagg, slik PREREG spesifiserer. Flaggene er klynget i segmenter og talere, så et klyngejustert intervall ville trolig vært bredere. Klassifiseringen av H2b (margin 0,0005) er følsom for dette.

(5) Segmenteringen i H1- og H2-kjøringene brukte inaVAMOS (https://github.com/ina-foss/inaVAMOS), som er lisensiert under Pantagruel Research-only License (art. 1 begrenser hvem som kan være lisenstaker; art. 3 forbyr bruk i kommersiell aktivitet); EcoDecos dekning under lisensen er uavklart; fra 2026-10-27 brukes inaVAMOS ikke lenger i verktøyet (se AV-25 i `docs/KLAR-LOG-0003_arkivklarering_avvikstabell_v1.9_2026-10-27.md`, ADR-0019). Resultatene står som preregistrert.

(6) Mulig overlapp mellom testdata og NB-Whispers treningsdata, og mulig skjevhet i referansen; utdyper (1). Sitatene er kopiert fra sitatfeltet i `docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.1_2026-10-27.md` (påstands-ID og kildenøkkel i parentes). Dette er en begrensning, ikke et funn om at overlapp finnes.

Treningsdata ifølge modellkortet til NbAiLab/nb-whisper-large (https://huggingface.co/NbAiLab/nb-whisper-large, avsnittet Training Data; OL-01, K20): «The training data originates from Språkbanken and the National Library of Norway's digital collection, including: […] NST Norwegian ASR Database (16 kHz) and its corresponding dataset - Transcribed speeches from the Norwegian Parliament by Språkbanken - TV broadcast (NRK) subtitles (NLN digital collection) - Audiobooks (NLN digital collection)». Kortets metadata lister NPSC blant datasettene: «datasets: - NbAiLab/ncc_speech - NbAiLab/NST - NbAiLab/NPSC» (OL-02, K20); hvilke NPSC-splitter, er ikke oppgitt.

Treningsdata ifølge NB-Whisper-artikkelen (Kummervold m.fl., arXiv 2402.01917, https://arxiv.org/html/2402.01917v1, avsnitt 4; K92): «We train on the following sources: […] NRK Subtitles. […] Audio Books. Professional narrators read these audio books with minimal deviations from the text.» (OL-04); fra de samme NRK-opptakene også lyd uten tale: «Additionally, we extract audio segments without speech from the same recordings.» (OL-05); og «The NST dataset. This dataset was created by the now defunct Nordisk Språkteknologi.» og «The Stortinget Speech Corpus. This is an open speech dataset created by the National Library of Norway in 2023 (Solberg et al., 2023).» (OL-06). Tabell 3, timer i trinn 1 og trinn 2 (OL-07): «NRK - Subtitles 16,518 2,478 NRK - No caption 715 312 Audio Books 2,461 2,275 The NST Dataset 260 490 The Stortinget Speech Corpus 2,230 523 Total 22,184 6,078 Table 3: Dataset size in hours.» Samme tabell står i PDF-utgaven, s. 3 (https://arxiv.org/pdf/2402.01917v1; OL-08, K93). Artikkelen nevner verken NPSC, NB Tale eller NB Samtale som trenings- eller testdata (OL-09, K92/K93); et fravær kan ikke sitat-sjekkes, og registeret fører i stedet at søk i den uttrukne teksten av HTML- og PDF-utgaven etter NPSC, Parliamentary Speech, Samtale og NB Tale gir null treff, og at kildelisten i avsnitt 4 bare har punktene (a)–(d). Stortingsdataene i artikkelen er altså Stortinget Speech Corpus (SSC), oppgitt uten splitter. Det eneste artikkelen sier om å unngå overlapp, gjelder NST-testdelen: «Care was taken to avoid speaker overlap between this test set and our training and validation data.» (OL-10, avsnitt 5).

SSC (Solberg m.fl. 2023, https://aclanthology.org/2023.resourceful-1.7.pdf, postside https://aclanthology.org/2023.resourceful-1.7/; K97, K96): lyden kommer fra Stortingets videoarkiv, «which contains videos of most ple- […] nary meetings from 2010 to 2022.» (OL-13, s. 2), og teksten fra ParlaMint-NO, som «contains the proceedings from Stortinget from […] 1998 to 2022.» (OL-14, s. 3). Artikkelen beskriver NPSC som et eget korpus med «126 hours of transcribed speech from meetings at […] Stortinget in 2017 and 2018.» (OL-15, s. 2). Språkbankens katalogpost for SSC (https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-91/, Data Splits; K98): «The parliamentary meetings which are part of the eval and test splits in the NPSC are kept aside as eval and test splits also in the SSC.» (OL-16). NPSC-testdagene i denne kjøringen, 20170207, 20171122, 20171219 og 20180530 (OL-12, K95), ligger i 2017–2018 og KAN derfor ligge i SSC-perioden; ifølge katalogen ligger de i så fall i SSCs eval- og testsplitt, ikke i treningssplitten. Om NB-Whisper bare har brukt SSCs treningssplitt, er IKKE avgjørbart fra kildene: artikkelen oppgir SSC uten splitter (OL-07), og modellkortet oppgir ikke hvilke NPSC-splitter som er brukt (OL-02).

Mulig referanseskjevhet: Språkbankens NPSC-post (https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-58/; K104) skriver «Transkripsjonsarbeidet er først gjort automatisk; resultatet av den automatiske transkripsjonen er manuelt sjekka og korrigert av kvalifiserte lingvistar og filologar.» (OL-18). Katalogen nevner ikke hvilket ASR-system som ble brukt. Referanseflaggene her er motorens utgang på denne transkripsjonen (`normsentence_text`); der rettingen har latt ordvalg eller skrivemåte fra det automatiske utkastet stå, kan referansen ligge nærmere en ASR-utgang enn en uavhengig transkripsjon ville gjort. Retningen og størrelsen av en slik skjevhet er ikke målt.

Tilsvarende for referansen i H1 (ny i v1.4): NB Samtale ble først transkribert automatisk, «The recordings were transcribed automatically using a Norwegian ASR system created by the AI- lab at the National Library of Norway.» (NB_Samtale_About_the_corpus.pdf, https://www.nb.no/sbfil/taledata/NB_Samtale_About_the_corpus.pdf, s. 5; OL-19, K99), og deretter rettet og gjennomgått manuelt: «These segments and transcriptions were then manually corrected by a transcriber according to a set of guidelines.» (OL-20). Begge referansene, NB Samtale (H1) og NPSC (H2), startet altså som automatisk transkripsjon; for NB Samtale var systemet fra NBs KI-lab, for NPSC navngir katalogen ikke systemet (OL-18). Om noen av disse systemene har felles opphav med NB-Whisper, er ikke opplyst i kildene. Se også KLAR-EVAL-0013 v1.3, Begrensninger (2).

## Intervallmetode (PREREG «Statistical models», avvik 7 og 11a)

Wilson 95 % for proporsjoner (H2), z = 1,96: `scripts/rapporter_intervaller.py:39–47` (`wilson`), brukt i tabellen via `flagg_tabell` (`scripts/rapporter_intervaller.py:102`, kall på linje 109 og 112); resultatfila bærer de samme intervallene fra skriptet selv (`eval/dev/kjor_flaggoverlevelse_ord.py:200` og `:202`, `wilson` importert fra `kjor_flaggoverlevelse_dev` på linje 32). Ingen bootstrap er brukt for H2: ingen B, ingen seed og ingen clusterenhet (Wilson over referanseflagg). Wilson-grensene er avrundet til tre desimaler (`wilson` returnerer `round(…, 3)`); for H2b er nedre grense 0,80047 ved full presisjon. Kommando: `.venv/bin/python scripts/rapporter_intervaller.py flagg <resultat.json>`.

## Kjøring

Metafil: `KLAR-EVAL-0014_arkivklarering_test-flaggoverlevelse-npsc_v1.0_2026-10-27_kjoring_meta.json`. Start 2026-10-27T09:22:22Z på commit `1be7358516467bff62f19f6e1a71bb68e04af379`, slutt 13:03:39Z, returkode 0, `git status --porcelain` tom ved start, kode uendret siden `testkjoring-v2` (`c49d17463c14f7719f9f271ae3d4af4824436c35`). Resultat committet som `efcfc42`. Ordtider: DTW (`-nfa -dtw large.v3`), paring på ordspenn med toleranse 0,5 s.
