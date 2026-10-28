#!/usr/bin/env python3
"""Lager kalibrering/KLAR-MANUS-0002_arkivklarering_testmanus_v1.3_<dato>.tsv.

TESTMANUS (v1.2: rettet før låsing, se KLAR-LOG-0001; v1.3: alle sju telefonnumre byttet, AV-29) for H4 i KLAR-PREREG-0001: 6 nye setninger per klasse og målform (13 klasser, 156 setninger), andre formuleringer,
navn, tall og steder enn i justeringsmanuset KLAR-MANUS-0001. Samme format og målelementer.

Manuset er skrevet uten å kjøre noen setning gjennom rørledningen, mønstrene eller ordlistene, og uten å lese ordlistene.
Det skal ikke kjøres gjennom dem før innlesingen er gjort og testdelene åpnes (KLAR-PREREG-0001). Sha256 av fila står i
preregistreringen; `tests/test_manus.py` kontrollerer den. Filen skal ikke endres etter det: en endring er en ny versjon
og et avvik som føres i KLAR-LOG-0001. H4 gjennomføres ikke i v1.0 (AV-27). v1.3 (AV-29) bytter alle sju telefonnumrene (tel01–tel06 og
kom02) til Nkoms nummerserie for TV- og filmproduksjon (68 05 00 00–68 05 99 99, blokkert for ordinær bruk), så manuset kan
publiseres: to lå i serier Nkom har tildelt en tilbyder, fire i ledige serier og ett i en blokkert serie. Ellers er setningene uendret. Sha256 for v1.2
står i preregistreringen, sha256 for v1.3 i `tests/test_manus.py`.

Alle personnavn er oppdiktede. Fødselsnumre har riktig format og fiktive sifre med bevisst ugyldig kontrollsiffer.
Telefonnumre er fiktive og ligger i Nkoms serie for TV- og filmproduksjon (Nkoms E.164-liste, KLAR-KILDE-0001, NK-radene).
E-postadresser bruker reserverte eksempeldomener. Stedsnavn er fra Gudbrandsdalen.
"""
import datetime
import json
import pathlib

DATO = datetime.date.today().isoformat()


def fnr(dato6, individ3):
    """Fødselsnummer med bevisst ugyldig kontrollsiffer 2 (k2), så det ikke kan være et gyldig nummer."""
    d = [int(c) for c in dato6 + individ3]
    k1 = (11 - sum(a * b for a, b in zip(d, (3, 7, 6, 1, 8, 9, 4, 5, 2))) % 11) % 11
    d1 = d + [k1 if k1 != 10 else 0]
    k2 = (11 - sum(a * b for a, b in zip(d1, (5, 4, 3, 2, 7, 6, 5, 4, 3, 2))) % 11) % 11
    ugyldig = (k2 + 3) % 10
    return f"{dato6}{individ3}{d1[-1]}{ugyldig}"


def el(typ, *former):
    return {"type": typ, "former": list(former)}


P = "person"; S = "sted"; D = "dato"; F = "fødselsår"; T = "telefon"; N = "fødselsnummer"; E = "e-post"
H = "helse"; O = "økonomi"; K = "konflikt"; R = "religion"; L = "politikk"

NR = [fnr("041256", "271"), fnr("180839", "342"), fnr("260771", "415"), fnr("091147", "558"), fnr("300684", "629"), fnr("130322", "703")]


def nr(i):
    return f"{NR[i][:6]} {NR[i][6:]}"


def par(nb, nn, e_nb, e_nn=None):
    return (nb, nn, e_nb, e_nn if e_nn is not None else e_nb)


