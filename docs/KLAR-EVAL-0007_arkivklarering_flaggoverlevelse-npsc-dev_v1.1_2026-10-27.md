# KLAR-EVAL-0007: Flaggoverlevelse på NPSC (v1.1, rålag med -nt)

Versjon 1.1, 2026-10-27. **DEV, ikke pilot.** Gjentatt etter at rålaget ble endret til `-nt` (ingen tidsstempeltokens; KLAR-ADR-0017, bakgrunn KLAR-EVAL-0011). **Forrige versjon er beholdt uendret og er «før -nt».** Rålaget er kjørt på nytt fra rådata med `scripts/reproduser.sh` på commit `d75bc40` (kode som ved taggen `h4-script-v2`, se KLAR-LOG-0001); det normaliserte laget er gjenbrukt fra lagret utdata (modell-sha256 `0f2f66f2…` og parametere uendret, ingen `-nt`; gjenbruket er logget i kjøringen). Tallene er generert, vurderingen er skrevet for hånd.

Rådata: `KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.1_2026-10-27.json` (sha256 `8c17de499ef69eab7ba9bce3dec3005cc14c32a787b0782ebb45ef79d977fd1c`). Forrige versjon: `KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_2026-10-26.md` (beholdt uendret; oppsett, utvalg, lisens og definisjoner står der og gjelder fortsatt).

## Før og etter -nt (generert av `scripts/lag_nt_versjoner.py`)

| kategori | lag | målform | før -nt | etter -nt |
|---|---|---|---|---|
| person | ra | bokmål | 67/85 (0,788) | 68/85 (0,800) |
| person | ra | nynorsk | 43/65 (0,662) | 43/65 (0,662) |
| person | ra | **samlet** | 110/150 (0,733) | 111/150 (0,740) |
| person | normalisert | bokmål | 80/85 (0,941) | 80/85 (0,941) |
| person | normalisert | nynorsk | 52/65 (0,800) | 52/65 (0,800) |
| person | normalisert | **samlet** | 132/150 (0,880) | 132/150 (0,880) |
| person | union | bokmål | 83/85 (0,976) | 83/85 (0,976) |
| person | union | nynorsk | 56/65 (0,862) | 56/65 (0,862) |
| person | union | **samlet** | 139/150 (0,927) | 139/150 (0,927) |
| sted | ra | bokmål | 51/80 (0,637) | 51/80 (0,637) |
| sted | ra | nynorsk | 5/22 (0,227) | 5/22 (0,227) |
| sted | ra | **samlet** | 56/102 (0,549) | 56/102 (0,549) |
| sted | normalisert | bokmål | 74/80 (0,925) | 74/80 (0,925) |
| sted | normalisert | nynorsk | 18/22 (0,818) | 18/22 (0,818) |
| sted | normalisert | **samlet** | 92/102 (0,902) | 92/102 (0,902) |
| sted | union | bokmål | 74/80 (0,925) | 74/80 (0,925) |
| sted | union | nynorsk | 18/22 (0,818) | 18/22 (0,818) |
| sted | union | **samlet** | 92/102 (0,902) | 92/102 (0,902) |

## Vurdering (håndført)

- **Unionen er helt uendret** for alle fire gruppene (person 139/150, bokmål 83/85, nynorsk 56/65; sted 92/102, bokmål 74/80, nynorsk 18/22). DEV-grunnlaget for H2a–H2f endres dermed ikke.
- **Rålaget alene:** person bokmål 67/85 → 68/85 (samlet 0,733 → 0,740); sted uendret (56/102 = 0,549). Endringen er ett flagg.
- **Rålaget er fortsatt klart lavere enn det normaliserte laget alene** (person 0,740 mot 0,880, sted 0,549 mot 0,902), så kontrollsjekk K2 i KLAR-PREREG-0001 holder.
- NPSC-utvalget (934 segmenter) er langt mindre berørt av `-nt` enn NB Samtale-utvalget. Jeg har ikke undersøkt hvorfor (talestil og segmentlengde er ulike; ingen påstått årsak).
