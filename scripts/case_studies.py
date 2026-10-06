"""Price path for each case study: company minus local index, trading days -60..+20 around the last close before the US action."""
import csv, datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json, time, urllib.request

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


CASES = [
    ('zte-2016', 'ZTE (Hong Kong)', '0763.HK', '^HSI', '2016-03-07', 'US export ban'),
    ('zte-2018', 'ZTE (Hong Kong)', '0763.HK', '^HSI', '2018-04-16', 'US export ban'),
    ('cosco-shipping-energy-2019', 'COSCO Shipping Energy (Hong Kong)', '1138.HK', '^HSI', '2019-09-25', 'US sanctions on two tanker units'),
    ('hengli-2026', 'Hengli Petrochemical (Shanghai)', '600346.SS', '000001.SS', '2026-04-24', 'US sanctions on Dalian refinery'),
    ('halkbank-2017', 'Halkbank (Istanbul)', 'HALKB.IS', 'XU100.IS', '2017-03-28', 'US arrests deputy CEO'),
    # DFS order came out after the London close on 2012-08-06
    ('standard-chartered-2012', 'Standard Chartered (London)', 'STAN.L', '^FTSE', '2012-08-06', 'New York regulator order', True),
]

rows = []
summary = []
for slug, name, t, ix, date, label, *after_close in CASES:
    D = dt.datetime.fromisoformat(date).replace(tzinfo=dt.UTC)
    p = dict(yahoo(t, D - dt.timedelta(days=130), D + dt.timedelta(days=120)))
    i = dict(yahoo(ix, D - dt.timedelta(days=130), D + dt.timedelta(days=120)))
    days = sorted(set(p) & set(i))
    before = [d for d in days if (d <= D.date() if t.endswith(ASIA) or after_close else d < D.date())]
    after = [d for d in days if d not in before]
    seq = before[-61:] + after[:20]
    t0 = before[-1]
    xs = list(range(-len(before[-61:]) + 1, len(after[:20]) + 1))
    ys = [100 * ((p[d] / p[t0]) - (i[d] / i[t0])) for d in seq]
    for x, d, y in zip(xs, seq, ys):
        rows.append([slug, t, ix, date, x, d.isoformat(), round(y, 2)])
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(xs, ys, color='#1f4e79', lw=2)
    ax.axvline(0.5, color='#c0392b', ls='--', lw=1)
    ax.axhline(0, color='grey', lw=0.8)
    ax.text(0.8, ax.get_ylim()[1] * 0.9 if ax.get_ylim()[1] > 0 else 0, label, color='#c0392b', fontsize=10)
    ax.set_xlabel('Trading days from the US action (0 = last close before it)')
    ax.set_ylabel('% vs local index')
    ax.set_title(f'{name}: share price against the local index')
    fig.tight_layout()
    fig.savefig(f'assets/case_{slug}.png', dpi=120)
    plt.close(fig)
    pick = {x: y for x, y in zip(xs, ys)}
    pre = lambda k: 100 * ((p[t0] / p[before[-1 - k]]) - (i[t0] / i[before[-1 - k]]))
    summary.append([slug, t, ix, date] + [round(pre(k), 1) for k in (60, 20, 5)] + [round(pick[k], 1) for k in (1, 5, 20)])
    print(slug, {k: round(pick[k], 1) for k in (-60, -20, -5, 1, 5, 20) if k in pick})

with open('data/case_study_price_paths.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['case', 'ticker', 'index', 'action_date', 'trading_day', 'date', 'pct_vs_index_from_day0'])
    w.writerows(rows)

with open('data/case_study_summary.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['case', 'ticker', 'index', 'action_date', 'pre_60d_pct', 'pre_20d_pct', 'pre_5d_pct', 'post_1d_pct', 'post_5d_pct', 'post_20d_pct'])
    w.writerows(summary)
