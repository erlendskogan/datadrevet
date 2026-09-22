# Sensorvurdering – Assignment 1 (IT3212), gruppe 50

Besvarelse: `Assignment1Datadrevet.pdf` (10 sider, oppgitt ordtelling 2984 av 3000).
Oppgavetekst: `oppgavetekst.pdf`.

Poengfordelingen i oppgaveteksten er 1 (10), 2 (20), 3 (20), 4 (30), 5 (10) og 6 bonus (10). Der en
begrunnelse blir bedt om og mangler, trekkes 10 poeng fra oppgaven.
Vurderingskriterier: (1) riktig bruk av teknikker, (2) klarhet og begrunnelse, (3) dokumentasjon og
lesbarhet, (4) fullstendighet og at instruksene er fulgt.

| Del | Maks | Vurdert | Status |
|---|---|---|---|
| Innledning | – (gir ikke poeng) | Sterk | ✅ Vurdert |
| 1 Data Exploration | 10 | 9 | ✅ Vurdert |
| 2 Data Cleaning | 20 | 18 | ✅ Vurdert |
| 3 Handling Outliers | 20 | 16 | ✅ Vurdert |
| 4 Data Transformation | 30 | 26 | ✅ Vurdert |
| 5 Data Splitting | 10 | 8 | ✅ Vurdert |
| 6 Bonus (PCA) | +10 | +9 | ✅ Vurdert |
| Formelle krav | – | 0 (risiko: ordgrensen) | ✅ Vurdert |
| **Totalt** | **90 (+10)** | **77 + 9 = 86** (−0 til −5 hvis ordgrensen regnes som brutt) | ✅ |

---

## Innledning

### Hva oppgaven ber om
Oppgaven har ingen egen innledningsdel. Den sier bare at gruppen selv velger ett eller flere datasett
fra Blackboard. Innledningen gir dermed ingen poeng direkte. Den teller likevel mot ordgrensen, og den
påvirker kriteriene *adherence to instructions* og *quality of documentation*. Den legger også
grunnlaget for alle valgene senere i besvarelsen.

### Hva gruppen har gjort
1. **Valg av datasett.** Gruppen vurderte 15 kandidatdatasett mot kravene i oppgavene: numeriske og
   kategoriske kolonner, reelle manglende verdier, realistiske outliers, håndterlig størrelse og
   selvforklarende kolonner. De valgte `crop1.csv` (FAOSTAT, avlingsstatistikk). `live1.csv` ble
   forkastet fordi det bare har én numerisk variabel med blandede enheter.
2. **Pivotering fra langt til bredt format.** `Value` blandet ha, tonn og hg/ha. Etter pivoteringen er
   hver rad én kombinasjon av land, vekst og år, med tre numeriske kolonner.
3. **Fjerning av 35 regioner og landgrupper**, blant dem «China», som er summen av fastlands-Kina,
   Taiwan, Hongkong og Macao. Begrunnelsen er dobbelttelling, og at summene ville dominert
   outlier-deteksjonen.
4. **Avgrensning til 2010–2020** i stedet for å velge ut noen få hovedvekster. Begrunnelsen er at
   hovedvekstene har nesten ingen manglende verdier, at alle 118 vekster og 200 land blir med til
   encodingen, og at det gir færre grenseendringer. Sudan-splittelsen i 2011 nevnes eksplisitt.
5. **Tabell 1** dokumenterer antall rader, land og vekster etter hvert steg og fastslår at ingen
   verdier er endret. Manglende verdier og outliers er bevisst latt stå til oppgave 2 og 3.

### Kontroll av påstandene (kjørt mot `food-bank/crop1.csv`)
| Påstand i rapporten | Resultat |
|---|---|
| 1,895,975 → 667,046 → 479,231 → 98,101 rader; 245 → 210 → 200 land; 118 vekster | ✅ Stemmer |
| `Value` blander ha, tonn og hg/ha | ✅ Stemmer (én enhet per `Element`) |
| `live1.csv` har én numerisk variabel med blandede enheter | ✅ Stemmer (`Stocks` i Head, 1000 Head og No) |
| Hvete 2019: verden 7.65·10⁸ t, største land 1.34·10⁸ t | ✅ Stemmer (fastlands-Kina 133.6 mill. t) |
| «China» er en sum (dobbelttelling) | ✅ Stemmer («China» 133,601,131 mot «China, mainland» 133,596,300) |
| Manglende produksjon for hvete 1.0 %, median over alle vekster 12.6 % | ✅ Stemmer |
| Manglende 15.1/11.0/16.0 % → 7.3/5.9/9.6 % | ✅ Stemmer |
| Ti land finnes bare før 2010 (USSR, Jugoslavia …) | ✅ Stemmer |
| «32 countries only appear later» | ⚠️ Upresist. 32 land dukker opp etter **1961**, men bare **2** etter 2010. Setningen kan leses som at 32 land kommer til etter 2010. |
| Sudan (former) 2010–2011, Sudan og South Sudan 2012–2020 | ✅ Stemmer |
| «keeps all 118 crops … for the encoding task» | ⚠️ Encodingen i 4a har 117 vekster, fordi soppen fjernes i oppgave 2 (`crop1_encoded.csv` har 117 `Item_`-kolonner) |

### Vurdering

**Styrker**
- Valget av datasett er begrunnet systematisk ut fra hva oppgavene faktisk krever, og det er
  forklart hvorfor alternativet ble forkastet. Dette er uvanlig grundig.
- Gruppen har fanget opp et reelt og lett oversett problem i datasettet, nemlig at aggregater og
  «China» gir dobbelttelling. Det er begrunnet med et konkret tall.
- Avgrensningen er begrunnet med tall, og alternativet (å velge ut hovedvekster) er vurdert og
  forkastet med en god grunn: det ville fjernet det meste av de manglende dataene som oppgave 2 skal
  håndtere.
- Arbeidet er åpent dokumentert. Tabell 1 gjør hvert steg etterprøvbart, og tallene i Tabell 1 stemmer.
- Skillet mellom å *tilpasse* datasettet og å *rense* det (oppgave 2 og 3) er tydelig og riktig.

**Svakheter og mulige merknader fra sensor**
1. **Ingen målvariabel eller modellformål.** Oppgaven handler om å klargjøre data «for modeling»,
   men innledningen sier ikke hva en modell skulle predikere. Det gjør det vanskeligere å vurdere om
   valgene i oppgave 3–5 (outliers, skalering, splitting) er riktige. README-en til gruppen sier selv
   at målvariabelen må bestemmes før oppgave 3. Vi må sjekke om den blir definert senere.
2. **Litt motstridende argumentasjon om manglende verdier.** Gruppen forkaster hovedvekstene fordi
   de *fjerner* manglende data, men framhever så at avgrensningen i tid *reduserer* andelen manglende
   verdier som en fordel. Begge deler kan forsvares (målet er realistiske, men håndterlige hull), men
   det burde vært sagt eksplisitt.
3. **80 % av radene fjernes før oppgave 1** (479k → 98k). Dette er transparent, men
   størrelsesargumentet er svakt, siden 480k rader ikke er et reelt problem. Den sterkeste
   begrunnelsen er stabile landgrenser og mer konsistent rapportering. En streng sensor kunne spurt om
   dette er seleksjon som burde vært drøftet under Data Cleaning.
4. **Den upresise setningen om «32 countries»** og **«118 crops … for the encoding task»** (encodingen
   har 117 vekster, se tabellen over). Dette er små presisjonsfeil.
5. **«Two properties … make it unsuitable»**: At `Value` blander enheter er strengt tatt ikke en feil
   i dataene. Det er langt format, og `Element` og `Unit` skiller enhetene. Å kalle det noe som ble
   «corrected» er litt overdrevet, men selve pivoteringen er riktig.
6. **Ordbruk.** Innledningen bruker rundt 380 ord, om lag 13 % av ordgrensen, på en del som ikke gir
   poeng. Oppgaven sier «no extra points for extra text». Nivået av detalj (Sudan, USSR) er
   interessant, men kunne vært kortet ned for å gi mer plass til begrunnelser i oppgaver som gir
   poeng. Vi må se om noe senere virker komprimert.
7. **Tidsserier.** Å beholde 11 år per land og vekst gir tidsserier. Det får betydning for
   splittingen (lekkasje) i oppgave 5. Innledningen nevner det ikke, men gruppen tar det opp i
   oppgave 5, så dette er bare et notat.

### Konklusjon
Innledningen gir mening, er faglig korrekt og er uvanlig godt begrunnet og dokumentert. Nesten
alle tallene vi kontrollerte stemmer (unntakene er «32 countries» og «118 crops»). Den gir ingen poeng og derfor heller ikke noe trekk. De viktigste
merknadene er at målvariabel og modellformål mangler, og at den bruker en stor del av ordgrensen.
Totalinntrykket er **meget sterkt**.

