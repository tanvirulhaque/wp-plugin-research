#!/usr/bin/env python3
"""
Guardrail for SKILL.md size and instruction safety.

Usage: python tools/check_skill.py [skills/wp-plugin-research]

Checks:
  1. SKILL.md body size: warn above 3,700 words, fail above 4,200
     (the Agent Skills spec recommends < 5,000 tokens for the body).
  2. Every references/, scripts/ and assets/ path mentioned in SKILL.md or a
     reference file exists - so moving text out never leaves a dead pointer.
  3. Every reference file is pointed to from SKILL.md - so nothing moved out
     becomes an orphan the agent never reads.
  4. Every phase (1-16) still has a heading in SKILL.md.
"""
import os, re, sys

root = sys.argv[1] if len(sys.argv) > 1 else "skills/wp-plugin-research"
skill = open(os.path.join(root, "SKILL.md"), encoding="utf-8").read()
body = skill.split("---", 2)[2]
words = len(body.split())
ok = True

if words > 4200:
    print(f"✗ SKILL.md body is {words} words (limit 4,200). Move detail into references/."); ok = False
elif words > 3700:
    print(f"⚠ SKILL.md body is {words} words (target ≤ 3,700).")
else:
    print(f"✓ SKILL.md body: {words} words")

texts = {"SKILL.md": skill}
ref_dir = os.path.join(root, "references")
for f in os.listdir(ref_dir):
    texts[f"references/{f}"] = open(os.path.join(ref_dir, f), encoding="utf-8").read()

pat = re.compile(r"(?<![/\w])((?:references|scripts|assets)/[A-Za-z0-9_\-]+\.(?:md|py|json))")
for name, txt in texts.items():
    for m in set(pat.findall(txt)):
        if not os.path.exists(os.path.join(root, m)):
            print(f"✗ {name} points to missing file: {m}"); ok = False
print("✓ all pointers resolve" if ok else "")

for f in os.listdir(ref_dir):
    if f"references/{f}" not in skill and f not in skill:
        print(f"✗ references/{f} is never mentioned in SKILL.md (orphan)"); ok = False

for n in range(1, 17):
    if not re.search(rf"^## PHASE {n} —", skill, flags=re.M):
        print(f"✗ PHASE {n} heading missing from SKILL.md"); ok = False

print("✓ skill check passed" if ok else "✗ skill check failed")
sys.exit(0 if ok else 1)
