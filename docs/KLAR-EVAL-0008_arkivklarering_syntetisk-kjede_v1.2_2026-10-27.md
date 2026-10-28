# KLAR-EVAL-0008: Syntetisk kjedekalibrering (v1.2, rålag med -nt)

Versjon 1.2, 2026-10-27. **DEV, ikke pilot.** Gjentatt etter at rålaget ble endret til `-nt` (ingen tidsstempeltokens; KLAR-ADR-0017, bakgrunn KLAR-EVAL-0011). **Forrige versjon er beholdt uendret og er «før -nt».** Rålaget er kjørt på nytt fra rådata med `scripts/reproduser.sh` på commit `d75bc40` (kode som ved taggen `h4-script-v2`, se KLAR-LOG-0001); det normaliserte laget er gjenbrukt fra lagret utdata (modell-sha256 `0f2f66f2…` og parametere uendret, ingen `-nt`; gjenbruket er logget i kjøringen). Tallene er generert, vurderingen er skrevet for hånd.

Rådata: `KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.2_2026-10-27.json` (sha256 `6ac5081065a129dfa7c1992cf2383d2ebdbc2442e166656ba2e4eeeeb709128f`). Forrige versjon: `KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.1_2026-10-26.md` (beholdt uendret; oppsett, utvalg, lisens og definisjoner står der og gjelder fortsatt).

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
