# KLAR-GT-0001: Ground truth (generert fra disk)

**Tilstand påstås aldri fra minne eller chat. Les denne fila eller disken.**

Versjon 1.35. Generert 2026-10-28T09:05:17+01:00 av `scripts/ground_truth.py`. Alt utenom «Håndført» er lest fra disk ved generering. HEAD under er commiten som var utsjekket da fila ble generert; GT-fila selv committes etterpå.

## Git og GitHub

- HEAD: `e1fac8a9661680ab3985b65e095c1738ad415078` (Steg 6.1 forberedelse: gt_fast.md fører det offentlige repoet (URL, commit), DOI-ene og OSF-statusen (embargoslutt bedt om, venter på godkjenning); ARK-0008 v1.15 merker GT v1.34; KILDE v1.19)
- gren: `main`
- remote: `https://github.com/avalyset/arkivklarering.git`
- origin/main: `e1fac8a9661680ab3985b65e095c1738ad415078`
- visibility (gh repo view): `PRIVATE https://github.com/avalyset/arkivklarering main`
- token-vakt: OK: gh bruker keyring, konto = avalyset, upstream-lesetilgang bekreftet (kelkalot/simpleaudit pull=true).
- arbeidstre: rent

## Modellfiler

- ra: `/Volumes/Vault/arkivklarering/modeller/nb-whisper-large-verbatim.ggml-model.bin` (3095033483 byte), sha256 `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d`, stemmer med lock
  - repo-symlink: `/Users/eirikbottennicolaysen/dev/arkivklarering/modeller/nb-whisper-large-verbatim.ggml-model.bin` -> `/Volumes/Vault/arkivklarering/modeller/nb-whisper-large-verbatim.ggml-model.bin`
- normalisert: `/Volumes/Vault/arkivklarering/modeller/nb-whisper-large.ggml-model.bin` (3095033483 byte), sha256 `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76`, stemmer med lock
  - repo-symlink: `/Users/eirikbottennicolaysen/dev/arkivklarering/modeller/nb-whisper-large.ggml-model.bin` -> `/Volumes/Vault/arkivklarering/modeller/nb-whisper-large.ggml-model.bin`

## Tester

- `pytest -q` (rask del, `-m 'not tung'`): 216 passed, 3 deselected in 64.55s (0:01:04)

## KLAR-dokumenter

