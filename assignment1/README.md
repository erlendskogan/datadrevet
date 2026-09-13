# Assignment 1 – Data Preprocessing (FAOSTAT crop1)

**Start her.** Datasett: FAOSTATs avlingsstatistikk, `crop1.csv` fra food-bank-mappen på Blackboard.
Oppgaveteksten ligger i [`oppgavetekst.pdf`](oppgavetekst.pdf).

## Status

| Del | Status | Rapporttekst | Kode |
|---|---|---|---|
| Valg og tilpasning av datasett | ✅ Ferdig | [`rapport/0-datasett.md`](rapport/0-datasett.md) | [`src/0_tilpass_datasett.py`](src/0_tilpass_datasett.py) |
| 1 Datautforskning | ✅ Ferdig | [`rapport/1-datautforskning.md`](rapport/1-datautforskning.md) | [`src/1_datautforskning.py`](src/1_datautforskning.py) |
| 2 Manglende verdier | ✅ Ferdig | [`rapport/2-manglende-verdier.md`](rapport/2-manglende-verdier.md) | [`src/2_manglende_verdier.py`](src/2_manglende_verdier.py) |
| 3 Outliers | ⏳ Gjenstår | – | – |
| 4 Encoding og skalering | ⏳ Gjenstår | – | – |
| 5 Splitting | ⏳ Gjenstår | – | – |
| 6 PCA (bonus) | ⏳ Gjenstår | – | – |

**Skal du gjøre oppgave 3–6? Les [`notater-oppgave3-6.md`](notater-oppgave3-6.md) først.**
Viktigst: gruppen må bestemme målvariabel før oppgave 3, fordi avling = produksjon × 10 000 / areal.

## Mappestruktur

```
assignment1/
├── README.md                 ← denne filen
├── oppgavetekst.pdf
├── notater-oppgave3-6.md     ← råd og ferdig utregnede tall til resten av oppgavene
├── rapport/                  ← norsk arbeidsversjon av rapportteksten (se «Rapporten» under)
│   ├── 0-datasett.md
│   ├── 1-datautforskning.md
│   ├── 2-manglende-verdier.md
│   └── figurer/              ← lages av src/1_datautforskning.py
└── src/                      ← ett skript per oppgave, kjøres i nummerrekkefølge
    ├── felles.py             ← stier og kolonnenavn, importeres av alle skriptene
    ├── 0_tilpass_datasett.py
    ├── 1_datautforskning.py
    └── 2_manglende_verdier.py
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
```

Skriptene sjekker seg selv underveis (blant annet at ingen verdier går tapt i pivoteringen og at
avling = produksjon × 10 000 / areal i alle rader), og stopper med en feilmelding hvis noe er galt.
Alle tall i rapporttekstene kommer fra utskriften til skriptene.

## Rapporten

Den innleverte rapporten skrives i **Overleaf, på engelsk**. Introduction (valg av datasett),
oppgave 1 og oppgave 2 er lagt inn der, med LaTeX-tabeller (booktabs) og figurene fra `rapport/figurer/`
(last dem opp i Overleaf-prosjektet). Filene i `rapport/` er den norske arbeidsversjonen av de samme tekstene.

## Når dere legger til oppgave 3–6

- Nytt skript: `src/3_outliers.py` osv. Start med `from felles import CLEAN, NUM, A, P, Y, read` og `df = read(CLEAN)`.
- Rapporttekst skrives rett i Overleaf (engelsk). Notater kan eventuelt legges i `rapport/3-outliers.md` osv.
- Nummerering: LaTeX nummererer selv – bruk `\label`/`\ref`. Table 1–5 og Figure 1–2 er brukt.
- Tallformat i rapporten: engelsk, med komma som tusenskille og desimalpunktum (98,101 og 7.3%).
- Figurer med engelske etiketter, i samme stil som `1_datautforskning.py`.

## Ordbudsjett (grense 3 000 ord)

Talt på den engelske teksten i Overleaf:

| Del | Ord (inkl. tabell- og figurtekster) |
|---|---|
| Introduction (datasett) | ca. 330 |
| Oppgave 1 | ca. 345 |
| Oppgave 2 | ca. 560 |
| **Brukt** | **ca. 1 240** |
| **Igjen til oppgave 3–6** | **ca. 1 760** |

Selve tabellinnholdet utgjør ca. 320 ord til. Oppgaveteksten sier at tabell- og figurtekster teller,
men ikke om tabellinnholdet gjør det – det bør avklares med faglærer.
