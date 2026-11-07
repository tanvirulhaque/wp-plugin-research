# Research Workbook (.xlsx) — the evidence file

The report tells the story; the workbook holds the evidence. Every claim in the report can be traced back through IDs to a review or source. Build it with `scripts/build_workbook.py` from a JSON file you fill in during research.

## Sheets and ID links

| Sheet | Holds | Links |
|---|---|---|
| README | Purpose, sheet list, confidence legend, limits | — |
| Plugin_Master | Every plugin from the Master List (incl. theme built-ins and suite modules) | P01… |
| Feature_Matrix | Plugins × features: Yes / Pro / Partial / No / ? (? = not verified) | uses P IDs |
| Review_Log | One row per review, forum thread or research item, paraphrased, with link | R01… → P ID |
| Pain_Points | User pains with severity, evidence strength, root cause, how we overcome | PN01… → R IDs, G IDs |
| Gaps_Opportunities | Opportunities tied to pains and to the user's existing products | G01… |
| Benefits | What users gain, with evidence type and honest strength | B01… |
| Decision_Scorecard | Editable weights and scores; formulas rank the gaps (top 5) | G IDs |
| Sources | Every URL with type and reliability | S01… |
| AI_Facts | One fact per row, auto-generated, for feeding an AI later | all IDs |

The chain: **Source → Review (R) → Pain (PN) → Gap (G) → Scorecard rank → Feature in the report.**

## JSON shape (all keys optional except plugins)

```json
{
  "title": "...", "prepared": "YYYY-MM-DD", "purpose": "...",
  "limits": ["Review coverage is a sample", "..."],
  "default_confidence": "Medium",
  "plugins": [{"id":"P01","name":"","vendor":"","channel":"","category":"dedicated / suite / theme built-in","model":"Free / Freemium / Premium","entry_price":49,"price_note":"","traction":"","rating":4.8,"reviews":17,"last_update":"","hpos":"Yes/No/?","blocks":"Yes/No/?","status_risk":"","url":"","confidence":"High/Medium/Low"}],
  "features": {"columns": ["Feature A","Feature B"], "rows": [{"plugin":"P01 Name","values":["Yes","Pro"]}]},
  "reviews": [{"id":"R01","plugin_id":"P01","source":"","platform":"","reviewer":"","rating":1,"date":"","persona":"","theme":"","summary":"paraphrased","sentiment":"Positive/Negative/Mixed","url":"","notes":""}],
  "pains": [{"id":"PN01","theme":"","what":"","evidence":"R01, R05","plugins":"","severity":"High/Medium/Low","evidence_strength":"Strong/Medium/Weak","root_cause":"(confirmed in code) / (inferred) ...","overcome":"","gaps":"G01"}],
  "gaps": [{"id":"G01","gap":"","why":"","who_weak":"","build":"","fit":"","effort":"High/Medium/Low"}],
  "benefits": [{"id":"B01","benefit":"","who":"","evidence_type":"vendor claim / user review / independent research","evidence":"","strength":"Strong/Medium/Weak"}],
  "scorecard": {"criteria": [{"name":"Evidence of user pain","weight":30},{"name":"Differentiation","weight":25},{"name":"Ease of build (5 = easy)","weight":15},{"name":"Fit with our portfolio","weight":15},{"name":"Revenue potential","weight":15}],
                "scores": {"G01":[5,4,2,4,5]}},
  "sources": [{"id":"S01","description":"","url":"","type":"Vendor / Marketplace / Forum / Tracker / Independent research","reliability":"High/Medium/Low"}]
}
```

## Build steps

1. Save the JSON to the working folder as you research (add rows as you go).
2. `python scripts/build_workbook.py research.json [plugin-slug]-research.xlsx`
3. Recalculate and check for zero errors with the xlsx skill's `recalc.py` (read the xlsx skill first).
4. Deliver it next to the report.

## Data-quality rules

- Paraphrase reviews; no long quotes. Keep the link.
- Unverified feature → "?", never a guess.
- Vendor claims that conflict with marketplace data (e.g. "18,000 sold" vs 1.4K CodeCanyon sales) → keep both, flag the conflict, trust the marketplace number.
- A star rating that contradicts its text (5★ with negative text) → leave the rating blank and note it.
- If the user has no existing products, drop the "Fit with our portfolio" criterion or rename it "Fit with our skills".
- Exclude piracy and nulled/GPL-resale sites from sources.
