# Drehem Ledger

**The oldest reconstructed ledger in the world** — the 4,000-year-old books of the Ur III state's livestock distribution center, rebuilt as a queryable accounting database.

Follow the analysis: [GRID Keeper](https://gridkeeper.substack.com/), a 14QBD273 project.

Drehem (ancient Puzriš-Dagan) was the central clearinghouse for livestock in the Ur III empire (~2100–2000 BCE). Over 15,000 administrative tablets survive, scattered across forty museums after the site was looted from 1909 onward. This project parses them as filled forms and reconstructs the archive as a unified ledger: who received what, who disbursed what, and whether the books balance.

## The headline finding

They don't balance — and that's the point. Recorded outflows exceed inflows by **~48%** across all commodities. Per published scholarship (Hilgert), delivery receipts were handed to the deliverers, so the archive preserves disbursements far better than receipts. The deficit is a **measurement of archival formation**, not an accounting error: a lower bound on how much of the inflow record is lost.

## Key numbers

- **15,745** tablets parsed (93.7% date coverage)
- **59,574** transactions (38,315 disbursements · 19,639 receipts · 1,620 transfers)
- **4,227** entities
- **296,876** animals received vs **574,891** disbursed
- **37,711** animals to Nanna's temple account (deity ranking reproduces the Ur III pantheon unprompted)

## Largest net positions (sheep)

| Entity | Inflow | Outflow | Net |
|---|---|---|---|
| ab-ba-sa-ga (Abbasaga) | 17,217 | 75,588 | -58,371 |
| in-ta-e-a (Intaea) | 0 | 15,509 | -15,509 |
| na-sa | 6,138 | 15,482 | -9,344 |
| na-ra-am-i-li | 0 | 7,846 | -7,846 |
| ur-ku-nun-na | 5,059 | 12,118 | -7,059 |

Negative = missing inflow records (the archival-formation signal), not debt.

## Yearly institutional flow (all livestock, Amar-Suen reign)

| Year | Inflow | Outflow | Net |
|---|---|---|---|
| 1 | 4,228 | 33,591 | -29,363 |
| 2 | 15,687 | 46,596 | -30,909 |
| 3 | 9,519 | 25,071 | -15,552 |
| 4 | 15,196 | 29,021 | -13,825 |
| 5 | 25,418 | 54,351 | -28,933 |
| 6 | 13,856 | 15,850 | -1,994 |
| 7 | 12,236 | 29,188 | -16,952 |
| 8 | 16,953 | 28,527 | -11,574 |
| 9 | 3,417 | 14,635 | -11,218 |

## Files

| File | Contents |
|---|---|
| `Drehem_Ledger.xlsx` | 7-sheet workbook (download to view) |
| `ledger.db` | SQLite database — 59,574 transactions, 4,227 entities |
| `webapp/` | QuickBooks-style browser app (open `index.html`, no server needed) |
| `docs/` | Forensic audit report, literature reviews, parser methodology |
| `scripts/` | Parser, ledger builder, analysis scripts |

## Method

Forensic accounting applied to cuneiform: clause-level form grammar → entity resolution (validated against Hilgert OIP 115/121) → conservation-constrained ledger. Imbalances are treated as evidence, not noise.

## Status

Research in progress. Not yet peer-reviewed.

## Sources

Transliterations from the Cuneiform Digital Library Initiative (CDLI), August 2022 bulk dump.

Cross-archive dates, provenience, and prosopographic data from Manuel Molina's **Database of Neo-Sumerian Texts (BDTNS)** — 105,187 documents, 29 years in the making. Our gratitude for the diligence in keeping it accurate; this work would not be possible without it. Data snapshot via Niek Veldhuis's *Compass* project. https://bdtns.cesga.es/

## License

CC-BY 4.0. If you figure out a way to commercialize a database of 4,000-year-old sheep transactions, God bless you. You deserve the money.
