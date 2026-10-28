**NB-Whisper er trent på NPSC. Talegjenkjenningen er derfor optimistisk her. Målingen gjelder flaggoverlevelse, ikke WER.**

# KLAR-EVAL-0007: Flaggoverlevelse på NPSC (DEV)

Versjon 1.0, 2026-10-26. **DEV, ikke pilot. Ingen konklusjoner om pilotkvalitet.** Tall generert av `eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc`; tolkning skrevet for hånd.

## Lisens (ordrett)

Datasettkort `NbAiLab/NPSC`, revisjon `e906435cc445e38961d86f3ebf53a7b38603b903`, YAML: `license: cc0-1.0`. Seksjonen «License», ordrett:

> The sound and the transcriptions are released under the [CC-ZERO-license](https://creativecommons.org/publicdomain/zero/1.0/). The curation of the HuggingFace Dataset is released under [CC-BY-SA-3-license](https://creativecommons.org/licenses/by-sa/3.0/).

Seksjonen «Considerations for Using the Data», ordrett:

> This corpus contains speech data. All recordings are of members of Parliament in a public setting, and can be distributed without any restrains.

`license.md` i datasettrepoet, ordrett:

> ## License CC-ZERO(https://creativecommons.org/publicdomain/zero/1.0/)

**Vurdering:** åpen for denne bruken. Lyd og transkripsjoner er CC0. Kurateringen av HF-datasettet (ikke dataene) er CC-BY-SA 3; vi bruker de opprinnelige filene og publiserer bare tall. Datasettkort og lisensfil er lagret ved dataene (`/Volumes/Vault/arkivklarering/eval-data/npsc/`).

## Stoppregel og utvalg (fastsatt uten å se utfall)

- **Datadel:** `validation` (mappen `eval/` i `NbAiLab/NPSC`; fem møter: 20170209, 20180109, 20180201, 20180307, 20180611), 16 kHz mp3. `test` er sperret i koden (`arkivklarering/evaldata.py`, krever `--prereg-id`). Referansen er feltet `normsentence_text`; målformen er `sentence_language_code`.
- **Utvalg:** segmenter på 1,5–25 s med ikke-tom referansetekst, trukket med fast seed (20261026) i en vektet rundtur på to bokmålssegmenter per nynorsksegment (nynorsk er ca. 13 % av segmentene), utvidet gradvis til minst 150 person- og 100 stedsflagg i referansen (begge målformer sammen) eller 2 timer lyd. Utvalget ble 936 segmenter og 1,98 timer.
- **Stoppregelen (v0.3-prompten, bekreftet senere):** det minste prefikset av utvalget i seed-rekkefølgen som gir minst 150 personflagg og 100 stedsflagg i referansen. Den ble regnet ut med personvernmotoren på de menneskelige transkripsjonene, uten Whisper, **2026-10-26T14:25:47+01:00, før noe rørledningsresultat for NPSC var lest** (bare antall ferdige segmenter i cachen, 400, var kjent). **Prefikslengde: 934 av 936 segmenter** (623 bokmål og 311 nynorsk, 7103 s lyd), med 150 personflagg og 102 stedsflagg i referansen.
- **Whisper** var kommet til 400 segmenter da regelen var regnet ut. Den ble stoppet og startet på nytt og kjørte bare de 534 som gjensto, til prefikset og ikke lenger. De to siste segmentene i utvalget er ikke kjørt og ikke evaluert.
- **Referanseflagg i prefikset** (omtaler): bokmål person 85, sted 80; nynorsk person 65, sted 22.

## Oppsett

- Rørledningen er den samme som i `KLAR-EVAL-0006` v1.1: segmentering, rålag (verbatim) og normalisert lag med DTW-ordtidsstempler, personvernflagg på begge lag og union paret på ordspenn. **Språk etter målform** (bokmål `-l no`, nynorsk `-l nn`), ikke `-l nn` for alle som i 0006. Modellene: `nb-whisper-large-verbatim` sha256 `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d`, `nb-whisper-large` sha256 `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76`.
- Kjøringen gikk som ett Whisper-kall per lag og språk per gruppe på 40 segmenter (modellen lastes én gang), og er ikke bitidentisk med én prosess per fil. Ressursvakten (minst 8 GiB ledig intern disk, høyst 6,5 GB swap) slo aldri til, ingen whisper-cli-krasj, ingen segmenter måtte kjøres uten DTW. Fem segmenter ga ingen rålagscue og tre ingen normalisert cue (tomt Whisper-resultat); de er med i evalueringen med null flagg.
- **Overlevelse (a):** referanseflagget har minst ett rørledningsflagg i samme kategori i samme segment. **Streng:** i tillegg delt ord eller inneholdt utdrag. **Ekstra:** rørledningsflagg uten referanseflagg i samme kategori i samme segment. 95 %-intervallene er Wilson-intervaller; segmenter fra samme møte og taler er ikke uavhengige, så intervallene er for smale.

## Resultat per målform (union = rørledningens flagg)

| målform | kategori | ra (verbatim) | normalisert | **union** | union-flagg | ekstra (a) | ekstra (streng) |
|---|---|---|---|---|---|---|---|
| bokmål (623 seg.) | person | 67/85 = **0,788** [0,690–0,862] · streng 0,753 | 80/85 = **0,941** [0,870–0,975] · streng 0,871 | 83/85 = **0,976** [0,918–0,994] · streng 0,929 | 112 | 4 (0,036) | 8 (0,071) |
| bokmål (623 seg.) | sted | 51/80 = **0,637** [0,528–0,734] · streng 0,575 | 74/80 = **0,925** [0,846–0,965] · streng 0,875 | 74/80 = **0,925** [0,846–0,965] · streng 0,875 | 92 | 17 (0,185) | 22 (0,239) |
| nynorsk (311 seg.) | person | 43/65 = **0,662** [0,540–0,765] · streng 0,615 | 52/65 = **0,800** [0,687–0,879] · streng 0,662 | 56/65 = **0,862** [0,757–0,925] · streng 0,754 | 88 | 18 (0,205) | 28 (0,318) |
| nynorsk (311 seg.) | sted | 5/22 = **0,227** [0,101–0,434] · streng 0,182 | 18/22 = **0,818** [0,615–0,927] · streng 0,727 | 18/22 = **0,818** [0,615–0,927] · streng 0,727 | 30 | 11 (0,367) | 13 (0,433) |

Celler: overlevd/referanse = andel [95 %-int.] · streng andel.

## Begge målformer samlet

| kategori | n ref | ra | normalisert | **union** | union-flagg | ekstra (a) |
|---|---|---|---|---|---|---|
| person | 150 | 110/150 = 0,733 | 132/150 = 0,880 | **139/150 = 0,927** [0,873–0,959] | 200 | 22 (0,110) |
| sted | 102 | 56/102 = 0,549 | 92/102 = 0,902 | **92/102 = 0,902** [0,829–0,946] | 122 | 28 (0,230) |

## Kategorier som ikke er målt (ikke målt – krever eget testmateriale)

**Ikke målt – krever eget testmateriale:** helse, økonomi, konflikt, religion, politikk, dato, fødselsår, telefon, fødselsnummer og e-post. Overlevelse er ikke regnet for dem, og organisasjon er heller ikke med (ikke bestilt). Personvernmotoren fant likevel referanseflagg i noen av dem i NPSC-prefikset (antall omtaler, bare for informasjon, ikke kontrollert for om de er riktige): bokmål: dato 1, helse 15, organisasjon 208, politikk 42, religion 1, telefon 4, økonomi 5; nynorsk: dato 3, helse 10, konflikt 1, organisasjon 87, politikk 9, økonomi 5. Stortingstale er ikke representativt for disse kategoriene, og nøkkelordlistene er ikke validert mot noe gullsett. De får egne tall fra kjedekalibreringen (`KLAR-EVAL-0008`, syntetisk) og fra menneskeinnlest manus før preregistrert måling.

## Vurdering (håndført)

- **n.** Stoppregelen ga 150 person- og 102 stedsreferanseflagg samlet. Per målform er n mindre: nynorsk sted har bare 22 referanseflagg (intervallet er 0,615–0,927) og kan ikke tolkes sikkert. Bokmål person (85) og sted (80) og nynorsk person (65) er brukbare for en retning.
- **Retning.** Unionen overlever best for personer (bokmål 0,976, nynorsk 0,862). For steder gir unionen **ingen gevinst** over det normaliserte laget alene (bokmål og nynorsk: samme antall); rålaget alene mister de fleste nynorske steder (5 av 22). Det samsvarer med funnet på NorNE (`KLAR-EVAL-0005`) om at små bokstaver uten tegnsetting svekker navnegjenkjenning.
- **Pris.** Unionen gir flere flagg uten referanse i samme segment, særlig på nynorsk: person 20,5 % (streng 31,8 %), sted 36,7 % (streng 43,3 %), mot 3,6 % og 18,5 % på bokmål. Det kan være ekte treff som referansen ikke har, transkripsjonsfeil som ligner navn eller falske flagg; det er ikke undersøkt linje for linje.
- **Optimisme.** NB-Whisper-kortet oppgir stortingstaler fra Språkbanken som treningsdata og sier ikke hvilke deler; validation-delen av NPSC kan ligge i treningsdataene. Tallene sier derfor lite om hvordan talegjenkjenningen vil gjøre det på arkivlyd, og de kan ikke sammenlignes med `KLAR-EVAL-0006` (annet materiale, annet språkvalg).
- **Referansen er ikke fasit.** Den er samme motor på riktig tekst, med recall under 1 (`KLAR-EVAL-0005`). «Overlevelse» sier hvor mye av det motoren finner i riktig tekst den også finner i transkripsjonen.

Rådata: `KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_2026-10-26.json` (bare tall; segment-ID-ene ligger i filen, ikke tekst).
