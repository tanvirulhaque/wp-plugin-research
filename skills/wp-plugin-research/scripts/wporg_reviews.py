#!/usr/bin/env python3
"""
wordpress.org reviews by star rating (rung 2): list pages → topic links → first post.

Usage:
  python wporg_reviews.py SLUG [SLUG...] --stars 1,2 [--newest5 5] [--pages 2] [--out raw/rev/wporg-reviews.json]

--stars 1,2   read 1- and 2-star reviews (pain evidence)
--newest5 N   also read the N newest 5-star reviews (what users value; support praise)
Captures the full date (with year), title, rating and the first post's text.
Star rating: read from the review page when possible; otherwise taken from the
?filter=N list it came from (stars_source = "page" or "filter" — both are exact).
Paraphrase before using any text in reports. Polite: ~1 s between requests.
"""
import argparse, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import get

BASE = "https://wordpress.org/support/plugin/{slug}/reviews/"

def text(s):
    s = re.sub(r"<br\s*/?>|</p>", "\n", s, flags=re.I)
    return html.unescape(re.sub(r"[ \t]+", " ", re.sub(r"<[^>]+>", "", s))).strip()

def topic_links(slug, stars, pages):
    links = []
    for page in range(1, pages + 1):
        url = BASE.format(slug=slug) + (f"page/{page}/" if page > 1 else "") + f"?filter={stars}"
        h = get(url)
        if not h:
            break
        found = re.findall(r'<a[^>]*class="bbp-topic-permalink"[^>]*href="([^"]+)"', h) or \
                re.findall(r'href="(https://wordpress\.org/support/topic/[^"/]+/)"', h)
        new = [u for u in dict.fromkeys(found) if u not in links]
        if not new:
            break
        links += new
    return links

def first_post(url):
    h = get(url)
    if not h:
        return None
    title = re.search(r'<h1[^>]*class="page-title"[^>]*>(.*?)</h1>', h, re.S) or re.search(r"<title>(.*?)</title>", h, re.S)
    rating = (re.search(r'wporg-ratings[^>]*data-rating="(\d)"', h)
              or re.search(r'data-rating="(\d)"[^>]*wporg-ratings', h)
              or re.search(r'(?:aria-label|title)="(\d)(?:\.\d)? out of 5 stars"', h)
              or re.search(r'Rating:\s*(\d) out of 5', h))
    date = re.search(r'<time[^>]*datetime="([^"]+)"', h) or re.search(r'title="([A-Z][a-z]+ \d{1,2}, \d{4}[^"]*)"', h)
    body = re.search(r'<div class="bbp-topic-content">(.*?)</div>\s*(?:<!-- \.bbp-topic-content -->|<div class="bbp)', h, re.S) or \
           re.search(r'<div class="bbp-topic-content">(.*?)</div>', h, re.S)
    return {"url": url, "title": text(title.group(1)) if title else "",
            "stars": int(rating.group(1)) if rating else None, "stars_source": "page" if rating else "",
            "date": date.group(1) if date else "", "text": text(body.group(1))[:3000] if body else ""}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="+")
    ap.add_argument("--stars", default="1,2")
    ap.add_argument("--newest5", type=int, default=0)
    ap.add_argument("--pages", type=int, default=2)
    ap.add_argument("--out", default="raw/rev/wporg-reviews.json")
    a = ap.parse_args()
    rows = []
    for slug in a.slugs:
        for s in [int(x) for x in a.stars.split(",") if x.strip()]:
            for u in topic_links(slug, s, a.pages):
                r = first_post(u)
                if r:
                    if r["stars"] is None: r["stars"], r["stars_source"] = s, "filter"
                    rows.append({"slug": slug, "filter": s, **r})
        if a.newest5:
            for u in topic_links(slug, 5, 1)[: a.newest5]:
                r = first_post(u)
                if r:
                    if r["stars"] is None: r["stars"], r["stars_source"] = 5, "filter"
                    rows.append({"slug": slug, "filter": 5, **r})
        print(f"{slug}: {sum(1 for r in rows if r['slug'] == slug)} reviews")
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(rows, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"Saved {len(rows)} reviews → {a.out}")
    if rows and all(not r["text"] for r in rows):
        print("Self-check: no review text parsed — wordpress.org markup may have changed.")

if __name__ == "__main__":
    main()
