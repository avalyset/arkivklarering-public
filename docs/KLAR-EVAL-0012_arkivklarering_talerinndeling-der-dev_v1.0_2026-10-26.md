# KLAR-EVAL-0012: Talerinndeling, DER på NB Samtale validation (DEV)

**DEV, ikke pilot. Konstruert sammenstilling av ytringer (hver kilde = ytringene i tidsrekkefølge), ikke hele opptak.**

Versjon 1.0, 2026-10-26. Tall generert av `eval/dev/kjor_der.py`; tolkning skrevet for hånd (under «Vurdering»).

## Oppsett

- **Modell:** `pyannote/speaker-diarization-community-1` (pyannote.audio, samme standardmodell som WhisperX), antall talere ukjent for modellen, enhet cpu.
- **Materiale:** NB Samtale validation (1194 ytringer, 35 kilder; CC0, KLAR-EVAL-0004). Se `eval/dev/kjor_der.py` for sammenstillingen: ytringer i tidsrekkefølge, pause mellom dem fra originalen begrenset til 0,2–2,0 s, ingen overlapp.
- **Mål:** DER = (missed speech + false alarm + speaker confusion) / total referansetale (pyannote.metrics), collar 0,25 s og 0 s. Referanse: `speaker_id` per ytring.

## Samlet

| collar | DER | missed | false alarm | confusion | total referansetale (s) |
|---|---|---|---|---|---|
| 0,25 s | 0,166 | 0,074 | 0,031 | 0,060 | 8032,6 |
| 0,0 s | 0,191 | 0,088 | 0,037 | 0,065 | 8330,7 |

Antall talere: riktig 11 av 35 kilder, for mange 21, for få 3.

## Per kilde (collar 0,25 s)

| kilde | lengde (s) | ytringer | talere ref/est | DER | missed | false alarm | confusion |
|---|---|---|---|---|---|---|---|
| 50f-10 | 148,2 | 19 | 3/4 | 0,239 | 0,032 | 0,090 | 0,118 |
| 50f-11 | 168,6 | 19 | 3/3 | 0,087 | 0,073 | 0,011 | 0,004 |
| 50f-14 | 194,9 | 27 | 3/3 | 0,128 | 0,043 | 0,020 | 0,065 |
| 50f-15 | 205,0 | 31 | 3/4 | 0,164 | 0,045 | 0,056 | 0,063 |
| 50f-16 | 278,8 | 31 | 3/4 | 0,084 | 0,050 | 0,011 | 0,023 |
| 50f-17 | 212,9 | 28 | 3/3 | 0,121 | 0,059 | 0,045 | 0,017 |
| 50f-18 | 219,8 | 38 | 3/2 | 0,220 | 0,051 | 0,004 | 0,165 |
| 50f-25 | 183,9 | 24 | 3/4 | 0,222 | 0,066 | 0,038 | 0,118 |
| 50f-32 | 263,0 | 27 | 3/2 | 0,072 | 0,041 | 0,020 | 0,011 |
| 50f-34 | 265,7 | 32 | 3/5 | 0,217 | 0,130 | 0,001 | 0,087 |
| 50f-6 | 148,9 | 15 | 2/3 | 0,108 | 0,089 | 0,004 | 0,015 |
| 50f-7 | 248,6 | 35 | 3/4 | 0,202 | 0,047 | 0,055 | 0,101 |
| 50f-9 | 244,2 | 22 | 3/3 | 0,082 | 0,032 | 0,040 | 0,010 |
| nb-1 | 443,1 | 54 | 5/7 | 0,258 | 0,043 | 0,094 | 0,121 |
| nb-12 | 143,1 | 21 | 2/3 | 0,119 | 0,069 | 0,010 | 0,040 |
| nb-13 | 433,8 | 54 | 3/4 | 0,234 | 0,053 | 0,086 | 0,095 |
| nb-19 | 212,9 | 21 | 2/2 | 0,152 | 0,038 | 0,067 | 0,048 |
| nb-2 | 137,0 | 15 | 2/2 | 0,124 | 0,070 | 0,022 | 0,032 |
| nb-20 | 354,7 | 47 | 2/4 | 0,305 | 0,106 | 0,063 | 0,135 |
| nb-21 | 301,2 | 28 | 2/2 | 0,105 | 0,090 | 0,012 | 0,004 |
| nb-22 | 549,5 | 71 | 5/8 | 0,236 | 0,093 | 0,022 | 0,121 |
| nb-23 | 477,0 | 45 | 4/6 | 0,124 | 0,068 | 0,007 | 0,049 |
| nb-24 | 317,6 | 35 | 2/3 | 0,100 | 0,075 | 0,002 | 0,023 |
| nb-26 | 140,2 | 12 | 2/2 | 0,128 | 0,123 | 0,005 | 0,000 |
| nb-27 | 606,4 | 73 | 4/6 | 0,226 | 0,086 | 0,042 | 0,099 |
| nb-28 | 338,1 | 29 | 4/3 | 0,114 | 0,064 | 0,025 | 0,025 |
| nb-29 | 172,7 | 20 | 2/3 | 0,137 | 0,043 | 0,048 | 0,047 |
| nb-3 | 340,0 | 50 | 3/4 | 0,360 | 0,052 | 0,099 | 0,209 |
| nb-30 | 309,7 | 33 | 3/4 | 0,252 | 0,154 | 0,044 | 0,053 |
| nb-33 | 521,7 | 46 | 5/6 | 0,182 | 0,123 | 0,026 | 0,033 |
| nb-35 | 142,9 | 15 | 2/2 | 0,112 | 0,111 | 0,000 | 0,001 |
| nb-4 | 952,6 | 102 | 7/8 | 0,097 | 0,065 | 0,005 | 0,026 |
| nb-5 | 479,2 | 41 | 3/3 | 0,079 | 0,064 | 0,000 | 0,015 |
| tr-31 | 155,0 | 21 | 3/4 | 0,180 | 0,125 | 0,000 | 0,055 |
| tr-8 | 135,0 | 13 | 2/2 | 0,152 | 0,104 | 0,026 | 0,023 |

