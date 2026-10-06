import csv,json,urllib.request,datetime as dt,sys
sys.path.insert(0,'scripts')
def yahoo(s,D):
    u=f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?period1={int((D-dt.timedelta(days=12)).timestamp())}&period2={int((D+dt.timedelta(days=60)).timestamp())}&interval=1d"
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30))['chart']['result'][0]
    q=d['indicators']['quote'][0]
    return [(dt.datetime.fromtimestamp(t,dt.UTC).date(),c) for t,c,v in zip(d['timestamp'],q['close'],q['volume']) if c and (v or s.startswith('^') or s.endswith('00.IS'))]
def moex(s,D):
    kind='index' if s=='IMOEX' else 'shares/boards/TQBR'
    u=f"https://iss.moex.com/iss/history/engines/stock/markets/{kind}/securities/{s}.json?from={(D-dt.timedelta(days=12)).date()}&till={(D+dt.timedelta(days=60)).date()}&iss.only=history&history.columns=TRADEDATE,CLOSE"
    d=json.load(urllib.request.urlopen(u,timeout=30))['history']['data']
    return [(dt.date.fromisoformat(a),c) for a,c in d if c]
def rets(p,D):
    # US announcements land after Istanbul/Seoul/Moscow close: measure from the announcement-day close
    base=[c for t,c in p if t<=D.date()][-1]; after=[c for t,c in p if t>D.date()]
    return [after[n-1]/base-1 if len(after)>=n else None for n in (1,5,20)]
f=lambda x:'' if x is None else f"{x*100:+.1f}"
rows=list(csv.DictReader(open('data/bank_actions_events.csv')))
w=csv.writer(open('data/bank_actions_price_impact.csv','w'))
w.writerow(list(rows[0])+['excess_1d_pct','excess_5d_pct','excess_20d_pct'])
for r in rows:
    out=['','','']
    if r['ticker']:
        D=dt.datetime.fromisoformat(r['date']).replace(tzinfo=dt.UTC)
        g=moex if r['index']=='IMOEX' else yahoo
        a=rets(g(r['ticker'],D),D); b=rets(g(r['index'],D),D)
        out=[f(x-y) if x is not None and y is not None else '' for x,y in zip(a,b)]
    w.writerow(list(r.values())+out); print(r['date'],r['bank'][:24].ljust(24),*[o.rjust(6) for o in out])
