#!/usr/bin/env python3
"""Export Drehem ledger SQLite data to JS files for the static QuickBooks-style web app."""
import sqlite3, json, os, math

REPO = os.path.expanduser("~/workspace/drehem-ledger")
DB = os.path.join(REPO, "ledger/drehem-ledger.db")
OUT = os.path.join(REPO, "webapp/data")
CHUNK = os.path.join(OUT, "txn")
os.makedirs(CHUNK, exist_ok=True)

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

# --- canonical king mapping ---
KINGS = {
    "Šulgi":     ("Šulgi", 0),
    "Amar-Suen": ("Amar-Suen", 48),
    "Šū-Suen":   ("Shu-Suen", 57),
    "Ibbi-Suen": ("Ibbi-Suen", 66),
}
def abs_year(king, year):
    if king in KINGS and year:
        return KINGS[king][1] + year
    return None

def disp_king(king):
    return KINGS.get(king, (king, 0))[0]

COMMODITY_EN = {
    "udu": "sheep", "u8": "ewe", "sila4": "lamb", "kir11": "suckling lamb",
    "masz2": "goat", "ud5": "she-goat", "masz-da3": "gazelle",
    "gu4": "ox", "ab2": "cow", "amar": "calf", "gukkal": "fat-tailed sheep",
    "lulim": "red deer", "szeg9-bar": "wild goat", "uz": "duck",
    "dara4": "dara4 (unidentified)",
}
LIVESTOCK = list(COMMODITY_EN.keys())

def js_write(path, varname, obj):
    with open(path, "w") as f:
        f.write(f"var {varname} = ")
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";")

# ---------- summary ----------
n_txn = cur.execute("SELECT COUNT(*) c FROM transactions").fetchone()["c"]
n_tab = cur.execute("SELECT COUNT(*) c FROM tablets").fetchone()["c"]
n_ent = cur.execute("SELECT COUNT(*) c FROM entities").fetchone()["c"]
dated = cur.execute("SELECT COUNT(*) c FROM transactions WHERE king IS NOT NULL AND king NOT IN ('00','--')").fetchone()["c"]
totals = {r["txn_type"]: (r["c"], r["q"]) for r in cur.execute(
    "SELECT txn_type, COUNT(*) c, SUM(qty) q FROM transactions GROUP BY txn_type")}
rec, dis, tra = totals.get("receipt", (0,0)), totals.get("disbursement", (0,0)), totals.get("transfer", (0,0))
rows = cur.execute("SELECT king, MIN(year) mn, MAX(year) mx FROM transactions WHERE king IN ('Šulgi','Amar-Suen','Šū-Suen','Ibbi-Suen') AND year>0 GROUP BY king").fetchall()
absmin = min(abs_year(r["king"], r["mn"]) for r in rows)
absmax = max(abs_year(r["king"], r["mx"]) for r in rows)
deficit = dis[1] - rec[1]
summary = {
    "tablets": n_tab, "transactions": n_txn, "entities": n_ent,
    "datedPct": round(100*dated/n_txn, 1),
    "receipts": {"n": rec[0], "qty": rec[1]},
    "disbursements": {"n": dis[0], "qty": dis[1]},
    "transfers": {"n": tra[0], "qty": tra[1]},
    "deficit": deficit, "deficitPct": round(100*deficit/dis[1], 1),
    "absMin": absmin, "absMax": absmax,
    "rangeLabel": "Šulgi 26 – Ibbi-Suen 4 (c. 2070–2000 BCE)",
}
js_write(f"{OUT}/summary.js", "QB_SUMMARY", summary)

# ---------- chart of accounts ----------
accts = []
for r in cur.execute("SELECT commodity, COUNT(*) c, SUM(qty) q FROM transactions GROUP BY commodity ORDER BY q DESC"):
    c = r["commodity"]
    accts.append({"code": c, "name": COMMODITY_EN.get(c, c), "type": "Livestock",
                  "txns": r["c"], "qty": r["q"]})
js_write(f"{OUT}/accounts.js", "QB_ACCOUNTS", accts)

