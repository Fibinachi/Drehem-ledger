# Literature Review: Historic Accounting Scholarship

**Date:** 2026-10-09
**Prepared for:** The Drehem/Ur III ledger reconstruction project
**Question:** What has the accounting-history and historical-accounting literature established about (1) plantation ledgers as accounting systems, (2) reconstructions of pre-modern accounting systems from fragmentary records, and (3) forensic or computational methods applied to historical archives — and has anyone done a complete computational ledger reconstruction of an ancient archive before?

**Short answer:** No. Across accounting history, Assyriology, economic history, and digital humanities, no verified prior work ingests tens of thousands of records from an ancient archive, computationally resolves entities, enforces accounting-conservation constraints, and produces auditable books. The closest precedents are manual/philological (de Roover's Medici Bank; Hilgert's Puzriš-Dagan offices), computational-but-not-accounting (Old Assyrian entity resolution; Bronze Age trade modeling), or infrastructure without reconstruction (CDLI, BDTNS, ORACC, Trismegistos).

---

## 1. Overview

Historic accounting scholarship splits into three traditions that rarely talk to each other:

1. **Accounting historians** (centered on the *Accounting Historians Journal*, *Accounting History*, *Accounting, Business & Financial History*) study bookkeeping technique, the double-entry origins debate, and accounting as a social/institutional practice. Their pre-modern work is overwhelmingly *manual and philological*: close readings of surviving books, treatises, and text editions.
2. **Economic and business historians** (e.g., the "slavery and capitalism" literature) use account books as *evidence for macro theses* — sampling ledgers for practices rather than reconstructing complete systems.
3. **Assyriologists and ancient historians** reconstruct ancient administrations from text editions, increasingly with database assistance — but the analytical layer (balances, entity resolution, conservation checks) is absent.