- docs/KLAR-ARK-0001_arkivklarering_arkitektur_v1.10_2026-10-28.md: ARK-0001, v1.10, 2026-10-28
- docs/KLAR-ARK-0002_arkivklarering_navnekonvensjon_v1.6_2026-10-28.md: ARK-0002, v1.6, 2026-10-28
- docs/KLAR-ARK-0003_arkivklarering_nummerregister_v1.27_2026-10-28.md: ARK-0003, v1.27, 2026-10-28
- docs/KLAR-ARK-0004_arkivklarering_modellkort_v1.9_2026-10-28.md: ARK-0004, v1.9, 2026-10-28
- docs/KLAR-ARK-0005_arkivklarering_datablad-manus_v1.12_2026-10-28.md: ARK-0005, v1.12, 2026-10-28
- docs/KLAR-ARK-0006_arkivklarering_veikart_v1.13_2026-10-28.md: ARK-0006, v1.13, 2026-10-28
- docs/KLAR-ARK-0008_arkivklarering_avklaringer-foer-frys_v1.15_2026-10-28.md: ARK-0008, v1.15, 2026-10-28
- docs/KLAR-ARK-0009_arkivklarering_artikkelutkast-joss_v0.15_2026-10-28.md: ARK-0009, v0.15, 2026-10-28
- docs/KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v1.5_2026-10-28.md: EVAL-0001, v1.5, 2026-10-28
- docs/KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_2026-10-26.md: EVAL-0005, v1.0, 2026-10-26
- docs/KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.0_2026-10-26.md: EVAL-0006, v1.0, 2026-10-26
- docs/KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.1_2026-10-26.md: EVAL-0006, v1.1, 2026-10-26
- docs/KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.2_2026-10-27.md: EVAL-0006, v1.2, 2026-10-27
- docs/KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_2026-10-26.md: EVAL-0007, v1.0, 2026-10-26
- docs/KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.1_2026-10-27.md: EVAL-0007, v1.1, 2026-10-27
- docs/KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.2_2026-10-27.md: EVAL-0008, v1.2, 2026-10-27
- docs/KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.5_2026-10-28.md: EVAL-0008, v1.5, 2026-10-28
- docs/KLAR-EVAL-0010_arkivklarering_degradering-dev_v1.5_2026-10-28.md: EVAL-0010, v1.5, 2026-10-28
- docs/KLAR-EVAL-0011_arkivklarering_tomt-raalag-diagnose_v1.0_2026-10-26.md: EVAL-0011, v1.0, 2026-10-26
- docs/KLAR-EVAL-0012_arkivklarering_talerinndeling-der-dev_v1.0_2026-10-26.md: EVAL-0012, v1.0, 2026-10-26
- docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.19_2026-10-28.md: KILDE-0001, v1.19, 2026-10-28
- docs/KLAR-LOG-0001_arkivklarering_avvik-og-hendelser_v1.53_2026-10-28.md: LOG-0001, v1.53, 2026-10-28
- docs/KLAR-LOG-0003_arkivklarering_avvikstabell_v1.22_2026-10-28.md: LOG-0003, v1.22, 2026-10-28
- docs/KLAR-LOG-0004_arkivklarering_portfunn-runde2_v1.0_2026-10-28.md: LOG-0004, v1.0, 2026-10-28
- docs/KLAR-LOG-0005_arkivklarering_portfunn-runde3_v1.0_2026-10-28.md: LOG-0005, v1.0, 2026-10-28
- docs/KLAR-PREREG-0001_arkivklarering_testdeler_v1.33_2026-10-28.md: PREREG-0001, v1.33, 2026-10-28
- docs/KLAR-REG-0001_arkivklarering_osf-metode_v1.0_2026-10-26.md: REG-0001, v1.0, 2026-10-26
- docs/KLAR-REG-0001_arkivklarering_osf-metode_v1.2_2026-10-27.md: REG-0001, v1.2, 2026-10-27
- docs/adr/KLAR-ADR-0001_arkivklarering_eget-verktoey_v1.0_2026-10-26.md: ADR-0001, v1.0, 2026-10-26
- docs/adr/KLAR-ADR-0002_arkivklarering_klarering-foer-publisering_v1.0_2026-10-26.md: ADR-0002, v1.0, 2026-10-26
- docs/adr/KLAR-ADR-0003_arkivklarering_mmif-internt-format_v1.2_2026-10-27.md: ADR-0003, v1.2, 2026-10-27
- docs/adr/KLAR-ADR-0004_arkivklarering_segmentregel_v1.5_2026-10-28.md: ADR-0004, v1.5, 2026-10-28
- docs/adr/KLAR-ADR-0005_arkivklarering_to-lag-nb-whisper-large_v1.3_2026-10-28.md: ADR-0005, v1.3, 2026-10-28
- docs/adr/KLAR-ADR-0006_arkivklarering_alias-tabell-uten-fuzzy_v1.0_2026-10-26.md: ADR-0006, v1.0, 2026-10-26
- docs/adr/KLAR-ADR-0007_arkivklarering_lokal-prosessering_v1.1_2026-10-27.md: ADR-0007, v1.1, 2026-10-27
- docs/adr/KLAR-ADR-0008_arkivklarering_personvernflagg-presidio-nbbert_v1.3_2026-10-27.md: ADR-0008, v1.3, 2026-10-27
- docs/adr/KLAR-ADR-0009_arkivklarering_eksport-webvtt-iiif_v1.1_2026-10-27.md: ADR-0009, v1.1, 2026-10-27
- docs/adr/KLAR-ADR-0010_arkivklarering_repo-privat-til-prereg_v1.1_2026-10-27.md: ADR-0010, v1.1, 2026-10-27
- docs/adr/KLAR-ADR-0011_arkivklarering_data-til-spraakbanken-etter-klarering_v1.0_2026-10-26.md: ADR-0011, v1.0, 2026-10-26
- docs/adr/KLAR-ADR-0012_arkivklarering_recall-foran-presisjon_v1.4_2026-10-28.md: ADR-0012, v1.4, 2026-10-28
- docs/adr/KLAR-ADR-0013_arkivklarering_katalogmodell_v1.1_2026-10-28.md: ADR-0013, v1.1, 2026-10-28
- docs/adr/KLAR-ADR-0014_arkivklarering_vendor-fra-norsk-tale_v1.1_2026-10-27.md: ADR-0014, v1.1, 2026-10-27
- docs/adr/KLAR-ADR-0015_arkivklarering_tunge-data-kun-paa-vault_v1.1_2026-10-27.md: ADR-0015, v1.1, 2026-10-27
- docs/adr/KLAR-ADR-0016_arkivklarering_talerinndeling-pyannote_v1.1_2026-10-28.md: ADR-0016, v1.1, 2026-10-28
- docs/adr/KLAR-ADR-0017_arkivklarering_nt-for-raalaget_v1.1_2026-10-28.md: ADR-0017, v1.1, 2026-10-28
- docs/adr/KLAR-ADR-0018_arkivklarering_innspillingsprotokoll-h4_v1.2_2026-10-28.md: ADR-0018, v1.2, 2026-10-28
- docs/adr/KLAR-ADR-0019_arkivklarering_inaseg-erstatning_v1.6_2026-10-28.md: ADR-0019, v1.6, 2026-10-28
- docs/adr/KLAR-ADR-0020_arkivklarering_lisens-agpl_v1.4_2026-10-28.md: ADR-0020, v1.4, 2026-10-28
- docs/stempler/KLAR-LOG-0002_arkivklarering_tidsstempler_v1.35_2026-10-28.md: LOG-0002, v1.35, 2026-10-28
- eval/dev/KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_2026-10-26.md: EVAL-0002, v1.0, 2026-10-26
- eval/dev/KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.1_2026-10-27.md: EVAL-0002, v1.1, 2026-10-27
- eval/dev/KLAR-EVAL-0004_arkivklarering_dev-lisens-nbsamtale_v1.0_2026-10-26.md: EVAL-0004, v1.0, 2026-10-26
- eval/test/KLAR-EVAL-0013_arkivklarering_test-nbsamtale-wer_v1.0_2026-10-27.md: EVAL-0013, v1.0, 2026-10-27
- eval/test/KLAR-EVAL-0013_arkivklarering_test-nbsamtale-wer_v1.3_2026-10-27.md: EVAL-0013, v1.3, 2026-10-27
- eval/test/KLAR-EVAL-0014_arkivklarering_test-flaggoverlevelse-npsc_v1.4_2026-10-27.md: EVAL-0014, v1.4, 2026-10-27
- eval/test/KLAR-EVAL-0015_arkivklarering_personvern-test_v1.5_2026-10-28.md: EVAL-0015, v1.5, 2026-10-28
- KLAR-GT-0001: denne fila (generert av scripts/ground_truth.py; forrige versjon ligger i git-historikken)

