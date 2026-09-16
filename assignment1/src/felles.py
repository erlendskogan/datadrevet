"""Felles stier, kolonnenavn og hjelpefunksjoner for skriptene i assignment1/src.

Nye skript for oppgave 3–6 kan importere herfra, f.eks.:
    from felles import CLEAN, NUM, A, P, Y
"""
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "food-bank"              # ligger utenfor git (se .gitignore)
RAW = DATA / "crop1.csv"               # originalen fra Blackboard
TRIMMED = DATA / "crop1_trimmed.csv"   # lages av 0_tilpass_datasett.py
CLEAN = DATA / "crop1_clean.csv"       # lages av 2_manglende_verdier.py
OUTLIERS = DATA / "crop1_outliers.csv"  # lages av 3_outliers.py
ENCODED = DATA / "crop1_encoded.csv"   # lages av 4_encoding.py
FIGURES = REPO / "assignment1" / "rapport" / "figurer"

A, P, Y = "area_harvested_ha", "production_tonnes", "yield_hg_per_ha"
NUM = [A, P, Y]
KEYS = ["Area", "Item", "Year"]
CAT = ["Area", "Item"]


def read(path):
    """Leser en CSV og sier hva som må kjøres først hvis filen mangler."""
    if not path.exists():
        hint = {RAW: "Legg crop1.csv fra Blackboard i food-bank/.",
                TRIMMED: "Kjør 0_tilpass_datasett.py først.",
                CLEAN: "Kjør 0_tilpass_datasett.py og 2_manglende_verdier.py først.",
                OUTLIERS: "Kjør 0_tilpass_datasett.py, 2_manglende_verdier.py og 3_outliers.py først.",
                ENCODED: "Kjør 0_tilpass_datasett.py, 2_manglende_verdier.py, 3_outliers.py og 4_encoding.py først."}
        raise SystemExit(f"Fant ikke {path}. {hint.get(path, '')}")
    return pd.read_csv(path)


class StepLog:
    """Logger rader, land og vekster etter hvert steg. Berørt = rader fjernet siden forrige steg."""

    def __init__(self):
        self.rows = []

    def __call__(self, name, df, affected=None):
        if affected is None and self.rows:
            affected = self.rows[-1][2] - len(df)
        self.rows.append((name, "–" if affected is None else int(affected), len(df),
                          df["Area"].nunique(), df["Item"].nunique(),
                          int(df[NUM].isna().any(axis=1).sum())))
        return df

    def print(self):
        cols = ["steg", "berørt", "rader", "land", "vekster", "rader_med_NaN"]
        print(pd.DataFrame(self.rows, columns=cols).to_string(index=False))
