# Analytics Playbook — Numbers That Drive the Decision

Read this before PHASE 5 (Analytics). It lists every metric to collect, where to get it, how to calculate it, and how to read it. Explain each number to the user in one plain sentence ("This means…"). Label every estimate as an estimate and show the math.

## Contents
1. Data sources
2. Plugin health metrics (per competitor)
3. Market structure metrics (whole niche)
4. Demand metrics
5. Revenue metrics and forecast
6. Sentiment & support metrics
7. Risk metrics
8. Competitor marketing metrics
9. Decision thresholds & red flags
10. Opportunity Dashboard format

---

## 1. Data sources

| Source | What it gives | How |
|---|---|---|
| WordPress.org Plugins API — search | Many plugins at once: active_installs, downloaded, rating, ratings (1–5★ counts), num_ratings, support_threads, support_threads_resolved, last_updated, added, version, tested, requires_php | `https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[search]=KEYWORD&request[per_page]=50` (public, no key) |
| WordPress.org Plugins API — one plugin | Same fields + sections (description, changelog, FAQ) | `https://api.wordpress.org/plugins/info/1.2/?action=plugin_information&request[slug]=SLUG` |
| WordPress.org download stats | Daily downloads history | `https://api.wordpress.org/stats/plugin/1.0/downloads.php?slug=SLUG&limit=365` |
| Plugin Pulse (plugins.wpmayor.com) | Estimated install trend, 30-day downloads, directory search rank, health score, compare pages | Search "plugins.wpmayor.com [plugin name]" |
| Store Leads / BuiltWith / Wappalyzer | Number of live WooCommerce stores; which live sites use a competitor plugin (when detectable); countries/industries | Public trend pages and reports |
| Google Trends | 5-year search interest trend | Search the keyword list |
| Keyword tools (Ahrefs/Semrush/Ubersuggest free tiers) | Search volume, keyword difficulty | Use whatever is reachable; otherwise say "not available" |
| CodeCanyon | Sales count, price, launch date, rating, comments | Item page |
| Similarweb / Ahrefs free checkers | Competitor website traffic and top keywords | Estimates only |
| Patchstack / WPScan / Wordfence Intelligence | Security vulnerability history per plugin | Search "[plugin] vulnerability patchstack" |
| Freemius / industry benchmarks | Conversion, churn, renewal benchmarks | See section 5 |

If the API cannot be reached (blocked network), use the fallback chain in `sources.md` and the metric fallback map in §2b, and say which source was used. Remember most fetch tools only open URLs that appeared in search results — search for each page first.

Important background: WordPress.org removed its public "active install growth" chart in 2022, so install growth must be estimated from download trends and third-party trackers. Active installs are shown in rounded bands (e.g. "10,000+"), so treat them as ranges.

---

## 2. Plugin health metrics (fill one row per competitor)

| Metric | Formula | How to read it |
|---|---|---|
| Active installs | from API | Size of user base (rounded band) |
| Age | today − `added` (years) | Older = more trust, but often older code |
| Install velocity | active_installs ÷ age in years | Installs gained per year. Compare: a young plugin with high velocity is a rising threat |
| Momentum | last 30 days downloads ÷ previous 30 days | >1.1 growing, 0.9–1.1 flat, <0.9 shrinking. Release weeks spike downloads — compare periods with similar release activity |
| Retention signal | active_installs ÷ downloaded | Rough share of downloads that stayed installed. Older and frequently-updated plugins read lower, so compare plugins of similar age |
| Update cadence | number of releases in last 12 months (changelog) | 0 = abandoned, 1–4 = slow, 5+ = active |
| Days since update | today − last_updated | >365 = abandoned → switching opportunity |
| Compatibility lag | current WP version − `tested` | Lagging versions = neglected product |
| Rating | rating ÷ 20 (API gives 0–100) | Out of 5 |
| Negative review share | (1★ + 2★) ÷ num_ratings | >15% = many unhappy users |
| Review rate | num_ratings ÷ active_installs × 1000 | Reviews per 1,000 installs — shows how engaged users are |
| Support resolution rate | support_threads_resolved ÷ support_threads (last 2 months) | <50% = weak support → opportunity |
| Support load | support_threads ÷ (active_installs ÷ 1000) | Threads per 1,000 installs — high = complex or buggy product (warns you about support work) |
| Modern compatibility | HPOS ✔/✘, Checkout Blocks ✔/✘ | ✘ = big gap you can fill |

### 2b. Metric fallback map (when the API is blocked)

Use these instead of leaving "?" everywhere:

