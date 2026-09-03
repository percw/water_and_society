import json, math, html
D = json.load(open(''+str(__import__('pathlib').Path(__file__).resolve().parent.parent.parent/'data'/'external'/'memo_chartdata.json')+''))

W, H = 860, 360
ML, MR, MT, MB = 56, 150, 22, 40

def nice_ticks(lo, hi, n=5, log=False):
    if log:
        lo_e, hi_e = math.floor(math.log10(lo)), math.ceil(math.log10(hi))
        t = []
        for e in range(lo_e, hi_e + 1):
            for m in (1, 2, 5):
                v = m * 10 ** e
                if lo <= v <= hi: t.append(v)
        return t
    span = hi - lo
    step = 10 ** math.floor(math.log10(span / n))
    for m in (1, 2, 2.5, 5, 10):
        if span / (step * m) <= n: step *= m; break
    t0 = math.floor(lo / step) * step
    return [round(t0 + i * step, 6) for i in range(int(span / step) + 3) if lo - 1e-9 <= t0 + i * step <= hi + 1e-9]

def line_chart(cid, years, series, title, ylab, log=False, ymin=None, ymax=None, bands=(), vlines=(), notes=(), fmt='{:.0f}'):
    """series: list of (name, values, slotclass). Returns SVG string with hover layer."""
    allv = [v for _, vals, _ in series for v in vals if v is not None]
    lo = ymin if ymin is not None else min(allv); hi = ymax if ymax is not None else max(allv)
    if not log: pad = (hi - lo) * 0.06; lo, hi = lo - pad, hi + pad
    x0, x1 = years[0], years[-1]
    pw, ph = W - ML - MR, H - MT - MB
    def X(y): return ML + (y - x0) / (x1 - x0) * pw
    def Y(v):
        if log: return MT + (1 - (math.log(v) - math.log(lo)) / (math.log(hi) - math.log(lo))) * ph
        return MT + (1 - (v - lo) / (hi - lo)) * ph
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}" data-chart="{cid}">']
    for a, b, lab in bands:
        out.append(f'<rect class="band" x="{X(a):.1f}" y="{MT}" width="{X(b)-X(a):.1f}" height="{ph}"/>')
        out.append(f'<text class="bandlab" x="{X(a)+6:.1f}" y="{MT+14}">{html.escape(lab)}</text>')
    yt = nice_ticks(lo, hi, log=log)
    for t in yt:
        out.append(f'<line class="grid" x1="{ML}" x2="{W-MR}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/>')
        out.append(f'<text class="tick" x="{ML-8}" y="{Y(t)+4:.1f}" text-anchor="end">{fmt.format(t)}</text>')
    step = 10 if x1 - x0 <= 60 else (20 if x1 - x0 <= 120 else 25 if x1 - x0 <= 200 else 50)
    xs = [y for y in range(int(math.ceil(x0 / step) * step), x1 + 1, step)]
    for y in xs:
        out.append(f'<text class="tick" x="{X(y):.1f}" y="{H-MB+18}" text-anchor="middle">{y}</text>')
    out.append(f'<line class="axis" x1="{ML}" x2="{W-MR}" y1="{MT+ph}" y2="{MT+ph}"/>')
    for yv, lab in vlines:
        out.append(f'<line class="vline" x1="{X(yv):.1f}" x2="{X(yv):.1f}" y1="{MT}" y2="{MT+ph}"/>')
        out.append(f'<text class="vlab" x="{X(yv)+5:.1f}" y="{MT+ph-6}">{html.escape(lab)}</text>')
    for name, vals, slot in series:
        pts = [(X(y), Y(v)) for y, v in zip(years, vals) if v is not None]
        d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        out.append(f'<path class="series {slot}" d="{d}"/>')
        lx, ly = pts[-1]
        out.append(f'<text class="dlabel {slot}" x="{lx+4:.1f}" y="{ly+4:.1f}">{html.escape(name)}</text>')
    for x, y, txt in notes:
        out.append(f'<text class="note" x="{X(x):.1f}" y="{Y(y):.1f}">{html.escape(txt)}</text>')
    out.append(f'<text class="ylab" x="{ML}" y="{MT-8}">{html.escape(ylab)}</text>')
    # hover layer
    out.append(f'<g class="hover" hidden><line class="cross" y1="{MT}" y2="{MT+ph}"/></g>')
    out.append(f'<rect class="hit" x="{ML}" y="{MT}" width="{pw}" height="{ph}" fill="transparent"/>')
    out.append('</svg>')
    meta = {'years': years, 'series': [{'name': n, 'values': v, 'slot': s} for n, v, s in series], 'ml': ML, 'pw': pw, 'fmt': fmt}
    return f'<figure class="fig"><figcaption class="ctitle">{html.escape(title)}</figcaption><div class="cwrap">{"".join(out)}<div class="tip" hidden></div></div><script type="application/json" class="cdata">{json.dumps(meta)}</script></figure>'

