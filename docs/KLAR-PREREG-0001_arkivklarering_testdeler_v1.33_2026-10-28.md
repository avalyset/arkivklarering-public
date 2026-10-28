# KLAR-PREREG-0001: Preregistrering av målingene på testdelene (arkivklarering v0.4)

Status: registrert https://osf.io/hc83q/

Mal: OSF Preregistration (feltene hentet fra https://api.osf.io/v2/schemas/registrations/697b72f611a8e98484c6139b/schema_blocks/, lagret ved dataene). Versjon 1.33, 2026-10-28 (v1.33: DOI for den tilgangsstyrte historikken er satt inn: 10.5281/zenodo.23723450 (steg 4.5); v1.32: bare avviksseksjonen: AV-34 (punkt 27 og tabellraden; A3 endret); v1.31: bare avviksseksjonen: AV-33 (punkt 26 og tabellraden; kodetaggen `testkjoring-v10`, mekanisk pekersjekk); v1.30: bare avviksseksjonen: pekere til versjoner som ikke er i treet er merket «(i git-historikken)», og pekere med linjenummer til forrige versjon av et dokument med ny versjon viser til den nye versjonen, samme linje; kontrollert med `scripts/sjekk_pekere.py`, 0 brudd (KLAR-LOG-0005, restfunn etter kontrollen); v1.29: bare avviksseksjonen: raden for AV-25 i oppsummeringstabellen sier at H4 utgår (AV-27), og AV-32 (punkt 25 og tabellraden) tar med endringen i GT-generatoren (porten, runde 3 (KLAR-LOG-0005), funn 8 og 15); v1.28: bare avviksseksjonen: punkt 24 (regelen for H4-tersklene i den registrerte teksten stemmer ikke med tabellen for person og sted, AV-31; den registrerte teksten er ikke endret) og punkt 25 (kodetaggen `testkjoring-v9`, AV-32), radene AV-31 og AV-32 i oppsummeringstabellen, raden AV-19 merket lukket av AV-27, linjen «Usikre celler» (AV-30 begrunnet med det som ikke er endret; AV-31), `modeller.lock.json` i punkt 23, seksjonsnavnet «Data collection procedures» i punkt 4, henvisningene til KLAR-LOG-0001 (fortløpende; nyeste v1.48) og henvisningen over tabellen («KLAR-LOG-0003 v1.17», «punktene 1–25»); ingen terskel og ingen annen tekst endret; v1.27: bare punkt 23 i avviksseksjonen (kodetaggene `testkjoring-v7` og `testkjoring-v8`; VTT-merknaden om musikk under tale rettet etter ADR-0019, AV-30), raden AV-30 i oppsummeringstabellen, linjen «Usikre celler» og henvisningen over tabellen («KLAR-LOG-0003 v1.15», «punktene 1–23»); ingen terskel og ingen annen tekst endret; v1.26: bare punkt 22 i avviksseksjonen (telefonnumrene i KLAR-MANUS-0001 og -0002 byttet til Nkoms fiktivserie 68 05 00 00–68 05 99 99, AV-29), raden AV-29 i oppsummeringstabellen, linjen «Usikre celler» og henvisningen over tabellen («KLAR-LOG-0003 v1.14», «punktene 1–22»); ingen terskel og ingen annen tekst endret, heller ikke sha256 for den registrerte MANUS-0002 v1.2; v1.25: bare punkt 21 i avviksseksjonen (kodeendringer etter `testkjoring-v5`: cache-stier per segmentering, datarot `ARKIVKLARERING_DATA`, tester i rent miljø; tag `testkjoring-v6`, AV-28), raden AV-28 i oppsummeringstabellen, linjen «Usikre celler» og henvisningen over tabellen («KLAR-LOG-0003 v1.13», «punktene 1–21»); ingen terskel og ingen annen tekst endret; v1.24: bare punkt 20 i avviksseksjonen (H4 gjennomføres ikke i v1.0, AV-27), raden AV-27 i oppsummeringstabellen, linjen «Usikre celler» og henvisningen over tabellen («KLAR-LOG-0003 v1.12», «punktene 1–20»); ingen terskel og ingen annen tekst endret; v1.23: bare punkt 19 i avviksseksjonen (inaSpeechSegmenter er standard segmentering i koden, inaVAMOS valgfritt tillegg, tag `testkjoring-v5`), raden AV-26 i oppsummeringstabellen og henvisningen over tabellen («KLAR-LOG-0003 v1.10», «punktene 1–19»); ingen terskel og ingen annen tekst endret; v1.22: bare OSF-statusen for metoderegistreringen fbme7 i linjen under (status sett i innlogget OSF-økt 2026-10-27, kan ikke etterprøves offentlig før embargoen oppheves; KLAR-KILDE-0001 OS-01); ingen terskel og ingen annen tekst endret; v1.21: bare en oppsummeringstabell øverst i avviksseksjonen (B6 i KLAR-ARK-0008); ingen terskel og ingen annen tekst endret; v1.20: bare punkt 18 i avviksseksjonen uten setningen om sensitivitetskjøring (utgår, eiers endring); ingen terskel og ingen annen tekst endret; v1.19: bare punkt 18 i avviksseksjonen (inaVAMOS erstattes av inaSpeechSegmenter fra H4); ingen terskel og ingen annen tekst endret; v1.18: bare punkt 17 i avviksseksjonen (primærintervall for H3, eiers beslutning); ingen terskel og ingen annen tekst endret; v1.17: bare punkt 15–16 i avviksseksjonen (H4-innleseren endret etter registrering; sha256 for testdataene ført etter H1-start); ingen terskel og ingen annen tekst endret; v1.16: bare punkt 14 i avviksseksjonen (rekkefølgen H1–H3 før H4); v1.15: bare punkt 12–13 i avviksseksjonen (innspillingsprotokoll for H4, kodetagg `testkjoring-v2`); v1.14: bare punkt 9–11 i avviksseksjonen (tellere per setning for NorNE, kodesjekk mot taggen `testkjoring-v1`, bekreftede beslutninger); v1.13: bare punkt 4–8 i avviksseksjonen (H1-utvalg, navn på testresultater, bevis for uendret utregning, intervallmetode, H4-begrensning); v1.12: bare punkt 3 i avviksseksjonen utvidet (commit, push og speil etter hver testdel); v1.11: bare punkt 3 i avviksseksjonen (kjøringsmetadata utenfra); v1.10: bare en ny avviksseksjon etter registreringen («Avvik etter registrering», nederst); ingen annen tekst og ingen terskel endret; den registrerte og opplastede versjonen er v1.8; v1.9: bare statuslinjen, satt etter innsending på OSF 2026-10-27 (https://osf.io/hc83q/, embargo til 2027-10-26); innholdet er ellers identisk med v1.8, som er den registrerte og opplastede versjonen (git-tag `prereg-v1` = `bfe647dbe27de68fcf4abd4bf563ecfbf63f8070`); v1.8: bare tekstrettelser, ingen tall og ingen terskel endret: «Manuset (v1.2)», presisert at koden (ikke mappene) er identisk med taggen, henvisningen fra H2f peker på riktig seksjonsnavn; v1.7: rålaget kjøres med `-nt` (KLAR-ADR-0017) etter KLAR-EVAL-0011; ny DEV for de berørte EVAL-ene; **bare terskelene H1a og H1d er satt på nytt, med uendret regel** (DEV + 0,10, rundet opp til nærmeste 0,05): H1a ≤ 0,35 → ≤ 0,25, H1d ≤ 0,45 → ≤ 0,35; alle andre terskler, testmanusets sha256 og kontrollsjekkene er uendret; ny analyse-kode-tag `h4-script-v2`; testdelene er fortsatt ikke åpnet; v1.6: kjent begrensning ved rålaget (tomt/kort utdata) ført inn etter KLAR-EVAL-0011; ingen terskel og ingen hash endret; v1.5: testmanuset rettet til v1.2 (oko04nn: «betalingsmerknaden», formen Nynorskordboka har), ny sha256; analyse-koden (tag h4-script-v1) er uendret; føres som avvik i KLAR-LOG-0001; v1.4: «versjon 4 av» fjernet fra malbeskrivelsen etter kildekontroll (KLAR-KILDE-0001, VT-04); hashen av testmanuset er uendret; føres som avvik i KLAR-LOG-0001; v1.3: analyse-kode for H4 låst, commit og tag ført inn; hashen av testmanuset er uendret fra v1.2; v1.2: testmanuset rettet før låsing, `KLAR-MANUS-0002` v1.1 med ny sha256, se `KLAR-LOG-0001`; v1.1: omdøpt fra `_pilot_` til `_testdeler_`; primærutfall og sekundære utfall skilt; kontrollsjekker flyttet ut av hypotesene; H4 flyttet til et eget, urørt testmanus, `KLAR-MANUS-0002`). Forfatter: Eirik Botten Nicolaysen, EcoDeco AS (ORCID 0009-0001-9188-6788).
Metoderegistreringen som denne bygger på er registrert på OSF: <https://osf.io/fbme7/> (under embargo til 2027-10-26; status sett i innlogget OSF-økt 2026-10-27, kan ikke etterprøves offentlig før embargoen oppheves). Dette dokumentet gjelder målingene på offentlige datasett og på et eget manus, ikke noe materiale fra museet. Museumspiloten får en egen preregistrering, `KLAR-PREREG-0002` (reservert; lages først etter ja fra museet og før pilotdata kjøres, `docs/gt_fast.md`, KLAR-ADR-0010).

**Ved innsending:** endre statuslinjen over til `Status: registrert <OSF-URL>` i en egen commit. Først da åpner `--prereg-id KLAR-PREREG-0001` testdelene (se «Annen informasjon»), og først da kan rørledningen lese `KLAR-MANUS-0002`. Dette utkastet åpner ingenting.

## Overview

### Research questions or hypotheses

Verktøyet arkivklarering foreslår hva et menneske må vurdere før et lydarkiv publiseres. Alle terskler under er satt **uten å ha sett noen testdata**, på grunnlag av DEV-målingene på valideringsdelene (`KLAR-EVAL-0002`, `-0005`, `-0006`, `-0007`) og den syntetiske kjedekalibreringen på justeringsmanuset (`KLAR-EVAL-0008`, `KLAR-MANUS-0001`). Ingen av DEV-tallene sier noe om kvalitet på arkivlyd. En hypotese regnes som **bekreftet** når punktestimatet oppfyller terskelen; 95 %-intervallet rapporteres alltid, og en hypotese er «klart bekreftet» bare når også intervallgrensen oppfyller terskelen.

**Primærutfall er H1 og H2.** Alt annet (H1b, H1d, H1e, H3, H4 og kontrollsjekkene) er **sekundært** og merkes slik i rapporteringen; et sekundært utfall brukes ikke til å redde eller felle primærutfallene.

**H1 (primær). Talegjenkjenning: WER for rålaget, målform matchet mot fasiten (NB Samtale test, DEV: `KLAR-EVAL-0002`, «ra/matchet»).** Språk etter fasitens skriftform for hvert segment (bokmål `-l no`, nynorsk `-l nn`), rålaget (`nb-whisper-large-verbatim`), korpus-WER mot `orthographic`, normalisert som i DEV.

Begrunnelse for valget av primærutfall: fasiten (`orthographic`) er ordrett og har målformen til hvert segment. WER måler gjenkjenning bare når laget og språkvalget svarer til fasiten: det ordrette rålaget med riktig målform. Det normaliserte laget, og `-l nn` for alle segmenter mot en bokmålsfasit, måler normalisering og rettskrivning, ikke gjenkjenning. De to siste er driftskonfigurasjonen og føres derfor som sekundære utfall.

| id | utfall | DEV (validation, 60 segmenter) | terskel |
|---|---|---|---|
| **H1a (primær)** | WER, rålag, målform matchet mot fasiten (ra/matchet) | 0,135 | ≤ 0,25 |
| H1b (sekundær) | WER, normalisert lag, målform matchet (normalisert/matchet) | 0,348 | ≤ 0,45 |
| H1d (sekundær) | WER, rålag med `-l nn` for alle segmenter (driftskonfigurasjonen, ra/nn) | 0,248 | ≤ 0,35 |
| H1e (sekundær) | WER, normalisert lag med `-l nn` for alle segmenter (driftskonfigurasjonen, normalisert/nn) | 0,463 | ≤ 0,60 |

Terskelen er DEV-estimatet pluss 0,10 absolutt, rundet opp til nærmeste 0,05. Marginen er valgt fordi DEV bygger på 60 segmenter, og fordi dialekt og skriftform er sammenblandet i DEV-utvalget. (H1c er flyttet til kontrollsjekkene.)

**Avvik: «rålag endret til -nt etter EVAL-0011, terskler satt på nytt med uendret regel».** I v1.6 var DEV-grunnlaget for H1a og H1d målt med et rålag som av og til ga tomt eller avkortet utdata (KLAR-EVAL-0011). Rålaget kjøres nå med `-nt` (KLAR-ADR-0017), og DEV er målt på nytt (KLAR-EVAL-0002 v1.1; det normaliserte laget er gjenbrukt fra lagret utdata, siden modellen og parametrene er uendret). Rålagets DEV-WER ble 0,135 (matchet; før `-nt` 0,250) og 0,248 (`-l nn`; før 0,317). Regelen over er anvendt uendret på de to nye tallene: ceil((0,1353 + 0,10)/0,05) × 0,05 = 0,25 (H1a) og ceil((0,2480 + 0,10)/0,05) × 0,05 = 0,35 (H1d). Samme regel på de gamle tallene gir de gamle tersklene (0,35 og 0,45), så regelen er den samme. H1b (0,348 → ≤ 0,45) og H1e (0,463 → ≤ 0,60) har uendret DEV (laget er ikke berørt) og dermed uendrede terskler; H2–H4 er ikke endret fordi unionen i H2 og tersklene i H3 og H4 ikke er satt fra de berørte tallene (DEV for H2 er identisk, H3 bruker ikke Whisper, H4-tørrtesten består som før). Tersklene er satt etter å ha sett ny DEV, men før testdelene er åpnet. Avviket er også ført i `KLAR-LOG-0001`.

**H2 (primær). Flaggoverlevelse for UNION per kategori (NPSC test, DEV: `KLAR-EVAL-0007`).** Overlevelse (a) i unionen av rålag og normalisert lag: andelen referanseflagg i en kategori som har minst ett rørledningsflagg i samme kategori i samme segment. Referansen er personvernmotoren på den menneskelige transkripsjonen (`normsentence_text`). Språk etter målform.

**NB-Whisper er trent på NPSC; overlevelsestallene er optimistiske for talegjenkjenningen.**

| id | kategori og gruppe (union) | DEV (prefiks 934 segmenter) | terskel |
|---|---|---|---|
| H2a | person, begge målformer samlet | 0,927 (139/150) | ≥ 0,85 |
| H2b | sted, begge målformer samlet | 0,902 (92/102) | ≥ 0,80 |
| H2c | person, bokmål | 0,976 (83/85) | ≥ 0,90 |
| H2d | sted, bokmål | 0,925 (74/80) | ≥ 0,80 |
| H2e | person, nynorsk | 0,862 (56/65) | ≥ 0,75 |
| H2f | sted, nynorsk | 0,818 (18/22) | ingen bekreftende terskel: DEV-n er 22 (se «Other planned analysis (utforskende)»); rapporteres |

**Sekundært. H3. Navnegjenkjenning (NorNE test, DEV: `KLAR-EVAL-0005`).** Hele motoren, terskel 0, original tekst; recall (overlapp) er hovedmålet (KLAR-ADR-0012), presisjon (overlapp) sekundær.

| id | gruppe | DEV recall | terskel recall | DEV presisjon | terskel presisjon |
|---|---|---|---|---|---|
| H3a | bokmål, person (PER) | 0,997 | ≥ 0,95 | 0,921 | ≥ 0,85 |
| H3b | bokmål, sted (LOC + GPE_LOC) | 0,970 | ≥ 0,95 | 0,875 | ≥ 0,80 |
| H3c | nynorsk, person | 0,954 | ≥ 0,90 | 0,769 | ≥ 0,70 |
| H3d | nynorsk, sted | 0,986 | ≥ 0,95 | 0,738 | ≥ 0,65 |

**Sekundært. H4. Flaggkjeden på menneskeinnlest testmanus, per kategori.** Måles **kun** på menneskeinnlest `KLAR-MANUS-0002` (156 setninger, 6 per klasse og målform, 13 klasser). Manuset (v1.2) er urørt testmateriale: det er skrevet og rettet (språkform kontrollert mot Nynorskordboka og Bokmålsordboka, personnavn i setninger med sensitiv kategori byttet til etternavn uten treff i SSBs navnesøk) uten å kjøre noen setning gjennom rørledningen, mønstrene eller ordlistene, og rørledningen kan ikke lese det før denne preregistreringen er registrert (`kalibrering.les_manus`, `tests/test_manus.py`). **Sha256 av fila `kalibrering/KLAR-MANUS-0002_arkivklarering_testmanus_v1.2_2026-10-26.tsv`: `9a3d12d1e2438b09f9fcb6aa43300ace406888732d058e3cbabf70cb0ad963b1`.** Justeringsmanuset `KLAR-MANUS-0001` (nytt navn `justeringsmanus`) er brukt til å justere mønstrene og tersklene og inngår ikke i H4. Målet er andelen målelementer (union av lagene) som har et flagg i riktig kategori som dekker elementet (`flagg_treff`), samlet over alle opptak av testmanuset. Innlesingen gjøres og scores før testdelene kjøres.

**Analyse-kode låst (H4):** `kalibrering/kjor_h4.py` (scoring av menneskeinnleste opptak mot tersklene under), sammen med resten av koden i commit `224bd0a497b4bbba73efd8840992162fef825afd`, git-tag `h4-script-v2` (erstatter `h4-script-v1` = `55bb7914f441caafaaf2ca1343f088ba29f4959a`, som er beholdt og ikke flyttet; forskjellen er `-nt` for rålaget, KLAR-ADR-0017). Koden som ga DEV-tallene (`scripts/reproduser.sh` på commit `d75bc40`) er identisk med taggen: ingen .py-fil i `arkivklarering/`, `kalibrering/`, `eval/` eller `tests/` er endret siden taggen. Under `eval/` er det bare lagt til resultatfiler (EVAL-0002 v1.1 og H4-tørrtesten), og i `scripts/` bare `lag_nt_versjoner.py`, som ikke brukes i noen måling. Skriptet er testet end-to-end på de syntetiske filene av justeringsmanuset («tørrtest på justeringsmanus», `eval/dev/h4_torrtest_justeringsmanus_2026-10-27.md`; alle tolv kategorier består, som før `-nt`); oppsettet er språk etter målform («matchet»). Endringer i denne koden etter taggen føres som avvik i `KLAR-LOG-0001` før resultatet brukes.

Tersklene er beholdt uendret. **Grunnlaget for dem er «satt fra syntetisk kjøring på justeringsmanuset»** (en TTS-stemme, `KLAR-EVAL-0008`, `KLAR-MANUS-0001`), og de er forhåndsregistrert på menneskeinnlest testmanus. De er satt lavere enn de syntetiske tallene fordi menneskestemmer og dialekt gir flere transkripsjonsfeil.

| kategori | grunnlag: syntetisk kjøring på justeringsmanuset (union, flagg-treff/n, begge målformer, etter rettelsen av mønstre) | terskel (på menneskeinnlest `KLAR-MANUS-0002`) |
|---|---|---|
| person | 18/26 (0,69) | ≥ 0,60 |
| sted | 33/40 (0,82) | ≥ 0,70 |
| dato | 14/14 (1,00) | ≥ 0,70 |
| fødselsår | 16/18 (0,89) | ≥ 0,70 |
| telefon | 12/14 (0,86) | ≥ 0,60 |
| fødselsnummer | 10/12 (0,83) | ≥ 0,50 |
| e-post | 0/12 (0,00) | forventet negativt: ≤ 0,10 (kjent begrensning: Whisper skriver ikke talte e-postadresser som adresser) |
| helse | 26/26 (1,00) | ≥ 0,75 |
| økonomi | 19/22 (0,86) | ≥ 0,70 |
| konflikt | 22/26 (0,85) | ≥ 0,65 |
| religion | 12/16 (0,75) | ≥ 0,55 |
| politikk | 16/18 (0,89) | ≥ 0,70 |

Terskelen er det syntetiske tallet minus 0,15 til 0,35 (mer for kategorier med lite n og for tall som er sårbare for uttale), rundet til nærmeste 0,05.

(Syntetiske tall: konfigurasjonen «matchet» i `KLAR-EVAL-0008` v1.0, de to målformene summert; n per kategori er 12 til 40 elementer og dermed små. Tallene er målt etter at telefon-, fødselsnummer- og nøkkelordmønstrene ble rettet på grunnlag av den første syntetiske kjøringen på justeringsmanuset; mønstrene er dermed justert mot `KLAR-MANUS-0001`, ikke mot testmanuset. Terskelene er satt etter rettelsen og før noen menneskeinnlesing og før testdelene.)

### Kontrollsjekker (forventes per konstruksjon)

Disse er **ikke hypoteser** og regnes ikke som bekreftelse eller avkreftelse av noe. Retningen følger av hvordan laget og målingen er laget; en sjekk som ikke går som forventet er et tegn på at noe er galt med kjøringen, og rapporteres som det. Tallene i parentes er DEV.

| id | kontrollsjekk | DEV | kriterium |
|---|---|---|---|
| K1 | rålaget har lavere WER enn det normaliserte laget (matchet; var H1c) | 0,135 mot 0,348 | WER(rå) < WER(normalisert); parret clusterbootstrap-intervall for differansen rapporteres |
| K2 | rålaget alene har lavere overlevelse enn det normaliserte laget, for både person og sted (samlet; var H2g) | 0,740 mot 0,880 (person), 0,549 mot 0,902 (sted) | punktestimat rå < normalisert for begge |
| K3 | recall faller minst 0,15 på små bokstaver uten tegnsetting (som rålaget) sammenlignet med original tekst, i alle fire NorNE-gruppene (var H3e) | 0,28 / 0,23 / 0,36 / 0,48 | differanse ≥ 0,15 i alle fire |

### Foreknowledge of data or evidence

Valideringsdelene (NB Samtale validation, NorNE validation, NPSC validation) er brukt i DEV og er kjent. **Testdelene er ikke åpnet:** ingen testfil er lastet ned eller lest (NB Samtale `test_*`, NorNE `test`, NPSC `data/test/`), og koden sperrer dem (se «Annen informasjon»). Det finnes ingen menneskeinnlesing av testmanuset ennå; den gjøres før testdelene kjøres, og testmanuset er ikke kjørt gjennom rørledningen. Forbehold som gjør tallene optimistiske: NB-Whisper-kortet oppgir stortingstaler fra Språkbanken som treningsdata (NPSC), NB-BERT-base-ner er finjustert på NorNE, og spaCy-modellens treningsdata er ikke kontrollert. De offentlige datasettene er skrevet tekst og parlamentstale, ikke lokalradio.

### Explanation of foreknowledge and managing unintended influences

Terskler og analyseplan er skrevet før testdelene er åpnet, og koden er fryst ved innsending (git-tag `prereg-v1` på den committen Eirik velger; ingen endring i rørledning, motor, ordlister, terskel eller vendor-kode etter taggen uten avviksføring). Ordlistene (`vokabular/sensitivt_*.txt`) og mønstrene er laget uten å se testdata og justert mot justeringsmanuset (`KLAR-MANUS-0001`), ikke mot testmanuset (`KLAR-MANUS-0002`). Testmanuset er skrevet av samme forfatter som ordlistene; ordlistene ble ikke åpnet under skrivingen, men forfatteren kjenner dem, og det kan gjøre testmanuset mer velvillig enn et manus skrevet av en annen. Kjøringene gjøres én gang per datasett.

## Research Design

### Study type

Observasjonell evaluering av en eksisterende rørledning på sekundære, offentlige datasett (CC0 for NB Samtale og NPSC; NorNE med NDT-lisensen, annotasjonene CC0), pluss menneskeinnlesing av et fast manus. Ingen deltakere utover innleseren(e) av manuset; ingen personopplysninger om dem lagres utover region og skriftform.

### Intention for causal interpretation

Ingen. Målingene er beskrivende; terskelsammenligningene er ikke årsaksutsagn.

### Blinding of experimental treatments

Ikke aktuelt (ingen behandlingsgrupper). Terskler og kode er låst før testdelene er åpnet; det er den eneste «blindingen».

### Additional blinding during research or analysis

Testdelene er sperret i koden (`arkivklarering/evaldata.py`): de kan ikke lastes uten `--prereg-id KLAR-PREREG-0001` **og** en `docs/KLAR-PREREG-0001_*.md` med statuslinjen `Status: registrert <OSF-URL>`. Analysen kjøres av skript som er skrevet og testet på valideringsdelene.

### Study design

Fire parallelle målinger (H1 til H4), hver mot sin egen datakilde, med samme rørledning som i DEV (segmentering med inaVAMOS, rålag `nb-whisper-large-verbatim` (kjørt med `-nt`, KLAR-ADR-0017) og normalisert lag `nb-whisper-large` (uten `-nt`), begge med DTW-ordtidsstempler, personvernflagg på begge lag og union paret på ordspenn; KLAR-ADR-0004, -0005 og -0012). Modellfilene er låst av sha256 i `modeller.lock.json` (`0227866e…` og `0f2f66f2…`).

### Randomization

Fast seed 20261026 for alle utvalg. Ingen tilfeldig tildeling.

## Sampling

### Data collection procedures

- **H1, NB Samtale test:** `Sprakbanken/nb_samtale`, del `test`, samme filter som DEV (ingen overlapp mot forrige/neste segment, 2–12 s, minst tre ord i `orthographic`). Utvalg: opptil 60 segmenter per dialektområde (e, n, sw, t, w), trukket med seed 20261026; har et område færre kvalifiserte segmenter, tas alle. Antall per område rapporteres.
- **H2, NPSC test:** `NbAiLab/NPSC`, del `test` (`data/test/`, 16 kHz mp3), referanse `normsentence_text`, målform fra `sentence_language_code`, segmenter på 1,5–25 s. Samme utvalgsprosedyre som i DEV (seed, vektet rundtur to bokmål : ett nynorsk) men **doble mål**: minste prefiks i seed-rekkefølgen som gir minst **300 personflagg og 200 stedsflagg** i referansen, eller 4 timer lyd. Prefikslengden regnes ut med personvernmotoren på referansetranskripsjonene før noe Whisper-resultat leses.
- **H3, NorNE test:** `NbAiLab/norne`, configene `bokmaal` og `nynorsk`, del `test`, **hele delen**.
- **H4, manus:** `KLAR-MANUS-0002` (156 setninger, sha256 over). Innlesing med norsk-tales rigg (`scripts/rigg_manus.py`) av Eirik og eventuelt andre lesere, med region og skriftform registrert per runde. Alle innleste opptak teller. Innlesingen gjøres og scores før noen testdel kjøres.

### Sample size

H1: opptil 300 segmenter. H2: ikke kjent før prefikset er regnet ut; minst 300 person- og 200 stedsreferanseflagg eller 4 timer lyd. H3: hele NorNE test (antall setninger er ikke kjent for oss, siden delen ikke er åpnet). H4: 156 setninger per leser.

### Sample size rationale

DEV-utvalgene var små (NB Samtale 60 segmenter; NPSC 150 og 102 flagg; nynorsk sted bare 22). Utvalgene er derfor økt der kostnaden tillater det, og terskler for grupper med DEV-n under 30 er gjort utforskende i stedet for bekreftende (H2f). Det er ikke gjort noen formell styrkeberegning.

### Starting and stopping rules

Ingen datadrevet stopp. Utvalgene er faste (seed og filter over), og rørledningen kjøres én gang per datasett. For NPSC (H2) er stoppregelen «minste prefiks med minst 300 personflagg og 200 stedsflagg i referansen, eller 4 timer lyd», regnet på referansen alene og logget før rørledningsresultater leses. Whisper-kjøringen avbrytes bare av ressursvakten (KLAR-ADR-0015: minst 8 GiB ledig intern disk, høyst 6,5 GB swap) og tas opp igjen; krasjer whisper-cli, kjøres den krasjende filen uten DTW, og ingen fil droppes. Rørledningen endres ikke underveis.

## Variables

### Manipulated variables

Ingen. Oppsettene som sammenlignes er: lag (rålag, normalisert lag, union) og språkvalg (etter skriftform, primært, mot `-l nn` for alle, sekundært) i H1; lag og union i H2; original mot små bokstaver uten tegnsetting i H3.

### Measured variables

- H1: korpus-WER (jiwer, vendor `norm.normaliser` fra norsk-tale, KLAR-ADR-0014) per lag, språkoppsett og dialektområde.
- H2: overlevelse (a) og streng overlevelse (delt ord eller inneholdt utdrag) per kategori, målform og lag; andel «ekstra» rørledningsflagg uten referanseflagg i samme kategori i samme segment.
- H3: recall og presisjon (overlapp og nøyaktig span) for PER og LOC + GPE_LOC per målform, i tekstformene original og små bokstaver uten tegnsetting, for hele motoren og for hver gjenkjenner.
- H4: `tekst_treff` (elementet står i transkripsjonen) og `flagg_treff` (et flagg i samme kategori dekker elementet) per målelement, kategori, lag, målform og dialektfelt; målformfeil separat (vendor `score.py`).

### Indices

Ingen sammensatte indekser. Samlede tall (begge målformer) er summer av tellerne, ikke gjennomsnitt av rater.

## Analysis Plan

### Statistical models

Beskrivende. Proporsjoner med Wilson-95 %-intervall (H2, H3, H4); korpus-WER med **clusterbootstrap** over taler (NB Samtale `speaker_id`; NPSC `speaker_id`), 2000 gjentak, seed 20261026; differansen i K1 med parret clusterbootstrap. NorNE: bootstrap over setninger. Analysen kjøres med `eval/dev/`-skriptene (`kjor_dev.py`, `kjor_personvern_dev.py`, `kjor_flaggoverlevelse_ord.py`, `kjor_syntetisk.py`) med `--splitt test --prereg-id KLAR-PREREG-0001`; skriptene er ikke endret etter at testdelene ble sperret opp. H4 på menneskelyd scores med `kalibrering.score_flagg` mot `KLAR-MANUS-0002`; skriptet som kjører opptakene gjennom rørledningen skrives og testes på justeringsmanuset (TTS) og fryses før denne preregistreringen sendes inn (ikke gjort per v1.1; det føres i `KLAR-LOG-0001` når det er gjort).

### Transformations

Små bokstaver og fjerning av tegnsetting for WER (vendor `norm.normaliser`). Tallord normaliseres til sifre i H4 (vendor `score.py`). Ingen andre transformasjoner.

### Inference criteria

Hver hypotese i H1–H4 vurderes for seg mot sin terskel (punktestimat), uten justering for flere sammenligninger: tersklene er beskrivende, ikke signifikanstester. «Klart bekreftet» krever at også 95 %-intervallgrensen på riktig side av terskelen. Kontrollsjekkene K1–K3 er ingen hypoteser: de rapporteres med tall og om kriteriet er oppfylt, og for K1 også om det parrede intervallet utelukker 0.

### Data inclusion and exclusion

Inklusjon etter filtrene i «Data collection procedures». Ekskluderes: segmenter uten referansetekst. Segmenter der Whisper gir tomt resultat beholdes (null flagg, alle ord er sletting i WER). Segmenter som måtte kjøres uten DTW beholdes, flagges i rapporten, og unionen faller tilbake til cuenes tidsrom for dem. Ingen utelatelse etter å ha sett utfall.

### Missing data

Krasjer whisper-cli også uten DTW, får segmentet tomt resultat (`feil`), regnes som tomt Whisper-resultat og rapporteres med antall. Manglende opptak i manuset (H4) regnes ikke med i nevneren for den leseren; antall rapporteres.

### Other planned analysis (utforskende)

Per dialektområde (H1), per lag og målform for H2 (rålag og normalisert lag hver for seg), per målform og kilde-gjenkjenner (H3), nynorsk sted (H2f, n er for lite til bekreftelse), andel ekstra flagg, målformfeil per lag, og den kategorivise sammenhengen mellom `tekst_treff` og `flagg_treff` (H4). Organisasjon og kategoriene uten bekreftende terskel i NPSC (helse, økonomi, konflikt, religion, politikk, dato, fødselsår, telefon, fødselsnummer, e-post) måles ikke på NPSC; de måles bare i H4 (sekundært). Utforskende funn merkes slik og regnes ikke som bekreftelse.

## Other

### Context and additional information

- **Negative resultater** rapporteres på lik linje med positive: alle H1–H4 rapporteres i et eget `KLAR-EVAL`-dokument med tall, intervall og om terskelen er oppfylt, uavhengig av utfall, og README oppdateres. Brutte terskler forklares ikke bort; en eventuell forklaring merkes utforskende. Rettelser og negative resultater publiseres (jf. prinsippene i `KLAR-REG-0001`).
- **Kjent begrensning ved rålaget, rettet med `-nt` (KLAR-EVAL-0011, KLAR-ADR-0017):** `nb-whisper-large-verbatim` avsluttet noen ganger et dekodingsvindu med `[_EOT_]` uten avsluttende tidsstempeltoken, og whisper.cpp kastet da teksten etter det første tidsstempeltokenet (kilde: `src/whisper.cpp`, `result_len = i + 1` bare ved tidsstempeltoken). I DEV ga det tomt eller under halvparten av referanseordene for 6 av 60 NB Samtale-segmenter (10 %). Rålaget kjøres nå med `-nt`; med `-nt` er antall tomme rålag-hypoteser i DEV 0 av 60 (før: 2 for «matchet» og 6 for `-l nn`). Det normaliserte laget kjøres uten `-nt` (samme feil i mindre grad; unionen i H2 og H4 kompenserer delvis). Ordtidene for rålaget kommer fortsatt fra DTW. Konsekvensen for tersklene er beskrevet under H1 («Avvik»).
- **Avviksføring:** alle avvik fra denne planen (endret kode etter taggen, endret utvalg, avbrutt kjøring, endret terskel) føres i `KLAR-LOG-0001` med årsak før resultatet av avviket brukes. Terskler endres ikke etter at testdelene er åpnet; et behov for det registreres som en ny preregistrering (`KLAR-PREREG-<neste>`).
- **Sperre i koden:** `arkivklarering/evaldata.py` avviser `--splitt test` uten `--prereg-id KLAR-PREREG-<NNNN>`, uten en `docs/KLAR-PREREG-<NNNN>_*.md`, og uten statuslinjen `Status: registrert <OSF-URL>` i fila. Sperren åpnes bare med denne ID-en, og først når denne fila er registrert. Den er enhetstestet (`tests/test_evaldata.py`).
- **Datakilder og lisenser:** `KLAR-EVAL-0004` (NB Samtale, CC0), `KLAR-EVAL-0005` (NorNE), `KLAR-EVAL-0007` (NPSC, CC0). Lyd fra museet går aldri inn i git, sky eller GitHub (`docs/gt_fast.md`); ingenting fra museet inngår i denne preregistreringen.
- **Museumspiloten** forutsetter ja fra museet; den får en egen preregistrering, `KLAR-PREREG-0002` (reservert), som lages først etter det og før pilotdata kjøres.
- **Referanser:** `KLAR-ARK-0001` (kilder), `KLAR-ADR-0004`, `-0005`, `-0012`, `-0014`, `-0015`; kode og tidsstempler: GitHub (privat) `avalyset/arkivklarering`, `docs/stempler/`.

## Avvik etter registrering

Tabellen under er bare en oppsummering, med én rad per avvik. Den fullstendige føringen er `KLAR-LOG-0003` (avvikstabellen, v1.17) og punktene 1–25 under.

| AV-ID | kort innhold | endrer hypotese | endrer primærutfall | endrer terskel | endrer utvalg | endrer analysemetode | endrer datasett | PREREG-punkt |
|---|---|---|---|---|---|---|---|---|
| AV-01 | Rålaget ga tomt eller avkortet utdata på 6 av 60 DEV-segmenter; ført som kjent begrensning | nei | nei | nei | nei | nei | nei | – |
| AV-02 | Rålaget kjøres med `-nt`; DEV målt på nytt; terskel H1a ≤ 0,25 og H1d ≤ 0,35 | nei | nei | ja | nei | ja | nei | – |
| AV-03 | Analysekoden tagget på nytt: `h4-script-v2` erstatter `h4-script-v1`, som er beholdt | nei | nei | nei | nei | nei | nei | – |
| AV-04 | `KLAR-MANUS-0002` rettet til v1.2 (ett ord fantes ikke i Nynorskordboka); ny sha256 | nei | nei | nei | nei | nei | ja | – |
| AV-05 | PREREG v1.8 (i git-historikken): bare tekstrettelser; ingen tall endret | nei | nei | nei | nei | nei | nei | – |
| AV-06 | OSF fjerner tekst i vinkelparenteser; skjemafeltene avviker i ordlyd, opplastet PREREG-fil har originalen | nei | nei | nei | nei | nei | nei | – |
| AV-07 | Foreknowledge på OSF satt feil; testdelene var ikke lastet inn eller observert | nei | nei | nei | nei | nei | nei | 1 |
| AV-08 | Tre sperretester og filvalg rettet: versjonssortering i stedet for leksikografisk sortering | nei | nei | nei | nei | nei | nei | 2 |
| AV-09 | `scripts/kjor_testdel.sh` starter testdelene utenfra og skriver kjøringsmetadata etter hver del | nei | nei | nei | nei | nei | nei | 3 |
| AV-10 | `kjor_dev.py` fikk `--per-dialekt` og `min(N, len(pool))`; H1 kjøres med 60 per dialektområde | nei | nei | nei | ja | nei | nei | 4, 11 |
| AV-11 | H1–H3-skriptene fikk `--ut-mappe`, `--etikett` og `--eval-nr`; testresultater får egne EVAL-numre | nei | nei | nei | nei | nei | nei | 5 |
| AV-12 | Bevis for uendret utregning: `scripts/verifiser_uendret.py` sammenligner DEV-skriptene eksakt med lagrede resultater | nei | nei | nei | nei | nei | nei | 6 |
| AV-13 | 95 %-intervallmetoden låst: persentilintervall; intervalltypen var ikke spesifisert | nei | nei | nei | nei | ja | nei | 7, 11 |
| AV-14 | H4-begrensning: bare én leser, som er forfatter og kjenner målelementene | nei | nei | nei | ja | nei | nei | 8 |
| AV-15 | `kjor_personvern_dev.py` skriver tellere per setning; bootstrap over setninger for NorNE | nei | nei | nei | nei | ja | nei | 9 |
| AV-16 | `kjor_testdel.sh` nekter å starte en testdel hvis koden er endret siden `testkjoring-v1` | nei | nei | nei | nei | nei | nei | 10 |
| AV-17 | Innspillingsprotokoll for H4 spesifisert før datainnsamling (`KLAR-ADR-0018`; ikke i PREREG) | nei | nei | nei | nei | nei | nei | 12 |
| AV-18 | Ny kodetagg `testkjoring-v2`; `kjor_testdel.sh` kontrollerer den; `testkjoring-v1` beholdt | nei | nei | nei | nei | nei | nei | 13 |
| AV-19 | Lukket av AV-27 (H4 gjennomføres ikke i v1.0): H4 ble ikke gjennomført; innlesingen 27.10 ble ikke lagret; rettet i grenen h4-fiks | nei | nei | nei | nei | nei | nei | – |
| AV-20 | Testdelene H1–H3 kjøres før H4-innlesingen, motsatt av rekkefølgen i PREREG | nei | nei | nei | nei | nei | nei | 14 |
| AV-21 | Speil ikke kjørt etter hver testdel; speil, GT og stempling én gang etter H1–H3 | nei | nei | nei | nei | nei | nei | – |
| AV-22 | H4-innleseren endret etter registrering og før datainnsamling (tag `h4-rigg-v3`) | nei | nei | nei | nei | nei | nei | 15 |
| AV-23 | sha256 for testdataene (13 filer) ført etter H1-start; identiteten fastlagt mot offentlige HF-revisjoner | nei | nei | nei | nei | nei | nei | 16 |
| AV-24 | Wilson er primær for H3; bootstrap over setninger rapporteres som sensitivitetsanalyse | nei | nei | nei | nei | ja | nei | 17 |
| AV-25 | inaVAMOS brukes ikke lenger; H4 kjøres med inaSpeechSegmenter (H4 utgår i v1.0, AV-27); H1 og H2 står som preregistrert | nei | nei | nei | nei | ja | nei | 18 |
| AV-26 | inaSpeechSegmenter er standard segmentering i koden; inaVAMOS er valgfritt tillegg `reproduksjon-h1h2`; ny kodetagg `testkjoring-v5` | nei | nei | nei | nei | nei | nei | 19 |
| AV-27 | H4 gjennomføres ikke i v1.0 (Eiriks beslutning 2026-10-27, før noen H4-data er samlet inn); ekstern test på NB Tale modul 3 i v1.1 (KLAR-PREREG-0003) | ja | nei | nei | nei | nei | ja | 20 |
| AV-28 | Kodeendringer etter `testkjoring-v5`: cache-stier per segmentering, datarot `ARKIVKLARERING_DATA`, tester i rent miljø; ny kodetagg `testkjoring-v6`; ingen utregning for H1–H3 endret | nei | nei | nei | nei | nei | nei | 21 |
| AV-29 | Telefonnumrene i KLAR-MANUS-0002 (v1.2 → v1.3) og KLAR-MANUS-0001 (v1.1 → v1.2) byttet til Nkoms fiktivserie 68 05 00 00–68 05 99 99 før publisering; setningene ellers uendret | nei | nei | nei | nei | nei | ja | 22 |
| AV-30 | Kodetaggene `testkjoring-v7` (versjon 1.0.0, fiktive telefonnumre i testdata, kodesjekk) og `testkjoring-v8` (VTT-merknaden om musikk under tale rettet etter ADR-0019) etter `testkjoring-v6`; ingen utregning for H1–H3 endret | nei | nei | nei | nei | nei | nei | 23 |
| AV-31 | Regelen for H4-tersklene i den registrerte teksten («det syntetiske tallet minus 0,15 til 0,35», v1.8 linje 76) stemmer ikke med tabellen for person (0,69 → 0,60, −0,09) og sted (0,82 → 0,70, −0,12); den registrerte teksten og tersklene er ikke endret; ingen følger fordi H4 utgår (AV-27) | nei | nei | nei | nei | nei | nei | 24 |
| AV-32 | Kodetaggen `testkjoring-v9` etter `testkjoring-v8`: hjelpeteksten til `--ingen-ordtider` i `arkivklarering/cli.py`, kodetaggen i `scripts/kjor_testdel.sh` og testen, og at GT-generatoren (`scripts/ground_truth.py`) ikke lister forrige GT-versjon (med ny test); ingen analysekode og ingen utregning for H1–H3 endret | nei | nei | nei | nei | nei | nei | 25 |
| AV-33 | Kodetaggen `testkjoring-v10` etter `testkjoring-v9`: ny mekanisk pekersjekk (`scripts/sjekk_pekere.py`) med test, og kodesjekken i `scripts/kjor_testdel.sh` og testen; ingen analysekode og ingen utregning for H1–H3 endret | nei | nei | nei | nei | nei | nei | 26 |
| AV-34 | A3 endret: offentlig repo fra rent tre (én commit), full git-historikk i tilgangsstyrt deponering; ingen kode, data eller utregning endret | nei | nei | nei | nei | nei | nei | 27 |

Usikre celler: AV-02 analysemetode (`-nt` endrer hvordan rålaget lages, ikke WER-beregningen); AV-04 datasett (manuset er H4-materialet, rettet før registrering og før noe opptak); AV-10 utvalg (koden gir nå utvalget PREREG beskriver, men trekket er endret fra fast 12 per område); AV-14 utvalg (PREREG nevner «Eirik og eventuelt andre lesere», H4 måles med én leser); AV-15 analysemetode (bootstrap over setninger for NorNE regnes nå, aggregatene er uendret); AV-25 analysemetode (segmenteren i rørledningen er byttet for H4, analysen og tersklene er uendret); AV-27 hypotese (ordlyden i H4 er uendret, men den sekundære hypotesen H4 prøves ikke i v1.0; primærutfallene H1 og H2 er ikke berørt) og datasett (H4-opptakene av `KLAR-MANUS-0002` samles ikke inn; datasettene for H1–H3 er uendret; utvalget i H1–H3 er uendret, derfor «nei» for utvalg); AV-28 analysemetode (cache-filnavnet velges nå etter segmenteringen, men med `inavamos`, som H1 og H2 kjøres med, leses samme cache som i testkjøringen, og ingen utregning er endret, derfor «nei»); AV-29 datasett (testmanuset `KLAR-MANUS-0002` er endret, bare i telefonnumrene; H4 gjennomføres ikke i v1.0 (AV-27), så ingen kjørt test bruker det; datasettene for H1–H3 er uendret); AV-30 analysemetode («nei» fordi det som brukes i analysen, ikke er endret mellom `testkjoring-v6` og `testkjoring-v8`: ingen fil under `eval/`, ikke `scripts/rapporter_intervaller.py`, og ingen av funksjonene for WER (`arkivklarering/_vendor/norsk_tale`, `eval/dev`), flaggscoring (`arkivklarering/personvern.py`: bare en docstring er endret) og Wilson; det som er endret, står i punkt 23); AV-31 terskel (regelen i den registrerte teksten og tabellen er uenige for person og sted, men tersklene i tabellen er de registrerte og er ikke endret, derfor «nei»; H4 prøves ikke, AV-27).

Ført 2026-10-27, etter registreringen på OSF (https://osf.io/hc83q/; registrert innhold = v1.8). Ingen terskel, ingen tekst i planen og ingen hash er endret; avvikene er også ført fortløpende i `KLAR-LOG-0001` (fra v1.26; nyeste v1.48) og i `KLAR-LOG-0003` (avvikstabellen).

1. **Foreknowledge på OSF ble satt til ‹Authors have observed the data, but have not performed the proposed analyses›. Det riktige er: testdelene (NB Samtale, NorNE, NPSC test) er ikke lastet inn eller observert (sperret i koden). Testmanuset er skrevet av forfatterne, men ingen opptak finnes. DEV-dataene (validation) er observert.** Valget på OSF er ikke endret.
2. **Kode og tester, endret etter taggene `prereg-v1` og `h4-script-v2`:** (a) versjonssortering i stedet for leksikografisk sortering ved valg av PREREG- og MANUS-fil (`v1.10` er nyere enn `v1.9`): `arkivklarering/evaldata.py` (nye `versjonsnokkel` og `siste_versjon`; `sjekk_splitt` bruker dem), `kalibrering/kjor_h4.py`, `eval/dev/kjor_syntetisk.py`, `scripts/ordbokkontroll.py`, `scripts/navnesjekk.py`, `scripts/rigg_manus.py`; (b) `evaldata.sjekk_splitt` leser `DOCS` ved kall (`docs=None`), slik at tester kan peke den til en egen mappe; (c) de tre sperretestene (`tests/test_evaldata.py::test_utkast_apner_ikke_testdelen`, `tests/test_kjor_h4.py::test_testmanus_kan_ikke_scores_for_preregistreringen_er_registrert`, `tests/test_manus.py::test_testmanuset_er_sperret_for_roerledningen_foer_registrering`) bruker nå et utkast i en egen mappe i stedet for repoets ekte PREREG-fil (som er registrert), og `tests/test_manus.py` og `tests/test_kjor_h4.py` velger PREREG-fila med versjonssortering; ny test `tests/test_evaldata.py::test_versjonssortering_ikke_leksikografisk`. Alle 123 tester er grønne. Endringen påvirker ingen målte tall (bare filvalg og testoppsett); sperren virker som før. Ingen ny tag er laget: `h4-script-v2` peker fortsatt på koden som ga DEV-tallene.
3. **Kjøring av testdelene utenfra (ny fil, ingen analysekode endret):** `scripts/kjor_testdel.sh` starter én testdel om gangen (H1, H2, H3, H4 eller `alle` i den rekkefølgen) med de eksisterende skriptene, og etter HVER del skriver den en egen fil ved siden av resultatet (`<resultat>_kjoring_meta.json`: commit-SHA ved start, `git status --porcelain` ved start, kommando, tider, returkode, resultatfiler, SHA-ene til taggene `prereg-v1` og `h4-script-v2` og sha256 for PREREG- og MANUS-fila), committer resultat og metafil, pusher (privat) og kjører `scripts/speil.sh` før neste del starter. Er arbeidstreet ikke helt rent ved start av en del (også usporede filer), kjøres ingenting. Skriptet stopper uten å committe hvis en kjøring har endret en sporet fil, og stopper etter en feilet del (som committes med returkoden). EVAL-dokumentene siterer metadatafila. Testet i `tests/test_kjor_testdel.py` (stubber i et midlertidig repo med lokalt origin; ingen testdel er kjørt), blant annet to og fire kjøringer etter hverandre. Parametrene for H2 er de forhåndsregistrerte (`--mal-person 300 --mal-sted 200 --maks-timer 4`). `kjor_h4.py`, `evaldata.py` og annen analysekode er ikke endret for dette. Planen er ellers uendret.

   Diff (ordrett) mot commit `13124a2` (`git diff 13124a2 -- scripts/kjor_testdel.sh tests/test_kjor_testdel.py`):

```diff
diff --git a/scripts/kjor_testdel.sh b/scripts/kjor_testdel.sh
index f763123..2ad2d3a 100755
--- a/scripts/kjor_testdel.sh
+++ b/scripts/kjor_testdel.sh
@@ -1,57 +1,112 @@
 #!/bin/bash
 #
-# kjor_testdel.sh: starter en kjøring av kalibrering/kjor_h4.py (typisk H4 på testmanuset) utenfra og skriver kjøringens identitet til
-# en egen fil ved siden av resultatet: <resultat>_kjoring_meta.json (commit-SHA, `git status --porcelain` ved start, kommando, tider,
-# returkode, SHA-er for taggene og sha256 for PREREG- og MANUS-fila). EVAL-dokumentet siterer den fila. Analysekoden er uendret.
+# kjor_testdel.sh: kjører testdelene (H1–H4) én og én utenfra, og etter HVER del committer den resultat og kjøringsmetadata, pusher (privat)
+# og kjører scripts/speil.sh før neste del starter. Analysekoden er uendret; skriptet bare starter den.
 #
-#   source scripts/miljo.sh && scripts/kjor_testdel.sh [--tor] --prereg-id KLAR-PREREG-0001 [flere argumenter til kjor_h4.py]
+#   source scripts/miljo.sh && scripts/kjor_testdel.sh [--tor] <H1|H2|H3|H4|alle> --prereg-id KLAR-PREREG-0001 [-- ekstra argumenter]
 #
-# Arbeidstreet må være helt rent ved start (`git status --porcelain` tom, også uten usporede filer), ellers kjøres ingenting (exit 1).
-# --tor skriver hva som ville blitt kjørt og avslutter; ingenting kjøres og ingen fil skrives.
+#   H1  eval/dev/kjor_dev.py --splitt test                                              (NB Samtale test)
+#   H2  eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --mal-person 300 --mal-sted 200 --maks-timer 4   (PREREG: doble mål)
+#   H3  eval/dev/kjor_personvern_dev.py --splitt test                                   (NorNE test)
+#   H4  kalibrering/kjor_h4.py                                                          (menneskeinnlest testmanus)
+#   alle = H1, H2, H3, H4 i den rekkefølgen (H4 til sist: opptakene må være innlest og scoret først, se PREREG).
+#
+# Før hver del: `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1). Etter hver del skrives
+# <resultat>_kjoring_meta.json (commit-SHA ved start, tom porcelain, kommando, tider, returkode, resultatfiler, SHA-ene til taggene og sha256 for PREREG-
+# og MANUS-fila). Så: commit av resultat og metafil, push, speil. Stopper hele kjøringen (ingen neste del) hvis en del feiler, hvis en SPORET fil er
+# endret av kjøringen (da committes ingenting, exit 4; fjerner ikke noe), eller hvis commit, push eller speil feiler. Feilede deler committes (med
+# returkoden i metafila) og stopper deretter. --tor skriver bare hva som ville blitt kjørt.
 set -euo pipefail
 
 REPO="$(cd "$(dirname "$0")/.." && pwd)"
 cd "$REPO"
 PY="${KLAR_PY:-.venv/bin/python}"
-TOR=0; ARGV=()
-for a in "$@"; do if [ "$a" = "--tor" ]; then TOR=1; else ARGV+=("$a"); fi; done
+SPEIL="${KLAR_SPEIL:-scripts/speil.sh}"
+REMOTE="${KLAR_REMOTE:-origin}"
+TOR=0; DEL=""; ID=""; EKSTRA=()
+while [ $# -gt 0 ]; do
+  case "$1" in
+    --tor) TOR=1 ;;
+    --prereg-id) ID="${2:?mangler verdi til --prereg-id}"; shift ;;
+    --) shift; EKSTRA=("$@"); break ;;
+    H1|H2|H3|H4|alle) DEL="$1" ;;
+    *) echo "ukjent argument: $1" >&2; exit 2 ;;
+  esac
+  shift
+done
+[ -n "$DEL" ] && [ -n "$ID" ] || { echo "bruk: kjor_testdel.sh [--tor] <H1|H2|H3|H4|alle> --prereg-id KLAR-PREREG-<NNNN> [-- ekstra]" >&2; exit 2; }
+if [ "$DEL" = alle ]; then DELER=(H1 H2 H3 H4); else DELER=("$DEL"); fi
 
