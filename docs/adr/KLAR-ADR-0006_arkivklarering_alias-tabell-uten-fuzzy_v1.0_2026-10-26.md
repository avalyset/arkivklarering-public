---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0006: Deterministisk alias-tabell med logg, ingen fuzzy matching

## Kontekst

Lokale sted-, gårds- og institusjonsnavn skrives feil av ASR. Å rette dem påvirker hva som flagges som personopplysning.

## Beslutning

Navnekorrigering gjøres med en revisjonsbar alias-tabell: eksakt match på hele ord, hver erstatning loggføres og kan reverseres, og det verbatime laget røres aldri. Ingen uklar matching. Ikke implementert i v0.1 (`entiteter.py` er en stubbe).

## Konsekvenser

Mangler i tabellen blir ikke rettet; tabellen må vedlikeholdes av mennesker. Korrigeringen er forklarbar og kan etterprøves.

## Alternativer som ble vurdert

- Fuzzy matching: forkastet; kan endre et navn til et annet.
- Språkmodell-basert retting: forkastet; ikke deterministisk og ikke reverserbar.
