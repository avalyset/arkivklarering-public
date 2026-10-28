---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0009: Eksport til WebVTT og IIIF Presentation 3

Versjon 1.1, 2026-10-27 (v1.1: implementeringsstatusen rettet etter koden: IIIF Presentation 3 er implementert og testet, ikke TODO; OHMS XML og MMIF skrives også (KLAR-ADR-0003); beslutningen er uendret; v1.0: første versjon).

## Kontekst

Transkripsjon må kunne vises i avspillere og i arkivets visere.

## Beslutning

WebVTT per lag og `segments.json` er implementert. IIIF Presentation 3 (transkripsjon som merknad med motivasjonen `supplementing` på lydens tidsakse) er også implementert (v1.1): `arkivklarering/eksport.py` (`bygg_iiif_manifest`, `valider_iiif`, `skriv_iiif_manifest`) lager ett manifest per sending etter IIIF Cookbook 0231 og 0219, med lyden som `painting`-annotasjon og hvert transkripsjonslag som `supplementing`-annotasjoner (én for WebVTT-fila og én per cue), og `arkivklarering/cli.py` skriver `<navn>.iiif.json` ved hver kjøring. Testene (`tests/test_eksport_formater.py`) prøver manifestet mot validatoren og validatoren mot den offisielle oppskriften 0219 (README «Installasjon»). I tillegg skrives OHMS XML og MMIF (README «Hva verktøyet gjør», punkt 5; KLAR-ADR-0003).

## Konsekvenser

Åpne, utbredte formater. At `supplementing` er riktig motivasjon for transkripsjon er en tolkning av spesifikasjonen som må prøves mot en viser. v1.1: manifestet er prøvd mot repoets validator og oppskriften 0219, ikke i en IIIF-viser.

## Alternativer som ble vurdert

- Bare WebVTT: forkastet; viser ikke segmentdisposisjon og flagg.
- Proprietært arkivformat: forkastet.
