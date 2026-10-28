# KLAR-LOG-0005: Portfunn, runde 3 (publiseringsporten for v1.0)

Versjon 1.0, 2026-10-28. Forfatter: Eirik Botten Nicolaysen, EcoDeco AS.

Funnlista fra publiseringsporten, runde 3 (én Opus-subagent, HEAD `bf48dfe`), ført ordrett fra rapporten på Vault (`reproduksjon/port-v1.0/port_runde3_2026-10-28_HEAD-bf48dfe.md`, sha256 `a9bfe2d849988e7ca3f3c9bb0bbb22f8cec6371ce7deacaa5ee5017d1101ffb5`) FØR noe rettes. Rapporten har ellers: (g) 0 funn, (i) ren installasjon bestått, 66 av 69 funn fra runde 2 bekreftet rettet (de tre andre er funn 3, 8 og 9 her). Status føres i tabellen nederst.

## FUNN I TREET

Format: fil:linje | klasse | hva | retting.

1. `eval/test/KLAR-EVAL-0013_…_v1.0_2026-10-27_kjoring_meta.json:24`, `…EVAL-0014…_kjoring_meta.json:22` og `…EVAL-0015…_kjoring_meta.json:23` | f/a | Kjøringsmetadataene fra 2026-10-27 (H1 startet `07:42:54Z`) har fått `"fil": "docs/KLAR-PREREG-0001_arkivklarering_testdeler_v1.28_2026-10-28.md"` i den mekaniske commiten `bf48dfe`. Fila fantes ikke da kjøringen ble gjort. `"sha256": "56b1cc80…"` er sha256 for v1.16 (`git show bfe094e:…v1.16…`), mens v1.28 har `c7a0ebb3…`. Kjøringsprotokollen sier dermed noe som ikke stemmer, og ARK-0009 v0.9:53 og :174 viser til disse filene som belegg. | Sett `fil` tilbake til `docs/KLAR-PREREG-0001_arkivklarering_testdeler_v1.16_2026-10-27.md`, som i `bfe094e`. Kjøringsmetadata skal aldri omskrives mekanisk.

2. `docs/KLAR-GT-0001_arkivklarering_ground-truth_v1.34_2026-10-28.md:30–161`, `:9`, `:26`, `:83`, `:174`, `:180` og `:217` | a/f/e | Den mekaniske omskrivingen har ødelagt den genererte fila:
   - :30–32 lister `…ARK-0001…v1.9…` tre ganger, som «v1.4», «v1.5» og «v1.6». Det samme mønsteret står for ARK-0003, -0004, -0005, -0006, -0008, -0009, KILDE, LOG-0003, PREREG, ADR-0003, ADR-0019 og EVAL-0013–0015.
   - 30 av stiene finnes ikke, for eksempel :33 ARK-0001 v1.8, :83 GT v1.33, :124 ADR-0004 v1.3, :146 og :217 LOG-0002 v1.33, :174 «register: …v1.23», og :180 KILDE v1.11 med «252 påstander».
   - :9 HEAD er `d89fc90`, og :26 sier «211 passed».
   - Fila har sha256 `f3d801d1…`. Stempelet i LOG-0002 v1.35:291 og `docs/stempler/…v1.34…a098e469a109.ots` gjelder `a098e469…`, som er innholdet i `058f3ff`. `ots verify -f` mot treet feiler derfor. Det er den eneste stemplede fila i treet som ikke stemmer med noe stempel.
   - Rettingen av funn 66 i generatoren (951091e) vises ikke, fordi GT ikke er generert på nytt. Funn 3 sa «GT regenereres».
   | Sett v1.34 tilbake til innholdet i `058f3ff`, så stempelet holder. Generer GT v1.35 på HEAD med den rettede generatoren. Hold GT utenfor mekaniske omskrivinger.

