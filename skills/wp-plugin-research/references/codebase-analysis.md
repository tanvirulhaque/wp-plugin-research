# Competitor Codebase Analysis — How They Really Solve It

Read this before the Codebase phase. Goal: look behind the scenes of the top competitors to learn **how** they solve the problem, **where** their code is strong or weak, **how** they split Free and Pro, and turn that into **our own technical strategy**.

## Contents
1. Rules (legal & ethical)
2. Which plugins to analyze
3. How to get the code
4. Step-by-step reading method
5. The 14 analysis lenses
6. Linking user complaints to code causes
7. Code Card format
8. Comparison & our technical strategy
9. Limits

---

## 1. Rules (legal & ethical)

- **Free versions** on WordPress.org are GPL and public. Downloading, reading and studying them is fine.
- **Pro versions:** the user purchases them and shares the code, so analyze them fully — they reveal the real money features and the Free/Pro locking mechanism. **Never** use nulled/pirated copies; besides being wrong, nulled files often contain malware.
- **Learn, don't clone.** GPL allows reuse with credit, but the goal is to understand patterns and write our own better solution. Don't copy brand names, docs text, images or UI design.
- Don't publish the competitor's code or private details in the report — describe the approach in your own words, with short file/function references.

## 2. Which plugins to analyze

Pick **2–4** from the deep-research shortlist:
- the market leader,
- the best-rated or fastest-growing plugin,
- one with many complaints (to learn what goes wrong),
- optionally an open-source plugin on GitHub with public issues/PRs.

## 3. How to get the code

**Free versions — get them yourself:**
- WordPress.org: `https://downloads.wordpress.org/plugin/SLUG.zip` (version history: `https://plugins.svn.wordpress.org/SLUG/`)
- GitHub (if the seller publishes it): `https://codeload.github.com/OWNER/REPO/zip/refs/heads/BRANCH` — issues and pull requests show real bugs and fixes.
- If the environment blocks the download, add the plugin to the user request instead.

**Pro versions — ask the user, once.** Use this format:

```
📦 Pro code request — I can't download these paid versions. Please share the ones you can:
1. [Plugin] Pro — why: [e.g. market leader, see how Pro features are locked]
   Pricing: [link] (cheapest license is enough)
2. ...
Share as: a local folder path (Claude Code / Cowork) or upload the .zip files here.
Any you don't share, I'll skip and use the rest.
```

Send one Pro code request listing each Pro plugin, why its code matters, and its pricing page (cheapest license is usually enough). The user buys them and shares:
1. **Local folder path** (Claude Code / Cowork) — read directly, e.g. `~/plugins-research/[slug]-pro/` or a local test site's `wp-content/plugins/`.
2. **Uploaded zips** (Claude.ai) — in `/mnt/user-data/uploads/`; unzip each into the working folder first.

Tips for the user: Free and Pro in separate, clearly named folders/zips (`leader-free.zip`, `leader-pro.zip`); latest versions; an older version too is a bonus.

**Missing Pro code — skip, don't block:**
If the user doesn't share a Pro plugin, skip it without asking again. Analyze everything available, and in the report list which Pro versions weren't analyzed. For those, base Free/Pro findings on the Free code plus the public Pro feature list, and label them "not code-verified".

## 4. Step-by-step reading method

Big plugins have tens of thousands of lines. Don't read everything — map first, then read the important parts.

1. **Map:** run `python scripts/analyze_plugin.py <zip_or_folder> --json out.json`. It lists: header (versions, requirements), size, largest files, WooCommerce hooks used, hooks offered to developers, REST/AJAX/cron entry points, data storage (options, meta, custom tables), HPOS/Blocks declarations, Free/Pro and licensing signals, security and performance signals, architecture style.
2. **Find the main file** (has the "Plugin Name:" header) → follow how it boots (autoloader, main class, init hooks).
3. **Trace the core feature:** pick the plugin's main job (e.g. "apply wholesale price") and follow it from the hook into the logic and back to the output. Write the flow as 4–8 simple steps.
4. **Trace 2–3 edge cases** that users complain about (variable products, coupons, taxes, multi-currency, block checkout).
5. **Check the flagged files** from the script (raw SQL, superglobals, unlimited queries, largest files).
6. **Read the changelog + GitHub issues** for recurring bug types and how they were fixed.
7. **Optional, in the user's local setup:** run Plugin Check on each competitor (`wp plugin check SLUG` with WP-CLI on a local test site) for a quick, objective quality and guideline report.

## 5. The 15 analysis lenses

