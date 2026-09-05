# Abstract

Britain's industrial take-off is usually dated by steam. This paper dates it by water. Combining annual British sectoral output, 1700–1870, with a new series of canal mileage by completion year, installed steam and water horsepower, and the Google Books British corpus, we show that Britain passed through two growth regimes. In the first, opening in 1775–1792 as the canal network was built, aggregate output, coal, iron and population accelerated while income per head did not. In the second, from 1818, steam raised income per head. Canal mileage predicts coal output over the following two decades but not income per head or agriculture; steam raises income per head only after 1830. In print, coal travels by barge a generation before it burns in engines. A cross-country difference-in-differences cannot see any of this, because the Napoleonic collapse of continental controls masquerades as a British take-off. Water infrastructure was the precondition for a coal economy, in Tvedt's sense: necessary, and not sufficient.

**Keywords:** Industrial Revolution, canals, coal, water infrastructure, transport revolution, organic economy, growth regimes, Great Divergence


---

# 1. Introduction

Every account of the British Industrial Revolution has to choose a clock. The steam clock starts in the 1780s with Watt's rotative engine and reads industrialisation as the arrival of a new prime mover and, with it, of sustained growth in income per head (Landes 1969; Allen 2009). The canal clock starts in 1761, when the Duke of Bridgewater's canal halved the price of coal in Manchester, and reads the same century as a transport revolution that integrated markets long before factories filled with engines (Bogart 2014; Szostak 1991; Maw 2013). The two clocks are rarely set against each other with data, because they measure different things. The steam clock is calibrated to income per head, which barely moved before 1830 (Crafts 1985; Crafts and Harley 1992). The canal clock is calibrated to tonnage, prices and towns.

This paper sets the two clocks side by side using annual British data and asks a narrower question than "which mattered more". Following Terje Tvedt's argument that Britain's water systems were the *precondition* for a coal economy rather than a rival to it (Tvedt 2010), we ask whether the timing, sequencing and sectoral incidence of British growth between 1700 and 1870 are consistent with water infrastructure enabling coal, and coal then enabling steam. A precondition claim is a claim about order and dependence. It predicts that the canal-served sectors accelerate before steam is a significant power source; that coal output responds to the canal network; that steam capacity follows coal; and that the sectors canals did not serve, and the outcome canals could not directly raise, do not move. Each of these is testable with series that already exist. It is a British test of a global-history thesis, and we say at the end what it does and does not establish about the Netherlands and China.

Three findings follow. First, Britain had two growth regimes, not one. Using the annual output series of Broadberry, Campbell, Klein, Overton and van Leeuwen, we find trend breaks between 1775 and 1792 in total output, industry, services, coal, iron and population, and a break in 1818 in income per head. In the first regime the growth of aggregate output nearly tripled and the growth of population quadrupled, while income per head grew no faster than it had since 1700 and, between 1760 and 1790, slower. Population absorbed the acceleration. This reconciles the canal historians with the Crafts–Harley chronology: both are right, about different variables.

Second, the canal network is a dose that predicts the right things. We assemble a year-by-year series of canal miles from the completion dates of 155 British canals and corroborate its timing with 152 parliamentary authorisations recovered from Priestley's 1831 survey. Cumulative canal mileage predicts coal output over the following five to twenty years and it predicts population; it predicts neither income per head nor agricultural output, and the coal result survives a quadratic trend, first differences and two predetermined versions of the dose. Steam horsepower, in turn, raises income per head only after 1830. In the language of the Google Books British corpus the same order appears, to within a decade: "coal barge" and "coal wharf" reach a quarter of their mid-century frequency around 1781 and 1800; "steam engine" and "steam power" around 1808 and 1826.

Third, the standard cross-country test of an eighteenth-century British take-off is broken by war, and we show how. A difference-in-differences on Maddison GDP per head with France and the Netherlands as controls locates Britain's break in 1807. That date is the Dutch economy losing 44 per cent of its income per head under French occupation and blockade, while Britain, uninvaded, held level. Any two-group comparison that spans 1790–1815 will find a British "effect" whatever Britain did with its rivers. We retain the cross-country evidence only at benchmark years: between 1700 and 1820 British output tripled while German output doubled and French output grew by half, and Britain did this while steam supplied a fifth of its stationary power in 1800 and about a third in 1820.

The contribution is fourfold. To the transport-revolution literature, we add an annual national dose series and a sequencing test that connects canals to the energy transition rather than to urban growth, the channel that Alvarez-Palau, Bogart, Satchell and Shaw-Taylor have recently quantified (Alvarez-Palau et al. 2025). To the energy-history debate among Wrigley, Allen, Pomeranz and Malm, we add the observation that the escape from the Malthusian ceiling was under way, in aggregate, before steam, in what Wrigley calls the advanced organic economy: powered by water and moved by water, but already burning coal for heat. To the growing practice of historical difference-in-differences (Roth et al. 2023), we add a worked example of how a control group's catastrophe becomes a treatment group's miracle. And to the text-as-data literature we add a cautionary measurement: the frequency of "canal" in print tracks the level of the canal network at 0.91, but detrended the correlation falls to 0.23. The corpus records that the network existed, not how fast it grew.

The paper proceeds as follows. The next section places the argument in the literature. We then describe the data and the empirical strategy, report the two regimes, the canal dose, the precondition chain, the semantic sequence and the failure of the cross-country design, and discuss what the results mean for Tvedt's thesis and for the Great Divergence. The limitations, which are real, come before the conclusion.


---

# 2. Water, coal and the chronology of British growth

## 2.1 The transport revolution and its canals

The transport revolution of eighteenth-century Britain is well documented and, until recently, poorly measured. Between the Bridgewater Canal of 1761 and the opening of the Liverpool and Manchester Railway in 1830, Parliament authorised roughly 165 canal companies and the navigable network grew from about 1,400 miles of improved river to some 4,000 miles of river and canal (Hadfield 1984; Bogart 2014). The coal trade itself was older and larger than the canals: the coastal trade from the Tyne and Wear to London was already the largest bulk-freight flow in Europe in 1700, and Britain's coal output had been rising for two centuries before the first canal was cut (Hatcher 1993; Flinn 1984; Pollard 1980). What canals changed was inland access. Contemporaries did not doubt this. Priestley's survey of 1831, written at the network's peak, opens its account of the Bridgewater Canal by noting that the Duke's "primary object" was "to open his valuable collieries at Worsley, and to supply the town of Manchester with coal, at a much cheaper rate" (Priestley 1831). Turnbull's regional study documented the same point: canals were built where coal was, they carried coal above all else, and the counties that acquired them saw coal output and population grow faster than those that did not (Turnbull 1987). Szostak went furthest, arguing that the transport improvements were a necessary condition for the factory system itself, since only wide markets could absorb the output of a mechanised mill (Szostak 1991).

Quantitative work has caught up in the last decade. Bogart's survey collects the mileage, cost and freight-rate evidence and concludes that inland freight costs fell by half or more between 1700 and 1830 (Bogart 2014). Alvarez-Palau, Bogart, Satchell and Shaw-Taylor, using a multi-modal transport network reconstructed in GIS, estimate that transport costs relative to producer prices fell by nearly 75 per cent between 1680 and 1830 and that, without that fall, inland towns would have been 20 to 25 per cent smaller in 1841 (Alvarez-Palau et al. 2025). Their outcome is urban population. Ours is the energy system. The two are complementary: towns grew where coal could be delivered, and coal could be delivered where water had been engineered.

## 2.2 Energy, the organic economy and the Great Divergence

The energy literature starts from a different place. Wrigley's organic economy is bounded by the annual product of the land; sustained growth required a "mineral-based energy economy" in which coal replaced wood as a source of heat and, much later, water and wind as a source of power (Wrigley 1988; Wrigley 2010; Wrigley 2016). Wrigley is careful that the first of these transitions was under way in England from the sixteenth century and that the eighteenth-century economy was an advanced organic one, burning mineral heat while its power remained organic; Warde's energy accounts confirm the chronology (Warde 2007). The steam clock belongs to Wrigley's readers more than to Wrigley. Allen's induced-innovation account makes cheap British coal and dear British labour the reason the steam engine was worth inventing in Britain and nowhere else (Allen 2009). Pomeranz gives coal a starring role in the Great Divergence, alongside the ghost acres of the Americas (Pomeranz 2000). Clark and Jacks and, more recently, Fernihough and O'Rourke have tested the coal hypothesis on prices, output and city growth and found that proximity to coal mattered a great deal for where Europe industrialised (Clark and Jacks 2007; Fernihough and O'Rourke 2021). Malm's *Fossil Capital* accepts coal's centrality but denies that its adoption was driven by thermodynamic superiority or scarcity of water power: steam won because it freed capital from the riverbank and allowed mills to be sited where labour could be disciplined (Malm 2016).