-PORC="$(git status --porcelain)"
-if [ -n "$PORC" ]; then
-  echo "FEIL: arbeidstreet er ikke rent; kjører ikke. git status --porcelain:" >&2
-  echo "$PORC" >&2
-  exit 1
-fi
-SHA="$(git rev-parse HEAD)"
-KMD="$PY kalibrering/kjor_h4.py ${ARGV[*]:-}"
-if [ "$TOR" -eq 1 ]; then echo "(--tor) ville kjørt på $SHA: $KMD"; exit 0; fi
+kommando() {  # skriver skriptet og argumentene for en del, ett ord per linje
+  case "$1" in
+    H1) printf '%s\n' eval/dev/kjor_dev.py --splitt test --prereg-id "$ID" ;;
+    H2) printf '%s\n' eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --prereg-id "$ID" --mal-person 300 --mal-sted 200 --maks-timer 4 ;;
+    H3) printf '%s\n' eval/dev/kjor_personvern_dev.py --splitt test --prereg-id "$ID" ;;
+    H4) printf '%s\n' kalibrering/kjor_h4.py --prereg-id "$ID" ;;
+  esac
+}
 
-PRE="$(ls docs/KLAR-PREREG-0001_*.md | sort -V | tail -1)"
-MAN="$(ls kalibrering/KLAR-MANUS-0002_*.tsv | sort -V | tail -1)"
-TID="$(date +%Y%m%d-%H%M%S)"
-START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
-FOR="$(ls docs/KLAR-EVAL-0009_*.json eval/dev/h4_*.json 2>/dev/null | sort || true)"
+rent_eller_stopp() {
+  local p; p="$(git status --porcelain)"
+  if [ -n "$p" ]; then
+    echo "FEIL: arbeidstreet er ikke rent; kjører ikke. git status --porcelain:" >&2
+    echo "$p" >&2
+    exit 1
+  fi
+}
+
+rent_eller_stopp
+if [ "$TOR" -eq 1 ]; then
+  for d in "${DELER[@]}"; do
+    K=(); while IFS= read -r l; do K+=("$l"); done < <(kommando "$d")
+    echo "(--tor) $d ville kjørt på $(git rev-parse HEAD): $PY ${K[*]} ${EKSTRA[*]:-}"
+  done
+  exit 0
+fi
 