**Trekk: 0 (innledningen gir ikke poeng).** Punkt 1 og 6 tas med videre i vurderingen av oppgave 3–5
og av formelle krav.

---

## Oppgave 1 – Data Exploration (10 poeng)

### Hva oppgaven ber om
- **a.** Vis de første radene, oppsummerende statistikk og datatypen til hver kolonne.
- **b.** Finn manglende verdier, outliers og unike verdier i de kategoriske kolonnene.

Denne oppgaven ber ikke om begrunnelser, så regelen om 10 poengs trekk for manglende begrunnelse
gjelder ikke her.

### Hva gruppen har gjort
| Krav | Løsning i rapporten | Dekket |
|---|---|---|
| De første radene | Tabell 2 (fem rader) | ✅ |
| Oppsummerende statistikk | Tabell 4 (count, mean, std, min, kvartiler, max) + tekst om skjevhet | ✅ |
| Datatyper | Tabell 3, med begrunnelse for at `Year` behandles som numerisk | ✅ |
| Manglende verdier | Tabell 3 + Figur 1 (andel per kolonne), 5,622 helt tomme rader, ingen duplikater | ✅ |
| Outliers | Figur 2 (boksplott på log-skala), IQR-regelen brukt innenfor hver vekst, eksempler på ekstreme men reelle verdier, antall nuller | ✅ |
| Unike verdier i kategoriske kolonner | 200 land og 118 vekster, spredning i antall rader per kategori, 13 «nes»-kategorier | ✅ |

Gruppen går også litt lenger enn det som kreves, på en nyttig måte: skjevheten kvantifiseres
(gjennomsnittlig produksjon er over 50 ganger medianen), og funnene knyttes eksplisitt til senere oppgaver
(nuller til oppgave 3, antall kategorier til encodingen i oppgave 4). Pekeren om nullene er likevel
misvisende. Rapporten skriver «Their handling follows in Task 3», men nesten alle nullene fjernes i
oppgave 2 («ikke dyrket» og skjulte manglende verdier). I `crop1_clean.csv` er det 0 nuller igjen i
areal og bare 31 i produksjon og avling.

### Kontroll av påstandene (kjørt mot `food-bank/crop1_trimmed.csv`)
| Påstand | Resultat |
|---|---|
| 98,101 rader, 6 kolonner, datatyper som i Tabell 3 | ✅ |
| Manglende 7,172 / 5,758 / 9,448; 5,622 helt tomme rader; ingen duplikater | ✅ |
| Tabell 4 (mean, std, kvartiler, max) | ✅ |
| Gjennomsnittlig produksjon er over 50 ganger medianen (53.8×); std er større enn gjennomsnittet | ✅ |
| Maks produksjon er 5,360 ganger Q3 | ✅ |
| IQR innenfor hver vekst: 13–14 % (areal 13.2 %, produksjon 13.9 %) og 4.5 % (avling) | ✅ |
| India ris 45 mill. ha, Brasil sukkerrør 769 mill. t, nederlandsk sopp 5,085 t/ha | ✅ |
| Nuller: 2,179 / 2,132 / 30 | ✅ |
| Rader per kategori fra 11 (Faroe Islands, Tallowtree seed) til 1,298 **(China)** | ⚠️ Tallene stemmer (Marshall Islands har også 11 rader), men landet heter **«China, mainland»**. I innledningen står det at «China» er fjernet. |
| 13 «nes»-vekster med 12,944 rader | ✅ |

### Vurdering

**Styrker**
- Alle underpunktene i a og b er besvart, og alle tallene vi kontrollerte stemmer.
- Outliers undersøkes innenfor hver vekst. Det er faglig riktig, fordi sopp og hvete ikke har samme
  skala. Gruppen skiller også mellom *statistiske* outliers og *feil*, og argumenterer med konkrete
  eksempler for at de største verdiene er ekte.
- Tabellene er ryddige og kompakte, og mye informasjon formidles med få ord.

**Svakheter og mulige merknader fra sensor**
1. **«China» brukt om «China, mainland».** Dette er en intern selvmotsigelse, siden innledningen
   sier at «China» er fjernet. En oppmerksom sensor vil legge merke til det. Det er en liten feil,
   men den svekker inntrykket av presisjon.
2. **Figur 2 og teksten bruker forskjellig IQR-grunnlag.** Boksplottene bruker IQR på *alle*
   vekster samlet (da flagges ca. 16 % av areal og produksjon og 7 % av avlingene), mens teksten
   oppgir andeler med IQR *innenfor hver vekst*. Forskjellen blir ikke forklart, og leseren kan tro
   at figuren viser tallene i teksten. I tillegg beregnes kvartiler og værhår på rå skala, men vises
   på log-akse. Nedre værhår går derfor alltid ned til minimum, og bare høye outliers kan vises.
3. **Avling er avledet fra de andre kolonnene** (avling = produksjon × 10,000 / areal). Denne
   sammenhengen er et viktig funn fra utforskningen, men den nevnes først i oppgave 2. Den er
   avgjørende for outliers, skalering og PCA, og den ville passet naturlig her. Det gir ikke trekk,
   men det er en svakhet i strukturen.
4. **Formatering:** `Year` vises med tusenskille i Tabell 4 («2,015», «2,010»). Dette er kosmetisk.
5. **Figur 1 gjentar Tabell 3.** Den viser de samme tallene for manglende verdier og tar plass uten
   å tilføre noe nytt. Figurteksten teller også mot ordgrensen.
6. Det mangler oppsummerende statistikk for de kategoriske kolonnene, som mest vanlige verdi og
   frekvens. Dette dekkes delvis av teksten om rader per kategori, så det er akseptabelt.

### Konklusjon
Oppgaven er fullstendig og korrekt besvart, og analysen er bedre enn det som trengs for full
uttelling. Trekket er lite og skyldes presisjon og konsistens (China-navnet og at figur og tekst
bruker forskjellig IQR-grunnlag), ikke innhold.

**Poeng: 9 / 10** (spenn 9–10; en mild sensor gir 10).

---

## Oppgave 2 – Data Cleaning (20 poeng)

### Hva oppgaven ber om
- **a.** Håndter manglende verdier.
- **b.** Velg passende metoder, for eksempel imputering med gjennomsnitt eller median for numeriske
  data, imputering med modus for kategoriske data, eller sletting av rader eller kolonner.
- **c.** **Begrunn valgene.** Her gjelder regelen om 10 poengs trekk hvis begrunnelsen mangler.

### Hva gruppen har gjort
Gruppen bruker samme a/b/c-struktur som oppgaven. I **a** undersøkes *hvorfor* verdiene mangler, i
**b** beskrives tiltakene og i **c** begrunnes hvert tiltak. Tabell 5 oppsummerer det hele.

| Situasjon | Rader | Tiltak | Begrunnelse i rapporten |
|---|---|---|---|
| Helt tomme rader | 5,622 | Slettet | Ingen verdi å imputere fra, så imputering ville vært ren gjetting |
| Mushrooms and truffles | 745 | Hele veksten fjernet | Dyrkes innendørs, så areal og avling per hektar gir lite mening. 44 av 70 land rapporterer aldri areal, og avlingene spenner fra 0.6 til 5,085 t/ha |
| Ikke dyrket (verken areal eller produksjon > 0) | 2,128 | Slettet | Avling er udefinert (deling på null). Avling = 0 ville sett ut som avlingssvikt |
| Skjulte manglende verdier (produksjon på 0 ha) | 125 | Areal satt til manglende | Fysisk umulig. Medianproduksjonen er 9 t, så arealet er trolig rundet ned til 0 |
| Delvise hull uten egne landdata | 871 | Slettet | Et anslag måtte kommet fra andre land, der variasjonen er stor (CV 0.71) |
| Delvise hull med egne landdata | 256 | Avling imputert med medianen for samme land og vekst. Areal eller produksjon utledet fra identiteten | Avling er skalauavhengig og stabil innen et land (CV 0.10). Median er valgt fremfor gjennomsnitt fordi fordelingene er skjeve |

I tillegg:
- En `imputed`-kolonne markerer de imputerte radene.
- Lekkasjen fra imputering før splitting blir erkjent.
- Resultatet er 88,735 rader, 200 land og 117 vekster, uten manglende verdier.

