#!/usr/bin/env python3
"""r/dataisbeautiful visualization: 40 years of Ur III state livestock flows."""
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import numpy as np

# --- Load data ---
rows = list(csv.DictReader(open('/tmp/ur3_yearly.csv')))
# Regnal order for x-axis sequencing
order = {'Šulgi': 0, 'Amar-Suen': 1, 'Šū-Suen': 2, 'Ibbi-Suen': 3}
seq = sorted(set((r['king'], int(r['year'])) for r in rows),
             key=lambda k: (order[k[0]], k[1]))
idx = {k: i for i, k in enumerate(seq)}
n = len(seq)
receipts = np.zeros(n)
disburs = np.zeros(n)
for r in rows:
    i = idx[(r['king'], int(r['year']))]
    if r['txn_type'] == 'receipt':
        receipts[i] = int(r['total'])
    elif r['txn_type'] == 'disbursement':
        disburs[i] = int(r['total'])

labels = [f"{k} {y}" for k, y in seq]
# Reign boundaries (x positions where reign changes)
bounds = []
prev = None
for i, (k, y) in enumerate(seq):
    if k != prev:
        bounds.append((i, k))
        prev = k

# --- Style: warm clay/parchment theme ---
plt.rcParams['font.family'] = 'DejaVu Sans'
BG = '#FAF6EF'
INK = '#2B2118'
GOLD = '#C8952B'      # receipts
TERRA = '#A8432A'     # disbursements
GRID = '#E4DACA'

fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

x = np.arange(n)

# Filled areas
ax.fill_between(x, 0, receipts, color=GOLD, alpha=0.85, linewidth=0,
                label='Received (inflow)')
ax.fill_between(x, 0, disburs, color=TERRA, alpha=0.55, linewidth=0,
                label='Disbursed (outflow)')
ax.plot(x, receipts, color='#8A6414', linewidth=1.5)
ax.plot(x, disburs, color='#7A2F1D', linewidth=1.5)

# Reign boundary lines + labels
for i, k in bounds:
    ax.axvline(i - 0.5, color='#B9A88F', linewidth=1, linestyle='--', alpha=0.7)
reign_mid = {}
for reign in ['Šulgi', 'Amar-Suen', 'Šū-Suen', 'Ibbi-Suen']:
    xs = [i for i, (k, y) in enumerate(seq) if k == reign]
    if xs:
        reign_mid[reign] = (min(xs) + max(xs)) / 2
ymax = max(disburs.max(), receipts.max()) * 1.22
for reign, mid in reign_mid.items():
    ax.text(mid, ymax * 0.97, reign, ha='center', va='top', fontsize=13,
            fontweight='bold', color='#6B5B45', style='italic')

# Annotate the Amar-Suen 5 spike
as5 = idx[('Amar-Suen', 5)]
ax.annotate('Amar-Suen yr 5: disbursement\nspike (54,351 head)',
            xy=(as5, disburs[as5]), xytext=(as5 + 7, disburs[as5] * 1.02),
            fontsize=10, color=INK,
            arrowprops=dict(arrowstyle='->', color=INK, lw=1.2),
            ha='left', va='bottom',
            bbox=dict(boxstyle='round,pad=0.4', fc='white', ec=GRID, alpha=0.9))

# Annotate the collapse
is_years = [i for i, (k, y) in enumerate(seq) if k == 'Ibbi-Suen']
if is_years:
    ax.annotate('State collapse:\nrecords dwindle',
                xy=(is_years[1], max(disburs[is_years[1]], 6000)),
                xytext=(is_years[0] - 6, ymax * 0.42),
                fontsize=10, color=INK,
                arrowprops=dict(arrowstyle='->', color=INK, lw=1.2),
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.4', fc='white', ec=GRID, alpha=0.9))

# Formatting
ax.set_xlim(-0.5, n - 0.5)
ax.set_ylim(0, ymax)
ax.set_ylabel('Animals (head)', fontsize=12, color=INK)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{int(v):,}'))
ax.tick_params(colors=INK, labelsize=10)
ax.set_xticks([])
ax.grid(axis='y', color=GRID, linewidth=0.8, alpha=0.8)
for spine in ax.spines.values():
    spine.set_visible(False)

# Legend
leg = ax.legend(frameon=True, facecolor='white', edgecolor=GRID,
                fontsize=11, loc='upper left', bbox_to_anchor=(0.01, 0.99))
for t in leg.get_texts():
    t.set_color(INK)

# Title block
fig.text(0.5, 0.94, 'The National Sheep Budget of Ur',
         ha='center', fontsize=24, fontweight='bold', color=INK)
fig.text(0.5, 0.905,
         'Annual livestock flows through Puzriš-Dagan (Drehem), the Ur III state\u2019s central clearinghouse  \u00b7  c. 2070\u20132025 BCE',
         ha='center', fontsize=12, color='#6B5B45', style='italic')

# Honest deficit note
fig.text(0.02, 0.02,
         'Note: outflows exceed inflows by ~48%. This is a filing pattern, not fraud \u2014 sealed intake receipts were kept\n'
         'by the deliverer as proof of delivery (Widell 2020, Orient 55), so they never entered Drehem\u2019s archive.',
         ha='left', va='bottom', fontsize=9, color='#6B5B45', style='italic')

# Source line
fig.text(0.98, 0.02,
         'Source: reconstructed from 15,745 cuneiform tablets (CDLI)  \u00b7  github.com/Fibinachi/Drehem-ledger',
         ha='right', va='bottom', fontsize=9, color='#6B5B45')

plt.tight_layout(rect=[0, 0.05, 1, 0.88])
plt.savefig('/home/hatch/workspace/drehem-ledger/webapp/reddit-viz.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print("saved")
