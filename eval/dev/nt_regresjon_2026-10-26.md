# Regresjon av `-nt` på de 60 DEV-segmentene (GREN nt-regresjon, ikke på main)

2026-10-26. Generert av `eval/dev/kjor_nt_regresjon.py` i commit `981acac` (env-bryter som la `-nt` på begge lag; skriptet er fjernet etter at bryteren ble gjort per lag, KLAR-ADR-0017). Historisk grunnlag for KLAR-ADR-0017 (eier besluttet `-nt` bare for rålaget).

## WER (korpus, 60 segmenter, språk etter målform)

| lag | målform | n | uten `-nt` (EVAL-0010 «før») | med `-nt` |
|---|---|---|---|---|
| rålag | nb | 38 | 0,258 (0,185–0,338) | 0,090 (0,063–0,118) |
| rålag | nn | 22 | 0,258 (0,19–0,335) | 0,213 (0,167–0,262) |
| rålag | samlet | 60 | 0,258 (0,207–0,315) | 0,137 (0,109–0,168) |
| normalisert | nb | 38 | 0,315 (0,232–0,397) | 0,349 (0,249–0,454) |
| normalisert | nn | 22 | 0,405 (0,336–0,489) | 0,628 (0,477–0,785) |
| normalisert | samlet | 60 | 0,350 (0,293–0,41) | 0,456 (0,363–0,551) |

Segmenter der rålaget gir under halvparten av referanseordene: uten `-nt` 6 (nb-12_0038680-0043036, nb-22_4330585-4333333, nb-5_3313160-3315610, nb-4_8680050-8683538, nb-21_1124060-1131216, nb-21_2788286-2792913); med `-nt` 0 ().
Rålags-cuer uten ordtidsstempler med `-nt`: 0.

## Flaggoverlevelse (a): overlevd / referanseflagg

| kategori | lag | målform | uten `-nt` | med `-nt` |
|---|---|---|---|---|
| person | ra | nb | 6/8 (0,750) | 6/8 (0,750) |
| person | ra | nn | 6/9 (0,667) | 6/9 (0,667) |
| person | ra | samlet | 12/17 (0,706) | 12/17 (0,706) |
| sted | ra | nb | 6/10 (0,600) | 8/10 (0,800) |
| sted | ra | nn | 4/4 (1,000) | 4/4 (1,000) |
| sted | ra | samlet | 10/14 (0,714) | 12/14 (0,857) |
| person | normalisert | nb | 8/8 (1,000) | 8/8 (1,000) |
| person | normalisert | nn | 5/9 (0,556) | 2/9 (0,222) |
| person | normalisert | samlet | 13/17 (0,765) | 10/17 (0,588) |
| sted | normalisert | nb | 10/10 (1,000) | 7/10 (0,700) |
| sted | normalisert | nn | 3/4 (0,750) | 3/4 (0,750) |
| sted | normalisert | samlet | 13/14 (0,929) | 10/14 (0,714) |
| person | union | nb | 8/8 (1,000) | 8/8 (1,000) |
| person | union | nn | 7/9 (0,778) | 6/9 (0,667) |
| person | union | samlet | 15/17 (0,882) | 14/17 (0,824) |
| sted | union | nb | 10/10 (1,000) | 10/10 (1,000) |
| sted | union | nn | 4/4 (1,000) | 4/4 (1,000) |
| sted | union | samlet | 14/14 (1,000) | 14/14 (1,000) |
