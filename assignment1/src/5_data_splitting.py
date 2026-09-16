"""Oppgave 5 – train/test-splitting (rapportens avsnitt 5).

Tilfeldig 80-20-splitt på rader. Datasettet er paneldata (land x vekst x år);
begrunnelse for å likevel bruke tilfeldig splitt står i rapporten (5a).

Inn: food-bank/crop1_encoded.csv  ->  Ut: crop1_train.csv, crop1_test.csv
Kjør: python assignment1/src/5_datasplitting.py
"""
from sklearn.model_selection import train_test_split

from felles import CLEAN, DATA, ENCODED, read

TEST_SIZE = 0.2
SEED = 42

df = read(ENCODED)

train, test = train_test_split(df, test_size=TEST_SIZE, random_state=SEED)

train.to_csv(DATA / "crop1_train.csv", index=False)
test.to_csv(DATA / "crop1_test.csv", index=False)

print(f"Train: {len(train):,} rader ({len(train) / len(df):.0%})")
print(f"Test:  {len(test):,} rader ({len(test) / len(df):.0%})")