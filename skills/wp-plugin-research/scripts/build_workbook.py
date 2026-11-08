#!/usr/bin/env python3
"""
Build the Research Workbook (.xlsx) from a research JSON file.

Usage:
  python build_workbook.py research.json output.xlsx

The JSON shape is documented in references/research-workbook.md.
Every sheet is optional except "plugins". IDs (P01, R01, PN01, G01, B01, S01)
link the sheets together so every claim can be traced back to its evidence.
Then recalculate: python <xlsx-skill>/scripts/recalc.py output.xlsx
"""
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

FONT = "Arial"
HEAD_FILL = PatternFill("solid", fgColor="1F3864")
INPUT_FILL = PatternFill("solid", fgColor="FFFF00")
HEAD_FONT = Font(name=FONT, bold=True, color="FFFFFF")
BODY_FONT = Font(name=FONT)
INPUT_FONT = Font(name=FONT, color="0000FF")
BOLD = Font(name=FONT, bold=True)

# key -> (sheet name, [(json field, column header), ...])
TABLES = {
    "plugins": ("Plugin_Master", [
        ("id", "ID"), ("name", "Plugin"), ("vendor", "Vendor"), ("channel", "Channel"),
        ("category", "Category (dedicated / suite / theme built-in)"), ("model", "Model"),
        ("entry_price", "Entry price (USD/yr)"), ("price_note", "Price note"),
        ("traction", "Installs / sales"), ("rating", "Rating"), ("reviews", "Reviews (count)"),
        ("last_update", "Maintenance / recency"), ("hpos", "HPOS"), ("blocks", "Checkout Blocks"),
        ("status_risk", "Status and risk"), ("url", "Main URL"), ("confidence", "Data confidence")]),
    "reviews": ("Review_Log", [
        ("id", "ID"), ("plugin_id", "Plugin ID"), ("source", "Plugin / source"),
        ("platform", "Platform"), ("reviewer", "Reviewer"), ("rating", "Rating (1-5)"),
        ("date", "Date"), ("persona", "Persona (if known)"), ("theme", "Theme"),
        ("summary", "Summary (paraphrased)"), ("sentiment", "Sentiment"),
        ("url", "Source URL"), ("notes", "Notes")]),
    "pains": ("Pain_Points", [
        ("id", "ID"), ("theme", "Pain theme"), ("what", "What users suffer"),
        ("evidence", "Evidence (Review_Log IDs)"), ("plugins", "Plugins affected"),
        ("severity", "Severity"), ("evidence_strength", "Evidence strength"),
        ("root_cause", "Likely root cause (label: confirmed in code / inferred)"),
        ("overcome", "How we overcome it"), ("gaps", "Related gap IDs")]),
    "gaps": ("Gaps_Opportunities", [
        ("id", "ID"), ("gap", "Gap / opportunity"), ("why", "Why it matters (evidence)"),
        ("who_weak", "Who is weak today"), ("build", "What we build"),
        ("fit", "Fit with user's existing products"), ("effort", "Effort")]),
    "benefits": ("Benefits", [
        ("id", "ID"), ("benefit", "Benefit users get"), ("who", "Who benefits"),
        ("evidence_type", "Evidence type (vendor claim / user review / independent research)"),
        ("evidence", "Evidence"), ("strength", "Strength")]),
    "health": ("Health_Metrics", [
        ("plugin_id", "Plugin ID"), ("plugin", "Plugin"), ("installs_floor", "Installs (band floor)"),
        ("age_years", "Age (years)"), ("velocity", "Installs per year (est.)"), ("momentum", "Momentum"),
        ("updates_12m", "Releases last 12 months"), ("days_since_update", "Days since update"),
        ("rating", "Rating"), ("negative_share", "1-2 star share"), ("support_resolved", "Support resolved %"),
        ("support_load", "Threads per 1k installs"), ("vulns", "Known vulnerabilities"),
        ("source", "Source / fallback used")]),
    "demand_proxy": ("Demand_Proxy", [
        ("signal", "Signal"), ("value", "Value found"), ("points", "Points (0-2)"), ("source", "Source")]),
    "pricing": ("Pricing_Benchmarks", [
        ("plugin_id", "Plugin ID"), ("plugin", "Plugin"), ("tier_1", "1 site (USD/yr)"),
        ("tier_5", "5 sites (USD/yr)"), ("tier_unlimited", "Unlimited (USD/yr)"),
        ("lifetime", "Lifetime deal"), ("trial", "Trial / refund"), ("url", "Pricing URL")]),
    "feature_set": ("Final_Feature_Set", [
        ("id", "ID"), ("feature", "Feature"), ("category", "Category"), ("type", "Type (Must-have / Better / New)"),
        ("priority", "Priority (MVP / v1.1 / v2 / Later)"), ("tier", "Free or Pro"), ("impact", "Impact"),
        ("effort", "Effort"), ("evidence", "Evidence (PN / G IDs)"), ("why", "Why")]),
    "sources": ("Sources", [
        ("id", "ID"), ("description", "Description"), ("url", "URL"),
        ("type", "Type"), ("reliability", "Reliability")]),
}
FACT_SHEETS = ["plugins", "reviews", "pains", "gaps", "benefits"]


