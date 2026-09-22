"""Oppgave 3 - håndtering av outliers (rapportens Tabell 6, Figur 3).

  C1  Detekter per vekst (Item), tre metoder til sammenligning:
      rå IQR, IQR på log10(x+1), og z-score (rå skala)
  C2  Avgjørelse: log10(x+1)-transformer alle tre målinger (log1p-varianten
      håndterer de 31 radene med produksjon = avling = 0), og cap
      (winsoriser) de gjenværende outlierne på log-skala med IQR per vekst

Outliers er stort sett ekte (tunghalede fordelinger, jf. oppgave 1b), så ingen
rader slettes her. Kolonnene *_log10 er log-transformert og klare til skalering
i oppgave 4; *_capped markerer cappede celler (samme mønster som `imputed`).
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
# (skjevhet), ikke feil i dataene -> vi transformerer fremfor å fjerne/cappe
# på rå skala, og capper bare det som fortsatt stikker seg ut etterpå.
section("3b  Avgjørelse: log10(x+1)-transformer, cap gjenværende outliers på log-skala")

LOG = {c: f"{c}_log10" for c in NUM}
for c in NUM:
    df[LOG[c]] = np.log10(df[c] + 1)

cap_stats = []
for c in NUM:
    lc = LOG[c]
    q1 = df.groupby("Item")[lc].transform(lambda g: g.quantile(0.25))
    q3 = df.groupby("Item")[lc].transform(lambda g: g.quantile(0.75))
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    flag = (df[lc] < lo) | (df[lc] > hi)
    df[lc] = df[lc].clip(lower=lo, upper=hi)
    df[f"{c}_capped"] = flag
    cap_stats.append({"kolonne": c, "cappet_celler": int(flag.sum()),
                       "cappet_%": round(flag.mean() * 100, 1)})

print(pd.DataFrame(cap_stats).to_string(index=False))
any_capped = df[[f"{c}_capped" for c in NUM]].any(axis=1)
print(f"\nRader med >=1 cappet verdi: {any_capped.sum():,} ({any_capped.mean() * 100:.1f} %)")
print(f"Rader/land/vekster uendret: {len(df):,} rader, {df['Area'].nunique()} land, {df['Item'].nunique()} vekster")

df.to_csv(OUTLIERS, index=False)

# ================================ Figur 3 ===================================
fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.8))
clean_raw = read(CLEAN)
for ax, c in zip(axes, NUM):
    before = np.log10(clean_raw[c] + 1)
    after = df[LOG[c]]
    ax.boxplot([before, after], widths=0.5, patch_artist=True, tick_labels=["before", "after"],
               boxprops=dict(facecolor="#cde2fb", edgecolor=BLUE, linewidth=1.2),
               medianprops=dict(color=BLUE, linewidth=2), whiskerprops=dict(color=BLUE),
               capprops=dict(color=BLUE),
               flierprops=dict(marker="o", markersize=2, markerfacecolor=INK2,
                               markeredgewidth=0, alpha=0.25))
    ax.set_title(FIG_LABEL[c], color=INK, fontsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8, which="major")
    ax.set_axisbelow(True)
fig.suptitle("log10(x+1), before vs. after capping remaining outliers", color=INK, fontsize=9)
fig.tight_layout()
fig.savefig(FIG / "fig3_outliers.png")
plt.close(fig)

section("Figur")
print(f"{FIG / 'fig3_outliers.png'}")
print(f"Resultat: {OUTLIERS.relative_to(OUTLIERS.parents[1])} ({OUTLIERS.stat().st_size / 1e6:.1f} MB), "
      f"{len(df):,} rader, {df.shape[1]} kolonner")
