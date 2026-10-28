# Endringslogg

Format etter [Keep a Changelog](https://keepachangelog.com/no/1.1.0/); versjonene følger `pyproject.toml`. Alt er utviklet 2026-10-26–28 (ett arbeidsløp). Kvalitetspåstander står bare i KLAR-EVAL-dokumentene; avvik og hendelser i `docs/KLAR-LOG-0001_*`.

## [1.0.1] - 2026-10-28

- Kilderader for Zenodo-adressene og DOI-er i CITATION.cff, .zenodo.json og README. Ingen endring i kode, analyse eller resultater. v1.0.0 er arkivert før disse rettingene; kildesjekken feiler der på to adresser (se LOG-0001). sjekk_pekere feilet i det offentlige repoet fordi historikken ikke finnes der; rettet. Gjelder også v1.0.0.

## [1.0.0] - 2026-10-27

### Endret
- **Lisens:** egen kode er lisensiert **AGPL-3.0-or-later** (var Apache-2.0); rettighetshaveren tilbyr kommersiell lisens som tillegg (eirik@ecodeco.no). `LICENSE` er AGPL-3.0-teksten fra gnu.org, byte-lik den lagrede kopien (KLAR-KILDE-0001 v1.7, K123); `pyproject.toml` (`license = "AGPL-3.0-or-later"`), `CITATION.cff`, `NOTICE` og README er oppdatert. Hele historikken publiseres, med lisenserklæring i `LICENSING-HISTORY.md`. Eiriks beslutning A2/A3 2026-10-27 (KLAR-ARK-0008 v1.3; KLAR-ADR-0020). Tredjepartskomponenter og modeller beholder egne lisenser (`NOTICE`). **A3 endret 2026-10-28 (AV-34):** det offentlige repoet lages fra et rent tre (én commit), og hele git-historikken deponeres med begrenset tilgang på Zenodo (DOI 10.5281/zenodo.23723450).
- **VTT-merknaden om musikk under tale rettet (kodetagg `testkjoring-v8`; AV-30):** NOTE-linjen i WebVTT og `merknad` i `segments.json` (`arkivklarering/eksport.py:19–21`) sa «Tale med musikk under er transkribert og flagget.», som ikke stemmer med inaSpeechSegmenter (ingen `speech+music`, flagget lages ikke; KLAR-ADR-0019 v1.3). Ny tekst: «Tale med musikk under transkriberes bare når segmenteringen merker den som tale; flagget «musikk under tale» lages bare med inaVAMOS (ADR-0019).» `scripts/kjor_testdel.sh` kontrollerer `testkjoring-v8`; `testkjoring-v7` (`9ded8d8`, versjon 1.0.0, fiktive telefonnumre i testdata (AV-29)) og eldre tagger er beholdt. `_merknad` i `modeller.lock.json` sier nå at modellstien løses mot datarota (`transkriber.standard_modellsti`), uten symlink i repoet. `scripts/sjekk_kilder.py` velger nyeste kilderegister etter versjonsnummer (v1.10 etter v1.9), med test.
- **Hjelpeteksten til `--ingen-ordtider` rettet (kodetagg `testkjoring-v9`; AV-32):** `arkivklarering/cli.py:47` sa «(-ml 1 -sow)», men koden ber om DTW-ordtidsstempler (`-nfa -dtw large.v3 -ojf`); ny tekst sier det, og at cuene da får whisper.cpps segmenttider. Kodesjekken i `scripts/kjor_testdel.sh` viser til `testkjoring-v9`. I samme kodetagg lister GT-generatoren (`scripts/ground_truth.py`) ikke lenger forrige GT-versjon (portfunn 66, med ny test i `tests/test_ground_truth_wer.py`). Ingen analysekode endret. **Mekanisk pekersjekk (kodetagg `testkjoring-v10`; AV-33):** `scripts/sjekk_pekere.py` kontrollerer henvisninger til arkivnøkler og fil:linje-pekere (regelen i KLAR-ARK-0002), og kjøres som test (`tests/test_sjekk_pekere.py`); kodesjekken i `scripts/kjor_testdel.sh` viser til `testkjoring-v10`. Ingen analysekode endret. **Kodetagg `testkjoring-v11` (AV-35):** `scripts/sjekk_pekere.py` prøver historikkregelen bare når bundle-commiten `e7ee2fc` finnes i repoet; kodesjekken i `scripts/kjor_testdel.sh` viser til `testkjoring-v11`. Ingen analysekode endret.
- Dokumentasjonen rettet etter runde 2 av den uavhengige publiseringsporten (KLAR-LOG-0004, funn 1–69 unntatt 64 og 66): nye versjoner av ARK-0001 (v1.9), -0002, -0003, -0004, -0005, -0008, -0009 (v0.9), KILDE (v1.12, fem nye kilder K130–K134 for lisensgrunnlaget i ADR-0019), LOG-0001, LOG-0003 og PREREG (v1.28: AV-31, terskelregelen for H4 i den registrerte teksten stemmer ikke med tabellen; AV-32), ADR-0004, -0005, -0012, -0013, -0016, -0018 og -0019, EVAL-0001, -0008, -0010 og -0015; README, CONTRIBUTING og `paper.bib` peker på nyeste versjoner (KLAR-LOG-0001 v1.48). Funn 66 er rettet i `testkjoring-v9` og funn 64 i `bf48dfe` (eldre versjoner tatt ut av treet); runde 3 av porten (KLAR-LOG-0005, 16 funn) er rettet i nye versjoner av ARK-0001, -0002, -0003, -0004, -0005, -0008, -0009, KILDE, LOG-0001, LOG-0003, PREREG, ADR-0004, ADR-0019 og EVAL-0010, og `bf48dfe`s omskriving av kjøringsmetadata, GT v1.34 og EVAL-0013/-0014 er satt tilbake.
- Dokumentasjonen rettet etter en uavhengig gjennomgang før frys (ingen kodeendring; kodetaggen er fortsatt `testkjoring-v8`): ADR-0004, -0007, -0008, -0009, -0012, -0014, -0015 og -0019 beskriver det koden gjør i v1.0 (bl.a. datarota med fallback, IIIF implementert, risikoordningen av flagg som plan, H4 ikke gjennomført, lisensene); arkitekturen (KLAR-ARK-0001 v1.8), modellkortet (v1.4), databladet (v1.6), veikartet (v1.10), nummerregisteret (v1.23), artikkelutkastet (v0.8), avklaringene før frys (v1.6), avviksloggen (v1.45), avvikstabellen (v1.16) og kilderegisteret (v1.11) er oppdatert; README-stegene for formattestene er kjørt i en ny datarot (KLAR-LOG-0001 v1.45).
- README: installasjonssteg for `ohms.xsd` (K34, sha256-kontroll), IIIF-oppskrift 0219 og katalogmodellen; dagens testtall fra den rene installasjonen 2026-10-27; ytelsestallene beskrevet som preregistrerte målinger fra testkjøringene (`testkjoring-v2`, inaVAMOS), gjenberegnet fra de lagrede utdataene (KLAR-LOG-0001 v1.44).
- **Versjon 1.0.0** i `pyproject.toml`, `CITATION.cff` og `.zenodo.json`; `date-released` er satt til 2026-10-27 og settes til publiseringsdatoen ved publisering.
- **H4 gjennomføres ikke i v1.0** (AV-27; Eiriks beslutning A1 2026-10-27). Blindtesten på NB Tale modul 3 er planlagt som v1.1 (KLAR-PREREG-0003).
- **Datarot og cacher (kodetagg `testkjoring-v6`, commit `57dedaf`; AV-28):** alt tungt ligger under `ARKIVKLARERING_DATA` (standard `/Volumes/Vault/arkivklarering` når Vault er montert, ellers `${XDG_DATA_HOME:-~/.local/share}/arkivklarering`; `ARKIVKLARERING_EVAL_DATA` overstyrer evalueringsdataene); cachene med tidslinje heter `<navn>_inaseg.jsonl` og `<navn>_inavamos.jsonl` (eldre cacher uten suffiks er laget med inaVAMOS og leses bare med `inavamos`); testene går i et rent miljø uten Vault. `scripts/kjor_testdel.sh` kontrollerer koden mot `testkjoring-v6`; `testkjoring-v1`–`v5` er beholdt. Ingen utregning for H1–H3 er endret.
- Standard segmentering er inaSpeechSegmenter 0.8.0 i eget venv (`segment_inaseg.py`, `_inaseg_runner.py`, `requirements-inaseg.lock`); `ARKIVKLARERING_SEGMENTERING=inaseg` er standard, også uten variabelen (KLAR-ADR-0019 v1.3, alternativ A; commit `076bb8d`; AV-26). Tale over musikk blir `speech` eller `music`, og flagget «musikk under tale – vurder rettigheter» produseres ikke lenger.
- inaVAMOS er et valgfritt tillegg (`reproduksjon-h1h2`; Pantagruel Research-only License), bare for å reprodusere H1 og H2. `scripts/kjor_testdel.sh` setter `inavamos` for H1 og H2 og `inaseg` for H4; `scripts/reproduser.sh` setter `inavamos` for alle steg unntatt H4 (steg 9, `inaseg`) (AV-25, AV-26).
- Kodetagg `testkjoring-v5` (commit `076bb8d`): kodesjekken i `scripts/kjor_testdel.sh` går mot den; `testkjoring-v1`–`v4` er beholdt.
- `scripts/ground_truth.py` hopper over utvalgs- og metafiler under `eval/test/` (med test; commit `9adad34`, LOG v1.35).
- README, NOTICE og CHANGELOG oppdatert for v1.0 (behov, avhengigheter, installasjon, bruk, moduler, tester, begrensninger; kreditering for NB-BERT-base-ner og pyannote; lisensstatus for segmenteringen).
- KLAR-MANUS-0001 omdøpt til justeringsmanus (v1.1). KLAR-MANUS-0002 (testmanus) rettet til v1.1 før låsing.
- KLAR-PREREG-0001 (`testdeler`, v1.2): primærutfall H1a og H2, kontrollsjekker K1–K3, H4 på testmanuset.

### Lagt til
- `KLAR-ARK-0008` (avklaringer før frys, v1.0–v1.3) med Eiriks beslutninger A1–A3 og frysregelen.
- `KLAR-ADR-0020` (lisens: AGPL-3.0-or-later med kommersiell lisens som tillegg, full historikk), `LICENSING-HISTORY.md` og `.zenodo.json` (samme metadata som `CITATION.cff`).
- KLAR-ADR-0019: inaSpeechSegmenter erstatter inaVAMOS i verktøyet og var valgt for H4 (v1.0 vedtatt av eier 2026-10-27; v1.4 gjeldende). H4 gjennomføres ikke i v1.0 (AV-27), så segmentøren er bare brukt i verktøyet.
- Testdelene H1–H3 kjørt én gang via `scripts/kjor_testdel.sh` og rapportert, også negative og uklare utfall: H1 (KLAR-EVAL-0013), H2 (KLAR-EVAL-0014), H3 (KLAR-EVAL-0015). H1a 0,127 mot terskel ≤ 0,25; H2a–H2e bekreftet (H2c ikke klar); H3 alle åtte terskler bekreftet (tre ikke klare). H4 er ikke gjennomført.
- `CONTRIBUTING.md`.
- H4-innleser uten resultat (`arkivklarering/h4_innlesing.py`, `scripts/rigg_manus.py`; KLAR-ADR-0018) og veikart (`docs/KLAR-ARK-0006`).
- `scripts/kjor_testdel.sh` (testdelene H1–H4 én og én med commit, push og speil), `scripts/rapporter_intervaller.py`, `scripts/verifiser_uendret.py`; avvikstabell (`docs/KLAR-LOG-0003`).
- `scripts/reproduser.sh`: kjører EVAL-ene i rekkefølge fra rådata i en frittstående worktree og skriver sha256 for hvert resultat.
- `requirements.lock`: låst miljø med sha256 for alle distribusjoner.
- `docs/KLAR-ARK-0004` (modellkort, Mitchell mfl. 2019) og `docs/KLAR-ARK-0005` (datablad for manusene, Gebru mfl. 2021).
- `kalibrering/kjor_h4.py`: H4-scoring av menneskeinnleste opptak av KLAR-MANUS-0002 mot tersklene i KLAR-PREREG-0001; tørrtest på justeringsmanuset.
- `scripts/ordbokkontroll.py` og `scripts/navnesjekk.py`: kontroll av KLAR-MANUS-0002 mot Nynorskordboka/Bokmålsordboka og SSBs navnesøk.

## [0.4.0] - 2026-10-26

### Lagt til
- Katalogutkast (`katalog.py`, lokal ollama, `borealis-open-4b`, KLAR-ADR-0013).
- Eksport: WebVTT per lag, OHMS XML (validert mot arkivert `ohms.xsd` v5.4), IIIF Presentation 3, MMIF; `LICENSE` (Apache-2.0), `NOTICE`, `CITATION.cff`, README.
- Justeringsmanus (KLAR-MANUS-0001), syntetisk kjede (KLAR-EVAL-0008), NPSC DEV (KLAR-EVAL-0007), vendor-kopi fra norsk-tale (KLAR-ADR-0014), Vault-regelen (KLAR-ADR-0015).
- Preregistreringsutkast KLAR-PREREG-0001 (ikke registrert; testdelene er sperret i koden).

## [0.3.0] - 2026-10-26
- Ordtidsstempler (DTW) i rålaget og union av flagg på ordspenn; flaggoverlevelse (KLAR-EVAL-0006); nummerregister (KLAR-ARK-0003).

## [0.2.0] - 2026-10-26
- Personvernflagg v0 (Presidio, NB-BERT-base-ner, mønstre og ordlister; KLAR-ADR-0008, -0012; KLAR-EVAL-0005); alt tungt flyttet til Vault; miljøvakt.

## [0.1.0] - 2026-10-26
- Rørledning fra lydfil til WebVTT i to lag og `segments.json` (inaVAMOS, NB-Whisper large verbatim og normalisert); DEV-måling av WER (KLAR-EVAL-0002); repodisiplin (arkivnøkler, ADR-er, GT, tidsstempling med OpenTimestamps, speiling til tre kopier).
- Metoderegistrering på OSF: <https://osf.io/fbme7/> (embargo til 2027-10-26).
