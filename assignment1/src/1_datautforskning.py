"""Oppgave 1 – datautforskning av crop1_trimmed.csv (rapportens Tabell 2–4, Figur 1–2).

1a  Første rader, datatyper og oppsummerende statistikk
1b  Manglende verdier, tegn på outliers og unike verdier i kategoriske kolonner
    (metodesammenligning for outliers hører til oppgave 3)

Year behandles som numerisk (ordnet, like avstander).
Inn: food-bank/crop1_trimmed.csv  ->  Ut: assignment1/rapport/figurer/*.png
Kjør: python assignment1/src/1_datautforskning.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from felles import FIGURES as FIG, NUM, TRIMMED, A, P, Y, read

FIG.mkdir(parents=True, exist_ok=True)

LABEL = {A: "Areal (ha)", P: "Produksjon (tonn)", Y: "Avling (hg/ha)"}
# Figurene står i den engelske Overleaf-rapporten, så etikettene der er på engelsk
FIG_LABEL = {A: "Area harvested (ha)", P: "Production (tonnes)", Y: "Yield (hg/ha)"}
CAT = ["Area", "Item"]
BLUE, INK, INK2, GRID = "#2a78d6", "#0b0b0b", "#52514e", "#e6e5e1"

pd.set_option("display.width", 200)
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 160})


def fmt(v):
    return f"{v:,.0f}".replace(",", " ")


def section(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


df = read(TRIMMED)

# ================================== 1a ======================================
section(f"1a  Første 5 rader  (form: {df.shape[0]:,} rader x {df.shape[1]} kolonner)")
print(df.head().to_string(index=False))

section("1a+1b  Kolonneoversikt: datatype, manglende og unike verdier")
overview = pd.DataFrame({
    "datatype": df.dtypes.astype(str),
    "ikke-tomme": df.notna().sum(),
    "manglende": df.isna().sum(),
    "manglende_%": (df.isna().mean() * 100).round(1),
    "unike": df.nunique(),
})
print(overview.to_string())
empty = df[NUM].isna().all(axis=1).sum()
print(f"\nHelt tomme rader (alle tre målinger mangler): {empty:,} "
      f"| duplikater (Area, Item, Year): {df.duplicated(['Area', 'Item', 'Year']).sum()}")

section("1a  Oppsummerende statistikk (numeriske kolonner)")
desc = df[["Year"] + NUM].describe().T
print(desc.map(fmt).to_string())

# ================================== 1b ======================================
section("1b  Unike verdier i kategoriske kolonner")
for col in CAT:
    counts = df[col].value_counts()
    print(f"{col}: {counts.size} unike | rader per verdi: min {counts.min()} ({counts.idxmin()}), "
          f"median {counts.median():.0f}, maks {counts.max()} ({counts.idxmax()})")
    print(f"  vanligst: {', '.join(counts.index[:5])}")
nes = df.loc[df["Item"].str.contains(r"\bnes\b"), "Item"]
print(f"Sekkekategorier ('nes' = not elsewhere specified): {nes.nunique()} vekster, {len(nes):,} rader")
print(f"Year: {df['Year'].nunique()} verdier ({df['Year'].min()}–{df['Year'].max()}), "
      f"{df['Year'].value_counts().min():,}–{df['Year'].value_counts().max():,} rader per år")

section("1b  Tegn på outliers (metodesammenligning kommer i oppgave 3)")


def iqr_flags(s):
    q1, q3 = s.quantile([0.25, 0.75])
    return (s < q1 - 1.5 * (q3 - q1)) | (s > q3 + 1.5 * (q3 - q1))


rows = []
for c in NUM:
    s = df[c].dropna()
    per_item = df.dropna(subset=[c]).groupby("Item")[c].transform(iqr_flags)
    rows.append({"kolonne": c, "median": fmt(s.median()), "gjennomsnitt": fmt(s.mean()),
                 "Q3": fmt(s.quantile(0.75)), "maks": fmt(s.max()),
                 "maks/Q3": f"{s.max() / s.quantile(0.75):,.0f}x".replace(",", " "),
                 "skjevhet": round(s.skew(), 1), "nuller": int((s == 0).sum()),
                 "IQR-flagget per vekst_%": round(per_item.mean() * 100, 1)})
print(pd.DataFrame(rows).to_string(index=False))
for c in NUM:
    top = df.nlargest(3, c)[["Area", "Item", "Year", c]]
    print(f"\nStørste {c}:\n{top.to_string(index=False)}")

# ================================ Figurer ===================================
# Figur 1: andel manglende per numerisk måling
miss = (df[NUM].isna().mean() * 100)
fig, ax = plt.subplots(figsize=(5.2, 1.9))
y = np.arange(len(NUM))[::-1]
ax.barh(y, miss.values, color=BLUE, height=0.55)
for yi, v, n in zip(y, miss.values, df[NUM].isna().sum()):
    ax.text(v + 0.15, yi, f"{v:.1f}%  ({n:,})", va="center", color=INK, fontsize=8.5)
ax.set_yticks(y, [FIG_LABEL[c] for c in NUM], color=INK)
ax.set_xlim(0, miss.max() * 1.45)
ax.set_xlabel("Share of missing values (%)")
ax.grid(axis="x", color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig(FIG / "fig1_manglende.png")
plt.close(fig)

# Figur 2: boksplott på log-skala, ett panel per måling (ulike enheter -> egne akser).
# Kvartiler og værhår (1,5·IQR) beregnes på rå verdier; nuller kan ikke vises på log-skala.
fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.8))
zeros = {}
for ax, c in zip(axes, NUM):
    s = df[c].dropna()
    zeros[c] = int((s == 0).sum())
    ax.boxplot(s[s > 0], widths=0.5, patch_artist=True,
               boxprops=dict(facecolor="#cde2fb", edgecolor=BLUE, linewidth=1.2),
               medianprops=dict(color=BLUE, linewidth=2), whiskerprops=dict(color=BLUE),
               capprops=dict(color=BLUE),
               flierprops=dict(marker="o", markersize=2, markerfacecolor=INK2,
                               markeredgewidth=0, alpha=0.25))
    ax.set_yscale("log")
    ax.set_title(FIG_LABEL[c], color=INK, fontsize=9)
    ax.set_xticks([])
    ax.grid(axis="y", color=GRID, linewidth=0.8, which="major")
    ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(FIG / "fig2_boksplott_log.png")
plt.close(fig)

section("Figurer")
print(f"{FIG / 'fig1_manglende.png'}")
print(f"{FIG / 'fig2_boksplott_log.png'}  (utelatt nuller: "
      + ", ".join(f"{LABEL[c]} {fmt(n)}" for c, n in zeros.items()) + ")")