| Metric | Fallback source / method |
|---|---|
| Active installs | Plugin page band ("10,000+") → tracker page |
| Age | Tracker "added" date → first version in changelog → earliest review date (label as estimate) |
| Install velocity | Band floor ÷ age (estimate) |
| Momentum | Tracker trend (PluginTracker / Plugin Pulse, e.g. 13-week download average) → "?" |
| Retention signal | Skip if no `downloaded` count (say so) |
| Negative review share | Plugin page star breakdown → count 1–2★ on the reviews pages |
| Review rate | Review count ÷ band floor × 1000 (estimate) |
| Support resolution | Plugin page "issues resolved in last two months" box → tracker support % |
| Update cadence | Changelog entries in the last 12 months |
| HPOS / Blocks | Code scan → Marketplace "Compatibility" box → changelog lines |

---

## 3. Market structure metrics (whole niche)

| Metric | Formula | How to read it |
|---|---|---|
| Total niche installs | sum of active_installs of all Master List plugins (use band floors; label as estimate) | Proven reachable market |
| Paid users (small niches) | WooCommerce Marketplace installs/stores + CodeCanyon sales + known Pro customer counts | Many single-feature niches are small in free installs but healthy in paid users — count both |
| Leader share | leader installs ÷ total niche installs | >60% = one dominant player |
| Top-3 share | top 3 installs ÷ total | >80% = concentrated market |
| Concentration verdict | combine with leader's satisfaction | Concentrated + leader loved = hard. Concentrated + leader disliked/outdated = one big switching target (good) |
| New-entrant success | plugins added in last 3 years that reached 1,000+ installs | 0 = newcomers struggle; several = market is open |
| Abandoned share | plugins with no update in 12+ months ÷ all plugins | High = users left behind, switching opportunity |
| Paid share | paid or freemium plugins ÷ all plugins | High = users already used to paying |
| Platform context | live WooCommerce store count and its year-over-year trend (Store Leads) | A shrinking platform means growth must come from winning share, not from new stores. Check the current figure; it changes quarterly |
| Niche share of stores (estimate) | total niche installs ÷ live WooCommerce stores | How common this need is among stores |

**Market sizing (TAM / SAM / SOM)** — label all as estimates and show the math:
- **TAM (total market):** live WooCommerce stores that could need this × average yearly price. Use store-type data (e.g. share of B2B stores, stores in a country) when the niche is narrower.
- **SAM (reachable market):** the part of TAM you can actually serve — your language, regions, store sizes and use case. A good proxy is total niche installs plus stores asking for it without a plugin.
- **SOM (what you can win in 2–3 years):** a realistic share of SAM, based on what recent newcomers achieved (new-entrant success above). Usually small — say 1–5% of SAM.

---

## 4. Demand metrics

| Metric | Source | How to read it |
|---|---|---|
| Monthly search volume per keyword | keyword tool | Bigger = more people looking |
| Keyword difficulty | keyword tool | High = hard to rank, plan more marketing |
| 5-year trend | Google Trends | Rising / flat / falling |
| Directory search rank | search wordpress.org or Plugin Pulse for each keyword | Who owns the top 5 results for each keyword — they get most free installs |
| Community question count | Reddit/Facebook/forum threads in last 12 months | Ongoing pain = steady demand |
| Freelance job count | Upwork/Codeable searches | People paying for custom solutions = willingness to pay |
| Feature request count | support forums + reviews | Which features users ask for most (feeds Phase 6) |

### 4b. Demand proxy score (when no keyword or trend tool is available)

Score each signal 0–2 and add them up (max 10):

| Signal | 0 | 1 | 2 |
|---|---|---|---|
| Plugins in the niche (Master List) | < 5 | 5–15 | > 15 |
| Leader's installs or paid users | < 5,000 | 5,000–50,000 | > 50,000 |
| New entrants in the last 3 years with 1,000+ installs or 500+ sales | 0 | 1 | 2+ |
| Community threads asking for it (last 12 months, real threads) | < 3 | 3–10 | > 10 |
| Freelance jobs / custom-work requests | none found | a few | many |

**0–3 = Low · 4–6 = Medium · 7–10 = High.** Show the table in the workbook so the user can check it. If keyword data *is* available, use it and keep the proxy as a cross-check.

---

## 5. Revenue metrics and forecast

**Competitor revenue signals**
- CodeCanyon: sales × price = lifetime gross (estimate; ignores discounts and fees). Divide by months since launch = average monthly sales.
- Freemium estimate: active_installs × conversion rate × average yearly price.

**Benchmarks to use (cite them, and say they are averages, not guarantees)**
- Free → paid conversion for freemium WordPress products is low: Freemius reported about 1.5% average free-to-paid for products in its trial study; general freemium benchmarks are often quoted at 2–5%. Use **1%, 2%, 3%** as pessimistic / realistic / optimistic.
- Trials convert much higher than plain freemium (Freemius reported ~19% for trials without a card and ~70% with a card) — mention if a trial is recommended.
- Annual license churn for WordPress plugins: about **29% per year** (Freemius benchmark) → roughly 70% renew.
- Freemium plugins survive longer than free-only plugins (Freemius analysis), which supports the Free + Pro model.

