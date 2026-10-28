#!/usr/bin/env python3
"""Lager kalibrering/KLAR-MANUS-0001_arkivklarering_justeringsmanus_v1.2_<dato>.tsv.

Manus for kjedekalibrering av personvernflaggene: radiolignende setninger per kategori, hver på bokmål og nynorsk.
Alle personnavn er oppdiktede. Fødselsnumre har riktig format og fiktive sifre, med bevisst ugyldig kontrollsiffer (de kan
ikke være ekte). Telefonnumre følger riktig format og har fiktive sifre. v1.2 (AV-29): alle telefonnumrene er byttet til Nkoms
nummerserie for TV- og filmproduksjon (68 05 00 00–68 05 99 99, blokkert for ordinær bruk); fem av de seks gamle lå i serier Nkom
har tildelt en tilbyder, det sjette i en ledig serie (Nkoms E.164-liste, KLAR-KILDE-0001, NK-radene). E-postadresser bruker
reserverte eksempeldomener. Gards- og stedsnavn er fra Gudbrandsdalen.

Kolonner som i norsk-tale (kalibrering/manus_v1.tsv): id, malform, klasse, setning, elementer (JSON), dialektutvalg.
`elementer` er det som må flagges: {"type": <kategori>, "former": [aksepterte skriveformer]}.
Kategoriene er de samme som i personvern.KATEGORI.
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
    ugyldig = (k2 + 3) % 10  # alltid et annet siffer enn det riktige
    return f"{dato6}{individ3}{d1[-1]}{ugyldig}"


def el(typ, *former):
    return {"type": typ, "former": list(former)}


# (kode, klasse, [(nb, nn, elementer_nb, elementer_nn)], dialektutvalg-indekser)
P = "person"; S = "sted"; D = "dato"; F = "fødselsår"; T = "telefon"; N = "fødselsnummer"; E = "e-post"
H = "helse"; O = "økonomi"; K = "konflikt"; R = "religion"; L = "politikk"

NR = [fnr("010163", "123"), fnr("150575", "456"), fnr("230248", "789"), fnr("311290", "321"), fnr("070854", "654"), fnr("120300", "987")]


def par(nb, nn, e_nb, e_nn=None):
    return (nb, nn, e_nb, e_nn if e_nn is not None else e_nb)


MANUS = [
    ("per", "person", [
        par("Ordføreren ønsket Halvor Brekkebu velkommen til jubileet.", "Ordføraren ønskte Halvor Brekkebu velkommen til jubileet.", [el(P, "Halvor Brekkebu")]),
        par("Reportasjen handler om Sigrun Haugvold og hesten hennes.", "Reportasjen handlar om Sigrun Haugvold og hesten hennar.", [el(P, "Sigrun Haugvold")]),
        par("Vi snakket med Torbjørn Stuvstad etter konserten.", "Vi snakka med Torbjørn Stuvstad etter konserten.", [el(P, "Torbjørn Stuvstad")]),
        par("Eli Marit Vinstra leste dikt fra scenen.", "Eli Marit Vinstra las dikt frå scena.", [el(P, "Eli Marit Vinstra")]),
        par("Ragnhild Dalsegg og Anders Fjellheim fortalte om oppveksten.", "Ragnhild Dalsegg og Anders Fjellheim fortalde om oppveksten.", [el(P, "Ragnhild Dalsegg"), el(P, "Anders Fjellheim")]),
        par("Takk til Oddvar Granheim som kom innom studio i dag.", "Takk til Oddvar Granheim som kom innom studio i dag.", [el(P, "Oddvar Granheim")]),
    ], []),
    ("ste", "sted", [
        par("Vi sender direkte fra Vinstra i kveld.", "Vi sender direkte frå Vinstra i kveld.", [el(S, "Vinstra")]),
        par("Gården Nordre Brenden ligger like ved Hundorp.", "Garden Nordre Brenden ligg like ved Hundorp.", [el(S, "Nordre Brenden"), el(S, "Hundorp")]),
        par("Veien over Gålåvatnet var stengt fra Espedalen til Skåbu.", "Vegen over Gålåvatnet var stengd frå Espedalen til Skåbu.", [el(S, "Gålåvatnet"), el(S, "Espedalen"), el(S, "Skåbu")]),
        par("Han vokste opp på Bjølstad i Sør-Fron.", "Han voks opp på Bjølstad i Sør-Fron.", [el(S, "Bjølstad"), el(S, "Sør-Fron", "Sørfron")]),
        par("Markedet på Otta samler folk fra hele Sel og Dovre.", "Marknaden på Otta samlar folk frå heile Sel og Dovre.", [el(S, "Otta"), el(S, "Sel"), el(S, "Dovre")]),
        par("Skolebussen går fra Fåvang til Ringebu hver morgen.", "Skulebussen går frå Fåvang til Ringebu kvar morgon.", [el(S, "Fåvang"), el(S, "Ringebu")]),
    ], []),
    ("dat", "dato", [
        par("Møtet ble holdt 3. november 1965 i bygdehuset.", "Møtet vart halde 3. november 1965 i bygdehuset.", [el(D, "3. november 1965")]),
        par("Brevet er datert 15.03.1972 og ligger i arkivet.", "Brevet er datert 15.03.1972 og ligg i arkivet.", [el(D, "15.03.1972", "15. mars 1972")]),
        par("Den 12. juni 1948 kom jernbanen til bygda.", "Den 12. juni 1948 kom jernbana til bygda.", [el(D, "12. juni 1948")]),
        par("Skjenkebevillingen utløp 1. desember 1999.", "Skjenkeløyvet gjekk ut 1. desember 1999.", [el(D, "1. desember 1999")]),
        par("Gudstjenesten 24. desember 1957 ble sendt på radio.", "Gudstenesta 24. desember 1957 vart sendt på radio.", [el(D, "24. desember 1957")]),
        par("Protokollen fra 9. mai 1981 mangler to sider.", "Protokollen frå 9. mai 1981 manglar to sider.", [el(D, "9. mai 1981")]),
    ], []),
    ("fod", "fødselsår", [
        par("Hun er født i 1934 og har bodd i bygda hele livet.", "Ho er fødd i 1934 og har budd i bygda heile livet.", [el(F, "1934")]),
        par("Han var født 1951 og vokste opp på en liten gård.", "Han var fødd 1951 og voks opp på ein liten gard.", [el(F, "1951")]),
        par("Bestemoren min er født i 1928.", "Bestemora mi er fødd i 1928.", [el(F, "1928")]),
        par("Sangeren, født i 1969, slipper plate i høst.", "Songaren, fødd i 1969, gir ut plate i haust.", [el(F, "1969")]),
        par("Han ble født i 1943, midt under krigen.", "Han vart fødd i 1943, midt under krigen.", [el(F, "1943")]),
        par("Kunstneren, født i 1957, har utstilling i Lillehammer.", "Kunstnaren, fødd i 1957, har utstilling i Lillehammer.", [el(F, "1957"), el(S, "Lillehammer")]),
    ], []),
    ("tel", "telefon", [
        par("Ring oss på 68 05 45 67 hvis du vet mer.", "Ring oss på 68 05 45 67 viss du veit meir.", [el(T, "68054567", "68 05 45 67")]),
        par("Nummeret til redaksjonen er 68 05 33 44.", "Nummeret til redaksjonen er 68 05 33 44.", [el(T, "68053344", "68 05 33 44")]),
        par("Legevakten svarer på 68 05 12 34 hele døgnet.", "Legevakta svarer på 68 05 12 34 heile døgnet.", [el(T, "68051234", "68 05 12 34")]),
        par("Send en SMS til 68 05 76 54 og få svar i morgen.", "Send ein SMS til 68 05 76 54 og få svar i morgon.", [el(T, "68057654", "68 05 76 54")]),
        par("Du når meg på mobil 68 05 34 56 etter klokka fire.", "Du når meg på mobil 68 05 34 56 etter klokka fire.", [el(T, "68053456", "68 05 34 56")]),
        par("Kontoret har nummer 68 05 11 22.", "Kontoret har nummer 68 05 11 22.", [el(T, "68051122", "68 05 11 22")]),
    ], []),
    ("fnr", "fødselsnummer", [
        par(f"Fødselsnummeret hans er {NR[0][:6]} {NR[0][6:]}.", f"Fødselsnummeret hans er {NR[0][:6]} {NR[0][6:]}.", [el(N, NR[0], f"{NR[0][:6]} {NR[0][6:]}")]),
        par(f"Oppgi fødselsnummer {NR[1][:6]} {NR[1][6:]} i skjemaet.", f"Oppgi fødselsnummer {NR[1][:6]} {NR[1][6:]} i skjemaet.", [el(N, NR[1], f"{NR[1][:6]} {NR[1][6:]}")]),
        par(f"Saken gjelder personen med fødselsnummer {NR[2][:6]} {NR[2][6:]}.", f"Saka gjeld personen med fødselsnummer {NR[2][:6]} {NR[2][6:]}.", [el(N, NR[2], f"{NR[2][:6]} {NR[2][6:]}")]),
        par(f"Journalen er merket {NR[3][:6]} {NR[3][6:]}.", f"Journalen er merkt {NR[3][:6]} {NR[3][6:]}.", [el(N, NR[3], f"{NR[3][:6]} {NR[3][6:]}")]),
        par(f"Hun oppga {NR[4][:6]} {NR[4][6:]} som sitt personnummer.", f"Ho oppgav {NR[4][:6]} {NR[4][6:]} som sitt personnummer.", [el(N, NR[4], f"{NR[4][:6]} {NR[4][6:]}")]),
        par(f"Registeret har nummeret {NR[5][:6]} {NR[5][6:]} to ganger.", f"Registeret har nummeret {NR[5][:6]} {NR[5][6:]} to gonger.", [el(N, NR[5], f"{NR[5][:6]} {NR[5][6:]}")]),
    ], []),
    ("epo", "e-post", [
        par("Send meldingen til ola.hansen@example.org innen fredag.", "Send meldinga til ola.hansen@example.org innan fredag.", [el(E, "ola.hansen@example.org")]),
        par("Adressen er kari.bakken@example.com hvis du vil skrive.", "Adressa er kari.bakken@example.com viss du vil skrive.", [el(E, "kari.bakken@example.com")]),
        par("Redaksjonen svarer på post@eksempel.test hver dag.", "Redaksjonen svarer på post@eksempel.test kvar dag.", [el(E, "post@eksempel.test")]),
        par("Skriv til hilde.dalen@example.net med emnet radioarkiv.", "Skriv til hilde.dalen@example.net med emnet radioarkiv.", [el(E, "hilde.dalen@example.net")]),
        par("Tips kan sendes til tips@example.org uten navn.", "Tips kan sendast til tips@example.org utan namn.", [el(E, "tips@example.org")]),
        par("Min e-post er per.berg@example.com, og den er ny.", "Mi e-postadresse er per.berg@example.com, og ho er ny.", [el(E, "per.berg@example.com")]),
    ], []),
    ("hel", "helse", [
        par("Han var syk i flere år før han døde i 1952.", "Han var sjuk i fleire år før han døydde i 1952.", [el(H, "syk"), el(F, "1952")], [el(H, "sjuk"), el(F, "1952")]),
        par("Hun ble innlagt på sykehus etter hjerneslaget.", "Ho vart innlagd på sjukehus etter hjerneslaget.", [el(H, "sykehus"), el(H, "hjerneslaget", "hjerneslag")], [el(H, "sjukehus"), el(H, "hjerneslaget", "hjerneslag")]),
        par("Legen stilte diagnosen kreft i fjor.", "Legen sette diagnosen kreft i fjor.", [el(H, "diagnosen", "diagnose"), el(H, "kreft")]),
        par("Naboen slet med depresjon og angst i mange år.", "Naboen sleit med depresjon og angst i mange år.", [el(H, "depresjon"), el(H, "angst")]),
        par("Hun har diabetes og går til legetime hver måned.", "Ho har diabetes og går til legetime kvar månad.", [el(H, "diabetes"), el(H, "legetime")]),
        par("Han ble operert for hjerteinfarkt på Lillehammer.", "Han vart operert for hjerteinfarkt på Lillehammer.", [el(H, "operert"), el(H, "hjerteinfarkt"), el(S, "Lillehammer")]),
    ], []),
    ("oko", "økonomi", [
        par("Gården gikk konkurs, og familien satt igjen med stor gjeld.", "Garden gjekk konkurs, og familien sat att med stor gjeld.", [el(O, "konkurs"), el(O, "gjeld")]),
        par("Han fikk inkasso fordi regningen ikke ble betalt.", "Han fekk inkasso fordi rekninga ikkje vart betalt.", [el(O, "inkasso")]),
        par("Mange i bygda levde på sosialhjelp på åttitallet.", "Mange i bygda levde på sosialhjelp på åttitalet.", [el(O, "sosialhjelp")]),
        par("Hun var arbeidsledig og hadde økonomiske problemer.", "Ho var arbeidsledig og hadde økonomiske problem.", [el(O, "arbeidsledig"), el(O, "økonomiske problemer", "økonomiske problem")]),
        par("Banken tok tvangssalg av huset i 1991.", "Banken tok tvangssal av huset i 1991.", [el(O, "tvangssalg", "tvangssal")]),
        par("De snakket åpent om svart arbeid og svindel.", "Dei snakka ope om svart arbeid og svindel.", [el(O, "svart arbeid"), el(O, "svindel")]),
    ], []),
    ("kon", "konflikt", [
        par("Rettssaken mot naboen varte i tre uker.", "Rettssaka mot naboen varte i tre veker.", [el(K, "rettssaken", "rettssak")], [el(K, "rettssaka", "rettssak")]),
        par("Han ble dømt for vold og satt i fengsel.", "Han vart dømd for vald og sett i fengsel.", [el(K, "dømt"), el(K, "vold"), el(K, "fengsel")], [el(K, "dømd", "dømt"), el(K, "vald"), el(K, "fengsel")]),
        par("Konflikten mellom grendene endte med en tvist om vegen.", "Konflikten mellom grendene enda med ein tvist om vegen.", [el(K, "konflikten", "konflikt"), el(K, "tvist")]),
        par("Hun anmeldte mobbingen til politiet.", "Ho melde mobbinga til politiet.", [el(K, "anmeldte", "anmeldt"), el(K, "mobbingen", "mobbing")], [el(K, "mobbinga", "mobbing")]),
        par("Barnevernet overtok omsorgen etter skilsmissen.", "Barnevernet tok over omsorga etter skilsmissa.", [el(K, "barnevernet"), el(K, "skilsmissen", "skilsmisse")], [el(K, "barnevernet"), el(K, "skilsmissa", "skilsmisse")]),
        par("Naboene trakk saken inn for forliksrådet.", "Naboane trekte saka inn for forliksrådet.", [el(K, "forliksrådet", "forliksråd")]),
    ], []),
    ("rel", "religion", [
        par("Familien var aktive i frikirken og pinsemenigheten.", "Familien var aktive i frikyrkja og pinsemenigheita.", [el(R, "frikirken", "frikirke")], [el(R, "frikyrkja", "frikirke")]),
        par("Han konverterte til islam og ble muslim.", "Han konverterte til islam og vart muslim.", [el(R, "muslim")]),
        par("Mange av dem var lestadianere fra Nord-Norge.", "Mange av dei var lestadianarar frå Nord-Norge.", [el(R, "lestadianere", "lestadiansk")], [el(R, "lestadianarar", "lestadiansk")]),
        par("Hun er katolikk og går til messe hver søndag.", "Ho er katolikk og går til messe kvar sundag.", [el(R, "katolikk")]),
        par("De sluttet seg til Jehovas vitner i sytti-årene.", "Dei slutta seg til Jehovas vitne på sytti-talet.", [el(R, "jehovas vitner", "jehovas vitne")]),
        par("Han var ateist og meldte seg ut av trossamfunnet.", "Han var ateist og melde seg ut av trusamfunnet.", [el(R, "ateist"), el(R, "trossamfunnet", "trossamfunn")], [el(R, "ateist"), el(R, "trusamfunnet", "trusamfunn")]),
    ], []),
    ("pol", "politikk", [
        par("Han stemte på Arbeiderpartiet i alle år.", "Han stemde på Arbeiderpartiet i alle år.", [el(L, "Arbeiderpartiet")]),
        par("Hun var medlem av Senterpartiet og ledet lokallaget.", "Ho var medlem av Senterpartiet og leidde lokallaget.", [el(L, "Senterpartiet")]),
        par("Under krigen var han nazist og medlem av Nasjonal Samling.", "Under krigen var han nazist og medlem av Nasjonal Samling.", [el(L, "nazist"), el(L, "Nasjonal Samling")]),
        par("Han ble kjent som kommunist og aktivist.", "Han vart kjend som kommunist og aktivist.", [el(L, "kommunist"), el(L, "aktivist")]),
        par("De diskuterte politiske meninger og Fremskrittspartiet.", "Dei diskuterte politiske meiningar og Framstegspartiet.", [el(L, "Fremskrittspartiet")], [el(L, "Framstegspartiet", "Fremskrittspartiet")]),
        par("Hun gikk til valg for Kristelig Folkeparti.", "Ho gjekk til val for Kristeleg Folkeparti.", [el(L, "Kristelig Folkeparti")], [el(L, "Kristeleg Folkeparti", "Kristelig Folkeparti")]),
    ], []),
    ("kom", "kombinert", [
        par("Anders Fjellheim, født i 1938 på Bjølstad, var syk i flere år.", "Anders Fjellheim, fødd i 1938 på Bjølstad, var sjuk i fleire år.", [el(P, "Anders Fjellheim"), el(F, "1938"), el(S, "Bjølstad"), el(H, "syk")], [el(P, "Anders Fjellheim"), el(F, "1938"), el(S, "Bjølstad"), el(H, "sjuk")]),
        par("Eli Marit Vinstra ringte 68 05 45 67 den 3. november 1965 om rettssaken.", "Eli Marit Vinstra ringde 68 05 45 67 den 3. november 1965 om rettssaka.", [el(P, "Eli Marit Vinstra"), el(T, "68054567", "68 05 45 67"), el(D, "3. november 1965"), el(K, "rettssaken", "rettssak")], [el(P, "Eli Marit Vinstra"), el(T, "68054567", "68 05 45 67"), el(D, "3. november 1965"), el(K, "rettssaka", "rettssak")]),
        par("Halvor Brekkebu fra Otta gikk konkurs og stemte på Senterpartiet.", "Halvor Brekkebu frå Otta gjekk konkurs og stemde på Senterpartiet.", [el(P, "Halvor Brekkebu"), el(S, "Otta"), el(O, "konkurs"), el(L, "Senterpartiet")]),
        par("Sigrun Haugvold i Sør-Fron er katolikk og har diabetes.", "Sigrun Haugvold i Sør-Fron er katolikk og har diabetes.", [el(P, "Sigrun Haugvold"), el(S, "Sør-Fron", "Sørfron"), el(R, "katolikk"), el(H, "diabetes")]),
        par("Torbjørn Stuvstad, født i 1951, bor på Nordre Brenden og har gjeld.", "Torbjørn Stuvstad, fødd i 1951, bur på Nordre Brenden og har gjeld.", [el(P, "Torbjørn Stuvstad"), el(F, "1951"), el(S, "Nordre Brenden"), el(O, "gjeld")]),
        par("Ragnhild Dalsegg på Dovre ble anmeldt for vold i 1987.", "Ragnhild Dalsegg på Dovre vart melde for vald i 1987.", [el(P, "Ragnhild Dalsegg"), el(S, "Dovre"), el(K, "anmeldt", "anmeldte"), el(K, "vold")], [el(P, "Ragnhild Dalsegg"), el(S, "Dovre"), el(K, "vald")]),
    ], [0, 1, 2, 3, 4, 5]),
]


def main():
    ut = pathlib.Path("kalibrering") / f"KLAR-MANUS-0001_arkivklarering_justeringsmanus_v1.2_{DATO}.tsv"
    ut.parent.mkdir(exist_ok=True)
    rader = []
    for kode, klasse, sett, dialekt in MANUS:
        for i, (nb, nn, e_nb, e_nn) in enumerate(sett, 1):
            ja = "ja" if (i - 1) in dialekt else "nei"
            rader.append((f"{kode}{i:02d}nb", "nb", klasse, nb, e_nb, ja))
            rader.append((f"{kode}{i:02d}nn", "nn", klasse, nn, e_nn, ja))
    hode = ["# arkivklarering justeringsmanus KLAR-MANUS-0001 v1.2: radiolignende setninger per kategori, hver på bokmål og nynorsk.",
            "# STATUS: brukt til mønsterjustering (KLAR-EVAL-0008), IKKE til testing. Mønstrene og tersklene er justert mot dette manuset; testmaterialet for H4 er KLAR-MANUS-0002.",
            "# Personnavn er oppdiktede. Fødselsnumre har riktig format, fiktive sifre og bevisst ugyldig kontrollsiffer. Telefonnumre er fiktive og ligger i Nkoms serie for TV- og filmproduksjon, 68 05 00 00–68 05 99 99 (v1.2, AV-29: alle byttet dit), e-postadresser bruker reserverte eksempeldomener.",
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
