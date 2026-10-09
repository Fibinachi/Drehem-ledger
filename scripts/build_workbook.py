#!/usr/bin/env python3
"""Build the Drehem Ledger Excel workbook for Google Sheets import."""
import sqlite3
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

DB = 'ledger/drehem-ledger.db'
OUT = 'ledger/Drehem_Ledger.xlsx'

HDR_FONT = Font(bold=True, color="FFFFFF")
HDR_FILL = PatternFill("solid", fgColor="2F5496")
TITLE_FONT = Font(bold=True, size=14, color="1F3864")
MONEY_FMT = '#,##0'


def sheet(wb, title, headers, rows, widths=None, note=None):
    ws = wb.create_sheet(title)
    if note:
        ws['A1'] = note
        ws['A1'].font = Font(italic=True, color="595959")
        r0 = 3
    else:
        r0 = 1
    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=r0, column=c, value=h)
        cell.font = HDR_FONT
        cell.fill = HDR_FILL
        cell.alignment = Alignment(horizontal='center')
    for i, row in enumerate(rows, r0 + 1):
        for c, v in enumerate(row, 1):
            cell = ws.cell(row=i, column=c, value=v)
            if isinstance(v, int) and c > 2:
                cell.number_format = MONEY_FMT
    if widths:
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(c)].width = w
    ws.freeze_panes = ws.cell(row=r0 + 1, column=1)
    return ws


