# KLAR-ARK-0001: Arkitektur for arkivklarering

Versjon 1.10, 2026-10-28 (v1.10: pekere til dokumenter med ny versjon i runde 3 viser til den nye versjonen; pekere til versjoner som ikke er i treet er merket «(i git-historikken)» (porten, runde 3 (KLAR-LOG-0005)); v1.9: henvisningene til ADR-versjoner som er fjernet fra arbeidstreet peker på gjeldende versjon (KLAR-ADR-0019 v1.5 i § 2 og § 3, KLAR-ADR-0004 v1.4 i § 3); segmenteringsraden i § 2 har kilden for inaSpeechSegmenter (KLAR-KILDE-0001 IS-01, K119, og IS-02, K130) med hentedatoene, og § 6 har en rad for den; personvernraden i § 2 sier at flaggene også er målt som flaggoverlevelse på transkribert tale (KLAR-EVAL-0006, -0007, -0014), ikke på arkivlyd; § 3 sier at tale over musikk blir `speech` eller `music`; v1.8: § 1 «Verktøyet klarerer før publisering» rettet til at verktøyet foreslår hva et menneske må klarere; statuslinjen, § 2 og § 5 oppdatert til faktisk tilstand i versjon 1.0.0 (katalogutkast, OHMS XML, IIIF og MMIF er implementert, `cli.py` skriver seks filer, personvernflaggene er også målt på transkribert tale), ikke «kun v0.1»; § 3 segmentregelen: med `-nt` skriver begge lag `<|nocaptions|>`, rålaget skrev «.» før `-nt` (KLAR-EVAL-0001 v1.3); henvisningene til gjeldende ADR-versjoner oppdatert; v1.7: § 3.1 «Tale over musikk transkriberes og flagges» gjelder bare med inaVAMOS, med inaSpeechSegmenter (standard) faller flagget bort; § 5 `segment.py` rettet til inaSpeechSegmenter som standard og inaVAMOS som valgfritt tillegg (KLAR-ADR-0019 v1.3); v1.6: segmenteringen i § 2 og § 3 rettet: inaSpeechSegmenter er standard, inaVAMOS er valgfritt tillegg `reproduksjon-h1h2` for reproduksjon av H1 og H2 (KLAR-ADR-0019 v1.3, AV-26); v1.5: OSF-statusen for metoderegistreringen fbme7 i § 1 presisert: embargo til 2027-10-26, status sett i innlogget OSF-økt 2026-10-27, kan ikke etterprøves offentlig før embargoen oppheves (KLAR-KILDE-0001 OS-01); v1.4: påstander om kildene strammet inn eller rettet etter kildekontroll, KLAR-KILDE-0001; v1.3: personvernflagging implementert som v0 og målt, rålagets rolle justert; v1.0 samme dag; v1.1: kildene kontrollert og rettet, se § 6; v1.2: begrunnelsen for segmentregelen skrevet om etter måling og kildekontroll, se § 3 og KLAR-ADR-0004 v1.1). Beslutningene står i [docs/adr/](adr/), navnekonvensjonen i KLAR-ARK-0002. Forfatter: Eirik Botten Nicolaysen, EcoDeco AS.
Status (v1.8): arkitekturen for versjon 1.0.0. Rørledningen i § 2 er implementert, unntatt det som er merket [plan] (alias-tabell og menneskelig godkjenning); se § 5.

## 1. Formål

Norske lokalradio- og fortellerarkiv kan ikke publiseres før hvert opptak er klarert for
personopplysninger og tredjeparts musikkrettigheter. Klarering gjøres i dag ved at ansatte og
frivillige lytter gjennom hver time. For arkiv på tusenvis av timer er denne lyttingen
flaskehalsen, ikke digitalisering eller transkripsjon.

Verktøyet **foreslår hva et menneske må klarere før publisering**. Søkbarhet er en bieffekt, ikke målet.
**Mennesket avgjør alt, verktøyet foreslår.** Ingen klipp, ingen publisering og ingen
rettelse skjer uten en menneskelig godkjenning. All behandling skjer lokalt; lyd forlater ikke
arkivet.

