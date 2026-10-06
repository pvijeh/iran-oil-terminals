"""For each OFAC Iran-action vessel IMO, pull Ukraine GUR 'War & Sanctions'
ship card: owner, commercial manager, ISM manager, former names, P&I club,
builder, visited ports. Source: https://war-sanctions.gur.gov.ua/en/transport/ships"""
import csv, html, json, pathlib, re, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw/gur_ships"; RAW.mkdir(parents=True, exist_ok=True)
OUT = ROOT / "data/gur_ships.csv"
B = "https://war-sanctions.gur.gov.ua/en/transport/ships"


def get(url):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "ignore")
        except Exception:
            time.sleep(5 * (i + 1))
    return ""


def flat(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    x = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "|", h)))
    return re.sub(r"(\|\s*)+", "|", x)


def field(x, label, stop):
    m = re.search(re.escape(label) + r"\s*\|(.*?)\|(?:" + stop + ")", x)
    return m.group(1).strip(" |") if m else ""


LABELS = ["Ship Owner (IMO / Country / Date)", "Commercial ship manager (IMO / Country / Date)",
          "Ship Safety Management Manager (IMO / Country / Date)", "Former ship names", "Flags (former)",
          "Build year", "Builder (country)", "Web Resources", "P&I Club", "Sanctions", "Visited ports", "Use Ctrl"]
STOP = "|".join(re.escape(l) for l in LABELS)

imos = {}
for r in csv.DictReader(open(ROOT / "data/ofac_iran_entries.csv")):
    for i in re.findall(r"IMO (\d{7})", r["excerpt"]):
        if re.search(r"Tanker|Vessel|vessel", r["excerpt"]):
            imos.setdefault(i, (r["name"].split(" (")[0], r["action_date"], r["programs"]))
if len(sys.argv) > 1:
    imos = dict(list(imos.items())[: int(sys.argv[1])])
rows = []
for n, (imo, (name, date, prog)) in enumerate(imos.items()):
    f = RAW / f"{imo}.html"
    if not f.exists():
        s = get(f"{B}?f%5Bsearch%5D={imo}")
        ids = []
        for m in re.finditer(r'href="https://war-sanctions\.gur\.gov\.ua/en/transport/ships/(\d+)"', s):
            if imo in s[m.start(): m.start() + 3000]:
                ids.append(m.group(1))
        page = get(f"{B}/{ids[0]}") if ids else ""
        if page and imo not in page:
            page = ""
        f.write_text(page); time.sleep(1)
    page = f.read_text()
    if not page:
        rows.append({"imo": imo, "ofac_name": name, "ofac_date": date, "programs": prog, "found": 0}); continue
    x = flat(page)
    rows.append({"imo": imo, "ofac_name": name, "ofac_date": date, "programs": prog, "found": 1,
                 "owner": field(x, LABELS[0], STOP), "commercial_manager": field(x, LABELS[1], STOP),
                 "ism_manager": field(x, LABELS[2], STOP), "former_names": field(x, LABELS[3], STOP),
                 "former_flags": field(x, LABELS[4], STOP), "build_year": field(x, LABELS[5], STOP),
                 "builder": field(x, LABELS[6], STOP), "pi_club": field(x, "P&I Club", STOP),
                 "visited_ports": field(x, "Visited ports", STOP)[:1500]})
    if n % 20 == 0:
        print(n, len(imos), sum(r["found"] for r in rows), file=sys.stderr)
keys = ["imo", "ofac_name", "ofac_date", "programs", "found", "owner", "commercial_manager", "ism_manager", "former_names",
        "former_flags", "build_year", "builder", "pi_club", "visited_ports"]
with open(OUT, "w") as fh:
    w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(rows)
print("imos", len(imos), "found", sum(r["found"] for r in rows), file=sys.stderr)
