# Data

Every table behind the report. Counts of ships are counts of different IMO numbers (a ship's permanent ID).

- `listed_company_links.csv`: sanctioned terminals, depots and refineries matched to listed parent companies, with stake, evidence level and the filing that shows the link. Evidence levels: **proven** (a sanctioned subsidiary), **documented** (a filing or registry shows the link), **lead** (needs checking).
- `ofac_iran_designations.csv`: entities OFAC designated under its Iran programs, parsed from [OFAC recent actions](https://ofac.treasury.gov/recent-actions), with Chinese business registration numbers (USCC) where OFAC lists them. US government data, public domain.
- `vessel_designation_dates.csv`: first US Iran-related designation date for each ship, from OFAC recent actions and [OpenSanctions](https://www.opensanctions.org/) (CC BY-NC 4.0).
- `gfw_ports_summary.csv`, `gfw_countries_summary.csv`, `gfw_china_post_designation.csv`: port visits by sanctioned ships, summarised per port, per country and per Chinese anchorage. "Before" means before the ship's sanction date; "after_12m" means after it, in the 12 months to 2026-10-06; "at_dock" means tied up at a pier. Derived from [Global Fishing Watch](https://globalfishingwatch.org/) port-visit events, [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): non-commercial use only, with credit.
- `gur_ships.csv`, `gur_prc_port_calls.csv`: owners, managers, former names and undated port areas for sanctioned tankers, from Ukraine's military intelligence (GUR) [War & Sanctions site](https://war-sanctions.gur.gov.ua/en/transport/ships).
- `gur_iran_drone_component_makers.csv`: makers of parts found in Iranian-designed Shahed and Geran drones, from GUR's [components database](https://war-sanctions.gur.gov.ua/en/components).
- `mirror_trade_crude.csv`: crude trade as reported by China and by each partner country, from [UN Comtrade](https://comtradeplus.un.org/).

Not included: the 220,000 individual Global Fishing Watch port visits. Its licence bars commercial use, and a public copy can't enforce that. Rebuild it with `scripts/fetch_gfw_port_visits.py` and a free [GFW API token](https://globalfishingwatch.org/our-apis/tokens) (set `GFW_TOKEN`), then run `scripts/summarize_gfw_port_visits.py`.

## ofac_enforcement_iran.csv

OFAC civil penalties and settlements, 2018 to 2025, whose enforcement notice mentions Iran. `mentions_itsr` is true when the notice cites the Iranian Transactions and Sanctions Regulations (56 of the 60 rows). Source: https://ofac.treasury.gov/civil-penalties-and-enforcement-information (US government work, public domain).

## iran_enforcement_price_impact.csv

US Iran-related fines, export bans, sanctions and indictments against listed companies or their subsidiaries, 2009 to 2026, with the share price change after each one minus the local index change: first trading day, 5 and 20 trading days. Asian stocks are measured from that day's close, because US announcements come after Asian markets close. Days with no trading (halts) are skipped. The events are in `price_impact_events.csv`. Credit Suisse and SCG have no price data. Prices: Yahoo Finance. Built with `scripts/price_impact.py`.

## eu_exports_to_iran.csv

EU exports to Iran in euros, by reporting country (2023 to 2025, all goods) and by two-digit HS product chapter (2025, for the EU total, Germany, Italy and the Netherlands). Source: Eurostat Comext dataset DS-045409, reused under the Eurostat copyright notice (free reuse with credit).

## bank_actions_events.csv / bank_actions_price_impact.csv

Non-Chinese banks named in US Iran actions (sanctions, cut-offs from US correspondent accounts, criminal cases, fines not already in `iran_enforcement_price_impact.csv`), with whether each is listed and, for listed ones, the share change minus the local index change after 1, 5 and 20 trading days, measured from the announcement-day close (weekend news from the prior close). Prices: Yahoo Finance, and the Moscow Exchange ISS API for VTB. Iraqi banks trade on the Iraq Stock Exchange, which has no free price feed. Built with `scripts/bank_price_impact.py`.
