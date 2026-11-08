# Portability — running on any agent


This skill follows the open Agent Skills format. Some steps need tools that not every agent has, so adapt instead of failing:

| If the agent can't… | Do this instead |
|---|---|
| Search the web | Stop and tell the user: this skill needs web search; ask them to turn it on |
| Run Python (scripts) | Skip the scripts. Read competitor code directly, and give the workbook data as Markdown tables or CSV text |
| Recalculate Excel formulas | Deliver the .xlsx as is — Excel and Google Sheets calculate the formulas when the file opens |
| Create Claude Docs | Write the reports as Markdown files (or in the chat if files aren't possible) |
| Read uploaded zips | Ask the user to paste the main plugin files, or a folder path in a local agent |



## Claude Docs mode

When reports are written with the Claude Docs connector:

- **When to create docs:** create them at the start of the reporting turn (turn 2 in `run-plan.md`), as that turn's first calls — not before research. This satisfies the connector's "skeleton first" rule without leaving empty docs for a whole turn.
- **One doc, three tabs:** prefer one doc with tabs **Summary · Research · Technical** (one link, fewer setup calls). Use separate docs only if tabs aren't available.
- **Group writes:** write 2–4 related sections per call, or create a tab with its full content in one call, to stay within the call budget.
- **No emoji in docs:** use the words **Good / Watch / Bad**, **Top priority**, and **Not verified** instead of ✅ ⚠️ ❌ 🔥 ?. Emoji are fine in Markdown files and chat.
- **Visuals:** the positioning map and priority map may be tables when the budget is tight; draw diagrams only if calls remain.
- Follow the connector's own instructions (e.g. its guide) for everything else.

## Recalculating the workbook

Find the xlsx recalculation script instead of guessing its path:
```
find / -name recalc.py -path "*xlsx*" 2>/dev/null | head -1
```
(On claude.ai it is usually `/mnt/skills/public/xlsx/scripts/recalc.py`.) If none exists, skip it — Excel and Google Sheets calculate formulas on open.