What these accounts share is a clock calibrated to steam and coal combustion. Tvedt's intervention is to move the clock upstream. In "Why England and not China and India?", he argues that Britain's distinctive endowment was not coal as such, which China had in abundance, but a hydrological regime of gentle gradients, steady flow and navigable rivers that could be engineered into a national network of canals and water-powered mills at low cost (Tvedt 2010). The monsoonal rivers of Asia could not. On this reading the water system is the precondition: it created the market integration, the cheap coal at the point of use, and the water-powered factory template on which steam later built. Tvedt's evidence is comparative and qualitative. This paper asks whether the annual British record supports the sequence he proposes.

A precondition is not a rival cause. Coal remains the fuel of the second regime and steam its engine. The claim is that neither would have arrived when and where it did without the first regime, and that the first regime is visible in the data if one looks at the variables canals could move: coal, aggregate output, and the number of people the economy could feed.

## 2.3 Two chronologies of growth

The macroeconomic chronology has moved decisively towards gradualism. Crafts, and Crafts and Harley, cut the growth rates of the 1780–1830 period that Deane and Cole had estimated and showed that income per head grew slowly until well into the nineteenth century (Crafts 1985; Crafts and Harley 1992). Broadberry, Campbell, Klein, Overton and van Leeuwen's reconstruction of British output from the medieval period confirms the picture: annual growth of GDP per head averaged around 0.3 per cent from 1700 to the 1820s and only then accelerated (Broadberry et al. 2015). Crafts's growth-accounting of steam finds its contribution to labour-productivity growth trivial before 1830 and dominant only after 1850 (Crafts 2004). Kanefsky's estimates of installed power, on which Crafts draws, put steam at 35,000 horsepower in 1800 against 120,000 for water wheels; steam did not overtake water until the 1830s (Kanefsky 1979; Kanefsky and Robey 1980).

Gradualism in income per head has been read as a verdict against any eighteenth-century take-off. It is not. The same Broadberry series show total output and population doubling between 1760 and 1830. A growth regime in which aggregate output accelerates while income per head does not is exactly what Malthus described and exactly what an infrastructure shock in an organic economy should produce: more mouths fed, not richer mouths. The distinction between the aggregate and the per-capita clock is, we argue, the key to reconciling the canal historians with the cliometricians.

## 2.4 Text as data and historical difference-in-differences

Two methodological literatures frame our tools. Michel et al. introduced the Google Books corpus as a quantitative record of culture, and Pechenick, Danforth and Dodds documented its limits: the corpus over-weights technical publishing and records what was printed rather than said (Michel et al. 2011; Pechenick et al. 2015). For infrastructure vocabulary that bias is a feature, and we show below what it does and does not measure. The historical difference-in-differences literature has grown cautious about serial correlation, heterogeneous effects and pre-trends (Bertrand, Duflo, and Mullainathan 2004; Roth et al. 2023; Rambachan and Roth 2023). We add a more elementary hazard: a control group hit by a war the treatment group escaped, whose economic consequences Crouzet described sixty years ago (Crouzet 1964).


---

# 3. Data and empirical strategy

## 3.1 British output, population and power

Annual real output for Great Britain by sector, 1700–1870, comes from Broadberry, Campbell, Klein, Overton and van Leeuwen as published in the Bank of England's *A Millennium of Macroeconomic Data for the UK*, version 3.1 (Broadberry et al. 2015; Thomas and Dimsdale 2017). We use total GDP, agriculture, industry and services, and from the industrial-production tables the physical output indices for coal, iron and textiles. Population of Great Britain is from the same source, based on Wrigley and Schofield's reconstitution to 1801 and the censuses thereafter. GDP per head is total output divided by population. The series are indices with 1700 = 100.

Installed stationary power is from Kanefsky's estimates as tabulated by Crafts: steam horsepower of 5,000 in 1760, 35,000 in 1800, 160,000 in 1830 and 2.06 million in 1870; water horsepower of 70,000, 120,000, 160,000 and 230,000 at the same dates; wind 10,000, 15,000, 20,000 and 10,000 (Kanefsky 1979; Crafts 2004). Steam and water were at parity in 1830. We interpolate log-linearly between the four benchmarks, wind included. The interpolated series are smooth by construction, and we treat inference that depends on their year-to-year variation with corresponding caution.

## 3.2 The canal network as a dose

A single treatment date cannot represent the canal network. It was built over sixty years in two waves, and a binary indicator cannot distinguish the Grand Cross of the 1770s from the mania canals completed between 1790 and 1816. We therefore construct a continuous dose, which we call the canal stock: cumulative canal miles in operation by year.

The primary series is assembled from the completion year and length of 155 canals in Great Britain, taken from the reference table of British canals maintained on Wikipedia and retrieved on 3 September 2026; we include every entry with a stated length and opening year, and use the year of full completion where a canal opened in stages, which biases the series late by a few years relative to first use. The 155 canals total 2,967 miles, of which 2,320 were open by 1830. The series excludes river navigations improved before 1700, which were the bulk of the network's initial 1,400 miles, so it measures additions to the network rather than its level; for the growth regressions this is the relevant quantity. Hadfield's count of roughly 165 canal companies authorised between 1761 and 1830 is a count of undertakings, several of which built no canal or merged, and is not directly comparable (Hadfield 1984).

We corroborate the timing with an independent source. Priestley's *Historical Account of the Navigable Rivers, Canals, and Railways throughout Great Britain* records the Acts that authorised each navigation with regnal year and date of Royal Assent (Priestley 1831). From the digitised 1831 text we identify 325 entries by their capitalised headings and recover a first-authorisation year for 152, including 70 canals authorised between 1760 and 1829, thirty of them in the 1790s; the rest are lost to the quality of the optical character recognition, and lengths could not be recovered at all. The authorisation series leads the completion series by roughly a decade, as it should, and both show the same two waves.

## 3.3 Cross-country data

Cross-country GDP per head is from the Maddison Project Database 2023 (Bolt and van Zanden 2025). The series labelled GBR is the United Kingdom including Ireland; we note where this matters. For Britain, France, the Netherlands, Sweden, Germany, Spain and Portugal the series is annual from 1700; for Belgium, Italy, China, India and Japan it is interpolated between benchmarks and we use it only descriptively. Population in the Maddison database is a benchmark series before 1820, so cross-country total output is compared only at the benchmark years 1700, 1820 and 1870.

## 3.4 Text data

Word and phrase frequencies are from the Google Books Ngram corpus, British English 2019 edition, 1700–1900, retrieved with the viewer's three-year smoothing (Michel et al. 2011). The unigram "canal" is used to test what the print record measures. For the semantic sequence we retrieved sixteen bigrams naming coal's mode of use and use eight: "coal barge", "coal wharf", "coal boat" and "canal boat" for coal moved by water; "steam engine" and "steam power" for coal burned in engines; "coal field" as the geologist's term; and "fire engine", the eighteenth-century name for an atmospheric engine, as a check on terminological drift. "Steam boat" was retrieved and excluded because it names water transport as much as steam. Each bigram is indexed to its own 1850 frequency and the groups are equal-weighted averages of their members, so that a single common term cannot dominate; a further five-year centred mean is applied before thresholds are read.

## 3.5 Empirical strategy

Our questions are about timing, sequence and incidence within one national economy over 170 years. The sample is small, the series are smooth and trending, and the treatment is itself a slowly accumulating stock. We match the tools to those facts, and we use linear methods throughout: with 130 annual observations, flexible machine-learning estimators fit the time trend closely enough to leave no treatment variation to estimate from.

