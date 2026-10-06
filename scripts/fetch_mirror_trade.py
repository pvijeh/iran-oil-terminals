"""UN Comtrade mirror check: crude oil (HS 2709) China says it imported from X vs what X says it exported to China."""
import csv, time, pathlib, requests
ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTNERS = {"458": "Malaysia", "360": "Indonesia", "784": "UAE", "512": "Oman", "364": "Iran"}
rows = []
def get(rep, par, yr, flow):
    for _ in range(5):
        r = requests.get("https://comtradeapi.un.org/public/v1/preview/C/A/HS", timeout=60,
                         params={"reporterCode": rep, "partnerCode": par, "period": yr, "cmdCode": "2709", "flowCode": flow})
        if r.ok and "data" in r.json():
            d = r.json()["data"]; return (d[0]["primaryValue"], d[0].get("netWgt")) if d else (0, 0)
        time.sleep(8)
    return (None, None)
for code, name in PARTNERS.items():
    for yr in range(2015, 2026):
        cn = get("156", code, yr, "M"); time.sleep(3)
        px = get(code, "156", yr, "X") if code != "364" else (None, None); time.sleep(3)
        rows.append({"partner": name, "year": yr, "china_reported_imports_usd": cn[0], "china_reported_kg": cn[1],
                     "partner_reported_exports_usd": px[0], "partner_reported_kg": px[1]})
        print(rows[-1], flush=True)
with (ROOT / "data/mirror_trade_crude.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
