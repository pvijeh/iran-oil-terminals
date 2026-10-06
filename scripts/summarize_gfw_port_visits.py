"""Summarize Global Fishing Watch port visits by sanctioned tankers, per port and per country.

Input: data/gfw_port_visits.csv (not published; rebuild with fetch_gfw_port_visits.py and a GFW token).
Counts are of different ships (IMO numbers). "Before" = any visit before the ship's first US Iran
designation; "after_12m" = visits on or after that date within 365 days of AS_OF.
"""
import csv, collections, datetime, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AS_OF = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date(2026, 10, 6)
cutoff = (AS_OF - datetime.timedelta(days=365)).isoformat()
dates = {r["imo"]: r["first_us_iran_designation"]
         for r in csv.DictReader(open(ROOT / "data/vessel_designation_dates.csv"))}


def new():
    return {"before": set(), "after_12m": set(), "after_12m_at_dock": set()}


ports, countries = collections.defaultdict(new), collections.defaultdict(new)
for r in csv.DictReader(open(ROOT / "data/gfw_port_visits.csv")):
    d = dates.get(r["imo"])
    if not d:
        continue
    day = r["start"][:10]
    for agg in (ports[(r["country"], r["port_id"])], countries[r["country"]]):
        if day < d:
            agg["before"].add(r["imo"])
        elif day >= cutoff:
            agg["after_12m"].add(r["imo"])
            if r["at_dock"] == "True":
                agg["after_12m_at_dock"].add(r["imo"])


def write(path, key_fields, agg):
    rows = [dict(zip(key_fields, k if isinstance(k, tuple) else (k,)),
                 ships_before=len(a["before"]), ships_after_12m=len(a["after_12m"]),
                 ships_after_12m_at_dock=len(a["after_12m_at_dock"]))
            for k, a in agg.items()]
    rows.sort(key=lambda r: (-r["ships_after_12m"], -r["ships_before"]))
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


write(ROOT / "data/gfw_ports_summary.csv", ["country", "port_id"], ports)
for r in write(ROOT / "data/gfw_countries_summary.csv", ["country"], countries)[:15]:
    print(r)
