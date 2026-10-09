#!/usr/bin/env python3
"""Imbalance report: quantify non-negativity violations in the ledger.

Per PLAN.md, each imbalance is a bad link, a bad date, or a real phenomenon.
The central-office deficit is EXPLAINED (receipts given to deliverers);
this report quantifies it and hunts for UNEXPLAINED anomalies.
"""
import sqlite3, csv, json
from collections import defaultdict

cx = sqlite3.connect('ledger/drehem-ledger.db')

print("=" * 70)
print("DREHEM LEDGER — IMBALANCE REPORT")
print("=" * 70)

# 1. Institutional deficit by commodity (all years)
print("\n1. CENTRAL OFFICE DEFICIT (explained: receipts given to deliverers)")
print(f"{'commodity':10} {'in':>12} {'out':>12} {'net':>12} {'deficit %':>10}")
tot_in = tot_out = 0
for r in cx.execute('''
    SELECT t.commodity, SUM(CASE WHEN t.txn_type='receipt' THEN t.qty ELSE 0 END),
           SUM(CASE WHEN t.txn_type='disbursement' THEN t.qty ELSE 0 END)
    FROM transactions t
    GROUP BY t.commodity ORDER BY 3 DESC LIMIT 12'''):
    net = (r[1] or 0) - (r[2] or 0)
    pct = -net / (r[2] or 1) * 100
    print(f"{r[0]:10} {(r[1] or 0):>12,} {(r[2] or 0):>12,} {net:>12,} {pct:>9.1f}%")
    tot_in += r[1] or 0
    tot_out += r[2] or 0
print(f"{'TOTAL':10} {tot_in:>12,} {tot_out:>12,} {tot_in-tot_out:>12,} "
      f"{-(tot_in-tot_out)/tot_out*100:>9.1f}%")

# 2. Entities with largest unexplained deficits (excluding central office)
print("\n2. LARGEST ENTITY DEFICITS (outflow >> inflow), udu, all years")
print(f"{'entity':22} {'type':10} {'in':>10} {'out':>10} {'net':>10}")
for r in cx.execute('''
    SELECT e.canon, e.etype,
           SUM(b.inflow), SUM(b.outflow)
    FROM balances b JOIN entities e ON b.eid = e.eid
    WHERE b.commodity = 'udu' AND e.canon != 'ab-ba-sa-ga'
    GROUP BY e.eid HAVING SUM(b.outflow) > 1000
    ORDER BY SUM(b.inflow) - SUM(b.outflow) LIMIT 15'''):
    net = (r[2] or 0) - (r[3] or 0)
    print(f"{r[0]:22} {r[1]:10} {(r[2] or 0):>10,} {(r[3] or 0):>10,} {net:>10,}")

# 3. Entities with surplus (inflow >> outflow) — potential missing outflow records
print("\n3. LARGEST ENTITY SURPLUSES (inflow >> outflow), udu, all years")
print(f"{'entity':22} {'type':10} {'in':>10} {'out':>10} {'net':>10}")
for r in cx.execute('''
    SELECT e.canon, e.etype,
           SUM(b.inflow), SUM(b.outflow)
    FROM balances b JOIN entities e ON b.eid = e.eid
    WHERE b.commodity = 'udu'
    GROUP BY e.eid HAVING SUM(b.inflow) > 500
    ORDER BY SUM(b.inflow) - SUM(b.outflow) DESC LIMIT 10'''):
    net = (r[2] or 0) - (r[3] or 0)
    print(f"{r[0]:22} {r[1]:10} {(r[2] or 0):>10,} {(r[3] or 0):>10,} {net:>10,}")

# 4. Undated transactions (can't be balanced by year)
n_und = cx.execute("SELECT COUNT(*) FROM transactions WHERE year IS NULL").fetchone()[0]
print(f"\n4. UNDATED TRANSACTIONS: {n_und:,} "
      f"({n_und/59574*100:.1f}% of ledger — excluded from annual balances)")

# 5. Low-confidence transactions
n_lo = cx.execute("SELECT COUNT(*) FROM transactions WHERE conf='medium'").fetchone()[0]
print(f"5. MEDIUM-CONFIDENCE CLAUSES: {n_lo:,} "
      f"({n_lo/59574*100:.1f}% — bare-name attribution, needs review)")

cx.close()
print("\n" + "=" * 70)
