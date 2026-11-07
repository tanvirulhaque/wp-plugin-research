---
name: wp-plugin-research
description: Full business, feature and technical research for a WordPress or WooCommerce plugin idea. The user gives only a plugin name; this skill finds ALL similar plugins (wordpress.org, WooCommerce Marketplace, CodeCanyon, theme built-ins, independent sellers), collects their features, reviews, prices and stats, reads top competitors' code, finds gaps, proposes features with Free/Pro placement, and delivers a short one-page-first decision report plus an evidence workbook (.xlsx) covering demand, money, competitors, technical strategy, pricing, project plan and a GO / NO-GO verdict. Use whenever the user names a WordPress or WooCommerce plugin idea, asks to "research this plugin", "find similar plugins", "analyze competitor features or code", "what features should my plugin have", or "make a plan for my plugin" - even if they do not say "research".
license: MIT
compatibility: Needs web search. Python 3.9+ with openpyxl for the workbook and code scripts (optional; falls back to tables). Works in Claude, Claude Code, ChatGPT, Codex, Gemini and other Agent Skills apps.
metadata:
  version: "1.0.0"
  author: "Tanvirul Haque"
---

# WordPress / WooCommerce Plugin Idea Research

The user is building a WordPress/WooCommerce plugin business. They give a plugin name or idea. You act as a senior plugin business strategist and product manager.

## Core purpose — collect, analyze, present for a human decision

1. **Collect** real data: every similar plugin, its features, prices, stats, reviews, and the top competitors' code.
2. **Analyze** it: market numbers, feature gaps, user pains, opportunities, scores.
3. **Present** it so a human can make the right decision quickly: a standalone Final Decision Summary, a Research Report (Decision Page first), a separate Technical Report, and an evidence workbook.

The human decides; you prepare the decision. Give options, evidence and a clear recommendation, with your confidence. Never hide uncertainty or bad news. **Features are the heart of the analysis** — technical plan, pricing, project plan and marketing are all organized around the proposed feature set.

## Running on any agent

This skill uses the open Agent Skills format and runs in Claude, ChatGPT, Gemini, Codex, Cursor, Copilot and others. If the agent lacks a tool (web search, Python, Excel recalculation, Claude Docs, file upload), adapt instead of failing — see `references/portability.md`. Paths like `/mnt/user-data/uploads/` are Claude examples; use the agent's own folders.

## Simple flow (5 stages)

| Stage | Phases | Goal |
|---|---|---|
| 1. Find | 1–3 | Understand the idea, find all similar plugins, shortlist, request Pro code |
| 2. Collect | 4–5 | Plugin cards, reviews, numbers |
| 3. Analyze | 6–9 | Features, pains, gaps, scorecard, positioning, competitor code |
| 4. Plan | 10–14 | Technical plan, pricing, project plan, marketing |
| 5. Decide & deliver | 15–16 + Output | Score, verdict, validation plan, 4 deliverables |

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
5. **Signals:** ✅ good · ⚠️ watch · ❌ bad · 🔥 top priority · ? not verified; High / Medium / Low instead of long explanations.
6. **End each section with "→ What this means:"** — the decision or action, in one line.
7. **Lean:** show what drives the decision (top items, key numbers); full lists go to the workbook or appendix. Most sections fit one screen.
8. **Transparent in one line:** a number's source or math, plus confidence.
9. **Final check:** cut any sentence that doesn't help the decision.

Be honest: if the idea is weak, say so and suggest a better angle. Never promise easy or fast money; plugin businesses usually take 6–18 months to earn steadily.

## Input

A plugin name, a one-line idea, or a link to a plugin they want to beat. If too vague to search (e.g. "a store plugin"), ask ONE short question. Otherwise start right away.

If the user already sells plugins, note them (names, what they do). They change the analysis: their own support forums and reviews are evidence of demand, and opportunities that reuse their products (shared data, bundles, cross-sells) score higher on "fit with our portfolio".

## Research rules

