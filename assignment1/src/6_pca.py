"""Oppgave 6 (bonus) - PCA på de standardiserte målingene (rapportens Figur 4).

Følger stegene i forelesningen («PCA in a nutshell»): korrelerte data ->
sentrert (gjort i 4b) -> kovariansmatrise -> egenvektorer/egenverdier ->
velg m < d komponenter -> projiser -> ukorrelerte data. sklearn gjør steg 3-6.

Bare de tre *_scaled-kolonnene er med: Area/Item er one-hot-kodet (oppgave 4a)
og gir ingen meningsfull avstand å ta med i PCA, og Year er ikke skalert i 4b.
PCA fittes kun på treningssettet, som scaleren i 4b. m velges slik at minst
95 % av variansen beholdes. Area/Item rekonstrueres fra one-hot-kolonnene kun
for å identifisere radene i output-filene, ikke som input til PCA-en.

Inn: food-bank/crop1_train_scaled.csv, crop1_test_scaled.csv (fra 4b_scaling.py)
Ut:  food-bank/crop1_train_pca.csv, crop1_test_pca.csv,
     assignment1/rapport/figurer/fig4_pca.png
Kjør: python assignment1/src/6_pca.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression

from felles import DATA, FIGURES as FIG, KEYS, NUM, A, P, Y, read

SCALED = [f"{c}_scaled" for c in NUM]
FLAGS = ["imputed"] + [f"{c}_capped" for c in NUM]
SHORT = {A: "Area", P: "Production", Y: "Yield"}
THRESHOLD = 0.95
BLUE, INK, INK2, GRID = "#2a78d6", "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 160})


def section(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


train = read(DATA / "crop1_train_scaled.csv")
test = read(DATA / "crop1_test_scaled.csv")
X_train, X_test = train[SCALED].to_numpy(), test[SCALED].to_numpy()


def undummy(df, prefix):
    """Rekonstruerer én tekstkolonne fra one-hot-kolonnene <prefix>_<verdi>."""
    cols = [c for c in df.columns if c.startswith(f"{prefix}_")]
    return df[cols].idxmax(axis=1).str[len(prefix) + 1:]


for df in (train, test):
    df["Area"] = undummy(df, "Area")
    df["Item"] = undummy(df, "Item")

section("Steg 1-2  Korrelasjon (train) og sentrering fra 4b")
print(train[SCALED].corr().round(3).to_string())
print(f"Gjennomsnitt train: {np.round(X_train.mean(axis=0), 3)}")

section("Steg 3-5  Egenverdier, forklart varians og egenvektorer (fit på train)")
pca = PCA().fit(X_train)
names = [f"PC{i + 1}" for i in range(pca.n_components_)]
print(pd.DataFrame({"egenverdi": pca.explained_variance_.round(4),
                    "andel_%": (pca.explained_variance_ratio_ * 100).round(2),
                    "kumulativ_%": (pca.explained_variance_ratio_.cumsum() * 100).round(2)},
                   index=names).to_string())
print("\nEgenvektorer (loadings):")
print(pd.DataFrame(pca.components_.round(3), index=names, columns=SCALED).to_string())

m = int(np.argmax(pca.explained_variance_ratio_.cumsum() >= THRESHOLD)) + 1
print(f"\nm = {m} komponent(er) gir >= {THRESHOLD:.0%} forklart varians "
      f"(Kaiser, egenverdi > 1, ville gitt {int((pca.explained_variance_ > 1).sum())})")

section("Steg 6-7  Projeksjon og kontroll av at komponentene er ukorrelerte")
Z_train, Z_test = pca.transform(X_train)[:, :m], pca.transform(X_test)[:, :m]
print("Kovariansmatrise for komponentene (train):")
print(pd.DataFrame(np.cov(Z_train, rowvar=False).reshape(m, m).round(6),
                   index=names[:m], columns=names[:m]).to_string())

section(f"Effekt: rekonstruksjonsfeil med {m} av 3 dimensjoner")
for label, X, Z in [("train", X_train, Z_train), ("test", X_test, Z_test)]:
    X_hat = Z @ pca.components_[:m] + pca.mean_
    print(f"PCA ({m} komp.)   {label}: MSE {np.mean((X - X_hat) ** 2):.5f} "
          f"(andel av total varians {np.mean((X - X_hat) ** 2) / X.var(axis=0).mean():.2%})")

# Alternativ fra forelesningen: dropp kolonnen som er nær avhengig av de andre
# (avling ~ produksjon / areal) og mål tapet på samme måte
reg = LinearRegression().fit(X_train[:, :2], X_train[:, 2])
for label, X in [("train", X_train), ("test", X_test)]:
    X_hat = np.column_stack([X[:, :2], reg.predict(X[:, :2])])
    print(f"Dropp avling    {label}: MSE {np.mean((X - X_hat) ** 2):.5f} "
          f"(avling gjenskapt lineært fra areal og produksjon, R² {reg.score(X[:, :2], X[:, 2]):.4f})")

pcs = names[:m]
for df, Z, path in [(train, Z_train, DATA / "crop1_train_pca.csv"),
                    (test, Z_test, DATA / "crop1_test_pca.csv")]:
    out = pd.concat([df[KEYS + FLAGS].reset_index(drop=True), pd.DataFrame(Z, columns=pcs)], axis=1)
    out.to_csv(path, index=False)
    print(f"\nResultat: {path.relative_to(DATA.parent)}, {len(out):,} rader, kolonner: {', '.join(out.columns)}")

# ================================ Figur 4 ===================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw={"width_ratios": [1, 1.25]})
x = np.arange(1, pca.n_components_ + 1)
ax1.bar(x, pca.explained_variance_ratio_ * 100, color=BLUE, width=0.55)
ax1.plot(x, pca.explained_variance_ratio_.cumsum() * 100, color=INK, marker="o", markersize=3.5,
         linewidth=1.2, label="Cumulative")
ax1.axhline(THRESHOLD * 100, color=INK2, linestyle="--", linewidth=0.8)
ax1.text(3.35, THRESHOLD * 100 - 7, f"{THRESHOLD:.0%}", color=INK2, fontsize=8, ha="right")
for xi, v in zip(x, pca.explained_variance_ratio_ * 100):
    ax1.text(xi, v + 1.5, f"{v:.2f}%" if v < 1 else f"{v:.1f}%", ha="center", color=INK, fontsize=8)
ax1.set_xticks(x, names)
ax1.set_ylim(0, 108)
ax1.set_ylabel("Explained variance (%)")
ax1.legend(frameon=False, fontsize=8, loc="center right")
ax1.grid(axis="y", color=GRID, linewidth=0.8)
ax1.set_axisbelow(True)

sample = np.random.default_rng(42).choice(len(X_train), 5000, replace=False)
Z_all = pca.transform(X_train[sample])
ax2.scatter(Z_all[:, 0], Z_all[:, 1], s=2, color=BLUE, alpha=0.2, linewidths=0)
scale = np.abs(Z_all[:, :2]).max() * 0.6
for vec, c in zip(pca.components_[:2].T, NUM):
    ax2.annotate("", xy=vec * scale, xytext=(0, 0),
                 arrowprops=dict(arrowstyle="-|>", color=INK, linewidth=1.1))
    ax2.text(*(vec * scale * 1.35), SHORT[c], color=INK, fontsize=8, ha="center", va="center")
ax2.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
ax2.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
ax2.grid(color=GRID, linewidth=0.8)
ax2.set_axisbelow(True)
fig.tight_layout()
fig.savefig(FIG / "fig4_pca.png")
plt.close(fig)

section("Figur")
print(f"{FIG / 'fig4_pca.png'}  (spredningsplott: tilfeldig utvalg på 5 000 rader fra train)")
