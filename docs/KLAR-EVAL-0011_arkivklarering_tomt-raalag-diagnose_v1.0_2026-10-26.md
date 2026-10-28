# KLAR-EVAL-0011: Diagnose av tomt og kort rålag-utdata (DEV)

**DEV, ikke pilot. Diagnose av seks NB Samtale validation-segmenter. Ingen kode er endret; ingen tidligere EVAL-tall er endret.**

Versjon 1.0, 2026-10-26. Tall og loggutdrag generert av `eval/dev/diagnose_tomt_raalag.py`; tolkning skrevet for hånd. Bakgrunn: i `KLAR-EVAL-0010` ga rålaget (`nb-whisper-large-verbatim`) tomt eller mindre enn halvparten av referanseordene på seks av de 60 rene segmentene (tre tomt). Oppgaven omtalte «9 segmenter»; det er seks (de tre tomme er en del av de seks).

## Materiale og metode

- Segmentene: `nb-12_0038680-0043036`, `nb-22_4330585-4333333`, `nb-5_3313160-3315610`, `nb-4_8680050-8683538`, `nb-21_1124060-1131216` (to talesegmenter) og `nb-21_2788286-2792913` (referanse 16, 8, 9, 17, 11 og 15 ord). Lyden er den rene NB Samtale-lyden (CC0, `KLAR-EVAL-0004`), kuttet med samme tidslinje og samme `_kutt` som rørledningen.
- whisper.cpp: commit `4834a232` (versjon 1.9.2), `whisper-cli` med rørledningens argumenter (`-l no|nn`, `-nfa -dtw large.v3 -ojf`, modell `nb-whisper-large-verbatim`, sha256 `0227866e…`). For å få whisper.cpps egne beslutningslinjer er det bygget en separat `whisper-cli` fra samme kilde med `-DWHISPER_DEBUG` (egen byggemappe på Vault; kildetreet er ikke endret; byggemappen og binæren committes ikke). Standardbyggets loggnivå skriver ikke ut disse linjene (`WHISPER_LOG_DEBUG` er kompilert bort uten flagget).
- Alle kjøringer er én whisper-cli-prosess om gangen. Variantene er kjørt som beskrevet i tabellen; «V0» er én prosess per fil; de andre kjører alle seks segmentene i én prosess med `-mc 0` (ingen tekstkontekst mellom filene), og V0b/V8 viser at det ikke endrer utfallet.

## Hva som skjer (ordrett fra loggene)

Første dekodingsvindu for `nb-12_0038680-0043036` (talesegmentet fra inaVAMOS er 3,6 s, `-l no`). Beam search (fem dekodere) genererer tokenene i rekkefølgen `[_TT_3]`, `' vi'`, `' skal'`, `' n'`, `'ær'`, `'me'`, `' oss'` … `' skal'`, `' bli'`, `[_EOT_]` (`p = 0.997`), altså hele setningen «vi skal nærme oss hva norden er og kanskje til og med hva norden skal bli», uten et avsluttende tidsstempeltoken. Likevel er utfallet for vinduet:

```
whisper_full_with_state: decoder  0: score = -0.08457, result_len =   1, avg_logprobs = -0.08457, entropy =  0.00000
whisper_full_with_state: best decoder = 0
seek = 6, seek_delta = 6
```

Det gjentar seg: 55 vinduer for dette segmentet, 54 med `result_len = 1`; `seek` flyttes 6 hundredels sekunder om gangen; først i vindu 55 kommer tekst, og da bare de to siste ordene (« skal bli», tidsrom 3,02–33,02 s): når vinduet har flyttet seg til slutten av lyden gjelder grenen «end of audio reached» (`seek + seek_delta + delta_min >= seek_end`, linje 7406), som beholder tokens (`result_len = i + 1`). Tilsvarende for de andre: `nb-21_2788…` 68 vinduer, i loggparsingen alle med `result_len = 1` (utdata varierte mellom 0 og 5 ord fra kjøring til kjøring); `nb-22…` 40 vinduer, 39 med `result_len = 1` (utdata «.»: bare siste vindu har tekst); `nb-5…` 27 vinduer, 26 med `result_len = 1` (« osv altså»); `nb-21_1124…_0` 47 vinduer, 46 med `result_len = 1`. `nb-4…` har 3 vinduer med `result_len = 1` og gir full tekst (17 av 17 ord) i denne kjøringen, men var tomt i rørledningens batch.