## Nummerregister (KLAR-ARK-0003 mot disken)

- ADR: 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0010, 0011, 0012, 0013, 0014, 0015, 0016, 0017, 0018, 0019, 0020
- ARK: 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009
- EVAL: 0001, 0002, 0003, 0004, 0005, 0006, 0007, 0008, 0009, 0010, 0011, 0012, 0013, 0014, 0015, 0016, 0017 (reservert: 0009, 0016, 0017)
- GT: 0001
- KILDE: 0001
- LOG: 0001, 0002, 0003, 0004, 0005
- MANUS: 0001, 0002
- PREREG: 0001, 0002, 0003 (reservert: 0002, 0003)
- REG: 0001
- register: docs/KLAR-ARK-0003_arkivklarering_nummerregister_v1.27_2026-10-28.md; 59 nøkler i registeret, 54 på disk

Varsler: ingen.

## Kilderegister (KLAR-KILDE-0001 mot lagrede kopier på Vault)

- register: docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.19_2026-10-28.md; 259 påstander
- status etter mekanisk kontroll (sitat som eksakt delstreng av lagret kopi): delvis 7, ikke funnet 3, motsagt 1, verifisert 248
- brudd (sitat ikke funnet, manglende kopi eller sha256-avvik): 0
- kildelenker i KLAR-dokumenter, README og ADR-er uten rad i registeret: 0

## Siste eval-resultater

- eval/dev/KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_2026-10-26.json (DEV, ikke pilot): korpus-WER totalt ra/nn 0.317, ra/matchet 0.250, normalisert/nn 0.463, normalisert/matchet 0.348
- eval/dev/KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.1_2026-10-27.json (DEV, ikke pilot): korpus-WER totalt ra/nn 0.248, ra/matchet 0.135, normalisert/nn 0.463, normalisert/matchet 0.348
- eval/test/KLAR-EVAL-0013_arkivklarering_test-nbsamtale-wer_v1.0_2026-10-27.json (TEST – preregistrert (OSF hc83q)): korpus-WER totalt ra/nn 0.254, ra/matchet 0.128, normalisert/nn 0.464, normalisert/matchet 0.337
- docs/KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v1.5_2026-10-28.md
- docs/KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_2026-10-26.md
- docs/KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.0_2026-10-26.md
- docs/KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.1_2026-10-26.md
- docs/KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.2_2026-10-27.md
- docs/KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_2026-10-26.md
- docs/KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.1_2026-10-27.md
- docs/KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.2_2026-10-27.md
- docs/KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.5_2026-10-28.md
- docs/KLAR-EVAL-0010_arkivklarering_degradering-dev_v1.5_2026-10-28.md
- docs/KLAR-EVAL-0011_arkivklarering_tomt-raalag-diagnose_v1.0_2026-10-26.md
- docs/KLAR-EVAL-0012_arkivklarering_talerinndeling-der-dev_v1.0_2026-10-26.md

## Vault

