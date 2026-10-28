# KLAR-EVAL-0013: H1, NB Samtale test (WER), med 95 %-intervaller og terskelvurdering

Versjon 1.3, 2026-10-27 (v1.3: under Begrensninger (2) ett nytt avsnitt om perioden Stortinget Speech Corpus dekker, med sitat og URL (OL-13, OL-14, OL-16; B12 i KLAR-ARK-0008), sitatene kopiert fra sitatfeltet i `docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.4_2026-10-27.md`; ingen ny beregning og ingen endring i tall, tabeller, klassifisering eller resultatfiler; v1.0: skriptets egen utskrift, `…_v1.0_2026-10-27.md`, uendret; v1.1: intervaller etter KLAR-PREREG-0001, terskelvurdering, utvalgstrakt; v1.2: ny del Begrensninger med to punkter, inaVAMOS-lisensen og mulig overlapp mellom testdata og NB-Whispers treningsdata (sitater fra KLAR-KILDE-0001 v1.1), ingen ny beregning og ingen endring i tall, tabeller, klassifisering eller resultatfiler). Datasett: `Sprakbanken/nb_samtale`, del `test`, revisjon `1c7028101858b854d3d568761778d8f63bb7e33f`. Kjørt én gang via `scripts/kjor_testdel.sh H1`; resultatfil `KLAR-EVAL-0013_arkivklarering_test-nbsamtale-wer_v1.0_2026-10-27.json`.

**Foreknowledge (avvik 1 i PREREG, ordrett):** «Foreknowledge på OSF ble satt til ‹Authors have observed the data, but have not performed the proposed analyses›. Det riktige er: testdelene (NB Samtale, NorNE, NPSC test) er ikke lastet inn eller observert (sperret i koden). Testmanuset er skrevet av forfatterne, men ingen opptak finnes. DEV-dataene (validation) er observert.» Valget på OSF er ikke endret.

## Resultat

n = 252 segmenter, 51 talere. WER er korpus-WER (sum feil / sum referanseord). Punktestimat fra de lagrede hypotesene (`e/n`); 95 %-intervall er clusterbootstrap over `speaker_id`.

| kolonne | gruppe | WER | 95 %-intervall | segmenter | talere |
|---|---|---|---|---|---|
| ra/nn | totalt | 0,254 | 0,221–0,285 | 252 | 51 |
| ra/nn | skrift:bm | 0,315 | 0,280–0,346 | 159 | 38 |
| ra/nn | skrift:nn | 0,154 | 0,126–0,181 | 93 | 17 |
| ra/matchet | totalt | 0,127 | 0,112–0,144 | 252 | 51 |
| ra/matchet | skrift:bm | 0,111 | 0,096–0,130 | 159 | 38 |
| ra/matchet | skrift:nn | 0,154 | 0,126–0,181 | 93 | 17 |
| normalisert/nn | totalt | 0,464 | 0,428–0,507 | 252 | 51 |
| normalisert/nn | skrift:bm | 0,518 | 0,478–0,558 | 159 | 38 |
| normalisert/nn | skrift:nn | 0,375 | 0,319–0,442 | 93 | 17 |
| normalisert/matchet | totalt | 0,337 | 0,305–0,373 | 252 | 51 |
| normalisert/matchet | skrift:bm | 0,314 | 0,275–0,352 | 159 | 38 |
| normalisert/matchet | skrift:nn | 0,375 | 0,319–0,442 | 93 | 17 |

Avrunding: resultatfila lagrer ra/matchet totalt som 0,1275 (fire desimaler), og v1.0-tabellen viser derfor 0,128. Intervallskriptet regner fra feilord og ordtall og får 0,1275 avrundet nedover til 0,127. Samme tall, to avrundinger.

Per dialektområde (fra v1.0, ingen intervaller; hvert område har få talere): ra/matchet e 0,101, n 0,115, sw 0,134, t 0,144, w 0,159.