def bar_chart(cid, cats, vals, title, ylab, highlight=None, fmt='{:.0f}', horizontal=False):
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">']
    if horizontal:
        ml = 60; pw = W - ml - 70; ph = H - MT - 20; n = len(cats); bh = ph / n
        hi = max(vals) * 1.05
        for t in nice_ticks(0, hi, n=5):
            x = ml + t / hi * pw
            out.append(f'<line class="grid" x1="{x:.1f}" x2="{x:.1f}" y1="{MT}" y2="{MT+ph}"/>')
            out.append(f'<text class="tick" x="{x:.1f}" y="{MT+ph+16}" text-anchor="middle">{fmt.format(t)}</text>')
        for i, (c, v) in enumerate(zip(cats, vals)):
            y = MT + i * bh + 3; h = bh - 6; w = v / hi * pw
            cls = 's1' if c == highlight else 'smuted'
            out.append(f'<rect class="bar {cls}" x="{ml}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3"><title>{html.escape(c)}: {fmt.format(v)}</title></rect>')
            out.append(f'<text class="tick" x="{ml-8}" y="{y+h/2+4:.1f}" text-anchor="end">{html.escape(c)}</text>')
            out.append(f'<text class="vallab" x="{ml+w+6:.1f}" y="{y+h/2+4:.1f}">{fmt.format(v)}</text>')
        out.append(f'<line class="axis" x1="{ml}" x2="{ml}" y1="{MT}" y2="{MT+ph}"/>')
        out.append(f'<text class="ylab" x="{ml}" y="{MT-8}">{html.escape(ylab)}</text>')
    else:
        pw, ph = W - ML - MR, H - MT - MB; n = len(cats); bw = pw / n
        hi = max(vals) * 1.1
        for t in nice_ticks(0, hi, n=5):
            y = MT + (1 - t / hi) * ph
            out.append(f'<line class="grid" x1="{ML}" x2="{W-MR}" y1="{y:.1f}" y2="{y:.1f}"/>')
            out.append(f'<text class="tick" x="{ML-8}" y="{y+4:.1f}" text-anchor="end">{fmt.format(t)}</text>')
        for i, (c, v) in enumerate(zip(cats, vals)):
            x = ML + i * bw + bw * 0.15; w = bw * 0.7; h = v / hi * ph; y = MT + ph - h
            cls = 's1' if (highlight is None or c in highlight) else 'smuted'
            out.append(f'<rect class="bar {cls}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3"><title>{html.escape(str(c))}: {fmt.format(v)}</title></rect>')
            out.append(f'<text class="tick" x="{x+w/2:.1f}" y="{H-MB+18}" text-anchor="middle">{html.escape(str(c))}</text>')
            if v > 0: out.append(f'<text class="vallab" x="{x+w/2:.1f}" y="{y-5:.1f}" text-anchor="middle">{fmt.format(v)}</text>')
        out.append(f'<line class="axis" x1="{ML}" x2="{W-MR}" y1="{MT+ph}" y2="{MT+ph}"/>')
        out.append(f'<text class="ylab" x="{ML}" y="{MT-8}">{html.escape(ylab)}</text>')
    out.append('</svg>')
    return f'<figure class="fig"><figcaption class="ctitle">{html.escape(title)}</figcaption><div class="cwrap">{"".join(out)}</div></figure>'

