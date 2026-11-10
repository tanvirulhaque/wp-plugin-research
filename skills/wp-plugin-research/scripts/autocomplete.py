#!/usr/bin/env python3
"""
Google autocomplete phrasing (rung 1): how people actually type the need.

Usage: python autocomplete.py "woocommerce product video" ["seed 2" ...] [--az] [--out raw/autocomplete.json]
--az also queries "<seed> a" ... "<seed> z" (27 calls per seed, ~1 s apart).
Gives real phrasing (e.g. "... plugin free", "... without plugin") — not volumes.
"""
import argparse, json, os, string, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import get

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seeds", nargs="+")
    ap.add_argument("--az", action="store_true")
    ap.add_argument("--out", default="raw/autocomplete.json")
    a = ap.parse_args()
    out = {}
    for seed in a.seeds:
        qs = [seed] + ([f"{seed} {c}" for c in string.ascii_lowercase] if a.az else [])
        found = []
        for q in qs:
            j = get("https://suggestqueries.google.com/complete/search?client=firefox&q=" + urllib.parse.quote(q), as_json=True)
            if j and len(j) > 1:
                found += [s for s in j[1] if s not in found]
        out[seed] = found
        print(f"{seed}: {len(found)} suggestions")
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"Saved {a.out}")

if __name__ == "__main__":
    main()