| # | Lens | What to look for | Why it matters to us |
|---|---|---|---|
| 1 | Architecture | Folder structure, OOP vs procedural, namespaces, autoloading, main class, modules | Shows maintainable vs messy design |
| 2 | Boot & loading | What loads on every page vs only when needed | Speed |
| 3 | Core solution logic | Step-by-step flow of the main feature; which WC hooks/filters it relies on | Learn the proven approach, spot fragile spots |
| 4 | Data model | Options, post/order meta, custom tables, transients; autoloaded options | Scalability and HPOS readiness |
| 5 | WooCommerce integration | Hooks used, CRUD objects (`$order->get_meta`) vs direct post meta, Store API / Checkout Blocks integration, HPOS declaration | Modern compatibility gaps = our edge |
| 6 | Edge-case handling | Variable products, taxes, coupons, multi-currency, guest checkout, refunds | Where competitors break |
| 7 | Free vs Pro mechanism | One plugin with locked code? Separate Pro add-on plugin extending Free via hooks? Freemius `__premium_only` code stripping? How Pro checks run (`class_exists`, constants, license) | Choose our own Free/Pro architecture |
| 8 | Licensing & updates | Freemius, EDD Software Licensing, custom server; how updates are delivered | Pick our selling stack |
| 9 | Upsell & UX placement | Where upgrade prompts appear (notices, locked settings, menus) and how pushy | Learn conversion tactics without annoying users |
| 10 | Extensibility | Hooks they offer, templates that themes can override, REST endpoints, WP-CLI | Developer ecosystem = loyalty |
| 11 | Security | Nonces, capability checks, sanitize/escape, prepared SQL, ABSPATH guards; vulnerability history | Avoid their mistakes; "security-first" marketing |
| 12 | Performance | Assets loaded globally, heavy queries (`-1` limits), queries inside loops, missing caching | "Faster" is a strong selling point |
| 13 | Code quality & tech debt | Huge files (>1,500 lines), duplicated code, old jQuery-only admin, outdated PHP patterns, tests/CI presence, coding standards | Shows how fast they can improve — slow movers are beatable |
| 14 | Admin UI tech | PHP settings forms vs React / WordPress components; settings structure | Our UX advantage |
| 15 | Modern-WC & AI readiness | Store API / Checkout Blocks integration, Action Scheduler vs WP-Cron, full-page-cache safety, Abilities API (`wp_register_ability`) and MCP exposure | Shows who is ready for where WooCommerce is going |

Score each lens **Strong / OK / Weak** with one line of evidence (file or function name).

## 6. Linking user complaints to code causes

This is where the codebase pays off most. For each top complaint from the gap analysis, find the probable code cause:

| User complaint | Probable code cause (file/function) | How our design avoids it |
|---|---|---|
| "Breaks with block checkout" | Only classic `woocommerce_checkout_*` hooks; no Store API integration | Build on Store API + blocks integration from day one |
| "Slows down my shop" | Scripts enqueued on every page; meta queries on each product load | Conditional loading, cached rule lookups |

Mark each as **confirmed** (seen in code) or **likely** (inferred).

## 7. Code Card format

```
### Code Card — [Plugin] v[version]
- Source: wp.org zip / GitHub (link) / user upload
- Size: X PHP lines, Y files; largest files: ...
- Requirements: PHP x, WP x, WC x; tested up to ...
- Architecture: ...
- Core solution flow: 1) ... 2) ... 3) ...
- Data storage: ...
- WooCommerce: HPOS ✔/✘, Checkout Blocks ✔/✘, hooks relied on: ...
- Free vs Pro mechanism: ...
- Licensing/updates: ...
- Extensibility: N hooks offered, templates overridable ✔/✘, REST ✔/✘
- Security: Strong/OK/Weak — evidence
- Performance: Strong/OK/Weak — evidence
- Code quality & tech debt: ...
- Lens scores (15): ...
- Learn from them (good ideas): ...
- Avoid (their mistakes): ...
```

## 8. Comparison & our technical strategy

1. **Comparison table:** lenses as rows, analyzed plugins as columns, Strong/OK/Weak.
2. **Patterns everyone uses** (proven approach — probably adopt).
3. **Weaknesses everyone shares** (best opportunities).
4. **Our technical strategy** — decisions with reasons:
   - Architecture & modules
   - Data model (meta vs custom tables; HPOS-safe CRUD only)
   - Core logic approach (which hooks / Store API)
   - Free/Pro mechanism (e.g. Free plugin + Pro add-on extending through our own hooks)
   - Licensing & update stack
   - Performance plan (what loads where, caching)
   - Security standard
   - Extensibility plan (hooks, templates, REST, WP-CLI)
   - Admin UI tech
   - Testing & quality (PHPUnit, coding standards, CI)
5. **Tech-based differentiators** to feed back into features and marketing (e.g. "works with block checkout", "50% fewer queries", "developer-friendly hooks").

## 9. Limits

- Static reading can miss runtime behaviour; say "likely" when unsure.
- Pro-only logic may be invisible if only the Free version is available — state this.
- Large codebases: analyze the core feature path deeply and the rest at map level.
