"""Crawl OFAC 'Recent Actions' pages for Iran-related designations and extract
each designated entry with Chinese name and registration IDs (USCC etc.)."""
import csv, html, pathlib, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw/ofac_recent_actions"; RAW.mkdir(parents=True, exist_ok=True)
OUT = ROOT / "data/ofac_iran_designations.csv"
OUT_NEW = OUT
BASE = "https://ofac.treasury.gov"


def get(url):
    for i in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "ignore")
        except Exception:
            time.sleep(5 * (i + 1))
    return ""


def text(h):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)))


def list_actions(max_pages=120):
    acts = {}
    for p in range(max_pages):
        h = get(f"{BASE}/recent-actions?search_api_fulltext=Iran&page={p}")
        found = re.findall(r'href="(/recent-actions/\d{8}[^"]*)"[^>]*>([^<]+)<', h)
        if not found:
            break
        for u, t in found:
            if "Iran" in t:
                acts[u] = html.unescape(t)
        print("page", p, len(acts), file=sys.stderr)
    return acts


ENTRY = re.compile(r"([A-Z0-9][A-Z0-9 .,&'()\-/]{4,}?(?:LTD|LIMITED|CO|COMPANY|CORPORATION|INC|LLC|L\.L\.C|PTE|GROUP|BANK|FZE|FZCO|S\.A|JSC|DMCC)\.?,?\)?)\s*(\(Chinese (?:Simplified|Traditional): ([^)]+)\))?(.*?)\[([A-Z0-9\-, ]+)\]")


def parse(url, title):
    f = RAW / (url.strip("/").replace("/", "_") + ".html")
    if not f.exists():
        f.write_text(get(BASE + url))
    t = text(f.read_text())
    date = re.search(r"/(\d{8})", url).group(1)
    rows = []
    for m in ENTRY.finditer(t):
        body = m.group(4)
        if "Designat" in m.group(1) or len(m.group(1)) > 160:
            continue
        ids = re.findall(r"(Unified Social Credit Code \(USCC\)|Business Registration Number|Registration Number|Legal Entity Number|Identification Number IMO|Registration ID)\s+([A-Z0-9\-]+)(?: \(([^)]+)\))?", body)
        rows.append({"action_date": date, "action_url": BASE + url, "name": m.group(1).strip(" ,"),
                     "chinese_name": (m.group(3) or "").strip(), "programs": m.group(5),
                     "china": int("China" in body or "Hong Kong" in body),
                     "uscc": ";".join(v for k, v, c in ids if "USCC" in k),
                     "other_ids": ";".join(f"{k}:{v}:{c}" for k, v, c in ids if "USCC" not in k),
                     "address_excerpt": body[:300]})
    return rows


def main():
    acts = list_actions()
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda kv: parse(*kv), acts.items()))
    rows = [r for rs in res for r in rs]
    with open(OUT, "w") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("actions", len(acts), "entries", len(rows), "china", sum(r["china"] for r in rows), "uscc", sum(1 for r in rows if r["uscc"]))


if __name__ == "__main__":
    main()