Rådata: `KLAR-EVAL-0012_arkivklarering_talerinndeling-der-dev_v1.0_2026-10-26.json` (bare tall).
## Vurdering

Skrevet for hånd. Tallene over er målt, tolkningen er min.

- **Samlet DER 0,166 (collar 0,25 s) og 0,191 (collar 0 s)** på 8 033 s referansetale (35 kilder). Medianen per kilde er 0,137 (laveste 0,072, høyeste 0,360); 18 av 35 kilder ligger på 0,15 eller lavere. Feilen fordeler seg på overhørt tale (0,074), falsk alarm (0,031) og taleforveksling (0,060).
- **Tallet er ikke sammenlignbart med DER på hele opptak.** Kildene er konstruert av ytringer i tidsrekkefølge, uten overlappende tale og med pauser begrenset til 0,2–2,0 s (se oppsettet). Mangel på overlapp gjør oppgaven lettere; kunstige overganger og korte lydbiter gjør den vanskeligere. Jeg vet ikke nettoeffekten og påstår ingen retning.
- **Antall talere er det svakeste punktet:** riktig i 11 av 35 kilder, for mange i 21, for få i 3. Modellen deler altså oftere én taler i to enn den slår to sammen. For brukeren betyr det at TALER_n er et forslag til menneskelig vurdering og ikke en fasit på hvor mange personer som snakker, slik MERKNAD i `diarisering.py` og README allerede sier.
- **Hva målingen ikke dekker:** ekte båndlyd, overlappende tale, lange opptak, og andre målformer/dialekter enn de i NB Samtale. Ingen terskel i KLAR-PREREG-0001 hviler på dette tallet; talerinndeling er et valgfritt tillegg (`--taler`, KLAR-ADR-0016) og er utenfor de forhåndsregistrerte hypotesene.
- **Kjøring:** CPU, 7 697 s, én prosess om gangen (ikke samtidig med Whisper).
