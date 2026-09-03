# Abstract

Britain's industrial take-off is usually dated by steam. This paper dates it by water. Combining annual British sectoral output, 1700–1870, with a new series of canal mileage by completion year, installed steam and water horsepower, and the Google Books British corpus, we show that Britain passed through two growth regimes. In the first, opening in 1775–1792 as the canal network was built, aggregate output, coal, iron and population accelerated while income per head did not. In the second, from 1818, steam raised income per head. Canal mileage predicts coal output over the following two decades but not per-capita income or agriculture; steam raises per-capita income only after 1830. In print, coal moves by barge before it burns in engines. We also show why cross-country difference-in-differences cannot detect the canal era: the Napoleonic collapse of continental controls masquerades as a British take-off. Water infrastructure was the precondition for a coal economy.

**Keywords:** Industrial Revolution, canals, coal, water infrastructure, growth regimes, Google Books Ngram, Great Divergence

**JEL Classification:** N13, N73, O14, O18, C22


---

# 1. Introduction

Every account of the British Industrial Revolution has to choose a clock. The steam clock starts in the 1780s with Watt's rotative engine and reads industrialisation as an escape from the organic economy into a mineral one (Wrigley 2010; Allen 2009). The canal clock starts in 1761, when the Duke of Bridgewater's canal halved the price of coal in Manchester, and reads the same century as a transport revolution that integrated markets long before factories filled with engines (Bogart 2014; Szostak 1991). The two clocks are rarely set against each other with data, because they measure different things. The steam clock is calibrated to income per head, which barely moved before 1830 (Crafts 1985; Crafts and Harley 1992). The canal clock is calibrated to tonnage, prices and towns.

This paper sets the two clocks side by side using annual British data and asks a narrower question than "which mattered more". Following Terje Tvedt's argument that Britain's water systems were the *precondition* for a coal economy rather than a rival to it (Tvedt 2010), we ask whether the timing, sequencing and sectoral incidence of British growth between 1700 and 1870 are consistent with water infrastructure enabling coal, and coal then enabling steam. A precondition claim is a claim about order and dependence. It predicts that the canal-served sectors accelerate before steam is a significant power source; that coal output responds to the canal network; that steam capacity follows coal; and that the sectors canals did not serve, and the outcome canals could not directly raise, do not move. Each of these is testable with series that already exist.

Three findings follow. First, Britain had two growth regimes, not one. Using the annual output series of Broadberry, Campbell, Klein, Overton and van Leeuwen, we find trend breaks between 1775 and 1792 in total output, industry, services, coal, iron and population, and a second break around 1818 in income per head. In the first regime, aggregate output growth roughly doubled and population growth quadrupled, while GDP per capita grew at the same 0.3 per cent a year it had grown since 1700. Population absorbed the acceleration. This reconciles the canal enthusiasts with the Crafts–Harley chronology: both are right, about different variables.

Second, the canal network is a dose that predicts the right things. We assemble a year-by-year series of canal miles from the completion dates of 155 British canals and corroborate its timing with 152 parliamentary authorisations transcribed from Priestley's 1831 survey. Cumulative canal mileage predicts coal output over the following five to twenty years and installed steam horsepower over fifteen to twenty, and it predicts population. It predicts neither income per head nor agricultural output. Steam horsepower, in turn, raises income per head only in samples that extend past 1830. In the language of the Google Books British corpus the same order appears: "coal barge" and "coal wharf" reach a quarter of their mid-century frequency in 1781 and 1800; "steam engine" in 1808 and "steam power" in 1826.

Third, the standard cross-country test of an eighteenth-century British take-off is broken by war, and we show how. A difference-in-differences on Maddison GDP per capita with France and the Netherlands as controls, which an earlier version of this paper reported, locates Britain's break in 1807. That date is the Dutch economy losing 44 per cent of its income per head under French occupation and blockade, while Britain, uninvaded, held level. Any two-group comparison that spans 1790–1815 will find a British "effect" whatever Britain did with its rivers. We retain the cross-country evidence only in benchmark years: between 1700 and 1820 Britain's total output grew 240 per cent, twice the next European economy, while also raising income per head, and it did so while steam supplied at most a fifth of its stationary power.

The contribution is therefore threefold. To the transport-revolution literature, we add an annual national dose series and a sequencing test that connects canals to the energy transition rather than to urban growth, the channel that Alvarez-Palau, Bogart, Satchell and Shaw-Taylor have recently quantified (Alvarez-Palau et al. 2024). To the energy-history debate between Wrigley, Allen, Pomeranz and Malm, we add the observation that the escape from the organic economy's Malthusian ceiling was under way, in aggregate, within the organic economy, powered by water and moved by water. To the growing practice of historical difference-in-differences (Roth et al. 2023), we add a worked example of how a control group's catastrophe becomes a treatment group's miracle. Finally, we show that a text-as-data index of infrastructure vocabulary tracks the physical stock of canals with a correlation of 0.91 and tracks the building rate not at all, which turns the Google Books corpus from an ornament into a measurement instrument for the built environment.

The paper proceeds as follows. Section 2 places the argument in the literature. Section 3 describes the data and the empirical strategy, including why we prefer linear local projections to machine-learning estimators for a single national time series. Section 4 reports the two regimes, the canal dose, the precondition chain, the semantic sequence, and the failure of the cross-country design. Section 5 discusses what the results mean for Tvedt's thesis and for the Great Divergence. Section 6 concludes and Section 7 sets out the limitations, which are real.


---

# 2. Water, coal and the chronology of British growth

## 2.1 The transport revolution and its canals

The transport revolution of eighteenth-century Britain is well documented and, until recently, poorly measured. Between the Bridgewater Canal of 1761 and the opening of the Liverpool and Manchester Railway in 1830, Parliament authorised roughly 165 canal companies and the navigable network grew from about 1,400 miles of improved river to some 4,000 miles of river and canal (Hadfield 1984; Bogart 2014). Contemporaries did not doubt why. Priestley's survey of 1831, written at the network's peak, opens its account of the Bridgewater Canal by noting that the Duke's "primary object" was "to open his valuable collieries at Worsley, and to supply the town of Manchester with coal, at a much cheaper rate" (Priestley 1831). Turnbull's regional study established the same point statistically: canals were built where coal was, they carried coal above all else, and the counties that acquired them saw coal output and population grow faster than those that did not (Turnbull 1987). Szostak went furthest, arguing that the transport improvements were a necessary condition for the factory system itself, since only wide markets could absorb the output of a mechanised mill (Szostak 1991).

Quantitative work has caught up in the last decade. Bogart's survey collects the mileage, cost and freight-rate evidence and concludes that inland freight costs fell by half or more between 1700 and 1830 (Bogart 2014). Alvarez-Palau, Bogart, Satchell and Shaw-Taylor, using a multi-modal transport network reconstructed in GIS, estimate that transport costs relative to producer prices fell by nearly 75 per cent between 1680 and 1830 and that, without that fall, inland towns would have been 20 to 25 per cent smaller in 1841 (Alvarez-Palau et al. 2024). Their outcome is urban population. Ours is the energy system. The two are complementary: towns grew where coal could be delivered, and coal could be delivered where water had been engineered.

