"""Oppgave 4b - skalering (standardisering) av de numeriske kolonnene.

Standardisering (Z-score, x' = (x - gjennomsnitt) / std) er valgt fremfor
min-max. Oppgave 3 log10-transformerte og cappet de tre målingene, noe som
gjorde fordelingene tilnærmet symmetriske - da gir gjennomsnitt/std mer
mening enn min/maks, som fortsatt ville vært styrt av de ytterpunktene
(cappet, men ikke fjernet) som ligger igjen i dataene.

Det er *_log10-kolonnene fra oppgave 3 som skaleres (area_harvested_ha_log10,
production_tonnes_log10, yield_hg_per_ha_log10) - det er disse som faktisk
skal brukes videre, ikke de rå målingene. Area/Item (heltallskoder fra
oppgave 4a), Year, imputed og *_capped skaleres ikke.

Kjøres ETTER splitting (oppgave 5), ikke før, for å unngå datalekkasje:
StandardScaler fittes KUN på treningssettet (fit_transform), og de samme
parametrene (gjennomsnitt/std fra treningssettet) brukes til å transformere
testsettet (transform, ikke fit_transform). Å fitte på hele datasettet - eller
å fitte én egen scaler per sett - ville latt informasjon fra testsettet
påvirke skaleringen (evt. gitt de to settene ulik skala), og gitt et for
optimistisk bilde av hvor godt modellen generaliserer til usette data.

Inn: food-bank/crop1_train.csv, food-bank/crop1_test.csv (fra 5_data_splitting.py)
Ut:  food-bank/crop1_train_scaled.csv, food-bank/crop1_test_scaled.csv
Kjør: python assignment1/src/4b_scaling.py
"""
from sklearn.preprocessing import StandardScaler

from felles import DATA, NUM, TEST, TRAIN, read

LOG = [f"{c}_log10" for c in NUM]
SCALED = [f"{c}_scaled" for c in NUM]
TRAIN_SCALED = DATA / "crop1_train_scaled.csv"
TEST_SCALED = DATA / "crop1_test_scaled.csv"

train = read(TRAIN)
test = read(TEST)

scaler = StandardScaler()
train[SCALED] = scaler.fit_transform(train[LOG])
test[SCALED] = scaler.transform(test[LOG])

train.to_csv(TRAIN_SCALED, index=False)
test.to_csv(TEST_SCALED, index=False)

print(f"Standardisert {', '.join(LOG)}\n(fit på treningssettet, samme gjennomsnitt/std brukt til å transformere testsettet)\n")
print(f"Treningssett: {len(train):,} rader | Testsett: {len(test):,} rader\n")

print("Skaleringsparametre (fra treningssettet):")
for c, lc, mean, std in zip(NUM, LOG, scaler.mean_, scaler.scale_):
    print(f"  {lc}: gjennomsnitt={mean:.3f}, std={std:.3f}")

print("\nKontroll etter skalering (gjennomsnitt / std per kolonne):")
for c, sc in zip(NUM, SCALED):
    print(f"  {sc}: train {train[sc].mean():.3f} / {train[sc].std():.3f}   "
          f"test {test[sc].mean():.3f} / {test[sc].std():.3f}")

print(f"\nResultat: {TRAIN_SCALED.relative_to(TRAIN_SCALED.parents[1])} "
      f"({TRAIN_SCALED.stat().st_size / 1e6:.1f} MB), "
      f"{TEST_SCALED.relative_to(TEST_SCALED.parents[1])} ({TEST_SCALED.stat().st_size / 1e6:.1f} MB)")
