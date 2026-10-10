# Ur III Ledger — QuickBooks-style Web App

A static, QuickBooks-style accounting interface for the reconstructed books of
Puzriš-Dagan (Drehem), the livestock clearinghouse of the Ur III state
(c. 2070–2000 BCE). The joke is the product: it's just QuickBooks, but Bronze Age.

## Run it

Open `index.html` in any browser. No build step, no server, no dependencies.
Works from `file://` (data loads via `<script>` tags, not `fetch`).

GitHub Pages-ready: push this directory and serve.

## What's inside

| View | Source |
|---|---|
| Dashboard | `data/summary.js`, `data/pl.js` |
| Chart of Accounts | `data/accounts.js` |
| General Ledger + drill-down | `data/gl.js` |
| Profit & Loss | `data/pl.js` (filterable by reign) |
| Balance Sheet | `data/pl.js` (cumulative) |
| Trial Balance | `data/trial_balance.js`, `data/tb_year.js` |
| Cash Flow Statement | `data/pl.js` |
| A/R & A/P Aging | `data/aging.js`, `data/aging_ap.js` |
| Transaction Register | `data/txn/chunk_*.js` (59,574 txns, lazy-loaded) |
| Auditor's Attestation | static + `data/summary.js` |

Reports support filtering by date range (reign presets), account (commodity),
counterparty (entity search), and transaction type.

## Data

Exported from `ledger/drehem-ledger.db` via `build_data.py`:

- 15,745 tablets · 59,574 transactions · 4,227 entities
- Receipts 296,876 head · Disbursements 574,891 head
- Unreconciled balance 278,015 head (48.4%) — structural, see Audit view

Re-run `python3 build_data.py` after any database rebuild.

## Status

Drehem data is validated. Umma/Girsu archives are marked "in audit" in the UI
until their parsers are refined.