3. `docs/KLAR-ARK-0008_arkivklarering_avklaringer-foer-frys_v1.8_2026-10-28.md`, A, B og D | e/a | Pekere som ble feil i den mekaniske omskrivingen (stien er byttet, men linjenummeret er beholdt) eller som peker på fjernede versjoner:
   - **:13 (A1):** «PREREG v1.28:1172 (avvikspunkt 20)». Linje :1172 er punkt 15 (AV-22), og AV-27 står på :1177. I tillegg peker «`…LOG-0001…v1.45…`:1502» på en fil som er fjernet; teksten står på v1.48:1502.
   - **:17 (A5):** «v1.4 (`…EVAL-0015…v1.5…:39`) er gjeldende versjon».
   - **:28 (B2):** viser til `…ADR-0019…v1.3…:22`, som er fjernet. Sitatet står i v1.5:22.
   - **:32 (B6):** «rader :206–231», «26 rader», «AV-01–AV-26». Tabellen i PREREG v1.28 er nå :206–237, med 32 rader (AV-01–AV-32).
   - **:33 (B7):** «den fete setningen i :237». Linje :237 er raden for AV-32, og avvikspunkt 1 står på :243.
   - **:34 (B8):** «(v1.6: README lenker nå til v1.4)», mens sitatet og README:166 lenker til v1.5.
   - **:44–46 (B3 (a)):** etter «v1.12:340» for DL-01 står «:328», «:329» og så videre for DL-02–DL-10. I v1.12 er :328–336 OL-09–OL-17, og DL-02–DL-10 står på :341–349.
   - **:124:** «`CHANGELOG.md:53` (historikk)». Embargo-linjen står nå på :55.
   - **:212:** «KLAR-ARK-0005 v1.6:46, :89» er fjernet. Gjeldende er v1.7.
   | Lag ARK-0008 v1.9 med pekerne kontrollert mot gjeldende linjer.

4. ARK-0008 v1.8, F-radene :169, :175, :176, :177, :178 og :183 (samt :7, :208 og :211) | h/e | Bevispekerne for OPPFYLT-radene er brutt:
   - F4 (:169): «GN-01 (:376, verifisert)». KILDE v1.12:376 er JO-02, og GN-01 står på :381.
   - F10, F11, F12, F13 og F18 viser til `docs/KLAR-LOG-0001_arkivklarering_avvik-og-hendelser_v1.45_2026-10-27.md:1526–1554`. Den fila finnes ikke i treet, og den står ikke blant de 30 unntakene i LOG-0004. Innholdet står på de samme linjene i v1.48 (kontrollert for :1502, :1524–1532, :1552 og :1554).
   Statusene holder, men beviset må kunne leses i treet. | Pek på v1.48 og KILDE v1.12:381.

5. `ARK-0008 v1.8:219`, `:31`, `:34`; `eval/test/KLAR-EVAL-0013_…_v1.3_2026-10-27.md:3`, `:47`, `:49`; `eval/test/KLAR-EVAL-0014_…_v1.4_2026-10-27.md:3`, `:59`, `:61` | a | `bf48dfe` har skrevet om historikk og sitater, selv om LOG-0004:189 sier at «Historiske omtaler … er ikke skrevet om»:
   - **ARK-0008:219:** rundene for v1.4, v1.3 og v1.1 oppgir nå at KILDE v1.12, ARK-0003 v1.25, LOG-0003 v1.17, PREREG v1.28, ARK-0004 v1.5, ARK-0005 v1.7 og ARK-0009 v0.9 ble laget i de rundene. I tillegg nevnes «ARK-0006 v1.9», som ikke finnes.
   - **ARK-0008:31 og :34:** sitatene av README er endret til `](../NOTICE)` og `](adr/…)`. README:245 har `](NOTICE)`, og README:166 har `](docs/adr/…)`, så sitatene er ikke lenger ordrette.
   - **EVAL-0013 v1.3 og EVAL-0014 v1.4:** dokumentene er datert 2026-10-27 og endret på plass, slik at de sier at sitatene ble «kopiert fra sitatfeltet i `…kilderegister_v1.12_2026-10-28.md`». Det strider mot CONTRIBUTING:18 («Versjonerte dokumenter (`KLAR-*`) endres ikke»).
   | Sett linjene tilbake til teksten i `20440a5` (ARK-0008) og `bfe094e` (EVAL-0013 og EVAL-0014).

