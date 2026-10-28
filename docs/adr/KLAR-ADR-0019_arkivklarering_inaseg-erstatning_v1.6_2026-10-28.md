---
status: vedtatt for v1.0 (alternativ A)
date: 2026-10-27
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0019: inaSpeechSegmenter erstatter inaVAMOS i verktøyet og i H4

Versjon 1.6, 2026-10-28 (v1.6: påstandene om README og setup.py ved v0.8.0 er tatt ut, fordi ingen lagret kilde dekker dem (porten, runde 3 (KLAR-LOG-0005), funn 12); v1.5: kildene for PyPI-metadataene, `remote_utils.py`, release «interspeech23» og VBx-lisensene er hentet og registrert (KLAR-KILDE-0001 IS-02–IS-06, K130–K134), og sitatet «Classification models used in inaSpeechSegmenter», som ikke har kilde, er fjernet; «tale over musikk blir `speech`» har fått «eller `music`» som i «Tale over musikk»; venv-stiene skrives som i koden (`$ARKIVKLARERING_DATA/venv-inaseg`); linjenumrene for segmenteringskallet gjelder HEAD, med linjene ved `testkjoring-v2` i parentes; beslutningen er uendret; v1.4: H4 gjennomføres ikke i v1.0 (AV-27, Eiriks beslutning 2026-10-27); punktet om H4 i beslutningen er merket med det, og valget av segmentør for H4 gjelder bare hvis H4 gjennomføres senere; ellers uendret; v1.3: standard segmentering i koden er inaSpeechSegmenter og inaVAMOS er valgfritt tillegg `reproduksjon-h1h2` (AV-26, tag `testkjoring-v5`); «Hva koden gjør» og Kontekst rettet tilsvarende; ellers uendret; v1.2: URL i lisenssitatet utelatt (kilderegister); v1.1: sensitivitetskjøringen av H1 og H2 utgår (eiers endring); v1.0: vedtatt av eier for v1.0 med alternativ A; v0.1: kladd på grenen `inaseg-erstatning`).

## Beslutning (eier, 2026-10-27)

- **Alternativ A for v1.0.** Verktøyet bruker inaSpeechSegmenter 0.8.0 (`segment_inaseg.py`, eget venv `$ARKIVKLARERING_DATA/venv-inaseg` (`arkivklarering/segment_inaseg.py:27`; på Vault `/Volumes/Vault/arkivklarering/venv-inaseg`), `requirements-inaseg.lock`). Tale over musikk blir `speech` og transkriberes, eller `music` og transkriberes ikke (se «Tale over musikk»); flagget «musikk under tale – vurder rettigheter» bortfaller fra segmenteringen. **B og C står åpne for produktet** (se «Tale over musikk»); veikartet fører PANNs/AST (B/C) etter v1.0.
- **H4 kjøres med inaSpeechSegmenter** (`ARKIVKLARERING_SEGMENTERING=inaseg` satt av `scripts/kjor_testdel.sh` for H4; kodetagg `testkjoring-v4`, fra AV-26 `testkjoring-v5`), besluttet før noen H4-data er sett. **v1.4: H4 gjennomføres ikke i v1.0** (AV-27, Eiriks beslutning 2026-10-27; ingen H4-data er samlet inn); `scripts/kjor_testdel.sh` setter fortsatt `inaseg` for H4, men H4 kjøres ikke i v1.0. inaVAMOS brukes ikke lenger fra 2026-10-27.
- **H1 og H2 står som preregistrert** (inaVAMOS). H3 bruker ingen segmentering.
- **Standard i koden er inaSpeechSegmenter** (AV-26 i `KLAR-LOG-0003`, tag `testkjoring-v5`): uten miljøvariabelen, eller med `ARKIVKLARERING_SEGMENTERING=inaseg`, brukes inaSpeechSegmenter i CLI, `arkivklarering/segment.py` og `eval/dev/felles.py`. inaVAMOS er det valgfrie tillegget `reproduksjon-h1h2` (Pantagruel Research-only License; bare forskning), ikke en kjerneavhengighet, og brukes bare med `ARKIVKLARERING_SEGMENTERING=inavamos` for å reprodusere H1 og H2.

## Vektlisensen (ordrett, og at den er uklar)

Lisensen for **vektene** er uklar. Ingen kilde oppgir en egen lisens for dem, og ingen kilde oppgir NC- eller forskningsvilkår. Treningsdata er ikke omtalt for de tre Keras-modellene.

