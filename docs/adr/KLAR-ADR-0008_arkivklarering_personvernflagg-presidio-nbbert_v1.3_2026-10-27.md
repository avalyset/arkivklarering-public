---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0008: Personvernflagg med Presidio (norsk oppsett) og NB-BERT-base-ner

Versjon 1.3, 2026-10-27 (v1.3: «ordnes etter risiko» merket som plan, ikke implementert; koden ordner flaggene etter tid). Versjon 1.2, 2026-10-26 (v1.2: forfatterangivelsen for CLEANUP-guiden rettet etter kildekontroll, KLAR-KILDE-0001). v1.1: implementert i v0 (`personvern.py`); se KLAR-ADR-0012 for terskel og prioritering og KLAR-EVAL-0005 for måling.

## Kontekst

Kandidater til personopplysninger må flagges med tidskode og ordnes etter risiko for menneskelig vurdering. **Plan, ikke implementert (v1.3):** flaggene ordnes i dag etter tid, ikke etter risiko: `arkivklarering/personvern.py:223` sorterer flaggene i ett lag etter start, stopp, kategori og kilde, og `:321` sorterer unionen etter start, stopp, kategori og lag. Ingen kø eller risikoordning er bygget (den hører til godkjenningsflaten, KLAR-ARK-0006 «Etter v1.0»).

## Beslutning

Presidio er rammeverket, med norsk oppsett etter CLEANUP-guiden (forfatter: «NR and NAV through the CLEANUP-project»; NR = Norsk Regnesentral er vår utvidelse av forkortelsen), og NB-BERT-base-ner for navn. Flagg er forslag. Implementert som v0 i `personvern.py`: Presidio med `nb_core_news_md` registrert for `nb` og `nn`, NB-BERT-base-ner som egen gjenkjenner, mønstre for dato, fødselsår, telefon og fødselsnummer, og nøkkelordlister i `vokabular/sensitivt_*.txt`.

## Konsekvenser

Guiden dekker bokmål med spaCy og ikke nynorsk; spaCy har ingen nynorskmodell, så `nn` bruker bokmålsmodellen. Hvordan NB-BERT-base-ner og spaCy gjør det på nynorsk er målt på NorNE (KLAR-EVAL-0005), ikke på tale. Gjenkalling og presisjon må måles mot fasit fra full lytting før flaggene brukes til å spare lyttetid.

## Alternativer som ble vurdert

- Regex og ordlister alene: forkastet som eneste lag; fanger ikke navn.
- Språkmodell til flagging: ikke valgt; ikke deterministisk.
