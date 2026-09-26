# Innsending 2: *Floated before Fired*

Målet med versjonen er å gi størst mulig sjanse for publisering etter desk-avvisningen fra JGH
(22. september 2026). Bakgrunnen står i [`../../revision/2026-09-26_jgh_desk_rejection.md`](../../revision/2026-09-26_jgh_desk_rejection.md).

## Hva som er gjort

| | JGH-versjonen (avvist) | Denne versjonen |
|---|---|---|
| Innramming | Global historie: Tvedts spørsmål og fire land | Energihistorie: to klokker i Storbritannias energiomstilling |
| Kanalserie | Referansetabell ukorrigert (feil for Kennet & Avon, Oxford, Coventry m.fl.; sørwalisiske kanaler manglet) | 24 dokumenterte rettelser, 7 walisiske kanaler lagt til (`data/external/canal_corrections.csv`) |
| Dose-respons | «predicts coal … survives every specification» | Assosiasjon, med ærlig grense: timingplacebo og randomiseringsinferens (ny figur 3) |
| Førstedifferanser | p for joint F rapportert som om den gjaldt summen | p for summen |
| Størrelseskorreksjon | Ikke nevnt | p < 0,003 og minste påviselige effekt (~40 %) |
| Nytt bidrag | — | Tre-trinns sjekk for infrastruktur-som-forutsetning, overførbar til jernbane, strømnett og rørledninger |
| DiD | Egen seksjon, tabell og figur | Én setning i det komparative avsnittet |
| Lengde | 12 500 ord | 6 557 ord inkl. noter, tabeller og figurtekster (tekst 4 961, noter 940); abstract 143 |

Lengden er valgt slik at samme manuskript passer **både** Journal of Energy History og
Journal of Transport History (maks 8 000 ord inkl. noter, abstract < 150). Det kan dermed sendes
videre uten å skrives om hvis det første tidsskriftet sier nei.

## Filer

| Fil | Innhold | I git? |
|---|---|---|
| `manuscript.md` | Kilde (anonymisert) | ja |
| `manuscript.docx`, `manuscript.pdf` | Innsendingsfiler: Times 12, dobbel linjeavstand, 32 fotnoter, 4 figurer, 4 tabeller | ja |
| `replication_package_anonymous.zip` | 35 filer, anonymisert, kjørt på nytt fra bunnen med identiske resultater | nei (bygges med `build_replication.py`) |
| `title_page.*`, `cover_letter.*`, `cover_letter_jth.*` | Tittelside og følgebrev (JEH og JTH), med navn | nei (identifiserende) |
| `build.py`, `build_replication.py` | Bygger alt | ja |

```bash
python build.py && python build_replication.py
```

## Tidsskriftstige

1. **Journal of Energy History / Revue d'histoire de l'énergie.** Tidsskriftet har den beste faglige
   passformen: Wrigley, Malm, Allen og energiomstillingens kronologi. Det er diamond open access og
   bruker to fagfeller. *Retningslinjene kunne ikke leses herfra (nettstedet var blokkert), så sjekk
   lengde, referansestil og innsendingsmåte på energyhistory.eu før du sender.*
2. **The Journal of Transport History (SAGE).** Grensen på 8 000 ord inkl. noter og abstract under
   150 ord er bekreftet og oppfylt. `cover_letter_jth` er klar.
3. **Water History (IWHA/Springer).** Dette er Tvedts fagmiljø. Abstract må være 150–250 ord, så det
   må utvides litt.

Parallelt, som egen artikkel: **Historical Methods**, der metoden fra `expansion/` og
`src/methods/` er hovedbidraget.

## Sjekkliste før innsending (må gjøres av deg)

- [ ] **Kontroller kanalrettelsene** i `data/external/canal_corrections.csv` mot Hadfield. Datoene er
      standardopplysninger, men de er satt fra sekundærkunnskap og ikke slått opp side for side.
      Lengdene for de walisiske kanalene er runde tall. Resultatene er robuste for rettelsene (se
      `docs/results_regime_v1.txt` mot `_v2.txt`), men en fagfelle i kanalhistorie vil sjekke dem.
- [ ] Fyll inn tilknytning, postadresse, ORCID og biografi. Lag `author_config.ini` med seksjon
      `[author]` og nøklene `affiliation`, `postal_address`, `orcid`, `biography`, og kjør `build.py`
      på nytt.
- [ ] Sjekk retningslinjene til JEH: lengde, noter eller forfatter–år, og om figurer skal leveres som
      separate filer. Figurene ligger i `data/` i 300 dpi (`fig1`, `fig2`, `fig8` = figur 3, `fig4`).
- [ ] Åpne `manuscript.docx` i Word én gang for å kontrollere fotnoter og figurer.
- [ ] Følgebrevet nevner JGH-avvisningen åpent. Det er vanlig og ærlig, men du kan fjerne setningen
      hvis du vil.
