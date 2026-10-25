# Drehem Ledger — Standards Alignment

Status: mapped by the author, 2026-10-25. Not reviewed, endorsed, approved, or accredited by the South Carolina Department of Education, the National Council for the Social Studies, or the Common Core authors. "Aligned to" means the activity in the interface fits the published indicator below. It does not mean any authority reviewed this webapp.

Source data: Ur III Puzris-Dagan (Drehem) archive, 15,745 tablets parsed, 59,574 transactions, from CDLI transliterations, first-pass parser output, subject to philological review. See the Auditor's Attestation in the webapp for qualifications, including the 48.4% unreconciled balance, which is structural: sealed intake receipts were kept by the deliverer as proof of delivery.

Interface: https://fibinachi.github.io/Drehem-ledger/webapp/
Dashboard charts pushed to main 2026-10-25.

## South Carolina Social Studies, Grade 6

- **SC 6.1.CO — Compare the development of social systems among the early river valley civilizations.**
  - Standard 6.1: Demonstrate an understanding of the organization and transformation(s) of world civilizations to 550.
  - Fit: Early Mesopotamia is listed under 6.1.CO. A student using the Drehem ledger compares a Mesopotamian social system in its own records: a livestock clearinghouse with officials, counterparties, receipts (su ba-ti), disbursements (zi-ga), and transfers, across the reigns of Sulgi, Amar-Suen, Shu-Suen, and Ibbi-Suen. The Chart of Accounts, General Ledger, and Transaction Register show division of labor, government administration, and trade/transfer, not a textbook summary of them.
  - Note on code history: an older South Carolina Grade 6 code, 6-1.3, asked students to compare river valley civilizations of the Tigris and Euphrates, Nile, Indus, and Huang He, including written language, government, trade systems, architecture, and forms of social order. That code is superseded by the current 6.1 structure. Do not cite 6-1.3 as the current code.

## C3 Framework (National Council for the Social Studies, voluntary inquiry framework)

- **D2.His.1.6-8 — Analyze connections among events and developments in broader historical contexts.**
  - Fit: Annual throughput by reign, and throughput by reign in the Dashboard charts, let a student trace change and continuity from Sulgi 26 through Ibbi-Suen 4, and ask why disbursements outrun receipts in most years.
- **D2.His.10.6-8 — Analyze how a primary source's point of view and limits affect what can be learned.**
  - Fit: The Audit attestation is the point. The ledger is a reconstruction from transliterations, with a stated 48.4% unreconciled balance and a stated reason for it. A student must say what the tablets do not prove, not just what the totals show.
- **D2.Eco.1.6-8 — Explain how economic decisions affect the well-being of individuals and society.**
  - Fit: Receipts, disbursements, and transfers of livestock are allocation decisions under scarcity. Sheep 452,076 head lifetime volume, goat 148,579, ox 97,024, and the rest of the Chart of Accounts show what the state chose to move, to whom, and in what quantities.

## Common Core Literacy in History/Social Studies

- **CCSS.ELA-Literacy.RH.6-8.7 — Integrate visual information (e.g., in charts, graphs, photographs, videos, or maps) with other information in print and digital texts.**
  - Fit: This is the new Dashboard charts panel, added 2026-10-25: annual throughput bars, throughput by reign, largest accounts by lifetime volume, and share of volume. A student must read the chart against the Profit and Loss table and the Audit note, not read the chart alone.
- **CCSS.ELA-Literacy.RH.9-10.7 — Integrate quantitative or technical analysis (e.g., charts, research data) with qualitative analysis in print or digital text.**
  - Fit: The same charts at the 9-10 level, plus the Trial Balance, Balance Sheet, and Cash Flow views. Quantitative totals are checked against the qualitative explanation in the Audit: why a 48.4% gap is not, on this evidence, a claim of fraud or fabrication.
- **CCSS.ELA-Literacy.RH.6-8.9 — Analyze the relationship between a primary and secondary source on the same topic.**
  - Fit: The Transaction Register and General Ledger are built from primary tablet records. The webapp's own Audit, summary, and framing text are secondary. A student can compare what a tablet attests with what the reconstruction claims.

## What this alignment does not claim

- It does not claim the Drehem ledger is a complete classroom lesson, with teacher instructions, a debrief, or an assessment. Meeting History figures carry those. The ledger is a research interface that fits the indicators above when a teacher frames a question around it.
- It does not claim approval by any standards body.
- It does not hide the parser caveat. Any classroom use must carry the Audit qualification with it.
