# KLAR-EVAL-0010: Robusthet for båndlyd (simulert degradering, DEV)

**SIMULERT DEGRADERING (DEV, ikke pilot): båndlyd-lignende støy lagt på ren NB Samtale-lyd. Ikke ekte båndlyd.**

Versjon 1.5, 2026-10-28 (v1.5: pekere til versjoner som ikke er i treet er merket «(i git-historikken)», og pekere med linjenummer til forrige versjon av et dokument med ny versjon viser til den nye versjonen, samme linje; kontrollert med `scripts/sjekk_pekere.py`, 0 brudd (KLAR-LOG-0005, restfunn etter kontrollen); v1.4: setningen om forrige versjon sier at v1.1 ligger i git-historikken (porten, runde 3 (KLAR-LOG-0005), funn 13); v1.3: bare rådatapekeren nederst rettet til `KLAR-EVAL-0010_arkivklarering_degradering-dev_v1.2_2026-10-27.json`; tall og tekst ellers uendret). Versjon 1.2, 2026-10-27. Gjentatt etter at rålaget ble endret til `-nt` (ingen tidsstempeltokens; KLAR-ADR-0017, bakgrunn KLAR-EVAL-0011). **Forrige versjon (v1.1) er «før -nt»; md-fila ligger i git-historikken (KLAR-ARK-0002), og rådataene `KLAR-EVAL-0010_arkivklarering_degradering-dev_v1.0_2026-10-26.json` ligger i `docs/`.** Rålaget er kjørt på nytt fra rådata med `scripts/reproduser.sh` på commit `d75bc40` (kode som ved taggen `h4-script-v2`, se KLAR-LOG-0001); det normaliserte laget er gjenbrukt fra lagret utdata (modell-sha256 `0f2f66f2…` og parametere uendret, ingen `-nt`; gjenbruket er logget i kjøringen). Tallene er generert, vurderingen er skrevet for hånd. Rådata: `KLAR-EVAL-0010_arkivklarering_degradering-dev_v1.2_2026-10-27.json` (sha256 `b4f303973f5e302b04efc037b0f02de6be146d6928fb05d658278310259750cc`). Forrige versjon: v1.1 (2026-10-26). DEV, ikke pilot. Tall generert av `eval/dev/kjor_degradering.py`; tolkning skrevet for hånd (under «Vurdering»).

## Oppsett

- **Materiale:** de samme 60 NB Samtale validation-segmentene som KLAR-EVAL-0002, -0003 og -0006 (CC0, se KLAR-EVAL-0004). Referanse for WER: `orthographic`; referanse for flaggene: personvernmotoren på referanseteksten.
- **Degradering** (`eval/dev/degrader_lyd.py`, audiomentations 0.43.1 og ffmpeg, eget venv): hastighet: ffmpeg vibrato f=0.8 d=1.0 (±1,15 % frekvensavvik målt); bandbegrensning: HighPassFilter 300 Hz + LowPassFilter 3400 Hz, 12 dB/oktav; sus: AddGaussianSNR 15 dB; kompresjon: Mp3Compression 24 kbit/s (lameenc). Fast seed per segment. Parametrene er valgt for å ligne smalbånds båndlyd, ikke målt mot noen ekte båndmaskin.
- **Rørledning:** som i KLAR-EVAL-0006 v1.1, men **språk etter målform** (bokmål `-l no`, nynorsk `-l nn`, «matchet»). «Før» er kjørt på nytt her med samme kode som «etter», og er derfor ikke bitidentisk med KLAR-EVAL-0002 (rålag/matchet 0,135 i KLAR-EVAL-0002 v1.1, med -nt).
- **WER:** korpus-WER (jiwer), små bokstaver og tegnsetting fjernet; 95 %-intervall fra bootstrap over segmenter (2000 gjentak, seed 20261026). Intervallene er for smale: segmentene kommer fra få talere og er ikke uavhengige.
- **Flaggoverlevelse (a):** andelen referanseflagg i kategorien som har minst ett rørledningsflagg i samme kategori i samme segment. Bare person og sted måles (n er lite: se tabellen).

## WER (korpus, 60 segmenter)

| lag | målform | n | før | 95 %-int. | etter | 95 %-int. |
|---|---|---|---|---|---|---|
| rålag (hovedutfall) | nb | 38 | 0,090 | 0,063–0,118 | 0,161 | 0,127–0,193 |
| rålag (hovedutfall) | nn | 22 | 0,213 | 0,167–0,262 | 0,235 | 0,178–0,305 |
| rålag (hovedutfall) | samlet | 60 | 0,137 | 0,109–0,168 | 0,189 | 0,157–0,221 |
| normalisert | nb | 38 | 0,315 | 0,232–0,397 | 0,299 | 0,257–0,336 |
| normalisert | nn | 22 | 0,405 | 0,336–0,489 | 0,351 | 0,281–0,431 |
| normalisert | samlet | 60 | 0,350 | 0,293–0,41 | 0,319 | 0,283–0,354 |

