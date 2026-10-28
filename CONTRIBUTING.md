# Bidra til arkivklarering

*English: report bugs and propose changes by e-mail to eirik@ecodeco.no (security issues too, never in a public issue); pull requests must keep the frozen analysis code unchanged, add new versions of versioned documents instead of editing them, keep heavy data under the data root `ARKIVKLARERING_DATA`, and pass `pytest -q -m 'not tung'`. Contributions are licensed under AGPL-3.0-or-later.*

## Melde feil, få hjelp og foreslå endringer

Det offentlige repoet er [avalyset/arkivklarering-public](https://github.com/avalyset/arkivklarering-public), fra 2026-10-28, med én commit fra et rent tre (Zenodo-DOI 10.5281/zenodo.23723666). Arbeidsrepoet er privat ([KLAR-ADR-0010](docs/adr/KLAR-ADR-0010_arkivklarering_repo-privat-til-prereg_v1.1_2026-10-27.md)), og hele historikken er deponert med begrenset tilgang og tilgang på forespørsel (DOI 10.5281/zenodo.23723450), med lisenserklæring for hele historikken i [LICENSING-HISTORY.md](LICENSING-HISTORY.md) (A3, endret 2026-10-28; [KLAR-ADR-0020](docs/adr/KLAR-ADR-0020_arkivklarering_lisens-agpl_v1.4_2026-10-28.md)).

- **Feil, spørsmål og forslag** sendes per e-post til eieren, Eirik Botten Nicolaysen, <eirik@ecodeco.no> (`pyproject.toml`). Har du tilgang til GitHub-repoet, kan du bruke issues og pull requests der.
- **En feilrapport** bør ha commit (`git rev-parse HEAD`), kommandoen du kjørte, hele feilmeldingen, operativsystem, og om `source scripts/miljo.sh` var kjørt.
- **Legg aldri ved lyd fra arkiv eller museer, transkripsjoner av slik lyd eller personopplysninger** i en feilrapport, issue eller pull request. Lyd fra museet går aldri inn i git, sky eller GitHub (`docs/gt_fast.md`). Bruk den syntetiske røyktestlyden (`scripts/lag_testlyd.py`) til å vise feilen.

## Kjøreregler som gjelder bidrag

Fra [`CLAUDE.md`](CLAUDE.md) og repoets praksis:

1. **Analysekoden er låst med siste `testkjoring`-tagg** (nå `testkjoring-v12`). `scripts/kjor_testdel.sh` nekter å kjøre testdelene hvis `arkivklarering`, `kalibrering`, `tests`, `scripts` eller `.py`-filer under `eval/` er endret siden taggen. Endring i analysekoden krever eiers beslutning, en rad i avvikstabellen ([KLAR-LOG-0003](docs/KLAR-LOG-0003_arkivklarering_avvikstabell_v1.24_2026-10-28.md)) og en ny tagg; gamle tagger flyttes ikke (CLAUDE.md regel 5; AV-16, AV-18).
2. **Versjonerte dokumenter (`KLAR-*`) endres ikke.** En endring blir en ny fil med ny versjon og dato i navnet, og forrige versjon endres ikke (CLAUDE.md «Arbeidskø»; filnavnet etter [KLAR-ARK-0002](docs/KLAR-ARK-0002_arkivklarering_navnekonvensjon_v1.6_2026-10-28.md)). Nye nummer føres i [KLAR-ARK-0003](docs/KLAR-ARK-0003_arkivklarering_nummerregister_v1.27_2026-10-28.md). Kode, README og konfigurasjon er vanlige filer (ARK-0002 § 3), og git-historikken er versjoneringen.
3. **Beslutninger** skrives som ADR (MADR) i `docs/adr/`. Påstander om eksterne kilder får en rad med sitat i [KLAR-KILDE-0001](docs/KLAR-KILDE-0001_arkivklarering_kilderegister_v1.22_2026-10-28.md); `scripts/ground_truth.py` varsler om kildelenker uten rad. Kvalitetspåstander står bare i `KLAR-EVAL`-dokumentene.
4. **Tunge data, cacher og lyd ligger bare under datarota `ARKIVKLARERING_DATA`** (standard `/Volumes/Vault/arkivklarering` når Vault er montert, ellers `~/.local/share/arkivklarering`; `source scripts/miljo.sh`; [KLAR-ADR-0015](docs/adr/KLAR-ADR-0015_arkivklarering_tunge-data-kun-paa-vault_v1.1_2026-10-27.md)). Én tung kjøring (Whisper eller pyannote) om gangen (CLAUDE.md regel 6).
5. **Sjekk og endring holdes adskilt:** en sjekk rapporterer og reparerer ikke (CLAUDE.md regel 2). Nye skript eller utvidelser avtales med eieren først (regel 7).
6. **Testdelene** (`test`-splittene) er sperret i koden (`arkivklarering/evaldata.py`) og brukes ikke i utvikling.

Tester før hver pull request:

```bash
source scripts/miljo.sh
.venv/bin/python -m pytest -q -m 'not tung'               # raske tester;  -m tung  kjører Whisper og krever modellene
```

Det er ingen CI i repoet; testene kjøres lokalt.

## Slik skal en pull request se ut

- Én avgrenset endring, med en beskrivelse av hva som er endret og hvorfor, og henvisning til ADR, avvik (AV-nr.) eller veikartsteg der det finnes.
- Resultatet av `pytest -q -m 'not tung'` (antall bestått) i beskrivelsen.
- Ingen endring i analysekoden under `testkjoring`-taggen uten eiers beslutning (punkt 1).
- Nye versjoner av dokumenter i stedet for endringer i gamle (punkt 2).
- Ingen lyd, modeller, evalueringsdata, `ut/` eller `.env` (`.gitignore`).
- En linje i `CHANGELOG.md` under en oppføring «Ikke utgitt» øverst (lag den over den siste utgitte versjonen hvis den mangler).

## Lisens for bidrag

Egen kode er lisensiert GNU Affero General Public License v3.0 eller senere (`AGPL-3.0-or-later`, [LICENSE](LICENSE); Eiriks beslutning A2 2026-10-27), og bidrag lisensieres under den samme lisensen. Rettighetshaveren tilbyr i tillegg kommersiell lisens for egen kode (eirik@ecodeco.no); kode fra andre bidragsytere kan bare tas med i en kommersiell lisens etter egen avtale med bidragsyteren (det finnes ingen bidragsavtale ennå). Tredjepartskode beholder sin lisens (`NOTICE`).

## Atferd

Vær saklig og respektfull mot alle, også i uenighet. Trakassering og nedsettende omtale av personer godtas ikke. Personer som omtales i opptak, skal ikke kunne identifiseres gjennom det du skriver.

## Sikkerhetsproblemer

Sårbarheter, og personopplysninger eller lyd som har havnet i repoet, meldes direkte per e-post til <eirik@ecodeco.no>, ikke i en issue eller pull request.
