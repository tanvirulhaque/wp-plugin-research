---
name: wp-plugin-research
description: Full business, feature and technical research for a WordPress or WooCommerce plugin idea. The user gives only a plugin name; this skill finds every similar plugin (wordpress.org, WooCommerce Marketplace, CodeCanyon, theme built-ins, independent sellers), collects features, reviews, prices and stats, scans competitors' code, finds gaps, proposes features with Free/Pro placement, and delivers a Final Decision Summary (GO / MAYBE / NO-GO), Research and Technical reports, and an evidence workbook (.xlsx) with forecast, pricing and verdict - run in planned turns with saved progress. Use whenever the user names a WordPress or WooCommerce plugin idea, asks to "research this plugin", "find similar plugins", "analyze competitor features or code", "what features should my plugin have", or "make a plan for my plugin" - even if they do not say "research".
license: MIT
compatibility: Needs web search. Python 3.9+ with openpyxl for the workbook and code scripts (optional; falls back to tables). Works in Claude, Claude Code, ChatGPT, Codex, Gemini and other Agent Skills apps.
metadata:
  version: "1.2.0"
  author: "Tanvirul Haque"
---

# WordPress / WooCommerce Plugin Idea Research

The user is building a WordPress/WooCommerce plugin business. They give a plugin name or idea. You act as a senior plugin business strategist and product manager.

## Core purpose — collect, analyze, present for a human decision

1. **Collect** real data: every similar plugin, its features, prices, stats, reviews, and the top competitors' code.
2. **Analyze** it: market numbers, feature gaps, user pains, opportunities, scores.
3. **Present** it so a human can make the right decision quickly: a standalone Final Decision Summary, a Research Report, a separate Technical Report, and an evidence workbook.

The human decides; you prepare the decision. Give options, evidence and a clear recommendation, with your confidence. Never hide uncertainty or bad news. **Features are the heart of the analysis** — technical plan, pricing, project plan and marketing are all organized around the proposed feature set.

## Running on any agent

This skill uses the open Agent Skills format and runs in Claude, ChatGPT, Gemini, Codex, Cursor, Copilot and others. If the agent lacks a tool (web search, Python, Excel recalculation, Claude Docs, file upload), adapt instead of failing — see `references/portability.md`. Paths like `/mnt/user-data/uploads/` are Claude examples; use the agent's own folders.

## Simple flow (5 stages)

| Stage | Phases | Goal |
|---|---|---|
| 1. Find | 1–3 | Understand the idea, find all similar plugins, shortlist, choose code to study |
| 2. Collect | 4–5 | Plugin cards, reviews, numbers |
| 3. Analyze | 6–9 | Features, pains, gaps, scorecard, positioning, competitor code |
| 4. Plan | 10–14 | Technical plan, pricing, project plan, marketing |
| 5. Decide & deliver | 15–16 + Output | Score, verdict, validation plan, 4 deliverables |

## Run plan — plan in turns from the start

A full run rarely fits in one reply (tool-call caps, context). Follow `references/run-plan.md`:

| Turn | Covers | Ends with |
|---|---|---|
| 0 — Capability check (~2 min) | Local WordPress? agent browser? user's browser OK? Python/openpyxl? (`references/collectors.md` §2) | Answers in `notes.md`, a starting rung per source |
| 1 — Research | Stages 1–3 (+ code-signal scan of every Free plugin) | `research.json` + `notes.md` saved, workbook built, end-of-turn message + **code request** |
| 2 — Reports | Stages 4–5 | 4 deliverables |
| 3 — Pro code (optional) | Deep code check | Updated Technical Report |

- **Resume rule:** if `research.json` exists, read it and `notes.md` and continue from the phase after `phase_done` — never restart.
- **Modes:** Full (default) or **Lite** ("quick"/"lite", or a tiny niche): 3 deep plugins, Final Decision Summary + workbook only.
- Keep a **coverage checklist** in `notes.md` (with the ladder rung that worked per source) and copy it into Limits & coverage.
- **End-of-turn-1 message** names the deep-research plugins — always including any plugin matching the idea's exact name — states which rung worked per source, and lists what's still missing with what the user can do about each.

## Keep it simple — without losing data

- **Every piece of data lives in one place: the workbook.** Reports summarize and point to IDs (P03, PN01, G02) instead of repeating rows.
- **Each report has one job:** Decision Summary = decide, Research Report = business reasoning, Technical Report = build. No section appears in full in two reports.
- **Scale depth to the niche.** Small niche (under ~10 plugins): fewer deep-research plugins (3–4), shorter sections. Skip any step that doesn't apply and say so in one line — don't fill space.
- **Collect fully, show selectively.** Keep everything you find in `research.json` / the workbook; show only what changes the decision in the reports.
- **Plain over clever.** If a metric or table doesn't help the decision, leave it in the workbook only.

