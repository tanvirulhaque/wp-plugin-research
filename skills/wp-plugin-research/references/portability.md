# Portability — running on any agent


This skill follows the open Agent Skills format. Some steps need tools that not every agent has, so adapt instead of failing:

| If the agent can't… | Do this instead |
|---|---|
| Search the web | Stop and tell the user: this skill needs web search; ask them to turn it on |
| Run Python (scripts) | Skip the scripts. Read competitor code directly, and give the workbook data as Markdown tables or CSV text |
| Recalculate Excel formulas | Deliver the .xlsx as is — Excel and Google Sheets calculate the formulas when the file opens |
| Create Claude Docs | Write the reports as Markdown files (or in the chat if files aren't possible) |
| Read uploaded zips | Ask the user to paste the main plugin files, or a folder path in a local agent |


