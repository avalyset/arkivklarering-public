# DEV-måling (2026-10-26): WER på nb_samtale (validation), 60 segmenter

**DEV, ikke pilot. Ingen konklusjoner om pilotkvalitet.** 12 segmenter per dialektområde (e, n, sw, t, w), seed 20261026. Fasit: `orthographic`. Korpus-WER etter normalisering (små bokstaver, tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.

`ra` = NB-Whisper large verbatim, `normalisert` = NB-Whisper large (ikke verbatim). `nn` = `-l nn` for alle; `matchet` = språk etter fasitens skriftform. Rålaget skriver ut nøling og omtrent som sagt og scores likevel mot ortografisk fasit, så ra-tallene er ikke likestilt med normalisert lag.

| gruppe (n) | ra/nn | ra/matchet | normalisert/nn | normalisert/matchet |
|---|---|---|---|---|
| e (12) | 0.381 | 0.243 | 0.403 | 0.204 |
| n (12) | 0.367 | 0.294 | 0.599 | 0.419 |
| sw (12) | 0.356 | 0.327 | 0.500 | 0.460 |
| t (12) | 0.343 | 0.248 | 0.314 | 0.166 |
| w (12) | 0.169 | 0.146 | 0.423 | 0.400 |
| totalt (60) | 0.317 | 0.250 | 0.463 | 0.348 |
| skrift:bm (38) | 0.373 | 0.264 | 0.492 | 0.305 |
| skrift:nn (22) | 0.228 | 0.228 | 0.417 | 0.417 |

Segmenter uten noen tekst (tom hypotese), av 60: ra/nn: 6, ra/matchet: 2, normalisert/nn: 1, normalisert/matchet: 1

Modeller: ra: `nb-whisper-large-verbatim.ggml-model.bin` sha256 `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d`; normalisert: `nb-whisper-large.bin` sha256 `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76`

## Merknader (håndført, ikke generert)

- **DEV, ikke pilot.** Tallene beskriver 60 segmenter fra validation-delen av NB Samtale og sier ikke noe om kvalitet på arkivmateriale.
- **Dialekt og skriftform er sammenblandet.** sw og w er for det meste nynorsk, e, n og t for det meste bokmål (se `KLAR-EVAL-0003`). Kolonnene `nn` straffer bokmålsfasit; kolonnene `matchet` fjerner den effekten for språkvalget, men ikke for annen forskjell mellom talere og opptak.
- **12 segmenter per dialektområde er lite.** Én enkelt taler eller ett opptak kan flytte en rad. Det er ikke regnet konfidensintervall.
- **Rålaget er ikke skåret mot sin egen fasit.** Verbatim-modellen skriver ordrett, men er skåret mot den ortografiske fasiten; de to lagene er ikke likestilt (se over).
- **Overlapp med treningsdata er ikke utelukket.** NB-Whisper-kortet lister NST, Stortingstaler, NRK-teksting og lydbøker som treningsdata og nevner ikke NB Samtale; det er ikke det samme som at ingen opptak overlapper.
- **Dekning:** alle 60 segmenter fikk minst halvparten av varigheten merket som tale av segmenteringen. Tomme hypoteser (av 60): ra/nn 6, ra/matchet 2, normalisert/nn 1, normalisert/matchet 1. Ett segment fikk flagget «musikk under tale – vurder rettigheter».
