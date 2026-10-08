"""Figures 2-4 of the main page, from data/ CSVs. Saved as small palette PNGs (GitHub Pages' legacy build failed on a large RGBA PNG)."""
import csv, collections, io
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': '#1f2937', 'axes.labelcolor': '#6b7280', 'xtick.color': '#6b7280', 'ytick.color': '#6b7280', 'axes.edgecolor': '#9ca3af', 'axes.grid': True, 'grid.color': '#e5e7eb', 'axes.axisbelow': True, 'axes.titlecolor': '#1f2937'})
from PIL import Image
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})

def save(fig, path):
    buf = io.BytesIO(); fig.savefig(buf, dpi=130); plt.close(fig)
    Image.open(buf).convert('RGB').quantize(64).save(path, optimize=True)

# Figure 2: the six big falls, cumulative move vs index from 60 days before to 20 after
names = {'zte-2016': 'ZTE 2016: export ban', 'zte-2018': 'ZTE 2018: export ban',
         'cosco-shipping-energy-2019': 'COSCO Shipping Energy 2019: tankers',
         'hengli-2026': 'Hengli 2026: refinery sanctioned', 'halkbank-2017': 'Halkbank 2017: deputy CEO arrested',
         'standard-chartered-2012': 'Standard Chartered 2012: NY licence threat'}
paths = collections.defaultdict(list)
for r in csv.DictReader(open('data/case_study_price_paths.csv')):
    paths[r['case']].append((int(r['trading_day']), float(r['pct_vs_index_from_day0'])))
fig, axes = plt.subplots(2, 3, figsize=(11, 5.6), sharex=True, sharey=True)
for ax, (case, title) in zip(axes.flat, names.items()):
    pts = sorted(paths[case])
    ax.plot([d for d, _ in pts], [v for _, v in pts], color='#b45309', lw=1.6)
    ax.axvline(0, color='#1f2937', lw=0.7, ls='--'); ax.axhline(0, color='#e5e7eb', lw=0.5)
    ax.set_title(title, fontsize=9.5, loc='left')
for ax in axes[1]: ax.set_xlabel('Trading days from the US action')
for ax in axes[:, 0]: ax.set_ylabel('% vs local index')
fig.suptitle('Flat before, down after: the six biggest falls', x=0.01, ha='left', fontweight='bold')
fig.tight_layout(); save(fig, 'assets/fig3_six_falls.png')

# Figure 3: time of day OFAC posts list updates, with market closes (New York time, US summer time)
hrs = [datetime.fromisoformat(r['published_us_eastern']) for r in csv.DictReader(open('data/ofac_list_publication_times.csv'))]
h = [t.hour + t.minute / 60 for t in hrs]
fig, ax = plt.subplots(figsize=(9, 3.6))
ax.hist(h, bins=[x / 2 for x in range(12, 42)], color='#0066cc')
for x, lab in [(4.0, 'Hong Kong, Shanghai close'), (6.0, 'Mumbai, Dubai close'), (11.0, 'Istanbul closes'), (11.5, 'London closes'), (16.0, 'New York closes')]:
    ax.axvline(x, color='#b45309', lw=0.9, ls='--'); ax.text(x + 0.1, ax.get_ylim()[1] * 0.92, lab, rotation=90, va='top', fontsize=8.5, color='#b45309')
ax.set_xlim(3, 20); ax.set_xticks(range(3, 21, 2), [f'{x}:00' for x in range(3, 21, 2)])
ax.set_xlabel('Time posted, New York time'); ax.set_ylabel('List updates (2024 to Oct 2026)')
ax.set_title(f'OFAC posts after Asia has closed ({len(h)} sanctions-list updates)', loc='left', fontweight='bold')
fig.tight_layout(); save(fig, 'assets/fig4_ofac_posting_times.png')

# Figure 4: every fine, size against 5-day share move
fines = [r for r in csv.DictReader(open('data/iran_enforcement_price_impact.csv')) if r['type'] == 'fine' and r['excess_5d_pct'] and r['amount_usd_m']]
fig, ax = plt.subplots(figsize=(9, 4.2))
xs = [float(r['amount_usd_m']) for r in fines]; ys = [float(r['excess_5d_pct']) for r in fines]
ax.scatter(xs, ys, color='#475569', s=28)
ax.axhspan(-5, 5, color='#f1f5f9', zorder=0); ax.axhline(0, color='#1f2937', lw=0.5)
ax.set_xscale('log'); ax.set_xlabel('Fine (US$ millions, log scale)'); ax.set_ylabel('Share move vs index, 5 days (%)')
for r, x, y in zip(fines, xs, ys):
    if x >= 600 or abs(y) >= 5: ax.annotate(f"{r['company'].split(' (')[0]} {r['date'][:4]}", (x, y), fontsize=8, xytext=(4, 3), textcoords='offset points')
inside = sum(abs(y) < 5 for y in ys)
ax.set_title(f'Fines: {inside} of {len(ys)} moved the shares less than 5% (shaded band)', loc='left', fontweight='bold')
fig.tight_layout(); save(fig, 'assets/fig2_fines.png')
print(len(fines), inside)

# Figure 5: names added under Iran programs per year, from the OFAC recent-actions pages we parsed (2022 on)
c = collections.Counter(r['action_date'][:4] for r in csv.DictReader(open('data/ofac_iran_designations.csv'))
                        if any(p in r['programs'] for p in ('IRAN', 'IFSR', 'IRGC')))
yrs = [str(y) for y in range(2022, 2027)]
fig, ax = plt.subplots(figsize=(7, 3.2))
ax.bar(yrs, [c[y] for y in yrs], color=['#cbd5e1'] * 3 + ['#b45309'] * 2)
for i, y in enumerate(yrs): ax.text(i, c[y] + 8, str(c[y]), ha='center', fontsize=9)
ax.set_ylabel('Names added'); ax.set_xticks(range(5), yrs[:-1] + ['2026 (to Oct)'])
ax.set_title('Names OFAC added under its Iran programs, per year', loc='left', fontweight='bold')
fig.tight_layout(); save(fig, 'assets/fig5_designations_per_year.png')
print({y: c[y] for y in yrs})
