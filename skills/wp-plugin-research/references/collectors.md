# Collectors — the collection ladder

**Core rule:** "the fetch tool can't read it" does not mean "the data is not available". Try every rung in order, and record which rung worked for each source in the coverage checklist (`notes.md` → Limits & coverage).

**Never write "only N are public" or "unreachable" after rung 1 or 2.** Say which rungs were tried and why each failed.

## 1. The ladder

| Rung | Method | Use when | Tools |
|---|---|---|---|
| 1 | Public API (curl / Python) | wordpress.org plugin info, download stats, core version | `wporg_discover.py`, Plugins API |
| 2 | Plain HTML fetch + parser | wordpress.org reviews and support forums | `wporg_reviews.py`, `wporg_threads.py` |
| 3 | **In-page collector** in the agent's browser | Data loads by script or in-page pagination (WooCommerce Marketplace reviews, Google Trends, vendor demo pages) | `collectors/*.js` |
| 4 | **User's own browser**: agent opens URLs, the loaded tabs are saved, then parsed | A site blocks the agent's tools but not the user (Reddit, Facebook groups, logged-in tools) | `userbrowser/*.sh`, `parsers/*.py` |
| 5 | **User export or official API with the user's own keys** | A site blocks page scripts too, or needs an account (Keyword Planner CSV, Reddit API) | `parse_keyword_csv.py`, `reddit_collector.py` |
| 6 | Record "not reachable" with the reason | Only after rungs 1–5 | coverage checklist |

## 2. Turn 0 — capability check (about 2 minutes, before research)

Answer these and write them to `notes.md`; then pick a starting rung per source:

