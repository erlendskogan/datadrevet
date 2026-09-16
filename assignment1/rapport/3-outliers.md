# Oppgave 3 – Håndtering av outliers

> Norsk arbeidsversjon – den engelske teksten skrives i Overleaf-rapporten. Kode: `src/3_outliers.py`. Ca. 430 ord inkl. tabelltekst.

**a.**
Fordi de tre målingene spenner over helt ulike skalaer fra vekst til vekst, detekteres outliers per vekst (`Item`), ikke på hele kolonnen samlet – ellers ville man sammenlignet f.eks. sukkerrør med vanilje. Tre metoder ble sammenlignet (Tabell 6). Rå IQR (1,5·IQR per vekst) flagger 13,1–13,9 % av areal og produksjon og 4,5 % av avling – tallene som allerede er oppgitt i oppgave 1b. Som der ble påpekt, er de fleste av disse ekte: Nederlandske veksthusagurker har nå den høyeste avlingen (743 tonn/ha) siden sopp er fjernet i oppgave 2, og er et reelt, men annet produksjonssystem (veksthus) enn friland. En vanlig z-score (rå skala, per vekst) flagger færre (1,5–2,2 %), men forutsetter en noenlunde symmetrisk fordeling, noe disse høyreskjeve målingene ikke har. IQR beregnet på log10(x+1) flagger enda færre (1,3 % for areal og produksjon, 2,9 % for avling). At andelen faller så mye ved en log-transformasjon, viser at det meste av det rå IQR-metoden flagger, er en konsekvens av skjevheten i fordelingen – ikke feil i dataene.

**b.**
Vi transformerer areal, produksjon og avling med log10(x+1) fremfor å fjerne eller cappe på rå skala. Begrunnelsen er tabellen over: siden log-transformasjonen alene reduserer andelen flagget fra 13–14 % til 1,3–2,9 %, er en generell transformasjon mer treffsikkert enn å fjerne eller cappe en tidels av dataene, som i stor grad er ekte variasjon (jf. oppgave 1b). Vi brukte log10(x+1) fremfor log10(x) fordi 31 rader har produksjon og avling lik 0 (reell avlingssvikt, areal er alltid > 0 for disse); log10(0) er udefinert, mens log1p-varianten gir disse radene verdien 0 uten å forvrenge de øvrige verdiene merkbart. Alternativet – å utelate radene – ble forkastet fordi avlingssvikt er en ekte hendelse, ikke en feil, og fjerning ville laget et lite, usystematisk hull i 31 av 8 436 tidsserier.

De resterende outlierne etter transformasjonen (1,3–2,9 %, jf. IQR på log10) er trolig i større grad genuint ekstreme, siden log-transformasjonen allerede har rettet opp skjevheten. Disse cappes (winsoriseres) til 1,5·IQR-grensen per vekst på log-skala. Dette berører 1,3–2,9 % av cellene (3 986 av 88 735 rader har minst én cappet verdi) og endrer ingen rad, land eller vekst – i motsetning til oppgave 2, hvor sletting var eneste utvei for verdier som ikke kunne anslås. Kolonnene `area_harvested_ha_log10`, `production_tonnes_log10` og `yield_hg_per_ha_log10` er log-transformert og cappet, klare til skalering i oppgave 4 (i tråd med notatet om at skalering bør skje etter log), og `*_capped` markerer de cappede cellene – samme mønster som `imputed` i oppgave 2. De opprinnelige, ucappede kolonnene beholdes uendret for etterprøvbarhet.

**Tabell 6: Andel flagget per vekst, tre metoder.**

| Kolonne | IQR (rå), % | IQR (log10), % | z-score (rå), % |
|---|---:|---:|---:|
| area_harvested_ha | 13,1 | 1,3 | 2,2 |
| production_tonnes | 13,9 | 1,3 | 2,1 |
| yield_hg_per_ha | 4,5 | 2,9 | 1,5 |

**Figur 3:** Boksplott av log10(x+1) før og etter capping av gjenværende outliers, én rute per måling.
