"""Oppgave 4a - encoding av kategoriske kolonner i crop1_outliers.csv.

Label encoding: hver unike verdi i Area og Item erstattes med et heltall (0, 1,
2, ...), tildelt i alfabetisk rekkefølge. Tallene har ingen betydning i seg selv
- de er bare en id - men gruppen har valgt label encoding fremfor one-hot for å
holde antall kolonner nede (one-hot ville gitt 317 nye kolonner: 200 land + 117
vekster). Tekstkolonnene erstattes (ikke beholdes ved siden av), siden koden og
teksten er samme informasjon og modellen uansett bare skal se tallene. Mappingen
mellom navn og kode skrives ut under kjøring til bruk i rapporten.

Merk til rapporten: label encoding innfører en kunstig rekkefølge (Albania=1 <
Brasil=20) som ikke finnes i dataene. Det bør nevnes som en bevisst avveining i
begrunnelsen, særlig for modeller som tolker tall som avstand (f.eks. lineær
regresjon, k-NN) - for trebaserte modeller (beslutningstrær, random forest,
gradient boosting) er dette mindre av et problem siden de kun splitter på
terskelverdier og ikke antar noen avstand mellom kategoriene.

Bygger videre på oppgave 3 (crop1_outliers.csv), som la til *_log10 (log-
transformerte målinger, klare til skalering i 4b) og *_capped (flagg for
cappede celler, samme rolle som `imputed`). Disse kolonnene røres ikke her -
de følger bare med videre uendret. Year holdes numerisk (som i oppgave 1) og
encodes ikke. `imputed` og *_capped er flagg, ikke kategorier, og encodes
heller ikke.

Inn: food-bank/crop1_outliers.csv  ->  Ut: food-bank/crop1_encoded.csv
Kjør: python assignment1/src/4_encoding.py
"""
from sklearn.preprocessing import LabelEncoder

from felles import CAT, ENCODED, OUTLIERS, read

df = read(OUTLIERS)

encoders = {}
for col in CAT:
    enc = LabelEncoder()
    df[col] = enc.fit_transform(df[col])
    encoders[col] = enc

df.to_csv(ENCODED, index=False)

print(f"Label-encodet {', '.join(CAT)} i {len(df):,} rader (tekst erstattet med kode)\n")
for col in CAT:
    enc = encoders[col]
    print(f"{col}: {len(enc.classes_)} unike verdier, kodet 0-{len(enc.classes_) - 1}")
    example = ", ".join(f"{name}={code}" for code, name in enumerate(enc.classes_[:5]))
    print(f"  eksempel: {example}, ...")

print("\nFørste rader:")
print(df[CAT + ["Year"]].head().to_string(index=False))

print(f"\nResultat: {ENCODED.relative_to(ENCODED.parents[1])} ({ENCODED.stat().st_size / 1e6:.1f} MB), "
      f"{df.shape[1]} kolonner")