### Kontroll av påstandene (kjørt mot `crop1_trimmed.csv` og `crop1_clean.csv`)
| Påstand | Resultat |
|---|---|
| 9,448 rader med minst én manglende verdi, 5,622 helt tomme | ✅ |
| Sopp: 745 rader, 44 av 70 land rapporterer aldri areal, en tredjedel av de delvise hullene (571 av 1,698 = 34 %) | ⚠️ Tallene stemmer, men rapporten oppgir ikke nevneren. Med rapportens egne definisjoner er soppen 558 av 1,685 delvise hull før fjerningen (33 %; 13 av de 571 soppradene med manglende verdier er «ikke dyrket»). Det er en annen mengde enn de 1,127 som senere kalles «partial gaps» |
| 2,128 «ikke dyrket», 125 skjulte manglende verdier (medianproduksjon 9 t) | ✅ |
| 1,127 delvise hull, fordelt på 256 imputerte og 871 slettede | ✅ |
| CV for avling er 0.10 innen land og 0.71 mellom land; gjennomsnittet ligger 21 % over medianen | ✅ (medianverdier) |
| 120 av 8,436 tidsserier fjernet | ✅ (8,436 − 120 = 8,316 serier igjen) |
| 88,735 rader, 200 land, 117 vekster, 256 imputerte | ✅ |
| Identiteten avling = produksjon × 10,000 / areal gjelder i alle rader etterpå | ✅ (kontrolleres med `assert` i koden) |

### Vurdering

**Styrker**
- **Metoden er faglig riktig.** Gruppen undersøker *årsaken* til hver type manglende verdi før de
  velger tiltak, i stedet for å bruke én metode på alle hullene. Dette er nettopp det
  vurderingskriteriet «justification of decisions» belønner.
- **Hvert valg har en egen begrunnelse**, og begrunnelsene er underbygget med tall (CV 0.10 mot 0.71,
  gjennomsnitt 21 % over medianen). Det er ingen fare for 10 poengs trekk.
- Imputering med medianen for samme land og vekst er bedre enn den enkle løsningen oppgaven foreslår
  (medianen for hele kolonnen). Å utlede areal eller produksjon fra identiteten holder dataene
  internt konsistente.
- «Skjulte manglende verdier» (0 ha med produksjon) viser et kritisk blikk på dataene. Mange grupper
  ville ikke fanget opp dette.
- `imputed`-kolonnen og erkjennelsen av lekkasje gir god sporbarhet og faglig ærlighet.
- Tabell 5 gjør hele prosessen lett å følge.

**Svakheter og mulige merknader fra sensor**
1. **De fem situasjonene er ikke en oppdeling av de 9,448 radene, og det blir ikke forklart.**
   Summen blir 9,747. Dette skyldes to ting. Sopp-tallet (745) omfatter også 174 komplette rader, og
   de 125 skjulte verdiene telles to ganger. De mangler allerede avling (areal = 0 gir ingen avling)
   og er derfor blant de 9,448, men de telles både som «hidden» og inne i de 1,127 delvise hullene
   (9,747 − 174 − 125 = 9,448). I tillegg brukes «partial gaps» om to ulike mengder: «a third of the
   partial gaps» gjelder de delvise hullene *før* soppen fjernes (558 av 1,685), mens
   «Partial gaps» senere er 1,127 rader. Teksten åpner med «9,448 lack at least one value … We found five situations», så leseren
   forventer at tallene summerer. En sensor som prøver å avstemme dem, blir forvirret.
2. **Rapporten sier ikke hva som til slutt skjer med de 125 skjulte manglende verdiene.** Tabell 5
   sier bare «Area set to missing». Vår kontroll viser at 64 av dem blir imputert og 61 slettet
   (de blir en del av de delvise hullene), men dette kommer ikke fram.
3. **Interpolasjon i tid er ikke vurdert.** Dataene er tidsserier med 11 år per land og vekst, og
   lineær interpolasjon mellom nabo-år er det åpenbare alternativet til medianen for landet. Når
   gruppen selv skriver at avlingen er stabil over tid, burde interpolasjon vært nevnt og avvist
   eller valgt. Dette er ikke et krav, men en sensor kan savne det.
4. **Begrunnelsen for å godta lekkasjen er svak.** «The order follows the assignment» er ikke et
   faglig argument. Medianene kunne ha vært beregnet på treningsdataene alene. Lekkasjen er liten
   (0.3 %) og ærlig erkjent, så dette er en liten merknad.
5. **Mye slettes** (9,366 rader, 9.5 %, og en hel vekst). Hver sletting er begrunnet, men det mangler
   en samlet vurdering av om slettingene kan skjevfordele dataene, for eksempel om små land eller
   fattige land oftere mangler egne data og derfor blir slettet.
6. Argumentet «keeping empty values would cause problems for scaling and PCA» for «ikke dyrket»-radene
   er tynt. Det sier bare at manglende verdier er et problem. Det sterke argumentet er det første,
   at avlingen er udefinert, og det holder alene.

### Konklusjon
Dette er en meget god besvarelse. Metodene er riktige og begrunnet grundig med tall, og den går
lenger enn oppgaven krever. Det er ingen risiko for 10 poengs trekk. Trekket skyldes klarhet
(tallene lar seg ikke avstemme, og det er uklart hva som skjer med de skjulte verdiene) og at
interpolasjon i tid ikke er vurdert, ikke feil i selve metoden.

**Poeng: 18 / 20** (spenn 17–19).

*Notat til senere:* Oppgave 3 skriver «31 of 8,436 time series», men etter oppgave 2 er det 8,316
serier igjen (8,436 er tallet *før* slettingen). Oppgave 5 bruker riktig tall (8,316).

---

## Oppgave 3 – Handling Outliers (20 poeng)

### Hva oppgaven ber om
- **a.** Finn outliers med metoder som IQR eller z-score.
- **b.** Velg om outlierne skal fjernes, cappes eller transformeres, og **begrunn valget**. Her gjelder
  regelen om 10 poengs trekk hvis begrunnelsen mangler.

### Hva gruppen har gjort
- **a.** Outliers finnes *per vekst* (ellers ville sukkerrør blitt sammenlignet med vanilje).
  Tre metoder sammenlignes (Tabell 6):

  | Metode | Areal | Produksjon | Avling |
  |---|---|---|---|
  | IQR, rå skala | 13.1 % | 13.9 % | 4.5 % |
  | IQR på log10(x+1) | 1.3 % | 1.3 % | 2.9 % |
  | z-score, rå skala | 2.2 % | 2.1 % | 1.5 % |

  z-score forkastes fordi den forutsetter en symmetrisk fordeling. At log-transformasjonen alene
  fjerner det meste av det rå IQR flagger, brukes som bevis på at flaggingen skyldes skjevhet og ikke
  feil i dataene.
- **b.** Valget er en kombinasjon av **transformasjon og capping**:
  - Alle tre målingene transformeres med log10(x+1). Varianten med +1 velges fordi 31 rader har
    produksjon = avling = 0 (avlingssvikt), som gruppen vil beholde som ekte hendelser.
  - Gjenværende outliers (1.3–2.9 %) **cappes (winsoriseres) til 1.5×IQR-grensen per vekst**
    på log-skala. 3,986 rader får minst én cappet verdi.
  - Ingen rader slettes. Kolonnene `*_capped` markerer de cappede verdiene, og de opprinnelige
    kolonnene beholdes.
  - Figur 3 viser boksplott før og etter cappingen.

### Kontroll (kjørt `src/3_outliers.py` og egne sjekker)
| Påstand | Resultat |
|---|---|
| Tabell 6 (alle ni prosentene) | ✅ |
| «the same figures already reported in Task 1b» | ⚠️ Nesten. Oppgave 1b er regnet på `crop1_trimmed` (før rensingen) og oppgave 3 på de 88,735 rensede radene (areal 13.2 % mot 13.1 %) |
| Høyeste avling er nå nederlandske agurker, 743 t/ha | ✅ |
| 31 rader med produksjon = avling = 0, der areal alltid er > 0 | ✅ |
| 3,986 av 88,735 rader har minst én cappet verdi; ingen rader, land eller vekster endret | ✅ |
| «a small, unsystematic gap in **31 of 8,436** time series» | ❌ De 31 radene fordeler seg på **17** serier, og etter oppgave 2 finnes det **8,316** serier, ikke 8,436 |
| **Hvilken side som cappes** (sjekket av oss, ikke nevnt i rapporten) | ⚠️ **Rundt 75 % av de cappede verdiene ligger i den *nedre* halen og blir *hevet*.** Areal: 870 av 1,160. Produksjon: 898 av 1,132. Avling: 1,937 av 2,575 |
| **De 31 radene med avlingssvikt** (sjekket av oss) | ❌ **Avlingen i alle 31 radene cappes opp** fra 0 (for eksempel til omtrent 1,329 hg/ha for lin), og produksjonen cappes opp i 18 av dem. Dette er nettopp de verdiene gruppen argumenterer for å beholde som «genuine crop failure» |
| Identiteten avling = produksjon × 10,000 / areal etter capping (sjekket av oss) | ⚠️ Brytes med mer enn 0.1 på log-skala i 2,578 av 3,986 cappede rader. Dette nevnes først i oppgave 6. Også 205 rader uten capping avviker med mer enn 0.1, på grunn av log10(x+1), slik rapporten selv forklarer i oppgave 6 |