**Your forecast table (years 1–3)**

| Scenario | Free installs (end of year) | Conversion | Paying customers | Avg price | New revenue | Renewals (70%) | Total |

Rules:
- Base install growth on what similar newer plugins achieved (install velocity of recent entrants), not on the leader. If added dates are missing, estimate age from the first changelog version or earliest review (§2b).
- Show the math in one line under the table.
- Add a simple **break-even**: estimated build + first-year cost ÷ average revenue per customer = customers needed.

**Pricing analytics**
- Min / median / max price per tier (1 site, 5 sites, unlimited) across competitors.
- Share of competitors offering lifetime deals.
- Price-to-feature check: who gives the most features for the price.

---

## 6. Sentiment & support metrics

- **Complaint themes count:** tag each 1–3★ review and unresolved thread with a theme (missing feature, bug, UX, speed, support, price, compatibility). Count per theme and per plugin.
- **Recent vs lifetime rating:** average of reviews from the last 12 months vs overall. Falling recent rating = declining product.
- **Support reply speed:** typical time to first reply in recent threads.
- **Love themes:** what 4–5★ reviews praise — those are must-keep qualities.
- **Sentiment by persona (optional):** where reviewers reveal who they are (agency, small shop, B2B, store size, cart size or SKU counts mentioned), note which persona is happiest and which is most frustrated — the frustrated persona is often the best target. Personas are rarely stated, so if there isn't enough signal, skip it and say so.

---

## 7. Risk metrics

| Risk | How to check | Read |
|---|---|---|
| Security history | vulnerability count and severity per competitor (Patchstack/WPScan/Wordfence) | Many vulns = lesson for you + marketing angle ("security-first") |
| WooCommerce core overlap | Search WooCommerce blog/roadmap/GitHub for the feature | If WooCommerce plans to build it into core, the niche may vanish |
| Big-player risk | Is a large company (e.g. Automattic, StellarWP, Awesome Motive, YITH) active here? | Strong marketing budgets |
| Dependency risk | Relies on a third-party API, theme, or builder | Price/API changes can break you |
| Support burden | support load metric (section 2) | Predicts how many tickets you'll get |
| Platform trend | WooCommerce store count trend | Shrinking base = tougher growth |

---

## 8. Competitor marketing metrics

- Website traffic estimate and top traffic sources (Similarweb-type estimates).
- Top organic keywords and number of blog posts targeting this niche.
- YouTube: number of tutorial videos about each competitor.
- Affiliate program: yes/no and commission rate.
- Where they get reviews/mentions ("best plugin" lists that include them).

Use this to choose which channels are crowded and which are open.

---

## 9. Decision thresholds & red flags

Use these as guides, not hard rules:

**Good signs**
- Total niche installs ≥ 50,000 **or**, for small paid niches, paid users ≥ 2,000 (marketplace + CodeCanyon + known Pro customers), with at least one paid plugin selling well.
- Leader has negative review share > 15% or support resolution < 50%.
- 25%+ of plugins abandoned or missing HPOS/Checkout Blocks support.
- At least one newer plugin (≤ 3 years old) reached 1,000+ installs → newcomers can win.
- Search trend flat or rising.
- Realistic forecast reaches break-even within 12–24 months.

**Red flags**
- Leader has 80%+ share, 4.7★+, active updates and fast support.
- WooCommerce core is adding the feature.
- Total niche installs < 5,000 **and** paid users < 500, with no paid competitor selling well.
- Falling search trend and falling downloads across most plugins.
- Very high support load in all competitors (hard, ticket-heavy product).

---

## 10. Opportunity Dashboard format

Put this near the top of the report:

```
📊 OPPORTUNITY DASHBOARD
Market
- Live WooCommerce stores: X (trend: ±Y% YoY, source, date)
- Total niche installs: X across N plugins
- Leader share: X% | Top-3 share: X%
- Abandoned plugins: X% | Missing Checkout Blocks: X%
- New entrants that broke 1,000 installs (last 3 yrs): N
Demand
- Main keyword volume: X/mo | Trend: rising/flat/falling
Money
- Paid options: N | Price range (1 site): $X–$Y, median $Z
- Est. revenue Year 1 (realistic): $X | Break-even: N customers
Weakness of competitors
- Leader negative reviews: X% | Leader support resolution: X%
- Top complaint theme: ...
Risk
- Core overlap: yes/no | Security issues in niche: N | Support load: low/med/high
```
