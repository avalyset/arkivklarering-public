---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0003: MMIF som internt format (CLAMS)

Versjon 1.2, 2026-10-27 (v1.2: implementeringsstatusen rettet etter koden: siden v0.4 skrives MMIF 1.2.0 som eksport med `mmif-python` 1.5.4 (`eksport.bygg_mmif`/`skriv_mmif`, kalt fra `cli.py`), TODO-en i `eksport.py` er borte, men komponentene utveksler ennå ikke data via MMIF; beslutningen er uendret; v1.1: «sporbarhet per verktøy og kjøring» strammet inn til det kilden dekker, KLAR-KILDE-0001 CL-09; beslutningen er uendret; v1.0: første versjon).

## Kontekst

Komponentene (segmentering, transkripsjon, flagg, katalog) trenger et felles utvekslingsformat der resultatene kan spores til verktøyet som laget dem. I MMIF har hver visning (view) metadata om applikasjonen som laget den og opprettelsesdato (Rim m.fl., LREC 2022).

## Beslutning

MMIF fra CLAMS-prosjektet (Brandeis University og GBH Archives) velges som internt format. I v0.1 var det ikke implementert (TODO i `eksport.py`). Fra v0.4 skrives MMIF som eksport (`eksport.skriv_mmif`, `mmif-python`), men komponentene utveksler ennå ikke data via MMIF; `segments.json` er fortsatt et midlertidig format.

## Konsekvenser

Komponentene kan byttes ut uten å endre resten. Utvekslingen mellom komponentene må gå over til MMIF (eksporten finnes), og `segments.json` utfases. Spesifikasjonen versjoneres av andre (1.2.0 ved kontroll 2026-10-26).

## Alternativer som ble vurdert

- Eget JSON-format: enklere nå, men uten sporbarhet og uten økosystem.
- IIIF som internt format: laget for presentasjon, ikke for analyseresultater.
