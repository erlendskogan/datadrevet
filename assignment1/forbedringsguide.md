# Fra dagens rapport til en A

Guide til gruppe 50 for å gjøre rapporten helhetlig. Den bygger på `sensorvurdering.md`, men
er skrevet som en arbeidsliste, ikke som en vurdering. Alt som står her gjelder **innholdet i
rapporten**, ikke koden.

Dagens nivå er 86 av 100, med et realistisk sensorspenn på 79 til 92. Det som mangler er ikke
kunnskap, men konsistens. Rapporten leser som seks gode svar skrevet av tre personer, ikke som
én pipeline. Denne guiden lukker det gapet med rundt 150 nye ord, rundt 450 fjernede ord og en
redaksjonell runde.

---

## Slik leser en sensor helheten

Vurderingskriteriene er fire, og bare det første handler om enkeltoppgavene.

| Kriterium | Hva det egentlig måler | Dagens status |
|---|---|---|
| 1 Riktig bruk av teknikker | Hver deloppgave for seg | Sterkt, 1, 2 og 6 er A-nivå |
| 2 Klarhet og begrunnelse | At valgene henger sammen på tvers | Ujevnt, tre prinsipper brukes selektivt |
| 3 Dokumentasjon og lesbarhet | Førsteinntrykk, korrektur, figurer | Svakest, feilene er synlige uten data |
| 4 Fullstendighet og instruks | Ordgrense, struktur, alle spørsmål besvart | Risiko på ordgrensen, to tynne svar |

Kriterium 2, 3 og 4 handler altså om helheten. Det er der A-en ligger.

---

## Del 1, fire grep som bærer hele rapporten

Gjør disse fire først. De er de eneste endringene som faktisk flytter det faglige inntrykket,
resten er opprydding.

### G1 Si hva dataene skal brukes til, og si det i innledningen

**Problemet.** Rapporten sier aldri hva modellen skal predikere. Ordet «regression» står én gang,
i siste setning av 4a. 4b snakker om «distance- or gradient-based models», 5b om «the model»,
og 6 om «the dataset». Leseren møter tre modellbilder og ingen målvariabel, og da henger
imputeringen i 2, cappingen i 3, skaleringen i 4b og PCA-en i 6 i løse luften.

**Grepet.** Velg målvariabel nå, og la den styre formuleringene i alle seks oppgavene.

Vi anbefaler **produksjon som mål, med areal, land, vekst og år som features, og avling holdt
utenfor featurene**. Begrunnelsen er at valget gjør oppgave 6 til en bekreftelse i stedet for en
oppdagelse, siden PCA-konklusjonen «the dataset contains one redundant measurement» da er nøyaktig
den kolonnen innledningen allerede har lagt bort. Valget gjør også imputeringen mindre
problematisk, fordi målet bare er utledet i 34 av de 256 imputerte radene, mens areal er utledet
i de øvrige 222.

Alternativet er **avling som mål, med areal, land, vekst og år som features, og produksjon holdt
utenfor**. Det er like forsvarlig, men da er målet selv imputert i alle 256 radene og cappet i
2 575 celler, og begge deler må nevnes eksplisitt i 2c og 3b.

**Hvor det skal stå.**
- Innledningen, én setning rett etter valget av datasett.
- 2c, én bisetning om at de imputerte radene er merket fordi enten målet eller en feature er
  utledet i dem.
- 3b, én bisetning om at cappingen også treffer målkolonnen.
- 4b-ii, bytt «distance- or gradient-based models» med den modellen dere faktisk sikter mot.
- 5b, bytt «the model» med samme modell.
- 6, koble «one redundant measurement» til valget i innledningen.

### G2 Gjør identiteten til en rød tråd i stedet for et funn

**Problemet.** Sammenhengen avling = produksjon × 10 000 / areal bærer hele besvarelsen, men
behandles ulikt i hver oppgave. Den nevnes ikke i 1, brukes aktivt i 2b, brytes stille i 3, og
gjenoppdages som hovedfunn i 6. At 6 presenterer som et funn det 2b allerede regnet med som kjent,
får rapporten til å framstå som om den ikke husker seg selv.

**Grepet.** Introduser identiteten der målingene introduseres, i 1a, og la de andre oppgavene
referere tilbake til den.