- Vault montert: **ja** (/Volumes/Vault)
- datarot (ARKIVKLARERING_DATA): `/Volumes/Vault/arkivklarering`
  - arkivklarering/repo-bundle: finnes, 35 oppføringer
  - arkivklarering/modeller: finnes, 3 oppføringer
  - arkivklarering/lyd: finnes, 225 oppføringer
  - arkivklarering/eval-data: finnes, 5163 oppføringer

## Tidsstempler (OpenTimestamps)

- .ots-filer: 298, Bitcoin-bekreftet: 264, ventende: 34
- logg: docs/stempler/KLAR-LOG-0002_arkivklarering_tidsstempler_v1.35_2026-10-28.md

## Håndført (fra docs/gt_fast.md, ikke generert)

- OSF-metoderegistrering: https://osf.io/fbme7/ – embargo til 2027-10-26. Embargo godkjent 26.10.2026 av Eirik via OSFs e-postlenke (oppgitt av eier, ikke etterprøvd av CC – økten var logget ut). Prosjekt (privat): https://osf.io/dmb6g/
- OSF-status sjekket 2026-10-27 kl. 08:13 (CET) i innlogget Chrome (konto Eirik Botten Nicolaysen), siden https://osf.io/fbme7/overview og https://osf.io/hc83q/overview: begge viser ordrett «Embargoed registration» (ingen «Pending embargo approval»). Sidene viser ikke embargodato; datoene er fra OSF-API-et (`api.osf.io/v2/registrations/<id>/`, innlogget økt): fbme7 (Open-Ended Registration, registrert 2026-10-26 08:10 UTC): `embargoed` true, `pending_embargo_approval` false, `pending_registration_approval` false, `pending_embargo_termination_approval` false, `embargo_end_date` «2027-10-26T00:00:00Z», `public` false, `withdrawn` false, `archiving` false. hc83q (OSF Preregistration, registrert 2026-10-27 03:13 UTC): `embargoed` true, `pending_embargo_approval` false, `pending_registration_approval` false, `pending_embargo_termination_approval` false, `embargo_end_date` «2027-10-26T00:00:00Z», `public` false, `withdrawn` false, `archiving` false. Altså godkjent embargo på begge, og arkiveringen på hc83q er ferdig. Hvem som godkjente hc83q (eier eller automatisk) viser ikke OSF her. Registration DOI-feltet er tomt på begge sidene.
- Pitch til Gudbrandsdalsmusea sendt 26.10.2026 (mottaker: folkemusikk@gudbrandsdalsmusea.no – ikke verifisert mot Sendt-mappen).
- norsk-tale er bare referanse. Arkivklarering er et eget verktøy.
- Museumspilotens preregistrering er KLAR-PREREG-0002 (reservert); den lages først etter ja fra museet og før pilotdata kjøres. KLAR-PREREG-0001 gjelder testdelene av offentlige datasett og testmanuset (KLAR-MANUS-0002).
- Lyd fra museet går aldri inn i git, sky eller GitHub.
- Offentlig repo (egen linje): https://github.com/avalyset/arkivklarering-public – opprettet 2026-10-28 fra et rent tre (`git archive` av den private `4f98d1c`, én commit `565bc98` «arkivklarering v1.0»); tag `v1.0.0` = commit `f3d84754ffceab205b829bbfc171f3de364a7343` (tag-objekt `bac837ecb806bd2f296d381ebb76b5aa05f1268b`); HEAD `b336ee7` har samme tre som den private `48f4497`. Det private repoet `avalyset/arkivklarering` er fortsatt privat.
- Zenodo 2026-10-28: programvarearkivet, versjon 1.0.0: DOI 10.5281/zenodo.23723667, konsept-DOI 10.5281/zenodo.23723666 (laget fra GitHub-releasen v1.0.0). Full git-historikk (`git bundle --all`, siste commit `e7ee2fcbcf998da55d1b0a287de0410dae7e155c`, sha256 `9c8ddf34c53b2aae7feeaa5cd972d98fcc2e342d917895f44f66383f5a65cf0f`), tilgangsstyrt med tilgang på forespørsel: DOI 10.5281/zenodo.23723450. Kopi av bundlen med OTS-stempel på Vault: `reproduksjon/historikk/`.
- OSF-status 2026-10-28 (innlogget Chrome-økt, `api.osf.io/v2/registrations/<id>/`): embargoslutt er bedt om på hc83q og fbme7 («End embargo early», bekreftet). Begge har `reviews_state` «pending_embargo_termination», `pending_embargo_termination_approval` true og `public` false. Godkjenningen kommer på e-post til Eirik; den er ikke gitt per denne GT-en. Prosjektet dmb6g (privat) har lenken til det offentlige repoet og alle DOI-ene i beskrivelsen; registreringene er ikke endret.
