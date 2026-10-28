# KLAR-EVAL-0006: Hvor mange personvernflagg overlever talegjenkjenningen? (DEV)

Versjon 1.1, 2026-10-26. **DEV, ikke pilot. Ingen konklusjoner om pilotkvalitet.** Tall generert av `eval/dev/kjor_flaggoverlevelse_ord.py --datasett nbsamtale`; tolkning skrevet for hånd. v1.0 (union paret på likhet, uten ordtidsstempler) er beholdt i git-historikken og er tidsstemplet.

## Hva som er nytt i v1.1

- **Unionen parer nå på tidsoverlapp mellom flaggenes ordspenn** (DTW-ordtidsstempler fra whisper.cpp, `-nfa -dtw large.v3`, toleranse 0,5 s), og likheten mellom utdragene brukes bare til å skille flere tidstreff (KLAR-ADR-0012 v1.2). I v1.0 ble flaggene paret på likhet, fordi rålaget ga én cue over hele segmentet.
- **Både rålaget og det normaliserte laget er kjørt på nytt** på de samme 60 segmentene (`-l nn`) med ordtidsstempler. Instruksen sa «bare rålaget», men paring på ordspenn i hvert lag krever ordtider i begge. Kjøringen gikk som ett Whisper-kall per lag og språk (modellen lastes én gang), og `-nfa` er påkrevd for DTW.
- **Teksten ble ikke den samme som i DEV-kjøringen.** Etter normalisering (små bokstaver, tegnsetting fjernet) er bare 35 av 60 rålagstekster og 45 av 60 normaliserte tekster identiske med hypotesene i `KLAR-EVAL-0002`. Årsaken er ikke isolert: forskjellen kan komme fra `-nfa` (annen numerikk enn flash-attention), fra at flere filer ble kjørt i samme prosess (kjent fra norsk-tale: ikke bitidentisk med én prosess per fil), eller fra DTW-modusen. Sammenligningen mot v1.0 er derfor ikke et rent mål på effekten av ordtidsstempler.
- **To rålagssegmenter krasjet whisper-cli med DTW** (SIGABRT uten feilmelding, begge på tale på 3,5 og 3,6 s). De ble kjørt uten DTW og har tekst, men ingen ordtidsstempler; unionen faller tilbake til cuenes tidsrom for dem. Det normaliserte laget krasjet ikke.

## Resultat, `-l nn`, union (a) = overlevelse i samme kategori i samme segment, «streng» krever delt ord

| kategori | n ref | ra | normalisert | union (ny, ordspenn) | union v1.0 (likhet) | union-flagg ny / v1.0 | ekstra (a) ny / v1.0 |
|---|---|---|---|---|---|---|---|
| person | 17 | 12/17 (0,71) · streng 0,65 | 13/17 (0,76) · streng 0,71 | **14/17 (0,82) · streng 0,82** | 14/17 (0,82) · streng 0,76 | 21 / 20 | 5 / 5 |
| sted | 14 | 10/14 (0,71) · streng 0,64 | 13/14 (0,93) · streng 0,64 | **14/14 (1,00) · streng 0,93** | 14/14 (1,00) · streng 0,93 | 18 / 16 | 1 / 1 |
| organisasjon | 3 | 1/3 (0,33) · streng 0,33 | 3/3 (1,00) · streng 1,00 | **3/3 (1,00) · streng 1,00** | 3/3 (1,00) · streng 1,00 | 6 / 5 | 3 / 2 |

Union-flagg etter kildelag (ny): nb: begge 11, normalisert 17, ra 6; nn: begge 6, normalisert 4, ra 2. («begge» = parret mellom lagene.)

## Antall referanseflagg (n)

Person 17, sted 14, organisasjon 3; **null** for dato, fødselsår, telefon, fødselsnummer, e-post, helse, økonomi, konflikt, religion og politikk. Se `KLAR-EVAL-0007` for kategoriene som ikke er målt.

## Vurdering (håndført)

- **Overlevelsestallene endret seg ikke på det som kan måles.** Unionen fanger fortsatt 14 av 17 personer og 14 av 14 steder; antall ekstra personflagg (a) er fortsatt 5. Det er forventet, siden «overlevelse (a)» bare ser på om kategorien finnes i segmentet, og paringen bare bestemmer hvordan flaggene telles og vises.
- **Det som endret seg er antall union-flagg:** flere flagg står nå som egne (person 21 mot 20, sted 18 mot 16, organisasjon 6 mot 5), som er det en strammere paring gir (færre flagg slås sammen, og to ulike personer slås ikke sammen). Forskjellen er noen få flagg og er blandet med at teksten ikke ble identisk.
- **n er fortsatt for liten** (person 17, sted 14, organisasjon 3) til å si mer enn dette. Se `KLAR-EVAL-0007` (NPSC, større n).

Rådata: `KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.1_2026-10-26.json` (bare tall). Segmentene kommer fra `Sprakbanken/nb_samtale` validation (CC0, `KLAR-EVAL-0004`).
