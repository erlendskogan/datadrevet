"""Oppgave 3 - HOG-features (Histogram of Oriented Gradients).

Deloppgavene:
1. beregn HOG med skimage.feature.hog
2. bruk det på minst tre bilder, både enkle og komplekse scener
3. vis original, gradientbilde og HOG-bilde
4. sammenlign deskriptorene og drøft cellestørrelse, blokkstørrelse og bins

Bilder: HOG kan bruke hvilke bilder som helst (se assignment2/README.md), så vi
blander ett heatmap fra datasettet med tre standardbilder fra skimage.data:
  horse     - svart silhuett på hvit bakgrunn (enkel scene)
  heatmap   - hm20, deltaker 0: lysbilde med tekst og fiksasjonsflekker
  camera    - fotografi i gråtone (middels)
  astronaut - fargefoto med mange objekter og teksturer (kompleks scene)
Alle beskjæres til kvadrat og skaleres til 256x256, slik at deskriptorene får
samme lengde og kan sammenlignes direkte. Heatmapet beskjæres til venstre
540x540, der teksten og fiksasjonene ligger, og hesten til høyre kvadrat.

Vinkelkonvensjon i utskrift og figurer: 0 grader = horisontal gradient
(loddrett kant), 90 grader = vertikal gradient (vannrett kant).

Inn: heatmap-performance/hm20/, hm30/ og skimage.data
Ut:  assignment2/rapport/figurer/hog_*.png
Kjør: python assignment2/src/3_HOG.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import hsv_to_rgb
from PIL import Image
from skimage import color, data, exposure, transform
from skimage.feature import hog

ROOT = Path(__file__).resolve().parents[2]
HEAT = ROOT / "heatmap-performance"
FIG = ROOT / "assignment2" / "rapport" / "figurer"
FIG.mkdir(parents=True, exist_ok=True)

SIZE = 256
DEFAULT = dict(orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm="L2-Hys")
FLAT = 0.01          # celler med gjennomsnittlig |G| under dette regnes som «flate»

BLUE, INK, INK2, GRID = "#2a78d6", "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 160})


def section(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def prepare(img, box=None):
    """RGB/gråtone -> gråtone i [0, 1], beskåret til kvadrat og skalert til SIZE x SIZE."""
    img = np.asarray(img)
    if img.ndim == 3:
        img = color.rgb2gray(img[..., :3])
    img = img.astype(np.float64)
    if img.max() > 1:
        img /= 255
    if box is None:                                   # midtre kvadrat
        h, w = img.shape
        s = min(h, w)
        box = ((h - s) // 2, (w - s) // 2, s)
    r, c, s = box
    img = img[r:r + s, c:c + s]
    return transform.resize(img, (SIZE, SIZE), anti_aliasing=True)


def heatmap(slide, participant):
    return np.asarray(Image.open(HEAT / f"hm{slide}" / f"Heat Map ({participant}).png").convert("RGB"))


def gradients(img):
    """Sentral differanse [-1, 0, 1] som i HOG. Returnerer |G| og vinkel i [0, 180)."""
    gx = np.zeros_like(img)
    gy = np.zeros_like(img)
    gx[:, 1:-1] = img[:, 2:] - img[:, :-2]
    gy[1:-1, :] = img[:-2, :] - img[2:, :]           # opp minus ned -> y peker opp
    mag = np.hypot(gx, gy)
    ang = np.rad2deg(np.arctan2(gy, gx)) % 180
    return mag, ang


def orientation_hist(mag, ang, bins=9):
    """Gradientstyrke summert per retningsbin over hele bildet, normalisert til sum 1."""
    h, _ = np.histogram(ang, bins=bins, range=(0, 180), weights=mag)
    return h / h.sum()


def cosine(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def hog_vec(img, **kw):
    return hog(img, **{**DEFAULT, **kw})


# ================================ Bildene ===================================
IMAGES = {
    "horse": prepare(1 - data.horse().astype(float), box=(0, 72, 328)),  # bool, True = bakgrunn; høyre kvadrat har hele hesten
    "heatmap": prepare(heatmap(20, 0), box=(0, 0, 540)),
    "camera": prepare(data.camera()),
    "astronaut": prepare(data.astronaut()),
}
LABEL = {"horse": "Horse (simple)", "heatmap": "Heatmap hm20/0", "camera": "Camera", "astronaut": "Astronaut (complex)"}
# Ekstra heatmaps til likhetsanalysen: to andre deltakere på samme lysbilde og ett annet lysbilde
EXTRA = {
    "hm20/7": prepare(heatmap(20, 7), box=(0, 0, 540)),
    "hm20/23": prepare(heatmap(20, 23), box=(0, 0, 540)),
    "hm30/0": prepare(heatmap(30, 0), box=(0, 0, 540)),
}

# ======================= Deloppgave 1-3: HOG per bilde ======================
section("Deloppgave 1-3  HOG med standardparametre (9 bins, 8x8 celler, 2x2 blokker, L2-Hys)")
results = {}
print(f"{'bilde':<11} {'lengde':>7} {'snitt |G|':>10} {'flate celler':>13} {'entropi bit':>12} "
      f"{'dominant':>9} {'0/90 grader %':>14}")
for name, img in IMAGES.items():
    features, hog_img = hog(img, visualize=True, **DEFAULT)
    mag, ang = gradients(img)
    c = DEFAULT["pixels_per_cell"][0]
    cell_energy = mag.reshape(SIZE // c, c, SIZE // c, c).mean(axis=(1, 3))
    oh = orientation_hist(mag, ang)
    entropy = -np.sum(oh[oh > 0] * np.log2(oh[oh > 0]))
    # andel gradientenergi innenfor +-10 grader fra 0/180 og 90 grader (loddrette/vannrette kanter)
    near_axis = np.sum(mag[(ang < 10) | (ang >= 170) | ((ang >= 80) & (ang < 100))]) / mag.sum()
    results[name] = dict(features=features, hog_img=hog_img, mag=mag, ang=ang, oh=oh)
    print(f"{name:<11} {features.size:>7,} {mag.mean():>10.4f} {np.mean(cell_energy < FLAT):>12.0%} "
          f"{entropy:>12.2f} {np.argmax(oh) * 20:>6}-{np.argmax(oh) * 20 + 20:<3}"
          f"{near_axis * 100:>13.1f}")
print(f"(maks entropi med 9 bins: log2(9) = {np.log2(9):.2f} bit, jevn fordeling gir 2/9 = 22 % nær 0/90)")

section("Global retningsfordeling (andel av gradientenergi per 20-graders bin)")
print(f"{'bilde':<11} " + " ".join(f"{b * 20:>3}-{b * 20 + 20:<3}" for b in range(9)))
for name, r in results.items():
    print(f"{name:<11} " + " ".join(f"{v * 100:>6.1f}%" for v in r["oh"]))

# ======================= Deloppgave 4: sammenligning ========================
section("Deloppgave 4  Cosinuslikhet mellom deskriptorene (standardparametre)")
vecs = {n: results[n]["features"] for n in IMAGES}
vecs.update({n: hog_vec(img) for n, img in EXTRA.items()})
names = list(vecs)
S = np.array([[cosine(vecs[a], vecs[b]) for b in names] for a in names])
print(" " * 11 + " ".join(f"{n:>9}" for n in names))
for n, row in zip(names, S):
    print(f"{n:<11}" + " ".join(f"{v:>9.3f}" for v in row))
same = [S[names.index("heatmap"), names.index(o)] for o in ("hm20/7", "hm20/23")]
print(f"\nSamme lysbilde, ulike deltakere: {np.mean(same):.3f}. "
      f"Annet lysbilde: {S[names.index('heatmap'), names.index('hm30/0')]:.3f}. "
      f"Snitt mellom de fire ulike motivene: "
      f"{np.mean([S[i, j] for i in range(4) for j in range(4) if i < j]):.3f}")

# ================== Deloppgave 4: parametre, én om gangen ===================
# Robusthet: cosinuslikhet mellom deskriptoren for bildet og en endret versjon,
# snitt over de fire bildene. Høyere = mer robust. «Ulike bilder» er snitt-likheten
# mellom de fire motivene; lavere = deskriptoren skiller bedre.
# Skygge: venstre halvdel får 10 % lysstyrke, med en myk overgang (6 px) rundt midten
# så overgangen ikke lager en ny skarp kant.
shadow = np.tile(0.1 + 0.9 / (1 + np.exp(-(np.arange(SIZE) - SIZE / 2) / 6)), (SIZE, 1))


def variants(img):
    return {
        "shift": transform.warp(img, transform.AffineTransform(translation=(4, 3)), mode="reflect"),
        "rot": transform.rotate(img, 10, mode="reflect"),
        "light": img * shadow,
    }


VARIANTS = {n: variants(img) for n, img in IMAGES.items()}


def evaluate(**kw):
    base = {n: hog_vec(img, **kw) for n, img in IMAGES.items()}
    rob = {k: np.mean([cosine(base[n], hog_vec(VARIANTS[n][k], **kw)) for n in IMAGES])
           for k in ("shift", "rot", "light")}
    ns = list(IMAGES)
    diff = np.mean([cosine(base[a], base[b]) for i, a in enumerate(ns) for b in ns[i + 1:]])
    return base["camera"].size, rob, diff


SWEEP = ([("pixels_per_cell", (p, p)) for p in (4, 8, 16, 32)]
         + [("cells_per_block", (b, b)) for b in (1, 2, 3, 4)]
         + [("orientations", o) for o in (3, 6, 9, 12, 18)]
         + [("block_norm", n) for n in ("L1", "L2", "L2-Hys")])
section("Deloppgave 4  Parametre varieres én om gangen rundt standardoppsettet")
print("shift = flyttet (4, 3) px, rot = rotert 10 grader, light = venstre halvdel i skygge (10 %)")
print(f"{'parameter':<17} {'verdi':>8} {'lengde':>8} {'shift':>7} {'rot':>7} {'light':>7} {'ulike':>7}")
for key, val in SWEEP:
    length, rob, diff = evaluate(**{key: val})
    v = val[0] if isinstance(val, tuple) else val
    print(f"{key:<17} {str(v):>8} {length:>8,} {rob['shift']:>7.3f} {rob['rot']:>7.3f} "
          f"{rob['light']:>7.3f} {diff:>7.3f}")


def raw_cells(img, c=8, bins=9):
    """Cellehistogrammer uten noen normalisering, bygget direkte fra gradientene."""
    mag, ang = gradients(img)
    b = np.minimum((ang / (180 / bins)).astype(int), bins - 1)
    cell = np.arange(SIZE) // c
    idx = (cell[:, None] * (SIZE // c) + cell[None, :]) * bins + b
    return np.bincount(idx.ravel(), weights=mag.ravel(), minlength=(SIZE // c) ** 2 * bins)


# Uten blokknormalisering: hvor mye gjør normaliseringen for robustheten mot skygge?
raw_light = np.mean([cosine(raw_cells(img), raw_cells(img * shadow)) for img in IMAGES.values()])
print(f"\nUten normalisering (rå cellehistogrammer), light-likhet: {raw_light:.3f}")

# ================================ Figurer ===================================
# 1) Oversikt: original, |G|, retning og HOG for hvert bilde
fig, axes = plt.subplots(len(IMAGES), 4, figsize=(7.2, 1.85 * len(IMAGES)))
for r, (name, img) in enumerate(IMAGES.items()):
    res = results[name]
    m = res["mag"]
    mn = np.clip(m / np.percentile(m, 99), 0, 1)
    hsv = np.stack([res["ang"] / 180, np.ones_like(m), mn], axis=-1)
    hog_show = exposure.rescale_intensity(res["hog_img"], in_range=(0, res["hog_img"].max() / 2))
    panels = [(img, "gray"), (mn, "gray"), (hsv_to_rgb(hsv), None), (hog_show, "gray")]
    for c, (im, cmap) in enumerate(panels):
        axes[r, c].imshow(im, cmap=cmap, vmin=0 if cmap else None, vmax=1 if cmap else None)
        axes[r, c].set_xticks([])
        axes[r, c].set_yticks([])
        axes[r, c].spines[:].set_visible(False)
    axes[r, 0].set_ylabel(LABEL[name], fontsize=8)
for c, t in enumerate(["Original", "Gradient magnitude |G|", "Gradient direction (hue)", "HOG (9 bins, 8×8)"]):
    axes[0, c].set_title(t, fontsize=8)
fig.tight_layout()
fig.savefig(FIG / "hog_oversikt.png")
plt.close(fig)

# 2) Global retningsfordeling + likhetsmatrise
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw=dict(width_ratios=[1.25, 1]))
x = np.arange(9)
wbar = 0.2
cols = ["#0b0b0b", "#2a78d6", "#e3862b", "#6aa84f"]
for i, (name, r) in enumerate(results.items()):
    a1.bar(x + (i - 1.5) * wbar, r["oh"] * 100, width=wbar, color=cols[i], label=LABEL[name])
a1.set_xticks(x, [f"{b * 20}–{b * 20 + 20}" for b in x], rotation=45, fontsize=7)
a1.set_xlabel("Gradient orientation (degrees)")
a1.set_ylabel("Share of gradient energy (%)")
a1.axhline(100 / 9, color=INK2, linestyle="--", linewidth=0.8)
a1.legend(frameon=False, fontsize=7)
a1.grid(axis="y", color=GRID, linewidth=0.8)
a1.set_axisbelow(True)
short = ["horse", "heatmap", "camera", "astro.", "hm20/7", "hm20/23", "hm30/0"]
im = a2.imshow(S, cmap="Blues", vmin=0, vmax=1)
a2.set_xticks(range(len(names)), short, rotation=45, fontsize=7)
a2.set_yticks(range(len(names)), short, fontsize=7)
for i in range(len(names)):
    for j in range(len(names)):
        a2.text(j, i, f"{S[i, j]:.2f}", ha="center", va="center", fontsize=6,
                color="white" if S[i, j] > 0.6 else INK)
a2.set_title("Cosine similarity of HOG descriptors", fontsize=8)
a2.spines[:].set_visible(False)
fig.tight_layout()
fig.savefig(FIG / "hog_sammenligning.png")
plt.close(fig)

# 3) Parametre visuelt: cellestørrelse og bins på camera
img = IMAGES["camera"]
rows = [("pixels_per_cell", [(p, p) for p in (4, 8, 16, 32)], lambda v: f"cell {v[0]}×{v[0]}"),
        ("orientations", [3, 6, 9, 18], lambda v: f"{v} bins")]
fig, axes = plt.subplots(2, 4, figsize=(7.2, 4.1))
for r, (key, vals, fmt) in enumerate(rows):
    for c, v in enumerate(vals):
        _, hi = hog(img, visualize=True, **{**DEFAULT, key: v})
        axes[r, c].imshow(exposure.rescale_intensity(hi, in_range=(0, hi.max() / 2)), cmap="gray")
        axes[r, c].set_title(fmt(v), fontsize=8)
        axes[r, c].axis("off")
fig.tight_layout()
fig.savefig(FIG / "hog_parametre.png")
plt.close(fig)

# 4) Zoom på ett område (hodet/kameraet) for å vise stjernene tydelig
fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.7))
crop = (slice(40, 120), slice(80, 160))
_, hi8 = hog(img, visualize=True, **DEFAULT)
axes[0].imshow(img[crop], cmap="gray")
axes[0].set_title("Camera, zoom 80×80 px", fontsize=8)
mag, ang = results["camera"]["mag"], results["camera"]["ang"]
axes[1].imshow(np.clip(mag[crop] / np.percentile(mag, 99), 0, 1), cmap="gray")
axes[1].set_title("|G|", fontsize=8)
axes[2].imshow(exposure.rescale_intensity(hi8[crop], in_range=(0, hi8.max() / 2)), cmap="gray")
axes[2].set_title("HOG, 8×8 cells", fontsize=8)
for a in axes:
    a.axis("off")
fig.tight_layout()
fig.savefig(FIG / "hog_zoom.png")
plt.close(fig)

print(f"\nFigurer lagret i {FIG.relative_to(ROOT)}/")
