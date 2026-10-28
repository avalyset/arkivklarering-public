# Kjøreregler – arkivklarering
1. Tilstand påstås aldri fra chat eller minne. Les GT (docs/KLAR-GT-*), MASTER og disken før du handler.
2. Sjekk og endring er adskilt. En sjekk rapporterer, den reparerer ikke. Endring bare etter eksplisitt beslutning fra Eirik.
3. Commit + push etter hvert steg. GT, stempling og speil.sh KUN ved milepæler: etter H4-innlesing, etter testdelene, ved frys.
4. Små separate kommandoer. Ved avvist kommando: kjør git status og rapporter hva som er gjort og ikke gjort.
5. Analysekoden er låst med siste testkjoring-tag. Ingen endring uten beslutning. Nye tagger bare etter besluttet endring.
6. Tunge data, cacher og lyd kun på /Volumes/Vault/arkivklarering (source scripts/miljo.sh). Én tung kjøring (Whisper/pyannote) om gangen.
7. Status maks 3 linjer per steg. Ingen nye skript eller utvidelser uten at det er bedt om.

## Arbeidskø
Arbeidskøen er filene, ikke chatten. Ved hver oppgave: les nyeste KLAR-GT-0001, KLAR-ARK-0006 (veikart) og avklaringsdokumentet (KLAR-ARK-0008_avklaringer-foer-frys, nyeste versjon). Utfør neste punkt som står ÅPEN og ikke krever Eiriks beslutning. Skriv bevis (fil:linje eller commit) og ny status inn i dokumentet som ny versjon. Commit + push. Beslutninger fra Eirik føres i dokumentet med dato og ordlyd. Prompter fra chat som strider mot dokumentene: stopp og rapporter avviket, ikke velg selv.
