# Roadmap

Ideas under consideration. Nothing here is built yet.

## 💡 Gate the deep code check behind the verdict — status: deciding

**Idea:** read competitor Pro code only when the business research says the idea is worth it.

**Proposed flow**
1. **Step 1 (always):** business research + public technical info + light automatic scan of Free versions (free, minutes) → **preliminary verdict**.
2. **Gate:**
   - ❌ NO-GO → stop; no Pro licenses needed; suggest better ideas.
   - ⚠️ MAYBE → deep check (code often decides a MAYBE).
   - ✅ GO → deep check to build the technical strategy.
3. **Step 2 (GO / MAYBE):** deep check with Pro code → Technical Report → **final verdict**.
4. User can always say "do the deep check anyway".

**What each level shows**
| Level | Learns |
|---|---|
| No code | What competitors do and where they fail (reviews, docs, changelogs, vulnerability DBs) — "inferred" |
| Free code | Real compatibility, Free logic, data, speed, security signals |
| Free + Pro code | Pro features, how Pro is locked, Pro-only edge cases |

**Why:** saves money (no Pro licenses for NO-GO ideas), faster answers, verdict stays honest thanks to the free light scan.

**Caution:** code can change the verdict, so Step 1's verdict is labeled "preliminary".

**To implement:** Phase 3 code request → move to the gate; Phase 9 → split into light (Step 1) and deep (Step 2); Decision Summary → show preliminary vs final verdict.