6. `docs/KLAR-ARK-0004_…_v1.5_2026-10-28.md` (35 kortformpekere), `docs/KLAR-ARK-0005_…_v1.7_2026-10-28.md` (13 pekere) og `KLAR-KILDE-0001 v1.12:3` | e/a | Funn 64 er bare delvis gjennomført:
   - **ARK-0004** viser til versjoner som ble fjernet i `bf48dfe`, blant annet «KLAR-EVAL-0013 v1.2:49», «KLAR-EVAL-0014 v1.3:61» og «v1.3:11» (:126), «v1.2:57» og «v1.3:69» (:127), «KLAR-EVAL-0015 v1.4:39» (:47), ADR-0019 v1.2 (:15, :26, :53, :63, :131) og ARK-0006 v1.8:59 (:135). Det gjelder også :41, :52, :61, :69, :78, :80, :93, :102, :129 og :132–134.
   - **ARK-0005** har samme type pekere på :12, :15, :29–31, :71–73, :82 og :93: EVAL-0013 v1.2, EVAL-0014 v1.3, EVAL-0015 v1.4, PREREG v1.22, KILDE v1.3 og ADR-0019 v1.2.
   - Ingen av disse står i LOG-0004-lista over de 30 unntakene, og det er samme type som funn 57–59 i runde 2.
   - KILDE v1.12:3 sier at «kolonnen «dokument:linje» peker ikke lenger på versjoner som ikke finnes». Det er usant etter `bf48dfe`: 28 rader gjør det (LOG-0004:191–220).
   | Pek på gjeldende versjoner (EVAL-0013 v1.3, EVAL-0014 v1.4, EVAL-0015 v1.5, ADR-0019 v1.5 osv.) med linjene kontrollert, eller merk hver peker «(i git-historikken)». Skriv om KILDE:3. Unntak: versjonsnotatene og ARK-0004:27, som bevisst er historiske.

7. `docs/KLAR-ARK-0002_arkivklarering_navnekonvensjon_v1.4_2026-10-28.md:24–25` (og :3) | b | Regelen «en ny versjon … erstatter den gamle i arbeidstreet» står uten unntak, og :3 sier at regelen er uendret. HEAD har likevel eldre versjoner ved siden av nyere: REG-0001 v1.0 (ved siden av v1.2), EVAL-0002 v1.0, EVAL-0006 v1.0 og v1.1, EVAL-0007 v1.0, EVAL-0008 v1.2 og EVAL-0013 v1.0 (md). Unntaket er bare begrunnet i LOG-0004:189. Runde 2 (funn 64) ba om at regelen ble endret eller at filene ble fjernet. | Legg inn unntaket i ARK-0002 § 3: den registrerte teksten, og md-filer som har en JSON-fil med samme stamme.

8. PREREG v1.28:237 og :1182; LOG-0003 v1.17:38; LOG-0001 v1.48:1576, :1580 og :1582; ARK-0004 v1.5:8; CHANGELOG:10 og :11; ARK-0008 v1.8:3, :125, :213 og :215 | a | Taggen `testkjoring-v9` og statusen for funn 64 og 66 stemmer ikke med git:
   - `git diff testkjoring-v8 testkjoring-v9` endrer også `scripts/ground_truth.py` (+3) og `tests/test_ground_truth_wer.py` (en ny test), altså rettingen av funn 66. AV-32 sier likevel overalt «bare hjelpeteksten til `--ingen-ordtider` … og kodetaggen», og LOG:1580 sier «Ingen annen kodeendring».
   - LOG-0004:74 sier «66 rettet i testkjoring-v9». ARK-0008 v1.8:3, :125, :213 og :215, LOG:1576 og CHANGELOG:11 sier derimot at 66 ikke er rettet, og at rettingen krever en endring som ikke er tillatt.
   - De samme stedene sier at funn 64 ikke er gjort, selv om `bf48dfe` har gjort det.
   - Kontrollen på LOG:1586 («211 passed») ble kjørt før den nye testen kom.
   | Før opp endringen i `ground_truth.py` og testen i AV-32 (PREREG punkt 25, tabellraden, LOG-0003, LOG, ARK-0004:8 og CHANGELOG), og oppdater statusen for 64 og 66.

9. `README.md:130` | e | «Dagens tall … 211 av 214 tester … 207 bestått, 4 hoppet over … Med datarota på Vault: 211 bestått». På `testkjoring-v9` og HEAD `bf48dfe` er tallene 212 av 215 innsamlet, og med ren venv og tom datarot 208 bestått, 4 hoppet over og 3 utvalgt bort (denne porten, (i)). | Oppdater til tallene for koden i v1.0.0.

10. `README.md:145` | e | Det står «(AV-01–AV-30)», men LOG-0003 v1.17 har AV-01–AV-32. | Skriv AV-01–AV-32.

