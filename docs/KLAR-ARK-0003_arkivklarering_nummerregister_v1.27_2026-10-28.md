# KLAR-ARK-0003: Nummerregister

Versjon 1.27, 2026-10-28 (v1.27: raden for ADR-0020 sier at A3 er endret (offentlig repo fra rent tre, full historikk i tilgangsstyrt deponering); v1.26: LOG-0005 portfunn-runde3 i bruk (porten, runde 3 (KLAR-LOG-0005)); v1.25: raden for ARK-0005 sier at NB Tale modul 3 er planlagt for v1.1 (KLAR-PREREG-0003), ikke «i vurdering»; raden for MANUS-0002 sier at sperren åpnes med `--prereg-id` fordi preregistreringen er registrert, og at H4 utgår i v1.0; v1.24: LOG-0004 portfunn-runde2 i bruk; v1.23: raden for PREREG-0001 sier at den er registrert (OSF hc83q); raden for EVAL-0009 sier at den er reservert, men at H4 utgår i v1.0 (AV-27); raden for MANUS-0002 viser til v1.3 (AV-29); v1.22: ADR-0020 lisens-agpl i bruk (v1.0, vedtatt 2026-10-27: AGPL-3.0-or-later med kommersiell lisens som tillegg, full historikk); plassholderen for A1/A2/A3 i raden for ARK-0009 erstattet med de avgjorte beslutningene; PREREG-0003 viser til den avgjorte A1; v1.21: ARK-0008 avklaringer-foer-frys i bruk (v1.0); v1.20: ARK-0009 artikkelutkast-joss i bruk; PREREG-0003 blindtest-nb-tale-modul-3 reservert; «brukt av» for ARK-0004 (v1.1), ARK-0005 (v1.2) og ARK-0008 (finnes ikke på disk ennå) oppdatert; v1.19: EVAL-0016 og -0017 avlyst (sensitivitetskjøringen utgår; numrene gjenbrukes ikke); v1.18: ARK-0008 avklaringer-foer-frys reservert; slugene for EVAL-0016 og -0017 rettet til det kjøreskriptene produserer; v1.17: ADR-0019 vedtatt (v1.0), EVAL-0016 og -0017 reservert for sensitivitetskjøringene av H1 og H2; v1.16: ADR-0019 (kladd, foreslått) på grenen inaseg-erstatning; v1.15: ARK-0007 testdata-sha256 (hashfil med .ots) i bruk; v1.14: EVAL-0013, -0014 og -0015 i bruk (v1.0 resultat, v1.1 med intervaller); v1.13: ADR-0018 innspillingsprotokoll og ARK-0006 veikart i bruk; v1.12: EVAL-0013, -0014 og -0015 reservert for H1–H3 på testdelene (eval/test/), LOG-0003 avvikstabell i bruk; v1.11: EVAL-0012 i bruk; v1.10: ADR-0017 -nt for rålaget; v1.9: EVAL-0011 i bruk; v1.8: ADR-0016 talerinndeling; EVAL-0011 (tomt rålag) og EVAL-0012 (DER) reservert; v1.7: EVAL-0010 i bruk; KILDE-0001 kilderegister i bruk; v1.6: ARK-0004 modellkort og ARK-0005 datablad i bruk; EVAL-0009 (H4) og EVAL-0010 (simulert degradering) reservert; MANUS-0002 v1.1; v1.5: PREREG-0001 omdøpt til testdeler, PREREG-0002 reservert for museumspiloten, MANUS-0001 omdøpt til justeringsmanus, MANUS-0002 (testmanus) lagt til; v1.4: ADR-0013, EVAL-0008 og PREREG-0001 tatt i bruk; v1.3: ADR-0015 lagt til; v1.1: KLAR-EVAL-0007 tatt i bruk; v1.2: ADR-0013 og ADR-0014, EVAL-0008 og MANUS-0001 lagt til, ADR-0013 kontrollert ledig før bruk). Forfatter: Eirik Botten Nicolaysen, EcoDeco AS.

Alle brukte (og reserverte) KLAR-nummer per type, slugen de bærer og hvem som bruker dem (skript, dokument eller person som fører dem).
Reglene står i KLAR-ARK-0002: et nummer gjenbrukes aldri, og alle versjoner av samme dokument har samme `TYPE-NNNN` og samme slug.
`scripts/ground_truth.py` leser dette registeret mot disken og varsler i `KLAR-GT-0001` ved hull, dobbel bruk (samme nummer med to ulike
slug), nummer på disk som ikke står her, og nummer her som ikke finnes på disk (unntatt `reservert`). Registeret rettes for hånd når et nummer tas i bruk;
versjonen i filnavnet økes da.

