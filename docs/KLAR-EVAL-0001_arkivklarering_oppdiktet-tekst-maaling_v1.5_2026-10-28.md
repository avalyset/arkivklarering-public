# Oppdiktet tekst: whisper.cpp direkte på stillhet, støy og musikk (2026-10-26)

Versjon 1.5 (2026-10-28; v1.5: pekere til versjoner som ikke er i treet er merket «(i git-historikken)», og pekere med linjenummer til forrige versjon av et dokument med ny versjon viser til den nye versjonen, samme linje; kontrollert med `scripts/sjekk_pekere.py`, 0 brudd (KLAR-LOG-0005, restfunn etter kontrollen); v1.4: kjøretidene per kjøring er generert på nytt fra JSON-fila v1.3 (`docs/KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v1.3_2026-10-27.json`, kjøringen med `-nt`) med formatet i `scripts/mal_oppdiktet_tekst.py`; v1.3 av md-fila hadde kjøretidene fra JSON v1.1, fra før `-nt`; utdataene og tolkningen er uendret; v1.3: rålaget kjøres nå med `-nt` (KLAR-ADR-0017), og skriver da spesialtokenet `<|nocaptions|>` i stedet for «.» på alle fem lydene; ellers uendret; v1.2: én setning strammet inn etter kildekontroll, KLAR-KILDE-0001; v1.1: v1.0 hadde ikke rosa støy). Dokumentasjon på hvorfor rørledningen aldri sender `music` eller `other` til Whisper. Syntetisk lyd (20 s hver; hvit støy med standardavvik 0,2 er klippet ved ±1), `-l nn`, whisper.cpp med standardinnstillinger, én kjøring per modell og lyd. Sier hva modellene gjør på akkurat denne lyden, ikke hvor ofte det skjer i et arkiv. Generert av `scripts/mal_oppdiktet_tekst.py`.

## ra · stillhet (digital nuller)
Modell `nb-whisper-large-verbatim.ggml-model.bin`, sha256 `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d`, 6.2 s.

- 0.00–30.00 s: «<|nocaptions|>»

## ra · svak hvit støy (amplitude 0,01)
Modell `nb-whisper-large-verbatim.ggml-model.bin`, sha256 `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d`, 5.5 s.

- 0.00–30.00 s: «<|nocaptions|>»

## ra · hvit støy (amplitude 0,2)
Modell `nb-whisper-large-verbatim.ggml-model.bin`, sha256 `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d`, 5.8 s.

- 0.00–30.00 s: «<|nocaptions|>»

## ra · rosa støy (1/f, toppverdi 0,5)
Modell `nb-whisper-large-verbatim.ggml-model.bin`, sha256 `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d`, 5.5 s.

- 0.00–30.00 s: «<|nocaptions|>»

## ra · syntetisk musikk (arpeggio)
Modell `nb-whisper-large-verbatim.ggml-model.bin`, sha256 `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d`, 5.4 s.

- 0.00–30.00 s: «<|nocaptions|>»

## normalisert · stillhet (digital nuller)
Modell `nb-whisper-large.ggml-model.bin`, sha256 `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76`, 3.2 s.

- 0.00–30.00 s: «<|nocaptions|>»

## normalisert · svak hvit støy (amplitude 0,01)
Modell `nb-whisper-large.ggml-model.bin`, sha256 `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76`, 3.6 s.

- 0.00–30.00 s: «<|nocaptions|>»

## normalisert · hvit støy (amplitude 0,2)
Modell `nb-whisper-large.ggml-model.bin`, sha256 `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76`, 3.6 s.

- 0.00–30.00 s: «<|nocaptions|>»

## normalisert · rosa støy (1/f, toppverdi 0,5)
Modell `nb-whisper-large.ggml-model.bin`, sha256 `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76`, 3.6 s.

- 0.00–30.00 s: «<|nocaptions|>»

## normalisert · syntetisk musikk (arpeggio)
Modell `nb-whisper-large.ggml-model.bin`, sha256 `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76`, 5.1 s.

- 0.00–30.00 s: «<|nocaptions|>»

## Tolkning

- **Ingen av de ti kjøringene ga prosa.** Rålaget (verbatim, nå med `-nt`; i v1.2 uten `-nt` skrev det bare «.») og normalisert lag skrev begge spesialtokenet `<|nocaptions|>` for hele 30 s-vinduet whisper.cpp pakker lyden i, på alle fem lydene: stillhet, to nivåer hvit støy, rosa støy og musikk. Utdataene er uten ord, men de er ikke «ingen tekst»: en nedstrøms prosess som teller cuer eller viser teksten uten filter ville vist dem, og rålagets cue har tidskode 0–30 s. Koden filtrerer slike cuer (`er_lydmerke`), og det er testet.
- **Dette er ikke en gjengivelse av funnet til Koenecke m.fl. 2024, og det motbeviser det ikke.** Artikkelen finner at ca. 1 % av transkripsjonene hadde oppdiktede fraser, og at oppdiktingen var uforholdsmessig hyppigere for talere med lengre andeler ikke-vokal tid, altså pauser i tale. Her er lyden syntetisk, hvert tilfelle er kjørt én gang per modell, det går ingen tale foran, og lyden er ikke tale med pauser. Målingen sier derfor lite om pauser inne i tale, som er der artikkelen finner hyppigst oppdiktet tekst; artikkelen beskriver også oppdiktede setninger «when no one is speaking in the input audio files».
- **Hva målingen støtter:** på ren stillhet, støy og musikk, uten tale i vinduet, skriver disse to modellene med `-l nn` ikke prosa. Den støtter ikke at Whisper dikter opp tekst på slik lyd.
- **Regelen «music og other går aldri til Whisper» står derfor ikke på hallusinasjon som påvist atferd** (se KLAR-ADR-0004 v1.1 (i git-historikken)): det er ingenting å transkribere i slike segmenter, og utdata som ser ut som tekst over ren musikk kan forveksles med innhold.
