# KLAR-EVAL-0005: Personvernflagging, DEV-måling på NorNE (validation)

Versjon 1.0, 2026-10-26. **DEV, ikke pilot. Ingen konklusjoner om kvalitet på arkivmateriale.** Generert av `eval/dev/kjor_personvern_dev.py` (tall) og skrevet for hånd (tolkning). Nummeret er 0005 fordi `KLAR-EVAL-0002` til `0004` allerede er brukt av DEV-målingen på NB Samtale, og et nummer gjenbrukes aldri (KLAR-ARK-0002).

## Lisens (ordrett)

Datasettkort `NbAiLab/norne`, revisjon `1ca12d437b84f65a34c454d339317d39d35c8149`, YAML: `license: other`. Seksjonen «Licensing Information», ordrett:

> The NorNE corpus is published under the same [license](https://github.com/ltgoslo/norne/blob/master/LICENSE_NDT.txt) as the Norwegian Dependency Treebank

`LICENSE_NDT.txt` (ltgoslo/norne, `master`), avsnittene som gjelder bruk, ordrett:

> To the extent possible under law, the National Library of Norway has waived all copyright and related or neighboring rights to the linguistic annotations in Norwegian Dependency Treebank. This work is published from: Norway. 
> (See http://creativecommons.org/publicdomain/zero/1.0/).
> The original third-party contents are not included in this CC0 license, and these individual works may not be republished as stand-alone texts. The original texts (with sources) are listed in
> The National Library of Norway has obtained permission from the authors/publishers to use the original texts for inclusion in Norwegian Dependency Treebank.

**Vurdering:** åpen for denne bruken. Annotasjonene er CC0. De opprinnelige tredjepartstekstene (aviser, blogger, stortingstekster, rapporter) er ikke dekket av CC0 og kan ikke gjenpubliseres som frittstående tekster. Målingen leser validation-delen lokalt, lagrer og skriver ut ingen setninger, og publiserer bare tall. Datasettkort og lisensfil er lagret ved dataene (`/Volumes/Vault/arkivklarering/eval-data/norne/`).

## Oppsett

- Data: `NbAiLab/norne`, configene `bokmaal` (2410 setninger) og `nynorsk` (1890 setninger), **kun validation**. `test` er sperret (`arkivklarering/evaldata.py`, krever `--prereg-id KLAR-PREREG-<NNNN>`). `ltg/norne` har ingen oppdeling i bokmål og nynorsk og er ikke brukt.
- Gull: PER → person; LOC og GPE_LOC → sted. GPE_ORG regnes som organisasjon og evalueres ikke (en stedsprediksjon på en GPE_ORG teller som falskt flagg).
- Motor: Presidio med `nb_core_news_md` (registrert for `nb` og `nn`; spaCy har ingen nynorskmodell), `NbAiLab/nb-bert-base-ner`, mønstre og ordlister; terskel 0,0. Bare flagg i kategoriene person og sted telles. Overlappende prediksjoner av samme type slås sammen.
- **Recall (overlapp)** er hovedmålet: andelen gullentiteter som overlappes av minst én prediksjon av samme type. Nøyaktig recall krever identisk start og slutt. Presisjon er regnet på samme måte over prediksjonene. 95 %-intervall for recall er Wilson-intervall, ikke korrigert for at setninger fra samme tekst ligner hverandre.
- Tekstformer: **original** (setningen slik NorNE har den) og **små** (små bokstaver, tegnsetting fjernet, slik rålaget skrives).
- Tidsbruk 661 s på CPU.

## Hovedresultat: hele motoren, original tekst

| målform | entitet | gull | predikert | recall (overlapp) | 95 %-int. | recall (nøyaktig) | presisjon (overlapp) | presisjon (nøyaktig) |
|---|---|---|---|---|---|---|---|---|
| bokmål | PER (person) | 611 | 661 | **0,997** | 0,988–0,999 | 0,982 | 0,921 | 0,908 |
| bokmål | LOC + GPE_LOC (sted) | 368 | 408 | **0,970** | 0,947–0,983 | 0,967 | 0,875 | 0,873 |
| nynorsk | PER (person) | 481 | 597 | **0,954** | 0,932–0,970 | 0,933 | 0,769 | 0,752 |
| nynorsk | LOC + GPE_LOC (sted) | 280 | 374 | **0,986** | 0,964–0,994 | 0,971 | 0,738 | 0,727 |

## Per gjenkjenner, original tekst (recall overlapp / presisjon overlapp)

| målform | entitet | NB-BERT-base-ner | spaCy `nb_core_news_md` | hele motoren |
|---|---|---|---|---|
| bokmål | PER (person) | 0,993 / 0,977 | 0,930 / 0,930 | 0,997 / 0,921 |
| bokmål | LOC + GPE_LOC (sted) | 0,946 / 0,936 | 0,870 / 0,896 | 0,970 / 0,875 |
| nynorsk | PER (person) | 0,950 / 0,981 | 0,834 / 0,751 | 0,954 / 0,769 |
| nynorsk | LOC + GPE_LOC (sted) | 0,968 / 0,897 | 0,729 / 0,701 | 0,986 / 0,738 |

## Små bokstaver uten tegnsetting (som rålaget), recall overlapp / presisjon overlapp

| målform | entitet | NB-BERT-base-ner | spaCy `nb_core_news_md` | hele motoren |
|---|---|---|---|---|
| bokmål | PER (person) | 0,527 / 0,988 | 0,592 / 0,890 | 0,715 / 0,901 |
| bokmål | LOC + GPE_LOC (sted) | 0,312 / 0,921 | 0,647 / 0,850 | 0,739 / 0,848 |
| nynorsk | PER (person) | 0,418 / 0,971 | 0,447 / 0,648 | 0,599 / 0,714 |
| nynorsk | LOC + GPE_LOC (sted) | 0,246 / 0,812 | 0,443 / 0,747 | 0,504 / 0,723 |

## Tolkning og forbehold (håndført)

- **Små bokstaver uten tegnsetting svekker gjenkjenningen kraftig.** Hele motorens recall for personer går fra 0,997 til 0,715 på bokmål og fra 0,954 til 0,599 på nynorsk; for steder fra 0,970 til 0,739 (bokmål) og fra 0,986 til 0,504 (nynorsk). Rålaget (verbatim) skrives slik, så navnegjenkjenning på rålaget er langt svakere enn på det normaliserte laget. Personvernflagg lages derfor på begge lag, og rålagets flagg er et supplement, ikke grunnlaget som KLAR-ADR-0005 antydet.
- **Dette er skrevet tekst, ikke tale.** NorNE er avis-, blogg-, stortings- og rapporttekst. Talespråk og dialekt, og transkripsjonsfeil i navn (ASR skriver «Kari» som «Karin»), er ikke med. Recall på transkripsjoner vil være lavere enn tallene her.
- **Overlapp med treningsdata er ikke kontrollert.** NB-BERT-base-ner er finjustert på NorNE (modellkortet), og spaCys norske pipeline er ikke sjekket her. Validation er ikke testdelen, men tallene er sannsynligvis optimistiske for tekst av denne typen.
- **Nynorsk er svakere enn bokmål**, særlig for spaCy, som bruker bokmålsmodellen også for `nn`. Kombinasjonen med NB-BERT-base-ner hever recall, men gir flere falske flagg (lavere presisjon) på nynorsk.
- **Terskel 0 gir lav presisjon på nynorsk** (hele motoren, original tekst, person). Det er et bevisst valg (KLAR-ADR-0012), ikke et funn om at motoren er dårlig.
- Ingen setninger er hoppet over: tokenjusteringen mot originalteksten lyktes for alle setninger.
- Kategoriene dato, fødselsår, telefon, fødselsnummer og nøkkelordlistene (helse, økonomi, konflikt, religion, politikk) er **ikke målt** her; det finnes ingen etablert gullstandard for dem i dette oppsettet. De har bare enhetstester.

Rådata: `KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_2026-10-26.json` (bare tall).
