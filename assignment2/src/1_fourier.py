"""Fourier-transformasjon, deloppgave 1–4 (rapportens figur 1–6).

Følger forelesningen (lecture 3, «Fourier Transform»), bare i 2D i stedet for 1D:
scipy.fft med fftfreq for frekvensaksen, magnitude |F| og fase for hver frekvens,
invers transformasjon gir originalen tilbake, 20·log10 (dB) og klipping for å vise
spekteret, og Hann-vindu (np.hanning) mot kanteffekter.

Eksempelbildet er lysbilde hm10 («Evaluation»), deltaker 10, som har mye tekst og
mange separate varmeflekker. Deltaker 18 har nesten ingen varme på samme lysbilde
og brukes som sammenligning i deloppgave 1. Hovedfunnene i deloppgave 2 og 4 er
kontrollert på deltaker 10 i alle 55 lysbildene.

Alle filtrene er reelle og symmetriske, H(u, v) = H(-u, -v). De endrer bare
magnituden og aldri fasen, så ingenting i bildet flytter seg, og den inverse
transformasjonen er reell (.real fjerner bare avrundingsstøy).

Ut:  assignment2/rapport/figurer/fourier1_spektrum.png … fourier6_kompresjon_kurver.png
Kjør: .venv/bin/python assignment2/src/1_fourier.py
"""
import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from PIL import Image
from scipy import fft, ndimage

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "heatmap-performance"    # hm1–hm55, én mappe per lysbilde, én fil per deltaker
FIG = REPO / "assignment2" / "rapport" / "figurer"
SLIDES = [f"hm{i}" for i in range(1, 56)]

# Samme stil som figurene i assignment1. Seriefargene brukes i fast rekkefølge.
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 160})


def heatmap(slide, participant):
    """Stien til heatmapen for ett lysbilde (hm1–hm55) og én deltaker (filnummer 0–39)."""
    path = DATA / slide / f"Heat Map ({participant}).png"
    if not path.exists():
        raise SystemExit(f"Fant ikke {path}. Pakk ut heatmap-performance.zip fra Canvas i roten av repoet.")
    return path


def load_gray(path):
    """Leser en heatmap som gråtone i [0, 1].

    PIL bruker luma L = 0,299 R + 0,587 G + 0,114 B. Alfakanalen er 255 i alle
    bildene, så den kan kastes.
    """
    return np.asarray(Image.open(path).convert("L"), dtype=float) / 255


