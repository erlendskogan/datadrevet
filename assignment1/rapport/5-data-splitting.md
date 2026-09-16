# Oppgave 3 – Data splitting

> Norsk arbeidsversjon – den engelske teksten skrives i Overleaf-rapporten. Kode: `src/5_data_splitting.py`. Ca. 230 ord.

**a.**
En 70-30- eller 80-20-splitt brukes ofte når man deler forhåndsbehandlede datasett i trenings- og testsett. Vi valgte en 80-20-splitt, siden datasettets betydelige størrelse (88 735 rader) gir nok data i begge settene selv med den større treningsandelen.

Datasettet består av 8 316 tidsserier per land og vekst, som typisk spenner over 11 år, og avlingen varierer lite innen en serie (variasjonskoeffisient 0,10, oppgave 2c). En tilfeldig radsplitt plasserer derfor nesten identiske rader fra samme serie i begge settene, noe som sannsynligvis gir et for optimistisk ytelsesestimat og forsterker lekkasjen fra medianimputeringen som allerede er nevnt i oppgave 2. En gruppert splitt, som holder hver serie samlet i ett sett, ville unngått dette, men noen land og vekster forekommer bare i én serie, så å plassere denne serien i testsettet ville latt landet eller veksten være helt usett for encodingen i oppgave 4. Vi bruker derfor en tilfeldig 80-20-splitt og rapporterer serielekkasjen som en begrensning.

**b.**
Splitting av dataene lar modellen evalueres på rader den ikke har sett under trening. Uten et eget testsett måler man bare hvor godt modellen har memorert treningsdataene, ikke hvor godt den generaliserer. Et stort gap mellom trenings- og testytelse signalerer overfitting, der modellen har lært mønstre som er spesifikke for treningsradene i stedet for det underliggende forholdet mellom variablene. 80-20-forholdet balanserer nok treningsdata til å tilpasse en pålitelig modell mot nok testdata til et stabilt ytelsesestimat.