- **1a** får én setning om at de tre målingene bare er to uavhengige størrelser.
- **2b** står allerede riktig, men bytt «the identity» til «the identity from Task 1a».
- **3b** får én setning om at capping per kolonne bryter identiteten, og at det er prisen for
  å beholde alle radene.
- **6** endrer status fra oppdagelse til bekreftelse, «PCA confirms what Task 1a noted».

Etter dette står identiteten nevnt i fire oppgaver som fire trinn i samme resonnement, ikke som
fire løsrevne observasjoner.

### G3 Bruk lekkasjeprinsippet likt i alle ledd, og si rekkefølgen én gang

**Problemet.** Rapporten forklarer lekkasje bedre enn de fleste, men bruker prinsippet i tre av
fire ledd. 2c erkjenner lekkasjen fra medianene, men begrunner den delvis med at «the order
follows the assignment», som er en formell og ikke faglig begrunnelse. 3 sier ingenting om at
cappinggrensene er regnet på hele datasettet. 4b og 6 er derimot strenge og godt forklart. En
sensor som leser 4b etter 3, ser at gruppen kjente løsningen og ikke brukte den konsekvent.

**Grepet.** Tre små tillegg, ingen ny analyse.

1. **2c**, bytt ut «the order follows the assignment» med et faglig argument, at lekkasjen er
   avgrenset til 256 rader som dessuten er merket og kan holdes utenfor evalueringen.
2. **3b**, én setning om at grensene er beregnet på hele datasettet, hva det betyr, og hvorfor
   det aksepteres.
3. **5a**, én setning først som slår fast rekkefølgen i pipelinen.

**Rekkefølgen leseren trenger.** Rapporten presenterer 2, 3, 4a, 4b, 5, 6, mens arbeidet faktisk
gikk 2, 3, 4a, 5, 4b, 6. I dag må leseren snu om på det selv, fordi 4b refererer framover til
oppgave 5 mens oppgave 5 aldri refererer tilbake til 4b. Én setning i 5a løser hele problemet
uten å flytte noen seksjon.

### G4 Ta panelstrukturen inn fra starten

**Problemet.** At datasettet er 8 316 tidsserier med typisk 11 år hver, er avgjørende for tre
oppgaver, men konsekvensen drøftes først i 5a, og da bare som en begrensning gruppen godtar.
5a sitt eget motargument mot gruppesplitt, at noen land og vekster bare finnes i én serie, blir
heller ikke tallfestet, og uten tall er det ikke et argument.

**Grepet.** Nevn strukturen i 1b sammen med de kategoriske kolonnene, siden den er en egenskap ved
dataene og hører hjemme i utforskningen, og tallfest motargumentet i 5a. Dersom dere vil strekke
dere lenger, si i 2c at interpolasjon mellom nabo-år er alternativet til medianen per land, og
i 3a at et hopp innenfor én serie er en bedre feilindikator enn IQR på tvers av land. Begge deler
koster en halv setning og viser at strukturen er tenkt inn, ikke oppdaget til slutt.

---

## Del 2, ferdige tekstbiter

Alt under er skrevet på engelsk i rapportens egen stil og kan limes rett inn. Ordtallet står i
parentes.

### Innledningen, etter «...making feature scaling trivial and PCA meaningless.»

> Throughout the report we prepare the data for one purpose, predicting production from harvested
> area, country, crop and year. Yield is therefore not part of the feature set, since it is a
> deterministic function of the other two measurements. (34 ord)

### 1a, etter «...(Table~\ref{tab:columns})»

> The three measurements are not independent, since yield is production divided by area, scaled to
> hg/ha. The dataset therefore holds two independent quantities, which shapes every later step.
> (29 ord)

### 1b, erstatt «Their handling follows in Task 3.»

> These zeros are handled in Task 2, where they turn out to mark crops that were not cultivated.
> (18 ord, erstatter 6)

### 1b, bytt «1,298 (China)» til

> 1,298 (China, mainland) (3 ord, erstatter 2)

Aggregatet «China» ble fjernet i innledningen, så dagens formulering motsier innledningen direkte.

### 1b, etter setningen om kategorier

> The rows also form 9,421 country and crop time series of up to 11 years each, a structure we
> return to in Tasks 2 and 5. (26 ord)