Metoden og prioriteten er registrert på OSF: <https://osf.io/fbme7/> (under embargo til 2027-10-26; status sett i innlogget OSF-økt 2026-10-27, kan ikke etterprøves offentlig før embargoen oppheves;
metoderegistreringen står også i [KLAR-REG-0001](KLAR-REG-0001_arkivklarering_osf-metode_v1.0_2026-10-26.md)).
En egen studiespesifikk preregistrering med låst analyseplan blir sendt før pilotdata behandles.

## 2. Rørledning

```
lydfil
  └─ segment      (inaSpeechSegmenter; inaVAMOS valgfritt)  speech | music | other (+ speech+music bare med inaVAMOS)
       ├─ music                        → «foreslått klipp» (aldri til Whisper)
       ├─ other                        → ingen handling    (aldri til Whisper)
       └─ speech, speech+music         → transkriber (to lag, ett pass hver)
            │                            speech+music får flagget
            │                            «musikk under tale – vurder rettigheter» (bare med inaVAMOS)
            ├─ rålag: NB-Whisper large verbatim (-nt)
            └─ normalisert lag: NB-Whisper large
                 ├─ talerinndeling (valgfritt, --taler: pyannote, TALER_1, TALER_2 …)
                 ├─ entiteter (deterministisk alias-tabell, med logg)        [plan]
                 └─ personvern (flagg på begge lag, union uten terskel, recall foran presisjon)
                      └─ katalog (utkast til katalogpost, lokal ollama; ikke validert)
                           └─ eksport (WebVTT per lag, segments.json, OHMS XML, IIIF Presentation 3, MMIF)
                                └─ menneskelig godkjenning                             [plan]
```

v1.8: rekkefølgen er den `arkivklarering/cli.py` kjører (`main`: segmentering, to transkripsjonspass, valgfri talerinndeling, personvern, `segments.json`, katalogutkast, OHMS, IIIF og MMIF). Eksporten skrives uten noen godkjenning; utdataene er forslag til den menneskelige vurderingen, som ikke er bygget som egen flate (§ 5).

## 3. Lagvalg

Hvert valg har begrunnelse, kilde og kildestatus. «Verifisert 2026-10-26» betyr at den
oppgitte URL-en ble hentet denne dagen og at siden inneholder det påstanden bygger på; hva siden
faktisk sier står i § 6. Påstander om andre systemers ytelse er ikke gjengitt.