**Regime detection.** For each British series we estimate a linear trend in logs and test for a single break in level and slope at an unknown date using the Andrews sup-F statistic with 15 per cent trimming, reporting the statistic against the Andrews critical value, and for two breaks by grid search with a minimum segment of twenty years (Andrews 1993; Bai and Perron 1998). We also fix the break at 1761 and test for a change in trend slope over 1700–1830 with Newey–West standard errors (Newey and West 1987); since the data-chosen breaks fall later, this fixed date is a conservative pre-test. Agriculture and GDP per head are the placebo series: canals did not carry harvests to any great extent, and a precondition operating through population should leave income per head unchanged.

**Dose-response.** We regress the log of each output series on the canal stock, in thousands of miles, and a linear trend over 1700–1830, the period before railways. Because a cumulative stock is itself a smooth, accelerating series, we report three further specifications that a sceptical reader would demand: a quadratic trend with a dummy for war years (1756–63, 1775–83, 1793–1815); a first-difference model with ten lags of new mileage, reporting the sum of the lag coefficients and the joint F-test; and a horse race that adds the print frequency of "steam" and the war dummy. We test the residuals of the level regressions for a unit root. We build mainly on coefficients that survive all specifications; where an outcome survives most but not all, we say so.

**Predetermined doses.** Canals were promoted where trade was growing, so the contemporaneous stock is not exogenous. We therefore also use two doses fixed before the outcome window: the completion-based stock lagged ten and fifteen years, and the cumulative number of canals *authorised* by Act of Parliament, from Priestley, lagged ten years. An Act precedes completion by roughly a decade and cannot respond to output after it is passed. These doses remove contemporaneous feedback; they do not remove anticipation, and we test for it directly by regressing new authorisations on past output growth and by adding the outcome's own past growth to the dose regressions.

**Sequencing by local projection.** To test the chain water → coal → steam → income per head, we estimate local projections (Jordà 2005): the change in the log outcome over horizons of one to twenty years is regressed on the regressor of interest, the outcome's own level and a trend, with Newey–West errors whose bandwidth is the larger of ten years and the horizon. Agriculture is again the placebo. Steam equations start in 1760, when the horsepower series begins; the income equations are estimated on 1760–1830, 1760–1870 and 1830–1870, with an interaction of horsepower and a post-1830 indicator, since the thesis predicts that steam's per-capita effect appears only after it becomes the majority power source. With eight outcomes, four specifications and four reported horizons, we treat a Bonferroni threshold of about 0.002 as the family-wise bar and say which results clear it.

**Semantic sequencing.** For each bigram group we record the first year in which the five-year moving average reaches 10, 25 and 50 per cent of its 1850 level, and the year in which "steam engine" overtakes "fire engine" in print. Because the British sub-corpus is thin before 1780, we repeat the 25 per cent threshold with three-, five- and nine-year windows and with 1830 as well as 1850 as the reference year. We also re-estimate the steam links of the chain with the print frequency of "steam engine" in place of interpolated horsepower, as an independent, if noisier, measure of steam's diffusion.

**Cross-country.** We estimate the two-way fixed-effects difference-in-differences on Maddison GDP per head, in levels and logs, with 1761 as treatment date, for three control groups and three sample windows, with its ten-year event-study version, in order to show what it measures; Newey–West errors on a stacked panel are not a valid treatment of cross-sectional dependence, so we report clustered and collapsed alternatives beside them. We then compare peak-to-trough drawdowns in GDP per head over 1785–1815 by country and report growth between the Maddison benchmark years.

All code, the tidy data files, the Priestley parsing rules and the horsepower interpolation are in the replication repository named in the data availability statement; the code and the text were prepared with the assistance of an AI tool under the author's direction, as declared in the acknowledgements; the mediation decomposition we also estimated, which is not identified once a quadratic trend is absorbed, is reported there as a negative result.


---

# 4. Results

## 4.1 Two growth regimes

Figure 1 plots the British series on a logarithmic scale with the two canal-building waves shaded. Panel (a) shows total output, population and income per head; panel (b) shows coal, industry and agriculture. The visual impression is of a fan opening after 1760: total output and population steepen together while income per head continues at its previous slope until the 1820s. Agriculture never steepens at all.

<div align="center">
  <img src="../../data/fig1_two_regimes.png" alt="Figure 1: Britain's two growth regimes" width="800">
  <br>
  <em><strong>Figure 1: Britain's two growth regimes.</strong> Annual indices, 1700 = 100, log scale. Shaded bands mark the first canal wave (1760–1780) and the canal-mania completions (1790–1816). Vertical lines at 1761 and 1818. Source: Bank of England millennium dataset (Broadberry et al. 2015).</em>
</div>

Table 1 gives the trend growth rates by period. Between 1700–1760 and 1790–1815, growth of total output rose from 0.55 to 1.58 per cent a year, industry from 0.47 to 1.81, coal from 0.87 to 2.85 and population from 0.29 to 1.18. Income per head grew at 0.25 per cent a year in the first period, 0.08 in 1760–1790 and 0.40 in 1790–1815. Agriculture is flat throughout.

**Table 1: Trend growth of British series, per cent per year**

| Period | Total GDP | Industry | Coal | Services | Population | GDP per head | Agriculture |
|:--|--:|--:|--:|--:|--:|--:|--:|
| 1700–1760 | 0.55 | 0.47 | 0.87 | 0.50 | 0.29 | 0.25 | 0.75 |
| 1760–1790 | 0.82 | 1.16 | 2.05 | 0.83 | 0.74 | 0.08 | 0.60 |
| 1790–1815 | 1.58 | 1.81 | 2.85 | 2.02 | 1.18 | 0.40 | 0.81 |
| 1815–1830 | 1.98 | 3.64 | 2.84 | 1.62 | 1.49 | 0.50 | 0.63 |
| 1830–1870 | 2.35 | 2.85 | 3.57 | 2.62 | 1.16 | 1.19 | 0.78 |

*Source: own calculations from the Bank of England millennium dataset (Broadberry et al. 2015). Slopes of log-linear trends fitted within each window.*

Table 2 formalises the comparison. Fixing the break at 1761 and estimating over 1700–1830, the trend slope of total output rises by 0.85 percentage points a year, industry by 1.42, coal by 1.62, iron by 3.24, textiles by 1.51, services by 1.07 and population by 0.83, all with p-values below 0.01 under Newey–West errors. The slope of income per head changes by 0.02 points and that of agriculture by −0.04, neither distinguishable from zero. The fixed date is a pre-test, so the table also reports the break the data choose. The single best break falls between 1777 (population) and 1792 (total output) for every canal-served series, with sup-F statistics far above the Andrews critical value, and at 1818 for income per head. Agriculture's best break is not significant: there is none. Allowing two breaks places the first in 1774–1775 for total output, industry and services and the second in 1818–1823 for output and industry; coal's first break falls earlier, in 1741, and its second in 1798, which we return to below. The data pick out the two regimes without being told where to look.

**Table 2: Change in trend slope at 1761 and data-chosen break dates**

| Series | Trend before 1761, % per year | Change after 1761, points per year | p | Best single break (sup-F) | Best two breaks |
|:--|--:|--:|--:|--:|:--|
| Total GDP | 0.52 | +0.85 | <0.01 | 1792 (778) | 1775, 1818 |
| Industry | 0.39 | +1.42 | <0.01 | 1789 (909) | 1774, 1823 |
| Coal | 0.77 | +1.62 | <0.01 | 1784 (667) | 1741, 1798 |
| Iron | 0.26 | +3.24 | <0.01 | 1786 (1,294) | 1786, 1815 |
| Textiles | 0.69 | +1.51 | <0.01 | 1779 (240) | 1728, 1817 |
| Services | 0.44 | +1.07 | <0.01 | 1786 (927) | 1775, 1844 |
| Population | 0.23 | +0.83 | <0.01 | 1777 (3,052) | 1730, 1783 |
| *GDP per head* | 0.29 | +0.02 | 0.82 | 1818 (270) | 1720, 1818 |
| *Agriculture* | 0.82 | −0.04 | 0.84 | none (4.2, not significant) | 1720, 1757 |

*Slope-change regressions on 1700–1830 with Newey–West (10 lags) errors. Break searches on 1700–1870: Andrews sup-F with 15 per cent trimming (5 per cent critical value approximately 11.8 for two parameters) and a two-break grid search with a minimum segment of 20 years, which cannot place a break after 1850.*

