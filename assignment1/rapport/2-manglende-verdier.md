# Oppgave 2 – Håndtering av manglende verdier

> Norsk arbeidsversjon – den engelske teksten står i Overleaf-rapporten. Kode: `src/2_manglende_verdier.py`. Ca. 500 ord inkl. tabelltekst.

Av 98 101 rader mangler 9 448 minst én verdi. Vi undersøkte først hvorfor verdiene mangler, siden årsaken avgjør hvilken metode som passer. Tabell 5 oppsummerer stegene.

*Helt tomme rader.* I 5 622 rader mangler alle tre målingene. Radene inneholder bare land, vekst og år, så det finnes ingen verdi å imputere fra, og å fylle inn alle tre ville vært ren gjetning. Vi slettet dem.

*Sopp og trøfler.* Denne veksten sto for en tredjedel av de delvise hullene, fordi 44 av 70 land aldri rapporterer areal. Sopp dyrkes i hovedsak innendørs, så «høstet areal» og «avling per hektar» gir lite mening, og observert avling spenner fra 0,6 til 5 085 tonn/ha. En imputert verdi ville derfor vært tilnærmet tilfeldig, så vi fjernet veksten (745 rader, 0,8 %). Fjerningen tar også ut de tre største avlingene i datasettet (342 ganger Q3), men det er en følge av valget og ikke begrunnelsen. Outliers håndteres i oppgave 3.

*Ikke dyrket.* I 2 128 rader er verken areal eller produksjon større enn 0. Veksten ble altså ikke dyrket, og avlingen er udefinert (deling på null), ikke manglende. Avling satt til 0 ville sett ut som avlingssvikt, og tomme verdier ville skapt problemer for skalering og PCA. Vi slettet derfor radene.

*Skjulte manglende verdier.* 125 rader oppgir produksjon på 0 hektar, noe som er fysisk umulig. De fleste har svært liten produksjon (median 9 tonn), så arealet er trolig rundet ned til 0 eller ikke registrert. Vi behandlet nullen som en manglende verdi.

*Imputering eller sletting.* De resterende 1 127 radene (1,3 %) mangler avling og enten areal eller produksjon. Vi valgte å anslå avlingen, fordi den er uavhengig av landstørrelse, mens areal og produksjon varierer med flere tierpotenser mellom land. Den manglende målingen kan da regnes ut fra sammenhengen avling = produksjon × 10 000 / areal. Hvor godt anslaget blir, avhenger av om landet har egne data. I 256 rader har landet observert avling for samme vekst i andre år. Avlingen varierer lite innen et land over tid (variasjonskoeffisient 0,10), så vi imputerte med landets median. Vi brukte median fremfor gjennomsnitt fordi fordelingene er høyreskjeve: per vekst ligger gjennomsnittet typisk 21 % over medianen. I de øvrige 871 radene (1,0 %) har landet aldri rapportert avling for veksten i perioden. Da måtte anslaget kommet fra andre land, der avlingen varierer langt mer (variasjonskoeffisient 0,71), og arealet ville i praksis blitt diktet opp. Vi slettet derfor disse radene. Det fjerner 120 av 8 436 tidsserier, men ingen land eller vekster. Fordi manglende areal og produksjon regnes ut fra avlingen, oppfyller også de imputerte radene sammenhengen mellom målingene, og kolonnen `imputed` markerer dem. Medianene er beregnet før datasettet deles i trenings- og testsett (oppgave 5). Det gir en liten lekkasje, som vi aksepterer fordi rekkefølgen følger oppgaveteksten og bare 256 rader (0,3 %) er imputert.

Resultatet er 88 735 rader med 200 land og 117 vekster uten manglende verdier. Outliers er beholdt til oppgave 3.

**Tabell 5: Håndtering av manglende verdier, steg for steg.**

| Steg | Årsak | Tiltak | Rader berørt | Rader igjen |
|---|---|---|---|---|
| Utgangspunkt | – | – | – | 98 101 |
| Helt tomme rader | Ingen verdi å imputere fra | Slettet | 5 622 | 92 479 |
| Sopp og trøfler | Areal gir lite mening (innendørs) | Veksten fjernet | 745 | 91 734 |
| Ikke dyrket | Avlingen er udefinert | Slettet | 2 128 | 89 606 |
| Produksjon på 0 ha | Skjult manglende areal | Arealet satt til manglende | 125 | 89 606 |
| Hull uten landets egne data | Anslaget ville vært svært usikkert | Slettet | 871 | 88 735 |
| Hull med landets egne data | Avlingen er stabil innen land | Avling imputert med landets median, areal eller produksjon regnet ut | 256 | 88 735 |