| Lag | Valg | Begrunnelse | Kilde | Status |
|---|---|---|---|---|
| Internt format | MMIF (Multi-Media Interchange Format) | Versjonert datamodell for å overføre analyseresultater mellom CLAMS-apper. CLAMS-prosjektet er åpen kildekode. Hver visning (view) i en MMIF-fil har metadata om applikasjonen som laget den og opprettelsesdato (Rim m.fl., LREC 2022), så resultater kan spores til verktøyet. At komponentene blir utskiftbare er vår egen slutning. | CLAMS-prosjektet (Brandeis University i samarbeid med GBH Archives): <https://clams.ai/home/>, spesifikasjon <https://mmif.clams.ai/> | Verifisert 2026-10-26 |
| Menneskelige godkjenningssteg og måling per komponent | Godkjenningspunkter mellom komponentene, og måling av hver komponent for seg | AMP kombinerer automatiske mekanismer med menneskelig arbeid. Vi gjør hvert menneskelig steg til et eksplisitt godkjenningspunkt og måler komponentene hver for seg. Målingen er vår egen design, ikke tilskrevet AMP. | Audiovisual Metadata Platform (AMP), Indiana University: <https://hdl.handle.net/2022/21982> | Delvis verifisert 2026-10-26: kombinasjonen av automatikk og menneskelig arbeid står i rapportens sammendrag. Hele planleggingsrapporten (2018) og AMPPD-sluttrapporten (2021) er lest. Sluttrapporten beskriver at AMPPD evaluerte verktøy (metadata generation mechanisms) i åtte kategorier ved utvelgelsen; «måling per komponent» som løpende grep står ikke i sitatet. |
| Indeksutkast og opplæring | Maskinutkast til indeks, rettet av mennesker; opplæring av eksterne miljøer til å indeksere egne intervjuer | Nunn Centers SpeakEZ lager råtranskript (Verbatimizer, Whisper) og utkast til OHMS-indeks (OHMSifier). Nunn Center har også en modell for å lære opp eksterne miljøer til å lage indekser selv. Utkastet erstatter ikke lytting der klarering avhenger av innholdet. | Nunn Center, University of Kentucky: <https://research.uky.edu/news/making-history-accessible-doug-boyds-curate-research> | Verifisert 2026-10-26. SpeakEZ er ifølge siden et lukket, internt system; vi bruker det som modell, ikke som komponent. |
| Retteflate | Webgrensesnitt for retting av transkripsjon og flagg | FixIt+ er en crowdsourcing-plattform der brukere retter maskingenererte transkripsjoner mens de lytter til lyden, linje for linje. Retteflaten er også stedet der klarering besluttes. | FixIt+, GBH / American Archive of Public Broadcasting: <https://blog.americanarchive.org/2020/06/05/how-to-fix-it-and-why-crowdsourcing-to-save-public-media/> | Verifisert 2026-10-26 |
| Segmentering | inaSpeechSegmenter 0.8.0 (standard); inaVAMOS som valgfritt tillegg `reproduksjon-h1h2`, bare for reproduksjon av de preregistrerte kjøringene H1 og H2 (KLAR-ADR-0019 v1.6, AV-26) | inaSpeechSegmenter gir `speech`, `music` og `other`, uten klasse for tale over musikk (KLAR-ADR-0019). inaVAMOS: to uavhengige detektorer (tale og musikk) kombineres til `speech`, `music`, `speech+music` og `other`. Modellene (ca. 80 MB) lastes ned én gang og kjører lokalt etter det. | inaSpeechSegmenter (INA): `LICENSE` ved tagg v0.8.0, <https://github.com/ina-foss/inaSpeechSegmenter/blob/v0.8.0/LICENSE> (KLAR-KILDE-0001 IS-01, K119), og PyPI-metadataene for 0.8.0, <https://pypi.org/pypi/inaSpeechSegmenter/0.8.0/json> (IS-02, K130); PyPI `inaVAMOS` (INA): <https://pypi.org/project/inaVAMOS/>, <https://github.com/ina-foss/inaVAMOS> | inaSpeechSegmenter: verifisert 2026-10-27 (K119) og 2026-10-28 (K130); inaVAMOS: verifisert 2026-10-26 |
| Segmentregel | Segmentering foran Whisper; `music` og `other` går aldri til Whisper | Segmenter uten tale har ingenting å transkribere. Egen måling (stillhet, to nivåer hvit støy, rosa støy og musikk, direkte til whisper.cpp med `-l nn`, én kjøring per modell) ga ingen prosa, men spesialtokenet `<\|nocaptions\|>` over hele 30 s-vinduet på begge lag (rålaget kjøres med `-nt`; før `-nt` skrev rålaget «.»), som kan forveksles med innhold; se [KLAR-EVAL-0001](KLAR-EVAL-0001_arkivklarering_oppdiktet-tekst-maaling_v1.5_2026-10-28.md). Regelen står ikke på påvist hallusinasjon på stillhet eller støy. Koenecke m.fl. fant ca. 1 % oppdiktede fraser og at de var hyppigere for talere med lengre ikke-vokale andeler, altså pauser i tale. Det er en risiko inne i `speech`-segmenter som regelen ikke fjerner. NB-Whisper-kortet sier selv at modellene kan hallusinere og utelate deler. | Koenecke m.fl. 2024, «Careless Whisper: Speech-to-Text Hallucination Harms», <https://arxiv.org/abs/2402.08021> (ACM-DOI 10.1145/3630106.3658996 er oppgitt som relatert DOI); [KLAR-ADR-0004](adr/KLAR-ADR-0004_arkivklarering_segmentregel_v1.5_2026-10-28.md) | Verifisert 2026-10-26 (arXiv-sammendraget). Utgivelsessted: ACM FAccT ’24, Rio de Janeiro, 3.–6. juni 2024 (oppgitt i PDF-en, ikke på arXiv-siden). ACM-DOI gir 403 mot curl. |
| Transkripsjon | NB-Whisper large, to lag: verbatim (rålag) og standard (normalisert lag), `-l nn` | Verbatim-varianten er finjustert videre (kortet: «outputting only text in lowercase and without punctation», mer ordrett, ingen forsøk på å rette grammatikk). Standardmodellen gir ifølge kortet grammatisk korrekt skriftspråk. Begge modellkortene lister nynorsk som språk; kodeeksempelet med `language: nn` står i standardkortet. | NB AI-Lab: <https://huggingface.co/NbAiLab/nb-whisper-large-verbatim>, <https://huggingface.co/NbAiLab/nb-whisper-large>, <https://github.com/NbAiLab/nb-whisper> | Verifisert 2026-10-26. «Normalisert» her betyr modellens standardstil, ikke en egen normalisering til nynorsk eller bokmål; den kommer med alias-tabellen. |
| Navnekorrigering | Deterministisk alias-tabell med logg, ingen uklar matching | Hver erstatning er revisjonsbar og kan reverseres. Uklar matching kan endre et navn til et annet og er uakseptabelt i et klareringsløp. | Egen design | Ikke aktuelt (ingen ekstern kilde) |
| Personvernflagg | Presidio med norsk oppsett, pluss NB-BERT-base-ner | Presidio er ifølge CLEANUP-guiden «a software tool that allows you to detect PII using a combination of detectors», og egne gjenkjennere kan kobles til. CLEANUP-guiden viser hvordan Presidio settes opp for norsk bokmål (spaCy-modell, egen gjenkjenner for dato og kartlegging av spaCys stedsetiketter til Presidios LOCATION). NB-BERT-base-ner er en NER-modell finjustert på NorNE. Flagg er forslag, ikke avgjørelser. Implementert som v0 (KLAR-ADR-0012: recall foran presisjon); DEV-måling på NorNE i KLAR-EVAL-0005. | Presidio: <https://presidio.dataprivacystack.org/>; CLEANUP-guiden (Norsk Regnesentral og NAV): <https://data.nav.no/fortelling/cleanup-guide>, kap. 7.2; `NbAiLab/nb-bert-base-ner`: <https://huggingface.co/NbAiLab/nb-bert-base-ner> | Verifisert 2026-10-26, med forbehold: NAV-guiden dekker bokmål (`nb`) med spaCy, ikke nynorsk og ikke NB-BERT-base-ner. Hvordan de to gjør det på nynorsk er målt på skrevet tekst (NorNE) i KLAR-EVAL-0005; i tillegg er flaggene målt som flaggoverlevelse på transkribert tale fra offentlige datasett (KLAR-EVAL-0006, -0007, -0014, § 5), ikke på arkivlyd. Presidio-adressen har flyttet seg fra microsoft.github.io. |
| Eksport | WebVTT og IIIF Presentation 3 (v1.8: i tillegg OHMS XML og MMIF, se § 5 og KLAR-ADR-0003, -0009) | WebVTT gir tidskodet tekst for avspillere. IIIF Presentation 3 har motivasjonen `supplementing` for ressurser som knyttes til et Canvas, slik at transkripsjon kan legges på lydens tidsakse. | W3C WebVTT: <https://www.w3.org/TR/webvtt1/>; IIIF: <https://iiif.io/api/presentation/3.0/> | Verifisert 2026-10-26. At `supplementing` er den riktige motivasjonen for transkripsjon (mot f.eks. `commenting`) er en tolkning av spesifikasjonen, ikke et ordrett krav. |