def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font, cell.fill = HEAD_FONT, HEAD_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="top")


def write_table(ws, cols, rows, start=1):
    for i, (_, head) in enumerate(cols, 1):
        ws.cell(row=start, column=i, value=head)
    style_header(ws, start, len(cols))
    for r, item in enumerate(rows, start + 1):
        for c, (key, _) in enumerate(cols, 1):
            v = item.get(key, "")
            cell = ws.cell(row=r, column=c, value=v if v != "" else None)
            cell.font = BODY_FONT
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    for i, (key, head) in enumerate(cols, 1):
        longest = max([len(str(head))] + [len(str(x.get(key, ""))) for x in rows])
        ws.column_dimensions[get_column_letter(i)].width = max(8, min(55, longest + 2))
    ws.freeze_panes = ws.cell(row=start + 1, column=2)


def build(data, out):
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    readme = [
        (data.get("title", "Plugin research workbook"), ""),
        ("", ""),
        ("Prepared", data.get("prepared", "")),
        ("Purpose", data.get("purpose", "")),
        ("", ""),
        ("Sheet", "What it holds"),
    ]
    present = [k for k in TABLES if data.get(k)]
    for k in present:
        readme.append((TABLES[k][0], f"{len(data[k])} rows"))
    if data.get("features"):
        readme.append(("Feature_Matrix", "Plugins x features. Yes = confirmed, Pro = paid tier only, Partial = limited, No = missing, ? = not verified"))
    if data.get("forecast"):
        readme.append(("Forecast", "Revenue scenarios for years 1-3; edit the yellow inputs (installs, conversion, price, renewal, cost)"))
    if data.get("verdict") and any(f.get("score") for f in data["verdict"]["factors"]):
        readme.append(("Verdict", "7 factor scores (yellow, 1-5); total out of 35 and GO / MAYBE / NO-GO update automatically"))
    if data.get("scorecard"):
        readme.append(("Decision_Scorecard", "Edit the yellow cells (weights and scores); weighted score and rank update automatically"))
    readme.append(("AI_Facts", "One fact per row, generated from the other sheets, for feeding to an AI later"))
    readme += [("", ""),
               ("ID links", "P = plugin, R = review, PN = pain, G = gap, B = benefit, S = source. Pains cite review IDs; gaps cite pains."),
               ("Confidence legend", "High = official page read directly. Medium = third-party tracker or blog. Low = single unverified mention."),
               ("Limits", "; ".join(data.get("limits", [])) or "-"),
               ("Not included", "Piracy and nulled/GPL-resale sites are excluded.")]
    for r, (a, b) in enumerate(readme, 1):
        ws.cell(row=r, column=1, value=a or None).font = BOLD
        ws.cell(row=r, column=2, value=b or None).font = BODY_FONT
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    ws["A1"].font = Font(name=FONT, bold=True, size=14)
    ws.column_dimensions["A"].width, ws.column_dimensions["B"].width = 22, 110

    # no user products -> portfolio criterion becomes skills fit (as the reference says)
    if data.get("scorecard") and not data.get("user_products"):
        for c in data["scorecard"]["criteria"]:
            if "portfolio" in c["name"].lower():
                c["name"] = "Fit with our skills"
    order = ["plugins", "health", "features", "reviews", "pains", "gaps", "benefits", "demand_proxy",
             "scorecard", "pricing", "feature_set", "forecast", "verdict", "sources"]
    for key in order:
        if key == "features" and data.get("features"):
            f = data["features"]
            fs = wb.create_sheet("Feature_Matrix")
            cols = [("plugin", "Plugin")] + [(f"c{i}", name) for i, name in enumerate(f["columns"])]
            rows = [dict({"plugin": r["plugin"]}, **{f"c{i}": v for i, v in enumerate(r["values"])}) for r in f["rows"]]
            write_table(fs, cols, rows)
            for i in range(2, len(cols) + 1):
                fs.column_dimensions[get_column_letter(i)].width = 16
        elif key == "scorecard" and data.get("scorecard") and data["scorecard"].get("scores"):
            build_scorecard(wb, data)
        elif key == "forecast" and data.get("forecast"):
            build_forecast(wb, data["forecast"])
        elif key == "verdict" and data.get("verdict") and any(f.get("score") for f in data["verdict"]["factors"]):
            build_verdict(wb, data["verdict"])
        elif key in TABLES and data.get(key):
            name, cols = TABLES[key]
            write_table(wb.create_sheet(name), cols, data[key])

    # AI_Facts
    af = wb.create_sheet("AI_Facts")
    heads = ["Fact ID", "Entity type", "Entity ID", "Entity name", "Attribute", "Value",
             "Source URL", "Confidence", "Collected on"]
    for i, h in enumerate(heads, 1):
        af.cell(row=1, column=i, value=h)
    style_header(af, 1, len(heads))
    n, r = 0, 2
    for key in FACT_SHEETS:
        for item in data.get(key, []):
            name_key = {"plugins": "name", "reviews": "source", "pains": "theme",
                        "gaps": "gap", "benefits": "benefit"}[key]
            for fkey, head in TABLES[key][1]:
                if fkey in ("id", "url", name_key) or item.get(fkey) in (None, ""):
                    continue
                n += 1
                row = [f"F{n:04d}", key.rstrip("s"), item.get("id"), item.get(name_key), head,
                       item.get(fkey), item.get("url", ""), item.get("confidence", data.get("default_confidence", "Medium")),
                       data.get("prepared", "")]
                for c, v in enumerate(row, 1):
                    af.cell(row=r, column=c, value=v if v != "" else None).font = BODY_FONT
                r += 1
    for i, w in enumerate([8, 10, 9, 30, 28, 60, 45, 11, 12], 1):
        af.column_dimensions[get_column_letter(i)].width = w
    af.freeze_panes = "A2"
    wb.save(out)
    print(f"Saved {out}: {len(wb.sheetnames)} sheets, {n} AI facts")