## Writing style — short, clear, easy

The user is making a business decision and reads fast; long text hides findings. Lots of data is fine, lots of text is not. In reports, workbook and chat:

1. **Answer first:** each section opens with one bold takeaway line.
2. **Short and plain:** sentences of ~15 words, words a 5th-grader knows; explain a technical term in 3–5 words once.
3. **Tables, not paragraphs:** one idea per bullet, one line per bullet.
4. **No filler or repetition.**
5. **Signals:** ✅ good · ⚠️ watch · ❌ bad · 🔥 top priority · ? not verified; High / Medium / Low instead of long explanations. In Claude Docs use words instead of emoji (Good / Watch / Bad / Top priority / Not verified).
6. **End each section with "→ What this means:"** — the decision or action, in one line.
7. **Lean:** show what drives the decision (top items, key numbers); full lists go to the workbook or appendix. Most sections fit one screen.
8. **Transparent in one line:** a number's source or math, plus confidence.
9. **Final check:** cut any sentence that doesn't help the decision.

Be honest: if the idea is weak, say so and suggest a better angle. Never promise easy or fast money; plugin businesses usually take 6–18 months to earn steadily.

## Input

A plugin name, a one-line idea, or a link to a plugin they want to beat. If too vague to search (e.g. "a store plugin"), ask ONE short question. Otherwise start right away.

If the user says "quick" or "lite", use Lite mode. If the user already sells plugins, note them in `user_products`: their own forums and reviews are demand evidence, and opportunities that reuse their products score higher on "fit with our portfolio". If they haven't said, ask at the end of turn 1.

## Research rules

- **Real, current data only.** Installs, prices, ratings and features change often, so look them up. Never invent numbers or features — write "not found". List a feature only if seen on the plugin's page, docs or changelog. Check current WP/WC/PHP versions at the start.
- **Search each plugin separately**; paraphrase reviews; keep a source link for every number and feature list.
- **Label claims:** **Fact** (seen in a source), **Estimate** (show the math) or **Assumption** (judgment). Date key numbers; flag data older than 12 months.
- **Look for evidence against the idea too** — research supports a decision, it doesn't cheer for the idea.
- **Collection ladder:** follow `references/collectors.md` — API → HTML parser → in-page collector → the user's browser (with consent) → user export / own-key API → "not reachable". **Never write "only N are public" or "unreachable" after rung 1 or 2**; say which rungs were tried.
- **Sources and data quality:** follow `references/sources.md` — pre-flight check of wordpress.org access, **search first, then fetch** (most fetch tools reject typed URLs), page-size limits, the fallback chain when wordpress.org is blocked, the piracy blocklist, and rules for vendor pages, conflicting numbers, duplicates and review spread. Unverified feature → "?"; a star rating contradicting its text → leave it out.
- **Record as you go:** collectors write `raw/`; append findings with `scripts/add_row.py`, or keep hand-made findings in `overrides.json` and rebuild with `scripts/merge_research.py` (idempotent, stable review IDs). Keep `notes.md` updated, so a cut-off loses nothing.
- Expect roughly 40–80 searches/fetches in Full mode, split across turns with the per-phase budgets in `run-plan.md`. Budgets plan the turns; they never cut data — if a phase runs over, save and continue it next turn.

---

# STAGE 1 — Find

## PHASE 1 — Understand the idea and build keywords

1. In 2–3 lines: the job the plugin does, who uses it (store type), the pain it removes.
2. **Keyword list:** 5–10 ways people describe it, with synonyms and real user words. (E.g. "wholesale pricing" → B2B pricing, tiered pricing, role-based pricing, bulk discount, dynamic pricing, minimum order quantity.)
3. **User types (personas):** list the 2–4 kinds of users (e.g. small shop owner, B2B wholesaler, agency building client stores). For each, write in one line each: their main job-to-be-done, what triggers them to look for a plugin, what makes them buy, and their biggest objection (price, complexity, fear of breaking checkout…). Features, pricing and marketing will later be mapped to these personas.

## PHASE 2 — Discover every similar plugin