# ---------- P&L by year ----------
pl = []
for r in cur.execute("""SELECT king, year,
    SUM(CASE WHEN txn_type='receipt' THEN qty ELSE 0 END) ri,
    SUM(CASE WHEN txn_type='receipt' THEN 1 ELSE 0 END) rn,
    SUM(CASE WHEN txn_type='disbursement' THEN qty ELSE 0 END) do,
    SUM(CASE WHEN txn_type='disbursement' THEN 1 ELSE 0 END) dn,
    SUM(CASE WHEN txn_type='transfer' THEN qty ELSE 0 END) tq
    FROM transactions WHERE king IN ('Šulgi','Amar-Suen','Šū-Suen','Ibbi-Suen') AND year>0
    GROUP BY king, year ORDER BY 1,2"""):
    a = abs_year(r["king"], r["year"])
    pl.append({"king": disp_king(r["king"]), "year": r["year"], "abs": a,
               "income": r["ri"] or 0, "incomeN": r["rn"],
               "expense": r["do"] or 0, "expenseN": r["dn"],
               "transfers": r["tq"] or 0, "net": (r["ri"] or 0) - (r["do"] or 0)})
js_write(f"{OUT}/pl.js", "QB_PL", pl)

# ---------- trial balance ----------
tb = []
for r in cur.execute("""SELECT commodity,
    SUM(CASE WHEN txn_type IN ('receipt','transfer') THEN qty ELSE 0 END) dr,
    SUM(CASE WHEN txn_type IN ('disbursement','transfer') THEN qty ELSE 0 END) cr,
    COUNT(*) c FROM transactions GROUP BY commodity ORDER BY dr DESC"""):
    tb.append({"code": r["commodity"], "name": COMMODITY_EN.get(r["commodity"], r["commodity"]),
               "dr": r["dr"] or 0, "cr": r["cr"] or 0, "n": r["c"]})
js_write(f"{OUT}/trial_balance.js", "QB_TB", tb)

# ---------- trial balance by year (for date filters) ----------
tby = []
for r in cur.execute("""SELECT king, year, commodity,
    SUM(CASE WHEN txn_type IN ('receipt','transfer') THEN qty ELSE 0 END) dr,
    SUM(CASE WHEN txn_type IN ('disbursement','transfer') THEN qty ELSE 0 END) cr
    FROM transactions WHERE king IN ('Šulgi','Amar-Suen','Šū-Suen','Ibbi-Suen') AND year>0
    GROUP BY king, year, commodity"""):
    tby.append({"abs": abs_year(r["king"], r["year"]), "code": r["commodity"],
                "dr": r["dr"] or 0, "cr": r["cr"] or 0})
js_write(f"{OUT}/tb_year.js", "QB_TB_YEAR", tby)

# ---------- general ledger summaries ----------
gl = []
for c in [a["code"] for a in accts]:
    r = cur.execute("""SELECT COUNT(*) n, SUM(qty) q FROM transactions WHERE commodity=?""", (c,)).fetchone()
    cp = cur.execute("""SELECT e.canon nm, SUM(t.qty) q FROM transactions t
        LEFT JOIN entities e ON t.to_eid=e.eid WHERE t.commodity=?
        GROUP BY e.canon ORDER BY q DESC LIMIT 5""", (c,)).fetchall()
    cp2 = cur.execute("""SELECT e.canon nm, SUM(t.qty) q FROM transactions t
        LEFT JOIN entities e ON t.from_eid=e.eid WHERE t.commodity=?
        GROUP BY e.canon ORDER BY q DESC LIMIT 5""", (c,)).fetchall()
    yr = cur.execute("""SELECT king, year, SUM(qty) q FROM transactions
        WHERE commodity=? AND king IN ('Šulgi','Amar-Suen','Šū-Suen','Ibbi-Suen') AND year>0
        GROUP BY king, year""", (c,)).fetchall()
    gl.append({"code": c, "name": COMMODITY_EN.get(c, c), "txns": r["n"], "qty": r["q"],
               "topTo": [{"n": x["nm"], "q": x["q"]} for x in cp],
               "topFrom": [{"n": x["nm"], "q": x["q"]} for x in cp2],
               "byYear": [{"abs": abs_year(x["king"], x["year"]), "q": x["q"]} for x in yr]})
