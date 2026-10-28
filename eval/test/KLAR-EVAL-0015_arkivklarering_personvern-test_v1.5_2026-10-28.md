# KLAR-EVAL-0015: H3, NorNE test (navnegjenkjenning), med 95 %-intervaller og terskelvurdering

Versjon 1.5, 2026-10-28 (v1.5: beskrivelsen av bootstrap over setninger sier at trekket gjøres per gruppe (målform, type, motor, variant) med n = 1 939 (bokmål) eller 1 511 (nynorsk) setninger, ikke 3 450 per konfigurasjon; ingen tall og ingen klassifisering endret; v1.4: det åpne punktet om H3-primærintervall er markert «avgjort 2026-10-27, se AV-24» i stedet for fjernet; v1.3: det åpne punktet var avgjort av eier (AV-24), ingen tall og ingen klassifisering endret; v1.0: resultatfila `…_v1.0_2026-10-27.json` og `….setninger.json` fra skriptet, uendret; v1.1: intervaller og terskelvurdering; v1.2: «klart bekreftet» følger Wilson som primærintervall, bootstrap over setninger er sensitivitetsanalyse og merket slik; eneste endring i klassifisering: H3d recall; ingen tall endret). Datasett: `NbAiLab/norne`, configene `bokmaal` og `nynorsk`, del `test`, hele delen, revisjon `1ca12d437b84f65a34c454d339317d39d35c8149`: 1 939 bokmålssetninger og 1 511 nynorskssetninger (3 450). Ingen setninger hoppet over (`setninger_hoppet_over_pga_tokenjustering` er tom). Kjørt én gang via `scripts/kjor_testdel.sh H3`.

**Foreknowledge (avvik 1 i PREREG, ordrett):** «Foreknowledge på OSF ble satt til ‹Authors have observed the data, but have not performed the proposed analyses›. Det riktige er: testdelene (NB Samtale, NorNE, NPSC test) er ikke lastet inn eller observert (sperret i koden). Testmanuset er skrevet av forfatterne, men ingen opptak finnes. DEV-dataene (validation) er observert.» Valget på OSF er ikke endret.

H3 er **sekundær** i PREREG og brukes ikke til å redde eller felle H1 og H2. «Hele motoren» er konfigurasjonen `kombinert` (spaCy `nb_core_news_md` + NB-BERT-NER + mønstre, terskel 0; `eval/dev/kjor_personvern_dev.py:14` og `:133`), tekstform `original`. Recall (overlapp) er hovedmålet (KLAR-ADR-0012).

## Terskler (PREREG; punktestimat; primærintervall: Wilson; bootstrap over setninger er sensitivitetsanalyse)

«Klart bekreftet» vurderes mot Wilson-grensen (primærintervallet, se «Intervallmetode»). Kolonnen «bootstrap (sensitivitet)» er en sensitivitetsanalyse og avgjør ikke klassifiseringen.

| id | gruppe | gull / predikert | recall (DEV → test) | terskel | Wilson 95 % | bootstrap 95 % (sensitivitet) | utfall recall |
|---|---|---|---|---|---|---|---|
| H3a | bokmål, person | 564 / 623 | 0,997 → **1,000** | ≥ 0,95 | 0,993–1,000 | 1,000–1,000 | bekreftet, klart |
| H3b | bokmål, sted | 360 / 438 | 0,970 → **0,975** | ≥ 0,95 | 0,953–0,987 | 0,955–0,991 | bekreftet, klart |
| H3c | nynorsk, person | 397 / 532 | 0,954 → **0,982** | ≥ 0,90 | 0,964–0,991 | 0,969–0,995 | bekreftet, klart |
| H3d | nynorsk, sted | 253 / 321 | 0,986 → **0,976** | ≥ 0,95 | 0,949–0,989 | 0,956–0,992 | bekreftet, ikke klart (Wilson-grense 0,949 < 0,95); sensitivitet: bootstrap nedre 0,956 ≥ 0,95 |

| id | gruppe | presisjon (DEV → test) | terskel | Wilson 95 % | bootstrap 95 % (sensitivitet) | utfall presisjon |
|---|---|---|---|---|---|---|
| H3a | bokmål, person | 0,921 → **0,904** | ≥ 0,85 | 0,878–0,924 | 0,879–0,927 | bekreftet, klart |
| H3b | bokmål, sted | 0,875 → **0,811** | ≥ 0,80 | 0,771–0,844 | 0,769–0,848 | bekreftet, ikke klart (nedre 0,771 / 0,769 < 0,80) |
| H3c | nynorsk, person | 0,769 → **0,733** | ≥ 0,70 | 0,694–0,769 | 0,693–0,773 | bekreftet, ikke klart (nedre 0,694 / 0,693 < 0,70) |
| H3d | nynorsk, sted | 0,738 → **0,769** | ≥ 0,65 | 0,720–0,812 | 0,713–0,822 | bekreftet, klart |