Merk at tallet er 9 421 her og ikke 8 316. Oppgave 1 beskriver datasettet før rensingen, og antallet
serier faller til 8 436 etter de første stegene i oppgave 2 og til 8 316 etter det siste. Sørg for at
hvert tall står i den oppgaven det gjelder.

### 2c, erstatt «We accept it because the order follows the assignment and only 256 rows (0.3%) are imputed.»

> We accept it because the leakage is confined to 256 flagged rows (0.3%), which can be excluded
> from evaluation, and because the alternative, imputing separately in each set, would leave the
> two sets with different medians. (37 ord, erstatter 21)

### 3b, etter «...the same pattern as \texttt{imputed} in Task 2.»

> Two consequences follow. The bounds are computed on the full dataset, so capping leaks in the
> same limited sense as the imputation in Task 2, and capping each column separately breaks the
> identity from Task 1a, which is why PC3 in Task 6 is close to but not exactly zero. Capping the
> lower bound also lifts the 31 crop failure rows off zero, which we accept because the flag makes
> the change reversible. (73 ord)

Denne ene bolken lukker tre av inkonsistensene sensorvurderingen peker på, og den koster mindre
enn gjentakelsene i 4a.

### 3b, erstatt «are more likely to be genuinely extreme, since the transform has already corrected the skew»

> are extreme relative to their own crop even after the skew is corrected, which is the case where
> capping changes the fewest values for the largest effect (25 ord, erstatter 17)

Dagens formulering begrunner cappingen med at verdiene er ekte, som er det samme argumentet 1b og
3a bruker mot capping.

### 4b-ii, erstatt «roughly 0--7 for area, 0--9 for production, 0--7 for yield»

> roughly 0 to 7.7 for area, 0 to 8.9 for production and 2.6 to 6.7 for yield (18 ord, erstatter 13)

### 4b, erstatt «since they are binary indicators or discrete codes, not continuous measurements»

> since the one hot columns and the flags are binary, and \texttt{Year} is an ordered count on its
> own natural scale (Task 1a) (22 ord, erstatter 12)

Dagens formulering sier at `Year` er en «discrete code», mens 1a slår fast at den er numerisk fordi
årene er ordnet og likt fordelt.

### 4b-ii, nytt avsnitt til slutt, dette er svaret på «how it impacts the model»

> Scaling changes no information in the data, only its representation, but it changes how a model
> uses it. A linear model fitted on unscaled columns gives coefficients in units per hectare and
> per tonne, which cannot be compared, and gradient descent converges slowly when one column is
> orders of magnitude wider than another. With standardised inputs the coefficients are comparable
> in standard deviations, regularisation penalises every column equally, and PCA in Task 6 finds
> the directions of largest variance rather than the column with the largest unit. (85 ord)

### 5a, ny førstesetning

> The dataset is split after encoding (Task 4a) and before scaling (Task 4b), so that every
> parameter fitted later sees the training set only. (24 ord)

### 5a, erstatt «but some countries and crops occur in only one series»

> but three countries and one crop occur in a single series each, so four series would have to be
> forced into the training set for the encoding in Task 4a to cover every category (35 ord,
> erstatter 12)

Tallfestingen gjør argumentet etterprøvbart, og den viser at gruppesplitt var mulig, som er mer
ærlig enn dagens formulering.

### 5b, nytt avsnitt til slutt, dette er svaret på «how it prevents overfitting»

> The split does not prevent overfitting by itself, it makes it visible, and that is what lets us
> act on it. Because the test set is untouched during fitting, the gap between training and test
> error is an honest signal, and it is the signal that drives model choice, early stopping and
> regularisation strength. A model tuned directly on the test set would lose that signal, which is
> why a validation split or cross validation inside the training set is the usual next step. (86 ord)

### 6, erstatt «PCA thus shows that the dataset contains one redundant measurement»

> PCA thus confirms on the data what Task 1a stated from the definition, that the three
> measurements carry two independent quantities, and it supports the choice in the introduction to
> leave yield out of the feature set (38 ord, erstatter 12)

### 6, stryk «\texttt{Year} is not scaled.»

Setningen henger i løse luften, siden `Year` heller ikke er med i PCA-en.

---

## Del 3, hva som skal bort

Tilleggene over koster rundt 550 ord. Her er 700 ord som kan hentes uten at noe faglig går tapt.