A fourth, emergent tradition — **computational humanities** — has applied entity resolution, network analysis, and structural economic modeling to ancient corpora, but never to rebuild an accounting ledger. Forensic-accounting techniques (Benford's law, anomaly detection, balance-check forensics) have essentially no verified empirical application to pre-1500 records at all.

---

## 2. Plantation Accounting Literature

This is the literature that inspired the Drehem project: Richard Barnes's plantation-ledger conversation, then Caitlin Rosenthal's *Accounting for Slavery*. It is also the most contested ground in recent accounting history, and its methodological lessons transfer directly.

### 2.1 The "slavery and capitalism" historians

**Edward Baptist, *The Half Has Never Been Told: Slavery and the Making of American Capitalism* (Basic Books, 2014).** Baptist argues US chattel slavery was the dynamic engine of American capitalism: cotton-picking productivity roughly quadrupled 1801–1862 via the "pushing system" of calibrated torture ratcheting up daily quotas, and cotton-related activity accounted for ~half of US economic activity by the 1830s. Methods: narrative history from WPA ex-slave testimonies, production statistics, and secondary estimates — *not* grounded in original plantation ledger research. **Criticism:** Alan Olmstead and Paul Rhode ("Cotton, slavery, and the new history of capitalism," *Explorations in Economic History* 67 (2018): 1–17) dismantled both central claims: productivity growth was driven overwhelmingly by improved cotton seed varieties (biological innovation), not escalating torture, and cotton was ~5% of GDP, not ~50% (Baptist double- and triple-counted). Related critiques: Stanley Engerman (*Journal of Economic Literature* 55(2) (2017)); Eric Hilt (*Journal of Economic History* 77(2) (2017)).

**Caitlin Rosenthal, *Accounting for Slavery: Masters and Management* (Harvard University Press, 2018).** Drawing on hundreds of plantation account books from the British West Indies and the American South (c. 1780–1880), Rosenthal argues elite slave-planters pioneered quantitative management accounting *ahead of* Northern manufacturers: double-entry-style recordkeeping, standardized labor units ("hands," "fractional hands"), per-slave productivity tracking, depreciation applied to human capital, preprinted plantation forms, incentive systems. Thesis: systematic management accounting "thrived on antebellum plantations — not despite the chattel principle, but because of it," since absolute control over a non-mobile workforce eased data collection. Developed from her 2012 Harvard dissertation and "From Memory to Mastery: Accounting for Control in America, 1750–1880," *Enterprise & Society* 14(4) (2013). **Criticism:** Robert Gudmestad's review (*The History Teacher*, 2019) flags the unresolved internal tension — Rosenthal concedes her cases are "histories of exceptional people" (p. 8) while claiming "sophisticated accounting practices were relatively widespread" (p. 100). The representativeness problem is the hinge of the whole debate.

**Context:** Sven Beckert, *Empire of Cotton* (Knopf, 2014); Beckert & Rockman, eds., *Slavery's Capitalism* (University of Pennsylvania Press, 2016) — includes Rosenthal's chapter tracing plantation accounting into management practice; Walter Johnson, *River of Dark Dreams* (Harvard University Press, 2013).

### 2.2 The accounting historians' response

The sustained accounting-history engagement comes from **Richard K. Fleischman, Thomas N. Tyson, and David Oldroyd** (collaborative program from ~2004, in *Accounting History*, *Accounting, Auditing & Accountability Journal*, *Economic History Review* — notably, no dedicated *Accounting Historians Journal* special issue on slavery was found):

- Tyson, Fleischman & Oldroyd, "Theoretical perspectives on accounting for labor on slave plantations of the USA and British West Indies," *AAAJ* 17(5) (2004): 758–778.
- Fleischman, Oldroyd & Tyson, "Monetising human life: Slave valuations on US and British West Indian plantations," *Accounting History* 9(2) (2004): 35–62. Annual valuation parades assigning dollar/pound values to individual slaves; BWI valuations linked more to skill sets, the US showed a male premium; accounting helped *legitimize* slavery under abolitionist pressure.
- Fleischman & Tyson, "Accounting in service to racism: Monetizing slave property in the antebellum south," *Critical Perspectives on Accounting* 15(3) (2004): 376–399.
- Fleischman, Oldroyd & Tyson, "Plantation accounting and management practices in the US and the British West Indies at the end of their slavery eras," *Economic History Review* 64(3) (2011): 765–797. **The central empirical engagement.** Findings cutting against Rosenthal/Baptist: plantation bookkeeping was **highly non-uniform across estates**; much recordkeeping was stewards'-charge accounting for absentee owners rather than productivity optimization; little evidence of true double-entry as a management-control system in mainstream practice. Valuation lists served valuation and collateralization — a *financial* accounting function, not cost-management innovation.
- Tyson & Oldroyd, "Accounting for slavery during the Enlightenment: Contradictions and interpretations," *Accounting History* 24(2) (2018): 212–235. The most direct rebuttal of the productivity thesis from within accounting history: plantation accounting "was not geared toward improving productivity"; productivity was governed by established social norms.
- Fleischman, "Confronting moral issues from accounting's dark side," *Accounting History* 9(1) (2004): 7–23.

**Grounds of pushback, in short:** (1) double-entry was exceptional, not standard — most plantation books are charge-and-discharge/agency records; (2) productivity gains cannot be attributed to accounting; (3) sampling bias — the sophisticated ledgers are elite outliers; (4) the books served valuation/collateralization and moral legitimation more than cost management.

### 2.3 Other plantation-accounting studies

- **Joseph R. Razek, "Accounting on the old plantation: A study of the financial records of an antebellum Louisiana sugar planter," *AHJ* 12(1) (1985): 17–36.** The earliest AHJ entry — a single-planter, full-book case study; close in spirit to reconstructing a complete accounting system from one estate's books.
- **Dale L. Flesher & Tonya K. Flesher, "Human resource accounting in Mississippi before 1865," *Accounting and Business Research* 10, suppl. 1 (1980): 124–129.** Early claim of proto-human-resource accounting in valuing slaves.
- **Lúcia Lima Rodrigues, Russell J. Craig, Paulo Schmidt & José Luis Santos, "Documenting, monetising and taxing Brazilian slaves in the eighteenth and nineteenth centuries," *Accounting History Review* 25(1) (2015): 43–67.** Key Brazilian entry: because Brazilian managers were usually also owners, there was *less* need to value slaves for agency purposes than in absentee Caribbean settings — a natural experiment against Rosenthal's absentee-ownership mechanism.
- **Martin Giraudeau, "The farm as an accounting laboratory," LSE Research Online (2017).** Agricultural enterprises as early sites of accounting experimentation.
- **Daniel Tinkelman, "'Money does not stink' — Accounting and slavery," *Accounting History* 29(2) (2024).** Recent synthesis; more restatement than innovation.

### 2.4 Methodological lessons for the Drehem project

1. **Reconstruct completely, don't sample for practices.** Rosenthal reads ledgers "as maps" — sampling books for practices — which is exactly what opened her to the representativeness critique. Razek (1985) and the valuation-parade studies show reconstructing a *complete* accounting system is feasible and is the stronger evidential move. The Drehem ledger does this by construction.
2. **The representativeness caution cuts both ways.** The Fleischman school's warning applies equally to Sumerian reconstruction: the Drehem livestock clearinghouse can document a system's *logic* without proving it was universal across the Ur III state. Claims should be scoped to what the archive is.
3. **Distinguish financial from managerial functions.** Fleischman et al.'s finding that plantation books served valuation/collateralization more than cost management is a useful analytical lens for Drehem: the tablets' primary function may be accountability/charge-and-discharge rather than decision-oriented management accounting — and that is a finding, not a failure.

---

## 3. Pre-modern / Historical Accounting Reconstruction

### 3.1 The double-entry origins debate (context)

- **Luca Pacioli**, *Summa de arithmetica* (Venice, 1494): the first *printed* exposition of double-entry (*Particularis de computis et scripturis*); codifier, not inventor.
- **Benedetto Cotrugli**, *Della mercatura e del mercante perfetto* (written 1458, printed 1573): earliest known *manuscript* description.
- **Raymond de Roover** (1937, "Aux origines d'une technique intellectuelle," *Annales d'histoire économique et sociale* 9): double entry evolved among Italian merchant-bankers by c. 1300.
- **Basil Yamey** (1949, "Scientific bookkeeping and the rise of capitalism," *Economic History Review*; 1964, *Journal of Accounting Research*): debunked Sombart's claim that double entry *caused* capitalism — early businessmen rarely computed profits; regular annual closings only became common in the late 18th century.
- **Alan Sangster** (2016, "The Genesis of Double Entry Bookkeeping," *The Accounting Review* 91(1)): double entry emerged in *banks* (debtors/creditors were existential), essentially complete before the last decade of the 13th century; pushes earliest evidence to 1211 Florentine fragments. (His 2022 working paper on the 1211 fragments: publication status unconfirmed.)
- **Converged position:** double entry in northern/central Italy, 13th century, banking contexts; Pacioli as transmitter; rejection of Sombart's causal claim; ongoing split over whether medieval double entry was "complete" by modern standards (Sangster vs. Yamey/Hoskin & Macve).

### 3.2 Medieval and early-modern ledger reconstructions

**Raymond de Roover, *The Rise and Decline of the Medici Bank, 1397–1494* (Harvard University Press, 1963).** The single closest precedent in the literature for reconstructing a pre-modern enterprise's accounts from surviving fragments: exhaustive study built on the *libri segreti* (confidential ledgers) discovered in 1950, rebuilding the bank's organization, operating methods, loan policy, and decline. Entirely manual/philological — but the model of "reconstruct the system from fragments." Companion studies: Collard de Marke (1366–1369), Guillaume Ruyelle (1369), *Money, Banking and Credit in Medieval Bruges* (1948).

**Fugger accounts:** Kazuo Inoue (1982), "Threefold bookkeeping by Matthaus Schwarz," *AHJ* 9(1) — Schwarz's 1518 manuscript; Baker & Quéré (2019), "Governance and accounting practices in the Fugger family firm," *Accounting History* — treatise-centered rather than ledger-reconstruction-centered.

**English manorial accounts (charge and discharge):** Robert Bryer (1994), "Accounting for the Social Relations of Feudalism," *Accounting and Business Research* 24(95) — charge-and-discharge as adequate to feudalism's needs. Alisdair Dobie (2011), "A Review of the Granators' Accounts of Durham Cathedral Priory 1294–1433," *Accounting History Review* 21 — detailed reconstruction of monastic process accounting; also Dobie (2024), "Medieval Monastic Accounting Records: Potentials and Pitfalls for Statistical Analysis," in Casson & Lee, eds., *Medieval Statistics* (Palgrave) — a survey of what medieval accounts *could* yield statistically and the pitfalls.

**Gary Spraakman, *Management Accounting at the Hudson's Bay Company: From Quill Pen to Digitization* (Emerald, 2015).** 335-year longitudinal study (1670–2005) exploiting a near-complete archive; five discrete management-accounting regimes. The longest continuous archival accounting reconstruction in the literature — but qualitative-historical, not computational.

**Roman accounting:** David Oldroyd (1995), "Role of accounting in public expenditure and monetary policy in the first century AD Roman Empire," *AHJ* 22(2); Lauren Lagroue (2014), *Accounting and Auditing in Roman Society* (UNC Chapel Hill PhD dissertation) — synthesizes the Journey of Theophanes, the Heroninos archive, and the Vindolanda tablets.

### 3.3 Ancient accounting scholarship

**Denise Schmandt-Besserat** — *Before Writing* (2 vols., UT Press, 1992); *How Writing Came About* (1996). ~8,000 clay tokens from 116 Near Eastern sites: cuneiform descends from an 8000 BC accounting-token system; sealed *bullae* impressed on the outside created the 2D representation that became writing.

**Hans Nissen, Peter Damerow & Robert Englund** — *Archaic Bookkeeping* (University of Chicago Press, 1993). Philology plus **computer analysis** of numerical notation on ~5,000 proto-cuneiform tablets from Uruk/Jemdet Nasr: the earliest tablets record economic administration (grain/livestock/labor accounts); metrological systems deciphered; checking of actual against theoretical amounts "perhaps the most important accounting operation introduced during the third millennium BC." Englund's MSVO work includes "Proto-cuneiform account-books and journals" (CDLI-hosted). Note: computer analysis was used to decode *notation*, not to rebuild a ledger.

**Richard Mattessich** — the accounting theorist of ancient accounting: "Prehistoric accounting and the problem of representation" (*AHJ* 14(2) (1987)); "Archaeology of accounting and Schmandt-Besserat's contribution" (*ABFH* 4(1) (1994)); "Recent insights into Mesopotamian accounting of the 3rd millennium B.C." (*AHJ* 25(1) (1998)); *The Beginnings of Accounting and Accounting Thought* (Taylor & Francis, 2000). Formal/matrix-theoretic modeling of ancient record systems; the sealed token envelope as double recording (tokens inside = assets; impressions outside = equity). Also treats Kautilya's *Arthaśāstra* (c. 300 BC) as the first treatise with accounting content.

**Ur III / Drehem as an accounting system (Assyriological side)** — text-edition plus institutional reconstruction, no computational ledgers:
- Piotr Steinkeller (1987), "The administrative and economic organization of the Ur III state," SAOC 46; (2003), "Archival Practices at Babylonia in the Third Millennium," in Brosius, ed., *Ancient Archives and Archival Traditions* (OUP) — uses the ~15,000-tablet Umma archive to identify bureaus; (2004), "The Function of Written Documentation," in Hudson & Wunsch, eds., *Creating Economic Order* (CDL Press).
- Walther Sallaberger (1999), "Ur III-Zeit," OBO 160/3 — the master synthesis of ~40,000 published Ur III documents; (2013), "Killing and Skinning Animals in the Ur III Period," *Altorientalische Forschungen* 40 — reconstructs a Drehem sub-office from keyword + prosopographical analysis.
- Christina Tsouparopoulou (2008), *The Material Face of Bureaucracy* (Cambridge PhD) — Drehem sealing/archiving practice; (2015), *The Ur III Seals Impressed on Documents from Puzriš-Dagān (Drehem)*, HSAO 16.
- Marcel Sigrist (1992), *Drehem* (CDL Press) — text edition catalog; Markus Hilgert (1998), *Cuneiform Texts from the Ur III Period in the Oriental Institute, Vol. 1*, OIP 115 (499 tablets).
- Steven Garfinkle (2004), "Shepherds, Merchants, and Credit," *JESHO* 47(1) — Ur III lending; Jacob Dahl (2020), *Ur III Texts in the Schøyen Collection*, CUSAS 39.
- Garfinkle & Molina, eds. (2013), *From the 21st Century B.C. to the 21st Century A.D.* (Eisenbrauns) — includes a chapter "Symbols and Bureaucratic Performances in the Ur III Administrative Sphere: An Interpretation Through Data Mining" (author unverified), signaling the computational turn in Assyriology.
- **Balanced accounts (nig₂-ka₉-ak):** Ur III yearly accounts structured as debits, credits, and a balance carried forward as surplus (*diri*) or deficit (*la₂-ia₃*). The Assyriological literature (e.g., Jacob Dahl's work, per an *ORIENT* 55 (2020) article whose author/title could not be verified) already questions whether these accounts were ever literally "balanced" — which is exactly the kind of claim a computational reconstruction would test rather than assume.

**Ancient Egyptian accounting:** Mahmoud Ezzamel — "Accounting, control and accountability: preliminary evidence from ancient Egypt" (*CPA* 8(6) (1997)); "Accounting and redistribution" (*AHJ* 29(1) (2002)); "Accounting and accountability in ancient civilizations: Mesopotamia and ancient Egypt" (*AAAJ* 20(2) (2007)) — critical review proposing an accountability framework and research agenda; *Accounting and Order* (Routledge, 2012); Ezzamel & Hoskin (2002), "Retheorizing accounting, writing and money," *CPA* 13(3).

**Survey landmarks:** Stevelinck & Most (1985), "Accounting in ancient times," *AHJ* 12(1); Tom Mouck (2004), "Ancient Mesopotamian accounting and human cognitive evolution," *AHJ* 31(2).

### 3.4 The *Accounting Historians Journal* as a venue

The *AHJ* (ISSN 0148-4184, now published by the American Accounting Association; full backfile open at egrove.olemiss.edu/aah_journal) is the principal Anglophone venue for pre-1800 accounting research. Verified landmark pre-1800 papers: Mattessich (1987) on token accounting; Oldroyd (1995) on Roman public expenditure; Ezzamel (2002) on Middle Kingdom Egypt; Inoue (1982) on Fugger bookkeeping; Sangster (2015) on de Raphaeli; Yamey (2012) on personal accounts c.1200–c.1800; Mouck (2004) on Mesopotamian accounting; Razek (1985) on the Louisiana plantation. The ancient/medieval strand is small but continuous since the 1980s — and it has published exactly the kind of method-and-reconstruction paper the Drehem project proposes.

---

## 4. Methods Used in the Field

| Tradition | Typical method | Unit of analysis | Computational content |
|---|---|---|---|
| Accounting historians (AHJ etc.) | Close reading of surviving books/treatises; doctrinal comparison | Single books, firms, treatises | None |
| de Roover-style reconstruction | Exhaustive archival study; manual cross-referencing across ledgers | Whole firm (Medici Bank) | None |
| Plantation historians (Rosenthal) | Archival sampling for practices; case studies of exceptional books | Practices across estates | None |
| Fleischman/Oldroyd/Tyson | Comparative ledger analysis; valuation-list aggregation | Estates, valuation parades | None (tabular aggregation) |
| Assyriologists (Steinkeller, Hilgert, Sallaberger) | Text edition; prosopography; institutional inference; database-assisted search (CDLI/BDTNS) | Archives, bureaus, offices | Databases as search aids only |
| Nissen/Damerow/Englund (1993) | Philology + computer analysis of numerical notation | Sign/metrological systems | Notation decoding, not ledgers |
| Old Assyrian computational work (Bamman/Anderson/Smith 2013; Anderson thesis) | Probabilistic latent-variable models; NLP + network theory for entity disambiguation | ~5,700 texts; social networks | Entity resolution — but output is networks/rank, not accounts |
| Bronze Age trade modeling (Barjamovic, Chaney, Coşar & Hortaçsu 2019, *QJE*) | Structural gravity (Ricardian) model on commercial records | Trade flows; lost cities | Economic modeling — not books |
| Medieval cliometrics (Clark 2007; Claridge et al. 2026) | Digitized *samples* of accounts for wage/price series | Series, panels | Sampling, not full-corpus ingestion |
| Prosopographical infrastructure (Trismegistos People; BDTNS; CDLI; ORACC; Ebla Digital Archives) | NER, linked open data, searchable corpora | Names, texts | Infrastructure — no analytical accounting layer |
| Forensic accounting (Benford etc.) | Statistical anomaly detection | Modern financial statements | No verified pre-1500 application |

**The pattern:** every tradition stops one step short of the Drehem method. Accounting historians reconstruct systems but manually; Assyriologists use databases but only as search aids; computational humanists resolve entities but build networks, not ledgers; cliometricians digitize but only samples; forensic accountants never touch ancient records.

---

## 5. Gaps and Opportunities

### 5.1 The gap is real and specific

To the best of verified knowledge, **no one has done a complete computational ledger reconstruction of an ancient (pre-1500) state accounting archive**: ingesting tens of thousands of records, computationally resolving entities, enforcing accounting-conservation constraints, and producing auditable books.

Closest prior art and how each differs:

1. **Hilgert (2013), "A Reconstruction of the Puzriš-Dagan Central Livestock Agency," *CDLJ* 2013:2** — same archive family (~13,500 Drehem tablets), database-assisted via CDLI/BDTNS, explicitly a reconstruction of the accounting administration into offices/bureaus. But philological (Yoffee's "artificial archives" method): no entity-resolution pipeline, no computed balances, no conservation constraints enforced computationally.
2. **Bamman, Anderson & Smith (2013), "Inferring Social Rank in an Old Assyrian Trade Network" (DH2013; arXiv:1303.2873)** — the only verified computational *entity resolution* over an ancient economic corpus (~5,700 Old Assyrian texts), jointly inferring individuals and rank. But the output is a social network, not a ledger; no accounting constraints.
3. **Barjamovic, Chaney, Coşar & Hortaçsu (2019), "Trade, Merchants, and the Lost Cities of the Bronze Age," *QJE* 134(3)** — the only verified *quantitative economic model* estimated on a large ancient commercial corpus. But it models bilateral trade flows to locate cities — no entity resolution, no conservation, no books.
4. **Trismegistos People / BDTNS / CDLI / ORACC / Ebla Digital Archives** — the data-infrastructure layer (prosopography, search, retrieval, linked open data). None reconstructs transactional books or enforces balance.
5. **Medieval cliometrics (Clark; Claridge et al.)** — digitize *samples* of account books for wage/price series; never ingest complete books as transactional databases. The Datini archive (500 account books, ~150,000 papers — the natural medieval candidate for full ledger ingestion) has only been studied with manual accounting-history methods.
6. **Forensic accounting on history** — essentially nonexistent as an empirical program. Kossovsky (2014) only theorizes that Benford's law *could* apply to ancient numeral systems; no study applies Benford, anomaly detection, or balance-check forensics to actual pre-1500 records. No verified application of missing-record estimation to ancient archives.

### 5.2 What this means for the Drehem project

- **Novelty claim (method):** "Computational full-ledger reconstruction of an ancient state archive with conservation-constraint validation" appears to be a first. The defensible novelty is the *method* — forensic flow reconstruction with physical conservation constraints (no-negative-inventory validation; imbalances as a lower bound on missing tablets; inventory as a chronology check) — not any single historical finding.
- **The accounting paper goes first for a reason.** AHJ has published Mattessich (1987, 1998), Ezzamel (2002), Mouck (2004), and Stevelinck & Most (1985) — the venue is proven for ancient-accounting method papers, and the field's own gap (no computational reconstructions) is the paper's warrant.
- **Borrow the Fleischman caution.** Scope claims to the archive: Drehem documents the *clearinghouse's* logic. Whether provincial practice matched is a separate empirical question the Umma/Girsu ledgers can address.
- **Borrow Rosenthal's ambition, not her sampling.** Full-corpus reconstruction answers the representativeness critique by construction.
- **The receipt-custody mechanism (Widell 2020, *Orient* 55)** converts the 48% deficit from an anomaly into a testable archival-formation hypothesis — exactly the kind of philology-meets-forensics result the method enables.
- **Open methodological questions to address in the paper:** (a) whether Ur III *nig₂-ka₉-ak* accounts were ever literally balanced (Dahl's skepticism); (b) namesake disambiguation limits (Berkeley authority does not disambiguate namesakes); (c) the double-entry question — the Drehem system is charge-and-discharge/balanced-account, not double-entry, and the paper should say so explicitly rather than invite the Sangster/Yamey debate.

### 5.3 Verification caveats (explicit)

- Author/title of the *ORIENT* 55 (2020) article on Ur III archiving and balanced accounts could not be verified (J-STAGE PDF fetch failed); do not cite until confirmed.
- Sangster's 2022 AECA working paper on the 1211 double-entry fragments: described from its abstract only; publication status unconfirmed.
- Author of the "Data Mining" chapter in Garfinkle & Molina (2013): unverified.
- Craig–Rodrigues follow-up Brazil paper ("The role of government accounting and taxation in the institutionalization of slavery in Brazil," believed *Critical Perspectives on Accounting*): year/issue unverified — treat as provisional.
- Tinkelman (2024) end page unverified.
- *Accounting History* volume/issue details for Orlandi (2021) unverified.
- No AHJ special issue on slavery was found, but absence was established by search, not by exhaustive backfile inspection.

---

## 6. Bibliography

- Baker, C. R. & Quéré, B. P. (2019). Governance and accounting practices in the Fugger family firm at the beginning of the sixteenth century. *Accounting History* (SAGE). DOI 10.1177/1032373219848146.
- Bamman, D., Anderson, A., & Smith, N. A. (2013). Inferring social rank in an Old Assyrian trade network. *Digital Humanities 2013*, Lincoln, NE. arXiv:1303.2873.
- Baptist, Edward E. (2014). *The Half Has Never Been Told: Slavery and the Making of American Capitalism*. New York: Basic Books.
- Barjamovic, G., Chaney, T., Coşar, A. K., & Hortaçsu, A. (2019). Trade, merchants, and the lost cities of the Bronze Age. *Quarterly Journal of Economics* 134(3): 1455–1503.
- Beckert, Sven (2014). *Empire of Cotton: A Global History*. New York: Alfred A. Knopf.
- Beckert, Sven, and Seth Rockman, eds. (2016). *Slavery's Capitalism: A New History of American Economic Development*. Philadelphia: University of Pennsylvania Press.
- Bryer, R. A. (1994). Accounting for the social relations of feudalism. *Accounting and Business Research* 24(95): 209–228. DOI 10.1080/00014788.1994.9729480.
- Carmona, S. & Ezzamel, M. (2007). Accounting and accountability in ancient civilizations: Mesopotamia and ancient Egypt. *Accounting, Auditing & Accountability Journal* 20(2): 177–209. DOI 10.1108/09513570710740993.
- Dahl, J. L. (2020). *Ur III Texts in the Schøyen Collection.* CUSAS 39. Eisenbrauns/Penn State University Press.
- de Roover, R. (1937). Aux origines d'une technique intellectuelle: la formation et l'expansion de la comptabilité à partie double. *Annales d'histoire économique et sociale* 9: 171–193, 270–298.
- de Roover, R. (1938). Characteristics of bookkeeping before Pacioli. *The Accounting Review* 13(2): 144–149.
- de Roover, R. (1948). *Money, Banking and Credit in Medieval Bruges.* Mediaeval Academy of America.
- de Roover, R. (1955). New perspectives on the history of accounting. *The Accounting Review* 30(3): 405–420.
- de Roover, R. (1963). *The Rise and Decline of the Medici Bank, 1397–1494.* Harvard University Press.
- Dobie, A. (2011). A review of the granators' accounts of Durham Cathedral Priory 1294–1433: An early example of process accounting? *Accounting History Review* 21: 1–35.
- Dobie, A. (2024). Medieval monastic accounting records: Potentials and pitfalls for statistical analysis. In Casson, M. & Lee, J. S. (eds.), *Medieval Statistics*, Palgrave Studies in the History of Finance, pp. 37–67. DOI 10.1007/978-3-031-69730-2_3.
- Engerman, Stanley L. (2017). Review of *The Half Has Never Been Told*. *Journal of Economic Literature* 55(2): 637–643.
- Englund, R. K. (2004). Proto-cuneiform account-books and journals. In Englund, R. K. & Nissen, H. J. (eds.), *Archaic Bookkeeping II* (CDLI-hosted).
- Ezzamel, M. (1994). The emergence of the 'accountant' in the institutions of Ancient Egypt. *Management Accounting Research* 5: 221–246.
- Ezzamel, M. (1997). Accounting, control and accountability: preliminary evidence from ancient Egypt. *Critical Perspectives on Accounting* 8(6): 563–601. DOI 10.1006/cpac.1997.0123.
- Ezzamel, M. (2002). Accounting and redistribution: The palace and mortuary cult in the Middle Kingdom, ancient Egypt. *Accounting Historians Journal* 29(1), Article 4.
- Ezzamel, M. (2012). *Accounting and Order.* Routledge. DOI 10.4324/9780203123300.
- Ezzamel, M. & Hoskin, K. (2002). Retheorizing accounting, writing and money with evidence from Mesopotamia and ancient Egypt. *Critical Perspectives on Accounting* 13(3): 333–367. DOI 10.1006/cpac.2001.0500.
- Fleischman, Richard K. (2004). Confronting moral issues from accounting's dark side. *Accounting History* 9(1): 7–23.
- Fleischman, Richard K., David Oldroyd, and Thomas N. Tyson (2004). Monetising human life: Slave valuations on US and British West Indian plantations. *Accounting History* 9(2): 35–62.
- Fleischman, Richard K., David Oldroyd, and Thomas N. Tyson (2011). Plantation accounting and management practices in the US and the British West Indies at the end of their slavery eras. *Economic History Review* 64(3): 765–797.
- Fleischman, Richard K., David Oldroyd, and Thomas N. Tyson (2011). The efficacy/inefficacy of accounting in controlling labour during the transition from slavery in the United States and British West Indies. *Accounting, Auditing & Accountability Journal* 24(6): 751–780.
- Fleischman, Richard K., and Thomas N. Tyson (2004). Accounting in service to racism: Monetizing slave property in the antebellum south. *Critical Perspectives on Accounting* 15(3): 376–399.
- Flesher, Dale L., and Tonya K. Flesher (1980). Human resource accounting in Mississippi before 1865. *Accounting and Business Research* 10, suppl. 1: 124–129.
- Garfinkle, S. J. (2004). Shepherds, merchants, and credit: Some observations on lending practices in Ur III Mesopotamia. *Journal of the Economic and Social History of the Orient* 47(1): 1–30.
- Garfinkle, S. J. & Molina, M., eds. (2013). *From the 21st Century B.C. to the 21st Century A.D.: Proceedings of the International Conference on Sumerian Studies, Madrid 2010.* Eisenbrauns.
- Gardin, J.-C. & Garelli, P. (1961). Étude des établissements assyriens en Cappadoce par ordinateurs. *Annales* 16(5): 837–876.
- Giraudeau, Martin (2017). The farm as an accounting laboratory: An essay on the history of accounting and agriculture. LSE Research Online 74106.
- Hilgert, M. (1998). *Cuneiform Texts from the Ur III Period in the Oriental Institute, Vol. 1: Drehem Administrative Documents from the Reign of Shulgi.* OIP 115. Oriental Institute, Chicago.
- Hilgert, M. (2013). A reconstruction of the Puzriš-Dagan central livestock agency. *Cuneiform Digital Library Journal* 2013:2.
- Hilt, Eric (2017). Economic history, historical analysis, and the 'new history of capitalism'. *Journal of Economic History* 77(2): 511–536.
- Hoskin, K. W. & Macve, R. H. (1986). Accounting and the examination: a genealogy of disciplinary power. *Accounting, Organizations and Society* 11(2): 105–136.
- Inoue, K. (1982). Threefold bookkeeping by Matthaus Schwarz. *Accounting Historians Journal* 9(1), Article 3.
- Johnson, Walter (2013). *River of Dark Dreams: Slavery and Empire in the Cotton Kingdom*. Cambridge, MA: Harvard University Press.
- Kossovsky, A. E. (2014). *Benford's Law: Theory, the General Law of Relative Quantities, and Forensic Fraud Detection Applications*. World Scientific.
- Lagroue, L. (2014). *Accounting and Auditing in Roman Society.* PhD dissertation, University of North Carolina at Chapel Hill.
- Mattessich, R. (1987). Prehistoric accounting and the problem of representation: On recent archeological evidence of the Middle-East from 8000 B.C. to 3000 B.C. *Accounting Historians Journal* 14(2): 71–91. DOI 10.2308/0148-4184.14.2.71.
- Mattessich, R. (1994). Archaeology of accounting and Schmandt-Besserat's contribution. *Accounting, Business and Financial History* 4(1): 5–28.
- Mattessich, R. (1998). Recent insights into Mesopotamian accounting of the 3rd millennium B.C. — Successor to token accounting. *Accounting Historians Journal* 25(1); correction 25(2): 147–149.
- Mattessich, R. (2000). *The Beginnings of Accounting and Accounting Thought: Accounting Practice in the Middle East (8000 BC to 2000 BC) and Accounting Thought in India (300 BC and the Middle Ages).* Taylor & Francis.
- Mouck, T. (2004). Ancient Mesopotamian accounting and human cognitive evolution. *Accounting Historians Journal* 31(2): 97–124.
- Nissen, H. J., Damerow, P. & Englund, R. K. (1993). *Archaic Bookkeeping: Early Writing and Techniques of Economic Administration in the Ancient Near East.* University of Chicago Press.
- Oldroyd, D. (1995). Role of accounting in public expenditure and monetary policy in the first century AD Roman Empire. *Accounting Historians Journal* 22(2), Article 5.
- Olmstead, Alan L., and Paul W. Rhode (2018). Cotton, slavery, and the new history of capitalism. *Explorations in Economic History* 67: 1–17.
- Orlandi, A. (2021). The emergence of double-entry bookkeeping in Tuscan firms of the thirteenth and fourteenth centuries. *Accounting History* (SAGE). [Volume/issue unverified.]
- Pacioli, L. (1494). *Summa de arithmetica, geometria, proportioni et proportionalità.* Venice: Paganino de Paganini.
- Razek, Joseph R. (1985). Accounting on the old plantation: A study of the financial records of an antebellum Louisiana sugar planter. *The Accounting Historians Journal* 12(1): 17–36.
- Rodrigues, L. L., Craig, R. J., Schmidt, P. & Santos, J. L. (2015). Documenting, monetising and taxing Brazilian slaves in the eighteenth and nineteenth centuries. *Accounting History Review* 25(1): 43–67.
- Rosenthal, Caitlin C. (2013). From memory to mastery: Accounting for control in America, 1750–1880. *Enterprise & Society* 14(4): 732–748.
- Rosenthal, Caitlin (2018). *Accounting for Slavery: Masters and Management*. Cambridge, MA: Harvard University Press.
- Sallaberger, W. (1999). Ur III-Zeit. In Sallaberger, W. & Westenholz, A., *Mesopotamien: Akkade-Zeit und Ur III-Zeit*, OBO 160/3. Universitätsverlag Freiburg / Vandenhoeck & Ruprecht.
- Sallaberger, W. (2013). Killing and skinning animals in the Ur III period: The Puzriš-Dagan (Drehem) office managing of dead animals and slaughter by-products. *Altorientalische Forschungen* 40.
- Sangster, A. (2015). The earliest known treatise on double entry bookkeeping by Marino de Raphaeli. *Accounting Historians Journal* 42(2): 1–33. DOI 10.2308/0148-4184.42.2.1.
- Sangster, A. (2016). The genesis of double entry bookkeeping. *The Accounting Review* 91(1): 299–315. DOI 10.2308/accr-51115.
- Sangster, A. (2018). Pacioli's lens: God, humanism, Euclid, and the rhetoric of double entry. *The Accounting Review* 93(2): 299–314.
- Schmandt-Besserat, D. (1992). *Before Writing, Vol. I: From Counting to Cuneiform; Vol. II: A Catalog of Near Eastern Tokens.* University of Texas Press.
- Schmandt-Besserat, D. (1996). *How Writing Came About.* University of Texas Press.
- Sigrist, M. (1992). *Drehem.* CDL Press.
- Spraakman, G. (2015). *Management Accounting at the Hudson's Bay Company: From Quill Pen to Digitization.* Emerald (Studies in the Development of Accounting Thought, vol. 17). ISBN 9781784415860.
- Steinkeller, P. (1987). The administrative and economic organization of the Ur III state: The core and the periphery. In Gibson, M. & Biggs, R. D. (eds.), *The Organization of Power*, SAOC 46. Oriental Institute, Chicago, 15–34.
- Steinkeller, P. (2003). Archival practices at Babylonia in the third millennium. In Brosius, M. (ed.), *Ancient Archives and Archival Traditions: Concepts of Record-Keeping in the Ancient World.* Oxford University Press, 37–58.
- Steinkeller, P. (2004). The function of written documentation in the administrative praxis of early Babylonia. In Hudson, M. & Wunsch, C. (eds.), *Creating Economic Order: Recordkeeping, Standardization and the Development of Accounting in the Ancient Near East.* CDL Press, 65–88.
- Stevelinck, E. & Most, K. S. (1985). Accounting in ancient times. *Accounting Historians Journal* 12(1): 1–16.
- Tinkelman, Daniel (2024). 'Money does not stink' — Accounting and slavery. *Accounting History* 29(2). DOI 10.1177/10323732241236974. [End page unverified.]
- Tsouparopoulou, C. (2008). *The Material Face of Bureaucracy: Writing, Sealing and Archiving Tablets for the Ur III State at Drehem.* PhD dissertation, University of Cambridge.
- Tsouparopoulou, C. (2015). *The Ur III Seals Impressed on Documents from Puzriš-Dagān (Drehem).* HSAO 16. Heidelberger Orientverlag.
- Tyson, Thomas, David Oldroyd, and Richard K. Fleischman (2004). Theoretical perspectives on accounting for labor on slave plantations of the USA and British West Indies. *Accounting, Auditing & Accountability Journal* 17(5): 758–778.
- Tyson, Thomas, and David Oldroyd (2018). Accounting for slavery during the Enlightenment: Contradictions and interpretations. *Accounting History* 24(2): 212–235.
- Widell, Magnus (2020). Ur III economy and bureaucracy: The Neo-Sumerian cuneiform tablets in the Hood Museum of Art, Dartmouth College (I). *Orient* 55: 117–154. [Receipt-custody mechanism: the deliverer kept the sealed receipt as evidence.]
- Yamey, B. S. (1949). Scientific bookkeeping and the rise of capitalism. *The Economic History Review* 1(2/3): 99–113.
- Yamey, B. S. (1964). Accounting and the rise of capitalism: further notes on a theme by Sombart. *Journal of Accounting Research* 2(2): 117–136.
- Yamey, B. S. (2012). Personal accounts, account books and their probative value: Historical notes, c.1200–c.1800. *Accounting Historians Journal* 39(2), Article 2.

### Provisional / unverified (do not cite until confirmed)

- Craig, Rodrigues et al., "The role of government accounting and taxation in the institutionalization of slavery in Brazil" (believed *Critical Perspectives on Accounting*; year/issue unverified).
- *ORIENT* 55 (2020) article on Ur III archiving and balanced accounts (author/title unverified; J-STAGE PDF fetch failed).
- Sangster (2022), AECA working paper on the 1211 double-entry fragments (publication status unconfirmed).
- Author of "Symbols and Bureaucratic Performances in the Ur III Administrative Sphere: An Interpretation Through Data Mining," in Garfinkle & Molina (2013).

---

*Method note: this review was produced by three parallel research passes (plantation accounting; pre-modern accounting history; forensic/computational methods) with web verification of authors, titles, years, and venues. It is a web-search review, not a systematic bibliographic survey. Before publication, systematically check the* Accounting Historians Journal *backfile (egrove.olemiss.edu), CDLI publications, Assyriological RAI proceedings, and the* Journal of Computer Applications in Archaeology.