def build_scorecard(wb, data):
    sc = data["scorecard"]
    crit = sc["criteria"]  # [{"name":..., "weight":...}]
    ws = wb.create_sheet("Decision_Scorecard")
    ws["A1"] = "Decision scorecard - edit yellow cells (weights in row 5, scores below); score and rank update automatically"
    ws["A1"].font = Font(name=FONT, bold=True, size=12)
    ws["A2"] = "Scores 1-5 (5 = best). For effort/ease, 5 = easiest. All scores are analyst estimates - change them to your priorities."
    ws["A2"].font = BODY_FONT
    k = len(crit)
    first, last = 3, 2 + k                     # criteria columns C..
    fl, ll = get_column_letter(first), get_column_letter(last)
    score_col, rank_col = get_column_letter(last + 1), get_column_letter(last + 2)
    ws["A4"], ws["A5"] = "Criterion", "Weight"
    ws["A4"].font = ws["A5"].font = BOLD
    for j, c in enumerate(crit):
        col = first + j
        ws.cell(row=4, column=col, value=c["name"]).font = BOLD
        w = ws.cell(row=5, column=col, value=c["weight"])
        w.font, w.fill = INPUT_FONT, INPUT_FILL
    ws.cell(row=5, column=last + 1, value=f"=SUM({fl}5:{ll}5)").font = BODY_FONT
    ws.cell(row=4, column=last + 1, value="Weight total").font = BOLD
    heads = ["Gap ID", "Gap / opportunity"] + [c["name"] for c in crit] + ["Weighted score (1-5)", "Rank"]
    for i, h in enumerate(heads, 1):
        ws.cell(row=8, column=i, value=h)
    style_header(ws, 8, len(heads))
    ids = list(sc["scores"].keys())
    r0, r1 = 9, 8 + len(ids)
    for i, gid in enumerate(ids):
        r = r0 + i
        ws.cell(row=r, column=1, value=gid).font = BODY_FONT
        ws.cell(row=r, column=2, value=f"=IFERROR(INDEX(Gaps_Opportunities!$B:$B,MATCH(A{r},Gaps_Opportunities!$A:$A,0)),\"\")").font = BODY_FONT
        for j, v in enumerate(sc["scores"][gid]):
            cell = ws.cell(row=r, column=first + j, value=v)
            cell.font, cell.fill = INPUT_FONT, INPUT_FILL
        ws.cell(row=r, column=last + 1,
                value=f"=SUMPRODUCT({fl}{r}:{ll}{r},${fl}$5:${ll}$5)/SUM(${fl}$5:${ll}$5)").number_format = "0.00"
        ws.cell(row=r, column=last + 2,
                value=f"=RANK({score_col}{r},${score_col}${r0}:${score_col}${r1})+COUNTIF(${score_col}${r0}:{score_col}{r},{score_col}{r})-1")
    top = r1 + 3
    ws.cell(row=top, column=1, value="Top 5 by weighted score").font = BOLD
    for i, h in enumerate(["Rank", "Gap ID", "Gap / opportunity", "Score"], 1):
        ws.cell(row=top + 1, column=i, value=h)
    style_header(ws, top + 1, 4)
    rng = f"${rank_col}${r0}:${rank_col}${r1}"
    for n in range(1, min(5, len(ids)) + 1):
        r = top + 1 + n
        ws.cell(row=r, column=1, value=n)
        ws.cell(row=r, column=2, value=f"=INDEX($A${r0}:$A${r1},MATCH(A{r},{rng},0))")
        ws.cell(row=r, column=3, value=f"=INDEX($B${r0}:$B${r1},MATCH(A{r},{rng},0))")
        ws.cell(row=r, column=4, value=f"=INDEX(${score_col}${r0}:${score_col}${r1},MATCH(A{r},{rng},0))").number_format = "0.00"
    ws.column_dimensions["A"].width, ws.column_dimensions["B"].width = 12, 48
    for col in range(first, last + 3):
        ws.column_dimensions[get_column_letter(col)].width = 16


