# KLAR-EVAL-0008: Syntetisk kjedekalibrering (v1.4, rålag med -nt)

Versjon 1.5, 2026-10-28 (v1.5: pekere til versjoner som ikke er i treet er merket «(i git-historikken)», og pekere med linjenummer til forrige versjon av et dokument med ny versjon viser til den nye versjonen, samme linje; kontrollert med `scripts/sjekk_pekere.py`, 0 brudd (KLAR-LOG-0005, restfunn etter kontrollen); v1.4: bare to merknader under overskriften til vedlegg A (gjengivelsen selv er uendret): «før»-tallet for telefon er ulikt i tekst og tabell og kan ikke avgjøres mot lagrede data, og «n er 6 til 26» gjelder 6 til 20 per kategori og målform; tall, tabeller og vurdering er uendret; v1.3: bare dokumentasjon, AV-29: v1.1 («før -nt») er fjernet fra arbeidstreet fordi den inneholdt et telefonnummer i en serie Nkom har tildelt en tilbyder, og er gjengitt i vedlegg A nederst, ordrett bortsett fra at nummeret er erstattet med «[fiktivt nummer, byttet 2026-10-27, AV-29]» og at overskriftene er flyttet to nivåer ned; henvisningene til forrige versjon peker dit; tall, tabeller og vurdering er uendret fra v1.2). **DEV, ikke pilot.** Gjentatt etter at rålaget ble endret til `-nt` (ingen tidsstempeltokens; KLAR-ADR-0017, bakgrunn KLAR-EVAL-0011). **Forrige versjon (v1.1) er «før -nt» og står i vedlegg A.** Rålaget er kjørt på nytt fra rådata med `scripts/reproduser.sh` på commit `d75bc40` (kode som ved taggen `h4-script-v2`, se KLAR-LOG-0001); det normaliserte laget er gjenbrukt fra lagret utdata (modell-sha256 `0f2f66f2…` og parametere uendret, ingen `-nt`; gjenbruket er logget i kjøringen). Tallene er generert, vurderingen er skrevet for hånd.

Rådata: `KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.2_2026-10-27.json` (sha256 `6ac5081065a129dfa7c1992cf2383d2ebdbc2442e166656ba2e4eeeeb709128f`). Forrige versjon: `KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.1_2026-10-26.md` (i git-historikken) (sha256 `ef3d82abe487163ddcbef66dd6a39bad5ec65222b4dd3eca93df9694a6405cfa`, OTS-stemplet, KLAR-LOG-0002; fjernet fra arbeidstreet ved AV-29 og i git-historikken), gjengitt i vedlegg A; oppsett, utvalg, lisens og definisjoner står der og gjelder fortsatt.

## Før og etter -nt (generert av `scripts/lag_nt_versjoner.py`)

| konfigurasjon | kategori | før -nt | etter -nt |
|---|---|---|---|
| matchet | person | 18/26 | 18/26 |
| matchet | sted | 33/40 | 34/40 |
| matchet | dato | 14/14 | 14/14 |
| matchet | fødselsår | 16/18 | 15/18 |
| matchet | telefon | 12/14 | 12/14 |
| matchet | fødselsnummer | 10/12 | 10/12 |
| matchet | e-post | 0/12 | 0/12 |
| matchet | helse | 26/26 | 26/26 |
| matchet | økonomi | 19/22 | 19/22 |
| matchet | konflikt | 22/26 | 22/26 |
| matchet | religion | 12/16 | 12/16 |
| matchet | politikk | 16/18 | 16/18 |
| nn | person | 20/26 | 20/26 |
| nn | sted | 33/40 | 33/40 |
| nn | dato | 14/14 | 14/14 |
| nn | fødselsår | 16/18 | 16/18 |
| nn | telefon | 12/14 | 12/14 |
| nn | fødselsnummer | 10/12 | 10/12 |
| nn | e-post | 0/12 | 0/12 |
| nn | helse | 26/26 | 26/26 |
| nn | økonomi | 19/22 | 20/22 |
| nn | konflikt | 22/26 | 22/26 |
| nn | religion | 12/16 | 12/16 |
| nn | politikk | 16/18 | 16/18 |

## Vurdering (håndført)

- **Nesten uendret:** konfigurasjon «matchet»: sted 33/40 → 34/40, fødselsår 16/18 → 15/18; konfigurasjon `nn`: økonomi 19/22 → 20/22. Resten er identisk. Endringene er enkeltelementer.
- **H4-tørrtesten** (tabell i eget avsnitt i `eval/dev/h4_torrtest_justeringsmanus_2026-10-27.md`) gir samme vurdering som før: alle tolv kategorier består tersklene, e-post er fortsatt 0/12 (forventet negativt).
- Tersklene for H4 i KLAR-PREREG-0001 er satt fra v1.1-tallene og er ikke endret. Det syntetiske grunnlaget er en TTS-stemme og sier ikke noe om menneskestemmer.