## 2.2 Energy, the organic economy and the Great Divergence

The energy literature starts from a different place. Wrigley's organic economy is bounded by the annual product of the land; sustained growth required a "mineral-based energy economy" in which coal replaced wood, wind and water (Wrigley 1988; Wrigley 2010; Wrigley 2016). Allen's induced-innovation account makes cheap British coal and dear British labour the reason the steam engine was worth inventing in Britain and nowhere else (Allen 2009). Pomeranz gives coal a starring role in the Great Divergence, alongside the ghost acres of the Americas (Pomeranz 2000). Clark and Jacks and, more recently, Fernihough and O'Rourke have tested the coal hypothesis on prices, output and city growth and found that proximity to coal mattered a great deal for where Europe industrialised (Clark and Jacks 2007; Fernihough and O'Rourke 2021). Malm's *Fossil Capital* accepts coal's centrality but denies that its adoption was driven by thermodynamic superiority or scarcity of water power: steam won because it freed capital from the riverbank and allowed mills to be sited where labour could be disciplined (Malm 2016).

What these accounts share is a clock calibrated to steam and coal combustion. Tvedt's intervention is to move the clock upstream. In "Why England and not China and India?", he argues that Britain's distinctive endowment was not coal as such, which China had in abundance, but a hydrological regime of gentle gradients, steady flow and navigable rivers that could be engineered into a national network of canals and water-powered mills at low cost (Tvedt 2010). The monsoonal rivers of Asia could not. On this reading the water system is the precondition: it created the market integration, the cheap coal at the point of use, and the water-powered factory template on which steam later built. Tvedt's evidence is comparative and qualitative. This paper asks whether the annual British record supports the sequence he proposes.

A precondition is not a rival cause. Coal remains the fuel of the second regime and steam its engine. The claim is that neither would have arrived when and where it did without the first regime, and that the first regime is visible in the data if one looks at the variables canals could move: coal, aggregate output, and the number of people the economy could feed.

## 2.3 Two chronologies of growth

The macroeconomic chronology has moved decisively toward gradualism. Crafts, and Crafts and Harley, cut the growth rates of the 1780–1830 period that Deane and Cole had estimated and showed that income per head grew slowly until well into the nineteenth century (Crafts 1985; Crafts and Harley 1992). Broadberry, Campbell, Klein, Overton and van Leeuwen's reconstruction of British output from the medieval period confirms the picture: annual growth of GDP per head averaged around 0.3 per cent from 1700 to the 1820s and only then accelerated (Broadberry et al. 2015). Crafts' growth-accounting of steam finds its contribution to labour-productivity growth trivial before 1830 and dominant only after 1850 (Crafts 2004). Kanefsky's estimates of installed power, on which Crafts draws, put steam at 35,000 horsepower in 1800 against 120,000 for water wheels; steam did not overtake water until the 1830s (Kanefsky 1979; Kanefsky and Robey 1980).

Gradualism in income per head has been read as a verdict against any eighteenth-century take-off. It is not. The same Broadberry series show total output and population doubling between 1760 and 1830. A growth regime in which aggregate output accelerates while income per head does not is exactly what Malthus described and exactly what an infrastructure shock in an organic economy should produce: more mouths fed, not richer mouths. The distinction between the aggregate and the per-capita clock is, we argue, the key to reconciling the canal historians with the cliometricians.

## 2.4 Text as data and historical difference-in-differences

Two methodological literatures frame our tools. Michel et al. introduced the Google Books corpus as a quantitative record of culture, and Pechenick, Danforth and Dodds documented its limits: the corpus over-weights scientific and technical publishing, and frequencies track what was printed rather than what was said (Michel et al. 2011; Pechenick et al. 2015). We treat that bias as a feature. Technical vocabulary about canals is a record of canals, and we show below that it tracks the physical stock of the network closely.

The historical difference-in-differences literature has grown fast and grown cautious. Bertrand, Duflo and Mullainathan showed how serial correlation inflates significance in long panels (Bertrand, Duflo, and Mullainathan 2004); Roth, Sant'Anna, Bilinski and Poe survey the newer concerns about heterogeneous effects and pre-trends, and Rambachan and Roth offer tools for honest inference when parallel trends are doubtful (Roth et al. 2023; Rambachan and Roth 2023). Our contribution here is a case study of a more elementary hazard: a control group hit by a shock, war, that the treatment group escaped. Crouzet described the economic consequences of the Revolutionary and Napoleonic wars for the continent half a century ago (Crouzet 1964); the Maddison data now make it possible to see how large they were, and how completely they can be mistaken for a British take-off.


---

# 3. Data and empirical strategy

## 3.1 British output, population and power

Annual real output for Great Britain by sector, 1700–1870, comes from Broadberry, Campbell, Klein, Overton and van Leeuwen as published in the Bank of England's *Millennium of Macroeconomic Data* (Broadberry et al. 2015). We use total GDP, agriculture, industry and services, and from the industrial-production tables the physical output indices for coal, iron and textiles. Population of Great Britain is from the same source, based on Wrigley and Schofield's reconstitution to 1801 and the censuses thereafter. GDP per head is total output divided by population. The series are indices with 1700 equal to 100.

Installed stationary power is from Kanefsky's estimates as reported in Crafts's Table 3: steam horsepower of 5,000 in 1760, 35,000 in 1800, 160,000 in 1830 and 2.06 million in 1870; water horsepower of 70,000, 120,000, 160,000 and 230,000 at the same dates; wind 10,000, 15,000, 20,000 and 10,000 (Kanefsky 1979; Crafts 2004). Steam and water were at parity in 1830. We interpolate log-linearly between the four benchmarks. The interpolated series is smooth by construction, and we treat inference that depends on its year-to-year variation with corresponding caution.

## 3.2 The canal network as a dose

The treatment in the earlier version of this paper was a single date, 1761. The network it stood for was built over sixty years in two waves, and a binary indicator cannot distinguish the Grand Cross of the 1770s from the mania completions of 1800–1816. We therefore construct a continuous dose: cumulative canal miles in operation by year.

The primary series is assembled from the completion year and length of 155 canals in Great Britain, taken from the standard reference tables and totalling 2,967 miles, of which 2,320 were open by 1830. Where a canal opened in stages we use the year of full completion, which biases the series late by a few years relative to first use. The series excludes river navigations improved before 1700, which were the bulk of the network's initial 1,400 miles, so it measures additions to the network rather than its level. For the growth regressions this is the relevant quantity.

We corroborate the timing with an independent source. Priestley's *Historical Account of the Navigable Rivers, Canals, and Railways throughout Great Britain* records the Acts of Parliament that authorised each navigation, with regnal year and date of Royal Assent (Priestley 1831). From the digitised text we recover first-authorisation years for 152 navigations, including 70 canals authorised between 1760 and 1829. Thirty of those 70 were authorised in the 1790s. The authorisation series leads the completion series by roughly a decade, as it should, and both show the same two waves.

## 3.3 Cross-country data

