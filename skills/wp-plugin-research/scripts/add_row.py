#!/usr/bin/env python3
"""
Append one finding to research.json (creates it from the template if missing).

Usage:
  python add_row.py research.json SECTION key=value [key=value ...]
  python add_row.py research.json SECTION --json '{"name": "...", ...}'
  python add_row.py research.json --phase 4          # mark phase 4 done
  python add_row.py research.json --set prepared=2026-11-08

SECTION: plugins, reviews, pains, gaps, benefits, sources, health, pricing,
         feature_set, demand_proxy
IDs are added automatically when missing (P01, R01, PN01, G01, B01, S01, F01).
Numbers are stored as numbers. Writing one row right after each page keeps the
research safe if the run is cut off.
"""
import json, os, sys

PREFIX = {"plugins": "P", "reviews": "R", "pains": "PN", "gaps": "G", "benefits": "B",
          "sources": "S", "feature_set": "F"}
TEMPLATE = os.path.join(os.path.dirname(__file__), "..", "assets", "research-template.json")

def load(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    with open(TEMPLATE, encoding="utf-8") as fh:
        return json.load(fh)

def num(v):
    try:
        return int(v) if v.isdigit() else float(v) if v.replace(".", "", 1).isdigit() else v
    except Exception:
        return v

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    path, args = sys.argv[1], sys.argv[2:]
    data = load(path)
    if args[0] == "--phase":
        data["phase_done"] = int(args[1])
    elif args[0] == "--set":
        for kv in args[1:]:
            k, v = kv.split("=", 1); data[k] = num(v)
    else:
        section = args[0]
        if "--json" in args:
            row = json.loads(args[args.index("--json") + 1])
        else:
            row = {}
            for kv in args[1:]:
                k, v = kv.split("=", 1); row[k] = num(v)
        rows = data.setdefault(section, [])
        if section in PREFIX and "id" not in row:
            width = 2 if PREFIX[section] != "PN" else 2
            row = {"id": f"{PREFIX[section]}{len(rows) + 1:0{width}d}", **row}
        rows.append(row)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    last = data[args[0]][-1] if args[0] not in ("--phase", "--set") else args
    print("saved:", json.dumps(last, ensure_ascii=False)[:160])

if __name__ == "__main__":
    main()