## Vedlegg A: KLAR-EVAL-0008 v1.1 («før -nt»), gjengitt

Ordrett fra `KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.1_2026-10-26.md` (i git-historikken) (sha256 over), med to endringer: telefonnummeret i punktet «Rettelse underveis» er erstattet med «[fiktivt nummer, byttet 2026-10-27, AV-29]» (AV-29), og overskriftene er flyttet to nivåer ned. Fila selv ligger i git-historikken (t.o.m. a583a28). **Merknader (v1.4, 2026-10-28; ikke del av gjengivelsen):** (1) «Rettelse underveis» sier at den første evalueringen ga flagg-treff for telefon «4 av 14», mens tabellen «Resultat, union …» har 8/14 i kolonnen «før rettelsen». Den første evalueringen er ikke lagret: JSON-fila fra v1.0 (`KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.0_2026-10-26.json` (i git-historikken), i git-historikken fra commit `9ff2d1a`) har bare tallene etter rettelsen (konfigurasjon matchet, union, begge målformer: telefon 12/14 med tekst-treff 14/14, fødselsnummer 10/12 med tekst-treff 10/12), og de stemmer med kolonnen «etter rettelsen». Hvilket «før»-tall for telefon som er riktig, kan derfor ikke avgjøres; begge er ikke verifisert. Fødselsnummer «4 av 12» er likt i tekst og tabell, men er heller ikke lagret. (2) «n er 6 til 26 elementer per kategori og målform» stemmer ikke: JSON v1.0 og v1.2 gir n = 6 til 20 per kategori og målform (union, matchet); 26 er summen over begge målformer (person, 13 + 13).

### KLAR-EVAL-0008: Syntetisk kjedekalibrering

**SYNTETISK – kjede og flagglogikk, ikke talekvalitet.**

Versjon 1.1, 2026-10-26 (v1.1: bare navnet på manusfila er rettet; tallene er uendret fra v1.0. Manuset `KLAR-MANUS-0001_arkivklarering_kategorier_v1.0_2026-10-26.tsv` som ble kjørt, heter nå `KLAR-MANUS-0001_arkivklarering_justeringsmanus_v1.1_2026-10-26.tsv` (i git-historikken) og er justeringsmanuset: mønstrene er justert mot det, så denne kjøringen er ikke en test). DEV. Tall generert av `eval/dev/kjor_syntetisk.py`; tolkning skrevet for hånd. Resultatene sier noe om om flaggkjeden (transkripsjon, mønstre, ordlister, union) virker, og ingenting om hvordan den virker på ekte tale: stemmen er macOS-TTS og leser alle setninger likt og tydelig.

#### Oppsett

- Manus: justeringsmanuset `KLAR-MANUS-0001` (156 setninger: 13 klasser × 6 setninger × bokmål og nynorsk), oppdiktede navn, fiktive tall med riktig format (fødselsnumre med bevisst ugyldig kontrollsiffer), reserverte eksempeldomener for e-post.
- Lyd: `say -v Nora` (nb_NO; **det finnes ingen nynorskstemme på maskinen**, så nynorske setninger leses med en bokmålsstemme og uttalen er ufullkommen), 16 kHz mono wav under `/Volumes/Vault/arkivklarering/lyd/syntetisk/`. Ingen runde gjennom høyttaler og mikrofon: norsk-tales rigg tar opp i nettleseren med en menneskelig leser og kan ikke kjøres uten.
- Rørledning: segmentering, rålag og normalisert lag (DTW-ordtidsstempler), personvernflagg på begge lag, union paret på ordspenn. To konfigurasjoner: **matchet** (språk etter manusets målform) og **nn** (`-l nn` for alle, slik rørledningen kjører). Modeller som i `KLAR-EVAL-0007`. Ett Whisper-kall per lag og språk i grupper på 40 filer; ingen krasj, ingen ressursvakt-utløsninger.
- Scoring: vendor `score.py` fra norsk-tale (`KLAR-ADR-0014`). Per målelement: **tekst-treff** (elementet står i transkripsjonen; tallord normaliseres til sifre) og **flagg-treff** (et flagg i samme kategori har et utdrag som dekker elementet). Målformfeil rapporteres separat og feller aldri elementet.
- **Rettelse underveis (kalibreringen virket).** Første evaluering ga lave flagg-treff for telefon (4 av 14) og fødselsnummer (4 av 12) selv om teksten var riktig transkribert (tekst-treff 14 og 10): Whisper skriver talte tall som «[fiktivt nummer, byttet 2026-10-27, AV-29]» (fire sifferpar skilt med komma) og «150 575 45 615», og mønstrene krevde ett bestemt mellomromsmønster. Nøkkelordene manglet bøyningsformer («mobbingen», «anmeldte», «sykehuset»). Mønstrene tillater nå skilletegn og validerer sifrene (8 siffer fra 2–9; 11 siffer med plausibel dato; ikke datoer eller årstallslister), og nøkkelord på fire bokstaver eller mer får bøyningsendelser (`personvern.py`, tester i `tests/test_personvern.py`). Resultatene under er **etter** rettelsen; «før» står i tabellen. Rettelsen er gjort på syntetiske data og endrer ikke person og sted (NorNE, NPSC).

