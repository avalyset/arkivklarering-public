# KLAR-LOG-0001: Avvik og hendelser

Fortløpende logg. Nyeste oppføring nederst. Versjonen i filnavnet økes når oppføringer legges til. v1.52 (bundle og DOI for den tilgangsstyrte historikken): oppføringen på linje 1599 er ny, og «DOI 10.5281/zenodo.23723450» i oppføringen for AV-34 er erstattet med DOI-en. v1.51 (AV-34, A3 endret): oppføringen på linje 1597 er ny. v1.50 (AV-33, restfunnene etter kontrollen): oppføringen på linje 1595 er ny. v1.49 (portfunn runde 3 rettet, KLAR-LOG-0005): oppføringen på linje 1593 er ny, og ingen eldre linjer er endret. v1.48 (portfunn runde 2 rettet): oppføringene fra linje 1578 er nye; i linje 1510, 1552, 1554, 1560 og 1564 er versjonshenvisninger, et klokkeslett og en telling rettet (KLAR-LOG-0004, funn 27–31 og 36; se oppføringen «Portfunn runde 2 rettet»); linje 1–1577 er ellers like v1.47 (bortsett fra denne linjen), og v1.47 er fjernet fra arbeidstreet (i git-historikken). v1.47 (portrapportene lagret): oppføringen på linje 1576 er ny. v1.46 (publiseringsporten ikke passert): oppføringene fra linje 1566 er nye; linje 1–1564 er ellers like v1.45 (bortsett fra denne linjen), og v1.45 er fjernet fra arbeidstreet (i git-historikken). v1.45 (rettinger før frys): oppføringene fra linje 1556 er nye; i linje 1524 er plassholderen for commiten til `testkjoring-v8` erstattet med SHA-en, og i linje 1526 viser stien til loggene nå til kopien på Vault i stedet for sesjonens scratchpad; linje 1–1554 er ellers like v1.44 (bortsett fra denne linjen), og v1.44 er fjernet fra arbeidstreet (i git-historikken). v1.44 (AV-30): oppføringene fra linje 1524 er nye; linje 1–1522 er like v1.43 bortsett fra denne linjen, og v1.43 er fjernet fra arbeidstreet (i git-historikken). v1.43 (AV-29): telefonnumrene på linje 62, 70 og 124–132 er erstattet med «[fiktivt nummer, byttet 2026-10-27, AV-29]»; ellers er linje 1–1512 like v1.42 (bortsett fra denne linjen), og v1.28–v1.42 er fjernet fra arbeidstreet (de ligger i git-historikken).

## 2026-10-26

**Testdel-sjekk (NB Samtale): ingen avvik.** `eval/dev/utvalg_dev_2026-10-26.json` har `"splitt": "validation"`.
De 60 segmentene er trukket fra validation-delen av `Sprakbanken/nb_samtale` (revisjon `1c7028101858b854d3d568761778d8f63bb7e33f`).
Av datafilene er bare `validation_metadata.jsonl`, `validation_bm_1.tar.gz` og `validation_nn_1.tar.gz` hentet; ingen `test_*`-fil er lastet ned. Utvalget må derfor ikke flyttes.
Som tiltak ble det lagt en hard sperre i `arkivklarering/evaldata.py`: test-delen kan ikke lastes uten `--prereg-id KLAR-PREREG-<NNNN>` og en eksisterende `docs/KLAR-PREREG-<NNNN>_*.md`.

**Navn: `KLAR-ARK-0001` fikk `v1.1`, ikke `v1.0`.** Instruksen sa at manglende versjon skulle bli `v1.0`. Dokumentet oppgir selv versjon 1.1 etter kildekontrollen samme dag, og filnavnet skal stemme med overskriften (KLAR-ARK-0002 § 4). `KLAR-REG-0001` ble `v1.0`.

**Pitch til museet er ikke verifisert.** `docs/gt_fast.md` har selv forbeholdet «ikke verifisert mot Sendt-mappen». Ingen sendt-mappe er lest.

**Modellfil for normalisert lag.** `nb-whisper-large.bin` lå i `/Volumes/Vault/norsk-tale/modeller/` (sha256 `0f2f66f2…`, samme som HF). Fila er norsk-tales og er ikke flyttet, fordi norsk-tale peker på stien; det er laget en kopi under `/Volumes/Vault/arkivklarering/modeller/` slik at arkivklarering ikke avhenger av norsk-tale (KLAR-ADR-0001).

**Ingen separat DEV-økt; commit-rekkefølge.** Utviklingsmålingen (DEV, `eval/dev/kjor_dev.py`) er en bakgrunnsjobb i samme økt som repodisiplinen; `ListAgents` viste ingen annen økt som arbeider i repoet, og `git log` hadde ved start bare `2237b0f`. Det fantes derfor ingen DEV-commit å vente på, bare en kjøring som måtte bli ferdig. Disiplinarbeidet (omdøping med `git mv`, ADR-er, konvensjon, skript) lå i samme arbeidstre og ble committet i en egen commit etter DEV-commiten. Kildeverifiseringen i `KLAR-ARK-0001` ble skrevet før omdøpingen og fulgte med `git mv` til det nye navnet; det fantes aldri en gammel fil ved siden av, så det var ingenting å flette.

**sha256 av modellfil under DEV-kjøringen.** Mens DEV-kjøringen pågikk ble den klonede normaliserte modellen (`cp -c`) hashet én gang (3 GB lesing) for å verifisere klonen. Det skjedde før instruksen om å vente med modell-hashing, og påvirker ikke WER-tallene; ytterligere hashing av modellfiler ventet til DEV var ferdig.

**Rålagets tidskoder (funn i røyktest).** Verbatim-modellen ga via whisper.cpp én cue med tidskode 0–30 s for hele vinduet, som havnet utenfor segmentet og gjorde `segments.json` tom for rålaget. Rettet i `transkriber.py` (cuer begrenses til segmentet) med test. Rålagets tidskoder er derfor på segmentnivå. DEV-målingen er upåvirket, siden den limer sammen cue-tekst uten å bruke tidskodene.

**`~/bin/bump-master.sh` endret.** Sporet `arkivklarering` er lagt til i `spor_config` (arkiv `Arkivklarering/arkiv`, prefiks `MASTER_ARKIVKLARERING`, datoformat `dotted`, repo `~/dev/arkivklarering`). Utover det er skriptet urørt (`diff` mot sikkerhetskopien viser bare sporblokken og feilmeldingen). `bump-master.sh check arkivklarering` ga OK på v0.1.

**Tidsstempling (OpenTimestamps).** `opentimestamps-client` 0.7.2 installert i prosjektets venv. `scripts/stempel.py` stempler docs/ og (med `--head`) HEAD, og `scripts/speil.sh` kjører den og `ots upgrade` ved hver kjøring. Stemplene og loggen `KLAR-LOG-0002` ligger i `docs/stempler/`. Bare sha256-sammendrag sendes til de offentlige kalendertjenestene.

**Kontroll av rålagets WER etter cue-fiksen: tallene er gyldige, ingen ny kjøring.** Spørsmålet var om rålagets `segments.json` var tom eller avkortet da WER ble regnet. WER-regningen i `eval/dev/kjor_dev.py` (linje 133–134) bruker aldri `segments.json` og ikke tidskodene: den limer sammen `c.tekst` fra cuene `transkriber.transkriber()` returnerer. Cue-fiksen (commit `0f9e95b`) endrer bare `start` og `stop` på cuene (`min(max(…))`); tekst og filtrering (`er_lydmerke`) er uendret. Tomheten gjaldt `segments.json` i røyktesten, der cuer ble tilordnet segmentet etter midtpunktet; DEV-kjøringen skriver ingen `segments.json`. Rålaget er heller ikke avkortet i DEV: 996 ord for ra/nn mot 775 for normalisert/nn og 1096 i fasiten. Seks tomme hypoteser for ra/nn (to for ra/matchet) kommer fra Whisper-utdata, ikke fra cue-håndteringen. Rålagets WER er dermed ikke merket ugyldig, og ingenting ble kjørt på nytt. Ingen Whisper-kjøring ble startet, så minnekontrollen mot det andre sporets minnevakt var ikke aktuell.

**Modellidentitet kontrollert (DEV-målingen): normalisert lag er large, ikke medium.** `modeller.lock.json` og HF-API-et (`/api/models/<repo>?blobs=true`) gir: rålag `nb-whisper-large-verbatim.ggml-model.bin`, 3 095 033 483 byte, sha256 `0227866e…ffc7d` = `NbAiLab/nb-whisper-large-verbatim`; normalisert lag `nb-whisper-large.ggml-model.bin`, 3 095 033 483 byte, sha256 `0f2f66f2…a33e76` = `NbAiLab/nb-whisper-large`. Medium har sha256 `f7314140…a73d` og 1 533 763 076 byte, og ingen av filene stemmer med den. DEV-resultatene (`KLAR-EVAL-0002`) bærer de samme sha256-verdiene. Medium ble bare brukt i v0-røyktesten. De gamle tallene beholdes uten merknaden «normalisert = medium», og normalisert lag ble ikke kjørt på nytt.

**Test av oppdiktet tekst: (a) var kjørt, (b) manglet rosa støy.** (a) rene `music`- og `other`-segmenter gjennom rørledningen: raskt test (Whisper blir aldri kalt) og tung test (musikk, stillhet og støy gjennom hele rørledningen) består. (b) direkte til Whisper var kjørt for stillhet, to nivåer hvit støy og musikk, men ikke rosa støy som instruksen ba om. Kjørt på nytt 2026-10-26 etter at det andre sporets minnevakt (`vakt.sh`) var borte og 74 % minne var ledig, med rosa støy lagt til: `KLAR-EVAL-0001` v1.1, ti kjøringer. Alle fem lydene ga «.» (rålag, tidskode 0–30 s) og `<|nocaptions|>` (normalisert lag). v1.0 av `KLAR-EVAL-0001` er erstattet (ligger i git-historikken og er tidsstemplet).

**ADR-0004 v1.1 og KLAR-ARK-0001 v1.2: begrunnelsen skrevet om.** v1.0 av ADR-0004 og v1.1 av ARK-0001 begrunnet regelen med oppdiktet tekst og stillhet/støy. Koenecke m.fl. sier at oppdiktingen er hyppigere ved pauser i tale (ikke-vokal tid), og egen måling viste ingen prosa på stillhet, støy eller musikk. Regelen er uendret; begrunnelsen hviler nå på (1) at det ikke er tale å transkribere og at utdata («.», `<|nocaptions|>`) kan forveksles med innhold, og er uttrykkelig ikke påvist hallusinasjon på slik lyd. Risikoen i pauser inne i tale er ført som gjenstående konsekvens.

**Alt tungt flyttet til Vault.** `df -h /`: før 460 Gi størrelse, 18 Gi ledig (42 % brukt); etter 19 Gi ledig (41 %). `df -h /Volumes/Vault`: før 55 Gi ledig, etter 53 Gi. Nytt venv `/Volumes/Vault/arkivklarering/venv` (1,2 GB; installert fra `pip freeze` av det gamle pluss presidio-analyzer, spaCy, `nb_core_news_md`, pyarrow); `~/dev/arkivklarering/.venv` er en symlink dit. `pytest -q` var grønt (19 passerte, den tunge testen bestått offline) før det gamle venv-et (956 MB) ble slettet. Cacher under `/Volumes/Vault/arkivklarering/cache/{hf,pip,torch,spacy,uv}` og `tmp/`; `scripts/miljo.sh` kildes før kjøring (stopper hvis Vault ikke er montert) og de samme linjene står i `.env` (ikke i git). `uv` får Vault-cache via `XDG_CACHE_HOME`. `cache/spacy/` er opprettet som bedt, men ubrukt: spaCy-modellen ligger i venv-et.
- **Flyttet** (bare det som tilhører arkivklarering): `models--ina-foss--ssl-vad-music2vec` og `models--ina-foss--ssl-music-detection-music2vec` med lås-mapper, og de tre vektfilene de peker på i HFs delte blob-lager (`hub/blobs/ea/eaf6e837…`, `24/24f8ee97…`, `98/982d9a8a…`, til sammen 62 MB). Hver ble byte-sammenlignet med kopien på Vault (`cmp`) og verifisert mot HF-navnets sha256 før originalen ble slettet; ingen andre symlinker i `~/.cache/huggingface/hub` pekte på dem. Offline-test av inaVAMOS fra Vault-cachen bestått. `nb_samtale` lå aldri i `~/.cache` (lastet rett til Vault). Torch hub finnes ikke.
- **Ikke flyttet, ikke rørt** (eier ikke arkivklarering eller usikker): `~/.cache/uv` (15 GB, delt av alle uv-prosjekter), `~/.cache/huggingface/hub` med `models--NbAiLab--nb-bert-base` (682 MB, ukjent eier; ikke samme repo som `nb-bert-base-ner`) og de andre modell- og datasett-mappene, `~/.cache/huggingface/datasets`, og `chroma`, `claude`, `codex-runtimes`, `conda`, `gh`, `mteb`, `pkg`, `pre-commit`, `puppeteer`, `stifinner-turruter`.

**Avvik: dokumentnummeret.** Instruksen ba om `KLAR-EVAL-0002_…personvern-dev…`. `KLAR-EVAL-0002` til `0004` er allerede DEV-målingen på NB Samtale, og nummer gjenbrukes aldri (KLAR-ARK-0002 § 1). Personvernmålingen er derfor `KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_2026-10-26`.

**Personvern v0 og NorNE.** `personvern.py` er implementert (KLAR-ADR-0008 v1.1, KLAR-ADR-0012). NorNE hentet som `NbAiLab/norne` (config `bokmaal` og `nynorsk`, revisjon `1ca12d43…`), fordi `ltg/norne` har én samlet config uten oppdeling i bokmål og nynorsk. Lisensen står ordrett i `KLAR-EVAL-0005`; åpen for denne bruken (annotasjonene er CC0, tredjepartstekstene ikke gjenpubliseres, og ingen setninger lagres). Bare `validation`; `test` er sperret på samme måte som for NB Samtale.

**Funn: rålaget har klart svakere navnegjenkjenning.** På NorNE validation faller hele motorens recall for personer fra 0,997 til 0,715 (bokmål) og fra 0,954 til 0,599 (nynorsk) når teksten gjøres om til små bokstaver uten tegnsetting, slik rålaget skrives. KLAR-ADR-0005 v1.0 og KLAR-ARK-0001 v1.2 sa at rålaget var grunnlaget for personvernflagging. Det er rettet (ADR-0005 v1.1, ARK-0001 v1.3): flagg lages på begge lag, det normaliserte laget bærer flaggene for navn og steder, og rålaget er grunnlaget for revisjon.

**Røyktest av flagg.** På `rokytest.wav` (ingen navn i teksten) ga normalisert lag ett falskt flagg («Heim» som person, spaCy, score 0,6) og rålaget ingen. På `rokytest_personvern.wav` (TTS, bokmålsstemme som leser nynorsk tekst med navn, fødselsår, sykdom, parti og telefonnummer) ble navn, sted, fødselsår, helse, organisasjon, politikk og telefon flagget i normalisert lag; rålaget fikk alle unntatt navnet «Kari Nordmann» (skrevet «karin», score 0,497). TTS-stemmen leste «1972» som «1917»; det er lydfilens feil, ikke flaggingens.

**Union av personvernflagg (v0.2).** `personvern.slaa_sammen_lag` slår flagg fra rålaget og det normaliserte laget sammen: samme kategori og overlappende tid blir ett flagg (kildelag «ra», «normalisert» eller «begge», høyeste score, begge lagenes utdrag og tidsgrenser i `per_lag`); flagg som bare finnes i ett lag beholdes, og ingen terskel filtrerer. `segments.json` har `personvern_union` per segment ved siden av de rå flaggene per lag. **Begrensning:** rålaget gir ofte én cue som dekker hele segmentet, så tid alene kan ikke skille to ulike treff i samme kategori. Paringen er derfor én-til-én og grådig etter likhet mellom utdragene, uten likhetsterskel; to ulike entiteter i samme kategori kan dermed bli pariert hvis de er de eneste i hvert lag. Ingen informasjon går tapt (begge utdrag ligger i flagget), men antall «begge»-flagg kan overvurdere samsvar. Røykfila `rokytest_personvern.wav` ga 8 union-flagg: 6 «begge» og 2 bare i normalisert lag («Titto» som person og «Volda» som sted). Whisper ble kjørt på nytt bare for røykfila (vakten var ikke aktiv, 74 % minne ledig).

**Flaggoverlevelse (DEV, `KLAR-EVAL-0006`): for få referanseflagg.** Whisper ble ikke kjørt på nytt; hypotesene kom fra DEV-kjøringen. Referanseflagg på de 60 segmentene: person 17, sted 14, organisasjon 3, og null for dato, fødselsår, telefon, fødselsnummer, e-post, helse, økonomi, konflikt, religion og politikk. Overlevelse er derfor målt bare for person og sted (union 14/17 og 14/14, med brede intervaller); organisasjon (n = 3) er ikke tolkbar, og ti kategorier er ikke målt. Datasettkortet sier ikke om navn er anonymisert.

**Nummerregister.** `KLAR-ARK-0003` registrerer alle brukte KLAR-numre per type og hvem som bruker dem, med `KLAR-PREREG-0001` som reservert. `scripts/ground_truth.py` leser registeret mot disken og varsler (øverst i GT under «VARSLER») ved hull, dobbel bruk (to slugger på samme nummer), nummer på disk som ikke står i registeret, registrerte nummer som mangler på disk (unntatt reserverte), reservert-men-i-bruk og slug som avviker. Funksjonen har enhetstester. Ved første kjøring: ingen varsler, 25 nøkler på disk og 26 i registeret (PREREG-0001 reservert).

**Diagnose av tapt diskplass (26.10, ca. 13:30).** Ledig plass på den interne disken hadde falt med ca. 13 GiB siden morgenen (30 til 17 GiB på data-volumet; brukeren oppga 30 GB). Ingen arkivklarering-prosess skrev til den interne disken, `~/.cache/huggingface` var uendret siden 09:21, `/tmp` var 0 B. Plassen gikk til Claude-appens VM-bilde (14 GB, `rootfs.img` endret 13:22), swap (7 swapfiler, 5,9 av 7,2 GB brukt, tre opprettet samme dag) og en voksende ollama-logg (941 MB). Ingenting ble slettet eller flyttet. Dette ble årsak til KLAR-ADR-0015 (skrevet i ettertid) og til miljø- og ressursvaktene. Vi kan ikke utelukke at Whisper-kjøringene bidro indirekte via swap.

**Miljøvakt innført.** `scripts/miljo.sh` og `arkivklarering/miljo.py` avbryter hvis `HF_HOME`, `HF_DATASETS_CACHE`, `TMPDIR` eller `XDG_CACHE_HOME` peker utenfor Vault; alle Python-skript, `speil.sh`, `tests/conftest.py` og riggwrapperen kaller vakten først. Ressursvakt for Whisper: minst 8 GiB ledig intern disk, høyst 6,5 GB swap, minst 6 GB ledig minne og ikke det andre sporets minnevakt. Vaktene slo ikke til under NPSC- og syntetisk kjøring.

**DTW-ordtidsstempler i stedet for `-ml 1 -sow`.** `-ml 1 -sow` klumpet de siste ordene i segmentets slutt for verbatim-modellen. `--dtw large.v3` (med `-nfa`) ga monoton tid; NB-Whisper large har whisper-large-v3-arkitektur (128 mel-bånd, 32 dekoderlag). To rålagssegmenter (3,5 og 3,6 s) i NB Samtale krasjet whisper-cli med DTW (SIGABRT uten melding); de ble kjørt uten DTW. Gruppekjøring (modellen lastes én gang) er ikke bitidentisk med én prosess per fil: bare 35 av 60 rålagstekster og 45 av 60 normaliserte tekster ble identiske med DEV-hypotesene (se KLAR-EVAL-0006 v1.1).

**NPSC (KLAR-EVAL-0007): stoppregel regnet uten å se utfall.** Utvalget ble 936 segmenter (1,98 t). Regelen «minste prefiks med minst 150 personflagg og 100 stedsflagg i referansen» ble regnet ut på referansen alene (14:25:47, før noe NPSC-rørledningsresultat var lest): **934 av 936**. Whisper var da kommet til 400 segmenter; kjøringen ble stoppet og startet på nytt og kjørte bare de 534 som gjensto. De to siste segmentene er ikke kjørt. Kategorier utenom person og sted er ikke målt (instruksen), selv om referansemotoren fant noen flagg i NPSC (antall står i EVAL-0007). Organisasjon er ikke med.

**Syntetisk kalibrering (KLAR-EVAL-0008) fant to feil i flaggene.** (1) Telefon- og fødselsnummermønstrene krevde ett bestemt mellomromsmønster, men Whisper skriver «[fiktivt nummer, byttet 2026-10-27, AV-29]» (fire sifferpar skilt med komma) og «150 575 45 615»: flagg-treff 4 av 14 og 4 av 12 selv med riktig tekst. (2) Nøkkelordene hadde ingen bøyningsformer. Begge er rettet i `personvern.py` (sifre med skilletegn og validering; bøyningsendelser på nøkkelord på fire bokstaver eller mer), med tester, og tallene før og etter står i EVAL-0008. Rettelsen er gjort på syntetiske data, ikke på testdata. Det finnes ingen nynorskstemme på maskinen (bare Nora, nb_NO), og en runde gjennom høyttaler og mikrofon ble ikke gjort (riggen krever en menneskelig leser i nettleseren).

**Testsperren strammet inn.** Et utkast til preregistrering åpner ikke testdelene: `docs/KLAR-PREREG-<NNNN>_*.md` må ha statuslinjen `Status: registrert <OSF-URL>` (`arkivklarering/evaldata.py`, test i `tests/test_evaldata.py`). `KLAR-PREREG-0001` er skrevet som utkast og er ikke sendt inn.

**Eksportformater (v0.4): hva som ble hentet og hva som ikke ble det.** OHMS-skjemaet (`ohms.xsd`, versjon 5.4) ble hentet fra Wayback Machines kopi av den offisielle adressen, fordi `avpreserve.com` svarer med en Cloudflare-bot-sjekk (ikke omgått). OHMS' CSV-importmal ligger bare på Dropbox, som serverte en HTML-side til en uautentisert henting, og er derfor ikke hentet og ikke brukt. De fem offisielle eksempelfilene (`ohms_xml_samples.zip`, versjon 4, uten navnerom) validerer ikke mot XSD-en (navnerom og `date`-element med tekst); vår XML valideres mot XSD-en, og `sync` (transkripsjonssynkronisering) genereres ikke. IIIF Cookbook-oppskrift 0231 er en metaoppskrift; manifestet følger alternativ 2 og 3 med `supplementing`-annotasjoner og mønsteret i 0219, validert med `iiif-prezi3` (som også godtar den offisielle 0219-manifesten). MMIF 1.2.0 via `mmif-python` 1.5.4 (`TimeFrame.label`, ikke det utfasede `frameType`). WebVTT har bare en parserkontroll (`webvtt-py`).

**Vendor-kopi fra norsk-tale** (KLAR-ADR-0014): `norm.py` og `score.py` uendret, commit `bcfef63d`, sha256 i `ORIGIN.txt`, kontroll i `tests/test_vendor.py`. Riggen (`rigg.py`) kopieres ikke; `scripts/rigg_manus.py` bruker den fra norsk-tales katalog med arkivklarerings manus og opptaksmappe på Vault (156 setninger, 12 med dialektutvalg). Ingenting er tatt opp; kommandoen står i rapporten.

**Katalogmodell (KLAR-ADR-0013) og røyktest fra ende til ende.** Valget av `borealis-open-4b` bygger på fire sendinger med menneskelig NPSC-tekst, ikke på Whisper-utdata; `nb-llama-3.1-8b-instruct` feilet reproduserbart med HTTP 500 etter 18 kall og er ikke vurdert på norsk kvalitet; ingen språkkvalitet er vurdert av et menneske. Røyktesten (`rokytest_personvern.wav`, 40 s, hele CLI-et med Whisper og ollama, 83 s) ga alle seks filer, og alle fem eksportvalidatorene ga ingen feil. Den viste at emneordene kunne inneholde et telefonnummer («[fiktivt nummer, byttet 2026-10-27, AV-29]»): `katalog.rens_post` forkaster nå emneord som ligner et nummer (test lagt til). Sammendraget gjengir fortsatt det transkripsjonen sier (også et telefonnummer); utkastet er merket ikke klarert og er ikke en klarering.

**Rettelser før registrering av KLAR-PREREG-0001 (v1.1).** (1) *Manus delt.* `KLAR-MANUS-0001` ble brukt til å justere mønstrene (telefon, fødselsnummer, nøkkelord) og til å sette H4-tersklene; det er derfor ikke egnet som test. Det er omdøpt til `justeringsmanus` (v1.1, status i fila: brukt til mønsterjustering, ikke til testing; `scripts/lag_manus.py` gir byte-lik fil). `KLAR-MANUS-0002` (`testmanus`, 6 nye setninger per klasse og målform, andre formuleringer, navn, tall og steder; `scripts/lag_manus2.py`) er skrevet uten å kjøre noen setning gjennom rørledningen, mønstrene eller ordlistene (ordlistene ble ikke åpnet under skrivingen, men er skrevet av samme forfatter). Formatkontrollen (`tests/test_manus.py`) er ren strengsjekk av kolonner, antall, at målelementene står i setningen, at fødselsnumrene er ugyldige, og at ingen setning, person, sted, telefon, fødselsnummer, e-post eller dato er felles med justeringsmanuset. `kalibrering.les_manus` avviser 0002 uten registrert preregistrering (samme sperre som testdelene). Sha256 `b8dee027…` står i preregistreringen og kontrolleres av en test. `KLAR-EVAL-0008` fikk v1.1 (bare navnet på manusfila rettet, tallene uendret). (2) *Preregistreringen omdøpt* fra `_pilot_` til `_testdeler_` (v1.1); museumspiloten er `KLAR-PREREG-0002` (reservert). Primærutfall: H1a (WER, rålag, målform matchet mot fasiten, ra/matchet) og H2 (union per kategori); alt annet er sekundært (H1b, H1d, H1e, H3, H4). «Rå < normalisert» (WER og overlevelse) og «recall faller ≥ 0,15 på små bokstaver» er flyttet fra hypotesene til kontrollsjekkene K1–K3. H1-primær ble endret fra «`-l nn` per lag» til «rålag, matchet målform» etter Eiriks retting: fasiten er ordrett og har målformen til hvert segment, og normalisert lag og `-l nn` mot bokmålsfasit måler normalisering og rettskrivning, ikke gjenkjenning. Tallene i tersklene er uendret. H2 bærer ordrett «NB-Whisper er trent på NPSC; overlevelsestallene er optimistiske for talegjenkjenningen». H4-tersklene er beholdt, med grunnlaget «satt fra syntetisk kjøring på justeringsmanuset». (3) *Ikke gjort:* skriptet som kjører menneskeopptak av testmanuset gjennom rørledningen finnes ikke ennå (`kjor_syntetisk.py` leser justeringsmanuset); det må skrives og testes på justeringsmanuset og fryses før innsending. Ingen Whisper-kjøring og ingen endring i `personvern.py` ble gjort i denne runden. (4) *README:* OHMS-linjen sier nå hva som er sjekket. `docs/gt_fast.md` (håndført) er rettet til å skille PREREG-0001 (testdeler) fra PREREG-0002 (museumspilot).

**KLAR-MANUS-0002 rettet til v1.1 før låsing (2026-10-26).** Manuset er ikke kjørt gjennom rørledningen, mønstrene eller ordlistene (Whisper ble bare kjørt på justeringsmanuset, se tørrtesten under). Ny sha256: `d0684b0a2f6c21309c7087a5a5915921a378023320f6a6bd1b85232809b78599` (v1.0 hadde `b8dee027af75cf27f20cb2480d2893f1693f46a060d7c1230f863db717d9dafc`); PREREG-0001 er oppdatert til v1.2 med den nye verdien, og testen som låser hashen leser den derfra. Nummerregisteret og `KLAR-ARK-0005` (datablad) peker på v1.1. Rettede rader (før/etter, målelementer der de er endret):

ste04nb
    før:  Elva Sjoa renner gjennom Heidal og ned mot Kvam.
    etter: Elva Sjoa renner gjennom Heidal før den møter Lågen.
    målelementer før:  [('sted', 'Sjoa'), ('sted', 'Heidal'), ('sted', 'Kvam')]
    målelementer etter: [('sted', 'Sjoa'), ('sted', 'Heidal'), ('sted', 'Lågen')]
ste04nn
    før:  Elva Sjoa renn gjennom Heidal og ned mot Kvam.
    etter: Elva Sjoa renn gjennom Heidal før ho møter Lågen.
    målelementer før:  [('sted', 'Sjoa'), ('sted', 'Heidal'), ('sted', 'Kvam')]
    målelementer etter: [('sted', 'Sjoa'), ('sted', 'Heidal'), ('sted', 'Lågen')]
fod06nn
    før:  Han er fødd i 1955 og var yngst av sju syskin.
    etter: Han er fødd i 1955 og var yngst av sju sysken.
hel01nb
    før:  Bestemor fikk demens og flyttet på sykehjem.
    etter: Bestemor fikk demens og flyttet til sykehjem.
hel01nn
    før:  Bestemor fekk demens og flytte på sjukeheim.
    etter: Bestemor fekk demens og flytta til sjukeheim.
kon01nn
    før:  Striden om grensegjerdet havna hos lensmannen.
    etter: Striden om grensegjerdet hamna hos lensmannen.
kon03nb
    før:  Søsknene havnet i et bittert arvekrangel.
    etter: Søsknene havnet i en bitter arvekrangel.
kon03nn
    før:  Syskena havna i eit bittert arvekrangel.
    etter: Syskena hamna i ein bitter arvekrangel.
rel03nb
    før:  Familien var buddhister og reiste til templet hvert år.
    etter: Familien var buddhister og reiste til tempelet hvert år.
pol01nb
    før:  Han satt i bystyret for Høyre i to perioder.
    etter: Han satt i kommunestyret for Høyre i to perioder.
pol01nn
    før:  Han sat i bystyret for Høgre i to periodar.
    etter: Han sat i kommunestyret for Høgre i to periodar.
kom01nb
    før:  Reidun Hovde, født i 1936 på Kvam, fikk revmatisme som ung.
    etter: Reidun Hovdesæter, født i 1936 på Kvam, fikk revmatisme som ung.
    målelementer før:  [('person', 'Reidun Hovde'), ('fødselsår', '1936'), ('sted', 'Kvam'), ('helse', 'revmatisme')]
    målelementer etter: [('person', 'Reidun Hovdesæter'), ('fødselsår', '1936'), ('sted', 'Kvam'), ('helse', 'revmatisme')]
kom01nn
    før:  Reidun Hovde, fødd i 1936 på Kvam, fekk revmatisme som ung.
    etter: Reidun Hovdesæter, fødd i 1936 på Kvam, fekk revmatisme som ung.
    målelementer før:  [('person', 'Reidun Hovde'), ('fødselsår', '1936'), ('sted', 'Kvam'), ('helse', 'revmatisme')]
    målelementer etter: [('person', 'Reidun Hovdesæter'), ('fødselsår', '1936'), ('sted', 'Kvam'), ('helse', 'revmatisme')]
kom02nb
    før:  Sverre Bakken ringte [fiktivt nummer, byttet 2026-10-27, AV-29] den 21. mars 1988 om arvestriden.
    etter: Sverre Bakkelien ringte [fiktivt nummer, byttet 2026-10-27, AV-29] den 21. mars 1988 om arvestriden.
    målelementer før:  [('person', 'Sverre Bakken'), ('telefon', '[fiktivt nummer, byttet 2026-10-27, AV-29]'), ('dato', '21. mars 1988'), ('konflikt', 'arvestriden/arvestrid')]
    målelementer etter: [('person', 'Sverre Bakkelien'), ('telefon', '[fiktivt nummer, byttet 2026-10-27, AV-29]'), ('dato', '21. mars 1988'), ('konflikt', 'arvestriden/arvestrid')]
kom02nn
    før:  Sverre Bakken ringde [fiktivt nummer, byttet 2026-10-27, AV-29] den 21. mars 1988 om arvestriden.
    etter: Sverre Bakkelien ringde [fiktivt nummer, byttet 2026-10-27, AV-29] den 21. mars 1988 om arvestriden.
    målelementer før:  [('person', 'Sverre Bakken'), ('telefon', '[fiktivt nummer, byttet 2026-10-27, AV-29]'), ('dato', '21. mars 1988'), ('konflikt', 'arvestriden/arvestrid')]
    målelementer etter: [('person', 'Sverre Bakkelien'), ('telefon', '[fiktivt nummer, byttet 2026-10-27, AV-29]'), ('dato', '21. mars 1988'), ('konflikt', 'arvestriden/arvestrid')]
kom03nb
    før:  Torunn Skjelbred fra Garmo er kveker og stemmer Venstre.
    etter: Torunn Skjelbrekke fra Garmo er kveker og stemmer Venstre.
    målelementer før:  [('person', 'Torunn Skjelbred'), ('sted', 'Garmo'), ('religion', 'kveker'), ('politikk', 'Venstre')]
    målelementer etter: [('person', 'Torunn Skjelbrekke'), ('sted', 'Garmo'), ('religion', 'kveker'), ('politikk', 'Venstre')]
kom03nn
    før:  Torunn Skjelbred frå Garmo er kvekar og stemmer Venstre.
    etter: Torunn Skjelbrekke frå Garmo er kvekar og stemmer Venstre.
    målelementer før:  [('person', 'Torunn Skjelbred'), ('sted', 'Garmo'), ('religion', 'kvekar/kveker'), ('politikk', 'Venstre')]
    målelementer etter: [('person', 'Torunn Skjelbrekke'), ('sted', 'Garmo'), ('religion', 'kvekar/kveker'), ('politikk', 'Venstre')]
kom04nb
    før:  Arne Odden, født i 1958, bor på Nedre Frya og fikk dagpenger.
    etter: Arne Oddvollen, født i 1958, bor på Nedre Frya og fikk dagpenger.
    målelementer før:  [('person', 'Arne Odden'), ('fødselsår', '1958'), ('sted', 'Nedre Frya'), ('økonomi', 'dagpenger')]
    målelementer etter: [('person', 'Arne Oddvollen'), ('fødselsår', '1958'), ('sted', 'Nedre Frya'), ('økonomi', 'dagpenger')]
kom04nn
    før:  Arne Odden, fødd i 1958, bur på Nedre Frya og fekk dagpengar.
    etter: Arne Oddvollen, fødd i 1958, bur på Nedre Frya og fekk dagpengar.
    målelementer før:  [('person', 'Arne Odden'), ('fødselsår', '1958'), ('sted', 'Nedre Frya'), ('økonomi', 'dagpengar/dagpenger')]
    målelementer etter: [('person', 'Arne Oddvollen'), ('fødselsår', '1958'), ('sted', 'Nedre Frya'), ('økonomi', 'dagpengar/dagpenger')]
kom05nb
    før:  Liv Heggeli på Bjorli ble anmeldt for trusler 14. juli 1993.
    etter: Liv Brekkeslåen på Bjorli ble anmeldt for trusler 14. juli 1993.
    målelementer før:  [('person', 'Liv Heggeli'), ('sted', 'Bjorli'), ('konflikt', 'anmeldt/anmeldte'), ('konflikt', 'trusler'), ('dato', '14. juli 1993')]
    målelementer etter: [('person', 'Liv Brekkeslåen'), ('sted', 'Bjorli'), ('konflikt', 'anmeldt/anmeldte'), ('konflikt', 'trusler'), ('dato', '14. juli 1993')]
kom05nn
    før:  Liv Heggeli på Bjorli vart melde for truslar 14. juli 1993.
    etter: Liv Brekkeslåen på Bjorli vart meld for truslar 14. juli 1993.
    målelementer før:  [('person', 'Liv Heggeli'), ('sted', 'Bjorli'), ('konflikt', 'melde/anmeldt'), ('konflikt', 'truslar/trusler'), ('dato', '14. juli 1993')]
    målelementer etter: [('person', 'Liv Brekkeslåen'), ('sted', 'Bjorli'), ('konflikt', 'meld/anmeldt'), ('konflikt', 'truslar/trusler'), ('dato', '14. juli 1993')]
kom06nb
    før:  Magnus Rudi, født 1949, er buddhist og bor på Hafjell.
    etter: Magnus Rudisæter, født 1949, er buddhist og bor på Hafjell.
    målelementer før:  [('person', 'Magnus Rudi'), ('fødselsår', '1949'), ('religion', 'buddhist'), ('sted', 'Hafjell')]
    målelementer etter: [('person', 'Magnus Rudisæter'), ('fødselsår', '1949'), ('religion', 'buddhist'), ('sted', 'Hafjell')]
kom06nn
    før:  Magnus Rudi, fødd 1949, er buddhist og bur på Hafjell.
    etter: Magnus Rudisæter, fødd 1949, er buddhist og bur på Hafjell.
    målelementer før:  [('person', 'Magnus Rudi'), ('fødselsår', '1949'), ('religion', 'buddhist'), ('sted', 'Hafjell')]
    målelementer etter: [('person', 'Magnus Rudisæter'), ('fødselsår', '1949'), ('religion', 'buddhist'), ('sted', 'Hafjell')]
23 rader endret

Rettelsene er av tre slag: (1) språkform, kontrollert mot ordbøkene (se under); (2) navn: alle seks personer som står i samme setning som helse, økonomi, konflikt, religion eller politikk (kom01–kom06) fikk et etternavn uten treff i SSBs navnesøk; (3) innhold (ste04, pol01, hel01, kom05nn). `epo05nn` («så svarer vi») er uendret etter Eiriks instruks: Nynorskordboka viser «svarer» som presens i `svare` (artikkel 75805, paradigme 2), så formen er gyldig.

