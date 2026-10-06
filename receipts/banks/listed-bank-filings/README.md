# Listed non-Chinese banks: Iran exposure screen (retrieved 2026-10-06)

**What this is:** a first-pass screen of stock-listed banks outside mainland China that could face US sanctions or loss of US-dollar access over Iranian money, after OFAC's 2026-10-05 warning that foreign banks dealing with sanctioned Iranian banks can be sanctioned without notice (EO 13902 / EO 13224).

**Files:** `banks.csv` (one row per bank: listing, ticker, market cap in local currency, evidence level, source, receipt). `INDEX.md` lists every receipt with URL and retrieval date.

**Evidence levels:** proven = a US authority acted against the bank; documented = official record, court record, the bank's own filing, or published list names it; lead = news, NGO or inference. Nothing here claims any bank broke the law.

**What we found**
- Proven (US action): Banque Misr UAE (FinCEN proposed cut-off, unlisted branch), Golden Global (OFAC, unlisted), VTB (OFAC, MOEX-listed, Russia), Halkbank (DOJ deferred prosecution Mar 2026, case dismissed Jun 2026; listed HALKB).
- Documented: HSBC's own 20-F (FY2025) discloses ~14 legacy guarantees involving Bank Tejarat, Bank Melli, Bank of Industry and Mine, being wound down. UCO Bank's CEO says it still runs sanctions-compliant rupee trade with Iranian banks (Jul 2026).
- Iraq: press-published lists of banks barred from US-dollar transactions: 14 in July 2023 (Shafaq, Reuters via Wayback), 8 in Feb 2024 (The New Arab), 5 more in Feb 2025 (IraqiNews). The US did not publish the names itself. Al Janoob Islamic Bank (tied to PM Al-Zaidi) still banned per Treasury, Jul 2026.
- Leads only: other Turkish (Borsa Istanbul) and UAE (DFM/ADX) listed banks, Omani banks, Kaspi. Jurisdiction-level risk; no bank-specific Iran evidence found in the time box.

**Market caps:** from stockanalysis.com quote pages (screenshots `mcap_*`), in local currency, retrieved 2026-10-06. Not converted to USD.

**What failed / not done**
- Annual reports and KAP disclosures for Turkish banks were not read (time box). UAE bank annual reports not read.
- Iraq Stock Exchange site (isx-iq.net) refused connections, so ISX listing of the barred Iraqi banks is not verified.
- Reuters blocks direct capture; Wayback snapshot used for the 2023-07-28 Reuters article (see INDEX.md).
- Telegraph HSBC/StanChart story is paywalled; only headline captured.
- Not screened: Halyk, Bank of Georgia, TBC, Armenian, Kyrgyz (other than Keremet), Qatar, Pakistan, Afghanistan, Lebanon banks; Ziraat, Denizbank, Kuveyt Turk, Turkiye Finans, Aktif.
- Browser crash mid-run stopped HKEX market-cap captures (HSBC, StanChart, BOC HK).
