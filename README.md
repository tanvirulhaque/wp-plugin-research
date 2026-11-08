# wp-plugin-research

An open [Agent Skill](https://agentskills.io) for researching WordPress / WooCommerce plugin ideas. It works in Claude, ChatGPT, Gemini, Codex, Cursor and Copilot.

**Type a plugin idea. Get a clear decision: build it or not, and how.**

**Version 1.1.0.** See [CHANGELOG](CHANGELOG.md) for what's new.

## ⚡ Quick start (Claude, 3 steps)

1. **Install:** click **Save skill** on the `wp-plugin-research.skill` file card.
2. **Open a new chat** with **Web search** and **Code execution and file creation** turned on.
3. **Type:**
   ```
   /wp-plugin-research WooCommerce wholesale pricing
   ```

It runs in **2 turns**:
- **Turn 1:** research, then the evidence workbook and an early verdict.
- **Turn 2:** reply **`continue`** to get the full reports.

Using ChatGPT, Gemini, Codex, Cursor or Copilot? See **section 2**.

---

## 1. What it does

| Step | What happens |
|---|---|
| 1. Find | Finds all similar plugins (WordPress.org, WooCommerce Marketplace, CodeCanyon, themes, independent sellers) |
| 2. Collect | Collects features, prices, installs, ratings, reviews, and competitor code |
| 3. Analyze | Finds user pains, feature gaps, opportunities, and technical weak spots |
| 4. Plan | Proposes features, Free vs Pro, pricing, tech strategy, and a 12-week plan |
| 5. Decide | Gives GO / MAYBE / NO-GO with a score, and lists the decisions only you can make |

---

## 2. Install

### Which file to use

Download the files from the [Releases page](https://github.com/tanvirulhaque/wp-plugin-research/releases), or build them yourself with `bash tools/package.sh` (they're saved to `dist/`).

| File | Use it for |
|---|---|
| `wp-plugin-research.skill` | **Claude** (click Save skill) |
| `wp-plugin-research.zip` | **ChatGPT, Gemini, and other apps** that upload a zip with `SKILL.md` at the top |
| The folder `skills/wp-plugin-research/` | **Coding agents** (Claude Code, Codex, Gemini CLI, Cursor, Copilot). Clone this repo and copy that folder into the agent's skills folder |

All of them are the same skill. It uses the open **Agent Skills** format (a folder with a `SKILL.md`), which most AI tools now read.

### What each app needs

| App | Plan needed | Web search | Runs scripts? | Result |
|---|---|---|---|---|
| Claude (web / desktop / mobile) | Free or paid | ✅ | ✅ | ✅ Full |
| Claude Code / Cowork | Paid | ✅ | ✅ | ✅ Full, and best for reading competitor code |
| ChatGPT | **Business, Enterprise or Edu** (the Skills feature) | ✅ | ✅ | ✅ Full |
| OpenAI Codex (CLI / IDE) | ChatGPT plan or API | ✅ (if enabled) | ✅ | ✅ Full |
| Gemini app (gemini.google.com) | **Google AI Pro / Ultra** (availability varies by country) | ✅ | ⚠️ may not | ⚠️ Reports yes; workbook as tables |
| Gemini CLI | Free or paid | ✅ | ✅ | ✅ Full |
| Cursor / GitHub Copilot | Paid | ⚠️ depends on setup | ✅ | ⚠️ Good for the code parts |

⚠️ Skill features change often. If a menu has moved, search the app's help for "skills".

---

### Claude: web, desktop and mobile
1. Click **Save skill** on the `.skill` file card, or go to **Settings → Capabilities → Skills → Upload skill**.
2. In **Settings → Capabilities**, turn on **Web search** and **Code execution and file creation**.
3. **Check:** type `/` in a new chat. You should see `wp-plugin-research`.

### Claude Code / Cowork
1. Clone this repo: `git clone https://github.com/tanvirulhaque/wp-plugin-research.git`
2. Copy `skills/wp-plugin-research/` to `~/.claude/skills/wp-plugin-research/` (for all projects) or `.claude/skills/` (one project).
3. Restart, then type `/` to check.

### ChatGPT (Business / Enterprise / Edu)
1. Open **Plugins → Skills → Create → Upload from your computer**. (In the desktop app: **Skills → Create → Upload**.)
2. Choose `wp-plugin-research.zip`.
3. Turn on **web search** and **code / data analysis** in the chat.
4. **Check:** type `@` in a chat. You should see `wp-plugin-research`.

### OpenAI Codex (CLI / IDE)
1. Copy the folder to `~/.agents/skills/wp-plugin-research/` (all projects) or `.agents/skills/` (one project).
2. Restart Codex.
3. **Check:** run `/skills`.

### Gemini app (gemini.google.com, Mac app)
1. Open **Settings → Skills → Upload**.
2. Upload `wp-plugin-research.zip`, or the unzipped folder. `SKILL.md` must be at the top of what you upload.
3. **Check:** type `/` in a chat.
4. **To update:** on the Skills page, click the skill → **More → Replace skill**.

### Gemini Enterprise
1. Open the Gemini Enterprise web app, then **Skills → + → Upload skill**.
2. Upload `wp-plugin-research.zip`.

### Gemini CLI
1. Copy the folder to `~/.gemini/skills/wp-plugin-research/` (or `~/.agents/skills/`).
2. Restart Gemini CLI.

### Cursor
Copy the folder to `~/.cursor/skills/wp-plugin-research/` (or `.cursor/skills/` in a project). Cursor also reads `.agents/skills/`.

### GitHub Copilot (VS Code)
Copy the folder to `~/.copilot/skills/wp-plugin-research/` (or `.github/skills/` in a project).

### One command for many coding agents
The community Skills CLI installs it for Claude Code, Codex, Cursor, Gemini CLI, Copilot and more:
```
npx skills add tanvirulhaque/wp-plugin-research
```
Only install skills from sources you trust, and read their files first.

**To update in any app:** install the new version the same way. The same name replaces the old one.

---

## 3. How to start

### Start command in each app

| App | Type this |
|---|---|
| Claude, Claude Code, Cowork | `/wp-plugin-research WooCommerce wholesale pricing` |
| ChatGPT | `@wp-plugin-research WooCommerce wholesale pricing` |
| Codex | `$wp-plugin-research WooCommerce wholesale pricing` (or pick it from `/skills`) |
| Gemini app | `/wp-plugin-research WooCommerce wholesale pricing` |
| Gemini CLI, Cursor, Copilot | `Use the wp-plugin-research skill: WooCommerce wholesale pricing` |

### Or just ask (it starts on its own in every app)
```
Research: WooCommerce wholesale pricing plugin
```
```
Is a "variations as single products" plugin worth building?
```

The command is the surest way. Plain asking works when your message clearly matches the skill.

**Rules for best results**
- Use a **new chat** for each idea. A long chat can run out of room.
- Name **one idea** per run.
- If you already sell plugins, say so:
  ```
  /wp-plugin-research I sell a swatches plugin. Idea: show variations as single products
  ```
- Use the **strongest model** your app offers. This is a long research task.
- Want only the business side? Add **"business only"**:
  ```
  /wp-plugin-research WooCommerce bookings — business only
  ```

---

## 4. How a run works

| Turn | What happens | You do |
|---|---|---|
| 1. Research | Finds plugins, collects data, analyzes, builds the workbook | Read the early verdict, then reply **`continue`** (and name any plugins you already sell) |
| 2. Reports | Writes the 4 deliverables | Read the Final Decision Summary first |
| 3. Pro code (optional) | Deep code check on code you share | Share the Pro zips it asked for |

- **If a run stops partway** (tool or context limits), just reply `continue`. It resumes from its saved progress (`research.json` and `notes.md`) instead of starting over.
- **Want it faster?** Add **"quick"** for **Lite mode**: 3 competitors, Decision Summary and workbook only.
  ```
  /wp-plugin-research quick: WooCommerce wholesale pricing
  ```

---

## 5. What you'll be asked (up to 3 short things)

| When | Question | What to do |
|---|---|---|
| Only if your idea is vague | One short clarifying question | Answer in one line |
| End of turn 1 | Do you already sell plugins? | Name them, or skip |
| End of turn 2 | 📦 **Code request**: 2–4 paid plugins it can't download, plus any free ones whose download was blocked | Share a **folder path** (Claude Code / Cowork) or **upload the .zip** files. It updates the Technical Report. Skip any you don't want to buy |

It downloads the Free versions itself. The research never stops to wait for code.

---

## 6. What you get (4 outputs)

| # | Output | Read it when | Time |
|---|---|---|---|
| 1 | 🧭 **Final Decision Summary** | Always, first | 5 min |
| 2 | 📊 **Research Report** | You want the business reasoning | 15–20 min |
| 3 | 🛠 **Technical Report** | You or your developer plan the build | 15–20 min |
| 4 | 📁 **Research Workbook (.xlsx)** | You want to check evidence or change priorities | As needed |

In Claude, reports open as one Claude Doc with **Summary · Research · Technical** tabs (editable, shareable, downloadable as Word or PDF). In other apps, they're Markdown files or appear in the chat. Apps that can't run scripts give the workbook data as tables instead of an .xlsx file. Say **"business only"** to skip the Technical Report.

**Workbook sheets:** Plugin_Master, Health_Metrics, Feature_Matrix, Review_Log, Pain_Points, Gaps_Opportunities, Benefits, Demand_Proxy, Decision_Scorecard, Pricing_Benchmarks, Final_Feature_Set, Forecast, Verdict, Sources and AI_Facts. Change the yellow cells and everything recalculates.

---

## 7. How to read the results

**Signals:** ✅ good · ⚠️ watch · ❌ bad · 🔥 top priority · ? not verified
(In Claude Docs these appear as words: Good / Watch / Bad / Top priority / Not verified.)

**Labels:** **Fact** (seen in a source) · **Estimate** (calculated, with the math shown) · **Assumption** (judgment)

**Verdict (score out of 35):**
| Score | Verdict |
|---|---|
| 28–35 | ✅ GO: build it |
| 21–27 | ⚠️ MAYBE: only with a sharp angle |
| below 21 | ❌ NO-GO: better nearby ideas are suggested |

**Check any claim:** every finding has an ID you can trace back in the workbook.

```
Source (S) → Review (R) → Pain (PN) → Gap (G) → Scorecard rank → Feature
```

**Change priorities:** edit the yellow cells in **Decision_Scorecard** (gap ranking), **Forecast** (revenue scenarios) or **Verdict** (factor scores). The results update automatically.

---

## 8. Test the skill (after installing or editing it)

1. Open a **new chat** in your app.
2. Type the start command from section 3, for example `/wp-plugin-research WooCommerce wholesale pricing`
3. After turn 1 (early verdict + workbook), reply `continue`, then wait for the 4 outputs.
4. Check them:

| # | Check | Pass if… |
|---|---|---|
| 1 | Verdict | The Decision Summary shows GO / MAYBE / NO-GO, a score out of 35, and confidence |
| 2 | Workbook | The .xlsx has Plugin_Master, Review_Log, Pain_Points and Decision_Scorecard, with no errors |
| 3 | Evidence | Every pain cites a Review ID (R01…) |
| 4 | Sources | Every plugin has a link |
| 5 | Technical | The Technical Report shows HPOS and Checkout Blocks status per competitor |
| 6 | Code request | At most 4 Pro plugins are requested, each with a reason |
| 7 | Your decisions | 2–4 decisions are listed, each with options and a recommendation |
| 8 | Turn 1 checkpoint | Turn 1 ends with an early verdict, the workbook, and a request to reply `continue` |
| 9 | Coverage | **Limits & coverage** lists what was checked, what was partial, and what was blocked |

Quick extra tests:
- `research a woocommerce plugin that makes money` should ask **one** question and stop.
- `quick research: WooCommerce product bundles` should research **3** competitors and give only the Decision Summary and workbook.

---

## 9. Good follow-up prompts

- `Go deeper on gap G02`
- `Here is the Pro code for [plugin]` (attach the zip) → the Technical Report is updated
- `Turn the MVP features into a requirements list`
- `Make the landing page for validation`
- `Re-score with weights: pain 40, revenue 30, ease 30`

---

## 10. Limits

- Review coverage is a sample, not every review. Gaps are listed in **Limits & Coverage**.
- Vendor claims can be wrong. Conflicts are flagged, and marketplace numbers are trusted first.
- Revenue numbers are estimates based on industry averages, not guarantees.
- Code reading is static, so runtime behaviour is marked "likely".
- A full run takes many searches, so it's split into 2 turns. Big niches take longer.
- Some sources can be blocked (for example wordpress.org from some sandboxes). The skill switches to backup sources such as tracker sites, jsDelivr and GitHub mirrors, and lists what it couldn't reach under **Limits & coverage**.
- Keyword and trend tools usually aren't available, so demand uses a transparent **proxy score** you can check in the Demand_Proxy sheet.
- It never uses nulled or pirated plugins.

---

## 11. Repository layout

```
wp-plugin-research/
├── README.md                 ← this file
├── LICENSE                   ← MIT
├── CHANGELOG.md
├── ROADMAP.md                ← ideas under consideration
├── requirements.txt          ← openpyxl (for the scripts)
├── skills/
│   └── wp-plugin-research/   ← THE SKILL (copy this folder to install)
│       ├── SKILL.md          ← workflow: 5 stages, 16 phases
│       ├── references/       ← playbooks, templates, run plan, sources (loaded only when needed)
│       ├── assets/research-template.json ← starter data file
│       └── scripts/
│           ├── analyze_plugin.py   ← scans a plugin's code (bundled SDKs excluded, hot-path checks)
│           ├── compare_code.py     ← side-by-side technical comparison
│           ├── fetch_code.py       ← downloads free code (wordpress.org or GitHub mirrors)
│           ├── add_row.py          ← saves each finding to research.json
│           └── build_workbook.py   ← builds the evidence .xlsx (15 data sheets + README)
├── tests/
│   ├── evals/                ← 5 test cases (prompts + pass/fail checks)
│   ├── fixtures/demo-plugin/ ← tiny plugin for the scanner test
│   └── sample-research.json  ← sample data for the workbook smoke test
├── tools/package.sh          ← builds dist/*.skill and dist/*.zip
├── tools/check_skill.py      ← SKILL.md size + pointer guardrail
├── tools/check_no_loss.py    ← audit: no instruction lost vs an older version
└── .github/workflows/validate.yml  ← spec validation + script checks on every push
```

---

## 12. For maintainers

- **Size and pointer check:** `python tools/check_skill.py`. It warns if SKILL.md grows past about 3,700 words, and fails on missing or orphan reference files or a missing phase.
- **Validate:** `skills-ref validate skills/wp-plugin-research`. This is the official Agent Skills validator, and GitHub Actions runs it on every push.
- **No-loss audit (before every release):** compare with the last release so no instruction disappears:
  ```
  mkdir -p /tmp/old && git archive <last-release-tag> skills | tar -x -C /tmp/old
  python tools/check_no_loss.py /tmp/old/skills/wp-plugin-research skills/wp-plugin-research
  ```
  Every flagged line must be reworded or moved on purpose, never dropped.
- **Release:**
  1. Run the checks above, then update `metadata.version` in `SKILL.md` and `CHANGELOG.md`.
  2. Run `bash tools/package.sh`.
  3. Create a GitHub Release and attach both files from `dist/`.
- **Contribute:** open an issue or a pull request. Keep `SKILL.md` lean and put details in `references/`.

## Author

Made by **Tanvirul Haque**: [tanvirulhaque.com](https://tanvirulhaque.com) · [GitHub](https://github.com/tanvirulhaque)

## License

MIT. See [LICENSE](LICENSE).