Cross-country GDP per head is from the Maddison Project Database 2023 (Bolt and van Zanden 2024). For Britain, France, the Netherlands, Sweden, Germany, Spain and Portugal the series is annual from 1700; for Belgium, Italy, China, India and Japan it is interpolated between benchmarks and we use it only descriptively. Population in the Maddison database is a benchmark series before 1820, so cross-country total output is compared only at the benchmark years 1700, 1820 and 1870.

## 3.4 Text data

Word and phrase frequencies are from the Google Books Ngram corpus, British English 2019 edition, 1700–1900, with three-year smoothing (Michel et al. 2011). We use the 71-term vocabulary of the earlier version of this paper for the infrastructure index and add sixteen bigrams that name coal's mode of use: "coal barge", "coal wharf", "coal boat" and "canal boat" for coal moved by water; "steam engine", "steam power" and "steam boat" for coal burned in engines; and "fire engine", the eighteenth-century term for an atmospheric engine, as a check on terminological drift. Each bigram is indexed to its own 1850 frequency and the groups are equal-weighted averages of their members, so that a single common term cannot dominate.

## 3.5 Empirical strategy

Our questions are about timing, sequence and incidence within one national economy over 170 years. The sample is small, the series are smooth and trending, and the treatment is itself a slowly accumulating stock. We match the tools to those facts.

**Regime detection.** For each British series we estimate a linear trend in logs and test for a single break in level and slope at an unknown date using the Andrews sup-F statistic with 15 per cent trimming, and for two breaks by grid search (Andrews 1993; Bai and Perron 1998). We also fix the break at 1761 and test for a change in trend slope over 1700–1830 with Newey–West standard errors. Agriculture and GDP per head are designated placebo series in advance: canals did not carry harvests to any great extent, and a precondition operating through population should leave income per head unchanged.

**Dose-response.** We regress the log of each output series on cumulative canal mileage, in thousands of miles, and a linear trend over 1700–1830, the period before railways. Because a cumulative stock is itself a smooth, accelerating series, we report three further specifications that a sceptical reader would demand: a quadratic trend, a first-difference model with ten lags of new mileage, and a horse race that adds installed steam horsepower and a dummy for war years. Coefficients that survive all four are the ones we build on.

**Sequencing by local projection.** To test the chain water → coal → steam → income per head, we estimate local projections in the sense of Jordà (Jordà 2005): the change in the log outcome over horizons of one to twenty years is regressed on the regressor of interest, the outcome's own level, and a trend, with Newey–West errors. This gives the cumulative response of coal to the canal stock, of steam horsepower to the canal stock and to coal, and of income per head to canals and to steam, at each horizon, without imposing a parametric lag structure. Agriculture is again the placebo. We estimate the steam equations from 1760, when the horsepower series begins, and the income equations on both the 1760–1830 and the 1760–1870 samples, since the precondition thesis predicts that steam's per-capita effect appears only in the later one.

**Why not machine learning.** The earlier version of this paper reported a double/debiased machine-learning estimator on the cross-country panel. We do not use it for the within-Britain analysis. With 130 annual observations, tree-based learners fit the year trend closely enough to leave no treatment variation to estimate from, a failure mode we documented in that version, and linear learners with a quadratic trend reduce to the specifications above. A linear mediation decomposition with a moving-block bootstrap, which we also estimated, produces intervals that span zero for every path once a quadratic trend is absorbed; we report it in the replication materials as a negative result and rest the sequencing evidence on the local projections.

**Semantic sequencing.** For each bigram group we record the first year in which the five-year moving average reaches 10, 25 and 50 per cent of its 1850 level, and the year in which "steam engine" overtakes "fire engine" in print.

**Cross-country.** We re-estimate the two-way fixed-effects difference-in-differences of the earlier version on log GDP per head, with 1761 as treatment date and Newey–West errors, for three control groups and three sample windows, and its ten-year event-study version, in order to show what it measures. We then compare peak-to-trough drawdowns in GDP per head over 1785–1815 by country and report growth in total output and population between the Maddison benchmark years.


---

# 4. Results

## 4.1 Two growth regimes

Figure 1 plots the British series on a logarithmic scale with the two canal-building waves shaded. Panel (a) shows total output, population and income per head; panel (b) shows coal, industry and agriculture. The visual impression is of a fan opening after 1760: total output and population steepen together while income per head continues at its previous slope until the 1820s. Agriculture never steepens at all.

<div align="center">
  <img src="../../data/fig1_two_regimes.png" alt="Figure 1: Britain's two growth regimes" width="800">
  <br>
  <em><strong>Figure 1: Britain's two growth regimes.</strong> Annual indices, 1700 = 100, log scale. Shaded bands mark the first canal wave (1760–1780) and the canal-mania completions (1790–1816). Vertical lines at 1761 and 1818. Source: Broadberry et al. (2015) via Bank of England.</em>
</div>

Table 1 gives the trend growth rates by period. Between 1700–1760 and 1790–1815, growth of total output rose from 0.55 to 1.58 per cent a year, industry from 0.47 to 1.81, coal from 0.87 to 2.85 and population from 0.29 to 1.18. Income per head grew at 0.25 per cent a year in the first period and 0.40 in the third; the difference is within the noise of the series. Agriculture is flat throughout.

**Table 1: Trend growth of British series, per cent per year**

| Period | Total GDP | Industry | Coal | Services | Population | GDP per head | Agriculture |
|:--|--:|--:|--:|--:|--:|--:|--:|
| 1700–1760 | 0.55 | 0.47 | 0.87 | 0.50 | 0.29 | 0.25 | 0.75 |
| 1760–1790 | 0.82 | 1.16 | 2.05 | 0.83 | 0.74 | 0.08 | 0.60 |
| 1790–1815 | 1.58 | 1.81 | 2.85 | 2.02 | 1.18 | 0.40 | 0.81 |
| 1815–1830 | 1.98 | 3.64 | 2.84 | 1.62 | 1.49 | 0.50 | 0.63 |
| 1830–1870 | 2.35 | 2.85 | 3.57 | 2.62 | 1.16 | 1.19 | 0.78 |

*Source: authors' calculations from Broadberry et al. (2015). Slopes of log-linear trends fitted within each window.*

Table 2 formalises the comparison. Fixing the break at 1761 and estimating over 1700–1830, the trend slope of total output rises by 0.85 percentage points a year, industry by 1.42, coal by 1.62, iron by 3.24, services by 1.07 and population by 0.83, all with p-values below 0.01 under Newey–West errors. The slope of income per head changes by 0.02 points and that of agriculture by −0.04, neither distinguishable from zero. When the break date is left free, the single best break falls between 1777 (population) and 1792 (total output) for every canal-served series, and at 1818 for income per head. Allowing two breaks places the first at 1774–1775 for total output, industry and services and the second at 1818–1823. The data pick out the two regimes without being told where to look.

**Table 2: Change in trend slope at 1761 and data-chosen break dates**

