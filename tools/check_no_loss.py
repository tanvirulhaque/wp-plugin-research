#!/usr/bin/env python3
"""
No-instruction-loss audit: compares an older version of the skill with the
current one and lists old instruction lines whose wording no longer appears
anywhere (SKILL.md or references). Use before every release.

Usage:
  git archive <old-tag> skills | tar -x -C /tmp/old
  python tools/check_no_loss.py /tmp/old/skills/wp-plugin-research skills/wp-plugin-research
Lines below 70% phrase coverage are printed for a human to confirm they were
reworded or moved on purpose.
"""
import os, re, sys

def corpus(root):
    out = {}
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".md"):
                out[os.path.relpath(os.path.join(dp, f), root)] = open(os.path.join(dp, f), encoding="utf-8").read()
    return out

def words(t): return re.findall(r"[a-z0-9]+", t.lower())

old, new = corpus(sys.argv[1]), corpus(sys.argv[2])
nw = words(" ".join(new.values()))
nb = set(zip(nw, nw[1:]))
flags, checked = [], 0
for f, txt in old.items():
    for line in txt.splitlines():
        w = words(line)
        if len(w) < 8:
            continue
        checked += 1
        b = list(zip(w, w[1:]))
        cov = sum(1 for x in b if x in nb) / len(b)
        if cov < 0.7:
            flags.append((round(cov, 2), f, line.strip()[:160]))
print(f"Checked {checked} instruction lines; {len(flags)} need a human look:")
for x in sorted(flags):
    print(f"  {x[0]:.2f}  {x[1]}: {x[2]}")
