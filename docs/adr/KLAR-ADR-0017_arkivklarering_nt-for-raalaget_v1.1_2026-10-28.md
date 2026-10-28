---
status: accepted
date: 2026-10-27
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0017: whisper.cpp `-nt` (ingen tidsstempeltokens) bare for rålaget

## Kontekst

`KLAR-EVAL-0011` fant at `nb-whisper-large-verbatim` (rålaget) noen ganger avslutter et dekodingsvindu med `[_EOT_]` uten avsluttende tidsstempeltoken. whisper.cpp setter `result_len = i + 1` bare ved tidsstempeltoken (`src/whisper.cpp`, commit `4834a232`, linje 7389–7390) og kaster derfor teksten etter det første tidsstempeltokenet; vinduet flyttes 0,06 s om gangen til slutten av lyden. I DEV ga det tomt eller under halvparten av referanseordene for 6 av 60 segmenter (10 %). Det er ikke en kodefeil hos oss. Terskler (`no_speech`, `avg_logprob`), DTW, kontekst mellom filer, språkvalg og beam/grådig dekoding er prøvd og forkastet som årsak. Flagget `-nt` (`--no-timestamps`, `whisper_full_params.no_timestamps`) setter `result_len = i + 1` ved slutten av segmentet (linje 7417–7420) og beholder teksten.

Regresjonen på de 60 DEV-segmentene (gren `nt-regresjon`, `eval/dev/nt_regresjon_2026-10-26.md`) med `-nt` på begge lag: rålag-WER 0,258 → 0,137, segmenter med under halvparten av ordene 6 → 0, men **normalisert lag-WER 0,350 → 0,456** (nynorsk 0,405 → 0,628).

## Beslutning

**`-nt` brukes bare for rålaget; det normaliserte laget er uendret.** Bryteren ligger i `transkriber.Oppsett.uten_tidsstempeltokens`, som `finn_oppsett` setter til sann for `ra` og usann for `normalisert`. DTW-ordtidsstemplene (`-nfa -dtw large.v3 -ojf`) beholdes, så unionen av lagenes flagg fortsatt parer flaggene via ordspenn (KLAR-ADR-0012; enhetstest `tests/test_nt.py`: begge lag har ordspenn og et flagg på samme ord i begge lag blir ett unionflagg). Miljøvariabelen `ARKIVKLARERING_MED_TIDSSTEMPELTOKENS=1` slår `-nt` av og gjenskaper tallene «før -nt».

Grunnlag: `KLAR-EVAL-0011` (årsak og tall) og regresjonen på grenen. Ny DEV for de berørte EVAL-ene er kjørt med `scripts/reproduser.sh` (rålaget på nytt; det normaliserte lagets lagrede utdata er gjenbrukt fordi modellens sha256 og alle parametere er uendret, og loggført), og tersklene H1a og H1d i `KLAR-PREREG-0001` er regnet på nytt med uendret regel. Analysekoden er låst med taggen `h4-script-v2`.

## Konsekvenser

- Rålagets tekst begynner ikke lenger midt i en ytring i de tilfellene EVAL-0011 fant. Rålagets WER (H1a, H1d) blir lavere i DEV; de gamle tallene beholdes og merkes «før -nt».
- Rålaget har ikke lenger whisper.cpps segmenttidsstempler fra tidsstempeltokens (ett segment per vindu); cuenes tid kommer fra DTW-ordtidene. Kvaliteten på ordtidene er ikke målt separat (de brukes til paring i unionen).
- Resultater fra før innføringen (EVAL-0002, -0006, -0007, -0008, -0010, H4-tørrtesten, og -0001 hvis berørt) har ny versjon; sammenligninger på tvers av versjonene må ta hensyn til dette.
- Kjent forbehold: ett eksisterende flagg, tre varianter og ett segmentutvalg på seks; effekten av `-nt` på arkivlyd er ikke målt. `suppress_blank` og `max_initial_ts` (bibliotekparametere uten CLI-flagg) er ikke testet.

## Alternativer som ble vurdert

- **Ingen endring:** behold dagens oppsett og dokumenter begrensningen (PREREG-0001 v1.6 (i git-historikken)). Forkastet av eier fordi rålaget mister starten av ytringer i omtrent hvert tiende segment.
- **`-nt` på begge lag:** forkastet; normalisert lag blir klart verre (WER 0,350 → 0,456).
- **`--vad` (Silero):** endret utfallet litt (39 mot 30 av 76 ord) men løste ikke problemet.
- **0,5 s stillhet foran segmentet:** ga 68 av 76 ord, men er et eget grep uten kilde.
- **Grådig dekoding (`-bs 1`):** ga verre utfall (8 av 76).


Versjon 1.1, 2026-10-28 (v1.1: pekere til versjoner som ikke er i treet er merket «(i git-historikken)», og pekere med linjenummer til forrige versjon av et dokument med ny versjon viser til den nye versjonen, samme linje; kontrollert med `scripts/sjekk_pekere.py`, 0 brudd (KLAR-LOG-0005, restfunn etter kontrollen)). Versjon 1.0, 2026-10-26.