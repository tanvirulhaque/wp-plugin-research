# Changelog

All notable changes to this project are listed here. Versions follow [Semantic Versioning](https://semver.org/).

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