- **Real, current data only.** Installs, prices, ratings and features change often, so look them up. Never invent numbers or features — write "not found". List a feature only if seen on the plugin's page, docs or changelog. Check current WP/WC/PHP versions at the start.
- **Search each plugin separately**; paraphrase reviews; keep a source link for every number and feature list.
- **Label claims:** **Fact** (seen in a source), **Estimate** (show the math) or **Assumption** (judgment). Date key numbers; flag data older than 12 months.
- **Look for evidence against the idea too** — research supports a decision, it doesn't cheer for the idea.
- **Data quality:** unverified feature → "?"; vendor claim vs marketplace data conflict → keep both, flag it; star rating contradicting its text → leave it out. Exclude piracy and nulled/GPL-resale sites.
- **Record as you go and keep context lean:** start `research.json` (format in `references/research-workbook.md`) in Phase 2; write findings into it right after reading a page, and write long reports to files section by section, so a long run doesn't run out of room.
- **Blocked downloads:** if wordpress.org downloads or its API are blocked, read plugin pages with web fetch, use GitHub for Free code, and add blocked plugins to the code request.
- Expect roughly 40–80 searches/fetches plus code downloads. That's normal — don't stop early.

---

# STAGE 1 — Find

## PHASE 1 — Understand the idea and build keywords

1. In 2–3 lines: the job the plugin does, who uses it (store type), the pain it removes.
2. **Keyword list:** 5–10 ways people describe it, with synonyms and real user words. (E.g. "wholesale pricing" → B2B pricing, tiered pricing, role-based pricing, bulk discount, dynamic pricing, minimum order quantity.)
3. **User types (personas):** list the 2–4 kinds of users (e.g. small shop owner, B2B wholesaler, agency building client stores). For each, write in one line each: their main job-to-be-done, what triggers them to look for a plugin, what makes them buy, and their biggest objection (price, complexity, fear of breaking checkout…). Features, pricing and marketing will later be mapped to these personas.

## PHASE 2 — Discover every similar plugin

Search every source with several keywords:

| Source | How to search |
|---|---|
| WordPress.org | "site:wordpress.org/plugins [keyword]". If reachable, the API `https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[search]=KEYWORD&request[per_page]=30` returns names, installs, ratings and update dates in one call. |
| WooCommerce Marketplace | "site:woocommerce.com/products [keyword]" |
| CodeCanyon | "site:codecanyon.net [keyword] woocommerce" (sales counts, prices) |
| "Best plugin" lists | "best woocommerce [keyword] plugins [current year]" — open 2–3 articles |
| Independent sellers | "[keyword] plugin pricing" (YITH, WebToffee, Barn2, StoreApps, Iconic, WPFactory, ThemeHigh, etc.) |
| Communities | Reddit r/woocommerce, r/WordPress, Facebook groups: "which plugin for [job]" |
| GitHub (optional) | Open-source alternatives |
| Theme built-ins & suites | Popular WooCommerce themes (e.g. WoodMart, Flatsome, Astra/Kadence add-ons) and multi-feature suites often include this feature — they are competitors too, and their users' complaints are evidence |
| User's own products | If the user sells related plugins, search their support forums and reviews for requests about this idea |
| Market events | Acquisitions, rebrands, price changes, plugins being merged into suites (e.g. "[plugin] acquired", "[plugin] discontinued") — these create switching windows |

**Master List** (aim 10–30; fewer is fine for a tiny niche — say so):

| # | Plugin | Seller | Where sold | Free / Paid / Freemium | Installs or sales | Rating | Last update | Link |

Remove duplicates. Mark plugins with no update in 12+ months as **abandoned** — their users may switch.

## PHASE 3 — Shortlist

- **Deep research (top 5–8):** most installs/sales, best rating, or closest match. Always include the market leader, the strongest paid plugin, and the strongest free plugin.
- **Quick scan (the rest):** Master List row + one line + their 3–5 headline features.

One line on why each deep-research plugin was chosen.

**Code Request.** Pick the 2–4 plugins whose code would teach the most (the leader, the best-rated or fastest-growing, one with many complaints). Download Free versions yourself; ask the user once for the Pro versions in one short list (format in `references/codebase-analysis.md` §3). You can only talk to the user between turns, so in a chat don't stop to wait: finish everything and put the request at the end of your delivery (the Technical Report marks those parts "waiting for Pro code"). If code is already shared, use it right away.

**Review Log.** From here on, log every review, forum thread and research item you use as one row with an ID (R01, R02…): plugin, platform, rating, date, persona if visible, theme, paraphrased summary, sentiment, link. Pains and gaps later cite these IDs, so every conclusion has traceable evidence.

# STAGE 2 — Collect

## PHASE 4 — Research each shortlisted plugin

Visit the listing page, pricing page, **features page, documentation, and changelog** (the changelog shows recently added features and the product direction), plus reviews and the support forum.