### 3.1 Regler som er avgjørende for klarering

- **Segmentering før transkripsjon.** Bare `speech` og `speech+music` går til Whisper. `music`
  og `other` går aldri dit; koden avviser det, og en test sjekker det. Begrunnelsen er at det ikke er tale å
  transkribere der og at utdata kan forveksles med innhold, ikke påvist hallusinasjon (se KLAR-ADR-0004 v1.5).
  Risikoen for oppdiktet tekst i pauser inne i tale gjenstår og krever menneskelig vurdering.
- **Tale over musikk transkriberes og flagges (bare med inaVAMOS).** `speech+music` får tekst og flagget
  «musikk under tale – vurder rettigheter». Med inaSpeechSegmenter (standard, KLAR-ADR-0019 v1.6) finnes ikke
  `speech+music`: tale over musikk får det modellen gir, i praksis `speech` (transkriberes) eller `music` (transkriberes ikke), og flagget faller bort. Når tale over korte gap slås sammen, beholdes
  tidsintervallene der musikken lå.
- **Ren musikk får ingen tekst.** Den merkes «foreslått klipp». Det er et forslag; verktøyet
  klipper ikke.
- **To lag, to pass.** Rålaget (verbatim) er grunnlaget for revisjon. Personvernflagg lages på begge lag: navnegjenkjenning
  bruker store bokstaver, og på rålaget (små bokstaver, ingen tegnsetting) faller recall kraftig (KLAR-EVAL-0005), så det normaliserte
  laget bærer flaggene for navn og steder og rålaget er et supplement. Lagene transkriberes hver for seg over de samme segmentene.
