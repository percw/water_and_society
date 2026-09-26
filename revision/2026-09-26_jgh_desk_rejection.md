# JGH-2026-0216: desk-avvisning 22. september 2026

## 1. Hva svaret betyr

Standardbrev: manuskriptet «has not been advanced to the peer review stage as the editors
have judged that it is not the right fit». Ingen fagfeller har lest det, og det følger ingen
kommentarer. Å klage er meningsløst, og det trengs ikke noe svar.

Den sannsynlige grunnen er nettopp det brevet sier, nemlig at artikkelen ikke passer inn:

- JGH publiserer global historie om forbindelser, sirkulasjon og sammenligning. Kjernen i
  manuskriptet er en tidsserieanalyse av *ett* land (sup-F, lokale projeksjoner, DiD) med
  fire komparative «lesninger» ved Maddison-benchmarkårene. Tvedt-innrammingen løste ikke
  dette, fordi redaktørene så at testen er britisk.
- Den økonometriske verktøykassa ligger langt fra det JGH-lesere vanligvis møter.

Redaktørene har altså ikke vurdert analysen. Da jeg selv gikk gjennom analysen etter
avvisningen, fant jeg likevel et problem som fagfeller i et økonomisk-historisk tidsskrift
ville ha funnet. Det er viktigere enn selve avvisningen.

## 2. Svakheten i analysen (nye tester, `src/methods/falsification.py`)

Resultatene ligger i `docs/results_falsification_v1.txt`.

**a) Tabell 3, kolonnen for førstedifferanser, rapporterte feil test.** p-verdien var
joint-F for elleve lagger, mens teksten tolket den som om den gjaldt den kumulative
effekten. Testen av selve summen gir:

| Utfall | Sum per 1 000 miles | p (sum) | p (joint F, slik det ble rapportert) |
|---|--:|--:|--:|
| Kull | +27,0 % | 0,068 | <0,001 |
| Industri | +14,3 % | 0,26 | <0,001 |
| Befolkning | +16,6 % | <0,001 | <0,001 |
| Jordbruk (placebo) | −18,8 % | 0,33 | <0,001 |

At placeboen jordbruk også «slår ut» på joint F, viser at denne testen ikke skiller
noe fra noe.

**b) Timingplacebo.** Under kvadratisk trend passer kanalbestanden fem år *fram* i tid,
altså kanaler som ennå ikke var åpnet, like godt til kulldataene som dagens bestand
(t = 3,3 mot 3,2). Den laggede bestanden passer dårligere allerede fra ti år tilbake. En
forutsetning («precondition») skulle gitt motsatt mønster. Datering ved full ferdigstillelse
forklarer litt av dette, men ikke alt.

**c) Randomiseringsinferens.** Den årlige serien av nye kanalmiles forskyves sirkulært
innenfor 1700–1830 (130 placeboer som beholder de to bølgene og klumpetheten).

| Spesifikasjon | HAC-p (kull) | RI-p (kull) |
|---|--:|--:|
| Kvadratisk trend + krig | 0,001 | **0,22** |
| Lokal projeksjon, h = 10 | <0,001 | **0,38** |

En hvilken som helst bestand som akkumuleres mens kullproduksjonen akselererer, «predikerer»
kull. Kanalbestanden gjør det godt, men ikke unikt. Dose-respons-resultatet er derfor
*forenlig med* Tvedts sekvens, men det *tester* den ikke. Dette henger sammen med funnet i
Monte Carlo-arbeidet fra 11. september (dosen er 97,6 % kvadratisk trend), og det er
strengere enn det funnet: størrelseskorrigert p < 0,003 svarer på om bestanden passer bedre
enn trenden, ikke på om timingen betyr noe.

### Det som står seg

- **To regimer.** Aggregatet bryter i 1775–92 og per capita i 1818. Dette er deskriptivt og
  robust (sup-F langt over kritisk verdi), og jordbruk bryter ikke.
- **Dampens andel.** Damp stod for 6 % av installert stasjonær kraft i 1760, 21 % i 1800 og nådde paritet i
  1833 (Kanefsky/Crafts).
- **Rekkefølgen i trykte kilder.** Vann-bigrammer kommer før damp-bigrammer uansett
  glatting og referanseår.
- **Krigskonfunderingen i DiD.** 1807-bruddet skyldes det nederlandske sammenbruddet.
- **Forekomst.** Kull og befolkning beveger seg med kanalene, inntekt per innbygger gjør det
  ikke. Dette gjelder som assosiasjon.