def section(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


SLIDE, PARTICIPANT, CLEAN_PARTICIPANT = "hm10", 10, 18
CROP = (slice(130, 330), slice(40, 420))   # utsnittet med tekst og flekker i figur 2, 4 og 5
RING = 0.01                                 # ringbredde (sykler/piksel) for radiell effekt
SIGMAS = [0.05, 0.1, 0.2]                   # støynivåer i deloppgave 2
SIGMA = 0.1                                 # hovedeksempelet
CUTOFFS = np.round(np.arange(0.01, 0.505, 0.01), 2)
STRONG = 0.05                               # «for lav» grense i figur 2 og midtkolonnen i figur 4
DB_RANGE = (15, 65)                         # visningsområde for spekteret, DC (113 dB) klippes
HP_CUTOFFS = [0.02, 0.05, 0.15]
SHARPEN_K = 1.0
PERCENTS = [0.1, 0.5, 1, 2, 5, 10, 20, 50]
SHOWN = [1, 5, 20]                          # prosentene som vises i figur 5
JPEG_QUALITIES = [5, 10, 20, 30, 50, 70, 90, 95]
# Lagringsmodell i deloppgave 4. Et reelt bilde har konjugert symmetrisk spekter,
# F(-u, -v) = F(u, v)*, så de største koeffisientene kommer i par med lik magnitude.
# Vi lagrer bare den ene i hvert par, som to float32 (re, im) og en uint32-posisjon,
# altså 12 byte per par = 6 byte per beholdt koeffisient. Lavpassvalget trenger ingen
# posisjoner, bare radien, altså 4 byte per koeffisient. Originalen har 1 byte per piksel.
BYTES_TOPK, BYTES_LOWPASS = 6, 4

FIG.mkdir(parents=True, exist_ok=True)
f = load_gray(heatmap(SLIDE, PARTICIPANT))
M, N = f.shape
MN = M * N
FY, FX = fft.fftfreq(M)[:, None], fft.fftfreq(N)[None, :]   # sykler per piksel, som fftfreq i forelesningen
D = np.hypot(FX, FY)                                         # avstand fra DC i frekvensplanet
RINGS = (D / RING).astype(int)
CENTRES = (np.arange(RINGS.max() + 1) + 0.5) * RING
dataset = {s: load_gray(heatmap(s, PARTICIPANT)) for s in SLIDES}   # deltaker 10 på alle lysbildene


def filtrer(img, H):
    """Multipliserer spekteret med filteret H og transformerer tilbake."""
    return fft.ifft2(fft.fft2(img) * H).real


def ideal_lp(d0):
    return (D <= d0).astype(float)


def gauss_lp(d0):
    return np.exp(-D ** 2 / (2 * d0 ** 2))


def mse(a, b):
    return np.mean((a - b) ** 2)


def mse_spectral(A, B):
    """MSE mellom to bilder regnet rett fra spektrene deres (Parseval), uten invers DFT."""
    return np.sum(np.abs(A - B) ** 2) / MN ** 2


def psnr(err):
    """PSNR i dB fra en MSE. Toppverdien er 1 fordi bildene er skalert til [0, 1]."""
    return 10 * np.log10(1 / err)


def radial_power(F):
    """Gjennomsnittlig effekt |F|²/MN i ringer på 0,01 sykler/piksel rundt DC.

    Hvit støy med varians σ² har forventet effekt σ² i alle ringene.
    """
    return np.bincount(RINGS.ravel(), (np.abs(F) ** 2).ravel() / MN) / np.bincount(RINGS.ravel())


def crossing(F, sigma):
    """Nedre kant av den første ringen der bildets effekt er lavere enn støyeffekten σ²."""
    return (int(np.argmax(radial_power(F)[1:] < sigma ** 2)) + 1) * RING


def coloured_share(slide, participant):
    """Andel piksler med tydelig farge (HSV-metning > 40), et grovt mål på varmedekning."""
    hsv = np.asarray(Image.open(heatmap(slide, participant)).convert("RGB").convert("HSV"))
    return (hsv[..., 1] > 40).mean()


def show(ax, img, title, signed=False, box=True):
    """Tegner et bilde i gråtoner. Fortegnsbilder skaleres symmetrisk rundt 0 (midtgrå)."""
    if signed:
        v = np.percentile(np.abs(img), 99.5)
        ax.imshow(img, cmap="gray", vmin=-v, vmax=v)
    else:
        ax.imshow(np.clip(img, 0, 1), cmap="gray", vmin=0, vmax=1)
    ax.set_title(title, fontsize=8, color=INK, loc="left")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(box)
        spine.set_color(GRID)


# ============================ 1  DFT og spekter ==============================
section("1  DFT av eksempelbildet")
F = fft.fft2(f)
power = np.abs(F) ** 2
back = fft.ifft2(F)
assert np.abs(back.real - f).max() < 1e-12 and np.abs(back.imag).max() < 1e-12
assert np.isclose(np.sum(f ** 2), power.sum() / MN)   # Parseval
print(f"{SLIDE}/Heat Map ({PARTICIPANT}).png: {N}×{M} px, {MN:,} komplekse koeffisienter, "
      f"{coloured_share(SLIDE, PARTICIPANT):.1%} fargede piksler")
print(f"Invers DFT gir originalen tilbake, største avvik {np.abs(back.real - f).max():.1e} "
      f"(forelesningen: «original signal and FT have same information»)")
print(f"DC-leddet F(0,0)/MN = {F[0, 0].real / MN:.4f} = middelverdien {f.mean():.4f}, "
      f"og det har {power[0, 0] / power.sum():.1%} av energien")
db = 20 * np.log10(np.abs(F) + 1e-12)
print(f"20·log10|F|: DC {db[0, 0]:.0f} dB, median {np.median(db):.0f} dB, "
      f"99,9-persentil {np.percentile(db, 99.9):.0f} dB, så spekteret må vises logaritmisk og klippes")

ac = power.copy()
ac[0, 0] = 0
print("\nEnergikonsentrasjon (DC holdt utenfor):")
print(f"{'radius':>8} {'periode (px)':>13} {'andel koeff.':>13} {'andel AC-energi':>16}")
for r in [0.01, 0.02, 0.05, 0.1, 0.2, 0.3]:
    print(f"{r:8.2f} {1 / r:13.0f} {(D <= r).mean():13.2%} {ac[D <= r].sum() / ac.sum():16.1%}")

vert = (FX == 0) & (np.abs(FY) > 0.02)
beyond = D > 0.02
hann = np.outer(np.hanning(M), np.hanning(N))
windowed = np.abs(fft.fft2((f - f.mean()) * hann)) ** 2
print()
for name, P in [("uten vindu", power), ("med Hann-vindu", windowed)]:
    print(f"Vertikal akse (u = 0, |v| > 0,02) {name}: {P[vert].sum() / P[beyond].sum():.1%} av effekten "
          f"over 0,02 på {vert.sum() / beyond.sum():.2%} av koeffisientene")
print(f"Kantene i den periodiske utvidelsen: øverste rad {f[0].mean():.2f}, nederste {f[-1].mean():.2f}, "
      f"venstre kolonne {f[:, 0].mean():.2f}, høyre {f[:, -1].mean():.2f}")

no_logo = f.copy()
no_logo[440:, 790:] = np.median(f)   # SMI-logoen nederst til høyre males over med bakgrunnen
angle = np.degrees(np.arctan2(FY, FX)) % 180
diagonal = ((np.abs(angle - 30) < 3) | (np.abs(angle - 150) < 3)) & (D > 0.1)
print(f"Effekt langs linjene 30° og 150° (D > 0,1): {power[diagonal].mean():.0f} med logoen, "
      f"{(np.abs(fft.fft2(no_logo)) ** 2)[diagonal].mean():.0f} når logoen er malt over")

clean = load_gray(heatmap(SLIDE, CLEAN_PARTICIPANT))
rp, rp_clean = radial_power(F), radial_power(fft.fft2(clean))
print(f"\nSammenligning med deltaker {CLEAN_PARTICIPANT} på samme lysbilde "
      f"({coloured_share(SLIDE, CLEAN_PARTICIPANT):.1%} fargede piksler):")
for lo, hi in [(0.01, 0.10), (0.10, 0.50)]:
    band = (CENTRES > lo) & (CENTRES < hi)
    print(f"  {lo:.2f}–{hi:.2f} sykler/piksel (perioder {1 / hi:.0f}–{1 / lo:.0f} px): "
          f"deltaker {PARTICIPANT} har {rp[band].sum() / rp_clean[band].sum():.2f} × effekten")

mag_only = fft.ifft2(np.abs(F)).real
phase_only = fft.ifft2(np.exp(1j * np.angle(F))).real
print(f"\nKorrelasjon med originalen: bare magnitude r = {np.corrcoef(mag_only.ravel(), f.ravel())[0, 1]:.2f}, "
      f"bare fase r = {np.corrcoef(phase_only.ravel(), f.ravel())[0, 1]:.2f}")

# ============================ 2  Lavpassfilter ===============================
section("2  Lavpassfilter mot høyfrekvent støy")
noise = np.random.default_rng(42).standard_normal(f.shape)   # samme støymønster, skalert med σ
lowpass = {"ideal": ideal_lp, "gauss": gauss_lp}
print(f"{'σ':>5} {'støyete':>8} {'beste ideell':>18} {'beste gauss':>18} {'effekt < σ² fra':>16}")
for sigma in SIGMAS:
    G = fft.fft2(f + sigma * noise)
    curves = {k: np.array([psnr(mse_spectral(G * H(d0), F)) for d0 in CUTOFFS]) for k, H in lowpass.items()}
    best = {k: CUTOFFS[np.argmax(c)] for k, c in curves.items()}
    print(f"{sigma:5.2f} {psnr(mse(f + sigma * noise, f)):6.2f} dB "
          f"{best['ideal']:7.2f} ({curves['ideal'].max():5.2f} dB) {best['gauss']:7.2f} ({curves['gauss'].max():5.2f} dB) "
          f"{crossing(F, sigma):12.2f}")
    if sigma == SIGMA:
        lp_curves, lp_best = curves, best

g = f + SIGMA * noise
print(f"\nMed σ = {SIGMA} er beste ideelle grense {lp_best['ideal']}, altså perioder ned til "
      f"{1 / lp_best['ideal']:.0f} px beholdes")
for d0 in [STRONG, lp_best["gauss"]]:
    sx = 1 / (2 * np.pi * d0)
    diff = np.abs(filtrer(g, gauss_lp(d0)) - ndimage.gaussian_filter(g, sx, mode="wrap")).max()
    print(f"Gaussisk LPF med D0 = {d0} tilsvarer gaussisk blur med σ = {sx:.2f} px i bildet, "
          f"største avvik {diff:.1e} (konvolusjonsteoremet)")

masks = [ideal_lp(d0) for d0 in CUTOFFS]
hits, best_cutoffs, misses = 0, [], []
for img in dataset.values():
    Fi = fft.fft2(img)
    Gi = fft.fft2(img + SIGMA * noise)
    best = CUTOFFS[np.argmin([mse_spectral(Gi * H, Fi) for H in masks])]
    best_cutoffs.append(best)
    misses.append(abs(best - crossing(Fi, SIGMA)))
    hits += misses[-1] < RING / 2
print(f"Alle {len(dataset)} lysbildene (deltaker {PARTICIPANT}, σ = {SIGMA}): beste ideelle grense = "
      f"frekvensen der effekten faller under σ² i {hits} av {len(dataset)} (største avvik {max(misses):.2f}), "
      f"beste grense varierer fra {min(best_cutoffs):.2f} til {max(best_cutoffs):.2f}")
for label, value in [("Lavest", min(best_cutoffs)), ("Høyest", max(best_cutoffs))]:
    print(f"{label} grense ({value:.2f}): "
          f"{', '.join(s for s, b in zip(SLIDES, best_cutoffs) if b == value)}")

lp_images = {("ideal", "best"): filtrer(g, ideal_lp(lp_best["ideal"])),
             ("gauss", "best"): filtrer(g, gauss_lp(lp_best["gauss"])),
             ("ideal", "strong"): filtrer(g, ideal_lp(STRONG)),
             ("gauss", "strong"): filtrer(g, gauss_lp(STRONG))}
for (kind, which), img in lp_images.items():
    print(f"{kind:5} {which:6}: PSNR {psnr(mse(img, f)):.2f} dB")

# ============================ 3  Høypassfilter ===============================
section("3  Høypassfilter for kanter")
snr_before = f.var() / (SIGMA * noise).var()
print(f"Uten filter: effekt i bildet (varians) / støyeffekt = {10 * np.log10(snr_before):.1f} dB (σ = {SIGMA})")
hp_filters = {f"gauss {d0}": 1 - gauss_lp(d0) for d0 in HP_CUTOFFS} | {f"ideal {STRONG}": 1 - ideal_lp(STRONG)}
for name, H in hp_filters.items():
    out = filtrer(f, H)
    snr = out.var() / filtrer(SIGMA * noise, H).var()
    print(f"HPF {name:10}: middelverdi {out.mean():+.1e}, beholder {(ac * H ** 2).sum() / ac.sum():5.1%} "
          f"av AC-energien, signal/støy etter filteret {10 * np.log10(snr):+.1f} dB")
sharp = filtrer(f, 1 + SHARPEN_K * (1 - gauss_lp(STRONG)))
print(f"Skjerping f + {SHARPEN_K:g}·HPF(D0 = {STRONG}): verdier fra {sharp.min():.2f} til {sharp.max():.2f}, "
      f"altså over- og undershoot (haloer) rundt skarpe kanter")

# ============================ 4  Kompresjon ==================================
section("4  Kompresjon: behold de største Fourier-koeffisientene")
by_magnitude = np.argsort(np.abs(F).ravel())[::-1]
by_radius = np.argsort(D.ravel(), kind="stable")


def keep_first(order, k):
    mask = np.zeros(MN, bool)
    mask[order[:k]] = True
    return mask.reshape(M, N)


print(f"{'prosent':>7} {'k':>8} {'PSNR':>7} {'Parseval':>9} {'lavpass':>8} {'nominell':>9} "
      f"{'byte':>8} {'faktisk':>8} {'bpp':>6}")
comp, reconstructions = [], {}
for p in PERCENTS:
    k = round(p / 100 * MN)
    keep = keep_first(by_magnitude, k)
    rec = fft.ifft2(F * keep).real
    rec_lp = fft.ifft2(F * keep_first(by_radius, k)).real
    reconstructions[p] = rec
    row = dict(p=p, k=k, psnr=psnr(mse(rec, f)), predicted=psnr(power[~keep].sum() / MN ** 2),
               psnr_lp=psnr(mse(rec_lp, f)), bytes=BYTES_TOPK * k, bytes_lp=BYTES_LOWPASS * k)
    assert abs(row["psnr"] - row["predicted"]) < 0.05
    comp.append(row)
    print(f"{p:6g}% {k:8,} {row['psnr']:5.2f}dB {row['predicted']:7.2f}dB {row['psnr_lp']:6.2f}dB "
          f"{MN / k:8.1f}:1 {row['bytes']:8,} {MN / row['bytes']:7.2f}:1 {8 * row['bytes'] / MN:6.2f}")
print(f"Byte per beholdt koeffisient: {BYTES_TOPK} (største magnitude), {BYTES_LOWPASS} (lavpass), "
      f"original 1 byte per piksel. Faktisk forhold < 1 betyr at filen blir større enn originalen.")

desc = np.sort(power.ravel())[::-1]
psnr_by_k = psnr(np.maximum(desc.sum() - np.cumsum(desc), 1e-12) / MN ** 2)   # PSNR når de k største beholdes


def k_for_psnr(target):
    return int(np.argmax(psnr_by_k >= target)) + 1


g8 = np.round(f * 255).astype(np.uint8)


def encode(fmt, **kw):
    buf = io.BytesIO()
    Image.fromarray(g8).save(buf, fmt, **kw)
    return buf.getvalue()


png = encode("PNG", optimize=True)
assert np.array_equal(np.asarray(Image.open(io.BytesIO(png))), g8)   # tapsfri
k_png = len(png) // BYTES_TOPK
print(f"\nPNG (tapsfri): {len(png):,} byte, {MN / len(png):.1f}:1, {8 * len(png) / MN:.2f} bpp. Med samme "
      f"filstørrelse kan Fourier-metoden beholde {k_png / MN:.1%} av koeffisientene, som gir "
      f"{psnr_by_k[k_png - 1]:.1f} dB")
print(f"{'JPEG q':>7} {'byte':>8} {'forhold':>8} {'bpp':>6} {'PSNR':>7} {'Fourier trenger':>16}")
jpeg = []
for q in JPEG_QUALITIES:
    data = encode("JPEG", quality=q)
    err = psnr(mse(np.asarray(Image.open(io.BytesIO(data)).convert("L"), float) / 255, f))
    jpeg.append((q, len(data), err))
    need = BYTES_TOPK * k_for_psnr(err)
    print(f"{q:7} {len(data):8,} {MN / len(data):7.1f}:1 {8 * len(data) / MN:6.2f} {err:5.2f}dB "
          f"{need:10,} byte ({need / len(data):.0f}×)")

spread = []
for img in dataset.values():
    P = np.sort((np.abs(fft.fft2(img)) ** 2).ravel())[::-1]
    discarded = P.sum() - np.cumsum(P)
    spread.append([psnr(discarded[round(p / 100 * MN) - 1] / MN ** 2) for p in PERCENTS])
spread = np.array(spread)
print(f"\nAlle {len(dataset)} lysbildene (deltaker {PARTICIPANT}), PSNR i dB:")
print(f"{'prosent':>7} {'min':>6} {'median':>7} {'maks':>6} {SLIDE:>6}")
for j, p in enumerate(PERCENTS):
    print(f"{p:6g}% {spread[:, j].min():6.1f} {np.median(spread[:, j]):7.1f} {spread[:, j].max():6.1f} "
          f"{comp[j]['psnr']:6.1f}")
j5 = PERCENTS.index(5)
ranked = np.argsort(spread[:, j5])
print(f"Ved 5 %: dårligst {', '.join(f'{SLIDES[i]} ({spread[i, j5]:.1f})' for i in ranked[:3])}, "
      f"best {', '.join(f'{SLIDES[i]} ({spread[i, j5]:.1f})' for i in ranked[::-1][:3])}")
cov = [coloured_share(s, PARTICIPANT) for s in SLIDES]
print(f"Korrelasjon mellom varmedekning og PSNR ved 5 %: r = {np.corrcoef(cov, spread[:, j5])[0, 1]:.2f}")

# ================================ Figur 1 ====================================
fig = plt.figure(figsize=(7.2, 4.7))
gs = fig.add_gridspec(2, 2, width_ratios=[1.3, 1], hspace=0.45, wspace=0.28)
ax = fig.add_subplot(gs[0, 0])
show(ax, f, f"(a) Greyscale image ({SLIDE}, participant {PARTICIPANT})", box=True)
r, c = CROP
ax.add_patch(Rectangle((c.start, r.start), c.stop - c.start, r.stop - r.start, fill=False,
                       edgecolor=BLUE, linewidth=1))

ax = fig.add_subplot(gs[0, 1])
fs_x, fs_y = fft.fftshift(fft.fftfreq(N)), fft.fftshift(fft.fftfreq(M))
im = ax.imshow(fft.fftshift(db), cmap="gray", vmin=DB_RANGE[0], vmax=DB_RANGE[1], aspect="equal",
               extent=(fs_x[0], fs_x[-1], fs_y[-1], fs_y[0]))
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
cb.set_label("20 log$_{10}$|F| (dB)", fontsize=8)
cb.ax.tick_params(labelsize=7)
ax.set_xlabel("u (cycles/pixel)")
ax.set_ylabel("v (cycles/pixel)")
ax.set_title("(b) Magnitude spectrum, centred", fontsize=8, color=INK, loc="left")
arrow = dict(arrowstyle="-|>", color="white", linewidth=0.8)
ax.annotate("horizontal edges\nand text lines", xy=(0, 0.3), xytext=(-0.46, 0.40), color="white",
            fontsize=7, arrowprops=arrow, va="center")
ax.annotate("logo edges", xy=(-0.40, -0.23), xytext=(-0.46, -0.44), color="white", fontsize=7,
            arrowprops=arrow, va="center")

ax = fig.add_subplot(gs[1, 0])
lo, hi = np.percentile(phase_only, [1, 99])
show(ax, (phase_only - lo) / (hi - lo), "(c) Inverse DFT of the phase alone (|F| = 1)")

ax = fig.add_subplot(gs[1, 1])
upto = CENTRES <= 0.5
ax.axvspan(0.10, 0.5, color=GRID, alpha=0.5, linewidth=0)
ax.plot(CENTRES[upto][1:], rp[upto][1:], color=BLUE, linewidth=1.4, label=f"Participant {PARTICIPANT}")
ax.plot(CENTRES[upto][1:], rp_clean[upto][1:], color=ORANGE, linewidth=1.4,
        label=f"Participant {CLEAN_PARTICIPANT} (almost no heat)")
ax.set_yscale("log")
ax.set_xlim(0, 0.5)
ax.set_xlabel("Distance from centre D (cycles/pixel)")
ax.set_ylabel("Mean power |F|²/MN")
ax.text(0.30, 0.9, "text", transform=ax.get_xaxis_transform(), color=INK2, fontsize=8, ha="center")
ax.text(0.05, 0.9, "blobs", transform=ax.get_xaxis_transform(), color=INK2, fontsize=8, ha="center")
ax.legend(frameon=False, fontsize=7, loc="lower left")
ax.set_title("(d) Radial power spectrum", fontsize=8, color=INK, loc="left")
ax.grid(axis="y", color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
fig.savefig(FIG / "fourier1_spektrum.png", bbox_inches="tight")
plt.close(fig)

# ================================ Figur 2 ====================================
fig, axes = plt.subplots(2, 3, figsize=(7.2, 3.1), gridspec_kw={"hspace": 0.25, "wspace": 0.04})
panels = [(f, "(a) Original"),
          (lp_images["ideal", "best"], f"(b) Ideal, D$_0$ = {lp_best['ideal']:.2f}"),
          (lp_images["gauss", "best"], f"(c) Gaussian, D$_0$ = {lp_best['gauss']:.2f}"),
          (g, f"(d) Noisy, σ = {SIGMA}"),
          (lp_images["ideal", "strong"], f"(e) Ideal, D$_0$ = {STRONG}"),
          (lp_images["gauss", "strong"], f"(f) Gaussian, D$_0$ = {STRONG}")]
for ax, (img, title) in zip(axes.ravel(), panels):
    value = "" if img is f else f"  {psnr(mse(img, f)):.1f} dB"
    show(ax, img[CROP], title + value)
fig.savefig(FIG / "fourier2_lavpass.png", bbox_inches="tight")
plt.close(fig)

# ================================ Figur 3 ====================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.8), gridspec_kw={"wspace": 0.3})
ax1.plot(CENTRES[upto][1:], rp[upto][1:], color=BLUE, linewidth=1.4, label="Clean image")
for sigma in SIGMAS:
    x0 = crossing(F, sigma)
    ax1.axhline(sigma ** 2, color=INK2, linestyle="--", linewidth=0.8)
    ax1.text(0.495, sigma ** 2 * 1.25, f"noise σ = {sigma}", color=INK2, fontsize=7, ha="right")
    ax1.plot(x0, sigma ** 2, "o", color=INK, markersize=4)
    ax1.annotate(f"{x0:.2f}", (x0, sigma ** 2), xytext=(-4, -11), textcoords="offset points",
                 fontsize=7, color=INK, ha="right")
ax1.set_yscale("log")
ax1.set_xlim(0, 0.5)
ax1.set_xlabel("Distance from centre D (cycles/pixel)")
ax1.set_ylabel("Mean power |F|²/MN")
ax1.set_title("(a) Where the image sinks below the noise", fontsize=8, color=INK, loc="left")
ax1.grid(axis="y", color=GRID, linewidth=0.6)
ax1.set_axisbelow(True)

for kind, colour, label in [("gauss", BLUE, "Gaussian"), ("ideal", ORANGE, "Ideal")]:
    y = lp_curves[kind]
    ax2.plot(CUTOFFS, y, color=colour, linewidth=1.4, label=label)
    i = int(np.argmax(y))
    ax2.plot(CUTOFFS[i], y[i], "o", color=colour, markersize=4)
    ax2.annotate(f"{y[i]:.1f} dB at {CUTOFFS[i]:.2f}", (CUTOFFS[i], y[i]), xytext=(6, 2),
                 textcoords="offset points", fontsize=7, color=INK)
noisy_psnr = psnr(mse(g, f))
ax2.axhline(noisy_psnr, color=INK2, linestyle="--", linewidth=0.8)
ax2.text(0.495, noisy_psnr + 0.3, "no filter", color=INK2, fontsize=7, ha="right")
ax2.set_xlim(0, 0.5)
ax2.set_xlabel("Cutoff D$_0$ (cycles/pixel)")
ax2.set_ylabel("PSNR against clean image (dB)")
ax2.set_title(f"(b) Low-pass result, σ = {SIGMA}", fontsize=8, color=INK, loc="left")
ax2.legend(frameon=False, fontsize=7, loc="lower right")
ax2.grid(axis="y", color=GRID, linewidth=0.6)
ax2.set_axisbelow(True)
fig.savefig(FIG / "fourier3_lavpass_kurver.png", bbox_inches="tight")
plt.close(fig)

# ================================ Figur 4 ====================================
fig, axes = plt.subplots(2, 3, figsize=(7.2, 3.1), gridspec_kw={"hspace": 0.25, "wspace": 0.04})
panels = [(filtrer(f, hp_filters[f"gauss {HP_CUTOFFS[0]}"]), f"(a) Gaussian HPF, D$_0$ = {HP_CUTOFFS[0]}", True),
          (filtrer(f, hp_filters[f"gauss {HP_CUTOFFS[1]}"]), f"(b) Gaussian HPF, D$_0$ = {HP_CUTOFFS[1]}", True),
          (filtrer(f, hp_filters[f"gauss {HP_CUTOFFS[2]}"]), f"(c) Gaussian HPF, D$_0$ = {HP_CUTOFFS[2]}", True),
          (sharp, "(d) Sharpened, f + HPF", False),
          (filtrer(f, hp_filters[f"ideal {STRONG}"]), f"(e) Ideal HPF, D$_0$ = {STRONG}", True),
          (filtrer(g, hp_filters[f"gauss {STRONG}"]), f"(f) Gaussian HPF on noisy, σ = {SIGMA}", True)]
for ax, (img, title, signed) in zip(axes.ravel(), panels):
    show(ax, img[CROP], title, signed=signed)
fig.savefig(FIG / "fourier4_hoypass.png", bbox_inches="tight")
plt.close(fig)

# ================================ Figur 5 ====================================
fig, axes = plt.subplots(2, 3, figsize=(7.2, 3.3), gridspec_kw={"hspace": 0.25, "wspace": 0.04})
err_max = 0.3
for j, p in enumerate(SHOWN):
    rec = reconstructions[p]
    row = next(r for r in comp if r["p"] == p)
    show(axes[0, j], rec[CROP], f"({'abc'[j]}) {p} % kept  {row['psnr']:.1f} dB")
    im = axes[1, j].imshow(np.abs(rec - f)[CROP], cmap="Blues", vmin=0, vmax=err_max)
    axes[1, j].set_title(f"({'def'[j]}) Absolute error, {p} %", fontsize=8, color=INK, loc="left")
    axes[1, j].set_xticks([])
    axes[1, j].set_yticks([])
    for spine in axes[1, j].spines.values():
        spine.set_color(GRID)
cb = fig.colorbar(im, cax=axes[1, 2].inset_axes([1.03, 0, 0.03, 1]))
cb.set_label("|error|", fontsize=7)
cb.ax.tick_params(labelsize=7)
fig.savefig(FIG / "fourier5_kompresjon.png", bbox_inches="tight")
plt.close(fig)

# ================================ Figur 6 ====================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"wspace": 0.3})
ax1.fill_between(PERCENTS, spread.min(axis=0), spread.max(axis=0), color=BLUE, alpha=0.15, linewidth=0,
                 label=f"Largest |F|, range over {len(dataset)} slides")
ax1.plot(PERCENTS, [r["psnr"] for r in comp], color=BLUE, linewidth=1.4, marker="o", markersize=4,
         label=f"Largest |F|, {SLIDE}")
ax1.plot(PERCENTS, [r["psnr_lp"] for r in comp], color=ORANGE, linewidth=1.4, marker="o", markersize=4,
         label=f"Lowest frequencies, {SLIDE}")
ax1.set_xscale("log")
ax1.set_xticks(PERCENTS, [f"{p:g}" for p in PERCENTS])
ax1.set_xlabel("Coefficients kept (%)")
ax1.set_ylabel("PSNR (dB)")
ax1.set_title("(a) Quality against share of coefficients", fontsize=8, color=INK, loc="left")
ax1.legend(frameon=False, fontsize=7, loc="upper left")
ax1.grid(axis="y", color=GRID, linewidth=0.6)
ax1.set_axisbelow(True)

bpp = lambda b: 8 * np.asarray(b) / MN
ax2.plot(bpp([r["bytes"] for r in comp]), [r["psnr"] for r in comp], color=BLUE, linewidth=1.4,
         marker="o", markersize=4, label="Fourier, largest |F|")
ax2.plot(bpp([r["bytes_lp"] for r in comp]), [r["psnr_lp"] for r in comp], color=ORANGE, linewidth=1.4,
         marker="o", markersize=4, label="Fourier, lowest frequencies")
ax2.plot(bpp([b for _, b, _ in jpeg]), [e for _, _, e in jpeg], color=AQUA, linewidth=1.4, marker="o",
         markersize=4, label="JPEG")
for x, label in [(8, "8-bit original"), (bpp(len(png)), "PNG, lossless")]:
    ax2.axvline(x, color=INK2, linestyle="--", linewidth=0.8)
    ax2.text(x / 1.08, 42, label, color=INK2, fontsize=7, rotation=90, va="center", ha="right")
ax2.set_xscale("log")
ax2.set_xticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20], ["0.1", "0.2", "0.5", "1", "2", "5", "10", "20"])
ax2.set_xticks([], minor=True)
ax2.set_ylim(18, 62)
ax2.set_xlabel("Bits per pixel (log scale)")
ax2.set_ylabel("PSNR (dB)")
ax2.set_title("(b) Quality against file size", fontsize=8, color=INK, loc="left")
ax2.legend(frameon=False, fontsize=7, loc="upper left")
ax2.grid(axis="y", color=GRID, linewidth=0.6)
ax2.set_axisbelow(True)
fig.savefig(FIG / "fourier6_kompresjon_kurver.png", bbox_inches="tight")
plt.close(fig)

section("Figurer")
for name in ["fourier1_spektrum", "fourier2_lavpass", "fourier3_lavpass_kurver", "fourier4_hoypass",
             "fourier5_kompresjon", "fourier6_kompresjon_kurver"]:
    print(FIG / f"{name}.png")