| nøkkel | slug | status | sted | brukt av |
|---|---|---|---|---|
| KLAR-REG-0001 | osf-metode | i bruk | `docs/` | OSF-metoderegistreringen (https://osf.io/fbme7/); ført av CC-kjøringene på instruks fra Eirik |
| KLAR-PREREG-0001 | testdeler | i bruk | `docs/` | **registrert på OSF 2026-10-27** (https://osf.io/hc83q/, embargo til 2027-10-26; statuslinjen `Status: registrert https://osf.io/hc83q/` i dokumentet, registrert innhold = v1.8, avvik etter registrering i dokumentet og i KLAR-LOG-0003): preregistrering av målingene på testdelene (NB Samtale, NPSC, NorNE) og testmanuset; primærutfall H1 og H2; testdelene var låst i `arkivklarering/evaldata.py` til linjen `Status: registrert <OSF-URL>` sto i dokumentet (KLAR-ADR-0010); sperren åpner nå bare med `--prereg-id KLAR-PREREG-0001` |
| KLAR-PREREG-0002 | museumspilot | reservert | `docs/` | museumspilotens preregistrering; lages først etter ja fra museet og før pilotdata kjøres (`docs/gt_fast.md`, KLAR-ADR-0010) |
| KLAR-PREREG-0003 | blindtest-nb-tale-modul-3 | reservert | `docs/` | reservert – blindtest NB Tale modul 3 (se KLAR-ARK-0008 seksjon E); A1 avgjort 2026-10-27: blindtesten blir v1.1 med egen preregistrering |
| KLAR-ARK-0001 | arkitektur | i bruk | `docs/` | arkitekturdokumentet, ført for hånd |
| KLAR-ARK-0002 | navnekonvensjon | i bruk | `docs/` | navnekonvensjonen, ført for hånd |
| KLAR-ARK-0004 | modellkort | i bruk | `docs/` | modellkort for rørledningen (Mitchell mfl. 2019; v1.1: inaSpeechSegmenter som segmenterer, inaVAMOS valgfritt tillegg, talerinndeling, målte testresultater H1–H3 med intervaller), ført for hånd |
| KLAR-ARK-0005 | datablad-manus | i bruk | `docs/` | datablad for KLAR-MANUS-0001 og -0002 og (fra v1.2) for de offentlige datasettene i målingene (NB Samtale, NPSC, NorNE; NB Tale modul 3 planlagt for v1.1, KLAR-PREREG-0003) (Gebru mfl. 2021), ført for hånd; slugen beholdt |
| KLAR-ARK-0006 | veikart | i bruk | `docs/` | veikart: v1.0-stegene i rekkefølge med status, og det som kommer etter v1.0; ført for hånd |
| KLAR-ARK-0003 | nummerregister | i bruk | `docs/` | dette registeret, ført for hånd; leses av `scripts/ground_truth.py` |
| KLAR-ARK-0007 | testdata-sha256 | i bruk | `docs/` (`.txt`) og `docs/stempler/` (`.ots`) | sha256 for de 13 testdatafilene (H1–H3), ført for hånd etter H1-start (AV-23); stemplet |
| KLAR-ARK-0008 | avklaringer-foer-frys | i bruk | `docs/` | avklaringsdokumentet før frys (A: Eiriks beslutninger, B: kontroller med bevis, C: utsatt, D: rekkefølge, E: grunnlag for blindtest, F: JOSS-sjekkliste); v1.0 2026-10-27 (KLAR-ARK-0009 og KLAR-PREREG-0003 viser til det); ført for hånd; arbeidskøen i `CLAUDE.md` |
| KLAR-ARK-0009 | artikkelutkast-joss | i bruk | `docs/` | JOSS-artikkelutkast (v0.x, UTKAST), ført for hånd; Eiriks beslutninger 2026-10-27 innarbeidet: A1 H4 gjennomføres ikke i v1.0 (AV-27), A2 AGPL-3.0-or-later med kommersiell lisens som tillegg, A3 full historikk (KLAR-ADR-0020) |
| KLAR-ADR-0001 | eget-verktoey | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0002 | klarering-foer-publisering | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0003 | mmif-internt-format | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0004 | segmentregel | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0005 | to-lag-nb-whisper-large | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0006 | alias-tabell-uten-fuzzy | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0007 | lokal-prosessering | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0008 | personvernflagg-presidio-nbbert | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0009 | eksport-webvtt-iiif | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0010 | repo-privat-til-prereg | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0011 | data-til-spraakbanken-etter-klarering | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0012 | recall-foran-presisjon | i bruk | `docs/adr/` | beslutning, ført for hånd |
| KLAR-ADR-0013 | katalogmodell | i bruk | `docs/adr/` | valg av lokal ollama-modell for katalogutkastet (`eval/dev/velg_katalogmodell.py`); kontrollert 2026-10-26 (register, arbeidstre, git-historikk, Vault-bundle og -stempler, Master Dok., GitHub): ikke brukt tidligere |
| KLAR-ADR-0014 | vendor-fra-norsk-tale | i bruk | `docs/adr/` | beslutning, ført for hånd (tallnormalisering og scoring fra norsk-tale) |
| KLAR-ADR-0015 | tunge-data-kun-paa-vault | i bruk | `docs/adr/` | beslutning, ført for hånd (Vault-regelen og miljøvakten; skrevet i ettertid, etter at vakten var innført og testet) |
| KLAR-ADR-0016 | talerinndeling-pyannote | i bruk | `docs/adr/` | beslutning, ført for hånd (pyannote community-1, anonyme talermerker) |
| KLAR-ADR-0017 | nt-for-raalaget | i bruk | `docs/adr/` | beslutning, ført for hånd (whisper.cpp -nt bare for rålaget) |
| KLAR-ADR-0018 | innspillingsprotokoll-h4 | i bruk | `docs/adr/` | beslutning, ført for hånd (H4-innleser uten resultat, låst rigg, Vault-sti, omtakslogg) |
| KLAR-ADR-0019 | inaseg-erstatning | i bruk | `docs/adr/` | beslutning, ført for hånd (inaSpeechSegmenter erstatter inaVAMOS; vedtatt for v1.0 med alternativ A) |
| KLAR-ADR-0020 | lisens-agpl | i bruk | `docs/adr/` | beslutning, ført for hånd (AGPL-3.0-or-later for egen kode med kommersiell lisens som tillegg; full historikk med lisenserklæring i `LICENSING-HISTORY.md`; Eiriks beslutninger A2 og A3 2026-10-27; A3 endret 2026-10-28: offentlig repo fra rent tre, full historikk i tilgangsstyrt deponering) |
| KLAR-GT-0001 | ground-truth | i bruk | `docs/` | generert av `scripts/ground_truth.py` (versjon økes automatisk) |
| KLAR-EVAL-0001 | oppdiktet-tekst-maaling | i bruk | `docs/` | generert av `scripts/mal_oppdiktet_tekst.py`, tolkning for hånd |
| KLAR-EVAL-0002 | dev-nbsamtale-wer | i bruk | `eval/dev/` | `eval/dev/kjor_dev.py` (WER på NB Samtale, DEV) |
| KLAR-EVAL-0003 | dev-utvalg | i bruk | `eval/dev/` | `eval/dev/kjor_dev.py` (utvalget av de 60 segmentene) |
| KLAR-EVAL-0004 | dev-lisens-nbsamtale | i bruk | `eval/dev/` | lisensen for NB Samtale, ført for hånd |
| KLAR-EVAL-0005 | personvern-dev | i bruk | `docs/` | `eval/dev/kjor_personvern_dev.py` (NorNE, DEV), tolkning for hånd |
| KLAR-EVAL-0006 | flaggoverlevelse-dev | i bruk | `docs/` | `eval/dev/kjor_flaggoverlevelse_dev.py` (v1.0) og `eval/dev/kjor_flaggoverlevelse_ord.py --datasett nbsamtale` (v1.1), tolkning for hånd |
| KLAR-EVAL-0007 | flaggoverlevelse-npsc-dev | i bruk | `docs/` | `eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc` (DEV), tolkning for hånd |
| KLAR-EVAL-0008 | syntetisk-kjede | i bruk | `docs/` | `eval/dev/kjor_syntetisk.py` (SYNTETISK, kjede og flagglogikk), tolkning for hånd |
| KLAR-EVAL-0009 | h4-testmanus | reservert | `docs/` | `kalibrering/kjor_h4.py` (H4 på menneskeinnlest KLAR-MANUS-0002). Reservert, men H4 utgår i v1.0 (AV-27, Eiriks beslutning 2026-10-27), så EVAL-0009 skrives ikke i v1.0; nummeret står reservert hvis H4 gjennomføres senere |
| KLAR-EVAL-0010 | degradering-dev | i bruk | `docs/` | `eval/dev/kjor_degradering.py` (simulert degradering, DEV), tolkning for hånd |
| KLAR-EVAL-0011 | tomt-raalag-diagnose | i bruk | `docs/` | `eval/dev/diagnose_tomt_raalag.py`, tolkning for hånd |
| KLAR-EVAL-0012 | talerinndeling-der-dev | i bruk | `docs/` | `eval/dev/kjor_der.py` (DER på NB Samtale validation, DEV), tolkning for hånd |
| KLAR-EVAL-0013 | test-nbsamtale-wer | i bruk | `eval/test/` | `eval/dev/kjor_dev.py --splitt test --per-dialekt 60 --etikett TEST` (H1, NB Samtale test); startes av `scripts/kjor_testdel.sh` |
| KLAR-EVAL-0014 | test-flaggoverlevelse-npsc | i bruk | `eval/test/` | `eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --etikett TEST` (H2, NPSC test); startes av `scripts/kjor_testdel.sh` |
| KLAR-EVAL-0015 | personvern-test | i bruk | `eval/test/` | `eval/dev/kjor_personvern_dev.py --splitt test --etikett TEST` (H3, NorNE test); startes av `scripts/kjor_testdel.sh` |
| KLAR-EVAL-0016 | test-nbsamtale-wer | reservert | `eval/sensitivitet/` | avlyst 2026-10-27: sensitivitetskjøringen av H1/H2 utgikk (eiers endring); ingen resultat; nummeret gjenbrukes ikke |
| KLAR-EVAL-0017 | test-flaggoverlevelse-npsc | reservert | `eval/sensitivitet/` | avlyst 2026-10-27: sensitivitetskjøringen av H1/H2 utgikk (eiers endring); ingen resultat; nummeret gjenbrukes ikke |
| KLAR-MANUS-0001 | justeringsmanus | i bruk | `kalibrering/` | justeringsmanus (156 setninger): brukt til mønsterjustering og syntetisk kjede (KLAR-EVAL-0008), ikke til testing; `scripts/lag_manus.py` genererer det |
| KLAR-MANUS-0002 | testmanus | i bruk | `kalibrering/` | urørt testmanus for H4 i KLAR-PREREG-0001 (156 setninger; gjeldende v1.3 med telefonnumrene i Nkoms fiktivserie (AV-29), registrert v1.2; H4 utgår i v1.0, AV-27); `scripts/lag_manus2.py`; sha256 står i preregistreringen; innlesing via `scripts/rigg_manus.py`; sperret i rørledningen uten `--prereg-id` (`arkivklarering/kalibrering.py`, `les_manus` → `evaldata.sjekk_splitt`); preregistreringen er registrert (hc83q, se raden for PREREG-0001), så sperren åpnes med `--prereg-id KLAR-PREREG-0001`; H4 utgår i v1.0 (AV-27), så manuset leses ikke inn |
| KLAR-KILDE-0001 | kilderegister | i bruk | `docs/` | kilderegisteret (påstander mot lagrede primærkilder på Vault); sjekkes mekanisk av `scripts/sjekk_kilder.py` og av `scripts/ground_truth.py` |
| KLAR-LOG-0001 | avvik-og-hendelser | i bruk | `docs/` | avvikslogg, ført for hånd av CC-kjøringene |
| KLAR-LOG-0002 | tidsstempler | i bruk | `docs/stempler/` | ført av `scripts/stempel.py` |
| KLAR-LOG-0003 | avvikstabell | i bruk | `docs/` | avvikstabellen: én rad per avvik fra PREREG-planen, ført for hånd |
| KLAR-LOG-0004 | portfunn-runde2 | i bruk | `docs/` | funnlista fra publiseringsporten, runde 2 (69 funn i treet), med rettet-kolonne; ført for hånd |
| KLAR-LOG-0005 | portfunn-runde3 | i bruk | `docs/` | funnlista fra publiseringsporten, runde 3 (16 funn i treet), med rettet-kolonne; ført for hånd |

## Utenfor KLAR-nøklene

- **MASTER:** `MASTER_ARKIVKLARERING_v<maj>_<min>_<dato>.md` i `~/Desktop/Master Dok./Arkivklarering/arkiv/`, versjonert med `~/bin/bump-master.sh` (spor `arkivklarering`). Ligger utenfor git og har ikke KLAR-nummer (KLAR-ARK-0002 § 3).
- **`docs/gt_fast.md`:** håndført inndata til GT, ikke et arkivdokument.
