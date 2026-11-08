# Feature idea sources (Phase 7.1)

Propose 8–15 features that no competitor offers or that are done badly everywhere — these are what make users switch. Use these idea sources:
- Top-ranked opportunities from the scorecard (6.8), plus gaps and repeated requests (6.4, 6.5)
- Fixes for the biggest complaints (setup too hard, too slow, confusing)
- Better UX: setup wizard, ready-made templates/presets, live preview, plain-language rules
- Modern WooCommerce: full Checkout Blocks support, HPOS, block editor blocks, REST API
- Smart / AI help where genuinely useful (e.g. suggested rules, auto-generated text) — only if it solves a real problem
- **AI-agent ready:** register the plugin's key actions as WordPress Abilities (Abilities API, in WordPress core since 7.0) with MCP metadata, so store owners' AI assistants can use the plugin through the MCP Adapter. Before proposing it as new, check competitors' code for `wp_register_ability` (the scanner's `abilities_api` signal) and their changelogs — if a leader already ships it, it is a must-have, not a differentiator
- **Try-before-install demo:** a WordPress Playground live demo (opens a ready-made test store in the browser) linked from the wordpress.org page and sales page
- Reports and insights showing store owners the money the plugin made them
- Integrations with popular tools in this niche (email marketing, CRM, ERP, shipping, payments, page builders)
- Migration tool: "import settings from [abandoned/popular competitor]"
- Features for each user type from Phase 1 (e.g. agency: multisite, white-label, export/import settings)
- Developer extras: hooks, filters, REST endpoints, WP-CLI commands



# Feature planning details (Phases 7.3–7.4)

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

