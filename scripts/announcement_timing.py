"""When OFAC posts sanctions-list updates (US Eastern time) and how fast shares react at the next open."""
import collections, csv, datetime as dt, json, urllib.request

def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60))

rows = []
for y in (2024, 2025, 2026):
    rows += get(f"https://sanctionslistservice.ofac.treas.gov/changes/history/{y}")
with open('data/ofac_list_publication_times.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['publication_id', 'published_us_eastern'])
    for r in sorted(rows, key=lambda r: r['datePublished']):
        w.writerow([r['publicationID'], r['datePublished'][:19]])
hours = collections.Counter(int(r['datePublished'][11:13]) for r in rows)
print(len(rows), 'updates;', sorted(hours.items()))
print('10:00-10:59', hours[10], '; 09:00-14:59', sum(hours[h] for h in range(9, 15)))

CASES = [('ZTE', '0763.HK', '^HSI', '2016-03-07'), ('COSCO Shipping Energy', '1138.HK', '^HSI', '2019-09-25'),
         ('Qingdao Port', '6198.HK', '^HSI', '2025-08-21'), ('PetroChina', '0857.HK', '^HSI', '2025-08-21'),
         ('Sinopec Kantons', '0934.HK', '^HSI', '2025-10-09'), ('Hengli Petrochemical', '600346.SS', '000001.SS', '2026-04-24'),
         ('Halkbank', 'HALKB.IS', 'XU100.IS', '2017-03-28'), ('Halkbank', 'HALKB.IS', 'XU100.IS', '2019-10-15'),
         ('Industrial Bank of Korea', '024110.KS', '^KS11', '2020-04-20')]

def daily(s, D):
    u = (f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?period1={int((D - dt.timedelta(days=8)).timestamp())}"
         f"&period2={int((D + dt.timedelta(days=90)).timestamp())}&interval=1d")
    d = get(u)['chart']['result'][0]; q = d['indicators']['quote'][0]
    return [(dt.datetime.fromtimestamp(t, dt.UTC).date(), o, c) for t, o, c, v in zip(d['timestamp'], q['open'], q['close'], q['volume'])
            if c and o and (v or s.startswith('^') or s.endswith('00.IS') or s.startswith('000'))]

with open('data/next_open_reaction.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['company', 'ticker', 'action_date', 'first_session', 'open_gap_pct', 'index_open_gap_pct', 'first_close_pct', 'index_first_close_pct', 'close_5d_pct'])
    for name, s, ix, d in CASES:
        D = dt.datetime.fromisoformat(d).replace(tzinfo=dt.UTC)
        p = daily(s, D); i = {t: (o, c) for t, o, c in daily(ix, D)}
        b = [r for r in p if r[0] <= D.date()][-1]; a = [r for r in p if r[0] > D.date()]
        ib = [i[t][1] for t in sorted(i) if t <= D.date()][-1]
        pc = lambda x: f"{100 * x:+.1f}"
        row = [name, s, d, a[0][0], pc(a[0][1] / b[2] - 1), pc(i[a[0][0]][0] / ib - 1), pc(a[0][2] / b[2] - 1), pc(i[a[0][0]][1] / ib - 1), pc(a[4][2] / b[2] - 1)]
        w.writerow(row); print(row)