MANUS = [
    ("per", "person", [
        par("Programleder Gunnhild Bjerkås intervjuet bonden i studio.", "Programleiar Gunnhild Bjerkås intervjua bonden i studio.", [el(P, "Gunnhild Bjerkås")]),
        par("Kirkekoret ble ledet av Ivar Rustad i mange år.", "Kyrkjekoret vart leidd av Ivar Rustad i mange år.", [el(P, "Ivar Rustad")]),
        par("Marit Sandbu og Knut Aaseth var sammen om å starte lokallaget.", "Marit Sandbu og Knut Aaseth stod saman om å starte lokallaget.", [el(P, "Marit Sandbu"), el(P, "Knut Aaseth")]),
        par("Mange husker læreren Synnøve Lien fra småskolen.", "Mange hugsar læraren Synnøve Lien frå småskulen.", [el(P, "Synnøve Lien")]),
        par("Vi hører nå et opptak med Halfdan Moen på fele.", "Vi høyrer no eit opptak med Halfdan Moen på fele.", [el(P, "Halfdan Moen")]),
        par("Sangen ble skrevet av Berit Kolstad til bryllupet.", "Songen vart skriven av Berit Kolstad til bryllaupet.", [el(P, "Berit Kolstad")]),
    ], []),
    ("ste", "sted", [
        par("Været på Dombås er blitt verre utover dagen.", "Været på Dombås har vorte verre utover dagen.", [el(S, "Dombås")]),
        par("Seterdrifta på Øvre Rusten ble lagt ned for lenge siden.", "Seterdrifta på Øvre Rusten vart lagd ned for lenge sidan.", [el(S, "Øvre Rusten")]),
        par("Toget stanset ved Tretten, Øyer og Harpefoss.", "Toget stoppa ved Tretten, Øyer og Harpefoss.", [el(S, "Tretten"), el(S, "Øyer"), el(S, "Harpefoss")]),
        par("Elva Sjoa renner gjennom Heidal før den møter Lågen.", "Elva Sjoa renn gjennom Heidal før ho møter Lågen.", [el(S, "Sjoa"), el(S, "Heidal"), el(S, "Lågen")]),
        par("Vi besøkte Vågå, Lom og Skjåk i sommer.", "Vi besøkte Vågå, Lom og Skjåk i sommar.", [el(S, "Vågå"), el(S, "Lom"), el(S, "Skjåk")]),
        par("Han overnattet på Follebu før turen til Lesja.", "Han overnatta på Follebu før turen til Lesja.", [el(S, "Follebu"), el(S, "Lesja")]),
    ], []),
    ("dat", "dato", [
        par("Skolen åpnet 17. oktober 1957 med femti elever.", "Skulen opna 17. oktober 1957 med femti elevar.", [el(D, "17. oktober 1957")]),
        par("Dåpen står oppført med dato 02.08.1984 i kirkeboka.", "Dåpen står oppført med dato 02.08.1984 i kyrkjeboka.", [el(D, "02.08.1984", "2. august 1984")]),
        par("Hun giftet seg 5. januar 1923 i bygdekirken.", "Ho gifta seg 5. januar 1923 i bygdekyrkja.", [el(D, "5. januar 1923")]),
        par("Flommen kom natt til 28. februar 1990.", "Flaumen kom natt til 28. februar 1990.", [el(D, "28. februar 1990")]),
        par("Minnesmerket ble avduket 8. mai 1995.", "Minnesmerket vart avduka 8. mai 1995.", [el(D, "8. mai 1995")]),
        par("Rådmannen skrev under 11. september 1976.", "Rådmannen skreiv under 11. september 1976.", [el(D, "11. september 1976")]),
    ], []),
    ("fod", "fødselsår", [
        par("Mormor er født i 1922 og husker krigsårene godt.", "Mormor er fødd i 1922 og hugsar krigsåra godt.", [el(F, "1922")]),
        par("Han ble født i 1947, året etter at gården ble delt.", "Han vart fødd i 1947, året etter at garden vart delt.", [el(F, "1947")]),
        par("Skuespilleren, født 1962, var gjest i programmet.", "Skodespelaren, fødd 1962, var gjest i programmet.", [el(F, "1962")]),
        par("Hun er født i 1938 og har skrevet bygdebok.", "Ho er fødd i 1938 og har skrive bygdebok.", [el(F, "1938")]),
        par("Felespilleren, født i 1930, spilte på bryllup i hele dalen.", "Felespelaren, fødd i 1930, spelte på bryllaup i heile dalen.", [el(F, "1930")]),
        par("Han er født i 1955 og var yngst av sju søsken.", "Han er fødd i 1955 og var yngst av sju sysken.", [el(F, "1955")]),
    ], []),
    ("tel", "telefon", [
        par("Du kan ringe oss på 68 05 03 21 i åpningstiden.", "Du kan ringje oss på 68 05 03 21 i opningstida.", [el(T, "68050321", "68 05 03 21")]),
        par("Kommunen har telefon 68 05 77 12.", "Kommunen har telefon 68 05 77 12.", [el(T, "68057712", "68 05 77 12")]),
        par("Meld fra til vaktsentralen på 68 05 20 46 om du ser noe.", "Meld frå til vaktsentralen på 68 05 20 46 om du ser noko.", [el(T, "68052046", "68 05 20 46")]),
        par("Bestill billett på nummer 68 05 62 09 før klokka tre.", "Bestill billett på nummer 68 05 62 09 før klokka tre.", [el(T, "68056209", "68 05 62 09")]),
        par("Mobilnummeret hennes er 68 05 18 73.", "Mobilnummeret hennar er 68 05 18 73.", [el(T, "68051873", "68 05 18 73")]),
        par("Send en tekstmelding til 68 05 31 85 for å delta i konkurransen.", "Send ei tekstmelding til 68 05 31 85 for å delta i konkurransen.", [el(T, "68053185", "68 05 31 85")]),
    ], []),
    ("fnr", "fødselsnummer", [
        par(f"Mannen oppga {nr(0)} som fødselsnummer ved innmeldingen.", f"Mannen oppgav {nr(0)} som fødselsnummer ved innmeldinga.", [el(N, NR[0], nr(0))]),
        par(f"I skjemaet står det {nr(1)} under personnummer.", f"I skjemaet står det {nr(1)} under personnummer.", [el(N, NR[1], nr(1))]),
        par(f"Arkivet har registrert {nr(2)} på feil person.", f"Arkivet har registrert {nr(2)} på feil person.", [el(N, NR[2], nr(2))]),
        par(f"Saksbehandleren leste opp {nr(3)}, og så var det klart.", f"Saksbehandlaren las opp {nr(3)}, og så var det klart.", [el(N, NR[3], nr(3))]),
        par(f"Hun skrev fødselsnummeret {nr(4)} på lappen.", f"Ho skreiv fødselsnummeret {nr(4)} på lappen.", [el(N, NR[4], nr(4))]),
        par(f"Pasientens nummer, {nr(5)}, ble lest inn på lydbåndet.", f"Pasienten sitt nummer, {nr(5)}, vart lese inn på lydbandet.", [el(N, NR[5], nr(5))]),
    ], []),
    ("epo", "e-post", [
        par("Skriv til anne.lien@example.net hvis du har bilder.", "Skriv til anne.lien@example.net viss du har bilete.", [el(E, "anne.lien@example.net")]),
        par("Du når programmet på radio@lokalradio.example hele uka.", "Du når programmet på radio@lokalradio.example heile veka.", [el(E, "radio@lokalradio.example")]),
        par("Meld deg på via pamelding@lag.example.org innen mandag.", "Meld deg på via pamelding@lag.example.org innan måndag.", [el(E, "pamelding@lag.example.org")]),
        par("Han bruker adressen bjorn.hagen@example.com til alt.", "Han brukar adressa bjorn.hagen@example.com til alt.", [el(E, "bjorn.hagen@example.com")]),
        par("Send arkivspørsmål til arkiv@bygdemuseet.example, så svarer vi.", "Send arkivspørsmål til arkiv@bygdemuseet.example, så svarer vi.", [el(E, "arkiv@bygdemuseet.example")]),
        par("Den gamle adressen sofie_moen@example.org er ikke lenger i bruk.", "Den gamle adressa sofie_moen@example.org er ikkje lenger i bruk.", [el(E, "sofie_moen@example.org")]),
    ], []),
    ("hel", "helse", [
        par("Bestemor fikk demens og flyttet til sykehjem.", "Bestemor fekk demens og flytta til sjukeheim.", [el(H, "demens"), el(H, "sykehjem")], [el(H, "demens"), el(H, "sjukeheim", "sykehjem")]),
        par("Han hadde tuberkulose som gutt og lå lenge på sanatorium.", "Han hadde tuberkulose som gut og låg lenge på sanatorium.", [el(H, "tuberkulose"), el(H, "sanatorium")]),
        par("Hun døde av lungebetennelse våren etter krigen.", "Ho døydde av lungebetennelse våren etter krigen.", [el(H, "lungebetennelse")]),
        par("Faren fikk astma og måtte slutte i skogen.", "Faren fekk astma og måtte slutte i skogen.", [el(H, "astma")]),
        par("Hun gikk i terapi etter ulykken og var sykmeldt i et halvt år.", "Ho gjekk i terapi etter ulukka og var sjukmeldt i eit halvt år.", [el(H, "terapi"), el(H, "sykmeldt")], [el(H, "terapi"), el(H, "sjukmeldt", "sykmeldt")]),
        par("Mannen satt i rullestol etter ryggskaden.", "Mannen sat i rullestol etter ryggskaden.", [el(H, "rullestol"), el(H, "ryggskaden", "ryggskade")]),
    ], []),
    ("oko", "økonomi", [
        par("Familien tok opp lån og pantsatte skogen.", "Familien tok opp lån og pantsette skogen.", [el(O, "lån"), el(O, "pantsatte", "pantsette")]),
        par("Han skyldte skatt for tre år og fikk namsmannen på døra.", "Han skulda skatt for tre år og fekk namsmannen på døra.", [el(O, "namsmannen", "namsmann")]),
        par("Hun fikk dagpenger etter at sagbruket ble nedlagt.", "Ho fekk dagpengar etter at sagbruket vart lagt ned.", [el(O, "dagpenger", "dagpengar")]),
        par("Etter betalingsanmerkningen fikk han ikke lån i banken.", "Etter betalingsmerknaden fekk han ikkje lån i banken.", [el(O, "betalingsanmerkningen", "betalingsanmerkning")], [el(O, "betalingsmerknaden", "betalingsmerknad", "betalingsanmerkninga", "betalingsanmerkningen")]),
        par("Familien var avhengig av økonomisk støtte fra kommunen.", "Familien var avhengig av økonomisk støtte frå kommunen.", [el(O, "økonomisk støtte")]),
        par("Han ble tynget av spillegjeld og solgte traktoren.", "Han var tynga av spelegjeld og selde traktoren.", [el(O, "spillegjeld", "spelegjeld")]),
    ], []),
    ("kon", "konflikt", [
        par("Striden om grensegjerdet havnet hos lensmannen.", "Striden om grensegjerdet hamna hos lensmannen.", [el(K, "striden", "strid"), el(K, "lensmannen", "lensmann")]),
        par("Hun ble utsatt for trusler fra en tidligere samboer.", "Ho vart utsett for truslar frå ein tidlegare sambuar.", [el(K, "trusler", "truslar")]),
        par("Søsknene havnet i en bitter arvekrangel.", "Syskena hamna i ein bitter arvekrangel.", [el(K, "arvekrangel")]),
        par("Saken ble anket til lagmannsretten.", "Saka vart anka til lagmannsretten.", [el(K, "anket", "anke", "anka"), el(K, "lagmannsretten", "lagmannsrett")]),
        par("Han ble utestengt fra laget etter en slåsskamp.", "Han vart utestengd frå laget etter ein slåstkamp.", [el(K, "slåsskamp", "slåstkamp")]),
        par("Hun varslet om trakassering på arbeidsplassen.", "Ho varsla om trakassering på arbeidsplassen.", [el(K, "trakassering")]),
    ], []),
    ("rel", "religion", [
        par("Han var med i Indremisjonen og leste i bibelen hver kveld.", "Han var med i Indremisjonen og las i bibelen kvar kveld.", [el(R, "Indremisjonen")]),
        par("Hun døpte barna i Den norske kirke.", "Ho døypte borna i Den norske kyrkja.", [el(R, "Den norske kirke")], [el(R, "Den norske kyrkja", "Den norske kirke")]),
        par("Familien var buddhister og reiste til tempelet hvert år.", "Familien var buddhistar og reiste til tempelet kvart år.", [el(R, "buddhister")], [el(R, "buddhistar", "buddhister")]),
        par("Han ble baptist som ung mann.", "Han vart baptist som ung mann.", [el(R, "baptist")]),
        par("De var kvekere og nektet å sverge ed.", "Dei var kvekarar og nekta å sverje eid.", [el(R, "kvekere")], [el(R, "kvekarar", "kvekere")]),
        par("Hun konverterte til jødedommen i voksen alder.", "Ho konverterte til jødedommen i vaksen alder.", [el(R, "jødedommen", "jødedom")]),
    ], []),
    ("pol", "politikk", [
        par("Han satt i kommunestyret for Høyre i to perioder.", "Han sat i kommunestyret for Høgre i to periodar.", [el(L, "Høyre")], [el(L, "Høgre", "Høyre")]),
        par("Hun var aktiv i Rødt og i fagbevegelsen.", "Ho var aktiv i Raudt og i fagrørsla.", [el(L, "Rødt")], [el(L, "Raudt", "Rødt")]),
        par("Bestefar stemte Venstre helt til han døde.", "Bestefar stemde Venstre heilt til han døydde.", [el(L, "Venstre")]),
        par("Hun meldte seg inn i Sosialistisk Venstreparti som student.", "Ho melde seg inn i Sosialistisk Venstreparti som student.", [el(L, "Sosialistisk Venstreparti")]),
        par("Hun stilte til valg for Miljøpartiet De Grønne.", "Ho stilte til val for Miljøpartiet Dei Grøne.", [el(L, "Miljøpartiet De Grønne")], [el(L, "Miljøpartiet Dei Grøne", "Miljøpartiet De Grønne")]),
        par("Bestefaren var med i Bondepartiet før krigen.", "Bestefaren var med i Bondepartiet før krigen.", [el(L, "Bondepartiet")]),
    ], []),
    ("kom", "kombinert", [
        par("Reidun Hovdesæter, født i 1936 på Kvam, fikk revmatisme som ung.", "Reidun Hovdesæter, fødd i 1936 på Kvam, fekk revmatisme som ung.", [el(P, "Reidun Hovdesæter"), el(F, "1936"), el(S, "Kvam"), el(H, "revmatisme")]),
        par("Sverre Bakkelien ringte 68 05 52 80 den 21. mars 1988 om arvestriden.", "Sverre Bakkelien ringde 68 05 52 80 den 21. mars 1988 om arvestriden.", [el(P, "Sverre Bakkelien"), el(T, "68055280", "68 05 52 80"), el(D, "21. mars 1988"), el(K, "arvestriden", "arvestrid")]),
        par("Torunn Skjelbrekke fra Garmo er kveker og stemmer Venstre.", "Torunn Skjelbrekke frå Garmo er kvekar og stemmer Venstre.", [el(P, "Torunn Skjelbrekke"), el(S, "Garmo"), el(R, "kveker"), el(L, "Venstre")], [el(P, "Torunn Skjelbrekke"), el(S, "Garmo"), el(R, "kvekar", "kveker"), el(L, "Venstre")]),
        par("Arne Oddvollen, født i 1958, bor på Nedre Frya og fikk dagpenger.", "Arne Oddvollen, fødd i 1958, bur på Nedre Frya og fekk dagpengar.", [el(P, "Arne Oddvollen"), el(F, "1958"), el(S, "Nedre Frya"), el(O, "dagpenger")], [el(P, "Arne Oddvollen"), el(F, "1958"), el(S, "Nedre Frya"), el(O, "dagpengar", "dagpenger")]),
        par("Liv Brekkeslåen på Bjorli ble anmeldt for trusler 14. juli 1993.", "Liv Brekkeslåen på Bjorli vart meld for truslar 14. juli 1993.", [el(P, "Liv Brekkeslåen"), el(S, "Bjorli"), el(K, "anmeldt", "anmeldte"), el(K, "trusler"), el(D, "14. juli 1993")], [el(P, "Liv Brekkeslåen"), el(S, "Bjorli"), el(K, "meld", "anmeldt"), el(K, "truslar", "trusler"), el(D, "14. juli 1993")]),
        par("Magnus Rudisæter, født 1949, er buddhist og bor på Hafjell.", "Magnus Rudisæter, fødd 1949, er buddhist og bur på Hafjell.", [el(P, "Magnus Rudisæter"), el(F, "1949"), el(R, "buddhist"), el(S, "Hafjell")]),
    ], [0, 1, 2, 3, 4, 5]),
]

