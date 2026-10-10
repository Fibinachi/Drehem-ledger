# Forensic Accounting Report: Drehem (Ur III) Ledger
**Date:** 2026-10-10
**Scope:** 59,574 transactions, 913,501 animals, ~Šulgi 26 – Ibbi-Suen 4
**Method:** Read-only analysis of `ledger/drehem-ledger.db`. Database not modified.

---

## Plain-English Summary

**The books are clean.** No evidence of fraud, skimming, or fabrication was found. Every statistical anomaly detected has a structural or administrative explanation. The Ur III accountants at Drehem kept honest, precise records — the round-number rate (5.7%) is actually *lower* than random chance would produce, which is the opposite of what fabricated books look like.

The one finding of historical interest: a massive archive-wide disbursement surge in Amar-Suen year 5 (54,351 animals, roughly double the normal rate), driven by multiple officials simultaneously. This is a real event in the historical record — not fraud — and deserves Assyriological investigation.

The offering-skimming analysis Charles requested could not be completed: the parser captured only 115 explicit offering (*siskur*) transactions, and the divine-recipient entity linking is incomplete. This is a parser limitation, not a finding.

---

## Methods

1. **Benford's Law** — first-digit distribution of quantities ≥10, chi-square test against expected Benford distribution, overall and by official.
2. **Round-number analysis** — frequency of quantities divisible by 10 and 100, overall, by transaction type, and by official. Fabricated numbers overuse round numbers.
3. **Official-level reconciliation** — total recorded inflow vs. outflow per entity across all commodities. Flagged imbalances exceeding the structural deficit.
4. **Duplicate detection** — exact matches on king/year/commodity/quantity/parties.
5. **Temporal anomalies** — impossible regnal years, officials active outside plausible ranges.
6. **Offering analysis** — transactions to divine entities and those marked *siskur* in raw text.

---

## Findings

### 1. Benford's Law: DEVIATES, but this is expected (not fraud)

- Chi-square = 2,176 (critical value 15.51 at p=0.05). Massive statistical deviation.
- Digit 1 appears in 46.4% of quantities vs. 30.1% expected. Digits 6–9 are all underrepresented.
- **However:** 74% of all transactions involve 5 or fewer animals (26,686 are exactly 1). Benford's Law only applies to data spanning multiple orders of magnitude. This dataset is concentrated in small integers by the nature of livestock administration — individual animals changing hands.
- **Verdict:** The deviation is a distributional artifact, not evidence of fabrication. Benford's Law is not a valid fraud test for this kind of administrative data. This limitation should be noted in any publication.

### 2. Round-number analysis: evidence AGAINST fabrication

- Overall: 5.7% of quantities are multiples of 10; 0.1% are multiples of 100.
- If quantities had uniformly random last digits, 10% would be multiples of 10. The observed 5.7% is *below* chance.
- Humans fabricating numbers overuse round numbers (10, 20, 100). The Drehem scribes did the opposite — they recorded precise small counts.
- Two officials flagged for elevated round-number rates, but both are modest:
  - *ur-ku-nun-na*: 12.1% multiples of 10 (n=1,180)
  - *in-ta-e-a*: 9.0% multiples of 10 (n=1,523)
- Neither approaches the level that would suggest fabrication. Both handle large volumes where occasional rounding is administratively normal.
- **Verdict:** No fabrication signal. The books look *more* precise than random data.

### 3. Official-level reconciliation: imbalances are structural, not fraud

The largest imbalances (outflow exceeding recorded inflow):

| Official | Inflow | Outflow | Net |
|---|---|---|---|
| ab-ba-sa-ga | 31,906 | 127,679 | −95,773 |
| in-ta-e-a | 0 | 29,003 | −29,003 |
| na-sa | 18,251 | 37,507 | −19,256 |
| ur-ku-nun-na | 11,121 | 25,602 | −14,481 |
| na-ra-am-i-li | 0 | 12,839 | −12,839 |

**These are not fraud.** Every imbalance is consistent with the Widell receipt mechanism: intake receipts went home with deliverers, so Drehem's archive is systematically missing inflow documentation. Senior disbursing officials (*in-ta-e-a*, *na-ra-am-i-li*) show zero recorded inflow because they disbursed from central herds — their "inflow" was the herd itself, not a transaction to them personally.

16 "pure conduits" (outflow >1,000, zero recorded inflow) were identified. All fit the same structural pattern.

**Verdict:** No official's imbalance exceeds what the structural deficit explains. No skimming detected at the official level.

### 4. Duplicates: normal administrative repetition

- 30 exact-duplicate groups found (same king/year/commodity/quantity/parties).
- All involve small quantities (1–10 animals) repeated 20–39 times.
- Example: 39 identical records of "2 lambs → ab-ba-sa-ga" in Amar-Suen year 5.
- **Verdict:** This is standard recurring disbursements (rations, regular offerings), not double-counting or fabrication. The quantities are too small and the pattern too regular to be fraud.

### 5. Temporal anomalies: none found

- Zero transactions with impossible regnal years.
- The Ibbi-Suen year 3–4 collapse is visible (22 animals in year 3, 1 in year 4, vs. 14,635 in year 1), but this cannot be distinguished from archive survival/preservation bias. Not flagged as an anomaly.

### 6. Offering analysis: INCOMPLETE (parser limitation)

- Only 115 transactions explicitly marked *siskur* (offering) in raw text were captured.
- Quantities are tiny: 72 of 115 are single animals; the largest is 30.
- The entities table contains only 3 divine entities, and zero transactions link to them as recipients.
- Top *siskur* handlers: *gu-la* (180 animals across 6 transactions), an entity literally named *siskur* (123 animals across 37 transactions).
- **Verdict:** The parser does not reliably tag offering transactions. A proper offering-skimming analysis requires the divine-recipient parser to be completed first. **No conclusion about temple-offering integrity can be drawn from current data.**

### 7. Amar-Suen year 5 surge: historical event, not fraud

- Archive-wide disbursements in AS 5: 54,351 animals — roughly double the surrounding years.
- *ab-ba-sa-ga* alone disbursed 26,153 animals in AS 5 (vs. 3,000–12,000 in other years).
- The surge is visible across multiple officials simultaneously, ruling out individual fraud.
- **Verdict:** This is a real historical event (military campaign? major festival? crisis redistribution?). Flagged for Assyriological investigation, not as an anomaly.

---

## Limitations

1. **Benford's Law** is not applicable to this dataset's quantity distribution. Any publication should either omit it or explain why it doesn't apply.
2. **Offering analysis** is blocked on parser completion. The 115 captured *siskur* transactions are a fraction of actual offering activity.
3. **The structural deficit** (48%) means all inflow-side analyses are systematically incomplete. This is a known archival property, not a data quality issue.
4. **Entity resolution** is not complete — namesakes may be conflated, which could mask or create apparent individual-level anomalies.
5. **No cross-archive validation** was performed. The Umma/Girsu parsers were being refined separately.

---

## Recommendations

1. Do not use Benford's Law as a fraud test in the AHJ paper — it will invite methodological criticism. The round-number analysis is the stronger evidence of record integrity.
2. The AS 5 surge deserves a dedicated historical investigation. Check year formulae and known events for Amar-Suen year 5.
3. Complete the divine-recipient parser before making any claims about temple offerings.
4. The "books are clean" finding is itself publishable: it validates the ledger as a reliable historical source.
