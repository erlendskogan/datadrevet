# Valg og tilpasning av datasett

> Norsk arbeidsversjon. Den innleverte engelske teksten står i [`main.tex`](main.tex) (Introduction).
> Kode: `src/0_tilpass_datasett.py`.

Vi vurderte de 15 kandidatdatasettene opp mot det oppgavene krever: både numeriske og kategoriske
kolonner, ekte manglende verdier, realistiske uteliggere, håndterbar størrelse og selvforklarende
kolonner. Vi valgte FAOSTATs avlingsstatistikk (`crop1.csv`) fremfor husdyrfilen (`live1.csv`), som
bare har én numerisk variabel med blandede enheter og dermed gjør skalering triviell og PCA meningsløs.

**Formålet, som styrer hele rapporten:** vi forbereder dataene for å predikere *produksjon* fra
høstet areal, land, vekst og år. Avling er derfor ikke en feature, fordi den er en deterministisk
funksjon av de to andre målingene. Dette valget er det som binder oppgave 1 til 6 sammen, se
`../forbedringsguide.md` (G1).

To egenskaper ved råfilen gjør den uegnet som den er: kolonnen `Value` blander hektar, tonn og hg/ha,
og regioner og landgrupper teller land dobbelt. Vi pivoterte derfor filen fra langt til bredt format,
slik at hver rad er én kombinasjon av land, vekst og år med tre numeriske kolonner, og fjernet 35
regioner og landgrupper, blant annet «China», som er summen av fastlands-Kina, Taiwan, Hongkong og
Macao, og som ellers ville dominert outlier-deteksjonen. Vi avgrenset også til 2010–2020 i stedet for
til noen få hovedvekster, som er de best rapporterte og ville fjernet det meste av de manglende
dataene. Avgrensningen beholder alle 118 vekster og 200 land til encoding-oppgaven, unngår de fleste
grenseendringer bortsett fra Sudan, som ble delt i 2011 og opptrer som tre kategorier, og reduserer
andelen manglende verdier fra 15,1 %, 11,0 % og 16,0 % til 7,3 %, 5,9 % og 9,6 %, fordi rapporteringen
er bedre i nyere år. Ingen steg endrer en verdi (Tabell 1), og manglende verdier og outliers er latt
til oppgave 2 og 3.

**Tabell 1: Tilpasning av `crop1.csv` før oppgave 1. Ingen verdier er endret.**

| Steg | Rader | Land og områder | Vekster |
|---|---|---|---|
| Original (langt format) | 1 895 975 | 245 | 118 |
| Pivotert til bredt format | 667 046 | 245 | 118 |
| Uten 35 regioner og landgrupper | 479 231 | 210 | 118 |
| Avgrenset til 2010–2020 | 98 101 | 200 | 118 |
