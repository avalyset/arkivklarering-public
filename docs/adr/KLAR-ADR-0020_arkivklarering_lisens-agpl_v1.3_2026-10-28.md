---
status: vedtatt 2026-10-27; A3 endret 2026-10-28
date: 2026-10-27
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0020: AGPL-3.0-or-later med kommersiell lisens som tillegg; full historikk i tilgangsstyrt deponering

Versjon 1.3, 2026-10-28 (v1.3: DOI for den tilgangsstyrte historikken er satt inn: 10.5281/zenodo.23723450 (steg 4.5); v1.2: A3 er endret (Eiriks beslutning 2026-10-28, AV-34): offentlig repo fra rent tre, full historikk i tilgangsstyrt deponering; tittelen, A3, begrunnelsen, alternativene og konsekvensene er oppdatert; v1.1: pekere til versjoner som ikke er i treet er merket «(i git-historikken)», og pekere med linjenummer til forrige versjon av et dokument med ny versjon viser til den nye versjonen, samme linje; kontrollert med `scripts/sjekk_pekere.py`, 0 brudd (KLAR-LOG-0005, restfunn etter kontrollen); v1.0: første versjon; fører Eiriks beslutninger A2 og A3 2026-10-27 fra KLAR-ARK-0008 v1.3).

## Kontekst

Repoet hadde en LICENSE-fil med Apache-2.0 fra commit `9ff2d1a` (v0.4, 2026-10-26), men lisensen for egen kode var ikke vedtatt (KLAR-ARK-0008 v1.0 (i git-historikken)–v1.2, A2: «Apache-2.0 (står, ikke vedtatt)»). Før repoet gjøres offentlig må to ting være avgjort: hvilken lisens egen kode får (A2), og om hele git-historikken publiseres (A3). Historikken bærer etterprøvbarheten: preregistreringen (OSF hc83q) og avvikene viser til commit-SHA-er og tagger (`prereg-v1`, `testkjoring-v1`–`v6`, `h4-rigg-v3`), og OpenTimestamps-stemplene i `docs/stempler/` stempler både dokumenter og HEAD-filer (`HEAD_<sha>.txt`) som peker på commit-SHA-er.

## Beslutning (Eirik, 2026-10-27)

Ordrett: «Stopp beslutningsteateret og lever hel ved» = godkjenning av chat-Claudes anbefalinger (KLAR-ARK-0008 v1.3 (i git-historikken), A2 og A3).

- **A2: egen kode er lisensiert GNU Affero General Public License v3.0 eller senere (`AGPL-3.0-or-later`), med kommersiell lisens fra rettighetshaveren som tillegg.** Rettighetshaver: Eirik Botten Nicolaysen, EcoDeco AS (`NOTICE`). `LICENSE` er lisensteksten ordrett fra gnu.org (KLAR-KILDE-0001 v1.7 (i git-historikken), K123; byte-lik den lagrede kopien). For bruk som ikke er forenlig med AGPL, tilbys kommersiell lisens: eirik@ecodeco.no.
- **A3 (endret 2026-10-28): det offentlige repoet lages fra et rent tre, og hele historikken deponeres med begrenset tilgang.** Eiriks beslutning 2026-10-28, ordrett: «A3 er endret (Eiriks beslutning 2026-10-28): offentlig repo fra rent tre, full historikk i tilgangsstyrt deponering». `avalyset/arkivklarering-public` har én commit («arkivklarering v1.0») med treet ved HEAD i det private repoet (`git archive`); hele git-historikken (`git bundle create --all`) deponeres på Zenodo med begrenset tilgang og tilgang på forespørsel (DOI 10.5281/zenodo.23723450), under AGPL-3.0-or-later. Det private repoet forblir privat. Lisenserklæringen i `LICENSING-HISTORY.md` gjelder hele historikken: commitene med Apache-2.0-LICENSE og de 16 første commitene uten lisensfil er lisensiert AGPL-3.0-or-later. A3 slik den ble vedtatt 2026-10-27 (hele historikken publiseres) gjelder ikke lenger.
- **Tredjepart beholder egne lisenser:** vendor-kopien fra norsk-tale (Apache-2.0, egen `LICENSE` i `arkivklarering/_vendor/norsk_tale/`), modellene som lastes ned separat og inaSpeechSegmenter/inaVAMOS (`NOTICE`; README «Lisens»).