**Kildekoden forklarer det** (`src/whisper.cpp`, commit `4834a232`): `result_len` settes til `i + 1` bare når et tidsstempeltoken dekodes (linje 7389–7390: `seek_delta = seek_delta_new; result_len = i + 1; has_ts = true;`). Når dekoderen så avslutter med `[_EOT_]` uten et nytt tidsstempeltoken (linje 7404–7420), er `result_len` fortsatt 1, og alle tekst-tokens etter det første tidsstempeltokenet kastes. Vinduet flyttes deretter med det første tidsstempelets verdi (`seek_delta = 6`), og samme avkortede dekoding gjentas. Unntaket er parameteren `no_timestamps`: da settes `result_len = i + 1` ved slutten av segmentet (linje 7417–7420). I CLI-et styres den av `-nt`/`--no-timestamps`.

Terskelhypotesen forkastes av loggene: i de 42 fallback-beslutningene (`failed due to avg_logprobs … and no_speech_prob …`) er `no_speech_prob` 0,00000 hver gang (maks 0, snitt 0), så kravet `no_speech_prob > 0,6` kan aldri oppfylles for denne modellen; og vinduene med `result_len = 1` har `avg_logprobs` rundt −0,03 til −0,66, over terskelen −1,0, så de utløser ikke temperaturfallback. Temperaturfallback fungerer ellers: 42 vinduer med `avg_logprobs < −1,0` ble prøvd på nytt med høyere temperatur.

## Hypoteser, test og utfall

| hypotese | test | utfall |
|---|---|---|
| (a) segmentet er for kort | talesegmentenes varighet er 1,7–4,3 s; `nb-4` (3,5 s) går fint, `nb-12` (3,6 s) feiler | forkastet som eneste årsak |
| (b) terskel for ingen tale/entropi | `no_speech_prob = 0,0` i alle 42 fallback-beslutninger; `avg_logprobs` over −1,0 i `result_len = 1`-vinduene (kildekode: `is_no_speech` krever begge) | forkastet (kilde og logg) |
| (c) språkvalg | V5 `-l auto`: 32 mot 30 ord, ett segment får 7 ord | forkastet |
| (d) vår cue-kode | `json_til_cues` mot whisper.cpps JSON, med og uten ordtider: samme tekst; «.» fra `nb-22` er et lydmerke uten ord og droppes riktig | forkastet |
| (e) ordtidsstempler (DTW) | V1 uten DTW: 25 ord mot 25 (V0b) | forkastet |
| (f) segmentgrenser fra inaVAMOS | uavhengig av grensen i første kjøring (hele ytringen ga samme tekst for 4 av 6; logg i `diag_v1_logs`); V12 med 0,5 s stillhet foran gir 68 av 76 ord | grensen spiller inn (ytringen starter brått), men er ikke selve mekanismen |
| (g) tekstkontekst mellom filer i samme prosess | V8 mot V0b | forkastet (samme utfall) |
| (h) beam search velger kort sekvens | V10 grådig dekoding: 8 ord (verre) | forkastet |
| (i) innebygd VAD (`--vad`, silero-v6.2.0) | V13: 39 ord mot 30 | endrer utfallet litt (to segmenter delvis bedre), løser det ikke |
| (j) `-nt` (ingen tidsstempeltokens) | V14: **75 av 76 ord**; DTW-ordtider beholdes | **endrer rålagets oppførsel** (se under) |

## Resultat: ord ut per variant (referanse i parentes)

