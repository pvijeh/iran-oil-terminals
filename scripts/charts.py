"""Charts for index.md: price path around US actions, timeline of actions, Halkbank vs Istanbul index."""
import csv, json, time, statistics, urllib.request, datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': '#1f2937', 'axes.labelcolor': '#6b7280', 'xtick.color': '#6b7280', 'ytick.color': '#6b7280', 'axes.edgecolor': '#9ca3af', 'axes.grid': True, 'grid.color': '#e5e7eb', 'axes.axisbelow': True, 'axes.titlecolor': '#1f2937'})
import io
from PIL import Image
def save(fig, path):
    buf = io.BytesIO(); fig.savefig(buf, dpi=130)
    Image.open(buf).convert('RGB').quantize(64).save(path, optimize=True)
import matplotlib.dates as mdates

ASIA = ('.HK', '.SS', '.SZ', '.T', '.KS', '.SI', '.BK', '.NS', '.IS')
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})

def yahoo(s, a, b, interval='1d'):
    u = f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?period1={int(a.timestamp())}&period2={int(b.timestamp())}&interval={interval}"
    for _ in range(3):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))['chart']['result'][0]
            q = d['indicators']['quote'][0]
            return [(dt.datetime.fromtimestamp(t, dt.UTC).date(), c) for t, c, v in zip(d['timestamp'], q['close'], q['volume'])
                    if c and (v or s.startswith('^') or s.endswith('00.IS') or s.startswith('000') or s.startswith('399'))]
        except Exception as e:
            err = e; time.sleep(1)
    raise err

def path(ticker, index, date):
    """Company minus index, cumulative, for trading days -5..+20 around the close before the news."""
    D = dt.datetime.fromisoformat(date).replace(tzinfo=dt.UTC)
    asia = ticker.endswith(ASIA)
    p = dict(yahoo(ticker, D - dt.timedelta(days=20), D + dt.timedelta(days=120)))
    i = dict(yahoo(index, D - dt.timedelta(days=20), D + dt.timedelta(days=120)))
    days = sorted(set(p) & set(i))
    before = [t for t in days if (t <= D.date() if asia else t < D.date())]
    after = [t for t in days if t not in before]
    seq = before[-6:] + after[:20]
    b = len(before[-6:]) - 1
    if b < 5 or len(after) < 20:
        return None
    t0 = seq[b]
    return [100 * ((p[t] / p[t0]) - (i[t] / i[t0])) for t in seq]

events = list(csv.DictReader(open('data/iran_enforcement_price_impact.csv')))
banks = list(csv.DictReader(open('data/bank_actions_price_impact.csv')))

CUTOFF = {('2016-03-07', '0763.HK'), ('2018-04-16', '0763.HK'), ('2019-09-25', '1138.HK'), ('2026-04-24', '600346.SS')}
groups = {'Main business cut off (ZTE, COSCO Shipping Energy, Hengli)': [],
          'Bank or its executive charged (Halkbank)': [],
          'Part-owned oil terminal sanctioned (2025)': [],
          'Fine or settlement': []}
keys = list(groups)
for r in events:
    k = (r['date'], r['ticker'])
    if k in CUTOFF: g = keys[0]
    elif r['type'] == 'sanction' and r['date'].startswith('2025') and not r['ticker'].endswith(('.SS', '.SZ')) or k == ('2025-03-20', '600157.SS'): g = keys[2]
    elif r['type'] == 'fine': g = keys[3]
    else: continue
    groups[g].append((r['date'], r['ticker'], r['index']))
for r in banks:
    if r['bank'] == 'Halkbank' and r['date'] < '2020':
        groups[keys[1]].append((r['date'], r['ticker'], r['index']))

colors = ['#b45309', '#475569', '#0066cc', '#475569']
fig, ax = plt.subplots(figsize=(9, 5.2))
x = list(range(-5, 21))
for (g, ev), c in zip(groups.items(), colors):
    ps = []
    for e in ev:
        try:
            p = path(e[1], e[2], e[0])
        except Exception:
            p = None
        if p: ps.append(p)
        else: print('  skipped (no 20 days of prices):', e)
    med = [statistics.median(v) for v in zip(*ps)]
    ax.plot(x, med, color=c, lw=2.5, label=f"{g} — {len(ps)} cases")
    print(g, len(ps), f"day1 {med[6]:+.1f} day5 {med[10]:+.1f} day20 {med[25]:+.1f}")