| Series | Trend before 1761, % p.a. | Change after 1761, pp p.a. | p | Best single break | Best two breaks |
|:--|--:|--:|--:|--:|:--|
| Total GDP | 0.52 | +0.85 | <0.01 | 1792 | 1775, 1818 |
| Industry | 0.39 | +1.42 | <0.01 | 1789 | 1774, 1823 |
| Coal | 0.77 | +1.62 | <0.01 | 1784 | 1741, 1798 |
| Iron | 0.26 | +3.24 | <0.01 | 1786 | — |
| Services | 0.44 | +1.07 | <0.01 | 1786 | 1775, 1844 |
| Population | 0.23 | +0.83 | <0.01 | 1777 | 1730, 1783 |
| *GDP per head* | 0.29 | +0.02 | 0.82 | 1818 | 1720, 1818 |
| *Agriculture* | 0.82 | −0.04 | 0.84 | 1728 | — |

*Slope-change regressions on 1700–1830 with Newey–West (10 lags) errors. Break searches on 1700–1870, Andrews sup-F with 15 per cent trimming and two-break grid search with minimum segment of 20 years.*

The arithmetic of the first regime is simple. Between 1760 and 1815 the growth of total output rose by about a percentage point a year and the growth of population rose by about a percentage point a year. The economy grew faster and fed more people at the same income. In an organic economy that is the Malthusian outcome; what is unusual is that it continued for half a century without the income per head falling, and that it coincided with the doubling of coal output per head, from an index of 100 in 1700 to 202 in 1790 and 246 in 1800.

## 4.2 The canal network as a dose

Figure 2 shows the canal series. Panel (a) gives miles opened per decade: 117 in the 1760s, 353 in the 1770s, a lull of 83 in the 1780s, then 549 in the 1790s, 479 in the 1800s and 344 in the 1810s. Panel (b) gives the cumulative stock, from 218 miles in 1760 to 772 in 1790, 1,487 in 1800 and 2,320 in 1830. Panel (c) gives coal output per head. The correspondence between the two waves and the two steepenings of coal per head is visible to the eye; the regressions ask whether it survives detrending.

<div align="center">
  <img src="../../data/fig2_canal_dose.png" alt="Figure 2: The canal network and coal" width="800">
  <br>
  <em><strong>Figure 2: The canal network and coal.</strong> (a) Canal miles opened per decade, 155 canals by completion year. (b) Cumulative canal miles since 1700. (c) Coal output per head, 1700 = 100, with the year steam overtook water and wind as a source of stationary power. Sources: canal tables; Broadberry et al. (2015); Kanefsky (1979) via Crafts (2004).</em>
</div>

Table 3 reports the dose-response regressions over 1700–1830. In the simplest specification, log output on a linear trend and the canal stock, a thousand miles of canal is associated with 47 per cent more coal, 40 per cent more industrial output, 99 per cent more iron, 32 per cent more services and 24 per cent more population, and with no change in income per head or agriculture. The sceptical specifications thin this out. With a quadratic trend, only coal retains a large and significant coefficient, 30 per cent per thousand miles, with population marginal at 4 per cent; industry and total output are indistinguishable from the trend. In first differences with ten lags of new mileage, coal, industry and population respond and total output, income per head and agriculture do not. In the horse race with steam horsepower and war years, coal's canal coefficient is 41 per cent against a steam coefficient of 13 per cent that is not significant; for industry and population the two are of similar size and both significant.

**Table 3: Canal stock and British output, 1700–1830 (per 1,000 canal miles)**

| Outcome (log) | Linear trend | Quadratic trend | First differences, 10-year cumulative | Horse race: canal | Horse race: steam hp |
|:--|--:|--:|--:|--:|--:|
| Coal | +46.5% (p<0.001) | +29.8% (p=0.001) | +27.0% (p<0.001) | +40.8% (p<0.001) | +12.6% (p=0.08) |
| Industry | +40.1% (p<0.001) | −0.9% (p=0.89) | +14.3% (p<0.001) | +28.8% (p<0.001) | +30.4% (p=0.003) |
| Iron | +99.3% (p<0.001) | — | — | +88.2% (p<0.001) | +35.6% (p=0.17) |
| Population | +24.0% (p<0.001) | +4.1% (p=0.07) | +16.6% (p<0.001) | +18.6% (p<0.001) | +15.0% (p<0.001) |
| Total GDP | +24.7% (p<0.001) | +2.2% (p=0.52) | +4.2% (p=0.25) | +18.8% (p<0.001) | +19.0% (p<0.001) |
| *GDP per head* | +0.8% (p=0.69) | −1.9% (p=0.61) | −12.4% (p=0.33) | +0.2% (p=0.94) | +4.0% (p=0.08) |
| *Agriculture* | −0.5% (p=0.90) | −5.1% (p=0.56) | −18.8% (p<0.001) | −1.5% (p=0.72) | +7.3% (p=0.07) |

*Newey–West errors with 10 lags. Steam horsepower is the log of the interpolated Kanefsky series, indexed to 1830. The horse race includes a dummy for 1756–63, 1775–83 and 1793–1815.*

Two features of Table 3 matter for the argument. The first is that coal is the robust channel. It is also the channel the mechanism predicts, since the canals were dug to move it. The second is that the placebo rows behave. Income per head does not respond to canals in any specification, and agriculture's only significant coefficient is negative, in first differences, which is the structural shift away from farming rather than an effect on farming. We note, and return to in Section 7, that the reverse regression is not empty: past growth in coal, total output and population predicts subsequent canal openings. Canals were built where demand was growing. The dose is not exogenous, and we do not claim that it is; what we claim is that its timing and incidence are those of a precondition.

## 4.3 The precondition chain

Figure 3 reports the local projections that test the sequence directly. Each panel shows the cumulative response of the outcome, in log points, to a unit of the regressor, at horizons of one to twenty years, with 95 per cent Newey–West bands.

<div align="center">
  <img src="../../data/fig3_local_projections.png" alt="Figure 3: Local projections along the precondition chain" width="800">
  <br>
  <em><strong>Figure 3: Local projections along the precondition chain.</strong> Cumulative log response at horizons 1–20 years, per 1,000 canal miles or per log point of the regressor, controlling for the outcome's level and a trend. Samples 1700–1830 for canal regressors, 1760–1830 where steam horsepower enters. Shaded: 95 per cent HAC bands.</em>
</div>

The top-left panel is the first link: a thousand miles of canal raises coal output by 29 per cent after five years, 38 per cent after ten and 44 per cent after fifteen, with the whole path bounded away from zero. Controlling for contemporaneous steam horsepower, estimated from 1760, the canal effect on coal remains at 21 per cent over five to ten years and fades at fifteen to twenty, where steam takes over. The top-middle panel is the second link: canal stock predicts installed steam horsepower over fifteen to twenty years. The coefficient is small in log points because horsepower grew fifty-fold over the sample, but it is precisely estimated; we flag that the horsepower series is interpolated between five benchmarks, so this panel establishes ordering rather than magnitude. The top-right panel, coal to steam, is positive at every horizon but significant only at five years. On the interpolated series that is as much as can be asked.

