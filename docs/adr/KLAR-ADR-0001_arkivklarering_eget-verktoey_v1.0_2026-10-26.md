---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0001: Arkivklarering er et eget verktøy; norsk-tale er bare referanse

## Kontekst

norsk-tale er et diktering- og kalibreringsprosjekt med egen preregistrering. Arkivklarering har et annet formål, andre brukere og andre krav til personvern.

## Beslutning

Arkivklarering bygges som eget repo med eget navnerom, egne beslutninger og egen preregistrering. norsk-tale brukes bare som referanse (for eksempel for whisper.cpp-oppsettet), og kode eller data flyttes ikke mellom prosjektene uten en egen beslutning.

## Konsekvenser

Ingen delt kodebase å holde i takt. Funn og tall fra norsk-tale kan ikke siteres som måling av arkivklarering. Noe oppsett må gjentas.

## Alternativer som ble vurdert

- Bygge videre i norsk-tale: forkastet fordi formål og preregistreringer ville blandes.
- Felles bibliotek: forkastet inntil det finnes en gjenbruk å begrunne det med.
