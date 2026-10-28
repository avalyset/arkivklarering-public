---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0004: Segmentregel: speech og speech+music transkriberes, music og other aldri

Versjon 1.5, 2026-10-28 (v1.5: lenken til KLAR-EVAL-0001 sier hvilken versjon tallene står i (porten, runde 3 (KLAR-LOG-0005), funn 14); v1.4: Konsekvenser sier «feilklassifisering i segmentøren (standard inaSpeechSegmenter)» i stedet for «i inaVAMOS», fordi standarden i koden er inaSpeechSegmenter (KLAR-ADR-0019, AV-26); regelen er uendret). Versjon 1.3, 2026-10-27 (v1.3: merknad om at `speech+music` og flagget «musikk under tale» bare produseres med inaVAMOS; med standardsegmentøren inaSpeechSegmenter lages de ikke (KLAR-ADR-0019); regelen er uendret). Versjon 1.2, 2026-10-26 (v1.2: påstanden om Koenecke m.fl. strammet inn etter kildekontroll, KLAR-KILDE-0001). v1.1: v1.0 begrunnet regelen med at Whisper dikter opp tekst, og siterte Koenecke m.fl. for stillhet og støy. Kildekontrollen viste at artikkelen ikke sier «særlig i stillhet og støy»; den sier at oppdiktingen er hyppigere for talere med lengre ikke-vokale andeler, og den beskriver også oppdiktede setninger «when no one is speaking in the input audio files», og målingen under viste ingen oppdiktet prosa. Begrunnelsen er skrevet om; regelen er uendret.

## Kontekst

- **Koenecke m.fl. 2024** (<https://arxiv.org/abs/2402.08021>): ca. 1 % av transkripsjonene fra Whisper hadde hele oppdiktede fraser eller setninger, og oppdiktingen var uforholdsmessig hyppigere for talere med lengre andeler ikke-vokal tid, altså pauser i tale (talere med afasi). Artikkelen måler ikke ren stillhet, støy eller musikk som egne lydtyper. Den beskriver oppdiktede setninger «when no one is speaking in the input audio files» og antar bakgrunnsstøy i pauser som mulig årsak; musikk nevnes ikke.
- **Egen måling** ([KLAR-EVAL-0001](../KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v1.5_2026-10-28.md); tallene under er fra v1.1, før `-nt`; i v1.4, med `-nt` i rålaget, skriver begge lag `<|nocaptions|>`): 20 s stillhet, to nivåer hvit støy, rosa støy og syntetisk musikk sendt direkte til whisper.cpp med `-l nn`, én kjøring per modell og lyd. Ingen kjøring ga prosa. NB-Whisper large verbatim skrev «.» med tidskode 0–30 s, og NB-Whisper large skrev `<|nocaptions|>`. Lyden er syntetisk, uten tale foran, og målingen sier ikke noe om pauser inne i tale.
- Tale over musikk er viktig for rettighetsvurderingen og må ha tekst og flagg.

## Beslutning

Bare `speech` og `speech+music` sendes til Whisper. `speech+music` får både tekst og flagget «musikk under tale – vurder rettigheter». `music` merkes «foreslått klipp» og `other` får ingen handling; ingen av dem går til Whisper. Koden avviser det, og en test sjekker det. Whisper-utdata uten ord (`.`, `<|nocaptions|>`) filtreres.

**Merknad (v1.3):** `speech+music` produseres bare med inaVAMOS (det valgfrie tillegget `reproduksjon-h1h2`). Med standardsegmentøren inaSpeechSegmenter finnes ikke klassen: tale over musikk blir `speech` eller `music`, og flagget «musikk under tale – vurder rettigheter» lages ikke ([KLAR-ADR-0019](KLAR-ADR-0019_arkivklarering_inaseg-erstatning_v1.6_2026-10-28.md), «Tale over musikk» og «Hva det betyr for ADR-0004»). Regelen over gjelder fortsatt for de etikettene segmentøren gir.

Begrunnelsen er:

1. Segmenter uten tale har ingenting å transkribere. Målingen viser at modellene likevel skriver utdata som ligner tekst (en cue med «.» over 30 s, et spesialtoken), som en nedstrøms prosess kan vise eller telle som innhold.
2. Utdata over ren musikk kan forveksles med innhold i en klarering.
3. Whisper brukes ikke til noe den ikke er laget for.

Begrunnelsen er **ikke** at Whisper er påvist å dikte opp tekst på stillhet, støy eller musikk. Det er ikke funnet, verken i artikkelen eller i vår måling.

## Konsekvenser

- Ingen tekst for ren musikk eller stillhet. Feilklassifisering i segmentøren (standard inaSpeechSegmenter; inaVAMOS bare for å reprodusere H1 og H2, KLAR-ADR-0019) påvirker hva som blir transkribert; tale merket `music` blir ikke transkribert og må fanges av menneskelig vurdering.
- **Regelen fjerner ikke risikoen Koenecke m.fl. beskriver.** Pauser inne i tale ligger i `speech`-segmenter (og tale slås sammen over gap på høyst 1 s), og oppdiktet tekst der er ikke utelukket. Alle transkripsjoner må derfor vurderes av et menneske, og en måling på ekte arkivlyd med pauser er ikke gjort.
- `speech+music` kan flagges uten at det ligger musikk under (inaVAMOS flagget TTS-tale i røyktesten), så flere flagg enn nødvendig er mulig.

## Alternativer som ble vurdert

- Transkribere alt og filtrere etterpå: forkastet; segmentene har ingenting å transkribere, og utdata kan forveksles med innhold.
- Bare `speech`: forkastet i v0.1 fordi tale over musikk da ville mangle tekst og flagg.