The bottom row is the test that distinguishes a precondition from a cause. Canal stock has no effect on income per head at any horizon (bottom-left); the point estimates are negative and the bands include zero throughout. Steam horsepower has no effect on income per head either when the sample stops at 1830 (bottom-middle), but on the 1760–1870 sample it raises income per head by 0.55 log points per log point of horsepower after five years and 0.90 after twenty, all with p-values below 0.001. Steam's per-capita dividend is a post-1830 phenomenon. Canals raise coal and population (the population response is 3 to 7 per cent per thousand miles over five to twenty years, all significant) and leave income per head where it was. The bottom-right panel, agriculture, is negative at intermediate horizons, again the composition effect, and returns to zero.

The chain, read from Figure 3, is: canals raise coal within a decade; canals and coal are followed by steam capacity over one to two decades; steam raises income per head, but only once it is the majority power source. Water first, coal second, steam third, income last.

## 4.4 How much power was steam?

The precondition thesis requires that the first regime run on water rather than steam. Table 4 uses the Kanefsky benchmarks to check. In 1760 steam supplied about 6 per cent of Britain's stationary power; in 1800, when the first regime was thirty years old and the mania canals were opening, 21 per cent; in 1830 it had reached parity with water, at 47 per cent of the total. Steam overtook water and wind combined in 1833, fifteen years after the per-capita break. Over the same period coal output per unit of installed steam horsepower fell from 100 to 37: most of the coal being dug in 1800 was not being burned in engines. It was being carried, largely by water, to hearths, forges, kilns and salt pans.

**Table 4: Installed stationary power in Britain, thousands of horsepower**

| Year | Steam | Water | Wind | Steam share | Coal output per steam hp (1760 = 100) |
|:--|--:|--:|--:|--:|--:|
| 1760 | 5 | 70 | 10 | 6% | 100 |
| 1800 | 35 | 120 | 15 | 21% | 37 |
| 1830 | 160 | 160 | 20 | 47% | 19 |
| 1870 | 2,060 | 230 | 10 | 90% | 6 |

*Source: Kanefsky (1979, p. 338) as reported in Crafts (2004, Table 3); coal output from Broadberry et al. (2015). Shares from log-linear interpolation between benchmarks.*

## 4.5 The semantic sequence

If coal moved by water before it burned in engines, the language of the period should say so. Table 5 records, for each term or group, the first year in which its smoothed frequency in the British corpus reached 10, 25 and 50 per cent of its 1850 level. "Canal" reaches a quarter of its mid-century frequency in 1763, the year after the Bridgewater opening; "coal barge" in 1781; "coal wharf" in 1800. "Steam engine" reaches the same threshold in 1808, "steam power" in 1826, and "coal field", the geologist's term, in 1820. The coal-by-water group as a whole crosses 25 per cent in 1800, the coal-by-steam group in 1811. "Steam engine" overtakes "fire engine", the older name for the same machine, in 1800, which dates the terminological consolidation of steam to the decade after the canal mania. Figure 5 plots the three indices.

**Table 5: Year in which print frequency first reaches a share of its 1850 level (British English corpus, 5-year mean)**

| Term or group | 10% | 25% | 50% |
|:--|--:|--:|--:|
| "canal" | 1743 | 1763 | 1809 |
| "coal barge" | 1753 | 1781 | 1783 |
| "coal wharf" | 1774 | 1800 | 1815 |
| Coal-by-water group | 1780 | 1800 | 1817 |
| "steam engine" | 1800 | 1808 | 1821 |
| Coal-by-steam group | 1806 | 1811 | 1813 |
| "coal field" | 1788 | 1820 | 1831 |
| "steam power" | 1821 | 1826 | 1831 |

<div align="center">
  <img src="../../data/fig5_semantic_sequence.png" alt="Figure 5: The semantic sequence" width="800">
  <br>
  <em><strong>Figure 5: In print, coal travels by water before it is burned in engines.</strong> Five-year moving averages indexed to 1850 = 100. Coal-by-water: equal-weighted "coal barge", "coal wharf", "coal boat", "canal boat". Coal-by-steam: "steam engine", "steam power", "steam boat". Source: Google Books Ngram, eng_gb_2019.</em>
</div>

The corpus also tells us what kind of thing the infrastructure vocabulary measures. The frequency of "canal" correlates at 0.91 with the cumulative mileage of canals in existence over 1740–1850 and at −0.04 with the mileage opened in the surrounding decade. Print records the network that exists, not the digging. The 1766 crossover between engineered and naturalistic water vocabulary that the earlier version of this paper reported is, on this reading, the corpus registering the first wave of openings, and the vocabulary index can be used as a proxy for infrastructure in place where physical series are missing.

## 4.6 Why the cross-country test fails

The earlier version of this paper estimated a two-way fixed-effects difference-in-differences on Maddison GDP per head, treating Britain from 1761 against France and the Netherlands, and reported a treatment effect of 1,251 international dollars with a Newey–West p-value of 0.042. We reproduce that estimate exactly. We then ask when the gap between Britain and its controls actually opened. A sup-F search on the log gap places the single break in 1807, with the next-best candidates 1805–1809. The event study of the earlier version is consistent: no post-1761 bin is significant until the one beginning 45 years after treatment.

Figure 4(a) shows what happened in 1807. Britain's income per head, indexed to 1790, stood at 106 in 1805 and 110 in 1815. The Netherlands' fell from 100 in 1805 to 63 in 1808 and was still at 72 in 1815. Table 6 gives the drawdowns for the whole panel. Between the late 1780s and the Napoleonic trough the Netherlands lost 44 per cent of its income per head, Portugal 48, Sweden 27, France 22 and Spain 13. Britain lost 1.4 per cent. The 1761 "treatment effect" measured against a continental control group is, to a first approximation, the difference between being blockaded and doing the blockading. Of the growth in the level gap between 1761 and 1900 that the earlier version's counterfactual attributed to the canal era, 39 per cent occurs in the war years 1790–1815 alone.

**Table 6: GDP per head, peak 1785–95 to trough 1795–1815 (Maddison 2023, 2011 international dollars)**

| Country | Peak | Trough | Drawdown | 1815 relative to 1790 |
|:--|--:|--:|--:|--:|
| Britain | 3,207 (1795) | 3,161 (1798) | −1.4% | +13.6% |
| Netherlands | 4,666 (1794) | 2,632 (1808) | −43.6% | −28.3% |
| Portugal | 2,063 (1785) | 1,072 (1811) | −48.0% | −24.1% |
| Sweden | 1,661 (1791) | 1,221 (1809) | −26.5% | −11.9% |
| France | 2,016 (1788) | 1,580 (1801) | −21.7% | +1.3% |
| Spain | 1,454 (1790) | 1,265 (1811) | −13.0% | +3.2% |
| Germany | 1,820 (1792) | 1,725 (1805) | −5.2% | +8.1% |

<div align="center">
  <img src="../../data/fig4_war_confound.png" alt="Figure 4: Why the cross-country DiD fails" width="800">
  <br>
  <em><strong>Figure 4: Why a cross-country difference-in-differences on GDP per head cannot identify a canal-era effect.</strong> (a) GDP per head, 1790 = 100, for Britain, France and the Netherlands, with the war years shaded and the estimated break in the Britain–controls gap. (b) Britain's log GDP per head relative to two control groups, normalised to 1751–60. Source: Maddison Project Database 2023.</em>