ax.axvline(0, color='#1f2937', lw=0.8, ls=':')
ax.axhline(0, color='#1f2937', lw=0.6)
ax.set_xlabel('Trading days after the US action (0 = last close before the news)')
ax.set_ylabel('Share price minus local index, %')
ax.set_title('Only losing the main business crashes a stock\nTypical (median) share move around US Iran actions, 2009–2026', loc='left', fontsize=12)
ax.legend(frameon=False, fontsize=9.5, loc='lower left')
fig.tight_layout(); save(fig, 'assets/price_path_by_action.png')

# Timeline
fig, ax = plt.subplots(figsize=(9, 4.8))
style = {'fine': ('#475569', 'Fine or settlement'), 'sanction': ('#b45309', 'Sanction or export ban'), 'criminal': ('#475569', 'Criminal charge')}
seen = set()
pts = [(r['date'], r['company'] + (' (Hong Kong)' if r['ticker'].endswith('.HK') else ' (Shenzhen)' if r['ticker'].endswith('.SZ') else ''), r['type'], r['excess_5d_pct']) for r in events if r['excess_5d_pct']]
pts += [(r['date'], r['bank'], 'criminal', r['excess_5d_pct']) for r in banks
        if r['excess_5d_pct'] and r['bank'] == 'Halkbank' and r['date'] not in ('2019-10-15',) and r['date'] < '2026']
pts += [(r['date'], r['bank'], 'sanction', r['excess_5d_pct']) for r in banks if r['excess_5d_pct'] and r['bank'] == 'VTB Bank']
for d, name, t, v in pts:
    c, lab = style[t]
    ax.scatter(dt.date.fromisoformat(d), float(v), s=45, color=c, alpha=.8, label=None if lab in seen else lab); seen.add(lab)
    if float(v) < -9:
        ax.annotate(f"{name} {float(v):+.0f}%", (dt.date.fromisoformat(d), float(v)), xytext=(6, -3), textcoords='offset points', fontsize=8.5)
ax.axhline(0, color='#1f2937', lw=0.6)
ax.set_ylabel('5-day move minus local index, %')
ax.set_title('Every US Iran action against a listed company we measured\nMost moved the share price less than 5%', loc='left', fontsize=12)
ax.legend(frameon=False, fontsize=9.5, loc='lower left')
fig.tight_layout(); save(fig, 'assets/actions_timeline.png')

# Halkbank vs BIST Banks index
a, b = dt.datetime(2015, 1, 1, tzinfo=dt.UTC), dt.datetime(2020, 1, 1, tzinfo=dt.UTC)
h, i = dict(yahoo('HALKB.IS', a, b, '1wk')), dict(yahoo('XBANK.IS', a, b, '1wk'))
d = sorted(set(h) & set(i)); r0 = h[d[0]] / i[d[0]]
fig, ax = plt.subplots(figsize=(9, 4.6))
ax.plot(d, [100 * h[t] / i[t] / r0 for t in d], color='#1f2937', lw=1.6)
marks = [('2016-03-19', 'Zarrab arrested'), ('2017-03-28', 'Deputy CEO arrested'), ('2018-01-03', 'Deputy CEO convicted'),
         ('2019-10-15', 'Bank charged')]
for k, (m, lab) in enumerate(marks):
    md = dt.date.fromisoformat(m)
    ax.axvline(md, color='#b45309', lw=0.8, ls='--')
    ax.text(md, ax.get_ylim()[1] * (0.97 - 0.07 * (k % 3)), ' ' + lab, fontsize=8.5, color='#b45309')
ax.set_ylabel('Halkbank ÷ Istanbul bank index (Jan 2015 = 100)')
ax.set_title('Halkbank against other Turkish banks (BIST Banks index), 2015–2019, US actions marked\n(stops before the 2020 and 2022 share issues, which the price data does not adjust for)', loc='left', fontsize=12)
ax.xaxis.set_major_locator(mdates.YearLocator(1))
fig.tight_layout(); save(fig, 'assets/halkbank_vs_bist100.png')
