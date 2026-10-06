"""Count distinct sanctioned vessels visiting each Chinese anchorage after their first US designation."""
import csv, collections, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
dates = {r["imo"]: r["first_us_iran_designation"] for r in csv.DictReader(open(ROOT / "data/vessel_designation_dates.csv"))}
cutoff = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
agg = collections.defaultdict(lambda: {"post": set(), "post_12m": set(), "dock_12m": set(), "visits_12m": 0, "lat": [], "lon": [], "port_id": "", "name": ""})
for r in csv.DictReader(open(ROOT / "data/gfw_port_visits.csv")):
    d = dates.get(r["imo"])
    if r["country"] != "CHN" or not d or r["start"][:10] < d:
        continue
    a = agg[r["anchorage_id"]]
    a["post"].add(r["imo"]); a["port_id"] = r["port_id"]; a["name"] = r["anchorage"]
    a["lat"].append(float(r["lat"])); a["lon"].append(float(r["lon"]))
    if r["start"][:10] >= cutoff:
        a["post_12m"].add(r["imo"]); a["visits_12m"] += 1
        if r["at_dock"] == "True":
            a["dock_12m"].add(r["imo"])
rows = []
for k, a in agg.items():
    rows.append({"anchorage_id": k, "port_id": a["port_id"], "anchorage": a["name"],
                 "lat": round(sum(a["lat"]) / len(a["lat"]), 4), "lon": round(sum(a["lon"]) / len(a["lon"]), 4),
                 "ships_post_designation": len(a["post"]), "ships_post_designation_12m": len(a["post_12m"]),
                 "ships_at_dock_12m": len(a["dock_12m"]), "visits_12m": a["visits_12m"],
                 "imos_12m": ";".join(sorted(a["post_12m"]))})
rows.sort(key=lambda r: (-r["ships_post_designation_12m"], -r["ships_post_designation"]))
with open(ROOT / "data/gfw_china_post_designation.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows[:40]:
    print(r["port_id"], r["anchorage"], r["lat"], r["lon"], r["ships_post_designation"], r["ships_post_designation_12m"], r["ships_at_dock_12m"])
