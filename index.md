---
title: Two Hong Kong-listed companies own sanctioned Chinese oil terminals, and free ship tracking can't show which terminal is next
---

## Executive summary

- **What this is:** a check, using only public data, of which stock-market-listed companies own or supply businesses tied to Iran getting around US sanctions.
- **Why it matters:** Iran keeps selling oil to China despite US sanctions. Since March 2025 the US has punished Chinese oil terminals that unload it, one terminal at a time. If a listed company owns the next terminal hit, its profit and share price take the damage.
- **Where we looked:**
  - US sanctions lists (OFAC, OpenSanctions).
  - Company filings in Hong Kong and mainland China, to match each sanctioned terminal to its owner.
  - Ship-tracking records: 220,000 port visits by 669 sanctioned ships, from Global Fishing Watch.
  - Ukraine's database of parts found in Iranian drones.
- **What we found:**
  - **Two Hong Kong-listed companies own terminals already hit:** Sinopec Kantons (00934), which lost a terminal that made about 12% of its 2024 pre-tax profit, and Qingdao Port (06198).
  - **Tracking can't predict the next one:** once sanctioned, tankers stop showing up at Chinese crude piers, most likely because they switch off their location signal.
  - **One exception:** seven sanctioned gas carriers still dock openly at Chaozhou, in southern China. We haven't confirmed who owns that pier.
  - **Drone parts:** parts from 10 listed companies, 4 in Taiwan, were found in Iranian drones. Nothing shows the makers knew.
- **Still open:** which terminal is taking the oil now. That needs paid cargo-tracking data or satellite images.

**What "sanctioned" means here:** listed by the US Treasury's Office of Foreign Assets Control (OFAC) under its Iran programs. These are US measures; buying Iranian oil is not illegal under Chinese law. This page is research, not investment advice.

## The terminals already hit, and who owns them

**Sinopec Kantons (HKEX 00934): 50% of Rizhao Shihua, sanctioned 2025-10-09**

- **Liquidation:** Rizhao Shihua is being shut down. Its piers and tanks were sold for about RMB 2.41bn to buyers Kantons describes only as "independent third parties" ([liquidation notice](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0227/2026022702200.pdf)).
- **Cost:** Kantons expects a loss of about HK$127M from the liquidation ([profit warning](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0727/2026072700602.pdf)). First-half 2026 profit was HK$386M, down 31% from HK$563M a year earlier ([interim report](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0817/2026081701721.pdf)).
- **Still exposed:** it owns half of the main crude terminals at Qingdao and Ningbo, which are not sanctioned.
- **Unnamed customer:** its wholly owned Huizhou terminal, Huade, unloaded 1.21M tonnes of crude for a "third-party customer" in the first half of 2026, more than double a year earlier. We could not identify the customer.

**Qingdao Port (HKEX 06198, SSE 601298): 70% of Dongjiakou, sanctioned**

