"""Oppgave 2 – håndtering av manglende verdier (rapportens Tabell 5).

  B1  Dropp helt tomme rader (ingen verdi å imputere fra)
  B2  Fjern Mushrooms and truffles: dyrkes innendørs, så areal/avling per hektar er
      ikke meningsfullt (de fleste land rapporterer aldri areal)
  B3  Dropp «ikke dyrket»-rader (verken areal eller produksjon > 0): yield er udefinert
  B4  Areal = 0 med produksjon > 0 er fysisk umulig -> areal regnes som manglende
  B5  Slett hull der landet aldri har observert yield for veksten (anslaget ville
      måttet komme fra andre land og blitt svært usikkert)
  B6  Imputer yield med landets median for veksten og utled manglende
      areal/produksjon fra identiteten yield = produksjon * 10 000 / areal

Outliers beholdes – de håndteres i oppgave 3. Kolonnen `imputed` markerer imputerte rader.
Inn: food-bank/crop1_trimmed.csv  ->  Ut: food-bank/crop1_clean.csv
Kjør: python assignment1/src/2_manglende_verdier.py
"""
import numpy as np

from felles import CLEAN, NUM, TRIMMED, A, P, Y, StepLog, read

MUSHROOMS = "Mushrooms and truffles"

step = StepLog()
df = step("Utgangspunkt (crop1_trimmed.csv)", read(TRIMMED))

df = step("B1 Droppet helt tomme rader", df[df[NUM].notna().any(axis=1)])

assert MUSHROOMS in set(df["Item"])
df = step("B2 Fjernet Mushrooms and truffles", df[df["Item"] != MUSHROOMS])

# Verken areal eller produksjon > 0 (0 eller tom): veksten ble ikke dyrket
not_grown = ~(df[A] > 0) & ~(df[P] > 0)
df = step("B3 Droppet «ikke dyrket» (verken areal eller produksjon > 0)", df[~not_grown]).copy()

impossible = (df[A] == 0) & (df[P] > 0)
df.loc[impossible, A] = np.nan
step("B4 Areal=0 med produksjon>0 satt til manglende", df, affected=impossible.sum())

# B5: har landet aldri observert yield for veksten, måtte vi brukt vekstens median
# på tvers av land (svært usikker) – da slettes raden i stedet for å imputeres.
med_country = df.groupby(["Area", "Item"])[Y].transform("median")
no_own_data = df[Y].isna() & med_country.isna()
df = step("B5 Slettet hull uten landets egne data for veksten", df[~no_own_data]).copy()

# B6: yield er skalauavhengig og stabil innen et land over tid, mens areal/produksjon
# varierer med landstørrelse – derfor imputeres yield med landets median for veksten.
imputed = df[Y].isna()
df.loc[imputed, Y] = df.groupby(["Area", "Item"])[Y].transform("median")[imputed]
assert df.loc[imputed, Y].notna().all()

need_area, need_prod = imputed & df[A].isna(), imputed & df[P].isna()
assert (df.loc[need_area, Y] > 0).all()  # areal = produksjon / yield krever yield > 0
df.loc[need_area, A] = df.loc[need_area, P] * 1e4 / df.loc[need_area, Y]
df.loc[need_prod, P] = df.loc[need_prod, A] * df.loc[need_prod, Y] / 1e4
df["imputed"] = imputed
df = step("B6 Imputert yield (landets median), utledet areal/produksjon", df, affected=imputed.sum())

assert not df[NUM].isna().any().any()
violations = (~np.isclose(df[Y], df[P] * 1e4 / df[A], rtol=0.01, atol=1)).sum()
assert violations == 0, f"{violations} rader bryter yield = produksjon * 1e4 / areal"
df.to_csv(CLEAN, index=False)

step.print()
print(f"\nSlettet uten egne landdata: {no_own_data.sum():,} rader | imputert: {imputed.sum():,} rader "
      f"({imputed.mean() * 100:.1f} %), utledet areal i {need_area.sum()}, produksjon i {need_prod.sum()}")
print("yield = produksjon*1e4/areal stemmer (±1 %) i alle rader")
print(f"Resultat: {CLEAN.relative_to(CLEAN.parents[1])} ({CLEAN.stat().st_size / 1e6:.1f} MB), "
      f"{len(df):,} rader, {df['Area'].nunique()} land, {df['Item'].nunique()} vekster")
