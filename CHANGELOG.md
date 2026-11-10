# Changelog

All notable changes to this project are listed here. Versions follow [Semantic Versioning](https://semver.org/).

## [1.2.0] — 2026-11-10
From a real run ("Product Video for WooCommerce", Claude Code on macOS).
### Added
- **Collection ladder** (`references/collectors.md`): API → HTML parser → in-page collector → the user's browser (with consent) → user export / own-key API → "not reachable". Never "unreachable" after rung 1–2. Collector rules (find real pagination, wait on content change, dedupe, self-check, dated selectors) and per-site notes.
- **Turn 0 capability check**: local WordPress plugins, agent browser, user's browser consent, Python/openpyxl.
- Collectors: `woo-reviews-scraper.js` (user's console script) + `woo-reviews-return.js` (agent version with self-check), `google-trends.js`, `demo-probe.js`.
- User browser: `open_urls.sh`, `save_chrome_tabs.sh`; parsers `parse_reddit_search.py` (with relevance filter) and `parse_reddit_thread.py`.
- Scripts: `wporg_discover.py` (keywords × pages + tags, newcomer metric, error handling), `wporg_reviews.py` (low-star + newest 5★, full dates), `wporg_threads.py` (thread-title theme counts), `scan_signals.py` (niche signals across every plugin), `autocomplete.py`, `parse_keyword_csv.py`, `reddit_collector.py` (untested), `merge_research.py` (idempotent rebuild, stable review IDs).
- Pro-without-the-zip probes (demo page, Pro changelog/docs, Free-code hooks, forums) and a core-overlap check.
- Analytics: standard newcomer metric (24 months, 100 / 1,000 installs), supply-side trend, Trends reading rules, review-export stats, thread-mining-first pain ranking, direct/marketplace customers in the forecast.
### Changed
- Phase 2 looks locally first and discovers wide (keywords + tags, 2+ pages).
- Code request moves to the **end of turn 1**, with prices and what each purchase adds.
- End-of-turn-1 message names the deep plugins and the exact-name match, the rung per source, and what's missing.
- "Nobody does X" claims must cite the all-plugin scan ("of N scanned").
- Reports: ask Claude Docs or files once; files by default in a local code project.
- `build_workbook.py` falls back to CSV without openpyxl; Forecast has a direct-customers input.
- `check_skill.py` also checks pointers to subfolders and .js/.sh files.
### Verified
- No-loss audit against v1.1.0: every instruction present (one row expanded on purpose).
- Review collector tested on a simulated paginated page (3 pages, 7 reviews + 1 reply); parsers, merge (idempotent re-runs), scanner, workbook (0 errors) all pass.
- Google Trends collector (incl. multi-keyword regions) and demo probe tested against mocked responses / a simulated page; collector tests run in CI.
- **Live script check on macOS: 7 of 7 passed** (SSL pre-flight, wporg_discover, wporg_threads, wporg_reviews, autocomplete, fetch_code, analyze_plugin).
- Still to verify live: browser collectors (agent review collector, Trends, demo probe), Chrome tab saver, Reddit API.
### Fixed after the first live check on macOS
- **SSL on macOS (python.org Python has no certificates):** all scripts now share one HTTPS setup — Python's default store if it has certificates (keeps company-proxy certificates working), else the OS bundle (`/etc/ssl/cert.pem` on macOS), else `certifi`. Verification is never disabled. Tested with a simulated certificate-less Python.
- SSL failures are reported clearly with the one-line fix, instead of a silent "no response".
- `fetch_code.py` keeps trying the GitHub mirrors after an SSL or network error on one source.
- `reddit_collector.py` uses the same HTTPS setup.
- `tools/live_check.py` starts with an SSL / network pre-flight and tells you whether the problem is certificates or connectivity.

- `wporg_reviews.py`: the star rating wasn't found on review pages in the live check; it now tries more page patterns and otherwise uses the `?filter=N` value the review came from (exact), with `stars_source` recorded.

- `save_chrome_tabs.sh` checks Chrome's "Allow JavaScript from Apple Events" and the macOS Automation permission **before** saving, and stops with exact instructions instead of failing on every tab.
- New `save-page.js`: saves the current page with **no permissions** — any Chrome-based browser, any OS.

### Maintenance
- SKILL.md slimmed from 4,015 to 3,588 words: Phase 6–7 tables moved to `references/feature-analysis.md` (no-loss audit: 0 lines lost).
- `tools/live_check.py` + `tools/LIVE-CHECK.md`: one-command live test of the network collectors and a 10-minute browser checklist, producing a report to paste back.

### Fixed during review
- Review Log IDs explained (R01 when appended, stable R-xxxxxx when rebuilt).
- Forecast: drafted in turn 1, finalized in turn 2; includes direct / marketplace customers. Default direct customers = 0 (nothing invented).
- Pain ranking starts from support-thread title counts.
- Phase 9 "collect code" split into clear steps.
- Browser extensions inside the user's own browser (e.g. Claude in Chrome): rungs 3 and 4 merge — ask once before visiting sites that block automated tools.
- `save_chrome_tabs.sh`: removed a pre-check that could falsely report "no tabs" with several windows.
- `google-trends.js`: regions now correct per keyword when comparing several keywords.
- Decision Summary shows the newcomer metric.

## [1.1.0] — 2026-11-08
Improvements from 3 real test runs, a skill-creator review, and a no-loss audit against v1.0.0.

### Added
- **Run plan** (`references/run-plan.md`): 2–3 planned turns with checkpoints (`research.json` + `notes.md`), a resume rule, per-phase call budgets that plan turns without cutting data, **Lite mode**, and a coverage checklist.
- **Sources guide** (`references/sources.md`): pre-flight access check, search-then-fetch rule, page-size limits, fallback chain when wordpress.org is blocked (plugin pages, trackers, jsDelivr readme, GitHub mirrors), dead-vendor rule, piracy blocklist, and rules for vendor pages, conflicting numbers, duplicates and review spread.
- **Claude Docs mode**: create docs at the start of the reporting turn, one doc with Summary · Research · Technical tabs, grouped writes, words instead of emoji.
- Scripts: `fetch_code.py` (free code via wordpress.org or GitHub mirrors, with version check), `add_row.py` and `assets/research-template.json`.
- Workbook sheets: Health_Metrics, Demand_Proxy, Pricing_Benchmarks, Final_Feature_Set, Forecast and Verdict (formula-driven).
- Analytics: metric fallback map, demand proxy score, paid-user thresholds for small niches, band-floor rule.
- Maintainer tools: `tools/check_skill.py` (SKILL.md size, pointers, orphans, phases; runs in CI) and `tools/check_no_loss.py` (no instruction lost vs an older version).
- 2 new eval cases (Lite mode, turn-1 checkpoint) and a scanner test fixture.

### Changed
- `analyze_plugin.py`: definite third-party folders (vendor, node_modules, Freemius, Action Scheduler, update checkers) counted separately; `lib/`, `sdk/` and similar still analyzed and listed for a human check; readme.txt headers merged; React detection includes .tsx/.jsx; more Store API / Blocks patterns; caching, telemetry, hot-path cart work and admin vs front-end splits (old totals kept); delegated WC_AJAX security noted; `--quiet` and broken-pipe safety.
- `compare_code.py`: "not found in this code" instead of ❌ for declarations; rows for bundled code, caching, hot path and telemetry.
- The Final Decision Summary owns the decision (with 3 reasons for and 3 against); the Research Report no longer repeats it.
- Code request also lists free plugins whose download was blocked, and is sent at the end of turn 2.
- AI-agent feature idea requires checking competitors' code for `wp_register_ability` first.
- Description updated to match the real output; code collection and data-quality rules each written once.

### Verified
- Every v1.0.0 instruction still present (reworded or moved, never dropped).
- Scanner gives the same hooks, entry points, security and compatibility values as v1.0.0 on a real plugin.
- Workbook keeps every v1.0.0 sheet, column and row; 0 formula errors.

## [1.0.0] — 2026-11-07
### Added
- 5-stage research workflow (Find → Collect → Analyze → Plan → Decide) for WordPress/WooCommerce plugin ideas.
- 4 deliverables: Final Decision Summary, Research Report (Decision Page first), Technical Report, Research Workbook (.xlsx).
- Analytics playbook (wordpress.org metrics, market structure, TAM/SAM/SOM, revenue forecast, thresholds).
- Competitor codebase analysis (15 lenses) with `analyze_plugin.py` and `compare_code.py`.
- Evidence workbook builder `build_workbook.py` with ID links and editable scorecard.
- Portability guidance for Claude, ChatGPT, Gemini, Codex, Cursor, Copilot.
- 3 eval test cases.
- SKILL.md kept within the spec's recommended size; details live in `references/`.