### Vurdering

**Styrker**
- Det er riktig å finne outliers per vekst, og det er godt forklart.
- Sammenligningen av tre metoder, og særlig bruken av IQR på log-skala som *diagnose*, er et elegant
  argument for at det meste som flagges er skjevhet og ikke feil. Dette er den sterkeste delen av
  oppgaven.
- z-score forkastes med riktig faglig grunn (den forutsetter symmetri).
- Valget av log10(x+1) fremfor log10(x) er begrunnet konkret, med de 31 nullene.
- Ingen rader slettes, flaggkolonner legges til og originalkolonnene beholdes. Det gir god
  sporbarhet.
- Det finnes en begrunnelse for både a og b, så det blir ikke 10 poengs trekk.

**Svakheter og mulige merknader fra sensor**
1. **Begrunnelsen for cappingen er ufullstendig** (synlig for sensor i teksten). Gruppen skriver at
   de gjenværende outlierne «are more likely to be genuinely extreme, since the transform has already
   corrected the skew». Det betyr at de er ekte *statistiske* outliers, ikke at de er feil. Teksten
   forklarer likevel ikke hvorfor slike verdier skal cappes og ikke beholdes, for eksempel for å gjøre
   modellen robust. Det står også i kontrast til 1b og 3a, der de ekstreme verdiene omtales som ekte
   variasjon. Dette er den svakeste begrunnelsen i besvarelsen så langt.
2. **Cappingen hever hovedsakelig *små* verdier** (synlig i praksis, ikke i teksten). På log-skala
   blir den nedre halen lang: 5 ha gir log ≈ 0.8, mens medianen ligger rundt 3.5. Derfor ligger rundt
   75 % av de cappede verdiene i den nedre halen og blir *hevet*. Omtrent halvparten av dem er lave
   avlinger (1,937), og resten er små arealer eller små produksjonsvolum (870 + 898), altså små land og
   små produsenter. Dette er ekte data som endres, og det står i direkte kontrast til argumentet om at outliers er «genuine
   variation in country size» (oppgave 1b). Gruppen drøfter aldri nedre og øvre grense hver for seg.
3. **Argumentet om nullene blir undergravd.** Gruppen begrunner log10(x+1) med at avlingssvikt er en
   ekte hendelse som skal beholdes, men cappingen løfter avlingen i alle 31 radene opp fra 0.
   Sensor ser ikke dette direkte, men det gjør begrunnelsen i b internt inkonsistent.
4. **Cappingen bryter identiteten mellom avling, produksjon og areal**, fordi hver kolonne cappes for
   seg. Gruppen var nøye med å bevare identiteten i oppgave 2, men nevner ikke bruddet her (bare
   i forbifarten i oppgave 6). Det burde vært drøftet som en ulempe ved å cappe hver kolonne for seg.
5. **Grensene er beregnet på alle dataene før splittingen.** Kvartilene per vekst hentes fra hele
   datasettet. Det er samme type lekkasje som gruppen erkjente for medianimputeringen i oppgave 2,
   men her nevnes den ikke. Det er en inkonsistens.
6. **Feil tall:** «31 of 8,436 time series» skal være 17 av 8,316.
7. **Figur 3:**
   - Den er ikke henvist til i teksten.
   - Aksene har norske etiketter («før» og «etter») i en engelsk rapport.
   - Boksplottene er laget på alle vekster samlet, mens cappingen gjøres per vekst. Før og etter ser
     derfor nesten like ut for areal og produksjon, og det finnes fortsatt punkter utenfor
     whiskerne etter cappingen. Figuren underbygger dermed ikke påstanden, og den kan forvirre.
8. Terskelen for z-score (|z| > 3) står ikke i rapporten.
9. Mindre punkt: Transformasjonen gjøres her og ikke i oppgave 4. Det er greit, siden oppgaven
   nevner «transform» som et alternativ, men det flytter noe av skaleringslogikken hit.

### Konklusjon
Delen om *deteksjon* er meget sterk, og ideen om å bruke IQR på log-skala som diagnose er bedre enn
det som forventes. Delen om *håndtering* har en reell svakhet. Cappingen etter transformasjonen er
dårlig begrunnet (det står ikke hvorfor ekte outliers skal cappes), den rammer mest små, ekte verdier i den
nedre halen, og den motsier gruppens eget argument om nullene. Det kommer også feil tall, en
lekkasje som ikke nevnes, og en figur som verken er henvist til eller på riktig språk. Det blir ikke
10 poengs trekk, siden begrunnelsen finnes, men kvaliteten på den trekker ned.

**Poeng: 16 / 20** (spenn 14–17; en sensor som bare leser teksten, legger mest vekt på punkt 1, 6 og 7).

**Forslag til forbedring:** Behold bare log-transformasjonen, eller capp kun den øvre halen, og
begrunn capping med robusthet og ikke med at verdiene er feil. Henvis til Figur 3, bytt til
engelske etiketter, og rett 31 av 8,436 til 17 av 8,316.

---

## Oppgave 4 – Data Transformation (30 poeng)

### Hva oppgaven ber om
- **a. Encoding:**
  - i. Bruk label encoding eller one-hot encoding.
  - ii. **Begrunn valget.** Her gjelder regelen om 10 poengs trekk.
- **b. Feature scaling:**
  - i. Bruk min-max eller standardisering.
  - ii. **Forklar hvorfor skalering er nødvendig og hvordan det påvirker modellen.**

### Hva gruppen har gjort
**4a – Encoding**
- `Area` (200) og `Item` (117) one-hot-encodes, noe som gir 317 nye binære kolonner. `Year` er
  numerisk, og `imputed` og `*_capped` er flagg, så ingen av dem encodes.
- Begrunnelse:
  - Begge kolonnene er nominelle og har ingen naturlig rekkefølge.
  - Label encoding ville gitt en falsk rekkefølge og falske avstander (Albania = 1 ligger
    «nærmere» Algeria = 2 enn Brazil = 20).
  - Label encoding ville vært spesielt skadelig for PCA i oppgave 6, siden PCA leser varians og
    kovarians direkte.
- Antall kolonner drøftes også: 88,735 rader mot 317 kolonner er et greit forhold, og kolonnene kan
  lagres som en sparse matrise. Problemet ville vært størst for k-NN, men «downstream use is
  regression and PCA».

**4b – Skalering**
- Standardisering av de tre log-transformerte og cappede målingene.
- Hvorfor skalering er nødvendig: Målingene har fortsatt ulike spenn etter log-transformasjonen,
  og modeller basert på avstand eller gradienter er følsomme for det.
- Standardisering er valgt fremfor min-max fordi fordelingene er mer symmetriske etter oppgave 3,
  og fordi min-max ville vært styrt av de to endepunktene i hver kolonne.
- **Skaleringen tilpasses bare på treningssettet** og brukes deretter på testsettet, for å unngå
  lekkasje. Som kontroll oppgis at testsettet ikke får nøyaktig 0/1 (−0.005/0.990 for areal).
- One-hot-kolonnene, `Year` og flaggene skaleres ikke.
- Tabell 7 og 8 viser gjennomsnitt og standardavvik fra treningssettet.

### Kontroll (kjørt `4_encoding.py`, `5_data_splitting.py` og `4b_scaling.py`)
| Påstand | Resultat |
|---|---|
| 317 nye kolonner, 328 kolonner totalt | ✅ |
| Skaleringsparametrene (3.567/1.246, 4.283/1.310, 4.722/0.585) | ✅ |
| Testsettet etter skalering: −0.005/0.990 for areal | ✅ |
| Spenn på log-skala «roughly 0–7 for area, 0–9 for production, 0–7 for yield» | ⚠️ Faktisk er det 0.03–7.65 for areal, 0–8.89 for produksjon og **2.59–6.71 for avling**. Avlingen spenner altså ikke fra 0 etter cappingen |
| Tabell 7 og Tabell 8 | ❌ **Identiske tabeller**, med samme innhold og samme bildetekst. Teksten henviser bare til Tabell 8 |
| Starten av 4a | ❌ Det står **«textbfa.»** i stedet for fet **a.** (LaTeX-feil) |

### Vurdering