The arithmetic of the first regime is simple. Between 1760 and 1815 the growth of total output and the growth of population each rose by about a percentage point a year: the economy grew faster and fed more people at the same income, for half a century, while coal output per head doubled, from an index of 100 in 1700 to 202 in 1790 and 246 in 1800. Coal's early break in 1741 is a reminder that the coal trade did not begin with canals; the coastal trade from the Tyne to London was already Europe's largest bulk-freight flow (Hatcher 1993; Flinn 1984). What the canal era added was inland coal, and the second break in 1798 dates it.

## 4.2 The canal network as a dose

Figure 2 shows the canal series. Panel (a) gives miles opened per decade: 117 in the 1760s, 353 in the 1770s, a lull of 83 in the 1780s, then 548 in the 1790s, 479 in the 1800s and 344 in the 1810s. Panel (b) gives the cumulative stock, from 218 miles in 1760 to 772 in 1790, 1,487 in 1800 and 2,320 in 1830. Panel (c) gives coal output per head. The correspondence between the two waves and the two steepenings of coal per head is visible to the eye; the regressions ask whether it survives detrending.

<div align="center">
  <img src="../../data/fig2_canal_dose.png" alt="Figure 2: The canal network and coal" width="800">
  <br>
  <em><strong>Figure 2: The canal network and coal.</strong> (a) Canal miles opened per decade, 155 canals by completion year. (b) Cumulative canal miles since 1700. (c) Coal output per head, 1700 = 100, with the year steam overtook water and wind as a source of stationary power. Sources: canal reference table described in the data section; Bank of England millennium dataset (Broadberry et al. 2015); horsepower benchmarks from Kanefsky as tabulated in Crafts (Kanefsky 1979; Crafts 2004).</em>
</div>

Table 3 reports the dose-response regressions over 1700–1830. In the simplest specification, log output on a linear trend and the canal stock, a thousand miles of canal is associated with 47 per cent more coal, 40 per cent more industrial output, 99 per cent more iron, 32 per cent more services and 24 per cent more population, and with no change in income per head or agriculture. The sceptical specifications thin this out. With a quadratic trend and a war dummy, coal, iron and services retain large and significant coefficients; population is marginal; industry and total output are indistinguishable from the trend. In first differences with ten lags of new mileage, coal, industry and population respond, total output and income per head do not, and agriculture's response is negative. In a horse race against the print frequency of "steam", coal's canal coefficient is 41 per cent against an insignificant 13 for steam; for industry and population the two are of similar size. A horse race against installed steam horsepower is not informative: over 1760–1830 the interpolated steam and water horsepower series and the canal stock are all near-linear in time and correlate at 0.98, so partial coefficients apportion a common trend rather than separate three stocks. The ordering evidence must come from timing.

**Table 3: Canal stock and British output, 1700–1830 (per 1,000 canal miles)**

| Outcome (log) | Linear trend | Quadratic trend + war | First differences, 10-year cumulative | Horse race: canal | Horse race: "steam" in print |
|:--|--:|--:|--:|--:|--:|
| Coal | +46.5% (p<0.001) | +29.8% (p=0.001) | +27.0% (p<0.001) | +40.8% (p<0.001) | +12.6% (p=0.08) |
| Industry | +40.1% (p<0.001) | −0.9% (p=0.89) | +14.3% (p<0.001) | +28.8% (p<0.001) | +30.4% (p=0.003) |
| Iron | +99.3% (p<0.001) | +61.2% (p=0.013) | — | — | — |
| Services | +32.3% (p<0.001) | +12.2% (p=0.002) | — | — | — |
| Population | +24.0% (p<0.001) | +4.1% (p=0.07) | +16.6% (p<0.001) | +18.6% (p<0.001) | +15.0% (p<0.001) |
| Total GDP | +24.7% (p<0.001) | +2.2% (p=0.52) | +4.2% (p=0.25) | +18.8% (p<0.001) | +19.0% (p<0.001) |
| *GDP per head* | +0.8% (p=0.69) | −1.9% (p=0.61) | −12.4% (p=0.33) | +0.2% (p=0.94) | +4.0% (p=0.08) |
| *Agriculture* | −0.5% (p=0.90) | −5.1% (p=0.56) | −18.8% (p<0.001) | −1.5% (p=0.72) | +7.3% (p=0.07) |

*Newey–West errors with 10 lags. The first-difference column reports the sum of the coefficients on lags 0–10 of new mileage, with the p-value of the joint F-test that all eleven are zero. The steam regressor is the Google Books frequency of "steam", indexed to 1830. The war dummy covers 1756–63, 1775–83 and 1793–1815. An augmented Dickey–Fuller test rejects a unit root in the residuals of the linear-trend regressions at 5 per cent for every outcome except population (p = 0.24).*

Two features of Table 3 matter for the argument. The first is that coal is the robust channel. It is also the channel the mechanism predicts, since the canals were dug to move it. The second is that the placebo rows behave. Income per head does not respond to canals in any specification, and agriculture's only significant coefficient is negative, in first differences, which is the structural shift away from farming rather than an effect on farming.

The reverse regression is not empty: past growth in coal, total output and population predicts subsequent canal openings, and past coal growth predicts new parliamentary authorisations with a joint p-value below 0.001. Canals were built where demand was growing. The predetermined doses address the contemporaneous part of this. With the completion stock lagged ten or fifteen years the pattern of Table 3 is unchanged: coal 48 to 49 per cent per thousand miles, industry 40 to 43, population 24 to 25, income per head nothing. With the authorisation count lagged ten years, each ten canals authorised is followed by 12 per cent more coal, 10 per cent more industrial output and 6 per cent more population, again with no response in income per head; adding the outcome's own growth over the preceding decade leaves these at 11, 9 and 5 per cent, all significant at 1 per cent. Under a quadratic trend the authorisation dose falls to 4 per cent for coal, significant only at the 7 per cent level. In local projections it predicts coal at every horizon and does not predict population, income per head or agriculture. The dose is not exogenous, and we do not claim that it is; what we claim is that its timing and incidence, under both contemporaneous and predetermined measures, are those of a precondition.

## 4.3 The precondition chain

Figure 3 reports the local projections that test the sequence directly. Each panel shows the cumulative response of the outcome, in log points, to a unit of the regressor, at horizons of one to twenty years, with 95 per cent Newey–West bands whose bandwidth grows with the horizon.

<div align="center">
  <img src="../../data/fig3_local_projections.png" alt="Figure 3: Local projections along the precondition chain" width="800">
  <br>
  <em><strong>Figure 3: Local projections along the precondition chain.</strong> Cumulative log response at horizons 1–20 years, per 1,000 canal miles or per log point of the regressor, controlling for the outcome's level and a trend. Samples 1700–1830 where the canal stock is the regressor and 1760–1830 where steam horsepower enters, including the steam-to-income panel. Shaded: 95 per cent bands with Newey–West bandwidth equal to the larger of ten years and the horizon.</em>
</div>

The top-left panel is the first link: a thousand miles of canal raises coal output by 29 per cent after five years, 38 per cent after ten and 44 per cent after fifteen, with the band excluding zero at every horizon shown. Controlling for contemporaneous steam horsepower, estimated from 1760, the canal effect on coal remains at 21 per cent over five to ten years and is gone at fifteen to twenty. The top-middle panel, canal stock to steam horsepower, is positive and precisely estimated at every horizon, but the horsepower series is interpolated between four benchmarks and grew thirty-fold between 1760 and 1830, so this panel establishes that steam capacity rose after the network did, not the speed at which it did so. The top-right panel, coal to steam, is positive at every horizon but significant only at five years. On the interpolated series that is as much as can be asked.

The bottom row is the test that distinguishes a precondition from a cause. Canal stock has no effect on income per head at any horizon (bottom-left); the point estimates are negative and the bands include zero throughout. Steam horsepower has no effect on income per head when the sample stops at 1830 (bottom-middle). On the 1760–1870 sample it does, at every horizon and with p-values below 0.002; estimated on 1830–1870 alone the response is again positive at every horizon with p-values below 0.001, and an interaction of horsepower with a post-1830 indicator is positive and significant. The elasticities themselves, between 0.2 and 0.9 log points per log point of horsepower depending on sample and horizon, should not be read as magnitudes, for the reason given above; the sign and the timing are the result. Steam's per-capita dividend is a post-1830 phenomenon. Canals raise coal and population (the population response is 3 to 7 per cent per thousand miles over five to twenty years, significant beyond five years at the family-wise threshold) and leave income per head where it was. The bottom-right panel, agriculture, is negative at intermediate horizons, again the composition effect, and returns to zero.

