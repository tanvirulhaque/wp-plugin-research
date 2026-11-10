#!/usr/bin/env python3
"""
Support-thread title mining on wordpress.org (rung 2) — the cheapest pain ranking.

Usage:
  python wporg_threads.py SLUG [SLUG...] [--pages 3] [--themes themes.json] [--out raw/threads.json]

Reads the first PAGES pages of /support/plugin/SLUG/ (titles, links, resolved flag)
and counts themes by keyword. --themes is a JSON object {"Theme": ["word", "regex", ...]};
without it a default WooCommerce add-on map is used. Edit it per niche.
A run on 2026-11-10 got 646 titles from 9 plugins; "not showing" (207) beat "slow" (8),
which reversed an earlier assumption — so always run this before ranking pains.
"""
import argparse, html, json, os, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import get

DEFAULT_THEMES = {
    "Not showing / not working": [r"not (showing|working|displaying|appear)", r"doesn'?t (show|work)", r"missing", r"blank"],
    "Theme / builder conflict": [r"theme", r"elementor", r"divi", r"astra", r"flatsome", r"blocksy", r"kadence", r"woodmart", r"conflict"],
    "Crash / error": [r"critical error", r"fatal", r"error", r"crash", r"500"],
    "Mobile": [r"mobile", r"iphone", r"ios", r"android", r"safari"],
    "Speed": [r"slow", r"speed", r"performance", r"lcp", r"cls", r"pagespeed"],
    "Pro / license": [r"\bpro\b", r"licen[cs]e", r"premium", r"refund"],
    "Feature request": [r"feature", r"request", r"possible to", r"how (can|to)", r"option to"],
    "Update broke": [r"after update", r"since update", r"latest version", r"broke"],
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="+")
    ap.add_argument("--pages", type=int, default=3)
    ap.add_argument("--themes", default="")
    ap.add_argument("--out", default="raw/threads.json")
    a = ap.parse_args()
    themes = json.load(open(a.themes)) if a.themes else DEFAULT_THEMES
    rx = {t: re.compile("|".join(p), re.I) for t, p in themes.items()}
    rows = []
    for slug in a.slugs:
        n0 = len(rows)
        for page in range(1, a.pages + 1):
            h = get(f"https://wordpress.org/support/plugin/{slug}/" + (f"page/{page}/" if page > 1 else ""))
            if not h:
                break
            items = re.findall(r'<li[^>]*class="([^"]*)"[^>]*>\s*<div class="bbp-topic-title">.*?<a[^>]*class="bbp-topic-permalink"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', h, re.S)
            if not items:
                items = [("", u, t) for u, t in re.findall(r'<a[^>]*class="bbp-topic-permalink"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', h, re.S)]
            for cls, url, title in items:
                t = html.unescape(re.sub(r"<[^>]+>", "", title)).strip()
                rows.append({"slug": slug, "title": t, "url": url, "resolved": "resolved" in cls or "[Resolved]" in title,
                             "themes": [k for k, r in rx.items() if r.search(t)]})
        print(f"{slug}: {len(rows) - n0} titles")
    counts = Counter(t for r in rows for t in r["themes"])
    per_plugin = {s: dict(Counter(t for r in rows if r["slug"] == s for t in r["themes"])) for s in a.slugs}
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump({"titles": len(rows), "theme_counts": dict(counts.most_common()), "per_plugin": per_plugin, "rows": rows},
              open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(rows)} titles. Themes: " + ", ".join(f"{k} {v}" for k, v in counts.most_common()))
    print(f"Saved {a.out}")
    if not rows:
        print("Self-check: 0 titles — forum markup may have changed or the site is blocked (try rung 3/4).")

if __name__ == "__main__":
    main()
