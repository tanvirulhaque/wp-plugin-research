#!/usr/bin/env python3
"""
Wide plugin discovery on wordpress.org (rung 1) + newcomer metric.

Usage:
  python wporg_discover.py --keywords "product video,video gallery,featured video" \
      --tags "product-video,video-gallery" [--pages 2] [--filter "video"] [--out raw/all_seen.json]

Searches every keyword AND every tag, PAGES pages each (100 per page), keeps every
plugin seen (with the search-result fields, including `downloaded`, which the
per-plugin endpoint lacks), then filters by a regex on name/description/tags.

Prints:
  - screened vs matched counts (for the coverage checklist)
  - newcomer metric: matched plugins added in the last 24 months, and how many passed 100 / 1,000 installs
Handles {"error": ...} responses. If api.wordpress.org is blocked, see references/sources.md (fallbacks).
"""
import argparse, datetime, json, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import get

API = "https://api.wordpress.org/plugins/info/1.2/"
FIELDS = ["active_installs", "downloaded", "rating", "num_ratings", "ratings", "last_updated", "added",
          "tested", "requires_php", "short_description", "tags", "author", "version",
          "support_threads", "support_threads_resolved"]

def query(kind, value, page):
    p = {"action": "query_plugins", f"request[{kind}]": value, "request[per_page]": 100, "request[page]": page}
    for f in FIELDS:
        p[f"request[fields][{f}]"] = 1
    return get(API + "?" + urllib.parse.urlencode(p), as_json=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keywords", default="")
    ap.add_argument("--tags", default="")
    ap.add_argument("--pages", type=int, default=2)
    ap.add_argument("--filter", default="", help="regex on name + short description + tags (case-insensitive)")
    ap.add_argument("--out", default="raw/all_seen.json")
    a = ap.parse_args()
    jobs = [("search", k.strip()) for k in a.keywords.split(",") if k.strip()] + \
           [("tag", t.strip()) for t in a.tags.split(",") if t.strip()]
    if not jobs:
        sys.exit("Give --keywords and/or --tags.")
    seen, errors = {}, []
    for kind, val in jobs:
        for page in range(1, a.pages + 1):
            j = query(kind, val, page)
            if not j or "error" in j:
                errors.append(f"{kind}={val} p{page}: {(j or {}).get('error', 'no response')}")
                break
            for p in j.get("plugins", []):
                s = p["slug"]
                row = seen.setdefault(s, {k: p.get(k) for k in ["slug", "name"] + FIELDS})
                row.setdefault("found_by", [])
                row["found_by"].append(f"{kind}:{val}")
            if page >= j.get("info", {}).get("pages", 1):
                break
        print(f"{kind}={val}: {len(seen)} plugins seen so far")
    rx = re.compile(a.filter, re.I) if a.filter else None
    def text(p):
        tags = " ".join((p.get("tags") or {}).values()) if isinstance(p.get("tags"), dict) else str(p.get("tags") or "")
        return f"{p.get('name','')} {p.get('short_description','')} {tags}"
    matched = {s: p for s, p in seen.items() if not rx or rx.search(text(p))}
    today = datetime.date.today()
    def added(p):
        try: return datetime.date.fromisoformat((p.get("added") or "")[:10])
        except ValueError: return None
    new = [p for p in matched.values() if added(p) and (today - added(p)).days <= 730]
    newcomer = {"window": "last 24 months", "count": len(new),
                "passed_100": sum(1 for p in new if (p.get("active_installs") or 0) >= 100),
                "passed_1000": sum(1 for p in new if (p.get("active_installs") or 0) >= 1000),
                "slugs": sorted(p["slug"] for p in new)}
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump({"collected": str(today), "jobs": [f"{k}:{v}" for k, v in jobs], "pages": a.pages,
               "screened": len(seen), "matched": len(matched), "filter": a.filter, "errors": errors,
               "newcomers": newcomer, "plugins": matched}, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"Screened {len(seen)} → matched {len(matched)} (filter '{a.filter}'). "
          f"Newcomers (24 mo): {newcomer['count']}, ≥100 installs: {newcomer['passed_100']}, ≥1,000: {newcomer['passed_1000']}. Saved {a.out}")
    if errors:
        print("Errors:", *errors[:5], sep="\n  ")

if __name__ == "__main__":
    main()