| variant | 8680-0043036 (16) | 0585-4333333 (8) | 3160-3315610 (9) | 0050-8683538 (17) | 4060-1131216 (11) | 8286-2792913 (15) | sum ord (av 76) |
|---|---|---|---|---|---|---|---|
| rørledningens cache («før», batch à 40) | 2 | 0 | 2 | 0 | 4 | 0 | 8 |
| V0 rørledningens oppsett, én fil per prosess (debug-bygget whisper-cli) | 2 | 0 | 2 | 17 | 4 | 5 | 30 |
| V0b alle filer i én prosess, `-mc 0` | 2 | 0 | 2 | 17 | 4 | 0 | 25 |
| V8 alle filer i én prosess, standard tekstkontekst | 2 | 0 | 2 | 17 | 4 | 0 | 25 |
| V1 uten DTW | 2 | 0 | 2 | 17 | 4 | 0 | 25 |
| V5 språk `auto` | 2 | 7 | 2 | 17 | 4 | 0 | 32 |
| V10 grådig dekoding (`-bs 1`) | 2 | 0 | 2 | 0 | 4 | 0 | 8 |
| V13 `--vad` (silero-v6.2.0) | 2 | 0 | 2 | 17 | 7 | 11 | 39 |
| V12 0,5 s stillhet foran segmentet (kun diagnose, ikke et flagg) | 16 | 0 | 9 | 17 | 11 | 15 | 68 |
| V14 **`-nt` (ingen tidsstempeltokens), DTW beholdt** | 16 | 7 | 9 | 17 | 11 | 15 | 75 |
| V9 normalisert lag | 16 | 1 | 5 | 17 | 11 | 13 | 63 |
| V11 normalisert lag, grådig | 16 | 1 | 5 | 17 | 11 | 13 | 63 |
| V15 normalisert lag, `-nt` | 16 | 1 | 8 | 8 | 11 | 13 | 57 |
| rørledningens cache, degradert lyd («etter», EVAL-0010) | 16 | 0 | 9 | 16 | 11 | 15 | 67 |

Ord ut er ikke det samme som riktige ord; WER per segment ligger i `diagnose_tomt_raalag_2026-10-26.json` (V14: 0,188 / 0,75 / 0 / 0,059 / 0,091 / 0,067 per segment mot 0,875 / 1,0 / 0,778 / 0,059 / 0,636 / 0,733 for V0). Vi bruker «ord ut» som mål på om teksten blir kastet.

Flaggene i `whisper-cli --help` som finnes og er relevante: `-nth`, `-lpt`, `-et`, `-nf`, `-tp`/`-tpi` (terskler og temperaturfallback), `-bs`/`-bo` (beam), `-mc` (kontekst), `-sns` og `--suppress-regex` (undertrykker tokens etter tekst/regex; kan ikke rette seg mot «EOT uten avsluttende tidsstempel»), `--prompt`/`--carry-initial-prompt`, `--grammar` (GBNF), VAD-flaggene og `-nt`. **Bibliotekparametrene `suppress_blank` (standard på) og `max_initial_ts` (1,0) finnes i `whisper_full_params` men har ikke noe CLI-flagg**, så de er ikke testet (å teste dem krever egen kode mot biblioteket, som ikke er gjort). `--prompt` og `--grammar` er ikke prøvd: å tvinge fram tekst er et eget grep uten kilde for dette problemet.

## Sammenligning med det normaliserte laget

Det normaliserte laget (V9) gir 63 av 76 ord på de samme seks segmentene mot 30 for rålaget (V0), med hele teksten for tre av dem. Det har samme mekanisme i svakere grad (`nb-22`: 1 av 8). Rørledningens union av begge lag (KLAR-ADR-0012) dekker derfor flaggingen i stor grad selv når rålaget mister starten; WER for selve rålaget (H1a) påvirkes fullt ut.

## Vurdering (håndført)