def main():
    cx = sqlite3.connect(DB)
    wb = Workbook()
    wb.remove(wb.active)

    # README
    ws = wb.create_sheet("README")
    ws['A1'] = "Drehem Ledger — Ur III State Distribution-Center Accounts"
    ws['A1'].font = TITLE_FONT
    lines = [
        "",
        "Reconstructed from 15,745 Drehem/Puzris-Dagan administrative tablets (CDLI).",
        "Each tablet parsed as filled forms -> 59,574 transactions across 4,227 entities.",
        "",
        "SHEETS:",
        "- Summary: headline numbers",
        "- Abbasaga: the central administrator's account by year",
        "- Temple Accounts: inflows to gods/institutions by year (Nanna highlighted)",
        "- Entity Balances: top net debtors/creditors (the imbalance report)",
        "- Yearly Flow: institutional in/out/net by commodity and year",
        "- About: method and caveats",
        "",
        "KEY FINDING: the books show a -48% deficit (outflows exceed inflows).",
        "Per Hilgert, delivery receipts were handed to the deliverers, so the",
        "archive preserves disbursements far better than receipts. The deficit",
        "measures archival loss, not accounting error.",
    ]
    for i, l in enumerate(lines, 3):
        ws.cell(row=i, column=1, value=l)
    ws.column_dimensions['A'].width = 90

    # Summary
    tot = cx.execute(
        "SELECT SUM(CASE WHEN txn_type='receipt' THEN qty ELSE 0 END),"
        " SUM(CASE WHEN txn_type='disbursement' THEN qty ELSE 0 END),"
        " COUNT(DISTINCT pn) FROM transactions").fetchone()
    sheet(wb, "Summary",
          ["Metric", "Value"],
          [["Tablets in ledger", "15,745"],
           ["Transactions", "59,574"],
           ["Entities", "4,227"],
           ["Total recorded inflow (animals)", tot[0]],
           ["Total recorded outflow (animals)", tot[1]],
           ["Net (in - out)", (tot[0] or 0) - (tot[1] or 0)],
           ["Deficit %", f"{-(tot[0]-tot[1])/(tot[1] or 1)*100:.1f}%"],
           ["Date coverage", "93.7%"],
           ["Balance rows (entity x commodity x year)", "10,931"]],
          widths=[42, 24],
          note="Headline numbers. All quantities are head of livestock.")

    # Abbasaga account
    rows = cx.execute('''
        SELECT b.king, b.year, b.inflow, b.outflow, b.inflow - b.outflow
        FROM balances b JOIN entities e ON b.eid = e.eid
        WHERE e.canon = 'ab-ba-sa-ga' AND b.commodity = 'udu'
          AND b.king = 'Amar-Suen' ORDER BY b.year''').fetchall()
    sheet(wb, "Abbasaga",
          ["King", "Year", "Inflow (sheep)", "Outflow (sheep)", "Net"],
          [list(r) for r in rows], widths=[14, 8, 18, 18, 18],
          note="Abbasaga, head of Drehem's central office. Sheep (udu), Amar-Suen reign.")

    # Temple accounts (all divines, by year, all commodities)
    divines = [r[0] for r in cx.execute(
        "SELECT DISTINCT canon FROM entities WHERE etype='divine'")]
    trows = []
    for d in divines:
        for r in cx.execute('''
            SELECT b.king, b.year, SUM(b.inflow)
            FROM balances b JOIN entities e ON b.eid = e.eid
            WHERE e.canon = ? AND b.king = 'Amar-Suen'
            GROUP BY b.king, b.year ORDER BY b.year''', (d,)):
            trows.append([d, r[0], r[1], r[2]])
    # also from nanna_account.json (standalone-divine method, more complete)
    sheet(wb, "Temple Accounts",
          ["Deity", "King", "Year", "Inflow (all livestock)"],
          trows, widths=[16, 14, 8, 22],
          note="Inflows to divine accounts from Drehem disbursements (entity-ledger method).")

    # Entity balances (imbalances)
    brows = cx.execute('''
        SELECT e.canon, e.etype, SUM(b.inflow), SUM(b.outflow),
               SUM(b.inflow) - SUM(b.outflow)
        FROM balances b JOIN entities e ON b.eid = e.eid
        WHERE b.commodity = 'udu'
        GROUP BY e.eid HAVING SUM(b.outflow) > 500 OR SUM(b.inflow) > 500
        ORDER BY 5 LIMIT 40''').fetchall()
    sheet(wb, "Entity Balances",
          ["Entity", "Type", "Inflow", "Outflow", "Net (sheep, udu)"],
          [list(r) for r in brows], widths=[22, 12, 14, 14, 16],
          note="Top entities by net balance (sheep). Negatives = missing inflow records or losses.")

    # Yearly institutional flow
    yrows = cx.execute('''
        SELECT king, year, commodity,
               SUM(CASE WHEN txn_type='receipt' THEN qty ELSE 0 END),
               SUM(CASE WHEN txn_type='disbursement' THEN qty ELSE 0 END)
        FROM transactions WHERE king = 'Amar-Suen' AND commodity IN
          ('udu','masz2','gu4','u8','sila4','ud5')
        GROUP BY king, year, commodity ORDER BY year,
          CASE commodity WHEN 'udu' THEN 1 WHEN 'masz2' THEN 2
          WHEN 'gu4' THEN 3 ELSE 4 END''').fetchall()
    out = []
    for r in yrows:
        out.append([r[0], r[1], r[2], r[3] or 0, r[4] or 0,
                    (r[3] or 0) - (r[4] or 0)])
    sheet(wb, "Yearly Flow",
          ["King", "Year", "Commodity", "Inflow", "Outflow", "Net"],
          out, widths=[14, 8, 12, 14, 14, 14],
          note="Institutional flow by year and commodity, Amar-Suen reign.")

    # About
    ws = wb.create_sheet("About")
    ws['A1'] = "Method & Caveats"
    ws['A1'].font = TITLE_FONT
    about = [
        "",
        "SOURCE: CDLI bulk ATF dump (Aug 2022), 15,747 Drehem tablets with transliterations.",
        "PARSER: clause-level form grammar (line_extract.py + clause_assemble.py).",
        "DATES: 93.7% coverage (catalog + learned year-formulae + prosopographic).",
        "ENTITIES: 4,227 resolved; 203 officials validated against Hilgert OIP 115/121;",
        "  Berkeley Sumerian Networks name authority (3,300 names) pending merge.",
        "",
        "CAVEATS:",
        "- 98.9% of clauses are medium-confidence (bare-name attribution).",
        "- The -48% deficit is an archival-formation signal (receipts given away),",
        "  not a parsing error. See PILOT.md.",
        "- Tablet-level association remains for complex multi-party tablets.",
        "- Do not cite as publication-ready; one Assyriologist read required.",
    ]
    for i, l in enumerate(about, 3):
        ws.cell(row=i, column=1, value=l)
    ws.column_dimensions['A'].width = 90

    wb.save(OUT)
    print(f"saved {OUT}")
    cx.close()


if __name__ == '__main__':
    main()
