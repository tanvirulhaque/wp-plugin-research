#!/usr/bin/env python3
"""
Parse saved old.reddit.com THREAD pages (rung 4): post + comments.

Usage: python parse_reddit_thread.py DIR_OR_FILES... [--out threads.json] [--max-comments 40]
Markup: post title a.title · post body/comments div.usertext-body div.md ·
comment score span.score[title] · time[datetime].
The first div.md is usually the post body (empty for link posts).
Standard library only. Paraphrase before quoting anything in reports.
"""
import argparse, glob, html, json, os, re

def text(s):
    s = re.sub(r"<br\s*/?>|</p>", "\n", s, flags=re.I)
    return html.unescape(re.sub(r"[ \t]+", " ", re.sub(r"<[^>]+>", "", s))).strip()

def parse(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    title = re.search(r'<a[^>]*class="[^"]*\btitle\b[^"]*"[^>]*>(.*?)</a>', raw, re.S | re.I)
    canon = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', raw, re.I)
    times = re.findall(r'<time[^>]*datetime="([^"]+)"', raw, re.I)
    mds = re.findall(r'<div[^>]*class="[^"]*\busertext-body\b[^"]*"[^>]*>\s*<div[^>]*class="md"[^>]*>(.*?)</div>\s*</div>', raw, re.S | re.I)
    scores = [int(s) for s in re.findall(r'<span[^>]*class="[^"]*\bscore unvoted\b[^"]*"[^>]*title="(-?\d+)"', raw, re.I)]
    bodies = [text(m) for m in mds]
    return {
        "title": text(title.group(1)) if title else "",
        "url": canon.group(1) if canon else "",
        "date": times[0][:10] if times else "",
        "post": bodies[0][:3000] if bodies else "",
        "comments": [{"score": scores[i] if i < len(scores) else None, "text": b[:1500]}
                     for i, b in enumerate(bodies[1:])],
        "file": os.path.basename(path),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", default="reddit-threads.json")
    ap.add_argument("--max-comments", type=int, default=40)
    a = ap.parse_args()
    files = []
    for p in a.paths:
        files += sorted(glob.glob(os.path.join(p, "*.html"))) if os.path.isdir(p) else [p]
    out = []
    for f in files:
        t = parse(f); t["comments"] = t["comments"][: a.max_comments]; out.append(t)
    json.dump({"threads": len(out), "rows": out}, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(out)} threads, {sum(len(t['comments']) for t in out)} comments → {a.out}")
    empty = [t["file"] for t in out if not t["title"]]
    if empty:
        print("Self-check: no title found in", empty[:5], "— check the markup.")

if __name__ == "__main__":
    main()