</div>

Changing the control group does not rescue the design. Figure 4(b) plots Britain's log gap relative to the Netherlands and France and relative to France, Sweden, Germany and Spain, normalised to 1751–60. Against the second group Britain's relative position rises in the 1760s and again in the 1790s, but it was also rising from 1700 to 1720, so the pre-treatment bins of the event study are significantly negative and parallel trends fail in the opposite direction. The 1790s step is again a control-side collapse. And underneath all of this is the fact established in Section 4.1: Britain's own income per head grew at 0.08 per cent a year between 1760 and 1790. There was no canal-era per-capita acceleration for any control group to reveal. The difference-in-differences was measuring the right country with the wrong variable in the wrong decade.

## 4.7 The pre-steam divergence in benchmark years

What the cross-country data can establish is the aggregate divergence, and they establish it at benchmark years where population is measured rather than interpolated. Table 7 gives growth between 1700 and 1820, which is before steam supplied a quarter of British power. Britain's total output grew 240 per cent. The next European economy, Germany, grew 124 per cent; France 50; the Netherlands 9. Britain's population grew 148 per cent, more than any European country except Sweden's 104, and Britain alone among them combined that population growth with a rise in income per head of 37 per cent. Figure 6 juxtaposes this with the power benchmarks.

**Table 7: Growth between Maddison benchmark years, per cent**

| | GDP per head 1700–1820 | Population 1700–1820 | Total GDP 1700–1820 | GDP per head 1820–1870 |
|:--|--:|--:|--:|--:|
| Britain | +37 | +148 | +240 | +76 |
| Germany | +35 | +66 | +124 | +44 |
| Belgium | +8 | +72 | +85 | +82 |
| Spain | +22 | +39 | +69 | +16 |
| France | +3 | +46 | +50 | +65 |
| Sweden | −29 | +104 | +44 | +52 |
| Netherlands | −11 | +23 | +9 | +47 |
| China | −43 | +176 | +58 | +7 |

<div align="center">
  <img src="../../data/fig6_power_benchmark.png" alt="Figure 6: Steam was a minority power source when the aggregate divergence was established" width="800">
  <br>
  <em><strong>Figure 6: Steam was a minority power source when Britain's aggregate divergence was already established.</strong> (a) Installed steam and water horsepower, thousands, log scale. (b) Growth of total real GDP 1700–1820. Sources: Kanefsky (1979) via Crafts (2004); Maddison Project Database 2023.</em>
</div>

The Dutch row deserves attention because it is the comparative case Tvedt's argument needs. The Netherlands had the densest network of engineered waterways in Europe by the 1660s, a barge system that de Vries has described as the first scheduled public transport in the world (de Vries 1978). It had no coal. Its total output grew 9 per cent in 120 years. Water infrastructure without coal to move was not sufficient. Belgium, which had both coal and canals, was the first continental economy to industrialise. Britain had both, and the water to make the coal cheap at the point of use.


---

# 5. Discussion

## 5.1 Floated before fired

The results describe an economy that changed gear twice. The first change, in the 1770s and 1780s, was in the quantity of things: coal dug, iron smelted, goods made, people fed. The second, after 1818, was in the quantity per person. The first coincided with the building of the canal network and ran on water power and horse-drawn barges; the second coincided with steam becoming the majority power source. Coal is the hinge between them. Its output per head doubled during the first regime, when a fifth or less of it was going into engines, and it is the one outcome whose response to the canal stock survives every specification we can devise.

This is Tvedt's sequence in the annual record. Britain's water system did not compete with coal; it delivered coal. The Bridgewater Canal existed to bring the Worsley pits to Manchester. The Grand Cross joined the Trent, Mersey, Severn and Thames so that Staffordshire coal and Cheshire salt could reach the ports. The mania canals of the 1790s ran, disproportionately, from coalfields to towns. The result was a country in which, by 1800, coal was cheap far from the pithead in a way it was nowhere else in Europe, and in which the population that cheap heat and cheap freight could support had grown by half. The steam engine then found, ready-made, a market for its output, a fuel supply at its door, a factory system already organised around water wheels, and a financial and legal template in the canal company for raising capital by Act of Parliament. It did not have to create any of these. It had to improve on a prime mover that was, in 1800, three times its size.

## 5.2 What the first regime was, and was not

The first regime was not a rise in living standards. Income per head did not move, and the local projections show that canals did not move it. It was a rise in carrying capacity: the same income for half again as many people, sustained for two generations without the Malthusian check that had ended every earlier expansion. Wrigley's organic economy escaped its ceiling in aggregate before it escaped it per head, and it did so with organic power, by lowering the cost of moving the one mineral input that mattered (Wrigley 1988; Wrigley 2016). Tvedt's phrase for this is geographical symbiosis: growth by cooperating with the landscape's gradients and flows rather than overriding them. The data make the phrase concrete. The engineered river carried the coal that the engine would later burn.

This also disposes of a false choice. Malm argues that the transition from water to steam power in the 1830s and 1840s was driven by the spatial and disciplinary needs of capital rather than by the exhaustion of water (Malm 2016). Our results are consistent with that and add a prior stage to it: before steam could be chosen over water for its portability, water had to have created the markets and the fuel supply that made a portable prime mover worth having. Allen's induced-innovation story likewise needs coal to be cheap where engines were built (Allen 2009); the canals are a large part of why it was.

## 5.3 The two clocks reconciled

The cliometric revision of the 1980s established that income per head grew slowly until 1830 and has been read as denying an eighteenth-century take-off (Crafts 1985; Crafts and Harley 1992). Our results accept the revision and deny the reading. There was a take-off in the eighteenth century; it was an aggregate one, and it was absorbed by population. The canal historians and the growth accountants have been measuring different variables and talking past each other. Table 2 shows both clocks at once: total output, industry, coal and population break between 1775 and 1792; income per head breaks in 1818. Crafts's finding that steam's contribution to productivity growth is negligible before 1830 and large after 1850 is the second regime seen from the supply side (Crafts 2004). Our finding that steam horsepower raises income per head only in samples extending past 1830 is the same regime seen from the demand side.

## 5.4 The Great Divergence and the Netherlands

For the Great Divergence debate the precondition framing sharpens the comparison. Pomeranz's question is why Britain and not the Yangzi delta; Tvedt's is why Britain and not the Netherlands, which had the waterways, or China and India, which had the coal and the rivers but rivers of the wrong kind (Pomeranz 2000; Tvedt 2010). The benchmark data speak to the Dutch half of the question. The Netherlands had engineered water and no coal, and its total output grew 9 per cent between 1700 and 1820. Belgium had coal and built canals, and led the continent. Britain had coal, built canals, and had a hydrology that made canal building cheap. The Dutch case shows that water infrastructure was not sufficient; the Belgian and British cases show that where it met coal it was decisive; and the Chinese case, with its 176 per cent population growth and 43 per cent fall in income per head, shows what a Malthusian regime without cheap coal at the point of use looked like. The precondition was a match between two geographies, not either one alone.

## 5.5 A caution for historical difference-in-differences

