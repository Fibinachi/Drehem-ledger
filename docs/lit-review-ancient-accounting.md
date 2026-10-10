# Literature Review: Accounting in Ancient Civilizations

*Prepared 2026-10-09 in support of the Drehem-ledger project — a computational reconstruction of the Ur III state accounting system from ~50,000 cuneiform tablets (CDLI ATF data), with transaction ledger, entity resolution, and physical-conservation checks.*

**Method note.** This review was compiled from web searches conducted 2026-10-09. Every publication cited below was located and individually checked (year, title, venue) in this session via search results, publisher pages, library catalogs, or peer-reviewed bibliographies. Items are marked **VERIFIED** when confirmed through an authoritative source, **PARTIALLY VERIFIED** when cited in a reliable secondary source but not independently confirmed, and flagged when unverifiable. The review answers one central question: **has anyone previously built a unified computational ledger — with entity resolution and conservation checks — over the Ur III archives?**

---

## Overview

### The novelty question, answered plainly

**No.** Three independent research passes — Ur III administrative scholarship, accounting-history literature, and computational cuneiform studies — found **no published project that consolidates the Ur III archives into a single transaction ledger, performs global entity resolution across it, and validates flows with conservation (inflow = outflow) checks.** The pieces exist in isolation, but the combination does not.

What the field *has* done:

1. **Organizational reconstruction without a ledger.** The landmark is Tsouparopoulou 2013 (CDLJ 2013/2), "A Reconstruction of the Puzriš-Dagan Central Livestock Agency": she reconstructed Drehem's four-office structure from "artificial archives" and transaction formulas — offices and flows of *responsibility*, explicitly not a consolidated ledger. She states its limits herself: tentative, "not to be considered as an accurate depiction of the way in which the Puzriš-Dagan officials would themselves have perceived the organization," and with no archaeological control.
2. **Name disambiguation without accounting.** The Sumerian Network project (Veldhuis/Anderson, Berkeley, 2017–2021) ran unsupervised name disambiguation over ~15,000 Drehem texts — the nearest thing to Ur III entity resolution — but its product is *networks of name instances*, not a resolved transaction ledger.
3. **Quantitative mining of narrow questions.** Cripps (2017, CDLJ) extracted barley:silver price ratios from 60,000–70,000 CDLI Ur III texts — genuine at-scale quantitative work, but a price study, not a ledger. Widell (2020, JNES) ran statistical analysis of 3,080 delivery texts for seasonal breeding patterns — flow analysis of seasonality, not of accounting balance.
4. **Accounting theory on early periods, not on the Ur III corpus.** Mattessich's formal analyses (1987–2000) built the Mesopotamian-origins thesis inside accounting on token archaeology and the Uruk archaic tablets (Nissen, Damerow & Englund 1993), not on the Ur III administrative corpus at archive scale.
5. **Named-entity recognition, not resolution.** Liu, Luo, Hearne & Burkhart (2015–2016) did Sumerian NER — finding names in text — not deciding which mentions are the same person.

The gap is real and citable: **no consolidated ledger, no whole-archive flow/conservation analysis, no entity-resolved transaction layer across the Ur III archives.** Two independent subagent research passes reached this conclusion.

### Publication-strategy note

The *Accounting Historians Journal* (AHJ) is a proven venue for ancient-accounting work: Ezzamel (2002), Mattessich (1987, 1998), Mouck (2004), Vollmers (2009), Yeakel (1983) all published there. This supports the project's planned AHJ submission on the Drehem ledger method — the audience exists.

---

## Mesopotamian/Ur III Administrative Scholarship

### The record-keeping system

The Third Dynasty of Ur (2112–2004 BCE) left one of the densest administrative archives in antiquity — "almost a hundred thousand known documents" (Michalowski 2008), nearly all looted from unexcavated tells and dispersed through museums and private collections from 1909 onward. Ur III accounting scholarship converges on a system of **primary documents** (small, single-transaction tablets) rolled up into **secondary/consolidated accounts** — a two-tier bookkeeping structure Englund traces back to the proto-cuneiform period (Englund 2004).

Key document types:

- **Receipts — *šu ba-ti* ("received")**: record a delivery into an official's custody; the text is sealed by the receiving party and **retained by the deliverer as proof of performance**. Verified citation: Widell 2020, "Ur III Economy and Bureaucracy: The Neo-Sumerian Cuneiform Tablets in the Hood Museum of Art, Dartmouth College (I)," *Orient* 55: 117–154 (DOI 10.5356/orient.55.117). Widell 2009 (CDLJ 2009/6) is the companion piece on who-archived-what.
- **Disbursements — *zi-ga / ba-zi* ("booked out / issued")**: record issues from stores. A full study of *mu-TÚM* and *zi-ga/ba-zi* texts from the Drehem animal center appears as chapter 28 of Garfinkle & Molina (eds.) 2013.
- **Deliveries — *mu-kuₓ(DU)* ("delivery")**: the intake documents of the Drehem livestock system. Widell (JNES 79/2, 2020) found 3,080 such texts in BDTNS, 2,894 of them recording sheep/goat deliveries.
- **Balanced accounts — *níg-ka₉-ak* ("account made")**: periodic compilations that net receipts against disbursements, carried forward with opening balances. Drafting a year's summary was evidently painful — Van De Mieroop's 1999/2000 study is literally titled "An Accountant's Nightmare: the Drafting of a Year's Summary" (*AfO* 46/47: 111–129).
- **Audit/liability practice**: deficits were chased down the chain of command. See Wilcke 2005 ("The Liability of Superiors for Deficits of their Subordinates," *NABU* 2005/3: no. 74) and Waetzoldt & Sigrist 1993 on liability for unfulfilled service obligations.

Standardization was the precondition: Englund 1988 ("Administrative Timekeeping in Ancient Mesopotamia," *JESHO* 31/2) shows the 30-day administrative month / 12-month year was an accounting technology used for ration and labor-obligation calculation; theoretical (expected) vs. actual performance was checked against production norms (Nissen, Damerow & Englund 1993; Mattessich 1998).

### The three great archives

- **Drehem / Puzriš-Dagān**: the royal livestock center, founded by Šulgi ~year 38. Over 15,000 tablets looted from 1909 onward (al-Mutawalli, Sallaberger & Shalkham 2017, *ZA* 107/2); the first controlled excavation (Shalkham, 2007) yielded in-context records. Scholarship treats Drehem as a **livestock clearinghouse directly subordinated to the royal bureaucracy** (not to any provincial administration): animals arrived as taxes (*gun₂ ma-da*), tribute, war loot, and diplomatic gifts, and were redistributed to the cult, the army, the court, and foreign envoys (Steinkeller 1991; Tsouparopoulou 2013; Widell 2026). Tsouparopoulou's key revision: Drehem was primarily an **administrative center** — its officials were scribes collecting tablets, not herders; there was no giant stockyard on site (Tsouparopoulou 2013, CDLJ 2013/2).
- **Umma**: the largest provincial archive; the most-studied Ur III provincial bureaucracy. Molina's BDTNS-based corpus overview (Garfinkle & Johnson 2008) and his court-record studies (Molina 2010, 2014) are the entry points; prosopographic infrastructure from Stępień 1996 and Dahl 2007 (*The Ruling Family of Ur III Umma*, PIHANS 108). Umma is the foil for Drehem: provincially organized, operating within its own structures (Steinkeller 1987, 2001).
- **Girsu/Lagaš**: massive temple-household archive (pre-Sargonic through Ur III). The Ur III messenger-text corpus was published by Notizia 2009 (*Nisaba* 22); the *bala* (rotating provincial tax) system's Girsu anomaly is discussed by Sharlach 2004 (citing Sallaberger's suggestion it reflects Girsu's early-Ur III political importance).

### Scholars who study these archives as accounting/economic systems