**Styrker**
- **Begrunnelsen for encodingen er meget god.** Den tar for seg nominell og ordinal skala, gir et
  konkret eksempel på falsk avstand med label encoding og knytter valget til PCA senere i
  oppgaven. Det er ingen fare for 10 poengs trekk.
- Gruppen tar selv opp motargumentet om mange kolonner, og drøfter når det faktisk ville vært et
  problem (k-NN).
- **Skaleringen er faglig riktig gjennomført.** Den tilpasses bare på treningssettet, og det er
  forklart hvorfor. Mange grupper gjør dette feil, så det er et klart plusspoeng. Én detalj i
  forklaringen er likevel feil. Rapporten sier at med en egen scaler per sett ville «the test set's
  distribution … have influenced how the training data is represented». Men treningsdataene
  skaleres på samme måte i begge tilfeller. Problemet er at testsettet da skaleres med sine egne
  parametere, slik at informasjon fra testsettet brukes og de to settene får ulik skala.
- Valget av standardisering fremfor min-max er begrunnet og knyttet til valgene i oppgave 3.
  Argumentet holder: i praksis er min og maks for hele kolonnen uendret etter cappingen for areal
  (0.03–7.65) og produksjon (0–8.89). For avling endres spennet (0–6.87 → 2.59–6.71). Min-max
  ville uansett vært styrt av de gjenværende endepunktene.
- Det er riktig og begrunnet å ikke skalere binære kolonner.

**Svakheter og mulige merknader fra sensor**
1. **Tabell 7 og 8 er duplikater, og det står «textbfa.»** Dette er tydelige tegn på manglende
   korrektur, som går direkte på kriteriet *quality of documentation and readability*. Det er lett
   å se, og en sensor vil nesten sikkert kommentere det.
2. **`Year` skaleres ikke, og begrunnelsen er feil.** Teksten kaller `Year` «discrete codes», men i
   oppgave 1 ble `Year` eksplisitt behandlet som *numerisk* («ordered and equally spaced»). `Year`
   har verdier rundt 2015, som er i en helt annen størrelsesorden enn de standardiserte kolonnene.
   Etter gruppens eget argument (gradientbaserte modeller er følsomme for skala) burde `Year`
   derfor vært skalert. Dette er en intern inkonsistens.
3. **Feil tall for spennene.** Avlingen spenner fra 2.6 til 6.7, ikke fra 0 til 7, og areal går
   opp til 7.65, ikke 7. Spennene er
   dessuten ganske like (alle ligger innenfor 0–9). Det sterkere argumentet ville vært at
   standardavvikene er ulike (1.25, 1.31 og 0.59), men det brukes ikke. Argumentet for skalering
   blir dermed svakere enn det kunne vært.
4. **Forklaringen av hvordan skalering påvirker modellen er tynn.** Oppgaven ber eksplisitt om
   «how it impacts the model». Gruppen sier bare at modeller basert på avstand eller gradienter er
   følsomme for skala. Konkrete virkninger mangler, for eksempel raskere konvergens ved gradient
   descent, like vilkår for regularisering (L1/L2), at variabler med stor skala dominerer
   avstanden i k-NN, k-means og PCA, og at trebaserte modeller ikke påvirkes. Svaret er ikke fraværende,
   så det gir ikke 10 poengs trekk, men det er for kort.
5. **Modellformålet dukker opp her for første gang, uten å være definert.** «Our downstream use is
   regression and PCA» er første gang *regresjon* nevnes. Det står aldri hva som skal predikeres
   (se merknad 1 om innledningen). Med lineær regresjon gir full one-hot for to kategoriske kolonner
   i tillegg **perfekt multikollinearitet** (dummy-fellen), som løses ved å droppe én dummykolonne
   per kategorisk variabel (én for `Area` og én for `Item`). Dette nevnes ikke, selv om gruppen selv trekker fram regresjon.
6. **Påstanden om at det er få kolonner er litt lettvint.** I oppgave 1 skrev gruppen at «the high
   number of categories affects the choice of encoding in Task 4». Her avvises problemet raskt, og
   alternativer som target encoding, frequency encoding eller gruppering av sjeldne kategorier
   drøftes ikke.
7. **Kontrollargumentet er svakt.** At testsettet ikke får nøyaktig 0/1 er forventet, men det
   *beviser* ikke at prosedyren er riktig. Det er bare konsistent med at den er det.
8. **Ordbruk.** 4a er lang (rundt 380 ord bare for encoding) med mye gjentakelse av poenget om falsk
   rekkefølge. Den dupliserte Tabell 8 med bildetekst koster også ord. Ord som kunne gått til
   merknad 4 er brukt på gjentakelse.
9. Små ting: typografiske anførselstegn er feil (”more” i stedet for “more”), og
   kodekommentaren i `4b_scaling.py` omtaler fortsatt «heltallskoder fra oppgave 4a», som er igjen
   fra label encoding. Kodekommentaren er ikke synlig i rapporten.
10. **Det ferdige datasettet har tre versjoner av hver måling.** `crop1_train_scaled.csv` inneholder
    råkolonnene (uskalert, opptil 7.7·10⁸), `*_log10` (uskalert) og `*_scaled`. Listen over kolonner
    som ikke skaleres, nevner ikke råkolonnene, og rapporten sier aldri hvilke kolonner som er
    features. Dette henger sammen med at modellformålet mangler (se innledningen, merknad 1).
11. **«Standard tooling represents one-hot columns as a sparse matrix»** stemmer generelt, men er
    ikke det gruppen gjorde. Koden bruker `pd.get_dummies(dtype=int)`, som er tett, og skriver til CSV.

### Konklusjon
4a er sterk og fullt ut begrunnet. 4b er faglig riktig gjennomført (skaleringen tilpasses bare på
treningssettet), men forklaringen av hvordan skalering påvirker modellen er tynn, spennene er feil og
begrunnelsen for `Year` motsier oppgave 1. Den synlige mangelen på korrektur (duplisert tabell og
«textbfa.») trekker ned på dokumentasjonskvaliteten. Ingen begrunnelser mangler helt, så det blir
ikke 10 poengs trekk.

**Poeng: 26 / 30** (spenn 24–27). Oppgaveteksten sier ikke hvordan de 30 poengene fordeles mellom
a og b. Hvis vi antar 15/15, blir fordelingen omtrent 14/15 på a og 12/15 på b.

**Forslag til forbedring:**
- Slett Tabell 7 eller 8, og rett «textbfa.».
- Skaler `Year`, eller begrunn hvorfor ikke uten å kalle det «discrete codes».
- Bruk standardavvikene som argument for skalering, og rett spennene.
- Legg til 2–3 setninger om konkrete virkninger på modellen.
- Nevn dummy-fellen, og kort ned gjentakelsene i 4a.

---

## Oppgave 5 – Data Splitting (10 poeng)

### Hva oppgaven ber om
- **a.** Del det ferdig preprosesserte datasettet i trenings- og testsett, typisk 80-20 eller 70-30.
- **b.** **Forklar hvorfor splitting er viktig og hvordan det forhindrer overtilpasning (overfitting).**

### Hva gruppen har gjort
- **a.**
  - Tilfeldig 80-20-splitt, begrunnet med at datasettet er stort (88,735 rader), så begge settene
    blir store nok.
  - Gruppen påpeker selv at dataene består av 8,316 tidsserier (land × vekst) med stabil avling
    (CV 0.10). En tilfeldig splitt legger dermed nesten like rader i både trenings- og testsettet,
    noe som gir et for optimistisk anslag og forsterker lekkasjen fra imputeringen i oppgave 2.
  - En grupperingssplitt (hver serie i ett sett) vurderes, men forkastes fordi noen land og vekster
    bare har én serie og da ikke ville finnes i treningssettet.
  - Gruppen velger tilfeldig splitt og oppgir lekkasjen som en begrensning.
- **b.**
  - En modell må evalueres på rader den ikke har sett, ellers måler man bare hvor godt den har
    pugget treningsdataene.
  - Et stort gap mellom treningsresultat og testresultat er et tegn på overfitting.
  - Forholdet 80-20 balanserer nok treningsdata mot et stabilt anslag på testsettet.

### Kontroll
| Påstand | Resultat |
|---|---|
| 88,735 rader, delt i 70,988 / 17,747 (80/20) | ✅ |
| 8,316 tidsserier, som typisk spenner over 11 år | ✅ (93 % har 11 år, median 11) |
| «some countries and crops occur in only one series» | ✅, men det gjelder bare **3 land** (Macao, Faroe Islands, Marshall Islands) og **1 vekst** (Tallowtree seed) |
| Alle kategorier finnes i både trenings- og testsettet med tilfeldig splitt | ✅ (0 mangler) |
| Seed (`random_state=42`) | Brukt i koden, men ikke oppgitt i rapporten |

