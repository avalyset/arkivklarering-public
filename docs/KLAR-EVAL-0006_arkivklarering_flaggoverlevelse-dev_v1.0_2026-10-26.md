# KLAR-EVAL-0006: Hvor mange personvernflagg overlever talegjenkjenningen? (DEV)

Versjon 1.0, 2026-10-26. **DEV, ikke pilot. Ingen konklusjoner om pilotkvalitet.** Generert av `eval/dev/kjor_flaggoverlevelse_dev.py` (tall); tolkning skrevet for hånd.

## Oppsett

- Samme 60 segmenter fra `Sprakbanken/nb_samtale` (validation, seed 20261026; `KLAR-EVAL-0003`) og de lagrede hypotesene fra DEV-kjøringen av WER (`KLAR-EVAL-0002`). **Whisper ble ikke kjørt på nytt.** Lisens CC0 (`KLAR-EVAL-0004`).
- **Referanse:** personvernmotoren (Presidio med spaCy `nb_core_news_md`, NB-BERT-base-ner, mønstre og nøkkelordlister, terskel 0) på den menneskelige ortografiske transkripsjonen.
- **Rørledning:** samme motor på rålaget (verbatim) og det normaliserte laget, og union av dem (`personvern.slaa_sammen_lag`; samme kategori, hele segmentet regnes som overlappende tid, ingen terskel). Primært `-l nn` for alle segmenter (slik rørledningen kjører); `matchet` (språk etter fasitens skriftform) står sist.
- **Overlevelse (a):** andelen referanseflagg som har minst ett rørledningsflagg i samme kategori i samme segment. **Streng (b):** i tillegg deler flaggene minst ett ord eller det ene utdraget inneholder det andre. **Ekstra:** andelen rørledningsflagg (union) uten referanseflagg i samme kategori i samme segment, regnet som (a) og (b). Flagg i samme lag og kategori med overlappende tegnspenn telles som én omtale. Intervallet er Wilson-95 % for (a) i union.

## Antall referanseflagg per kategori (n)

| kategori | referanseflagg | segmenter med minst ett |
|---|---|---|
| person | 17 | 13 |
| sted | 14 | 9 |
| organisasjon | 3 | 3 |
| dato | 0 | 0 |
| fødselsår | 0 | 0 |
| telefon | 0 | 0 |
| fødselsnummer | 0 | 0 |
| e-post | 0 | 0 |
| helse | 0 | 0 |
| økonomi | 0 | 0 |
| konflikt | 0 | 0 |
| religion | 0 | 0 |
| politikk | 0 | 0 |

**Disse tallene er for små til å bety noe for de fleste kategoriene.** Tre kategorier har referanseflagg (person 17, sted 14, organisasjon 3), og ti har ingen: dato, fødselsår, telefon, fødselsnummer, e-post, helse, økonomi, konflikt, religion og politikk. For dem er overlevelse **ikke målt**. Datasettkortet sier ikke om navn er anonymisert, men 17 personomtaler på 60 korte segmenter tyder på få navn.

## Resultat, `-l nn` (rørledningens oppsett)

| kategori | n ref | ra | normalisert | union | 95 %-int. (union, a) | union-flagg | ekstra (a) | ekstra (b) |
|---|---|---|---|---|---|---|---|---|
| person | 17 | 12/17 (0,71) · streng 0,59 | 12/17 (0,71) · streng 0,71 | **14/17 (0,82) · streng 0,77** | 0,590–0,938 | 20 | 0,25 (5) | 0,40 (8) |
| sted | 14 | 10/14 (0,71) · streng 0,64 | 13/14 (0,93) · streng 0,64 | **14/14 (1,00) · streng 0,93** | 0,785–1,000 | 16 | 0,06 (1) | 0,19 (3) |
| organisasjon | 3 | 1/3 (0,33) · streng 0,33 | 3/3 (1,00) · streng 1,00 | **3/3 (1,00) · streng 1,00** | 0,438–1,000 | 5 | 0,40 (2) | 0,40 (2) |
| økonomi | 0 | – | – | – | – | 1 | 1,00 (1) | 1,00 (1) |

Cellene viser overlevd/referanse (andel) · streng andel. «ra» og «normalisert» er hvert lag alene; «union» er rørledningens flagg.

## Resultat, språk etter fasitens skriftform (`matchet`)

| kategori | n ref | ra | normalisert | union | 95 %-int. (union, a) | union-flagg | ekstra (a) | ekstra (b) |
|---|---|---|---|---|---|---|---|---|
| person | 17 | 11/17 (0,65) · streng 0,59 | 12/17 (0,71) · streng 0,71 | **14/17 (0,82) · streng 0,77** | 0,590–0,938 | 17 | 0,18 (3) | 0,29 (5) |
| sted | 14 | 10/14 (0,71) · streng 0,64 | 13/14 (0,93) · streng 0,86 | **14/14 (1,00) · streng 0,93** | 0,785–1,000 | 16 | 0,06 (1) | 0,19 (3) |
| organisasjon | 3 | 1/3 (0,33) · streng 0,33 | 3/3 (1,00) · streng 1,00 | **3/3 (1,00) · streng 1,00** | 0,438–1,000 | 6 | 0,50 (3) | 0,50 (3) |

## Vurdering (håndført)

- **Holder n? Nei, ikke til mer enn en grov retning.** Person (n = 17) og sted (n = 14) gir 95 %-intervaller på 0,59–0,94 (person) og 0,79–1,00 (sted) for overlevelse i union; org (n = 3) er ikke tolkbar, og ti kategorier har null referanseflagg. Forskjellen mellom ra, normalisert og union er noen få flagg (person: 12 mot 14 av 17; sted: 13 mot 14 av 14). Det kan ikke skilles fra tilfeldighet. Segmentene kommer fra 33 talere og to opptakstyper, og setninger fra samme taler er ikke uavhengige.
- **Retningen:** union fanger minst like mange referanseflagg som hvert lag alene, siden den beholder flagg som bare finnes i ett lag (person 0,824, sted 1,000). Rålaget alene lander lavere for sted (0,714) enn det normaliserte (0,929), i tråd med funnet på NorNE (`KLAR-EVAL-0005`) om at små bokstaver uten tegnsetting svekker navnegjenkjenning.
- **Pris:** en fjerdedel av unionens personflagg har ingen referanse i samme segment (streng: ca. 40 %). Noen er sannsynligvis ekte treff som referansemotoren ikke fant, andre er transkripsjonsfeil som ligner navn, andre falske flagg. Det er ikke undersøkt linje for linje, så andelen kan ikke tolkes som presisjon.
- **Referansen er ikke fasit.** Den er samme motor på riktig tekst, og den har selv recall under 1 (se NorNE). «Overlevelse» sier hvor mye av det motoren finner i riktig tekst den også finner i transkripsjonen, ikke hvor mye av alle personopplysninger som blir funnet.
- Dato, fødselsår, telefon, fødselsnummer og nøkkelordlistene kan ikke vurderes her. Det trengs et materiale der slike opplysninger faktisk forekommer (arkivopptak), og den målingen er pilotens oppgave.

Rådata: `KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.0_2026-10-26.json` (bare tall).
