#!/usr/bin/env python3
"""
Rebuild research.json safely from raw collector output + hand-edited overrides.

Usage:
  python merge_research.py [--rows raw/rows] [--overrides overrides.json] [--out research.json] [--base FILE]

Pattern from a real run (5 safe re-runs): collectors write raw files; findings you
add by hand live in overrides.json; this script merges them, so re-running a
collector never wipes your judgment calls.

  --base       starting file (default: assets/research-template.json — a clean rebuild every time,
               so re-running is idempotent; only point it at research.json for a one-off append)
  --rows DIR   every *.json in DIR: {"section": [rows...]} (e.g. {"reviews": [...]}) — appended
  --overrides  JSON with the same keys as research.json. Lists of rows are merged BY ID
               (override wins field by field); other keys replace the base value.

Stable IDs: any review without an id gets "R-" + 6 hex chars of hash(url + date),
so inserting rows never shifts existing evidence IDs. Other sections get the next
free number in their prefix (P, PN, G, B, S, F) only when the id is missing.
"""
import argparse, glob, hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PREFIX = {"plugins": "P", "pains": "PN", "gaps": "G", "benefits": "B", "sources": "S", "feature_set": "F"}

def stable_review_id(r):
    key = (r.get("url", "") + "|" + str(r.get("date", "")) + "|" + r.get("summary", "")[:40]).encode()
    return "R-" + hashlib.sha1(key).hexdigest()[:6]

def ensure_ids(section, rows, existing=()):
    """Give missing ids. `existing` = rows already in research.json, so new ids never collide."""
    used = {r.get("id") for r in list(rows) + list(existing) if r.get("id")}
    n = 0
    for r in rows:
        if r.get("id"):
            continue
        if section == "reviews":
            r["id"] = stable_review_id(r)
        elif section in PREFIX:
            while True:
                n += 1
                cand = f"{PREFIX[section]}{n:02d}"
                if cand not in used:
                    break
            r["id"] = cand
        used.add(r.get("id"))
    return rows

def merge_rows(base, extra):
    by = {r.get("id"): dict(r) for r in base if r.get("id")}
    order = [r.get("id") for r in base]
    loose = [r for r in base if not r.get("id")]
    for r in extra:
        i = r.get("id")
        if i and i in by:
            by[i].update(r)
        elif i:
            by[i] = dict(r); order.append(i)
        else:
            loose.append(r)
    return [by[i] for i in order if i in by] + loose

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="")
    ap.add_argument("--rows", default="raw/rows")
    ap.add_argument("--overrides", default="overrides.json")
    ap.add_argument("--out", default="research.json")
    a = ap.parse_args()
    base_path = a.base or os.path.join(HERE, "..", "assets", "research-template.json")
    data = json.load(open(base_path, encoding="utf-8"))
    added = {}
    for f in sorted(glob.glob(os.path.join(a.rows, "*.json"))):
        chunk = json.load(open(f, encoding="utf-8"))
        for sec, rows in chunk.items():
            if isinstance(rows, list):
                rows = ensure_ids(sec, [dict(r) for r in rows], data.get(sec, []))
                data[sec] = merge_rows(data.get(sec, []), rows)
                added[sec] = added.get(sec, 0) + len(rows)
    if os.path.exists(a.overrides):
        ov = json.load(open(a.overrides, encoding="utf-8"))
        for k, v in ov.items():
            if isinstance(v, list) and v and isinstance(v[0], dict) and isinstance(data.get(k), list):
                data[k] = merge_rows(data[k], ensure_ids(k, [dict(r) for r in v], data[k]))
            else:
                data[k] = v
    for sec in list(PREFIX) + ["reviews"]:
        if isinstance(data.get(sec), list):
            ensure_ids(sec, data[sec])
    json.dump(data, open(a.out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Merged from {os.path.basename(base_path)}: " + (", ".join(f"{k} +{v}" for k, v in added.items()) or "no row files") +
          (" + overrides" if os.path.exists(a.overrides) else "") + f" → {a.out}")

if __name__ == "__main__":
    main()