**Ordbokkontroll (Nynorskordboka for nn-setninger, Bokmålsordboka for nb-setninger).** API-dokumentasjonen (<https://ord.uib.no/ord_2_API.html>) ble lest først. Oppslag: `GET https://ord.uib.no/api/articles?w=<ord>&dict=<nn|bm>&scope=ei` (`e` oppslagsord og `i` bøyde former; søket skiller ikke store og små bokstaver); artikler lest via `/<dict>/article/<id>.json`. Hoppet over: ord i målelementene av typen person og sted (egennavn), tall og e-postadresser. `scripts/ordbokkontroll.py` slo opp 593 unike ord og lagret alle oppslag i `eval/dev/ordbokkontroll_manus0002_2026-10-26.json` (manusets sha256 ligger i fila). Funn i første kjøring der ordboka viste en annen form og som ble rettet: nb «templet» → «tempelet» (`tempel` har bestemt form «tempelet», ikke «templet»), nn «havna» → «hamna» (Nynorskordboka har verbet `hamne`; `havne` finnes ikke i nn), og Eiriks egne rettelser: bm `krangel` er bare hankjønn (`m.`), så «et bittert arvekrangel» ble «en bitter arvekrangel» (nn `krangel` er `m.`: «ein bitter»); nn «sysken» (n1, hovedform; «syskin» finnes ikke i Nynorskordboka; bestemt flertall «syskena»). «flytta», «meld» og «sysken» ga treff. Ord uten treff etter rettelsene (18 oppslag): nb «arkivspørsmål»; nb «arvekrangel»; nb «arvestriden»; nb «bygdekirken»; nb «grensegjerdet»; nb «mobilnummeret»; nb «pasientens»; nb «ryggskaden»; nb «vaktsentralen»; nn «arkivspørsmål»; nn «arvekrangel»; nn «arvestriden»; nn «betalingsanmerkinga»; nn «bygdekyrkja»; nn «grensegjerdet»; nn «mobilnummeret»; nn «ryggskaden»; nn «vaktsentralen». Alle unntatt «pasientens» (genitiv, lemma `pasient` finnes) er sammensatte ord uten egen oppføring; ordboka viste ingen alternativ form og ingenting ble rettet. Merk: Nynorskordboka har ikke `anmerking`/`anmerkning` (bokmål har `anmerkning`), så «betalingsanmerkinga» i oko04nn bygger på et ledd ordboka ikke kjenner; formen er beholdt fordi ordboka ikke viser noen annen, men setningen er et kandidatpunkt for Eiriks faktasjekk.

**Navnekontroll (SSB).** `scripts/navnesjekk.py` kaller navnesøket som ssb.no/befolkning/navn/statistikk/navn selv bruker (`https://www.ssb.no/_/service/mimir/nameSearch?name=<navn>`). SSB oppgir at «alle navn med mer enn tre navnebærere gir treff i navnesøket», så **«ingen treff» betyr 0 til 3 bærere, ikke sikkert 0**; null bærere kan SSB ikke bevise. Gamle etternavn og treff (familienavn / mellomnavn+familienavn): Hovde 1380 / 596, Bakken 7481 / 2243, Skjelbred 605 / 223, Odden 1066 / 398, Heggeli 101 / 45, Rudi 570 / 229 (pluss fornavn). Nye etternavn: Hovdesæter, Bakkelien, Skjelbrekke, Oddvollen, Brekkeslåen, Rudisæter, alle 0 treff. Resultat for alle 12 personforekomster (6 nb + 6 nn) i setninger med sensitiv kategori: 0 med treff (`eval/dev/navnesjekk_manus0002_2026-10-26.json`). Fornavn er ikke kontrollert. Personene i øvrige setninger beholder navnene.

**Telefonnumre i manusene.** Numrene i KLAR-MANUS-0001 og -0002 er fiktive, men har norsk format og er ikke sjekket mot virkelige abonnenter. Manusene publiseres ikke (repoet er privat) før numrene er sjekket. Ingen endring gjort nå.

**H4-skriptet `kalibrering/kjor_h4.py` og tørrtest.** Leser opptak fra riggen (`<rot>/<runde>/opptak/<id>.wav`), kjører rålag, normalisert lag og union, scorer målelementene per kategori og målform med vendor-`score.py` (via `kalibrering.score_flagg`), leser tersklene fra tabellen i PREREG-0001 og skriver `KLAR-EVAL-0009` med bestått/ikke bestått. Mot testmanuset kreves registrert preregistrering og at manusets sha256 står i den; uten dem avvises kjøringen. Oppsettet er språk etter målform («matchet», grunnlaget for tersklene); `--oppsett nn` er sekundært. **Tørrtest på justeringsmanus** (`--torrtest`, de 156 SYNTETISKE TTS-filene, ny Whisper-kjøring med batcher på 40, 819 s, cache `h4_torrtest_matchet.jsonl`): union flagg-treff per kategori er identisk med `KLAR-EVAL-0008` (matchet): person 18/26, sted 33/40, dato 14/14, fødselsår 16/18, telefon 12/14, fødselsnummer 10/12, e-post 0/12, helse 26/26, økonomi 19/22, konflikt 22/26, religion 12/16, politikk 16/18; alle kategorier «bestått» mot tersklene (dette er **ikke en H4-måling**, siden justeringsmanuset er det tersklene er satt fra). Resultat: `eval/dev/h4_torrtest_justeringsmanus_2026-10-26.{json,md}`.

**Artefakt-revisjon fra disk (oppgave A).** KLAR-dokumentene på disk stemmer med nummerregisteret (v1.7): ingen nummer på disk uten rad, ingen hull. KLAR-EVAL-0003 er `dev-utvalg`: utvalget av de 60 NB Samtale validation-segmentene (JSON i `eval/dev/`, seed 20261026, 12 per dialektområde). KLAR-EVAL-0004 er `dev-lisens-nbsamtale`: lisensvurderingen for NB Samtale (Markdown i `eval/dev/`, ført for hånd). Det som manglet og nå er laget: én kommando som kjører EVAL-ene fra rådata (`scripts/reproduser.sh`), låst miljø med hasher (`requirements.lock` og `requirements-degradering.lock`, fra Vault-venvet med `uv pip compile --generate-hashes`; spaCy-modellen `nb_core_news_md` er installert fra URL og ikke hash-låst), modellkort (`KLAR-ARK-0004`, Mitchell mfl. 2019), datablad for MANUS-0001 og -0002 (`KLAR-ARK-0005`, Gebru mfl. 2021) og `CHANGELOG.md`. `reproduser.sh` er testet slik: syntaks, `--tor`, og steg 4 (EVAL-0004) ende til ende i en egen worktree; steg 1–8 er **ikke kjørt på nytt** (timer med Whisper); H4-skriptet er kjørt ende til ende i tørrtesten. Det finnes ingen kjøring som gir sha256-lik gjengivelse: Whisper-batcher er ikke bitidentiske.

**Talerinndeling (oppgave B) stoppet: modellen er gated.** WhisperX bruker som standard `pyannote/speaker-diarization-community-1` (lest i `whisperx/diarize.py` på GitHub main, 2026-10-26). Hugging Face-API-et viser `gated: auto` for både `pyannote/speaker-diarization-community-1` og `pyannote/speaker-diarization-3.1`, og for `pyannote/segmentation-3.0`; det finnes ingen `HF_TOKEN` i miljøet. **Eirik må godta vilkårene på Hugging Face selv** før modellen kan lastes; B er ikke påbegynt (ingen ADR, ingen EVAL, ingen endring i rørledningen). For DER-målingen senere: NB Samtale validation har per segment `speaker_id`, `segment_order`, `overlap_previous` og `overlap_next` (datasettkortets eksempelrad); i den lokale `validation_metadata.jsonl` finnes i tillegg `source_file_id` og start- og stopptid i `segment_id`, så en referanse-RTTM per opptak kan bygges; lisensen er CC0 (KLAR-EVAL-0004).

**Miljøavvik og retting.** Installasjon av `audiomentations` og `lameenc` i analyse-venvet endret `librosa` (1.0.0 → 0.11.0) og `soxr` (1.1.0 → 0.5.0) og la til seks pakker. Det ble oppdaget før noe ble målt med det endrede miljøet; pakkene ble avinstallert, `librosa` og `soxr` satt tilbake, og `uv pip freeze` ble sammenlignet med pinnene i `requirements.lock` (identisk). Degraderingen kjører nå i et eget venv (`/Volumes/Vault/arkivklarering/venv-degradering`), så det låste analysemiljøet ikke berøres.

**Kildekontroll (KLAR-KILDE-0001, 2026-10-26).** Kilderegisteret er bygget av en underagent (fullkopier av primærkildene ligger bare på Vault, `/Volumes/Vault/arkivklarering/kilder/`, med `SHA256SUMS`; i repoet står URL, sha256, sidetall og sitat) og mekanisk kontrollert med `scripts/sjekk_kilder.py` (alle sitater er eksakte delstrenger av den lagrede kopien etter normalisering av mellomrom og linjeskift). Funn og rettelser: **motsagt (1):** KLAR-ADR-0004 sa at Koenecke mfl. ikke skriver at Whisper dikter opp tekst på ren stillhet, støy eller musikk; artikkelen beskriver oppdiktede setninger «when no one is speaking in the input audio files». Ordlyden i ADR-0004 (v1.2) er strammet inn. **Delvis (24), strammet inn til det sitatet dekker:** KLAR-ADR-0004 (kildekontrollens ordlyd), KLAR-ARK-0001 v1.4 (Koenecke-oppsummeringen, utgivelsessted FAccT ’24 oppgitt i PDF-en, MMIF/CLAMS-beskrivelsen, AMP planleggingsrapport/sluttrapport, FixIt+, nynorsk i NB-Whisper-kortene, Presidio og CLEANUP-guiden: forfatterangivelse «NR and NAV through the CLEANUP-project», stedsetiketter i stedet for stedsliste), KLAR-EVAL-0001 v1.2 (én setning), KLAR-ADR-0008 v1.2 (forfatterangivelse), README (OHMS-URL: weareavp.com, Wayback-snapshot og versjon 6.0 nyest) og KLAR-PREREG-0001 v1.4. **Ikke funnet (5):** OHMS' egne eksempelfiler (opphav ikke dokumentert; README sier nå «eksempelfilene vi har … opphav ikke dokumentert»), OHMS CSV-malen på Dropbox (historisk loggoppføring; kan ikke etterprøves uten URL, malen ble ikke brukt), OSF-registreringen (OSF-API-et svarer 401 under embargo; oppgitt av eier), og to påstander om svenske, danske og nederlandske arkiver i den registrerte OSF-teksten `KLAR-REG-0001` (kopi av registrert tekst, endres ikke). Lenken til AMP i ARK-0001 gjelder planleggingsrapporten (2018); sluttrapporten (AMPPD, desember 2021) er hentet separat. PyPI-siden for inaVAMOS svarer med en klientsjekk som ikke er omgått; innholdet er hentet fra PyPI JSON-API-et. **Avvik i PREREG-0001:** malbeskrivelsen sa «versjon 4 av malen»; det står ikke i OSF-skjemablokkene og er fjernet (v1.4). Hashen av KLAR-MANUS-0002 er uendret (`d0684b0a…`), og analyse-koden (tag `h4-script-v1`) er uendret.

**KLAR-MANUS-0002 rettet til v1.2 (oko04nn) før registrering.** Oppslag i Nynorskordboka via ord.uib.no-API-et (`articles?w=<ord>&dict=nn&scope=ei`, 2026-10-26): «anmerkning» og «anmerking» har ingen oppføring i Nynorskordboka (Bokmålsordboka har `anmerkning`, ikke `anmerking`); «merknad» finnes (m1, bestemt form «merknaden»), og det gjør «betalingsmerknad» (artikkel 120409, bestemt form «betalingsmerknaden»). Ordboka viser altså en annen form, så oko04nn er endret fra «Etter betalingsanmerkinga fekk han ikkje lån i banken.» til «Etter betalingsmerknaden fekk han ikkje lån i banken.» (målelementer nn: betalingsmerknaden / betalingsmerknad / betalingsanmerkninga / betalingsanmerkningen; nb er uendret). Ord uten treff etter rettelsen: 17 (16 sammensatte ord og én genitiv). Ny sha256 `9a3d12d1e2438b09f9fcb6aa43300ace406888732d058e3cbabf70cb0ad963b1` (v1.1 hadde `d0684b0a2f6c21309c7087a5a5915921a378023320f6a6bd1b85232809b78599`). PREREG-0001 v1.5 har den nye verdien; ARK-0005 v1.1 peker på v1.2. Analyse-koden (tag `h4-script-v1`) er uendret.

**Kilderegisteret utvidet (runde 3 og 4).** RG-01 (Mediesök) er verifisert mot KB.se; RG-02 (Det Kgl. Bibliotek) mot konferanseabstraktet på pure.kb.dk, og NISV-delen mot CLARIAH Media Suite (sekundær); NISVs egen side svarer med en omdirigering til en innloggingsside og er ikke hentet (RG-02d «ikke funnet»). OS-01: ingen fil på disk eller melding i Mail nevner «fbme7»; en OSF-varsel om registrering under embargo er lagret på Vault i redigert kopi (tokens og mottaker fjernet) og raden er «delvis», kildetype eieroppgitt (OSF fbme7, under embargo). OH-04 og OH-06 er «egen observasjon»: alle fem filer i `ohms_xml_samples.zip` (sha256 `14335d31…`) feiler mot `ohms.xsd` v5.4 (logg på Vault); Dropbox-lenken til CSV-malen står på Museums Ontarios OHMS-side og svarer HTTP 200 med en HTML-feilside (logg på Vault); «bare på Dropbox» kan ikke påvises (delvis). Registeret har 154 rader.

**HF-token og talerinndeling (oppgave B åpnet).** Det fantes ett Hugging Face-token i miljøet og i `.env`-filene (ikke to): `~/.cache/huggingface/token` (lengde 37, prefiks «hf_»). Konto: Avalyset. `HfApi().auth_check()` ga tilgang for alle tre pyannote-repoene (`speaker-diarization-community-1`, `speaker-diarization-3.1`, `segmentation-3.0`); en liten fil ble lastet ned fra hvert. Tokenet er lagt i `~/dev/arkivklarering/.env` som `HF_TOKEN` (gitignorert, modus 600) og leses bare inne i runner-prosessen. Modellkort og lisenser er lest ordrett inn i kilderegisteret før bruk (community-1: `license: cc-by-4.0`; 3.1 og segmentation-3.0: `license: mit`). `KLAR-ADR-0016` (pyannote community-1, anonyme TALER_n, `--taler`, eget venv `requirements-diarisering.lock`) og koden er skrevet og testet med enhetstester; DER-målingen (`eval/dev/kjor_der.py`, KLAR-EVAL-0012) er ikke kjørt ennå. Tilgangen for kilderegister-underagenten ble avslått av tillatelsessystemet, så kortene er hentet av hovedøkten.

**Rettelse i KLAR-EVAL-0010.** Teksten sa «sju segmenter»; det er seks (seks segmenter hadde under halvparten av referanseordene i «før»-kjøringen, tre av dem tomt; ett av de seks hadde også under halvparten etter degraderingen). WER uten disse seks er 0,211 før og 0,182 etter (54 segmenter). Oppgaveteksten omtalte «9 segmenter» (3 + 6); de 3 tomme er en del av de 6.

**Diagnose av tomt/kort rålag (pågår, KLAR-EVAL-0011).** Mellomstatus 2026-10-26: whisper.cpps beslutningslinjer (debug-bygget `whisper-cli`, egen byggemappe på Vault, samme kilde, `-DWHISPER_DEBUG`) viser at rålaget i de feilende segmentene gir sekvensen «bare ett tidsstempeltoken» med `avg_logprobs` rundt −0,03 til −0,1; vinduet flyttes så 0,06 s om gangen. Terskelen for ingen tale er ikke årsaken (kravet er `avg_logprobs < −1,0`). Analysekoden er ikke endret og taggen `h4-script-v1` er urørt. Endelig dokumentasjon i KLAR-EVAL-0011.

**Diagnose av tomt/kort rålag ferdig (KLAR-EVAL-0011) og ført som avvik før registrering.** Årsak (loggutdrag og kildelinjer i EVAL-0011): `nb-whisper-large-verbatim` avslutter noen vinduer med `[_EOT_]` uten avsluttende tidsstempeltoken; whisper.cpp (`result_len = i + 1` bare ved tidsstempeltoken) kaster da teksten etter det første tidsstempeltokenet og flytter vinduet 0,06 s om gangen (25–68 vinduer) til slutten av lyden. Ikke en kodefeil hos oss (cue-koden, DTW, kontekst mellom filer, språkvalg, no_speech-terskelen og beam-valget er alle prøvd og forkastet; `no_speech_prob` er 0,00000 i alle 42 fallback-beslutninger). Seks av 60 DEV-segmenter (ikke ni; de tre tomme er med i de seks). Ingen kode er endret, ingen tidligere EVAL-tall er endret, taggen `h4-script-v1` er urørt, og tersklene i PREREG-0001 er uendret. PREREG-0001 v1.6 har fått en kjent begrensning. Ett eksisterende CLI-flagg endrer rålagets oppførsel: `-nt` (ingen tidsstempeltokens; DTW-ordtider beholdes) ga 75 av 76 ord på de seks segmentene mot 30 uten flagget; `--vad` ga 39. `-nt` er **ikke innført**; en regresjon på de 60 DEV-segmentene kjøres på grenen `nt-regresjon`, og ingenting går inn på `main` før eier har bestemt seg. `suppress_blank` og `max_initial_ts` finnes bare som bibliotekparametere (ingen CLI-flagg) og er ikke testet. Store dekoderlogger ligger bare på Vault (sha256 i EVAL-0011); `.gitignore` utelukker byggemapper, binærer og rå logger. `ground_truth.py` ignorerer nå `.ots.bak` (ga en falsk «dobbel bruk»-melding om `pilot`/`testdeler`).

**Regresjon av `-nt` på grenen `nt-regresjon` (2026-10-26, ikke på main).** Grenen (commit `981acac` + resultat `bf98563`) har en opt-in-bryter (`ARKIVKLARERING_UTEN_TIDSSTEMPELTOKENS=1` legger `-nt` til whisper-cli-argumentene i `whisper_direkte` og `whisper_flere`) og `eval/dev/kjor_nt_regresjon.py`. Kjørt på de 60 DEV-segmentene (språk etter målform, begge lag, DTW, union; 392 s Whisper), sammenlignet med «før»-kjøringen fra EVAL-0010: **rålag-WER 0,258 → 0,137** (bokmål 0,258 → 0,090, nynorsk 0,258 → 0,213); segmenter med under halvparten av referanseordene i rålaget **6 → 0**; **normalisert lag-WER 0,350 → 0,456** (nynorsk 0,405 → 0,628); union person 15/17 → 14/17, union sted 14/14 → 14/14; rålag sted 10/14 → 12/14; normalisert person 13/17 → 10/17 og sted 13/14 → 10/14. `-nt` er altså bra for rålaget og dårlig for det normaliserte laget når det brukes på begge; en per-lag-løsning er ikke målt. Rålags-cuer uten ordtidsstempler med `-nt`: 0. Ingenting er innført på main; taggen `h4-script-v1` og alle tersklene er uendret. Beslutning venter hos eier.

**Talerinndeling: DER-kjøringen startet** (eget venv, pyannote community-1, CPU, 174 minutter sammenstilt NB Samtale-lyd) etter at alle Whisper-kjøringer var ferdige. Resultat i KLAR-EVAL-0012 når den er ferdig.


## 2026-10-27

**Talerinndeling: DER-kjøringen ferdig (KLAR-EVAL-0012).** Samlet DER 0,166 (collar 0,25 s) og 0,191 (collar 0 s) på konstruert sammenstilling av NB Samtale validation (35 kilder, 8 033 s referansetale); antall talere riktig i 11 av 35. Ikke sammenlignbart med DER på hele opptak. Ingen forhåndsregistrert terskel hviler på tallet. Nummerregisteret er v1.11 (EVAL-0012 i bruk). Whisper-kjøringene for -nt-reproduksjonen (ADR-0017) starter etter dette, én tung jobb om gangen.

**Avvik: rålag endret til -nt etter EVAL-0011, terskler satt på nytt med uendret regel (KLAR-PREREG-0001 v1.7, KLAR-ADR-0017).** Full reproduksjon med `scripts/reproduser.sh` på commit `d75bc40` (00:39–02:24 den 27.10, steg 1, 2, 4, 5, 6, 61, 7, 8, tørrtest, 10a og 10; ingen steg feilet; resultater og sha256 på Vault i `reproduksjon/20261027-003846/`). **Det normaliserte laget er gjenbrukt fra lagret utdata** (modell-sha256 `0f2f66f2…` og parametere uendret, uten `-nt`; gjenbruket er logget i kjøringen for alle ni datasett: NB Samtale 60 segmenter, NPSC 934, syntetisk matchet og `nn` 156 + 156, H4-tørrtest 156, degradering original og degradert 60 + 60); rålaget er kjørt på nytt fra rådata. Nye versjoner (gamle er «før -nt» og beholdt uendret): EVAL-0001 v1.3, EVAL-0002 v1.1, EVAL-0006 v1.2, EVAL-0007 v1.1, EVAL-0008 v1.2, EVAL-0010 v1.2, ny H4-tørrtest 2026-10-27. EVAL-0003 er bit-identisk og EVAL-0005 (NorNE, ingen Whisper) er identisk bortsett fra kjøretid (661 s → 616 s), så de er ikke gitt ny versjon. Viktigste tall: rålag/matchet WER 0,250 → 0,135, rålag/`-l nn` 0,317 → 0,248; tomme rålag-hypoteser 2 og 6 av 60 → 0 og 0; NPSC-union uendret i alle grupper; H4-tørrtest alle tolv kategorier består som før. **Terskler:** bare H1a (≤ 0,35 → ≤ 0,25) og H1d (≤ 0,45 → ≤ 0,35) er satt på nytt, med regelen DEV + 0,10 rundet opp til nærmeste 0,05; H1b, H1e, H2, H3, H4 og kontrollsjekkene er uendret. **Kontrollsjekker mot ny DEV:** K1 holder (0,135 mot 0,348), K2 holder (rålag alene 0,740 mot 0,880 for person og 0,549 mot 0,902 for sted på NPSC; også på NB Samtale 12/17 mot 13/17 og 12/14 mot 13/14), K3 er uberørt (NorNE, ingen Whisper). K2 er derfor **ikke** fjernet. **Analyse-kode:** ingen kode i `arkivklarering/`, `kalibrering/`, `eval/` eller `tests/` ble endret mellom taggen `h4-script-v2` (`224bd0a`) og kjøringen (`d75bc40`); forskjellen i `scripts/` er den nye `lag_nt_versjoner.py` (committet før kjøringen startet, lager bare tabeller). 122 tester grønne etter kjøringen. Taggen `h4-script-v2` er derfor ikke flyttet og pushes uendret; `h4-script-v3` er ikke laget. Én endring i oppførsel som ikke er et tall: på stillhet, støy og musikk skriver rålaget nå spesialtokenet `<|nocaptions|>` (tidligere «.»); koden filtrerer slike cuer (`er_lydmerke`), jf. EVAL-0001 v1.3. **Avvik i kjøringen:** `reproduser.sh` kjørte med `UTEN_CACHE=1` og gjenbruk av normalisert lag som standard; rålagets gamle cache ble ikke brukt.

**KLAR-PREREG-0001 v1.8 (bare tekstrettelser) og kjent svakhet i tests/ (ikke rettet før registrering).** Verifisert mot rådata-JSON før v1.8: H1e (normalisert/`-l nn`) 0,4632 (EVAL-0002 v1.1); H2a–H2f union-tellere 139/150, 92/102, 83/85, 74/80, 56/65, 18/22 (EVAL-0007 v1.1); H3a–H3d recall/presisjon 0,997/0,921, 0,970/0,875, 0,954/0,769, 0,986/0,738 (EVAL-0005, motor «kombinert», original tekst); gammel ra/matchet (EVAL-0002 v1.0) 0,2498, som med regelen gir 0,35 (setningen «samme regel på de gamle tallene» stemmer og er ikke endret). Ingen avvik fra v1.7. Rettet i teksten: «Manuset (v1.1)» → «v1.2»; setningen om at koden er identisk med taggen presisert (ingen .py-fil endret; under `eval/` bare resultatfiler, i `scripts/` bare `lag_nt_versjoner.py`); henvisningen fra H2f peker nå på seksjonen «Other planned analysis (utforskende)», som finnes og nevner H2f. **Svakhet:** `tests/test_manus.py::test_testmanusets_sha256_staar_i_preregistreringen` velger PREREG-fila med leksikografisk `sorted(glob(...))[-1]` og vil velge feil fil fra v1.10 (`v1.10` sorterer før `v1.7`). Ikke rettet før registrering fordi `tests/` er låst med taggen. **Rettes etter registrering som avvik** (naturlig sortering på versjonsnummer).

**KLAR-PREREG-0001 registrert på OSF 2026-10-27: https://osf.io/hc83q/** (mal «OSF Preregistration» v4, fra prosjektet dmb6g; lisens CC-By 4.0; subjects som KLAR-REG-0001; embargo til 2027-10-26, valgt i dialogen etter «Register»; godkjenningsmail fra OSF besvares av Eirik, ellers godkjennes den automatisk etter 48 timer; arkiveringen pågikk da siden ble lest sist, og filer i prosjektet skal ikke endres før arkiveringen er ferdig). Registrert innhold = PREREG v1.8 (tag `prereg-v1` = `bfe647dbe27de68fcf4abd4bf563ecfbf63f8070`; `h4-script-v2` = `224bd0a497b4bbba73efd8840992162fef825afd`; sha256 av testmanuset `9a3d12d1…`); PREREG-fila v1.8 er lastet opp som vedlegg (under Research Design). Fordi det ligger i denne fila (v1.9) at statuslinjen nå er «registrert», er testdelene formelt åpnet i koden (`evaldata.py`), men **ingen testdel er kjørt, og ingen skal kjøres før testmanuset er lest inn**. **Avvik i skjemateksten:** OSF fjerner tekst i vinkelparenteser, så plassholdere (`<OSF-URL>`, `<neste>`, `<NNNN>`) er skrevet med hakeparenteser i feltene «Additional blinding» og «Context»; den opplastede PREREG-fila har originalen. Valg som ikke følger ordrett av PREREG-teksten: «Foreknowledge of data or evidence» = «Authors have observed the data, but have not performed the proposed analyses» (valideringsdelene er sett og terskler er satt fra dem; testdelene er ikke åpnet); Study type = Non-randomized study + Descriptive study; Intention for causal interpretation = No causal relationship; Blinding = No blinding is involved; PREREG-avsnittene «Foreknowledge», «Study type», «Intention…» og «Blinding» er limt inn som tekst under de nærmeste fritekstfeltene (forklaringsfeltet og Study design) fordi malen har valgknapper der PREREG har tekst. Tittel = PREREG-titelen; beskrivelse = innledende avsnitt fra PREREG. **Kjent svakhet (uendret):** `tests/test_manus.py::test_testmanusets_sha256_staar_i_preregistreringen` og `evaldata.py` velger PREREG-fila med leksikografisk sortering (`filer[-1]`); fra v1.10 vil feil fil velges. Rettes etter registrering som avvik.

**Tre tester feiler etter at statuslinjen er satt til «registrert» (forventet, ikke rettet).** `tests/test_evaldata.py::test_utkast_apner_ikke_testdelen`, `tests/test_kjor_h4.py::test_testmanus_kan_ikke_scores_for_preregistreringen_er_registrert` og `tests/test_manus.py::test_testmanuset_er_sperret_for_roerledningen_foer_registrering` leser den ekte PREREG-fila og forutsetter statuslinjen `Status: UTKAST`; med `Status: registrert https://osf.io/hc83q/` heves sperren, og testene som skal bevise at sperren holder før registrering, feiler (resultat etter commit `9036026`: 3 failed, 119 passed; før statusendringen 122 passed). Koden er uendret, og sperren virker som tiltenkt. `tests/` er låst med taggen (`h4-script-v2`, `prereg-v1`) og er ikke endret. **Rettes etter registrering som avvik**, sammen med den leksikografiske sorteringen: testene bør bruke en egen fixture-PREREG med statuslinjen UTKAST i stedet for den ekte fila, og fil-valget bør bruke versjonsnummer, ikke leksikografisk sortering.

**Avvik etter registrering (KLAR-PREREG-0001 v1.10, «Avvik etter registrering»): sperretester og versjonssortering rettet; Foreknowledge på OSF var feil valgt.** (1) De tre sperretestene som feilet etter at statuslinjen ble «registrert» (se forrige oppføring) bruker nå et utkast i en egen mappe, og PREREG- og MANUS-fil velges med versjonssortering i stedet for leksikografisk (`arkivklarering/evaldata.py`, `kalibrering/kjor_h4.py`, `eval/dev/kjor_syntetisk.py`, `scripts/ordbokkontroll.py`, `scripts/navnesjekk.py`, `scripts/rigg_manus.py`, `tests/`); `evaldata.sjekk_splitt` leser `DOCS` ved kall. Ny test for v1.10 mot v1.9. 123 tester grønne (før: 3 failed, 119 passed). Ingen målte tall påvirket; ingen ny tag (`h4-script-v2` og `prereg-v1` er uendret). (2) **Foreknowledge på OSF ble satt til ‹Authors have observed the data, but have not performed the proposed analyses›. Det riktige er: testdelene (NB Samtale, NorNE, NPSC test) er ikke lastet inn eller observert (sperret i koden). Testmanuset er skrevet av forfatterne, men ingen opptak finnes. DEV-dataene (validation) er observert.** Ingen endring på OSF; prosjektet dmb6g er ikke berørt mens OSF-arkiveringen ikke er bekreftet ferdig.

**Kodediff mot `h4-script-v2` (ordrett), ført etter registreringen.** Kommando: `git diff 224bd0a HEAD -- arkivklarering/evaldata.py kalibrering/kjor_h4.py eval/dev/kjor_syntetisk.py scripts/` (HEAD = `efba7ad`). Ordren nevnte stien `kalibrering/kjor_syntetisk.py`; den finnes ikke, filen ligger i `eval/dev/kjor_syntetisk.py`, og det er den som er tatt med. `tests/` er ikke med i diffen (endringene der står i commit `27c6314`). **Hva diffen viser:** (a) i `kalibrering/kjor_h4.py`, `eval/dev/kjor_syntetisk.py`, `scripts/ordbokkontroll.py`, `scripts/navnesjekk.py` og `scripts/rigg_manus.py` er `sorted(glob(...))[-1]` byttet med versjonssortering (`evaldata.siste_versjon`, i `rigg_manus.py` en innebygd `max` med samme nøkkel): bare valg av hvilken PREREG- eller MANUS-fil som leses, ingen måle- eller analyselogikk; (b) i `arkivklarering/evaldata.py` er det lagt til to hjelpefunksjoner (`versjonsnokkel`, `siste_versjon`), og `sjekk_splitt` velger PREREG-fila med versjonsnøkkel i stedet for leksikografisk, og leser `DOCS` ved kall (parameteren `docs` har standardverdi `None` i stedet for `DOCS`, slik at tester kan peke den til en egen mappe); sperrens vilkår (`Status: registrert`, tegnstrengen i fila) er ikke endret; (c) `scripts/lag_nt_versjoner.py` er en ny fil (131 linjer, lager bare før/etter-tabeller), committet før reproduksjonskjøringen og allerede ført i oppføringen for 27.10. Diffen viser altså filvalg, to nye hjelpefunksjoner og én ny tabellskript; ingen endring i Whisper-kall, matching, flagging eller beregning av tall.

```diff
diff --git a/arkivklarering/evaldata.py b/arkivklarering/evaldata.py
index da10ada..bdfa763 100644
--- a/arkivklarering/evaldata.py
+++ b/arkivklarering/evaldata.py
@@ -21,14 +21,26 @@ class TestdelSperret(PermissionError):
     __test__ = False  # ikke en pytest-klasse
 
 
-def sjekk_splitt(splitt: str, prereg_id: str | None = None, docs: pathlib.Path = DOCS) -> str:
+def versjonsnokkel(sti) -> tuple:
+    """Sorteringsnøkkel etter versjonsnummeret i filnavnet (`..._v1.10_...` er nyere enn `..._v1.9_...`), ikke leksikografisk."""
+    m = re.search(r"_v(\d+(?:\.\d+)*)_", pathlib.Path(sti).name)
+    return (tuple(int(x) for x in m.group(1).split(".")) if m else (), pathlib.Path(sti).name)
+
+
+def siste_versjon(filer):
+    """Den nyeste filen etter versjonsnummer (versjonssortering). Tom liste gir IndexError, som `sorted(...)[-1]`."""
+    return sorted(filer, key=versjonsnokkel)[-1]
+
+
+def sjekk_splitt(splitt: str, prereg_id: str | None = None, docs: pathlib.Path | None = None) -> str:
     if splitt not in SPLITT:
         raise ValueError(f"Ukjent splitt «{splitt}». Gyldige: {', '.join(SPLITT)}")
     if splitt != "test":
         return splitt
     if not prereg_id or not _PREREG.match(prereg_id):
         raise TestdelSperret("test-delen kan ikke lastes uten --prereg-id KLAR-PREREG-<NNNN>")
-    filer = sorted(pathlib.Path(docs).glob(f"{prereg_id}_*.md"))
+    docs = DOCS if docs is None else docs  # leses ved kall, slik at tester kan peke DOCS til en egen mappe
+    filer = sorted(pathlib.Path(docs).glob(f"{prereg_id}_*.md"), key=versjonsnokkel)
     if not filer:
         raise TestdelSperret(f"{prereg_id}: fant ingen docs/{prereg_id}_*.md. "
                              "Preregistreringen må ligge i repoet før testdelen åpnes.")
diff --git a/eval/dev/kjor_syntetisk.py b/eval/dev/kjor_syntetisk.py
index a1dee0d..b290039 100644
--- a/eval/dev/kjor_syntetisk.py
+++ b/eval/dev/kjor_syntetisk.py
@@ -26,7 +26,7 @@ sys.path.insert(0, str(HER))
 import felles  # noqa: E402
 from felles import REPO, dict_til_cue, legg_til_jsonl, les_jsonl  # noqa: E402
 
-from arkivklarering import kalibrering, personvern, transkriber  # noqa: E402
+from arkivklarering import evaldata, kalibrering, personvern, transkriber  # noqa: E402
 
 DATO = datetime.date.today().isoformat()
 LYD = pathlib.Path("/Volumes/Vault/arkivklarering/lyd/syntetisk")
@@ -96,7 +96,7 @@ def main():
     ap = argparse.ArgumentParser()
     ap.add_argument("--fase", default="alle", choices=["lyd", "kjor", "evaluer", "alle"])
     a = ap.parse_args()
-    manus_sti = sorted(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0001_*.tsv")))[-1]
+    manus_sti = evaldata.siste_versjon(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0001_*.tsv")))
     manus = kalibrering.les_manus(manus_sti)
     if a.fase in ("lyd", "alle"):
         lag_lyd(manus)
diff --git a/kalibrering/kjor_h4.py b/kalibrering/kjor_h4.py
index fb09303..b43e48e 100644
--- a/kalibrering/kjor_h4.py
+++ b/kalibrering/kjor_h4.py
@@ -194,10 +194,10 @@ def main():
     ap.add_argument("--oppsett", default="matchet", choices=list(OPPSETT))
     a = ap.parse_args()
 
-    prereg = sorted(glob.glob(str(REPO / "docs" / "KLAR-PREREG-0001_*.md")))[-1]
+    prereg = evaldata.siste_versjon(glob.glob(str(REPO / "docs" / "KLAR-PREREG-0001_*.md")))
     terskler = les_terskler(prereg)
     if a.torrtest:
-        manus_sti = sorted(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0001_*.tsv")))[-1]
+        manus_sti = evaldata.siste_versjon(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0001_*.tsv")))
         manus = kalibrering.les_manus(manus_sti)
         opptak = [("syntetisk", {"dialektregion": None, "dialektkilde": None}, {r["id"]: SYNTETISK / f"{r['id']}.wav" for r in manus
                                                                                   if (SYNTETISK / f"{r['id']}.wav").is_file()})]
@@ -209,7 +209,7 @@ def main():
         if not a.prereg_id:
             sys.exit("H4 på testmanuset krever --prereg-id KLAR-PREREG-0001 (og at preregistreringen er registrert)")
         evaldata.sjekk_splitt("test", a.prereg_id)
-        manus_sti = sorted(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))[-1]
+        manus_sti = evaldata.siste_versjon(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))
         manus = kalibrering.les_manus(manus_sti, prereg_id=a.prereg_id)
         sha = sha256_fil(manus_sti)
         if sha not in pathlib.Path(prereg).read_text(encoding="utf-8"):
diff --git a/scripts/lag_nt_versjoner.py b/scripts/lag_nt_versjoner.py
new file mode 100644
index 0000000..327167d
--- /dev/null
+++ b/scripts/lag_nt_versjoner.py
@@ -0,0 +1,131 @@
+#!/usr/bin/env python3
+"""Lager før/etter-tabeller (før -nt / etter -nt for rålaget, KLAR-ADR-0017) for de berørte EVAL-ene fra to sett resultatfiler.
+
+    .venv/bin/python scripts/lag_nt_versjoner.py <ny-mappe> [--ut <mappe>]
+
+`<ny-mappe>` er `resultater/` fra `scripts/reproduser.sh`. «Før» leses fra de committede filene (versjonene før -nt). Skriver
+Markdown-tabeller til stdout/`--ut` og ingen kvalitetspåstander: bare tall. Tolkning skrives for hånd i EVAL-dokumentene.
+"""
+import glob
+import json
+import pathlib
+import sys
+
+REPO = pathlib.Path(__file__).resolve().parent.parent
+
+
+def f3(x):
+    return "–" if x is None else f"{x:.3f}".replace(".", ",")
+
+
+def siste(mønster, rot=REPO, som=-1):
+    fs = sorted(pathlib.Path(rot).glob(mønster))
+    return fs[som] if fs else None
+
+
+def les(p):
+    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
+
+
+def t_eval0002(for_, etter):
+    """WER totalt og per skriftform for de fire oppsettene."""
+    rader = ["| oppsett | gruppe | n | før -nt | etter -nt |", "|---|---|---|---|---|"]
+    for kol in ("ra/matchet", "ra/nn", "normalisert/matchet", "normalisert/nn"):
+        for g in ("totalt", "skrift:bm", "skrift:nn"):
+            rader.append(f"| {kol} | {g} | {for_['wer'][kol][g + '_n']} | {f3(for_['wer'][kol][g])} | {f3(etter['wer'][kol][g])} |")
+    return "\n".join(rader)
+
+
+def _surv(res):
+    ut = {}
+    for g, d in res.items():
+        for k, v in d["kategorier"].items():
+            ut[(g, k)] = (v["overlevd_a"], v["ref"])
+    return ut
+
+
+def t_overlevelse(for_, etter):
+    """Overlevelse (a) per målform, kategori og kilde (rålag/normalisert/union), samlet over målformer."""
+    a, b = _surv(for_["resultat"]), _surv(etter["resultat"])
+    rader = ["| kategori | lag | målform | før -nt | etter -nt |", "|---|---|---|---|---|"]
+    for kat in ("person", "sted"):
+        for kilde in ("ra", "normalisert", "union"):
+            tot_a = [0, 0]
+            tot_b = [0, 0]
+            for g in ("nb", "nn"):
+                x, y = a.get((g, f"{kilde}|{kat}"), (0, 0)), b.get((g, f"{kilde}|{kat}"), (0, 0))
+                rader.append(f"| {kat} | {kilde} | {'bokmål' if g == 'nb' else 'nynorsk'} | {x[0]}/{x[1]} ({f3(x[0] / x[1]) if x[1] else '–'}) | {y[0]}/{y[1]} ({f3(y[0] / y[1]) if y[1] else '–'}) |")
+                tot_a[0] += x[0]; tot_a[1] += x[1]; tot_b[0] += y[0]; tot_b[1] += y[1]
+            rader.append(f"| {kat} | {kilde} | **samlet** | {tot_a[0]}/{tot_a[1]} ({f3(tot_a[0] / tot_a[1]) if tot_a[1] else '–'}) | {tot_b[0]}/{tot_b[1]} ({f3(tot_b[0] / tot_b[1]) if tot_b[1] else '–'}) |")
+    return "\n".join(rader)
+
+
+def t_eval0008(for_, etter):
+    """Flagg-treff (union, begge målformer) per klasse, konfigurasjon matchet og nn."""
+    rader = ["| konfigurasjon | kategori | før -nt | etter -nt |", "|---|---|---|---|"]
+    kats = ["person", "sted", "dato", "fødselsår", "telefon", "fødselsnummer", "e-post", "helse", "økonomi", "konflikt", "religion", "politikk"]
+    for konf in ("matchet", "nn"):
+        for k in kats:
+            def sum_(j):
+                n = fl = 0
+                for mf in ("nb", "nn"):
+                    d = j["resultat"][konf]["elementer"].get(f"union|{mf}", {}).get(k)
+                    if d:
+                        n += d["n"]; fl += d["flagg"]
+                return fl, n
+            x, y = sum_(for_), sum_(etter)
+            rader.append(f"| {konf} | {k} | {x[0]}/{x[1]} | {y[0]}/{y[1]} |")
+    return "\n".join(rader)
+
+
+def t_eval0010(for_, etter):
+    rader = ["| lag | målform | betingelse | n | før -nt (EVAL-0010 v1.1) | etter -nt |", "|---|---|---|---|---|---|"]
+    for cond in ("for", "etter"):
+        for k in for_["wer"][cond]:
+            lag, g = k.split("|")
+            rader.append(f"| {lag} | {g} | {'ren lyd' if cond == 'for' else 'degradert'} | {for_['wer'][cond][k]['n']} | {f3(for_['wer'][cond][k]['wer'])} | {f3(etter['wer'][cond][k]['wer'])} |")
+    return "\n".join(rader)
+
+
+def t_h4(for_, etter):
+    rader = ["| kategori | før -nt | etter -nt | terskel | vurdering etter -nt |", "|---|---|---|---|---|"]
+    ef = {r["kategori"]: r for r in etter["union"]}
+    for r in for_["union"]:
+        e = ef[r["kategori"]]
+        rader.append(f"| {r['kategori']} | {r['flagg_treff']}/{r['n']} | {e['flagg_treff']}/{e['n']} | {r['terskel']} | {e['vurdering']} |")
+    return "\n".join(rader)
+
+
+def main():
+    ny = pathlib.Path(sys.argv[1])
+    ut = {}
+    p = siste("eval/dev/KLAR-EVAL-0002*v1.0_*.json")
+    q = siste("eval/dev/KLAR-EVAL-0002*v1.0_*.json", ny)
+    if p and q:
+        ut["EVAL-0002"] = t_eval0002(les(p), les(q))
+    p = siste("docs/KLAR-EVAL-0006*v1.1_*.json")
+    q = siste("docs/KLAR-EVAL-0006*v1.1_*.json", ny)
+    if p and q:
+        ut["EVAL-0006 v1.1 (ordtider)"] = t_overlevelse(les(p), les(q))
+    p = siste("docs/KLAR-EVAL-0007*v1.0_*.json")
+    q = siste("docs/KLAR-EVAL-0007*v1.0_*.json", ny)
+    if p and q:
+        ut["EVAL-0007"] = t_overlevelse(les(p), les(q))
+    p = siste("docs/KLAR-EVAL-0008*v1.1_*.json")
+    q = siste("docs/KLAR-EVAL-0008*v1.1_*.json", ny)
+    if p and q:
+        ut["EVAL-0008"] = t_eval0008(les(p), les(q))
+    p = siste("docs/KLAR-EVAL-0010*v1.0_*.json")
+    q = siste("docs/KLAR-EVAL-0010*v1.0_*.json", ny)
+    if p and q:
+        ut["EVAL-0010"] = t_eval0010(les(p), les(q))
+    p = siste("eval/dev/h4_torrtest_justeringsmanus_*.json")
+    q = siste("eval/dev/h4_torrtest_justeringsmanus_*.json", ny)
+    if p and q:
+        ut["H4-tørrtest"] = t_h4(les(p), les(q))
+    for k, v in ut.items():
+        print(f"## {k}\n\n{v}\n")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/scripts/navnesjekk.py b/scripts/navnesjekk.py
index c04db2e..ef8fc9a 100644
--- a/scripts/navnesjekk.py
+++ b/scripts/navnesjekk.py
@@ -37,8 +37,8 @@ def sok(navn):
 
 
 def main():
-    from arkivklarering import kalibrering
-    manus = sorted(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))[-1]
+    from arkivklarering import evaldata, kalibrering
+    manus = evaldata.siste_versjon(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))
     rader = kalibrering.les_manus(manus, kun_struktur=True)
     funn, sett = [], {}
     for r in rader:
diff --git a/scripts/ordbokkontroll.py b/scripts/ordbokkontroll.py
index f95d32d..a1ffa67 100644
--- a/scripts/ordbokkontroll.py
+++ b/scripts/ordbokkontroll.py
@@ -48,8 +48,8 @@ def tokens(setning):
 
 def main():
     import glob
-    from arkivklarering import kalibrering
-    manus = sorted(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))[-1]
+    from arkivklarering import evaldata, kalibrering
+    manus = evaldata.siste_versjon(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))
     sha = hashlib.sha256(pathlib.Path(manus).read_bytes()).hexdigest()
     rader = kalibrering.les_manus(manus, kun_struktur=True)
     cache = {}
diff --git a/scripts/rigg_manus.py b/scripts/rigg_manus.py
index af9887d..fe5c9dd 100644
--- a/scripts/rigg_manus.py
+++ b/scripts/rigg_manus.py
@@ -14,6 +14,7 @@ leser alle 156. Skriptet leser bare teksten som skal leses opp; det kjører inge
 import glob
 import os
 import pathlib
+import re
 import sys
 
 REPO = pathlib.Path(__file__).resolve().parent.parent
@@ -27,7 +28,7 @@ def main(argv=None):
     argv = list(sys.argv[1:] if argv is None else argv)
     tor = "--tor" in argv
     argv = [a for a in argv if a != "--tor"]
-    manus = sorted(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")))[-1]
+    manus = max(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")), key=lambda p: tuple(int(x) for x in re.search(r"_v(\d+(?:\.\d+)*)_", p).group(1).split(".")))  # versjonssortering
     for d in ("kalibrering", "kjerne", "lytter"):
         sys.path.insert(0, str(NORSK_TALE / d))
     import rigg  # norsk-tale/kalibrering/rigg.py
```

**Kjøringsmetadata for testdelene registreres utenfra (KLAR-PREREG-0001 v1.11, punkt 3).** Ordre: commit-SHA og `git status --porcelain` (skal være tom) skal følge testkjøringen, uten å endre `kalibrering/kjor_h4.py`, `arkivklarering/evaldata.py` eller annen analysekode. Slik var det ikke fra før: `kjor_h4.py` skriver verken SHA eller arbeidstrestatus i resultatet (`reproduser.sh` kjører riktignok i en worktree av HEAD og avviser urent tre, men skriver SHA bare i `sha256.txt` på Vault, og `--med-h4` er ikke en egen metadatafil). Tillagt: `scripts/kjor_testdel.sh` (ny fil) som starter `kjor_h4.py`, nekter å kjøre hvis `git status --porcelain` ikke er helt tom (exit 1, også usporede filer), og etterpå skriver `<resultat>_kjoring_meta.json` ved siden av resultatfila (`docs/KLAR-EVAL-0009_..._kjoring_meta.json`) med commit, tom porcelain, kommando, start og slutt (UTC), returkode, resultatfil, SHA-ene til `prereg-v1` og `h4-script-v2` og sha256 av gjeldende PREREG- og MANUS-fil. EVAL-0009 skal sitere fila. `--tor` skriver bare hva som ville blitt kjørt. Testet i `tests/test_kjor_testdel.py` (urent tre kjører ikke, `--tor` skriver ingenting, rent tre gir metafil, returkoden bevares); ingen testdel er kjørt. Ingen tall og ingen terskel berørt; ingen ny tag (skriptet er ikke analysekode, men er ført her og i PREREG v1.11).

**`scripts/kjor_testdel.sh`: commit, push og speil etter hver testdel (KLAR-PREREG-0001 v1.12, punkt 3).** Ordre: resultat og metafil skal committes etter HVER testdel (H1–H4), med push og speil, før neste starter; ellers ville wrapperen stoppet på sitt eget resultat (urent tre). Skriptet kjører nå `H1`, `H2`, `H3`, `H4` eller `alle` (rekkefølge H1, H2, H3, H4; H4 til sist) med de eksisterende skriptene (`eval/dev/kjor_dev.py`, `eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc ... --mal-person 300 --mal-sted 200 --maks-timer 4`, `eval/dev/kjor_personvern_dev.py`, `kalibrering/kjor_h4.py`, alle med `--splitt test --prereg-id` der det finnes). Før hver del: tomt `git status --porcelain` ellers exit 1. Etter hver del: metafil (`<resultat>_kjoring_meta.json`), `git add -A`, commit («Testdel Hn: ...»), `git push` til origin, `scripts/speil.sh`. Stopper uten commit (exit 4) hvis kjøringen har endret en sporet fil (ingenting tilbakestilles); en feilet del committes med returkoden og stopper deretter. Testet i `tests/test_kjor_testdel.py` (6 tester, bl.a. fire kjøringer etter hverandre med riktig start-commit, én commit, ett push og ett speil per del; ingen testdel kjørt). 129 tester grønne. Ingen analysekode endret, ingen tall og ingen terskel berørt, ingen ny tag. **Kjente forhold, ikke rettet (krever beslutning, se rapporten):** (1) `eval/dev/kjor_dev.py` trekker `PER_DIALEKT = 12` (60 segmenter), mens PREREG H1 sier opptil 60 per dialektområde (opptil 300); H1 gir derfor ikke PREREG-utvalget uten kodeendring. (2) H1–H3-skriptene skriver testresultatene under DEV-filnavn og DEV-overskrifter (EVAL-0002/-0003, -0005, -0007, «DEV-måling … 60 segmenter») med dagens dato; navn og nummer for testresultatene er ikke bestemt, og `kjor_flaggoverlevelse_ord.py` nekter `--datasett nbsamtale` på test.

   Diff (ordrett) mot commit `13124a2` (`git diff 13124a2 -- scripts/kjor_testdel.sh tests/test_kjor_testdel.py`):

```diff
diff --git a/scripts/kjor_testdel.sh b/scripts/kjor_testdel.sh
index f763123..2ad2d3a 100755
--- a/scripts/kjor_testdel.sh
+++ b/scripts/kjor_testdel.sh
@@ -1,57 +1,112 @@
 #!/bin/bash
 #
-# kjor_testdel.sh: starter en kjøring av kalibrering/kjor_h4.py (typisk H4 på testmanuset) utenfra og skriver kjøringens identitet til
-# en egen fil ved siden av resultatet: <resultat>_kjoring_meta.json (commit-SHA, `git status --porcelain` ved start, kommando, tider,
-# returkode, SHA-er for taggene og sha256 for PREREG- og MANUS-fila). EVAL-dokumentet siterer den fila. Analysekoden er uendret.
+# kjor_testdel.sh: kjører testdelene (H1–H4) én og én utenfra, og etter HVER del committer den resultat og kjøringsmetadata, pusher (privat)
+# og kjører scripts/speil.sh før neste del starter. Analysekoden er uendret; skriptet bare starter den.
 #
-#   source scripts/miljo.sh && scripts/kjor_testdel.sh [--tor] --prereg-id KLAR-PREREG-0001 [flere argumenter til kjor_h4.py]
+#   source scripts/miljo.sh && scripts/kjor_testdel.sh [--tor] <H1|H2|H3|H4|alle> --prereg-id KLAR-PREREG-0001 [-- ekstra argumenter]
 #
-# Arbeidstreet må være helt rent ved start (`git status --porcelain` tom, også uten usporede filer), ellers kjøres ingenting (exit 1).
-# --tor skriver hva som ville blitt kjørt og avslutter; ingenting kjøres og ingen fil skrives.
+#   H1  eval/dev/kjor_dev.py --splitt test                                              (NB Samtale test)
+#   H2  eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --mal-person 300 --mal-sted 200 --maks-timer 4   (PREREG: doble mål)
+#   H3  eval/dev/kjor_personvern_dev.py --splitt test                                   (NorNE test)
+#   H4  kalibrering/kjor_h4.py                                                          (menneskeinnlest testmanus)
+#   alle = H1, H2, H3, H4 i den rekkefølgen (H4 til sist: opptakene må være innlest og scoret først, se PREREG).
+#
+# Før hver del: `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1). Etter hver del skrives
+# <resultat>_kjoring_meta.json (commit-SHA ved start, tom porcelain, kommando, tider, returkode, resultatfiler, SHA-ene til taggene og sha256 for PREREG-
+# og MANUS-fila). Så: commit av resultat og metafil, push, speil. Stopper hele kjøringen (ingen neste del) hvis en del feiler, hvis en SPORET fil er
+# endret av kjøringen (da committes ingenting, exit 4; fjerner ikke noe), eller hvis commit, push eller speil feiler. Feilede deler committes (med
+# returkoden i metafila) og stopper deretter. --tor skriver bare hva som ville blitt kjørt.
 set -euo pipefail
 
 REPO="$(cd "$(dirname "$0")/.." && pwd)"
 cd "$REPO"
 PY="${KLAR_PY:-.venv/bin/python}"
