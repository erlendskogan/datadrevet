"""Steg 0 – tilpasning av crop1.csv før oppgave 1 (rapportens datasett-avsnitt, Tabell 1).

  A1  Pivot langt -> bredt: Element blir kolonner, enheten står i kolonnenavnet
  A2  Fjern 35 regioner/landgrupper (summer av land -> dobbelttelling)
  A3  Behold årene 2010–2020

Ingen verdier endres. Inn: food-bank/crop1.csv  ->  Ut: food-bank/crop1_trimmed.csv
Kjør: python assignment1/src/0_tilpass_datasett.py
"""
from felles import KEYS, NUM, RAW, TRIMMED, A, P, Y, StepLog, read

COLUMN_NAMES = {("Area harvested", "ha"): A, ("Production", "tonnes"): P, ("Yield", "hg/ha"): Y}
FIRST_YEAR, LAST_YEAR = 2010, 2020
AGGREGATES = {
    "World", "Africa", "Americas", "Asia", "Europe", "Oceania",
    "Eastern Africa", "Middle Africa", "Northern Africa", "Southern Africa", "Western Africa",
    "Caribbean", "Central America", "Northern America", "South America",
    "Central Asia", "Eastern Asia", "South-eastern Asia", "Southern Asia", "Western Asia",
    "Eastern Europe", "Northern Europe", "Southern Europe", "Western Europe",
    "Australia and New Zealand", "Melanesia", "Micronesia", "Polynesia",
    "European Union (27)", "Least Developed Countries", "Land Locked Developing Countries",
    "Low Income Food Deficit Countries", "Net Food Importing Developing Countries",
    "Small Island Developing States",
    "China",  # sum av China, mainland + Taiwan + Hongkong + Macao -> dobbelttelling
}

step = StepLog()
raw = read(RAW)

# Hvert Element har nøyaktig én enhet, og ingen måling finnes to ganger
units = raw.groupby("Element")["Unit"].unique()
assert all(len(u) == 1 for u in units), f"Blandede enheter: {units}"
assert {(e, u[0]) for e, u in units.items()} == set(COLUMN_NAMES)
assert not raw.duplicated(KEYS + ["Element"]).any()

raw["col"] = [COLUMN_NAMES[k] for k in zip(raw["Element"], raw["Unit"])]
wide = raw.pivot(index=KEYS, columns="col", values="Value").reindex(columns=NUM).reset_index()
wide.columns.name = None
assert wide[NUM].notna().sum().sum() == raw["Value"].notna().sum()  # ingen verdier tapt
df = step("A1 Pivotert til bredt format", wide)

assert AGGREGATES <= set(df["Area"])
df = step("A2 Fjernet 35 regioner/landgrupper", df[~df["Area"].isin(AGGREGATES)])
df = step(f"A3 Beholdt {FIRST_YEAR}–{LAST_YEAR}", df[df["Year"].between(FIRST_YEAR, LAST_YEAR)])
df.to_csv(TRIMMED, index=False)

print(f"Original: {len(raw):,} rader i langt format, {raw['Area'].nunique()} områder, "
      f"{raw['Item'].nunique()} vekster ({raw['Value'].isna().sum():,} tomme Value)\n")
step.print()
print("\nManglende (%): " + ", ".join(f"{c} {v}" for c, v in (df[NUM].isna().mean() * 100).round(1).items()))
print(f"Resultat: {TRIMMED.relative_to(TRIMMED.parents[1])} ({TRIMMED.stat().st_size / 1e6:.1f} MB)")
