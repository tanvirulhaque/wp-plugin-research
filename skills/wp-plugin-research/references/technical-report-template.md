# Technical Report — template (separate, for builders)

For the developer or technical decision-maker. Same writing rules: answer first, tables, ✅ ⚠️ ❌ signals, "→ What this means" lines. Built from Phases 9–11 and the code scanner.

```markdown
# [Plugin Idea] — Technical Report
Data as of [date] · Code analyzed: [list, with versions] · Skipped: [Pro versions not shared]

## 1. Technical verdict
**[One line: how hard, how risky, and the key technical edge]**
| Difficulty | MVP build time | Biggest technical risk | Our technical edge |
|---|---|---|---|

## 2. Code collected
| Plugin | Free code | Pro code | Source | Version |
|---|---|---|---|---|

## 3. Technical analytics (side by side)
Generated with `scripts/compare_code.py` from the scanner outputs:
size, requirements, HPOS / Checkout Blocks / Store API / Abilities API, licensing, Pro checks,
hooks offered, security signals, performance signals, tests.
→ What this means: one line.

## 4. How competitors solve it
| Plugin | Core solution flow (3–5 steps) | Strong | Weak |
|---|---|---|---|

## 5. 15-lens comparison
| Lens | Plugin A | Plugin B | Plugin C | Opportunity for us |
|---|---|---|---|---|
(Strong / OK / Weak with one evidence note each)

## 6. Complaints → code causes
| User complaint (Pain ID) | Code cause (confirmed / inferred) | How we avoid it |
|---|---|---|

## 7. Free / Pro & licensing patterns
| Plugin | Free/Pro mechanism | Licensing | Upsell placement | Lesson |
|---|---|---|---|---|

## 8. Our technical strategy
| Area | Decision | Why |
|---|---|---|
| Architecture | | |
| Data model | | |
| Core logic approach | | |
| Free/Pro mechanism | | |
| Licensing & updates | | |
| Performance | | |
| Security | | |
| Extensibility (hooks, REST, WP-CLI) | | |
| Admin UI | | |
| AI-agent readiness (Abilities/MCP) | | |

## 9. Feature technical table
| Feature | Areas touched | Hooks / APIs | Data storage | Risk | Effort |
|---|---|---|---|---|---|

## 10. Modern WooCommerce checklist
✅/⚠️/❌ per rule: HPOS CRUD, Store API/Checkout Blocks, Action Scheduler, full-page cache safe, emails, compatibility declarations, Plugin Check & guidelines.

## 11. Architecture & folder structure
Short tree + one line per module.

## 12. Testing plan
| Test area | How | Done when |
|---|---|---|

## 13. Build handoff
First 5 build actions + companion dev skills (review before installing).

## Limits
What wasn't analyzed (skipped Pro code, static-scan limits).
```
