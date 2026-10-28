---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0013: Lokal ollama-modell for katalogutkastet: Borealis-open 4B
Versjon 1.1, 2026-10-28 (v1.1: parameterantallet for standardmodellen har kilde (KLAR-KILDE-0001 LI-17, K46), og størrelsen 3,3 GB er merket som egen observasjon; «modellene på 4 til 8 GB» rettet til «4–8 mrd. parametere (3,3–4,9 GB)», som tabellen viser; beslutningen er uendret; v1.0: første versjon).
## Kontekst

Katalogutkastet (tittel, dato hvis den nevnes, talere, steder, 3–8 emneord og et sammendrag per segment med tidskode, merket «utkast – maskinforslag») skal lages med en **lokal** modell via ollama; ingenting går til skyen (KLAR-ADR-0007). Modellen skal skrive norsk (bokmål og nynorsk), følge et JSON-format og la være å finne på navn, steder og datoer. Installerte modeller på maskinen (ollama ligger på Vault): norske instruksjonsmodeller fra NbAiLab og NORA.LLM (`nb-llama-3.1-8b-instruct`, `normistral-7b-warm-instruct`, `borealis-open-4b`, `borealis-4b`, `borealis-open-12b`), samt flerspråklige (`gemma2:9b`, `llama3.1:8b`, `qwen2.5:7b`, `mistral`). Maskinen har 16 GB, og katalogutkastet kjøres sammen med spaCy og NB-BERT i samme prosess, så små modeller (høyst ca. 5 GB) er foretrukket.

## Beslutning

**`hf.co/NbAiLab/borealis-open-4b-gguf:Q4_K_M`** (Gemma 3-basert, 3,88 milliarder parametere ifølge Hugging Face-API-et (KLAR-KILDE-0001 LI-17, K46); 3,3 GB på disk, egen observasjon i ollama) er standard (`katalog.STANDARD_MODELL`); modellen kan byttes med `--katalogmodell`.

Valget bygger på en enkel, mekanisk sammenligning (`eval/dev/velg_katalogmodell.py`, DEV) av de fire norske modellene på 4–8 mrd. parametere (3,3–4,9 GB på disk, egen observasjon i ollama; tabellen under). Inndata var fire sammenhengende utdrag på 45 setninger av **menneskelig** transkripsjon fra NPSC validation (CC0): tre bokmål og ett nynorsk, trukket med fast seed. Det isolerer modellens norsk fra Whispers feil. Krav: minst 90 % gyldig JSON ved første forsøk, minst 25 % norske og under 2 % engelske stoppord i sammendragene. Blant modellene som oppfyller kravene velges den med færrest forslag som ikke står i teksten (forkastet av `katalog.rens_post`), deretter den raskeste.

| modell | kall | ugyldig JSON | norske stoppord | engelske stoppord | forkastede forslag per sending | emneord 3–8 | tittel ok | tid per sending | merknad |
|---|---|---|---|---|---|---|---|---|---|
| `nb-llama-3.1-8b-instruct` (NbAiLab, 4,9 GB) | 18 | 0.0 % | 34.0 % | 9.4 % | 0,0 | 0/4 | 0/4 | 20,8 s | **kjøringen feilet** med HTTP 500 etter 18 av ca. 27 kall, også ved omkjøring alene (reproduserbart); halv kjøring, tallene er ikke sammenlignbare; engelske stoppord er likevel over grensen |
| `normistral-7b-warm-instruct` (NORA.LLM, 4,4 GB) | 27 | 0.0 % | 36.0 % | 3.9 % | 1,0 | 3/4 | 4/4 | 46,7 s | engelske stoppord over grensen |
| **`borealis-open-4b`** (NbAiLab, Gemma 3, 3,3 GB) | 27 | 3.7 % | 37.6 % | 1.1 % | 0,25 | 3/4 | 3/4 | 51,4 s | **valgt** |
| `borealis-4b` (NbAiLab, 3,3 GB) | 27 | 3.7 % | 33.3 % | 1.6 % | 0,5 | 3/4 | 3/4 | 50,0 s | oppfyller kravene, flere oppdiktede forslag |

Tallene er fra én kjøring per modell (temperatur 0, fast seed) på fire sendinger. Det er et lite og enkelt utvalg.

## Konsekvenser

- **Språkkvaliteten er ikke vurdert av et menneske.** Stoppordandelen sier bare at teksten er norsk og ikke engelsk, ikke at den er god, idiomatisk eller i riktig målform. Katalogutkastet er ikke målt mot noe gullsett og er ikke preregistrert; før det brukes mot et arkiv bør et menneske lese et utvalg.
- **Modellen kan ta feil om navn, steder og datoer.** `katalog.rens_post` forkaster forslag som ikke står i transkripsjonen eller i personvernflaggene og logger dem i `forkastet`. Tittel, emneord og sammendrag sjekkes ikke mot noe.
- **Lisens.** Borealis-open er basert på `google/gemma-3-4b-it`, og HF-kortet oppgir lisensen `gemma` (Gemmas bruksvilkår), ikke en åpen kildekode-lisens. Vilkårene er ikke gjennomgått her; det må gjøres før modellen brukes i en pilot eller et produkt. Modellen lastes ikke ned av repoet.
- **Katalogutkastet er ikke klarert.** Emneord som ligner et nummer forkastes, men sammendraget gjengir det transkripsjonen sier og kan derfor inneholde navn og tall som personvernflaggene har merket (røyktesten 2026-10-26: et telefonnummer sto i et sammendrag). Utkastet er merket «utkast – maskinforslag» og «ikke klarert for publisering» og skal ikke publiseres før et menneske har klarert teksten.
- Tid: ca. 50 sekunder per sending på 45 setninger. For lange sendinger vokser det med antall tidsvinduer (ett kall per minutt tekst).
- En av 27 kall ga ugyldig JSON (3,7 %); `katalog._json` faller tilbake til tomt svar, og feltet blir stående tomt.

## Alternativer som ble vurdert

- **`nb-llama-3.1-8b-instruct`:** falt ut fordi kjøringen feilet reproduserbart med HTTP 500 etter 18 kall (årsaken er ikke undersøkt). Det er ikke et funn om at modellen skriver dårlig norsk; den kan fortsatt være aktuell etter en feilsøking.
- **`normistral-7b-warm-instruct`:** gyldig JSON hver gang, men engelske stoppord over grensen (3,9 %) og flere oppdiktede forslag enn Borealis-open.
- **`borealis-4b`:** oppfyller kravene, men flere forkastede forslag enn `borealis-open-4b`, og HF-kortets lisens er `other`.
- **`borealis-open-12b` (8,2 GB):** ikke testet; for stor til å kjøre sammen med resten av rørledningen på 16 GB uten å risikere swap-vakten (KLAR-ADR-0015).
- **Flerspråklige modeller (`gemma2:9b`, `llama3.1:8b`, `qwen2.5:7b`, `mistral`):** ikke testet; norskspesifikke modeller ble prioritert.
- **Sky-API:** utelukket av KLAR-ADR-0007.