- **Robert K. Englund (UCLA)**: metrology and accounting technology across the whole 3rd millennium. *Archaic Bookkeeping* (with Nissen & Damerow, 1993, U. Chicago Press) is the foundation. Ur III-specific work includes "Administrative Timekeeping in Ancient Mesopotamia" (1988, *JESHO* 31/2); "Hard Work — Where Will It Get You? Labor Management in Ur III Mesopotamia" (1991, *JNES* 50/4); *Organisation und Verwaltung der Ur III-Fischerei* (1990, BBVO 10); "Regulating Dairy Productivity in the Ur III Period" (1995, *Orientalia* 64/4); "Worcester Slaughterhouse Account" (2003, CDLB 2003/1); "Proto-Cuneiform Account-Books and Journals" (2004, in Hudson & Wunsch eds.). Also a co-director of CDLI.
- **Piotr Steinkeller (Harvard)**: the macro-model of the Ur III state. "The Administrative and Economic Organization of the Ur III State: The Core and the Periphery" (1987, in Gibson & Biggs eds., SAOC 46: 15–33) is the canonical statement that Drehem/Urim sat at the royal core while provinces like Umma and Girsu ran their own administrations. Also "Sheep and Goat Terminology in Ur III Sources from Drehem" (1995, *BSA* 8); "Money-Lending Practices in Ur III Babylonia" (2002, in Hudson & van de Mieroop eds.); "Toward a Definition of Private Economic Activity in Third Millennium Babylonia" (2004); "On Editing Ur III Economic Texts" (1982, *JAOS* 102/4).
- **Manuel Molina (CSIC Madrid)**: builder of BDTNS (the online Neo-Sumerian text database) — the infrastructural precondition for any system-level work. "The Corpus of Neo-Sumerian Tablets: An Overview" (2008, in Garfinkle & Johnson eds.); "Court Records From Umma" (2010, in Kleinerman & Sasson eds.); "Court Officials at Umma in Ur III Times" (2014, *ZA* 103/2); "On the Location of Irisaĝrig" (2013, in Garfinkle & Molina eds.). Co-editor of the 2008 Ur III workshops volume and the 2013 Madrid proceedings.
- **Magnus Widell (Liverpool)**: the most quantitatively inclined of the group. Verified works: *The Administrative and Economic Ur III Texts from the City of Ur* (2003, Gorgias Press); "The Ur III Metal Loans from Ur" (2008, in Garfinkle & Johnson eds.); "Two Ur III Texts from Umma: Observations on Archival Practices and Household Management" (2009, CDLJ 2009/6); "The Administration of Storage in Early Babylonia" (2018, *Orient* 53); "Ur III Economy and Bureaucracy: The Neo-Sumerian Cuneiform Tablets in the Hood Museum of Art, Dartmouth College (I)" (2020, *Orient* 55); "Destined for Slaughter: Identifying Seasonal Breeding Patterns in Sheep and Goats in Early Babylonia" (2020, *JNES* 79/2); and *Administration and Economy in Early Babylonian Society* (2026, Oxford UP).
- **Steven J. Garfinkle (Western Washington)**: the Ur III merchant/private-enterprise specialist — the closest thing to an accounting lens on the non-state sector. *Entrepreneurs and Enterprise in Early Mesopotamia* (2012, CUSAS/CDL Press); "Shepherds, Merchants, and Credit" (2004, *JESHO* 47/1); "Was the Ur III State Bureaucratic?" (2008); "The Third Dynasty of Ur and the Limits of State Power" (2013); "Ur III Administrative Texts: Building Blocks of State Community" (2015, in Delnero & Lauinger eds., SANER 9); "Family Firms in the Ur III Period" (2015, 57th RAI proceedings); "The House of Ursaga" (2020).
- **David I. Owen (Cornell)**: founding editor of the CUSAS monograph series (the main venue for Ur III text editions); editor of *Cuneiform Texts Primarily from Iri-Saĝrig/Āl-Šarrākī* (2013, Nisaba 15, CDL Press).
- **Walther Sallaberger (Munich)**: the great synthesizer. *Der kultische Kalender der Ur III-Zeit* (1993, UAVA 7/1); the ~300-page Ur III essay in Bauer, Englund & Krebernik (eds.), *Mesopotamien: Akkade-Zeit und Ur III-Zeit* (1999, OBO 160/3); co-author of the 2017 *ZA* report on the Iraqi excavation at Drehem.
- **Tonia M. Sharlach (Oklahoma State)**: *Provincial Taxation and the Ur III State* (2004, Cuneiform Monographs 26, Brill) — the first interarchival synthesis (Umma, Lagash, Puzriš-Dagan) of the *bala* rotating-tax system, with ~150 newly edited tablets.
- **Christina Tsouparopoulou**: the Drehem archival specialist — most directly relevant to a Drehem-ledger project. "A Reconstruction of the Puzriš-Dagan Central Livestock Agency" (2013, CDLJ 2013/2); "Killing and Skinning Animals in the Ur III Period" (2013, *AoF* 40/1); *The Ur III Seals Impressed on Documents from Puzriš-Dagān (Drehem)* (2015); "'Counter-Archaeology': Putting the Ur III Drehem Archives Back in the Ground" (2017).

Accounting-history angle (outside Assyriology): **Richard Mattessich**, "Recent Insights into Mesopotamian Accounting of the 3rd Millennium BC: Successor to Token Accounting" (1998, *AHJ* 25/1, plus 1998 correction 25/2); *The Beginnings of Accounting and Accounting Thought* (2000, Garland); **Tom Mouck**, "Ancient Mesopotamian Accounting and Human Cognitive Evolution" (2004, *AHJ* 31/2).

---

## Other Ancient Civilizations

### Ancient Egypt

Egyptian administration ran on scribes from Dynasty 0 (~3300 BC) onward. Key structural facts noted in the literature: grain and labor administration under royal storehouses with internal verification ("royal audits"), a money-of-account system (the *deben*) used as a common denominator across commodities despite the absence of coinage, and daily attendance/work-target lists on royal construction projects under Senusret III that resemble modern job-costing.

The **Wilbour Papyrus** (c. 1145 BC, 10 m, Brooklyn Museum) is the largest known non-funerary papyrus — a survey of cultivable lands in Middle Egypt with sections on privately/collectively owned land and royal land. Published edition: Gardiner, A. H. (1941–1952), *The Wilbour Papyrus*, Oxford University Press, 3 vols. (PARTIALLY VERIFIED — cited as "Gardiner, 1941" in Carmona & Ezzamel 2007).

**Mahmoud Ezzamel** (Cardiff/IE Business School) is the dominant figure in the *accounting-history* literature on Egypt, working from primary papyri:

- Ezzamel, M. (2002), "Accounting and redistribution: The palace and mortuary cult in the Middle Kingdom, ancient Egypt," *AHJ* 29(1). VERIFIED.
- Ezzamel, M. (2002), "Accounting for Private Estates and the Household in the Twentieth Century BC Middle Kingdom, Ancient Egypt," *Abacus* 38(2), 235–262. VERIFIED.
- Ezzamel, M. (2004), "Work Organization in the Middle Kingdom, Ancient Egypt," *Organization* 11(4), 497–537. VERIFIED.
- Ezzamel, M. (2005), "Accounting for the Practices of Funerary Temples: The Intertwining of the Sacred and the Profane," *Accounting and Business Research* 35(1), 29–51. VERIFIED. Analyzes how mortuary-cult endowment contracts allocated measured quantities of offerings — i.e., literally which gods/dead received what resources. **This is the single most on-point paper for the project's sociology-of-religion angle.**
- Ezzamel, M. & Hoskin, K. (2002), "Retheorizing Accounting, Writing and Money with Evidence from Mesopotamia and Ancient Egypt," *Critical Perspectives on Accounting* 13(3), 333–367. VERIFIED.
- Ezzamel, M. (2014), *Accounting and Order*, Routledge (Routledge Studies in Accounting). VERIFIED — draws on Egyptian inscriptions (offerings, taxation, redistribution, work organization) to theorize accounting as producing social order.

