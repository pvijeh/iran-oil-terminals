"""Re-parse cached OFAC recent-action pages into one row per designated
entry (entities and individuals), splitting on the program bracket."""
import csv, html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw/ofac_recent_actions"
OUT = ROOT / "data/ofac_iran_entries.csv"


def text(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)))


rows = []
for f in sorted(RAW.glob("*.html")):
    date = re.search(r"(\d{8})", f.name).group(1)
    t = text(f.read_text())
    # entries end with "[PROGRAM...]" optionally followed by "(Linked To: ...)." ; split there
    for chunk in re.split(r"(?<=\])(?:\s*\(Linked To:[^)]*\))*\.?\s+(?=[A-Z][A-Z'\-]+[ ,])", t):
        m = re.search(r"\[([A-Z0-9\-]+(?:[ ,]+[A-Z0-9\-]+)*)\]\s*(?:\(Linked To: ([^)]*)\))?\s*\.?\s*$", chunk)
        if not m or "IRAN" not in m.group(1) and "IFSR" not in m.group(1) and "IRGC" not in m.group(1) and "SDGT" not in m.group(1) and "NPWMD" not in m.group(1):
            continue
        body = chunk[-1500:]
        # start of entry: last occurrence of an ALLCAPS name at a sentence start
        s = re.search(r"([A-Z][A-Z0-9 .,&'\-/()]{3,200}?)(?:\s\((?:Chinese|a\.k\.a|Arabic|Persian|f\.k\.a)|,\s)", body)
        name = s.group(1).strip() if s else body[:80]
        ind = "(individual)" in chunk
        zh = re.search(r"Chinese (?:Simplified|Traditional): ([^)]+)\)", body)
        ids = re.findall(r"(Unified Social Credit Code \(USCC\)|Business Registration Number|Registration Number|Legal Entity Number|National ID No\.|Passport|Identification Number IMO|Company Number|Tax ID No\.)\s+([A-Z0-9\-]+)(?: \(([^)]+)\))?", body)
        dob = re.search(r"DOB ([0-9]{2} [A-Za-z]{3} [0-9]{4}|[0-9]{4})", body)
        rows.append({"action_date": date, "action_url": "https://ofac.treasury.gov/recent-actions/" + date,
                     "type": "individual" if ind else "entity", "name": name, "chinese_name": zh.group(1).strip() if zh else "",
                     "dob": dob.group(1) if dob else "", "programs": m.group(1), "linked_to": m.group(2) or "",
                     "china_hk": int(bool(re.search(r"China|Hong Kong", body))), "taiwan": int("Taiwan" in body),
                     "ids": ";".join(f"{k}|{v}|{c}" for k, v, c in ids), "excerpt": body[:600]})
with open(OUT, "w") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), "entries;", sum(r["china_hk"] for r in rows), "china/hk;", sum(1 for r in rows if "USCC" in r["ids"]), "with USCC;",
      sum(1 for r in rows if r["chinese_name"]), "with Chinese name;", sum(1 for r in rows if r["type"] == "individual" and r["china_hk"]), "CN/HK individuals")