11. `paper.bib:245` og `:254` | f | `author = {Nicolaysen, Eirik Botten}` gjør «Nicolaysen» til etternavn. CITATION.cff:9 har `family-names: Botten Nicolaysen`, og ORCID-posten (OR-01, K122) har `"family-name":{"value":"Botten Nicolaysen"}`. | Skriv `author = {Botten Nicolaysen, Eirik}`.

12. `docs/adr/KLAR-ADR-0019_arkivklarering_inaseg-erstatning_v1.5_2026-10-28.md:24` (og :30) | d | Ingen KILDE-rad eller lagret kopi dekker disse påstandene: README-sitatet L12, «Male and female classification models are optimized for French language since they were trained using French speakers», og at «LICENSE, README, setup.py, PyPI-beskrivelsen eller release-notatene» ikke nevner vektene. Det finnes bare K119 (LICENSE) og K130–K134, ikke README eller setup.py ved v0.8.0. Funn 43 dekket de andre påstandene i :23–25, men ikke denne. | Hent README og setup.py ved v0.8.0 og registrer dem som IS-rader, eller fjern påstanden.

13. `docs/KLAR-EVAL-0010_arkivklarering_degradering-dev_v1.3_2026-10-28.md:5` | e | Det står «**Forrige versjon er beholdt uendret og er «før -nt».**» og «Forrige versjon: v1.1 (2026-10-26)», men v1.1-md-en ble fjernet fra treet i `bf48dfe`. | Skriv at v1.1 ligger i git-historikken.

14. `docs/adr/KLAR-ADR-0004_arkivklarering_segmentregel_v1.4_2026-10-28.md:14` | b | Lenken peker nå på `KLAR-EVAL-0001 … v1.4` (endret i `bf48dfe`), men er merket «v1.1» og sier at «NB-Whisper large verbatim skrev «.»». EVAL-0001 v1.4 (:6–28, :57) viser at rålaget med `-nt` skriver `<|nocaptions|>`. | Skriv «v1.1, før `-nt`; i v1.4 med `-nt` skriver begge lag `<|nocaptions|>`», eller lenk til versjonen tallene står i.

15. `docs/KLAR-PREREG-0001_arkivklarering_testdeler_v1.28_2026-10-28.md:230` | e | Raden for AV-25 i oppsummeringstabellen sier fortsatt «H4 kjøres med inaSpeechSegmenter» uten merknad. AV-19 (:224) er merket lukket av AV-27, og LOG-0003 v1.17:31 sier at H4 utgår. | Legg til «(H4 utgår i v1.0, AV-27)».

16. `CHANGELOG.md:3` og `:16` | e/b | :3 sier «Alt er utviklet 2026-10-26–27», men kodetaggen `testkjoring-v9` og rettingsrundene er fra 2026-10-28. :16 sier «Tale over musikk blir `speech`», mens ADR-0019 v1.5:13 og :45 og README:166 sier «`speech` eller `music`». | Skriv 2026-10-26–28 og «`speech` eller `music`».


## Status

| funn | rettet (commit) |
|---|---|
| 1 | 73f8f62 |
| 2 | 73f8f62 (v1.34 tilbake, sha256 = stempelet; v1.35 genereres i steg 6, oppdragets regel: GT bare i steg 6) |
| 3 | delvis (0af05ee); resten rettet i efce3f4, se «Mekanisk kontroll» |
| 4 | 0af05ee |
| 5 | 73f8f62 (EVAL-0013/-0014 og ARK-0008 v1.8 tilbake); 0af05ee (ARK-0008 v1.9) |
| 6 | delvis (0af05ee); resten rettet i efce3f4, se «Mekanisk kontroll» |
| 7 | 0af05ee |
| 8 | delvis (0af05ee); resten rettet i efce3f4, se «Mekanisk kontroll» |
| 9 | 0af05ee |
| 10 | 0af05ee |
| 11 | 0af05ee |
| 12 | 0af05ee |
| 13 | 0af05ee |
| 14 | 0af05ee |
| 15 | 0af05ee |
| 16 | 0af05ee |

## Kontroll etter retting