def dot_chart(cid, xs, series, title, ylab, ref_label):
    lo = min(v for _, vals, _ in series for v in vals) - 0.05; hi = max(v for _, vals, _ in series for v in vals) + 0.05
    pw, ph = W - ML - MR, H - MT - MB
    def X(i): return ML + (i + 0.5) / len(xs) * pw
    def Y(v): return MT + (1 - (v - lo) / (hi - lo)) * ph
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">']
    for t in nice_ticks(lo, hi, n=5):
        out.append(f'<line class="grid{" zero" if abs(t)<1e-9 else ""}" x1="{ML}" x2="{W-MR}" y1="{Y(t):.1f}" y2="{Y(t):.1f}"/>')
        out.append(f'<text class="tick" x="{ML-8}" y="{Y(t)+4:.1f}" text-anchor="end">{t:+.1f}</text>')
    for i, x in enumerate(xs):
        if i % 2 == 0: out.append(f'<text class="tick" x="{X(i):.1f}" y="{H-MB+18}" text-anchor="middle">{x}s</text>')
    i0 = xs.index(1761)
    out.append(f'<line class="vline" x1="{X(i0)-pw/len(xs)/2:.1f}" x2="{X(i0)-pw/len(xs)/2:.1f}" y1="{MT}" y2="{MT+ph}"/>')
    out.append(f'<text class="vlab" x="{X(i0)-pw/len(xs)/2+5:.1f}" y="{MT+12}">1761 Bridgewater Canal</text>')
    for name, vals, slot in series:
        pts = [(X(i), Y(v)) for i, v in enumerate(vals)]
        out.append(f'<path class="series thin {slot}" d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + '"/>')
        for (x, y), xv, v in zip(pts, xs, vals):
            out.append(f'<circle class="dot {slot}" cx="{x:.1f}" cy="{y:.1f}" r="4.5"><title>{html.escape(name)}, {xv}s: {v:+.2f} log points</title></circle>')
        out.append(f'<text class="dlabel {slot}" x="{pts[-1][0]+6:.1f}" y="{pts[-1][1]+4:.1f}">{html.escape(name)}</text>')
    out.append(f'<text class="ylab" x="{ML}" y="{MT-8}">{html.escape(ylab)}</text>')
    out.append(f'<text class="note" x="{W-MR}" y="{H-4}" text-anchor="end">{html.escape(ref_label)}</text>')
    out.append('</svg>')
    return f'<figure class="fig"><figcaption class="ctitle">{html.escape(title)}</figcaption><div class="cwrap">{"".join(out)}</div></figure>'

# ---------- charts ----------
war = D['war']
c_war = line_chart('war', war['years'], [('Britain', war['GBR'], 's1'), ('France', war['FRA'], 's2'), ('Netherlands', war['NLD'], 's3')],
    'GDP per capita, 1790 = 100 (Maddison Project 2023)', 'Index, 1790 = 100', ymin=55, ymax=125,
    bands=[(1793, 1815, 'Revolutionary and Napoleonic Wars')], vlines=[(1807, 'estimated break in GBR–controls gap')])

gb = D['gb']
c_agg = line_chart('agg', gb['years'], [('Total GDP', gb['GDP'], 's1'), ('Population', gb['PopGB'], 's2'), ('GDP per capita', gb['GDPpc'], 's3')],
    'Great Britain: total GDP, population and GDP per capita, 1700 = 100, log scale (Broadberry et al. 2015 via Bank of England)', 'Index, 1700 = 100 (log)', log=True, ymin=60, ymax=1200,
    bands=[(1760, 1780, 'first canal wave'), (1790, 1816, 'canal mania completions')])
c_sec = line_chart('sec', gb['years'], [('Coal output', gb['Coal'], 's1'), ('Industry', gb['Ind'], 's2'), ('Agriculture', gb['Agri'], 's3')],
    'Great Britain: sectoral output, 1700 = 100, log scale', 'Index, 1700 = 100 (log)', log=True, ymin=60, ymax=4500,
    bands=[(1760, 1780, 'first canal wave'), (1790, 1816, 'canal mania completions')])

dec = D['decade']
c_dec = bar_chart('dec', [f"{d}s" for d in dec['decade']], dec['miles'], 'Canal miles opened per decade, Great Britain (155 canals, Wikipedia list, completion year)', 'Miles opened', highlight=['1760s', '1770s', '1790s', '1800s', '1810s'])

ng = D['ngram']
def idx(v, base): return [round(x / base * 100, 1) for x in v]
i1830 = ng['years'].index(1830)
c_ng = line_chart('ng', ng['years'], [('Cumulative canal miles', idx(ng['cum_miles'], ng['cum_miles'][i1830]), 's1'), ('“canal” print frequency', idx(ng['canal_ngram'], ng['canal_ngram'][i1830]), 's2')],
    'Print frequency of “canal” tracks the canal stock, not the building rate (both indexed 1830 = 100)', 'Index, 1830 = 100', ymin=0, ymax=130)

bench = [('Britain', 240), ('Germany', 124), ('Belgium', 85), ('Portugal', 75), ('Spain', 69), ('China', 58), ('France', 50), ('Sweden', 44), ('Japan', 41), ('Netherlands', 9)]
c_bench = bar_chart('bench', [b[0] for b in bench], [b[1] for b in bench], 'Growth of total real GDP, 1700 to 1820, per cent (Maddison Project 2023 benchmark years)', 'Per cent growth 1700–1820', highlight='Britain', horizontal=True)

es_x = list(range(1691, 1892, 10))
es_core = [-0.03, -0.09, -0.12, -0.04, -0.00, -0.02, 0.02, 0.01, 0.06, 0.13, 0.23, 0.37, 0.32, 0.32, 0.33, 0.39, 0.39, 0.40, 0.38, 0.39]
es_ex = [-0.13, -0.09, -0.12, -0.06, -0.04, -0.00, 0.09, 0.09, 0.07, 0.16, 0.21, 0.19, 0.13, 0.20, 0.25, 0.29, 0.29, 0.23, 0.22, 0.19]
c_es = dot_chart('es', es_x, [('vs NLD + FRA', es_core, 's1'), ('vs FRA, SWE, DEU, ESP', es_ex, 's2')],
    'Event study on log GDP per capita, 10-year bins, reference 1751–60', 'Britain relative to controls, log points', 'Two-way fixed effects, HAC standard errors. Bins before 1751 test parallel trends.')

CSS = r"""
:root{--bg:#f3f5f3;--surface:#fcfcfb;--ink:#14201f;--ink2:#4f5b5a;--muted:#858f8d;--grid:#e1e4e0;--axis:#c2c8c5;--accent:#1f6b72;--accent-ink:#17565c;--band:rgba(31,107,114,.07);--rule:rgba(20,32,31,.12);
 --s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--smuted:#b9c1be;--tipbg:#14201f;--tipink:#f3f5f3;color-scheme:light}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#101413;--surface:#181d1c;--ink:#f0f2ef;--ink2:#b7bfbc;--muted:#8a9491;--grid:#262c2a;--axis:#3a4341;--accent:#5fbfc7;--accent-ink:#7fd0d6;--band:rgba(95,191,199,.09);--rule:rgba(240,242,239,.14);--s1:#3987e5;--s2:#d95926;--s3:#199e70;--smuted:#4a5451;--tipbg:#f0f2ef;--tipink:#101413;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#101413;--surface:#181d1c;--ink:#f0f2ef;--ink2:#b7bfbc;--muted:#8a9491;--grid:#262c2a;--axis:#3a4341;--accent:#5fbfc7;--accent-ink:#7fd0d6;--band:rgba(95,191,199,.09);--rule:rgba(240,242,239,.14);--s1:#3987e5;--s2:#d95926;--s3:#199e70;--smuted:#4a5451;--tipbg:#f0f2ef;--tipink:#101413;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:"Source Sans 3",system-ui,-apple-system,"Segoe UI",sans-serif;font-size:17px;line-height:1.55;margin:0}
.wrap{max-width:900px;margin:0 auto;padding:40px 20px 80px}
.prose{max-width:66ch}
h1,h2,h3,.ctitle{font-family:"Newsreader",Georgia,"Times New Roman",serif;font-weight:500;text-wrap:balance;letter-spacing:-.005em}
h1{font-size:2.5rem;line-height:1.1;margin:.2em 0 .3em}
h2{font-size:1.7rem;line-height:1.2;margin:2.6em 0 .5em;padding-top:1.2em;border-top:1px solid var(--rule)}
h3{font-size:1.2rem;margin:1.8em 0 .4em}
.eyebrow{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink2)}
.lede{font-size:1.2rem;line-height:1.45;color:var(--ink2);margin:0 0 1.5em}
.verdict{background:var(--surface);border-left:3px solid var(--accent);padding:18px 22px;margin:1.6em 0;border-radius:0 6px 6px 0}
.verdict p{margin:.4em 0}
.verdict strong{color:var(--accent-ink)}
p{margin:0 0 1em}
ul,ol{padding-left:1.3em;margin:0 0 1em}
li{margin:.3em 0}
a{color:var(--accent-ink)}
strong{font-weight:600}
code,.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:.9em}
.fig{margin:1.6em 0 2.2em;max-width:900px}
.ctitle{font-size:1.05rem;color:var(--ink);margin:0 0 .5em}
.cwrap{position:relative;background:var(--surface);border:1px solid var(--rule);border-radius:6px;padding:8px 6px 4px;overflow-x:auto}
svg.chart{display:block;width:100%;height:auto;font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace}
.grid{stroke:var(--grid);stroke-width:1}
.grid.zero{stroke:var(--axis);stroke-width:1.5}
.axis{stroke:var(--axis);stroke-width:1}
.tick{fill:var(--muted);font-size:11px;font-variant-numeric:tabular-nums}
.ylab{fill:var(--ink2);font-size:11px}
.band{fill:var(--band)}
.bandlab{fill:var(--ink2);font-size:11px;font-family:"Source Sans 3",system-ui,sans-serif}
.vline{stroke:var(--ink2);stroke-width:1;stroke-dasharray:3 4}
.vlab{fill:var(--ink2);font-size:11px;font-family:"Source Sans 3",system-ui,sans-serif}
.note{fill:var(--muted);font-size:11px;font-family:"Source Sans 3",system-ui,sans-serif}
.series{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.series.thin{stroke-width:1.2;opacity:.7}
.s1{stroke:var(--s1)}.s2{stroke:var(--s2)}.s3{stroke:var(--s3)}
.dot{stroke:var(--surface);stroke-width:2}
.dot.s1{fill:var(--s1)}.dot.s2{fill:var(--s2)}.dot.s3{fill:var(--s3)}
.dlabel{font-size:12px;font-family:"Source Sans 3",system-ui,sans-serif;fill:var(--ink)}
.bar{stroke:none}.bar.s1{fill:var(--s1)}.bar.smuted{fill:var(--smuted)}
.vallab{fill:var(--ink2);font-size:11px;font-variant-numeric:tabular-nums}
.cross{stroke:var(--ink2);stroke-width:1}
.hover circle{stroke:var(--surface);stroke-width:2}
.tip{position:absolute;pointer-events:none;background:var(--tipbg);color:var(--tipink);font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12px;line-height:1.4;padding:6px 9px;border-radius:4px;white-space:nowrap;box-shadow:0 2px 8px rgba(0,0,0,.15)}
.tip b{font-weight:600}
table{border-collapse:collapse;width:100%;max-width:900px;margin:1em 0 1.6em;font-size:.95rem;background:var(--surface);border:1px solid var(--rule);border-radius:6px;overflow:hidden}
th,td{padding:8px 12px;text-align:left;border-bottom:1px solid var(--grid);vertical-align:top}
th{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink2);font-weight:500;background:transparent}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;font-size:.88rem}
tr:last-child td{border-bottom:none}
.tscroll{overflow-x:auto}
.small{font-size:.9rem;color:var(--ink2)}
.tag{display:inline-block;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;padding:2px 7px;border-radius:3px;border:1px solid var(--rule);color:var(--ink2);margin-right:6px;vertical-align:middle}
.steps{counter-reset:s;list-style:none;padding:0}
.steps>li{position:relative;padding-left:2.2em;margin:.9em 0}
.steps>li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:.05em;width:1.5em;height:1.5em;border-radius:50%;background:var(--accent);color:#fff;font-family:"IBM Plex Mono",monospace;font-size:.8rem;display:flex;align-items:center;justify-content:center}
footer{margin-top:3em;padding-top:1em;border-top:1px solid var(--rule);color:var(--ink2);font-size:.9rem}
@media (prefers-reduced-motion:no-preference){.hover{transition:opacity .08s}}
"""

JS = r"""
document.querySelectorAll('figure.fig').forEach(fig=>{
  const svg=fig.querySelector('svg[data-chart]'); const meta=fig.querySelector('.cdata'); if(!svg||!meta) return;
  const m=JSON.parse(meta.textContent); const tip=fig.querySelector('.tip'); const hov=svg.querySelector('.hover'); const cross=hov.querySelector('.cross');
  const hit=svg.querySelector('.hit'); const vb=svg.viewBox.baseVal;
  m.series.forEach(s=>{const c=document.createElementNS('http://www.w3.org/2000/svg','circle'); c.setAttribute('r','5'); c.setAttribute('class','dot '+s.slot); hov.appendChild(c); s.c=c;});
  // recover Y mapping from the drawn path points
  const paths=[...svg.querySelectorAll('path.series')];
  const pts=paths.map(p=>p.getAttribute('d').slice(1).split(' L').map(t=>t.split(',').map(Number)));
  function show(ev){
    const r=svg.getBoundingClientRect(); const sx=vb.width/r.width; const x=(ev.clientX-r.left)*sx;
    const n=m.years.length; let i=Math.round((x-m.ml)/m.pw*(n-1)); i=Math.max(0,Math.min(n-1,i));
    const px=m.ml+i/(n-1)*m.pw; cross.setAttribute('x1',px); cross.setAttribute('x2',px);
    let rows='<b>'+m.years[i]+'</b>';
    m.series.forEach((s,k)=>{const pt=pts[k][i]; if(!pt||isNaN(pt[1])) {s.c.setAttribute('hidden','');return;} s.c.removeAttribute('hidden'); s.c.setAttribute('cx',pt[0]); s.c.setAttribute('cy',pt[1]); const v=s.values[i]; rows+='<br>'+s.name+': '+(v==null?'–':(Math.abs(v)>=100?v.toFixed(0):v.toFixed(1)));});
    hov.hidden=false; tip.hidden=false; tip.innerHTML=rows;
    const wrap=fig.querySelector('.cwrap').getBoundingClientRect(); let tx=ev.clientX-wrap.left+14, ty=ev.clientY-wrap.top-10; if(tx+tip.offsetWidth>wrap.width-8) tx=ev.clientX-wrap.left-tip.offsetWidth-14; tip.style.left=tx+'px'; tip.style.top=ty+'px';
  }
  hit.addEventListener('mousemove',show); hit.addEventListener('mouseleave',()=>{hov.hidden=true; tip.hidden=true;});
});
"""

def tbl(head, rows, numcols=()):
    h = ''.join(f'<th class="{"n" if i in numcols else ""}">{html.escape(c)}</th>' for i, c in enumerate(head))
    b = ''.join('<tr>' + ''.join(f'<td class="{"n" if i in numcols else ""}">{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="tscroll"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

drawdown = tbl(['Country', 'Peak, 1785–95', 'Trough, 1795–1815', 'Drawdown', '1815 vs 1790'], [
    ['Britain', '3,207 (1795)', '3,161 (1798)', '−1.4%', '+13.6%'],
    ['Netherlands', '4,666 (1794)', '2,632 (1808)', '−43.6%', '−28.3%'],
    ['Portugal', '2,063 (1785)', '1,072 (1811)', '−48.0%', '−24.1%'],
    ['Sweden', '1,661 (1791)', '1,221 (1809)', '−26.5%', '−11.9%'],
    ['France', '2,016 (1788)', '1,580 (1801)', '−21.7%', '+1.3%'],
    ['Spain', '1,454 (1790)', '1,265 (1811)', '−13.0%', '+3.2%'],
    ['Germany', '1,820 (1792)', '1,725 (1805)', '−5.2%', '+8.1%'],
], numcols=(1, 2, 3, 4))

slopes = tbl(['Series (Britain, 1700–1830)', 'Trend growth before 1761, %/yr', 'Change in trend after 1761, pp/yr', 'p'], [
    ['Total GDP', '0.52', '+0.85', '<0.01'],
    ['Industrial output', '0.39', '+1.42', '<0.01'],
    ['Coal output', '0.77', '+1.62', '<0.01'],
    ['Iron output', '0.26', '+3.24', '<0.01'],
    ['Services', '0.44', '+1.07', '<0.01'],
    ['Population', '0.23', '+0.83', '<0.01'],
    ['<em>GDP per capita</em>', '0.29', '+0.02', '0.82'],
    ['<em>Agricultural output</em>', '0.82', '−0.04', '0.84'],
], numcols=(1, 2, 3))

breaks = tbl(['Series', 'Single best break (level + trend), 1700–1870', 'Best two breaks'], [
    ['Total GDP', '1792', '1775, 1818'], ['Industrial output', '1789', '1774, 1823'], ['Services', '1786', '1775, 1844'],
    ['Coal output', '1784', '1741, 1798'], ['Iron output', '1786', '—'], ['Population', '1777', '1730, 1783'], ['GDP per capita', '1818', '1720, 1818'],
], numcols=(1, 2))

dose = tbl(['Outcome (log, Britain 1700–1830)', 'Levels + linear trend', 'Levels + quadratic trend', 'First differences, 10-year cumulative', 'Horse race vs steam vocabulary'], [
    ['Coal output', '+46.5% <span class="small">(p<0.001)</span>', '+29.8% <span class="small">(p=0.001)</span>', '+27.0% <span class="small">(p<0.001)</span>', 'canal +40.8% (p<0.001), steam +12.6% (p=0.08)'],
    ['Industrial output', '+40.1% <span class="small">(p<0.001)</span>', '−0.9% <span class="small">(p=0.89)</span>', '+14.3% <span class="small">(p<0.001)</span>', 'canal +28.8% (p<0.001), steam +30.4% (p=0.003)'],
    ['Population', '+24.0% <span class="small">(p<0.001)</span>', '+4.1% <span class="small">(p=0.07)</span>', '+16.6% <span class="small">(p<0.001)</span>', 'canal +18.6%, steam +15.0% (both p<0.001)'],
    ['Total GDP', '+24.7% <span class="small">(p<0.001)</span>', '+2.2% <span class="small">(p=0.52)</span>', '+4.2% <span class="small">(p=0.25)</span>', 'canal +18.8%, steam +19.0% (both p<0.001)'],
    ['<em>GDP per capita</em>', '+0.8% <span class="small">(p=0.69)</span>', '−1.9% <span class="small">(p=0.61)</span>', '−12.4% <span class="small">(p=0.33)</span>', 'canal +0.2% (p=0.94)'],
    ['<em>Agriculture</em>', '−0.5% <span class="small">(p=0.90)</span>', '−5.1% <span class="small">(p=0.56)</span>', '−18.8% <span class="small">(p<0.001)</span>', 'canal −1.5% (p=0.72)'],
], numcols=(1, 2, 3))

bench_t = tbl(['1700 → 1820', 'GDP per capita', 'Population', 'Total GDP'], [
    ['Britain', '+37%', '+148%', '+240%'], ['Germany', '+35%', '+66%', '+124%'], ['Belgium', '+8%', '+72%', '+85%'],
    ['France', '+3%', '+46%', '+50%'], ['Sweden', '−29%', '+104%', '+44%'], ['Netherlands', '−11%', '+23%', '+9%'], ['China', '−43%', '+176%', '+58%'],
], numcols=(1, 2, 3))

page = f"""<title>Canals Before Steam</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<div class="wrap">
<div class="prose">
<div class="eyebrow">Research memo · Water and Society · 3 September 2026</div>
<h1>Canals Before Steam</h1>
<p class="lede">What the data can and cannot say about water infrastructure and British industrialisation, and how to rebuild the paper around the evidence that holds.</p>

<div class="verdict">
<p><strong>The thesis survives. The current identification does not.</strong> The 1806–1818 break the paper interprets as Britain's take-off is the Netherlands collapsing under French occupation, and British GDP per capita did not accelerate at all in the canal era. But Britain's aggregate output, coal, iron, industry and population all shift regime between 1775 and 1792, and the canal stock predicts coal output robustly. The paper should be rebuilt around a canals → coal → carrying-capacity mechanism, using sectoral output rather than GDP per capita as the outcome.</p>
</div>

<p>This memo reports a full re-analysis done outside the repository. It reuses the paper's Maddison and Google Books data, adds the Broadberry et al. (2015) sectoral series published by the Bank of England, the Maddison Project Database 2023 population benchmarks, and a canal-mileage series assembled from the completion years of 155 British canals. All numbers below reproduce from scripts in the session scratchpad and nothing in the repository was changed.</p>
</div>

<h2>What the current DiD is measuring</h2>
<div class="prose">
<p>The paper's headline effect (β₃ = 1,251, HAC p = 0.042) compares Britain with France and the Netherlands around a 1761 treatment date. A structural-break search on the Britain-minus-controls gap places the break at 1807, and the paper's own event study shows nothing significant until the bin starting 45 years after treatment. The chart below shows why. Britain's GDP per capita barely moved between 1790 and 1815. The Dutch series fell by 44 per cent.</p>
</div>
{c_war}
<div class="prose">
<p>The Revolutionary and Napoleonic Wars devastated the continental control group while Britain, uninvaded, held level. Any two-group comparison spanning 1790–1815 will therefore find a large British "effect" regardless of canals. The war years alone account for 39 per cent of the 1761–1900 growth in the level gap used for the paper's 47 per cent figure.</p>
</div>
{drawdown}
<div class="prose">
<p>Dropping the Netherlands does not rescue the design. Against France, Sweden, Germany and Spain, Britain's relative position rises in the 1760s and again in the 1790s, but the pre-1751 bins are significantly negative, so parallel trends fail in the other direction, and the 1790s step is again a control-side collapse. In levels, Britain's per-capita GDP grew 0.08 per cent a year between 1760 and 1790. There is no canal-era per-capita acceleration to detect, with any control group.</p>
</div>
{c_es}

<h2>Britain's canal-era regime shift</h2>
<div class="prose">
<p>The Broadberry et al. annual series for Great Britain tell a different story once the outcome is total rather than per-capita output. Between 1760 and 1815 the growth of aggregate GDP roughly doubled, industry and coal tripled their trend rate, and population growth rose from 0.3 to 1.2 per cent a year. GDP per capita was flat because population absorbed the entire acceleration. That is the pattern a transport-and-energy infrastructure shock should produce in an organic economy: more mouths fed at constant income, not richer mouths.</p>
</div>
{c_agg}
{c_sec}
<div class="prose">
<p>Fixing the break at 1761 and testing for a change in trend slope over 1700–1830 gives the following. Agriculture and GDP per capita are the natural placebo series, and both are flat.</p>
</div>
{slopes}
<div class="prose">
<p>Letting the data choose the break date puts the first regime change in the 1770s–1780s across every canal-served series, and a second one around 1818–1823 when steam and railways arrive. Population breaks first, in 1777. Per-capita income breaks only in 1818. The two-regime structure is the precondition thesis in the data: a canal-era acceleration of the aggregate, then a steam-era acceleration of the per-capita.</p>
</div>
{breaks}

<h2>Canal mileage as a dose</h2>
<div class="prose">
<p>The binary 1761 treatment is the wrong variable. Canal building came in two waves: the Grand Cross network of the 1760s–70s, and the mania authorised in 1791–96 and completed through 1816. A cumulative-mileage series built from completion years captures this.</p>
</div>
{c_dec}
<div class="prose">
<p>Regressing British sectoral output on the canal stock over 1700–1830 (before railways) gives large, significant coefficients for coal, industry, iron, services and population, and nothing for per-capita GDP or agriculture. The honest caveat is that a cumulative stock is itself a smooth accelerating series: with a quadratic trend added, only coal keeps its coefficient, and population marginally. In first differences, coal, industry and population all respond to canal openings over the following decade. Coal output growth also <em>predicts</em> later canal openings, so causality runs both ways, as the canal-company histories say it did.</p>
</div>
{dose}
<div class="prose">
<p>Coal is the robust channel, and it is the right one. Turnbull (1987) showed that the canals were built to move coal, and coal output per head doubled between 1700 and 1790, before any significant steam capacity existed. The fossil economy was floated on water before it was driven by it. This is a sharper and more defensible claim than "water caused GDP".</p>
</div>

<h2>The pre-steam divergence in benchmark data</h2>
<div class="prose">
<p>Maddison's population figures are interpolated between 1700 and 1820, so annual cross-country total-GDP regressions are not legitimate. The benchmark years themselves are. Between 1700 and 1820, before steam accounted for more than a small fraction of British power, Britain's total output grew by 240 per cent, twice the next European economy, while also raising income per head. No other country in the panel achieved both.</p>
</div>
{c_bench}
{bench_t}

<h2>The NLP index is a stock measure</h2>
<div class="prose">
<p>A useful methodological result for the paper: the print frequency of “canal” in the British corpus correlates at 0.91 with the cumulative mileage of canals in existence, and at roughly zero with miles opened in any given decade. Print culture tracks the built environment, not the construction boom. This is an argument for using the vocabulary index as a validated proxy for infrastructure stock, which is exactly how the DML specification already uses it, and it explains why the 1766 crossover follows the first openings rather than the authorisation acts.</p>
</div>
{c_ng}

<h2>How to rebuild the paper</h2>
<div class="prose">
<p>The contrast with the man-machine-versus-nature literature is intact and, if anything, sharper. Britain's first growth regime was a cooperation with topography that raised the economy's carrying capacity, and the fossil regime that followed depended on it physically, because coal reached markets by water. What changes is the evidence structure.</p>

<h3>Reframe the thesis</h3>
<p>Working title: <em>Canals, coal and the Malthusian escape: water infrastructure and Britain's pre-steam growth regime.</em> The claim becomes: canal-era infrastructure shifted Britain from a per-capita to an aggregate growth regime by 1775–1790, principally through coal, and per-capita divergence only appears once steam builds on that base after 1818. Agriculture and per-capita income are pre-registered placebo series.</p>

<h3>Three empirical designs, in order of strength</h3>
<ol class="steps">
<li><strong>Within-Britain dose-response with the real canal network.</strong> Request the Cambridge Group's <em>Inland waterways of England and Wales, 1600–1948</em> GIS dataset (opening and closing dates by section) from the CAMPOP transport project. Rebuild the mileage series from it rather than from Wikipedia, and estimate output responses to network growth with local-projection or distributed-lag models, reporting the quadratic-trend and first-difference specifications side by side.</li>
<li><strong>County or town panel.</strong> The same dataset, joined to the 1801–1831 census populations and the CAMPOP coal-deposit layer, allows a difference-in-differences on canal access with coalfield distance as the source of exogenous variation. Alvarez-Palau, Bogart, Satchell and Shaw-Taylor (Economic Journal, 2024) have done this for urban population and found inland towns would have been 20–25 per cent smaller without transport improvements. The paper must engage them directly. The open niche is the coal channel and the semantic evidence.</li>
<li><strong>Cross-country evidence, honestly bounded.</strong> Keep the Maddison comparison, but restrict the annual DiD to 1700–1790, report the war drawdowns as a confound, use benchmark-year total GDP for 1700–1820, and drop the 47 per cent counterfactual. Present the 1818 per-capita break as the steam-era result it is.</li>
</ol>

<h3>Keep and strengthen the text-as-data component</h3>
<ul>
<li>Report the 0.91 stock correlation as validation of the vocabulary index and describe the index as a proxy for infrastructure in place.</li>
<li>Re-run the DML with canal mileage as the treatment and the vocabulary index as an instrument or as a second measurement, which turns a rhetorical device into a measurement-error argument.</li>
<li>Extend the semantic analysis to coal vocabulary: does "coal" co-occur with "canal", "navigation" and "wharf" before it co-occurs with "engine" and "steam"? That is the linguistic form of the canals-carry-coal mechanism, and it can be tested with the bigram data already in the repository.</li>
</ul>

<h3>Data and literature to bring in</h3>
<ul>
<li>Bank of England, <em>A millennium of macroeconomic data</em> (Broadberry et al. sectoral output, population, capital stock). Already downloaded to the session scratchpad.</li>
<li>Maddison Project Database 2023, cited as Bolt and van Zanden (2024), <em>Journal of Economic Surveys</em>, DOI 10.1111/joes.12618.</li>
<li>CAMPOP inland waterways and coal-deposit GIS layers (request from the Cambridge Group; no public download link).</li>
<li>Kanefsky and Robey (1980) steam-engine counts by decade, to replace the steam vocabulary series in the horse race.</li>
<li>Turnbull (1987), <em>Economic History Review</em> 40(4): 537–560, on canals and coal; Bogart (2014) chapter in the <em>Cambridge Economic History of Modern Britain</em> (the manuscript currently cites it as a 2024 book); Alvarez-Palau et al. (2024); Crouzet (1964) on wartime economic change in Europe for the confound discussion.</li>
</ul>
</div>

<h2>Caveats on this memo</h2>
<div class="prose">
<ul>
<li>The canal-mileage series comes from a Wikipedia table (155 canals, 2,967 miles) and uses completion years. It excludes river navigations improved before 1700 and will undercount minor branches. Treat the dose-response magnitudes as provisional until the CAMPOP data replace it.</li>
<li>Broadberry et al. output indices are themselves partly interpolated between benchmark years for some sub-sectors, and their industrial series uses coal and iron output as inputs, so coal's strong result and industry's are not independent.</li>
<li>All break tests are single-series, within-Britain, and describe timing. They do not identify a causal effect on their own.</li>
<li>Steam is proxied by print frequency of “steam” in the horse race, which is exactly the kind of proxy the paper is criticised for. Engine counts should replace it.</li>
</ul>
</div>
<footer>Sources: Maddison Project Database 2023; Bank of England, <em>A millennium of macroeconomic data for the UK</em> v3.1 (Broadberry, Campbell, Klein, Overton and van Leeuwen 2015); Google Books Ngram <span class="mono">eng_gb_2019</span> via the repository's data; Wikipedia, <em>List of canals in the United Kingdom</em>. Analysis scripts and downloaded data are in the session scratchpad.</footer>
</div>
<script>{JS}</script>
"""
open(str(__import__('pathlib').Path(__file__).resolve().parent/'2026-09-03_canals_before_steam.html'), 'w').write(page)
print('written', len(page))
