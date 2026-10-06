"""Dated port visits for sanctioned vessels from the Global Fishing Watch API (needs GFW_TOKEN).

GFW data is CC BY-NC 4.0 (non-commercial use only)."""
import csv, json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw/gfw"
OUT = ROOT / "data/gfw_port_visits.csv"
API = "https://gateway.api.globalfishingwatch.org/v3"
TOKEN = os.environ["GFW_TOKEN"]


def get(path, params):
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(6):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": "iran-sanctions-enablers/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(5 * (attempt + 1))
                continue
            raise
        except Exception:
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(url)


def valid_imo(imo):
    return len(imo) == 7 and imo.isdigit() and imo[0] != "0" and sum(int(c) * (7 - i) for i, c in enumerate(imo[:6])) % 10 == int(imo[6])


def imo_list():
    imos = {}
    with open(ROOT / "data/gur_ships.csv") as fh:
        for r in csv.DictReader(fh):
            imos[r["imo"]] = {"name": r["ofac_name"], "ofac_date": r["ofac_date"], "programs": r["programs"]}
    with open(ROOT / "data/iran_nodes.csv") as fh:
        for r in csv.DictReader(fh):
            for imo in filter(None, (r.get("imo") or "").replace("IMO", "").replace(" ", "").split(";")):
                if valid_imo(imo) and r.get("iran_sanctioned") in ("1", "True", "true"):
                    imos.setdefault(imo, {"name": r["name"], "ofac_date": "", "programs": r["programs"]})
    with open(ROOT / "data/vessel_designation_dates.csv") as fh:
        for r in csv.DictReader(fh):
            if valid_imo(r["imo"]):
                imos.setdefault(r["imo"], {"name": "", "ofac_date": r["first_us_iran_designation"], "programs": "US-IRAN"})
    return imos


def fetch(imo):
    f = RAW / f"{imo}.json"
    if f.exists():
        return json.loads(f.read_text())
    s = get("vessels/search", {"query": imo, "datasets[0]": "public-global-vessel-identity:latest"})
    ids = []
    for e in s.get("entries", []):
        for si in e.get("selfReportedInfo", []):
            if si.get("imo") == imo or any(r.get("imo") == imo for r in e.get("registryInfo", [])):
                ids.append(si["id"])
    visits = []
    if ids:
        params = {f"vessels[{i}]": v for i, v in enumerate(ids)}
        params.update({"datasets[0]": "public-global-port-visits-events:latest",
                       "start-date": "2017-01-01", "end-date": time.strftime("%Y-%m-%d"), "limit": 99999, "offset": 0})
        visits = get("events", params).get("entries", [])
    d = {"imo": imo, "vessel_ids": ids, "visits": visits}
    f.write_text(json.dumps(d))
    return d


def main():
    imos = imo_list()
    print(len(imos), "IMOs", flush=True)
    rows = []
    for n, (imo, meta) in enumerate(sorted(imos.items())):
        try:
            d = fetch(imo)
        except Exception as e:
            print("fail", imo, e, flush=True)
            continue
        for v in d["visits"]:
            pv = v.get("port_visit", {})
            a = pv.get("intermediateAnchorage") or pv.get("startAnchorage") or {}
            rows.append({"imo": imo, "ofac_name": meta["name"], "ofac_date": meta["ofac_date"], "programs": meta["programs"],
                         "ais_name": v["vessel"].get("name"), "mmsi": v["vessel"].get("ssvid"), "start": v["start"][:19],
                         "end": v["end"][:19], "hours": round(pv.get("durationHrs") or 0, 1), "port_id": a.get("id"),
                         "anchorage_id": a.get("anchorageId"), "anchorage": a.get("name"), "country": a.get("flag"),
                         "at_dock": a.get("atDock"), "lat": a.get("lat"), "lon": a.get("lon"),
                         "confidence": pv.get("confidence")})
        if n % 25 == 0:
            print(n, imo, len(d["vessel_ids"]), len(d["visits"]), flush=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("rows", len(rows))


if __name__ == "__main__":
    main()
