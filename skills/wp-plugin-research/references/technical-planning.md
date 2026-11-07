# Technical analysis & technical plan (Phases 10–11)

Use with the Technical Report template. Cover only what applies to this plugin.

## Phase 10 — Technical analysis (per feature)

**10.1 Feature technical table**

| Feature | WooCommerce/WP areas touched | Hooks / APIs needed | Data storage (options, meta, custom table) | Risk (L/M/H) | Notes |

Areas: products, cart, checkout, orders, emails, My Account, admin, REST API, cron, blocks.

**10.2 Compatibility must-haves:** HPOS, Cart & Checkout Blocks, current PHP/WP/WC versions, multisite if relevant, WPML/Polylang, multi-currency plugins, caching plugins, popular themes and page builders.

**10.2b Modern WooCommerce rules (check each one that applies):**
- Orders only through WooCommerce CRUD (`wc_get_order`, `$order->get_meta()`), never direct post meta — required for HPOS.
- Cart/checkout changes through the **Store API** and Checkout Blocks integration, not only classic `woocommerce_checkout_*` hooks.
- Background and scheduled jobs through **Action Scheduler**, not plain WP-Cron.
- **Full-page cache safe:** nothing user-specific baked into cached pages; dynamic parts loaded separately.
- Emails compatible with WooCommerce's current email system (including the block email editor if enabled).
- Declare compatibility in code (HPOS, Checkout Blocks) and keep "WC tested up to" current.
- Optional: **Abilities API + MCP** for AI-agent access (see 7.1).
- Pass **Plugin Check** and the wordpress.org plugin guidelines (GPL, naming, no hidden tracking, upsell rules).

**10.3 Risks:** which features are most likely to break or cause tickets; use competitors' bug complaints and the code causes found in Phase 9 as a warning list.

**10.4 Performance and security:** load assets only where needed, avoid heavy queries, use caching; capability checks, nonces, sanitize input, escape output, prepared SQL.

**10.5 Third-party APIs** needed by features, with cost/limits.

**10.6 Difficulty:** Easy / Medium / Hard overall, plus estimated build time for MVP and for each later version.

## Phase 11 — Technical plan

- **Use Our Technical Strategy from Phase 9** as the base for every decision below.
- **Model:** Free on wordpress.org + Pro on own site, following the Free/Pro split from 7.2 and the Free/Pro mechanism chosen in Phase 9.
- **Selling/licensing:** Freemius, EDD + Software Licensing, Lemon Squeezy, or WooCommerce Marketplace — pick one, say why.
- **Architecture:** short folder tree (OOP, namespaces, Composer autoload; admin/ frontend/ includes/ assets/ languages/), with **one module per major feature** so features can be switched on/off and Pro can extend Free cleanly. Note if React admin screens or blocks are needed.
- **Settings design:** how settings pages are organized by feature, plus a setup wizard if proposed.
- **Testing:** LocalWP, Query Monitor, Plugin Check, a test store with realistic data, a test checklist per MVP feature (from 7.4), testing on both classic and block checkout, with HPOS on and off, behind a page cache, and alongside common companion plugins. A WordPress Playground blueprint gives a one-click test/demo store.