Because the horsepower series is interpolated, we re-estimate the steam links with the print frequency of "steam engine", which correlates at 0.90 with interpolated horsepower but varies year to year. The ordering survives, more weakly: the canal stock predicts "steam engine" at ten years (p = 0.06) and coal output predicts it at twenty (p = 0.003). The print series predicts income per head negatively at fifteen years, which is a warning about the series rather than about steam: it records that engines were being discussed, not how much power they supplied. The last link of the chain therefore rests on the horsepower benchmarks, the 1818 break in income per head and the 1833 crossover in installed power.

The chain, read from Figure 3 and Table 4, is: canals raise coal within a decade; steam capacity rises after the network and after coal, on a scale that only the benchmarks can date; steam raises income per head, but only once it is the majority power source. Water first, coal second, steam third, income last.

## 4.4 How much power was steam?

The precondition thesis requires that the first regime run on water rather than steam. Table 4 uses the Kanefsky benchmarks to check. In 1760 steam supplied about 6 per cent of Britain's installed stationary power; in 1800, when the first regime was thirty years old, 21 per cent; by 1820 about a third; in 1830 parity with water, at 47 per cent. Steam overtook water and wind combined in 1833, fifteen years after the per-capita break. Coal output per unit of installed steam horsepower fell from 100 to 37 between 1760 and 1800: coal grew far faster than the engines that could burn it, and most of it went to hearths, forges, kilns and salt pans, inland by water.

**Table 4: Installed stationary power in Britain, thousands of horsepower**

| Year | Steam | Water | Wind | Steam share | Coal output per steam hp (1760 = 100) |
|:--|--:|--:|--:|--:|--:|
| 1760 | 5 | 70 | 10 | 6% | 100 |
| 1800 | 35 | 120 | 15 | 21% | 37 |
| 1830 | 160 | 160 | 20 | 47% | 19 |
| 1870 | 2,060 | 230 | 10 | 90% | 6 |

*Source: Kanefsky's estimates as tabulated in Crafts (Kanefsky 1979; Crafts 2004); coal output from the Bank of England millennium dataset (Broadberry et al. 2015). Shares from log-linear interpolation between benchmarks, wind included.*

## 4.5 The semantic sequence

If coal moved by water before it burned in engines, the language of the period should say so. Table 5 records, for each term or group, the first year in which its smoothed frequency in the British corpus reached 10, 25 and 50 per cent of its 1850 level. "Canal" reaches a quarter of its mid-century frequency in 1763, the year after the Bridgewater opening; "coal barge" in 1781; "coal wharf" in 1800; "canal boat", a later coinage, in 1823. "Steam engine" reaches the same threshold in 1808, "steam power" in 1826, and "coal field", the geologist's term, in 1820. The coal-by-water group as a whole crosses 25 per cent in 1800, the coal-by-steam group in 1819. "Steam engine" overtakes "fire engine", the older name for the same machine, in 1800, which dates the terminological consolidation of steam to the decade after the canal mania. Figure 4 plots the three indices.

**Table 5: Year in which print frequency first reaches a share of its 1850 level (British English corpus, five-year mean)**

| Term or group | 10% | 25% | 50% |
|:--|--:|--:|--:|
| "canal" | 1743 | 1763 | 1809 |
| "coal barge" | 1753 | 1781 | 1783 |
| "coal wharf" | 1774 | 1800 | 1815 |
| "canal boat" | 1812 | 1823 | 1825 |
| Coal-by-water group | 1780 | 1800 | 1817 |
| "steam engine" | 1800 | 1808 | 1821 |
| "steam power" | 1821 | 1826 | 1831 |
| Coal-by-steam group | 1804 | 1819 | 1825 |
| "coal field" | 1788 | 1820 | 1831 |

*Source: Google Books Ngram corpus, British English 2019 edition, three-year API smoothing and a five-year centred mean. Groups are equal-weighted averages of member terms each indexed to 1850; the coal-by-water group also contains "coal boat", which is too rare before 1800 to threshold on its own.*

<div align="center">
  <img src="../../data/fig4_semantic_sequence.png" alt="Figure 4: The semantic sequence" width="800">
  <br>
  <em><strong>Figure 4: In print, coal travels by water before it is burned in engines.</strong> Five-year moving averages indexed to 1850 = 100. Coal-by-water: equal-weighted "coal barge", "coal wharf", "coal boat", "canal boat". Coal-by-steam: "steam engine", "steam power". Source: Google Books Ngram corpus, British English 2019 edition.</em>
</div>

The ordering does not depend on the smoothing or the reference year. Across three-, five- and nine-year windows and with 1830 or 1850 as reference, "coal barge" crosses a quarter of its reference level in 1780–1781, "canal" in 1763–1766, "steam engine" in 1807–1809 and "steam power" in 1822–1826; the coal-by-water group crosses between 1785 and 1801 and the coal-by-steam group between 1814 and 1819 in every combination. "Coal wharf" is the one sensitive term, crossing in 1776 or 1800 depending on the reference, and in both cases before steam. Read as decades, the order is stable.

The corpus also tells us what kind of thing the infrastructure vocabulary measures. The frequency of "canal" correlates at 0.91 with the cumulative mileage of canals in existence over 1740–1850 and at −0.04 with the mileage opened in the surrounding decade; linearly detrended, the first correlation falls to 0.23, and in first differences to 0.16. Print records the level of the network, which is written about every year it exists, not the rate of building. The vocabulary index is a fair proxy for infrastructure in place and a poor one for investment, and we use it only in the first sense.

## 4.6 Why the cross-country test fails

The natural test of an eighteenth-century British take-off is a difference-in-differences on Maddison GDP per head, treating Britain from 1761 against continental controls. In levels, with France and the Netherlands as controls, year and country effects and Newey–West errors on the stacked panel, the treatment coefficient is 1,251 international dollars with a p-value of 0.042; the collapsed two-period estimator of Bertrand, Duflo and Mullainathan gives 0.63 (Bertrand, Duflo, and Mullainathan 2004). In logs the same design returns coefficients of 0.08 to 0.31 with p-values below 0.001 for every control group and window we tried, including windows ending in 1790. Taken at face value these say that Britain pulled away from the continent from 1761. We do not take them at face value, for three reasons.

First, the event study fails on both sides of the treatment. In ten-year bins relative to 1751–60, Britain's log gap to the Netherlands and France is significantly negative in the 1700s and 1710s and significantly positive by the 1780s; against France, Sweden, Germany and Spain the pre-treatment bins are negative and significant from 1691 to 1731. Britain was converging on the continent for the first half of the century, so there is no parallel pre-trend to break. Second, the gap opens in two steps, both on the control side. A sup-F search on the log gap to the Netherlands and France places the single break in 1807, with 1805–1809 as the next candidates. Figure 5 shows what happened then: Britain's income per head, indexed to 1790, stood at 109 in 1805 and 114 in 1815; the Netherlands' at 100 in 1805, 63 in 1808 and 72 in 1815. The earlier step, in the 1780s and 1790s, is the French series falling by a fifth during the Revolution. Third, underneath both, Britain's own income per head grew at 0.08 per cent a year between 1760 and 1790. There was no canal-era per-capita acceleration for any control group to reveal. The design was measuring the right country with the wrong variable in the wrong decade.

Table 6 gives the drawdowns for the whole panel. Between the late 1780s and the Napoleonic trough the Netherlands lost 44 per cent of its income per head, Portugal 48, Sweden 27, France 22 and Spain 13. Britain lost 1.4 per cent. The 1761 "treatment effect" measured against a continental control group is, to a first approximation, the difference between being blockaded and doing the blockading. Of the growth in the level gap between 1761 and 1900, 39 per cent occurs in the war years 1790–1815 alone; a counterfactual that attributes the pre-1810 share of that gap to canals inherits the war.

**Table 6: GDP per head, peak 1785–95 to trough 1795–1815 (Maddison Project Database 2023, 2011 international dollars)**