The synthesis anchor for comparative ancient-accounting scholarship:

- Carmona, S. & Ezzamel, M. (2007), "Accounting and accountability in ancient civilizations: Mesopotamia and ancient Egypt," *Accounting, Auditing & Accountability Journal* 20(2), 177–209. VERIFIED.
- Carmona, S. & Ezzamel, M. (2008), "Ancient accounting," in Edwards, R. & Walker, S.P. (eds.), *The Routledge Companion of Accounting History*, pp. 73–94. VERIFIED.

From within Egyptology proper: Janssen, J.J. (1979), "The Role of the Temple in the Egyptian Economy During the New Kingdom," in Lipiński (ed.), *State and Temple Economy in the Ancient Near East*, Vol. 2, Leuven, p. 509 (VERIFIED — argued New Kingdom temples were part of state administration, "at the disposal of Pharaoh"); Janssen, J.J. (1975), *Commodity Prices from the Ramessid Period* (Brill) and "Prolegomena to the study of Egypt's economic history during the New Kingdom," *SAK* 3, 127–185 (PARTIALLY VERIFIED — cited in published bibliographies).

### Temples as economic entities (sociology-of-religion angle)

This thread directly serves the "which gods received what resources" research question:

- Haring, B.J.J. (1997), *Divine Households: Administrative and Economic Aspects of the New Kingdom Royal Memorial Temples in Western Thebes*, Leiden: NINO (Egyptologische Uitgaven 12). VERIFIED — directly addresses whether temples were economically independent or integrated into state administration.
- Ezzamel, M. (2005) — see above; funerary-temple endowment contracts as measured resource allocation to the divine/dead.
- Ezzamel, M. (2002), "Accounting and redistribution" — covers inflow (taxation in kind to state granaries) and outflow (provisions to palace dependents; mortuary-cult contracts), i.e., the full redistributive cycle through temples and palace.
- Janssen, J.J. (1979) — temple role in the Egyptian economy (above).
- PARTIALLY VERIFIED: Stevens, M.E. (2006), *Temples, Tithes, and Taxes: The Temple and the Economic Life of Ancient Israel*, Hendrickson (Jerusalem temple as central bank, tax collector, lender, debt collector; written by a CPA-turned-OT scholar); Hudson, M. (2024), *Temples of Enterprise* (ISLET — money, markets, and land tenure originating in Near Eastern temples and palaces).

The Persepolis Fortification tablets (see below) show ration flows through a royal (not temple) institution — a useful contrast for temple-vs-palace arguments.

### Inca quipu

The best-documented non-literate accounting system, with the clearest archival evidence (the Inkawasi storehouse find gave the first in-use archaeological context):

- Yeakel, J.A. (1983), "The Accountant-Historians of the Incas," *AHJ* 10(2), Art. 3. VERIFIED — argues the quipucamayocs were accountant-historians recording decimal quantities without money as a common denominator.
- Urton, G. & Chu, A. (2015), "Accounting in the King's Storehouse: The Inkawasi Khipu Archive," *Latin American Antiquity* 26(4), 512–529. VERIFIED — 34 khipus excavated 2013–14 at the Inkawasi state storehouse; standardized produce accounting units and "checks-and-balances" practices; first evidence of Inca taxation in kind.
- Urton, G. & Brezine, C.J. (2005), "Khipu Accounting in Ancient Peru," *Science* (12 Aug 2005). VERIFIED.
- Urton, G. (2003), *Signs of the Inka Khipu: Binary Coding in the Andean Knotted-String Records*, University of Texas Press. VERIFIED.
- Urton, G. (2017), *Inka History in Knots: Reading Khipus as Primary Sources*, University of Texas Press (PROSE Award, 2018). VERIFIED.

### Early China

The three-pillar (*sanzhufa*) single-entry system — journal (*caoliu*) and ledger (*zongqing*), entries headed by *ru* (income) / *chu* (expenditure), closed by the equation income − expenditure = balance (*yu*) — is attributed to the Western Zhou (1122–771 BC), with specialized state-account officials, budgetary control, 10-day/monthly/yearly reporting, and government audit:

- Fu, P. (1971), "Governmental Accounting in China during the Chao [Zhou] Dynasty (1122 B.C.-256 B.C.)," *Journal of Accounting Research* 9 (Spring 1971), 40–51. VERIFIED.
- Guo, D. (1982, 1988), *Sketches on the History of Accounting in China*, Vols. 1–2 (in Chinese), Beijing: China Financial and Economic Publishing House. VERIFIED (published reference list; Guo is the leading Chinese accounting historian).

### Achaemenid Persia