Én Opus-kontroll (kun lesing) av de 16 funnene på HEAD `5eb46cc`, 2026-10-28; rapporten ligger på Vault: `reproduksjon/port-v1.0/kontroll_runde3_2026-10-28_HEAD-5eb46cc.md` (sha256 `f0d9588ba87d25227336c558d3ea4f532a0c27e2471c2358ea78f54e1142f14a`). Resultat: 13 rettet (1, 2, 4, 5, 7, 9–16), 3 ikke fullt rettet (3: ARK-0008 v1.9:212; 6: umerkede pekere i ARK-0004 v1.6 :15, :26, :53, :63, :131, :135 og ARK-0005 v1.8 :12, :15, :80, :93, og påstandene på :3; 8: LOG-0003 v1.18:38, konsekvenscellen for AV-32 og tilleggsteksten uten skilletegn), og 4 nye feil fra rettingene. Taket for steg 3 (én port pluss én kontroll av restfunnene) er nådd; restfunnene er ikke rettet.

### Nye feil fra rettingene (på rørte linjer)

- A. Foreldede linjepekere etter versjonsøkningen i ARK-0008 v1.9: :124 «PREREG v1.28:198 (registrert tekst) og :245, :260»; :77 «LOG-0001 v1.48:66».
- B. KILDE v1.13: umerkede kortformpekere på rørte linjer: :242 og :293 («rettelsen står i v1.48:1487»), :380 («ARK-0009 v0.9:5»); påstanden i KILDE:3 holder derfor ikke.
- C. Ujevn merking i ARK-0008 v1.9: :7 («KLAR-PREREG-0001 v1.27», «KLAR-KILDE-0001 v1.11» umerket), :208 («KLAR-ARK-0009 v0.8», «KLAR-PREREG-0001 v1.27»), :125 og :213 («KLAR-LOG-0001 v1.46»).
- D. `paper.bib:1` sier «artikkelutkastet KLAR-ARK-0009 (v0.9, 2026-10-28)»; gjeldende er v0.10.

Ikke talt med (kosmetisk eller bevisst): merker inne i kodespenn; ARK-0008:34 README-relativ lenke (ordrett sitat); LOG-0001 v1.49:1 «ingen eldre linjer er endret» selv om linje 1 er endret; ARK-0004 v1.6:63 gjentar «trent på franske talere» (pekeren dekket av funn 6).

### Restfunn

1. Funn 3: ARK-0008 v1.9:212.
2. Funn 6: ARK-0004 v1.6 og ARK-0005 v1.8, med påstandene på :3.
3. Funn 8: LOG-0003 v1.18:38.
4. Nytt A.
5. Nytt B.
6. Nytt C.
7. Nytt D.

RESTFUNN: 7
KONTROLL: IKKE PASS

## Mekanisk kontroll (etter Eiriks beslutning 2026-10-28)

Eirik besluttet 2026-10-28 at de 7 restfunnene rettes (også versjonslinjene :3 i KLAR-ARK-0004 og -0005 og skilletegnet i cellen i KLAR-LOG-0003), og at kontrollen deretter gjøres mekanisk, uten Opus: `scripts/sjekk_pekere.py`, som også kjøres som test (`tests/test_sjekk_pekere.py`). Skriptet og testen ligger i kodetaggen `testkjoring-v10` (AV-33).

| restfunn | rettet (commit) |
|---|---|
| 1 (funn 3: ARK-0008:212) | efce3f4 |
| 2 (funn 6: ARK-0004 og ARK-0005, med :3) | efce3f4 |
| 3 (funn 8: LOG-0003:38, med skilletegnet; `git diff --stat testkjoring-v8 testkjoring-v9 -- arkivklarering kalibrering tests scripts` gir «5 files changed, 27 insertions(+), 9 deletions(-)») | efce3f4 |
| 4 (A: ARK-0008 :77, :124) | efce3f4 |
| 5 (B: KILDE :242, :293, :380, med :3) | efce3f4 |
| 6 (C: ARK-0008 :7, :125, :208, :213) | efce3f4 |
| 7 (D: paper.bib:1) | efce3f4 |

Skriptet fant i tillegg at KLAR-ARK-0008 v1.9:219 nevnte KLAR-ARK-0009 v0.5, som aldri ble committet (rettet i efce3f4). Resultat på `testkjoring-v10` og på commiten med AV-33: `python3 scripts/sjekk_pekere.py` gir «0 brudd i 95 filer». Unntakene i skriptet ut over oppdragets liste står i skriptets dokumentasjon og i KLAR-LOG-0001 v1.50 (AV-33).