def _inp(cell, value, fmt=None):
    cell.value = value
    cell.font, cell.fill = INPUT_FONT, INPUT_FILL
    if fmt: cell.number_format = fmt


def build_forecast(wb, f):
    ws = wb.create_sheet("Forecast")
    ws["A1"] = "Revenue forecast - estimates, edit the yellow inputs"
    ws["A1"].font = Font(name=FONT, bold=True, size=12)
    labels = [("Average yearly price (USD)", f.get("avg_price", 79), '"$"#,##0'),
              ("Renewal rate (share renewing yearly)", f.get("renewal_rate", 0.7), "0%"),
              ("First-year cost to build & launch (USD)", f.get("first_year_cost", 15000), '"$"#,##0')]
    for i, (lab, val, fmt) in enumerate(labels, 3):
        ws.cell(row=i, column=1, value=lab).font = BOLD
        _inp(ws.cell(row=i, column=2), val, fmt)
    heads = ["Scenario", "Year", "Free installs (end of year)", "Conversion", "New paying customers",
             "Renewing customers", "New revenue", "Renewal revenue", "Total revenue"]
    hr = 8
    for i, h in enumerate(heads, 1):
        ws.cell(row=hr, column=i, value=h)
    style_header(ws, hr, len(heads))
    r = hr + 1
    totals = {}
    for name, sc in f.get("scenarios", {}).items():
        first = r
        for y in range(3):
            ws.cell(row=r, column=1, value=name).font = BODY_FONT
            ws.cell(row=r, column=2, value=y + 1).font = BODY_FONT
            _inp(ws.cell(row=r, column=3), sc["installs"][y], "#,##0")
            _inp(ws.cell(row=r, column=4), sc["conversion"], "0.0%")
            prev = f"C{r-1}" if y else "0"
            ws.cell(row=r, column=5, value=f"=ROUND(MAX(C{r}-{prev},0)*D{r},0)").number_format = "#,##0"
            ws.cell(row=r, column=6, value=f"=ROUND((E{r-1}+F{r-1})*$B$4,0)" if y else 0).number_format = "#,##0"
            ws.cell(row=r, column=7, value=f"=E{r}*$B$3").number_format = '"$"#,##0'
            ws.cell(row=r, column=8, value=f"=F{r}*$B$3").number_format = '"$"#,##0'
            ws.cell(row=r, column=9, value=f"=G{r}+H{r}").number_format = '"$"#,##0'
            r += 1
        totals[name] = (first, r - 1)
    r += 1
    ws.cell(row=r, column=1, value="Break-even").font = BOLD
    ws.cell(row=r + 1, column=1, value="Paying customers needed in year 1")
    ws.cell(row=r + 1, column=2, value="=ROUNDUP($B$5/$B$3,0)").number_format = "#,##0"
    rr = r + 2
    for name, (a, b) in totals.items():
        ws.cell(row=rr, column=1, value=f"{name}: 3-year total revenue")
        ws.cell(row=rr, column=2, value=f"=SUM(I{a}:I{b})").number_format = '"$"#,##0'
        rr += 1
    ws.cell(row=rr + 1, column=1, value="Math: new customers = new installs x conversion; renewals = last year's paying customers x renewal rate. All figures are estimates.").font = BODY_FONT
    ws.column_dimensions["A"].width = 42
    for c in "BCDEFGHI":
        ws.column_dimensions[c].width = 16


