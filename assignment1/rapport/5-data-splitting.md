# Oppgave 5 – Data splitting

> Norsk arbeidsversjon. Den innleverte engelske teksten står i [`main.tex`](main.tex) (Data Splitting).
> Kode: `src/5_data_splitting.py`.

**a.**
Datasettet splittes etter encoding (oppgave 4a) og før skalering (oppgave 4b), slik at hver parameter som tilpasses senere, bare ser treningssettet. Vi valgte en 80-20-splitt, siden 88 735 rader gir nok data i begge settene selv med den større treningsandelen.

Datasettet består av de 8 316 seriene som er igjen etter rensingen, som typisk spenner over 11 år, og avlingen varierer lite innen en serie (variasjonskoeffisient 0,10, oppgave 2c). En tilfeldig radsplitt plasserer derfor nesten identiske rader fra samme serie i begge settene, noe som sannsynligvis gir et for optimistisk ytelsesestimat og forsterker lekkasjen fra medianimputeringen som allerede er nevnt i oppgave 2. En gruppert splitt ville unngått dette, men tre land og én vekst forekommer bare i én serie hver, så fire serier måtte vært låst til treningssettet for at encodingen i oppgave 4a skal dekke alle kategorier. Vi beholder den tilfeldige splitten som konvensjonen oppgaveteksten nevner, og rapporterer serielekkasjen som en begrensning, samtidig som vi sier at den grupperte splitten er det sterkere designet.

**b.**
Splitting av dataene lar modellen evalueres på rader den ikke har sett under trening. Uten et eget testsett måler man bare hvor godt modellen har memorert treningsdataene, ikke hvor godt den generaliserer. Et stort gap mellom trenings- og testytelse signalerer overfitting, der modellen har lært mønstre som er spesifikke for treningsradene i stedet for det underliggende forholdet mellom variablene. 80-20-forholdet balanserer nok treningsdata til å tilpasse en pålitelig modell mot nok testdata til et stabilt ytelsesestimat.