### Vurdering

**Styrker**
- Splitten er gjennomført riktig, og forholdet er begrunnet.
- **Drøftingen av tidsseriene er uvanlig god.** Gruppen ser selv at en tilfeldig splitt lekker
  informasjon mellom rader i samme serie, knytter det til imputeringen i oppgave 2, vurderer en
  grupperingssplitt og er ærlig om begrensningen. Dette er langt over det forventede nivået.
- I 5b skilles det riktig mellom å *oppdage* overfitting (gap mellom trening og test) og å
  bare måle hvor godt modellen har pugget.

**Svakheter og mulige merknader fra sensor**
1. **Begrunnelsen for å forkaste grupperingssplitten er svak.** Den gjelder bare 3 land og
   1 vekst. De fire seriene kunne enkelt vært lagt i treningssettet (en tvungen gruppesplitt), og da
   ville lekkasjen vært løst. Gruppen erkjenner et reelt problem, men velger den løsningen som har
   problemet, med et argument som veier lite. En sensor vil sannsynligvis påpeke dette.
   Argumentet er dessuten teknisk feil. Rapporten sier at kategorien da blir «unseen for the
   encoding in Task 4», men encodingen gjøres på hele datasettet *før* splittingen
   (`4_encoding.py` kjøres før `5_data_splitting.py`). Encodingen kan derfor ikke mangle en
   kategori. Problemet ville vært at *modellen* aldri har sett kategorien under trening.
2. **Tidsbasert splitt er ikke vurdert.** Dataene er tidsserier, og det naturlige alternativet er å
   trene på 2010–2018 og teste på 2019–2020. Det gir tilfeldigvis **82/18**, altså nesten nøyaktig
   80-20, beholder alle land og vekster i treningssettet og speiler hvordan en modell faktisk brukes
   (å predikere fremtiden). Den løser likevel ikke lekkasjen gruppen peker på: 7,985 av 8,316 serier
   har rader i begge periodene, og imputeringsmedianene bruker også 2019–2020. Det er bare en
   gruppesplitt (merknad 1) som fjerner begge. Dette er det største faglige hullet i oppgaven.
3. **«Hvordan splitting forhindrer overfitting» er bare delvis besvart.** Gruppen forklarer at
   splitting *oppdager* overfitting, men ikke hvordan det *forhindrer* den. Svaret er at et eget
   valideringssett (eller kryssvalidering på treningsdataene) brukes til å velge modell,
   kompleksitet, regularisering og tidlig stopp, mens testsettet bare brukes én gang til slutt.
   Valideringssett (til forskjell fra testsettet) og kryssvalidering nevnes ikke. Svaret finnes, så det blir ikke 10 poengs
   trekk, men det er ufullstendig.
4. **Begrunnelsen for 80-20 fremfor 70-30 er generisk.** «Stort datasett» og «balanse» er riktig,
   men gruppen tallfester ikke, for eksempel ved å si at 17,747 testrader gir et presist anslag.
   Dette er en mindre merknad.
5. **Seed og reproduserbarhet** (`random_state=42`) står ikke i rapporten. Det er en liten merknad.
6. **Rekkefølgen i pipelinen** (imputering og capping før splitting, skalering etter) er bare
   delvis synlig. Lekkasjen fra cappingen i oppgave 3 nevnes ikke her heller (se oppgave 3,
   merknad 5).

### Konklusjon
Oppgave 5 er korrekt gjennomført, og drøftingen av tidsserier og lekkasje er sterkere enn forventet.
Men når gruppen først har identifisert problemet, blir det mer synlig at løsningen (en tvungen
gruppesplitt) avvises på svakt grunnlag, og at en tidsbasert splitt ikke vurderes. Forklaringen av hvordan
splitting *forhindrer* overfitting er også ufullstendig.

**Poeng: 8 / 10** (spenn 7–9).

**Forslag til forbedring:** Bruk en gruppesplitt der de 4 enkeltseriene tvinges inn i
treningssettet, som fjerner lekkasjen mellom rader i samme serie. Alternativt kan en tidsbasert splitt
(2010–2018 mot 2019–2020, som gir 82/18) gi et realistisk prognoseoppsett, men den fjerner ikke
lekkasjen. Legg til én til to
setninger om valideringssett og kryssvalidering som mekanismen som forhindrer overfitting.

---

## Oppgave 6 – Bonus: PCA (10 poeng, valgfri)

### Hva oppgaven ber om
Bruk en metode for dimensjonsreduksjon, som PCA, og **drøft hvordan den påvirker datasettet**.
Oppgaven ber ikke eksplisitt om begrunnelser, men sier «discuss».

### Hva gruppen har gjort
- **Metode:**
  - PCA er valgt fremfor LDA fordi datasettet ikke har klasser.
  - PCA kjøres på de log-transformerte og standardiserte målingene. Da blir identiteten
    avling = produksjon × 10,000 / areal tilnærmet lineær (log avling ≈ log produksjon − log areal + 4),
    noe som passer til at PCA er en lineær metode.
  - `Year` og one-hot-kolonnene er ikke med i hovedkjøringen.
  - PCA tilpasses bare på treningssettet, akkurat som skaleringen.
- **Resultater (Tabell 9 og Figur 4):**
  - Korrelasjonen mellom areal og produksjon er r = 0.89.
  - PC1 og PC2 forklarer til sammen 99.95 % av variansen. To komponenter beholdes, både etter
    terskelen på 95 % og etter Kaisers kriterium (egenverdi > 1).
  - PC1 måler omfanget av dyrkingen (areal og produksjon), PC2 måler produktivitet (avling), og
    PC3 er selve identiteten mellom målingene (nesten ingen varians).
- **One-hot-kolonnene:** Gruppen tester å ta med de 317 kolonnene. Da trengs 213 av 320 komponenter
  for å nå 95 %, fordi hver kolonne har liten varians (0.006) og kolonnene utelukker hverandre.
  PC1 og PC2 endres nesten ikke. Konklusjonen er å kjøre PCA bare på målingene.
- **Effekt på datasettet:**
  - Datasettet går fra 3 til 2 kolonner som er ukorrelerte.
  - Rekonstruksjonsfeilen er 0.05 % på treningssettet og 0.06 % på testsettet.
  - Sammenligning: å bare droppe avling (R² = 0.98) koster 0.5–0.6 %, men gir kolonner som er lettere
    å tolke.
  - Konklusjon: PCA avslører én overflødig måling, men med bare tre målinger koster komponentene
    mer i tolkbarhet enn de sparer.

### Kontroll (kjørt `src/6_pca.py`)
| Påstand | Resultat |
|---|---|
| r(areal, produksjon) = 0.89 | ✅ (0.894) |
| Egenverdiene 1.914 / 1.085 / 0.001, forklart varians 63.79 / 36.16 / 0.05 %, egenvektorene i Tabell 9 | ✅ |
| 213 av 320 komponenter med one-hot; 99.8 % og 99.2 % av vekten ligger på målingene | ✅ |
| Rekonstruksjonsfeil 0.05 % (trening) og 0.06 % (test) | ✅ |
| R² = 0.98 når avling predikeres fra areal og produksjon; å droppe avling koster 0.5–0.6 % | ✅ (0.986 / 0.982) |
| Komponentene er ukorrelerte | ✅ (kovariansen utenfor diagonalen er 0) |

### Vurdering

**Styrker**
- **Faglig moden analyse.**
  - Valget av PCA fremfor LDA er begrunnet.
  - Log-transformasjonen knyttes til at PCA er lineær.
  - PCA tilpasses bare på treningssettet.
  - Antall komponenter velges med to kriterier (95 % og Kaiser).
  - Komponentene tolkes meningsfullt.
- **At PC3 identifiseres som selve identiteten** mellom målingene, og at gruppen forklarer hvorfor
  den ikke er nøyaktig null (log10(x+1) og cappingen), viser ekte forståelse.
- **Testen av one-hot-kolonnene** besvarer et naturlig oppfølgingsspørsmål med tall, i stedet for
  å anta svaret.
- **Drøftingen av hvordan PCA påvirker datasettet er meget god.** Den tar for seg dimensjon,
  korrelasjon, informasjonstap (også på testsettet) og tolkbarhet, og sammenligner med et enklere
  alternativ (å droppe avling). Gruppen trekker en ærlig konklusjon om at gevinsten er liten, og
  det er nettopp den typen kritisk drøfting oppgaven ber om.
- Alle tall stemmer.

**Svakheter og mulige merknader fra sensor**
1. **Resultatet er i stor grad gitt på forhånd.** Avling er per definisjon en funksjon av areal og
   produksjon, så det er ikke overraskende at to komponenter forklarer 99.95 %. Gruppen *sier* dette
   («one redundant measurement»), men kunne vært tydeligere på at PCA her i hovedsak bekrefter
   noe som var kjent fra oppgave 2. En mer interessant analyse kunne tatt med flere variabler.
