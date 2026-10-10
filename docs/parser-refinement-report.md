# Provincial Parser Refinement Report (v2)

**Date:** 2026-10-09
**Scope:** Umma and Girsu ATF parsers rebuilt from first pass to v2.
**Drehem database was not touched** (verified: still 59,574 transactions).

## What was wrong in v1

1. **Direction classification was per-line.** Receipt markers (`szu ba-ti`) sit on
   their own line, separate from quantity lines. v1 checked markers only on the
   quantity's line → 98.1% of Umma and 96.6% of Girsu transactions unassigned.
2. **`ba-zi` treated as a receipt marker.** It is a disbursement verb, and it also
   appears inside personal names (`lugal-szuba-zi`) → misclassifications.
3. **Date regex was ASCII-only** (`[A-Za-z\-]+`). Catalog kings are Unicode
   (`Šū-Suen`, `Šulgi`) → most dates silently dropped. v1 Umma kings were a mix
   of `Shulgi`/`Šulgi` from rare ASCII catalog variants.
4. **Totals double-counted.** `szunigin`/`sag-nig2-gur11-ra`/`si-i3-tum`/
   `la2-ia3` summary lines were parsed as regular entries.
5. **All entities typed `person`.** Gods, temples, and titles conflated.
6. **Primed line numbers (`3'.`) skipped** — broken tablets lost content.
7. **Fractions (`1/2(disz)`) unparsed.**
8. **Narrow commodities.** Rations, silver, textiles, fish, reeds, land area ignored.

## What v2 does

- **Tablet-level clause assembly** (`scripts/provincial_parse2.py`): every tablet's
  lines are parsed, then markers, parties, dates, and commodity vectors are
  unioned at the tablet level. Direction is classified once per tablet with
  explicit priority: receipt markers > disbursement markers > ration genre >
  from/to structure > internal (labor rosters, land surveys) > unassigned.
- **Damage-tolerant, standalone-only markers.** `ba-zi`/`zi-ga` must be standalone
  tokens (not inside names); `szu ba-ti-esz2` plurals accepted.
- **Place-name exclusion.** `{ki}`-marked tokens and `egir X-sze3` locatives are
  never treated as recipients.
- **Totals flagged, not deleted.** `is_total=1`, `line_role` in
  (`total`, `grand_total`, `remainder`, `deficit`); `nig2-ka9-ak` tablets marked
  `tablet_kind='balanced_account'`.
- **Dates from two sources** (`scripts/provincial_build2.py`): (a) catalog join
  via ATF publication designation → `dates_referenced` (King.Year.Month.Day);
  (b) in-text year formulae matched against `sources/year_formulae.json`
  (363 normalized variants, `us2-sa` handled). Catalog wins conflicts.
  Kings canonicalized (`Šulgi`, `Amar-Suen`, `Šū-Suen`, `Ibbi-Suen`);
  regnal sequence stored for sorting (`king_seq`, `date_sort`).
- **Typed entities:** person / deity (`{d}…`) / institution (`e2-…`) / title.
- **Schema extended, not broken.** New columns on `tablets` and `transactions`;
  every transaction keeps `(pn, line_no, raw_text)` provenance.
- **Period flagging.** Girsu mixes Ur III with ED IIIb / Lagash II / Old Akkadian
  texts — `period` column separates them so pre-Ur-III texts can't pollute
  national accounts.

## Metric changes

| Metric | Umma v1 | Umma v2 | Girsu v1 | Girsu v2 |
|---|---|---|---|---|
| Tablets represented | 20,484 | 30,411 | 14,099 | 25,094 |
| Transactions | 23,245 | 53,580 | 17,644 | 55,506 |
| Dated transactions | 9,001 (38.7%) | 39,609 (73.9%) | 3,578 (20.3%) | 33,570 (60.5%) |
| Dated tablets | 9,114 (44.5%) | 22,528 (74.1%) | — | 12,737 (50.8%) |
| Unassigned direction | 22,812 (98.1%) | 13,431 (25.1%) | 17,044 (96.6%) | 15,147 (27.3%) |
| Receipts | 231 | 25,629 | 474 | 19,389 |
| Disbursements | 202 | 6,032 | 126 | 15,360 |
| Transfers | 0 | 3,908 | 0 | 3,888 |
| Internal (rosters/surveys) | 0 | 4,580 | 0 | 1,722 |
| Flagged totals | 0 | 4,758 | 0 | 4,457 |
| Entities (typed) | 3,182 | 7,142 | 3,673 | 8,633 |
| King-name variants | 4 (dupes) | 0 (canonical) | 2 | 0 (Ur III) |

Date sources (tablets): Umma — catalog 18,616, in-text 3,912, none 7,883.
Girsu — catalog 12,047, in-text 690, none 12,357.

## Spot-checks passed

- P100002 (AAS 014): labor receipt, `szu ba-ti` on reverse, year formula → Šulgi 44. ✓
- P100003 (AAS 015): receipt, Šulgi 46 (catalog). ✓
- P100013: was false `disbursement` (locative `egir igi-e2-mah-sze3` misread as
  recipient) → now `unassigned`. ✓
- P100026: was false `disbursement` (`nibru{ki}` as recipient) → now `internal`. ✓
- P100016: `sahar zi-ga` correctly `disbursement`. ✓
- Duplicate `&P` entries (tablet + envelope, 5 Umma / 3 Girsu) merged, not dropped.

## Known limitations (not publication-ready yet)

1. **~25% of transactions still directionless.** Mostly proto-cuneiform tablets
   (no parseable Sumerian), fragments, and ambiguous rosters.
2. **Girsu date coverage 60.5%.** ~6,400 Ur III-period tablets have no catalog
   date and no matchable year formula (only 18 have damaged-but-present formulae).
   Pre-Ur-III tablets (ED IIIb, Lagash II, Old Akkadian) are correctly flagged
   but mostly undatable to a year — this is an evidence limit, not a parser bug.
3. **`gu2` labeled generically.** It's a load/bundle unit (gypsum, flour), not a
   textile — stored as commodity `gu2`/unit `count`; do not describe as textiles.
4. **Month numbers are Reichskalender best-effort.** `month_name` is verbatim;
   `month_num` mapping may be off for local Umma/Girsu calendars.
5. **Entity resolution is string-level.** Namesakes not disambiguated (Berkeley
   authority not yet cross-walked to provincial entities).
6. **Direction rules are heuristic.** Marker-priority logic was spot-checked, not
   formally validated against a hand-coded gold sample — that validation is the
   next step before publication.
7. **Commodity quantities are parser outputs.** Unit conversions (esp. area in
   `sar`, rations) need Assyriological review.

## Files

- `scripts/provincial_parse2.py` — v2 tablet-level parser (Umma + Girsu)
- `scripts/provincial_build2.py` — v2 database builder
- `sources/umma-ledger/umma-ledger.db` — refined (v1 in `v1-backup/`)
- `sources/girsu-ledger/girsu-ledger.db` — refined (v1 in `v1-backup/`)
- Superseded: `scripts/umma_parse.py`, `scripts/umma_build.py` (kept for reference)
