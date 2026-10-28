# H4-skriptet: tørrtest på justeringsmanus

**TØRRTEST PÅ JUSTERINGSMANUS (SYNTETISK, TTS). Ingen H4-måling: justeringsmanuset er brukt til å justere mønstrene og tersklene, og lyden er syntetisk.**

Generert 2026-10-27 av `kalibrering/kjor_h4.py`. Manus: `KLAR-MANUS-0001_arkivklarering_justeringsmanus_v1.1_2026-10-26.tsv` (sha256 `9857f82c526e550591aa6282392c3247600cbf983ade5af1c46d63c572cc3ee8`). Oppsett: matchet. Preregistrering: `KLAR-PREREG-0001_arkivklarering_testdeler_v1.6_2026-10-26.md`.

## Union per kategori (flagg-treff / n; terskel fra KLAR-PREREG-0001)

| kategori | n | flagg-treff | andel | 95 %-int. (Wilson) | terskel | vurdering | bokmål | nynorsk |
|---|---|---|---|---|---|---|---|---|
| person | 26 | 18 | 0,692 | 0,500–0,835 | ≥ 0.60 | bestått | 9/13 | 9/13 |
| sted | 40 | 34 | 0,850 | 0,709–0,929 | ≥ 0.70 | bestått (klart) | 18/20 | 16/20 |
| dato | 14 | 14 | 1,000 | 0,785–1,000 | ≥ 0.70 | bestått (klart) | 7/7 | 7/7 |
| fødselsår | 18 | 15 | 0,833 | 0,608–0,942 | ≥ 0.70 | bestått | 7/9 | 8/9 |
| telefon | 14 | 12 | 0,857 | 0,601–0,960 | ≥ 0.60 | bestått (klart) | 7/7 | 5/7 |
| fødselsnummer | 12 | 10 | 0,833 | 0,552–0,953 | ≥ 0.50 | bestått (klart) | 5/6 | 5/6 |
| e-post | 12 | 0 | 0,000 | 0,000–0,243 | ≤ 0.10 | bestått | 0/6 | 0/6 |
| helse | 26 | 26 | 1,000 | 0,871–1,000 | ≥ 0.75 | bestått (klart) | 13/13 | 13/13 |
| økonomi | 22 | 19 | 0,864 | 0,667–0,953 | ≥ 0.70 | bestått | 10/11 | 9/11 |
| konflikt | 26 | 22 | 0,846 | 0,665–0,939 | ≥ 0.65 | bestått (klart) | 13/14 | 9/12 |
| religion | 16 | 12 | 0,750 | 0,505–0,898 | ≥ 0.55 | bestått | 7/8 | 5/8 |
| politikk | 18 | 16 | 0,889 | 0,672–0,969 | ≥ 0.70 | bestått | 9/9 | 7/9 |

«Bestått» gjelder punktestimatet; «klart» betyr at også 95 %-intervallgrensen er på riktig side av terskelen. Intervallene antar uavhengige målelementer, og elementer i samme setning, fra samme leser og fra samme opptak er ikke uavhengige.

## Per lag (rålag, normalisert lag og union; flagg-treff / n)

| lag og målform | person | sted | dato | fødselsår | telefon | fødselsnummer | e-post | helse | økonomi | konflikt | religion | politikk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| normalisert|nb | 8/13 | 17/20 | 7/7 | 7/9 | 5/7 | 5/6 | 0/6 | 13/13 | 10/11 | 13/14 | 7/8 | 9/9 |
| normalisert|nn | 9/13 | 16/20 | 7/7 | 8/9 | 5/7 | 5/6 | 0/6 | 13/13 | 9/11 | 9/12 | 4/8 | 7/9 |
| ra|nb | 7/13 | 7/20 | 2/7 | 6/9 | 3/7 | 2/6 | 0/6 | 13/13 | 10/11 | 13/14 | 6/8 | 9/9 |
| ra|nn | 8/13 | 7/20 | 2/7 | 6/9 | 3/7 | 2/6 | 0/6 | 13/13 | 9/11 | 9/12 | 5/8 | 7/9 |
| union|nb | 9/13 | 18/20 | 7/7 | 7/9 | 7/7 | 5/6 | 0/6 | 13/13 | 10/11 | 13/14 | 7/8 | 9/9 |
| union|nn | 9/13 | 16/20 | 7/7 | 8/9 | 5/7 | 5/6 | 0/6 | 13/13 | 9/11 | 9/12 | 5/8 | 7/9 |

Opptak: 156; segmenter i cachen: 156.