## Flaggoverlevelse (a): overlevd / referanseflagg

| kategori | lag | målform | før | etter |
|---|---|---|---|---|
| person | ra | nb | 6/8 (0,750) | 5/8 (0,625) |
| person | ra | nn | 6/9 (0,667) | 7/9 (0,778) |
| person | ra | samlet | 12/17 (0,706) | 12/17 (0,706) |
| sted | ra | nb | 8/10 (0,800) | 8/10 (0,800) |
| sted | ra | nn | 4/4 (1,000) | 4/4 (1,000) |
| sted | ra | samlet | 12/14 (0,857) | 12/14 (0,857) |
| person | normalisert | nb | 8/8 (1,000) | 8/8 (1,000) |
| person | normalisert | nn | 5/9 (0,556) | 4/9 (0,444) |
| person | normalisert | samlet | 13/17 (0,765) | 12/17 (0,706) |
| sted | normalisert | nb | 10/10 (1,000) | 9/10 (0,900) |
| sted | normalisert | nn | 3/4 (0,750) | 4/4 (1,000) |
| sted | normalisert | samlet | 13/14 (0,929) | 13/14 (0,929) |
| person | union | nb | 8/8 (1,000) | 8/8 (1,000) |
| person | union | nn | 6/9 (0,667) | 7/9 (0,778) |
| person | union | samlet | 14/17 (0,824) | 15/17 (0,882) |
| sted | union | nb | 10/10 (1,000) | 9/10 (0,900) |
| sted | union | nn | 4/4 (1,000) | 4/4 (1,000) |
| sted | union | samlet | 14/14 (1,000) | 13/14 (0,929) |

Rådata: `KLAR-EVAL-0010_arkivklarering_degradering-dev_v1.2_2026-10-27.json` (bare tall; v1.3: v1.2 og eldre pekte på `…_v1.0_2026-10-27.json`, som ikke finnes; tabellene stemmer med v1.2-fila).

## Før og etter -nt (generert av `scripts/lag_nt_versjoner.py`)

| lag | målform | betingelse | n | før -nt (EVAL-0010 v1.1 (i git-historikken)) | etter -nt |
|---|---|---|---|---|---|
| ra | nb | ren lyd | 38 | 0,258 | 0,090 |
| ra | nn | ren lyd | 22 | 0,258 | 0,213 |
| ra | samlet | ren lyd | 60 | 0,258 | 0,137 |
| normalisert | nb | ren lyd | 38 | 0,315 | 0,315 |
| normalisert | nn | ren lyd | 22 | 0,405 | 0,405 |
| normalisert | samlet | ren lyd | 60 | 0,350 | 0,350 |
| ra | nb | degradert | 38 | 0,156 | 0,161 |
| ra | nn | degradert | 22 | 0,225 | 0,235 |
| ra | samlet | degradert | 60 | 0,183 | 0,189 |
| normalisert | nb | degradert | 38 | 0,299 | 0,299 |
| normalisert | nn | degradert | 22 | 0,351 | 0,351 |
| normalisert | samlet | degradert | 60 | 0,319 | 0,319 |

## Vurdering (håndført)

- **Retningen har snudd.** I v1.1 var rålagets WER lavere på degradert lyd (0,183) enn på ren (0,258), og jeg forklarte det med seks segmenter med tomt eller kort rålag på ren lyd. Med `-nt` er rålagets WER 0,137 på ren lyd og 0,189 på degradert: degraderingen gjør rålaget litt dårligere (0,052 absolutt), slik man ville vente. Nynorsk 0,213 → 0,235 og bokmål 0,090 → 0,161.
- **Normalisert lag er uendret** (gjenbrukt utdata): 0,350 ren og 0,319 degradert. Her er forskjellen mellom ren og degradert fortsatt i «feil» retning; jeg har ikke undersøkt hvorfor, og påstår ingen årsak.
- Målingen sier fortsatt ikke at rørledningen tåler (eller ikke tåler) ekte båndlyd: simulert degradering, én parametersetting, én seed. Flaggoverlevelsen er i denne versjonen ikke tolket på nytt; se tabellene over og rådataene.
- Intervallene (segmentbootstrap) er for smale (se Oppsett).