| Country | Peak | Trough | Drawdown | 1815 relative to 1790 |
|:--|--:|--:|--:|--:|
| Britain (UK) | 3,207 (1795) | 3,161 (1798) | −1.4% | +13.6% |
| Netherlands | 4,666 (1794) | 2,632 (1808) | −43.6% | −28.3% |
| Portugal | 2,063 (1785) | 1,072 (1811) | −48.0% | −24.1% |
| Sweden | 1,661 (1791) | 1,221 (1809) | −26.5% | −11.9% |
| France | 2,016 (1788) | 1,580 (1801) | −21.7% | +1.3% |
| Spain | 1,454 (1790) | 1,265 (1811) | −13.0% | +3.2% |
| Germany | 1,820 (1792) | 1,725 (1805) | −5.2% | +8.1% |

*Source: Maddison Project Database 2023 (Bolt and van Zanden 2025). The series labelled Britain is the United Kingdom, including Ireland.*

<div align="center">
  <img src="../../data/fig5_war_confound.png" alt="Figure 5: The 1807 break is the Dutch collapse" width="700">
  <br>
  <em><strong>Figure 5: The 1807 "break" in the cross-country design is the Dutch collapse.</strong> GDP per head, 1790 = 100, for Britain, France and the Netherlands, with the Revolutionary and Napoleonic war years shaded and the estimated break in the Britain–controls gap marked. Source: Maddison Project Database 2023 (Bolt and van Zanden 2025).</em>
</div>

## 4.7 The pre-steam divergence in benchmark years

What the cross-country data can establish is the aggregate divergence, and they establish it at benchmark years where population is measured rather than interpolated. Table 7 gives growth between 1700 and 1820, which is before steam supplied a third of British power. The Maddison series for Britain is the United Kingdom including Ireland; the Broadberry series for Great Britain alone is shown beneath it. On either measure British output roughly tripled. The next European economy, Germany, doubled; France grew by half; the Netherlands by 9 per cent. Britain's population grew by more than any other country in the European panel, and Britain was the only economy in the panel to double its population while also raising income per head.

**Table 7: Growth between benchmark years, per cent**

| | GDP per head 1700–1820 | Population 1700–1820 | Total GDP 1700–1820 | GDP per head 1820–1870 |
|:--|--:|--:|--:|--:|
| Britain (UK, Maddison) | +37 | +148 | +240 | +76 |
| Great Britain (Broadberry) | +37 | +125 | +209 | +76 |
| Germany | +35 | +66 | +124 | +44 |
| Belgium | +8 | +72 | +85 | +82 |
| Spain | +22 | +39 | +69 | +16 |
| France | +3 | +46 | +50 | +65 |
| Sweden | −29 | +104 | +44 | +52 |
| Netherlands | −11 | +23 | +9 | +47 |
| China | −43 | +176 | +58 | +7 |

*Sources: Maddison Project Database 2023 (Bolt and van Zanden 2025); Great Britain row from the Bank of England millennium dataset (Broadberry et al. 2015). The 1700 figure for China is contested (Broadberry, Guan, and Li 2018).*

The Dutch and Belgian rows are the comparative cases Tvedt's argument invites, and we discuss what they can and cannot show in the next section.


---

# 5. Discussion

## 5.1 Floated before fired

The results describe an economy that changed gear twice. The first change, in the 1770s and 1780s, was in the quantity of things: coal dug, iron smelted, goods made, people fed. The second, after 1818, was in the quantity per person. The first coincided with the building of the canal network and ran on water power and horse-drawn barges; the second coincided with steam becoming the majority power source. Coal is the hinge between them. Its output per head doubled during the first regime, when steam supplied between a twentieth and a fifth of installed power, and it is the one outcome whose response to the canal stock survives every specification, including the most demanding, where it retains significance only at the 7 per cent level.

This is Tvedt's sequence in the annual record. Britain's water system did not compete with coal; it delivered coal. The Bridgewater Canal existed to bring the Worsley pits to Manchester; the Grand Cross, begun in 1766 and completed when the Oxford Canal reached the Thames in 1790, joined the Trent, Mersey, Severn and Thames; the mania canals of the 1790s ran, disproportionately, from coalfields to towns. Inland canals were not the largest coal flow, since the Newcastle–London sea-coal trade carried more tonnage throughout the century (Flinn 1984; Hatcher 1993); what canals changed was where coal could go inland, and at what price (Pollard 1980). By 1800 coal was cheap far from the pithead in a way it was nowhere else in Europe, and the population had grown by half over the same forty years. We do not claim that canals caused that growth, which the demographic literature attributes to earlier marriage (Wrigley 1988); we claim that the economy fed it at constant income, and that cheap inland coal and freight were part of how. The steam engine then found, ready-made, a market, a fuel supply, a factory system organised around water wheels, and in the canal company a legal template for raising capital by Act of Parliament (Ward 1974). It had to improve on a prime mover that was, in 1800, three times its size.

## 5.2 What the first regime was, and was not

The first regime was not a rise in living standards. Income per head did not move, and the local projections show that canals did not move it. It was a rise in carrying capacity: the same income for half again as many people, sustained for two generations without the Malthusian check that had ended every earlier expansion. In Wrigley's terms this is not an escape from the organic economy, which by his definition Britain had begun to leave when it turned to coal for heat in the sixteenth century (Wrigley 1988; Warde 2007); it is the advanced organic economy working at full stretch, with mineral heat, organic power and engineered water. The escape from the ceiling in aggregate came before the escape per head, and it came before steam. Britain's engineered rivers carried the coal that the engine would later burn.

This also disposes of a false choice. Malm argues that the transition from water to steam power in the 1830s and 1840s was driven by the spatial and disciplinary needs of capital rather than by the exhaustion of water (Malm 2016). Our results are consistent with that and add a prior stage to it: before steam could be chosen over water for its portability, water had to have created the markets and the fuel supply that made a portable prime mover worth having. Allen's induced-innovation story likewise needs coal to be cheap where engines were built (Allen 2009); the canals are a large part of why it was.

## 5.3 The two clocks reconciled

The cliometric revision of the 1980s established that income per head grew slowly until 1830 and has been read as denying an eighteenth-century take-off (Crafts 1985; Crafts and Harley 1992). Our results accept the revision and deny the reading. There was a take-off in the eighteenth century; it was an aggregate one, and it was absorbed by population. The canal historians and the growth accountants have been measuring different variables and talking past each other. Table 2 shows both clocks at once: total output, industry, coal and population break between 1775 and 1792; income per head breaks in 1818. Crafts's finding that steam's contribution to productivity growth is negligible before 1830 and large after 1850 is the second regime seen from the supply side (Crafts 2004). Our finding that steam horsepower raises income per head only after 1830 is the same regime seen from the demand side.

One rival explanation of the 1818 break deserves to be named, because we have used it against the cross-country design: peace. Demobilisation, deflation and reopened trade could produce a per-capita break in 1816–1818 without steam. Absorbing a war dummy moves the estimated break from 1818 to 1816 and does not remove it, and the per-capita trend over 1816–1830, at 0.7 per cent a year, is well below the 1.2 per cent of 1830–1870. The break is real; its timing is over-determined; and the acceleration that follows it belongs to the steam decades.

## 5.4 The Great Divergence, and what this paper can say about it

For the Great Divergence debate the precondition framing sharpens the comparison, but a British time series can only frame it, not settle it. Pomeranz's question is why Britain and not the Yangzi delta, and part of his answer is that Chinese coal lay far from the Jiangnan core (Pomeranz 2000); Tvedt's is why Britain and not the Netherlands, which had the waterways, or China and India, which had coal and rivers but rivers of the wrong kind (Tvedt 2010).

The Dutch case is the one the benchmark data can speak to, and it is less clean than a slogan. The Netherlands had the densest network of engineered waterways in Europe by the 1660s (de Vries 1978). It ran on peat, not coal, and imported the coal it burned from Newcastle and Liège (de Zeeuw 1978; Kander, Malanima, and Warde 2013). Its total output grew 9 per cent between 1700 and 1820, for reasons the literature locates in trade, finance, wages and war rather than fuel (de Vries and van der Woude 1997). The case is consistent with water infrastructure not being sufficient; it does not show that coal was what was missing. Belgium is a caution rather than a confirmation: it had coal, but its coalfield canals of Mons–Condé and Charleroi–Brussels date from 1818 and 1832, and its income per head grew 8 per cent between 1700 and 1820 before the steam-led take-off Mokyr describes (Mokyr 1976). China we leave to one hedged sentence: its Maddison figure for 1700 is contested (Broadberry, Guan, and Li 2018), and a 176 per cent rise in population with a fall in income per head is what a Malthusian regime looks like, whatever its cause. On the British evidence the precondition was a match between coal and navigable water; whether the same match explains the continent is a question for a comparative paper with the data to answer it.