Alle åtte terskler (fire recall, fire presisjon) er oppfylt av punktestimatet. Fem er klart bekreftet etter Wilson (H3a recall og presisjon, H3b recall, H3c recall, H3d presisjon); tre er bekreftet uten å være klare: H3d recall (Wilson-grense 0,949 < 0,95; bootstrap-grensen 0,956 ligger over, som sensitivitet) og presisjonene H3b og H3c (begge intervallmetoder under terskelen). Presisjonen er hovedsvakheten, spesielt i nynorsk der den ligger lavest (person 0,733, sted 0,769): motoren flagger mer enn gullet.

Alle 24 kombinasjoner (målform × type × konfigurasjon × tekstform) med begge intervallene står i listen nederst.

**K3 (kontrollsjekk, ikke hypotese):** recall (overlapp) for hele motoren faller minst 0,15 på små bokstaver uten tegnsetting (som rålaget) mot original tekst, i alle fire grupper: bokmål person 1,000 → 0,551 (−0,449), bokmål sted 0,975 → 0,694 (−0,281), nynorsk person 0,982 → 0,564 (−0,418), nynorsk sted 0,976 → 0,498 (−0,478). Kriteriet (≥ 0,15 i alle fire) er oppfylt. Det gjelder også for BERT og spaCy hver for seg (minste fall 0,250, spaCy bokmål sted). Fallene er beregnet fra de avrundede recall-verdiene i tabellen under.

## Tolkning (for hånd)

Hele motoren finner nesten alle navn i original tekst (recall 0,975–1,000), men avhenger sterkt av store bokstaver: uten dem faller recall til 0,50–0,69 (K3). Navnegjenkjenningen i rørledningen er altså følsom for hvilken tekstform transkripsjonslaget leverer; NorNE alene sier ikke hvilken form lagene faktisk gir. NorNE er skrevet tekst, ikke tale; tallene sier ingenting om hvordan motoren oppfører seg på transkripsjoner med feil (det måler H2, og H4 på menneskeinnlest manus er ikke gjennomført).

## Intervallmetode (PREREG «Statistical models» linje 166, avvik 7, 9 og 11a)

**Primærintervall: Wilson. Bootstrap over setninger: sensitivitetsanalyse.** PREREG er ikke eksplisitt om rangeringen for H3. Teksten (`prereg-v1`, linje 166, uendret i v1.16) har to setninger som begge treffer H3: «Proporsjoner med Wilson-95 %-intervall (H2, H3, H4)» og «NorNE: bootstrap over setninger.» Avvik 7, 9 og 11a rangerer dem heller ikke (avvik 9: bootstrap regnes «ved siden av Wilson»). Åpent punkt (ført i v1.2: valget av primærintervall for H3 var ikke tatt av PREREG og ført til eier): **avgjort 2026-10-27, se AV-24.** Eier har besluttet at Wilson er primær for H3 og at bootstrap over setninger rapporteres som sensitivitetsanalyse. Beslutningen er tatt etter at resultatene var kjent, og går i retning av den mer konservative klassifiseringen. Det endrer klassifiseringen av ett utfall (H3d recall, se over); ingen tall er endret. Begge metodene er brukt og rapportert side om side:
- **Wilson 95 %** for recall og presisjon fra tellerne (z = 1,96): `scripts/rapporter_intervaller.py:39–47` (`wilson`), kall i `norne_tabell` (`:156`, `:163`). Resultatfila har selv Wilson-intervallet for recall (`recall_overlapp_ki95`): `eval/dev/kjor_personvern_dev.py:183` og `:186`, `wilson` definert på linje 100. Presisjonens Wilson-intervall kommer bare fra rapportskriptet.
- **Bootstrap over setninger** (PREREG, avvik 9 / AV-15): `scripts/rapporter_intervaller.py:128–153` (`norne_bootstrap`). Cluster-enheten er setningen (en rad per setning i `….setninger.json`; trekket gjøres per gruppe (målform, type, motor, variant; linje 133–135) med n = antall setninger i gruppen, 1 939 for bokmål og 1 511 for nynorsk (3 450 til sammen), med tilbakelegging, `rng.integers(0, n, size=(b, n))`, linje 142). B = 2000 (`B`, linje 29), seed 20261026 (`SEED`, linje 30), `numpy.random.default_rng(seed)` (linje 136) brukt i rekkefølgen av sorterte gruppenøkler (linje 137–138). Recall = Σ treff / Σ gull og presisjon = Σ treff / Σ predikert per gjentak; gjentak med null nevner utelates. Persentilintervall: nedre = element `int(0,025·n)`, øvre = element `int(0,975·n) − 1` av de sorterte verdiene (linje 151).

Primærintervallet (Wilson) følger PREREG linje 166 og avvik 7; bootstrap over setninger følger avvik 9 og er sensitivitetsanalysen. Der de to er uenige om «klart bekreftet» (H3d recall), gjelder Wilson. Kommando: `.venv/bin/python scripts/rapporter_intervaller.py norne <resultat.json> <setninger.json>`.

## Kjøring

