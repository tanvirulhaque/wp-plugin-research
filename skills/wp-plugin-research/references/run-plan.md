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
| **0 — Capability check** (~2 min) | Local WordPress install and plugins? Agent browser able to run page scripts? User willing to use rung 4 (their browser) — give the one-time setup now? Python + openpyxl? (`collectors.md` §2) | Answers in `notes.md`; a starting rung per source |
| **1 — Research** | Stages 1–3: local plugins first, pre-flight, **wide discovery** (keywords × 2 pages + tags), plugin cards, **all-plugin code-signal scan**, **support-thread mining**, low-star + newest 5★ reviews, **Marketplace review collector**, **Trends + autocomplete**, **Reddit via the user's browser**, newcomer metric, core-overlap check, analytics, features, pains, gaps, scorecard | `research.json` + `notes.md` saved, **workbook built**, end-of-turn message **with the code request** (below) |
| **2 — Reports** | Stages 4–5: ask Claude Docs or files once (files by default in a local code project), technical plan, pricing, project plan, marketing, score, deliverables | All reports delivered |
| **3 — Pro code (optional)** | Deep code check on code the user shares | Updated Technical Report and any affected scores |

End-of-turn-1 message (keep it this short):
```
Research done: N plugins screened → M in the niche, X deep-researched, Y pains, Z gaps.
Deep plugins: [names] — exact-name match: [plugin with the idea's exact name, or "none found"].
Early read: [GO / MAYBE / NO-GO] (preliminary).
Sources: [source → rung that worked, one line each]. Still missing: [item → what you can do].
Code request: [Pro plugins + price + what each would add to the decision] (skip any).
Workbook: [file]. Reply "continue" for the full reports.
Optional: do you already sell plugins? Name them — it changes the "fit" score.
```
If the agent can do everything in one turn (no cap hit), or the user asks for a full run without stopping, continue straight to turn 2.

## Call budget (Full mode, approximate)

| Phase | Calls |
|---|---|
| Capability check + pre-flight + versions + store count | 5 |
| Discovery (Phase 2) | ~10 calls + `wporg_discover.py` (scripts don't count against the budget) |
| Plugin cards (Phase 4) | ~15 (2–3 per plugin) |
| Analytics gaps (Phase 5) | ~8 |
| Code scan (Phase 9) | ~6 + `scan_signals.py` over every Free plugin |
| Collectors (reviews, threads, Trends, Reddit) | scripted; ~5 agent calls to run and save them |
| Delivery (turn 2) | ~10–15 |

**Subagents** (if available): use them for vendor pricing pages and security history; keep reviews, forums and code in the main session with scripts (subagent fetches are summarised and hit the same blocks). Subagents must report what was blocked.

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