## 5.5 A caution for historical difference-in-differences

The cross-country result is methodological. In the long eighteenth century the control group went to war on its own territory and the treatment group did not; a comparison spanning 1790–1815 will attribute the difference to whatever the British treatment happens to be, whether canals, enclosure or the Bank of England. The remedies are the ones applied above: locate the break before interpreting the coefficient, examine the controls' own series, prefer within-country evidence where the treatment is national, and use cross-country data at benchmark years for the aggregate question they can answer. The estimator is not at fault; the history is (Roth et al. 2023).

## 5.6 What the text can and cannot measure

The most useful text result is a negative one. "Canal" correlates at 0.91 with the mileage of canals in existence and at 0.23 once both series are detrended: the corpus records the level of the built environment, not its growth, and vocabulary is a fair proxy for stock and a poor one for investment. The bigram sequencing is on firmer ground because it asks about order rather than magnitude. "Coal barge" around 1781 and "coal wharf" around 1800 record coal on the water; "steam engine" around 1808 and "steam power" around 1826 record coal in the engine. The order in the language is the order in the economy, give or take a decade, and the technical-publishing bias of the corpus works in favour of exactly this kind of vocabulary (Pechenick et al. 2015).


---

# 6. Limitations

The argument rests on timing, sequence and incidence in a single national time series, and it carries the limitations of that design.

## 6.1 The dose is endogenous

Canals were built where coal and people were. The reverse regressions confirm it: past growth in coal, total output or population predicts subsequent canal openings, and past coal growth predicts new authorisations. The dose-response coefficients are therefore not causal effects of an exogenous treatment. The predetermined doses remove contemporaneous feedback, and adding the outcome's own past growth leaves the authorisation coefficients intact, but nothing here removes anticipation: a promoter who expected coal demand to grow would seek an Act in advance of it. What the design establishes is that the canal stock precedes coal output by five to twenty years under every measure of the dose and that income per head does not respond. Turnbull's regional evidence and Alvarez-Palau and co-authors' market-access estimates supply the cross-sectional identification this paper lacks (Turnbull 1987; Alvarez-Palau et al. 2025); a county panel joining the Cambridge Group's waterway reconstruction to coal output and population, with terrain as the source of exogenous variation in canal access, is the natural next step, and we have not taken it.

## 6.2 Trending series and multiple tests

Every series in the paper trends. The level regressions in Table 3 are exposed to spurious regression; the augmented Dickey–Fuller test on their residuals rejects a unit root at 5 per cent for every outcome except population, so the level evidence for population should be discounted and the first-difference and local-projection results relied on. The fixed 1761 break is a pre-test; the sup-F statistics are reported against the Andrews critical value, and agriculture's is not significant. With eight outcomes, four specifications and four horizons, a Bonferroni threshold of about 0.002 is the honest bar: coal, industry, population beyond five years and the post-1830 steam result clear it; the five-year population response, the authorisation dose under a quadratic trend and the coal-to-steam link do not.

## 6.3 The canal series is provisional

The mileage series is built from a published reference table of 155 canals by completion year. It omits river navigations improved before 1700 and minor branches, and it dates staged openings to their completion. Priestley's authorisation dates corroborate the two waves independently, but they were recovered from optical character recognition of an 1831 text and only 152 of his 325 entries yielded a parseable regnal year; a length could not be recovered reliably. A definitive series would come from the Cambridge Group's *Inland Waterways of England and Wales, 1600–1948* dataset, which records opening and closing dates by section. Our magnitudes per thousand miles should be read with that in mind; the timing is less fragile than the coefficients.

## 6.4 Steam and water horsepower are interpolated

Kanefsky's estimates exist at four dates within our sample. The interpolated series are log-linear between them, so regressions that use them are identified from three kinks: the local projections involving steam establish ordering across benchmarks rather than annual dynamics, their standard errors understate the uncertainty, and the elasticities of industry and income per head with respect to steam should not be read as magnitudes. The same interpolation makes water horsepower collinear with the canal stock over 1760–1830 (r = 0.98), so the two halves of Tvedt's water thesis, transport and power, cannot be separated with these data; our dose is transport only. The print frequency of "steam engine" confirms the canal-to-steam ordering weakly and cannot check the steam-to-income link. Engine counts by decade from Kanefsky and Robey would tighten both (Kanefsky and Robey 1980). That steam raises income per head only after 1830 does not depend on the interpolation: it follows from the 1818 break, the 1833 crossover in installed power, and estimation on 1830–1870 alone.

## 6.5 Agriculture is an imperfect placebo

Agriculture's response to the canal stock is negative and significant at ten to fifteen years in the local projections and in first differences. We interpret this as compositional: labour and capital moved out of farming as canal-served sectors grew. It is not, strictly, a null result, and a reader who prefers a cleaner placebo can substitute income per head, which is null in every specification.

## 6.6 Text frequencies measure print, not speech

The Google Books corpus over-represents technical and legal publishing, and its British-English sub-corpus is small in the eighteenth century, so bigram frequencies before 1770 are noisy; the jump of "coal barge" from a quarter to half of its reference level in two years is a count spike, not an event. We use thresholds of a reference level rather than absolute frequencies for that reason, and we use groups of terms rather than single terms where we can. The ordering of water terms before steam terms holds for every combination of smoothing window and reference year we tried; individual crossing years move by one or two years, and "coal wharf" by more. The exact years should be read as decades. "Fire engine" also denotes a fire pump, which is why we use it only to date the terminological consolidation of "steam engine".

## 6.7 What the cross-country data cannot do

Population in the Maddison database is interpolated between 1700 and 1820, so cross-country regressions on total output over that period are not legitimate and we have not run them; Table 7 is descriptive, and its Maddison row for Britain is the United Kingdom including Ireland. The war-drawdown result is a property of the controls and so is robust to their choice, but it means that cross-country per-capita evidence for a British take-off before 1815 is, in our reading, unrecoverable from the Maddison series with any difference-in-differences design.


---

# 7. Conclusion

Britain industrialised on two clocks. The first, set in the 1770s, measured how much the economy produced and how many people it fed; the second, set around 1818, measured how much each of them had. The first ran on water. Canals carried the coal inland, water wheels drove the mills, and the aggregate economy accelerated while steam supplied a twentieth and then a fifth of its power. The second ran on steam, and it was steam that finally raised income per head. Coal connects the two: its output per head doubled in the first regime, when most of it was burned in hearths, forges and kilns rather than engines, and it is the one variable whose response to the canal network survives every specification we tried.

This is what a precondition looks like in data. Water infrastructure did not cause the Industrial Revolution in the sense of raising British incomes; it did not, and the local projections say so. It made the coal economy possible by making coal cheap far from the pit, and it made the population that would work in the steam economy possible by feeding it at constant income for two generations. Tvedt's argument that Britain's water systems were the enabling condition for its coal-based industrialisation is consistent with the annual British record from 1700 to 1870 in its sequence and in its sectoral incidence. Its comparative implication, that the Netherlands lacked the coal and China the rivers, is not tested here, and the Dutch and Belgian benchmarks show that it will need a more careful test than a slogan.

Three things follow for how the period is studied. The distinction between aggregate and per-capita growth should be made explicit in any account of the eighteenth century, because the two chronologies that have divided the literature are chronologies of different variables. Cross-country difference-in-differences spanning the Revolutionary and Napoleonic wars should be read with the controls' own histories in view, because the largest economic event of the period happened to the control group. And the digitised print record, used with care, can date the use of the built environment even where it cannot measure its growth; in this case it dates the coal barge a generation before the steam engine.

The fossil economy was floated before it was fired. That is a claim about order, and the order is in the data.


---

# 8. References

Allen, Robert C. 2009. *The British Industrial Revolution in Global Perspective*. Cambridge: Cambridge University Press.

Alvarez-Palau, Eduard J., Dan Bogart, Max Satchell, and Leigh Shaw-Taylor. 2025. "Transport and Urban Growth in the First Industrial Revolution." *The Economic Journal* 135 (668): 1191–1228. https://doi.org/10.1093/ej/ueae111.

