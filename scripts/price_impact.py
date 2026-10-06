import json,urllib.request,datetime as dt,csv,time
cache={}
def get(s,D):
    u=f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?period1={int((D-dt.timedelta(days=12)).timestamp())}&period2={int((D+dt.timedelta(days=150)).timestamp())}&interval=1d"
    for i in range(3):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30))['chart']['result'][0]
            q=d['indicators']['quote'][0]
            return [(dt.datetime.fromtimestamp(t,dt.UTC).date(),c) for t,c,v in zip(d['timestamp'],q['close'],q['volume']) if c and (v or s.startswith('^') or s.endswith('.SS') and s.startswith('000'))]
        except Exception as e: err=e; time.sleep(1)
    raise err
ASIA=('.HK','.SS','.SZ','.T','.KS','.SI','.BK','.NS')
def rets(p,D,asia):
    base=[c for t,c in p if (t<=D.date() if asia else t<D.date())][-1]; after=[c for t,c in p if (t>D.date() if asia else t>=D.date())]
    # day0..: capture first 2 sessions (announcement often after close), 5 and 20 sessions
    g=lambda n: after[n-1]/base-1 if len(after)>=n else None
    return (g(1) if asia else g(2)),g(5),g(20)
rows=list(csv.DictReader(open('data/price_impact_events.csv')))
out=[]
for r in rows:
    D=dt.datetime.fromisoformat(r['date']).replace(tzinfo=dt.UTC)
    try:
        asia=r['ticker'].endswith(ASIA); a=rets(get(r['ticker'],D),D,asia); b=rets(get(r['index'],D),D,asia)
        ab=[(x-y) if x is not None and y is not None else None for x,y in zip(a,b)]
        r.update(raw_2d=a[0],excess_2d=ab[0],excess_5d=ab[1],excess_20d=ab[2])
    except Exception as e: r.update(raw_2d=None,excess_2d=None,excess_5d=None,excess_20d=None,err=str(e)[:40])
    out.append(r)
f=lambda x: '' if x is None else f"{x*100:+.1f}"
w=csv.writer(open('data/iran_enforcement_price_impact.csv','w'))
w.writerow(['date','company','ticker','index','type','action','amount_usd_m','excess_first_day_pct','excess_5d_pct','excess_20d_pct'])
for r in out:
    w.writerow([r['date'],r['company'],r['ticker'],r['index'],r['type'],r['action'],r['amount_usd_m'],f(r['excess_2d']),f(r['excess_5d']),f(r['excess_20d'])])
    print(r['date'],r['company'][:28].ljust(28),r['ticker'].ljust(11),r['type'][:5],f(r['excess_2d']).rjust(6),f(r['excess_5d']).rjust(6),f(r['excess_20d']).rjust(6),r.get('err',''))
