---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0005: To lag: NB-Whisper large verbatim (rå) og large -l nn (normalisert)

## Kontekst

Revisjon og personvernflagging trenger en ordrett tekst. Brukere og søk trenger lesbar tekst. NB AI-Lab publiserer en verbatim-variant og en standardvariant av large.

## Beslutning

Rålaget er `NbAiLab/nb-whisper-large-verbatim` (ggml), normalisert lag er `NbAiLab/nb-whisper-large` med `-l nn`. Hvert lag er et eget pass over de samme segmentene, ett om gangen. sha256 sjekkes mot `modeller.lock.json` før kjøring.

## Konsekvenser

Versjon 1.3, 2026-10-28: rålagets tidskoder er segmentnivå bare med `--ingen-ordtider`; som standard kommer cuenes tider fra DTW-ordtidene (Konsekvenser, siste avsnitt); beslutningen er uendret. Versjon 1.2: flagg fra de to lagene slås sammen til én liste (union, `personvern.slaa_sammen_lag`). Samme kategori og overlappende tid blir ett flagg med begge lagenes utdrag og tidsgrenser, kildelag («ra», «normalisert» eller «begge») og høyeste score. Et flagg som bare finnes i ett lag beholdes alltid. Unionen kan bare gi flere treff enn hvert lag alene; prisen er flere flagg uten motstykke i det andre laget (KLAR-EVAL-0006).

Versjon 1.1: personvernflagg lages på begge lag (KLAR-ADR-0012). Rålaget har små bokstaver uten tegnsetting, og navnegjenkjenningens recall faller kraftig der (KLAR-EVAL-0005), så det normaliserte laget er det som bærer flagg for navn og steder. «Rålaget er grunnlaget for personvernflagging» gjelder ikke lenger; rålaget er grunnlaget for revisjon.

To transkripsjoner å lagre og vise. Dobbel kjøretid. Verbatim-modellen gir via whisper.cpp ofte én cue med tidskode for hele 30 s-vinduet. Som standard ber rørledningen om DTW-ordtidsstempler (`-nfa -dtw large.v3 -ojf`), og cuene lages fra ordtidene og grupperes etter pauser og setningsslutt (`arkivklarering/cli.py:83`, `arkivklarering/transkriber.py:158`, KLAR-ADR-0017:24). Bare med `--ingen-ordtider` (`arkivklarering/cli.py:47`) brukes whisper.cpps segmenttider, begrenset til segmentet; da er rålagets tidskoder segmentnivå, ikke setningsnivå. «Normalisert» betyr modellens standardstil, ikke normalisering til nynorsk eller bokmål; den kommer med alias-tabellen. Utviklingsmålingen (DEV) viser hvordan lagene skårer og er ikke pilotkvalitet.

## Alternativer som ble vurdert

- Ett lag: forkastet; ordrett og lesbar tekst har ulike formål.
- Medium-modell: forkastet etter at large var tilgjengelig lokalt; ikke målt mot large.