def build_verdict(wb, v):
    ws = wb.create_sheet("Verdict")
    ws["A1"] = "Verdict - edit the yellow scores (1-5); total and verdict update automatically"
    ws["A1"].font = Font(name=FONT, bold=True, size=12)
    for i, h in enumerate(["Factor", "Score (1-5)", "Why (the number behind it)"], 1):
        ws.cell(row=3, column=i, value=h)
    style_header(ws, 3, 3)
    r = 4
    for fct in v["factors"]:
        ws.cell(row=r, column=1, value=fct["name"]).font = BODY_FONT
        _inp(ws.cell(row=r, column=2), fct.get("score", 0))
        ws.cell(row=r, column=3, value=fct.get("why", "")).font = BODY_FONT
        r += 1
    last = r - 1
    ws.cell(row=r + 1, column=1, value="Total (out of 35)").font = BOLD
    ws.cell(row=r + 1, column=2, value=f"=SUM(B4:B{last})")
    ws.cell(row=r + 2, column=1, value="Verdict").font = BOLD
    ws.cell(row=r + 2, column=2, value=f'=IF(B{r+1}>=28,"GO",IF(B{r+1}>=21,"MAYBE","NO-GO"))')
    ws.cell(row=r + 3, column=1, value="Confidence").font = BOLD
    ws.cell(row=r + 3, column=2, value=v.get("confidence", "Medium"))
    ws.cell(row=r + 5, column=1, value="Rule: 28-35 GO, 21-27 MAYBE, below 21 NO-GO.").font = BODY_FONT
    ws.column_dimensions["A"].width, ws.column_dimensions["B"].width, ws.column_dimensions["C"].width = 32, 14, 70


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        build(json.load(fh), sys.argv[2])