- **Not disclosed:** its 2026 interim report does not mention the Dongjiakou sanction ([report](http://static.cninfo.com.cn/finalpage/2026-08-29/1225524260.PDF)).
- **Deal cancelled:** on 2025-12-12 it cancelled a RMB 1.79bn purchase of half of Rizhao Shihua, citing the US listing ([announcement](http://static.cninfo.com.cn/finalpage/2025-12-12/1224871861.PDF)).

**Smaller or mainland-only exposure**

- **PetroChina (HKEX 00857):** owns about 21% of the sanctioned Yangshan Shengang depot in Shanghai, a small part of its business.
- **Wintime Energy (SSE 600157):** owns 80% of the sanctioned Huaying Huizhou terminal.
- **Hengli Petrochemical (SSE 600346):** owns the sanctioned Hengli Dalian refinery.
- **Sources:** every link is in [listed_company_links.csv](data/listed_company_links.csv), with the filing behind it.

## Sanctioned tankers disappear from the tracking data

**How we checked:** we looked up 737 ships on OFAC's Iran lists in [Global Fishing Watch](https://globalfishingwatch.org/), which records port visits from ships' location signals. It had 669 of them.

**What it shows:** before their sanctions, hundreds called at China's big crude ports. After, almost none did.

| Port | Ships seen before their sanction (since 2017) | Seen after, last 12 months | Tied up at a pier after |
|---|---|---|---|
| Ningbo | 271 | 7 | 0 |
| Qingdao | 157 | 0 | 0 |
| Dongjiakou | 135 | 1 | 0 |
| Rizhao | 78 | 0 | 0 |
| Tianjin, Caofeidian, Huizhou, Zhanjiang | 51 to 67 each | 0 | 0 |
| Chaozhou (Jinshiwan) | 29 | 7 | 7 |

**Why that doesn't mean the oil stopped:**

- Sanctioned tankers can switch off their location signal before going in.
- Or they pass the oil at sea to an unsanctioned ship, which docks instead.
- So this data can't show which crude terminal is taking the cargoes now.

**Where sanctioned tankers still show up (last 12 months, mostly at anchorages, not piers):**

| Country | Sanctioned tankers seen |
|---|---|
| UAE | 204 |
| China (mostly anchorages off Zhuhai, Shanghai and Hong Kong) | 76 |
| Iraq | 62 |
| India | 59 |
| Taiwan | 0 (149 before their sanctions) |

- **Taiwan:** no Taiwan-listed company or subsidiary is on OFAC's Iran lists.
- **Iran's cargo ships behave the same way:** of 160 sanctioned container ships, bulk carriers and general-cargo ships, 65 were seen in Chinese waters in the last 12 months. Only 3 tied up at a pier, each at a different port (Shanghai, Nantong, Taicang). They dock openly at Iranian ports and at Jebel Ali in Dubai.

## Chaozhou: the one place sanctioned ships still dock openly

- **What happened:** seven sanctioned ships tied up at a pier in Chaozhou's Jinshiwan port area, Guangdong, between 2025-10-27 and 2026-07-22. Each stayed one to three days, all after their sanction dates.
- **Cargo:** most are gas carriers, including Cape Gas and Sapphire Gas, so the cargo was probably liquefied petroleum gas (LPG) rather than crude.
- **Nearby terminals:** Chaozhou Asia-Pacific Fuel Storage, Ouhua Energy and a Huaying LNG terminal. The Huaying terminal shares a name with the sanctioned Huaying Huizhou terminal, but we found no ownership link between them.
- **Not confirmed:** which terminal the ships used, who owns it, and whether the gas came from Iran.

## Listed companies whose parts were found in Iranian drones

**Source:** Ukraine's military intelligence (GUR) takes apart Iranian-designed Shahed and Geran drones shot down over Ukraine. It publishes each part's maker in its [components database](https://war-sanctions.gur.gov.ua/en/components). This is a separate question from the oil terminals.

**Listed makers we matched:**

- **Taiwan:** Delta Electronics (2308), Winbond Electronics (2344), Kaimei Electronic (2375, Jamicon capacitors) and PANJIT International (2481).
- **Taiwan, not matched to a listing:** Molicel, Minmax, Fotek, Oupiin, NAK and VBsemi.
- **Hong Kong:** Man Yue Technology (HKEX 00894), a capacitor maker.
- **Shanghai and Shenzhen:** GigaDevice (603986), Shanghai Belling (600171), Yangjie Technology (300373), Hongfa (600885, Xiamen Hongfa relays) and Aihua (603989).

**What this does and doesn't show:**

- These are chips, capacitors, relays, diodes and power supplies sold in the millions through distributors.
- A part in a drone shows someone bought it, usually through resellers. It does not show the maker sold to Iran or knew.
- None of these companies is on OFAC's Iran lists.

## What would show which terminal is next

1. **Chaozhou's pier:** match the seven visits to one berth, find who holds its port operating licence, and trace that owner to a listed parent.
2. **A paid cargo tracker:** Kpler and Vortexa estimate where dark tankers unload, using satellite images and port agents. Kpler costs about $55,000 a year according to [Vendr](https://www.vendr.com/marketplace/kpler). Their terminal-level figures, matched against the owners above, would show which listed companies still handle Iranian crude.
3. **Free radar satellite images:** the EU's [Sentinel-1](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1) satellites photograph these coasts every few days, at night and through cloud. A large tanker at the Qingdao, Ningbo or Huizhou crude piers with no location signal is hiding where it is.
4. **Rizhao's buyers and Huade's customer:** Chinese company registries such as Qichacha, and Shandong Port Group's bond filings, may name who bought Rizhao Shihua's assets and who is behind Huade's extra crude.

**Our view:** Kantons is the listed company most exposed to the next terminal sanction, because it owns half of the crude piers at Qingdao and Ningbo where sanctioned tankers used to call. Free data cannot say whether those piers are still taking Iranian oil. A paid tracker or satellite images can, and that is the test worth running before anyone acts on this.

## Data

Every table behind this page is in [data/](https://github.com/pvijeh/iran-oil-terminals/tree/main/data), with its source and licence. The scripts that built them are in [scripts/](https://github.com/pvijeh/iran-oil-terminals/tree/main/scripts).

- **Sanctions:** [OFAC recent actions](https://ofac.treasury.gov/recent-actions) and [OpenSanctions](https://www.opensanctions.org/).
- **Port visits:** [Global Fishing Watch](https://globalfishingwatch.org/), under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) (non-commercial use only).
- **Tanker histories and drone parts:** [Ukraine GUR](https://war-sanctions.gur.gov.ua/en/transport/ships).
- **Company links:** the HKEX and [cninfo](http://www.cninfo.com.cn/) filings linked above.