1. **Local WordPress?** If the working folder (or a path the user names) is a WordPress install, list `wp-content/plugins/` and match folder names against the keyword list; note the WooCommerce version. Also check `./competitors/`. Anything found goes straight onto the Master List and the code-scan list.
2. **Agent browser?** Can it open pages and run page scripts? Which sites refuse it? If the agent's browser is an extension running **inside the user's own browser** (e.g. Claude in Chrome), rungs 3 and 4 merge: ask the user's OK once before visiting sites that block automated tools, and stay read-only.
3. **User's browser (rung 4)?** Ask once: "Some sources (e.g. Reddit) only open in your own browser. It needs one setting and about 2 minutes. OK to use it?" If yes, give the one-time setup now (section 5).
4. **HTTPS from Python?** On macOS, python.org builds lack certificates; the scripts fall back to the system bundle automatically. If requests still fail with `CERTIFICATE_VERIFY_FAILED`, the user runs `pip3 install certifi` or Python's "Install Certificates.command". Never disable verification.
5. **Python + openpyxl?** If missing, create a venv in the scratch folder (`python3 -m venv .venv && .venv/bin/pip install openpyxl`) or fall back to CSV.
6. **Shell:** do loops in Python, not shell (zsh doesn't word-split `$LIST`), and quote every glob (`--include='*.php'`).

## 3. Rules for every collector

- **Find the real pagination or "load more" control before concluding anything.** Check `nav`, `[rel=next]`, `aria-busy`, buttons, and network requests. A guessed class name that matches nothing is not proof of a single page.
- **Wait on a content-signature change** (e.g. the joined item IDs), not a fixed sleep.
- **Dedupe by item ID.** Pause about 1 second between pages (2–3 s for Google endpoints). **Read-only** — never post, vote, log in, or change anything.
- **Return compact JSON** (counts + rows) to the agent; write the full file to `raw/<source>/`.
- **Self-check:** each collector reports `{pages, total, hasNav}` (or equivalent) so a broken selector shows up as "1 page, no nav" instead of silently returning page 1.
- **Selectors live at the top** of each collector with a "last verified" date. When a collector returns suspiciously little, re-inspect the page before trusting the result.
- **Paraphrase** reviews and posts in reports; raw files are working data, not for publication.

## 4. Source notes (selectors and quirks)

| Source | Rung that worked | Notes | Last verified |
|---|---|---|---|
| wordpress.org Plugins API | 1 | `query_plugins` by `search` **and** `tag`, 2+ pages each; `plugin_information` has no `downloaded` — read it from the search result; a missing slug returns `{"error": ...}` | 2026-11-10 |
| wordpress.org reviews | 2 | `/support/plugin/SLUG/reviews/?filter=N` (N = stars) → topic links → first post; keep the full date with year. Star rating may not be on the page — take it from the `?filter=N` list | 2026-11-10 (packaged script, live) |
| wordpress.org support threads | 2 | `/support/plugin/SLUG/` and `/page/2/`, `/page/3/` — titles are enough for theme counts | 2026-11-10 (packaged script, live) |
| WooCommerce Marketplace reviews | 3 | List `ul.wccom-reviews-comments` (has `aria-busy` while loading), items `li.wccom-reviews-comment`, next `nav.woo-pagination a.page-numbers.next`; full text in `.wccom-read-more__measurement--full`; vendor replies are nested items (keep them, `replyTo` set) | 2026-11-10 |
| Google Trends | 3 | Open the Trends **home page first** (sets cookies), then explore; call `/trends/api/explore` → widget tokens → `/trends/api/widgetdata/multiline`, `relatedsearches`, `comparedgeo` from inside the page; strip the `)]}'` prefix | 2026-11-10 |
| Google autocomplete | 1 | `suggestqueries.google.com/complete/search?client=firefox&q=...` | 2026-11-10 (packaged script, live) |
| Reddit | 4 | Search tool and agent browser refused; `.json` URLs return 403 even logged in. Use `old.reddit.com` search URLs in the user's browser (plain HTML, 100 per page), save tabs, parse. Results: `div.search-result-link[data-fullname]`, `a.search-title`, `time[datetime]`, `.search-score`, `.search-comments`; thread comments in `div.usertext-body div.md` | 2026-11-10 |
| Reddit API | 5 | `reddit_collector.py` with the user's own app keys as environment variables — **untested** | — |
| Vendor demo pages | 3 | `demo-probe.js` on a public demo product page | to verify |
| Keyword volumes | 5 | Trends is an index only. Ask for a Google Ads Keyword Planner CSV → `parse_keyword_csv.py` | — |
| Upwork / Fiverr | 4 (untried) | Try via the user's browser before marking unreachable | — |

**Verifying collectors:** the repo's `tools/live_check.py` (scripts) and `tools/LIVE-CHECK.md` (browser collectors) test each one on a real target; update the "Last verified" column from the report.

## 5. Rung 4 setup (user's browser, macOS + Chrome)

Two routes — offer both and let the user choose:

| Route | Permissions | Works on |
|---|---|---|
| **A. Automatic tab saver** (`save_chrome_tabs.sh`) | The user grants, once: Chrome → View → Developer → **Allow JavaScript from Apple Events**, and macOS "Terminal wants to control Google Chrome" → OK. The script checks both first and stops with instructions if one is missing. | macOS + Chrome |
| **B. Console saver** (`save-page.js`) | **None** — the user pastes it in the DevTools console on each page; it downloads the page HTML | Any Chrome-based browser, any OS |

The agent must **ask**, never change these settings. The user can switch the Chrome setting off again afterwards.

Then:
1. Build the URL list (old-Reddit search URLs: `https://old.reddit.com/r/SUB/search?q=PHRASE&restrict_sr=on&sort=new&t=all&limit=100` for each subreddit × phrase from the keyword list; skip site-wide "new" searches — they return noise).
2. `bash scripts/userbrowser/open_urls.sh urls.txt` — opens them in the user's Chrome.
3. `bash scripts/userbrowser/save_chrome_tabs.sh old.reddit.com raw/reddit/search` — saves each matching tab's loaded HTML (route A), **or** the user pastes `scripts/userbrowser/save-page.js` into the console on each tab and moves the downloads into `raw/reddit/search` (route B).
4. `python scripts/parsers/parse_reddit_search.py raw/reddit/search --core video --context "product,store,shop,woocommerce,gallery"` → filtered results.
5. Open the on-topic threads the same way, save, then `parse_reddit_thread.py`.

**Windows / Linux / other browsers:** use route B, or save each page with Ctrl/Cmd+S → "Webpage, HTML only" into `raw/<source>/`. The parsers read all of these the same way.

The same route works for Facebook groups, Stack Overflow (if blocked) and logged-in keyword tools.

## 6. Boundaries (keep these)

- Read-only, rate-limited, public pages only. Paraphrase reviews.
- If a site blocks the agent's own tools, do **not** route around it with another agent tool. Use the user's browser with their consent (rung 4) or an official API with their keys (rung 5).
- The agent never changes browser security settings and never types credentials. The user does both; API keys go into environment variables in the user's own terminal, never into chat.
- No nulled, reseller or "GPL club" copies of paid plugins.
- Subagents: fine for vendor pricing pages and security history; keep reviews, forums and code in the main session with scripts. Subagents must report what was blocked.