-TOR=0; ARGV=()
-for a in "$@"; do if [ "$a" = "--tor" ]; then TOR=1; else ARGV+=("$a"); fi; done
+SPEIL="${KLAR_SPEIL:-scripts/speil.sh}"
+REMOTE="${KLAR_REMOTE:-origin}"
+TOR=0; DEL=""; ID=""; EKSTRA=()
+while [ $# -gt 0 ]; do
+  case "$1" in
+    --tor) TOR=1 ;;
+    --prereg-id) ID="${2:?mangler verdi til --prereg-id}"; shift ;;
+    --) shift; EKSTRA=("$@"); break ;;
+    H1|H2|H3|H4|alle) DEL="$1" ;;
+    *) echo "ukjent argument: $1" >&2; exit 2 ;;
+  esac
+  shift
+done
+[ -n "$DEL" ] && [ -n "$ID" ] || { echo "bruk: kjor_testdel.sh [--tor] <H1|H2|H3|H4|alle> --prereg-id KLAR-PREREG-<NNNN> [-- ekstra]" >&2; exit 2; }
+if [ "$DEL" = alle ]; then DELER=(H1 H2 H3 H4); else DELER=("$DEL"); fi
 
-PORC="$(git status --porcelain)"
-if [ -n "$PORC" ]; then
-  echo "FEIL: arbeidstreet er ikke rent; kjører ikke. git status --porcelain:" >&2
-  echo "$PORC" >&2
-  exit 1
-fi
-SHA="$(git rev-parse HEAD)"
-KMD="$PY kalibrering/kjor_h4.py ${ARGV[*]:-}"
-if [ "$TOR" -eq 1 ]; then echo "(--tor) ville kjørt på $SHA: $KMD"; exit 0; fi
+kommando() {  # skriver skriptet og argumentene for en del, ett ord per linje
+  case "$1" in
+    H1) printf '%s\n' eval/dev/kjor_dev.py --splitt test --prereg-id "$ID" ;;
+    H2) printf '%s\n' eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --prereg-id "$ID" --mal-person 300 --mal-sted 200 --maks-timer 4 ;;
+    H3) printf '%s\n' eval/dev/kjor_personvern_dev.py --splitt test --prereg-id "$ID" ;;
+    H4) printf '%s\n' kalibrering/kjor_h4.py --prereg-id "$ID" ;;
+  esac
+}
 
-PRE="$(ls docs/KLAR-PREREG-0001_*.md | sort -V | tail -1)"
-MAN="$(ls kalibrering/KLAR-MANUS-0002_*.tsv | sort -V | tail -1)"
-TID="$(date +%Y%m%d-%H%M%S)"
-START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
-FOR="$(ls docs/KLAR-EVAL-0009_*.json eval/dev/h4_*.json 2>/dev/null | sort || true)"
+rent_eller_stopp() {
+  local p; p="$(git status --porcelain)"
+  if [ -n "$p" ]; then
+    echo "FEIL: arbeidstreet er ikke rent; kjører ikke. git status --porcelain:" >&2
+    echo "$p" >&2
+    exit 1
+  fi
+}
+
+rent_eller_stopp
+if [ "$TOR" -eq 1 ]; then
+  for d in "${DELER[@]}"; do
+    K=(); while IFS= read -r l; do K+=("$l"); done < <(kommando "$d")
+    echo "(--tor) $d ville kjørt på $(git rev-parse HEAD): $PY ${K[*]} ${EKSTRA[*]:-}"
+  done
+  exit 0
+fi
 
-set +e
-"$PY" kalibrering/kjor_h4.py "${ARGV[@]+"${ARGV[@]}"}"
-RC=$?
-set -e
+for d in "${DELER[@]}"; do
+  rent_eller_stopp   # etter forrige dels commit skal treet være rent igjen
+  K=(); while IFS= read -r l; do K+=("$l"); done < <(kommando "$d")
+  SHA="$(git rev-parse HEAD)"
+  KMD="$PY ${K[*]} ${EKSTRA[*]:-}"
+  PRE="$(ls docs/${ID}_*.md | sort -V | tail -1)"
+  MAN="$(ls kalibrering/KLAR-MANUS-0002_*.tsv | sort -V | tail -1)"
+  TID="$(date +%Y%m%d-%H%M%S)"
+  START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
+  echo "== $d ($KMD) på $SHA"
+  set +e
+  "$PY" "${K[@]}" "${EKSTRA[@]+"${EKSTRA[@]}"}"
+  RC=$?
+  set -e
+  SLUTT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
 
-SLUTT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
-ETTER="$(ls docs/KLAR-EVAL-0009_*.json eval/dev/h4_*.json 2>/dev/null | sort || true)"
-NY="$(comm -13 <(echo "$FOR") <(echo "$ETTER") | tail -1 || true)"
-if [ -n "$NY" ]; then META="${NY%.json}_kjoring_meta.json"; else META="docs/kjoring_meta_$TID.json"; fi
-export META SHA START SLUTT RC KMD PRE MAN NY
-export TAG_PREREG="$(git rev-parse -q --verify 'refs/tags/prereg-v1^{commit}' || echo mangler)"
-export TAG_H4="$(git rev-parse -q --verify 'refs/tags/h4-script-v2^{commit}' || echo mangler)"
-export SHA_PRE="$(shasum -a 256 "$PRE" | cut -d' ' -f1)" SHA_MAN="$(shasum -a 256 "$MAN" | cut -d' ' -f1)"
-"$PY" - <<'PYEOF'
+  ENDRET="$(git status --porcelain --untracked-files=no)"
+  if [ -n "$ENDRET" ]; then
+    echo "STOPP: kjøringen endret sporede filer; ingenting committet, ingen neste del. Sjekk med git diff (ingenting er fjernet eller tilbakestilt):" >&2
+    echo "$ENDRET" >&2
+    exit 4
+  fi
+  NYE="$(git status --porcelain --untracked-files=all | sed 's/^?? //' | sort)"
+  RES="$(echo "$NYE" | grep -E '^(docs/KLAR-EVAL|eval/dev/KLAR-EVAL).*\.json$' | head -1 || true)"
+  [ -n "$RES" ] || RES="$(echo "$NYE" | grep -E '\.json$' | head -1 || true)"
+  if [ -n "$RES" ]; then META="${RES%.json}_kjoring_meta.json"; else META="docs/kjoring_meta_${d}_$TID.json"; fi
+  export META SHA START SLUTT RC KMD PRE MAN RES DEL_NAVN="$d" NYE
+  export TAG_PREREG="$(git rev-parse -q --verify 'refs/tags/prereg-v1^{commit}' || echo mangler)"
+  export TAG_H4="$(git rev-parse -q --verify 'refs/tags/h4-script-v2^{commit}' || echo mangler)"
+  export SHA_PRE="$(shasum -a 256 "$PRE" | cut -d' ' -f1)" SHA_MAN="$(shasum -a 256 "$MAN" | cut -d' ' -f1)"
+  "$PY" - <<'PYEOF'
 import json, os
 e = os.environ
-ut = {"commit": e["SHA"], "git_status_porcelain_ved_start": [], "kommando": e["KMD"], "start_utc": e["START"], "slutt_utc": e["SLUTT"],
-      "returkode": int(e["RC"]), "resultatfil": e["NY"] or None, "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"],
+ut = {"del": e["DEL_NAVN"], "commit": e["SHA"], "git_status_porcelain_ved_start": [], "kommando": e["KMD"], "start_utc": e["START"], "slutt_utc": e["SLUTT"],
+      "returkode": int(e["RC"]), "resultatfil": e["RES"] or None, "nye_filer": [x for x in e["NYE"].split("\n") if x],
+      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"],
       "preregistrering": {"fil": e["PRE"], "sha256": e["SHA_PRE"]}, "manus": {"fil": e["MAN"], "sha256": e["SHA_MAN"]}}
 open(e["META"], "w", encoding="utf-8").write(json.dumps(ut, ensure_ascii=False, indent=2) + "\n")
 print(e["META"])
 PYEOF
-exit "$RC"
+  git add -A
+  git commit -q -m "Testdel $d: resultat og kjøringsmetadata (returkode $RC, start på ${SHA:0:7})"
+  git push -q "$REMOTE" HEAD
+  bash "$SPEIL"
+  if [ "$RC" -ne 0 ]; then echo "STOPP: $d feilet (returkode $RC); resultat og metafil er committet, pushet og speilet. Ingen neste del." >&2; exit "$RC"; fi
+done
diff --git a/tests/test_kjor_testdel.py b/tests/test_kjor_testdel.py
index 975a827..eae3447 100644
--- a/tests/test_kjor_testdel.py
+++ b/tests/test_kjor_testdel.py
@@ -1,80 +1,131 @@
-"""scripts/kjor_testdel.sh: kjører ikke på urent arbeidstre, og skriver kjoring_meta ved siden av resultatet (testdelene kjøres ikke her:
-kalibrering/kjor_h4.py er en stubb i et midlertidig repo)."""
+"""scripts/kjor_testdel.sh: kjører ikke på urent arbeidstre; skriver kjoring_meta ved siden av resultatet; committer, pusher og speiler etter HVER
+testdel før neste starter; stopper på feil og på endrede sporede filer. Testdelene kjøres ikke her: skriptene er stubber i et midlertidig repo
+med et lokalt bart repo som origin og en stubb for speil."""
 import json
+import os
 import pathlib
 import shutil
 import subprocess
 import sys
 
 REPO = pathlib.Path(__file__).resolve().parent.parent