## 3. Hva som er endret (`submission/02_journal_of_energy_history/manuscript_v2.md`)

Arbeidskopien bygger på JGH-teksten, og påstandene er rettet:

1. Abstract og innledning: «predicts» er erstattet med assosiasjon, og det står eksplisitt
   at dosen ikke identifiserer timing.
2. §4.2: tallene for førstedifferanser er rettet, jern er fjernet fra listen over
   signifikante utfall, og det er lagt til et nytt avsnitt med timingplacebo og RI.
3. §4.3: lokale projeksjoner er merket med RI-forbeholdet.
4. Diskusjon og konklusjon: «survives every specification» er fjernet (det sto tre steder).
5. Begrensninger: størrelseskorreksjonen (p < 0,003), minste påviselige effekt (42 %) og RI
   er lagt inn.
6. Tabell 3: p-verdiene for førstedifferanser gjelder nå summen.

Artikkelens tese flyttes dermed fra «dosen viser sekvensen» til «sekvensen vises i
bruddatoene, kraftbenchmarkene og trykte kilder, og dosen er forenlig med den». Tesen blir
svakere, men den tåler en fagfelle.

**Ikke gjort ennå (krever deg):**

- Tilpasse lengde og format til tidsskriftets retningslinjer. Energyhistory.eu var blokkert
  herfra, så grensene må sjekkes.
- Kutte JGH-spesifikk innramming (åpningen «in this journal»).
- Bygge .docx/PDF. `build_submission.py` peker fortsatt på JGH.

## 4. Anbefalte tidsskrifter

| # | Tidsskrift | Hvorfor | Forbehold |
|---|---|---|---|
| **1** | **Journal of Energy History / Revue d'histoire de l'énergie** | Den reelle debatten artikkelen tar del i er Wrigley–Allen–Malm–Pomeranz: rekkefølgen i energiomstillingen og «fossil economy». Tidsskriftet er tverrfaglig, har åpen tilgang uten forfatteravgift og bruker to fagfeller for Varia-artikler. Det aksepterer kvantitativ-deskriptiv historie uten krav om kausal identifikasjon. | Lengdegrense og referansestil må sjekkes på energyhistory.eu |
| 2 | Water History (IWHA/Springer) | Dette er Tvedts eget fagmiljø, og tesen er direkte relevant. Double-blind, abstract på 150–250 ord. | Lesere som er mindre kvantitative, så metodedelen bør kortes |
| 3 | Journal of Transport History (SAGE) | Tidsskriftet dekker kanaler og transportrevolusjonen, og Bogart-litteraturen publiseres der. | Maks 8 000 ord inkl. sluttnoter betyr at teksten må kuttes med rundt 40 % |

**Ikke nå:** Economic History Review, Explorations in Economic History, EREH og JEH. Når
RI-p er 0,22, vil de avvise på identifikasjon. De blir aktuelle først med et fylkespanel
der terreng gir eksogen variasjon i kanaltilgang (se Begrensninger §7.1).

### Egen metodeartikkel: Historical Methods

Artikkelen bør ta utgangspunkt i `expansion/` sammen med de nye testene. Poenget er at en
akkumulerende dose kan gi HAC-p = 0,001 og RI-p = 0,22 på samme data. Monte Carlo-arbeidet
(størrelse og styrke), timingplaceboen og RI-diagnostikken er et reelt metodebidrag.
Historical Methods tar artikler på 7 000–10 000 ord ekskl. noter, og krever at bidraget er
metodisk og ikke bare bruk av etablerte metoder. Den nye DiD-krigskonfunderingen passer
også her.

## 5. Oppfølging 26. september: full leveranse

Resultatet ligger i [`submission/02_journal_of_energy_history/`](../submission/02_journal_of_energy_history/):
et nytt manuskript på 6 557 ord, Word og PDF, følgebrev til JEH og JTH, tittelside og en anonymisert
replikasjonspakke.

Under arbeidet ble det funnet feil i selve kanaltabellen. Kennet & Avon var datert 1727, flere store
kanaler var datert etter Act-år eller første åpning i stedet for ferdigstillelse, og de sørwalisiske
kanalene manglet. Serien er rettet (24 endringer, alle dokumentert), og hele analysen er kjørt på
nytt (`docs/results_*_v2.txt`). Etter rettelsen er kull p = 0,003 med kvadratisk trend, altså akkurat
på den størrelseskorrigerte terskelen. Randomiserings-p er 0,34 og 0,41 i den lokale projeksjonen.
Konklusjonene i avsnitt 2 over gjelder uendret.