- `LICENSE` (ina-foss/inaSpeechSegmenter, tagg v0.8.0) L1: «The MIT License». L3: «Copyright (c) 2018 Ina (David Doukhan - […])». L5–9: «Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software». MIT-teksten nevner «software and associated documentation files»; vektfilene nevnes ikke.
- PyPI (0.8.0): `license = 'MIT'`, classifier «License :: OSI Approved :: MIT License»; hjulet `inaspeechsegmenter-0.8.0-py3-none-any.whl` er 39 345 byte (KLAR-KILDE-0001 IS-02, K130). Pakken inneholder bare kode; vektene ligger ikke i pakken og, ved v0.8.0, heller ikke i repoet. De lastes ned ved kjøring fra GitHub-releases (`remote_utils.py` L4–15 ved v0.8.0: adressene for releasene `models` og `interspeech23` og hvilke vektfiler som hentes fra hver; IS-03, K131).
- Ingen av de lagrede kildene (LICENSE, K119; PyPI-metadataene, K130; releasen «interspeech23», K132) nevner ordene model, weights, hdf5, onnx eller pretrained i lisenssammenheng. README og setup.py ved v0.8.0 er ikke lagret som kilder, og denne ADR-en sier ingenting om dem.
- Release «interspeech23» (kjønns- og x-vektor-vektene, **ikke brukt** med `detect_gender=False`): «final.onnx and raw81.pth are pretrained X-vector Resnet101 architectures, obtained from VBX project (Brno University of Technology)» (IS-04, K132). VBx-README: «Licensed under the Apache License, Version 2.0», uten å nevne modellfilene (IS-05, K133); `LICENSE` i treningsoppskriften `phonexiaresearch/VBx-training-recipe` er «Attribution-NonCommercial 4.0 International» (IS-06, K134), og ingen kilde knytter den til de publiserte vektene.

## Kontekst

- Segmenteringen (`arkivklarering/segment.py`) brukte inaVAMOS 0.1.1 som standard frem til AV-26 (Pantagruel Research-only License; art. 3 forbyr bruk «in the course of a commercial activity», se lisenslesingen 2026-10-27). H1, H2 og H4 kaller segmenteringen (`kjor_dev.py:139`, `felles.py:113` via `kjor_flaggoverlevelse_ord.py:264` og `kalibrering/kjor_h4.py:134` på HEAD; ved `testkjoring-v2`, som H1–H3 ble kjørt fra, `felles.py:109` og `kjor_flaggoverlevelse_ord.py:261`); H3 gjør det ikke.
- inaSpeechSegmenter 0.8.0 (INA, `ina-foss/inaSpeechSegmenter`) er MIT-lisensiert som programvare (`LICENSE` L1–7: «The MIT License», «this software and associated documentation files»). **Lisensen for vektene er uklar:** vektene ligger ikke i repoet ved v0.8.0 eller i PyPI-pakken, men lastes ned fra GitHub-releases (`remote_utils.py` L4–15, IS-03), og ingen av de lagrede kildene (LICENSE, PyPI-metadataene, release-notatene) omtaler vektene lisensmessig. Treningsdata for de tre Keras-modellene er ikke omtalt i disse kildene. Release «interspeech23» (kjønns- og x-vektor-vektene) sier «obtained from VBX project (Brno University of Technology)» for `final.onnx` og `raw81.pth` (fila heter `raw_81.pth` i releasen; IS-04); VBx-README sier Apache-2.0 uten å nevne modellfilene (IS-05), og treningsoppskriften `phonexiaresearch/VBx-training-recipe` er CC BY-NC 4.0 (IS-06; ingen kilde knytter den til de publiserte vektene). Ingen kilde oppgir NC- eller forskningsvilkår for vektene.
- Kjøreren bruker `detect_gender=False` og `vad_engine="smn"`. Da lastes **bare** `keras_speech_music_noise_cnn.hdf5` (3 244 808 byte, sha256 `f04b5e3c86fa2e81666d106b0867350fe7858c7bd006c2a74c27b5b45507e7d8`, lagret under `/Volumes/Vault/arkivklarering/cache/keras/inaSpeechSegmenter/`); kjønns- og VBx-vektene lastes ikke.

## Hva koden gjør

