# TEST – preregistrert (OSF hc83q) (2026-10-27): WER på nb_samtale (test), 252 segmenter

**TEST – preregistrert (OSF hc83q).** Opptil 60 segmenter per dialektområde (e, n, sw, t, w), seed 20261026; har et område færre kvalifiserte segmenter, tas alle. Antall per område: e 60, n 60, sw 60, t 21, w 51. Fasit: `orthographic`. Korpus-WER etter normalisering (små bokstaver, tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.

`ra` = NB-Whisper large verbatim, `normalisert` = NB-Whisper large (ikke verbatim). `nn` = `-l nn` for alle; `matchet` = språk etter fasitens skriftform. Rålaget skriver ut nøling og omtrent som sagt og scores likevel mot ortografisk fasit, så ra-tallene er ikke likestilt med normalisert lag.

| gruppe (n) | ra/nn | ra/matchet | normalisert/nn | normalisert/matchet |
|---|---|---|---|---|
| e (60) | 0.273 | 0.101 | 0.494 | 0.285 |
| n (60) | 0.288 | 0.115 | 0.491 | 0.326 |
| sw (60) | 0.210 | 0.134 | 0.386 | 0.323 |
| t (21) | 0.342 | 0.144 | 0.590 | 0.414 |
| w (51) | 0.196 | 0.159 | 0.421 | 0.390 |
| totalt (252) | 0.254 | 0.128 | 0.464 | 0.337 |
| skrift:bm (159) | 0.315 | 0.111 | 0.518 | 0.314 |
| skrift:nn (93) | 0.154 | 0.154 | 0.375 | 0.375 |

Segmenter uten noen tekst (tom hypotese), av 252: ra/nn: 0, ra/matchet: 0, normalisert/nn: 5, normalisert/matchet: 1

Modeller: ra: `nb-whisper-large-verbatim.ggml-model.bin` sha256 `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d`; normalisert: `nb-whisper-large.ggml-model.bin` sha256 `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76`