Section 4.6 is a methodological result and we state it as one. Cross-country difference-in-differences in the long eighteenth century is exposed to a confound that has nothing to do with parallel trends in the usual sense: the control group went to war on its own territory and the treatment group did not. The Netherlands lost 44 per cent of its income per head, Portugal 48, and Britain lost nothing. A comparison spanning 1790–1815 will attribute the difference to whatever the British treatment happens to be, whether canals, enclosure, the Bank of England or the Book of Common Prayer. The remedies are the ones we have applied: locate the break before interpreting the coefficient, examine the controls' own series, prefer within-country evidence where the treatment is national, and use cross-country data at benchmark years for the aggregate question they can answer. We add this case to the catalogue that Roth and co-authors have assembled (Roth et al. 2023) not because the estimator is at fault but because the history is.

## 5.6 Text as instrument

The text-as-data component of this paper began as a way of dating a cultural shift and ends as a way of measuring a physical stock. That "canal" tracks the mileage of canals in existence with a correlation of 0.91, and the building rate not at all, means that the Google Books corpus behaves, for infrastructure vocabulary, like an inventory. This has two uses. Where physical series are missing, a vocabulary index can stand in for the stock, with the technical-publishing bias that Pechenick and co-authors identify working in the index's favour rather than against it (Pechenick et al. 2015). And where physical series exist, as here, the corpus can date the *use* of the stock in a way mileage cannot: "coal barge" in 1781 and "coal wharf" in 1800 record coal on the water; "steam engine" in 1808 and "steam power" in 1826 record coal in the engine. The order in the language is the order in the economy.


---

# 6. Conclusion

Britain industrialised on two clocks. The first, set in the 1770s, measured how much the economy produced and how many people it fed; the second, set around 1818, measured how much each of them had. The first ran on water. Canals carried the coal, water wheels drove the mills, and the aggregate economy accelerated while steam supplied a twentieth and then a fifth of its power. The second ran on steam, and it was steam that finally raised income per head. Coal connects the two: its output per head doubled in the first regime, mostly to be burned in hearths and furnaces rather than engines, and it is the one variable whose response to the canal network survives every test.

This is what a precondition looks like in data. Water infrastructure did not cause the Industrial Revolution in the sense of raising British incomes; it did not, and the local projections say so. It made the coal economy possible by making coal cheap far from the pit, and it made the population that would work in the steam economy possible by feeding it at constant income for two generations. Tvedt's argument that Britain's water systems were the enabling condition for its coal-based industrialisation is, on the annual British record from 1700 to 1870, correct in its sequence, correct in its sectoral incidence, and correct in its comparative implication: the Netherlands, with water and no coal, did not industrialise, and China, with coal and the wrong rivers, did not either.

Three things follow for how the period is studied. The distinction between aggregate and per-capita growth should be made explicit in any account of the eighteenth century, because the two chronologies that have divided the literature are chronologies of different variables. Cross-country difference-in-differences spanning the Revolutionary and Napoleonic wars should be read with the controls' own histories in view, because the largest economic event of the period happened to the control group. And the digitised print record, used with care, can measure the built environment and date its use; in this case it dates the coal barge a generation before the steam engine.

The fossil economy was floated before it was fired. That is a claim about order, and the order is in the data.


---

# 7. Limitations

The argument rests on timing, sequence and incidence in a single national time series, and it carries the limitations of that design.

## 7.1 The dose is endogenous

Canals were built where coal and people were. The reverse regressions confirm it: ten years of past growth in coal, total output or population predicts subsequent canal openings, with joint p-values of 0.002 to 0.03. The dose-response coefficients in Table 3 are therefore not causal effects of an exogenous treatment. What the design can establish is that the canal stock precedes coal output by five to twenty years in the local projections, that the relationship survives a quadratic trend for coal but not for industry or total output, and that the placebo series do not respond. Turnbull's regional evidence and Alvarez-Palau, Bogart, Satchell and Shaw-Taylor's market-access estimates supply the cross-sectional identification this paper lacks (Turnbull 1987; Alvarez-Palau et al. 2024); a county panel joining the Cambridge Group's waterway reconstruction to coal output and population is the natural next step, and we have not taken it.

## 7.2 The canal series is provisional

The mileage series is built from published reference tables of 155 canals by completion year. It omits river navigations improved before 1700 and minor branches, and it dates staged openings to their completion. Priestley's authorisation dates corroborate the two waves independently, but they were recovered from optical character recognition of an 1831 text and only 152 of his roughly 300 entries yielded a parseable regnal year. A definitive series would come from the Cambridge Group's *Inland Waterways of England and Wales, 1600–1948* dataset, which records opening and closing dates by section, or from a full transcription of Priestley's lengths. Our magnitudes per thousand miles should be read with that in mind; the timing is less fragile than the coefficients.

## 7.3 Steam horsepower is interpolated

Kanefsky's estimates exist at four benchmark dates within our sample (1760, 1800, 1830, 1870). The interpolated annual series is log-linear between them, so the local projections involving steam identify ordering across benchmarks rather than annual dynamics, and their standard errors understate the true uncertainty. Replacing the interpolation with the engine counts by decade in Kanefsky and Robey would tighten the second and third links of the chain (Kanefsky and Robey 1980). The finding that steam raises income per head only on the sample extending past 1830 does not depend on the interpolation; it follows from the 1818 break in income per head and the 1833 crossover in installed power.

## 7.4 Agriculture is an imperfect placebo

Agriculture's response to the canal stock is negative and significant at ten to fifteen years in the local projections and in first differences. We interpret this as compositional: labour and capital moved out of farming as canal-served sectors grew. It is not, strictly, a null result, and a reader who prefers a cleaner placebo can substitute income per head, which is null in every specification.

## 7.5 Text frequencies measure print, not speech

The Google Books corpus over-represents technical and legal publishing, and its British-English sub-corpus is small in the eighteenth century, so bigram frequencies before 1770 are noisy. We use thresholds of the 1850 level rather than absolute frequencies for that reason, and we use groups of terms rather than single terms where we can. "Coal barge" reaching a quarter of its mid-century frequency in 1781 is robust to the smoothing window; the exact year is not.

## 7.6 What the cross-country data cannot do

Population in the Maddison database is interpolated between 1700 and 1820, so cross-country regressions on total output over that period are not legitimate and we have not run them. The benchmark comparison in Table 7 is descriptive. The war-drawdown result in Section 4.6 is robust to the choice of controls because it is a property of the controls, but it means that the cross-country per-capita evidence for a British take-off before 1815 is, in our reading, unrecoverable from the Maddison series with any difference-in-differences design.

## 7.7 The earlier version of this paper

An earlier version reported the 1761 difference-in-differences of Section 4.6 as its central estimate, together with a counterfactual attributing 47 per cent of Britain's 1900 lead over the continent to the period before 1810. We withdraw both. The estimate is reproduced exactly and is an artefact of the Napoleonic collapse of the control group; the counterfactual inherits the artefact. We have kept the analysis in the paper because the failure is instructive and because the replication materials of the earlier version remain public.


---

# 8. References

Allen, Robert C. 2009. *The British Industrial Revolution in Global Perspective*. Cambridge: Cambridge University Press.