def main():
    ut = pathlib.Path("kalibrering") / f"KLAR-MANUS-0002_arkivklarering_testmanus_v1.3_{DATO}.tsv"
    ut.parent.mkdir(exist_ok=True)
    rader = []
    for kode, klasse, sett, dialekt in MANUS:
        for i, (nb, nn, e_nb, e_nn) in enumerate(sett, 1):
            ja = "ja" if (i - 1) in dialekt else "nei"
            rader.append((f"{kode}{i:02d}nb", "nb", klasse, nb, e_nb, ja))
            rader.append((f"{kode}{i:02d}nn", "nn", klasse, nn, e_nn, ja))
    hode = ["# arkivklarering testmanus KLAR-MANUS-0002 v1.3: radiolignende setninger per kategori, hver på bokmål og nynorsk.",
            "# STATUS: urørt testmateriale for H4 i KLAR-PREREG-0001. IKKE kjørt gjennom rørledningen, mønstrene eller ordlistene. H4 gjennomføres ikke i v1.0 (AV-27). v1.3 (AV-29) bytter bare de sju telefonnumrene; sha256 for den registrerte v1.2 står i preregistreringen.",
            "# Personnavn er oppdiktede. Fødselsnumre har riktig format, fiktive sifre og bevisst ugyldig kontrollsiffer. Telefonnumre er fiktive og ligger i Nkoms serie for TV- og filmproduksjon, 68 05 00 00–68 05 99 99 (v1.3, AV-29: alle byttet dit), e-postadresser bruker reserverte eksempeldomener.",
            "# elementer: det som må flagges, {type: kategori, former: [skriveformer]}. Tall skrives som sifre; utdata normaliseres (tallord -> sifre) før sammenligning (vendor/norsk_tale/score.py).",
            "# dialektutvalg=ja: setningene som leses inn av talere med dialekt (norsk-tale-riggens dialektmodus).",
            "id\tmalform\tklasse\tsetning\telementer\tdialektutvalg"]
    linjer = hode + ["\t".join([i, m, k, s, json.dumps(e, ensure_ascii=False), d]) for i, m, k, s, e, d in rader]
    ut.write_text("\n".join(linjer) + "\n", encoding="utf-8")
    print(ut, len(rader), "rader,", len({r[2] for r in rader}), "klasser")


if __name__ == "__main__":
    from arkivklarering.miljo import krev_vault_miljo
    krev_vault_miljo()
    main()