Metafil: `KLAR-EVAL-0015_arkivklarering_personvern-test_v1.0_2026-10-27_kjoring_meta.json`. Start 2026-10-27T13:03:59Z på commit `efcfc42374c3aee52f9ebe284877dbb6c5dc8428`, slutt 13:12:57Z (motorer klare etter 15 s, bokmål ferdig etter 308 s, nynorsk ferdig etter 536 s; tidene i skriptloggen er fortløpende), returkode 0, `git status --porcelain` tom ved start, kode uendret siden `testkjoring-v2` (`c49d17463c14f7719f9f271ae3d4af4824436c35`). Resultat committet som `3e34815`.

## Alle grupper (recall og presisjon, overlapp)

| målform \| type \| motor \| variant | recall | Wilson 95 % | presisjon | Wilson 95 % | bootstrap recall | bootstrap presisjon |
|---|---|---|---|---|---|---|
| nb\|person\|bert\|original | 1,000 | 0,993–1,000 | 0,966 | 0,948–0,978 | 1,000–1,000 | 0,949–0,980 |
| nb\|person\|bert\|små | 0,436 | 0,396–0,477 | 0,969 | 0,940–0,984 | 0,391–0,483 | 0,945–0,988 |
| nb\|person\|kombinert\|original | 1,000 | 0,993–1,000 | 0,904 | 0,878–0,924 | 1,000–1,000 | 0,879–0,927 |
| nb\|person\|kombinert\|små | 0,551 | 0,510–0,592 | 0,910 | 0,875–0,936 | 0,507–0,593 | 0,877–0,939 |
| nb\|person\|spacy\|original | 0,936 | 0,913–0,954 | 0,907 | 0,881–0,928 | 0,915–0,956 | 0,882–0,931 |
| nb\|person\|spacy\|små | 0,429 | 0,389–0,470 | 0,905 | 0,863–0,935 | 0,387–0,473 | 0,871–0,938 |
| nb\|sted\|bert\|original | 0,964 | 0,939–0,979 | 0,921 | 0,890–0,944 | 0,942–0,983 | 0,889–0,950 |
| nb\|sted\|bert\|små | 0,339 | 0,292–0,389 | 0,919 | 0,860–0,954 | 0,285–0,391 | 0,862–0,966 |
| nb\|sted\|kombinert\|original | 0,975 | 0,953–0,987 | 0,811 | 0,771–0,844 | 0,955–0,991 | 0,769–0,848 |
| nb\|sted\|kombinert\|små | 0,694 | 0,645–0,740 | 0,847 | 0,802–0,884 | 0,646–0,743 | 0,803–0,888 |
| nb\|sted\|spacy\|original | 0,844 | 0,803–0,878 | 0,817 | 0,775–0,853 | 0,804–0,880 | 0,772–0,859 |
| nb\|sted\|spacy\|små | 0,594 | 0,543–0,644 | 0,835 | 0,785–0,876 | 0,541–0,649 | 0,786–0,882 |
| nn\|person\|bert\|original | 0,977 | 0,957–0,988 | 0,977 | 0,957–0,988 | 0,962–0,990 | 0,961–0,992 |
| nn\|person\|bert\|små | 0,436 | 0,388–0,485 | 0,989 | 0,960–0,997 | 0,380–0,490 | 0,970–1,000 |
| nn\|person\|kombinert\|original | 0,982 | 0,964–0,991 | 0,733 | 0,694–0,769 | 0,969–0,995 | 0,693–0,773 |
| nn\|person\|kombinert\|små | 0,564 | 0,515–0,612 | 0,648 | 0,596–0,696 | 0,513–0,614 | 0,593–0,696 |
| nn\|person\|spacy\|original | 0,859 | 0,821–0,890 | 0,713 | 0,670–0,751 | 0,824–0,891 | 0,671–0,756 |
| nn\|person\|spacy\|små | 0,388 | 0,341–0,437 | 0,560 | 0,501–0,617 | 0,339–0,437 | 0,500–0,620 |
| nn\|sted\|bert\|original | 0,968 | 0,939–0,984 | 0,866 | 0,822–0,901 | 0,945–0,988 | 0,810–0,916 |
| nn\|sted\|bert\|små | 0,253 | 0,203–0,310 | 0,788 | 0,690–0,862 | 0,200–0,310 | 0,692–0,875 |
| nn\|sted\|kombinert\|original | 0,976 | 0,949–0,989 | 0,769 | 0,720–0,812 | 0,956–0,992 | 0,713–0,822 |
| nn\|sted\|kombinert\|små | 0,498 | 0,437–0,559 | 0,746 | 0,676–0,805 | 0,441–0,556 | 0,669–0,815 |
| nn\|sted\|spacy\|original | 0,739 | 0,682–0,789 | 0,759 | 0,702–0,808 | 0,679–0,794 | 0,695–0,820 |
| nn\|sted\|spacy\|små | 0,336 | 0,281–0,396 | 0,714 | 0,627–0,788 | 0,277–0,394 | 0,627–0,795 |
