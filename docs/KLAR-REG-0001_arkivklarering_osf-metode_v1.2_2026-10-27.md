# Clearance-first processing of Norwegian local-radio and oral-history audio archives: method registration

Versjon 1.2, 2026-10-27 (v1.2: kildemerknaden under streken er utvidet med Mediesök, KLAR-KILDE-0001 RG-01; registrert tekst er uendret; v1.1: kildemerknad nederst, under streken, til «primarily for search and description», KLAR-KILDE-0001 AM-05 og AA-04; denne linjen og merknaden er ikke del av registrert tekst, alle andre linjer er byte-like med v1.0; v1.0: kopi av teksten registrert på OSF, https://osf.io/fbme7/, uten versjonslinje).

Author: Eirik Botten Nicolaysen, EcoDeco AS (ORCID 0009-0001-9188-6788)
Date: 2026-10-26
Status: Method and priority registration. A separate, study-specific preregistration with a locked analysis plan will be filed before any pilot data are processed.

## Problem
Digitised local-radio and oral-history archives in Norway cannot be published until each recording has been cleared for personal data and third-party music rights. Clearance is done by staff and volunteers listening through every hour. For archives of thousands of hours this listening, not digitisation or transcription, is the bottleneck.

## Framing (the claim of this registration)
Prior systems for audiovisual archives (Indiana University's Audiovisual Metadata Platform; the American Archive of Public Broadcasting's FixIt+; the National Library of Sweden's Mediesök; ASR on the Danish Royal Library's and Netherlands Institute for Sound and Vision's broadcast archives) use automatic processing primarily for search and description. This work treats clearance before publication as the primary task, with searchability as a by-product, and targets Norwegian speech in both written standards (Bokmål and Nynorsk) and dialect-heavy material.

## Pipeline
All processing runs locally; audio does not leave the holding institution.
1. Speech/music segmentation; pure-music segments proposed for cutting, speech-over-music sent to human review.
2. Transcription with the National Library of Norway's NB-Whisper in two layers: an untouched verbatim layer and a normalised, searchable layer (Nynorsk or Bokmål), with timestamps.
3. Deterministic entity correction against an auditable alias table (local place and farm names, institution names), every substitution logged and reversible. No fuzzy matching.
4. Flagging of candidate personal data (names via Norwegian named-entity recognition; health, finances, conflicts and other sensitive categories) with timestamps; review queue ordered by risk.
5. Draft catalogue record (title, date, speakers, places, subjects) for human correction.
Human reviewers decide every cut and every publication. The system only proposes.

## Outcomes to be measured (thresholds locked in the study preregistration)
- Recall and precision of clearance-relevant segments (personal data; music) flagged by the system, against a gold standard from full human listening.
- Reviewer time per recording: flag-guided review vs. full listening, on the same material, counterbalanced.
- Word error rate on dialect speech, against volunteer-corrected transcripts.
- Share of draft catalogue fields accepted without change.

## Principles
Preregistration before data processing; open code with DOI; reversible corrections with logs; corrections and negative results published.

---

**Kildemerknad 2026-10-27, ikke del av registrert tekst:** “primarily for search and description” (under «Framing») er bare delvis dekket av kildene: AMP «mass description» (KLAR-KILDE-0001 K05), FIX IT+ «improve the searchability» (K17), Mediesök «by searching through AI-transcribed text» og «improve searchability» (K71; kilden dekker søk, men «description» står ikke i den). Se KLAR-KILDE-0001 AM-05, AA-04, RG-01.