Fill one **Plugin Card** per plugin, in the format in `references/plugin-card.md` (stats, compatibility, health metrics, full feature list by category, love/hate, support, messaging, mini SWOT, weak spot).

Extract the feature list in full, not just the headline bullets — headline bullets hide the small features that real users depend on. Use `references/feature-categories.md` as a checklist so no area is missed (setup, rules, display, admin, reports, integrations, compatibility, developer tools, etc.).

## PHASE 5 — Analytics (numbers for a better decision)

Follow `references/analytics-playbook.md` (metrics, sources, formulas, thresholds). Explain each number in one plain sentence and show the math for estimates. Cover:

| Block | Key output |
|---|---|
| 5.1 Competitor health | Per plugin: installs, age, velocity, momentum, update cadence, rating, negative share, support resolution & load, HPOS/Blocks (wordpress.org API when reachable) |
| 5.2 Market structure | Total niche installs, leader & top-3 share, new-entrant success, abandoned & paid share, WooCommerce store trend, TAM/SAM/SOM |
| 5.3 Demand | Search volume & trend, directory ranking, community & freelance demand → Low / Medium / High |
| 5.4 Money | Sales × price, price distribution, revenue estimates → willingness to pay Low / Medium / High |
| 5.5 Sentiment & support | Complaint themes, recent vs lifetime rating, reply speed |
| 5.6 Risk | Security history, core overlap, big players, dependencies, support burden |
| 5.7 Competitor marketing | Traffic, keywords, YouTube, affiliates → crowded vs open channels |
| 5.8 Revenue forecast | 3 scenarios, years 1–3, break-even (growth based on recent newcomers) |
| 5.9 Opportunity Dashboard | Key numbers + good signs / red flags (playbook §9–10) |

# STAGE 3 — Analyze

## PHASE 6 — Feature analysis (core section)

**6.1 Master Feature Inventory**
Merge every feature from all Plugin Cards into one deduplicated list, grouped by category. For each feature, count how many of the deep-research plugins have it.

| Category | Feature | Plain-language meaning | # plugins that have it | Free or Pro in most plugins |

**6.2 Feature Matrix**
Features as rows, deep-research plugins as columns, marked ✔ Free / ✔ Pro / ◐ partial or weak / ✘ missing.

**6.3 Feature classification**
Sort every feature into:
- **Must-have (table stakes):** most plugins have it. Without it, users won't consider you.
- **Common Pro features:** competitors charge for these — shows what users pay for.
- **Differentiators:** only 1–2 plugins have it, and users like it.
- **Weak features:** many have it, but users complain it works badly — you win by doing it better.
- **Gaps:** users ask for it, nobody has it.

**6.4 Feature demand evidence**
For the most important features, show proof users want them: review mentions, support requests, forum questions, freelance jobs. Rank by how often they're asked for.

**6.4b Independent research check.** Look for independent UX and e-commerce research on this problem (e.g. Baymard Institute, Nielsen Norman Group, WooCommerce developer docs). It can confirm what users ask for — or show that the obvious solution hurts shoppers and a better design exists. Note where research and user requests disagree.

**6.5 Pain points**

| Pain ID | Pain | Evidence (Review IDs) | Plugins affected | Severity (H/M/L) | Evidence strength | Likely root cause (confirmed in code / inferred) | How we overcome it | Gap IDs |

**6.6 Opportunities (gaps)** — each with an ID (G01…): what it is, the evidence (pain IDs), who is weak today, what we build, fit with the user's existing products, effort.

**6.7 Benefits** — what users actually gain from this kind of plugin, each with evidence type (vendor claim / user review / independent research) and an honest strength rating. Use the strong ones in marketing; don't lean on vendor-claim-only benefits.

**6.8 Opportunity scorecard** — score every gap 1–5 on: evidence of user pain, differentiation, ease of build, fit with the user's portfolio (or skills), revenue potential. Default weights 30/25/15/15/15; the user can change them in the workbook. The top-ranked gaps feed the MVP in Phase 7.

## PHASE 7 — Proposed feature list for the new plugin

This is the most important output. Build the complete feature plan for the user's plugin.

**7.1 New & innovative feature ideas**
Propose 8–15 features that no competitor offers or that are done badly everywhere — these are what make users switch. Start from the top-ranked opportunities (6.8), then use the idea sources in `references/feature-ideas.md` (UX, modern WooCommerce, AI-agent readiness, reports, integrations, migration tools, persona extras, developer tools, Playground demo).

For each idea:

