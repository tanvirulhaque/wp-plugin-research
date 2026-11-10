#!/usr/bin/env python3
"""
Parse a keyword-tool export (rung 5) — Google Ads Keyword Planner CSV and similar.

Usage: python parse_keyword_csv.py export.csv [--out raw/keywords.json]
Handles Keyword Planner's UTF-16 tab-separated files and plain UTF-8 CSVs.
Looks for columns like "Keyword", "Avg. monthly searches", "Competition",
"Top of page bid (low range)" and monthly "Searches: Mon YYYY" columns.
Output: rows sorted by average monthly searches, plus a 12-month trend per keyword.
"""
import argparse, csv, io, json, os, re

def read(path):
    raw = open(path, "rb").read()
    for enc in ("utf-16", "utf-8-sig", "utf-8", "latin-1"):
        try:
            txt = raw.decode(enc)
            if "\x00" not in txt:
                break
        except UnicodeDecodeError:
            continue
    lines = txt.splitlines()
    start = next((i for i, l in enumerate(lines) if re.match(r'"?keyword"?[\t,]', l, re.I)), 0)
    body = "\n".join(lines[start:])
    delim = "\t" if body.split("\n")[0].count("\t") > body.split("\n")[0].count(",") else ","
    return list(csv.DictReader(io.StringIO(body), delimiter=delim))

def num(v):
    v = (v or "").replace(",", "").strip()
    if re.match(r"^\d+(\.\d+)?$", v): return float(v)
    m = re.match(r"^(\d+)[Kk]\s*[–-]\s*(\d+)[Kk]$", v)
    if m: return (int(m.group(1)) + int(m.group(2))) * 500.0
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--out", default="raw/keywords.json")
    a = ap.parse_args()
    rows = read(a.csv)
    if not rows:
        raise SystemExit("No rows found.")
    cols = rows[0].keys()
    kcol = next(c for c in cols if c and c.strip().lower() in ("keyword", "keywords", "query"))
    vcol = next((c for c in cols if c and "avg" in c.lower() and "search" in c.lower()), None) or \
           next((c for c in cols if c and "volume" in c.lower()), None)
    mcols = [c for c in cols if c and c.lower().startswith("searches:")]
    out = []
    for r in rows:
        out.append({"keyword": r[kcol].strip(), "avg_monthly": num(r.get(vcol)) if vcol else None,
                    "competition": r.get("Competition", r.get("competition", "")),
                    "monthly": {c.split(":", 1)[1].strip(): num(r[c]) for c in mcols}})
    out.sort(key=lambda x: -(x["avg_monthly"] or 0))
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(out)} keywords (volume column: {vcol or 'none found'}). Top: " +
          ", ".join(f"{k['keyword']} {int(k['avg_monthly'] or 0)}" for k in out[:5]) + f". Saved {a.out}")

if __name__ == "__main__":
    main()
