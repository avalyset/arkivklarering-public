---
status: accepted (H4 utgår i v1.0, AV-27; protokollen gjelder hvis H4 gjennomføres senere)
date: 2026-10-27
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0018: Innspillingsprotokoll for H4

Versjon 1.2, 2026-10-28 (v1.2: merknad om at H4 utgår i v1.0 (AV-27 i KLAR-LOG-0003, Eiriks beslutning 2026-10-27, før noen H4-data er samlet inn): ingen opptak er laget under protokollen, `kjor_h4.py` kjøres ikke i v1.0, og beskrivelsene av kodelåsing og scoring under gjelder bare hvis H4 gjennomføres senere; protokollen er ellers uendret; v1.1: etter diagnosen av innlesingen 27.10, der ingen runde ble startet og ingenting ble lagret: testopptaket i mikrofonsjekken fjernet, banner uten runde, statuslinje, bekreftelse ved avslutning og hendelseslogg, punkt 8–11; protokollkravene i punkt 1–7 er uendret; koden låses på grenen `h4-fiks` med taggen `h4-rigg-v3`; v1.0: første versjon).

## Kontekst

H4 i `KLAR-PREREG-0001` måler flaggkjeden på menneskeinnlest `KLAR-MANUS-0002` (156 setninger). Innlesingen er den eneste delen av testdelene som lages av et menneske, og den må ikke påvirkes av at leseren ser hva maskinen gjør med opptaket. Ingen innspillingsprotokoll er beskrevet i PREREG; den spesifiseres her, **før datainnsamling** (avvik AV-17 i `KLAR-LOG-0003`). `scripts/rigg_manus.py` startet til nå norsk-tales kalibreringsrigg som den er: den har sider for transkripsjon, rapport, eksport og bidrag, og lagret på `lyd/menneske/` (`KLAR-ADR-0014` bestemte at riggen ikke kopieres). Se leseundersøkelsen av riggen i `KLAR-LOG-0001` og veikartet i `KLAR-ARK-0006`.

**v1.1.** Diagnosen av innlesingen 27.10 (ren lesing; `lyd/h4/` tom): ingen runde ble startet, og serveren ble stoppet via `POST /api/avslutt`, den eneste kodeveien til en kontrollert stopp (`h4_side.html:264` i `testkjoring-v2`). Mikrofonsjekken hadde et testopptak (`h4_side.html:209-213`) som så ut som innlesing men ikke lagret noe, og serveren hadde ingen hendelseslogg. Endringene i punkt 8–11 gjør det synlig for den som leser inn om noe lagres, og gir en logg som viser hva som skjedde. De berører innsamlingsverktøyet, ikke analysen, scoringen, utvalget, intervallene eller tersklene.

## Beslutning

Innlesingen skjer i en egen **H4-modus** (`arkivklarering/h4_innlesing.py`, `arkivklarering/h4_side.html`, startet av `scripts/rigg_manus.py`):

1. **Riggversjon låst.** norsk-tale må stå på commit `bcfef63d1be49ac239956dfb67784c002cecf310`, og de seks riggfilene som lastes må ha disse sha256-verdiene, ellers stopper innlesingen før serveren starter (`kontroller_rigg`; `rigg_manus.py --tor` viser kontrollen):
  - `kalibrering/rigg.py` sha256 `d79d692658235dd4a53877a25e933a689fd26ced896661c11b67a6bc1d480d68`
  - `kalibrering/aggreger.py` sha256 `08e315e85dc5e820013fdca9f6ae56a56b150b3b09a89f70ba2c95d534c9b73d`
  - `kalibrering/score.py` sha256 `90859617b4d1d59c88d0b2d95466f6c3f6b3626c4cff787ed835f36088aebfec`
  - `kalibrering/norm.py` sha256 `70826a80cdb8b02810e1f70ad57509c1675f2a004fb114342d4bee917bbe6283`
  - `kjerne/kjerne.py` sha256 `962e691c47824a4160bbd8fd208330abac5a7d4fd85ab803bedfaa17fb528a24`
  - `kjerne/korriger.py` sha256 `335bc6ac2454ee1744556f411c2f7cf6a44fcd02579b07ba9d201e863752cc68`
   Riggen kopieres fortsatt ikke (ADR-0014 gjelder for `norm.py` og `score.py`); modusen er en underklasse (`H4Rigg`, `H4Handler`) av norsk-tales `Rigg` og `Handler`. Commit og filhasher føres i `runde.json` for hver runde.