| Sted | Hva | Ord |
|---|---|---|
| 4b | Den dupliserte tabellen med bildetekst | 30 |
| 4a | Tredje avsnitt om antall kolonner, kortes til én setning om at 317 binære kolonner mot 88 735 rader er håndterbart | 90 |
| 4a | Gjentakelsen i andre avsnitt, poenget om manglende rangordning står tre ganger, behold PCA-varianten | 110 |
| Innledningen | Sudan-detaljen og USSR-detaljen, behold konklusjonen om at årsavgrensningen unngår grenseendringer | 70 |
| 2c | Soppavsnittet, spennet 0,6 til 5 085 tonn per hektar holder, resten kan kortes | 40 |
| 3b | «Dropping these rows instead was rejected...», kortes til en bisetning | 30 |
| 6 | One-hot-avsnittet, behold tallene 213 av 320 og variansen 0,006, kort resten | 60 |
| 1b | «Many flagged values are therefore likely genuine variation...», overlapper med 3a | 25 |
| Hele | Ordrike innledninger til avsnitt, «It is worth noting that», «In other words» | 50 |

Tilleggene i del 2 er til sammen rundt 550 ord, og de erstatter rundt 95 ord som går ut, så netto
tillegg er rundt 455 ord. Med 700 ord fjernet blir rapporten rundt 245 ord kortere enn i dag, og de
nye ordene ligger der oppgaveteksten faktisk ber om forklaring.

---

## Del 4, ordgrensen

Dette er det mest undervurderte punktet i hele rapporten.

| Telling | Ord |
|---|---|
| Brødtekst, som oppgitt på forsiden | 2 984 |
| Bildetekster, 13 stykker | 168 |
| Seksjonsoverskrifter | 16 |
| **Sum etter oppgavetekstens regel** | **≈ 3 168** |

Oppgaveteksten sier rett ut at «the table and figure captions are counted». Forsidens 2 984 er
altså brødteksten alene, og rapporten ligger reelt rundt 5 prosent over grensen.

**Mål.** Brødteksten ned til rundt 2 740 ord, som er der del 2 og del 3 lander den. Med 155 ord bildetekster, etter at den dupliserte
tabellen er fjernet, og 16 ord overskrifter, lander totalen på rundt 2 910.

**Forsiden.** Oppgi tallet som følger oppgavetekstens regel, ikke brødteksten alene. Et tall som
er lavere enn sensors egen telling, ser verre ut enn et ærlig tall like under grensen.

**Gratis plass.** Referanser teller ikke. En kort referanseliste med FAOSTAT og forelesningsnotatene
koster null ord og retter en mangel sensorvurderingen påpeker.

---

## Del 5, redaksjonell opprydding

Dette er kriterium 3, og det er det en sensor ser først, før noe faglig er lest.

| Nr | Feil | Fiks |
|---|---|---|
| 1 | Tabell 7 og 8 er identiske, med samme bildetekst og samme `\label{tab:scaling}` | Slett den ene |
| 2 | Seksjon 4 starter med «textbfa.» i PDF-en, `\textbf` mangler backslash | Rett til `\textbf{a.}` |
| 3 | Figur 3 har norske akseetiketter, «før» og «etter» | Generer figuren på nytt med «before» og «after», last opp på nytt |
| 4 | Figur 3 er aldri henvist til i teksten | Legg inn `(Figure~\ref{fig:outliers})` i 3b, eller stryk figuren og spar 24 ord |
| 5 | Figur 3 viser tilnærmet like bokser før og etter | Vis heller bare avlingsruten, der forskjellen er synlig, eller bytt til et histogram av de cappede cellene |
| 6 | Anførselstegn, «China» er korrekt i innledningen, ”more”, ”less” og ”centred” er feil i 4a og 4b | Bruk ``...'' overalt |
| 7 | 5b bruker amerikansk rettskriving, «memorized» og «generalizes», resten er britisk | Ensrett til britisk |
| 8 | 5a og 5b setter «a.» og «b.» inne i løpende tekst | Sett dem på egen linje som i de andre seksjonene |
| 9 | `Year` vises med tusenskille i Tabell 4, «2,015» | Fjern skilletegnet i årstallene |
| 10 | 8 436 mot 8 316 tidsserier | 2c er riktig, den teller før slettingen, 3b skal være 8 316, og gjelder 17 serier og ikke 31 |
| 11 | Ni kommentarlinjer fra utkastet ligger igjen i kilden over seksjon 3 | Slett dem, de påvirker ikke PDF-en, men de følger med i kilden |
| 12 | Ingen referanseliste, FAOSTAT nevnes uten kilde | Legg til, koster ingen ord |

