"""Deterministisk navnekorrigering mot en alias-tabell. STUBBE: ikke implementert.

Plan:
  - Alias-tabell (CSV/TSV under versjonskontroll) med lokale sted- og gårdsnavn og
    institusjonsnavn: «feil form» -> «riktig form», med kilde og dato per rad.
  - Eksakt strengmatch på hele ord, ingen uklar matching. Uklar matching kan endre et navn
    til et annet, og det er uakseptabelt i et klareringsløp.
  - Hver erstatning loggføres (tidskode, før, etter, rad i tabellen) og kan reverseres. Det
    verbatime laget røres aldri; korrigeringen lager et eget lag.
  - Normalisert lag (nynorsk eller bokmål) bygges her eller i et eget steg, med samme logg.
Se docs/KLAR-ARK-0001, § 3.
"""


def korriger(cues, alias_tabell):
    raise NotImplementedError("entiteter.py er en stubbe i v0")