2. **Lagring bare på Vault.** Opptakene ligger KUN under `/Volumes/Vault/arkivklarering/lyd/h4/` (`H4_ROT`, fast i koden: skriptet har ingen `--opptak` og avviser andre argumenter), aldri i git og aldri i sky (`KLAR-ADR-0007`, `-0015`). Format som H4-skriptet forventer: `<runde>/opptak/<manus-id>.wav`, 16 kHz, mono, 16 bit (ffmpeg fra nettleserens opptak), med `runde.json`. `kalibrering/kjor_h4.py` leser dem med `--opptak /Volumes/Vault/arkivklarering/lyd/h4`, som `scripts/kjor_testdel.sh` sender.
3. **Leseinstruks.** «Les i naturlig tempo og på din vanlige dialekt. Ikke legg ekstra trykk på navn, tall eller fremmedord.» vises i et eget kort øverst på siden, gjentas over hver setning, og leseren må bekrefte at den er lest før en runde kan startes.
4. **Ta om bare ved feillesing.** Et omtak krever en grunn av tre: «feil ord», «avbrudd» eller «støy»; serveren avviser omtak uten slik grunn (HTTP 400), og første forsøk kan ikke ha grunn. Aldri omtak på grunn av maskinens resultat: leseren får ikke se noe resultat (punkt 5). Forkastede opptak beholdes i `<runde>/forkastet/<manus-id>_forsok<N>.wav` (utenfor `opptak/`, som H4-skriptet leser).
5. **Ingen visning av transkripsjon, flagg eller poeng, under eller etter innspillingen.** Resultatside og eksport er AV i denne modusen: rutene for transkripsjon, resultat, rapport, bidrag, sletting og selvtest finnes ikke (HTTP 404), og siden har ingen slike elementer. «Hopp over» er tatt bort, slik at leseren ikke kan utelate vanskelige setninger; de kan navigere frem og tilbake.
6. **Logg per opptak.** `<runde>/opptakslogg.jsonl`, én linje per lagret opptak: `id`, `runde`, `tidspunkt` (lokal tid, sekund), `forsok` (antall forsøk så langt), `grunn_omtak` (null ved første forsøk), `bytes`, `wav_sha256`, `forkastet_fil`.
7. **Rom og mikrofon** noteres én gang per runde, i fritekst, påkrevd før runden starter (`rom_og_mikrofon` i `runde.json`).
8. **Mikrofonsjekken tar ikke opp noe.** «Ta opp testsetning», «Stopp» og «Spill av» i mikrofonsjekken er fjernet (siden hadde et testopptak som så ut som innlesing). Tillatelsen til mikrofonen og nivåmåleren er beholdt; teksten på siden sier at ingenting tas opp eller lagres i sjekken.
9. **Banner og statuslinje.** Uten åpen runde vises øverst: «Ingen runde startet – ingenting lagres. Fyll ut og trykk Start ny runde.» Med åpen runde vises en alltid synlig statuslinje: «Runde <id> – lagret X av N». Den oppdateres bare etter svar fra serveren (åpnet runde, lagret opptak), aldri ut fra hva siden tror.
10. **Bekreftelse ved avslutning.** «Avslutt innleseren» krever `confirm`: «Avslutte innleseren? X av N opptak er lagret i denne runden. Du kan fortsette senere.», og uten runde «Avslutte? Ingen runde er startet.». Avbrytes bekreftelsen, sendes ingenting til serveren.
11. **Hendelseslogg.** `<H4_ROT>/serverlogg.jsonl`, JSONL med tidsstempel (lokal tid med forskyvning, millisekund), skrevet i forespørselslaget i `h4_innlesing.py` (ikke i norsk-tales `rigg.py`): `oppstart` (arkivklarering-commit, tagger på HEAD, nærmeste `h4-rigg-v*`-tagg som er forfar til HEAD og om de tre riggfilene er identiske med den, om riggfilene er uendret siden commiten, norsk-tale-commit, port, opptaksrot), `runde_ny` (ok, eller avvist med grunn og status), `opptak_lagret` (runde, id, forsøk), `omtak` (runde, id, grunn, forsøk), `avslutt` og `stoppet` (med `via`: `avslutt`, `tidsavbrudd` eller `avbrutt`). Aldri lyd og aldri tekst fra opptak. Loggfila ligger i opptaksroten, ikke i en rundemappe: `kalibrering/kjor_h4.py` leser bare mapper som heter `runde-*` (`finn_opptak`, linje 96), og riggens rundeliste bare mapper med `runde.json`, så loggen kan ikke tolkes som en runde.