Andrews, Donald W. K. 1993. "Tests for Parameter Instability and Structural Change with Unknown Change Point." *Econometrica* 61 (4): 821–856.

Bai, Jushan, and Pierre Perron. 1998. "Estimating and Testing Linear Models with Multiple Structural Changes." *Econometrica* 66 (1): 47–78.

Bertrand, Marianne, Esther Duflo, and Sendhil Mullainathan. 2004. "How Much Should We Trust Differences-in-Differences Estimates?" *Quarterly Journal of Economics* 119 (1): 249–275.

Bogart, Dan. 2014. "The Transport Revolution in Industrialising Britain: A Survey." In *The Cambridge Economic History of Modern Britain, Volume 1: 1700–1870*, edited by Roderick Floud, Jane Humphries, and Paul Johnson, 368–391. Cambridge: Cambridge University Press. https://doi.org/10.1017/CHO9781139815017.014.

Bolt, Jutta, and Jan Luiten van Zanden. 2025. "Maddison-Style Estimates of the Evolution of the World Economy: A New 2023 Update." *Journal of Economic Surveys* 39 (2): 631–671. https://doi.org/10.1111/joes.12618.

Broadberry, Stephen, Hanhui Guan, and David Daokui Li. 2018. "China, Europe, and the Great Divergence: A Study in Historical National Accounting, 980–1850." *Journal of Economic History* 78 (4): 955–1000.

Broadberry, Stephen, Bruce M. S. Campbell, Alexander Klein, Mark Overton, and Bas van Leeuwen. 2015. *British Economic Growth, 1270–1870*. Cambridge: Cambridge University Press.

Clark, Gregory, and David Jacks. 2007. "Coal and the Industrial Revolution, 1700–1869." *European Review of Economic History* 11 (1): 39–72.

Crafts, Nicholas F. R. 1985. *British Economic Growth during the Industrial Revolution*. Oxford: Clarendon Press.

Crafts, Nicholas F. R. 2004. "Steam as a General Purpose Technology: A Growth Accounting Perspective." *The Economic Journal* 114 (495): 338–351. https://doi.org/10.1111/j.1468-0297.2003.00200.x.

Crafts, Nicholas F. R., and C. Knick Harley. 1992. "Output Growth and the British Industrial Revolution: A Restatement of the Crafts–Harley View." *Economic History Review* 45 (4): 703–730.

Crouzet, François. 1964. "Wars, Blockade, and Economic Change in Europe, 1792–1815." *Journal of Economic History* 24 (4): 567–588.

de Vries, Jan. 1978. *Barges and Capitalism: Passenger Transportation in the Dutch Economy, 1632–1839*. Utrecht: HES Publishers.

de Vries, Jan, and Ad van der Woude. 1997. *The First Modern Economy: Success, Failure, and Perseverance of the Dutch Economy, 1500–1815*. Cambridge: Cambridge University Press.

de Zeeuw, J. W. 1978. "Peat and the Dutch Golden Age: The Historical Meaning of Energy-Attainability." *A.A.G. Bijdragen* 21: 3–31.

Fernihough, Alan, and Kevin Hjortshøj O'Rourke. 2021. "Coal and the European Industrial Revolution." *The Economic Journal* 131 (635): 1135–1149.

Flinn, Michael W. 1984. *The History of the British Coal Industry, Volume 2: 1700–1830, The Industrial Revolution*. Oxford: Clarendon Press.

Hadfield, Charles. 1984. *British Canals: An Illustrated History*. 7th ed. Newton Abbot: David and Charles.

Hatcher, John. 1993. *The History of the British Coal Industry, Volume 1: Before 1700*. Oxford: Clarendon Press.

Jordà, Òscar. 2005. "Estimation and Inference of Impulse Responses by Local Projections." *American Economic Review* 95 (1): 161–182.

Kander, Astrid, Paolo Malanima, and Paul Warde. 2013. *Power to the People: Energy in Europe over the Last Five Centuries*. Princeton: Princeton University Press.

Kanefsky, John W. 1979. "The Diffusion of Power Technology in British Industry, 1760–1870." PhD thesis, University of Exeter.

Kanefsky, John, and John Robey. 1980. "Steam Engines in 18th-Century Britain: A Quantitative Assessment." *Technology and Culture* 21 (2): 161–186.

Landes, David S. 1969. *The Unbound Prometheus: Technological Change and Industrial Development in Western Europe from 1750 to the Present*. Cambridge: Cambridge University Press.

Maw, Peter. 2013. *Transport and the Industrial City: Manchester and the Canal Age, 1750–1850*. Manchester: Manchester University Press.

Malm, Andreas. 2016. *Fossil Capital: The Rise of Steam Power and the Roots of Global Warming*. London: Verso.

Michel, Jean-Baptiste, Yuan Kui Shen, Aviva Presser Aiden, Adrian Veres, Matthew K. Gray, and Erez Lieberman Aiden. 2011. "Quantitative Analysis of Culture Using Millions of Digitized Books." *Science* 331 (6014): 176–182.

Mokyr, Joel. 1976. *Industrialization in the Low Countries, 1795–1850*. New Haven: Yale University Press.

Newey, Whitney K., and Kenneth D. West. 1987. "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix." *Econometrica* 55 (3): 703–708.

Pechenick, Eitan Adam, Christopher M. Danforth, and Peter Sheridan Dodds. 2015. "Characterizing the Google Books Corpus: Strong Limits to Inferences of Socio-Cultural and Linguistic Evolution." *PLOS ONE* 10 (10): e0137041.

Pollard, Sidney. 1980. "A New Estimate of British Coal Production, 1750–1850." *Economic History Review* 33 (2): 212–235.

Pomeranz, Kenneth. 2000. *The Great Divergence: China, Europe, and the Making of the Modern World Economy*. Princeton: Princeton University Press.

Priestley, Joseph. 1831. *Historical Account of the Navigable Rivers, Canals, and Railways, throughout Great Britain*. London: Longman, Rees, Orme, Brown and Green.

Rambachan, Ashesh, and Jonathan Roth. 2023. "A More Credible Approach to Parallel Trends." *Review of Economic Studies* 90 (5): 2555–2591.

Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. "What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature." *Journal of Econometrics* 235 (2): 2218–2244.

Szostak, Rick. 1991. *The Role of Transportation in the Industrial Revolution: A Comparison of England and France*. Montreal: McGill-Queen's University Press.

Thomas, Ryland, and Nicholas Dimsdale. 2017. *A Millennium of UK Data*. Bank of England OBRA dataset. https://www.bankofengland.co.uk/statistics/research-datasets.

Turnbull, Gerard. 1987. "Canals, Coal and Regional Growth during the Industrial Revolution." *Economic History Review* 40 (4): 537–560.

Tvedt, Terje. 2010. "Why England and Not China and India? Water Systems and the History of the Industrial Revolution." *Journal of Global History* 5 (1): 29–50.

Ward, J. R. 1974. *The Finance of Canal Building in Eighteenth-Century England*. Oxford: Oxford University Press.

Warde, Paul. 2007. *Energy Consumption in England and Wales, 1560–2000*. Naples: CNR-ISSM.

Wrigley, E. A. 1988. *Continuity, Chance and Change: The Character of the Industrial Revolution in England*. Cambridge: Cambridge University Press.

Wrigley, E. A. 2010. *Energy and the English Industrial Revolution*. Cambridge: Cambridge University Press.

Wrigley, E. A. 2016. *The Path to Sustained Growth: England's Transition from an Organic Economy to an Industrial Revolution*. Cambridge: Cambridge University Press.

---

# Data Availability Statement

All code and data required to reproduce the analyses are publicly available at [https://github.com/percw/water_and_society](https://github.com/percw/water_and_society). British sectoral output, population and capital stock are from the Bank of England's *A Millennium of Macroeconomic Data for the UK* (Thomas and Dimsdale 2017), which reproduces Broadberry et al. (2015). Cross-country GDP per head and population are from the Maddison Project Database 2023 (Bolt and van Zanden 2025). Installed horsepower benchmarks are from Kanefsky (1979) as reported in Crafts (2004). Canal completion years and lengths are compiled from published reference tables and parliamentary authorisation years are parsed from the digitised text of Priestley (1831); both series are included in the repository with their construction scripts. Word and phrase frequencies are from the Google Books Ngram Corpus, British English 2019 edition. A self-contained replication package is available as a supplementary archive.


---

