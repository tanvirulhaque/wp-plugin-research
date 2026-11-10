# Live check — about 10 minutes, once

My build sandbox can't reach wordpress.org, Google or Reddit, so these collectors
need one real run on your computer. Then paste `live-check-report.md` back into
the chat that maintains the skill. Every check is read-only.

## 0. If everything fails with an SSL error

Python from python.org on macOS ships without trusted certificates. The
scripts fall back to the macOS system certificates automatically. If the
pre-flight still fails with `CERTIFICATE_VERIFY_FAILED`, fix it once with either:
```
pip3 install certifi
open "/Applications/Python 3.X/Install Certificates.command"   # X = your Python version
```
Never turn certificate checks off.

## 1. Scripts (one command, ~2 minutes)

```
cd ~/Sites/wp-plugin-research
python3 tools/live_check.py
```
Checks first that HTTPS works (SSL pre-flight), then: wordpress.org discovery (API), forum titles, reviews with full dates,
Google autocomplete, free-code download, and the code scanner on that download.
It writes `live-check-report.md`.

## 2. Browser collectors (~2 minutes each)

Open Chrome → DevTools (Cmd+Opt+I) → **Console**. Paste the file, press Enter.
Write the result into the "Browser checks" table at the end of the report.

| Check | Open this page | Paste | PASS if |
|---|---|---|---|
| Marketplace reviews | `https://woocommerce.com/products/product-video-for-woocommerce/` (scroll to Reviews) | `skills/wp-plugin-research/scripts/collectors/woo-reviews-return.js`, then run `await $_` if nothing prints | `check.pages` > 1, `check.reviews` ≈ the review count shown on the page, `hasNav: true` |
| Google Trends | First `https://trends.google.com/`, then `https://trends.google.com/trends/explore` | `.../collectors/google-trends.js` | `check.errors` is empty and `timeline` has yearly numbers |
| Demo probe | Any vendor's public demo product page with a video | `.../collectors/demo-probe.js` | `gallery`, `video` and `weight` filled; `weight.scripts` > 0 |

Tip: in the Console, `copy(await $_)` copies the last result so you can paste it.

## 3. Chrome tab saver + Reddit parser (macOS, ~3 minutes)

1. Chrome → View → Developer → **Allow JavaScript from Apple Events** (you turn this on; turn it off again afterwards if you like). The first time, macOS asks "Terminal wants to control Google Chrome" → **OK**. If either is missing, the script stops and says exactly what to do.
   *No-permission alternative:* skip this step, open the page, paste `skills/wp-plugin-research/scripts/userbrowser/save-page.js` into the DevTools console, and move the downloaded file into `/tmp/rd`.
2. Make `urls.txt` with one line:
   `https://old.reddit.com/r/woocommerce/search?q=product+video&restrict_sr=on&sort=new&t=all&limit=100`
3. Run:
   ```
   S=skills/wp-plugin-research/scripts
   bash $S/userbrowser/open_urls.sh urls.txt
   bash $S/userbrowser/save_chrome_tabs.sh old.reddit.com /tmp/rd
   python3 $S/parsers/parse_reddit_search.py /tmp/rd --core video --context "product,store,shop,woocommerce,gallery" --out /tmp/rd.json
   ```
PASS if the tab is saved and the parser reports more than 0 results.

## 4. Reddit API (optional — only if you created a Reddit app)

```
export REDDIT_CLIENT_ID=...   # in your own terminal, never in chat
export REDDIT_CLIENT_SECRET=...
python3 skills/wp-plugin-research/scripts/reddit_collector.py --subs woocommerce --queries "product video" --relevant video --out /tmp/reddit-api.json
```
PASS if it prints "Done: N threads" with N > 0.

## What happens next

Send the report back. Anything that FAILs gets its selectors or parser fixed, and
`references/collectors.md` gets a new "last verified" date for everything that passed.
