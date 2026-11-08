# Run Plan — turns, budgets, checkpoints, modes

A full run does not fit in one reply on most agents (tool-call caps per turn, context size). Plan it in turns from the start, and save a checkpoint at the end of each turn so the next turn resumes cleanly.

## Modes

| Mode | When | Deep plugins | Deliverables |
|---|---|---|---|
| **Full** (default) | Normal request | 5–8 (3–4 in a small niche) | All 4 |
| **Lite** | User says "quick", "lite", "fast", or the niche is tiny | 3 | Final Decision Summary + workbook |

## Turn plan

| Turn | Does | Ends with |
|---|---|---|
| **1 — Research** | Stages 1–3: pre-flight check, discovery, plugin cards, analytics, features, pains, gaps, scorecard, light code scan of Free versions | `research.json` + `notes.md` saved, **workbook built**, then a short chat message (below) |
| **2 — Reports** | Stages 4–5: technical plan, pricing, project plan, marketing, score, deliverables | All reports delivered + Pro code request (if any) |
| **3 — Pro code (optional)** | Deep code check on code the user shares | Updated Technical Report and any affected scores |

End-of-turn-1 message (keep it this short):
```
Research done: N plugins found, X deep-researched, Y pains, Z gaps.
Early read: [GO / MAYBE / NO-GO] (preliminary).
Workbook: [file]. Reply "continue" for the full reports.
Optional: do you already sell plugins? Name them — it changes the "fit" score.
```
If the agent can do everything in one turn (no cap hit), or the user asks for a full run without stopping, continue straight to turn 2.

## Call budget (Full mode, approximate)

| Phase | Calls |
|---|---|
| Pre-flight + versions + store count | 3 |
| Discovery (Phase 2) | ~20 |
| Plugin cards (Phase 4) | ~15 (2–3 per plugin) |
| Analytics gaps (Phase 5) | ~8 |
| Light code scan (Phase 9) | ~6 |
| Delivery (turn 2) | ~10–15 |

Lite mode: about half. The budget is a **guide for planning turns, not a cap on data**: when a phase hits its budget, save progress and continue it in the next turn — don't drop it. Only skip a source when it is truly unreachable, and record that in the coverage checklist.

## Checkpoints and resume

- `research.json` holds the data; add `"phase_done": <number>` and update it after each phase.
- `notes.md` holds short working notes: decisions taken, URLs still to check, coverage gaps.
- **Build the workbook at the end of turn 1**, so a cut-off still leaves the evidence file.
- **Resume rule:** if `research.json` exists at the start of a turn, read it and `notes.md`, then continue from the phase after `phase_done`. Never restart from zero.
- Use `scripts/add_row.py` to append one row per finding — it keeps the habit cheap and the file valid.

## Coverage checklist

Fill this in `notes.md` as you go, and copy it into **Limits & coverage**:

| Item | Done / Partial / Skipped | Note |
|---|---|---|
| wordpress.org data (API or pages) | | |
| WooCommerce Marketplace | | |
| CodeCanyon | | |
| Theme built-ins & suites | | |
| Reviews from ≥ 3 plugins (incl. 1–2★ pages) | | |
| Community (Reddit / forums) | | |
| Security history per deep plugin | | |
| Current WP / WC versions (official) | | |
| WooCommerce store count | | |
| Free code scanned | | |
| Pro code analyzed | | |
| Keyword / trend data | | |
| Competitor marketing | | |
