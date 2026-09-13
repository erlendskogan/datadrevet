# Notater til dere som gjør oppgave 3–6

Les dette før dere begynner. Alle tall er regnet på `food-bank/crop1_clean.csv`
(lages av `src/2_manglende_verdier.py`).

## Før dere starter: bestem målvariabel

Oppgave 4 og 5 spør om effekten på «modellen», så gruppen bør bli enige om hva som skal predikeres før oppgave 3.

- **Avling er nøyaktig produksjon × 10 000 / areal** (stemmer i alle rader). Den kolonnen som kan regnes ut fra de andre, må ut av featurene, ellers lekker fasiten inn. To naturlige alternativer:
  - (a) avling fra `Area`, `Item`, `Year` (og eventuelt areal), uten produksjon
  - (b) produksjon fra areal, `Area`, `Item`, `Year`, uten avling
- **Lekkasje i de imputerte radene:** I de 256 radene med `imputed = True` er avlingen en median, og areal (222 rader) eller produksjon (34 rader) er regnet ut fra de andre kolonnene. Uansett hvilket mål dere velger, er enten målet eller en feature i disse radene regnet ut og ikke observert. Hold dem utenfor trening og testing, eller begrunn hvorfor de er med.

## Oppgave 3 – Outliers

- **Outlierne er stort sett ekte, ikke feil.** Fordelingene er tunghalede. Andel flagget per vekst:

  | Metode | Areal og produksjon | Avling |
  |---|---|---|
  | IQR | 13–14 % | 4,5 % |
  | IQR på log10 | 1,3–1,4 % | 2,9 % |
  | z > 3 | 2,1–2,2 % | 1,5 % |

  Dette gir et godt grunnlag for å diskutere om man bør fjerne, cappe eller log-transformere.
- **Detekter per vekst (`Item`).** Samlet sammenligner man sukkerrør med vanilje, og da måler man forskjell mellom vekster.
- **Største avling nå:** Nederlandske veksthusagurker (743 t/ha). Den er ekte, men er et annet produksjonssystem.
- **Soppen:** Oppgave 2 sier allerede at soppfjerningen tok ut de tre største avlingene, og at det ikke var outlier-håndtering. Henvis til det.
- **Nuller:** 31 rader har produksjon 0 og avling 0 (avlingssvikt). De tåler ikke log, så bruk log1p eller utelat dem, og forklar valget.

## Oppgave 4 – Encoding og skalering

- **Anbefaling: one-hot for `Area` og `Item`.** De er kategorier uten rekkefølge, og label-encoding ville gitt en rekkefølge som ikke finnes (for eksempel at Albania < Brasil). One-hot gir 317 kolonner, så kardinaliteten bør diskuteres.
- **`Year`** er bestemt som numerisk i oppgave 1, så den skal ikke encodes.
- **`imputed`** er et flagg. Ikke skaler den og ikke bruk den som feature.
- **Skalering er nødvendig:** Målingene spenner over flere tierpotenser (maks er 4 968 ganger Q3 for produksjon). Vurder log før skalering, i tråd med valget i oppgave 3.
- **Sudan:** Delingen i 2011 gir tre kategorier for samme område (se `rapport/0-datasett.md`).

## Oppgave 5 – Splitting

- **Lekkasje fra imputeringen** er allerede nevnt i oppgave 2. Henvis til det.
- **Paneldata:** Datasettet består av 8 316 tidsserier per land og vekst, med typisk 11 år hver. Avlingen varierer lite innen en serie (variasjonskoeffisient 0,10). En tilfeldig 80/20-split legger derfor nesten like rader i både trening og test og gir for optimistiske resultater. Vurder å splitte per serie (GroupShuffleSplit på Area + Item) eller på tid (for eksempel test = 2019–2020), eller begrunn den tilfeldige splitten.
- Husk lekkasjen om målvariabelen over.

## Oppgave 6 – PCA (bonus)

- **Bare to uavhengige målinger:** log(avling) = log(produksjon) − log(areal) + 4 stemmer eksakt i alle 88 704 rader der alle tre er større enn 0. På log-skala får den tredje hovedkomponenten derfor tilnærmet null varians. Det er et godt poeng å diskutere. På rå skala er sammenhengen ikke lineær.
- **Hold `imputed` utenfor,** og bestem om `Year` og one-hot-kolonnene skal være med.
