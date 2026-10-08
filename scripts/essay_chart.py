"""Figure 1 of the main page: 5-day share move against the local index for every listed company hit by a US Iran action, plus the largest fines."""
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': '#1f2937', 'axes.labelcolor': '#6b7280', 'xtick.color': '#6b7280', 'ytick.color': '#6b7280', 'axes.edgecolor': '#9ca3af', 'axes.grid': True, 'grid.color': '#e5e7eb', 'axes.axisbelow': True, 'axes.titlecolor': '#1f2937'})
plt.rcParams.update({'font.size': 10.5, 'axes.spines.top': False, 'axes.spines.right': False})

CUT = {'ZTE', 'COSCO Shipping Energy', 'Hengli Petrochemical'}
rows = []
for r in csv.DictReader(open('data/iran_enforcement_price_impact.csv')):
    if not r['excess_5d_pct']:
        continue
    y, v, t = r['date'][:4], float(r['excess_5d_pct']), r['type']
    mkt = ' (Shenzhen)' if r['ticker'].endswith('.SZ') and r['company'] == 'ZTE' else ' (Shanghai)' if r['ticker'].endswith('.SS') and r['company'] in ('Qingdao Port', 'COSCO Shipping Energy') else ''
    name = f"{r['company']}{mkt}, {y}"
    if r['company'] in CUT and t == 'sanction':
        rows.append((name, v, 'Main business cut off'))
    elif t == 'sanction':
        rows.append((name, v, 'Part-owned terminal sanctioned'))
    elif r['company'] == 'Standard Chartered' and r['date'] == '2012-08-06':
        rows.append(('Standard Chartered, 2012 (licence threat)', v, 'Bank threatened or charged'))
    elif t == 'fine' and r['amount_usd_m'] and float(r['amount_usd_m']) >= 300:
        rows.append((f"{r['company']}, {y} (${float(r['amount_usd_m']):.0f}M fine)", v, 'Fine of $300M or more'))
for r in csv.DictReader(open('data/bank_actions_price_impact.csv')):
    if r['excess_5d_pct'] and r['bank'] != 'Industrial Bank of Korea' and r['action_type'] != 'charges dropped':
        rows.append((f"{r['bank'].replace(' Bank', '')}, {r['date'][:4]} ({r['action_type']})", float(r['excess_5d_pct']), 'Bank threatened or charged'))
rows = [(n + ' (−25% after 20 days)' if n.startswith('Hengli') else n, v, g) for n, v, g in rows]
rows.sort(key=lambda x: x[1])
colors = {'Main business cut off': '#b45309', 'Bank threatened or charged': '#475569', 'Part-owned terminal sanctioned': '#0066cc', 'Fine of $300M or more': '#cbd5e1'}
fig, ax = plt.subplots(figsize=(9, 0.3 * len(rows) + 1.4))
ax.barh(range(len(rows)), [v for _, v, _ in rows], color=[colors[g] for _, _, g in rows])
ax.set_yticks(range(len(rows)), [n for n, _, _ in rows])
ax.invert_yaxis()
ax.axvline(0, color='#1f2937', lw=0.6)
ax.set_xlabel('Share move vs local index, 5 trading days after the action (%)')
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, label=g) for g, c in colors.items()], loc='lower left', frameon=False)
ax.set_title('Only being cut off crashes the stock', loc='left', fontweight='bold')
fig.tight_layout()
import io
from PIL import Image
buf = io.BytesIO(); fig.savefig(buf, dpi=130)
Image.open(buf).convert('RGB').quantize(64).save('assets/fig1_every_company_hit.png', optimize=True)
print(len(rows)); [print(r) for r in rows]
