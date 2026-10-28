# KLAR-EVAL-0006: Hvor mange personvernflagg overlever talegjenkjenningen (NB Samtale) (v1.2, rålag med -nt)

Versjon 1.2, 2026-10-27. **DEV, ikke pilot.** Gjentatt etter at rålaget ble endret til `-nt` (ingen tidsstempeltokens; KLAR-ADR-0017, bakgrunn KLAR-EVAL-0011). **Forrige versjon er beholdt uendret og er «før -nt».** Rålaget er kjørt på nytt fra rådata med `scripts/reproduser.sh` på commit `d75bc40` (kode som ved taggen `h4-script-v2`, se KLAR-LOG-0001); det normaliserte laget er gjenbrukt fra lagret utdata (modell-sha256 `0f2f66f2…` og parametere uendret, ingen `-nt`; gjenbruket er logget i kjøringen). Tallene er generert, vurderingen er skrevet for hånd.

Rådata: `KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.2_2026-10-27.json` (sha256 `9122c3b087567de9682e761b69c27616a1027be2072f480178d64c8d2f6d0d65`). Forrige versjon: `KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.1_2026-10-26.md` (beholdt uendret; oppsett, utvalg, lisens og definisjoner står der og gjelder fortsatt).

## Før og etter -nt (generert av `scripts/lag_nt_versjoner.py`)

| kategori | lag | målform | før -nt | etter -nt |
|---|---|---|---|---|
| person | ra | bokmål | 7/8 (0,875) | 7/8 (0,875) |
| person | ra | nynorsk | 5/9 (0,556) | 5/9 (0,556) |
| person | ra | **samlet** | 12/17 (0,706) | 12/17 (0,706) |
| person | normalisert | bokmål | 8/8 (1,000) | 8/8 (1,000) |
| person | normalisert | nynorsk | 5/9 (0,556) | 5/9 (0,556) |
| person | normalisert | **samlet** | 13/17 (0,765) | 13/17 (0,765) |
| person | union | bokmål | 8/8 (1,000) | 8/8 (1,000) |
| person | union | nynorsk | 6/9 (0,667) | 6/9 (0,667) |
| person | union | **samlet** | 14/17 (0,824) | 14/17 (0,824) |
| sted | ra | bokmål | 6/10 (0,600) | 8/10 (0,800) |
| sted | ra | nynorsk | 4/4 (1,000) | 4/4 (1,000) |
| sted | ra | **samlet** | 10/14 (0,714) | 12/14 (0,857) |
| sted | normalisert | bokmål | 10/10 (1,000) | 10/10 (1,000) |
| sted | normalisert | nynorsk | 3/4 (0,750) | 3/4 (0,750) |
| sted | normalisert | **samlet** | 13/14 (0,929) | 13/14 (0,929) |
| sted | union | bokmål | 10/10 (1,000) | 10/10 (1,000) |
| sted | union | nynorsk | 4/4 (1,000) | 4/4 (1,000) |
| sted | union | **samlet** | 14/14 (1,000) | 14/14 (1,000) |

## Vurdering (håndført)

- **Unionen er uendret** for både person (14/17) og sted (14/14), og det normaliserte laget er uendret (gjenbrukt).
- **Rålaget alene:** sted 10/14 → 12/14 (bokmål 6/10 → 8/10); person uendret (12/17). Forskjellen er to enkeltflagg (n er 17 person- og 14 stedsreferanser; ett flagg er 6 til 7 prosentpoeng) og kan ikke skilles fra tilfeldig variasjon med dette utvalget.
- Rålaget er fortsatt lavere enn det normaliserte laget alene for både person (0,706 mot 0,765) og sted (0,857 mot 0,929), men gapet er mindre for sted. Antallene er små.
- Kjøringen uten ordtider (v1.0-oppsettet, `…v1.0_2026-10-27.json`, sha256 `bcbb65b4…`) er også kjørt på nytt; den ligger i reproduksjonsmappen på Vault og er ikke tolket her.
