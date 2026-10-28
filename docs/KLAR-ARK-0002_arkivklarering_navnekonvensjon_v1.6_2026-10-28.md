# KLAR-ARK-0002: Navnekonvensjon for arkivnøkler

Versjon 1.6, 2026-10-28 (v1.6: eksemplet på et filnavn er merket; pekere til versjoner som ikke er i treet er merket «(i git-historikken)», og pekere med linjenummer til forrige versjon av et dokument med ny versjon viser til den nye versjonen, samme linje; kontrollert med `scripts/sjekk_pekere.py`, 0 brudd (KLAR-LOG-0005, restfunn etter kontrollen); v1.5: unntakene fra regelen om at en ny versjon erstatter den gamle i arbeidstreet, og merkingen av pekere til versjoner som ikke er i treet, er skrevet inn (porten, runde 3 (KLAR-LOG-0005), funn 7); v1.4: filtypen `txt` (hashfila KLAR-ARK-0007) er tatt med under `<ext>`; plasseringen for EVAL har også `eval/test/` (testdelene, KLAR-EVAL-0013–0015) og `eval/sensitivitet/` (bare de avlyste KLAR-EVAL-0016 og -0017; mappen finnes ikke), og for LOG `docs/stempler/` (KLAR-LOG-0002); regelen om at en ny versjon erstatter den gamle i arbeidstreet er uendret; v1.3: typen KILDE for kilderegisteret; v1.2: PREREG-0001 gjelder testdelene, museumspiloten er PREREG-0002; v1.1: typen MANUS for kalibreringsmanus, med `tsv` som filtype og plassering i `kalibrering/`). Forfatter: Eirik Botten Nicolaysen, EcoDeco AS.

## 1. Format

```
KLAR-<TYPE>-<NNNN>_arkivklarering_<slug>_v<maj>.<min>_<ÅÅÅÅ-MM-DD>.<ext>
```

Eksempel: `KLAR-ARK-0001_arkivklarering_arkitektur_v1.1_2026-10-26.md` (i git-historikken).

| Del | Regel |
|---|---|
| `KLAR` | fast prefiks for dette verktøyet |
| `<TYPE>` | én av typene i § 2 |
| `<NNNN>` | firesifret løpenummer per type, fra 0001. Gjenbrukes aldri, heller ikke etter at et dokument er trukket tilbake |
| `arkivklarering` | fast prosjektledd |
| `<slug>` | små bokstaver a–z og 0–9, ord skilt med `-`. Norske bokstaver skrives æ→`ae`, ø→`oe`, å→`aa` |
| `v<maj>.<min>` | versjonen dokumentet selv oppgir i overskriften. Minor ved rettelser og presiseringer, major når en påstand eller beslutning endres |
| `<ÅÅÅÅ-MM-DD>` | datoen for denne versjonen |
| `<ext>` | `md` for tekst, `tsv` for manus, `txt` for ren tekst som skal hashes eller stemples uendret (hashfila KLAR-ARK-0007). Data som hører til et dokument (`json`) bærer samme nøkkel og stamme |

Samme dokument har samme `TYPE-NNNN` gjennom alle versjoner. En ny versjon får nytt filnavn
(ny versjon og ny dato) og erstatter den gamle i arbeidstreet; den gamle ligger i git-historikken. Unntak: den registrerte teksten (KLAR-REG-0001 v1.0, låst på OSF) og en md-fil som har en JSON-fil med samme stamme (rapporten til en lagret kjøring) blir stående ved siden av nyere versjoner. I dokumentene som beskriver gjeldende tilstand (KLAR-ARK-0001, -0004, -0005, -0008, -0009 og KLAR-KILDE-0001) merkes en peker til en versjon som ikke lenger er i treet «(i git-historikken)». Andre dokumenter viser til versjonene som gjaldt da de ble skrevet; logger (LOG), avviksteksten i PREREG, stempellista, GT og funnlistene er historiske, og pekerne der merkes ikke.

## 2. Typer

| Type | Bruk | Plassering |
|---|---|---|
| `REG` | registrering (OSF-metoderegistrering o.l.) | `docs/` |
| `PREREG` | studiespesifikk preregistrering. `KLAR-PREREG-0001` gjelder testdelene av offentlige datasett og testmanuset; museumspilotens er `KLAR-PREREG-0002` (reservert) og lages først etter ja fra museet og før pilotdata kjøres | `docs/` |
| `ARK` | arkitektur og konvensjoner | `docs/` |
| `ADR` | én arkitekturbeslutning (MADR), status `accepted` når vedtatt | `docs/adr/` |
| `GT` | ground truth, generert fra disk av `scripts/ground_truth.py`. Versjonen økes automatisk | `docs/` |
| `EVAL` | målinger og tilhørende data, alltid merket `dev` eller `pilot` i innholdet (testdelene: merknaden «TEST – preregistrert» i resultatfila) | `docs/`, `eval/dev/` eller `eval/test/` (testdelene, KLAR-EVAL-0013–0015); `eval/sensitivitet/` var satt av til de avlyste KLAR-EVAL-0016 og -0017 og finnes ikke |
| `LOG` | avviks- og hendelseslogg, ført fortløpende | `docs/`; tidsstempelloggen KLAR-LOG-0002 i `docs/stempler/` |
| `MANUS` | manus (setninger med målelementer, lest inn eller syntetisert): justeringsmanus (0001) eller testmanus (0002) | `kalibrering/` |
| `KILDE` | kilderegister: én rad per påstand med kildelenke, lagret kopi (sha256) og ordrett sitat | `docs/` |
| `MASTER` | oversiktsdokument per spor. Ligger utenfor git (se § 3) | `~/Desktop/Master Dok./Arkivklarering/arkiv/` |

## 3. Unntak

- **MASTER** følger `~/bin/bump-master.sh` sitt format, `MASTER_ARKIVKLARERING_v<maj>_<min>_<ÅÅÅÅ-MM-DD>.md`, med understrek i
  versjonen, og pekes ut av `POINTER.txt`. MASTER committes aldri til git.
- **`docs/gt_fast.md`** er den håndførte inndata til GT og er ikke et eget arkivdokument.
- **Kode, README, `modeller.lock.json` og konfigurasjon** er ikke arkivdokumenter og har vanlige filnavn.
- Dokumenter som er utarbeidet før konvensjonen (`KLAR-REG-0001`, `KLAR-ARK-0001`) fikk 2026-10-26 nytt navn
  med `git mv`. `v1` ble `v1.0`. `KLAR-ARK-0001` ble `v1.1`, fordi innholdet selv sier 1.1 etter kildekontrollen
  samme dag.

## 4. Regler

- Nytt navn gis med `git mv`, slik at historikken følger filen. Lenker i andre dokumenter rettes i samme commit.
- Filnavnets versjon og dato skal stemme med dokumentets overskrift. Avvik føres i `KLAR-LOG-0001`.
- Tilstand påstås aldri fra minne eller chat. Les `KLAR-GT-0001_*` eller disken.