-set +e
-"$PY" kalibrering/kjor_h4.py "${ARGV[@]+"${ARGV[@]}"}"
-RC=$?
-set -e
+for d in "${DELER[@]}"; do
+  rent_eller_stopp   # etter forrige dels commit skal treet være rent igjen
+  K=(); while IFS= read -r l; do K+=("$l"); done < <(kommando "$d")
+  SHA="$(git rev-parse HEAD)"
+  KMD="$PY ${K[*]} ${EKSTRA[*]:-}"
+  PRE="$(ls docs/${ID}_*.md | sort -V | tail -1)"
+  MAN="$(ls kalibrering/KLAR-MANUS-0002_*.tsv | sort -V | tail -1)"
+  TID="$(date +%Y%m%d-%H%M%S)"
+  START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
+  echo "== $d ($KMD) på $SHA"
+  set +e
+  "$PY" "${K[@]}" "${EKSTRA[@]+"${EKSTRA[@]}"}"
+  RC=$?
+  set -e
+  SLUTT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
 
-SLUTT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
-ETTER="$(ls docs/KLAR-EVAL-0009_*.json eval/dev/h4_*.json 2>/dev/null | sort || true)"
-NY="$(comm -13 <(echo "$FOR") <(echo "$ETTER") | tail -1 || true)"
-if [ -n "$NY" ]; then META="${NY%.json}_kjoring_meta.json"; else META="docs/kjoring_meta_$TID.json"; fi
-export META SHA START SLUTT RC KMD PRE MAN NY
-export TAG_PREREG="$(git rev-parse -q --verify 'refs/tags/prereg-v1^{commit}' || echo mangler)"
-export TAG_H4="$(git rev-parse -q --verify 'refs/tags/h4-script-v2^{commit}' || echo mangler)"
-export SHA_PRE="$(shasum -a 256 "$PRE" | cut -d' ' -f1)" SHA_MAN="$(shasum -a 256 "$MAN" | cut -d' ' -f1)"
-"$PY" - <<'PYEOF'
+  ENDRET="$(git status --porcelain --untracked-files=no)"
+  if [ -n "$ENDRET" ]; then
+    echo "STOPP: kjøringen endret sporede filer; ingenting committet, ingen neste del. Sjekk med git diff (ingenting er fjernet eller tilbakestilt):" >&2
+    echo "$ENDRET" >&2
+    exit 4
+  fi
+  NYE="$(git status --porcelain --untracked-files=all | sed 's/^?? //' | sort)"
+  RES="$(echo "$NYE" | grep -E '^(docs/KLAR-EVAL|eval/dev/KLAR-EVAL).*\.json$' | head -1 || true)"
+  [ -n "$RES" ] || RES="$(echo "$NYE" | grep -E '\.json$' | head -1 || true)"
+  if [ -n "$RES" ]; then META="${RES%.json}_kjoring_meta.json"; else META="docs/kjoring_meta_${d}_$TID.json"; fi
+  export META SHA START SLUTT RC KMD PRE MAN RES DEL_NAVN="$d" NYE
+  export TAG_PREREG="$(git rev-parse -q --verify 'refs/tags/prereg-v1^{commit}' || echo mangler)"
+  export TAG_H4="$(git rev-parse -q --verify 'refs/tags/h4-script-v2^{commit}' || echo mangler)"
+  export SHA_PRE="$(shasum -a 256 "$PRE" | cut -d' ' -f1)" SHA_MAN="$(shasum -a 256 "$MAN" | cut -d' ' -f1)"
+  "$PY" - <<'PYEOF'
 import json, os
 e = os.environ
