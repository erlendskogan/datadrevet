# Assignment 1 – Data Preprocessing (FAOSTAT crop1)

**Start her.** Datasett: FAOSTATs avlingsstatistikk, `crop1.csv` fra food-bank-mappen på Blackboard.
Oppgaveteksten ligger i [`oppgavetekst.pdf`](oppgavetekst.pdf).

## Status

Alle deler er ferdige. Den innleverte rapporten er [`rapport/main.tex`](rapport/main.tex),
som er den samme filen som ligger i Overleaf-prosjektet.

| Del | Status | Norsk arbeidsversjon | Kode |
|---|---|---|---|
| Valg og tilpasning av datasett | ✅ | [`rapport/0-datasett.md`](rapport/0-datasett.md) | [`src/0_tilpass_datasett.py`](src/0_tilpass_datasett.py) |
| 1 Datautforskning | ✅ | [`rapport/1-datautforskning.md`](rapport/1-datautforskning.md) | [`src/1_datautforskning.py`](src/1_datautforskning.py) |
| 2 Manglende verdier | ✅ | [`rapport/2-manglende-verdier.md`](rapport/2-manglende-verdier.md) | [`src/2_manglende_verdier.py`](src/2_manglende_verdier.py) |
| 3 Outliers | ✅ | [`rapport/3-outliers.md`](rapport/3-outliers.md) | [`src/3_outliers.py`](src/3_outliers.py) |
| 4 Encoding og skalering | ✅ | [`rapport/4-transformation.md`](rapport/4-transformation.md) | [`src/4_encoding.py`](src/4_encoding.py), [`src/4b_scaling.py`](src/4b_scaling.py) |
| 5 Splitting | ✅ | [`rapport/5-data-splitting.md`](rapport/5-data-splitting.md) | [`src/5_data_splitting.py`](src/5_data_splitting.py) |
| 6 PCA (bonus) | ✅ | [`rapport/6-pca.md`](rapport/6-pca.md) | [`src/6_pca.py`](src/6_pca.py) |

**Målvariabel:** produksjon, predikert fra areal, land, vekst og år. Avling er holdt utenfor
featurene fordi avling = produksjon × 10 000 / areal. Dette valget står i innledningen i rapporten og
styrer begrunnelsene i oppgave 2, 3, 4b, 5 og 6.

**Vurdering og videre arbeid:** [`sensorvurdering.md`](sensorvurdering.md) er en gjennomgang av
besvarelsen mot oppgaveteksten, og [`forbedringsguide.md`](forbedringsguide.md) er arbeidslisten som
ble brukt til å rette rapporten. Notatene i [`notater-oppgave3-6.md`](notater-oppgave3-6.md) er
historiske, fra før oppgave 3–6 ble skrevet.

## Mappestruktur

```
assignment1/
├── README.md                 ← denne filen
├── oppgavetekst.pdf
├── sensorvurdering.md        ← vurdering av besvarelsen mot oppgaveteksten
├── forbedringsguide.md       ← arbeidslisten som ble brukt til å rette rapporten
├── notater-oppgave3-6.md     ← historiske notater fra før oppgave 3–6 ble skrevet
├── rapport/
│   ├── main.tex              ← den innleverte rapporten, identisk med Overleaf
│   ├── 0-datasett.md … 6-pca.md   ← norsk arbeidsversjon per oppgave
│   └── figurer/              ← lages av 1_datautforskning.py, 3_outliers.py og 6_pca.py
└── src/                      ← ett skript per oppgave, kjøres i nummerrekkefølge
    ├── felles.py             ← stier og kolonnenavn, importeres av alle skriptene
    ├── 0_tilpass_datasett.py
    ├── 1_datautforskning.py
    ├── 2_manglende_verdier.py
    ├── 3_outliers.py
    ├── 4_encoding.py
    ├── 4b_scaling.py         ← kjøres etter 5_data_splitting.py
    ├── 5_data_splitting.py
    └── 6_pca.py
```

## Dataflyt

Dataene ligger i `food-bank/` i roten av repoet og er holdt utenfor git (se `.gitignore`).
`crop1.csv` er for stor for GitHub (101 MB), så hver må legge den inn selv.

```
food-bank/crop1.csv            original fra Blackboard (1,9 mill. rader, langt format)
  │  src/0_tilpass_datasett.py   pivot, fjern 35 regioner, behold 2010–2020
  ▼
food-bank/crop1_trimmed.csv    98 101 rader, med manglende verdier   ← oppgave 1 beskriver denne
  │  src/2_manglende_verdier.py  håndter manglende verdier
  ▼
food-bank/crop1_clean.csv      88 735 rader, 0 manglende, outliers beholdt   ← start for oppgave 3–6
```

Kolonner i `crop1_clean.csv`: `Area` (200 land), `Item` (117 vekster), `Year` (2010–2020, numerisk),
`area_harvested_ha`, `production_tonnes`, `yield_hg_per_ha`, `imputed` (True i de 256 imputerte radene).

## Kjøre koden

Fra roten av repoet:

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt   # første gang
# legg crop1.csv i food-bank/
.venv/bin/python assignment1/src/0_tilpass_datasett.py
.venv/bin/python assignment1/src/1_datautforskning.py
.venv/bin/python assignment1/src/2_manglende_verdier.py
.venv/bin/python assignment1/src/3_outliers.py
.venv/bin/python assignment1/src/4_encoding.py
.venv/bin/python assignment1/src/5_data_splitting.py
.venv/bin/python assignment1/src/4b_scaling.py   # etter splitting, for å unngå lekkasje
.venv/bin/python assignment1/src/6_pca.py
```

Skriptene sjekker seg selv underveis (blant annet at ingen verdier går tapt i pivoteringen og at
avling = produksjon × 10 000 / areal i alle rader), og stopper med en feilmelding hvis noe er galt.
Alle tall i rapporttekstene kommer fra utskriften til skriptene.

## Rapporten

Den innleverte rapporten skrives i **Overleaf, på engelsk**, og kilden ligger i
[`rapport/main.tex`](rapport/main.tex). Filen i repoet og filen i Overleaf skal være identiske,
så endrer du én av dem, last den opp eller kopier den over til den andre. Figurene i
`rapport/figurer/` lastes opp i Overleaf-prosjektet. Filene `0-datasett.md` til `6-pca.md` er den
norske arbeidsversjonen av de samme tekstene.

## Regler for rapporten

- Nummerering: LaTeX nummererer selv, bruk `\label` og `\ref`. Rapporten har Table 1–7 og Figure 1–3.
- Tallformat: engelsk, med komma som tusenskille og desimalpunktum (98,101 og 7.3%).
- Figurer skal ha **engelske** etiketter, i samme stil som `1_datautforskning.py`.
- Alle tabeller og figurer skal være henvist til i teksten.
- Britisk rettskriving i hele rapporten (standardisation, winsorised, artefact, centred).

## Ordbudsjett (grense 3 000 ord)

Oppgaveteksten sier at tabell- og figurtekster teller, men at kode og referanser ikke gjør det.
Målt med Overleafs egen teller (texcount) på `main.tex`:

| Post | Ord |
|---|---|
| Brødtekst | 2 772 |
| Bildetekster (11 stykker) | 152 |
| Seksjonsoverskrifter | 16 |
| **Sum** | **2 940** |
| Minus referanselisten, som ikke teller | −23 |
| **Oppgitt på forsiden** | **2 917** |

Tallet hentes med `GET /project/<id>/wordcount?file=main.tex` i Overleaf, eller fra menyen.
Legger du til tekst, må du hente ut like mye et annet sted.