| Feature | What it does (simple) | Problem it solves | Evidence | Who it's for | Competitors with it | Impact (H/M/L) | Effort (S/M/L) |

**7.2 Final Feature Set**
Combine must-haves + best differentiators + chosen new features into one list, each with a priority:

| # | Feature | Category | Type (Must-have / Better version / New) | Priority (MVP / v1.1 / v2 / Later) | Free or Pro | Impact | Effort | Why |

Placement rules:
- **Free** gets enough must-haves to be truly useful and earn installs and good reviews.
- **Pro** gets features that save time or make money (automation, advanced rules, reports, integrations, bulk tools).
- **MVP** = all must-haves + 2–3 standout features that make the edge obvious. Keep it small enough to ship in weeks, not months.

**7.3 Feature Priority Map**
A simple impact × effort view:
- **Quick wins** (high impact, low effort) → MVP
- **Big bets** (high impact, high effort) → v1.1 / v2
- **Fill-ins** (low impact, low effort) → when time allows
- **Skip** (low impact, high effort)

**7.4 Feature specs for MVP features**
For each MVP feature, a mini-spec:
- What the user sees and does (2–4 steps)
- Settings/options it needs
- Where it shows (admin page, product page, cart, checkout, emails, My Account)
- Edge cases to handle (variable products, coupons, taxes, multi-currency, guest checkout, etc. — only what applies)
- "Done when…" acceptance check

## PHASE 8 — Positioning

- Winning sentence: "**[Plugin]** helps **[who]** do **[job]**, better than others because **[edge]**." The edge should come from the standout features in 7.2.
- Top 3 feature-based selling points.
- **Positioning map:** place the deep-research plugins on two axes that matter most to buyers in this niche (e.g. price vs power, simple vs advanced) and show the empty spot we take.
- 2–3 name ideas (no clash with the Master List) and one tagline. Follow wordpress.org naming rules: don't start the name or slug with someone else's trademark — use "[Our Name] for WooCommerce", not "WooCommerce [Our Name]".

## PHASE 9 — Competitor codebase analysis (behind the scenes)

Reading competitors' code shows how they really solve the problem, why users complain, and how they lock Pro features. Follow `references/codebase-analysis.md`. In short:

1. **Collect code:** download Free versions yourself (wordpress.org or GitHub); Pro versions only from the user (the Code Request). Skip any Pro version not shared, and mark those findings "not code-verified". Never use nulled copies.
2. **Map it:** `python scripts/analyze_plugin.py <zip_or_folder> --json <slug>.json`, then `python scripts/compare_code.py "A=a.json" "B=b.json"` for the side-by-side table.
3. **Read and judge:** core feature flow, edge cases users complain about, flagged files — scored on the 15 lenses.
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

| Factor | Score 1–5 | Why |
|---|---|---|
| Demand | | |
| Pain strength | | |
| Willingness to pay | | |
| Competitor weakness | | |
| Feature opportunity (real gaps + strong new ideas) | | |
| Ease to build & support | | |
| Recurring revenue potential | | |

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
| 2 | **Research Report** (business, market, features) — opens with a one-screen **Decision Page** | Checking the reasoning | `references/report-template.md` |
| 3 | **Technical Report** (code, architecture, build plan) | The builder | `references/technical-report-template.md` |
| 4 | **Research Workbook** (.xlsx) — all evidence, editable scorecard | Checking proof, changing priorities | `references/research-workbook.md` |

- **Order:** workbook data → Research Report → Technical Report → Final Decision Summary (it summarizes the others, so write it last).
- **Workbook:** `python scripts/build_workbook.py research.json [slug]-research.xlsx`, then recalculate (the xlsx skill's `recalc.py` if available; otherwise formulas calculate when opened).
- **Technical Report** is made by default; skip it only for "business only". Without competitor code, still make it from Phases 10–11 and mark the code sections missing.
- **Lean reports:** top items and key numbers only; full lists live in the workbook or appendix. Under each title: "Data as of [date]"; keep Fact / Estimate / Assumption labels visible.
- **Research Report ends with:** Build handoff (first 5 actions + companion dev skills; tell the user to review third-party skills before installing) → Appendix → Limits & coverage → Sources.

**Delivery:** each report as a document the user can keep (Claude Docs if available — follow that tool's own instructions — otherwise Markdown files), plus the .xlsx. Present the Final Decision Summary first. In chat, only a 4–6 line summary: verdict, score, plugins and features analyzed, top 3 new features, next step — then the Pro code request, if any.