Tomme hypoteser av 252: ra/nn 0, ra/matchet 0, normalisert/nn 5, normalisert/matchet 1.

## Terskler (PREREG, punktestimat; «klart bekreftet» krever også at intervallgrensen er på riktig side)

| id | utfall | DEV | terskel | test | 95 %-intervall | utfall |
|---|---|---|---|---|---|---|
| **H1a (primær)** | ra/matchet | 0,135 | ≤ 0,25 | **0,127** | 0,112–0,144 | bekreftet, klart |
| H1b (sekundær) | normalisert/matchet | 0,348 | ≤ 0,45 | 0,337 | 0,305–0,373 | bekreftet, klart |
| H1d (sekundær) | ra/nn | 0,248 | ≤ 0,35 | 0,254 | 0,221–0,285 | bekreftet, klart |
| H1e (sekundær) | normalisert/nn | 0,463 | ≤ 0,60 | 0,464 | 0,428–0,507 | bekreftet, klart |

**K1 (kontrollsjekk, ikke hypotese):** WER(normalisert/matchet) − WER(ra/matchet), totalt, parret clusterbootstrap: differanse 0,209 (0,337 − 0,127), 95 %-intervall 0,176–0,248. Kriteriet WER(rå) < WER(normalisert) er oppfylt, og intervallet utelukker 0.

Tolkning (for hånd): alle fire terskler holder, og testtallene ligger nær DEV (H1a 0,127 mot DEV 0,135). Det normaliserte laget har WER 0,34 mot ortografisk fasit selv med riktig målform; PREREG forklarer det med at laget måler normalisering og rettskrivning, ikke gjenkjenning, og tallet er ikke et mål på gjenkjenningskvalitet. Rålaget med `-l nn` på bokmålssegmenter (skrift:bm, ra/nn) gir 0,315 mot 0,111 med riktig målform; driftskonfigurasjonen uten målformvalg er altså klart dårligere på bokmål. Alle tall gjelder offentlig samtaleopptak med utvalgt lyd (2–12 s, uten overlapp), ikke arkivlyd. Det er ikke kontrollert om NB-Whisper har sett NB Samtale test i treningen (åpent punkt i veikartet).

## Begrensninger

