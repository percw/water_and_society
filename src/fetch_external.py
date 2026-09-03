#!/usr/bin/env python3
"""
Fetch and tidy the external series used by regime_analysis.py.

Sources
  1. Bank of England, "A millennium of macroeconomic data for the UK" (v3.1)
     -> Broadberry et al. (2015) GB sectoral output, industrial production, population,
        Feinstein capital stock. Saved as data/external/boe_gb.csv
  2. Maddison Project Database 2023 (Bolt & van Zanden 2024), via Dataverse
     -> annual GDP per capita and population for the 13-country panel, log-interpolated,
        saved as data/external/mpd_panel.csv  (population pre-1820 is benchmark-interpolated;
        use lgdppc annually, use lpop/ltot only at benchmark years 1700, 1820, 1870)
  3. Wikipedia, "List of canals in the United Kingdom" (raw wikitext via MediaWiki API)
     -> canal name, length (miles), completion year, region: data/external/uk_canals_wiki.csv
     -> cumulative canal miles opened since 1700: data/external/canal_cum_miles.csv
     NB: provisional dose series. Replace with Priestley (1831) or the CAMPOP waterways
     dataset before publication (see docs/strategy_v2.md).

Usage:  python src/fetch_external.py [--force]
Raw downloads are cached in data/external/raw/ (git-ignored).
"""
import re, sys, json, argparse
from pathlib import Path
import numpy as np, pandas as pd, requests, openpyxl

ROOT = Path(__file__).resolve().parent.parent
EXT = ROOT / 'data' / 'external'; RAW = EXT / 'raw'
RAW.mkdir(parents=True, exist_ok=True)

BOE_URL = 'https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/a-millennium-of-macroeconomic-data-for-the-uk.xlsx'
MPD_URL = 'https://dataverse.nl/api/access/datafile/421302'   # mpd2023.xlsx (DOI 10.34894/INZBF2)
WIKI_API = 'https://en.wikipedia.org/w/api.php'
PANEL = ['GBR', 'NLD', 'FRA', 'BEL', 'SWE', 'DEU', 'ESP', 'PRT', 'POL', 'ITA', 'CHN', 'IND', 'JPN']


def download(url, dest, force=False):
    if dest.exists() and not force:
        print(f'  cached: {dest.name}'); return dest
    print(f'  downloading {url}')
    r = requests.get(url, timeout=120); r.raise_for_status(); dest.write_bytes(r.content); return dest


def tidy_boe(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    def sheet(name, cols, start_row):
        ws = wb[name]; rows = list(ws.iter_rows(min_row=start_row, values_only=True))
        df = pd.DataFrame([r[:len(cols)] for r in rows], columns=cols)
        df = df[pd.to_numeric(df['Year'], errors='coerce').notna()]; df['Year'] = df['Year'].astype(int)
        return df.set_index('Year').apply(pd.to_numeric, errors='coerce')
    gdp = sheet('A7. GB GDP(O) 1700-1870', ['Year', 'Agri', 'Ind', 'Serv', 'GDP', 'nAgri', 'nInd', 'nServ', 'nGDP', 'Defl'], 9)
    ind = sheet('A4. Ind Production 1270-1870', ['Year', 'Tin', 'Iron', 'Coal', 'Textiles', 'Leather', 'Food', 'Construction', 'Books', 'MetalsMining', 'TextLeather', 'Other', 'TotalInd'], 9)
    pop = sheet('A2. Pop of Eng & GB 1086-1870', ['Year', 'PopEng', 'PopGB'], 9)
    cap = sheet('A55. Capital Stock', ['Year', 'K_nondwell_GB', 'K_dwell_GB'], 7)
    df = gdp.join(ind[['Coal', 'Iron', 'Textiles', 'TotalInd', 'Construction']]).join(pop).join(cap)
    df.to_csv(EXT / 'boe_gb.csv'); print(f'  wrote boe_gb.csv {df.shape}')


def tidy_mpd(path):
    m = pd.read_excel(path, sheet_name='Full data')
    d = m[m.countrycode.isin(PANEL) & (m.year >= 1700) & (m.year <= 1900)]
    w = d.pivot(index='year', columns='countrycode', values='gdppc').reindex(range(1700, 1901))
    p = d.pivot(index='year', columns='countrycode', values='pop').reindex(range(1700, 1901))
    lw = np.log(w).interpolate(limit_direction='both'); lp = np.log(p).interpolate(limit_direction='both')
    out = pd.DataFrame({'lgdppc': lw.stack(), 'lpop': lp.stack(), 'ltot': (lw + lp).stack()}).reset_index()
    out.columns = ['year', 'cc', 'lgdppc', 'lpop', 'ltot']
    out.to_csv(EXT / 'mpd_panel.csv', index=False); print(f'  wrote mpd_panel.csv {out.shape}')


def tidy_canals(force=False):
    dest = RAW / 'wiki_List_of_canals_in_the_United_Kingdom.txt'
    if not dest.exists() or force:
        r = requests.get(WIKI_API, params={'action': 'parse', 'page': 'List_of_canals_in_the_United_Kingdom', 'prop': 'wikitext', 'format': 'json', 'formatversion': 2, 'redirects': 1}, timeout=60)
        dest.write_text(r.json()['parse']['wikitext'])
    t = dest.read_text(); rows = []
    for tbl in t.split('{|')[1:]:
        for r in tbl.split('\n|-')[1:]:
            cells = [c.strip() for c in re.split(r'\|\|', r.strip().lstrip('|'))]
            if len(cells) < 7: continue
            name = re.sub(r'\[\[([^\]|]*)(\|[^\]]*)?\]\]', r'\1', cells[0]); name = re.sub(r'<ref.*?(/>|</ref>)', '', name).strip(' ,')
            m = re.search(r'convert\|([\d.]+)\|(mi|km)', cells[1])
            if not m: continue
            L = float(m.group(1)); L = L if m.group(2) == 'mi' else L / 1.609
            yc = cells[6]; ms = re.search(r'sort\|(\d{4})', yc); yrs = re.findall(r'1[5-9]\d\d', yc)
            if ms: y = int(ms.group(1))
            elif yrs: y = int(yrs[-1])          # completion year when a range is given
            else: continue
            rows.append((name, L, y, cells[5].strip()))
    df = pd.DataFrame(rows, columns=['canal', 'miles', 'year', 'region']).drop_duplicates('canal')
    df.to_csv(EXT / 'uk_canals_wiki.csv', index=False)
    yr = pd.Series(0.0, index=range(1700, 1901)); yr.update(df[(df.year >= 1700) & (df.year <= 1900)].groupby('year').miles.sum())
    yr.cumsum().rename('cum_miles').to_csv(EXT / 'canal_cum_miles.csv', index_label='Year')
    print(f'  wrote uk_canals_wiki.csv ({len(df)} canals, {df.miles.sum():.0f} miles) and canal_cum_miles.csv')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--force', action='store_true'); a = ap.parse_args()
    print('Bank of England millennium dataset'); tidy_boe(download(BOE_URL, RAW / 'boe_millennium.xlsx', a.force))
    print('Maddison Project Database 2023'); tidy_mpd(download(MPD_URL, RAW / 'mpd2023.xlsx', a.force))
    print('UK canal list'); tidy_canals(a.force)
