# KLAR-ARK-0006: Veikart

Versjon 1.13, 2026-10-28 (v1.13: DOI for den tilgangsstyrte historikken er satt inn: 10.5281/zenodo.23723450 (steg 4.5); v1.12: A3 er endret 2026-10-28 (AV-34): offentlig repo fra rent tre, full git-historikk i tilgangsstyrt deponering (DOI 10.5281/zenodo.23723450); v1.11: pekere til versjoner som ikke er i treet er merket «(i git-historikken)», og pekere med linjenummer til forrige versjon av et dokument med ny versjon viser til den nye versjonen, samme linje; kontrollert med `scripts/sjekk_pekere.py`, 0 brudd (KLAR-LOG-0005, restfunn etter kontrollen); v1.10: steg 15 og 21 oppdatert til faktisk tilstand (H1–H3 rapportert, README og avvikstabellen oppdatert; versjon 1.0.0 satt, DOI og utgivelsestagg gjenstår); merknad under definisjonen om at v1.0.0 utgis før (d) etter eiers beslutning 2026-10-27 (A7); «v0.1 har ingen» i «Etter v1.0» rettet til v1.0; v1.9: A1–A3 avgjort av Eirik 2026-10-27 (KLAR-ARK-0008 v1.3); steg 13–14 (innlesing og H4) utgår i v1.0 (AV-27); v1.1 = blindtest på NB Tale modul 3 (KLAR-PREREG-0003); henvisningene til H4 i (b), steg 15, avsnittet under tabellen og «Åpne punkter» rettet etter det; ellers uendret; v1.8: sensitivitetskjøringen av H1 og H2 utgår (eiers endring); v1.7: inaSpeechSegmenter i H4 og som standard i verktøyet (ADR-0019, AV-25), linjen om musikk under tale; v1.6: h4-fiks flettet og `testkjoring-v3` satt (AV-22), AV-23, linjen «Utsatt til etter v1.0»; v1.5: innleserfeil: årsak funnet og rettet i grenen h4-fiks, H4 står åpent; v1.4: steg 9–12 gjort, H1–H3 kjørt og rapportert; v1.3: nytt steg 9 (nedlasting av testdelenes datafiler), H4 som åpent punkt, H1–H3 før H4; v1.2: steg 8 rettet, tørrkjøringen er uendret `--tor`; v1.1: v1.0-definisjonen vedtatt av eier; stegene omskrevet etter den; v1.0: første utkast). Status på dagen; **tilstand for øvrig leses fra `KLAR-GT-0001` (generert fra disk), ikke herfra.**

## Definisjonen av v1.0 (vedtatt av Eirik 2026-10-27)

v1.0 er nådd når alle fire er sanne:

- **(a)** `KLAR-PREREG-0001` er registrert (OSF hc83q).
- **(b)** H4-innlesingen og testdelene H1–H3 er kjørt én gang via `scripts/kjor_testdel.sh`, og alle resultater er rapportert (også negative). (v1.9: H4 utgår i v1.0, AV-27; Eiriks beslutning A1 2026-10-27, KLAR-ARK-0008 v1.3 (i git-historikken). For v1.0 gjelder (b) testdelene H1–H3.)
- **(c)** Frys: linje-for-linje-lesing av innholdet fra disk, Zenodo-DOI, repoet offentlig, og embargoen opphevet på hc83q og fbme7.
- **(d)** Verktøyet er oppført på Nasjonalbibliotekets leverandørliste via ai-lab@nb.no.

**Merknad (v1.10):** NBs leverandørliste (d) kommer etter publiseringen: e-posten til NB sendes etter alt annet (A7, Eiriks vedtak; KLAR-ARK-0008, A7 og D5). Versjon 1.0.0 utgis derfor før (d) er sann, etter eiers beslutning 2026-10-27; (d) står som steg 20 og gjelder fortsatt for v1.0-definisjonen.

Museumspiloten er ikke en del av v1.0 (den krever ja fra museet og egen preregistrering, `KLAR-PREREG-0002`).

## v1.0: stegene i rekkefølge

