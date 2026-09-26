#!/usr/bin/env python3
"""
Canal series, version 2: the reference table (uk_canals_wiki.csv) with documented corrections.

The reference table mixes completion years with first openings and Act years for some of the
largest canals, dates the Kennet and Avon to 1727, counts the 1927 Grand Union amalgamation, and
omits the South Wales canals. data/external/canal_corrections.csv lists every change with its reason
(dates from Hadfield, British Canals, and the regional canal histories). Staged canals are dated to
completion of the through route, as the paper states.

Writes data/external/uk_canals_v2.csv and canal_cum_miles.csv (the v1 series is kept as
canal_cum_miles_v1.csv for comparison).
"""
from pathlib import Path
import pandas as pd

EXT = Path(__file__).resolve().parent.parent / 'data' / 'external'
v1 = pd.read_csv(EXT / 'uk_canals_wiki.csv'); fx = pd.read_csv(EXT / 'canal_corrections.csv')
d = v1.set_index('canal')
for r in fx.itertuples():
    if r.action == 'set':
        assert r.canal in d.index, r.canal; d.loc[r.canal, ['miles', 'year', 'region']] = [r.miles, int(r.year), r.region]
    elif r.action == 'drop':
        d = d.drop(r.canal)
    elif r.action == 'add':
        assert r.canal not in d.index, r.canal; d.loc[r.canal] = [r.miles, int(r.year), r.region]
d = d.reset_index(); d['year'] = d['year'].astype(int)
d.to_csv(EXT / 'uk_canals_v2.csv', index=False)


def cum(df):
    yr = pd.Series(0.0, index=range(1700, 1901)); yr.update(df[(df.year >= 1700) & (df.year <= 1900)].groupby('year').miles.sum())
    return yr.cumsum().rename('cum_miles')


if not (EXT / 'canal_cum_miles_v1.csv').exists():
    cum(v1).to_csv(EXT / 'canal_cum_miles_v1.csv', index_label='Year')
c1, c2 = cum(v1), cum(d)
c2.to_csv(EXT / 'canal_cum_miles.csv', index_label='Year')
print(f'v2: {len(d)} entries, {d.miles.sum():.0f} miles; {len(fx)} documented corrections')
print('Cumulative miles        ' + '  '.join(f'{y}' for y in range(1760, 1831, 10)))
print('  v1 (reference table)  ' + '  '.join(f'{c1[y]:4.0f}' for y in range(1760, 1831, 10)))
print('  v2 (corrected)        ' + '  '.join(f'{c2[y]:4.0f}' for y in range(1760, 1831, 10)))
op = c2.diff().fillna(c2.iloc[0]); print('v2 miles opened per decade:', {f'{y}s': round(op.loc[y:y + 9].sum()) for y in range(1760, 1830, 10)})