## Begrunnelse

- **AGPL hindrer at andre lukker koden i en vertstjeneste.** AGPL § 13 («Remote Network Interaction») krever at brukere som samhandler med et endret program over nettverk, tilbys kildekoden (KLAR-KILDE-0001 GN-03). En tjenesteleverandør kan derfor ikke ta verktøyet, endre det og tilby det som lukket nettjeneste til arkiv.
- **Lokal bruk hos arkiv er fri.** Verktøyet er laget for å kjøre lokalt hos den som klarerer (KLAR-ADR-0007). AGPL § 2 bekrefter en ubegrenset rett til å kjøre det uendrede programmet (KLAR-KILDE-0001 GN-04), og plikten i § 13 gjelder bare et endret program som brukere samhandler med over nettverk.
- **Kommersiell lisens som tillegg** gir en vei for bruk som ikke er forenlig med AGPL (for eksempel innbygging i et lukket produkt), uten at den åpne lisensen svekkes.
- **«Eller senere»** følger AGPL § 14: programmet kan følge den nummererte versjonen eller en senere versjon fra Free Software Foundation (KLAR-KILDE-0001 GN-02).
- **Full historikk gjør prereg-v1 og stemplene etterprøvbare.** Preregistreringen, avvikstabellen (KLAR-LOG-0003) og `kjoring_meta`-filene for H1–H3 viser til commit-SHA-er og tagger, og OTS-stemplene og HEAD-filene i `docs/stempler/` peker på commit-SHA-er. En omskrevet eller ny historikk ville gjort disse henvisningene ugyldige. **Tilgangsstyringen (2026-10-28):** historikken har sju oppdiktede telefonnumre i tildelte nummerserier (AV-29); de kan ikke fjernes uten å skrive om historikken, og omskriving ville brutt beviskjeden til PREREG og stemplene. Prinsippet er «så åpent som mulig, så lukket som nødvendig»: treet er offentlig, historikken er tilgjengelig på forespørsel, og numrene publiseres ikke.

## Alternativer som ble vurdert

- **Apache-2.0 (det som sto i repoet):** forkastet. Tillater at andre lukker endret kode, også i en vertstjeneste.
- **Lukket (ingen åpen lisens):** forkastet. Hindrer etterprøving og ekstern bruk hos arkiv, og er uforenlig med JOSS-kravet om en OSI-godkjent lisens (KLAR-ARK-0008, F4).
- **Ren AGPL uten kommersiell lisens:** forkastet. Gir ingen vei for bruk som ikke er forenlig med AGPL.
- **Ny historikk (squash eller nytt repo):** forkastet. Bryter henvisningene fra preregistreringen, avvikene, `kjoring_meta`-filene og stemplene til commit-SHA-ene. (2026-10-28: et nytt offentlig repo fra rent tre er valgt, men bare sammen med den tilgangsstyrte deponeringen av hele historikken, der henvisningene kan etterprøves; omskriving av historikken er fortsatt forkastet. Å publisere hele historikken som den er, er forkastet fordi numrene i tildelte serier da ville blitt offentlige.)

## Konsekvenser

- `LICENSE`, `NOTICE`, `pyproject.toml` (`license = "AGPL-3.0-or-later"`), `CITATION.cff`, `.zenodo.json`, README («Lisens») og `CONTRIBUTING.md` er endret i samme commit, rett oppå `57dedaf` (`testkjoring-v6`). Ingen kode er endret.
- `LICENSING-HISTORY.md` beholder plassholderen `[PUBLISERINGSDATO]` til publiseringen. Erklæringen er ikke juridisk vurdert. Commit-SHA-ene som PREREG, `kjoring_meta`-filene, kodetaggene og stemplene viser til, finnes i den tilgangsstyrte historikken (DOI 10.5281/zenodo.23723450); KLAR-MANUS-0002 v1.2 (i git-historikken), som OSF-registreringen låser med sha256, kan etterprøves der.
- Bidrag lisensieres under AGPL-3.0-or-later (`CONTRIBUTING.md`). Kode fra andre bidragsytere kan bare inngå i en kommersiell lisens etter egen avtale med bidragsyteren; det finnes ingen bidragsavtale ennå.
