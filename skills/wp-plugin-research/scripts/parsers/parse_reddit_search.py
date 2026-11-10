#!/usr/bin/env python3
"""
Parse saved old.reddit.com SEARCH pages (rung 4) and filter for relevance.

Usage:
  python parse_reddit_search.py DIR_OR_FILES... --core video \
      --context "product,store,shop,woocommerce,gallery" [--out results.json]

Reads every .html file given (or in a folder). Old-Reddit markup:
  div.search-result-link[data-fullname] · a.search-title · time[datetime]
  .search-score · .search-comments · .search-subreddit-link
Relevance (Reddit search is loose): keep rows whose TITLE contains a --core word
AND whose title or snippet contains a --context word. Prints the funnel
(raw → unique → relevant) so it can go in the coverage checklist.
Standard library only.
"""
import argparse, glob, html, json, os, re, sys

BLOCK = re.compile(r'<div[^>]*class="[^"]*\bsearch-result-link\b[^"]*"[^>]*>', re.I)

def attr(tag, name):
    m = re.search(rf'{name}="([^"]*)"', tag)
    return html.unescape(m.group(1)) if m else ""

def text(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()

def parse(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    starts = [m.start() for m in BLOCK.finditer(raw)] + [len(raw)]
    rows = []
    for a, b in zip(starts, starts[1:]):
        chunk = raw[a:b]
        head = BLOCK.match(chunk).group(0)
        title_m = re.search(r'<a[^>]*class="[^"]*\bsearch-title\b[^"]*"[^>]*>(.*?)</a>', chunk, re.S | re.I)
        href_m = re.search(r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*\bsearch-title\b', chunk, re.I) or \
                 re.search(r'<a[^>]*class="[^"]*\bsearch-title\b[^"]*"[^>]*href="([^"]+)"', chunk, re.I)
        time_m = re.search(r'<time[^>]*datetime="([^"]+)"', chunk, re.I)
        score_m = re.search(r'class="[^"]*\bsearch-score\b[^"]*"[^>]*>([^<]*)<', chunk, re.I)
        com_m = re.search(r'class="[^"]*\bsearch-comments\b[^"]*"[^>]*>([^<]*)<', chunk, re.I)
        sub_m = re.search(r'class="[^"]*\bsearch-subreddit-link\b[^"]*"[^>]*>([^<]*)<', chunk, re.I)
        body_m = re.search(r'class="[^"]*\bsearch-result-body\b[^"]*"[^>]*>(.*?)</div>\s*</div>', chunk, re.S | re.I)
        num = lambda s: int(re.sub(r"[^\d]", "", s) or 0) if s else 0
        url = html.unescape(href_m.group(1)) if href_m else ""
        rows.append({
            "id": attr(head, "data-fullname"),
            "title": text(title_m.group(1)) if title_m else "",
            "url": ("https://old.reddit.com" + url) if url.startswith("/") else url,
            "date": (time_m.group(1)[:10] if time_m else ""),
            "score": num(score_m.group(1)) if score_m else 0,
            "comments": num(com_m.group(1)) if com_m else 0,
            "sub": text(sub_m.group(1)) if sub_m else "",
            "snippet": text(body_m.group(1))[:500] if body_m else "",
            "file": os.path.basename(path),
        })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--core", required=True, help="comma list; title must contain one")
    ap.add_argument("--context", default="", help="comma list; title or snippet must contain one")
    ap.add_argument("--out", default="reddit-search-results.json")
    a = ap.parse_args()
    files = []
    for p in a.paths:
        files += sorted(glob.glob(os.path.join(p, "*.html"))) if os.path.isdir(p) else [p]
    if not files:
        sys.exit("No .html files found.")
    allrows = [r for f in files for r in parse(f)]
    uniq = {}
    for r in allrows:
        uniq.setdefault(r["id"] or r["url"], r)
    core = [w.strip().lower() for w in a.core.split(",") if w.strip()]
    ctx = [w.strip().lower() for w in a.context.split(",") if w.strip()]
    keep = [r for r in uniq.values()
            if any(c in r["title"].lower() for c in core)
            and (not ctx or any(c in (r["title"] + " " + r["snippet"]).lower() for c in ctx))]
    keep.sort(key=lambda r: r["date"], reverse=True)
    json.dump({"files": len(files), "raw": len(allrows), "unique": len(uniq), "relevant": len(keep), "rows": keep},
              open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(files)} files → {len(allrows)} results → {len(uniq)} unique → {len(keep)} relevant. Saved {a.out}")
    if len(allrows) == 0:
        print("Self-check: 0 results parsed — is this old.reddit.com markup? Re-check selectors (references/collectors.md).")

if __name__ == "__main__":
    main()