#### Resultat, union (flagg-treff / målelementer; begge målformer summert), konfigurasjon matchet

| kategori | før rettelsen | etter rettelsen | tekst-treff (union) |
|---|---|---|---|
| person | 18/26 (0,69) | **18/26 (0,69)** | 18/26 (0,69) |
| sted | 33/40 (0,82) | **33/40 (0,82)** | 33/40 (0,82) |
| dato | 14/14 (1,00) | **14/14 (1,00)** | 13/14 (0,93) |
| fødselsår | 16/18 (0,89) | **16/18 (0,89)** | 18/18 (1,00) |
| telefon | 8/14 (0,57) | **12/14 (0,86)** | 14/14 (1,00) |
| fødselsnummer | 4/12 (0,33) | **10/12 (0,83)** | 10/12 (0,83) |
| e-post | 0/12 (0,00) | **0/12 (0,00)** | 0/12 (0,00) |
| helse | 24/26 (0,92) | **26/26 (1,00)** | 26/26 (1,00) |
| økonomi | 19/22 (0,86) | **19/22 (0,86)** | 20/22 (0,91) |
| konflikt | 17/26 (0,65) | **22/26 (0,85)** | 26/26 (1,00) |
| religion | 9/16 (0,56) | **12/16 (0,75)** | 16/16 (1,00) |
| politikk | 16/18 (0,89) | **16/18 (0,89)** | 18/18 (1,00) |
| **alle** | 178/244 (0,73) | **198/244 (0,81)** | 212/244 (0,87) |

#### Per lag og målform (alle elementer, etter rettelsen)

| lag | bokmål, matchet | nynorsk, matchet | bokmål, nn | nynorsk, nn |
|---|---|---|---|---|
| ra | flagg 77/123 (0,63) · tekst 96/123 (0,78) | flagg 68/121 (0,56) · tekst 89/121 (0,74) | flagg 78/123 (0,63) · tekst 96/123 (0,78) | flagg 70/121 (0,58) · tekst 92/121 (0,76) |
| normalisert | flagg 101/123 (0,82) · tekst 106/123 (0,86) | flagg 92/121 (0,76) · tekst 102/121 (0,84) | flagg 105/123 (0,85) · tekst 109/123 (0,89) | flagg 94/121 (0,78) · tekst 103/121 (0,85) |
| union | flagg 105/123 (0,85) · tekst 108/123 (0,88) | flagg 93/121 (0,77) · tekst 104/121 (0,86) | flagg 105/123 (0,85) · tekst 110/123 (0,89) | flagg 95/121 (0,79) · tekst 105/121 (0,87) |

#### Målformfeil (separat; antall setninger der utdata hadde motsatt målforms markører, av 78 per målform)

| lag og målform | matchet | nn |
|---|---|---|
| ra|nb | 2 | 14 |
| normalisert|nb | 2 | 5 |
| ra|nn | 0 | 0 |
| normalisert|nn | 5 | 4 |

#### Funn (håndført)

- **e-post: 0 av 12.** Whisper skriver ikke talte e-postadresser som adresser (teksten har ikke tegnet @), så ingen e-postgjenkjenning kan treffe. Dette er en kjent begrensning og står i preregistreringen som forventet negativt.
- **Navn: flaggene følger transkripsjonen.** Person og sted har flagg-treff lik tekst-treff; bommene skyldes stavefeil i transkripsjonen (for eksempel «Hauvold» for «Haugvold», «Dahlsegg» for «Dalsegg»), ikke flaggingen. Det er den uunngåelige begrensningen til en kjede som flagger transkribert tekst.
- **Rålaget alene** treffer dårligere enn normalisert lag (små bokstaver uten tegnsetting; tall skrevet som tallord i rålaget og som sifre i normalisert), og unionen er best eller lik (tabellen over). Det samsvarer med `KLAR-EVAL-0005` og `KLAR-EVAL-0007`.
- **Nøkkelord dekker ikke alle bøyninger og feiltranskripsjoner** (for eksempel «tildømt» i stedet for «dømt»): konflikt og religion har fortsatt bom der teksten er riktig. Ordlistene er korte og ikke validert mot noe gullsett.
- **Målformfeil** er flest i rålaget for bokmålssetninger i konfigurasjonen `nn`, som forventet når `-l nn` tvinges på bokmålstale; de feller ikke elementer.
- **n er 6 til 26 elementer per kategori og målform.** Tallene viser om kjeden virker, ikke hvor ofte. De er ikke et mål på kvalitet og brukes bare til å sette de forhåndsregistrerte tersklene for menneskeinnlest manus (`KLAR-PREREG-0001`, H4).

Rådata: `KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.0_2026-10-26.json` (i git-historikken) (bare tall; bom i union med `id`, `klasse` og `type`).
