---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0016: Talerinndeling med pyannote (anonyme talermerker)
Versjon 1.1, 2026-10-28 (v1.1: venv-stien skrives som i koden, `$ARKIVKLARERING_DATA/venv-diarisering` (`arkivklarering/diarisering.py:20`), ikke som den faste stien på Vault; beslutningen er uendret; v1.0: første versjon).
## Kontekst

Et lydarkiv med flere talere kan ikke klareres uten at det er synlig hvem som sier hva: samtykke, personvernflagg og opplysninger om tredjepersoner gjelder per taler. Rørledningen hadde ingen talerinndeling (det største hullet i arkitekturen). Kravene fra eier: standardløsningen, den samme modellen som WhisperX bruker, anonyme merker (TALER_1, TALER_2 …), ingen navn og ingen stemmegjenkjenning mot kjente personer.

## Beslutning

**`pyannote/speaker-diarization-community-1`** (pyannote.audio 4) er modellen; det er WhisperX' standardmodell (`whisperx/diarize.py`, `KLAR-KILDE-0001`). Modellen er gated på Hugging Face (`gated: auto`) og er lisensiert **CC BY 4.0** (navngivelse kreves; se `NOTICE`). Lisens og vilkår er lest ordrett fra modellkortet og ført i `KLAR-KILDE-0001` før bruk. Tokenet ligger i `.env` (`HF_TOKEN`, gitignorert) og leses bare inne i runner-prosessen; det skrives aldri ut eller logges.

- **Talermerker:** `TALER_1`, `TALER_2` … i den rekkefølgen talerne først snakker i sendingen. Merkene gjelder bare innenfor én sending. Ingen navn og ingen stemmegjenkjenning mot kjente personer; ingen taleravtrykk lagres.
- **Kjøring:** `--taler` i CLI-et (valgfritt, av som standard fordi modellen er gated og krever nettverk ved første lasting). Pyannote kjører i et eget venv (`$ARKIVKLARERING_DATA/venv-diarisering`, på Vault `/Volumes/Vault/arkivklarering/venv-diarisering`; `requirements-diarisering.lock`) via `arkivklarering/_diarisering_runner.py`, så det låste analysemiljøet ikke berøres. Én tung prosess om gangen: talerinndelingen kjøres etter Whisper.
- **Tildeling:** hver cue får taleren med mest tidsoverlapp (`diarisering.tildel_cuer`); ingen overlapp gir ingen taler (`null`). Pyannotes ikke-overlappende inndeling (`exclusive_speaker_diarization`) brukes, slik WhisperX gjør.
- **Utdata:** `segments.json` (talermerke per cue, `taler` parallelt med `tekst`, og `talerinndeling` med turer), OHMS XML (transkripsjonen får linjeprefikset `TALER_n:`; `interviewee` brukes ikke), WebVTT (voice span `<v TALER_n>`). IIIF og MMIF har ikke talermerker ennå.

## Konsekvenser

- **Kvalitet:** målt som DER på NB Samtale validation (CC0) i `KLAR-EVAL-0012`, DEV. Målingen gjelder en konstruert sammenstilling av ytringer, ikke hele opptak, og er ikke sammenlignbar med DER på hele samtaler; den sier ingenting om kvaliteten på arkivlyd, overlappende tale eller båndlyd. Se EVAL-dokumentet for tall og forbehold.
- **Feiltyper å vente:** for mange eller for få talere i en sending, talerbytte midt i en cue (cuen får bare én taler), og at samme person får ulike merker i ulike filer. Merkene er forslag til menneskelig vurdering, ikke en identifikasjon.
- **Personvern:** talerinndeling avslører ikke hvem noen er, men gjør det mulig å følge én stemme gjennom en sending. Behandles som øvrige maskinforslag: lokalt, ikke publisert før et menneske har klarert (KLAR-ADR-0002, -0007).
- **Avhengigheter:** pyannote.audio med torch (stor, eget venv); modellen lastes ned fra Hugging Face første gang. Lisensen (CC BY 4.0) krever navngivelse ved videre bruk av modellen.

## Alternativer som ble vurdert

- **`pyannote/speaker-diarization-3.1`:** MIT-lisensiert og også gated; eldre modell, ikke WhisperX' nåværende standard. Ikke valgt.
- **Talerinndeling med egne triks eller klynging av taleravtrykk:** forkastet; kravet var standardløsningen.
- **Stemmegjenkjenning mot kjente personer:** forkastet av eier.