| # | Steg | Del av | Status | Grunnlag |
|---|---|---|---|---|
| 1 | Kjeden fra lydfil til WebVTT, `segments.json`, katalogutkast, OHMS, IIIF og MMIF | forutsetning | ferdig (v0.4, røyktestet) | CHANGELOG, ARK-0001 § 5 |
| 2 | Personvernflagg v0, union av lag, DTW-ordtider; DEV-målinger med dokumenterte begrensninger (inkludert `-nt` for rålaget) | forutsetning | ferdig; målt bare på DEV | EVAL-0002 til -0012, ADR-0012, -0017 |
| 3 | Metoderegistrering på OSF | forutsetning | ferdig (osf.io/fbme7, embargo til 2027-10-26) | REG-0001 |
| 4 | **Preregistrering av testdelene på OSF** | **(a)** | **ferdig 2026-10-27** (osf.io/hc83q). OSF viser «Embargoed registration», embargo til 2027-10-26, godkjent; arkiveringen er ferdig (sjekket 2026-10-27 kl. 08:13, `docs/gt_fast.md`). | PREREG-0001, LOG-0001 |
| 5 | Fryse koden og kjøremåten: `prereg-v1`, `h4-script-v2`, `testkjoring-v2`; `scripts/kjor_testdel.sh` (commit, push og speil etter hver del; kodesjekk mot taggen) | (b) | ferdig | AV-16, AV-18 |
| 6 | Rapporteringsverktøy: 95 %-intervaller etter PREREG (`scripts/rapporter_intervaller.py`) og bevis for uendret utregning | (b) | ferdig | AV-12, AV-13, AV-15 |
| 7 | Innspillingsprotokoll og H4-innleser uten resultat (låst rigg, Vault-sti, instruks, omtakslogg) | (b) | ferdig (spesifisert, implementert, testet); ikke brukt ennå | ADR-0018, AV-17 |
| 8 | Tørrkjøring: `kjor_testdel.sh --tor` for H1–H4 (kontrollerer rent tre og kodetagg og skriver kommandoene; laster ingen testdata, kjører ingen Whisper) | (b) | ferdig 2026-10-27: exit 0 for H1, H2, H3 og H4 i en ren klon av `add7be0`. Kontrollerer ikke flagg, stier, PREREG-status eller utdatanavn (en utvidet kontroll ble laget og forkastet av eier). | LOG-0001 |
| 9 | **Last ned testdelenes datafiler (NB Samtale, NPSC, NorNE) til Vault, uten å åpne innholdet.** | (b) | **ferdig 2026-10-27** (LOG-0001 v1.27 (i git-historikken)) | PREREG, `CLAUDE.md` |
| 10 | **H1: NB Samtale test** (`KLAR-EVAL-0013`) | (b) | **ferdig 2026-10-27** (commit `1be7358`); H1a 0,127 mot terskel ≤ 0,25, bekreftet; kjørt før H4 (AV-20) | PREREG H1, EVAL-0013 v1.1 (i git-historikken) |
| 11 | **H2: NPSC test** (`KLAR-EVAL-0014`) | (b) | **ferdig 2026-10-27** (commit `efcfc42`); H2a–H2e alle bekreftet (H2c ikke klart); kjørt før H4 (AV-20) | PREREG H2, EVAL-0014 v1.1 (i git-historikken) |
| 12 | **H3: NorNE test** (`KLAR-EVAL-0015`) | (b) | **ferdig 2026-10-27** (commit `3e34815`); alle åtte terskler bekreftet (sekundær); kjørt før H4 (AV-20) | PREREG H3, EVAL-0015 v1.1 (i git-historikken) |
| 13 | **Innlesing av `KLAR-MANUS-0002`** (156 setninger) | **(b)** | **utgår i v1.0 (AV-27)**; Eiriks beslutning A1 2026-10-27 | PREREG H4, AV-19, AV-27 |
| 14 | **H4-scoring** på innleste opptak (`KLAR-EVAL-0009`) | **(b)** | **utgår i v1.0 (AV-27)**; EVAL-0009 skrives ikke i v1.0 | PREREG H4, AV-19, AV-27 |
| 15 | Intervaller og rapport for H1–H4, uavhengig av utfall; EVAL-dokumentene med tolkning for hånd; README og avvikstabell sluttført | (b) | **ferdig for H1–H3** (v1.10): intervaller og EVAL-dokumenter for H1–H3 er skrevet (v1.1, 2026-10-27; gjeldende EVAL-0013 v1.3, EVAL-0014 v1.4, EVAL-0015 v1.4 (i git-historikken)), README «Resultater» har alle tre med negative og uklare utfall, og avvikstabellen har AV-01–AV-30; H4 utgår i v1.0 (AV-27). Tekstene i README og metadataene som sier at repoet er privat og registreringene under embargo, oppdateres i publiseringscommiten (KLAR-ARK-0008 v1.6 (i git-historikken), D4) | PREREG («Negative resultater»), README, LOG-0003 |
| 16 | **Frys, del 1: linje-for-linje-lesing** av innholdet fra disk (ikke fra minne eller chat) | **(c)** | **ikke gjort** | |
| 17 | **Frys, del 2: Zenodo-DOI** | **(c)** | **ikke gjort** | |
| 18 | **Frys, del 3: repoet offentlig** (ADR-0010 tillater det nå som PREREG-0001 er registrert) | **(c)** | **ikke gjort** (eier) | ADR-0010 |
| 19 | **Frys, del 4: embargoen opphevet på hc83q og fbme7** (hc83q og fbme7 har embargo til 2027-10-26) | **(c)** | **ikke gjort** (eier) | LOG-0001, ADR-0010 |
| 20 | **Oppføring på Nasjonalbibliotekets leverandørliste via ai-lab@nb.no** | **(d)** | **ikke gjort** (eier) | ADR-0011 |
| 21 | Utgivelse v1.0 (versjon i `pyproject.toml`, CHANGELOG, CITATION.cff med DOI) | alle | **delvis** (v1.10): versjon 1.0.0 står i `pyproject.toml:7`, `CITATION.cff:5`, `.zenodo.json` og `CHANGELOG.md` («## [1.0.0] - 2026-10-27»); DOI-en, `date-released` lik publiseringsdatoen og utgivelsestaggen gjenstår og gjøres ved frysen (KLAR-ARK-0008 v1.6 (i git-historikken), D4) | CHANGELOG, KLAR-ARK-0008 |

Rekkefølgen er endret (AV-20): steg 9, deretter H1–H3 (steg 10–12), deretter innlesing og H4 (steg 13–14), som utgår i v1.0 (AV-27). PREREG sier det motsatte (innlesingen gjøres og scores før noen testdel kjøres). Testdelene kjøres med `scripts/kjor_testdel.sh` (H1, H2, H3, H4, eller `alle`), én og én med commit og push mellom hver (speil ble hoppet over per del, AV-21). Kjente forhold som må være avgjort før steg 10: se `KLAR-LOG-0003` (AV-10, AV-11). Testdelenes datafiler ble lastet ned i steg 9. H1–H3 er kjørt (2026-10-27); H4 gjennomføres ikke i v1.0 (AV-27).

## Åpne punkter

- **A1–A3 avgjort av Eirik 2026-10-27** (KLAR-ARK-0008 v1.3 (i git-historikken)): A1 = H4 gjennomføres ikke i v1.0, blindtesten blir v1.1; A2 = AGPL-3.0-or-later for egen kode, med kommersiell lisens fra rettighetshaveren som tillegg; A3 = full historikk publiseres, med lisenserklæring for hele historikken; A3 endret 2026-10-28 (AV-34): offentlig repo fra rent tre, full historikk i tilgangsstyrt deponering.
- **H4 (steg 13–14): utgår i v1.0 (AV-27).** Innleserfeilen (AV-19) ble funnet og rettet i grenen h4-fiks (ADR-0018 v1.1 (i git-historikken)), men innlesingen gjøres ikke i v1.0: testmanuset og mønstrene i personvernmotoren er laget av samme forfatter, og målingen ville hatt én leser, så den ville ikke gitt ekstern gyldighet. Kategoriene uten naturlige forekomster i H1–H3 er ikke målt på tale i v1.0.


## Etter v1.0 (ikke del av v1.0)

| Punkt | Hvorfor det venter | Grunnlag |
|---|---|---|
| **v1.1: blindtest på NB Tale modul 3** med egen preregistrering (`KLAR-PREREG-0003`, reservert) | Ekstern test på spontan dialekttale utenfor NB-Whispers treningsdata; erstatter ikke H4 i v1.0 (A1, AV-27) | KLAR-ARK-0008 v1.3 (i git-historikken) (A1, seksjon E) |
| Museumspilot med egen preregistrering (`KLAR-PREREG-0002`, reservert) | Krever ja fra museet; lages før pilotdata kjøres | gt_fast, PREREG-0001 |
| Måling på ekte arkivlyd (pauser, støy, bånd, dialekt) | Alle tall til nå er DEV eller offentlige datasett; hallusinasjon i stillhet er ikke utelukket | ADR-0004, README «Begrensninger» |
| Menneskelig godkjenningsflate og alias-tabell | v1.0 har ingen; utdata er forslag, ikke klarering | ARK-0001 § 5 |
| Entitetsmodul (`entiteter.py` er en stubb) | Planlagt, ikke bygget | ARK-0001 § 5 |
| Nynorsk navnegjenkjenning | spaCy har ingen nynorskmodell; nynorsk er svakere enn bokmål | MASTER, EVAL-0005 |
| Talte e-postadresser | Whisper skriver dem ikke som adresser (0 av 12) | EVAL-0008 |
| Vurdering av katalogmodellen (norsk kvalitet, Gemma-lisens) | Valgt mekanisk på fire DEV-utdrag | MASTER, ADR-0013 |
| Gullsett til Språkbanken | Først etter klarering og avtale med eier | ADR-0011 |
| Flere lesere i H4 | Med én leser (forfatteren) gjelder H4 bare én taler | PREREG-0001, avvik punkt 8 |
| Forbedringer i innleseren: tastatursnarveier, kvalitetskontroll per opptak (for stille, for kort, tomt), ekstra opptakstid på slutten, avbryte opptak, direkte wav-opptak uten opus-steg, metadata per opptak (enhet, varighet, toppnivå, samplingsrate) | Ikke nødvendig for protokollen; ville endre koden under taggen | ADR-0018 |
| Overlapp mellom testdelene og NB-Whispers treningsdata | Ikke kontrollert | EVAL-0005, EVAL-0007 |

Utsatt til etter v1.0: sammenligning med ePADD og TNA/FCDO sensitivity review, primærkilde for Beeld en Geluid (RG-02d), elusion-validering som kandidat for KLAR-PREREG-0002, mikrofoneffekt med NB Tale (egen preregistrering, erstatter ikke H4).

Musikk under tale: vurder PANNs/AST (ADR-0019 B/C). Standard segmentering i verktøyet: inaSpeechSegmenter; inaVAMOS valgfritt bare for reproduksjon av H1/H2.