2. **`Year` utelates med begrunnelsen «Year is not scaled».** Dette arver inkonsistensen fra 4b.
   `Year` burde vært skalert og testet, eller utelatt med en faglig begrunnelse.
3. **Figur 4 (høyre)** viser en ustrukturert punktsky. Hvis punktene var farget etter for eksempel
   vekstgruppe, kunne figuren vist hva PC1 og PC2 faktisk skiller. Venstre del er god.
4. **Tolkningen av PC3 som «production − area − yield»** er en forenkling. Vektene er −0.657,
   0.687 og −0.309, altså ikke like store, fordi kolonnene er standardisert med ulike standardavvik.
   Dette er en mindre merknad.
5. **Ordbruk.** Bonusdelen er lang (rundt 450–500 ord, omtrent 16 % av ordgrensen). Med «no extra
   points for extra text» og en total på 2984 av 3000 ord er det mye ord på en valgfri del,
   mens for eksempel 4b og 5b er tynne (se formelle krav).

### Konklusjon
Bonusoppgaven er meget god, og kanskje den sterkeste delen av besvarelsen. Metoden er riktig
gjennomført, tolkningen er god og konklusjonen om nytten av PCA er kritisk og ærlig. Merknadene
gjelder i hovedsak at resultatet langt på vei er gitt av identiteten, og at `Year` utelates med en
svak begrunnelse.

**Poeng: +9 / 10** (spenn 8–10).

---

## Formelle krav

### Hva oppgaven krever
- Innlevering som PDF (valgfri mal), med resultater og kode «where necessary». Kode skal bare
  være med når forklaringen ikke kan fullføres uten den.
- «Be as precise as possible … There are no extra points for extra text.»
- Maks **3000 ord**. Kode og referanser teller ikke, men tabell- og figurtekster teller.
- Vurderingskriterium 3: *quality of documentation and readability*. Kriterium 4: *completeness
  and adherence to instructions*.

### Sjekkliste
| Krav | Status | Kommentar |
|---|---|---|
| PDF | ✅ | 10 sider, LaTeX (pdfTeX), letter-format |
| Forside med gruppe og navn | ✅ | Gruppe 50, fem navn, oppgitt ordtelling |
| Kode bare når nødvendig | ✅ | Ingen kode i rapporten. Det er i tråd med instruksen. Alle tall er reproduserbare fra `src/`, men rapporten viser ikke til koden, for eksempel i et vedlegg eller med en lenke |
| Struktur etter oppgavenummer og deloppgaver | ✅ | Seksjonene 1–6 med a/b/c følger oppgaveteksten |
| Alle oppgavene besvart | ✅ | 1–5 og bonusoppgave 6 |
| Begrunnelse der det kreves (2c, 3b, 4a-ii, 4b-ii, 5b) | ✅ | Ingen mangler helt, så det blir ikke 10 poengs trekk noe sted. 4b-ii og 5b er tynne |
| Ordgrense 3000 | ⚠️ | Se under |
| Referanser | ⚠️ | Ingen referanseliste. FAOSTAT nevnes, men siteres ikke, og det er ingen henvisning til pensum |
| Alle figurer og tabeller henvist til i teksten | ❌ | Figur 3 er ikke henvist til. Tabell 7 er ikke henvist til, fordi den er en duplikat av Tabell 8 |
| Språklig konsistens | ❌ | Figur 3 har norske etiketter («før» og «etter») i en engelsk rapport |
| Korrektur og LaTeX | ❌ | «textbfa.» i 4a, identiske Tabell 7 og 8, feil anførselstegn (”more”), og `Year` vises med tusenskille («2,015») i Tabell 4 |
| Numerisk konsistens mellom oppgavene | ⚠️ | «China» mot «China, mainland» (1b), 8,436 mot 8,316 serier (3b mot 5a), spenn for avling «0–7» (4b) |

### Ordgrensen, vurdert nærmere
Gruppen oppgir **2984 ord**, altså 16 ord under grensen. Vår kontroll med tekst hentet ut fra PDF-en:

| Tellemåte | Ord |
|---|---|
| Alt i PDF-en (inkludert tabellinnhold, forside og sidetall) | ≈ 3,660 |
| Uten tabellinnhold, forside og sidetall | ≈ 3,250 |
| Som over, men bare tokens som inneholder bokstaver (tall og symboler ikke talt) | ≈ 3,000 |

- Tallet 2984 er troverdig hvis man bruker en teller som *texcount* og ser bort fra tall,
  matematikk og tabellinnhold. **En sensor som kopierer teksten inn i Word, vil få mellom 3,250 og
  3,660 ord.**
- Oppgaven sier ikke eksplisitt om tabellinnhold teller. Gruppens egen README pekte på denne
  uklarheten og anbefalte å avklare den med faglærer.
- Oppgaven sier ingenting om trekk for å gå over ordgrensen, bare «Please be within this limit».
  Et eventuelt trekk er derfor skjønn.
- Marginen er uansett **16 ord**. Den dupliserte Tabell 8 med bildetekst (rundt 30 ord med innhold)
  alene er nok til å skape tvil.

### Vurdering
- **Positivt:** Rapporten er profesjonelt satt opp i LaTeX med nummererte tabeller og figurer,
  følger oppgavestrukturen tett, inneholder ingen unødvendig kode, og alle deloppgavene er besvart.
  Alle begrunnelser som kreves, finnes.
- **Negativt:** Det er tydelige tegn på at rapporten ikke er korrekturlest til slutt. Dette gjelder
  særlig oppgave 3 og 4, som ser ut til å være skrevet sist og av andre enn de som skrev oppgave 1–2
  (duplisert tabell, «textbfa.», norske etiketter i figuren, figur uten henvisning og tall som ikke
  henger sammen). Dette går direkte på kriteriene 3 og 4.
- **Ordfordelingen er skjev:** Innledningen (rundt 380 ord) og bonusoppgaven (rundt 480 ord) bruker
  nesten 30 % av ordene, mens delene som krever forklaring og gir poeng (4b-ii og 5b), er tynne.

**Trekk under formelle krav:** Formelle krav har ingen egen poengsum. Svakhetene i dokumentasjonen
er allerede trukket i oppgave 3 og 4. **Det eneste reelle ekstra trekket er risikoen ved ordgrensen:
0 poeng hvis sensor godtar 2984 ord, opptil omtrent 5 poeng hvis sensor teller selv og mener
grensen er brutt.**

### Rask gevinst før innlevering (hvis det fortsatt er mulig)
1. Slett Tabell 7 eller 8. Det sparer rundt 30 ord og fjerner den mest synlige feilen.
2. Rett «textbfa.» og anførselstegnene, bytt «før» og «etter» til «before» og «after», og henvis
   til Figur 3 i teksten.
3. Rett «China» til «China, mainland», «31 of 8,436» til «17 of 8,316» og spennet for avling.
4. Kort ned innledningen (Sudan og USSR) og gjentakelsene i 4a med til sammen rundt 150 ord, og
   bruk ordene på 4b-ii (virkninger på modellen) og 5b (valideringssett og kryssvalidering).
5. Legg til en kort referanseliste (FAOSTAT og forelesningsnotatene).

---

## Helhetsvurdering

### Det bærende grepet: en pipeline som bygger på data, ikke på oppskrifter
Det som skiller denne besvarelsen fra en gjennomsnittlig besvarelse, er at nesten hvert valg bygger på
en *undersøkelse av dataene* og ikke på en standardoppskrift:
- Datasettet er valgt ut fra hva oppgavene krever.
- Aggregatene er fjernet fordi de gir dobbelttelling.
- Årsaken til de manglende verdiene er undersøkt før tiltakene ble valgt.
- Outliers er vurdert per vekst, og IQR på log-skala er brukt som diagnose.
- Gruppen testet om one-hot-kolonnene faktisk bidrar i PCA i stedet for å anta det.

Påstandene er nesten alltid tallfestet. Av flere titalls tall vi kontrollerte mot dataene var bare
rundt fem feil eller upresise («32 countries», 117 og ikke 118 vekster, «China» i stedet for
«China, mainland», «31 of 8,436» i stedet for 17 av 8,316, og spennene i 4b), og ingen av dem endrer en konklusjon. Rapporten er også uvanlig ærlig om begrensninger,
som lekkasje ved imputering og splitting og den lille gevinsten av PCA. Vurderingskriterium 2
(*justification*) er derfor gjennomgående godt oppfylt, og det finnes ingen deloppgave med 10 poengs
trekk.