Alvarez-Palau, Eduard J., Dan Bogart, Max Satchell, and Leigh Shaw-Taylor. 2024. "Transport and Urban Growth in the First Industrial Revolution." *The Economic Journal* 135 (668): 1191–1228. https://doi.org/10.1093/ej/ueae111.

Andrews, Donald W. K. 1993. "Tests for Parameter Instability and Structural Change with Unknown Change Point." *Econometrica* 61 (4): 821–856.

Bai, Jushan, and Pierre Perron. 1998. "Estimating and Testing Linear Models with Multiple Structural Changes." *Econometrica* 66 (1): 47–78.

Bertrand, Marianne, Esther Duflo, and Sendhil Mullainathan. 2004. "How Much Should We Trust Differences-in-Differences Estimates?" *Quarterly Journal of Economics* 119 (1): 249–275.

Bogart, Dan. 2014. "The Transport Revolution in Industrialising Britain: A Survey." In *The Cambridge Economic History of Modern Britain, Volume 1: 1700–1870*, edited by Roderick Floud, Jane Humphries, and Paul Johnson, 368–391. Cambridge: Cambridge University Press. https://doi.org/10.1017/CHO9781139815017.014.

Bolt, Jutta, and Jan Luiten van Zanden. 2024. "Maddison-Style Estimates of the Evolution of the World Economy: A New 2023 Update." *Journal of Economic Surveys* 39 (2): 631–671. https://doi.org/10.1111/joes.12618.

Broadberry, Stephen, Bruce M. S. Campbell, Alexander Klein, Mark Overton, and Bas van Leeuwen. 2015. *British Economic Growth, 1270–1870*. Cambridge: Cambridge University Press.

Clark, Gregory, and David Jacks. 2007. "Coal and the Industrial Revolution, 1700–1869." *European Review of Economic History* 11 (1): 39–72.

Crafts, Nicholas F. R. 1985. *British Economic Growth during the Industrial Revolution*. Oxford: Clarendon Press.

Crafts, Nicholas F. R. 2004. "Steam as a General Purpose Technology: A Growth Accounting Perspective." *The Economic Journal* 114 (495): 338–351. https://doi.org/10.1111/j.1468-0297.2003.00200.x.

Crafts, Nicholas F. R., and C. Knick Harley. 1992. "Output Growth and the British Industrial Revolution: A Restatement of the Crafts–Harley View." *Economic History Review* 45 (4): 703–730.

Crouzet, François. 1964. "Wars, Blockade, and Economic Change in Europe, 1792–1815." *Journal of Economic History* 24 (4): 567–588.

de Vries, Jan. 1978. *Barges and Capitalism: Passenger Transportation in the Dutch Economy, 1632–1839*. Utrecht: HES Publishers.

Fernihough, Alan, and Kevin Hjortshøj O'Rourke. 2021. "Coal and the European Industrial Revolution." *The Economic Journal* 131 (635): 1135–1149.

Hadfield, Charles. 1984. *British Canals: An Illustrated History*. 7th ed. Newton Abbot: David and Charles.

Jordà, Òscar. 2005. "Estimation and Inference of Impulse Responses by Local Projections." *American Economic Review* 95 (1): 161–182.

Kanefsky, John W. 1979. "The Diffusion of Power Technology in British Industry, 1760–1870." PhD thesis, University of Exeter.

Kanefsky, John, and John Robey. 1980. "Steam Engines in 18th-Century Britain: A Quantitative Assessment." *Technology and Culture* 21 (2): 161–186.

Landes, David S. 1969. *The Unbound Prometheus: Technological Change and Industrial Development in Western Europe from 1750 to the Present*. Cambridge: Cambridge University Press.

Malm, Andreas. 2016. *Fossil Capital: The Rise of Steam Power and the Roots of Global Warming*. London: Verso.

Michel, Jean-Baptiste, Yuan Kui Shen, Aviva Presser Aiden, Adrian Veres, Matthew K. Gray, and Erez Lieberman Aiden. 2011. "Quantitative Analysis of Culture Using Millions of Digitized Books." *Science* 331 (6014): 176–182.

Newey, Whitney K., and Kenneth D. West. 1987. "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix." *Econometrica* 55 (3): 703–708.

Pechenick, Eitan Adam, Christopher M. Danforth, and Peter Sheridan Dodds. 2015. "Characterizing the Google Books Corpus: Strong Limits to Inferences of Socio-Cultural and Linguistic Evolution." *PLOS ONE* 10 (10): e0137041.

Pomeranz, Kenneth. 2000. *The Great Divergence: China, Europe, and the Making of the Modern World Economy*. Princeton: Princeton University Press.

Priestley, Joseph. 1831. *Historical Account of the Navigable Rivers, Canals, and Railways, throughout Great Britain*. London: Longman, Rees, Orme, Brown and Green.

Rambachan, Ashesh, and Jonathan Roth. 2023. "A More Credible Approach to Parallel Trends." *Review of Economic Studies* 90 (5): 2555–2591.

Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. "What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature." *Journal of Econometrics* 235 (2): 2218–2244.

Szostak, Rick. 1991. *The Role of Transportation in the Industrial Revolution: A Comparison of England and France*. Montreal: McGill-Queen's University Press.

Thomas, Ryland, and Nicholas Dimsdale. 2017. *A Millennium of UK Data*. Bank of England OBRA dataset. https://www.bankofengland.co.uk/statistics/research-datasets.

Turnbull, Gerard. 1987. "Canals, Coal and Regional Growth during the Industrial Revolution." *Economic History Review* 40 (4): 537–560.

Tvedt, Terje. 2010. "Why England and Not China and India? Water Systems and the History of the Industrial Revolution." *Journal of Global History* 5 (1): 29–50.

Ward, J. R. 1974. *The Finance of Canal Building in Eighteenth-Century England*. Oxford: Oxford University Press.

Wrigley, E. A. 1988. *Continuity, Chance and Change: The Character of the Industrial Revolution in England*. Cambridge: Cambridge University Press.

Wrigley, E. A. 2010. *Energy and the English Industrial Revolution*. Cambridge: Cambridge University Press.

Wrigley, E. A. 2016. *The Path to Sustained Growth: England's Transition from an Organic Economy to an Industrial Revolution*. Cambridge: Cambridge University Press.

---

# Data Availability Statement

All code and data required to reproduce the analyses are publicly available at [https://github.com/percw/water_and_society](https://github.com/percw/water_and_society). British sectoral output, population and capital stock are from the Bank of England's *A Millennium of Macroeconomic Data for the UK* (Thomas and Dimsdale 2017), which reproduces Broadberry et al. (2015). Cross-country GDP per head and population are from the Maddison Project Database 2023 (Bolt and van Zanden 2024). Installed horsepower benchmarks are from Kanefsky (1979) as reported in Crafts (2004). Canal completion years and lengths are compiled from published reference tables and parliamentary authorisation years are parsed from the digitised text of Priestley (1831); both series are included in the repository with their construction scripts. Word and phrase frequencies are from the Google Books Ngram Corpus, British English 2019 edition. A self-contained replication package is available as a supplementary archive.


---