js_write(f"{OUT}/gl.js", "QB_GL", gl)

# ---------- AR / AP aging ----------
MAXABS = absmax
def bucket(last):
    age = MAXABS - last
    if age <= 2: return "Current"
    if age <= 10: return "3–10 yrs"
    if age <= 20: return "11–20 yrs"
    return "20+ yrs"
rows = cur.execute("""SELECT b.eid, e.canon nm, e.etype tp,
    SUM(b.inflow - b.outflow) net,
    MAX(CASE WHEN b.king='Šulgi' THEN b.year
             WHEN b.king='Amar-Suen' THEN 48+b.year
             WHEN b.king='Šū-Suen' THEN 57+b.year
             WHEN b.king='Ibbi-Suen' THEN 66+b.year ELSE NULL END) lastabs,
    (SELECT commodity FROM balances b2 WHERE b2.eid=b.eid
     GROUP BY commodity ORDER BY SUM(ABS(b2.inflow-b2.outflow)) DESC LIMIT 1) topc
    FROM balances b JOIN entities e ON b.eid=e.eid
    WHERE b.commodity IN ({}) AND b.king IN ('Šulgi','Amar-Suen','Šū-Suen','Ibbi-Suen')
    GROUP BY b.eid HAVING net != 0""".format(",".join("?"*len(LIVESTOCK))), LIVESTOCK).fetchall()
ar, ap = [], []
for r in rows:
    item = {"name": r["nm"], "type": r["tp"], "net": r["net"],
            "vintage": bucket(r["lastabs"]) if r["lastabs"] else "Unknown",
            "commodity": COMMODITY_EN.get(r["topc"], r["topc"])}
    (ar if r["net"] > 0 else ap).append(item)
ar.sort(key=lambda x: -x["net"]); ap.sort(key=lambda x: x["net"])
js_write(f"{OUT}/aging.js", "QB_AR", ar[:60])
with open(f"{OUT}/aging_ap.js", "w") as f:
    f.write("var QB_AP = "); json.dump(ap[:60], f, ensure_ascii=False, separators=(",", ":")); f.write(";")

# ---------- entities (for filter dropdown) ----------
ents = [{"eid": r["eid"], "name": r["canon"], "type": r["etype"], "n": r["n_attest"]}
        for r in cur.execute("SELECT eid, canon, etype, n_attest FROM entities ORDER BY n_attest DESC LIMIT 300")]
js_write(f"{OUT}/entities.js", "QB_ENTITIES", ents)

# ---------- transaction chunks ----------
CH = 2500
rows = cur.execute("""SELECT t.txn_id, t.pn, t.king, t.year, e1.canon f, e2.canon o,
    t.commodity, t.qty, t.txn_type
    FROM transactions t LEFT JOIN entities e1 ON t.from_eid=e1.eid
    LEFT JOIN entities e2 ON t.to_eid=e2.eid ORDER BY t.txn_id""").fetchall()
n_chunks = math.ceil(len(rows)/CH)
for i in range(n_chunks):
    seg = rows[i*CH:(i+1)*CH]
    arr = [[r["txn_id"], r["pn"], disp_king(r["king"]) if r["king"] else None, r["year"],
            abs_year(r["king"], r["year"]), r["f"], r["o"], r["commodity"], r["qty"], r["txn_type"]]
           for r in seg]
    js_write(f"{CHUNK}/chunk_{i:02d}.js", f"TXN_CHUNK_{i:02d}", arr)
with open(f"{OUT}/chunks.js", "w") as f:
    f.write(f"var QB_CHUNKS = {n_chunks};")

print(f"chunks: {n_chunks}, txns: {len(rows)}, AR: {len(ar)}, AP: {len(ap)}")
print("summary:", json.dumps(summary, ensure_ascii=False)[:200])
con.close()
