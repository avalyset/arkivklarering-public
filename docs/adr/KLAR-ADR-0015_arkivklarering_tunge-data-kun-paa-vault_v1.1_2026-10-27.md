---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0015: Tunge data og cacher kun på Vault, med miljøvakt

Versjon 1.1, 2026-10-27 (v1.1: beslutningen beskriver datarota `ARKIVKLARERING_DATA` med fallback slik koden gjør siden AV-28 (`arkivklarering/miljo.py`, `scripts/miljo.sh`, README «Installasjon»), i stedet for «ingen fallback til den interne disken» og «peker utenfor `/Volumes/Vault`»; begrunnelsen for Vault i Eiriks oppsett står; `krev_vault_miljo()` heter nå `krev_miljo()` (det gamle navnet er alias); filnavnet (slug) er beholdt etter KLAR-ARK-0002; v1.0: første versjon).

## Kontekst

Den interne disken er nesten full (ca. 14–20 GiB ledig av 460 GiB). Arkivklarering trenger mye plass: to ggml-modeller på 3,1 GB hver, venv med torch og transformers (1,2 GB), HF-, pip-, torch- og uv-cacher, evalueringsdata (NB Samtale, NorNE, NPSC), lyd og Whisper-mellomfiler. 2026-10-26 falt ledig plass på den interne disken med ca. 13 GiB i løpet av noen timer, og brukeren ba om diagnose. Diagnosen fant **ingenting fra arkivklarering** på den interne disken (Claude-appens VM-bilde på 14 GB, swap på 5–7 GB og en voksende ollama-logg tok plassen). Vakten er altså innført som forebygging etter dette, ikke fordi en lekkasje ble påvist. Repoet (kode og dokumenter) er lite og ligger i `~/dev`.

v1.1: Før publiseringen må verktøyet kunne installeres og testes på en maskin uten Vault. Derfor ble de faste Vault-stiene erstattet med én datarot i AV-28 (`57dedaf`, `testkjoring-v6`); i Eiriks oppsett er rota fortsatt Vault.

## Beslutning

**Én datarot for alt tungt, `ARKIVKLARERING_DATA`** (`arkivklarering/miljo.py`, `scripts/miljo.sh`; README «Installasjon»): modeller (`modeller/`), venv (`venv/`, med `.venv` som symlink, `venv-inaseg/`, `venv-diarisering/`), cacher (`cache/hf`, `cache/hf/datasets`, `cache/pip`, `cache/torch`, `cache/keras`, `cache/spacy`, `cache/uv`), midlertidige filer (`tmp/`), evalueringsdata (`eval-data/`; `ARKIVKLARERING_EVAL_DATA` overstyrer bare den), lyd (`lyd/`) og repo-bundles (`repo-bundle/`). Ikke-tungt (kode, dokumenter, resultater som tall) ligger i repoet og speiles etter KLAR-ADR-0010.

**Standard og fallback.** Er `ARKIVKLARERING_DATA` ikke satt, er rota `/Volumes/Vault/arkivklarering` når Vault er montert og mappen finnes (Eiriks oppsett, uendret), ellers `${XDG_DATA_HOME:-~/.local/share}/arkivklarering`, som opprettes (`miljo.standard_data`, `scripts/miljo.sh:9–17`). En satt `ARKIVKLARERING_DATA` som ikke finnes, opprettes ikke og gir stopp (exit 3), og det samme gjør en rot under et umontert `/Volumes/<disk>` (`miljo.sjekk`, `scripts/miljo.sh:18–31`). **Vault i Eiriks oppsett:** den interne disken er nesten full (Kontekst), så på denne maskinen skal rota være Vault; fallbacken brukes bare når Vault ikke er montert, og `scripts/miljo.sh` skriver da en merknad om hvilken rot som brukes.

