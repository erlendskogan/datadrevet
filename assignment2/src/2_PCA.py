"""Oppgave 2 - PCA på gråtone-heatmaps (egne «eigen-heatmaps»).

Følger stegene i oppgaveteksten, implementert for hånd med numpy:
1. bildene -> matrise X (én rad per bilde, én kolonne per piksel)
2. kovariansmatrise  3. egenverdier/egenvektorer  4. sorter synkende
5. velg topp k egenvektorer  6. projiser på underrommet
Deretter rekonstruksjon, varians-kurve, bildesammenligning for ulike k og MSE.
Til slutt en kontroll mot sklearn.decomposition.PCA.

Data: de 40 deltakerne på samme lysbilde (hm20). Alle har identisk bakgrunn,
så variansen mellom bildene kommer kun fra hvor deltakerne så. Bildene
nedskaleres fra 960x540 til 96x54 (5 184 piksler), ellers ville
kovariansmatrisen fått ~2,7e11 elementer.

Inn: heatmap-performance/hm20/Heat Map (0..39).png
Ut:  assignment2/rapport/figurer/pca_*.png
Kjør: python assignment2/src/2_PCA.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SLIDE = ROOT / "heatmap-performance" / "hm20"
FIG = ROOT / "assignment2" / "rapport" / "figurer"
FIG.mkdir(parents=True, exist_ok=True)

SIZE = (96, 54)                   # (bredde, høyde) etter nedskalering
K_VALUES = [1, 2, 5, 10, 20, 39]  # 40 bilder -> maks 39 komponenter med varians > 0
THRESHOLD = 0.90                  # «optimal» k: minste k med >= 90 % forklart varians
SHOW = [0, 7, 23]                 # bildene som vises i sammenligningsfiguren

BLUE, INK, INK2, GRID = "#2a78d6", "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 160})


def section(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def load_images(folder, size):
    """Leser Heat Map (0..n).png i numerisk rekkefølge som gråtone, skalert til [0, 1]."""
    paths = sorted(folder.glob("Heat Map (*).png"), key=lambda p: int(p.stem.split("(")[1][:-1]))
    imgs = [np.asarray(Image.open(p).convert("L").resize(size, Image.LANCZOS), dtype=np.float64) / 255
            for p in paths]
    return np.stack(imgs), [p.name for p in paths]


def pca_fit(X):
    """PCA fra bunnen av. Returnerer gjennomsnitt, egenverdier og egenvektorer (kolonner),
    sortert synkende etter egenverdi."""
    mean = X.mean(axis=0)
    Xc = X - mean                                     # sentrering
    cov = Xc.T @ Xc / (X.shape[0] - 1)                # steg 2: kovariansmatrise (d x d)
    eigvals, eigvecs = np.linalg.eigh(cov)            # steg 3: eigh fordi cov er symmetrisk
    order = np.argsort(eigvals)[::-1]                 # steg 4: sorter synkende
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]
    eigvals = np.clip(eigvals, 0, None)               # små negative verdier er avrundingsstøy
    return mean, eigvals, eigvecs


def pca_project(X, mean, eigvecs, k):
    """Steg 5-6: velg topp k egenvektorer og projiser (n x d) -> (n x k)."""
    return (X - mean) @ eigvecs[:, :k]


def pca_reconstruct(Z, mean, eigvecs):
    """Tilbake til pikselrommet: (n x k) -> (n x d)."""
    k = Z.shape[1]
    return Z @ eigvecs[:, :k].T + mean


# =========================== Steg 1: datamatrise ============================
section("Steg 1  Bilder -> matrise")
images, names = load_images(SLIDE, SIZE)
n, h, w = images.shape
X = images.reshape(n, h * w)
print(f"{n} bilder fra {SLIDE.relative_to(ROOT)}, {w}x{h} px -> X har form {X.shape}")
print(f"Pikselverdier i [{X.min():.2f}, {X.max():.2f}] (normalisert fra 0-255)")

# ====================== Steg 2-4: kovarians og egenpar ======================
section("Steg 2-4  Kovariansmatrise, egenverdier og sortering")
mean, eigvals, eigvecs = pca_fit(X)
ratio = eigvals / eigvals.sum()
cum = ratio.cumsum()
print(f"Kovariansmatrise: {h * w} x {h * w}")
print(f"Egenverdier > 1e-10: {(eigvals > 1e-10).sum()} (maks n-1 = {n - 1}, "
      "resten er null fordi 40 bilder bare spenner et 39-dim. underrom)")
print(f"\n{'PC':>4} {'egenverdi':>11} {'andel %':>8} {'kumulativ %':>12}")
for i in range(15):
    print(f"{i + 1:>4} {eigvals[i]:>11.4f} {ratio[i] * 100:>8.2f} {cum[i] * 100:>12.2f}")

k_opt = int(np.argmax(cum >= THRESHOLD)) + 1
print(f"\nMinste k med >= {THRESHOLD:.0%} forklart varians: k = {k_opt}")
for t in (0.5, 0.8, 0.95, 0.99):
    print(f"  >= {t:.0%}: k = {int(np.argmax(cum >= t)) + 1}")

# ================= Steg 5-6 + rekonstruksjon, MSE for alle k ================
section("Steg 5-6  Projeksjon, rekonstruksjon og MSE")
d = h * w
print(f"{'k':>3} {'forklart %':>11} {'MSE':>10} {'PSNR dB':>8} {'lagrede tall':>13} {'kompresjon':>11}")
mse_all = []
for k in range(1, n):
    Z = pca_project(X, mean, eigvecs, k)
    X_hat = pca_reconstruct(Z, mean, eigvecs)
    mse = np.mean((X - X_hat) ** 2)
    mse_all.append(mse)
    # lagring: n*k koeffisienter + k egenvektorer à d + gjennomsnittsbildet
    stored = n * k + k * d + d
    if k in K_VALUES or k == k_opt:
        print(f"{k:>3} {cum[k - 1] * 100:>11.2f} {mse:>10.6f} {10 * np.log10(1 / mse):>8.2f} "
              f"{stored:>13,} {n * d / stored:>10.2f}x")
mse_all = np.array(mse_all)
print(f"(original: {n * d:,} tall)")
# Kontroll: MSE = summen av de forkastede egenverdiene / d  (skalert med (n-1)/n)
k = k_opt
print(f"\nKontroll k={k}: MSE {mse_all[k - 1]:.6f} = sum forkastede egenverdier * (n-1)/(n*d) "
      f"= {eigvals[k:].sum() * (n - 1) / (n * d):.6f}")

# =================== Generalisering: nye bilder (holdout) ===================
section("Generalisering: fit på 32 deltakere, rekonstruer 8 nye")
rng = np.random.default_rng(42)
idx = rng.permutation(n)
tr, te = idx[:32], idx[32:]
m_tr, ev_tr, V_tr = pca_fit(X[tr])
print(f"{'k':>3} {'MSE train':>10} {'MSE test':>10}")
for k in [1, 5, 10, 20, 31]:
    err = []
    for part in (tr, te):
        X_hat = pca_reconstruct(pca_project(X[part], m_tr, V_tr, k), m_tr, V_tr)
        err.append(np.mean((X[part] - X_hat) ** 2))
    print(f"{k:>3} {err[0]:>10.6f} {err[1]:>10.6f}")
print(f"Bare gjennomsnittsbildet (k=0): test MSE {np.mean((X[te] - m_tr) ** 2):.6f}")

# ======================= Kontroll mot sklearn =========================
section("Kontroll mot sklearn.decomposition.PCA")
try:
    from sklearn.decomposition import PCA
    sk = PCA(n_components=n - 1).fit(X)
    print(f"Maks avvik forklart varians-andel: {np.abs(sk.explained_variance_ratio_ - ratio[:n - 1]).max():.2e}")
    # egenvektorer er bare bestemt opp til fortegn
    dots = np.abs(np.sum(sk.components_[:10] * eigvecs[:, :10].T, axis=1))
    print(f"|cos| mellom de 10 første egenvektorene: min {dots.min():.6f}")
except ImportError:
    print("sklearn ikke installert, hopper over")

# ================================ Figurer ===================================
# 1) Forklart varians
fig, ax = plt.subplots(figsize=(6.4, 3.0))
x = np.arange(1, n)
ax.bar(x, ratio[:n - 1] * 100, color=BLUE, width=0.7, label="Per komponent")
ax.plot(x, cum[:n - 1] * 100, color=INK, marker="o", markersize=2.5, linewidth=1.1, label="Kumulativ")
ax.axhline(THRESHOLD * 100, color=INK2, linestyle="--", linewidth=0.8)
ax.axvline(k_opt, color=INK2, linestyle=":", linewidth=0.8)
ax.text(k_opt + 0.5, 30, f"k = {k_opt}\n({cum[k_opt - 1]:.0%})", color=INK2, fontsize=8)
ax.set_xlabel("Antall hovedkomponenter k")
ax.set_ylabel("Forklart varians (%)")
ax.set_ylim(0, 105)
ax.legend(frameon=False, fontsize=8, loc="center right")
ax.grid(axis="y", color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(FIG / "pca_forklart_varians.png")
plt.close(fig)

# 2) Gjennomsnittsbilde + de første egenvektorene («eigen-heatmaps»)
n_eig = 7
fig, axes = plt.subplots(2, 4, figsize=(8, 2.6))
axes = axes.ravel()
axes[0].imshow(mean.reshape(h, w), cmap="gray", vmin=0, vmax=1)
axes[0].set_title("Gjennomsnitt", fontsize=8)
for i in range(n_eig):
    v = eigvecs[:, i].reshape(h, w)
    lim = np.abs(v).max()
    axes[i + 1].imshow(v, cmap="RdBu_r", vmin=-lim, vmax=lim)
    axes[i + 1].set_title(f"PC{i + 1} ({ratio[i]:.1%})", fontsize=8)
for a in axes:
    a.axis("off")
fig.tight_layout()
fig.savefig(FIG / "pca_egenvektorer.png")
plt.close(fig)

# 3) Original ved siden av rekonstruksjoner for ulike k
ks = sorted(set(K_VALUES + [k_opt]))
fig, axes = plt.subplots(len(SHOW), len(ks) + 1, figsize=(1.45 * (len(ks) + 1), 0.95 * len(SHOW) + 0.4))
for r, i in enumerate(SHOW):
    axes[r, 0].imshow(images[i], cmap="gray", vmin=0, vmax=1)
    axes[r, 0].set_ylabel(names[i].replace(".png", ""), fontsize=7)
    for c, k in enumerate(ks, start=1):
        X_hat = pca_reconstruct(pca_project(X[i:i + 1], mean, eigvecs, k), mean, eigvecs)
        axes[r, c].imshow(np.clip(X_hat.reshape(h, w), 0, 1), cmap="gray", vmin=0, vmax=1)
        if r == 0:
            axes[r, c].set_title(f"k = {k}", fontsize=8)
        axes[r, c].set_xlabel(f"MSE {np.mean((X[i] - X_hat) ** 2):.4f}", fontsize=6)
axes[0, 0].set_title("Original", fontsize=8)
for a in axes.ravel():
    a.set_xticks([])
    a.set_yticks([])
    a.spines[:].set_visible(False)
fig.tight_layout()
fig.savefig(FIG / "pca_rekonstruksjon.png")
plt.close(fig)

# 4) MSE mot k (kompresjon vs. feil)
fig, ax = plt.subplots(figsize=(6.4, 2.8))
ax.plot(np.arange(1, n), mse_all, color=BLUE, marker="o", markersize=2.5, linewidth=1.2)
ax.axvline(k_opt, color=INK2, linestyle=":", linewidth=0.8)
ax.set_xlabel("Antall hovedkomponenter k")
ax.set_ylabel("MSE (piksel i [0, 1])")
ax.grid(color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(FIG / "pca_mse.png")
plt.close(fig)

print(f"\nFigurer lagret i {FIG.relative_to(ROOT)}/")