(1) Segmenteringen i H1- og H2-kjøringene brukte inaVAMOS (https://github.com/ina-foss/inaVAMOS), som er lisensiert under Pantagruel Research-only License (art. 1 begrenser hvem som kan være lisenstaker; art. 3 forbyr bruk i kommersiell aktivitet); EcoDecos dekning under lisensen er uavklart; fra 2026-10-27 brukes inaVAMOS ikke lenger i verktøyet (se AV-25 i `docs/KLAR-LOG-0003_arkivklarering_avvikstabell_v1.9_2026-10-27.md`, ADR-0019). Resultatene står som preregistrert.

(2) Mulig overlapp mellom testdata og NB-Whispers treningsdata, og mulig skjevhet i referansen. Sitatene er kopiert fra sitatfeltet i `docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.1_2026-10-27.md` (påstands-ID og kildenøkkel i parentes). Punktet utdyper det åpne punktet i tolkningen over; det er en begrensning, ikke et funn om at overlapp finnes.

Treningsdata ifølge modellkortet til NbAiLab/nb-whisper-large (https://huggingface.co/NbAiLab/nb-whisper-large, avsnittet Training Data; OL-01, K20): «The training data originates from Språkbanken and the National Library of Norway's digital collection, including: […] NST Norwegian ASR Database (16 kHz) and its corresponding dataset - Transcribed speeches from the Norwegian Parliament by Språkbanken - TV broadcast (NRK) subtitles (NLN digital collection) - Audiobooks (NLN digital collection)». Kortet sier ikke hvilke splitter av datasettene som er brukt.

Treningsdata ifølge NB-Whisper-artikkelen (Kummervold m.fl., arXiv 2402.01917, https://arxiv.org/html/2402.01917v1, avsnitt 4; K92): «We train on the following sources: […] NRK Subtitles. […] Audio Books. Professional narrators read these audio books with minimal deviations from the text.» (OL-04); fra de samme NRK-opptakene også lyd uten tale: «Additionally, we extract audio segments without speech from the same recordings.» (OL-05); og «The NST dataset. This dataset was created by the now defunct Nordisk Språkteknologi.» og «The Stortinget Speech Corpus. This is an open speech dataset created by the National Library of Norway in 2023 (Solberg et al., 2023).» (OL-06). Tabell 3, timer i trinn 1 og trinn 2 (OL-07): «NRK - Subtitles 16,518 2,478 NRK - No caption 715 312 Audio Books 2,461 2,275 The NST Dataset 260 490 The Stortinget Speech Corpus 2,230 523 Total 22,184 6,078 Table 3: Dataset size in hours.» Samme tabell står i PDF-utgaven, s. 3 (https://arxiv.org/pdf/2402.01917v1; OL-08, K93).

Artikkelen nevner verken NPSC, NB Tale eller NB Samtale som trenings- eller testdata (OL-09, K92/K93). Et fravær kan ikke sitat-sjekkes; registeret fører i stedet at søk i den uttrukne teksten av HTML- og PDF-utgaven etter NPSC, Parliamentary Speech, Samtale og NB Tale gir null treff, og at kildelisten i avsnitt 4 (som åpner med «We train on the following sources:») bare har punktene (a)–(d). Om NB Samtale test ble holdt utenfor treningsdataene, er ikke opplyst i kildene.

Perioden Stortinget Speech Corpus (SSC) dekker (ny i v1.3): lyden kommer fra Stortingets videoarkiv, «which contains videos of most ple- […] nary meetings from 2010 to 2022.» (Solberg m.fl. 2023, https://aclanthology.org/2023.resourceful-1.7.pdf, s. 2, postside https://aclanthology.org/2023.resourceful-1.7/; OL-13, K97, K96), og teksten fra ParlaMint-NO, som «contains the proceedings from Stortinget from […] 1998 to 2022.» (s. 3; OL-14). Språkbankens katalogpost for SSC (https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-91/, Data Splits; K98): «The parliamentary meetings which are part of the eval and test splits in the NPSC are kept aside as eval and test splits also in the SSC.» (OL-16). Ifølge sitatene er SSC bygget av opptak og referater fra Stortingets møter; sitatene nevner ikke NB Samtale. For H1 gir SSC-perioden derfor ingen opplysning om overlapp; den er relevant for H2, der NPSC-testdagene (2017–2018) kan ligge i SSC-perioden (KLAR-EVAL-0014 v1.4, begrensning (6)). Om NB Samtale-opptak finnes i NB-Whispers treningsdata, er fortsatt ikke opplyst i kildene.

Referansen i NB Samtale startet som automatisk talegjenkjenning fra NBs KI-lab og ble deretter rettet og gjennomgått manuelt (NB_Samtale_About_the_corpus.pdf, https://www.nb.no/sbfil/taledata/NB_Samtale_About_the_corpus.pdf, s. 5; K99): «The recordings were transcribed automatically using a Norwegian ASR system created by the AI- lab at the National Library of Norway.» (OL-19) og «These segments and transcriptions were then manually corrected by a transcriber according to a set of guidelines. All the manual transcriptions were reviewed by a second person in order to avoid substantial discrepancies between transcribers.» (OL-20). Referansen er altså manuelt rettet og gjennomgått, men utgangspunktet var utgangen fra et NB-ASR-system, og sitatet navngir ikke systemet. Der rettingen har latt ordvalg, normering eller segmentering fra utkastet stå, kan referansen ligge nærmere et NB-ASR-system enn en uavhengig transkripsjon ville gjort. Det kan gi en skjevhet i NB-Whispers favør (lavere WER); størrelsen er ikke målt og kan ikke anslås fra kildene.

## Utvalget og hvorfor n = 252

n = 252 følger av regelen (t og w under 60 kvalifiserte; tas alle), ikke avvik.

PREREG (v1.16, linje 128, som i registrert v1.8): «Utvalg: opptil 60 segmenter per dialektområde (e, n, sw, t, w), trukket med seed 20261026; har et område færre kvalifiserte segmenter, tas alle. Antall per område rapporteres.»
PREREG (linje 135): «H1: opptil 300 segmenter.» (300 = 5 × 60 er et tak, ikke et mål.)
Kode (`eval/dev/kjor_dev.py:53–59`): linje 53–54 filtrerer kandidatene (`not r["overlap_previous"] and not r["overlap_next"] and 2 <= r["duration"] <= 12 and len(r["orthographic"].split()) >= 3`), linje 55 `random.Random(SEED)` (`SEED = 20261026`, linje 40), linje 58 sorterer hver pool på `(source_file_id, segment_id)` og linje 59 trekker `rng.sample(pool, min(PER_DIALEKT, len(pool)))`. `--per-dialekt 60` ble brukt (PREREG avvik 4).

Tall regnet på nytt 2026-10-27 fra `test_metadata.jsonl` og `…utvalg.json` (ikke fra meldinger):

| steg | rader |
|---|---|
| alle rader i `test_metadata.jsonl` | 1 195 |
| uten overlapp mot forrige segment | 921 |
| uten overlapp mot neste segment | 748 |
| varighet 2–12 s | 428 |
| minst tre ord i `orthographic` | 428 |
| trukket (opptil 60 per område) | 252 |

| område | rader | pool etter filter | trukket | bm/nn i pool | bm/nn i utvalget |
|---|---|---|---|---|---|
| e | 557 | 181 | 60 | 175 / 6 | 57 / 3 |
| n | 261 | 90 | 60 | 85 / 5 | 57 / 3 |
| sw | 163 | 85 | 60 | 24 / 61 | 19 / 41 |
| t | 78 | 21 | 21 (alle) | 18 / 3 | 18 / 3 |
| w | 136 | 51 | 51 (alle) | 8 / 43 | 8 / 43 |
| sum | 1 195 | 428 | 252 | 310 / 118 | 159 / 93 |

Utvalget har 159 bokmåls- og 93 nynorskssegmenter fra 51 talere. Skriftform og dialekt er sammenblandet (sw og w er mest nynorsk, e og n mest bokmål), som PREREG påpeker.

## Intervallmetode (AV-13, PREREG avvik 7 og 11a)

Kode: `scripts/rapporter_intervaller.py`. Clusterbootstrap over taler (`speaker_id`): `wer_intervaller`, linje 60–87; B = 2000 (`B`, linje 29), seed 20261026 (`SEED`, linje 30), `random.Random(seed)` (linje 76), like mange talere som det finnes trekkes med tilbakelegging (linje 77), alle segmentene til de trukne talerne følger med, bootstrap-WER = Σ feil / Σ referanseord per gjentak (linje 81), punktestimatet er e/n over alle segmenter (linje 82). Samme trekk brukes for alle kolonner og grupper (parret); K1 bruker det samme trekket (linje 84–87). Persentilintervall: `persentil`, linje 49–51, nedre = element `int(0,025·B)`, øvre = element `int(0,975·B) − 1` av de sorterte verdiene. Kommando: `.venv/bin/python scripts/rapporter_intervaller.py wer <resultat.json> <utvalg.json>`.

## Kjøring

Metafil: `KLAR-EVAL-0013_arkivklarering_test-nbsamtale-wer_v1.0_2026-10-27_kjoring_meta.json`. Start 2026-10-27T07:42:54Z på commit `279f301ded06dc88052451043dfb65a9e0cbf571`, slutt 09:21:45Z, returkode 0, `git status --porcelain` tom ved start, kode uendret siden `testkjoring-v2` (`c49d17463c14f7719f9f271ae3d4af4824436c35`). Resultat committet som `1be7358`. Modeller og sha256 står i v1.0-dokumentet.
