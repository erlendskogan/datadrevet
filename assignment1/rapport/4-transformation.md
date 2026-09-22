# Oppgave 4 – Encoding og skalering

> Norsk arbeidsversjon. Den innleverte engelske teksten står i [`main.tex`](main.tex) (Data Transformation).
> Kode: `src/4_encoding.py` og `src/4b_scaling.py`.

**a. Encoding.**
De eneste kategoriske kolonnene er `Area` (200 land) og `Item` (117 vekster). `Year` er allerede
numerisk (oppgave 1a), og `imputed` og `*_capped` er boolske flagg og ikke kategorier, så ingen av
dem encodes. Vi bruker one-hot encoding, der hver unike verdi får sin egen binære kolonne. Det gir
317 nye kolonner, 200 for `Area` og 117 for `Item`.

Begge kolonnene er nominelle kategorier uten naturlig rekkefølge, ett land eller én vekst er ikke
«mer» enn et annet, og one-hot er riktig valg nettopp derfor. Label encoding (Afghanistan = 0,
Albania = 1, …) ville innført en rangordning og en avstand som ikke finnes, og ville vært særlig
skadelig for en variansbasert metode som PCA, som leser enhver tallmessig spredning som struktur.
**Oppgave 6 tester dette direkte:** one-hot-kolonnene bærer nesten ingen varians, det motsatte av
det en label-encodet kolonne ville vist. Med 88 735 rader er 317 binære kolonner et håndterbart
forhold mellom rader og features, og et høyt kolonnetall ville først og fremst betydd noe for
avstandsbaserte metoder som k-NN, som vi ikke bruker.

**b. Skalering.**
Oppgave 3 rettet den sterke høyreskjevheten med log10(x+1) og capping, men de tre log-skalerte
målingene spenner fortsatt ulike områder (omtrent 0–7,7 for areal, 0–8,9 for produksjon og 2,6–6,7
for avling), og avstands- eller gradientbaserte modeller er følsomme for slike forskjeller.

Vi bruker standardisering (x' = (x − gjennomsnitt) / std) fremfor min-max. Fordi oppgave 3 allerede
har trukket inn uteliggerne, er gjennomsnitt og standardavvik mer meningsfulle mål på spredning enn
min og maks, som fortsatt ville vært styrt av de to ytterpunktene i hver kolonne.

Skaleringsparametrene beregnes bare på treningssettet fra oppgave 5 og brukes deretter på begge
settene, så datasettet splittes før det skaleres, ikke etter. Å fitte på hele datasettet, eller å
fitte én scaler per sett, ville latt testfordelingen påvirke representasjonen av treningsdataene.
Treningssettet får dermed gjennomsnitt 0 og standardavvik 1 per konstruksjon, mens testsettet lander
nær, men ikke nøyaktig på, 0/1 (−0,005/0,990 for areal), som er en kontroll på at framgangsmåten er
riktig. One-hot-kolonnene, `Year`, `imputed` og `*_capped` skaleres ikke, fordi one-hot-kolonnene og
flaggene er binære og `Year` er en ordnet telling på sin egen naturlige skala (oppgave 1a).
**Produksjon standardiseres sammen med de to andre målingene** fordi oppgave 6 trenger alle tre på
felles skala, og en modell ville blitt tilpasset på de standardiserte featurene med prediksjonene
transformert tilbake.

**Virkningen på modellen (svaret på 4b-ii).** Skalering endrer ingen informasjon i dataene, bare
representasjonen, men den endrer hvordan en modell bruker dem. En lineær modell på uskalerte kolonner
gir koeffisienter i enheter som ikke kan sammenlignes, og gradient descent konvergerer tregt når én
kolonne er flere tierpotenser bredere enn en annen. Med standardiserte input er koeffisientene
sammenlignbare i standardavvik, regularisering straffer alle kolonner likt, og PCA i oppgave 6 finner
retningene med størst varians i stedet for kolonnen med størst enhet.

**Tabell (rapportens Table 6): Standardiseringsparametre, beregnet kun på treningssettet.**

| Kolonne | Gjennomsnitt | Std.avvik |
|---|---:|---:|
| area_harvested_ha_log10 | 3,567 | 1,246 |
| production_tonnes_log10 | 4,283 | 1,310 |
| yield_hg_per_ha_log10 | 4,722 | 0,585 |