**Miljøvakt.** `scripts/miljo.sh` kildes før all kjøring fra shell. Den setter `HF_HOME`, `HF_DATASETS_CACHE`, `PIP_CACHE_DIR`, `TORCH_HOME`, `KERAS_HOME`, `XDG_CACHE_HOME` (uv bruker `$XDG_CACHE_HOME/uv`) og `TMPDIR` under rota, og **avbryter (exit 3) hvis `HF_HOME`, `HF_DATASETS_CACHE`, `TMPDIR` eller `XDG_CACHE_HOME` peker utenfor rota** (symlinker løses opp). Python-skriptene i repoet kaller `arkivklarering.miljo.krev_miljo()` (alias `krev_vault_miljo()`) først; den setter manglende variabler under rota og stopper med samme feil, og `tests/conftest.py` kaller den for hele pytest-økta, der tester som trenger data under rota, nett eller Vault hoppes over med en grunn. `scripts/speil.sh` kilder `miljo.sh`.

**Ressursvakt for Whisper** (`eval/dev/felles.py`, `transkriber.kjor_prosess`): Whisper starter bare når det er minst 6 GB ledig minne, det andre sporets minnevakt ikke kjører, minst 8 GiB ledig på den interne disken og høyst 6,5 GB swap brukt. Kjører Whisper allerede og disk eller swap passerer grensen, drepes prosessen og kjøringen tas opp igjen når ressursene er frie. Ventet den over 3 timer, feiler den høyt i stedet for å henge. Én Whisper-kjøring om gangen.

**Rør ikke det som ikke er vårt.** Delte cacher (`~/.cache/uv`, `~/.cache/huggingface` for andre prosjekter), norsk-tales filer og andre spor flyttes eller slettes ikke. Det som tilhørte arkivklarering ble flyttet etter byte-sammenligning og sha256-kontroll før originalen ble slettet (de to inaVAMOS-modellene og de tre vektfilene i HFs delte blob-lager, 62 MB).

## Konsekvenser

- I Eiriks oppsett må Vault være montert for kjøring, test og speiling på Vault-rota. Er den ikke det, brukes fallbacken under `~/.local/share` med en merknad (v1.1); en satt rot under et umontert `/Volumes/<disk>` gir stopp i stedet for å skrive et annet sted.
- Kjøringer er tregere av og til fordi data og modeller leses fra en ekstern disk, og modellfilene lastes inn for hvert Whisper-kall (batchkjøring i DEV-målingene demper det).
- **Det vakten ikke styrer:** swap, Metal-shader-cachen (`/var/folders/…/C/com.apple.metal`, noen hundre MB) og `whisper.cpp`-bygget i `~/whisper.cpp` ligger på den interne disken og styres av systemet. Vakten begrenser Whisper når swap eller ledig disk blir for lav, men kan ikke frigjøre noe av det.
- Ollama-modellene ligger allerede på Vault (symlink `~/.ollama/models`), men `~/.ollama` og ollama-loggen i `/opt/homebrew/var/log` er ikke arkivklarerings og ikke styrt av vakten.
- Vakten er testet (`tests/test_miljo.py`, `tests/test_ressursvakt.py`): variabel mangler, peker utenfor, symlink ut av rota, lignende prefiks, umontert rot, og drap av prosess ved lav disk eller høy swap.

## Alternativer som ble vurdert

- **Fallback til den interne disken når Vault mangler:** forkastet i v1.0; den interne disken er nesten full, og en stille fallback er nettopp feilen vakten skal hindre. v1.1: tatt inn i AV-28 for andre maskiner enn Eiriks, men ikke stille: fallbacken gjelder bare når `ARKIVKLARERING_DATA` ikke er satt, `scripts/miljo.sh` skriver hvilken rot som brukes, og en satt rot som mangler eller ligger på en umontert disk gir fortsatt stopp.
- **Symlinke `~/.cache` og `~/.cache/huggingface` til Vault:** forkastet; det ville flytte andre prosjekters cacher uten at de har bedt om det.
- **Bare miljøvariabler uten vakt:** forkastet; en kjøring uten `source scripts/miljo.sh` ville da skrive cacher til standardstiene på den interne disken uten at noen merket det.