-ut = {"commit": e["SHA"], "git_status_porcelain_ved_start": [], "kommando": e["KMD"], "start_utc": e["START"], "slutt_utc": e["SLUTT"],
-      "returkode": int(e["RC"]), "resultatfil": e["NY"] or None, "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"],
+ut = {"del": e["DEL_NAVN"], "commit": e["SHA"], "git_status_porcelain_ved_start": [], "kommando": e["KMD"], "start_utc": e["START"], "slutt_utc": e["SLUTT"],
+      "returkode": int(e["RC"]), "resultatfil": e["RES"] or None, "nye_filer": [x for x in e["NYE"].split("\n") if x],
+      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"],
       "preregistrering": {"fil": e["PRE"], "sha256": e["SHA_PRE"]}, "manus": {"fil": e["MAN"], "sha256": e["SHA_MAN"]}}
 open(e["META"], "w", encoding="utf-8").write(json.dumps(ut, ensure_ascii=False, indent=2) + "\n")
 print(e["META"])
 PYEOF
-exit "$RC"
+  git add -A
+  git commit -q -m "Testdel $d: resultat og kjøringsmetadata (returkode $RC, start på ${SHA:0:7})"
+  git push -q "$REMOTE" HEAD
+  bash "$SPEIL"
+  if [ "$RC" -ne 0 ]; then echo "STOPP: $d feilet (returkode $RC); resultat og metafil er committet, pushet og speilet. Ingen neste del." >&2; exit "$RC"; fi
+done
diff --git a/tests/test_kjor_testdel.py b/tests/test_kjor_testdel.py
index 975a827..eae3447 100644
--- a/tests/test_kjor_testdel.py
+++ b/tests/test_kjor_testdel.py
@@ -1,80 +1,131 @@
-"""scripts/kjor_testdel.sh: kjører ikke på urent arbeidstre, og skriver kjoring_meta ved siden av resultatet (testdelene kjøres ikke her:
-kalibrering/kjor_h4.py er en stubb i et midlertidig repo)."""
+"""scripts/kjor_testdel.sh: kjører ikke på urent arbeidstre; skriver kjoring_meta ved siden av resultatet; committer, pusher og speiler etter HVER
+testdel før neste starter; stopper på feil og på endrede sporede filer. Testdelene kjøres ikke her: skriptene er stubber i et midlertidig repo
+med et lokalt bart repo som origin og en stubb for speil."""
 import json
+import os
 import pathlib
 import shutil
 import subprocess
 import sys
 
 REPO = pathlib.Path(__file__).resolve().parent.parent