- **Årsaken er en kombinasjon av modellatferd og hvordan whisper.cpp tolker den:** verbatim-modellen avslutter noen ganger med `[_EOT_]` uten et avsluttende tidsstempeltoken, og whisper.cpp kaster da all tekst etter det første tidsstempeltokenet. Dette er ikke en feil i vår kode (hypotese d er forkastet), og det er ikke en følge av batch-kjøringen (V0, V0b og V8 gir samme feilmønster; produksjonsstien i `transkriber.transkriber_segment` bruker de samme flaggene og har derfor den samme begrensningen).
- **Omfang i DEV:** 6 av 60 segmenter (10 %) fikk under halvparten av referanseordene i rålaget i `KLAR-EVAL-0010`; dette ligger allerede i DEV-grunnlaget for terskelen H1a (rålag/matchet 0,250 i `KLAR-EVAL-0002`). Terskelen i PREREG-0001 er derfor ikke endret. Utvalget er lite (seks segmenter, ett datasett, ett whisper.cpp-bygg), og kjøringer i samme prosess er ikke bitidentiske (ett av seks segmenter ga 5 ord i V0 og 0 i V0b).
- **`-nt` er et eksisterende flagg som endrer rålagets oppførsel.** Det er **ikke innført**. Før det kan inn i rørledningen kreves ny DEV for de berørte EVAL-ene (0002, 0006, 0007, 0008, 0010 og H4-tørrtesten) og en ny tag `h4-script-v2`, og beslutning fra eier. En regresjon på de 60 DEV-segmentene kjøres på en egen gren (`nt-regresjon`) og rapporteres separat; ingenting går inn på `main`.
- **Det som ikke er undersøkt:** hvorfor modellen utelater avsluttende tidsstempel i disse vinduene; om `suppress_blank`/`max_initial_ts` ville hjulpet (ingen CLI-flagg); om andre verbatim-modeller (medium) har samme mønster; om `-nt` endrer ordtidsstemplene (DTW-ordtider er til stede i JSON, men kvaliteten er ikke målt).

## Filer

Store dekoderlogger (flere MB hver) ligger bare på Vault (`/Volumes/Vault/arkivklarering/tmp/`) og committes ikke; repoet har tallene (`eval/dev/diagnose_tomt_raalag_2026-10-26.json`, sha256 `87fca99fa4e4b9f027cff15b3623b9b6c055e7c3e770f47780910d9dd8f7a2f5`) og utdragene over.

