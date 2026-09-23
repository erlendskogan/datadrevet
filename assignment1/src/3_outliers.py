"""Oppgave 3 - håndtering av outliers (rapportens Tabell 6, Figur 3).

  C1  Detekter per vekst (Item), tre metoder til sammenligning:
      rå IQR, IQR på log10(x+1), og z-score (rå skala)
  C2  Avgjørelse: log10(x+1)-transformer alle tre målinger (log1p-varianten
      håndterer de 31 radene med produksjon = avling = 0). Ingenting fjernes
      eller cappes

Outliers er stort sett ekte (tunghalede fordelinger, jf. oppgave 1b), så ingen
rader slettes her. De som fortsatt flagges etter log-transformen er for det
meste små produsenter på nedsiden, og også de er ekte. Kolonnene *_log10 er
log-transformert og klare til skalering i oppgave 4.
Inn: food-bank/crop1_clean.csv  ->  Ut: food-bank/crop1_outliers.csv,
     assignment1/rapport/figurer/fig3_outliers.png
Kjør: python assignment1/src/3_outliers.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from felles import CLEAN, FIGURES as FIG, NUM, A, P, Y, read

FIG.mkdir(parents=True, exist_ok=True)
OUTLIERS = CLEAN.parent / "crop1_outliers.csv"

FIG_LABEL = {A: "Area harvested (ha)", P: "Production (tonnes)", Y: "Yield (hg/ha)"}
BLUE, INK, INK2, GRID = "#2a78d6", "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 160})


def section(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def iqr_flag(g, k=1.5):
    q1, q3 = g.quantile(0.25), g.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - k * iqr, q3 + k * iqr
    return (g < lo) | (g > hi)


def z_flag(g, k=3):
    m, s = g.mean(), g.std()
    if s == 0 or np.isnan(s):
        return pd.Series(False, index=g.index)
    return ((g - m) / s).abs() > k


df = read(CLEAN)

# ================================== 3a ======================================
# Steg 1 (tidligere) viste at fordelingene er skjeve (gjennomsnitt 2-49x
# medianen) -> en vanlig Z-score er mistenkelig. Steg 2 viste at IQR må
# regnes per vekst, ikke samlet. Her fullføres 3a: alle tre kolonner,
# tre metoder til sammenligning.
section("3a  Deteksjon: andel flagget per vekst, tre metoder (Tabell 6)")

rows = []
for c in NUM:
    raw = df.dropna(subset=[c]).groupby("Item")[c].transform(iqr_flag)
    log10 = np.log10(df[c] + 1).groupby(df["Item"]).transform(iqr_flag)
    z = df.dropna(subset=[c]).groupby("Item")[c].transform(z_flag)
    rows.append({"kolonne": c, "IQR (rå), %": round(raw.mean() * 100, 1),
                 "IQR (log10), %": round(log10.mean() * 100, 1),
                 "z-score (rå), %": round(z.mean() * 100, 1)})
print(pd.DataFrame(rows).to_string(index=False))

zero_mask = (df[P] == 0)
print(f"\nRader med produksjon = avling = 0 (avlingssvikt): {zero_mask.sum()} "
      f"(areal = 0: {(df[A] == 0).sum()})")
top = df.nlargest(3, Y)[["Area", "Item", "Year", Y]]
print(f"\nStørste avling nå (sopp fjernet i oppgave 2):\n{top.to_string(index=False)}")

# ================================== 3b ======================================
# At IQR på log10 flagger MYE færre (1.3-2.9 %) enn rå IQR (13-14 %/4.5 %)
# viser at det meste av det rå IQR flagger, skyldes formen på fordelingen
# (skjevhet), ikke feil i dataene -> vi transformerer. Det som fortsatt
# flagges etterpå, er for det meste små produsenter på nedsiden, og beholdes.
section("3b  Avgjørelse: log10(x+1)-transformer, behold gjenværende outliers")

LOG = {c: f"{c}_log10" for c in NUM}
for c in NUM:
    df[LOG[c]] = np.log10(df[c] + 1)

rest = []
for c in NUM:
    lc = LOG[c]
    q1 = df.groupby("Item")[lc].transform(lambda g: g.quantile(0.25))
    q3 = df.groupby("Item")[lc].transform(lambda g: g.quantile(0.75))
    iqr = q3 - q1
    low, high = df[lc] < q1 - 1.5 * iqr, df[lc] > q3 + 1.5 * iqr
    rest.append({"kolonne": c, "flagget": int((low | high).sum()), "nedside": int(low.sum()),
                 "overside": int(high.sum()), "median_rå_nedside": df.loc[low, c].median()})
print("Gjenværende outliers etter log10(x+1) (IQR per vekst), beholdes:")
print(pd.DataFrame(rest).to_string(index=False))
print(f"\nSkjevhet før -> etter log10(x+1): " + ", ".join(
    f"{c} {df[c].skew():.1f} -> {df[LOG[c]].skew():.2f}" for c in NUM))
print(f"Rader/land/vekster uendret: {len(df):,} rader, {df['Area'].nunique()} land, {df['Item'].nunique()} vekster")

df.to_csv(OUTLIERS, index=False)

# ================================ Figur 3 ===================================
# Samme måling på rå skala (øverst) og etter log10(x+1) (nederst), med andelen
# IQR per vekst flagger på hver skala (fra Tabell 6).
share = {r["kolonne"]: r for r in rows}
fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.2))
for j, c in enumerate(NUM):
    for i, (vals, key, label) in enumerate([(df[c], "IQR (rå), %", "raw"),
                                            (df[LOG[c]], "IQR (log10), %", "log10(x+1)")]):
        ax = axes[i, j]
        ax.hist(vals, bins=60, color=BLUE, edgecolor="none")
        ax.set_ylim(0, ax.get_ylim()[1] * 1.2)  # plass til teksten over søylene
        ax.set_title(f"{FIG_LABEL[c]}, {label}", color=INK, fontsize=8)
        ax.text(0.97, 0.9, f"{share[c][key]}% flagged", transform=ax.transAxes,
                ha="right", color=INK2, fontsize=8)
        ax.ticklabel_format(axis="x", style="sci", scilimits=(-3, 4))
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
    axes[0, j].set_ylabel("Rows" if j == 0 else "")
    axes[1, j].set_ylabel("Rows" if j == 0 else "")
fig.tight_layout()
fig.savefig(FIG / "fig3_outliers.png")
plt.close(fig)

section("Figur")
print(f"{FIG / 'fig3_outliers.png'}")
print(f"Resultat: {OUTLIERS.relative_to(OUTLIERS.parents[1])} ({OUTLIERS.stat().st_size / 1e6:.1f} MB), "
      f"{len(df):,} rader, {df.shape[1]} kolonner")