-STUBB = '''import pathlib, sys
-pathlib.Path("kjort.txt").write_text(" ".join(sys.argv[1:]))
-pathlib.Path("docs/KLAR-EVAL-0009_stubb_v1.0_2026-10-27.json").write_text("{}")
-sys.exit(int(__import__("os").environ.get("STUBB_RC", "0")))
+STUBB = '''import os, pathlib, sys
+navn = pathlib.Path(sys.argv[0]).stem
+with open("kjort.log", "a") as f:
+    f.write(navn + " " + " ".join(sys.argv[1:]) + "\\n")
+if os.environ.get("STUBB_OVERSKRIV") == navn:
+    pathlib.Path("docs/sporet.md").write_text("endret av kjøringen")
+pathlib.Path("docs/KLAR-EVAL-" + navn + "_v1.0_2026-10-27.json").write_text("{}")
+sys.exit(3 if os.environ.get("STUBB_FEIL") == navn else 0)
 '''
+SKRIPT = ["eval/dev/kjor_dev.py", "eval/dev/kjor_flaggoverlevelse_ord.py", "eval/dev/kjor_personvern_dev.py", "kalibrering/kjor_h4.py"]
 
 
 def git(r, *a):
-    return subprocess.run(["git", *a], cwd=r, check=True, capture_output=True, text=True).stdout.strip()
+    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=r, check=True, capture_output=True, text=True).stdout.strip()
 
 
 def lag_repo(tmp_path):
     r = tmp_path / "repo"
-    (r / "scripts").mkdir(parents=True)
-    (r / "docs").mkdir()
-    (r / "kalibrering").mkdir()
+    for d in ("scripts", "docs", "kalibrering", "eval/dev"):
+        (r / d).mkdir(parents=True)
     shutil.copy(REPO / "scripts" / "kjor_testdel.sh", r / "scripts")
-    (r / "kalibrering" / "kjor_h4.py").write_text(STUBB)
+    for s in SKRIPT:
+        (r / s).write_text(STUBB)
+    (r / "scripts" / "speil_stubb.sh").write_text('echo "speil $(git rev-parse --short HEAD) $(git status --porcelain | wc -l | tr -d " ")" >> "$(dirname "$0")/../speil.log"\n')
+    (r / ".gitignore").write_text("kjort.log\nspeil.log\n")
     (r / "kalibrering" / "KLAR-MANUS-0002_stubb_v1.2_2026-10-26.tsv").write_text("x\n")
     (r / "docs" / "KLAR-PREREG-0001_stubb_v1.9_2026-10-27.md").write_text("a\n")
     (r / "docs" / "KLAR-PREREG-0001_stubb_v1.10_2026-10-27.md").write_text("b\n")
+    (r / "docs" / "sporet.md").write_text("opprinnelig")
     git(r, "init", "-q", "-b", "main")
-    git(r, "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A")
-    git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "x")
+    git(r, "add", "-A")
+    git(r, "commit", "-q", "-m", "x")
     git(r, "tag", "prereg-v1")
     git(r, "tag", "h4-script-v2")
-    return r
+    bart = tmp_path / "origin.git"
+    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(bart)], check=True)
+    git(r, "remote", "add", "origin", str(bart))
+    return r, bart
 
 
-def kjor(r, *args, rc="0"):
-    import os
+def kjor(r, *args, **env):
     return subprocess.run(["bash", "scripts/kjor_testdel.sh", *args], cwd=r, capture_output=True, text=True,
-                          env={**os.environ, "KLAR_PY": sys.executable, "STUBB_RC": rc})
+                          env={**os.environ, "KLAR_PY": sys.executable, "KLAR_SPEIL": "scripts/speil_stubb.sh", **env})
+
+
+def kjort(r):
+    f = r / "kjort.log"
+    return f.read_text().splitlines() if f.exists() else []
 
 
 def test_urent_arbeidstre_kjorer_ikke(tmp_path):
-    r = lag_repo(tmp_path)
+    r, _ = lag_repo(tmp_path)
     (r / "uspor.txt").write_text("x")
-    p = kjor(r, "--prereg-id", "KLAR-PREREG-0001")
+    p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
     assert p.returncode == 1 and "uspor.txt" in p.stderr
-    assert not (r / "kjort.txt").exists() and not list((r / "docs").glob("*kjoring_meta*"))
+    assert kjort(r) == [] and not list((r / "docs").glob("*kjoring_meta*"))
     (r / "uspor.txt").unlink()
-    (r / "kalibrering" / "KLAR-MANUS-0002_stubb_v1.2_2026-10-26.tsv").write_text("endret\n")  # sporet fil endret
-    assert kjor(r, "--prereg-id", "KLAR-PREREG-0001").returncode == 1 and not (r / "kjort.txt").exists()
+    (r / "docs" / "sporet.md").write_text("endret")  # sporet fil endret
+    assert kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001").returncode == 1 and kjort(r) == []
 
 
 def test_tor_kjorer_ikke_og_skriver_ingenting(tmp_path):
-    r = lag_repo(tmp_path)
-    p = kjor(r, "--tor", "--prereg-id", "KLAR-PREREG-0001")
-    assert p.returncode == 0 and "ville kjørt" in p.stdout
-    assert not (r / "kjort.txt").exists() and git(r, "status", "--porcelain") == ""
+    r, _ = lag_repo(tmp_path)
+    p = kjor(r, "--tor", "alle", "--prereg-id", "KLAR-PREREG-0001")
+    assert p.returncode == 0 and p.stdout.count("ville kjørt") == 4 and "--mal-person 300 --mal-sted 200 --maks-timer 4" in p.stdout
+    assert kjort(r) == [] and git(r, "status", "--porcelain") == ""
+
+
+def test_en_del_committer_pusher_og_speiler_med_meta_ved_siden_av_resultatet(tmp_path):
+    r, bart = lag_repo(tmp_path)
+    start = git(r, "rev-parse", "HEAD")
+    p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
+    assert p.returncode == 0, p.stderr
+    assert kjort(r) == ["h4 --prereg-id KLAR-PREREG-0001".replace("h4", "kjor_h4")]
+    d = json.loads((r / "docs" / "KLAR-EVAL-kjor_h4_v1.0_2026-10-27_kjoring_meta.json").read_text())
+    assert d["commit"] == start and d["git_status_porcelain_ved_start"] == [] and d["returkode"] == 0 and d["del"] == "H4"
+    assert d["tag_prereg_v1"] == start == d["tag_h4_script_v2"] and d["preregistrering"]["fil"].endswith("_v1.10_2026-10-27.md")  # versjonssortering
+    assert d["resultatfil"] == "docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27.json"
+    assert git(r, "status", "--porcelain") == "" and git(r, "rev-parse", "HEAD") != start
+    assert git(bart, "rev-parse", "main") == git(r, "rev-parse", "HEAD")  # pushet
+    assert (r / "speil.log").read_text().splitlines() == [f"speil {git(r, 'rev-parse', '--short', 'HEAD')} 0"]  # speilet etter commit, rent tre
+    assert set(git(r, "show", "--name-only", "--format=", "HEAD").split()) == {"docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27.json", "docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27_kjoring_meta.json"}
 
 
-def test_rent_tre_skriver_meta_ved_siden_av_resultatet(tmp_path):
-    r = lag_repo(tmp_path)
-    p = kjor(r, "--prereg-id", "KLAR-PREREG-0001")
+def test_to_kjoringer_etter_hverandre_hver_med_egen_commit_push_og_speil(tmp_path):
+    r, bart = lag_repo(tmp_path)
+    start = git(r, "rev-parse", "HEAD")
+    p = kjor(r, "alle", "--prereg-id", "KLAR-PREREG-0001")
     assert p.returncode == 0, p.stderr
-    assert (r / "kjort.txt").read_text() == "--prereg-id KLAR-PREREG-0001"
-    meta = r / "docs" / "KLAR-EVAL-0009_stubb_v1.0_2026-10-27_kjoring_meta.json"
-    d = json.loads(meta.read_text())
-    assert d["commit"] == git(r, "rev-parse", "HEAD") and d["git_status_porcelain_ved_start"] == [] and d["returkode"] == 0
-    assert d["tag_prereg_v1"] == d["commit"] == d["tag_h4_script_v2"]
-    assert d["preregistrering"]["fil"].endswith("_v1.10_2026-10-27.md")  # versjonssortering
-    assert d["resultatfil"] == "docs/KLAR-EVAL-0009_stubb_v1.0_2026-10-27.json"
-
-
-def test_returkode_fra_kjoringen_bevares(tmp_path):
-    r = lag_repo(tmp_path)
-    p = kjor(r, "--prereg-id", "KLAR-PREREG-0001", rc="3")
-    assert p.returncode == 3
-    assert json.loads(next((r / "docs").glob("*kjoring_meta.json")).read_text())["returkode"] == 3
+    assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord", "kjor_personvern_dev", "kjor_h4"]
+    assert "--datasett npsc --splitt test --prereg-id KLAR-PREREG-0001 --mal-person 300 --mal-sted 200 --maks-timer 4" in kjort(r)[1]
+    log = git(r, "log", "--format=%H %s", f"{start}..HEAD").splitlines()[::-1]
+    assert [l.split(" ", 1)[1][:10] for l in log] == [f"Testdel H{i}" for i in (1, 2, 3, 4)]
+    metas = [json.loads(p_.read_text()) for p_ in sorted((r / "docs").glob("*kjoring_meta.json"))]
+    shas = {m["del"]: m["commit"] for m in metas}
+    hashes = [l.split()[0] for l in log]
+    assert [shas[f"H{i}"] for i in (1, 2, 3, 4)] == [start] + hashes[:3]  # hver del startet på forrige dels commit
+    assert all(m["git_status_porcelain_ved_start"] == [] for m in metas)
+    assert git(bart, "rev-parse", "main") == hashes[-1]
+    assert [l.split()[1] for l in (r / "speil.log").read_text().splitlines()] == [git(r, "rev-parse", "--short", h) for h in hashes]  # speil etter hver commit
+    assert all(l.endswith(" 0") for l in (r / "speil.log").read_text().splitlines())
+
+
+def test_feil_i_en_del_committer_den_og_stopper(tmp_path):
+    r, bart = lag_repo(tmp_path)
+    p = kjor(r, "alle", "--prereg-id", "KLAR-PREREG-0001", STUBB_FEIL="kjor_flaggoverlevelse_ord")
+    assert p.returncode == 3 and "H2 feilet" in p.stderr
+    assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord"]  # H3 og H4 startet ikke
+    m = json.loads(next((r / "docs").glob("*flaggoverlevelse_ord*kjoring_meta.json")).read_text())
+    assert m["returkode"] == 3 and git(r, "status", "--porcelain") == "" and git(bart, "rev-parse", "main") == git(r, "rev-parse", "HEAD")
+
+
+def test_endret_sporet_fil_gir_ingen_commit_og_stopper(tmp_path):
+    r, bart = lag_repo(tmp_path)
+    start = git(r, "rev-parse", "HEAD")
+    p = kjor(r, "H1", "--prereg-id", "KLAR-PREREG-0001", STUBB_OVERSKRIV="kjor_dev")
+    assert p.returncode == 4 and "endret sporede filer" in p.stderr
+    assert git(r, "rev-parse", "HEAD") == start and (r / "docs" / "sporet.md").read_text() == "endret av kjøringen"  # ingenting tilbakestilt
+    assert subprocess.run(["git", "rev-parse", "-q", "--verify", "main"], cwd=bart, capture_output=True).returncode != 0  # ingenting pushet
+    assert not (r / "speil.log").exists()
```
4. **H1-utvalget (kode): `--per-dialekt` i `eval/dev/kjor_dev.py`.** PREREG (Data collection procedures, ordrett): «Utvalg: opptil 60 segmenter per dialektområde (e, n, sw, t, w), trukket med seed 20261026; har et område færre kvalifiserte segmenter, tas alle. Antall per område rapporteres.» og (Sample size): «H1: opptil 300 segmenter.» `kjor_dev.py` trakk fast 12 per område (`PER_DIALEKT = 12`, 60 segmenter). Nå finnes parameteren `--per-dialekt` (standard 12, altså uendret DEV-utvalg), og trekket er `rng.sample(pool, min(PER_DIALEKT, len(pool)))`: har et område færre kvalifiserte segmenter enn N, tas alle (som PREREG sier; før ga det en feil); for pooler som er store nok er trekket identisk med før (testet mot den gamle logikken ordrett). Utvalgslogikken (filter, sortering, seed) og WER-beregningen er ikke endret. Testdelen H1 kjøres med `--per-dialekt 60`, verdien PREREG oppgir.
5. **Navn på testresultater (kode): `--ut-mappe`, `--etikett`, `--eval-nr` i H1–H3-skriptene** (`kjor_dev.py`, `kjor_flaggoverlevelse_ord.py`, `kjor_personvern_dev.py`). Standardverdiene (`eval/dev` eller `docs`, `DEV`, ingen `--eval-nr`) gir nøyaktig dagens DEV-filnavn, merknader og overskrifter. Med `--etikett TEST` er merknaden og overskriften «TEST – preregistrert (OSF hc83q)». Nye EVAL-numre fra nummerregisteret (ARK-0003 v1.12 (i git-historikken)): **KLAR-EVAL-0013** (H1, NB Samtale), **KLAR-EVAL-0014** (H2, NPSC), **KLAR-EVAL-0015** (H3, NorNE), filer under `eval/test/`; H4 bruker det reserverte **KLAR-EVAL-0009** (`kjor_h4.py` er ikke endret og skriver til `docs/`). `scripts/kjor_testdel.sh` sender disse parametrene.
6. **Bevis for at utregningen er uendret (`scripts/verifiser_uendret.py`):** DEV-skriptene kjørt med standardverdier, uten Whisper (lagrede hypoteser), og sammenlignet eksakt (floats bit for bit) med de committede resultatene. Resultat:

   | EVAL | sammenlignet med | identiske tall | enheter | første avvik |
   |---|---|---|---|---|
   | KLAR-EVAL-0002 v1.1 (WER NB Samtale, utvalg, hypoteser) | `eval/dev/kjor_dev.py` med standardverdier, Whisper byttet med lagrede hypoteser (samme segmentering, trekk og WER-kode) | **JA** | 60 segmenter | – |
   | KLAR-EVAL-0006 v1.2 (flaggoverlevelse NB Samtale) | `kjor_flaggoverlevelse_ord.py --datasett nbsamtale --fase evaluer` på lagrede hypoteser (reproduksjon 27.10) | **JA** | 60 segmenter | – |
   | KLAR-EVAL-0007 v1.1 (flaggoverlevelse NPSC) | `kjor_flaggoverlevelse_ord.py --datasett npsc --fase evaluer` på lagrede hypoteser | **JA** | 934 segmenter | – |
   | KLAR-EVAL-0005 (NorNE, recall og presisjon) | `kjor_personvern_dev.py` med standardverdier (full kjøring, ingen Whisper; kjøretid unntatt) | **JA** | 24 resultatnøkler | – |


   Nye filer (ingen analysekode): 
   - `scripts/verifiser_uendret.py` (sha256 `24d9ae67bb7fed9126703a4f2c9dc0446a9ee6470376e3cebeea8c0bd524d7c9`, 140 linjer)
   - `scripts/rapporter_intervaller.py` (sha256 `971c105dabf496f090011fface7ba44e2ad2c7cd47e35f6928b4a62a5d3b70d2`, 156 linjer)
   - `tests/test_dev_parametre.py` (sha256 `e57e6abd464a586fe2c7df5f27f5ac93e0534c4974c4ef87a55213105c7efda1`, 81 linjer)
   Diff (ordrett) mot commit `7ea3004` for analysekoden og wrapperen (`git diff HEAD -- eval/dev/kjor_dev.py eval/dev/kjor_flaggoverlevelse_ord.py eval/dev/kjor_personvern_dev.py scripts/kjor_testdel.sh tests/test_kjor_testdel.py`):

```diff
diff --git a/eval/dev/kjor_dev.py b/eval/dev/kjor_dev.py
index ada86e5..a2d6371 100644
--- a/eval/dev/kjor_dev.py
+++ b/eval/dev/kjor_dev.py
@@ -38,7 +38,11 @@ DATA = pathlib.Path(os.environ.get("ARKIVKLARERING_EVALDATA", "/Volumes/Vault/ar
 SPLITT = "validation"  # settes av --splitt; test-delen er sperret (arkivklarering/evaldata.py)
 PREREG_ID = None
 SEED = 20261026
-PER_DIALEKT = 12
+PER_DIALEKT = 12  # settes av --per-dialekt (standard 12 = DEV-utvalget)
+UT_MAPPE = None  # settes av --ut-mappe (standard: denne mappen)
+ETIKETT = "DEV"  # settes av --etikett (DEV eller TEST)
+EVAL_NR = None  # settes av --eval-nr (standard: KLAR-EVAL-0002 og -0003, dagens DEV-filnavn)
+ETIKETT_TEST = "TEST – preregistrert (OSF hc83q)"
 DIALEKTER = ["e", "n", "sw", "t", "w"]
 DATO = datetime.date.today().isoformat()
 SPRAK_FRA_SKRIFTFORM = {"bm": "no", "nn": "nn"}
@@ -52,7 +56,7 @@ def trekk_utvalg():
     valg = []
     for d in DIALEKTER:
         pool = sorted((r for r in kandidater if r["dialect"] == d), key=lambda r: (r["source_file_id"], r["segment_id"]))
-        valg += rng.sample(pool, PER_DIALEKT)
+        valg += rng.sample(pool, min(PER_DIALEKT, len(pool)))  # har et område færre kvalifiserte, tas alle (PREREG, Study design); gir samme trekk som før når poolen er stor nok
     return valg, len(kandidater)
 
 
@@ -87,15 +91,27 @@ def main():
     ap.add_argument("--splitt", default="validation", choices=evaldata.SPLITT,
                     help="datasettdel (standard: validation). test krever --prereg-id")
     ap.add_argument("--prereg-id", help="KLAR-PREREG-<NNNN>; kreves for --splitt test")
+    ap.add_argument("--per-dialekt", type=int, default=12, help="segmenter per dialektområde (standard 12 = DEV-utvalget; PREREG H1: 60)")
+    ap.add_argument("--ut-mappe", default=str(HER), help="mappe for utdata (standard: eval/dev)")
+    ap.add_argument("--etikett", default="DEV", choices=["DEV", "TEST"], help="DEV (standard) eller TEST (overskrift «TEST – preregistrert (OSF hc83q)»)")
+    ap.add_argument("--eval-nr", help="KLAR-EVAL-<NNNN> for utdatafilene (standard: -0002 for resultatet og -0003 for utvalget, som i DEV)")
     a = ap.parse_args()
-    global SPLITT, PREREG_ID
-    SPLITT, PREREG_ID = a.splitt, a.prereg_id
+    global SPLITT, PREREG_ID, PER_DIALEKT, UT_MAPPE, ETIKETT, EVAL_NR
+    SPLITT, PREREG_ID, PER_DIALEKT, UT_MAPPE, ETIKETT, EVAL_NR = a.splitt, a.prereg_id, a.per_dialekt, pathlib.Path(a.ut_mappe), a.etikett, a.eval_nr
     evaldata.sjekk_splitt(SPLITT, PREREG_ID)  # hard sperre før noe leses
 
     valg, n_kand = trekk_utvalg()
-    utvalg_sti = HER / f"KLAR-EVAL-0003_arkivklarering_dev-utvalg_v1.0_{DATO}.json"
+    UT_MAPPE.mkdir(parents=True, exist_ok=True)
+    if ETIKETT == "DEV" and EVAL_NR is None:
+        utvalg_sti = UT_MAPPE / f"KLAR-EVAL-0003_arkivklarering_dev-utvalg_v1.0_{DATO}.json"
+        stamme = UT_MAPPE / f"KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_{DATO}"
+    else:
+        nr = EVAL_NR or "KLAR-EVAL-0002"
+        utvalg_sti = UT_MAPPE / f"{nr}_arkivklarering_{ETIKETT.lower()}-nbsamtale-wer_v1.0_{DATO}.utvalg.json"
+        stamme = UT_MAPPE / f"{nr}_arkivklarering_{ETIKETT.lower()}-nbsamtale-wer_v1.0_{DATO}"
+    merknad = "DEV, ikke pilot" if ETIKETT == "DEV" else ETIKETT_TEST
     utvalg_sti.write_text(json.dumps({
-        "merknad": f"DEV, ikke pilot. Lagdelt utvalg fra Sprakbanken/nb_samtale ({SPLITT}), fast seed.",
+        "merknad": f"DEV, ikke pilot. Lagdelt utvalg fra Sprakbanken/nb_samtale ({SPLITT}), fast seed." if ETIKETT == "DEV" else f"{ETIKETT_TEST}. Lagdelt utvalg fra Sprakbanken/nb_samtale ({SPLITT}), fast seed.",
         "datasett_revisjon": "1c7028101858b854d3d568761778d8f63bb7e33f", "splitt": SPLITT,
         "seed": SEED, "per_dialekt": PER_DIALEKT,
         "filter": "ingen overlapp mot forrige/neste, 2–12 s, minst 3 ord i fasiten",
@@ -173,15 +189,22 @@ def main():
             tabell[kol][grp] = None if w is None else round(w, 4)
             tabell[kol][grp + "_n"] = len(par)
     modeller = {lag: {"modell": pathlib.Path(o.modell).name, "sha256": o.sha256} for lag, o in oppsett.items()}
-    (HER / f"KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_{DATO}.json").write_text(json.dumps(
-        {"merknad": "DEV, ikke pilot", "seed": SEED, "modeller": modeller, "wer": tabell,
+    pathlib.Path(str(stamme) + ".json").write_text(json.dumps(
+        {"merknad": merknad, "seed": SEED, "modeller": modeller, "wer": tabell,
          "segmenter": per_segment}, ensure_ascii=False, indent=2), encoding="utf-8")
 
     kols = list(tabell)
-    md = [f"# DEV-måling ({DATO}): WER på nb_samtale ({SPLITT}), 60 segmenter", "",
-          "**DEV, ikke pilot. Ingen konklusjoner om pilotkvalitet.** 12 segmenter per dialektområde "
-          f"(e, n, sw, t, w), seed {SEED}. Fasit: `orthographic`. Korpus-WER etter normalisering (små bokstaver, "
-          "tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.", "",
+    if ETIKETT == "DEV":
+        topp = [f"# DEV-måling ({DATO}): WER på nb_samtale ({SPLITT}), 60 segmenter", "",
+                "**DEV, ikke pilot. Ingen konklusjoner om pilotkvalitet.** 12 segmenter per dialektområde "
+                f"(e, n, sw, t, w), seed {SEED}. Fasit: `orthographic`. Korpus-WER etter normalisering (små bokstaver, "
+                "tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.", ""]
+    else:
+        topp = [f"# {ETIKETT_TEST} ({DATO}): WER på nb_samtale ({SPLITT}), {len(valg)} segmenter", "",
+                f"**{ETIKETT_TEST}.** Opptil {PER_DIALEKT} segmenter per dialektområde (e, n, sw, t, w), seed {SEED}; har et område færre kvalifiserte segmenter, tas alle. "
+                "Antall per område: " + ", ".join(f"{d} {sum(1 for r in valg if r['dialect'] == d)}" for d in DIALEKTER) + ". Fasit: `orthographic`. "
+                "Korpus-WER etter normalisering (små bokstaver, tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.", ""]
+    md = [*topp,
           "`ra` = NB-Whisper large verbatim, `normalisert` = NB-Whisper large (ikke verbatim). "
           "`nn` = `-l nn` for alle; `matchet` = språk etter fasitens skriftform. "
           "Rålaget skriver ut nøling og omtrent som sagt og scores likevel mot ortografisk fasit, så ra-tallene "
@@ -191,9 +214,9 @@ def main():
         n = tabell[kols[0]][grp + "_n"]
         md.append(f"| {grp} ({n}) | " + " | ".join("–" if tabell[k][grp] is None else f"{tabell[k][grp]:.3f}" for k in kols) + " |")
     ingen = {k: sum(1 for s in per_segment if not s["hyp"][k].strip()) for k in kols}
-    md += ["", "Segmenter uten noen tekst (tom hypotese), av 60: " + ", ".join(f"{k}: {v}" for k, v in ingen.items()), "",
+    md += ["", f"Segmenter uten noen tekst (tom hypotese), av {len(per_segment)}: " + ", ".join(f"{k}: {v}" for k, v in ingen.items()), "",
            "Modeller: " + "; ".join(f"{l}: `{m['modell']}` sha256 `{m['sha256']}`" for l, m in modeller.items())]
-    (HER / f"KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_{DATO}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
+    pathlib.Path(str(stamme) + ".md").write_text("\n".join(md) + "\n", encoding="utf-8")
     print("\n".join(md))
 
 
diff --git a/eval/dev/kjor_flaggoverlevelse_ord.py b/eval/dev/kjor_flaggoverlevelse_ord.py
index 87f07f0..7f64789 100644
--- a/eval/dev/kjor_flaggoverlevelse_ord.py
+++ b/eval/dev/kjor_flaggoverlevelse_ord.py
@@ -217,6 +217,9 @@ def main():
     ap.add_argument("--maks-timer", type=float, default=2.0)
     ap.add_argument("--mal-person", type=int, default=150)
     ap.add_argument("--mal-sted", type=int, default=100)
+    ap.add_argument("--ut-mappe", default=str(REPO / "docs"), help="mappe for resultatfila (standard: docs)")
+    ap.add_argument("--etikett", default="DEV", choices=["DEV", "TEST"], help="DEV (standard) eller TEST («TEST – preregistrert (OSF hc83q)» i merknaden)")
+    ap.add_argument("--eval-nr", help="KLAR-EVAL-<NNNN> for resultatfila (standard: -0006 for nbsamtale og -0007 for npsc, som i DEV)")
     a = ap.parse_args()
     evaldata.sjekk_splitt(a.splitt, a.prereg_id)  # hard sperre før noe leses
     if a.datasett == "nbsamtale" and a.splitt != "validation":
@@ -263,17 +266,21 @@ def main():
     if a.fase in ("evaluer", "alle"):
         motor = personvern.lag_motor()
         res = evaluer(items, cache, motor)
-        meta = {"merknad": "DEV, ikke pilot", "datasett": a.datasett, "splitt": a.splitt, "seed": a.seed,
+        meta = {"merknad": "DEV, ikke pilot" if a.etikett == "DEV" else "TEST – preregistrert (OSF hc83q)", "datasett": a.datasett, "splitt": a.splitt, "seed": a.seed,
                 "lyd_sek": round(sum(i["varighet"] for i in items if i["id"] in cache)), "segmenter": len([i for i in items if i["id"] in cache]),
                 "ikke_malt": IKKE_MALT, "ordtider": "DTW (-nfa -dtw large.v3), paring på ordspenn med toleranse "
                 + f"{personvern.TIDSTOLERANSE_S} s", "resultat": res}
         if a.datasett == "npsc" and prefiks_sti.exists():
             meta["prefiks"] = json.loads(prefiks_sti.read_text(encoding="utf-8"))
+        ut_mappe = pathlib.Path(a.ut_mappe)
+        ut_mappe.mkdir(parents=True, exist_ok=True)
         if a.datasett == "nbsamtale":
-            sti = REPO / "docs" / f"KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.1_{DATO}.json"
+            sti = ut_mappe / f"KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.1_{DATO}.json"
         else:
             meta["segment_ider"] = [i["id"] for i in items if i["id"] in cache]
-            sti = REPO / "docs" / f"KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_{DATO}.json"
+            sti = ut_mappe / f"KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_{DATO}.json"
+        if a.etikett == "TEST" or a.eval_nr:
+            sti = ut_mappe / f"{a.eval_nr or sti.name.split('_')[0]}_arkivklarering_{a.etikett.lower()}-flaggoverlevelse-{a.datasett}_v1.0_{DATO}.json"
         sti.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
         logg(sti)
 
diff --git a/eval/dev/kjor_personvern_dev.py b/eval/dev/kjor_personvern_dev.py
index d3b8105..bed5106 100644
--- a/eval/dev/kjor_personvern_dev.py
+++ b/eval/dev/kjor_personvern_dev.py
@@ -113,6 +113,9 @@ def main():
     ap = argparse.ArgumentParser()
     ap.add_argument("--splitt", default="validation", choices=evaldata.SPLITT)
     ap.add_argument("--prereg-id")
+    ap.add_argument("--ut-mappe", default=str(HER.parent.parent / "docs"), help="mappe for resultatfila (standard: docs)")
+    ap.add_argument("--etikett", default="DEV", choices=["DEV", "TEST"], help="DEV (standard) eller TEST («TEST – preregistrert (OSF hc83q)» i merknaden)")
+    ap.add_argument("--eval-nr", help="KLAR-EVAL-<NNNN> for resultatfila (standard: KLAR-EVAL-0005, som i DEV)")
     ap.add_argument("--maks", type=int, default=0, help="bare de første N setningene per målform (røyktest)")
     a = ap.parse_args()
     evaldata.sjekk_splitt(a.splitt, a.prereg_id)
@@ -178,11 +181,16 @@ def main():
             "recall_overlapp": r(c["gull_overlapp"], c["gull"]), "recall_overlapp_ki95": [lo, hi],
             "recall_noyaktig": r(c["gull_noyaktig"], c["gull"]),
             "presisjon_overlapp": r(c["pred_overlapp"], c["pred"]), "presisjon_noyaktig": r(c["pred_noyaktig"], c["pred"])}
-    ut = {"merknad": "DEV, ikke pilot", "datasett": "NbAiLab/norne", "revisjon": REVISJON, "splitt": a.splitt,
+    ut = {"merknad": "DEV, ikke pilot" if a.etikett == "DEV" else "TEST – preregistrert (OSF hc83q)", "datasett": "NbAiLab/norne", "revisjon": REVISJON, "splitt": a.splitt,
           "motor": {"spacy": personvern.SPACY_MODELL, "bert": personvern.BERT_MODELL, "terskel": 0.0},
           "setninger_hoppet_over_pga_tokenjustering": {f"{k[0]}|{k[1]}": v for k, v in hoppet.items()},
           "resultat": resultat, "sekunder": round(time.time() - t0)}
-    sti = HER.parent.parent / "docs" / f"KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_{DATO}.json"
+    ut_mappe = pathlib.Path(a.ut_mappe)
+    ut_mappe.mkdir(parents=True, exist_ok=True)
+    if a.etikett == "DEV" and not a.eval_nr:
+        sti = ut_mappe / f"KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_{DATO}.json"
+    else:
+        sti = ut_mappe / f"{a.eval_nr or 'KLAR-EVAL-0005'}_arkivklarering_personvern-{a.etikett.lower()}_v1.0_{DATO}.json"
     sti.write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
     print(sti, flush=True)
 
diff --git a/scripts/kjor_testdel.sh b/scripts/kjor_testdel.sh
index 2ad2d3a..79e6620 100755
--- a/scripts/kjor_testdel.sh
+++ b/scripts/kjor_testdel.sh
@@ -5,10 +5,11 @@
 #
 #   source scripts/miljo.sh && scripts/kjor_testdel.sh [--tor] <H1|H2|H3|H4|alle> --prereg-id KLAR-PREREG-0001 [-- ekstra argumenter]
 #
-#   H1  eval/dev/kjor_dev.py --splitt test                                              (NB Samtale test)
-#   H2  eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --mal-person 300 --mal-sted 200 --maks-timer 4   (PREREG: doble mål)
-#   H3  eval/dev/kjor_personvern_dev.py --splitt test                                   (NorNE test)
-#   H4  kalibrering/kjor_h4.py                                                          (menneskeinnlest testmanus)
+#   H1  eval/dev/kjor_dev.py --splitt test --per-dialekt 60 ... --eval-nr KLAR-EVAL-0013   (NB Samtale test; PREREG: opptil 60 per dialektområde)
+#   H2  eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --mal-person 300 --mal-sted 200 --maks-timer 4 ... --eval-nr KLAR-EVAL-0014   (PREREG: doble mål)
+#   H3  eval/dev/kjor_personvern_dev.py --splitt test ... --eval-nr KLAR-EVAL-0015      (NorNE test)
+#   H4  kalibrering/kjor_h4.py                                                          (menneskeinnlest testmanus; skriver docs/KLAR-EVAL-0009_..., reservert nummer)
+#   H1–H3 skriver til eval/test/ med --etikett TEST (merknad «TEST – preregistrert (OSF hc83q)»).
 #   alle = H1, H2, H3, H4 i den rekkefølgen (H4 til sist: opptakene må være innlest og scoret først, se PREREG).
 #
 # Før hver del: `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1). Etter hver del skrives
@@ -39,9 +40,9 @@ if [ "$DEL" = alle ]; then DELER=(H1 H2 H3 H4); else DELER=("$DEL"); fi
 
 kommando() {  # skriver skriptet og argumentene for en del, ett ord per linje
   case "$1" in
-    H1) printf '%s\n' eval/dev/kjor_dev.py --splitt test --prereg-id "$ID" ;;
-    H2) printf '%s\n' eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --prereg-id "$ID" --mal-person 300 --mal-sted 200 --maks-timer 4 ;;
-    H3) printf '%s\n' eval/dev/kjor_personvern_dev.py --splitt test --prereg-id "$ID" ;;
+    H1) printf '%s\n' eval/dev/kjor_dev.py --splitt test --prereg-id "$ID" --per-dialekt 60 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0013 ;;
+    H2) printf '%s\n' eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --prereg-id "$ID" --mal-person 300 --mal-sted 200 --maks-timer 4 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0014 ;;
+    H3) printf '%s\n' eval/dev/kjor_personvern_dev.py --splitt test --prereg-id "$ID" --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015 ;;
     H4) printf '%s\n' kalibrering/kjor_h4.py --prereg-id "$ID" ;;
   esac
 }
@@ -87,7 +88,7 @@ for d in "${DELER[@]}"; do
     exit 4
   fi
   NYE="$(git status --porcelain --untracked-files=all | sed 's/^?? //' | sort)"
-  RES="$(echo "$NYE" | grep -E '^(docs/KLAR-EVAL|eval/dev/KLAR-EVAL).*\.json$' | head -1 || true)"
+  RES="$(echo "$NYE" | grep -E '^(docs|eval/dev|eval/test)/KLAR-EVAL.*\.json$' | grep -v '\.utvalg\.json$' | head -1 || true)"
   [ -n "$RES" ] || RES="$(echo "$NYE" | grep -E '\.json$' | head -1 || true)"
   if [ -n "$RES" ]; then META="${RES%.json}_kjoring_meta.json"; else META="docs/kjoring_meta_${d}_$TID.json"; fi
   export META SHA START SLUTT RC KMD PRE MAN RES DEL_NAVN="$d" NYE
diff --git a/tests/test_kjor_testdel.py b/tests/test_kjor_testdel.py
index eae3447..f15dd47 100644
--- a/tests/test_kjor_testdel.py
+++ b/tests/test_kjor_testdel.py
@@ -99,7 +99,9 @@ def test_to_kjoringer_etter_hverandre_hver_med_egen_commit_push_og_speil(tmp_pat
     p = kjor(r, "alle", "--prereg-id", "KLAR-PREREG-0001")
     assert p.returncode == 0, p.stderr
     assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord", "kjor_personvern_dev", "kjor_h4"]
-    assert "--datasett npsc --splitt test --prereg-id KLAR-PREREG-0001 --mal-person 300 --mal-sted 200 --maks-timer 4" in kjort(r)[1]
+    assert "--datasett npsc --splitt test --prereg-id KLAR-PREREG-0001 --mal-person 300 --mal-sted 200 --maks-timer 4 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0014" in kjort(r)[1]
+    assert kjort(r)[0].endswith("--per-dialekt 60 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0013")
+    assert kjort(r)[2].endswith("--ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015") and kjort(r)[3].endswith("kjor_h4 --prereg-id KLAR-PREREG-0001")
     log = git(r, "log", "--format=%H %s", f"{start}..HEAD").splitlines()[::-1]
     assert [l.split(" ", 1)[1][:10] for l in log] == [f"Testdel H{i}" for i in (1, 2, 3, 4)]
     metas = [json.loads(p_.read_text()) for p_ in sorted((r / "docs").glob("*kjoring_meta.json"))]
```
7. **95 %-intervallmetoden (låst før noen testdel er åpnet).** PREREG (Statistical models & analysis plan, ordrett): «Beskrivende. Proporsjoner med Wilson-95 %-intervall (H2, H3, H4); korpus-WER med **clusterbootstrap** over taler (NB Samtale `speaker_id`; NPSC `speaker_id`), 2000 gjentak, seed 20261026; differansen i K1 med parret clusterbootstrap. NorNE: bootstrap over setninger.» Metoden er altså spesifisert (clusterbootstrap over taler, 2000 gjentak, seed 20261026, parret for K1; Wilson for proporsjoner), men **intervalltypen er ikke oppgitt**. Låst nå: **persentilintervall**, nedre grense = element `int(0,025·B)` og øvre = element `int(0,975·B) − 1` (0-indeksert) av de sorterte bootstrap-verdiene, B = 2000; per gjentak trekkes like mange talere som det finnes (med tilbakelegging), alle segmentene til de trukne talerne tas med, WER = sum av feil / sum av referanseord; samme trekk brukes for alle kolonner (parret). Verdiene B = 10 000 og «NorNE per dokument» er **ikke** brukt, fordi PREREG allerede fastsetter 2000 gjentak og setninger. Implementert i et eget rapportskript som leser resultat-JSON (`scripts/rapporter_intervaller.py`; analysekoden er ikke endret) og testet på DEV-resultatene (EVAL-0002 v1.1: totalt rålag/matchet 0,135, 95 %-intervall 0,095–0,171, 33 talere; K1-differanse 0,213, 0,149–0,282, utelukker 0). **Begrensning:** `kjor_personvern_dev.py` skriver bare aggregerte tellere, ikke tall per setning; bootstrap over setninger for NorNE (H3) er derfor ikke mulig fra resultat-JSON, og skriptet gir Wilson fra tellerne.
8. **H4-begrensning:** H4 måles med én leser, som er forfatter og kjenner målelementene. Resultatet gjelder bare én taler og kan ikke generaliseres. (PREREG nevner «Eirik og eventuelt andre lesere»; skal ikke flere lese inn, gjelder begrensningen alle H4-tall.) Skal stå i KLAR-EVAL-0009.
9. **AV-15: tellere per setning fra `eval/dev/kjor_personvern_dev.py` (NorNE, H3).** Beslutning 2026-10-27: skriptet skriver i tillegg tellere per setning i en ny utdatafil (`<resultat>.setninger.json`: målform, radnummer, `idx`, variant, motor, type og de seks tellerne `gull`, `gull_overlapp`, `gull_noyaktig`, `pred`, `pred_overlapp`, `pred_noyaktig`). Den aggregerte utregningen er ikke endret: tellene i resultat-JSON summeres fra de samme seks tallene som skrives per setning (`d`), så de er summen av filene. Dette løser begrensningen i AV-13 (bootstrap over setninger for NorNE kunne ikke regnes fra resultat-JSON): `scripts/rapporter_intervaller.py norne <resultat> <setninger>` gir bootstrap over setninger (B = 2000, `numpy.random.default_rng(20261026)` i rekkefølgen av sorterte gruppenøkler, persentilregelen fra AV-13) ved siden av Wilson. **Bevis (`scripts/verifiser_uendret.py --bare 5`, full kjøring med standardverdier):** aggregatene er identiske med KLAR-EVAL-0005 (**JA**, 24 resultatnøkler, ingen avvik, kjøretid unntatt), og tellerne i de 51 600 setningsradene summerer til de aggregerte tellene og gir de samme recall- og presisjonsverdiene (kontrollen er lagt inn i verifiseringsskriptet). EVAL-0002 v1.1, -0006 v1.2 og -0007 v1.1 er ikke berørt av denne endringen (kontrollert identisk i punkt 6; `kjor_dev.py` og `kjor_flaggoverlevelse_ord.py` er ikke endret siden).
10. **AV-16: kodesjekk mot taggen `testkjoring-v1` i `scripts/kjor_testdel.sh`, og taggen.** Før hver testdel kontrollerer skriptet at koden er uendret siden taggen: `git diff --quiet testkjoring-v1 -- arkivklarering kalibrering tests scripts` og alle `.py`-filer under `eval/` (`':(glob)eval/**/*.py'`); endret kode eller manglende tagg gir exit 5 og ingenting kjøres. Kravet er ikke at HEAD er taggen, fordi resultat-commitene (`docs/`, `eval/test/`) er tillatt. Metafila får `tag_testkjoring_v1` og `kode_uendret_siden_testkjoring_v1`. Testet i `tests/test_kjor_testdel.py` (endring i hver kodemappe stopper; resultatfiler og ikke-`.py`-filer under `eval/` tillates; manglende tagg stopper; to testdeler etter hverandre, og endret kode mellom dem nekter den andre). **Tag `testkjoring-v1`** er satt på commit `871dba942a665fc7401261153b6c7e0114289ac9` (annotert tag-objekt `7ddd1fbe8abd936d5add9a39b95e79dc691ac592`) etter 140 grønne tester, og pushet. Den peker på all kode testdelene kjøres med, inkludert punkt 4–7 over og punkt 9 her. Kode endret etter taggen betyr at testdelene ikke kan startes uten at en ny tag (og avvik) føres først.
11. **Bekreftet av eier 2026-10-27, før testdata:** (a) 95 %-intervallene følger PREREG uendret: clusterbootstrap over taler (2000 gjentak, seed 20261026), NorNE over setninger, Wilson for proporsjoner, persentilintervall (punkt 7); ingen endring. (b) `min(N, len(pool))` i `kjor_dev.py` er godkjent som tolkning av PREREG: ordlyden er «Utvalg: opptil 60 segmenter per dialektområde (e, n, sw, t, w), trukket med seed 20261026; har et område færre kvalifiserte segmenter, tas alle. Antall per område rapporteres.», og «tas alle» er det `min` gjør. (c) H4 skriver til `docs/KLAR-EVAL-0009…` som før (`kjor_h4.py` er ikke endret).

   Diff (ordrett) for denne endringen (`git diff 871dba9~1 871dba9 -- eval/dev/kjor_personvern_dev.py scripts/kjor_testdel.sh`):

```diff
diff --git a/eval/dev/kjor_personvern_dev.py b/eval/dev/kjor_personvern_dev.py
index bed5106..54d838a 100644
--- a/eval/dev/kjor_personvern_dev.py
+++ b/eval/dev/kjor_personvern_dev.py
@@ -107,6 +107,9 @@ def wilson(k, n, z=1.96):
     return (round(c - h, 3), round(c + h, 3))
 
 
+TELLERE = ("gull", "gull_overlapp", "gull_noyaktig", "pred", "pred_overlapp", "pred_noyaktig")
+
+
 def main():
     from arkivklarering.miljo import krev_vault_miljo
     krev_vault_miljo()  # avbryter hvis miljøet ikke peker til Vault (source scripts/miljo.sh først)
@@ -134,11 +137,12 @@ def main():
 
     tell = collections.defaultdict(lambda: collections.Counter())
     hoppet = collections.Counter()
+    per_setning = []  # tellere per setning (egen utdatafil `.setninger.json`); de aggregerte tellene under er summen av disse
     for config, sprak in MALFORM.items():
         tab = pq.read_table(evaldata.norne_sti(DATA, config, a.splitt, a.prereg_id)).to_pylist()
         if a.maks:
             tab = tab[:a.maks]
-        for rad in tab:
+        for rad_nr, rad in enumerate(tab):
             tokens, tags = rad["tokens"], rad["ner_tags"]
             gull = gull_spenn(tokens, tags)
             for variant in ("original", "små"):
@@ -163,12 +167,13 @@ def main():
                         g = [x for x in gs if x[2] == typ]
                         pp = [x for x in pred if x[2] == typ]
                         c = tell[(sprak, typ, navn, variant)]
-                        c["gull"] += len(g)
-                        c["gull_overlapp"] += sum(any(overlapper(x, y) for y in pp) for x in g)
-                        c["gull_noyaktig"] += sum(any(x == y for y in pp) for x in g)
-                        c["pred"] += len(pp)
-                        c["pred_overlapp"] += sum(any(overlapper(x, y) for y in g) for x in pp)
-                        c["pred_noyaktig"] += sum(any(x == y for y in g) for x in pp)
+                        d = {"gull": len(g), "gull_overlapp": sum(any(overlapper(x, y) for y in pp) for x in g),
+                             "gull_noyaktig": sum(any(x == y for y in pp) for x in g), "pred": len(pp),
+                             "pred_overlapp": sum(any(overlapper(x, y) for y in g) for x in pp),
+                             "pred_noyaktig": sum(any(x == y for y in g) for x in pp)}
+                        for k, v in d.items():
+                            c[k] += v
+                        per_setning.append([config, rad_nr, str(rad.get("idx", "")), variant, navn, typ, *(d[k] for k in TELLERE)])
         print(f"{config}: {len(tab)} setninger, {time.time() - t0:.0f} s", flush=True)
 
     resultat = {}
@@ -193,6 +198,11 @@ def main():
         sti = ut_mappe / f"{a.eval_nr or 'KLAR-EVAL-0005'}_arkivklarering_personvern-{a.etikett.lower()}_v1.0_{DATO}.json"
     sti.write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
     print(sti, flush=True)
+    sti_s = sti.with_name(sti.stem + ".setninger.json")  # ikke et KLAR-dokument i nummerregisteret (navnet slutter ikke på .json rett etter datoen)
+    sti_s.write_text(json.dumps({"merknad": ut["merknad"], "splitt": a.splitt, "revisjon": REVISJON,
+                                 "kolonner": ["config", "rad", "idx", "variant", "motor", "type", *TELLERE], "rader": per_setning},
+                                ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
+    print(sti_s, flush=True)
 
 
 if __name__ == "__main__":
diff --git a/scripts/kjor_testdel.sh b/scripts/kjor_testdel.sh
index 79e6620..5e8cafd 100755
--- a/scripts/kjor_testdel.sh
+++ b/scripts/kjor_testdel.sh
@@ -12,7 +12,9 @@
 #   H1–H3 skriver til eval/test/ med --etikett TEST (merknad «TEST – preregistrert (OSF hc83q)»).
 #   alle = H1, H2, H3, H4 i den rekkefølgen (H4 til sist: opptakene må være innlest og scoret først, se PREREG).
 #
-# Før hver del: `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1). Etter hver del skrives
+# Før hver del: (1) `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1); (2) koden må være uendret siden
+# taggen `testkjoring-v1` (`git diff --quiet testkjoring-v1 -- arkivklarering kalibrering tests scripts` og alle .py-filer under eval/), ellers kjøres
+# ingenting (exit 5; mangler taggen, er det også exit 5). Kravet er IKKE at HEAD er taggen: resultat-commitene (docs/, eval/test/) er tillatt. Etter hver del skrives
 # <resultat>_kjoring_meta.json (commit-SHA ved start, tom porcelain, kommando, tider, returkode, resultatfiler, SHA-ene til taggene og sha256 for PREREG-
 # og MANUS-fila). Så: commit av resultat og metafil, push, speil. Stopper hele kjøringen (ingen neste del) hvis en del feiler, hvis en SPORET fil er
 # endret av kjøringen (da committes ingenting, exit 4; fjerner ikke noe), eller hvis commit, push eller speil feiler. Feilede deler committes (med
@@ -56,7 +58,21 @@ rent_eller_stopp() {
   fi
 }
 
+kode_uendret_eller_stopp() {
+  local TAGG="${KLAR_KODETAGG:-testkjoring-v1}"
+  if ! git rev-parse -q --verify "refs/tags/$TAGG^{commit}" >/dev/null; then
+    echo "FEIL: taggen $TAGG finnes ikke; kan ikke vise at koden er uendret. Kjører ikke." >&2
+    exit 5
+  fi
+  if ! git diff --quiet "$TAGG" -- arkivklarering kalibrering tests scripts ':(glob)eval/**/*.py'; then
+    echo "FEIL: koden er endret siden taggen $TAGG; kjører ikke. Endrede filer:" >&2
+    git diff --name-only "$TAGG" -- arkivklarering kalibrering tests scripts ':(glob)eval/**/*.py' >&2
+    exit 5
+  fi
+}
+
 rent_eller_stopp
+kode_uendret_eller_stopp
 if [ "$TOR" -eq 1 ]; then
   for d in "${DELER[@]}"; do
     K=(); while IFS= read -r l; do K+=("$l"); done < <(kommando "$d")
@@ -67,6 +83,7 @@ fi
 
 for d in "${DELER[@]}"; do
   rent_eller_stopp   # etter forrige dels commit skal treet være rent igjen
+  kode_uendret_eller_stopp   # og koden fortsatt som i taggen (bare resultat-commiter er kommet til)
   K=(); while IFS= read -r l; do K+=("$l"); done < <(kommando "$d")
   SHA="$(git rev-parse HEAD)"
   KMD="$PY ${K[*]} ${EKSTRA[*]:-}"
@@ -94,13 +111,14 @@ for d in "${DELER[@]}"; do
   export META SHA START SLUTT RC KMD PRE MAN RES DEL_NAVN="$d" NYE
   export TAG_PREREG="$(git rev-parse -q --verify 'refs/tags/prereg-v1^{commit}' || echo mangler)"
   export TAG_H4="$(git rev-parse -q --verify 'refs/tags/h4-script-v2^{commit}' || echo mangler)"
+  export TAG_KODE="$(git rev-parse -q --verify "refs/tags/${KLAR_KODETAGG:-testkjoring-v1}^{commit}" || echo mangler)"
   export SHA_PRE="$(shasum -a 256 "$PRE" | cut -d' ' -f1)" SHA_MAN="$(shasum -a 256 "$MAN" | cut -d' ' -f1)"
   "$PY" - <<'PYEOF'
 import json, os
 e = os.environ
 ut = {"del": e["DEL_NAVN"], "commit": e["SHA"], "git_status_porcelain_ved_start": [], "kommando": e["KMD"], "start_utc": e["START"], "slutt_utc": e["SLUTT"],
       "returkode": int(e["RC"]), "resultatfil": e["RES"] or None, "nye_filer": [x for x in e["NYE"].split("\n") if x],
-      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"],
+      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"], "tag_testkjoring_v1": e["TAG_KODE"], "kode_uendret_siden_testkjoring_v1": True,
       "preregistrering": {"fil": e["PRE"], "sha256": e["SHA_PRE"]}, "manus": {"fil": e["MAN"], "sha256": e["SHA_MAN"]}}
 open(e["META"], "w", encoding="utf-8").write(json.dumps(ut, ensure_ascii=False, indent=2) + "\n")
 print(e["META"])
```
12. **AV-17: Innspillingsprotokoll spesifisert før datainnsamling (ikke i PREREG).** PREREG beskriver H4 («Innlesing med norsk-tales rigg … Alle innleste opptak teller») men ingen protokoll for selve innlesingen. Den er spesifisert i `KLAR-ADR-0018` (status accepted) før noe opptak finnes: riggversjon låst til norsk-tale `bcfef63d1be49ac239956dfb67784c002cecf310` med sha256 for de seks riggfilene (kontrollert ved start); lagring KUN under `/Volumes/Vault/arkivklarering/lyd/h4/` (fast i koden), aldri i git eller sky, som 16 kHz mono wav i `<runde>/opptak/<manus-id>.wav`; leseinstruksen «Les i naturlig tempo og på din vanlige dialekt. Ikke legg ekstra trykk på navn, tall eller fremmedord.» vises i riggen og må bekreftes lest; ta om bare ved feillesing (feil ord, avbrudd, støy), aldri på grunn av maskinens resultat; ingen visning av transkripsjon, flagg eller poeng (resultatside og eksport finnes ikke i modusen); logg per opptak (id, tidspunkt, forsøk, grunn); rom og mikrofon noteres én gang per runde. Ingen forhåndsregistrert terskel, utvalg eller analyse er berørt. Kode: `arkivklarering/h4_innlesing.py`, `arkivklarering/h4_side.html`, `scripts/rigg_manus.py`; tester: `tests/test_h4_innlesing.py` (ruter og side uten resultat, Vault-sti, instruks, omtakslogg, rigglås, kompatibilitet med `kjor_h4.finn_opptak`). `scripts/rigg_manus.py` startet tidligere norsk-tales hele rigg med `lyd/menneske/`; den starter nå bare H4-modusen. `kalibrering/kjor_h4.py` er ikke endret: standardmappen i skriptet er fortsatt `lyd/menneske`, og `scripts/kjor_testdel.sh` sender `--opptak /Volumes/Vault/arkivklarering/lyd/h4`.
13. **AV-18: ny kodetagg `testkjoring-v2`.** Innleseren ligger i `arkivklarering/` og `scripts/`, som kodesjekken i `scripts/kjor_testdel.sh` omfatter, så `testkjoring-v1` kunne ikke lenger brukes. `testkjoring-v1` (commit `871dba942a665fc7401261153b6c7e0114289ac9`) er beholdt og ikke flyttet. `testkjoring-v2` er satt etter 147 grønne tester på commit `c49d17463c14f7719f9f271ae3d4af4824436c35` (annotert tag-objekt `c4a7a8e5c293b6f20c880ab38cf705010882de9c`) og pushet; wrapperen kontrollerer nå `testkjoring-v2` og skriver både `tag_testkjoring` og `tag_testkjoring_v1` i metafila. Ingen analysekode (`kalibrering/`, `eval/`, resten av `arkivklarering/`) er endret mellom taggene; endringene er bare:
```
 arkivklarering/h4_innlesing.py | 189 +++++++++++++++++++++++++++++
 arkivklarering/h4_side.html    | 268 +++++++++++++++++++++++++++++++++++++++++
 scripts/kjor_testdel.sh        |  14 ++-
 scripts/rigg_manus.py          |  54 +++++----
 tests/test_h4_innlesing.py     | 164 +++++++++++++++++++++++++
 tests/test_kjor_testdel.py     |  11 +-
 6 files changed, 665 insertions(+), 35 deletions(-)
```
   Nye filer (ingen eksisterende analysekode):
   - `arkivklarering/h4_innlesing.py` (sha256 `262a3c2c747939ae55dc56cb3d8061ab7ba9c3e94647190740f88de7a3d2add6`, 189 linjer)
   - `arkivklarering/h4_side.html` (sha256 `d0b21d36a1c512f09607b4f6cbe04b70a4c110333cdbff28c8fe04232685aa9b`, 268 linjer)
   - `tests/test_h4_innlesing.py` (sha256 `1b9c655297ba504becd05fcdd0b128be77bfbade07eb98cd3b461807976a07a5`, 164 linjer)
   Diff (ordrett) for de eksisterende filene (`git diff testkjoring-v1 testkjoring-v2 -- scripts/rigg_manus.py scripts/kjor_testdel.sh tests/test_kjor_testdel.py`):

```diff
diff --git a/scripts/kjor_testdel.sh b/scripts/kjor_testdel.sh
index 5e8cafd..f95289c 100755
--- a/scripts/kjor_testdel.sh
+++ b/scripts/kjor_testdel.sh
@@ -8,12 +8,12 @@
 #   H1  eval/dev/kjor_dev.py --splitt test --per-dialekt 60 ... --eval-nr KLAR-EVAL-0013   (NB Samtale test; PREREG: opptil 60 per dialektområde)
 #   H2  eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --mal-person 300 --mal-sted 200 --maks-timer 4 ... --eval-nr KLAR-EVAL-0014   (PREREG: doble mål)
 #   H3  eval/dev/kjor_personvern_dev.py --splitt test ... --eval-nr KLAR-EVAL-0015      (NorNE test)
-#   H4  kalibrering/kjor_h4.py                                                          (menneskeinnlest testmanus; skriver docs/KLAR-EVAL-0009_..., reservert nummer)
+#   H4  kalibrering/kjor_h4.py --opptak /Volumes/Vault/arkivklarering/lyd/h4          (menneskeinnlest testmanus, innlest med scripts/rigg_manus.py; skriver docs/KLAR-EVAL-0009_...)
 #   H1–H3 skriver til eval/test/ med --etikett TEST (merknad «TEST – preregistrert (OSF hc83q)»).
 #   alle = H1, H2, H3, H4 i den rekkefølgen (H4 til sist: opptakene må være innlest og scoret først, se PREREG).
 #
 # Før hver del: (1) `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1); (2) koden må være uendret siden
-# taggen `testkjoring-v1` (`git diff --quiet testkjoring-v1 -- arkivklarering kalibrering tests scripts` og alle .py-filer under eval/), ellers kjøres
+# taggen `testkjoring-v2` (`git diff --quiet testkjoring-v2 -- arkivklarering kalibrering tests scripts` og alle .py-filer under eval/), ellers kjøres
 # ingenting (exit 5; mangler taggen, er det også exit 5). Kravet er IKKE at HEAD er taggen: resultat-commitene (docs/, eval/test/) er tillatt. Etter hver del skrives
 # <resultat>_kjoring_meta.json (commit-SHA ved start, tom porcelain, kommando, tider, returkode, resultatfiler, SHA-ene til taggene og sha256 for PREREG-
 # og MANUS-fila). Så: commit av resultat og metafil, push, speil. Stopper hele kjøringen (ingen neste del) hvis en del feiler, hvis en SPORET fil er
@@ -45,7 +45,7 @@ kommando() {  # skriver skriptet og argumentene for en del, ett ord per linje
     H1) printf '%s\n' eval/dev/kjor_dev.py --splitt test --prereg-id "$ID" --per-dialekt 60 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0013 ;;
     H2) printf '%s\n' eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --prereg-id "$ID" --mal-person 300 --mal-sted 200 --maks-timer 4 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0014 ;;
     H3) printf '%s\n' eval/dev/kjor_personvern_dev.py --splitt test --prereg-id "$ID" --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015 ;;
-    H4) printf '%s\n' kalibrering/kjor_h4.py --prereg-id "$ID" ;;
+    H4) printf '%s\n' kalibrering/kjor_h4.py --prereg-id "$ID" --opptak /Volumes/Vault/arkivklarering/lyd/h4 ;;
   esac
 }
 
@@ -59,7 +59,7 @@ rent_eller_stopp() {
 }
 
 kode_uendret_eller_stopp() {
-  local TAGG="${KLAR_KODETAGG:-testkjoring-v1}"
+  local TAGG="${KLAR_KODETAGG:-testkjoring-v2}"
   if ! git rev-parse -q --verify "refs/tags/$TAGG^{commit}" >/dev/null; then
     echo "FEIL: taggen $TAGG finnes ikke; kan ikke vise at koden er uendret. Kjører ikke." >&2
     exit 5
@@ -111,14 +111,16 @@ for d in "${DELER[@]}"; do
   export META SHA START SLUTT RC KMD PRE MAN RES DEL_NAVN="$d" NYE
   export TAG_PREREG="$(git rev-parse -q --verify 'refs/tags/prereg-v1^{commit}' || echo mangler)"
   export TAG_H4="$(git rev-parse -q --verify 'refs/tags/h4-script-v2^{commit}' || echo mangler)"
-  export TAG_KODE="$(git rev-parse -q --verify "refs/tags/${KLAR_KODETAGG:-testkjoring-v1}^{commit}" || echo mangler)"
+  export TAG_KODE="$(git rev-parse -q --verify "refs/tags/${KLAR_KODETAGG:-testkjoring-v2}^{commit}" || echo mangler)"
+  export TAG_KODE_NAVN="${KLAR_KODETAGG:-testkjoring-v2}"
+  export TAG_KODE_V1="$(git rev-parse -q --verify 'refs/tags/testkjoring-v1^{commit}' || echo mangler)"
   export SHA_PRE="$(shasum -a 256 "$PRE" | cut -d' ' -f1)" SHA_MAN="$(shasum -a 256 "$MAN" | cut -d' ' -f1)"
   "$PY" - <<'PYEOF'
 import json, os
 e = os.environ
 ut = {"del": e["DEL_NAVN"], "commit": e["SHA"], "git_status_porcelain_ved_start": [], "kommando": e["KMD"], "start_utc": e["START"], "slutt_utc": e["SLUTT"],
       "returkode": int(e["RC"]), "resultatfil": e["RES"] or None, "nye_filer": [x for x in e["NYE"].split("\n") if x],
-      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"], "tag_testkjoring_v1": e["TAG_KODE"], "kode_uendret_siden_testkjoring_v1": True,
+      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"], "tag_testkjoring": {"navn": e["TAG_KODE_NAVN"], "commit": e["TAG_KODE"]}, "tag_testkjoring_v1": e["TAG_KODE_V1"], "kode_uendret_siden_tagg": True,
       "preregistrering": {"fil": e["PRE"], "sha256": e["SHA_PRE"]}, "manus": {"fil": e["MAN"], "sha256": e["SHA_MAN"]}}
 open(e["META"], "w", encoding="utf-8").write(json.dumps(ut, ensure_ascii=False, indent=2) + "\n")
 print(e["META"])
diff --git a/scripts/rigg_manus.py b/scripts/rigg_manus.py
index fe5c9dd..956e1cc 100644
--- a/scripts/rigg_manus.py
+++ b/scripts/rigg_manus.py
@@ -1,45 +1,51 @@
 #!/usr/bin/env python3
-"""Starter norsk-tales kalibreringsrigg (lokal nettleserserver for innlesing) med arkivklarerings testmanus KLAR-MANUS-0002 (H4 i KLAR-PREREG-0001).
+"""Starter H4-innleseren (KLAR-ADR-0018) med arkivklarerings testmanus KLAR-MANUS-0002 (H4 i KLAR-PREREG-0001).
 
-norsk-tale er bare en referanse (KLAR-ADR-0001): riggen er et eksternt verktøy som brukes fra sin egen katalog
-(NORSK_TALE, standard ~/dev/norsk-tale) og kopieres ikke hit. Dette skriptet bytter bare ut manusfila og peker opptaksmappen
-til Vault. Lyd fra innlesingen ligger kun på Vault og går aldri i git (ADR-0007).
+Innleseren er en egen modus uten noe resultat: ingen transkripsjon, flagg, poeng, rapport eller eksport vises eller finnes som rute
+(`arkivklarering/h4_innlesing.py`). Den bygger på norsk-tales kalibreringsrigg, men bare når riggen står på den låste commiten med de låste
+filene (ellers stopper den). Lyd fra innlesingen ligger kun på Vault under /Volumes/Vault/arkivklarering/lyd/h4/ og går aldri i git eller sky
+(ADR-0007). `kalibrering/kjor_h4.py --opptak /Volumes/Vault/arkivklarering/lyd/h4` leser opptakene (scripts/kjor_testdel.sh sender det).
 
-    source scripts/miljo.sh && .venv/bin/python scripts/rigg_manus.py          # starter riggen; åpne URL-en som skrives ut
-    .venv/bin/python scripts/rigg_manus.py --tor                                # bare kontroller at manus og rigg laster
+    source scripts/miljo.sh && .venv/bin/python scripts/rigg_manus.py          # starter innleseren; åpne URL-en som skrives ut
+    .venv/bin/python scripts/rigg_manus.py --tor                                # bare kontroller manus, rigglås og opptaksmappe
 
-I riggen: velg målform og region (dialektfeltet), modus «dialekt» leser bare setningene med dialektutvalg=ja, modus «fullt»
-leser alle 156. Skriptet leser bare teksten som skal leses opp; det kjører ingenting gjennom rørledningen (testmanuset er sperret der til preregistreringen er registrert). Opptakene havner under /Volumes/Vault/arkivklarering/lyd/menneske/<runde>/ som 16 kHz mono wav.
+Skriptet leser bare teksten som skal leses opp; det kjører ingenting gjennom rørledningen (testmanuset er sperret der til preregistreringen er
+registrert). Innlesing til 16 kHz mono wav: `<runde>/opptak/<manus-id>.wav`, med `runde.json` og `opptakslogg.jsonl` (id, tidspunkt, forsøk, grunn).
 """
 import glob
-import os
 import pathlib
 import re
 import sys
 
 REPO = pathlib.Path(__file__).resolve().parent.parent
-NORSK_TALE = pathlib.Path(os.environ.get("NORSK_TALE", "~/dev/norsk-tale")).expanduser()
-OPPTAK = "/Volumes/Vault/arkivklarering/lyd/menneske"
+sys.path.insert(0, str(REPO))
+
+
+def siste_manus():
+    return max(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")), key=lambda p: tuple(int(x) for x in re.search(r"_v(\d+(?:\.\d+)*)_", p).group(1).split(".")))  # versjonssortering
 
 
 def main(argv=None):
+    from arkivklarering import h4_innlesing
     from arkivklarering.miljo import krev_vault_miljo
     krev_vault_miljo()
     argv = list(sys.argv[1:] if argv is None else argv)
-    tor = "--tor" in argv
-    argv = [a for a in argv if a != "--tor"]
-    manus = max(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")), key=lambda p: tuple(int(x) for x in re.search(r"_v(\d+(?:\.\d+)*)_", p).group(1).split(".")))  # versjonssortering
-    for d in ("kalibrering", "kjerne", "lytter"):
-        sys.path.insert(0, str(NORSK_TALE / d))
-    import rigg  # norsk-tale/kalibrering/rigg.py
-
-    rigg.MANUS = pathlib.Path(manus)
-    pathlib.Path(OPPTAK).mkdir(parents=True, exist_ok=True)
-    if tor:
-        r = rigg.Rigg(OPPTAK, {"modellvalg": None, "modell": None, "whisper": None})
-        print(f"manus: {manus}\n{len(r.manus)} setninger, {sum(1 for s in r.manus if s['dialektutvalg'])} med dialektutvalg; opptak: {r.rot}")
+    if any(a not in ("--tor",) for a in argv):
+        sys.exit("bruk: rigg_manus.py [--tor]  (opptaksmappen er fast: " + str(h4_innlesing.H4_ROT) + ")")
+    manus = siste_manus()
+    try:
+        lås = h4_innlesing.kontroller_rigg()
+    except h4_innlesing.RiggFeil as e:
+        sys.exit(str(e))
+    if argv:
+        rigg = h4_innlesing.last_rigg()
+        rigg.MANUS = pathlib.Path(manus)
+        H4Rigg, _ = h4_innlesing.lag_klasser(rigg)
+        r = H4Rigg(h4_innlesing.H4_ROT)
+        print(f"manus: {manus}\n{len(r.manus)} setninger, {sum(1 for s in r.manus if s['dialektutvalg'])} med dialektutvalg; opptak: {r.rot}\n"
+              f"rigg: norsk-tale commit {lås['norsk_tale_commit']}, {len(lås['filer'])} filer verifisert (sha256)\ninstruks: {h4_innlesing.INSTRUKS}")
         return 0
-    return rigg.main(["--opptak", OPPTAK, *argv])
+    return h4_innlesing.start(manus)
 
 
 if __name__ == "__main__":
diff --git a/tests/test_kjor_testdel.py b/tests/test_kjor_testdel.py
index 73224dc..d93293f 100644
--- a/tests/test_kjor_testdel.py
+++ b/tests/test_kjor_testdel.py
@@ -44,6 +44,7 @@ def lag_repo(tmp_path):
     git(r, "tag", "prereg-v1")
     git(r, "tag", "h4-script-v2")
     git(r, "tag", "testkjoring-v1")
+    git(r, "tag", "testkjoring-v2")
     bart = tmp_path / "origin.git"
     subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(bart)], check=True)
     git(r, "remote", "add", "origin", str(bart))
@@ -83,10 +84,10 @@ def test_en_del_committer_pusher_og_speiler_med_meta_ved_siden_av_resultatet(tmp
     start = git(r, "rev-parse", "HEAD")
     p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
     assert p.returncode == 0, p.stderr
-    assert kjort(r) == ["h4 --prereg-id KLAR-PREREG-0001".replace("h4", "kjor_h4")]
+    assert kjort(r) == ["kjor_h4 --prereg-id KLAR-PREREG-0001 --opptak /Volumes/Vault/arkivklarering/lyd/h4"]
     d = json.loads((r / "docs" / "KLAR-EVAL-kjor_h4_v1.0_2026-10-27_kjoring_meta.json").read_text())
     assert d["commit"] == start and d["git_status_porcelain_ved_start"] == [] and d["returkode"] == 0 and d["del"] == "H4"
-    assert d["tag_testkjoring_v1"] == start and d["kode_uendret_siden_testkjoring_v1"] is True
+    assert d["tag_testkjoring"] == {"navn": "testkjoring-v2", "commit": start} and d["tag_testkjoring_v1"] == start and d["kode_uendret_siden_tagg"] is True
     assert d["tag_prereg_v1"] == start == d["tag_h4_script_v2"] and d["preregistrering"]["fil"].endswith("_v1.10_2026-10-27.md")  # versjonssortering
     assert d["resultatfil"] == "docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27.json"
     assert git(r, "status", "--porcelain") == "" and git(r, "rev-parse", "HEAD") != start
@@ -103,7 +104,7 @@ def test_to_kjoringer_etter_hverandre_hver_med_egen_commit_push_og_speil(tmp_pat
     assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord", "kjor_personvern_dev", "kjor_h4"]
     assert "--datasett npsc --splitt test --prereg-id KLAR-PREREG-0001 --mal-person 300 --mal-sted 200 --maks-timer 4 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0014" in kjort(r)[1]
     assert kjort(r)[0].endswith("--per-dialekt 60 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0013")
-    assert kjort(r)[2].endswith("--ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015") and kjort(r)[3].endswith("kjor_h4 --prereg-id KLAR-PREREG-0001")
+    assert kjort(r)[2].endswith("--ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015") and kjort(r)[3].endswith("kjor_h4 --prereg-id KLAR-PREREG-0001 --opptak /Volumes/Vault/arkivklarering/lyd/h4")
     log = git(r, "log", "--format=%H %s", f"{start}..HEAD").splitlines()[::-1]
     assert [l.split(" ", 1)[1][:10] for l in log] == [f"Testdel H{i}" for i in (1, 2, 3, 4)]
     metas = [json.loads(p_.read_text()) for p_ in sorted((r / "docs").glob("*kjoring_meta.json"))]
@@ -162,7 +163,7 @@ def test_resultatfiler_og_andre_filtyper_under_eval_tillates(tmp_path):
 
 def test_manglende_tagg_stopper(tmp_path):
     r, bart = lag_repo(tmp_path)
-    git(r, "tag", "-d", "testkjoring-v1")
+    git(r, "tag", "-d", "testkjoring-v2")
     p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
     assert p.returncode == 5 and "finnes ikke" in p.stderr and kjort(r) == []
 
@@ -171,7 +172,7 @@ def test_to_testdeler_etter_hverandre_med_kodesjekk_for_hver(tmp_path):
     r, bart = lag_repo(tmp_path)
     p1 = kjor(r, "H1", "--prereg-id", "KLAR-PREREG-0001")
     assert p1.returncode == 0, p1.stderr
-    assert git(r, "rev-parse", "HEAD") != git(r, "rev-parse", "testkjoring-v1")  # HEAD har flyttet seg (resultat-commit), koden ikke
+    assert git(r, "rev-parse", "HEAD") != git(r, "rev-parse", "testkjoring-v2")  # HEAD har flyttet seg (resultat-commit), koden ikke
     p2 = kjor(r, "H2", "--prereg-id", "KLAR-PREREG-0001")
     assert p2.returncode == 0, p2.stderr
     assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord"]
```
14. **AV-20: Testdelene H1–H3 kjøres før H4-innlesingen, motsatt av rekkefølgen i PREREG, fordi innleseren feilet.** Se `KLAR-LOG-0003` (AV-19, AV-20) og `KLAR-LOG-0001` (v1.26; samme oppføring i nyeste v1.48). Beslutning av eier 2026-10-27.
15. **AV-22: H4-innleseren endret etter registrering og før datainnsamling.** H4-innleseren endret etter registrering og før datainnsamling (testopptak i mikrofonsjekken fjernet, banner, statuslinje, bekreftelse ved avslutning, hendelseslogg). H4 lest inn fra grenen h4-fiks, tag `h4-rigg-v3` `5a5a58671b2eea22cc2805787735332384d732a9` (tag-objekt `918f1fd414759294e78d062ed315547f9647e330`, opprettet 2026-10-27 09:54:43 +01:00), commit pushet til grenen 2026-10-27 09:54:17 +01:00 (lokal reflog for `origin/h4-fiks`, ikke uavhengig etterprøvbart), OTS-stempel sendt 2026-10-27 08:54:58Z–08:55:09Z (fem filer: HEAD-fil, ADR-0018 v1.1 (i git-historikken), `h4_innlesing.py`, `h4_side.html`, `scripts/rigg_manus.py`; `docs/stempler/`), Bitcoin-bekreftet, alle fem: tidligste attestasjon i blokk 973377 (2026-10-27T09:21:20Z), ytterligere attestasjoner i blokk 973378 (09:37:13Z) og 973384 (10:53:10Z). Første opptak: ikke lest inn ennå (`serverlogg.jsonl` har ingen `opptak_lagret`; innleseren er startet og har stoppet av tidsavbrudd uten runde). Riggkoden er byte-identisk med `testkjoring-v3` `68512e8ab0aa69fe217f6d0f2574c40380147e47` (tag-objekt `44a2081fd9bd9bd9becabf257203359064fb0ec2`; `git diff --quiet h4-rigg-v3 testkjoring-v3 -- arkivklarering/h4_innlesing.py arkivklarering/h4_side.html scripts/rigg_manus.py` gir 0; kontrollert også av uavhengig subagent). `scripts/kjor_testdel.sh` kontrollerer nå `testkjoring-v3` (v1 og v2 beholdt), som AV-18 gjorde for v2. Endringen berører innsamlingsverktøyet, ikke analysen eller tersklene. Se `KLAR-LOG-0003` (AV-22) og `KLAR-LOG-0001` (v1.30).
16. **AV-23: sha256 for testdataene ført etter H1-start.** sha256 for testdataene (13 filer) ble ført 2026-10-27 etter at H1 startet (`kjor_dev.py` 08:42:54 +01:00 = 07:42:54Z). Dataenes identitet er likevel fastlagt: alle 13 er byte-identiske med de offentlige, innholdsadresserte HF-revisjonene `Sprakbanken/nb_samtale@1c70281`, `NbAiLab/norne@1ca12d4` og `NbAiLab/NPSC@e906435` (LFS-oid eller git-blob), ført i LOG v1.27 (i git-historikken), commit `279f301` (committet 08:42:35; push 08:42:37 +01:00 ifølge lokal reflog, ikke uavhengig etterprøvbart; GitHub Events API viser den ikke; ikke OTS-stemplet). Hashfila ble skrevet 09:27:56 +01:00 (08:27:56Z) og stemplet; stempelet er Bitcoin-bekreftet i blokk 973374 (2026-10-27T08:44:17Z), dvs. etter H1-start og før H2-start. Hashfil (KLAR-ARK-0007, sha256 `8ac910b16ccbc7b91481f02272e48c051297ee11900bae4d6d00a936a04fb91c`): `docs/KLAR-ARK-0007_arkivklarering_testdata-sha256_v1.0_2026-10-27.txt`, med .ots: `docs/stempler/KLAR-ARK-0007_arkivklarering_testdata-sha256_v1.0_2026-10-27.txt.8ac910b16ccb.ots`. Se `KLAR-LOG-0003` (AV-23) og `KLAR-LOG-0001` (v1.30).
17. **AV-24: primærintervall for H3.** PREREG v1.8 (i git-historikken) (linje 166) nevner både Wilson og bootstrap over setninger for H3 uten å rangere dem. Eier beslutter 2026-10-27: Wilson er primær for H3, bootstrap over setninger rapporteres som sensitivitetsanalyse. Beslutningen er tatt etter at resultatene var kjent, og går i retning av den mer konservative klassifiseringen (H3d recall: ikke klart, Wilson-grense 0,949 < 0,95). Begge intervallene står i EVAL-0015 v1.2 (i git-historikken) (samme tall og klassifisering i v1.3). Se `KLAR-LOG-0003` (AV-24) og `KLAR-LOG-0001` (v1.31).
18. **AV-25: inaVAMOS brukes ikke lenger; H4 med inaSpeechSegmenter.** inaVAMOS (Pantagruel Research-only License; art. 1 begrenser lisenstakere, art. 3 forbyr bruk i kommersiell aktivitet) ble brukt i H1 og H2 og i DEV-arbeidet. EcoDecos dekning under lisensen er uavklart. Fra 2026-10-27 brukes den ikke. H4 kjøres med inaSpeechSegmenter (ADR-0019, tag testkjoring-v4), besluttet før noen H4-data er sett. H1 og H2 står som preregistrert. Merge-commit `40f0cbde6236fb96e90add4dc52d899b6c6bd80e` (inaseg-erstatning), kodetagg `testkjoring-v4` `3e0eead96b9238d26c5bad16a5b8b665b4341ecb` (tag-objekt `22b81d674770eef3da710d9f50ba17bb1ec60970`; `kjor_testdel.sh` kontrollerer den, v1–v3 beholdt); riggfilene er byte-identiske med `h4-rigg-v3` (`git diff --quiet h4-rigg-v3 testkjoring-v4 -- arkivklarering/h4_innlesing.py arkivklarering/h4_side.html scripts/rigg_manus.py` gir 0). `kjor_testdel.sh H4` setter `ARKIVKLARERING_SEGMENTERING=inaseg` og fører segmenteringsloggen i `kjoring_meta`; H1–H3-kommandoene er uendret. Kodeendringer før taggen: kjørervalg i `segment.py`, `segment_inaseg.py` med logg, miljøvariablene `ARKIVKLARERING_CACHE_SUFFIKS` og `ARKIVKLARERING_ETIKETT_TEST` i `kjor_flaggoverlevelse_ord.py` og `kjor_dev.py` (standardverdier gir uendret oppførsel). Vektlisensen for inaSpeechSegmenter er uklar (ADR-0019 v1.0 (i git-historikken)); ingen NC-vilkår er funnet. Eiers beslutning 2026-10-27. Se `KLAR-LOG-0003` (AV-25) og `KLAR-LOG-0001` (v1.34).
19. **AV-26: inaSpeechSegmenter er standard segmentering; inaVAMOS valgfritt tillegg.** inaSpeechSegmenter er standard segmentering i CLI, `arkivklarering/segment.py` og `eval/dev/felles.py` (miljøvariabelen ARKIVKLARERING_SEGMENTERING: inaseg standard, inavamos valgfritt); inaVAMOS er flyttet fra kjerneavhengighet til det valgfrie tillegget `reproduksjon-h1h2` (Pantagruel Research-only License; bare forskning). `scripts/kjor_testdel.sh` setter inavamos for H1/H2 (reproduksjon av de preregistrerte kjøringene) og inaseg for H4; reproduksjonsskriptene setter inavamos der de sammenligner mot lagrede inaVAMOS-resultater. Ny kodetagg `testkjoring-v5` (commit 076bb8d50906293a9bbe7c4a26f88da0150ce1ed, tag-objekt f1b0b1edf52c9654f472e5af4d79c1bc07cdc174); `testkjoring-v4` og tidligere beholdt; riggfilene er fortsatt byte-identiske med `h4-rigg-v3`. Endringen berører ikke H1–H3-resultatene eller tersklene; den følger av AV-25. Eiers beslutning 2026-10-27. Se `KLAR-LOG-0003` (AV-26) og `KLAR-LOG-0001` (v1.36).
20. **AV-27: H4 gjennomføres ikke i v1.0.** H4 gjennomføres ikke i v1.0 (Eiriks beslutning 2026-10-27, før noen H4-data er samlet inn). Testmanuset og mønstrene i personvernmotoren er laget av samme forfatter, og målingen ville hatt én leser, så den ville ikke gitt ekstern gyldighet. Ekstern test på spontan dialekttale utenfor NB-Whispers treningsdata gjøres i v1.1 (KLAR-PREREG-0003, NB Tale modul 3). Kategoriene uten naturlige forekomster i H1–H3 er ikke målt på tale i v1.0. Eiriks beslutning 2026-10-27 (A1 i `KLAR-ARK-0008` v1.3 (i git-historikken)). H4/EVAL-0009 rapporteres ikke, og tersklene for H4 er ikke prøvd; H1–H3 og tersklene deres er uendret. Se `KLAR-LOG-0003` (AV-27) og `KLAR-LOG-0001` (v1.41).
21. **AV-28: kodeendringer etter `testkjoring-v5`; ny kodetagg `testkjoring-v6`.** Cache-stier per segmentering (`<navn>_inaseg.jsonl`/`<navn>_inavamos.jsonl`; eldre cacher uten suffiks er laget med inaVAMOS og leses bare med `inavamos`), datarot `ARKIVKLARERING_DATA` med standard uten `/Volumes/Vault` når Vault ikke er montert, og tester som går i rent miljø, i commit `57dedaf77113300dc1dcbc64f4e5847712b1fc7c`. Ny kodetagg `testkjoring-v6` (commit `57dedaf77113300dc1dcbc64f4e5847712b1fc7c`, tag-objekt `33338900d9079d17355e470bb6517ca5c60cdeb3`); `testkjoring-v1`–`v5` beholdt; riggfilene er byte-identiske med `h4-rigg-v3`. Ingen utregning for H1–H3 er endret, bare stier og miljø: `git diff testkjoring-v5 testkjoring-v6 -- scripts/rapporter_intervaller.py` er tom, og i `eval/dev` er bare stikonstanter, valg av cache-filnavn (`felles.cache_sti`), en stopp ved manglende cache i en diagnose, en tom-verdi-regel for `ARKIVKLARERING_EVALDATA`, docstringer og kommentarer endret; WER, flaggscoring, Wilson, utvalg, bootstrap og tersklene er uendret. Endringene er gjort etter H1–H3 og berører ikke resultatene. Se `KLAR-LOG-0003` (AV-28) og `KLAR-LOG-0001` (v1.42).
22. **AV-29: KLAR-MANUS-0002 v1.2 → v1.3 og KLAR-MANUS-0001 v1.1 → v1.2 (telefonnumre).** KLAR-MANUS-0002 v1.2 → v1.3 og KLAR-MANUS-0001 v1.1 (i git-historikken) → v1.2 før repoet publiseres med historikk. Kontroll mot Nkoms liste over nummerserier (KLAR-KILDE-0001, NK-rader) viste at sju av tretten telefonnumre lå i serier Nkom har tildelt en tilbyder og dermed kan tilhøre en abonnent; de øvrige lå i ledige eller blokkerte serier. Alle er byttet til numre i Nkoms serie for TV- og filmproduksjon, 68 05 00 00–68 05 99 99 (blokkert for ordinær bruk). Setningene er ellers uendret. sha256 MANUS-0002: `9a3d12d1e2438b09f9fcb6aa43300ace406888732d058e3cbabf70cb0ad963b1` (v1.2, registrert) → `d71b5b138279f19b116f6f207cb0d1e586b1354d31c2ccb0fe044aaa03ff3003` (v1.3); MANUS-0001: `9857f82c526e550591aa6282392c3247600cbf983ade5af1c46d63c572cc3ee8` → `085e72c9f38b189eb5d66101660ea96f9ee75937d20a93b749a2bdccad443a66`. De gamle versjonene er fjernet fra arbeidstreet og ligger i git-historikken (som numrene, i commitene fra 26.10). H4 gjennomføres ikke i v1.0 (AV-27), så ingen kjørt test bruker MANUS-0002. Hypotese, utvalg, analyse og terskel er uendret. Sha256 for den registrerte v1.2 i planen over (Sekundært. H4) står uendret; sha256 for v1.3 og v1.2 er låst i `tests/test_manus.py`. Se `KLAR-LOG-0003` (AV-29) og `KLAR-LOG-0001` (v1.43).
23. **AV-30: kodetaggene `testkjoring-v7` og `testkjoring-v8`.** Kodetaggene `testkjoring-v7` (`9ded8d8…`, versjon 1.0.0, testdata med fiktive telefonnumre (AV-29), kodesjekk) og `testkjoring-v8` (0224d6db3e9d6900e6f65d4662466e6345b4c17b: VTT-merknaden om musikk under tale rettet etter ADR-0019) etter `testkjoring-v6`. Ingen analysekode for H1–H3 er endret i utregning; riggfilene er byte-identiske med `h4-rigg-v3`. `testkjoring-v7` er commit `9ded8d8442753f7ae6677e42207bf12165024bef` (tag-objekt `4c5ff2149730aaffa876d0499140273736526e8d`); `testkjoring-v8` er commit 0224d6db3e9d6900e6f65d4662466e6345b4c17b. I `testkjoring-v8` er bare `FORSLAG` i `arkivklarering/eksport.py` (NOTE-linjen i WebVTT og `merknad` i `segments.json`), taggen i `scripts/kjor_testdel.sh`, versjonssorteringen av kilderegisteret i `scripts/sjekk_kilder.py` og testene av dem endret, og utenfor kodestiene `_merknad` i `modeller.lock.json` (modellstien løses mot datarota); `git diff testkjoring-v6 testkjoring-v7 -- scripts/rapporter_intervaller.py eval` er tom, og ingen fil under `eval/` er endret for `testkjoring-v8`. WER, flaggscoring, Wilson, utvalg, bootstrap og tersklene er uendret. Endringene er gjort etter H1–H3 og berører ikke resultatene. Se `KLAR-LOG-0003` (AV-30) og `KLAR-LOG-0001` (v1.44).
24. **AV-31: regelen for H4-tersklene i den registrerte teksten stemmer ikke med tabellen (person og sted).** Den registrerte teksten (v1.8; linje 76 i denne versjonen, uendret) sier: «Terskelen er det syntetiske tallet minus 0,15 til 0,35 (mer for kategorier med lite n og for tall som er sårbare for uttale), rundet til nærmeste 0,05.» Tabellen rett over (linje 63–64) har person 18/26 (0,69) med terskel ≥ 0,60 (differanse −0,09) og sted 33/40 (0,82) med terskel ≥ 0,70 (−0,12); begge differansene er mindre enn 0,15, så regelen ville gitt lavere terskler (person 0,35–0,55, sted 0,45–0,65). For de andre ti kategoriene ligger differansen mellom −0,16 og −0,33 (e-post har en egen, negativ terskel). Tersklene i tabellen er de registrerte og gjelder; verken teksten eller tabellen er endret. Ingen følger for resultatene: H4 gjennomføres ikke i v1.0 (AV-27), så ingen H4-terskel er prøvd, og H1–H3 bruker ikke disse tersklene. Funnet av den uavhengige publiseringsporten, runde 2 (KLAR-LOG-0004, funn 26), 2026-10-28; ingen avvik dekket det før. Se `KLAR-LOG-0003` (AV-31) og `KLAR-LOG-0001` (v1.48).
25. **AV-32: kodetaggen `testkjoring-v9` (hjelpeteksten til `--ingen-ordtider`).** Etter `testkjoring-v8` er hjelpeteksten til `--ingen-ordtider` i `arkivklarering/cli.py:47` endret, og GT-generatoren er rettet (se nederst i punktet). Den sa «(-ml 1 -sow)», men koden ber om DTW-ordtidsstempler med `-nfa -dtw large.v3 -ojf` (`arkivklarering/transkriber.py:158` og `:178`), og `-ml 1 -sow` er forkastet (`arkivklarering/transkriber.py:156`; KLAR-ADR-0012 v1.4:28); DTW-ordtidene beholdes også for rålaget med `-nt` (KLAR-ADR-0017 v1.1:17). Ny tekst: «ikke be om DTW-ordtidsstempler (-nfa -dtw large.v3 -ojf); cuene får da whisper.cpps segmenttider, og union parer på cuenes tidsrom». Teksten vises bare i `--help`; oppførselen er uendret. Kodesjekken i `scripts/kjor_testdel.sh` er flyttet til `testkjoring-v9`, og `tests/test_kjor_testdel.py` er oppdatert etter samme mønster som for v8 (tag v9 i testrepoet, forventning v9, «manglende tagg»-testen sletter v9 mens v1–v8 finnes). Ingen analysekode er endret: ingen fil under `eval/`, ikke `scripts/rapporter_intervaller.py` og ingen funksjon for WER, flaggscoring, Wilson, utvalg eller bootstrap. Riggfilene (`arkivklarering/h4_innlesing.py`, `arkivklarering/h4_side.html`, `scripts/rigg_manus.py`) er ikke endret og skal være byte-identiske med `h4-rigg-v3` (kontrolleres med `git diff --quiet h4-rigg-v3 testkjoring-v9 -- …` etter taggingen). `testkjoring-v9` er commit 951091e73651967b3a7a3b3aa8dbf2d38b03b660; `testkjoring-v1`–`v8` er beholdt. Funnet av den uavhengige publiseringsporten, runde 2 (KLAR-LOG-0004, funn 52), 2026-10-28. Se `KLAR-LOG-0003` (AV-32) og `KLAR-LOG-0001` (v1.48). I tillegg (ført etter runde 3 av porten, KLAR-LOG-0005, funn 8): `scripts/ground_truth.py` lister ikke lenger forrige versjon av KLAR-GT-0001 i dokumentlista, men én linje for fila selv (3 linjer lagt til; portfunn 66 i KLAR-LOG-0004), og `tests/test_ground_truth_wer.py` har den nye testen `test_dokumentlista_viser_ikke_forrige_gt_men_denne_fila`. GT-generatoren lager bare dokumentasjon; den er ikke analysekode.

26. **AV-33: kodetaggen `testkjoring-v10` (mekanisk pekersjekk).** Etter `testkjoring-v9` er to filer lagt til: `scripts/sjekk_pekere.py`, som kontrollerer at hver henvisning til en arkivnøkkel med versjon finnes i treet eller er merket «(i git-historikken)», at den finnes i treet eller i git-historikken, og at fil:linje-pekere viser til en linje som finnes (regelen i KLAR-ARK-0002 v1.6:25), og `tests/test_sjekk_pekere.py`, som kjører kontrollen på repoet. Kodesjekken i `scripts/kjor_testdel.sh` er flyttet til `testkjoring-v10`, og `tests/test_kjor_testdel.py` er oppdatert etter samme mønster som for v9. `git diff --stat testkjoring-v9 testkjoring-v10 -- arkivklarering kalibrering tests scripts` gir «4 files changed, 348 insertions(+), 8 deletions(-)» (commit `efce3f443ecbd27ecf72e067ffc71bb0c3391ae1`). Ingen analysekode er endret: ingen fil under `arkivklarering/` eller `eval/`, ikke `scripts/rapporter_intervaller.py` og ingen funksjon for WER, flaggscoring, Wilson, utvalg eller bootstrap.

27. **AV-34: A3 endret (offentlig repo fra rent tre, full historikk i tilgangsstyrt deponering).** Eiriks beslutning 2026-10-28: det offentlige repoet (`avalyset/arkivklarering-public`) har én commit med treet ved HEAD i det private repoet; hele git-historikken deponeres som `git bundle --all` på Zenodo med begrenset tilgang og tilgang på forespørsel, under AGPL-3.0-or-later. Begrunnelse: «så åpent som mulig, så lukket som nødvendig»; historikken har sju oppdiktede telefonnumre i tildelte nummerserier (AV-29), og omskriving ville brutt beviskjeden til denne preregistreringen og stemplene. Numrene publiseres ikke. Commit-SHA-ene som denne preregistreringen, `kjoring_meta`-filene, kodetaggene og stemplene viser til, finnes i den tilgangsstyrte historikken (DOI 10.5281/zenodo.23723450); KLAR-MANUS-0002 v1.2 (i git-historikken), som OSF-registreringen låser med sha256, kan etterprøves der. Ingen kode, data eller utregning er endret.