- Vollmers, G.L. (2009), "Accounting and Control in the Persepolis Fortification Tablets," *AHJ* 36(2), 93–111. VERIFIED (eGrove repository; 509–494 BC ration-distribution bookkeeping, making "quantities, locations and individuals responsible" visible).
- Vollmers, G. (1996), "The Persepolis Fortification Texts: Accounting and Control in Ancient Persia from 509 to 494 B.C.," *Accounting Enquiries* 6(1), 1–43. PARTIALLY VERIFIED (cited in the 2009 paper's own reference list).

### Indus Valley

No accounting-history literature exists — the script remains undeciphered. Closest peer-reviewed statement of administrative/commercial use: Yadav, N. et al. (2019), "Interrogating Indus inscriptions to unravel their mechanisms of meaning conveyance," *Humanities and Social Sciences Communications* (VERIFIED — inscriptions cluster near workshops and gates, found with standardized weights, rarely in religious contexts; "seals/weights suggest administration" is as far as evidence goes).

### Mesoamerica

The Aztec *Matrícula de Tributos* (pre-Conquest pictographic manuscript, 16 folios, likely model for *Codex Mendoza* Part II, c. 1541–42) records per-province tribute in standardized numerical glyphs (flag = 20, feather = 400, pouch = 8,000), cross-validated against the Mendoza and Codex Azoyú II. Michael E. Smith (Arizona State) argues in *Archaeology* (May/June 2021) that the system was taxation (at least 11 tax types), not mere tribute. **Gap: no scholarship in the accounting-history journals treats the tribute codices as accounting systems** — a genuinely underdeveloped comparison (pictographic, standardized, quantified, scribe-audited, imperial revenue administration). The Maya case is thinner still.

### The "history of accounting" literature on Mesopotamian origins

**Richard Mattessich** (UBC) is the central academic figure — and his work is **based on actual archive/artifact analysis** (Schmandt-Besserat's token studies; the Uruk archaic texts as published by Nissen, Damerow & Englund), formalizing an "input–output principle" of early accounting:

- Mattessich, R. (1987), "Prehistoric accounting and the problem of representation: On recent archaeological evidence of the Middle-East from 8000 B.C. to 3000 B.C.," *AHJ* 14(2), 71–91. VERIFIED.
- Mattessich, R. (1989), "Accounting and the input-output principle in the ancient and prehistoric world," *Abacus* 25(2), 74–84. VERIFIED.
- Mattessich, R. (1994), "Archaeology of Accounting and Schmandt-Besserat's Contribution," *Accounting, Business & Financial History* 4(1), 5–28. VERIFIED.
- Mattessich, R. (1998), "Recent insights into Mesopotamian accounting of the 3rd millennium B.C. — Successor to token accounting," *AHJ* 25(1), 1–27 (plus 1998 follow-up correction, 25(2), 147–149). VERIFIED.
- Mattessich, R. (2000), *The Beginnings of Accounting and Accounting Thought: Accounting Practice in the Middle East (8000 B.C. to 2000 B.C.) and Accounting Thought in India (300 B.C. and the Middle Ages)*, New York: Garland. VERIFIED.

The archaeological foundation: Schmandt-Besserat, D. (1992), *Before Writing*, Vol. 1: *From Counting to Cuneiform*, UT Press; (1997), *How Writing Came About* (PARTIALLY VERIFIED — listed in published bibliographies); Nissen, H.J., Damerow, P. & Englund, R.K. (1993), *Archaic Bookkeeping*, U. Chicago Press (VERIFIED).

**Correction:** Basil Yamey is **not** a Mesopotamia-origins figure and should not be cited as one. His field was early Italian double-entry bookkeeping and accounting in art (medieval/Renaissance). See Sangster, A. (2021), "Basil Yamey (1919–2020)," *AHJ* 48(1). The Mesopotamian origins claim transmits in three tiers: (1) **empirical** (Schmandt-Besserat, Uruk tablets, Mattessich); (2) **disciplinary synthesis** (Carmona & Ezzamel 2007; *Routledge Companion* 2008); (3) **textbook folklore** (Wikipedia-tier summaries repeating the claim with no archive engagement).

**Live scholarly dispute to treat as hypothesis, not fact:** Hallo, W.W. (2004), "Bookkeeping in the Twenty-First Century BCE," in Hudson, M. & Wunsch, C. (eds.), *Creating Economic Order*, Vol. IV (PARTIALLY VERIFIED) — argued for something like double-entry in Ur III tablets. The Drehem ledger project is well positioned to test this.

---

## Computational and Quantitative Approaches

### The CDLI (Cuneiform Digital Library Initiative)

The CDLI is an international digital-library project founded in 1998 to put images and text of an estimated 500,000 cuneiform tablets online (VERIFIED — Wikipedia, NYCDH, Berkeley news). A joint project of UCLA, the University of Oxford, and the Max Planck Institute for the History of Science (Berlin); directors: Robert K. Englund (UCLA) and Jürgen Renn (MPIWG); co-PIs: Jacob Dahl (Oxford), Bertrand Lafont (CNRS, Nanterre), and Émilie Pagé-Perron (Toronto).

It provides catalog records, high-resolution images, **ATF transliterations** (Canonical ASCII Transliteration Format), some translations, bibliography, and seal data. Ur III texts are by far the largest third-millennium group. **Bulk data is publicly downloadable**: a daily data dump (catalog + full ATF file `cdliatf_unblocked.atf`) via the downloads page and the GitHub repository `github.com/cdli-gh/data` (~135,200 transliterated texts / ~3.5M lines), plus a no-auth CC0 publications API.

**At-scale quantitative use — verified example.** Eric L. Cripps (Liverpool), "The Structure of Prices in the neo-Sumerian Economy (I): Barley:Silver Price Ratios," *Cuneiform Digital Library Journal* 2017/2 (also CDL Preprint 7): extracted 157 attestations of barley:silver price ratios from approximately **60,000–70,000 transliterated Ur III administrative texts in the CDLI database**, each text identified by year date, provenance, and siglum. Follow-ups: "The Structure of Prices in the Neo-Sumerian Economy (II): the Wool:Silver Price Ratio" (*AfO* 113); "The Structure of Prices in the Ur III Economy: Cults and Prices at the Collapse of the Ur III State," *JCS* 71 (2019), 53–76 — both working from Ur III balanced accounts. (All VERIFIED.)

### Structured databases of Ur III administrative texts

**BDTNS** (Base de Datos de Textos Neo-Sumerios; Manuel Molina, CSIC Madrid; online since 2002; `bdtns.cesga.es`). VERIFIED via its own about page (May 2026): **105,187 texts**; 70,063 published with transliteration; **1,350,035 lines of transliteration**; 28,608 seal inscriptions; 142,123 bibliographic references; 888 collections in 49 countries. Provenance: Umma/region 35.4%, Girsu 31.2%, Puzriš-Dagan (Drehem) 18.0%, Ur 5.0%, Nippur 3.8%, Irisagrig 3.2%, GARšana 1.8%. BDTNS is a scholarly query interface with cleaner metadata than CDLI (Molina curates provenance, dates, bibliography), not a bulk-download API.

**ORACC** (Open Richly Annotated Cuneiform Corpus; UPenn umbrella). Its Ur III corpus is **~72,000 documents**, imported from CDLI and **cleaned and lemmatized by Niek Veldhuis (Berkeley) and Steve Tinney (UPenn)** (VERIFIED — Anderson, Kulikov & Veldhuis, IDEAH 2021). Lemmatization is ORACC's comparative advantage (BDTNS and CDLI are not lemmatized). JSON access via the ORACC API.

### The Sumerian Network project (Veldhuis / Anderson, Berkeley, 2017–2021)

PI Niek Veldhuis with Mellon postdoctoral fellow **Adam G. Anderson** (VERIFIED — Berkeley CDSS/BIDS, IDEAH 2021, GitHub). Goal: **reproducible socio-economic networks from the Ur III archives**, beginning with **~15,000 transliterated Drehem (Puzriš-Dagan) texts**. Methods: atomized network graphs of named entities (roles, titles) over social, institutional, geographical, and temporal substrates; statistical measurement of micro-economic transactions; and **novel computational methods for name disambiguation** — "in the absence of 'gold-standard' data, we built an atomized network based on name instances in textual attestations," enabling "progress toward **unsupervised disambiguation of the Ur III prosopography**."

Outputs: open Jupyter Notebooks (`github.com/niekveldhuis/Sumerian-network`), Gephi network files (`github.com/admndrsn/gephi`), a JupyterBook (`niekveldhuis.github.io/sumnet`). Key publication: Anderson, Kulikov & Veldhuis, "Sumerian Networks: Classifying Text Groups in the Drehem Archives," *IDEAH*, July 28, 2021 — which also gives the three-corpus comparison table (BDTNS = Ur III only, no lemmatization; CDLI = all cuneiform, no lemmatization; ORACC = project-based, lemmatized).

**Critical distinction:** this is the nearest thing to Ur III entity resolution, but its product is **networks of name instances, not a resolved transaction ledger.**

### Prior work on ledgers, entity resolution, conservation checks, network analysis

**Stated plainly: no published project builds a unified computational ledger with entity resolution and conservation (inflow = outflow) checks over the Ur III archives.** The closest work does pieces of the puzzle, on different corpora or without the accounting layer:

**(a) Consolidated transaction ledger across archives.** *None found.* Englund (2004) discusses ancient account-consolidation techniques (e.g., Jemdet Nasr accounts MSVO 1, 212–214 as "accounting transfer without any gaps"), and Nissen, Damerow & Englund (1993) describe scribes checking actual against theoretical amounts — but this is philological analysis of ancient practice, not a modern computational ledger. No modern project consolidates transactions across the dispersed Ur III archives.

**(b) Computational entity resolution / prosopography at scale.**
- Sumerian Network (Veldhuis/Anderson) — unsupervised name disambiguation across ~15,000 Drehem texts (above).
- Anderson, A. (2019), "Disambiguating the Old Assyrian Social Networks Using NLP and Network Theory" — supervised and unsupervised disambiguation of homonymous individuals across ~5,000 Kültepe texts, Old Assyrian period (1950–1750 BCE). Methodologically the template for Ur III work, but a different corpus.
- Liu, Luo, Hearne & Burkhart: "Unsupervised Sumerian Personal Name Recognition" (FLAIRS 2015); "Enhancing Sumerian Lemmatization by Unsupervised Named-Entity Recognition" (NAACL-HLT 2015); Liu, Hearne & Conrad, "Recognizing Proper Names in UR III Texts through Supervised Learning" (FLAIRS 2016). These are named-entity *recognition* (finding names), not entity *resolution* (same person?).
- Ueda, Tsuchiya & Itoh (2023), "Computational Dating for the Nuzi Cuneiform Archive: The Least Squares Constrained by Family Trees and Synchronisms," arXiv:2308.12883 — family trees from a Nuzi personal-names index, name-ambiguity solved, dating as constrained least-squares. Nuzi (15th–14th c.), not Ur III; aimed at dating, not accounting.
- Klein, Romach & Gordin (2026), "In Search of Lost Time — Estimating Dates of Broken Cuneiform Documents," Research Square preprint — network-based prosopographic dating of ~949 Neo-Babylonian/Achaemenid tablets via the Prosobab prosopography. First-millennium corpus, not Ur III.
- Traditional (manual) Ur III prosopography: Dahl, J.L. (2007), *The Ruling Family of Ur III Umma*, PIHANS 108 — not computational.

**(c) Flow/conservation analysis (inflows vs. outflows; missing-tablet detection).** *None found for Ur III.* A 2024 Cambridge Accelerate Programme project (with Assyriologist Jonathan Tenney) applied data science to Middle Babylonian tablets — name-based clustering, date prediction, metadata repair — and its write-up explicitly names **"detection of missing tablets" as an ongoing challenge, not a solved result**. The ancient scribes themselves performed actual-vs.-expected checks (Nissen et al. 1993), but no modern study runs conservation checks across the digital Ur III corpus.

**(d) Network analysis of officials/institutions.** Sumerian Network (Drehem); Anderson on Old Assyrian Kültepe; Michalowski, "Networks of Authority and Power in Ur III Times" (in Garfinkle & Molina 2013) is traditional historical analysis, not computational. Klein et al. (2026) note cuneiform social-network analysis "has been growing rapidly," but the cited applications are mostly first-millennium prosopographic networks.

### Venues and conference literature

- **CDLI's own publications** — CDLJ, CDLB, CDLP (`cdli.earth`): Cripps 2017 (CDLJ 2017/2, price ratios); Englund 2004 (numerical analysis of archaic accounts); CDLB 2023/4 survey of OCR/NLP on cuneiform.
- ***Archeologia e Calcolatori***: Di Filippo, Maiocchi, Milano & Orsini (2018), "A digital project on the Ebla archives," vol. 29, pp. 117–142 (VERIFIED) — conceptual-schema database of Ebla tablets with sign-level token modeling. Ebla (3rd millennium), not Ur III, but the closest published computational database design for a cuneiform archive.
- **IDEAH**: Anderson, Kulikov & Veldhuis 2021 (Sumerian Networks Drehem work).
- **The data-mining chapter — VERIFIED**: Alessandro Di Ludovico, "Symbols and Bureaucratic Performances in the Ur III Administrative Sphere: An Interpretation Through Data Mining," in Garfinkle & Molina (eds.), *From the 21st Century B.C. to the 21st Century A.D.: Proceedings of the International Conference on Neo-Sumerian Studies held in Madrid, 22–24 July 2010*, Winona Lake: Eisenbrauns, 2013, pp. 125–152 (ISBN 978-1-57506-296-9). Confirmed via the publisher's table of contents, library catalog, and De Gruyter Brill frontmatter. *Caveat:* methodological detail (what "data mining" denotes there) not recovered.
- **Workshops**: Pacific Northwest Regional NLP Workshop (Liu et al. 2014, Sumerian NER); VarDial 2019 shared task on cuneiform language/dialect identification; EACL/COLING 2020 ("Towards the First Machine Translation System for Sumerian Transliterations," MTAAC Ur III data); FLAIRS 2015/2016 (Sumerian NER).
- **The *Journal of Computer Applications in Archaeology* (JCAA): no cuneiform/Sumerian papers located in search** — the actual homes for computational cuneiform work are CDLI publications, IDEAH, *Archeologia e Calcolatori*, and NLP venues, not JCAA.

### Machine learning / NLP on cuneiform (2020+)

- Gordin et al. (2020), "Reading Akkadian cuneiform using natural language processing," *PLOS ONE*. VERIFIED.
- Dencker, Klinkisch, Maul & Ommer (2020), "Deep learning of cuneiform sign detection with weak supervision using transliteration alignment," *PLOS ONE*. VERIFIED — sign detector trained from transliterations only, Neo-Assyrian.
- Gutherz, Gordin, Sáenz, Levy & Berant (2023), "Translating Akkadian to English with neural machine translation," *PNAS Nexus* 2(5), pgad096. VERIFIED.
- Kapon, Fire & Gordin (2024), arXiv:2406.04039 — deep-learning classification of tablet shape over 94,936 CDLI images (ResNet50, macro-F1 71%).
- Jauhiainen et al. (2019) — language/dialect identification over 13,662 ORACC tablets (VarDial shared task).
- SumTablets (2026, arXiv:2602.22200) — HuggingFace transliteration dataset: 82,452 train / 4,577 val / 4,577 test, of which 71,116 train are Ur III administrative texts. VERIFIED.
- Chiarcos, Khait, Pagé-Perron, Schenk et al. (2018), "Annotating a Low-Resource Language with LLOD Technology: Sumerian Morphology and Syntax," *Information* 9(11), p. 290 (MDPI). VERIFIED — the MTAAC annotation pipeline.
- Pagé-Perron et al. (2020), "Towards the First Machine Translation System for Sumerian Transliterations," *Proc. COLING*. VERIFIED.
- *Unverified/partially checked:* "Neural Machine Translation of Old Assyrian Cuneiform Business Records into English" (Research Square preprint; Old Assyrian, not Ur III); Iraqi-journal survey pieces on CNN sign classification (uneven quality — cite with care); Veldhuis's **COMPASS (2024)** — cited in SumTablets for cuneiform social-graph reconstruction but the name is confounded by unrelated ML projects; treat as unverified pending direct access to Veldhuis's repository.

### Verification status of key claims

| Claim | Status |
|---|---|
| CDLI leadership (Englund/UCLA, Renn/MPIWG; Dahl, Lafont, Pagé-Perron co-PIs) | Verified (Wikipedia, NYCDH, Berkeley news) |
| CDLI bulk ATF data publicly downloadable (GitHub cdli-gh/data) | Verified (COMPASS docs, multiple GitHub audits) |
| BDTNS = Molina/CSIC, ~105K texts, 1.35M transliterated lines, provenance stats | Verified (bdtns.cesga.es about page, May 2026) |
| ORACC Ur III corpus ~72K docs, lemmatized by Veldhuis & Tinney | Verified (IDEAH 2021) |
| Sumerian Network = Veldhuis/Anderson, ~15K Drehem texts, unsupervised name disambiguation, open notebooks | Verified (Berkeley CDSS/BIDS, IDEAH 2021, GitHub) |
| Di Ludovico data-mining chapter, Madrid 2010 proceedings, Eisenbrauns 2013 | Verified (publisher, catalog, De Gruyter) |
| Cripps price-ratio study mined ~60–70K CDLI Ur III texts | Verified (CDLJ 2017/2, CDLP 7) |
| JCAA publishes computational-cuneiform work | Not found — no JCAA cuneiform papers located |
| Any unified computational ledger + entity resolution + conservation checks over Ur III | **None found — appears to be a genuine gap** |

---

## Gaps and Opportunities

### 1. The core gap: a consolidated, entity-resolved, conservation-checked ledger

No one has merged the Ur III archives into one transaction ledger, performed global entity resolution across it, or validated flows with conservation checks. The nearest efforts do one piece each: Tsouparopoulou (offices, not numbers), Sumerian Network (names, not transactions), Cripps (prices, not books), Mattessich (theory, not the corpus). **A unified Drehem/Umma/Girsu ledger with entity resolution and no-negative-balance validation would be methodologically novel** — and the first end-to-end test of the ancient system's own internal consistency.

### 2. Testing Hallo's double-entry hypothesis

Hallo (2004, "Bookkeeping in the Twenty-First Century BCE," PARTIALLY VERIFIED) argued for something like double-entry in Ur III tablets. A full transaction ledger is the instrument that could test this — systematically, across tens of thousands of tablets, rather than by philological example.

### 3. The deliverer-kept-receipt mechanism, quantified

Widell (2020) documents that *šu ba-ti* receipts were sealed by the receiving official and kept by the deliverer. The Drehem-ledger project's observed ~48% livestock inflow/outflow asymmetry is the first opportunity to test whether this archival mechanism can quantitatively explain the gap. No published work connects the receipt mechanism to aggregate flow statistics.

### 4. Counterpart-document reconciliation across archives

Charles's design goal — matching transactions across Drehem, Umma, and Girsu by date, commodity, quantity, direction, and parties — has no published precedent. Sharlach (2004) did interarchival synthesis of the *bala* system, but as institutional analysis, not transaction-level reconciliation. A provenance-bearing match table with confidence scores would be new.

### 5. Temples as economic entities — the sociology-of-religion paper

Ezzamel (2005) on Egyptian funerary-temple endowment contracts is the model: measured resource allocation to gods, enforced by contract and norm. No equivalent exists for Ur III: which divine institutions received what, and did allocation reflect local city gods, theological hierarchy, political patronage, or administrative geography? A divine-recipient parser over the Drehem outflow/offering records would be the first quantitative "who got fed" analysis.

### 6. Aztec tribute codices as accounting

Rich, standardized, quantified, scribe-audited imperial revenue records — and no accounting-history scholarship treats them as accounting systems. A comparative paper (Ur III vs. Aztec vs. Inca quipu vs. Persepolis) on ancient state revenue accounting would fill a genuine comparative gap.

### 7. Venue strategy

The *Accounting Historians Journal* has published Ezzamel (2002), Mattessich (1987, 1998), Mouck (2004), Vollmers (2009), and Yeakel (1983) — the method paper belongs there first, as planned. CDLJ/CDLB is the natural home for the data and corpus papers. JNES/JCS for historical implications after the method is validated. **JCAA is not currently a home for cuneiform computational work** — submit elsewhere.

### 8. Corrected framing points

- **Yamey is not an origins figure** — do not cite him for Mesopotamian accounting origins.
- **Veldhuis is not primarily an accounting-systems scholar** — his documented profile is lexical/digital infrastructure and computational text analysis (Sumerian Network aside). Verify via his academia.edu page before citing him as an accounting-systems authority.
- **The Widell 2020 receipts passage** is fully citable (*Orient* 55, DOI 10.5356/orient.55.117) but the exact full-text passage was not retrievable this session (abstract-only page; PDF fetch timed out).
- **COMPASS (2024)** — cited in SumTablets for cuneiform social-graph reconstruction but confounded by unrelated ML projects; unverified pending direct access to Veldhuis's repository.
- **Stevens (2006), *Temples, Tithes, and Taxes*** — check a catalog record before citing; details came from a publisher blurb mirrored on a piracy site.
- **Cambridge thesis on the Jerusalem Temple economy** (repository.cam.ac.uk) — author/year not established; do not cite yet.
- **Guo's "Confucius and Accounting"** — the translation circulates online; the original appeared in the Chinese journal *Finance and Accounting*; do not cite a Western venue without checking.

---

## Bibliography

*Consolidated from all three research passes; deduped. Markers: [V] = verified this session; [P] = partially verified (cited in reliable secondary sources, details not independently confirmed).*

### Ur III / Mesopotamian administration and accounting

- Adams, R. McC. (2012). "Shepherds at Umma in the Third Dynasty of Ur." *JESHO* 49/2: 133–169. [V]
- al-Mutawalli, N., Sallaberger, W. & Shalkham, A. U. (2017). "The Cuneiform Documents from the Iraqi Excavation at Drehem." *ZA* 107/2: 151–217. [V]
- Dahl, J. L. (2007). *The Ruling Family of Ur III Umma*. PIHANS 108. Leiden: NINO. [V]
- Dahl, J. L. (2020). *Ur III Texts in the Schøyen Collection*. CUSAS 39. Eisenbrauns. [V]
- Englund, R. K. (1988). "Administrative Timekeeping in Ancient Mesopotamia." *JESHO* 31/2: 121–185. [V]
- Englund, R. K. (1990). *Organisation und Verwaltung der Ur III-Fischerei*. BBVO 10. Berlin: Dietrich Reimer. [V]
- Englund, R. K. (1991). "Hard Work — Where Will It Get You? Labor Management in Ur III Mesopotamia." *JNES* 50/4: 255–280. [V]
- Englund, R. K. (1992). "Ur III Sundries." *Acta Sumerologica* 14: 77–102. [V]
- Englund, R. K. (1995). "Regulating Dairy Productivity in the Ur III Period." *Orientalia* 64/4: 377–429. [V]
- Englund, R. K. (2003). "Worcester Slaughterhouse Account." *CDLB* 2003/1. [V]
- Englund, R. K. (2004). "Proto-Cuneiform Account-Books and Journals." In M. Hudson & C. Wunsch (eds.), *Creating Economic Order*, CDL Press, pp. 23–46. [V]
- Garfinkle, S. J. (2004). "Shepherds, Merchants, and Credit: Some Observations on Lending Practices in Ur III Mesopotamia." *JESHO* 47/1: 1–30. [V]
- Garfinkle, S. J. (2008). "Was the Ur III State Bureaucratic? Patrimonialism and Bureaucracy in the Ur III Period." In Garfinkle & Johnson (eds.), *The Growth of an Early State in Mesopotamia*, Madrid: CSIC, pp. 55–61. [V]
- Garfinkle, S. J. (2012). *Entrepreneurs and Enterprise in Early Mesopotamia*. CUSAS. Bethesda: CDL Press. [V]
- Garfinkle, S. J. (2013). "The Third Dynasty of Ur and the Limits of State Power in Early Mesopotamia." In Garfinkle & Molina (eds.), *From the 21st Century B.C. to the 21st Century A.D.*, Eisenbrauns, pp. 153–168. [V]
- Garfinkle, S. J. (2015). "Family Firms in the Ur III Period." In A. Archi (ed.), *Tradition and Innovation in the Ancient Near East* (57th RAI), Eisenbrauns, pp. 517–524. [V]
- Garfinkle, S. J. (2015). "Ur III Administrative Texts: Building Blocks of State Community." In P. Delnero & J. Lauinger (eds.), *Texts and Contexts*, SANER 9, De Gruyter, pp. 143–165. [V]
- Garfinkle, S. J. (2020). "The House of Ursaga: Ur III Merchants in Their Non-Institutional Context." In J. Mas & P. Notizia (eds.), *Working at Home in the Ancient Near East*, Archaeopress, pp. 71–81. [V]
- Garfinkle, S. J. & Molina, M. (eds.) (2013). *From the 21st Century B.C. to the 21st Century A.D.: Proceedings of the International Conference on Neo-Sumerian Studies held in Madrid, 22–24 July 2010.* Winona Lake: Eisenbrauns. ISBN 978-1-57506-296-9. [V]
- Hallo, W. W. (2004). "Bookkeeping in the Twenty-First Century BCE." In M. Hudson & C. Wunsch (eds.), *Creating Economic Order*, Vol. IV. [P]
- Hilgert, M. (1993). *Drehem Administrative Documents from the Reign of Amar-Suena*. OIP 121. Chicago: Oriental Institute. [V]
- Jones, T. B. & Snyder, J. W. (1961). *Sumerian Economic Texts from the Third Ur Dynasty*. Minneapolis: University of Minnesota Press. [V]
- Liu Changyu (2017). *Organization, Administrative Practices and Written Documentation in Mesopotamia during the Ur III Period (c. 2112–2004 BC): A Case Study of Puzriš-Dagan in the Reign of Amar-Suen*. KEF 3. Münster: Ugarit-Verlag. [V]
- Mattessich, R. (1998). "Recent Insights into Mesopotamian Accounting of the 3rd Millennium BC: Successor to Token Accounting." *AHJ* 25/1: 1–27. (Correction: 25/2: 147–149.) [V]
- Mattessich, R. (2000). *The Beginnings of Accounting and Accounting Thought*. New York: Garland. [V]
- Michalowski, P. (ed.) (2008). *On the Third Dynasty of Ur: Studies in Honor of Marcel Sigrist*. JCS SS1. Boston. [V]
- Molina, M. (2008). "The Corpus of Neo-Sumerian Tablets: An Overview." In Garfinkle & Johnson (eds.), *The Growth of an Early State in Mesopotamia*, Madrid: CSIC. [P — pages not verified]
- Molina, M. (2010). "Court Records From Umma." In A. Kleinerman & J. M. Sasson (eds.), *Why Should Someone Who Knows Something Conceal It?* (Owen FS), CDL Press, pp. 201–217. [V]
- Molina, M. (2013). "On the Location of Irisaĝrig." In Garfinkle & Molina (eds.), *From the 21st Century B.C. to the 21st Century A.D.*, Eisenbrauns, pp. 59–87. [V]
- Molina, M. (2014). "Court Officials at Umma in Ur III Times." *ZA* 103/2: 125–148. [V]
- Mouck, T. (2004). "Ancient Mesopotamian Accounting and Human Cognitive Evolution." *AHJ* 31/2: 97–124. [V]
- Nissen, H. J., Damerow, P. & Englund, R. K. (1993). *Archaic Bookkeeping: Early Writing and Techniques of Economic Administration in the Ancient Near East*. Chicago: University of Chicago Press. [V]
- Notizia, P. (2009). *I testi dei messaggeri da Girsu-Lagaš della Terza Dinastia di Ur*. Nisaba 22. Messina. [V]
- Owen, D. I. (ed.) (2013). *Cuneiform Texts Primarily from Iri-Saĝrig/Āl-Šarrākī and the History of the Ur III Period*. Nisaba 15. Bethesda: CDL Press. [V]
- Sallaberger, W. (1993). *Der kultische Kalender der Ur III-Zeit*. UAVA 7/1. Berlin: De Gruyter. [V]
- Sallaberger, W. (1999). "Ur III-Zeit." In J. Bauer, R. K. Englund & M. Krebernik (eds.), *Mesopotamien: Akkade-Zeit und Ur III-Zeit*, OBO 160/3, Freiburg: Universitätsverlag. [V]
- Sharlach, T. M. (2004). *Provincial Taxation and the Ur III State*. Cuneiform Monographs 26. Leiden: Brill. [V]
- Sigrist, M. (1992). *Drehem*. Bethesda: CDL Press. [V]
- Steinkeller, P. (1982). "On Editing Ur III Economic Texts." *JAOS* 102/4: 639–644. [V]
- Steinkeller, P. (1987). "The Administrative and Economic Organization of the Ur III State: The Core and the Periphery." In McG. Gibson & R. D. Biggs (eds.), *The Organization of Power*, SAOC 46, Chicago: Oriental Institute, pp. 15–33. [V]
- Steinkeller, P. (1995). "Sheep and Goat Terminology in Ur III Sources from Drehem." *BSA* 8: 49–70. [V]
- Steinkeller, P. (2001). "New Light on the Hydrology and Topography of Southern Babylonia in the Third Millennium." *ZA* 91/1: 22–84. [V]
- Steinkeller, P. (2002). "Money-Lending Practices in Ur III Babylonia: the Issue of Economic Motivation." In M. Hudson & M. van de Mieroop (eds.), *Debt and Economic Renewal in the Ancient Near East*, CDL Press, pp. 109–137. [V]
- Steinkeller, P. (2004). "Toward a Definition of Private Economic Activity in Third Millennium Babylonia." In R. Rollinger & C. Ulf (eds.), *Commerce and Monetary Systems in the Ancient World*, Melammu Symposia 5, Stuttgart: Franz Steiner, pp. 91–111. [V]
- Stępień, M. (1996). *Animal Husbandry in the Ancient Near East: A Prosopographic Study of Third-Millennium Umma*. Bethesda: CDL Press. [V]
- Tsouparopoulou, C. (2013). "A Reconstruction of the Puzriš-Dagan Central Livestock Agency." *CDLJ* 2013/2. https://cdli.earth/articles/cdlj/2013-2 [V]
- Tsouparopoulou, C. (2013). "Killing and Skinning Animals in the Ur III Period." *AoF* 40/1: 150–182. [V]
- Tsouparopoulou, C. (2015). *The Ur III Seals Impressed on Documents from Puzriš-Dagān (Drehem)*. Heidelberg: Heidelberger Orientverlag. [V]
- Tsouparopoulou, C. (2017). "'Counter-Archaeology': Putting the Ur III Drehem Archives Back in the Ground." In Y. Heffron, A. Stone & M. Worthington (eds.), *At the Dawn of History*, Eisenbrauns, pp. 611–629. [V]
- Van De Mieroop, M. (1999/2000). "An Accountant's Nightmare: the Drafting of a Year's Summary." *AfO* 46/47: 111–129. [V]
- Waetzoldt, H. & Sigrist, M. (1993). "Haftung mit Privatvermögen bei Nichterfüllung von Dienstverpflichtungen." In M. E. Cohen, D. C. Snell & D. B. Weisberg (eds.), *The Tablet and the Scroll* (Hallo FS), CDL Press, pp. 271–280. [V]
- Widell, M. (2003). *The Administrative and Economic Ur III Texts from the City of Ur*. Piscataway: Gorgias Press. [V]
- Widell, M. (2008). "The Ur III Metal Loans from Ur." In Garfinkle & Johnson (eds.), *The Growth of an Early State in Mesopotamia*, pp. 207–223. [V]
- Widell, M. (2009). "Two Ur III Texts from Umma: Observations on Archival Practices and Household Management." *CDLJ* 2009/6. [V]
- Widell, M. (2018). "The Administration of Storage in Early Babylonia." *Orient* 53: 23–34. [V]
- Widell, M. (2020). "Ur III Economy and Bureaucracy: The Neo-Sumerian Cuneiform Tablets in the Hood Museum of Art, Dartmouth College (I)." *Orient* 55: 117–154. DOI 10.5356/orient.55.117. [V]
- Widell, M. (2020). "Destined for Slaughter: Identifying Seasonal Breeding Patterns in Sheep and Goats in Early Babylonia." *JNES* 79/2: 209–223. DOI 10.1086/710168. [V]
- Widell, M. (2026). *Administration and Economy in Early Babylonian Society*. Oxford: Oxford University Press. [V]
- Wilcke, C. (2005). "The Liability of Superiors for Deficits of their Subordinates." *NABU* 2005/3: no. 74. [V]
- Wu Yuhong (1996). "The Ewes Without Lambs and Lambs Cooked in é-uz-ga." *Journal of Ancient Civilizations* 11: 65–109. [V]

### History of accounting / comparative ancient accounting

- Carmona, S. & Ezzamel, M. (2007). "Accounting and accountability in ancient civilizations: Mesopotamia and ancient Egypt." *Accounting, Auditing & Accountability Journal* 20(2), 177–209. [V]
- Carmona, S. & Ezzamel, M. (2008). "Ancient accounting." In Edwards, R. & Walker, S.P. (eds.), *The Routledge Companion of Accounting History*, pp. 73–94. [V]
- Ezzamel, M. (2002). "Accounting and redistribution: The palace and mortuary cult in the Middle Kingdom, ancient Egypt." *AHJ* 29(1). [V]
- Ezzamel, M. (2002). "Accounting for Private Estates and the Household in the Twentieth Century BC Middle Kingdom, Ancient Egypt." *Abacus* 38(2), 235–262. [V]
- Ezzamel, M. (2004). "Work Organization in the Middle Kingdom, Ancient Egypt." *Organization* 11(4), 497–537. [V]
- Ezzamel, M. (2005). "Accounting for the Practices of Funerary Temples: The Intertwining of the Sacred and the Profane." *Accounting and Business Research* 35(1), 29–51. [V]
- Ezzamel, M. (2014). *Accounting and Order*. Routledge (Routledge Studies in Accounting). [V]
- Ezzamel, M. & Hoskin, K. (2002). "Retheorizing Accounting, Writing and Money with Evidence from Mesopotamia and Ancient Egypt." *Critical Perspectives on Accounting* 13(3), 333–367. [V]
- Fu, P. (1971). "Governmental Accounting in China during the Chao [Zhou] Dynasty (1122 B.C.-256 B.C.)." *Journal of Accounting Research* 9 (Spring 1971), 40–51. [V]
- Guo, D. (1982, 1988). *Sketches on the History of Accounting in China*, Vols. 1–2 (in Chinese). Beijing: China Financial and Economic Publishing House. [V]
- Haring, B.J.J. (1997). *Divine Households: Administrative and Economic Aspects of the New Kingdom Royal Memorial Temples in Western Thebes*. Leiden: NINO (Egyptologische Uitgaven 12). [V]
- Janssen, J.J. (1975). *Commodity Prices from the Ramessid Period*. Brill. [P]
- Janssen, J.J. (1975). "Prolegomena to the study of Egypt's economic history during the New Kingdom." *SAK* 3, 127–185. [P]
- Janssen, J.J. (1979). "The Role of the Temple in the Egyptian Economy During the New Kingdom." In Lipiński, E. (ed.), *State and Temple Economy in the Ancient Near East*, Vol. 2, Leuven, p. 509. [V]
- Mattessich, R. (1987). "Prehistoric accounting and the problem of representation." *AHJ* 14(2), 71–91. [V]
- Mattessich, R. (1989). "Accounting and the input-output principle in the ancient and prehistoric world." *Abacus* 25(2), 74–84. [V]
- Mattessich, R. (1994). "Archaeology of Accounting and Schmandt-Besserat's Contribution." *Accounting, Business & Financial History* 4(1), 5–28. [V]
- Sangster, A. (2021). "Basil Yamey (1919–2020): A Reflection on His Contribution to Accounting History." *AHJ* 48(1), 67–. [V — cited here as a corrective: Yamey is NOT a Mesopotamian-origins figure]
- Urton, G. & Brezine, C.J. (2005). "Khipu Accounting in Ancient Peru." *Science* (12 Aug 2005). [V]
- Urton, G. & Chu, A. (2015). "Accounting in the King's Storehouse: The Inkawasi Khipu Archive." *Latin American Antiquity* 26(4), 512–529. [V]
- Urton, G. (2003). *Signs of the Inka Khipu: Binary Coding in the Andean Knotted-String Records*. University of Texas Press. [V]
- Urton, G. (2017). *Inka History in Knots: Reading Khipus as Primary Sources*. University of Texas Press. [V]
- Vollmers, G.L. (2009). "Accounting and Control in the Persepolis Fortification Tablets." *AHJ* 36(2), 93–111. [V]
- Vollmers, G. (1996). "The Persepolis Fortification Texts: Accounting and Control in Ancient Persia from 509 to 494 B.C." *Accounting Enquiries* 6(1), 1–43. [P]
- Yadav, N. et al. (2019). "Interrogating Indus inscriptions to unravel their mechanisms of meaning conveyance." *Humanities and Social Sciences Communications*. [V]
- Yeakel, J.A. (1983). "The Accountant-Historians of the Incas." *AHJ* 10(2), Art. 3. [V]

### Computational / digital cuneiform

- Anderson, A. (2019). "Disambiguating the Old Assyrian Social Networks Using NLP and Network Theory." ResearchGate preprint. [V]
- Anderson, A. G., Kulikov, A. & Veldhuis, N. (2021). "Sumerian Networks: Classifying Text Groups in the Drehem Archives." *IDEAH*, July 28, 2021. [V]
- Chiarcos, C., Khait, I., Pagé-Perron, É., Schenk, N. et al. (2018). "Annotating a Low-Resource Language with LLOD Technology: Sumerian Morphology and Syntax." *Information* 9(11), p. 290 (MDPI). [V]
- Cripps, E. L. (2017). "The Structure of Prices in the neo-Sumerian Economy (I): Barley:Silver Price Ratios." *CDLJ* 2017/2; also CDL Preprint 7. [V]
- Cripps, E. L. "The Structure of Prices in the Neo-Sumerian Economy (II): the Wool:Silver Price Ratio." *AfO* 113. [V]
- Cripps, E. L. (2019). "The Structure of Prices in the Ur III Economy: Cults and Prices at the Collapse of the Ur III State." *JCS* 71, 53–76. [V]
- Dencker, T., Klinkisch, P., Maul, S. M. & Ommer, B. (2020). "Deep learning of cuneiform sign detection with weak supervision using transliteration alignment." *PLOS ONE*, Dec 16, 2020. [V]
- Di Filippo, F., Maiocchi, M., Milano, L. & Orsini, R. (2018). "A digital project on the Ebla archives." *Archeologia e Calcolatori* 29, 117–142. [V]
- Di Ludovico, A. (2013). "Symbols and Bureaucratic Performances in the Ur III Administrative Sphere: An Interpretation Through Data Mining." In Garfinkle & Molina (eds.), *From the 21st Century B.C. to the 21st Century A.D.*, Eisenbrauns, pp. 125–152. [V]
- Gordin, S. et al. (2020). "Reading Akkadian cuneiform using natural language processing." *PLOS ONE*. [V]
- Gutherz, G., Gordin, S., Sáenz, L., Levy, O. & Berant, J. (2023). "Translating Akkadian to English with neural machine translation." *PNAS Nexus* 2(5), pgad096. [V]
- Jauhiainen, T. et al. (2019). Language/dialect identification over 13,662 ORACC tablets (VarDial shared task). [V]
- Kapon, Fire & Gordin (2024). Deep-learning classification of cuneiform tablet shapes from CDLI imagery. arXiv:2406.04039. [V]
- Klein, S., Romach, A. & Gordin, S. (2026). "In Search of Lost Time — Estimating Dates of Broken Cuneiform Documents." Research Square preprint. DOI 10.21203/rs.3.rs-9033722/v1. [V]
- Liu, Y., Burkhart, C., Hearne, J. & Luo, L. (2015). "Enhancing Sumerian Lemmatization by Unsupervised Named-Entity Recognition." *Proc. NAACL-HLT* 2015, 1446–1451. [V]
- Liu, Y., Hearne, J. & Conrad, B. (2016). "Recognizing Proper Names in UR III Texts through Supervised Learning." *Proc. FLAIRS* 2016, 535–540. [V]
- Luo, L., Liu, Y., Hearne, J. & Burkhart, C. (2015). "Unsupervised Sumerian Personal Name Recognition." *Proc. FLAIRS* 2015, 193–198. [V]
- Pagé-Perron, É. et al. (2020). "Towards the First Machine Translation System for Sumerian Transliterations." *Proc. COLING* 2020. [V]
- SumTablets (2026). HuggingFace transliteration dataset. arXiv:2602.22200. [V]
- Ueda, S., Tsuchiya, T. & Itoh, Y. (2023). "Computational Dating for the Nuzi Cuneiform Archive." arXiv:2308.12883. [V]
- Veldhuis, N. (2021). Sumerian Networks JupyterBook. https://niekveldhuis.github.io/sumnet/welcome.html; notebooks: https://github.com/niekveldhuis/Sumerian-network [V]

---

*End of review. Research compiled 2026-10-09 by three parallel research passes. Items marked [V] verified this session; [P] partially verified; flagged items (Stevens 2006, COMPASS 2024, Cambridge thesis, Guo's "Confucius and Accounting" venue, CDL Umma-merchant preprint) should be checked against primary sources before citation.*