- `arkivklarering/segment_inaseg.py` og `_inaseg_runner.py`: inaSpeechSegmenter i eget venv (`$ARKIVKLARERING_DATA/venv-inaseg`, `arkivklarering/segment_inaseg.py:27`; `requirements-inaseg.lock`, TensorFlow bare der), kalt som subprosess med JSON inn og ut (mønster som `diarisering.py` og `_diarisering_runner.py`). Samme signatur som `segment.segmenter`: `segmenter(lydfil, enhet) -> [(etikett, start, stopp)]`.
- `segment.segmenter` velger kjøreren med miljøvariabelen `ARKIVKLARERING_SEGMENTERING` (`segment.valgt_segmentering`): `inaseg` er standard, også når variabelen mangler eller er tom; `inavamos` kjører inaVAMOS (tillegget `reproduksjon-h1h2`, importeres bare da); andre verdier, eller `inavamos` uten tillegget, gir `SegmenteringFeil` med melding om installasjon og lisens. CLI skriver hvilken segmentør som er brukt. `eval/dev/felles.py` bruker `segment.segmenter` og dermed samme valg; `kjor_h4.py` er ikke endret.
- `pyproject.toml`: ingen kjerneavhengighet til inaVAMOS; `reproduksjon-h1h2 = ["inaVAMOS>=0.1.1"]`. inaSpeechSegmenter installeres i eget venv fra `requirements-inaseg.lock`.
- `scripts/kjor_testdel.sh` setter `ARKIVKLARERING_SEGMENTERING=inavamos` for H1 og H2 (reproduksjon av de preregistrerte kjøringene) og `inaseg` for H4; H3 segmenterer ikke og får kallerens miljø. `scripts/reproduser.sh` og `scripts/verifiser_uendret.py` setter `inavamos` der de sammenligner mot lagrede inaVAMOS-resultater (`reproduser.sh` steg 9, H4, med `inaseg`).
- Etikettkart: `speech`, `male`, `female` → `speech`; `music` → `music`; `noise`, `noEnergy` → `other`. Naboer med samme etikett slås sammen. Ukjente etiketter beholdes og sendes til menneskelig vurdering av `bygg_tidslinje`.

## Tale over musikk

inaSpeechSegmenter har **ingen klasse for tale over musikk**. `speech+music` blir derfor aldri produsert. Alternativer:

- **A (vedtatt for v1.0):** tale over musikk får det modellen gir, i praksis `speech` (transkriberes) eller `music` (ikke transkribert, «foreslått klipp»). Flagget «musikk under tale – vurder rettigheter» faller bort.
- **B (åpen for produktet):** som A, men `music`-segmenter kortere enn en grense som ligger mellom to talesegmenter sendes til «menneskelig vurdering» i stedet for «foreslått klipp». Ikke implementert.
- **C (åpen for produktet):** et andre pass som søker tale i `music`-segmentene (f.eks. en VAD som Silero VAD, MIT) og setter `speech+music` der det finnes. Ikke implementert; ny avhengighet og egen måling.

DEV-sammenligningen (`eval/dev/sammenlign_inaseg_dev.py`, resultater i `eval/dev/inaseg_sammenligning_dev_2026-10-27.json`, kun DEV og røyktest, inaVAMOS ikke kjørt):

- NB Samtale validation (60 segmenter, 396,9 s): enighet per sekund 92,9 % (strengt) og 94,3 % når `speech+music` regnes som `speech`. inaVAMOS' `speech` → ny `speech`: 99,9 %. inaVAMOS' `other` (27,5 s) → ny `speech` 78,2 %, `other` 21,8 %.
- **inaVAMOS `speech+music` i DEV (2 intervaller, 5,66 s, begge i `nb-33_2350240-2357030`):** 100 % `speech` i ny kjører; begge transkriberes fortsatt.
- **Røyktestlydene** (TTS med musikk under tale, `rokytest` og `rokytest_personvern`): alle sju inaVAMOS-`speech+music`-intervaller (18,5 s) ble `speech` i ny kjører og transkriberes fortsatt; inne i de opprinnelige «musikk under tale»-intervallene ble 100 % merket `speech`. Flagget faller bort i alle.
- inaVAMOS `speech` → ny `music`: 0 s i DEV; inaVAMOS `music` (0,7 s i DEV) → ny `speech`.

## Hva det betyr for ADR-0004

- Regelen «speech og speech+music transkriberes, music og other aldri» står som den er, men `speech+music` blir en tom klasse med ny kjører: tale over musikk transkriberes bare hvis modellen kaller den `speech`.
- ADR-0004-konsekvensen «tale merket `music` blir ikke transkribert og må fanges av menneskelig vurdering» gjelder like mye. DEV gir ingen tilfelle der ny kjører merker inaVAMOS-tale som `music`, men DEV har bare to `speech+music`-intervaller og røyktesten er syntetisk; det er ikke målt på ekte arkivlyd med musikk.
- **Rettighetsflagget** («musikk under tale – vurder rettigheter», `FLAGG_MUSIKK_UNDER_TALE`) produseres ikke lenger av segmenteringen. Det er en funksjon som bare alternativ C (eller en annen mekanisme) kan gi tilbake.

## Åpne punkter

- Lisensen for vektene er uklar (se over); den er ikke avklart med INA.
- inaVAMOS' lisens: EcoDecos dekning under Pantagruel Research-only License er uavklart (AV i `KLAR-LOG-0003`). Å lese eksisterende inaVAMOS-utdata i DEV-sammenligningen er ikke avklart mot begrepet «Derivatives».
- B og C (musikk under tale): vurderes etter v1.0 (PANNs/AST, Silero VAD).
- ADR-0004 er ikke endret: regelen står, men `speech+music` er en tom klasse med inaSpeechSegmenter (se over).
