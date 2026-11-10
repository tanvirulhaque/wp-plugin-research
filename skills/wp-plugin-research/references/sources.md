# Sources — how to reach data, fallbacks, and quality rules

This file covers **where** to look and **quality rules**. **How** to collect when a tool can't read a page — the collection ladder, in-page collectors, the user's browser — is in `collectors.md`. Do loops in Python, not shell, and quote every glob.

## 1. Pre-flight check (start of Phase 2)

If the agent can run shell commands, test access once:
```
curl -s -m 10 -o /dev/null -w "%{http_code}" "https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[search]=test"
curl -s -m 10 -o /dev/null -w "%{http_code}" -I "https://downloads.wordpress.org/plugin/woocommerce.zip"
curl -s -m 10 -o /dev/null -w "%{http_code}" -I "https://codeload.github.com/WordPress/wordpress-develop/zip/refs/heads/trunk"
```
200 → use it. Anything else → switch to the fallback chain now, not mid-run. Note the result in `notes.md`.

Also do these early, required searches: current WordPress version, current WooCommerce version (official release posts), live WooCommerce store count (record a range if sources disagree).

## 2. Search first, then fetch

Many agents can only fetch URLs that appeared in search results (typed or constructed URLs are rejected, and even links inside fetched pages may be). So every URL below is a **search target**, not a link to type:

| Need | Search query that surfaces it |
|---|---|
| Plugin page | `site:wordpress.org/plugins [slug]` or `"[plugin name]" wordpress.org plugin` |
| Low-star reviews | `"[slug]" reviews wordpress.org support` → fetch the reviews page, then its `?filter=1` and `?filter=2` versions if allowed |
| Readme + changelog | `jsdelivr wp plugins [slug] readme.txt` (cdn.jsdelivr.net/wp/plugins/SLUG/trunk/readme.txt is a clean mirror) |
| Tracker stats | `plugintracker [plugin name]`, `pluginsdb [plugin name]`, `plugins.wpmayor.com [plugin name]` |
| Pricing | `[plugin name] pricing` |
| CodeCanyon | `codecanyon [plugin name]` → open the **item page** (has sales count), never the search page |
| Reddit | `site:reddit.com/r/woocommerce [keyword]` (or put "reddit r/woocommerce" in the query if `site:` is ignored) |
| Security history | `[plugin name] vulnerability patchstack` / `wpscan [slug]` |

- If `site:` is ignored by the search tool, put the domain name in the query instead.
- Budget ~2 calls per plugin per page type. If a page isn't found, write "not found" and move on.
- **Limit page size:** where the fetch tool allows it, cap text at ~1,500–3,000 tokens for listing, review and tracker pages (they are mostly menus). Prefer item pages over search pages (a CodeCanyon search page can be ~15K tokens).
- Write findings into `research.json` right after each fetch.

## 3. Fallback chain when wordpress.org is blocked

| Data | Try in order |
|---|---|
| Installs, rating, reviews count, last update, tested-up-to | wordpress.org plugin page via search → localized wordpress.org pages (e.g. de., id., te. — same data) → PluginTracker / PluginsDB / Plugin Pulse |
| Star breakdown, support % resolved | Plugin page "Ratings" and "Support" boxes → tracker pages |
| Downloads trend / momentum | PluginTracker or Plugin Pulse trend → mark "?" |
| Plugin age (date added) | Tracker page → first version in the changelog → earliest review date |
| Readme, changelog, requirements | jsDelivr readme (via search) → plugin page tabs |
| Free code | GitHub mirrors via `scripts/fetch_code.py SLUG` (tries `WordPressBugBounty/plugins-SLUG` and `common-repository/SLUG`, branches master/main/trunk, on codeload.github.com) → add to the user's code request |
| HPOS / Checkout Blocks status | Code scan → WooCommerce Marketplace "Compatibility" box → changelog lines → "?" |

- Don't use the GitHub search API first (it rate-limits fast); try known mirror names directly.
- **Verify mirrors:** compare the plugin header `Version` with the stable version on wordpress.org; mirrors can lag (e.g. v2.0 vs live v3.0). Record the mirror and version in Limits.

**Dead vendor rule:** if a vendor site is gone or redirects (acquisition), search the new owner's docs (e.g. "[product] docs [new owner]") and archive.org snapshots of the product page.

## 4. Source quality rules

- **Piracy blocklist — never use or cite:** pages with "nulled", "free download" of a paid plugin, "GPL club / GPL vault / GPL times"-style resellers, look-alike domains (e.g. codecanyonfree…), and `/wp-content/` file hosting of a paid plugin on unrelated domains (including hacked university or government subdomains).
- **Vendor-written comparisons:** a vendor's own "best plugins" or comparison page is usable for **its own** prices and features only — never as evidence of competitor weaknesses.
- **SEO articles about Reddit/forums don't count** as community evidence; only real threads do.
- **Conflicting numbers:** prefer the newest dated source, record both values, and flag the conflict in the workbook (e.g. "35 vs 67 reviews — tracker vs mirror").
- **Duplicate URLs:** wordpress.org returns the same plugin under `?p=…`, localized subdomains and others — dedupe by the canonical slug.
- **Pain evidence spread:** collect reviews from at least 3 plugins before scoring pain strength, so one product's forum doesn't skew it.
- **Rounded installs:** wordpress.org shows bands ("10,000+"). Use the band floor for share math and label results as estimates.

## 5. Discovery sources (Phase 2)

Cover every row. For wordpress.org, run `scripts/wporg_discover.py` with every keyword **and** tag, 2+ pages each, before any web search.

| Source | How to search |
|---|---|
| WordPress.org | "site:wordpress.org/plugins [keyword]". If the pre-flight check passed, the Plugins API returns installs, ratings and dates for many plugins in one call (see `analytics-playbook.md` §1); otherwise use the fallback chain |
| WooCommerce Marketplace | "site:woocommerce.com/products [keyword]" |
| CodeCanyon | "codecanyon woocommerce [keyword]" to find items → open each item page (sales count, price); avoid search pages |
| "Best plugin" lists | "best woocommerce [keyword] plugins [current year]" — open 2–3 articles |
| Independent sellers | "[keyword] plugin pricing" (YITH, WebToffee, Barn2, StoreApps, Iconic, WPFactory, ThemeHigh, etc.) |
| Communities | Reddit: search tools and agent browsers are usually refused — use rung 4 (the user's browser, `collectors.md` §5); r/woocommerce, r/WordPress, "which plugin for [job]", wordpress.org support forums, WooCommerce community, Facebook groups (rarely indexable — use if the user shares posts) — real threads only, not SEO articles about them |
| GitHub (optional) | Open-source alternatives |
| Theme built-ins & suites | Popular WooCommerce themes (e.g. WoodMart, Flatsome, Astra/Kadence add-ons) and multi-feature suites often include this feature — they are competitors too, and their users' complaints are evidence |
| User's own products | If the user sells related plugins, search their support forums and reviews for requests about this idea |
| Market events | Acquisitions, rebrands, price changes, plugins being merged into suites (e.g. "[plugin] acquired", "[plugin] discontinued") — these create switching windows |