- **Alle erstatninger loggføres og kan reverseres** (når alias-tabellen kommer).

### 3.2 Hva rørledningen ikke gjør

Den avgjør ikke at noe er klarert. Den avgjør ikke at noe er fritt for personopplysninger. Et
manglende flagg er ikke en garanti. Gjenkallingen (recall) av flaggene måles mot en fasit fra full
menneskelig lytting før noen bruker flaggene til å spare lyttetid (se OSF-registreringen).

## 4. Kanaler

- **Verktøy:** kode og dokumentasjon meldes til Nasjonalbibliotekets leverandørliste.
- **Gullsett:** overføres til Språkbanken først etter klarering og avtale med eier av opptakene.
  Før det forlater ingen opptak eller transkripsjoner arkivet.

## 5. Status for implementasjon (versjon 1.0.0)

| Modul | Status |
|---|---|
| `segment.py` | Implementert. inaSpeechSegmenter som standard, etikettene `speech`, `music` og `other` etter etikettkartet i KLAR-ADR-0019 v1.6; inaVAMOS (fire etiketter) som valgfritt tillegg. Sammenslåing av tale over korte gap, flagg for musikk under tale (bare med inaVAMOS). |
| `transkriber.py` | Implementert. whisper.cpp, to lag (verbatim og standard), sha256-kontroll mot `modeller.lock.json`, kun `speech` og `speech+music`. |
| `eksport.py` | Implementert: WebVTT per lag, `segments.json` med begge tekstene og flaggene, OHMS XML (skjema 5.4, validert i testene), IIIF Presentation 3 (`supplementing`, KLAR-ADR-0009) og MMIF (`mmif-python`, KLAR-ADR-0003), hver med validator (`valider_*`) og test. |
| `cli.py` | Implementert. Lyd inn; ut per lydfil `<navn>` seks filer: `<navn>.ra.vtt`, `<navn>.normalisert.vtt`, `<navn>.segments.json`, `<navn>.ohms.xml`, `<navn>.iiif.json` og `<navn>.mmif.json` (`arkivklarering/cli.py:86–126`). Flagg: README «Bruk». |
| `entiteter.py` | Stubb. Planen står i docstringen. |
| `personvern.py` | Implementert som v0: Presidio (`nb`/`nn`), NB-BERT-base-ner, mønstre (dato, fødselsår, telefon, fødselsnummer) og nøkkelordlister (`vokabular/sensitivt_*.txt`). Flagg i `segments.json` per segment og lag. Målt på skrevet tekst (NorNE validation, DEV, KLAR-EVAL-0005; NorNE test, H3, KLAR-EVAL-0015) og på transkribert tale som flaggoverlevelse mot samme motor på referanseteksten (NB Samtale og NPSC validation, DEV, KLAR-EVAL-0006 og KLAR-EVAL-0007; NPSC test, H2, KLAR-EVAL-0014). Ikke målt på arkivlyd. |
| `katalog.py` | Implementert: katalogutkast per sending via lokal ollama (standard `hf.co/NbAiLab/borealis-open-4b-gguf:Q4_K_M`, KLAR-ADR-0013), merket «utkast – maskinforslag»; forslag som ikke står i teksten, forkastes og logges. Ikke validert. |
| `diarisering.py` | Implementert, valgfritt (`--taler`): anonym talerinndeling med pyannote i eget venv (KLAR-ADR-0016); ikke kjørt i verifikasjonen av v1.0, bare dekket av testene. |

