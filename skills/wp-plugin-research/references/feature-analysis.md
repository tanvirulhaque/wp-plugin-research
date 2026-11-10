# Feature analysis and the proposed feature set (Phases 6–7)

The full tables and rules behind SKILL.md Phases 6 and 7. Idea sources and MVP spec format are in `feature-ideas.md`.

## Phase 6 — Feature analysis (core section)

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

**6.5 Pain points** — rank by support-thread title counts (`wporg_threads.py`) first, then confirm with reviews; titles are the widest, cheapest sample.

| Pain ID | Pain | Evidence (Review IDs) | Plugins affected | Severity (H/M/L) | Evidence strength | Likely root cause (confirmed in code / inferred) | How we overcome it | Gap IDs |

**6.6 Opportunities (gaps)** — each with an ID (G01…): what it is, the evidence (pain IDs), who is weak today, what we build, fit with the user's existing products, effort.

**6.7 Benefits** — what users actually gain from this kind of plugin, each with evidence type (vendor claim / user review / independent research) and an honest strength rating. Use the strong ones in marketing; don't lean on vendor-claim-only benefits.

**6.8 Opportunity scorecard** — score every gap 1–5 on: evidence of user pain, differentiation, ease of build, fit with the user's portfolio (or skills), revenue potential. Default weights 30/25/15/15/15; the user can change them in the workbook. The top-ranked gaps feed the MVP in Phase 7.

## §7 Phase 7 — Proposed feature list for the new plugin

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

**7.3 Feature Priority Map** and **7.4 MVP feature specs** — follow `references/feature-ideas.md` (quick wins / big bets / fill-ins / skip; a mini-spec with steps, settings, placement, edge cases and a "done when" check for each MVP feature).