### Men tråden holder ikke hele veien
Leser man rapporten som *én* pipeline og ikke som seks separate svar, kommer det fram fem
gjennomgående svakheter. Hver av dem er liten i én oppgave, men sammen trekker de helheten ned.

**1. Rapporten mangler et formål.** Oppgaven handler om å klargjøre data «for modeling», men det står
aldri hva modellen skal predikere. Ordet «regression» dukker opp for første gang i den siste setningen i 4a. Uten en
målvariabel henger flere valg i løse luften:
- Skal avling være målet? Da er det problematisk å imputere den (oppgave 2) og cappe den (oppgave 3).
- Hvilke modeller skal skaleringen tilpasses (oppgave 4b)?
- Hva er relevant lekkasje (oppgave 5)?
- Skal PCA brukes på features eller på alt (oppgave 6)?

Én setning i innledningen, for eksempel «we prepare the data for predicting yield from area,
country, crop and year», ville gitt alle de senere begrunnelsene et anker.

**2. Identiteten avling = produksjon × 10,000 / areal er den røde tråden, men den blir ikke brukt
konsekvent.**
- Den nevnes ikke i utforskningen (oppgave 1), der den hører hjemme.
- Den brukes aktivt og elegant i oppgave 2, der areal og produksjon utledes fra den imputerte
  avlingen.
- Den brytes stille i oppgave 3, fordi hver kolonne cappes for seg. Den blir da inkonsistent i
  2,578 rader.
- Den oppdages på nytt som hovedfunnet i oppgave 6: «one redundant measurement».

En samlet framstilling ville identifisert redundansen i oppgave 1 og tatt stilling til den der, for
eksempel ved å behandle avling som målvariabel eller droppe den. Da ville konklusjonen i PCA-delen
vært en bekreftelse og ikke en oppdagelse.

**3. Lekkasjeprinsippet brukes selektivt.** Gruppen viser at de forstår prinsippet svært godt:
skaleringen (4b) og PCA (6) tilpasses bare på treningssettet, og dette forklares grundig. Men
rekkefølgen i pipelinen er imputering (2) → capping (3) → encoding (4a) → splitting (5) →
skalering (4b) → PCA (6). Både imputeringsmedianene og cappinggrensene beregnes dermed på hele
datasettet. Lekkasjen erkjennes for imputeringen, men ikke for cappingen, og begrunnelsen for å
godta den («the order follows the assignment and only 256 rows (0.3%) are imputed») er bare delvis
faglig. At lekkasjen er liten, er et gyldig argument, men rekkefølgen i oppgaveteksten er det ikke. En sensor som leser 4b etter 2 og 3,
vil se at gruppen kjente løsningen, som er å splitte først og tilpasse alt på treningssettet, men
ikke brukte den konsekvent.

**4. Tidsseriene blir oppdaget sent og ikke utnyttet.** At dataene er 8,316 serier, de fleste (93 %) med 11 år,
er avgjørende for tre av oppgavene. Tidsseriene nevnes i innledningen, 2c og 3b, og stabiliteten
over tid brukes i 2c som begrunnelse for medianen per land. Konsekvensene for metodevalget drøftes
likevel først i oppgave 5, og da bare som en begrensning:
- **Oppgave 2:** Interpolasjon mellom nabo-år er det naturlige alternativet til medianen per land.
- **Oppgave 3:** Et hopp i en serie er en bedre indikator på feil enn IQR på tvers av land.
- **Oppgave 5:** En tidsbasert splitt (2010–2018 mot 2019–2020) gir 82/18, beholder alle
  kategorier i treningssettet og gir et realistisk prognoseoppsett. Den løser likevel ikke
  lekkasjen gruppen peker på, fordi seriene ligger i begge settene. Det gjør bare en gruppesplitt.

Rapporten viser at gruppen har forstått strukturen. Den mangler bare å tenke den inn fra starten.

**5. Synet på outliers skifter underveis.** I oppgave 1b og 3a er hovedargumentet at de ekstreme
verdiene er *ekte* variasjon i landstørrelse og produksjonssystem. I 3b capper gruppen de
gjenværende outlierne uten å forklare hvorfor ekte verdier skal endres. I praksis blir særlig små,
ekte produsenter endret, og de 31 radene med avlingssvikt, som gruppen eksplisitt begrunnet
log10(x+1) med å ville beholde, cappes opp fra 0. Dette er den tydeligste av flere interne
inkonsistenser (se også `Year` i 4b og argumentet mot gruppesplitt i 5a).

### Ujevn kvalitet: rapporten har flere stemmer
Innledningen og oppgave 1, 2 og 6 har samme presise og tette stil og er nesten feilfrie. Oppgave 3
og 4 har en annen stil:
- De er mer ordrike (4a gjentar det samme poenget flere ganger).
- Det er unøyaktige tall (spennene i 4b, der avlingen faktisk går fra 2.59 til 6.71).
- Det er korrekturfeil («textbfa.», duplisert tabell, norske figuretiketter, figur uten henvisning).
- Det er inkonsistenser mot resten (`Year` er «discrete codes», 8,436 serier).

Arbeidsfordeling er helt normalt, men en siste redaksjonell runde der én person leste hele
rapporten fra start til slutt, ville fanget nesten alle disse feilene. Det er også denne delen av
helheten en sensor legger merke til først, fordi den er synlig uten å kjøre data.

### Ordbudsjettet er feil prioritert
Rapporten ligger 16 ord under grensen etter egen telling og kan havne over etter sensors telling.
Samtidig brukes rundt 30 % av ordene på innledningen og bonusoppgaven, som ikke gir ordinære poeng,
mens de to spørsmålene som eksplisitt ber om forklaring (4b-ii «how it impacts the model» og 5b «how
it prevents overfitting»), er de tynneste svarene. Oppgaven sier «no extra points for extra text».
Her går ordene til det som er interessant for gruppen, og ikke til det som gir poeng.

### Hva en sensor faktisk vil se
Mange av merknadene over fant vi ved å kjøre koden mot dataene, og de er *ikke* synlige i PDF-en.
Det gjelder blant annet at cappingen hever små verdier og nullene, at de 125 skjulte verdiene fordeler
seg på 64 og 61 rader, og at grupperingsargumentet bare gjelder 4 serier. En vanlig sensor som bare
leser rapporten, vil se:
- en svært grundig og profesjonell rapport (sterkt førsteinntrykk),
- korrekturfeilene i oppgave 3–4,
- den mangelfulle begrunnelsen for cappingen,
- at `Year` behandles forskjellig i oppgave 1 og 4,
- tynne svar i 4b-ii og 5b,
- og eventuelt ordgrensen.

En slik sensor vil trolig ligge **i øvre del av spennet vårt eller over det**.

### Samlet poengsum

| Del | Maks | Vår vurdering | Spenn |
|---|---|---|---|
| 1 Data Exploration | 10 | 9 | 9–10 |
| 2 Data Cleaning | 20 | 18 | 17–19 |
| 3 Handling Outliers | 20 | 16 | 14–17 |
| 4 Data Transformation | 30 | 26 | 24–27 |
| 5 Data Splitting | 10 | 8 | 7–9 |
| **Sum ordinære** | **90** | **77** | **71–82** |
| 6 Bonus (PCA) | +10 | +9 | 8–10 |
| Ordgrense (risiko) | – | 0 | 0 til −5 |
| **Totalt** | **100** | **86** | **79–92** (74–92 med fullt trekk for ordgrensen) |

**Justering for helhet:** Ingen egen justering. Svakhetene i helheten (manglende formål,
selektiv lekkasjehåndtering og tidsseriene) er allerede trukket i oppgavene der de slår ut. Styrkene
i helheten (en datadrevet tilnærming, etterprøvbarhet og ærlighet) er grunnen til at ingen oppgave
ligger under 80 %. Å trekke en gang til ville vært dobbel straff.

### Konklusjon
Dette er en **sterk besvarelse**. Den er analytisk bedre enn det oppgaven krever, godt begrunnet og
etterprøvbar, men den er ikke helt ferdig som én samlet tekst. Faglig er den på A-nivå i oppgave 1,
2 og 6. Det som trekker ned, er ikke manglende kunnskap, men manglende *konsistens*: et formål som
aldri blir sagt, prinsipper som brukes i én oppgave og glemmes i en annen, og en siste
korrekturrunde som mangler. Med en times redaksjonelt arbeid (se «Rask gevinst» under formelle
krav) og én setning om målvariabel i innledningen ville besvarelsen trolig ligget på **90+**.

**Endelig vurdering: 86 / 100 (77/90 + 9 bonus)**, realistisk spenn hos en sensor 79–92 (74–92 hvis sensor trekker fullt for ordgrensen).