---

## Del 6, arbeidsrekkefølge

Rekkefølgen er valgt slik at ingen jobber mot en tekst som endres under dem.

1. **Gruppen, 15 minutter.** Bestem målvariabel, G1. Alt annet henger på dette valget.
2. **Én person, 30 minutter.** Legg inn G1, G2, G3 og G4 med tekstbitene fra del 2. Dette er de
   eneste endringene som krever at man har lest hele rapporten.
3. **Én person, 30 minutter.** Kutt de 700 ordene fra del 3. Gjør dette etter punkt 2, slik at
   ordbudsjettet regnes på den endelige teksten.
4. **Én person, 20 minutter.** Regenerer figur 3 med engelske etiketter, last den opp, og legg inn
   henvisningen.
5. **Én person, 30 minutter.** Punkt 1, 2, 6, 7, 8, 9, 10, 11 og 12 i del 5.
6. **Én person, 20 minutter.** Les hele rapporten fra første til siste side i ett strekk, uten å
   rette, og noter bare steder der teksten motsier seg selv. Dette er den runden som mangler i dag,
   og den er grunnen til at feilene i oppgave 3 og 4 fortsatt står.
7. **Gruppen, 10 minutter.** Sjekklisten i del 7.

Samlet er dette rundt to og en halv time for gruppen.

---

## Del 7, sjekkliste før innlevering

- [ ] Målvariabelen står i innledningen, og de samme ordene brukes i 2c, 3b, 4b-ii, 5b og 6
- [ ] Identiteten er nevnt i 1a, brukt i 2b, håndtert i 3b og bekreftet i 6
- [ ] Lekkasje er nevnt i 2c, 3b, 4b og 6, med samme begrunnelseslogikk
- [ ] Rekkefølgen i pipelinen står eksplisitt i 5a
- [ ] Alle tabeller og figurer er henvist til i teksten
- [ ] Ingen tabell eller figur står to ganger
- [ ] Alle tall som gjentas i flere oppgaver er like, særlig antall serier, antall vekster og navnet
      på den største landkategorien
- [ ] Alle figurer har engelske etiketter
- [ ] Anførselstegn og rettskriving er ensartet i hele rapporten
- [ ] Ordtellingen på forsiden inkluderer bildetekstene, og totalen er under 3 000
- [ ] Referanselisten finnes
- [ ] Hele rapporten er lest i ett strekk av én person etter siste endring

---

## Vedlegg, det som allerede er A-nivå

Ikke rør disse. De er grunnen til at rapporten ligger høyt fra før, og flere av dem er bedre enn
det oppgaven krever.

- **Soppen som gjennomgående eksempel.** Introdusert som ekte ekstremverdi i 1b, fjernet med
  begrunnelse i 2c, med eksplisitt presisering av at fjerningen ikke var outlier-håndtering, og
  fulgt opp i 3a med at største avling nå er nederlandske veksthusagurker. Dette er mønstergyldig
  sammenheng mellom tre oppgaver.
- **Flaggkolonnene.** `imputed` innføres i 2, `*_capped` i 3 med eksplisitt henvisning til samme
  mønster, og begge holdes utenfor både encoding og skalering. Konsistent hele veien.
- **Skjevheten.** Slått fast i 1a, tallfestet i 1b, brukt som argument for median i 2c, mot z-score
  i 3a og for standardisering i 4b. Den best gjennomførte tråden i rapporten.
- **Tre metoder sammenlignet i 3a.** Å bruke IQR på log-skala som diagnose, og ikke bare som
  metode, er et selvstendig poeng.
- **Kontrolltesten i 6.** At gruppen faktisk testet om one-hot-kolonnene bidrar, i stedet for å anta
  det, er det enkeltgrepet som skiller besvarelsen mest fra en gjennomsnittlig besvarelse.
- **Ærligheten.** Lekkasje, serielekkasje og den lille gevinsten av PCA er alle innrømmet. Behold
  det, og bygg heller ut begrunnelsene, som beskrevet i G3.