Utviklingsmåling (DEV, ikke pilot): `eval/dev/`. Den sier ikke noe om pilotkvalitet.

Versjon 1.0.0 har ingen alias-tabell og ingen menneskelig godkjenningsflate. Personvernflagging er v0; den er målt på skrevet tekst (NorNE) og som flaggoverlevelse på transkribert tale fra offentlige datasett (KLAR-EVAL-0006, -0007, -0014), ikke på arkivlyd.
Utdata er forslag til en menneskelig vurdering og skal ikke leses som en klarering.

## 6. Kildekontroll (2026-10-26)

Hver URL ble hentet 2026-10-26, og det påstanden bygger på ble lest på siden. Rettelser fra v1 er
merket.

| Kilde | Resultat |
|---|---|
| <https://clams.ai/home/> | CLAMS er utviklet ved Brandeis University i samarbeid med GBH Archives, finansiert av Mellon Foundation, og er åpen kildekode. MMIF er «an interchange format for multimodal annotations (text, audio, image/video)». <https://mmif.clams.ai/> beskriver MMIF som dataformat for å overføre analyseresultater mellom CLAMS-apper og viser versjoner til 1.2.0. **Rettet:** v1 oppga <https://clams.ai>, som bare videresender, og skrev «tidsbasert medium», som ikke står der. |
| <https://hdl.handle.net/2022/21982> (IU ScholarWorks) | Sammendraget: plattformen skal beskrive audiovisuelt innhold i stor skala med automatiske mekanismer «linked together with human labor in a recursive and reflexive workflow». Står ikke: «måling per komponent». **Rettet:** v1 skrev at AMP har «menneskelige godkjenningssteg og måling per komponent». Nå er kun det første tilskrevet AMP. v1 oppga heller ingen URL. PDF-en (planleggingsrapporten, 38 sider) er hentet og lest 2026-10-26; CNI-lysbildene er ikke lest. |
| <https://research.uky.edu/news/making-history-accessible-doug-boyds-curate-research> | SpeakEZ er «an in-house, closed system» med fem moduler. Verbatimizer: «Utilizing the Whisper model, this tool generates a raw transcript» i OHMS-kompatibelt format. OHMSifier: «creates a draft OHMS index by summarizing the interview at the segment level». Siden beskriver også at Nunn Center lærer opp eksterne miljøer til å indeksere egne intervjuer (Peace Corps-prosjektet). **Rettet:** v1 oppga «Nunn Center, University of Kentucky» uten URL og skrev «frivillige»; nå gjengis det siden sier. |
| <https://blog.americanarchive.org/2020/06/05/how-to-fix-it-and-why-crowdsourcing-to-save-public-media/> | FIX IT+ er ifølge AAPB «a crowdsourcing platform to correct simple grammatical errors» i maskingenererte transkripsjoner; brukeren lytter til lyden per linje. AAPB er et samarbeid der GBH er en av partene. |
| <https://pypi.org/project/inaVAMOS/> og <https://github.com/ina-foss/inaVAMOS> | Etikettene `speech`, `music`, `speech+music`, `other` fra to detektorer; modellene ca. 80 MB lastes ned første gang og kan brukes offline etterpå (`HF_HUB_OFFLINE=1`). |
| <https://github.com/ina-foss/inaSpeechSegmenter/blob/v0.8.0/LICENSE> og <https://pypi.org/pypi/inaSpeechSegmenter/0.8.0/json> | (v1.9; kontrollert 2026-10-27 og 2026-10-28, ikke 2026-10-26 som radene over; KLAR-KILDE-0001 IS-01–IS-06) inaSpeechSegmenter 0.8.0 er MIT-lisensiert som programvare (`LICENSE` L1 og L3 ved tagg v0.8.0, K119, hentet 2026-10-27), og PyPI-metadataene har `license` «MIT» (K130, hentet 2026-10-28). Vektene lastes ned fra GitHub-releases (`remote_utils.py` ved v0.8.0, K131), og lisensen for dem er uklar (KLAR-ADR-0019 v1.6). Etikettene `speech`, `music` og `other` er etikettkartet i koden (KLAR-ADR-0019), ikke en påstand fra kilden. |
| <https://arxiv.org/abs/2402.08021> | Koenecke m.fl.: ca. 1 % av transkripsjonene hadde hele oppdiktede fraser eller setninger; 38 % av hallusinasjonene hadde eksplisitt skadelig innhold; hallusinasjoner forekom uforholdsmessig oftere for talere med lengre andeler ikke-vokal tid (afasi). ACM-DOI 10.1145/3630106.3658996 står som relatert DOI. **Rettet:** v1 skrev «særlig i stillhet og støy». Artikkelen sier «longer shares of non-vocal durations», altså pauser og svake signaler i tale hos bestemte talere. Den beskriver også oppdiktede setninger «when no one is speaking in the input audio files» og antar bakgrunnsstøy som mulig årsak. v1 oppga «FAccT» som utgivelsessted; det står ikke på arXiv-siden, men det står i PDF-en («ACM FAccT ’24 …»). |
| NB-Whisper (<https://huggingface.co/NbAiLab/nb-whisper-large>, <https://huggingface.co/NbAiLab/nb-whisper-large-verbatim>, <https://github.com/NbAiLab/nb-whisper>) | Repoet er Apache-2.0. Standardmodellen er hovedmodellen; verbatim-varianten er trent videre og gir små bokstaver uten tegnsetting. Kortet viser transkripsjon til nynorsk med `language: nn`. Kortet sier at modellene kan «exhibit occasional hallucinations and may drop parts of the transcript». Treningsdata oppgis som NST, Stortingstaler, NRK-teksting og lydbøker. **Rettet:** v1 skrev «trent på norsk, med nynorsk og bokmål»; kortet oppgir ikke fordelingen mellom målformene i treningsdata, så det er fjernet. v1 skrev at verbatim-laget «bevarer det som ble sagt»; kortet sier «mer ordrett», ikke at det er fullstendig. |
| <https://presidio.dataprivacystack.org/> | Presidio-dokumentasjonen har flyttet fra microsoft.github.io, som videresender via data-privacy-stack.github.io. Siden har blant annet «Additional models/languages». **Rettet:** URL. |
| <https://data.nav.no/fortelling/cleanup-guide> | Forfatter er «NR and NAV through the CLEANUP-project» (NR = Norsk Regnesentral er vår utvidelse av forkortelsen), publisert 2024-10-07. Kap. 2.3 sier at Presidio fungerer på engelsk, ikke andre språk som norsk, og viser til kap. 7.2 for norsk. Kap. 7.2 setter opp Presidio med en spaCy-modell for norsk bokmål, norsk datogjenkjenner og en kartlegging av spaCys stedsetiketter til LOCATION (ikke en stedsliste). **Rettet:** v1 attribuerte guiden til NAV alene. v1 skrev også at den viser «et norsk oppsett» uten å si at det er bokmål og at den ikke bruker NB-BERT-base-ner. |
| <https://huggingface.co/NbAiLab/nb-bert-base-ner> | NB-BERT base finjustert for NER på NorNE, lisens CC-BY-4.0, utgitt 2021-11-17. Kortet sier ikke noe om nynorsk. |
| <https://iiif.io/api/presentation/3.0/> | Motivasjonen `supplementing` er definert for ressurser knyttet til et Canvas. Siden sier ikke at den er ment for transkripsjon spesielt. |
| <https://www.w3.org/TR/webvtt1/> | «WebVTT: The Web Video Text Tracks Format», W3C Candidate Recommendation Draft 2026-05-20. |
