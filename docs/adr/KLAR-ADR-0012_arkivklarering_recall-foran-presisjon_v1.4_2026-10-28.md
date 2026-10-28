---
status: accepted
date: 2026-10-26
decision-makers: Eirik Botten Nicolaysen
---

# KLAR-ADR-0012: Recall foran presisjon i personvernflagging

Versjon 1.4, 2026-10-28: parentesen «som spaCy-standarden i CLEANUP-guiden» ved det forkastede terskelalternativet er fjernet; den hadde ingen kilderad, og guiden (KLAR-KILDE-0001 K28) setter `default_score = 0.6` som poengsum for spaCy-treff, ikke en terskel; ellers uendret. Versjon 1.3, 2026-10-27: «ordnes etter risiko» merket som plan, ikke implementert (koden ordner flaggene etter tid). Versjon 1.2, 2026-10-26: union av flagg fra begge lag, uten terskel (v1.1); v1.2 parer flaggene på tidsoverlapp mellom ordspenn.

## Kontekst

Personvernflagg er forslag til menneskelig vurdering (KLAR-ADR-0002, KLAR-ADR-0008). Et oversett navn eller en oversett sensitiv opplysning kan slippe gjennom til publisering. Et falskt flagg koster et menneske noen sekunder. Flagg skal ordnes i en kø etter risiko. **Plan, ikke implementert (v1.3):** flaggene ordnes i dag etter tid, ikke etter risiko: `arkivklarering/personvern.py:223` sorterer flaggene i ett lag etter start, stopp, kategori og kilde, og `:321` sorterer unionen etter start, stopp, kategori og lag. Ingen kø eller risikoordning er bygget (den hører til godkjenningsflaten, KLAR-ARK-0006 «Etter v1.0»).

## Beslutning

Recall er hovedmålet. Flaggmotoren kjører med terskel 0, slik at alle gjenkjenneres treff beholdes, og flere gjenkjennere kombineres (spaCy via Presidio, NB-BERT-base-ner, mønstre og nøkkelordlister) selv om det gir overlapp og flere falske flagg. Utviklingsmålingen rapporterer recall først, og et mål på presisjon følger med. Et manglende flagg er ingen garanti, og et flagg er ikke en avgjørelse; ingenting fjernes eller endres.

## Konsekvenser

- Flere falske flagg og en lengre kø. Køen skal ordnes etter risiko (kategori og score), ikke ved å skjule flagg; v1.3: køen og risikoordningen er plan, ikke implementert (se Kontekst).
- Recall måles på et etablert norsk NER-gullsett (NorNE, validation) for personer og steder, per målform. Det sier ikke noe om recall på arkivlyd, dialekt og talespråk, som er målt ikke.
- Terskelen kan heves senere for presisjon når recall er målt på pilotdata, men først etter en ny beslutning.
- Rålaget (verbatim) har små bokstaver uten tegnsetting, og store bokstaver er et sterkt signal for navnegjenkjenning. Flagg lages derfor på begge lag, og rålagets recall forventes lavere (målt i KLAR-EVAL-0005).

- **Union (v1.1):** flagg fra rålaget og det normaliserte laget slås sammen (samme kategori, overlappende tid), og et flagg som bare finnes i ett lag beholdes alltid. Ingen terskel filtrerer bort flagg i denne versjonen. Det gir høyere recall enn hvert lag alene og flere flagg uten motstykke i det andre laget; hva det koster i presisjon på arkivlyd er ikke målt (DEV-tall i KLAR-EVAL-0006, for få referanseflagg til å konkludere).

- **Paring på ordtidsstempler (v1.2):** unionen parer flagg med samme kategori som overlapper i tid mellom flaggets ordspenn i hvert lag (toleranse 0,5 s). Likheten mellom utdragene brukes bare til å velge når flere flagg overlapper i tid. Det erstatter v1.1, som parte på likhet fordi rålaget ga én cue over hele segmentet, og som kunne slå sammen to ulike personer i samme segment. Ordtidsstemplene er DTW-tidsstempler fra whisper.cpp (`-nfa -dtw large.v3`) for begge lag. Metoden `-ml 1 -sow` ble forkastet: for verbatim-modellen klumpet de siste ordene seg i segmentets slutt. DTW-tidene kommer fra forhåndsvalgte alignment-hoder for whisper-large-v3, ikke fra hoder funnet for NB-Whisper, og kan avvike fra faktiske ordgrenser med noen tideler av et sekund (målt bare mot det normaliserte lagets tider i røykfilen, ikke mot håndsatte grenser). Et flagg uten partner beholdes som før.

## Alternativer som ble vurdert

- Presisjon eller F1 som hovedmål: forkastet; et oversett navn er verre enn et falskt flagg.
- Terskel rundt 0,5–0,6: forkastet i v0; kutter treff uten at det er målt hva det koster i recall.
- Bare ett lag (rålaget, som ADR-0005 foreslo som grunnlag): forkastet i v0 fordi rålagets små bokstaver svekker NER; begge lag flagges.