Kodelåsing: v1.0 var låst med taggen `testkjoring-v2` (commit `c49d17463c14f7719f9f271ae3d4af4824436c35`, tag-objekt `c4a7a8e5c293b6f20c880ab38cf705010882de9c`). v1.1 låses først på grenen `h4-fiks` med taggen `h4-rigg-v3` (SHA og tidsstempel føres i `KLAR-LOG-0001` og i `KLAR-PREREG-0001`, «Avvik etter registrering»), og deretter med `testkjoring-v3` etter merge til main, som `scripts/kjor_testdel.sh` kontrollerte før hver testdel (nå kontrollerer skriptet den nyeste kodetaggen; v1.2: H4 kjøres ikke i v1.0, AV-27). Innleserens tre filer (`arkivklarering/h4_innlesing.py`, `arkivklarering/h4_side.html`, `scripts/rigg_manus.py`) skal være byte-identiske mellom de to taggene. Riggen starter med `source scripts/miljo.sh` (`TMPDIR` på Vault): ligger `TMPDIR` på et annet volum enn opptaksroten, feiler lagringen med «Cross-device link», og statuslinja viser da uendret antall.

## Konsekvenser

- Leseren ser aldri hva maskinen gjør med opptakene; scoringen ville skjedd senere i `kjor_h4.py`, i testkjøringen. v1.2: H4 utgår i v1.0 (AV-27), så ingen opptak er laget og ingen scoring er gjort.
- Riggen er fortsatt en avhengighet utenfor repoet: den virker bare med norsk-tale på låst commit. Oppdateres norsk-tale, stopper innlesingen til hasher og commit her er oppdatert i en ny ADR-versjon og ny kodetagg.
- Avgrensninger som ikke er endret: opptak i nettleseren er opus (tapskomprimert) konvertert til wav, ikke direkte wav-opptak; automatisk forsterkning står på (`autoGainControl`), ekko- og støyundertrykking av; det er ingen kvalitetskontroll per opptak (for stille, for kort, tomt), ingen ekstra opptakstid på slutten, ingen tastatursnarveier og ingen Esc for å avbryte et opptak. Disse står på listen «etter v1.0» i `KLAR-ARK-0006`.
- H4 med én leser (forfatteren, som kjenner målelementene) gjelder bare én taler og kan ikke generaliseres (`KLAR-PREREG-0001`, «Avvik etter registrering» punkt 8).

## Alternativer som ble vurdert

- **Norsk-tales rigg uendret:** forkastet; den viser transkripsjon, rapport og eksport, og tillater omtak uten grunn.
- **Vendor-kopi av riggen med ORIGIN og sha256 (som ADR-0014):** forkastet; riggen trekker inn transkripsjonskjernen (`kjerne.py`) og rapportkoden, som er det modusen skal slippe. Låsing med commit og filhasher gir samme etterprøvbarhet uten kopi.
- **Egen opptaker fra bunnen:** forkastet; dupliserer riggens sikkerhetsgrenser (127.0.0.1, token, Host- og Origin-kontroll, CSP) og opptaksløp som allerede er brukt.
