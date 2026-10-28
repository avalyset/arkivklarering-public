# DEV-måling (2026-10-27, v1.1, rålag med -nt): WER på nb_samtale (validation), 60 segmenter

Gjentatt etter at rålaget ble endret til `-nt` (ingen tidsstempeltokens; KLAR-ADR-0017, bakgrunn KLAR-EVAL-0011). **Forrige versjon er beholdt uendret og er «før -nt».** Rålaget er kjørt på nytt fra rådata med `scripts/reproduser.sh` på commit `d75bc40` (kode som ved taggen `h4-script-v2`, se KLAR-LOG-0001); det normaliserte laget er gjenbrukt fra lagret utdata (modell-sha256 `0f2f66f2…` og parametere uendret, ingen `-nt`; gjenbruket er logget i kjøringen). Tallene er generert, vurderingen er skrevet for hånd.
Rådata: `KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.1_2026-10-27.json` (sha256 `8a45a9e4fa5659599f5eb64cafd5cb6247d9bfc42a4d0fb63d1b328df782a879`). Forrige versjon: `KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_2026-10-26.md`.

**DEV, ikke pilot. Ingen konklusjoner om pilotkvalitet.** 12 segmenter per dialektområde (e, n, sw, t, w), seed 20261026. Fasit: `orthographic`. Korpus-WER etter normalisering (små bokstaver, tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.

`ra` = NB-Whisper large verbatim, `normalisert` = NB-Whisper large (ikke verbatim). `nn` = `-l nn` for alle; `matchet` = språk etter fasitens skriftform. Rålaget skriver ut nøling og omtrent som sagt og scores likevel mot ortografisk fasit, så ra-tallene er ikke likestilt med normalisert lag.

| gruppe (n) | ra/nn | ra/matchet | normalisert/nn | normalisert/matchet |
|---|---|---|---|---|
| e (12) | 0.221 | 0.099 | 0.403 | 0.204 |
| n (12) | 0.311 | 0.100 | 0.599 | 0.419 |
| sw (12) | 0.297 | 0.238 | 0.500 | 0.460 |
| t (12) | 0.213 | 0.101 | 0.314 | 0.166 |
| w (12) | 0.181 | 0.142 | 0.423 | 0.400 |
| totalt (60) | 0.248 | 0.135 | 0.463 | 0.348 |
| skrift:bm (38) | 0.273 | 0.090 | 0.492 | 0.305 |
| skrift:nn (22) | 0.208 | 0.208 | 0.417 | 0.417 |

Segmenter uten noen tekst (tom hypotese), av 60: ra/nn: 0, ra/matchet: 0, normalisert/nn: 1, normalisert/matchet: 1

Modeller: ra: `nb-whisper-large-verbatim.ggml-model.bin` sha256 `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d`; normalisert: `nb-whisper-large.ggml-model.bin` sha256 `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76`


## Før og etter -nt (generert av `scripts/lag_nt_versjoner.py`)

| oppsett | gruppe | n | før -nt | etter -nt |
|---|---|---|---|---|
| ra/matchet | totalt | 60 | 0,250 | 0,135 |
| ra/matchet | skrift:bm | 38 | 0,264 | 0,090 |
| ra/matchet | skrift:nn | 22 | 0,228 | 0,208 |
| ra/nn | totalt | 60 | 0,317 | 0,248 |
| ra/nn | skrift:bm | 38 | 0,373 | 0,273 |
| ra/nn | skrift:nn | 22 | 0,228 | 0,208 |
| normalisert/matchet | totalt | 60 | 0,348 | 0,348 |
| normalisert/matchet | skrift:bm | 38 | 0,305 | 0,305 |
| normalisert/matchet | skrift:nn | 22 | 0,417 | 0,417 |
| normalisert/nn | totalt | 60 | 0,463 | 0,463 |
| normalisert/nn | skrift:bm | 38 | 0,492 | 0,492 |
| normalisert/nn | skrift:nn | 22 | 0,417 | 0,417 |

## Vurdering (håndført)

- **Rålagets WER falt mye; det normaliserte lagets er uendret.** ra/matchet 0,250 → 0,135 (bokmål 0,264 → 0,090, nynorsk 0,228 → 0,208) og ra/nn 0,317 → 0,248. Det normaliserte laget er identisk fordi utdataene er gjenbrukt, ikke fordi noe er målt på nytt.
- **Hovedforklaringen er at tomme og avkortede rålag-utdata er borte:** tomme hypoteser i rålaget gikk fra 6 (ra/nn) og 2 (ra/matchet) av 60 til 0 og 0. Det passer med årsaken i KLAR-EVAL-0011. Jeg har ikke gått gjennom hvilke enkeltsegmenter som endret seg utover det EVAL-0011 viser.
- **Bokmål-WER 0,090 for et ordrett lag mot ortografisk fasit er lavt.** Overlapp med treningsdata er ikke utelukket (NB-Whisper-kortet lister NST, Stortingstaler, NRK-teksting og lydbøker og nevner ikke NB Samtale, men det er ikke det samme som at ingen opptak overlapper). Tallet gir derfor ikke grunn til å vente samme WER på arkivlyd.
- **Merknadene i v1.0 gjelder fortsatt**, bortsett fra tellingen av tomme hypoteser (se over): DEV, ikke pilot; dialekt og skriftform er sammenblandet; 12 segmenter per dialektområde er lite; rålaget scores mot ortografisk fasit.
