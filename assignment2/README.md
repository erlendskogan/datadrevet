# Assignment 2 – Image Processing

Oppgaveteksten ligger i `oppgave.pdf`. Datasettet er fra Canvas og ligger i `heatmap-performance/`
i roten av repoet.

## Status

| Del | Status | Norsk arbeidsversjon | Kode |
|---|---|---|---|
| Fourier-transformasjon (deloppgave 1–4) | ✅ | [`rapport/1-fourier.md`](rapport/1-fourier.md) | [`src/1_fourier.py`](src/1_fourier.py) |
| PCA | – | | |
| HOG | – | | |
| LBP | – | | |
| Blob-deteksjon | – | | |
| Konturdeteksjon | – | | |

Kjør fra roten av repoet. Skriptet skriver tallene i rapportteksten og lager figurene i
`rapport/figurer/`. Det sjekker seg selv underveis (blant annet at invers DFT gir originalen tilbake og
at PSNR regnet med Parsevals teorem er lik den målte) og tar rundt 10 sekunder.

```bash
.venv/bin/python assignment2/src/1_fourier.py
```

## Valg av datasett: `heatmap-performance`

**Vi bruker `heatmap-performance`**: eye-tracking-heatmaps fra en MOOC-forelesning i Scala
(Sharma mfl. 2020, <https://doi.org/10.1186/s40561-020-00122-x>). Settet har 2 200 PNG-bilder på
960×540 px, fordelt på 55 mapper (`hm1`–`hm55`). Hver mappe er ett lysbilde, og filene
`Heat Map (0)`–`Heat Map (39)` i mappen er de 40 deltakerne. Med i zip-filen er også
`score-MOOC-ET.csv` (pre- og posttest for 40 studenter) og selve artikkelen.

### Hvorfor dette settet

Oppgaveteksten krever bare et datasett fra Canvas på ett sted: blob-deteksjonen skal kjøres på
*«one of the provided image datasets»*, og konturdeteksjonen på *«the same image dataset»*. Disse to oppgavene gir 30 av 100 poeng. Fourier, PCA, HOG og LBP kan bruke hvilke bilder som helst. Valget av
datasett avgjøres derfor først og fremst av hvor godt blob- og konturdeteksjonen fungerer, og
40 % av karakteren på hver oppgave gis for «Insight in Discussion».

1. **Blobber og konturer betyr noe konkret.** I en heatmap er en blob en fiksasjonsklynge, altså et
   sted deltakeren så på. En kontur er avgrensningen av et område med mye oppmerksomhet. Når vi
   rapporterer antall blobber, størrelse, posisjon, konturareal og omkrets, beskriver tallene dermed
   hvor studentene så og hvor spredt blikket var. I de tre andre settene blir blobbene og konturene
   tilfeldige bildeelementer som blader, refleksjoner og trafikkjegler, og statistikken sier lite.
2. **Settet er godt egnet til å sammenligne blob- og konturdeteksjon.** Små, runde fiksasjoner blir
   gode blobber. Når flere fiksasjoner smelter sammen langs en tekstlinje, blir området avlangt og
   uregelmessig. Da deler LoG det opp i mange blobber, mens konturdeteksjonen fanger hele formen som
   ett område. Dette gir konkrete eksempler til deloppgave 4–7 om fordeler, begrensninger og når hver
   metode passer best.
3. **Parameterne har en synlig og forklarbar effekt.** `min_sigma`/`max_sigma` bestemmer om vi
   finner enkeltfiksasjoner eller hele klynger, og terskelverdien bestemmer hvor «varm» en region må
   være for å telle med. Effekten kan forklares med det bildene faktisk viser.
4. **Bildene i hver mappe er justert mot hverandre, noe som passer PCA.** Alle 40 bildene i en mappe
   har nøyaktig samme lysbilde i bakgrunnen, så variasjonen mellom dem kommer bare fra hvor
   deltakerne så. Egenvektorene blir dermed tolkbare «oppmerksomhetsmønstre», omtrent som eigenfaces.
   Bildene har også lik størrelse, så de kan legges direkte inn i en matrise uten beskjæring.
5. **Fourier-oppgaven får et tydelig motstykke.** Lysbildene har skarp tekst, som gir høye
   frekvenser, og myke heat-flekker, som gir lave frekvenser. Et lavpassfilter beholder flekkene og
   visker ut teksten, mens et høypassfilter gjør det motsatte. Det gjør analysen i deloppgave 2–4
   enkel å forklare.
6. **Settet åpner for ekstra innsikt.** `score-MOOC-ET.csv` gjør det mulig å se om blob- og
   konturstatistikk henger sammen med testresultatene. Dette er valgfritt, men er den typen innsikt
   som gir uttelling på 40 %-kriteriet.

### Hva vi testet før valget

Vi kjørte samme oppsett på fire tilfeldige bilder fra hvert sett, med `skimage.feature.blob_log` og
`cv2.findContours` på et glattet gråtonebilde (Otsu-terskel). For heatmapene brukte vi et
«varme»-bilde i stedet, se fallgruven under.

| Datasett | Blobber per bilde | Konturer per bilde | Hva ble funnet |
|---|---|---|---|
| **heatmap-performance** | 2–12 | 1–5 | Fiksasjonsklynger og oppmerksomhetsområder, altså det bildet faktisk handler om |
| intel-image-classification | 2–51 | 1–40 | Blader, vinduer, bølger. Mest støy i skog- og gatebilder |
| vehicle-type-detection | 17–44 | 13–15 | Trafikkjegler, reflekser, hjul og bakgrunn. Svært få treff på selve kjøretøyet |
| facial-emotion-recognition | 0–12 | 4–8 | Ustabilt. Noen ganger øyne, ofte bakgrunn eller hår |

Med ren gråtonekonvertering uten tilpasning fant vi 70–470 blobber per bilde i Intel-settet og
120–210 i kjøretøysettet. Det er for mye til at tallene kan brukes til noe.

For PCA la vi 40 bilder av samme lysbilde (`hm20`, nedskalert til 96×54) inn i en matrise. Da
forklarte 10 komponenter 66 % og 20 komponenter 85 % av variansen. Kurven stiger jevnt, så det går
an å diskutere avveiningen mellom kompresjon og kvalitet.

### Hvorfor ikke de andre

- **intel-image-classification** (landskapsbilder på 150×150 i seks klasser, ca. 17 000 merkede bilder) er et
  godt nummer to. Settet egner seg godt til Fourier, HOG og LBP, med enkle scener som hav og isbre og
  komplekse scener som skog og gate. Problemet er blob- og konturdeteksjonen, som er den eneste delen
  som *må* bruke et Canvas-sett. Her finnes det ingen naturlige blobber, så antallet avhenger bare
  av parametrene, og diskusjonen får lite å bygge på. Bildene er heller ikke justert mot hverandre, så
  PCA fanger for det meste opp generell lysstyrke og fordeling av himmel og bakke.
- **vehicle-type-detection** (1 310 bilder) har nesten bare unike bildestørrelser (294 forskjellige i
  et utvalg på 300). Alle bildene må derfor skaleres om før PCA, og da blir de forvrengt. Blobbene
  havner på trafikkjegler og refleksjoner i stedet for på kjøretøyene.
- **facial-emotion-recognition** er bare et gratis utdrag av et kommersielt datasett: 152 bilder av
  19 personer, lisensiert CC BY-NC-ND. Bildene er mobilfoto i opptil 4608 px med 12 ulike
  oppløsninger, og ansiktene er ikke justert. PCA på så få ujusterte bilder gir dårlige eigenfaces,
  og blob-deteksjonen fant 0–12 treff uten noe fast mønster.

### Fallgruver og hvordan vi håndterer dem

- **Gråtone ødelegger heatmap-fargene.** Heatmapene bruker en jet-lignende fargeskala. Konverteres
  de direkte til gråtone, blir gult lysest mens rødt og blått blir mørkt, så en flekk ser ut som en
  ring. Til blob- og konturdeteksjonen lager vi derfor ett gråtonebilde med «varme» fra HSV: mettede
  piksler med fargetone fra rød til grønn. Bakgrunnslysbildet blir da svart. Dette er fortsatt
  gråtone og er i seg selv et diskusjonspoeng.
- **LBP ber om en naturscene, en tekstur og et ansikt.** Heatmapene inneholder ingen av delene.
  Oppgaven sier *«You are also allowed to use any other dataset from outside sources»*, og kravet om
  Canvas-data gjelder bare blob og kontur. Til LBP (og gjerne HOG) bruker vi derfor enkeltbilder
  i tillegg: et skogbilde fra Intel-settet som tekstur, et landskap fra Intel som naturscene, og et
  ansikt fra facial-emotion-settet eller `skimage.data.astronaut()`. Dette må stå tydelig i
  rapporten.
- **Koblingen til `score-MOOC-ET.csv` er en antakelse.** Filnavnene går fra 0 til 39, mens
  `subject` går fra 1 til 40, så vi antar at fil *n* tilhører subject *n*+1. Subject 1–3 og 21 har
  0/0 på begge testene, som trolig betyr at dataene mangler. Hvis vi bruker koblingen, må vi oppgi
  antakelsen og utelate disse fire.
- **Størrelse.** Zip-filen er 549 MB. Vi pakker bare ut mappene vi trenger og nedskalerer før PCA:
  kovariansmatrisen for 960×540 piksler ville hatt om lag 2,7 × 10¹¹ elementer.