**Look locally first:** list the user's `wp-content/plugins/` (if the working folder is a WordPress install), `./competitors/` and any path they name; matches go straight onto the Master List and the code-scan list. Then run the pre-flight check and required early searches (`references/sources.md`), and **discover wide**: `scripts/wporg_discover.py` with every keyword **and** tag, 2+ pages each, then filter by name/description/tags (a real run screened 1,211 plugins from 32 keywords + 8 tags). Then search every source:

Sources to cover (search queries for each in `references/sources.md` §5): **WordPress.org · WooCommerce Marketplace · CodeCanyon · "best plugin" lists · independent sellers · communities (Reddit via the user's browser — rung 4) · GitHub · theme built-ins & suites · the user's own products · market events** (acquisitions, rebrands, discontinued plugins — switching windows).

**Master List** (aim 10–30; fewer is fine for a tiny niche — say so):

| # | Plugin | Seller | Where sold | Free / Paid / Freemium | Installs or sales | Rating | Last update | Link |

Remove duplicates (dedupe wordpress.org results by slug). `wporg_discover.py` also gives the **newcomer metric** (added in the last 24 months; how many passed 100 / 1,000 installs). Mark plugins with no update in 12+ months as **abandoned** — their users may switch.

## PHASE 3 — Shortlist

- **Deep research (top 5–8):** most installs/sales, best rating, or closest match. Always include the market leader, the strongest paid plugin, and the strongest free plugin.
- **Quick scan (the rest):** Master List row + one line + their 3–5 headline features.

One line on why each deep-research plugin was chosen.

**Code to study.** Pick the 2–4 plugins whose code would teach the most (the leader, the best-rated or fastest-growing, one with many complaints). Phase 9 collects it; the user is asked once — **at the end of turn 1**, so code can arrive before the reports — for Pro versions and any Free versions whose download was blocked, with prices, links and **what each purchase would add to the decision** (format in `references/codebase-analysis.md` §3). Never stop research to wait for code; if code is already shared, use it.

**Review Log.** From here on, log every review, forum thread and research item you use as one row with an ID (R01… when appended with `add_row.py`; a stable `R-a1b2c3` when rebuilt with `merge_research.py`): plugin, platform, rating, date, persona if visible, theme, paraphrased summary, sentiment, link. Pains and gaps later cite these IDs, so every conclusion has traceable evidence.

# STAGE 2 — Collect

## PHASE 4 — Research each shortlisted plugin

Visit the listing page, pricing page, **features page, documentation, and changelog** (the changelog shows recently added features and the product direction), plus the **1–2★ and newest 5★ reviews** (`scripts/wporg_reviews.py`; Marketplace: `scripts/collectors/woo-reviews-return.js`, keeping vendor replies), **support-thread titles** (`scripts/wporg_threads.py` — theme counts across all deep plugins), and **security history** (Patchstack / WPScan). Budget 2–3 calls per plugin beyond the scripts; fallbacks in `references/sources.md`.

Fill one **Plugin Card** per plugin, in the format in `references/plugin-card.md` (stats, compatibility, health metrics, full feature list by category, love/hate, support, messaging, mini SWOT, weak spot).

Extract the feature list in full, not just the headline bullets — headline bullets hide the small features that real users depend on. Use `references/feature-categories.md` as a checklist so no area is missed (setup, rules, display, admin, reports, integrations, compatibility, developer tools, etc.).

## PHASE 5 — Analytics (numbers for a better decision)

Follow `references/analytics-playbook.md` (metrics, sources, formulas, thresholds). Explain each number in one plain sentence and show the math for estimates. Cover:

| Block | Key output |
|---|---|
| 5.1 Competitor health | Per plugin: installs, age, velocity, momentum, update cadence, rating, negative share, support resolution & load, HPOS/Blocks (API when reachable; otherwise the metric fallback map, playbook §2b) |
| 5.2 Market structure | Total niche installs, leader & top-3 share, new-entrant success, abandoned & paid share, WooCommerce store trend, TAM/SAM/SOM |
| 5.3 Demand | Search volume & trend if available, directory ranking (who owns the top results), community & freelance demand; without keyword tools use the **demand proxy score** (playbook §4b) → Low / Medium / High |
| 5.4 Money | Sales × price, price distribution, revenue estimates → willingness to pay Low / Medium / High |
| 5.5 Sentiment & support | Complaint themes, recent vs lifetime rating, reply speed |
| 5.6 Risk | Security history, core overlap, big players, dependencies, support burden |
| 5.7 Competitor marketing | Traffic, keywords, YouTube, affiliates → crowded vs open channels |
| 5.8 Revenue forecast | Draft in turn 1, finalize in turn 2: 3 scenarios, years 1–3, break-even; growth from recent newcomers, plus direct / marketplace customers for paid-only sales |
| 5.9 Opportunity Dashboard | Key numbers + good signs / red flags (playbook §9–10) |

# STAGE 3 — Analyze

## PHASE 6 — Feature analysis (core section)

Follow `references/feature-analysis.md` for the tables and rules. Produce, in order:

- **6.1 Master Feature Inventory** — every feature from all Plugin Cards, deduplicated, by category, with how many deep plugins have it.
- **6.2 Feature Matrix** — features × deep plugins (✔ Free / ✔ Pro / ◐ weak / ✘ missing).
- **6.3 Classification** — must-have · common Pro · differentiator · weak · gap.
- **6.4 Demand evidence** and **6.4b independent research check** (Baymard, NN/g, WooCommerce docs — note where research and user requests disagree).
- **6.5 Pain points** — rank by support-thread title counts (`wporg_threads.py`) first, then confirm with reviews; each pain cites Review IDs and a root cause (confirmed in code / inferred).
- **6.6 Gaps (G01…)**, **6.7 Benefits** (with honest evidence strength), **6.8 Opportunity scorecard** (weights 30/25/15/15/15; top gaps feed the MVP).

## PHASE 7 — Proposed feature list for the new plugin

The most important output. Follow `references/feature-analysis.md` §7 and `references/feature-ideas.md`:

- **7.1 New ideas (8–15)** — no competitor has them or all do them badly; start from the top scorecard gaps.
- **7.2 Final Feature Set** — must-haves + best differentiators + chosen new features, each with priority (MVP / v1.1 / v2 / Later), Free or Pro, impact, effort. Free = truly useful; Pro = saves time or makes money; MVP = must-haves + 2–3 standout features, shippable in weeks.
- **7.3 Priority Map** and **7.4 MVP specs**.

## PHASE 8 — Positioning

- Winning sentence: "**[Plugin]** helps **[who]** do **[job]**, better than others because **[edge]**." The edge should come from the standout features in 7.2.
- Top 3 feature-based selling points.
- **Positioning map:** place the deep-research plugins on two axes that matter most to buyers in this niche (e.g. price vs power, simple vs advanced) and show the empty spot we take.
- 2–3 name ideas (no clash with the Master List) and one tagline. Follow wordpress.org naming rules: don't start the name or slug with someone else's trademark — use "[Our Name] for WooCommerce", not "WooCommerce [Our Name]".

## PHASE 9 — Competitor codebase analysis (behind the scenes)

Reading competitors' code shows how they really solve the problem, why users complain, and how they lock Pro features. Follow `references/codebase-analysis.md`. In short:

1. **Collect code** (never nulled copies):
   - **Turn 1, every Free plugin:** `scripts/scan_signals.py` with a niche signals file, plus a light scan of the deep ones. Download Free code yourself (wordpress.org, or `scripts/fetch_code.py SLUG` for GitHub mirrors — check the mirror's version against wordpress.org).
   - **Turn 3, Pro code** the user shares → deep check.
   - **No Pro zip?** Use the **Pro probes** — vendor demo page via `scripts/collectors/demo-probe.js`, Pro changelog and docs, Free-code hooks and `class_exists('…Pro')` checks, Pro mentions in forums — and mark findings "not code-verified".
   - **Core overlap:** grep a local or GitHub copy of WooCommerce for the feature and read the class.
2. **Map it:** `python scripts/analyze_plugin.py <zip_or_folder> --json <slug>.json --quiet` (it separates bundled SDKs, flags hot-path cart work, caching, telemetry and admin vs front-end queries), then `python scripts/compare_code.py "A=a.json" "B=b.json"` for the side-by-side table.
3. **Read and judge:** core feature flow, edge cases users complain about, flagged files — scored on the 15 lenses. Any "nobody does X" claim must come from the all-plugin signal scan and say "of N scanned".
4. **Link complaints to code causes** and write **Our Technical Strategy** for the Technical Report. Learn the pattern; don't clone the code.

# STAGE 4 — Plan

## PHASE 10 — Technical analysis (per feature)

Follow `references/technical-planning.md`: a technical table per proposed feature (areas touched, hooks/APIs, data, risk), compatibility must-haves, the modern WooCommerce rules (HPOS CRUD, Store API, Action Scheduler, cache-safe, Plugin Check), risks from competitors' code, performance, security, APIs, and difficulty with build-time estimates.

## PHASE 11 — Technical plan

Also in `references/technical-planning.md`: business model and Free/Pro split (from 7.2 and Phase 9), licensing tool, one module per major feature, settings design, and the testing plan. Base every decision on Our Technical Strategy from Phase 9.

## PHASE 12 — Pricing (by feature tier)

| Tier | Sites | Price/year | Features included |

Base prices on competitor prices from Phase 4. Show the Free vs Pro feature comparison table that would appear on the pricing page. Say whether a lifetime deal makes sense.

## PHASE 13 — Project plan (by feature)

| Week | Task / features built | Done when… |

Usually ~12 weeks for MVP: validation → core setup → MVP features (in priority order) → beta → wordpress.org submission (review 1–4 weeks) → docs + sales page → launch. Then a **feature roadmap**:

| Version | Features | Target timing |

## PHASE 14 — Launch & marketing

5–8 ideas tied to features: SEO keywords from Phase 1 plus feature keywords ("woocommerce [feature]"), one tutorial/blog/YouTube topic per standout feature, communities, partner plugins for integrations, wordpress.org listing tips (feature-focused screenshots and description), and a "switch from [competitor]" guide/importer.

# STAGE 5 — Decide & deliver

## PHASE 15 — Score and verdict

Score 1–5, with the number behind each: **Demand · Pain strength · Willingness to pay · Competitor weakness · Feature opportunity · Ease to build & support · Recurring revenue potential** (the workbook's Verdict sheet totals them by formula).

Base each score on the Phase 5 numbers and the thresholds in the playbook (§9), and quote the number that justifies it (e.g. "Demand 4/5 — 120k niche installs, rising trend").

**Devil's advocate (pre-mortem):** before the verdict, imagine it is one year after launch and the plugin failed. Write the 3–5 most likely reasons (using the evidence found), and for each, how likely it is and what would prevent it. If a reason is very likely and can't be prevented, lower the score.

Total out of 35.
- **28–35: GO** — build it.
- **21–27: MAYBE** — only with a sharp feature angle; state it.
- **Below 21: NO-GO** — explain why and suggest 1–3 better nearby ideas.

## PHASE 16 — Validate before building

Landing page + waitlist showing the top 3–5 proposed features. Ask visitors to **vote on features** (simple form) so real users confirm priorities. Where to post, what to post, and a target (e.g. 50–100 signups or a few presales) that decides whether to start coding.

---

## Output — 4 deliverables

| # | Deliverable | For | Template |
|---|---|---|---|
| 1 | **Final Decision Summary** (standalone, 2–4 pages) | The decision-maker — read first | `references/decision-summary-template.md` |
| 2 | **Research Report** (business, market, features) — opens with the Opportunity Dashboard; the decision itself lives only in the Final Decision Summary | Checking the reasoning | `references/report-template.md` |
| 3 | **Technical Report** (code, architecture, build plan) | The builder | `references/technical-report-template.md` |
| 4 | **Research Workbook** (.xlsx) — all evidence, editable scorecard | Checking proof, changing priorities | `references/research-workbook.md` |

- **Order:** workbook built at the end of turn 1; in turn 2: Research Report → Technical Report → Final Decision Summary (it summarizes the others, so write it last), then rebuild the workbook with the turn-2 sheets (feature set, pricing, forecast, verdict).
- **Workbook:** `python scripts/build_workbook.py research.json [slug]-research.xlsx`, then recalculate (find `recalc.py` as shown in `references/portability.md`; otherwise formulas calculate when opened).
- **Technical Report** is made by default; skip it only for "business only". Without competitor code, still make it from Phases 10–11 and mark the code sections missing.
- **No repeats:** the Summary states the decision; the other reports link to it instead of restating it.
- **Lean reports:** top items and key numbers only; full lists live in the workbook or appendix. Under each title: "Data as of [date]"; keep Fact / Estimate / Assumption labels visible.
- **Research Report ends with:** Build handoff (first 5 actions + companion dev skills; tell the user to review third-party skills before installing) → Appendix → Limits & coverage → Sources.

**Delivery:** each report as a document the user can keep — ask once at the start of turn 2 (Claude Docs or files), defaulting to files when the session is a local code project; with Claude Docs, follow **Claude Docs mode** in `references/portability.md` (create docs at the start of turn 2, one doc with Summary · Research · Technical tabs, grouped writes, no emoji); otherwise Markdown files — plus the .xlsx. Present the Final Decision Summary first. In chat, only a 4–6 line summary: verdict, score, plugins and features analyzed, top 3 new features, next step.
