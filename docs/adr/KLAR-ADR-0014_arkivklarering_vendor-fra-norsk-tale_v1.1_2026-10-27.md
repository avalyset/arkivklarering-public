---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0014: Tallnormalisering og scoring tas inn som uendret vendor-kopi fra norsk-tale

Versjon 1.1, 2026-10-27 (v1.1: lisensene rettet etter lisensbyttet (KLAR-ADR-0020): norsk-tale er Apache-2.0, arkivklarering er AGPL-3.0-or-later; «samme lisens som arkivklarering» er fjernet; beslutningen er ellers uendret; v1.0: første versjon).

## Kontekst

KLAR-ADR-0001 sier at norsk-tale bare er referanse og at kode og data ikke flyttes mellom prosjektene uten en egen beslutning. Kjedekalibreringen av personvernflaggene (KLAR-MANUS-0001) trenger det norsk-tale allerede har bygd og kryssjekket: tallnormalisering (tallord til sifre, tusenskille og mellomrom i sifergrupper) og deterministisk scoring av målelementer per setning, med målformfeil rapportert separat. Å skrive dette på nytt eller å kopiere koden løst gir to varianter som driver fra hverandre.

## Beslutning

`norm.py` og `score.py` fra `avalyset/norsk-tale` tas inn som **uendret vendor-kopi** i `arkivklarering/_vendor/norsk_tale/`, med `ORIGIN.txt` (kilde, commit, sha256 per fil) og lisensfilen (`arkivklarering/_vendor/norsk_tale/LICENSE`). **Lisens:** norsk-tale er Apache-2.0, og vendor-kopien beholder den lisensen; arkivklarering er AGPL-3.0-or-later (KLAR-ADR-0020). Tredjepart beholder egne lisenser (KLAR-ADR-0020, «Beslutning»), og kopien er ført i `NOTICE` og README «Lisens». Opphav:

- repo: https://github.com/avalyset/norsk-tale
- commit: `bcfef63d1be49ac239956dfb67784c002cecf310` (HEAD og origin/main 2026-10-26); filene ble sist endret i `519fc11d05d8a19e5d934e363744d1e5af4276ad`
- `norm.py` sha256 `70826a80cdb8b02810e1f70ad57509c1675f2a004fb114342d4bee917bbe6283`, `score.py` sha256 `90859617b4d1d59c88d0b2d95466f6c3f6b3626c4cff787ed835f36088aebfec`

`tests/test_vendor.py` feiler hvis filene ikke stemmer med `ORIGIN.txt`. Det som er spesifikt for flaggene ligger i `arkivklarering/kalibrering.py` (`score_flagg`) og endrer ikke vendor-filene. Manusformatet (`id`, `malform`, `klasse`, `setning`, `elementer`, `dialektutvalg`) er det samme som i norsk-tale.

**Opptaksriggen (`kalibrering/rigg.py`) kopieres ikke.** Den brukes som et eksternt verktøy fra norsk-tales egen katalog (`scripts/rigg_manus.py` bytter bare ut manusfila og peker opptaksmappen til Vault).

## Konsekvenser

- Ett sted for tallnormalisering og scoring, og en kontroll som oppdager drift. Nye versjoner tas inn ved å kopiere på nytt, oppdatere `ORIGIN.txt` og denne ADR-en.
- Riggen er en avhengighet utenfor repoet: den virker bare der norsk-tale ligger (`NORSK_TALE`, standard `~/dev/norsk-tale`) og følger det repoets endringer. Riggen laster ikke noe fra arkivklarering.
- Scoringen kjenner typene `nektelse`, `tall` og `navn` fra norsk-tale, men leser `elementer` generisk (`type` og `former`), så kategorinavnene her fungerer uten endring. Scoringen sjekker om en skriveform står i teksten; om et flagg dekker elementet avgjøres i `kalibrering.score_flagg`.
- norsk-tale er fortsatt referanse: funn og tall derfra siteres ikke som mål på arkivklarering (KLAR-ADR-0001).

## Alternativer som ble vurdert

- **Python-avhengighet av norsk-tale** (pip fra GitHub): forkastet; norsk-tale er et plugin-repo uten pakke, og en avhengighet ville binde arkivklarering til dets utgivelser.
- **Løs kopi av koden**: forkastet av grunnen over; ingen kontroll mot drift.
- **Egen implementasjon**: forkastet; to implementasjoner med samme tall validerer bare der spesifikasjonene skiller lag, og her er målet å bruke den samme.
