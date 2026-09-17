"""Oppgave 4a - encoding av kategoriske kolonner i crop1_outliers.csv.

One-hot encoding: hver unike verdi i Area og Item får sin egen binære kolonne
(0/1), f.eks. Area_Afghanistan, Area_Albania, .... Gruppen byttet fra label
encoding til one-hot fordi label encoding innfører en kunstig rangordning
(Albania=1 < Brasil=20) som ikke finnes i dataene, og som ville vært misvisende
i PCA (oppgave 6): PCA er en lineær metode som bruker tallenes varians og
korrelasjon direkte, og en vilkårlig alfabetisk rangordning ville gitt PCA-en
meningsløs struktur å fange opp. Kostnaden er antall kolonner: 200 unike land
og 117 unike vekster gir til sammen 317 nye binære kolonner.

Bygger videre på oppgave 3 (crop1_outliers.csv), som la til *_log10 (log-
transformerte målinger, klare til skalering i 4b) og *_capped (flagg for
cappede celler, samme rolle som `imputed`). Disse kolonnene røres ikke her -
de følger bare med videre uendret. Year holdes numerisk (som i oppgave 1) og
encodes ikke. `imputed` og *_capped er flagg, ikke kategorier, og encodes
heller ikke.

Inn: food-bank/crop1_outliers.csv  ->  Ut: food-bank/crop1_encoded.csv
Kjør: python assignment1/src/4_encoding.py
"""
import pandas as pd

from felles import CAT, ENCODED, OUTLIERS, read

df = read(OUTLIERS)

counts = {col: df[col].nunique() for col in CAT}
cols_before = df.shape[1]
df = pd.get_dummies(df, columns=CAT, prefix=CAT, dtype=int)

df.to_csv(ENCODED, index=False)

print(f"One-hot-encodet {', '.join(CAT)} i {len(df):,} rader\n")
for col, n in counts.items():
    print(f"{col}: {n} unike verdier -> {n} nye binære kolonner ({col}_<verdi>)")
print(f"\nTotalt {sum(counts.values())} nye kolonner ({cols_before} kolonner før -> {df.shape[1]} etter)")

print(f"\nResultat: {ENCODED.relative_to(ENCODED.parents[1])} ({ENCODED.stat().st_size / 1e6:.1f} MB), "
      f"{df.shape[1]} kolonner")