| loggfil (under `tmp/`) | byte | sha256 |
|---|---|---|
| `diag/stderr_V0_nb-12_0038680-0043036_0.txt` | 960290 | `ffab4cd4fdb510b816a9bc5a89745dad65e06a19310ff8bb328fd205762d12da` |
| `diag/stderr_V0_nb-12_0038680-0043036_hele.txt` | 1027057 | `41216c7c3ff1f1ace2f4f9778817ebe64a5bae133f528d117bf1c767d769f348` |
| `diag/stderr_V0_nb-21_1124060-1131216_0.txt` | 607814 | `531b3abc57fa50811e50c41a3222c59341f6b0bdcb28e2518752630ae9eddc86` |
| `diag/stderr_V0_nb-21_1124060-1131216_1.txt` | 28783 | `50353e8c66159d204f2957b18275b626fdc39a2cc919d9c85862bce570ddded6` |
| `diag/stderr_V0_nb-21_1124060-1131216_hele.txt` | 45887 | `10b3ea95e2271c315e6bf06a9015da5a6cfe7b475ab13cb642d92a1e9e2f9ff5` |
| `diag/stderr_V0_nb-21_2788286-2792913_0.txt` | 1441783 | `e975abd282bb2e24e8681e7b7bc7fd0fba8dfe61abc6098811cb28f8323cc8e9` |
| `diag/stderr_V0_nb-21_2788286-2792913_hele.txt` | 1270786 | `b90505e93358757817a46d7888c7d0583eab2385beabaeadaec72827b2f60591` |
| `diag/stderr_V0_nb-22_4330585-4333333_0.txt` | 569014 | `de9abdfd08f18dc6f29b9435b69769a30a75866c1e7a43070dd84d6ae4a53a0d` |
| `diag/stderr_V0_nb-22_4330585-4333333_hele.txt` | 385333 | `5a455abf98adabeaac54aa4a3bdf7fe6b77c9147d3841b286b39d5d2b670ff82` |
| `diag/stderr_V0_nb-4_8680050-8683538_0.txt` | 122955 | `bf77caa82638998a3eda8e26f74ea814ef2ef82b6609610bf427a340727c93b4` |
| `diag/stderr_V0_nb-4_8680050-8683538_hele.txt` | 122964 | `d4b277ef4cc11e928e38ddce3d26fd563698cb4c09cc4c99d266e4ed100fc278` |
| `diag/stderr_V0_nb-5_3313160-3315610_0.txt` | 441502 | `26c358a269083cc15b26df3992fd21cf933c81c91142ce715c3e28f68ec010d1` |
| `diag/stderr_V0_nb-5_3313160-3315610_hele.txt` | 441511 | `0082a4fa278315576348fd546b6830980b16b241e037fd0a58a90caea1811e7e` |
| `diag_v1_logs/stderr_V0_nb-12_0038680-0043036_0.txt` | 960290 | `0fa9df5e19246e234a4b1b1406d2faf9caa3226998dd145c6b51a4cdea4d8461` |
| `diag_v1_logs/stderr_V0_nb-12_0038680-0043036_hele.txt` | 1027057 | `41216c7c3ff1f1ace2f4f9778817ebe64a5bae133f528d117bf1c767d769f348` |
| `diag_v1_logs/stderr_V0_nb-21_1124060-1131216_0.txt` | 607814 | `7e2367d31fe06c509169b876cc4e1c9abd2293638aa1262cc0594b5a5e0b7936` |
| `diag_v1_logs/stderr_V0_nb-21_1124060-1131216_1.txt` | 28783 | `7debcdc86c17900981ce29abc0fb580de22732a12502e3e69a889340c5b97b65` |
| `diag_v1_logs/stderr_V0_nb-21_1124060-1131216_hele.txt` | 45887 | `10b3ea95e2271c315e6bf06a9015da5a6cfe7b475ab13cb642d92a1e9e2f9ff5` |
| `diag_v1_logs/stderr_V0_nb-21_2788286-2792913_0.txt` | 1441783 | `db2026bb5543c78ae45ebceb93566aee41e563708b0c33cc067b823083b41807` |
| `diag_v1_logs/stderr_V0_nb-21_2788286-2792913_hele.txt` | 1270786 | `b90505e93358757817a46d7888c7d0583eab2385beabaeadaec72827b2f60591` |
| `diag_v1_logs/stderr_V0_nb-22_4330585-4333333_0.txt` | 569014 | `98203654cdb37817010b0c7a56b5e94871b72924a679609550469280a639b900` |
| `diag_v1_logs/stderr_V0_nb-22_4330585-4333333_hele.txt` | 385333 | `5a455abf98adabeaac54aa4a3bdf7fe6b77c9147d3841b286b39d5d2b670ff82` |
| `diag_v1_logs/stderr_V0_nb-4_8680050-8683538_0.txt` | 122955 | `62fc9fb8b3ec270fa57acdf6a1639dbadf9ae7d7569bded7f3d99338e2d3ce5c` |
| `diag_v1_logs/stderr_V0_nb-4_8680050-8683538_hele.txt` | 122964 | `d4b277ef4cc11e928e38ddce3d26fd563698cb4c09cc4c99d266e4ed100fc278` |
| `diag_v1_logs/stderr_V0_nb-5_3313160-3315610_0.txt` | 441502 | `fbafccc467bb9a24a1d07f8e96a126775a876430e5fe68a06d112f165eb56e8b` |
| `diag_v1_logs/stderr_V0_nb-5_3313160-3315610_hele.txt` | 441511 | `0082a4fa278315576348fd546b6830980b16b241e037fd0a58a90caea1811e7e` |