-STUBB = '''import pathlib, sys
-pathlib.Path("kjort.txt").write_text(" ".join(sys.argv[1:]))
-pathlib.Path("docs/KLAR-EVAL-0009_stubb_v1.0_2026-10-27.json").write_text("{}")
-sys.exit(int(__import__("os").environ.get("STUBB_RC", "0")))
+STUBB = '''import os, pathlib, sys
+navn = pathlib.Path(sys.argv[0]).stem
+with open("kjort.log", "a") as f:
+    f.write(navn + " " + " ".join(sys.argv[1:]) + "\\n")
+if os.environ.get("STUBB_OVERSKRIV") == navn:
+    pathlib.Path("docs/sporet.md").write_text("endret av kjøringen")
+pathlib.Path("docs/KLAR-EVAL-" + navn + "_v1.0_2026-10-27.json").write_text("{}")
+sys.exit(3 if os.environ.get("STUBB_FEIL") == navn else 0)
 '''
+SKRIPT = ["eval/dev/kjor_dev.py", "eval/dev/kjor_flaggoverlevelse_ord.py", "eval/dev/kjor_personvern_dev.py", "kalibrering/kjor_h4.py"]
 
 
 def git(r, *a):
-    return subprocess.run(["git", *a], cwd=r, check=True, capture_output=True, text=True).stdout.strip()
+    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=r, check=True, capture_output=True, text=True).stdout.strip()
 
 
 def lag_repo(tmp_path):
     r = tmp_path / "repo"
-    (r / "scripts").mkdir(parents=True)
-    (r / "docs").mkdir()
-    (r / "kalibrering").mkdir()
+    for d in ("scripts", "docs", "kalibrering", "eval/dev"):
+        (r / d).mkdir(parents=True)
     shutil.copy(REPO / "scripts" / "kjor_testdel.sh", r / "scripts")
-    (r / "kalibrering" / "kjor_h4.py").write_text(STUBB)
+    for s in SKRIPT:
+        (r / s).write_text(STUBB)
+    (r / "scripts" / "speil_stubb.sh").write_text('echo "speil $(git rev-parse --short HEAD) $(git status --porcelain | wc -l | tr -d " ")" >> "$(dirname "$0")/../speil.log"\n')
+    (r / ".gitignore").write_text("kjort.log\nspeil.log\n")
     (r / "kalibrering" / "KLAR-MANUS-0002_stubb_v1.2_2026-10-26.tsv").write_text("x\n")
     (r / "docs" / "KLAR-PREREG-0001_stubb_v1.9_2026-10-27.md").write_text("a\n")
     (r / "docs" / "KLAR-PREREG-0001_stubb_v1.10_2026-10-27.md").write_text("b\n")
+    (r / "docs" / "sporet.md").write_text("opprinnelig")
     git(r, "init", "-q", "-b", "main")
-    git(r, "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A")
-    git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "x")
+    git(r, "add", "-A")
+    git(r, "commit", "-q", "-m", "x")
     git(r, "tag", "prereg-v1")
     git(r, "tag", "h4-script-v2")
-    return r
+    bart = tmp_path / "origin.git"
+    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(bart)], check=True)
+    git(r, "remote", "add", "origin", str(bart))
+    return r, bart
 
 
-def kjor(r, *args, rc="0"):
-    import os
+def kjor(r, *args, **env):
     return subprocess.run(["bash", "scripts/kjor_testdel.sh", *args], cwd=r, capture_output=True, text=True,
-                          env={**os.environ, "KLAR_PY": sys.executable, "STUBB_RC": rc})
+                          env={**os.environ, "KLAR_PY": sys.executable, "KLAR_SPEIL": "scripts/speil_stubb.sh", **env})
+
+
+def kjort(r):
+    f = r / "kjort.log"
+    return f.read_text().splitlines() if f.exists() else []
 
 
 def test_urent_arbeidstre_kjorer_ikke(tmp_path):
-    r = lag_repo(tmp_path)
+    r, _ = lag_repo(tmp_path)
     (r / "uspor.txt").write_text("x")
-    p = kjor(r, "--prereg-id", "KLAR-PREREG-0001")
+    p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
     assert p.returncode == 1 and "uspor.txt" in p.stderr
-    assert not (r / "kjort.txt").exists() and not list((r / "docs").glob("*kjoring_meta*"))
+    assert kjort(r) == [] and not list((r / "docs").glob("*kjoring_meta*"))
     (r / "uspor.txt").unlink()
-    (r / "kalibrering" / "KLAR-MANUS-0002_stubb_v1.2_2026-10-26.tsv").write_text("endret\n")  # sporet fil endret
-    assert kjor(r, "--prereg-id", "KLAR-PREREG-0001").returncode == 1 and not (r / "kjort.txt").exists()
+    (r / "docs" / "sporet.md").write_text("endret")  # sporet fil endret
+    assert kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001").returncode == 1 and kjort(r) == []
 
 
 def test_tor_kjorer_ikke_og_skriver_ingenting(tmp_path):
-    r = lag_repo(tmp_path)
-    p = kjor(r, "--tor", "--prereg-id", "KLAR-PREREG-0001")
-    assert p.returncode == 0 and "ville kjørt" in p.stdout
-    assert not (r / "kjort.txt").exists() and git(r, "status", "--porcelain") == ""
+    r, _ = lag_repo(tmp_path)
+    p = kjor(r, "--tor", "alle", "--prereg-id", "KLAR-PREREG-0001")
+    assert p.returncode == 0 and p.stdout.count("ville kjørt") == 4 and "--mal-person 300 --mal-sted 200 --maks-timer 4" in p.stdout
+    assert kjort(r) == [] and git(r, "status", "--porcelain") == ""
+
+
+def test_en_del_committer_pusher_og_speiler_med_meta_ved_siden_av_resultatet(tmp_path):
+    r, bart = lag_repo(tmp_path)
+    start = git(r, "rev-parse", "HEAD")
+    p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
+    assert p.returncode == 0, p.stderr
+    assert kjort(r) == ["h4 --prereg-id KLAR-PREREG-0001".replace("h4", "kjor_h4")]
+    d = json.loads((r / "docs" / "KLAR-EVAL-kjor_h4_v1.0_2026-10-27_kjoring_meta.json").read_text())
+    assert d["commit"] == start and d["git_status_porcelain_ved_start"] == [] and d["returkode"] == 0 and d["del"] == "H4"
+    assert d["tag_prereg_v1"] == start == d["tag_h4_script_v2"] and d["preregistrering"]["fil"].endswith("_v1.10_2026-10-27.md")  # versjonssortering
+    assert d["resultatfil"] == "docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27.json"
+    assert git(r, "status", "--porcelain") == "" and git(r, "rev-parse", "HEAD") != start
+    assert git(bart, "rev-parse", "main") == git(r, "rev-parse", "HEAD")  # pushet
+    assert (r / "speil.log").read_text().splitlines() == [f"speil {git(r, 'rev-parse', '--short', 'HEAD')} 0"]  # speilet etter commit, rent tre
+    assert set(git(r, "show", "--name-only", "--format=", "HEAD").split()) == {"docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27.json", "docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27_kjoring_meta.json"}
 
 
-def test_rent_tre_skriver_meta_ved_siden_av_resultatet(tmp_path):
-    r = lag_repo(tmp_path)
-    p = kjor(r, "--prereg-id", "KLAR-PREREG-0001")
+def test_to_kjoringer_etter_hverandre_hver_med_egen_commit_push_og_speil(tmp_path):
+    r, bart = lag_repo(tmp_path)
+    start = git(r, "rev-parse", "HEAD")
+    p = kjor(r, "alle", "--prereg-id", "KLAR-PREREG-0001")
     assert p.returncode == 0, p.stderr
-    assert (r / "kjort.txt").read_text() == "--prereg-id KLAR-PREREG-0001"
-    meta = r / "docs" / "KLAR-EVAL-0009_stubb_v1.0_2026-10-27_kjoring_meta.json"
-    d = json.loads(meta.read_text())
-    assert d["commit"] == git(r, "rev-parse", "HEAD") and d["git_status_porcelain_ved_start"] == [] and d["returkode"] == 0
-    assert d["tag_prereg_v1"] == d["commit"] == d["tag_h4_script_v2"]
-    assert d["preregistrering"]["fil"].endswith("_v1.10_2026-10-27.md")  # versjonssortering
-    assert d["resultatfil"] == "docs/KLAR-EVAL-0009_stubb_v1.0_2026-10-27.json"
-
-
-def test_returkode_fra_kjoringen_bevares(tmp_path):
-    r = lag_repo(tmp_path)
-    p = kjor(r, "--prereg-id", "KLAR-PREREG-0001", rc="3")
-    assert p.returncode == 3
-    assert json.loads(next((r / "docs").glob("*kjoring_meta.json")).read_text())["returkode"] == 3
+    assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord", "kjor_personvern_dev", "kjor_h4"]
+    assert "--datasett npsc --splitt test --prereg-id KLAR-PREREG-0001 --mal-person 300 --mal-sted 200 --maks-timer 4" in kjort(r)[1]
+    log = git(r, "log", "--format=%H %s", f"{start}..HEAD").splitlines()[::-1]
+    assert [l.split(" ", 1)[1][:10] for l in log] == [f"Testdel H{i}" for i in (1, 2, 3, 4)]
+    metas = [json.loads(p_.read_text()) for p_ in sorted((r / "docs").glob("*kjoring_meta.json"))]
+    shas = {m["del"]: m["commit"] for m in metas}
+    hashes = [l.split()[0] for l in log]
+    assert [shas[f"H{i}"] for i in (1, 2, 3, 4)] == [start] + hashes[:3]  # hver del startet på forrige dels commit
+    assert all(m["git_status_porcelain_ved_start"] == [] for m in metas)
+    assert git(bart, "rev-parse", "main") == hashes[-1]
+    assert [l.split()[1] for l in (r / "speil.log").read_text().splitlines()] == [git(r, "rev-parse", "--short", h) for h in hashes]  # speil etter hver commit
+    assert all(l.endswith(" 0") for l in (r / "speil.log").read_text().splitlines())
+
+
+def test_feil_i_en_del_committer_den_og_stopper(tmp_path):
+    r, bart = lag_repo(tmp_path)
+    p = kjor(r, "alle", "--prereg-id", "KLAR-PREREG-0001", STUBB_FEIL="kjor_flaggoverlevelse_ord")
+    assert p.returncode == 3 and "H2 feilet" in p.stderr
+    assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord"]  # H3 og H4 startet ikke
+    m = json.loads(next((r / "docs").glob("*flaggoverlevelse_ord*kjoring_meta.json")).read_text())
+    assert m["returkode"] == 3 and git(r, "status", "--porcelain") == "" and git(bart, "rev-parse", "main") == git(r, "rev-parse", "HEAD")
+
+
+def test_endret_sporet_fil_gir_ingen_commit_og_stopper(tmp_path):
+    r, bart = lag_repo(tmp_path)
+    start = git(r, "rev-parse", "HEAD")
+    p = kjor(r, "H1", "--prereg-id", "KLAR-PREREG-0001", STUBB_OVERSKRIV="kjor_dev")
+    assert p.returncode == 4 and "endret sporede filer" in p.stderr
+    assert git(r, "rev-parse", "HEAD") == start and (r / "docs" / "sporet.md").read_text() == "endret av kjøringen"  # ingenting tilbakestilt
+    assert subprocess.run(["git", "rev-parse", "-q", "--verify", "main"], cwd=bart, capture_output=True).returncode != 0  # ingenting pushet
+    assert not (r / "speil.log").exists()
```

**Etter registrering, før testdata (KLAR-PREREG-0001 v1.13, punkt 4–8; alle avvik som tabell i KLAR-LOG-0003).** Samme tekst som i PREREG «Avvik etter registrering»:

4. **H1-utvalget (kode): `--per-dialekt` i `eval/dev/kjor_dev.py`.** PREREG (Study design, ordrett): «Utvalg: opptil 60 segmenter per dialektområde (e, n, sw, t, w), trukket med seed 20261026; har et område færre kvalifiserte segmenter, tas alle. Antall per område rapporteres.» og (Sample size): «H1: opptil 300 segmenter.» `kjor_dev.py` trakk fast 12 per område (`PER_DIALEKT = 12`, 60 segmenter). Nå finnes parameteren `--per-dialekt` (standard 12, altså uendret DEV-utvalg), og trekket er `rng.sample(pool, min(PER_DIALEKT, len(pool)))`: har et område færre kvalifiserte segmenter enn N, tas alle (som PREREG sier; før ga det en feil); for pooler som er store nok er trekket identisk med før (testet mot den gamle logikken ordrett). Utvalgslogikken (filter, sortering, seed) og WER-beregningen er ikke endret. Testdelen H1 kjøres med `--per-dialekt 60`, verdien PREREG oppgir.
5. **Navn på testresultater (kode): `--ut-mappe`, `--etikett`, `--eval-nr` i H1–H3-skriptene** (`kjor_dev.py`, `kjor_flaggoverlevelse_ord.py`, `kjor_personvern_dev.py`). Standardverdiene (`eval/dev` eller `docs`, `DEV`, ingen `--eval-nr`) gir nøyaktig dagens DEV-filnavn, merknader og overskrifter. Med `--etikett TEST` er merknaden og overskriften «TEST – preregistrert (OSF hc83q)». Nye EVAL-numre fra nummerregisteret (ARK-0003 v1.12): **KLAR-EVAL-0013** (H1, NB Samtale), **KLAR-EVAL-0014** (H2, NPSC), **KLAR-EVAL-0015** (H3, NorNE), filer under `eval/test/`; H4 bruker det reserverte **KLAR-EVAL-0009** (`kjor_h4.py` er ikke endret og skriver til `docs/`). `scripts/kjor_testdel.sh` sender disse parametrene.
6. **Bevis for at utregningen er uendret (`scripts/verifiser_uendret.py`):** DEV-skriptene kjørt med standardverdier, uten Whisper (lagrede hypoteser), og sammenlignet eksakt (floats bit for bit) med de committede resultatene. Resultat:

   | EVAL | sammenlignet med | identiske tall | enheter | første avvik |
   |---|---|---|---|---|
   | KLAR-EVAL-0002 v1.1 (WER NB Samtale, utvalg, hypoteser) | `eval/dev/kjor_dev.py` med standardverdier, Whisper byttet med lagrede hypoteser (samme segmentering, trekk og WER-kode) | **JA** | 60 segmenter | – |
   | KLAR-EVAL-0006 v1.2 (flaggoverlevelse NB Samtale) | `kjor_flaggoverlevelse_ord.py --datasett nbsamtale --fase evaluer` på lagrede hypoteser (reproduksjon 27.10) | **JA** | 60 segmenter | – |
   | KLAR-EVAL-0007 v1.1 (flaggoverlevelse NPSC) | `kjor_flaggoverlevelse_ord.py --datasett npsc --fase evaluer` på lagrede hypoteser | **JA** | 934 segmenter | – |
   | KLAR-EVAL-0005 (NorNE, recall og presisjon) | `kjor_personvern_dev.py` med standardverdier (full kjøring, ingen Whisper; kjøretid unntatt) | **JA** | 24 resultatnøkler | – |


   Nye filer (ingen analysekode): 
   - `scripts/verifiser_uendret.py` (sha256 `24d9ae67bb7fed9126703a4f2c9dc0446a9ee6470376e3cebeea8c0bd524d7c9`, 140 linjer)
   - `scripts/rapporter_intervaller.py` (sha256 `971c105dabf496f090011fface7ba44e2ad2c7cd47e35f6928b4a62a5d3b70d2`, 156 linjer)
   - `tests/test_dev_parametre.py` (sha256 `e57e6abd464a586fe2c7df5f27f5ac93e0534c4974c4ef87a55213105c7efda1`, 81 linjer)
   Diff (ordrett) mot commit `7ea3004` for analysekoden og wrapperen (`git diff HEAD -- eval/dev/kjor_dev.py eval/dev/kjor_flaggoverlevelse_ord.py eval/dev/kjor_personvern_dev.py scripts/kjor_testdel.sh tests/test_kjor_testdel.py`):

```diff
diff --git a/eval/dev/kjor_dev.py b/eval/dev/kjor_dev.py
index ada86e5..a2d6371 100644
--- a/eval/dev/kjor_dev.py
+++ b/eval/dev/kjor_dev.py
@@ -38,7 +38,11 @@ DATA = pathlib.Path(os.environ.get("ARKIVKLARERING_EVALDATA", "/Volumes/Vault/ar
 SPLITT = "validation"  # settes av --splitt; test-delen er sperret (arkivklarering/evaldata.py)
 PREREG_ID = None
 SEED = 20261026
-PER_DIALEKT = 12
+PER_DIALEKT = 12  # settes av --per-dialekt (standard 12 = DEV-utvalget)
+UT_MAPPE = None  # settes av --ut-mappe (standard: denne mappen)
+ETIKETT = "DEV"  # settes av --etikett (DEV eller TEST)
+EVAL_NR = None  # settes av --eval-nr (standard: KLAR-EVAL-0002 og -0003, dagens DEV-filnavn)
+ETIKETT_TEST = "TEST – preregistrert (OSF hc83q)"
 DIALEKTER = ["e", "n", "sw", "t", "w"]
 DATO = datetime.date.today().isoformat()
 SPRAK_FRA_SKRIFTFORM = {"bm": "no", "nn": "nn"}
@@ -52,7 +56,7 @@ def trekk_utvalg():
     valg = []
     for d in DIALEKTER:
         pool = sorted((r for r in kandidater if r["dialect"] == d), key=lambda r: (r["source_file_id"], r["segment_id"]))
-        valg += rng.sample(pool, PER_DIALEKT)
+        valg += rng.sample(pool, min(PER_DIALEKT, len(pool)))  # har et område færre kvalifiserte, tas alle (PREREG, Study design); gir samme trekk som før når poolen er stor nok
     return valg, len(kandidater)
 
 
@@ -87,15 +91,27 @@ def main():
     ap.add_argument("--splitt", default="validation", choices=evaldata.SPLITT,
                     help="datasettdel (standard: validation). test krever --prereg-id")
     ap.add_argument("--prereg-id", help="KLAR-PREREG-<NNNN>; kreves for --splitt test")
+    ap.add_argument("--per-dialekt", type=int, default=12, help="segmenter per dialektområde (standard 12 = DEV-utvalget; PREREG H1: 60)")
+    ap.add_argument("--ut-mappe", default=str(HER), help="mappe for utdata (standard: eval/dev)")
+    ap.add_argument("--etikett", default="DEV", choices=["DEV", "TEST"], help="DEV (standard) eller TEST (overskrift «TEST – preregistrert (OSF hc83q)»)")
+    ap.add_argument("--eval-nr", help="KLAR-EVAL-<NNNN> for utdatafilene (standard: -0002 for resultatet og -0003 for utvalget, som i DEV)")
     a = ap.parse_args()
-    global SPLITT, PREREG_ID
-    SPLITT, PREREG_ID = a.splitt, a.prereg_id
+    global SPLITT, PREREG_ID, PER_DIALEKT, UT_MAPPE, ETIKETT, EVAL_NR
+    SPLITT, PREREG_ID, PER_DIALEKT, UT_MAPPE, ETIKETT, EVAL_NR = a.splitt, a.prereg_id, a.per_dialekt, pathlib.Path(a.ut_mappe), a.etikett, a.eval_nr
     evaldata.sjekk_splitt(SPLITT, PREREG_ID)  # hard sperre før noe leses
 
     valg, n_kand = trekk_utvalg()
-    utvalg_sti = HER / f"KLAR-EVAL-0003_arkivklarering_dev-utvalg_v1.0_{DATO}.json"
+    UT_MAPPE.mkdir(parents=True, exist_ok=True)
+    if ETIKETT == "DEV" and EVAL_NR is None:
+        utvalg_sti = UT_MAPPE / f"KLAR-EVAL-0003_arkivklarering_dev-utvalg_v1.0_{DATO}.json"
+        stamme = UT_MAPPE / f"KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_{DATO}"
+    else:
+        nr = EVAL_NR or "KLAR-EVAL-0002"
+        utvalg_sti = UT_MAPPE / f"{nr}_arkivklarering_{ETIKETT.lower()}-nbsamtale-wer_v1.0_{DATO}.utvalg.json"
+        stamme = UT_MAPPE / f"{nr}_arkivklarering_{ETIKETT.lower()}-nbsamtale-wer_v1.0_{DATO}"
+    merknad = "DEV, ikke pilot" if ETIKETT == "DEV" else ETIKETT_TEST
     utvalg_sti.write_text(json.dumps({
-        "merknad": f"DEV, ikke pilot. Lagdelt utvalg fra Sprakbanken/nb_samtale ({SPLITT}), fast seed.",
+        "merknad": f"DEV, ikke pilot. Lagdelt utvalg fra Sprakbanken/nb_samtale ({SPLITT}), fast seed." if ETIKETT == "DEV" else f"{ETIKETT_TEST}. Lagdelt utvalg fra Sprakbanken/nb_samtale ({SPLITT}), fast seed.",
         "datasett_revisjon": "1c7028101858b854d3d568761778d8f63bb7e33f", "splitt": SPLITT,
         "seed": SEED, "per_dialekt": PER_DIALEKT,
         "filter": "ingen overlapp mot forrige/neste, 2–12 s, minst 3 ord i fasiten",
@@ -173,15 +189,22 @@ def main():
             tabell[kol][grp] = None if w is None else round(w, 4)
             tabell[kol][grp + "_n"] = len(par)
     modeller = {lag: {"modell": pathlib.Path(o.modell).name, "sha256": o.sha256} for lag, o in oppsett.items()}
-    (HER / f"KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_{DATO}.json").write_text(json.dumps(
-        {"merknad": "DEV, ikke pilot", "seed": SEED, "modeller": modeller, "wer": tabell,
+    pathlib.Path(str(stamme) + ".json").write_text(json.dumps(
+        {"merknad": merknad, "seed": SEED, "modeller": modeller, "wer": tabell,
          "segmenter": per_segment}, ensure_ascii=False, indent=2), encoding="utf-8")
 
     kols = list(tabell)
-    md = [f"# DEV-måling ({DATO}): WER på nb_samtale ({SPLITT}), 60 segmenter", "",
-          "**DEV, ikke pilot. Ingen konklusjoner om pilotkvalitet.** 12 segmenter per dialektområde "
-          f"(e, n, sw, t, w), seed {SEED}. Fasit: `orthographic`. Korpus-WER etter normalisering (små bokstaver, "
-          "tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.", "",
+    if ETIKETT == "DEV":
+        topp = [f"# DEV-måling ({DATO}): WER på nb_samtale ({SPLITT}), 60 segmenter", "",
+                "**DEV, ikke pilot. Ingen konklusjoner om pilotkvalitet.** 12 segmenter per dialektområde "
+                f"(e, n, sw, t, w), seed {SEED}. Fasit: `orthographic`. Korpus-WER etter normalisering (små bokstaver, "
+                "tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.", ""]
+    else:
+        topp = [f"# {ETIKETT_TEST} ({DATO}): WER på nb_samtale ({SPLITT}), {len(valg)} segmenter", "",
+                f"**{ETIKETT_TEST}.** Opptil {PER_DIALEKT} segmenter per dialektområde (e, n, sw, t, w), seed {SEED}; har et område færre kvalifiserte segmenter, tas alle. "
+                "Antall per område: " + ", ".join(f"{d} {sum(1 for r in valg if r['dialect'] == d)}" for d in DIALEKTER) + ". Fasit: `orthographic`. "
+                "Korpus-WER etter normalisering (små bokstaver, tegnsetting fjernet). Lisens: CC0, se KLAR-EVAL-0004.", ""]
+    md = [*topp,
           "`ra` = NB-Whisper large verbatim, `normalisert` = NB-Whisper large (ikke verbatim). "
           "`nn` = `-l nn` for alle; `matchet` = språk etter fasitens skriftform. "
           "Rålaget skriver ut nøling og omtrent som sagt og scores likevel mot ortografisk fasit, så ra-tallene "
@@ -191,9 +214,9 @@ def main():
         n = tabell[kols[0]][grp + "_n"]
         md.append(f"| {grp} ({n}) | " + " | ".join("–" if tabell[k][grp] is None else f"{tabell[k][grp]:.3f}" for k in kols) + " |")
     ingen = {k: sum(1 for s in per_segment if not s["hyp"][k].strip()) for k in kols}
-    md += ["", "Segmenter uten noen tekst (tom hypotese), av 60: " + ", ".join(f"{k}: {v}" for k, v in ingen.items()), "",
+    md += ["", f"Segmenter uten noen tekst (tom hypotese), av {len(per_segment)}: " + ", ".join(f"{k}: {v}" for k, v in ingen.items()), "",
            "Modeller: " + "; ".join(f"{l}: `{m['modell']}` sha256 `{m['sha256']}`" for l, m in modeller.items())]
-    (HER / f"KLAR-EVAL-0002_arkivklarering_dev-nbsamtale-wer_v1.0_{DATO}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
+    pathlib.Path(str(stamme) + ".md").write_text("\n".join(md) + "\n", encoding="utf-8")
     print("\n".join(md))
 
 
diff --git a/eval/dev/kjor_flaggoverlevelse_ord.py b/eval/dev/kjor_flaggoverlevelse_ord.py
index 87f07f0..7f64789 100644
--- a/eval/dev/kjor_flaggoverlevelse_ord.py
+++ b/eval/dev/kjor_flaggoverlevelse_ord.py
@@ -217,6 +217,9 @@ def main():
     ap.add_argument("--maks-timer", type=float, default=2.0)
     ap.add_argument("--mal-person", type=int, default=150)
     ap.add_argument("--mal-sted", type=int, default=100)
+    ap.add_argument("--ut-mappe", default=str(REPO / "docs"), help="mappe for resultatfila (standard: docs)")
+    ap.add_argument("--etikett", default="DEV", choices=["DEV", "TEST"], help="DEV (standard) eller TEST («TEST – preregistrert (OSF hc83q)» i merknaden)")
+    ap.add_argument("--eval-nr", help="KLAR-EVAL-<NNNN> for resultatfila (standard: -0006 for nbsamtale og -0007 for npsc, som i DEV)")
     a = ap.parse_args()
     evaldata.sjekk_splitt(a.splitt, a.prereg_id)  # hard sperre før noe leses
     if a.datasett == "nbsamtale" and a.splitt != "validation":
@@ -263,17 +266,21 @@ def main():
     if a.fase in ("evaluer", "alle"):
         motor = personvern.lag_motor()
         res = evaluer(items, cache, motor)
-        meta = {"merknad": "DEV, ikke pilot", "datasett": a.datasett, "splitt": a.splitt, "seed": a.seed,
+        meta = {"merknad": "DEV, ikke pilot" if a.etikett == "DEV" else "TEST – preregistrert (OSF hc83q)", "datasett": a.datasett, "splitt": a.splitt, "seed": a.seed,
                 "lyd_sek": round(sum(i["varighet"] for i in items if i["id"] in cache)), "segmenter": len([i for i in items if i["id"] in cache]),
                 "ikke_malt": IKKE_MALT, "ordtider": "DTW (-nfa -dtw large.v3), paring på ordspenn med toleranse "
                 + f"{personvern.TIDSTOLERANSE_S} s", "resultat": res}
         if a.datasett == "npsc" and prefiks_sti.exists():
             meta["prefiks"] = json.loads(prefiks_sti.read_text(encoding="utf-8"))
+        ut_mappe = pathlib.Path(a.ut_mappe)
+        ut_mappe.mkdir(parents=True, exist_ok=True)
         if a.datasett == "nbsamtale":
-            sti = REPO / "docs" / f"KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.1_{DATO}.json"
+            sti = ut_mappe / f"KLAR-EVAL-0006_arkivklarering_flaggoverlevelse-dev_v1.1_{DATO}.json"
         else:
             meta["segment_ider"] = [i["id"] for i in items if i["id"] in cache]
-            sti = REPO / "docs" / f"KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_{DATO}.json"
+            sti = ut_mappe / f"KLAR-EVAL-0007_arkivklarering_flaggoverlevelse-npsc-dev_v1.0_{DATO}.json"
+        if a.etikett == "TEST" or a.eval_nr:
+            sti = ut_mappe / f"{a.eval_nr or sti.name.split('_')[0]}_arkivklarering_{a.etikett.lower()}-flaggoverlevelse-{a.datasett}_v1.0_{DATO}.json"
         sti.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
         logg(sti)
 
diff --git a/eval/dev/kjor_personvern_dev.py b/eval/dev/kjor_personvern_dev.py
index d3b8105..bed5106 100644
--- a/eval/dev/kjor_personvern_dev.py
+++ b/eval/dev/kjor_personvern_dev.py
@@ -113,6 +113,9 @@ def main():
     ap = argparse.ArgumentParser()
     ap.add_argument("--splitt", default="validation", choices=evaldata.SPLITT)
     ap.add_argument("--prereg-id")
+    ap.add_argument("--ut-mappe", default=str(HER.parent.parent / "docs"), help="mappe for resultatfila (standard: docs)")
+    ap.add_argument("--etikett", default="DEV", choices=["DEV", "TEST"], help="DEV (standard) eller TEST («TEST – preregistrert (OSF hc83q)» i merknaden)")
+    ap.add_argument("--eval-nr", help="KLAR-EVAL-<NNNN> for resultatfila (standard: KLAR-EVAL-0005, som i DEV)")
     ap.add_argument("--maks", type=int, default=0, help="bare de første N setningene per målform (røyktest)")
     a = ap.parse_args()
     evaldata.sjekk_splitt(a.splitt, a.prereg_id)
@@ -178,11 +181,16 @@ def main():
             "recall_overlapp": r(c["gull_overlapp"], c["gull"]), "recall_overlapp_ki95": [lo, hi],
             "recall_noyaktig": r(c["gull_noyaktig"], c["gull"]),
             "presisjon_overlapp": r(c["pred_overlapp"], c["pred"]), "presisjon_noyaktig": r(c["pred_noyaktig"], c["pred"])}
-    ut = {"merknad": "DEV, ikke pilot", "datasett": "NbAiLab/norne", "revisjon": REVISJON, "splitt": a.splitt,
+    ut = {"merknad": "DEV, ikke pilot" if a.etikett == "DEV" else "TEST – preregistrert (OSF hc83q)", "datasett": "NbAiLab/norne", "revisjon": REVISJON, "splitt": a.splitt,
           "motor": {"spacy": personvern.SPACY_MODELL, "bert": personvern.BERT_MODELL, "terskel": 0.0},
           "setninger_hoppet_over_pga_tokenjustering": {f"{k[0]}|{k[1]}": v for k, v in hoppet.items()},
           "resultat": resultat, "sekunder": round(time.time() - t0)}
-    sti = HER.parent.parent / "docs" / f"KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_{DATO}.json"
+    ut_mappe = pathlib.Path(a.ut_mappe)
+    ut_mappe.mkdir(parents=True, exist_ok=True)
+    if a.etikett == "DEV" and not a.eval_nr:
+        sti = ut_mappe / f"KLAR-EVAL-0005_arkivklarering_personvern-dev_v1.0_{DATO}.json"
+    else:
+        sti = ut_mappe / f"{a.eval_nr or 'KLAR-EVAL-0005'}_arkivklarering_personvern-{a.etikett.lower()}_v1.0_{DATO}.json"
     sti.write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
     print(sti, flush=True)
 
diff --git a/scripts/kjor_testdel.sh b/scripts/kjor_testdel.sh
index 2ad2d3a..79e6620 100755
--- a/scripts/kjor_testdel.sh
+++ b/scripts/kjor_testdel.sh
@@ -5,10 +5,11 @@
 #
 #   source scripts/miljo.sh && scripts/kjor_testdel.sh [--tor] <H1|H2|H3|H4|alle> --prereg-id KLAR-PREREG-0001 [-- ekstra argumenter]
 #
-#   H1  eval/dev/kjor_dev.py --splitt test                                              (NB Samtale test)
-#   H2  eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --mal-person 300 --mal-sted 200 --maks-timer 4   (PREREG: doble mål)
-#   H3  eval/dev/kjor_personvern_dev.py --splitt test                                   (NorNE test)
-#   H4  kalibrering/kjor_h4.py                                                          (menneskeinnlest testmanus)
+#   H1  eval/dev/kjor_dev.py --splitt test --per-dialekt 60 ... --eval-nr KLAR-EVAL-0013   (NB Samtale test; PREREG: opptil 60 per dialektområde)
+#   H2  eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --mal-person 300 --mal-sted 200 --maks-timer 4 ... --eval-nr KLAR-EVAL-0014   (PREREG: doble mål)
+#   H3  eval/dev/kjor_personvern_dev.py --splitt test ... --eval-nr KLAR-EVAL-0015      (NorNE test)
+#   H4  kalibrering/kjor_h4.py                                                          (menneskeinnlest testmanus; skriver docs/KLAR-EVAL-0009_..., reservert nummer)
+#   H1–H3 skriver til eval/test/ med --etikett TEST (merknad «TEST – preregistrert (OSF hc83q)»).
 #   alle = H1, H2, H3, H4 i den rekkefølgen (H4 til sist: opptakene må være innlest og scoret først, se PREREG).
 #
 # Før hver del: `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1). Etter hver del skrives
@@ -39,9 +40,9 @@ if [ "$DEL" = alle ]; then DELER=(H1 H2 H3 H4); else DELER=("$DEL"); fi
 
 kommando() {  # skriver skriptet og argumentene for en del, ett ord per linje
   case "$1" in
-    H1) printf '%s\n' eval/dev/kjor_dev.py --splitt test --prereg-id "$ID" ;;
-    H2) printf '%s\n' eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --prereg-id "$ID" --mal-person 300 --mal-sted 200 --maks-timer 4 ;;
-    H3) printf '%s\n' eval/dev/kjor_personvern_dev.py --splitt test --prereg-id "$ID" ;;
+    H1) printf '%s\n' eval/dev/kjor_dev.py --splitt test --prereg-id "$ID" --per-dialekt 60 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0013 ;;
+    H2) printf '%s\n' eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --prereg-id "$ID" --mal-person 300 --mal-sted 200 --maks-timer 4 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0014 ;;
+    H3) printf '%s\n' eval/dev/kjor_personvern_dev.py --splitt test --prereg-id "$ID" --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015 ;;
     H4) printf '%s\n' kalibrering/kjor_h4.py --prereg-id "$ID" ;;
   esac
 }
@@ -87,7 +88,7 @@ for d in "${DELER[@]}"; do
     exit 4
   fi
   NYE="$(git status --porcelain --untracked-files=all | sed 's/^?? //' | sort)"
-  RES="$(echo "$NYE" | grep -E '^(docs/KLAR-EVAL|eval/dev/KLAR-EVAL).*\.json$' | head -1 || true)"
+  RES="$(echo "$NYE" | grep -E '^(docs|eval/dev|eval/test)/KLAR-EVAL.*\.json$' | grep -v '\.utvalg\.json$' | head -1 || true)"
   [ -n "$RES" ] || RES="$(echo "$NYE" | grep -E '\.json$' | head -1 || true)"
   if [ -n "$RES" ]; then META="${RES%.json}_kjoring_meta.json"; else META="docs/kjoring_meta_${d}_$TID.json"; fi
   export META SHA START SLUTT RC KMD PRE MAN RES DEL_NAVN="$d" NYE
diff --git a/tests/test_kjor_testdel.py b/tests/test_kjor_testdel.py
index eae3447..f15dd47 100644
--- a/tests/test_kjor_testdel.py
+++ b/tests/test_kjor_testdel.py
@@ -99,7 +99,9 @@ def test_to_kjoringer_etter_hverandre_hver_med_egen_commit_push_og_speil(tmp_pat
     p = kjor(r, "alle", "--prereg-id", "KLAR-PREREG-0001")
     assert p.returncode == 0, p.stderr
     assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord", "kjor_personvern_dev", "kjor_h4"]
-    assert "--datasett npsc --splitt test --prereg-id KLAR-PREREG-0001 --mal-person 300 --mal-sted 200 --maks-timer 4" in kjort(r)[1]
+    assert "--datasett npsc --splitt test --prereg-id KLAR-PREREG-0001 --mal-person 300 --mal-sted 200 --maks-timer 4 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0014" in kjort(r)[1]
+    assert kjort(r)[0].endswith("--per-dialekt 60 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0013")
+    assert kjort(r)[2].endswith("--ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015") and kjort(r)[3].endswith("kjor_h4 --prereg-id KLAR-PREREG-0001")
     log = git(r, "log", "--format=%H %s", f"{start}..HEAD").splitlines()[::-1]
     assert [l.split(" ", 1)[1][:10] for l in log] == [f"Testdel H{i}" for i in (1, 2, 3, 4)]
     metas = [json.loads(p_.read_text()) for p_ in sorted((r / "docs").glob("*kjoring_meta.json"))]
```
7. **95 %-intervallmetoden (låst før noen testdel er åpnet).** PREREG (Statistical models & analysis plan, ordrett): «Beskrivende. Proporsjoner med Wilson-95 %-intervall (H2, H3, H4); korpus-WER med **clusterbootstrap** over taler (NB Samtale `speaker_id`; NPSC `speaker_id`), 2000 gjentak, seed 20261026; differansen i K1 med parret clusterbootstrap. NorNE: bootstrap over setninger.» Metoden er altså spesifisert (clusterbootstrap over taler, 2000 gjentak, seed 20261026, parret for K1; Wilson for proporsjoner), men **intervalltypen er ikke oppgitt**. Låst nå: **persentilintervall**, nedre grense = element `int(0,025·B)` og øvre = element `int(0,975·B) − 1` (0-indeksert) av de sorterte bootstrap-verdiene, B = 2000; per gjentak trekkes like mange talere som det finnes (med tilbakelegging), alle segmentene til de trukne talerne tas med, WER = sum av feil / sum av referanseord; samme trekk brukes for alle kolonner (parret). Verdiene B = 10 000 og «NorNE per dokument» er **ikke** brukt, fordi PREREG allerede fastsetter 2000 gjentak og setninger. Implementert i et eget rapportskript som leser resultat-JSON (`scripts/rapporter_intervaller.py`; analysekoden er ikke endret) og testet på DEV-resultatene (EVAL-0002 v1.1: totalt rålag/matchet 0,135, 95 %-intervall 0,095–0,171, 33 talere; K1-differanse 0,213, 0,149–0,282, utelukker 0). **Begrensning:** `kjor_personvern_dev.py` skriver bare aggregerte tellere, ikke tall per setning; bootstrap over setninger for NorNE (H3) er derfor ikke mulig fra resultat-JSON, og skriptet gir Wilson fra tellerne.
8. **H4-begrensning:** H4 måles med én leser, som er forfatter og kjenner målelementene. Resultatet gjelder bare én taler og kan ikke generaliseres. (PREREG nevner «Eirik og eventuelt andre lesere»; skal ikke flere lese inn, gjelder begrensningen alle H4-tall.) Skal stå i KLAR-EVAL-0009.

**Etter registrering, før testdata (KLAR-PREREG-0001 v1.14, punkt 9–11; AV-15 og AV-16 i KLAR-LOG-0003).** Samme tekst som i PREREG «Avvik etter registrering»:

9. **AV-15: tellere per setning fra `eval/dev/kjor_personvern_dev.py` (NorNE, H3).** Beslutning 2026-10-27: skriptet skriver i tillegg tellere per setning i en ny utdatafil (`<resultat>.setninger.json`: målform, radnummer, `idx`, variant, motor, type og de seks tellerne `gull`, `gull_overlapp`, `gull_noyaktig`, `pred`, `pred_overlapp`, `pred_noyaktig`). Den aggregerte utregningen er ikke endret: tellene i resultat-JSON summeres fra de samme seks tallene som skrives per setning (`d`), så de er summen av filene. Dette løser begrensningen i AV-13 (bootstrap over setninger for NorNE kunne ikke regnes fra resultat-JSON): `scripts/rapporter_intervaller.py norne <resultat> <setninger>` gir bootstrap over setninger (B = 2000, `numpy.random.default_rng(20261026)` i rekkefølgen av sorterte gruppenøkler, persentilregelen fra AV-13) ved siden av Wilson. **Bevis (`scripts/verifiser_uendret.py --bare 5`, full kjøring med standardverdier):** aggregatene er identiske med KLAR-EVAL-0005 (**JA**, 24 resultatnøkler, ingen avvik, kjøretid unntatt), og tellerne i de 51 600 setningsradene summerer til de aggregerte tellene og gir de samme recall- og presisjonsverdiene (kontrollen er lagt inn i verifiseringsskriptet). EVAL-0002 v1.1, -0006 v1.2 og -0007 v1.1 er ikke berørt av denne endringen (kontrollert identisk i punkt 6; `kjor_dev.py` og `kjor_flaggoverlevelse_ord.py` er ikke endret siden).
10. **AV-16: kodesjekk mot taggen `testkjoring-v1` i `scripts/kjor_testdel.sh`, og taggen.** Før hver testdel kontrollerer skriptet at koden er uendret siden taggen: `git diff --quiet testkjoring-v1 -- arkivklarering kalibrering tests scripts` og alle `.py`-filer under `eval/` (`':(glob)eval/**/*.py'`); endret kode eller manglende tagg gir exit 5 og ingenting kjøres. Kravet er ikke at HEAD er taggen, fordi resultat-commitene (`docs/`, `eval/test/`) er tillatt. Metafila får `tag_testkjoring_v1` og `kode_uendret_siden_testkjoring_v1`. Testet i `tests/test_kjor_testdel.py` (endring i hver kodemappe stopper; resultatfiler og ikke-`.py`-filer under `eval/` tillates; manglende tagg stopper; to testdeler etter hverandre, og endret kode mellom dem nekter den andre). **Tag `testkjoring-v1`** er satt på commit `871dba942a665fc7401261153b6c7e0114289ac9` (annotert tag-objekt `7ddd1fbe8abd936d5add9a39b95e79dc691ac592`) etter 140 grønne tester, og pushet. Den peker på all kode testdelene kjøres med, inkludert punkt 4–7 over og punkt 9 her. Kode endret etter taggen betyr at testdelene ikke kan startes uten at en ny tag (og avvik) føres først.
11. **Bekreftet av eier 2026-10-27, før testdata:** (a) 95 %-intervallene følger PREREG uendret: clusterbootstrap over taler (2000 gjentak, seed 20261026), NorNE over setninger, Wilson for proporsjoner, persentilintervall (punkt 7); ingen endring. (b) `min(N, len(pool))` i `kjor_dev.py` er godkjent som tolkning av PREREG: ordlyden er «Utvalg: opptil 60 segmenter per dialektområde (e, n, sw, t, w), trukket med seed 20261026; har et område færre kvalifiserte segmenter, tas alle. Antall per område rapporteres.», og «tas alle» er det `min` gjør. (c) H4 skriver til `docs/KLAR-EVAL-0009…` som før (`kjor_h4.py` er ikke endret).

   Diff (ordrett) for denne endringen (`git diff 871dba9~1 871dba9 -- eval/dev/kjor_personvern_dev.py scripts/kjor_testdel.sh`):

```diff
diff --git a/eval/dev/kjor_personvern_dev.py b/eval/dev/kjor_personvern_dev.py
index bed5106..54d838a 100644
--- a/eval/dev/kjor_personvern_dev.py
+++ b/eval/dev/kjor_personvern_dev.py
@@ -107,6 +107,9 @@ def wilson(k, n, z=1.96):
     return (round(c - h, 3), round(c + h, 3))
 
 
+TELLERE = ("gull", "gull_overlapp", "gull_noyaktig", "pred", "pred_overlapp", "pred_noyaktig")
+
+
 def main():
     from arkivklarering.miljo import krev_vault_miljo
     krev_vault_miljo()  # avbryter hvis miljøet ikke peker til Vault (source scripts/miljo.sh først)
@@ -134,11 +137,12 @@ def main():
 
     tell = collections.defaultdict(lambda: collections.Counter())
     hoppet = collections.Counter()
+    per_setning = []  # tellere per setning (egen utdatafil `.setninger.json`); de aggregerte tellene under er summen av disse
     for config, sprak in MALFORM.items():
         tab = pq.read_table(evaldata.norne_sti(DATA, config, a.splitt, a.prereg_id)).to_pylist()
         if a.maks:
             tab = tab[:a.maks]
-        for rad in tab:
+        for rad_nr, rad in enumerate(tab):
             tokens, tags = rad["tokens"], rad["ner_tags"]
             gull = gull_spenn(tokens, tags)
             for variant in ("original", "små"):
@@ -163,12 +167,13 @@ def main():
                         g = [x for x in gs if x[2] == typ]
                         pp = [x for x in pred if x[2] == typ]
                         c = tell[(sprak, typ, navn, variant)]
-                        c["gull"] += len(g)
-                        c["gull_overlapp"] += sum(any(overlapper(x, y) for y in pp) for x in g)
-                        c["gull_noyaktig"] += sum(any(x == y for y in pp) for x in g)
-                        c["pred"] += len(pp)
-                        c["pred_overlapp"] += sum(any(overlapper(x, y) for y in g) for x in pp)
-                        c["pred_noyaktig"] += sum(any(x == y for y in g) for x in pp)
+                        d = {"gull": len(g), "gull_overlapp": sum(any(overlapper(x, y) for y in pp) for x in g),
+                             "gull_noyaktig": sum(any(x == y for y in pp) for x in g), "pred": len(pp),
+                             "pred_overlapp": sum(any(overlapper(x, y) for y in g) for x in pp),
+                             "pred_noyaktig": sum(any(x == y for y in g) for x in pp)}
+                        for k, v in d.items():
+                            c[k] += v
+                        per_setning.append([config, rad_nr, str(rad.get("idx", "")), variant, navn, typ, *(d[k] for k in TELLERE)])
         print(f"{config}: {len(tab)} setninger, {time.time() - t0:.0f} s", flush=True)
 
     resultat = {}
@@ -193,6 +198,11 @@ def main():
         sti = ut_mappe / f"{a.eval_nr or 'KLAR-EVAL-0005'}_arkivklarering_personvern-{a.etikett.lower()}_v1.0_{DATO}.json"
     sti.write_text(json.dumps(ut, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
     print(sti, flush=True)
+    sti_s = sti.with_name(sti.stem + ".setninger.json")  # ikke et KLAR-dokument i nummerregisteret (navnet slutter ikke på .json rett etter datoen)
+    sti_s.write_text(json.dumps({"merknad": ut["merknad"], "splitt": a.splitt, "revisjon": REVISJON,
+                                 "kolonner": ["config", "rad", "idx", "variant", "motor", "type", *TELLERE], "rader": per_setning},
+                                ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
+    print(sti_s, flush=True)
 
 
 if __name__ == "__main__":
diff --git a/scripts/kjor_testdel.sh b/scripts/kjor_testdel.sh
index 79e6620..5e8cafd 100755
--- a/scripts/kjor_testdel.sh
+++ b/scripts/kjor_testdel.sh
@@ -12,7 +12,9 @@
 #   H1–H3 skriver til eval/test/ med --etikett TEST (merknad «TEST – preregistrert (OSF hc83q)»).
 #   alle = H1, H2, H3, H4 i den rekkefølgen (H4 til sist: opptakene må være innlest og scoret først, se PREREG).
 #
-# Før hver del: `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1). Etter hver del skrives
+# Før hver del: (1) `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1); (2) koden må være uendret siden
+# taggen `testkjoring-v1` (`git diff --quiet testkjoring-v1 -- arkivklarering kalibrering tests scripts` og alle .py-filer under eval/), ellers kjøres
+# ingenting (exit 5; mangler taggen, er det også exit 5). Kravet er IKKE at HEAD er taggen: resultat-commitene (docs/, eval/test/) er tillatt. Etter hver del skrives
 # <resultat>_kjoring_meta.json (commit-SHA ved start, tom porcelain, kommando, tider, returkode, resultatfiler, SHA-ene til taggene og sha256 for PREREG-
 # og MANUS-fila). Så: commit av resultat og metafil, push, speil. Stopper hele kjøringen (ingen neste del) hvis en del feiler, hvis en SPORET fil er
 # endret av kjøringen (da committes ingenting, exit 4; fjerner ikke noe), eller hvis commit, push eller speil feiler. Feilede deler committes (med
@@ -56,7 +58,21 @@ rent_eller_stopp() {
   fi
 }
 
+kode_uendret_eller_stopp() {
+  local TAGG="${KLAR_KODETAGG:-testkjoring-v1}"
+  if ! git rev-parse -q --verify "refs/tags/$TAGG^{commit}" >/dev/null; then
+    echo "FEIL: taggen $TAGG finnes ikke; kan ikke vise at koden er uendret. Kjører ikke." >&2
+    exit 5
+  fi
+  if ! git diff --quiet "$TAGG" -- arkivklarering kalibrering tests scripts ':(glob)eval/**/*.py'; then
+    echo "FEIL: koden er endret siden taggen $TAGG; kjører ikke. Endrede filer:" >&2
+    git diff --name-only "$TAGG" -- arkivklarering kalibrering tests scripts ':(glob)eval/**/*.py' >&2
+    exit 5
+  fi
+}
+
 rent_eller_stopp
+kode_uendret_eller_stopp
 if [ "$TOR" -eq 1 ]; then
   for d in "${DELER[@]}"; do
     K=(); while IFS= read -r l; do K+=("$l"); done < <(kommando "$d")
@@ -67,6 +83,7 @@ fi
 
 for d in "${DELER[@]}"; do
   rent_eller_stopp   # etter forrige dels commit skal treet være rent igjen
+  kode_uendret_eller_stopp   # og koden fortsatt som i taggen (bare resultat-commiter er kommet til)
   K=(); while IFS= read -r l; do K+=("$l"); done < <(kommando "$d")
   SHA="$(git rev-parse HEAD)"
   KMD="$PY ${K[*]} ${EKSTRA[*]:-}"
@@ -94,13 +111,14 @@ for d in "${DELER[@]}"; do
   export META SHA START SLUTT RC KMD PRE MAN RES DEL_NAVN="$d" NYE
   export TAG_PREREG="$(git rev-parse -q --verify 'refs/tags/prereg-v1^{commit}' || echo mangler)"
   export TAG_H4="$(git rev-parse -q --verify 'refs/tags/h4-script-v2^{commit}' || echo mangler)"
+  export TAG_KODE="$(git rev-parse -q --verify "refs/tags/${KLAR_KODETAGG:-testkjoring-v1}^{commit}" || echo mangler)"
   export SHA_PRE="$(shasum -a 256 "$PRE" | cut -d' ' -f1)" SHA_MAN="$(shasum -a 256 "$MAN" | cut -d' ' -f1)"
   "$PY" - <<'PYEOF'
 import json, os
 e = os.environ
 ut = {"del": e["DEL_NAVN"], "commit": e["SHA"], "git_status_porcelain_ved_start": [], "kommando": e["KMD"], "start_utc": e["START"], "slutt_utc": e["SLUTT"],
       "returkode": int(e["RC"]), "resultatfil": e["RES"] or None, "nye_filer": [x for x in e["NYE"].split("\n") if x],
-      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"],
+      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"], "tag_testkjoring_v1": e["TAG_KODE"], "kode_uendret_siden_testkjoring_v1": True,
       "preregistrering": {"fil": e["PRE"], "sha256": e["SHA_PRE"]}, "manus": {"fil": e["MAN"], "sha256": e["SHA_MAN"]}}
 open(e["META"], "w", encoding="utf-8").write(json.dumps(ut, ensure_ascii=False, indent=2) + "\n")
 print(e["META"])
```

**Innspillingsprotokoll for H4 (KLAR-ADR-0018) og `testkjoring-v2` (KLAR-PREREG-0001 v1.15, punkt 12–13; AV-17 og AV-18 i KLAR-LOG-0003).** Samme tekst som i PREREG «Avvik etter registrering». Veikart: `KLAR-ARK-0006` (v1.0-stegene med status og det som kommer etter).

12. **AV-17: Innspillingsprotokoll spesifisert før datainnsamling (ikke i PREREG).** PREREG beskriver H4 («Innlesing med norsk-tales rigg … Alle innleste opptak teller») men ingen protokoll for selve innlesingen. Den er spesifisert i `KLAR-ADR-0018` (status accepted) før noe opptak finnes: riggversjon låst til norsk-tale `bcfef63d1be49ac239956dfb67784c002cecf310` med sha256 for de seks riggfilene (kontrollert ved start); lagring KUN under `/Volumes/Vault/arkivklarering/lyd/h4/` (fast i koden), aldri i git eller sky, som 16 kHz mono wav i `<runde>/opptak/<manus-id>.wav`; leseinstruksen «Les i naturlig tempo og på din vanlige dialekt. Ikke legg ekstra trykk på navn, tall eller fremmedord.» vises i riggen og må bekreftes lest; ta om bare ved feillesing (feil ord, avbrudd, støy), aldri på grunn av maskinens resultat; ingen visning av transkripsjon, flagg eller poeng (resultatside og eksport finnes ikke i modusen); logg per opptak (id, tidspunkt, forsøk, grunn); rom og mikrofon noteres én gang per runde. Ingen forhåndsregistrert terskel, utvalg eller analyse er berørt. Kode: `arkivklarering/h4_innlesing.py`, `arkivklarering/h4_side.html`, `scripts/rigg_manus.py`; tester: `tests/test_h4_innlesing.py` (ruter og side uten resultat, Vault-sti, instruks, omtakslogg, rigglås, kompatibilitet med `kjor_h4.finn_opptak`). `scripts/rigg_manus.py` startet tidligere norsk-tales hele rigg med `lyd/menneske/`; den starter nå bare H4-modusen. `kalibrering/kjor_h4.py` er ikke endret: standardmappen i skriptet er fortsatt `lyd/menneske`, og `scripts/kjor_testdel.sh` sender `--opptak /Volumes/Vault/arkivklarering/lyd/h4`.
13. **AV-18: ny kodetagg `testkjoring-v2`.** Innleseren ligger i `arkivklarering/` og `scripts/`, som kodesjekken i `scripts/kjor_testdel.sh` omfatter, så `testkjoring-v1` kunne ikke lenger brukes. `testkjoring-v1` (commit `871dba942a665fc7401261153b6c7e0114289ac9`) er beholdt og ikke flyttet. `testkjoring-v2` er satt etter 147 grønne tester på commit `c49d17463c14f7719f9f271ae3d4af4824436c35` (annotert tag-objekt `c4a7a8e5c293b6f20c880ab38cf705010882de9c`) og pushet; wrapperen kontrollerer nå `testkjoring-v2` og skriver både `tag_testkjoring` og `tag_testkjoring_v1` i metafila. Ingen analysekode (`kalibrering/`, `eval/`, resten av `arkivklarering/`) er endret mellom taggene; endringene er bare:
```
 arkivklarering/h4_innlesing.py | 189 +++++++++++++++++++++++++++++
 arkivklarering/h4_side.html    | 268 +++++++++++++++++++++++++++++++++++++++++
 scripts/kjor_testdel.sh        |  14 ++-
 scripts/rigg_manus.py          |  54 +++++----
 tests/test_h4_innlesing.py     | 164 +++++++++++++++++++++++++
 tests/test_kjor_testdel.py     |  11 +-
 6 files changed, 665 insertions(+), 35 deletions(-)
```
   Nye filer (ingen eksisterende analysekode):
   - `arkivklarering/h4_innlesing.py` (sha256 `262a3c2c747939ae55dc56cb3d8061ab7ba9c3e94647190740f88de7a3d2add6`, 189 linjer)
   - `arkivklarering/h4_side.html` (sha256 `d0b21d36a1c512f09607b4f6cbe04b70a4c110333cdbff28c8fe04232685aa9b`, 268 linjer)
   - `tests/test_h4_innlesing.py` (sha256 `1b9c655297ba504becd05fcdd0b128be77bfbade07eb98cd3b461807976a07a5`, 164 linjer)
   Diff (ordrett) for de eksisterende filene (`git diff testkjoring-v1 testkjoring-v2 -- scripts/rigg_manus.py scripts/kjor_testdel.sh tests/test_kjor_testdel.py`):

```diff
diff --git a/scripts/kjor_testdel.sh b/scripts/kjor_testdel.sh
index 5e8cafd..f95289c 100755
--- a/scripts/kjor_testdel.sh
+++ b/scripts/kjor_testdel.sh
@@ -8,12 +8,12 @@
 #   H1  eval/dev/kjor_dev.py --splitt test --per-dialekt 60 ... --eval-nr KLAR-EVAL-0013   (NB Samtale test; PREREG: opptil 60 per dialektområde)
 #   H2  eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --mal-person 300 --mal-sted 200 --maks-timer 4 ... --eval-nr KLAR-EVAL-0014   (PREREG: doble mål)
 #   H3  eval/dev/kjor_personvern_dev.py --splitt test ... --eval-nr KLAR-EVAL-0015      (NorNE test)
-#   H4  kalibrering/kjor_h4.py                                                          (menneskeinnlest testmanus; skriver docs/KLAR-EVAL-0009_..., reservert nummer)
+#   H4  kalibrering/kjor_h4.py --opptak /Volumes/Vault/arkivklarering/lyd/h4          (menneskeinnlest testmanus, innlest med scripts/rigg_manus.py; skriver docs/KLAR-EVAL-0009_...)
 #   H1–H3 skriver til eval/test/ med --etikett TEST (merknad «TEST – preregistrert (OSF hc83q)»).
 #   alle = H1, H2, H3, H4 i den rekkefølgen (H4 til sist: opptakene må være innlest og scoret først, se PREREG).
 #
 # Før hver del: (1) `git status --porcelain` må være helt tom (også usporede filer), ellers kjøres ingenting (exit 1); (2) koden må være uendret siden
-# taggen `testkjoring-v1` (`git diff --quiet testkjoring-v1 -- arkivklarering kalibrering tests scripts` og alle .py-filer under eval/), ellers kjøres
+# taggen `testkjoring-v2` (`git diff --quiet testkjoring-v2 -- arkivklarering kalibrering tests scripts` og alle .py-filer under eval/), ellers kjøres
 # ingenting (exit 5; mangler taggen, er det også exit 5). Kravet er IKKE at HEAD er taggen: resultat-commitene (docs/, eval/test/) er tillatt. Etter hver del skrives
 # <resultat>_kjoring_meta.json (commit-SHA ved start, tom porcelain, kommando, tider, returkode, resultatfiler, SHA-ene til taggene og sha256 for PREREG-
 # og MANUS-fila). Så: commit av resultat og metafil, push, speil. Stopper hele kjøringen (ingen neste del) hvis en del feiler, hvis en SPORET fil er
@@ -45,7 +45,7 @@ kommando() {  # skriver skriptet og argumentene for en del, ett ord per linje
     H1) printf '%s\n' eval/dev/kjor_dev.py --splitt test --prereg-id "$ID" --per-dialekt 60 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0013 ;;
     H2) printf '%s\n' eval/dev/kjor_flaggoverlevelse_ord.py --datasett npsc --splitt test --prereg-id "$ID" --mal-person 300 --mal-sted 200 --maks-timer 4 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0014 ;;
     H3) printf '%s\n' eval/dev/kjor_personvern_dev.py --splitt test --prereg-id "$ID" --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015 ;;
-    H4) printf '%s\n' kalibrering/kjor_h4.py --prereg-id "$ID" ;;
+    H4) printf '%s\n' kalibrering/kjor_h4.py --prereg-id "$ID" --opptak /Volumes/Vault/arkivklarering/lyd/h4 ;;
   esac
 }
 
@@ -59,7 +59,7 @@ rent_eller_stopp() {
 }
 
 kode_uendret_eller_stopp() {
-  local TAGG="${KLAR_KODETAGG:-testkjoring-v1}"
+  local TAGG="${KLAR_KODETAGG:-testkjoring-v2}"
   if ! git rev-parse -q --verify "refs/tags/$TAGG^{commit}" >/dev/null; then
     echo "FEIL: taggen $TAGG finnes ikke; kan ikke vise at koden er uendret. Kjører ikke." >&2
     exit 5
@@ -111,14 +111,16 @@ for d in "${DELER[@]}"; do
   export META SHA START SLUTT RC KMD PRE MAN RES DEL_NAVN="$d" NYE
   export TAG_PREREG="$(git rev-parse -q --verify 'refs/tags/prereg-v1^{commit}' || echo mangler)"
   export TAG_H4="$(git rev-parse -q --verify 'refs/tags/h4-script-v2^{commit}' || echo mangler)"
-  export TAG_KODE="$(git rev-parse -q --verify "refs/tags/${KLAR_KODETAGG:-testkjoring-v1}^{commit}" || echo mangler)"
+  export TAG_KODE="$(git rev-parse -q --verify "refs/tags/${KLAR_KODETAGG:-testkjoring-v2}^{commit}" || echo mangler)"
+  export TAG_KODE_NAVN="${KLAR_KODETAGG:-testkjoring-v2}"
+  export TAG_KODE_V1="$(git rev-parse -q --verify 'refs/tags/testkjoring-v1^{commit}' || echo mangler)"
   export SHA_PRE="$(shasum -a 256 "$PRE" | cut -d' ' -f1)" SHA_MAN="$(shasum -a 256 "$MAN" | cut -d' ' -f1)"
   "$PY" - <<'PYEOF'
 import json, os
 e = os.environ
 ut = {"del": e["DEL_NAVN"], "commit": e["SHA"], "git_status_porcelain_ved_start": [], "kommando": e["KMD"], "start_utc": e["START"], "slutt_utc": e["SLUTT"],
       "returkode": int(e["RC"]), "resultatfil": e["RES"] or None, "nye_filer": [x for x in e["NYE"].split("\n") if x],
-      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"], "tag_testkjoring_v1": e["TAG_KODE"], "kode_uendret_siden_testkjoring_v1": True,
+      "tag_prereg_v1": e["TAG_PREREG"], "tag_h4_script_v2": e["TAG_H4"], "tag_testkjoring": {"navn": e["TAG_KODE_NAVN"], "commit": e["TAG_KODE"]}, "tag_testkjoring_v1": e["TAG_KODE_V1"], "kode_uendret_siden_tagg": True,
       "preregistrering": {"fil": e["PRE"], "sha256": e["SHA_PRE"]}, "manus": {"fil": e["MAN"], "sha256": e["SHA_MAN"]}}
 open(e["META"], "w", encoding="utf-8").write(json.dumps(ut, ensure_ascii=False, indent=2) + "\n")
 print(e["META"])
diff --git a/scripts/rigg_manus.py b/scripts/rigg_manus.py
index fe5c9dd..956e1cc 100644
--- a/scripts/rigg_manus.py
+++ b/scripts/rigg_manus.py
@@ -1,45 +1,51 @@
 #!/usr/bin/env python3
-"""Starter norsk-tales kalibreringsrigg (lokal nettleserserver for innlesing) med arkivklarerings testmanus KLAR-MANUS-0002 (H4 i KLAR-PREREG-0001).
+"""Starter H4-innleseren (KLAR-ADR-0018) med arkivklarerings testmanus KLAR-MANUS-0002 (H4 i KLAR-PREREG-0001).
 
-norsk-tale er bare en referanse (KLAR-ADR-0001): riggen er et eksternt verktøy som brukes fra sin egen katalog
-(NORSK_TALE, standard ~/dev/norsk-tale) og kopieres ikke hit. Dette skriptet bytter bare ut manusfila og peker opptaksmappen
-til Vault. Lyd fra innlesingen ligger kun på Vault og går aldri i git (ADR-0007).
+Innleseren er en egen modus uten noe resultat: ingen transkripsjon, flagg, poeng, rapport eller eksport vises eller finnes som rute
+(`arkivklarering/h4_innlesing.py`). Den bygger på norsk-tales kalibreringsrigg, men bare når riggen står på den låste commiten med de låste
+filene (ellers stopper den). Lyd fra innlesingen ligger kun på Vault under /Volumes/Vault/arkivklarering/lyd/h4/ og går aldri i git eller sky
+(ADR-0007). `kalibrering/kjor_h4.py --opptak /Volumes/Vault/arkivklarering/lyd/h4` leser opptakene (scripts/kjor_testdel.sh sender det).
 
-    source scripts/miljo.sh && .venv/bin/python scripts/rigg_manus.py          # starter riggen; åpne URL-en som skrives ut
-    .venv/bin/python scripts/rigg_manus.py --tor                                # bare kontroller at manus og rigg laster
+    source scripts/miljo.sh && .venv/bin/python scripts/rigg_manus.py          # starter innleseren; åpne URL-en som skrives ut
+    .venv/bin/python scripts/rigg_manus.py --tor                                # bare kontroller manus, rigglås og opptaksmappe
 
-I riggen: velg målform og region (dialektfeltet), modus «dialekt» leser bare setningene med dialektutvalg=ja, modus «fullt»
-leser alle 156. Skriptet leser bare teksten som skal leses opp; det kjører ingenting gjennom rørledningen (testmanuset er sperret der til preregistreringen er registrert). Opptakene havner under /Volumes/Vault/arkivklarering/lyd/menneske/<runde>/ som 16 kHz mono wav.
+Skriptet leser bare teksten som skal leses opp; det kjører ingenting gjennom rørledningen (testmanuset er sperret der til preregistreringen er
+registrert). Innlesing til 16 kHz mono wav: `<runde>/opptak/<manus-id>.wav`, med `runde.json` og `opptakslogg.jsonl` (id, tidspunkt, forsøk, grunn).
 """
 import glob
-import os
 import pathlib
 import re
 import sys
 
 REPO = pathlib.Path(__file__).resolve().parent.parent
-NORSK_TALE = pathlib.Path(os.environ.get("NORSK_TALE", "~/dev/norsk-tale")).expanduser()
-OPPTAK = "/Volumes/Vault/arkivklarering/lyd/menneske"
+sys.path.insert(0, str(REPO))
+
+
+def siste_manus():
+    return max(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")), key=lambda p: tuple(int(x) for x in re.search(r"_v(\d+(?:\.\d+)*)_", p).group(1).split(".")))  # versjonssortering
 
 
 def main(argv=None):
+    from arkivklarering import h4_innlesing
     from arkivklarering.miljo import krev_vault_miljo
     krev_vault_miljo()
     argv = list(sys.argv[1:] if argv is None else argv)
-    tor = "--tor" in argv
-    argv = [a for a in argv if a != "--tor"]
-    manus = max(glob.glob(str(REPO / "kalibrering" / "KLAR-MANUS-0002_*.tsv")), key=lambda p: tuple(int(x) for x in re.search(r"_v(\d+(?:\.\d+)*)_", p).group(1).split(".")))  # versjonssortering
-    for d in ("kalibrering", "kjerne", "lytter"):
-        sys.path.insert(0, str(NORSK_TALE / d))
-    import rigg  # norsk-tale/kalibrering/rigg.py
-
-    rigg.MANUS = pathlib.Path(manus)
-    pathlib.Path(OPPTAK).mkdir(parents=True, exist_ok=True)
-    if tor:
-        r = rigg.Rigg(OPPTAK, {"modellvalg": None, "modell": None, "whisper": None})
-        print(f"manus: {manus}\n{len(r.manus)} setninger, {sum(1 for s in r.manus if s['dialektutvalg'])} med dialektutvalg; opptak: {r.rot}")
+    if any(a not in ("--tor",) for a in argv):
+        sys.exit("bruk: rigg_manus.py [--tor]  (opptaksmappen er fast: " + str(h4_innlesing.H4_ROT) + ")")
+    manus = siste_manus()
+    try:
+        lås = h4_innlesing.kontroller_rigg()
+    except h4_innlesing.RiggFeil as e:
+        sys.exit(str(e))
+    if argv:
+        rigg = h4_innlesing.last_rigg()
+        rigg.MANUS = pathlib.Path(manus)
+        H4Rigg, _ = h4_innlesing.lag_klasser(rigg)
+        r = H4Rigg(h4_innlesing.H4_ROT)
+        print(f"manus: {manus}\n{len(r.manus)} setninger, {sum(1 for s in r.manus if s['dialektutvalg'])} med dialektutvalg; opptak: {r.rot}\n"
+              f"rigg: norsk-tale commit {lås['norsk_tale_commit']}, {len(lås['filer'])} filer verifisert (sha256)\ninstruks: {h4_innlesing.INSTRUKS}")
         return 0
-    return rigg.main(["--opptak", OPPTAK, *argv])
+    return h4_innlesing.start(manus)
 
 
 if __name__ == "__main__":
diff --git a/tests/test_kjor_testdel.py b/tests/test_kjor_testdel.py
index 73224dc..d93293f 100644
--- a/tests/test_kjor_testdel.py
+++ b/tests/test_kjor_testdel.py
@@ -44,6 +44,7 @@ def lag_repo(tmp_path):
     git(r, "tag", "prereg-v1")
     git(r, "tag", "h4-script-v2")
     git(r, "tag", "testkjoring-v1")
+    git(r, "tag", "testkjoring-v2")
     bart = tmp_path / "origin.git"
     subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(bart)], check=True)
     git(r, "remote", "add", "origin", str(bart))
@@ -83,10 +84,10 @@ def test_en_del_committer_pusher_og_speiler_med_meta_ved_siden_av_resultatet(tmp
     start = git(r, "rev-parse", "HEAD")
     p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
     assert p.returncode == 0, p.stderr
-    assert kjort(r) == ["h4 --prereg-id KLAR-PREREG-0001".replace("h4", "kjor_h4")]
+    assert kjort(r) == ["kjor_h4 --prereg-id KLAR-PREREG-0001 --opptak /Volumes/Vault/arkivklarering/lyd/h4"]
     d = json.loads((r / "docs" / "KLAR-EVAL-kjor_h4_v1.0_2026-10-27_kjoring_meta.json").read_text())
     assert d["commit"] == start and d["git_status_porcelain_ved_start"] == [] and d["returkode"] == 0 and d["del"] == "H4"
-    assert d["tag_testkjoring_v1"] == start and d["kode_uendret_siden_testkjoring_v1"] is True
+    assert d["tag_testkjoring"] == {"navn": "testkjoring-v2", "commit": start} and d["tag_testkjoring_v1"] == start and d["kode_uendret_siden_tagg"] is True
     assert d["tag_prereg_v1"] == start == d["tag_h4_script_v2"] and d["preregistrering"]["fil"].endswith("_v1.10_2026-10-27.md")  # versjonssortering
     assert d["resultatfil"] == "docs/KLAR-EVAL-kjor_h4_v1.0_2026-10-27.json"
     assert git(r, "status", "--porcelain") == "" and git(r, "rev-parse", "HEAD") != start
@@ -103,7 +104,7 @@ def test_to_kjoringer_etter_hverandre_hver_med_egen_commit_push_og_speil(tmp_pat
     assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord", "kjor_personvern_dev", "kjor_h4"]
     assert "--datasett npsc --splitt test --prereg-id KLAR-PREREG-0001 --mal-person 300 --mal-sted 200 --maks-timer 4 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0014" in kjort(r)[1]
     assert kjort(r)[0].endswith("--per-dialekt 60 --ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0013")
-    assert kjort(r)[2].endswith("--ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015") and kjort(r)[3].endswith("kjor_h4 --prereg-id KLAR-PREREG-0001")
+    assert kjort(r)[2].endswith("--ut-mappe eval/test --etikett TEST --eval-nr KLAR-EVAL-0015") and kjort(r)[3].endswith("kjor_h4 --prereg-id KLAR-PREREG-0001 --opptak /Volumes/Vault/arkivklarering/lyd/h4")
     log = git(r, "log", "--format=%H %s", f"{start}..HEAD").splitlines()[::-1]
     assert [l.split(" ", 1)[1][:10] for l in log] == [f"Testdel H{i}" for i in (1, 2, 3, 4)]
     metas = [json.loads(p_.read_text()) for p_ in sorted((r / "docs").glob("*kjoring_meta.json"))]
@@ -162,7 +163,7 @@ def test_resultatfiler_og_andre_filtyper_under_eval_tillates(tmp_path):
 
 def test_manglende_tagg_stopper(tmp_path):
     r, bart = lag_repo(tmp_path)
-    git(r, "tag", "-d", "testkjoring-v1")
+    git(r, "tag", "-d", "testkjoring-v2")
     p = kjor(r, "H4", "--prereg-id", "KLAR-PREREG-0001")
     assert p.returncode == 5 and "finnes ikke" in p.stderr and kjort(r) == []
 
@@ -171,7 +172,7 @@ def test_to_testdeler_etter_hverandre_med_kodesjekk_for_hver(tmp_path):
     r, bart = lag_repo(tmp_path)
     p1 = kjor(r, "H1", "--prereg-id", "KLAR-PREREG-0001")
     assert p1.returncode == 0, p1.stderr
-    assert git(r, "rev-parse", "HEAD") != git(r, "rev-parse", "testkjoring-v1")  # HEAD har flyttet seg (resultat-commit), koden ikke
+    assert git(r, "rev-parse", "HEAD") != git(r, "rev-parse", "testkjoring-v2")  # HEAD har flyttet seg (resultat-commit), koden ikke
     p2 = kjor(r, "H2", "--prereg-id", "KLAR-PREREG-0001")
     assert p2.returncode == 0, p2.stderr
     assert [x.split()[0] for x in kjort(r)] == ["kjor_dev", "kjor_flaggoverlevelse_ord"]
```

**Tørrkjøring av `kjor_testdel.sh --tor` (2026-10-27; ingen kode endret, ingen avvik).** Uendret `--tor` er kjørt for H1, H2, H3 og H4 i en ren klon av `add7be0`: alle fire ga exit 0 og skrev kommandoene (eval-nummer `KLAR-EVAL-0013`, `-0014`, `-0015` for H1–H3; H4 med `--opptak /Volumes/Vault/arkivklarering/lyd/h4`). `--tor` kontrollerer bare rent arbeidstre og kodetagg (`testkjoring-v2`); det sjekker ikke flagg, stier, PREREG-status eller utdatanavn. En utvidet kontroll (`scripts/kjor_testdel_tor.py`, wrapper-endring og ny tag `testkjoring-v3`) ble laget og **forkastet av eier før den ble committet**; filene er slettet og wrapper og tester er tilbakestilt til committet versjon (kode lik `testkjoring-v2`). Funn fra den forkastede kontrollen som fortsatt gjelder: testdelenes datafiler (NB Samtale test, NPSC test, NorNE test) er ikke lastet ned lokalt, og `lyd/h4/` har ingen innlesing ennå; begge er forutsetninger som må være på plass før henholdsvis H1–H3 og H4 kan kjøres. Veikartet er rettet (`KLAR-ARK-0006` v1.2, steg 8).

**ÅPENT PUNKT (ikke avsluttet): H4 og innleseren (2026-10-27; AV-19 og AV-20 i KLAR-LOG-0003, `KLAR-ARK-0006` v1.3).** H4 er ikke gjennomført ennå. Innleseren stoppet da Eirik stoppet og gjenopptok under testopptaket. Ingen opptak ble lagret (lyd/h4/ tom). Årsaken er ikke undersøkt. Feilen i innleseren og H4 står åpne.

**Avvik fra rekkefølgen i PREREG (AV-20).** Testdelene H1–H3 kjøres før H4-innlesingen, motsatt av rekkefølgen i PREREG, fordi innleseren feilet. Beslutning av eier 2026-10-27. Før noen testdel kjøres: testdelenes datafiler lastes ned til Vault uten å åpnes (nytt steg 9 i veikartet), og `scripts/kjor_testdel.sh` kjører H1, H2 og H3 hver for seg (ikke H4) mot `testkjoring-v2`. Konsekvens: leseren av H4 kan kjenne H1–H3-resultatene før innlesingen, selv om innleseren ikke viser noe om maskinens lesing av H4-opptakene (ADR-0018).

**Testdelenes datafiler lastet ned (2026-10-27, veikart steg 9; ingen avvik).** Kun filene PREREG-0001 peker på, til `/Volumes/Vault/arkivklarering/eval-data/`, med samme revisjoner som DEV, uten å åpnes eller leses (kopiert fra HF-cachen på Vault; størrelsen sjekket mot HF-API-et): **NB Samtale** (`Sprakbanken/nb_samtale`, revisjon `1c7028101858b854d3d568761778d8f63bb7e33f`): `test_metadata.jsonl` (933 716 byte), `test_bm_1.tar.gz` (174 331 722), `test_nn_1.tar.gz` (54 146 357). **NorNE** (`NbAiLab/norne`, revisjon `1ca12d437b84f65a34c454d339317d39d35c8149`): `bokmaal/test-00000-of-00001.parquet` (1 134 680), `nynorsk/test-00000-of-00001.parquet` (943 542). **NPSC** (`NbAiLab/NPSC`, revisjon `e906435cc445e38961d86f3ebf53a7b38603b903`), `test/` med de fire dagene 20170207, 20171122, 20171219 og 20180530: `<dag>.json` (437 615; 1 279 227; 2 664 674; 1 191 841) og `<dag>_16K_mp3.tar.gz` (11 602 500; 30 671 734; 63 037 509; 27 201 057); 48 kHz-filene er ikke hentet (PREREG: 16 kHz mp3). Til sammen 369 576 174 byte. Ingenting i repoet er endret av nedlastingen.

**Testdelene H1, H2 og H3 kjørt (2026-10-27; AV-21, ingen annet avvik).** `scripts/kjor_testdel.sh` kjørte H1, H2 og H3 hver for seg (ikke H4), alle med returkode 0, `git status --porcelain` tom ved start og kode uendret siden `testkjoring-v2` (`c49d17463c14f7719f9f271ae3d4af4824436c35`). Resultat-commit: **H1 `1be7358`** (start `279f301`, 07:42–09:21 UTC), **H2 `efcfc42`** (start `1be7358`, 09:22–13:03 UTC), **H3 `3e34815`** (start `efcfc42`, 13:03–13:12 UTC). Metafiler `…_kjoring_meta.json` ligger ved resultatene i `eval/test/`. EVAL-dokumentene med intervaller og terskelvurdering: `…-0013/-0014/-0015_…_v1.1_2026-10-27.md` (commit `ce0d603`). Intervallene er regnet med `scripts/rapporter_intervaller.py` uendret (AV-13, AV-15). Resultat (punktestimat, 95 %-intervall):
- **H1a (primær)** ra/matchet WER 0,127 (0,112–0,144), n = 252 segmenter, 51 talere, terskel ≤ 0,25: bekreftet, klart. H1b 0,337 (0,305–0,373) ≤ 0,45; H1d 0,254 (0,221–0,285) ≤ 0,35; H1e 0,464 (0,428–0,507) ≤ 0,60: alle bekreftet, klare. n = 252 følger av regelen (t og w under 60 kvalifiserte; tas alle), ikke avvik. v1.0-tabellen viser 0,128 for ra/matchet, intervallskriptet 0,127: samme verdi 0,1275, to avrundinger.
- **H2 (primær)** union, overlevelse (a), Wilson: H2a person samlet 346/379 = 0,913 (0,880–0,937) ≥ 0,85; H2b sted samlet 172/201 = 0,856 (0,8005–0,898) ≥ 0,80, klar med margin 0,0005; H2c person bokmål 145/155 = 0,935 (0,885–0,965) ≥ 0,90, bekreftet, ikke klar; H2d sted bokmål 121/139 = 0,871 (0,805–0,916) ≥ 0,80; H2e person nynorsk 201/224 = 0,897 (0,851–0,931) ≥ 0,75. H2f sted nynorsk 51/62 = 0,823 (0,710–0,898), ingen terskel. 1 995 segmenter, 3,95 timer.
- **H3 (sekundær)** hele motoren, original tekst, recall (overlapp): H3a 1,000 (0,993–1,000) ≥ 0,95; H3b 0,975 (0,953–0,987) ≥ 0,95; H3c 0,982 (0,964–0,991) ≥ 0,90; H3d 0,976 (0,949–0,989; bootstrap 0,956–0,992) ≥ 0,95. Presisjon: H3a 0,904 ≥ 0,85; H3b 0,811 (0,771–0,844) ≥ 0,80; H3c 0,733 (0,694–0,769) ≥ 0,70; H3d 0,769 ≥ 0,65. Alle åtte punktestimater oppfyller terskelen; H3b og H3c presisjon er ikke klare, og H3d recall er klar bare etter bootstrap.
- **K1–K3 holdt:** K1 differanse 0,209 (0,176–0,248), utelukker 0; K2 person 0,749 mot 0,871 og sted 0,607 mot 0,801; K3 recall-fall 0,449 / 0,281 / 0,418 / 0,478 (alle ≥ 0,15).
Begrensninger fra EVAL-dokumentene: NB-Whisper er trent på NPSC (H2 optimistisk); Wilson i H2 behandler flagg som uavhengige; overlapp mellom testdelene og NB-Whispers treningsdata er ikke kontrollert; H4 er ikke gjennomført (AV-19).

**Avvik AV-21: speil ikke kjørt etter hver testdel.** PREREG («Avvik etter registrering» 3) og `scripts/kjor_testdel.sh` kjører `scripts/speil.sh` etter hver del. `CLAUDE.md` regel 3 (eier) sier at GT, stempling og speil bare kjøres ved milepæler. Wrapperen ble derfor kjørt med miljøvariabelen `KLAR_SPEIL` pekt på et skript som bare skriver «speil hoppet over», uten at wrapperen ble endret (koden er uendret siden `testkjoring-v2`). Commit og push skjedde etter hver del som vanlig. Speil, GT og stempling kjøres én gang etter H1–H3 (milepæl). Ingen tall berørt.

**H4-innleseren: årsak funnet og rettet i grenen h4-fiks (2026-10-27; AV-19, ren lesing av diagnosen, så endring i en egen gren).** Årsak til at innlesingen 27.10 ikke ble lagret: ingen runde ble startet, og serveren ble stoppet via Avslutt-knappen (eneste kodevei: `POST /api/avslutt`, `h4_side.html:264` i `testkjoring-v2`; innleseren stoppet kontrollert, exit 0, og inaktivitetsvakten er utelukket fordi serveren gikk i under to og et halvt minutt mot 1800 s). Siden tillot et testopptak som så ut som innlesing (`h4_side.html:209-213`), og avslutning uten bekreftelse. Serveren hadde ingen hendelseslogg, så hvem som trykket og når kan ikke leses ut av loggen. Rettet i grenen `h4-fiks` (commit `9f0613b`: testsetning fjernet, banner, statuslinje, bekreftelse, hendelseslogg `serverlogg.jsonl` i opptaksroten; ADR-0018 v1.1). Kodeendringene er bare i `arkivklarering/h4_innlesing.py` og `arkivklarering/h4_side.html` (pluss tester); norsk-tale og låsen mot `bcfef63…` er uendret, og det finnes ingen sha256-verdi for de endrede filene å oppdatere i riggen (`RIGG_FILER` gjelder bare norsk-tale). Kontroll: `tests/test_h4_innlesing.py` har 12 tester, fem av dem nye (ingen testopptak og banner, bekreftelse ved avslutning, ende-til-ende mot en server i prosess med logg i rekkefølgen oppstart, runde_ny, opptak_lagret, avslutt, stoppet, og H4-skriptets listing med loggfila i roten), alle 152 ikke-tunge tester grønne, og en nettlesertest av siden mot en midlertidig server (banner, statuslinje som står uendret når lagring feiler og øker etter serversvar, bekreftelsesteksten, avbrutt bekreftelse sender ingenting). Observasjon i nettlesertesten: lagring feiler med «Cross-device link» hvis `TMPDIR` ligger på et annet volum enn opptaksroten; riggen skal derfor startes etter `source scripts/miljo.sh` (`TMPDIR` på Vault). **H4 står åpent til innlesingen er gjort.**

**h4-fiks flettet inn i main, testkjoring-v3 satt, uavhengig kontroll (2026-10-27).** Merge-commit `49bf598c95df1bf66bba3bbc8ba970f7950ffd84` (to foreldre: main `64d5cb7` og h4-fiks `d387b61`). Tre versjonerte dokumenter var endret ulikt på begge sider med samme filnavn (LOG-0001 v1.28, LOG-0003 v1.4, ARK-0006 v1.4); mains versjoner står uendret, og ny versjon (høyeste versjon + 0,1: LOG-0001 v1.29, LOG-0003 v1.5, ARK-0006 v1.5) har mains innhold først og grenens tillegg etterpå; grenens egne v1.28/v1.4/v1.4 ligger i grenen `h4-fiks` (`d387b61`). Koden ble flettet uten konflikt. `scripts/kjor_testdel.sh` og testene peker nå på `testkjoring-v3` (commit `68512e8ab0aa69fe217f6d0f2574c40380147e47`, tag-objekt `44a2081fd9bd9bd9becabf257203359064fb0ec2`), satt først etter at 152 ikke-tunge tester var grønne. Byte-likhet h4-rigg-v3 mot testkjoring-v3 for de tre riggfilene bekreftet. Worktree for h4-fiks fjernet, grenen beholdt. Uavhengig kontroll av flettingen (Opus-subagent som ikke hadde sett flettearbeidet): ingen tekst tapt fra de sammenslåtte filene, AV-ID-ene (AV-01–AV-21) unike og entydige, `ground_truth.py` i en egen klone uten varsler om dobbel bruk eller hull (kun den kjente leseadvarselen «kunne ikke leses ('wer')» for `utvalg.json` og metafilene i `eval/test/`), og byte-likhet bekreftet.

**EVAL-0013, -0014 og -0015 kontrollert mot PREREG (2026-10-27).** Intervallmetoden i registrert PREREG (v1.8 = `prereg-v1`, linje 166) og avvik 7, 9 og 11a leses av en uavhengig subagent uten å se EVAL-dokumentene. H1: clusterbootstrap over taler (B = 2000, seed 20261026), uendret; H2: Wilson, uendret. **H3: PREREG rangerer ikke Wilson og bootstrap over setninger** (linje 166 har «Proporsjoner med Wilson-95 %-intervall (H2, H3, H4)» og «NorNE: bootstrap over setninger»; avvik 9 sier bootstrap regnes «ved siden av Wilson»). EVAL-0015 v1.2 lar klassifiseringen følge Wilson (den eneste metoden som er knyttet til H3 ved navn) og merker bootstrap som sensitivitetsanalyse; eneste endring i utfall er H3d recall: «ikke klart (Wilson-grense 0,949 < 0,95)», bootstrap-grensen 0,956 ligger over terskelen. Ingen tall er endret. Valget er ikke tatt av PREREG og stod som åpent punkt til eier: **avgjort 2026-10-27, se AV-24**. EVAL-0014 v1.2 har fått begrensningen om at Wilson-intervallene ikke er klyngejustert (H2b, margin 0,0005, er følsom for det); ingen ny beregning. EVAL-0013 er kontrollert uten endring: trakten (1 195 → 921 → 748 → 428 → 428 → 252) og tabellen per dialektområde (rader, pool, trukket, bm/nn) er regnet på nytt fra `test_metadata.jsonl` og `utvalg.json` og stemmer med v1.1.

**Avvik AV-22: H4-innleseren endret etter registrering og før datainnsamling.** H4-innleseren endret etter registrering og før datainnsamling (testopptak i mikrofonsjekken fjernet, banner, statuslinje, bekreftelse ved avslutning, hendelseslogg). H4 lest inn fra grenen h4-fiks, tag `h4-rigg-v3` `5a5a58671b2eea22cc2805787735332384d732a9` (tag-objekt `918f1fd414759294e78d062ed315547f9647e330`, opprettet 2026-10-27 09:54:43 +01:00), commit pushet til grenen 2026-10-27 09:54:17 +01:00 (lokal reflog for `origin/h4-fiks`, ikke uavhengig etterprøvbart), OTS-stempel sendt 2026-10-27 08:54:58Z–08:55:09Z (fem filer: HEAD-fil, ADR-0018 v1.1, `h4_innlesing.py`, `h4_side.html`, `scripts/rigg_manus.py`; `docs/stempler/`), Bitcoin-bekreftet, alle fem: tidligste attestasjon i blokk 973377 (2026-10-27T09:21:20Z), ytterligere attestasjoner i blokk 973378 (09:37:13Z) og 973384 (10:53:10Z). Første opptak: ikke lest inn ennå (`serverlogg.jsonl` har ingen `opptak_lagret`; innleseren er startet og har stoppet av tidsavbrudd uten runde). Riggkoden er byte-identisk med `testkjoring-v3` `68512e8ab0aa69fe217f6d0f2574c40380147e47` (tag-objekt `44a2081fd9bd9bd9becabf257203359064fb0ec2`; `git diff --quiet h4-rigg-v3 testkjoring-v3 -- arkivklarering/h4_innlesing.py arkivklarering/h4_side.html scripts/rigg_manus.py` gir 0; kontrollert også av uavhengig subagent). `scripts/kjor_testdel.sh` kontrollerer nå `testkjoring-v3` (v1 og v2 beholdt), som AV-18 gjorde for v2. Endringen berører innsamlingsverktøyet, ikke analysen eller tersklene.

**Avvik AV-23: sha256 for testdataene ført etter H1-start.** sha256 for testdataene (13 filer) ble ført 2026-10-27 etter at H1 startet (`kjor_dev.py` 08:42:54 +01:00 = 07:42:54Z). Dataenes identitet er likevel fastlagt: alle 13 er byte-identiske med de offentlige, innholdsadresserte HF-revisjonene `Sprakbanken/nb_samtale@1c70281`, `NbAiLab/norne@1ca12d4` og `NbAiLab/NPSC@e906435` (LFS-oid eller git-blob), ført i LOG v1.27, commit `279f301` (committet 08:42:35; push 08:42:37 +01:00 ifølge lokal reflog, ikke uavhengig etterprøvbart; GitHub Events API viser den ikke; ikke OTS-stemplet). Hashfila ble skrevet 09:27:56 +01:00 (08:27:56Z) og stemplet; stempelet er Bitcoin-bekreftet i blokk 973374 (2026-10-27T08:44:17Z), dvs. etter H1-start og før H2-start. Hashfil (KLAR-ARK-0007, sha256 `8ac910b16ccbc7b91481f02272e48c051297ee11900bae4d6d00a936a04fb91c`): `docs/KLAR-ARK-0007_arkivklarering_testdata-sha256_v1.0_2026-10-27.txt`, med .ots: `docs/stempler/KLAR-ARK-0007_arkivklarering_testdata-sha256_v1.0_2026-10-27.txt.8ac910b16ccb.ots`.

**Tilstand for testdelene, ført fra disk (2026-10-27).** Testdataene lå på Vault med filtid 07:42:01–07:42:23Z; H1 startet 07:42:54Z og sluttet 09:21:45Z (resultat-commit `1be7358`), H2 09:22:22Z–13:03:39Z (`efcfc42`), H3 13:03:59Z–13:12:57Z (`3e34815`), alle med returkode 0 (`…_kjoring_meta.json`). Ingen opptak av testmanuset finnes ennå (H4 er ikke gjennomført, AV-19 og AV-22).

**Stempler for h4-rigg-v3 ført i LOG-0002 (2026-10-27).** De fem `.ots`-filene fra `h4-rigg-v3` (`docs/stempler/`, commit `d387b61`), sendt 08:54:58Z–08:55:09Z, er ført i `KLAR-LOG-0002` v1.30 med status etter `ots upgrade`: alle fem Bitcoin-bekreftet (tidligste blokk 973377). Hashfila for testdataene (KLAR-ARK-0007) er ført der med blokk 973374.

**Avvik AV-24: primærintervall for H3 (beslutning av eier, 2026-10-27).** PREREG v1.8 (linje 166) nevner både Wilson og bootstrap over setninger for H3 uten å rangere dem. Eier beslutter 2026-10-27: Wilson er primær for H3, bootstrap over setninger rapporteres som sensitivitetsanalyse. Beslutningen er tatt etter at resultatene var kjent, og går i retning av den mer konservative klassifiseringen (H3d recall: ikke klart, Wilson-grense 0,949 < 0,95). Begge intervallene står i EVAL-0015 v1.2 (samme tall og klassifisering i v1.3). EVAL-0015 v1.4 fører beslutningen. Det åpne punktet fra v1.30 er ikke fjernet, men markert «avgjort 2026-10-27, se AV-24» (v1.31 og EVAL-0015 v1.3 fjernet det; rettet etter eiers presisering, LOG v1.32 og EVAL-0015 v1.4).

**Avvik AV-25: inaVAMOS brukes ikke lenger; H4 med inaSpeechSegmenter.** inaVAMOS (Pantagruel Research-only License; art. 1 begrenser lisenstakere, art. 3 forbyr bruk i kommersiell aktivitet) ble brukt i H1 og H2 og i DEV-arbeidet. EcoDecos dekning under lisensen er uavklart. Fra 2026-10-27 brukes den ikke. H4 kjøres med inaSpeechSegmenter (ADR-0019, tag testkjoring-v4), besluttet før noen H4-data er sett. H1 og H2 står som preregistrert. Merge-commit `40f0cbde6236fb96e90add4dc52d899b6c6bd80e` (inaseg-erstatning), kodetagg `testkjoring-v4` `3e0eead96b9238d26c5bad16a5b8b665b4341ecb` (tag-objekt `22b81d674770eef3da710d9f50ba17bb1ec60970`; `kjor_testdel.sh` kontrollerer den, v1–v3 beholdt); riggfilene er byte-identiske med `h4-rigg-v3` (`git diff --quiet h4-rigg-v3 testkjoring-v4 -- arkivklarering/h4_innlesing.py arkivklarering/h4_side.html scripts/rigg_manus.py` gir 0). `kjor_testdel.sh H4` setter `ARKIVKLARERING_SEGMENTERING=inaseg` og fører segmenteringsloggen i `kjoring_meta`; H1–H3-kommandoene er uendret. Kodeendringer før taggen: kjørervalg i `segment.py`, `segment_inaseg.py` med logg, miljøvariablene `ARKIVKLARERING_CACHE_SUFFIKS` og `ARKIVKLARERING_ETIKETT_TEST` i `kjor_flaggoverlevelse_ord.py` og `kjor_dev.py` (standardverdier gir uendret oppførsel). Vektlisensen for inaSpeechSegmenter er uklar (ADR-0019 v1.0); ingen NC-vilkår er funnet. Eiers beslutning 2026-10-27.

**Sensitivitetskjøring av H1 og H2 utgår (2026-10-27, eiers endring).** AV-teksten (AV-25) er rettet i denne versjonen: setningen om en sensitivitetskjøring er tatt ut. En kjøring var startet (H1 med `ARKIVKLARERING_SEGMENTERING=inaseg`, start 16:25:26Z på `e054070`+stempler, utdata i `eval/sensitivitet/`) og ble stoppet av meg ved eiers endring etter ca. 59 minutter, før noe resultat fantes (segmenteringen av 252 segmenter var gjort, ingen Whisper-utdata lagret). De to delvise filene i `eval/sensitivitet/` (utvalgsfil og segmenteringslogg) er slettet; ingen cache er opprettet og ingen resultatfil finnes. EVAL-0016 og -0017 er avlyst (numrene gjenbrukes ikke). Miljøvariablene `ARKIVKLARERING_CACHE_SUFFIKS` og `ARKIVKLARERING_ETIKETT_TEST` ligger igjen i koden (taggen `testkjoring-v4`) uten bruk; standardverdiene gir uendret oppførsel. Rigg og H4 (steg 3) utgår også i denne oppgaven; H4 er fortsatt ikke gjennomført (AV-19, AV-22, AV-25).

**Uavhengig kontroll av EVAL-0013–0015 og eval/test/ (2026-10-27, Opus-subagent, kun lesing).** Resultat: PASS. De ni filene i resultatcommitene `1be7358` (H1), `efcfc42` (H2) og `3e34815` (H3) og alle 16 filene under `eval/test/` i `e5b9c10` har samme sha256 i arbeidstreet nå (og samme blob-SHA-1); `git diff --stat e5b9c10 HEAD -- eval/test` er tom; ingen fil under `eval/test/` er noen gang slettet, endret eller omdøpt (`git log --diff-filter=DMR` tom). Gjeldende versjoner: EVAL-0013 v1.1, EVAL-0014 v1.2, EVAL-0015 v1.4. `eval/sensitivitet/` finnes ikke i arbeidstreet eller i noen commit. (Kontrollen om inaVAMOS-cache og H4-import utgår sammen med sensitivitetskjøringen og H4.)

**GT-retting (2026-10-27; endring i et dokumentasjonsverktøy etter siste testkjøring, uten betydning for analysen).** `scripts/ground_truth.py` (`seksjon_eval`) hopper nå over `….utvalg.json` og `…_kjoring_meta.json` når WER leses fra `eval/`, så leseadvarselen «kunne ikke leses ('wer')» for `KLAR-EVAL-0013_…utvalg.json` og metafilene faller bort; bare resultatfilene leses, og en resultatfil uten «wer» gir fortsatt advarsel. Ny test `tests/test_ground_truth_wer.py` (2 tester); 168 ikke-tunge tester grønne. Ingen ny tag: `testkjoring-v4` er satt på koden før denne endringen, og endringen berører ikke analysekoden (H1–H3 er kjørt; H4 er ikke kjørt).

**Avvik AV-26: inaSpeechSegmenter er standard segmentering; inaVAMOS valgfritt tillegg.** inaSpeechSegmenter er standard segmentering i CLI, `arkivklarering/segment.py` og `eval/dev/felles.py` (miljøvariabelen ARKIVKLARERING_SEGMENTERING: inaseg standard, inavamos valgfritt); inaVAMOS er flyttet fra kjerneavhengighet til det valgfrie tillegget `reproduksjon-h1h2` (Pantagruel Research-only License; bare forskning). `scripts/kjor_testdel.sh` setter inavamos for H1/H2 (reproduksjon av de preregistrerte kjøringene) og inaseg for H4; reproduksjonsskriptene setter inavamos der de sammenligner mot lagrede inaVAMOS-resultater. Ny kodetagg `testkjoring-v5` (commit 076bb8d50906293a9bbe7c4a26f88da0150ce1ed, tag-objekt f1b0b1edf52c9654f472e5af4d79c1bc07cdc174); `testkjoring-v4` og tidligere beholdt; riggfilene er fortsatt byte-identiske med `h4-rigg-v3`. Endringen berører ikke H1–H3-resultatene eller tersklene; den følger av AV-25. Eiers beslutning 2026-10-27. Kontrollert 2026-10-27: `git rev-parse testkjoring-v5 testkjoring-v5^{commit}` gir `f1b0b1edf52c9654f472e5af4d79c1bc07cdc174` og `076bb8d50906293a9bbe7c4a26f88da0150ce1ed`; `git diff --quiet h4-rigg-v3 testkjoring-v5 -- arkivklarering/h4_innlesing.py arkivklarering/h4_side.html scripts/rigg_manus.py` gir 0. Ført i `KLAR-LOG-0003` v1.10 og `KLAR-PREREG-0001` v1.23 (punkt 19 og raden AV-26 i oppsummeringstabellen). Dokumentene som sa at standarden var inaVAMOS er rettet: `KLAR-ADR-0019` v1.3, `KLAR-ARK-0001` v1.6; toppkommentaren i `requirements-inaseg.lock` sier nå «vedtatt for v1.0» i stedet for «kladd: foreslått, ikke vedtatt» (pakkelinjer og hasher uendret).

**Kildekontroll v1.3 og REG-0001 v1.2 (2026-10-27).** `KLAR-KILDE-0001` v1.3: IS-01 rettet fra «ikke funnet» til verifisert mot rå `LICENSE` for ina-foss/inaSpeechSegmenter ved tagg v0.8.0 (ny kilde K119). RG-01 forblir «delvis». Kildemerknaden under streken i `KLAR-REG-0001` v1.2 dekker nå også RG-01 (Mediesök); den registrerte teksten er byte-lik v1.0 (`diff` mot v1.0 viser bare tillagte linjer: versjonslinjen og merknaden under streken).

**Avvik fra instruks: `scripts/navnesjekk.py` kjørt (2026-10-27).** En agent kjørte `scripts/navnesjekk.py` mot instruks. Skriptet slår opp etternavnene i `KLAR-MANUS-0002` i SSBs navnesøk på nett (docstring linje 2–4). Utdatafila `eval/dev/navnesjekk_manus0002_2026-10-27.json` ble slettet; den finnes ikke i arbeidstreet og er aldri committet (`git log --all` for stien er tom).

**B4-rettinger 2026-10-27.** Dokumenter rettet i dag: `KLAR-ADR-0003` v1.1 (sporbarhet per verktøy og kjøring strammet inn til det kilden dekker, CL-09) og v1.2 (implementeringsstatus rettet etter koden: MMIF 1.2.0 skrives som eksport); `KLAR-REG-0001` v1.1 (kildemerknad under streken, AM-05 og AA-04) og v1.2 (merknaden utvidet med Mediesök, RG-01); `KLAR-ARK-0001` v1.5 og `KLAR-ADR-0010` v1.1 (OSF-statusen for fbme7 presisert, OS-01); `KLAR-PREREG-0001` v1.22 (bare OSF-statusen for fbme7); `KLAR-KILDE-0001` v1.1 (K91–K118 og 55 nye rader), v1.2 (radene peker på gjeldende dokumentversjoner; CL-09 verifisert, RG-01 delvis, ny rad IS-01) og v1.3 (K119, IS-01 verifisert); `KLAR-EVAL-0013` v1.2 og `KLAR-EVAL-0014` v1.3 (begrensninger: inaVAMOS-lisensen og mulig overlapp mellom testdata og NB-Whispers treningsdata; ingen tall endret); `KLAR-ADR-0019` v1.1 (sensitivitetskjøringen utgår), v1.2 (URL i lisenssitatet utelatt) og v1.3 (standarden i koden er inaSpeechSegmenter, AV-26); `KLAR-PREREG-0001` v1.21 (oppsummeringstabell over avvikene, B6). `source scripts/miljo.sh && .venv/bin/python scripts/sjekk_kilder.py` etter KILDE v1.3: «påstander per status: delvis: 7, ikke funnet: 3, motsagt: 1, verifisert: 206» (217 rader); exit 1 for ett brudd: «URL UTEN RAD» for ORCID-lenken i `KLAR-ARK-0009` v0.1 linje 5 (artikkelutkastet laget i dag, se under).

**Dokumentasjon laget eller oppdatert i dag (2026-10-27).** `README.md`, `NOTICE`, `CHANGELOG.md` og `CONTRIBUTING.md` (ny), `KLAR-ARK-0004` v1.1 (modellkort), `KLAR-ARK-0005` v1.2 (datablad for manus) og `KLAR-ARK-0009` v0.1 (JOSS-artikkelutkast, nytt).

**Kildekontroll-rettelser av tidligere LOG-tekst (2026-10-27).** Rettelse; teksten i v1.35 og v1.36 (oppføringen «Eksportformater (v0.4)», linje 66, uendret siden v1.11) står, og historikken skrives ikke om. (1) IW-08: IIIF Cookbook-oppskrift 0231 er en metaoppskrift («This meta recipe describes options …», K31) med tre alternativer for transkripsjoner; alternativ 2 og 3 bruker `supplementing`-annotasjoner. Manifestet bruker begge: per lag én `supplementing`-annotasjon for hele WebVTT-fila og én per cue med tidsfragment, og mønsteret i 0219 (`arkivklarering/eksport.py:195–212`). At manifestet følger alternativene er en påstand om vår kode, ikke noe kilden kan bekrefte (`KLAR-KILDE-0001` IW-08, delvis). (2) OH-06/OH-06b: lenken til OHMS' CSV-importmal på Museums Ontarios OHMS-side (K79) peker til Dropbox, som ga en HTML-feilside («Dropbox - Error», HTTP 200) ved en uautentisert henting 2026-10-26 (K78). Malen er ikke hentet og ikke brukt; om den finnes andre steder er ikke undersøkt. «Ligger bare på Dropbox» i linje 66 sier mer enn kildene dekker. Radene IW-08, OH-06 og OH-06b i `KLAR-KILDE-0001` v1.4 peker nå på denne oppføringen; statusen er fortsatt «delvis», fordi radenes påstand er den opprinnelige teksten.

**Nye versjoner etter kildekontrollen (2026-10-27).** `KLAR-ARK-0001` v1.7: § 3.1 sa at tale over musikk transkriberes og flagges, og § 5 sa «inaVAMOS, fire etiketter» for `segment.py`; med inaSpeechSegmenter (standard, KLAR-ADR-0019 v1.3) faller flagget bort, så begge er rettet (flagget gjelder bare med inaVAMOS). `KLAR-LOG-0003` v1.11: kolonnen «testdata sett?» sa «nei» på alle rader, også for avvik besluttet eller ført etter H1-start (07:42:54Z) eller etter at H1–H3-resultatene var kjent (H3 slutt 13:12:57Z); AV-19 og AV-21–AV-26 er rettet etter tidspunktene i denne loggen, commit-tidene og `eval/test/*_kjoring_meta.json`, og kolonneforklaringen er skrevet om. `KLAR-KILDE-0001` v1.4: radene som pekte på README-linjer, `KLAR-ARK-0004` v1.0 og `KLAR-ARK-0005` v1.1 peker på gjeldende linjer i README, ARK-0004 v1.1 og ARK-0005 v1.2 (AR4-02–AR4-04 står ikke ordrett i v1.1 og peker fortsatt på v1.0, med merknad); ny kilde K120 (inaVAMOS `LICENSE.en.md`, uoffisiell engelsk oversettelse) og K121 (`LICENSE.md`, fransk originaltekst som går foran), hentet 2026-10-27T18:45:10Z og 18:45:11Z med GitHub contents-API-et (to forespørsler, én per fil, logget i `inavamos_license_hentelogg_2026-10-27.txt` på Vault); nye rader PG-01 (art. 1, hvem som kan bruke modellen) og PG-02 (art. 3, kommersiell aktivitet), begge verifisert mot K120, fordi README, NOTICE og ARK-0004 v1.1 viser til artiklene uten kilderad; ny rad OR-01 («ikke funnet») for ORCID-lenken i `KLAR-ARK-0009` v0.1, som ikke endres og ellers gir «URL UTEN RAD». `KLAR-ARK-0009` v0.2: ORCID skrevet som «ORCID 0009-0001-9188-6788» uten URL (identifikatoren står i `CITATION.cff:12`). `KLAR-ARK-0003` v1.20: KLAR-ARK-0009 i bruk og KLAR-PREREG-0003 reservert ført; «brukt av» for ARK-0004, ARK-0005 og ARK-0008 oppdatert. `source scripts/miljo.sh && .venv/bin/python scripts/sjekk_kilder.py` etter KILDE v1.4: «påstander per status: delvis: 7, ikke funnet: 4, motsagt: 1, verifisert: 208» (220 rader), exit 0.


**KLAR-ARK-0008 v1.0 skrevet, med kontroller og rettinger (2026-10-27).** `docs/KLAR-ARK-0008_arkivklarering_avklaringer-foer-frys_v1.0_2026-10-27.md` (nytt): A (Eiriks beslutninger, [fra disk] fylt), B1–B12 (hver kontroll kjørt, bevis og status ført), C, D, E (grunnlag for blindtest, med punktene 0a, 0b og 0c som åpne punkter i E) og F (JOSS-sjekklista, én rad per punkt). Rettinger som nye versjoner: `KLAR-EVAL-0013` v1.3 (B12: perioden Stortinget Speech Corpus dekker, med sitat og URL, OL-13, OL-14, OL-16) og `KLAR-EVAL-0014` v1.4 (B12: NB Samtale-referansen startet som automatisk talegjenkjenning fra NBs KI-lab, med sitat og URL, OL-19, OL-20); ingen tall, tabeller, klassifisering eller resultatfiler endret. `KLAR-KILDE-0001` v1.5: nye rader NT-23 og NT-24 (katalogposten K108 lister `sennheiser_3.tar.gz` og `Annotation.zip`), verifisert mot den lagrede kopien av K108 uten ny henting, fordi ARK-0008 seksjon E har de to lenkene. `KLAR-ARK-0003` v1.21: KLAR-ARK-0008 i bruk. `source scripts/miljo.sh && .venv/bin/python scripts/sjekk_kilder.py` etter KILDE v1.5: «påstander per status: delvis: 7, ikke funnet: 4, motsagt: 1, verifisert: 210» (222 rader), exit 0. Ikke rettet (står åpne i ARK-0008): B4 (OR-01, ORCID i ARK-0009 v0.2:5, ikke funnet og ikke merket), B5 (README krediterer ikke NB-BERT-base-ner og pyannote community-1 med CC BY 4.0; README er ikke et versjonert dokument og er ikke endret) og B9 (EVAL-0009 finnes ikke; betinget av A1). B3-skanningen (sporte filer mot NB Samtale, NPSC og NorNE på Vault) ble kjørt med et skript utenfor repoet; ingen fil i repoet er endret av den. Ingen nett brukt utover `gh repo view` og `gh release list` for repoets synlighet og utgivelser.


**B4 og B5 lukket: ORCID-posten hentet, README rettet, KLAR-ARK-0008 v1.1 (2026-10-27).** Nettbruk: ett kall, 2026-10-27T19:22:44Z, `curl -sS -L -A 'arkivklarering-kildekontroll (eirik@ecodeco.no)' -H 'Accept: application/json'` mot ORCID Public API v3.0 (`/v3.0/0009-0001-9188-6788/person`), HTTP/2 200, 9 594 byte, uten token og uten gjentak; HTML-siden på orcid.org er ikke hentet. Råkopien er lagret uendret på Vault som `kilder/orcid_0009-0001-9188-6788_person.json` (K122, sha256 `ca2b2bb1b9cc03e783870641ad22b3a4013c016d290df75a72fa1e578424e79f`) med hentelogg `kilder/orcid_hentelogg_2026-10-27.txt`; begge er ført i `kilder/SHA256SUMS` (143 linjer, `shasum -a 256 -c` uten avvik), og utdraget for OR-01 er lagt til i `kilder/kilderegister_utdrag.md`. Posten har fornavn «Eirik», etternavn «Botten Nicolaysen» og kildenavn «Eirik Botten Nicolaysen» for iD-en 0009-0001-9188-6788. `KLAR-KILDE-0001` v1.6: ny kilde K122; OR-01 fra ikke funnet til verifisert med ordrett sitat fra K122; OL-01, OL-02, OL-04–OL-10, OL-13–OL-16 og OL-18–OL-20 peker på linjene i `KLAR-EVAL-0013` v1.3 og `KLAR-EVAL-0014` v1.4 der sitatet fra raden står ordrett (helt eller som utdrag) sammen med påstands-ID-en; OL-03, OL-11, OL-12 og OL-17 står uendret; NB-02, PY-10 og PY-13 peker også på README.md:235. `README.md` (endret på plass, ingen nye linjer): «Lisens og sitering» (linje 235) krediterer NB-BERT-base-ner (NbAiLab) og pyannote/speaker-diarization-community-1 (pyannote) med navn, lenke og CC BY 4.0, og sier at pyannote-modellen lastes ned av brukeren etter at vilkårene er godtatt; henvisningen til NOTICE og [AVVENTER]-merkene står. Lenkene peker på nyeste versjoner (ARK-0001 v1.7, ARK-0003 v1.21, KILDE v1.6, LOG-0001 v1.39, LOG-0003 v1.11, EVAL-0013 v1.3, EVAL-0014 v1.4) og har nye lenker til ARK-0008 v1.1 og ARK-0009 v0.2; sitatlenkene til EVAL-0006 v1.1, EVAL-0007 v1.0 og EVAL-0008 v1.1 er beholdt fordi sitatene ikke står ordrett i nyeste versjon. `KLAR-ARK-0008` v1.1: B4 og B5 LUKKET med de nye bevisene; B har nå LUKKET 11 og åpent 1 (B9); `grep -c "ÅPEN – før frys"` på v1.1 gir 23 (v1.0: 25). `source scripts/miljo.sh && .venv/bin/python scripts/sjekk_kilder.py`: «påstander per status: delvis: 7, ikke funnet: 3, motsagt: 1, verifisert: 211», exit 0. `.venv/bin/python -m pytest -q -m 'not tung'`: 181 passed, 3 deselected. Ingen andre nettkall.


**Avklaringsdokumentet KLAR-ARK-0008 og uavhengig kontroll av F-radene (2026-10-27).** `KLAR-ARK-0008` v1.0 og v1.1 (commit `75e214c`) og v1.2 (commit `3426010`) er laget, med seksjonene A–F, B12 (med detaljer), E (grunnlag for blindtest) og F (JOSS-sjekklista). En uavhengig kontroll (Opus-subagent) av de ti F-radene som i v1.1 stod som OPPFYLT (F14–F21, F23, F25), på HEAD `75e214c`, fant at F14 ikke holdt: README dekker problem og målgruppe (README:9, :11), men ikke forholdet til annet arbeid, som kriteriet krever (K117, `joss_review_criteria.html:277`). F14 er endret til ÅPEN – før frys i v1.2 (grunnen står i raden, ARK-0008 v1.2:167); de ni andre holdt og er uendret. `grep -c "ÅPEN – før frys" docs/KLAR-ARK-0008_*v1.2*` gir 24 (v1.1: 23, v1.0: 25). Åpne ID-er per seksjon i v1.2 («Status per 2026-10-27», linje 186–189): A: A1, A2, A3; B: B9; F: F3, F4, F5, F6, F10, F11, F12, F13, F14, F22, F24, F26, F27 (OPPFYLT 9; F1, F2, F7, F8, F9 ikke vurdert); E: 0a, 0b, 0c (hindrer blindtesten, ikke frysen). Frysen kan ikke starte etter regelen i ARK-0008 (linje 5).

**Utdatert og ikke rettet (observert av kontrollene, 2026-10-27).** Kontrollert med `grep` på HEAD `3426010`; ingen av filene er endret. (1) Raden F27 i `KLAR-ARK-0008` v1.2 (linje 180) kaller KILDE v1.5 «gjeldende»; nyeste er `KLAR-KILDE-0001` v1.6. (2) `CONTRIBUTING.md` lenker til eldre versjoner: `KLAR-LOG-0003` v1.10 (linje 17; nyeste v1.11), `KLAR-ARK-0003` v1.19 (linje 18; nyeste v1.21) og `KLAR-KILDE-0001` v1.3 (linje 19; nyeste v1.6).

**Avvik AV-27: H4 gjennomføres ikke i v1.0 (Eiriks beslutning 2026-10-27).** H4 gjennomføres ikke i v1.0 (Eiriks beslutning 2026-10-27, før noen H4-data er samlet inn). Testmanuset og mønstrene i personvernmotoren er laget av samme forfatter, og målingen ville hatt én leser, så den ville ikke gitt ekstern gyldighet. Ekstern test på spontan dialekttale utenfor NB-Whispers treningsdata gjøres i v1.1 (KLAR-PREREG-0003, NB Tale modul 3). Kategoriene uten naturlige forekomster i H1–H3 er ikke målt på tale i v1.0. Grunnlag: Eiriks beslutning A1 = (b), ordrett «Stopp beslutningsteateret og lever hel ved» = godkjenning av chat-Claudes anbefalinger. H4/EVAL-0009 rapporteres ikke, og tersklene for H4 er ikke prøvd; H1–H3 og tersklene deres er uendret. Det åpne punktet i AV-19 («H4 står åpent til innlesingen er gjort») står ikke lenger åpent. Ført i `KLAR-LOG-0003` v1.12 (ny rad AV-27, linje 33; «testdata sett?»: ja for H1–H3, nei for H4; innledningen sier at H4 ikke gjennomføres i v1.0) og `KLAR-PREREG-0001` v1.24 (avvikspunkt 20, linje 1172; raden AV-27 i oppsummeringstabellen, linje 232, med «ja» for hypotese og datasett og «nei» for primærutfall, terskel, utvalg og analysemetode, begrunnet i «Usikre celler»; «punktene 1–20»). Python-kontroll: 27 AV-ID-er i LOG-0003 v1.12, hver står én gang i tabellen (27 rader, 9 kolonner, bare «ja»/«nei» i de seks endrer-kolonnene); ingen mangler og ingen ekstra.

**Eiriks beslutninger A1–A3 og frysregelen (2026-10-27).** Ordrett: «Stopp beslutningsteateret og lever hel ved» = godkjenning av chat-Claudes anbefalinger. A1 = (b) for v1.0: H4 gjennomføres ikke; blindtesten på NB Tale modul 3 (KLAR-ARK-0008, seksjon E) blir v1.1 med egen preregistrering (KLAR-PREREG-0003), og E-punktene står åpne for v1.1 (AV-27). A2 = AGPL-3.0-or-later for egen kode, med kommersiell lisens fra rettighetshaveren som tillegg. A3 = full historikk publiseres, med lisenserklæring for hele historikken. Frysregelen: F-rader som bare kan oppfylles ved selve publiseringen (offentlig repo, lisens synlig på GitHub) merkes «oppfylles ved publisering» og unntas; alle andre må være OPPFYLT før publisering. B9 = LUKKET (bortfaller, fordi H4 ikke gjennomføres i v1.0). Merk: anbefalingen for A1 i kolonnen «Anbefaling» i KLAR-ARK-0008 v1.0–v1.2 var (a); den godkjente er chat-Claudes anbefaling i chat 2026-10-27, (b) for v1.0 med blindtesten som v1.1. Ført i `KLAR-ARK-0008` v1.3: A1–A3 LUKKET med dato og ordlyd, frysregelen i regelen øverst, B9 LUKKET, F3 «oppfylles ved publisering» (eneste F-rad som bare kan oppfylles ved publiseringen; F4 og F10 kan oppfylles i det private repoet og står åpne), E utsatt til v1.1, C og D oppdatert; `grep -c "ÅPEN – før frys"` på v1.3 gir 17 (v1.2: 24); A: LUKKET 7; B: LUKKET 12; F: OPPFYLT 9, ÅPEN – før frys 12, oppfylles ved publisering 1, «–» 5. `KLAR-ARK-0006` v1.9: steg 13–14 utgår i v1.0 (AV-27), v1.1 = blindtest på NB Tale modul 3, A1–A3 avgjort. Merkene for A1 er erstattet i `README.md` (på plass, ingen nye linjer; lenkene peker på de nye versjonene), `KLAR-ARK-0004` v1.2, `KLAR-ARK-0005` v1.3 og `KLAR-ARK-0009` v0.3; merkene for A2 og A3 står (føres i en senere runde). `LICENSE`, `pyproject.toml:11` og `CITATION.cff:7` sier fortsatt Apache-2.0 (HEAD `b0e8c47`). `source scripts/miljo.sh && .venv/bin/python scripts/sjekk_kilder.py`: «påstander per status: delvis: 7, ikke funnet: 3, motsagt: 1, verifisert: 211», exit 0. `.venv/bin/python -m pytest -q -m 'not tung' tests/test_nummerregister.py tests/test_manus.py`: 18 passed. Ingen nettkall.

**Avvik AV-28: kodeendringer etter `testkjoring-v5`; ny kodetagg `testkjoring-v6` (2026-10-27).** Commit `57dedaf77113300dc1dcbc64f4e5847712b1fc7c` (2026-10-27T21:34:00+01:00): cache-stier per segmentering (`<navn>_inaseg.jsonl`/`<navn>_inavamos.jsonl`, `eval/dev/felles.py:182–200`; eldre cacher uten suffiks er laget med inaVAMOS og leses bare med `inavamos` når `_inavamos`-fila mangler; `ARKIVKLARERING_CACHE_SUFFIKS` er fjernet), datarot `ARKIVKLARERING_DATA` (`arkivklarering/miljo.py:40–57`, `scripts/miljo.sh:9–17`; standard `/Volumes/Vault/arkivklarering` når Vault er montert og mappen finnes, ellers `${XDG_DATA_HOME:-~/.local/share}/arkivklarering`; `ARKIVKLARERING_EVAL_DATA` for evalueringsdataene) og tester som går i rent miljø (`tests/conftest.py`, ny `tests/test_cache_sti.py`). Kodetagg `testkjoring-v6`: `git rev-parse testkjoring-v6 testkjoring-v6^{commit}` gir `33338900d9079d17355e470bb6517ca5c60cdeb3` og `57dedaf77113300dc1dcbc64f4e5847712b1fc7c`; `testkjoring-v1`–`v5` beholdt; `git diff --quiet h4-rigg-v3 testkjoring-v6 -- arkivklarering/h4_innlesing.py arkivklarering/h4_side.html scripts/rigg_manus.py` gir 0. Påstanden om at ingen utregning for H1–H3 er endret, er kontrollert med `git diff testkjoring-v5 testkjoring-v6 -- eval/dev scripts/rapporter_intervaller.py`: `scripts/rapporter_intervaller.py` har ingen diff; `eval/dev` har 12 filer (105 linjer inn, 51 ut), med bare stikonstanter flyttet til `miljo.DATA`/`miljo.EVAL_DATA` (11 filer, med import av `miljo`), valg av cache-filnavn med `felles.cache_sti` (`kjor_flaggoverlevelse_ord.py`, `kjor_syntetisk.py`, `kjor_degradering.py`, `diagnose_tomt_raalag.py`, `sammenlign_inaseg_dev.py`), samme regel i `felles.gjenbruk_normalisert`, stopp med melding ved manglende cache i `diagnose_tomt_raalag.py`, `os.environ.get("ARKIVKLARERING_EVALDATA") or …` i `kjor_dev.py` (en tom verdi gir nå standardstien), og docstringer og kommentarer (i `kjor_flaggoverlevelse_dev.py` bare en kommentar). WER, flaggscoring (`evaluer`, `omtaler`, `streng_treff`), Wilson, utvalg, bootstrap og tersklene er ikke berørt. Med `inavamos` (H1 og H2 i `kjor_testdel.sh`) leser H2 samme cache som i testkjøringen (`eval-data/ord_npsc_test.jsonl`; ingen cache med suffiks finnes). Ført i `KLAR-LOG-0003` v1.13 (ny rad AV-28, linje 34; «testdata sett?»: ja for H1–H3, nei for H4) og `KLAR-PREREG-0001` v1.25 (avvikspunkt 21, linje 1174; raden AV-28 i oppsummeringstabellen, linje 233, med «nei» i alle seks endrer-kolonnene, og AV-28 analysemetode i «Usikre celler»; «punktene 1–21»). Python-kontroll: 28 AV-ID-er i LOG-0003 v1.13 (AV-01–AV-28 i rekkefølge, 8 kolonner); oppsummeringstabellen i PREREG v1.25 har 28 rader, 9 kolonner, bare «ja»/«nei» i de seks endrer-kolonnene, ingen mangler, ingen ekstra og ingen dubletter; siste avvikspunkt er 21.

**Lisensbyttet: AGPL-3.0-or-later med kommersiell lisens som tillegg, og full historikk (Eiriks beslutninger A2 og A3 2026-10-27).** Beslutningene står i `KLAR-ARK-0008` v1.3 (A2, A3) og er ført som `KLAR-ADR-0020` v1.0 (lisens-agpl, vedtatt 2026-10-27, i nummerregisteret `KLAR-ARK-0003` v1.22). Nettbruk: ett kall, 2026-10-27T20:36:44Z, `curl -sS -L -A 'arkivklarering-kildekontroll (eirik@ecodeco.no)'` mot https://www.gnu.org/licenses/agpl-3.0.txt, HTTP/1.1 200, ingen omdirigering, 34 523 byte, uten gjentak. Råkopien er lagret uendret på Vault som `kilder/gnu_agpl-3.0.txt` (K123, sha256 `0d96a4ff68ad6d4b6f1f30f713b18d5184912ba8dd389f86aa7710db079abcb0`) med hentelogg `kilder/gnu_agpl_hentelogg_2026-10-27.txt`; begge er ført i `kilder/SHA256SUMS` (145 linjer, `shasum -a 256 -c` uten avvik), og utdrag for de nye radene er lagt til i `kilder/kilderegister_utdrag.md`. `LICENSE` er erstattet med en kopi av K123; `cmp` mellom `LICENSE` og K123 gir ingen forskjell. Rettighetshaveren (Copyright 2026 Eirik Botten Nicolaysen, EcoDeco AS) står i `NOTICE` og README, ikke i LICENSE. Endret på plass: `NOTICE` (AGPL-3.0-or-later, kommersiell lisens, NB-Whisper Apache-2.0 og borealis-open-4b/`gemma` lagt til), `pyproject.toml` (`version = "1.0.0"`, `license = "AGPL-3.0-or-later"`, `license-files` uendret), `CITATION.cff` (`version: 1.0.0`, `date-released: 2026-10-27` (settes til publiseringsdatoen ved publisering), `license: AGPL-3.0-or-later`, forfatternavnet delt som i ORCID-posten K122: `family-names: Botten Nicolaysen`, `given-names: Eirik`, og OSF hc83q lagt til ved fbme7), README («## Lisens» med den besluttede ordlyden, tredjepartslisensene, «## Sitering», installasjon og miljø etter AV-28), `CONTRIBUTING.md` og `CHANGELOG.md` (`## [1.0.0] - 2026-10-27`). Nye filer: `LICENSING-HISTORY.md` (lisenserklæring for hele historikken: 105 commits fra `9ff2d1a` til `57dedaf` har samme Apache-2.0-LICENSE, de 16 før har ingen lisensfil; `[PUBLISERINGSDATO]` står til publiseringen) og `.zenodo.json` (samme tittel, versjon, forfatter, lisens, beskrivelse og nøkkelord som `CITATION.cff`; OSF hc83q med relasjonen `isDocumentedBy` og fbme7 med `isDescribedBy`; ingen DOI). Merkene for A2 og A3 er erstattet med avgjort ordlyd i README, `CONTRIBUTING.md`, `KLAR-ARK-0003` v1.22, `KLAR-ARK-0004` v1.3, `KLAR-ARK-0005` v1.4 og `KLAR-ARK-0009` v0.4 (merket UTKAST øverst); sitatene av de gamle merkene i `KLAR-ARK-0008` står. `KLAR-KILDE-0001` v1.7: K123, nye rader GN-01–GN-04 og NW-15, NW-16, og README- og NOTICE-linjene i radene peker på de nye linjene. Tredjepartslisensene er kontrollert mot registerradene: vendor-kopien fra norsk-tale har egen `LICENSE` (Apache-2.0, sha256 `c71d239d…`, samme som K22), NB-Whisper (NW-05, NW-15, NW-16), NB-BERT-base-ner (NB-02), pyannote community-1 (PY-10), borealis-open-4b (LI-15: lisensen `gemma`; navnet «Gemma Terms of Use» står ikke i noen lagret kilde og er ikke brukt), inaSpeechSegmenter (IS-01, MIT for koden; vektlisensen uklar, KLAR-ADR-0019) og inaVAMOS (PG-01, PG-02). Ingen kode er endret.

**Svar på spørsmålet om navnesjekken 27.10 (2026-10-27).** Kjøringen 27.10 (oppføringen «Avvik fra instruks: `scripts/navnesjekk.py` kjørt», v1.41:1481) sendte etter all sannsynlighet 13 oppdiktede etternavn fra `KLAR-MANUS-0002` v1.2 (sha256 `9a3d12d1e2438b09f9fcb6aa43300ace406888732d058e3cbabf70cb0ad963b1`, kontrollert med `shasum -a 256`; manuset linje 3: «Personnavn er oppdiktede») til SSBs navnesøk, de samme som i den dokumenterte kjøringen 26.10: `eval/dev/navnesjekk_manus0002_2026-10-26.json` har manus v1.2 med samme sha256, 26 oppslag og 13 unike etternavn (Aaseth, Bakkelien, Bjerkås, Brekkeslåen, Hovdesæter, Kolstad, Lien, Moen, Oddvollen, Rudisæter, Rustad, Sandbu, Skjelbrekke). Grunnlag: skriptet har ingen argumenter (ingen argparse, `sys.argv` leses ikke; `scripts/navnesjekk.py:39–73`) og leser bare manuset: nyeste `kalibrering/KLAR-MANUS-0002_*.tsv` (`scripts/navnesjekk.py:41`; bare v1.2 finnes på disk) med `kun_struktur=True` (:42); for hver personform slås bare siste ord opp (`form.split()[-1]`, :50), hvert etternavn én gang (:52–53), med `sok()` (:27–36) mot SSB-adressen i :24. Manuset og fila fra 26.10 er uendret siden commit `98c723f` (2026-10-26T21:36:49+01:00); skriptet er endret én gang etter det, i `27c6314` (2026-10-27T04:30:37+01:00), der bare filvalget gikk fra leksikografisk sortering til `evaldata.siste_versjon`, som med én fil på disk velger den samme. Ingen navn fra transkripsjoner eller fra DEV- eller testfasit i datasettene er sendt, fordi skriptet ikke leser andre filer. Det er ikke et brudd på KLAR-ADR-0007, som gjelder behandling av opptak (KLAR-ADR-0007 v1.0:15, i git-historikken; i v1.1:15 står overskriften; ordrett: «All behandling (segmentering, transkripsjon, flagging) kjører lokalt. Lyd sendes ikke til skytjenester eller GitHub.»); ingen lyd og ingen tekst fra opptak ble sendt. Derfor ingen egen AV; avviket fra instruksen er ført i v1.41:1481. Utdatafila fra 27.10 (`eval/dev/navnesjekk_manus0002_2026-10-27.json`) er slettet: den finnes ikke i arbeidstreet, og `git log --all` for stien er tom. Hva som faktisk ble sendt 27.10, kan derfor ikke etterprøves, og «etter all sannsynlighet» står.

**Kontroller etter lisensbyttet og AV-28 (2026-10-27).** Kjørt på HEAD `57dedaf` med de nye filene i arbeidstreet, ikke committet. `source scripts/miljo.sh && .venv/bin/python -m pytest -q -m 'not tung'`: 206 passed, 3 deselected. Samme tester med `env -i` og en ny, tom `ARKIVKLARERING_DATA` (samme `.venv`): 202 passed, 4 skipped, 3 deselected. Innsamling (`--co`): 206 av 209 tester, 3 merket `tung`. `.venv/bin/python scripts/sjekk_kilder.py`: «påstander per status: delvis: 7, ikke funnet: 3, motsagt: 1, verifisert: 217», exit 0 (OSF-adressene hoppes over av `sjekk_kilder.HOPP_OVER` som egne artefakter; gnu.org-adressen har raden K123). `.zenodo.json` er gyldig JSON og `CITATION.cff` gyldig YAML (`json` og `yaml` i `.venv`); tittel, versjon, lisens, beskrivelse, nøkkelord, forfatter, ORCID, tilknytning og OSF-adressene er like i de to. Ikke kjørt: `scripts/navnesjekk.py`, inaVAMOS, tunge jobber, GT, stempling og speil.

**Avvik AV-29: telefonnumrene i manusene byttet til Nkoms fiktivserie før publisering (2026-10-27).** KLAR-MANUS-0002 v1.2 → v1.3 og KLAR-MANUS-0001 v1.1 → v1.2 før repoet publiseres med historikk. Kontroll mot Nkoms liste over nummerserier (KLAR-KILDE-0001, NK-rader) viste at sju av tretten telefonnumre lå i serier Nkom har tildelt en tilbyder og dermed kan tilhøre en abonnent; de øvrige lå i ledige eller blokkerte serier. Alle er byttet til numre i Nkoms serie for TV- og filmproduksjon, 68 05 00 00–68 05 99 99 (blokkert for ordinær bruk). Setningene er ellers uendret. sha256 MANUS-0002: `9a3d12d1e2438b09f9fcb6aa43300ace406888732d058e3cbabf70cb0ad963b1` (v1.2, registrert) → `d71b5b138279f19b116f6f207cb0d1e586b1354d31c2ccb0fe044aaa03ff3003` (v1.3); MANUS-0001: `9857f82c526e550591aa6282392c3247600cbf983ade5af1c46d63c572cc3ee8` → `085e72c9f38b189eb5d66101660ea96f9ee75937d20a93b749a2bdccad443a66`. De gamle versjonene er fjernet fra arbeidstreet og ligger i git-historikken (som numrene, i commitene fra 26.10). H4 gjennomføres ikke i v1.0 (AV-27), så ingen kjørt test bruker MANUS-0002. Hypotese, utvalg, analyse og terskel er uendret. Detaljer: de seks ledige og blokkerte numrene ble byttet i en andre runde samme dag, slik at ingen nummer utenfor 68 05 står igjen (en ledig serie kan tildeles senere); nye numre: MANUS-0001 tel01–tel06 og kom02 68 05 45 67, 68 05 33 44, 68 05 12 34, 68 05 76 54, 68 05 34 56, 68 05 11 22 og 68 05 45 67; MANUS-0002 tel01–tel06 og kom02 68 05 03 21, 68 05 77 12, 68 05 20 46, 68 05 62 09, 68 05 18 73, 68 05 31 85 og 68 05 52 80 (ingen felles nummer mellom manusene, `tests/test_manus.py`). Fila er generert på nytt med `scripts/lag_manus.py` og `scripts/lag_manus2.py`; `diff` mot de committede versjonene (a583a28) viser bare de tre kommentarlinjene øverst og linjene 55–66 og 153–154 (telefon og kom02). Klassifiseringen er gjort lokalt mot den lagrede lista K125 (null oppslag, ingen nummer sendt til noen tjeneste; Nkoms oppslag for enkeltnummer er tatt ut av drift, K126). Samme bytte i `tests/test_personvern.py` (to setninger, også formatet med komma), `tests/test_katalog.py`, `scripts/lag_testlyd.py` og docstringen i `arkivklarering/personvern.py:104` (bare tekst). Nye tester i `tests/test_manus.py`: sha256 for MANUS-0001 v1.2 er låst, og alle telefonnumre i begge manus ligger i 68 05 (14 målelementer). Ført i `KLAR-LOG-0003` v1.14 og `KLAR-PREREG-0001` v1.26 (punkt 22).

**Versjon 1.0.0 i koden (2026-10-27).** `arkivklarering/__init__.py`: `__version__ = "1.0.0"` (var 0.1.0), som i `pyproject.toml`, `CITATION.cff` og `.zenodo.json`. WebVTT-hodet skrives fra `__version__` (`arkivklarering/eksport.py:35`, `WEBVTT - arkivklarering v1.0.0 - <lag>`; var hardkodet «v0.1»); ny test `tests/test_eksport_formater.py::test_versjonen_i_vtt_hodet_er_pakkeversjonen`; eksempelet i README (linje 112) er rettet. Koden (`arkivklarering`, `scripts`, `tests`) er endret etter `testkjoring-v6` (versjon, docstring og telefonnumre i tester og generatorer; ingen analysekode og ingen utregning endret); ny kodetagg settes av Eirik ved commit.

**Maskering og fjerning av eldre versjoner (AV-29, 2026-10-27).** Nye versjoner der numrene er erstattet med «[fiktivt nummer, byttet 2026-10-27, AV-29]» (der teksten gjengir hva som sto eller hva Whisper skrev) eller med et 68 05-nummer (i kode og manus): `KLAR-LOG-0001` v1.43 (denne fila; linje 62, 70, 124–132), `KLAR-EVAL-0008` v1.3 (v1.2 med v1.1 gjengitt i vedlegg A, linje 58 maskert) og `KLAR-KILDE-0001` v1.9 (NK-radene skriver ikke ut numrene eller seriegrensene utenfor 68 05). Fjernet fra arbeidstreet (eksplisitte stier, git-historikken har dem): `docs/KLAR-LOG-0001_arkivklarering_avvik-og-hendelser_v1.28_2026-10-27.md` til og med `…_v1.42_2026-10-27.md` (15 filer), `docs/KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.1_2026-10-26.md` (rådatafila `…_v1.1_2026-10-26.json` har ingen telefonnummer og er beholdt) og `docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.8_2026-10-27.md` (aldri committet; innholdet står i v1.9 med numrene maskert). Hver av v1.28–v1.41 er linje for linje lik begynnelsen av v1.42, bortsett fra linje 1457 (v1.30, v1.31), 1467 (v1.31) og 1469 (v1.33), som ble rettet i senere versjoner; derfor peker «vX:N» i eldre oppføringer og andre dokumenter på samme tekst i v1.43:N. Henvisninger oppdatert i `README.md`, `CONTRIBUTING.md`, `KLAR-KILDE-0001` v1.9, `KLAR-LOG-0003` v1.14, `KLAR-PREREG-0001` v1.26, `KLAR-ARK-0005` v1.5 og `KLAR-EVAL-0008` v1.3. Ikke endret: `KLAR-ARK-0008` v1.4 og `KLAR-ARK-0009` (en annen agent skriver i dem), `KLAR-GT-0001` v1.31 (genereres; lister de fjernede filene til neste generering), `docs/stempler/KLAR-LOG-0002` (stempelloggen fører filnavnene som ble stemplet, og .ots-filene står) og `CHANGELOG.md:15` («LOG v1.35» er proveniensen for en commit). Numrene finnes fortsatt i git-historikken: i manusene t.o.m. `a583a28` (først committet 26.10, `15aaa4a` og `98c723f`), i LOG-0001 v1.28–v1.42, EVAL-0008 v1.1, generatorene, testene og `personvern.py` i commitene før AV-29.

**Kildekontroll: OSI-siden for AGPL-3.0 (2026-10-27).** Nettbruk: ett kall, 2026-10-27T21:33:39Z, `curl -sS -L -A 'arkivklarering-kildekontroll (eirik@ecodeco.no)'` mot https://opensource.org/license/agpl-v3, som svarte HTTP/2 301 til /license/agpl-3.0; omdirigeringen ble fulgt i samme kall (HTTP/2 200, 226 995 byte), uten gjentak og uten innlogging. Råkopien er lagret uendret på Vault som `kilder/osi_license_agpl-3.0.html` (K127, sha256 `d8874d5bf5f566324e83fcfe0c814569ce483355b18bc2e4b519ab41190d71cf`) med hentelogg `kilder/osi_agpl_hentelogg_2026-10-27.txt`; begge er ført i `kilder/SHA256SUMS` (151 linjer, `shasum -a 256 -c` uten avvik). Ny rad OI-01 i `KLAR-KILDE-0001` v1.9 (verifisert): «GNU Affero General Public License version 3 […]Approved: March 3, 2008 […] SPDX short identifier: AGPL-3.0». README (linje 241 og 231) sier nå at lisensen er OSI-godkjent, med lenke og rad.

**Kontroller etter AV-29 (2026-10-27).** Kjørt på HEAD `a583a28` med endringene i arbeidstreet, ikke committet. `source scripts/miljo.sh && .venv/bin/python -m pytest -q -m 'not tung'`: 210 passed, 3 deselected (213 samlet inn). `.venv/bin/python scripts/sjekk_kilder.py`: «påstander per status: delvis: 7, ikke funnet: 3, motsagt: 1, verifisert: 237», exit 0 (KILDE v1.9, 248 rader). `ground_truth.nummerregister()`: ingen varsler (57 nøkler i registeret, 52 på disk); `ground_truth.seksjon_kilder()`: 0 brudd, 0 kildelenker uten rad. Lenkesjekk (Python) av alle markdown-lenker til lokale filer i README.md, CONTRIBUTING.md, CHANGELOG.md og nyeste versjon av hvert dokument under `docs/` og `eval/` (51 filer, 92 lenker): ingen lenke til en fjernet fil; to brutte relative lenker står i `KLAR-ARK-0008` v1.4 (linje 31 og 34, sitert README-tekst med stier relativt til rota; ikke endret her), og to treff i KILDE v1.9 (linje 286 og 360) er HTML- og XML-tagger i sitater, ikke lenker. Dekningssjekk (Python): PREREG v1.26 har én tabellrad per AV-01–AV-29, punktene 1–22 i rekkefølge, hvert punkt er henvist fra tabellen, og «punktene 1–22» står over tabellen; LOG-0003 v1.14 har AV-01–AV-29. Telefonnummerskanning (Python, alle 302 tekstfiler i `git ls-files -co --exclude-standard`; de 264 øvrige er .ots-stempler): 8 siffer tett eller i grupperinger med mellomrom, hardt mellomrom, komma eller bindestrek, med og uten +47/0047. Treff utenfor 68 05: datoer ÅÅÅÅMMDD (NPSC-møtene, 20261026), tall som begynner på 0 eller 1 (finnes ikke som 8-sifrede nummer, NK-01; blant dem den negative testen 12345678), filstørrelser i byte (KLAR-ARK-0007 og LOG-0001:1442), sifferlista `"23456789"` i `personvern.py:116` og årstallslista «2010, 2012» i en negativ test. Ingen av de tretten gamle numrene står i treet (`grep` uten treff). Ikke kjørt: `scripts/navnesjekk.py`, inaVAMOS, Whisper, `scripts/ground_truth.py` (GT genereres ved milepæl).

**Avvik AV-30: kodetaggene `testkjoring-v7` og `testkjoring-v8` (2026-10-27).** Kodetaggene `testkjoring-v7` (`9ded8d8…`, versjon 1.0.0, testdata med fiktive telefonnumre (AV-29), kodesjekk) og `testkjoring-v8` (0224d6db3e9d6900e6f65d4662466e6345b4c17b: VTT-merknaden om musikk under tale rettet etter ADR-0019) etter `testkjoring-v6`. Ingen analysekode for H1–H3 er endret i utregning; riggfilene er byte-identiske med `h4-rigg-v3`. `git rev-parse testkjoring-v7 testkjoring-v7^{commit}` gir `4c5ff2149730aaffa876d0499140273736526e8d` (tag-objekt) og `9ded8d8442753f7ae6677e42207bf12165024bef`; `git log --oneline testkjoring-v6..testkjoring-v7` gir `a583a28`, `010d6c0` og `9ded8d8`. Kodeendringene v6 → v7: versjon 1.0.0 og WebVTT-hodet fra `__version__`, lisensfeltet i `pyproject.toml`, telefonnumrene i manusene, generatorene og testene, en docstring i `personvern.py` og taggen i `kjor_testdel.sh` (15 filer, `git diff --stat`). For `testkjoring-v8` (eiers beslutning 2026-10-27, «Stopp beslutningsteateret og lever hel ved»): `FORSLAG` i `arkivklarering/eksport.py:19–21` (NOTE-linjen i WebVTT og `merknad` i `segments.json`) er endret fra «Tale med musikk under er transkribert og flagget.» til «Tale med musikk under transkriberes bare når segmenteringen merker den som tale; flagget «musikk under tale» lages bare med inaVAMOS (ADR-0019).», fordi inaSpeechSegmenter ikke har `speech+music` og flagget ikke lages (KLAR-ADR-0019 v1.3, «Tale over musikk»; funnet i utdataene fra verifikasjonen under); `scripts/kjor_testdel.sh` kontrollerer `testkjoring-v8`, og `tests/test_kjor_testdel.py` legger taggen v8 i testrepoet, forventer v8 og sletter v8 i «manglende tagg»-testen mens v1–v7 finnes; `_merknad` i `modeller.lock.json` sier at modellstien løses mot datarota (`transkriber.standard_modellsti`) og at det ikke trengs symlink i repoet. Ingen test sjekket den gamle setningen. I tillegg velger `registerfil()` i `scripts/sjekk_kilder.py` nå nyeste `KLAR-KILDE-0001` etter versjonsnummer: med `sorted()` ble `v1.7` valgt foran `v1.10` når `v1.9` var fjernet (funnet i denne runden før `sjekk_kilder.py` ble kjørt; ny test `tests/test_sjekk_kilder.py::test_registerfil_velger_nyeste_versjon_etter_versjonsnummer`). Kontroll: `git diff testkjoring-v6 testkjoring-v7 -- scripts/rapporter_intervaller.py eval` er tom; `git diff --name-only HEAD -- arkivklarering kalibrering tests scripts ':(glob)eval/**/*.py'` i arbeidstreet for v8 gir bare `arkivklarering/eksport.py`, `scripts/kjor_testdel.sh`, `scripts/sjekk_kilder.py`, `tests/test_kjor_testdel.py` og `tests/test_sjekk_kilder.py`; ingen kode under `eval/` eller `scripts/` bruker `FORSLAG` eller `skriv_vtt`; `git diff --quiet h4-rigg-v3 -- arkivklarering/h4_innlesing.py arkivklarering/h4_side.html scripts/rigg_manus.py` gir 0 både på HEAD (`testkjoring-v7`) og i arbeidstreet. Commit-SHA-en for `testkjoring-v8` er `0224d6db3e9d6900e6f65d4662466e6345b4c17b`, tag-objekt `dbec0e302c533ea68e311c71ef11c086e181a897` (`git rev-parse testkjoring-v8 testkjoring-v8^{commit}`, kontrollert 2026-10-27; v1.45 erstatter plassholderen som sto her). Ført i KLAR-LOG-0003 v1.15 (AV-30) og KLAR-PREREG-0001 v1.27 (avvikspunkt 23).

**Verifikasjon av installasjon, funksjon og ytelse fra ren klon (2026-10-27).** En uavhengig verifikatør (egen økt) kjørte README «Installasjon», «Bruk» og «Tester» i en ny klon av `9ded8d8` (`testkjoring-v7`) fra GitHub; klonen lå i `/Volumes/Vault/arkivklarering/tmp/verifikasjon-v1.0/klon` og er slettet etter kjøringen (mappen finnes ikke, kontrollert 2026-10-27). Skriptene og loggene lå i sesjonens scratchpad; v1.45: de er kopiert til `/Volumes/Vault/arkivklarering/reproduksjon/verifikasjon-v1.0/` (ikke i repoet), med `SHA256SUMS` (32 filer ved kopieringen, sha256 av `SHA256SUMS` `a5cb3b384af7949924e36c278826a88a27d056879a0e3fd4e436be9504eddb34`, kontrollert 2026-10-27; 33 filer etter at `f11_steg70-75.log` ble lagt til, se «F11: installasjonsstegene for formattestene i en ny datarot»): `f11_install.sh`/`.log`, `f11_sha256.log`, `f11_innsamling.log`, `f11_pytest_tom.sh`/`.log`, `f12_bruk.sh`/`.log`, `f12_valider.py`/`.log`, `f12_pytest_tung.sh`/`.log`, `f13_intervaller.sh`/`.log` og utdatakatalogene `ut_kjoring1`, `ut_kjoring2`, `ut_personvern`. Tidene er CET. Sammendrag fra loggene:

**F11 (installasjon).** HEAD `9ded8d8` (`git rev-parse --short HEAD` i `f11_pytest_tom.log` og `f12_*.log`). Datarot `ARKIVKLARERING_DATA=/Volumes/Vault/arkivklarering/tmp/verifikasjon-v1.0/data` (ny); `source scripts/miljo.sh` rc=0, og `HF_HOME`, `HF_DATASETS_CACHE`, `PIP_CACHE_DIR`, `TORCH_HOME`, `KERAS_HOME`, `XDG_CACHE_HOME` og `TMPDIR` ble satt under rota (`f11_install.log`, `set -x`). Kommandoene i README:61–68 (på `9ded8d8`) ordrett, med nett, 22:56:39–22:57:40: `uv venv --python 3.13 "$ARKIVKLARERING_DATA/venv" && ln -s "$ARKIVKLARERING_DATA/venv" .venv` rc=0; `VIRTUAL_ENV=$PWD/.venv uv pip install -e ".[test,eval,personvern,eksport,tidsstempel]" "nb_core_news_md @ …"`: «Resolved 93 packages in 8.28s», «Prepared 93 packages in 17.96s», «Installed 93 packages in 420ms», 26,9 s, rc=0; `uv venv --python 3.13 "$ARKIVKLARERING_DATA/venv-inaseg"` rc=0; `VIRTUAL_ENV="$ARKIVKLARERING_DATA/venv-inaseg" uv pip install --require-hashes --no-deps -r requirements-inaseg.lock`: «Resolved 58 packages in 2.31s», «Prepared 58 packages in 30.12s», «Installed 58 packages in 349ms» (blant dem `tensorflow==2.21.0`), 32,9 s, rc=0; `du -sh`: `venv` 990M, `venv-inaseg` 1.6G, `cache` 2.6G. Whisper-modellene ble lagt i den nye datarota som symlenker til de eksisterende filene (kommentaren i `f12_bruk.sh`), ikke lastet ned; `shasum -a 256` (`f11_sha256.log`, 22:57:58) gir `0227866ef47189f79d04347a080c73fcd8267c8e2255da5f77803506ab4ffc7d` for `nb-whisper-large-verbatim.ggml-model.bin` og `0f2f66f22e11a7c7da3c582d8e5c89cb2c0011753ba9c7c9731e320a4ba33e76` for `nb-whisper-large.ggml-model.bin`, begge 3 095 033 483 byte, likt `sha256` og `bytes` i `modeller.lock.json`; rørledningen kontrollerte dem på nytt ved hver kjøring (`ra: … sha256=0227866e…`, `normalisert: … sha256=0f2f66f2…` i `f12_bruk.log`). Innsamling (`f11_innsamling.log`): «210/213 tests collected (3 deselected) in 0.26s», og `-m tung` «3/213 tests collected (210 deselected)» (`test_oppdiktet_tekst.py::test_musikk_stillhet_og_stoy_gjennom_hele_rorledningen`, `test_personvern.py::test_motor_flagger_navn_sted_dato_og_nokkelord`, `test_segment_inaseg.py::test_ekte_runner_pa_rokytest`). Første forsøk i samme logg stoppet: «scripts/miljo.sh: line 26: mount: command not found» og «STOPP: /Volumes/Vault er ikke montert (…/tom)», i et miljø der `mount` (i `/sbin`) ikke var på PATH; `scripts/miljo.sh` er ikke endret (se oppføringen «Kontroller etter AV-30»). Tester med tom datarot (`f11_pytest_tom.log`, 22:58:37–22:59:50): `ARKIVKLARERING_DATA=/Volumes/Vault/arkivklarering/tmp/verifikasjon-v1.0/tom` med `ls -A … | wc -l` = 0, miljo rc=0, `.venv/bin/python -m pytest -q -m 'not tung' -rs`: «206 passed, 4 skipped, 3 deselected in 71.18s», pytest rc=0. De fire som ble hoppet over: `tests/test_diarisering.py:35`, `tests/test_eksport_formater.py:41` og `:48` («ohms.xsd finnes ikke (…/tom/eval-data/ohms/ohms.xsd; ligger under ARKIVKLARERING_DATA/eval-data/ohms, eller sett ARKIVKLARERING_OHMS_XSD)») og `tests/test_eksport_formater.py:91` («IIIF-oppskrift 0219 finnes ikke (…/tom/eval-data/iiif/recept_0219_manifest.json …)»). README har fått installasjonssteg for begge (README:70–74) og for katalogmodellen (README:75).

**F12 (funksjon).** README «Bruk» (README:91–95 på `9ded8d8`) ordrett med datarota over (`f12_bruk.log`, 23:00:27–23:03:59, HEAD `9ded8d8`, miljo rc=0). `scripts/lag_testlyd.py`: «lyd/rokytest.wav: 40.0 s», 1,67 s, rc=0. Kjøring 1, `.venv/bin/arkivklarering lyd/rokytest.wav -o ut/rokytest/` (med katalog og personvern): «segmentering (inaseg): 3 råsegmenter -> 3 (46.5 s)», «ra: 2 cuer (9.1 s)», «normalisert: 2 cuer (8.7 s)», «personvern: ra 0 flagg, normalisert 0 flagg; union 0 flagg (35.1 s)», «katalog: 1 segmentsammendrag, 0 forkastede forslag (14.7 s)»; 124,75 s, største RSS 4 119 609 344 byte, rc=0. Kjøring 2, `… -o ut/rokytest/ --ingen-katalog --ingen-personvern`: segmentering 6,7 s, «ra: 2 cuer (10.2 s)», «normalisert: 2 cuer (8.9 s)»; 35,60 s, rc=0. Den skrev til samme utkatalog som kjøring 1 (README-kommandoen på `9ded8d8`); verifikatøren kopierte utdataene etter hver kjøring. README bruker nå `ut/rokytest_enkel/` (README:102). Personvern: `scripts/lag_testlyd.py --personvern` («lyd/rokytest_personvern.wav: 40.0 s», rc=0) og `… lyd/rokytest_personvern.wav -o ut/rokytest_personvern/`: «ra: 2 cuer (8.9 s)», «normalisert: 3 cuer (8.3 s)», «personvern: ra 6 flagg, normalisert 8 flagg; union 9 flagg (9.3 s)», «katalog: 1 segmentsammendrag, 2 forkastede forslag (4.9 s)»; 48,29 s, rc=0. Alle tre kjøringene laget de seks filene (`.ra.vtt`, `.normalisert.vtt`, `.segments.json`, `.ohms.xml`, `.iiif.json`, `.mmif.json`; `ls -la` i loggen). Validering (`f12_valider.py`, med `arkivklarering.eksport.valider_vtt`, `valider_ohms` (mot `/Volumes/Vault/arkivklarering/eval-data/ohms/ohms.xsd`, sha256 `78e7fe404d7eed05027f165339663a0595f49609f3998ac2e8357c6f0bf9385c` = K34), `valider_iiif`, `valider_mmif` og en feltkontroll av `segments.json`): alle 18 filer «GYLDIG», unntatt `segments.json` fra kjøring 2, «mangler toppnivå ['personvern']», som er riktig med `--ingen-personvern` (`personvern` skrives bare når flagg lages, `arkivklarering/eksport.py:81`; README:121 sier det nå). Segmentene i `rokytest`: `music` 0,0–20,04 s «foreslått klipp», `speech` 20,04–29,86 s «transkriber», `other` 29,86–39,98 s «ingen handling», versjon 1.0.0; `personvern_union` per segment i `rokytest_personvern`: 0, 9, 0. NOTE-linjen i alle VTT-filene sa «Tale med musikk under er transkribert og flagget.» (rettet i `testkjoring-v8`, AV-30). `pytest -m tung` (`f12_pytest_tung.log`, 23:04:28–23:04:55): «3 passed, 210 deselected in 25.76s», pytest rc=0; varighet 14,24 s, 10,31 s og 1,00 s for de tre testene over; største RSS 1 274 871 808 byte.

**F13 (ytelse).** `f13_intervaller.log` (23:01:56–23:01:57, HEAD `9ded8d8`): `.venv/bin/python scripts/rapporter_intervaller.py` på de lagrede resultatfilene; Whisper og inaVAMOS er ikke kjørt. Tallene som stemmer med dokumentene og README:

| måling | kommando (`rapporter_intervaller.py …`) | gjenberegnet | står i |
|---|---|---|---|
| H1a, ra/matchet totalt | `wer eval/test/KLAR-EVAL-0013_…_v1.0_2026-10-27.json …utvalg.json` | 0,127 (0,112–0,144), 252 segmenter, 51 talere | EVAL-0013 v1.3:16 og :36; README:140 |
| H1, ra/matchet bokmål; ra/nn bokmål | samme | 0,111; 0,315 | EVAL-0013 v1.3:17 og :14 |
| H1b, normalisert/matchet totalt | samme | 0,337 (0,305–0,373) | EVAL-0013 v1.3:22 og :37 |
| K1 (normalisert/matchet − ra/matchet) | samme | 0,209 (0,176–0,248) | EVAL-0013 v1.3:41 |
| H2a, union person begge målformer | `flagg eval/test/KLAR-EVAL-0014_…_v1.0_2026-10-27.json` | 346/379, 0,913 (0,880–0,937) | EVAL-0014 v1.4:17 |
| H2b, union sted begge målformer | samme | 172/201, 0,856 (0,800–0,898) | EVAL-0014 v1.4:18; README:141 |
| H2c, union person bokmål | samme | 145/155, 0,935 (0,885–0,965) | EVAL-0014 v1.4:19; README:141 |
| H2, rålag samlet person; sted | samme | 284/379, 0,749; 122/201, 0,607 | EVAL-0014 v1.4:42–43 |
| H3 recall (kombinert, original): nb person, nb sted, nn person, nn sted | `norne eval/test/KLAR-EVAL-0015_…_v1.0_2026-10-27.json …setninger.json` | 1,000 (0,993–1,000), 0,975 (0,953–0,987), 0,982 (0,964–0,991), 0,976 (0,949–0,989) | EVAL-0015 v1.4:15–18 |
| H3 presisjon (kombinert, original), samme rekkefølge | samme | 0,904 (0,878–0,924), 0,811 (0,771–0,844), 0,733 (0,694–0,769), 0,769 (0,720–0,812) | EVAL-0015 v1.4:22–25; README:142 |
| DEV WER NB Samtale validation: ra/matchet, ra/nn, normalisert/matchet, normalisert/nn | `wer eval/dev/KLAR-EVAL-0002_…_v1.1_2026-10-27.json eval/dev/KLAR-EVAL-0003_…_v1.0_2026-10-26.json` | 0,135, 0,248, 0,348, 0,463 (60 segmenter, 33 talere) | README:153 |
| DEV NorNE validation, recall (kombinert): original; små bokstaver | `norne docs/KLAR-EVAL-0005_…_v1.0_2026-10-26.json` | 0,997, 0,970, 0,954, 0,986; 0,715, 0,739, 0,599, 0,504 | README:154 |
| DEV flaggoverlevelse NB Samtale, union samlet | `flagg docs/KLAR-EVAL-0006_…_v1.2_2026-10-27.json` | person 14/17, sted 14/14 | README:155 |
| DEV flaggoverlevelse NPSC, union samlet; nynorsk sted | `flagg docs/KLAR-EVAL-0007_…_v1.1_2026-10-27.json` | person 139/150 (0,927), sted 92/102 (0,902); 22 referanseflagg | README:156 |
| SYNTETISK (EVAL-0008), union alle; e-post | `h4 docs/KLAR-EVAL-0008_…_v1.2_2026-10-27.json` gir `KeyError: 'union'`, rc=1 (fila har ikke h4-formatet); summert i Python fra `resultat.matchet.elementer` i denne runden | 105 + 93 = 198 av 123 + 121 = 244 i både v1.1 og v1.2; e-post 0/12 | README:157 |

Ingen tall avviker. Det som er bekreftet, er analysen av de lagrede utdataene: H1–H3 er de preregistrerte målingene fra testkjøringene (kodetagg `testkjoring-v2`; H1 og H2 segmentert med inaVAMOS, H3 er tekst uten segmentering; `kjoring_meta`-filene i `eval/test/`), og DEV-tallene er fra utviklingsarbeidet. H1 og H2 er ikke kjørt på nytt: de ble segmentert med inaVAMOS (bare forskning, brukes ikke lenger, AV-25 og AV-26), og en ny kjøring med standardsegmentøren (inaSpeechSegmenter) ville vært en annen måling. H3 er heller ikke kjørt på nytt. README («Resultater», «Utviklingsresultater», den engelske delen) og KLAR-ARK-0009 (da v0.7; nyeste nå v0.9) sier dette nå, uten påstand om at rørledningen i v1.0 gir tallene.

**Kontroller etter AV-30 (2026-10-27).** Kjørt på HEAD `9ded8d8` med endringene for `testkjoring-v8` og de nye versjonene i arbeidstreet, ikke committet. `source scripts/miljo.sh && .venv/bin/python -m pytest -q -m 'not tung'`: 211 passed, 3 deselected (`--co`: 211/214; før `scripts/sjekk_kilder.py` ble rettet: 210 passed, 3 deselected). `.venv/bin/python scripts/sjekk_kilder.py`: «påstander per status: delvis: 7, ikke funnet: 3, motsagt: 1, verifisert: 237», exit 0, med `registerfil()` = KILDE v1.10. `ground_truth.nummerregister()` og `ground_truth.seksjon_kilder()`: ingen varsler. Dekningssjekk (Python): PREREG v1.27 har én tabellrad per AV-01–AV-30 (30 rader, 9 kolonner, bare «ja»/«nei» i de seks endrer-kolonnene), punktene 1–23 i rekkefølge, AV-30 henvist til punkt 23, og «punktene 1–23» står over tabellen; LOG-0003 v1.15 har AV-01–AV-30; `git grep -o 'AV-[0-9][0-9]'` pluss de nye filene gir 30 ulike ID-er, ingen mangler i tabellen. Referanser i KLAR-ARK-0009 v0.7 (Python + pandoc 3.10): 39 siterte nøkler = 39 rader i referansetabellen = 39 i `paper.bib`; de 37 K-nøklene har samme URL i KILDE v1.10; `pandoc … --citeproc --bibliography paper.bib` rc 0 uten advarsler; `sjekk_kilder.urler_uten_rad([ARK-0009 v0.7, README.md, LOG-0001 v1.44])` = `[]`. README har 264 linjer som før, og README-linjene KILDE peker på (3, 11, 22, 49, 64, 164, 188, 227, 235, 241, 248, 249) har samme innhold i starten av linjen som på HEAD; linje 70–109 har flyttet seg. Lenkesjekk (Python) av lokale markdown-lenker i README.md, CONTRIBUTING.md, CHANGELOG.md, NOTICE, CITATION.cff, .zenodo.json, LICENSING-HISTORY.md, paper.bib og nyeste versjon av hvert dokument under `docs/` og `eval/` (56 filer, 91 lenker): ingen lenke til en fjernet fil; de to brutte relative lenkene i KLAR-ARK-0008 (da v1.5, linje 31 og 34, sitert README-tekst; v1.5 er fjernet fra arbeidstreet, nyeste nå v1.8) står som før. `grep -c "ÅPEN – før frys"` i KLAR-ARK-0008 v1.5 = 5 (regelen, innledningene til B og F og to linjer i statuslista); ingen rad har statusen. Fjernet fra arbeidstreet (eksplisitte stier; git-historikken har dem): `docs/KLAR-ARK-0008_arkivklarering_avklaringer-foer-frys_v1.4_2026-10-27.md`, `docs/KLAR-ARK-0009_arkivklarering_artikkelutkast-joss_v0.6_2026-10-27.md`, `docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.9_2026-10-27.md`, `docs/KLAR-LOG-0001_arkivklarering_avvik-og-hendelser_v1.43_2026-10-27.md`, `docs/KLAR-LOG-0003_arkivklarering_avvikstabell_v1.14_2026-10-27.md` og `docs/KLAR-PREREG-0001_arkivklarering_testdeler_v1.26_2026-10-27.md`. Ikke rettet (observert): `scripts/miljo.sh:26` krever `mount` på PATH (F11); `scripts/ground_truth.py:141` og `scripts/verifiser_uendret.py:51` velger nyeste fil med leksikografisk `sorted()`, som `sjekk_kilder.py` gjorde (i dag uten feil, fordi versjonene de leser, har samme antall sifre); KLAR-ARK-0004 v1.3:8 nevner fortsatt kodetagg `testkjoring-v6`. Ikke kjørt: inaVAMOS, Whisper, `scripts/navnesjekk.py`, `scripts/ground_truth.py` som helhet (GT genereres ved milepæl); nett ikke brukt.

**Rettinger etter uavhengig port før frys (2026-10-27).** En uavhengig port fant 26 funn i dokumentasjonen på HEAD `79e1352` (main; kode = `testkjoring-v8`, `0224d6d`, tag-objekt `dbec0e3`; ren arbeidskopi ved start). Funn 2–26 er rettet i denne runden uten kodeendring (ingen fil under `arkivklarering/`, `kalibrering/`, `tests/` eller `scripts/` er endret, så ingen ny kodetagg). Funn 1 (git-historikken: eldre versjoner av manusene har de gamle telefonnumrene, AV-29) rettes ikke; KLAR-ARK-0005 v1.6:46 og :89 sier nå at publiseringen gjelder de gjeldende versjonene i treet og at eldre versjoner i historikken har de gamle numrene, uten å si at historikken er trygg. Nye versjoner (de forrige er fjernet fra arbeidstreet med eksplisitte stier, `git rm` gjøres av Eirik): KLAR-ARK-0001 v1.8 (§ 1 «foreslår hva et menneske må klarere», § 2 og § 5 etter koden, `-nt`/`<|nocaptions|>` i § 3), KLAR-ARK-0003 v1.23 (PREREG-0001 registrert, EVAL-0009 reservert men H4 utgår, MANUS-0002 v1.3), KLAR-ARK-0004 v1.4 (tittel, repo-status, `testkjoring-v8`, NOTICE L14–16 og L18–20), KLAR-ARK-0005 v1.6 (publiseringen gjelder gjeldende manusversjoner; RFC-kilder; H4 ikke gjennomført), KLAR-ARK-0006 v1.10 (steg 15 og 21, merknad om (d) og A7, «v1.0 har ingen»), KLAR-ARK-0008 v1.6, KLAR-ARK-0009 v0.8 (OHMS «tested against», `<|nocaptions|>`, `testkjoring-v8` i vedlegg B), KLAR-KILDE-0001 v1.11, KLAR-LOG-0003 v1.16 (AV-19 lukket av AV-27), denne fila, og KLAR-ADR-0004 v1.3 (`speech+music` bare med inaVAMOS), -0007 v1.1 (modellene som lastes ned), -0008 v1.3 og -0012 v1.3 («ordnes etter risiko» er plan; `arkivklarering/personvern.py:223` og `:321` sorterer etter tid), -0009 v1.1 (IIIF implementert), -0014 v1.1 (norsk-tale Apache-2.0, arkivklarering AGPL-3.0-or-later), -0015 v1.1 (datarot med fallback, AV-28) og -0019 v1.4 (H4 gjennomføres ikke i v1.0). Endret på plass: README.md (linje 109: 15 filer validert med `eksport.valider_vtt/ohms/iiif/mmif` og feltkontroll av de tre `segments.json`; linje 130: testtallene på `79e1352` og stegene for formattestene; lenkene), CHANGELOG.md (linje 10 og 26), CONTRIBUTING.md (lenkene) og LICENSING-HISTORY.md (linje 11: `testkjoring-v7` og `-v8` etter lisensbyttet). Tekstene som sier at repoet er privat og registreringene under embargo, er ikke endret; de står som sjekkliste i KLAR-ARK-0008 v1.6, D4.

**Bevis for F11–F13 flyttet fra scratchpad til Vault (2026-10-27).** Loggene fra verifikasjonen fra ren klon er kopiert til `/Volumes/Vault/arkivklarering/reproduksjon/verifikasjon-v1.0/` med `SHA256SUMS`. Kontroll før endringen: `SHA256SUMS` hadde 32 linjer, `shasum -a 256 -c SHA256SUMS` uten avvik, og `shasum -a 256 SHA256SUMS` = `a5cb3b384af7949924e36c278826a88a27d056879a0e3fd4e436be9504eddb34` (som oppgitt). KLAR-ARK-0008 v1.6 (F11–F13, «Til Eirik») og linje 1526 her viser nå dit.

**F11: installasjonsstegene for formattestene i en ny datarot (2026-10-27).** Nett brukt bare til dette og til RFC-hentingen under. Skript i sesjonens scratchpad, logg `f11_steg70-75.log` i `/Volumes/Vault/arkivklarering/reproduksjon/verifikasjon-v1.0/` (sha256 `203fddacc5e10dea145d52d999bc75e8b581c35b59a90f37fb897ae9d205a0ac`, lagt til i `SHA256SUMS`, som nå har 33 linjer og sha256 `f61c21bf5d82808e6a880fd4ca168f30a2eebe49d34da2555be1820358a7ff80`; `shasum -a 256 -c` uten avvik). Kjørt 2026-10-27 23:58:52–23:58:56 (CET; loggens «## dato» og «## slutt») på HEAD `79e1352` med ren arbeidskopi (`git status --short` tom i loggen). Ny datarot `/Volumes/Vault/arkivklarering/tmp/f11-steg/` (0 filer ved start; slettet etterpå med eksplisitt sti). Før stegene: `ARKIVKLARERING_DATA=<rota> .venv/bin/python -m pytest -q -m 'not tung' -rs tests/test_eksport_formater.py tests/test_diarisering.py` (med `ARKIVKLARERING_EVAL_DATA`, `ARKIVKLARERING_OHMS_XSD` og cache- og tmp-variablene fjernet fra miljøet) gir «12 passed, 4 skipped», hoppet over: `tests/test_eksport_formater.py:41`, `:48`, `:91` og `tests/test_diarisering.py:35`. Stegene i `README.md:71–75` ordrett etter `source scripts/miljo.sh` (rc=0): `curl -fL --create-dirs -o …/eval-data/ohms/ohms.xsd https://web.archive.org/web/20240830153336id_/https://www.weareavp.com/nunncenter/ohms/ohms.xsd` rc=0; `shasum -a 256 -c` «OK» (`78e7fe404d7eed05027f165339663a0595f49609f3998ac2e8357c6f0bf9385c`, K34); `git clone --depth 1 https://github.com/IIIF/cookbook-recipes …/tmp/cookbook-recipes` rc=0 (HEAD `870bcfbcfaf47df9ecff49023db876c17d35cb51`); `cp …/recipe/0219-using-caption-file/manifest.json …/eval-data/iiif/recept_0219_manifest.json` rc=0 (sha256 `746e756163dc21364c1d924a16423082099fa8db108c14eb6651aab6866be995`, samme som kopien på Vault); `ollama pull hf.co/NbAiLab/borealis-open-4b-gguf:Q4_K_M` «success» rc=0 (modellen fantes, manifestet ble kontrollert). Etter stegene: samme pytest-kommando med `-rA` gir «16 passed», blant dem de fire: `test_ohms_xml_er_gyldig_mot_xsd`, `test_ohms_xml_ugyldig_avvises`, `test_iiif_validatoren_godtar_den_offisielle_oppskriften` og `test_ohms_transcript_har_talermerke_og_validerer`. Stegene virket som README sier i første runde, så README er ikke endret (bare testtallene i linje 130). Kjøringen ble gjort to ganger (den første loggen hadde terminalens fargekoder fra `ollama pull`); mappen fra første kjøring ble slettet før andre, og loggen er fra andre kjøring. Kontroll av hele samlingen i denne runden (ikke i loggsettet): med en ny, tom rot «207 passed, 4 skipped, 3 deselected», og med `ohms.xsd` og oppskrift 0219 kopiert inn fra Vault (samme sha256) «211 passed, 3 deselected»; rota (`/Volumes/Vault/arkivklarering/tmp/tomrot-kontroll/`) er slettet.

**Kildekontroll: RFC 2606 og RFC 6761 (2026-10-27).** Nettbruk: ett kall per RFC, 2026-10-27T23:07:11Z, `curl -sS -L -A 'arkivklarering-kildekontroll (eirik@ecodeco.no)'` mot https://www.rfc-editor.org/rfc/rfc2606.txt (HTTP/2 200, 8 008 byte) og https://www.rfc-editor.org/rfc/rfc6761.txt (HTTP/2 200, 28 862 byte), uten omdirigering, gjentak eller innlogging. Råkopiene er lagret uendret på Vault som `kilder/rfc2606.txt` (K128, sha256 `b6869c8984701701bc2e6973b6ffc750d497f845cc1a65a106e9301590a13ab0`) og `kilder/rfc6761.txt` (K129, sha256 `549f6635f34eb0da627568657401f0115e8e33c2ba1ba7e37bf14ab27651339e`) med hentelogg `kilder/rfc_hentelogg_2026-10-27.txt`; alle tre er ført i `kilder/SHA256SUMS` (`shasum -a 256 -c` uten avvik). Nye rader RF-01–RF-04 i KLAR-KILDE-0001 v1.11 (verifisert) dekker påstanden i KLAR-ARK-0005 v1.6:46 og :89: `.test` og `.example` (RFC 2606, avsnitt 2; RFC 6761, avsnitt 6.2), `example.com`, `example.net`, `example.org` (RFC 2606, avsnitt 3) og navn under dem, som `lag.example.org` (RFC 6761, avsnitt 6.5). E-postdomenene i KLAR-MANUS-0001 v1.2 og KLAR-MANUS-0002 v1.3 (`grep`): `example.com`, `example.net`, `example.org`, `lag.example.org`, `eksempel.test`, `bygdemuseet.example` og `lokalradio.example`.

**Kontroller etter rettingene før frys (2026-10-27).** Kjørt på HEAD `79e1352` med endringene fra denne runden i arbeidstreet, ikke committet. `source scripts/miljo.sh && .venv/bin/python scripts/sjekk_kilder.py`: «påstander per status: delvis: 7, ikke funnet: 3, motsagt: 1, verifisert: 241», exit 0 (KILDE v1.11, 252 rader; +4 verifisert, RF-01–RF-04). `.venv/bin/python -m pytest -q -m 'not tung'` med datarota på Vault: «211 passed, 3 deselected», rc 0. `ground_truth.nummerregister()`: ingen varsler; `ground_truth.seksjon_kilder()`: 0 brudd, 0 kildelenker uten rad. Lenkesjekk (Python) av lokale markdown-lenker i README.md, CONTRIBUTING.md, CHANGELOG.md, NOTICE, CITATION.cff, LICENSING-HISTORY.md, .zenodo.json og nyeste versjon av hvert dokument under `docs/` og `eval/` (54 filer, 94 lenker): ingen lenke til en fjernet fil; de tre relative lenkene i KLAR-ARK-0008 v1.6 (linje 31 og 34, sitert README-tekst med stier relativt til rota; v1.5 hadde to, og v1.6:31 fikk en ny `](../NOTICE)`) står. README har fortsatt 264 linjer; bare linje 109 og 130 og lenkene er endret, så README-linjene KILDE peker på, er uendret (kontrollert rad for rad). Fjernet fra arbeidstreet (eksplisitte stier; git-historikken har dem): `docs/KLAR-ARK-0001_arkivklarering_arkitektur_v1.7_2026-10-27.md`, `docs/KLAR-ARK-0003_arkivklarering_nummerregister_v1.22_2026-10-27.md`, `docs/KLAR-ARK-0004_arkivklarering_modellkort_v1.3_2026-10-27.md`, `docs/KLAR-ARK-0005_arkivklarering_datablad-manus_v1.5_2026-10-27.md`, `docs/KLAR-ARK-0006_arkivklarering_veikart_v1.9_2026-10-27.md`, `docs/KLAR-ARK-0008_arkivklarering_avklaringer-foer-frys_v1.5_2026-10-27.md`, `docs/KLAR-ARK-0009_arkivklarering_artikkelutkast-joss_v0.7_2026-10-27.md`, `docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.10_2026-10-27.md`, `docs/KLAR-LOG-0001_arkivklarering_avvik-og-hendelser_v1.44_2026-10-27.md`, `docs/KLAR-LOG-0003_arkivklarering_avvikstabell_v1.15_2026-10-27.md`, `docs/adr/KLAR-ADR-0004_arkivklarering_segmentregel_v1.2_2026-10-26.md`, `docs/adr/KLAR-ADR-0007_arkivklarering_lokal-prosessering_v1.0_2026-10-26.md`, `docs/adr/KLAR-ADR-0008_arkivklarering_personvernflagg-presidio-nbbert_v1.2_2026-10-26.md`, `docs/adr/KLAR-ADR-0009_arkivklarering_eksport-webvtt-iiif_v1.0_2026-10-26.md`, `docs/adr/KLAR-ADR-0012_arkivklarering_recall-foran-presisjon_v1.2_2026-10-26.md`, `docs/adr/KLAR-ADR-0014_arkivklarering_vendor-fra-norsk-tale_v1.0_2026-10-26.md`, `docs/adr/KLAR-ADR-0015_arkivklarering_tunge-data-kun-paa-vault_v1.0_2026-10-26.md` og `docs/adr/KLAR-ADR-0019_arkivklarering_inaseg-erstatning_v1.3_2026-10-27.md`. Ikke kjørt: inaVAMOS, Whisper, `scripts/navnesjekk.py`, `scripts/ground_truth.py` som helhet (GT genereres ved milepæl).

## 2026-10-28

**Publiseringsporten er ikke passert; publiseringen er STOPPET (2026-10-28).** Den uavhengige Opus-porten (DEL 4.3) krever null funn. Runde 1 på `79e1352` ga 26 funn; funn 2–26 er rettet i `bafc752` (oppføringen «Rettinger etter uavhengig port før frys» over), funn 1 ble ikke rettet. Runde 2 på `bfe094e` (main, HEAD, ren arbeidskopi) ga 76 funn: 69 i treet og 7 i git-historikken. Tallene er portens; portrapporten ligger ikke i repoet.

- Trefunnene (69): utdaterte versjonshenvisninger og tellinger, noen overpåstander, påstander uten kilderad, én kodeendring (hjelpeteksten til `--ingen-ordtider` i `arkivklarering/cli.py:47`) og 84 utdaterte dokumentversjoner i treet mot regelen i KLAR-ARK-0002. 84 er portens telling; en grov telling i denne runden over `git ls-files` (gruppert på katalog, dokument-ID, navn og filtype, uten `docs/stempler/`) gir 91 eldre versjoner ved siden av en nyere, og forskjellen er ikke avstemt mot portens definisjon. Ingen av de 69 er rettet ennå; de rettes i neste runde uansett hvilket valg Eirik tar om historikken.
- Historikkfunnene (7, klasse g): sju numre i tildelte serier, se K125 og AV-29. Oppslag i denne runden i K125 (`nkom_E164.csv` på Vault): alle sju ligger i serier med status «Tildelt», fire hos Telenor (én fastnett, tre mobil), to hos Telia og én hos Chilimobil. Det er numrene AV-29 (`010d6c0`) byttet til Nkoms fiktiv-serie 68 05; de skrives ikke ut her. Kontroll i git 2026-10-28: ingen av dem står i HEAD eller i arbeidstreet (`git grep` og `grep -r`, også med komma, punktum eller uten mellomrom mellom sifferparene: 0 filer). De står i treet til 111 av de 129 commitene (`git rev-list --all --count`), fra `bc3ac9d` (2026-10-26) til og med `a583a28` (2026-10-27), som er forelderen til `010d6c0`; rotcommiten `2237b0f` har dem ikke. `git log --all -S'<nummer>' --format=%h | wc -l` gir 2–15 commits per nummer; det teller bare commits der antall forekomster av skrivemåten med mellomrom endres, ikke alle commits der nummeret står. Filene i historikken: eldre versjoner av KLAR-MANUS-0001 (justeringsmanus og kategorier) og KLAR-MANUS-0002, KLAR-LOG-0001 v1.8–v1.42 (fra v1.8, ikke fra v1.10 som oppgitt i oppdraget), KLAR-EVAL-0008 v1.0 og v1.1 (linje 13, i Whisper-skrivemåten med komma), testene `tests/test_personvern.py` og `tests/test_katalog.py` (uten mellomrom) og generatorene `scripts/lag_manus.py`, `scripts/lag_manus2.py` og `scripts/lag_testlyd.py`. Taggene `prereg-v1`, `h4-rigg-v3`, `h4-script-v1`, `h4-script-v2` og `testkjoring-v1`–`v6` peker på commits med numrene; `testkjoring-v7` og `testkjoring-v8` gjør det ikke.
- Hvorfor historikkfunnene ikke kan rettes innenfor oppdraget: oppdraget sier at historikken ikke skrives om, at hele historikken publiseres (A3), og at porten krever null funn. De tre kan ikke holde samtidig så lenge numrene står i historikken. Publiseringen (DEL 5: offentlig repo, Zenodo, tag `v1.0.0`, opphevet OSF-embargo) er derfor STOPPET 2026-10-28, og ingen av stegene er tatt. Den venter på Eiriks valg: (a) skrive om historikken (endrer commit-SHA-ene som `prereg-v1`, `testkjoring`-taggene, OTS-stemplene og PREREG og LOG viser til); (b) publisere historikken som den er, med begrunnelse; (c) publisere uten full historikk (endrer A3).
- Historikksøket i DEL 4.4 (lyd, filer fra `lyd/` eller `eval-data/`, tokens, `.env`, nøkler) over alle commits: 0 treff (portens resultat). Stikkprøve i denne runden over alle 129 commits (`git rev-list --all`): 0 stier under `lyd/` eller `eval-data/`, med lydendelse, `.env`, `.pem`, `.key`, `.p12` eller `id_rsa`, og 0 filer med mønstre for Hugging Face-, Anthropic- og GitHub-tokens eller private nøkler. Stikkprøven er ikke portens søk og erstatter det ikke.
- Endret i denne runden: denne fila (v1.46) og KLAR-ARK-0008 v1.7 (D4 og «Til Eirik»); v1.45 og KLAR-ARK-0008 v1.6 er fjernet fra arbeidstreet med eksplisitte stier, og `git rm` gjøres av Eirik. Ingen kode, ingen tagg, ingen commit.

**Portrapportene lagret (2026-10-28).** Runde 1: `/Volumes/Vault/arkivklarering/reproduksjon/port-v1.0/port_runde1_2026-10-27_HEAD-79e1352.md` (sha256 `963d89502c87f5c83ad455d600da67c73c6d06568be4877bc68253ac2d78e7b0`). Runde 2: `/Volumes/Vault/arkivklarering/reproduksjon/port-v1.0/port_runde2_2026-10-28_HEAD-bfe094e.md` (sha256 `bc4d82475d09d9edc16d9f6959c3fb1971100cb247405bb250411350aaf1bd8e`). Begge er hentet ordrett fra agentloggene og ligger bare på Vault, fordi runde 2 har en tabell med de sju telefonnumrene i historikken. Funnlista for treet (69 funn) uten numrene er `KLAR-LOG-0004` v1.0. Fram til nå lå funnlistene bare i økten; det var et brudd på arbeidskøregelen i `CLAUDE.md`.

**Portfunn runde 2 rettet (2026-10-28).** Funnene 1–69 i treet fra den uavhengige porten, runde 2 (`docs/KLAR-LOG-0004_arkivklarering_portfunn-runde2_v1.0_2026-10-28.md`), er rettet i arbeidstreet på HEAD `1c794b4` (main, ren arbeidskopi ved start), ikke committet, unntatt funn 64 (84 utdaterte dokumentversjoner i treet; Eirik gjør det mekanisk etterpå) og funn 66 (GT lister ikke seg selv: rettingen krever en endring i `scripts/ground_truth.py`, som ikke er tillatt i denne runden). Funn 50 (telefon «4 av 14» mot «8/14» i KLAR-EVAL-0008) kan ikke avgjøres mot lagrede data og står som merknad. Per funn: tabellen i oppdragsrapporten og `steg2_rettet.json` i sesjonens scratchpad; kolonnen «rettet (commit)» i KLAR-LOG-0004 fylles ved commit. Rettingene følger KLAR-ARK-0002: hvert versjonert dokument har fått én ny versjon (dato 2026-10-28) med alle rettingene, og den forrige versjonen er fjernet fra arbeidstreet med eksplisitt sti (`git rm` gjøres av Eirik). Frosset tekst er ikke rørt: PREREG v1.8-innholdet (linje 1–199 bortsett fra versjonslinjen 5) og REG-0001.

- Nye versjoner: KLAR-ARK-0001 v1.9, -0002 v1.4, -0003 v1.25, -0004 v1.5, -0005 v1.7, -0008 v1.8, -0009 v0.9; KLAR-KILDE-0001 v1.12; KLAR-LOG-0001 v1.48 (denne fila); KLAR-LOG-0003 v1.17; KLAR-PREREG-0001 v1.28; KLAR-ADR-0004 v1.4, -0005 v1.3, -0012 v1.4, -0013 v1.1, -0016 v1.1, -0018 v1.2, -0019 v1.5; KLAR-EVAL-0001 v1.4 (md, generert på nytt fra JSON v1.3), -0008 v1.4, -0010 v1.3, -0015 v1.5. Endret på plass: `README.md` (264 linjer som før; linje 109, 130, 136, 149, 157, 237, 264 og lenkene), `CONTRIBUTING.md` (lenkene, kodetaggen), `CHANGELOG.md`, `paper.bib` (hodet og note-feltene: KLAR-ARK-0009 v0.9, KLAR-KILDE-0001 v1.12).

- Kilder (funn 43): K130–K134 hentet 2026-10-28T05:51:54Z–05:52:14Z med ett kall per adresse, ærlig UA «arkivklarering-kildekontroll (eirik@ecodeco.no)», uten token: PyPI-metadataene for inaSpeechSegmenter 0.8.0, `remote_utils.py` ved v0.8.0, releasen «interspeech23», VBx-README og LICENSE i VBx-training-recipe; ett kall til (GitHub-API-et `/license` for VBx-training-recipe) ble ikke lagret fordi lisensteksten bare står som base64. Lagret uendret i `/Volumes/Vault/arkivklarering/kilder/` med hentelogg `inaseg_vbx_hentelogg_2026-10-28.txt`, alle seks ført i `kilder/SHA256SUMS` (`shasum -a 256 -c` uten avvik). Nye rader IS-02–IS-06, LI-17 (K46, funn 46) og JO-03 (K116:139, funn 17), alle verifisert. Funn 47 (CLEANUP-guiden og en terskel på 0,5–0,6): parentesen er fjernet fra KLAR-ADR-0012, fordi guiden (K28) setter `default_score = 0.6` som poengsum for spaCy-treff, ikke som terskel.

- Kode (funn 52, AV-32): hjelpeteksten til `--ingen-ordtider` i `arkivklarering/cli.py:47`, kodetaggen i `scripts/kjor_testdel.sh` (fem steder) og `tests/test_kjor_testdel.py` (tag v9 i testrepoet, forventning v9, «manglende tagg»-testen sletter v9 mens v1–v8 finnes). Ingen annen kodeendring. Taggen `testkjoring-v9` lages av Eirik etter commit; commit-SHA-en står som plassholderen 951091e73651967b3a7a3b3aa8dbf2d38b03b660 i KLAR-LOG-0003 v1.17 (AV-32), KLAR-PREREG-0001 v1.28 (punkt 25), KLAR-ARK-0004 v1.5:8 og KLAR-ARK-0009 v0.9 (vedlegg B), og her.

**AV-31: regelen for H4-tersklene i den registrerte teksten stemmer ikke med tabellen (2026-10-28).** Den registrerte teksten (PREREG v1.8; v1.28:76, uendret) sier: «Terskelen er det syntetiske tallet minus 0,15 til 0,35 (mer for kategorier med lite n og for tall som er sårbare for uttale), rundet til nærmeste 0,05.» Tabellen rett over (v1.28:63–64) har person 18/26 (0,69) med terskel ≥ 0,60 (differanse −0,09) og sted 33/40 (0,82) med terskel ≥ 0,70 (−0,12); begge differansene er mindre enn 0,15, så regelen ville gitt lavere terskler (person 0,35–0,55, sted 0,45–0,65). For de andre ti kategoriene ligger differansen mellom −0,16 og −0,33 (e-post har en egen, negativ terskel). Tersklene i tabellen er de registrerte og gjelder; verken teksten eller tabellen er endret. Ingen følger for resultatene: H4 gjennomføres ikke i v1.0 (AV-27), så ingen H4-terskel er prøvd, og H1–H3 bruker ikke disse tersklene. Funnet av den uavhengige publiseringsporten, runde 2 (KLAR-LOG-0004, funn 26), 2026-10-28; ingen avvik dekket det før. Ført i KLAR-LOG-0003 v1.17 (AV-31) og KLAR-PREREG-0001 v1.28 (punkt 24 og raden AV-31).

**AV-32: kodetaggen `testkjoring-v9` (2026-10-28).** Etter `testkjoring-v8` er bare hjelpeteksten til `--ingen-ordtider` i `arkivklarering/cli.py:47` endret. Den sa «(-ml 1 -sow)», men koden ber om DTW-ordtidsstempler med `-nfa -dtw large.v3 -ojf` (`arkivklarering/transkriber.py:158` og `:178`), og `-ml 1 -sow` er forkastet (`arkivklarering/transkriber.py:156`; KLAR-ADR-0012 v1.4:28); DTW-ordtidene beholdes også for rålaget med `-nt` (KLAR-ADR-0017 v1.0:17). Ny tekst: «ikke be om DTW-ordtidsstempler (-nfa -dtw large.v3 -ojf); cuene får da whisper.cpps segmenttider, og union parer på cuenes tidsrom». Teksten vises bare i `--help`; oppførselen er uendret. Kodesjekken i `scripts/kjor_testdel.sh` er flyttet til `testkjoring-v9`, og `tests/test_kjor_testdel.py` er oppdatert etter samme mønster som for v8 (tag v9 i testrepoet, forventning v9, «manglende tagg»-testen sletter v9 mens v1–v8 finnes). Ingen analysekode er endret: ingen fil under `eval/`, ikke `scripts/rapporter_intervaller.py` og ingen funksjon for WER, flaggscoring, Wilson, utvalg eller bootstrap. Riggfilene (`arkivklarering/h4_innlesing.py`, `arkivklarering/h4_side.html`, `scripts/rigg_manus.py`) er ikke endret og skal være byte-identiske med `h4-rigg-v3` (kontrolleres med `git diff --quiet h4-rigg-v3 testkjoring-v9 -- …` etter taggingen). `testkjoring-v9` er commit 951091e73651967b3a7a3b3aa8dbf2d38b03b660; `testkjoring-v1`–`v8` er beholdt. Funnet av den uavhengige publiseringsporten, runde 2 (KLAR-LOG-0004, funn 52), 2026-10-28. Ført i KLAR-LOG-0003 v1.17 (AV-32) og KLAR-PREREG-0001 v1.28 (punkt 25 og raden AV-32).

**Kontroller etter rettingene av portfunn runde 2 (2026-10-28).** Kjørt 2026-10-28 på HEAD `1c794b4` med endringene fra denne runden i arbeidstreet, ikke committet, og med de forrige versjonene fjernet. `source scripts/miljo.sh && .venv/bin/python -m pytest -q -m 'not tung'`: «211 passed, 3 deselected», rc 0. `.venv/bin/python scripts/sjekk_kilder.py`: «påstander per status: delvis: 7, ikke funnet: 3, motsagt: 1, verifisert: 248», exit 0 (KILDE v1.12, 259 rader; +7 verifisert: IS-02–IS-06, LI-17, JO-03). `ground_truth.nummerregister()` og `ground_truth.seksjon_kilder()`: ingen varsler. Dekningssjekk (Python): PREREG v1.28 har én tabellrad per AV-01–AV-32 (32 rader, 9 kolonner, bare «ja»/«nei» i de seks endrer-kolonnene), punktene 1–25 i rekkefølge, AV-31 henvist til punkt 24 og AV-32 til punkt 25, og «punktene 1–25» står over tabellen; linje 1–199 er like v1.27 bortsett fra versjonslinjen (5); LOG-0003 v1.17 har AV-01–AV-32 med 8 kolonner; ID-ene AV-01–AV-32 i dokumentene er 32 ulike. Referanser i KLAR-ARK-0009 v0.9 (Python): 39 siterte nøkler = 39 i `paper.bib`; de 37 K-nøklene har samme URL i KILDE v1.12. Lenkesjekk (Python) av lokale markdown-lenker i README.md, CONTRIBUTING.md, CHANGELOG.md, NOTICE, CITATION.cff, .zenodo.json, LICENSING-HISTORY.md, paper.bib og nyeste versjon av hvert dokument under `docs/` og `eval/` (57 filer, 96 lenker): ingen lenke til en fjernet fil (README:109, :130 og :237 pekte på KLAR-LOG-0001 v1.45 og KLAR-ARK-0008 v1.6, som var fjernet i forrige runde; nå v1.48 og v1.8). Fjernet fra arbeidstreet (eksplisitte stier; git-historikken har dem): `docs/adr/KLAR-ADR-0004_arkivklarering_segmentregel_v1.3_2026-10-27.md`, `docs/adr/KLAR-ADR-0005_arkivklarering_to-lag-nb-whisper-large_v1.2_2026-10-26.md`, `docs/adr/KLAR-ADR-0012_arkivklarering_recall-foran-presisjon_v1.3_2026-10-27.md`, `docs/adr/KLAR-ADR-0013_arkivklarering_katalogmodell_v1.0_2026-10-26.md`, `docs/adr/KLAR-ADR-0016_arkivklarering_talerinndeling-pyannote_v1.0_2026-10-26.md`, `docs/adr/KLAR-ADR-0018_arkivklarering_innspillingsprotokoll-h4_v1.1_2026-10-27.md`, `docs/adr/KLAR-ADR-0019_arkivklarering_inaseg-erstatning_v1.4_2026-10-27.md`, `docs/KLAR-ARK-0001_arkivklarering_arkitektur_v1.8_2026-10-27.md`, `docs/KLAR-ARK-0002_arkivklarering_navnekonvensjon_v1.3_2026-10-26.md`, `docs/KLAR-ARK-0003_arkivklarering_nummerregister_v1.24_2026-10-28.md`, `docs/KLAR-ARK-0004_arkivklarering_modellkort_v1.4_2026-10-27.md`, `docs/KLAR-ARK-0005_arkivklarering_datablad-manus_v1.6_2026-10-27.md`, `docs/KLAR-ARK-0008_arkivklarering_avklaringer-foer-frys_v1.7_2026-10-28.md`, `docs/KLAR-ARK-0009_arkivklarering_artikkelutkast-joss_v0.8_2026-10-27.md`, `docs/KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v1.3_2026-10-27.md`, `docs/KLAR-EVAL-0008_arkivklarering_syntetisk-kjede_v1.3_2026-10-27.md`, `docs/KLAR-EVAL-0010_arkivklarering_degradering-dev_v1.2_2026-10-27.md`, `docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.11_2026-10-27.md`, `docs/KLAR-LOG-0001_arkivklarering_avvik-og-hendelser_v1.47_2026-10-28.md`, `docs/KLAR-LOG-0003_arkivklarering_avvikstabell_v1.16_2026-10-27.md`, `docs/KLAR-PREREG-0001_arkivklarering_testdeler_v1.27_2026-10-27.md`, `eval/test/KLAR-EVAL-0015_arkivklarering_personvern-test_v1.4_2026-10-27.md`. JSON-fila `docs/KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v1.3_2026-10-27.json` står (md-en v1.4 er generert fra den). Ikke kjørt: inaVAMOS, Whisper, `scripts/navnesjekk.py`, `scripts/ground_truth.py` som helhet (GT genereres ved milepæl). Nett brukt bare til K130–K134 (over). Ikke gjort: commit, push, taggen `testkjoring-v9` (Eirik).


**Portfunn runde 3 rettet (2026-10-28).** Runde 3 av publiseringsporten (én Opus-subagent, HEAD `bf48dfe`) ga 16 funn i treet og 0 i (g) personopplysninger; ren installasjon fra README besto. Rapporten ligger på Vault: `/Volumes/Vault/arkivklarering/reproduksjon/port-v1.0/port_runde3_2026-10-28_HEAD-bf48dfe.md` (sha256 `a9bfe2d849988e7ca3f3c9bb0bbb22f8cec6371ce7deacaa5ee5017d1101ffb5`). Funnlista er ført ordrett i KLAR-LOG-0005 (commit `4525e0b`) før noe ble rettet. Rettelser av oppføringene over, som ikke er endret: (1) AV-32 og «Ingen annen kodeendring» er ufullstendige: `git diff testkjoring-v8 testkjoring-v9` endrer også `scripts/ground_truth.py` (3 linjer lagt til: forrige GT-versjon listes ikke; portfunn 66) og `tests/test_ground_truth_wer.py` (testen `test_dokumentlista_viser_ikke_forrige_gt_men_denne_fila`); ført i AV-32 i KLAR-LOG-0003 v1.18 og KLAR-PREREG-0001 v1.29 (punkt 25 og tabellraden). (2) Funn 64 er gjort i `bf48dfe` (77 eldre versjoner tatt ut av treet), og funn 66 er rettet i `testkjoring-v9`; de er ikke utestående. (3) Den mekaniske omskrivingen i `bf48dfe` skrev også om kjøringsmetadataene for EVAL-0013–0015, KLAR-GT-0001 v1.34 (så stempelet ikke lenger holdt) og historisk tekst i KLAR-ARK-0008 v1.8, KLAR-EVAL-0013 v1.3 og KLAR-EVAL-0014 v1.4. Det er satt tilbake i `73f8f62`; sha256 for GT v1.34 er igjen `a098e469a109…`, som stempelet. (4) Kontrollen nederst i v1.48 («211 passed») ble kjørt før den nye testen. På `testkjoring-v9`: innsamling 212 av 215 (3 `tung`); med datarota på Vault 212 bestått; med tom `ARKIVKLARERING_DATA` 208 bestått og 4 hoppet over. Øvrige rettinger (KLAR-LOG-0005, funn 3, 4 og 6–16): nye versjoner KLAR-ARK-0001 v1.10, -0002 v1.5 (unntakene fra versjonsregelen og merkingen «(i git-historikken)»), -0003 v1.26, -0004 v1.6, -0005 v1.8, -0008 v1.9, -0009 v0.10, KLAR-KILDE-0001 v1.13, KLAR-LOG-0003 v1.18, KLAR-PREREG-0001 v1.29, KLAR-ADR-0004 v1.5, -0019 v1.6 og KLAR-EVAL-0010 v1.4; `README.md` (testtallene, AV-01–AV-32), `CHANGELOG.md`, `paper.bib` (forfatternavnet) og `CONTRIBUTING.md` (lenkene) endret på plass. Ingen kode endret.

**AV-33: kodetaggen `testkjoring-v10` og mekanisk pekersjekk (2026-10-28).** Kontrollen av restfunnene etter runde 3 (én Opus-kontroll, kun lesing, HEAD `5eb46cc`) ga 7 restfunn (KLAR-LOG-0005, «Kontroll etter retting»; rapporten på Vault: `reproduksjon/port-v1.0/kontroll_runde3_2026-10-28_HEAD-5eb46cc.md`). Eirik besluttet 2026-10-28 at de rettes og kontrolleres mekanisk, uten ny Opus-runde. Rettet i `efce3f4`: de 7 restfunnene, versjonslinjene :3 i KLAR-ARK-0004 og -0005, og skilletegnet i cellen i KLAR-LOG-0003; i tillegg alle brudd som `scripts/sjekk_pekere.py` fant. Skriptet fant også at KLAR-ARK-0008 v1.9:219 nevnte KLAR-ARK-0009 v0.5 som fjernet fra treet og i git-historikken; v0.5 ble aldri committet (`git log --all`: v0.4 og v0.6–v0.10), og teksten er rettet. Unntak i skriptet ut over oppdragets liste (LOG-serien, CHANGELOG, versjonsnotatene i hodet): kodeblokker; JSON-rådata fra kjøringer, eldre versjoner som står etter unntaket i KLAR-ARK-0002 og den registrerte teksten i PREREG (før «Avvik etter registrering») er unntatt bare fra merkeregelen, fordi de ikke kan endres; KLAR-GT-0001 er generert og stemplet, og der gjelder bare linjeregelen. Uten git-historikk (ett commit, som i det offentlige repoet) prøves bare merkeregelen og linjeregelen for filer i treet. Funn 8: `git diff --stat testkjoring-v8 testkjoring-v9 -- arkivklarering kalibrering tests scripts` gir «5 files changed, 27 insertions(+), 9 deletions(-)», ført i KLAR-LOG-0003 v1.19:38. Kodetaggen `testkjoring-v10` = `efce3f443ecbd27ecf72e067ffc71bb0c3391ae1` (tag-objekt `42cd449cae51e4bafc9e8c164cf536c759a1b27c`), AV-33. Kontroller på `testkjoring-v10`: `python3 scripts/sjekk_pekere.py` gir «0 brudd i 95 filer»; innsamling 216 av 219 (3 `tung`); med datarota på Vault 216 bestått; med tom `ARKIVKLARERING_DATA` 212 bestått og 4 hoppet over; `scripts/sjekk_kilder.py` uendret (verifisert 248, delvis 7, ikke funnet 3, motsagt 1). Tillegget `[tidsstempel]` (opentimestamps-client 0.7.2) er installert i `.venv` med `uv pip install -e '.[tidsstempel]'`; `.venv/bin/ots verify` leser stemplene, men full verifisering mot Bitcoin krever en lokal Bitcoin-node.

**AV-34: A3 endret (2026-10-28).** Eiriks beslutning 2026-10-28, ordrett: «A3 er endret (Eiriks beslutning 2026-10-28): offentlig repo fra rent tre, full historikk i tilgangsstyrt deponering». Det offentlige repoet `avalyset/arkivklarering-public` lages fra et rent tre (én commit), og hele git-historikken deponeres som `git bundle --all` på Zenodo med begrenset tilgang og tilgang på forespørsel. Begrunnelse: «så åpent som mulig, så lukket som nødvendig»; omskriving ville brutt beviskjeden til PREREG og stemplene; numrene (AV-29) publiseres ikke. Ført i KLAR-LOG-0003 v1.21 (AV-34), KLAR-PREREG-0001 v1.32 (punkt 27), KLAR-ARK-0008 v1.12 (A3), KLAR-ADR-0020 v1.2, KLAR-ARK-0005 v1.10 (datablad), KLAR-ARK-0009 v0.13, KLAR-ARK-0006 v1.12, KLAR-ARK-0003 v1.27, `LICENSING-HISTORY.md`, `README.md` og `CHANGELOG.md`. DOI for deponeringen står som «DOI 10.5281/zenodo.23723450» til den er kjent.

**Tilgangsstyrt historikk deponert (2026-10-28, steg 4.3–4.5).** `git bundle create arkivklarering_full-historikk_2026-10-28_e7ee2fcbcf99.bundle --all` av det private repoet på HEAD `e7ee2fcbcf998da55d1b0a287de0410dae7e155c` (commit «Steg 4.2: A3 endret (AV-34) …»): `git bundle verify` sier «The bundle records a complete history»; 27 refs (`git bundle list-heads`), 145 commits (`git rev-list --count --all`), 14 tagger; størrelse 3 236 822 byte; sha256 `9c8ddf34c53b2aae7feeaa5cd972d98fcc2e342d917895f44f66383f5a65cf0f`; md5 `ac79e07d52202a99b12ace9fb7592288`. Siste commit i bundlen: `e7ee2fcbcf998da55d1b0a287de0410dae7e155c` (`refs/heads/main` og `refs/remotes/origin/main`). OTS-stemplet med `.venv/bin/ots stamp` (stempelfil `arkivklarering_full-historikk_2026-10-28_e7ee2fcbcf99.bundle.ots`, sha256 `bade879e9ba4a7842966dffd0a8da6596d7cf6be4c5c02e159de1c83af7a56e8`; `ots info` viser fil-sha256 lik bundlen). Kopi på Vault: `/Volumes/Vault/arkivklarering/reproduksjon/historikk/` (bundle, .ots og `SHA256SUMS`). Zenodo-posten «arkivklarering – full git-historikk (tilgangsstyrt)» er publisert 2026-10-28 i den innloggede økten (API-et med øktens CSRF-token, ingen API-token): https://zenodo.org/records/23723450, DOI 10.5281/zenodo.23723450 (konsept-DOI 10.5281/zenodo.23723449); posten er offentlig, fila begrenset (`access.files = restricted`), lisens AGPL-3.0-or-later, tilgang på forespørsel slått på for brukere og gjester, med vilkårstekst; md5 for den opplastede fila er lik den lokale. Uten innlogging gir `https://zenodo.org/api/records/23723450/files` HTTP 403, og nedlastingslenken sender til innlogging (302 til `/login/`). Metadataene oppgir innhold, sha256, siste commit-SHA, at tilgangsstyringen skyldes sju oppdiktede telefonnumre i tildelte serier (AV-29), og hvordan man ber om tilgang. «DOI 10.5281/zenodo.23723450» er erstattet med 10.5281/zenodo.23723450 i commiten som fører denne oppføringen. **Den commiten er ikke i bundlen**: bundlen slutter på `e7ee2fcbcf998da55d1b0a287de0410dae7e155c`.