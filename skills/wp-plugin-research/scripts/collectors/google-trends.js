/*
 * Google Trends collector — AGENT VERSION (returns JSON)
 * Rung 3 of the collection ladder (references/collectors.md).
 *
 * Use:
 *   1. In the agent's browser open https://trends.google.com/ (home page FIRST — sets cookies).
 *   2. Then open https://trends.google.com/trends/explore (any query is fine).
 *   3. Set KEYWORDS (max 5), GEO ('' = worldwide) and TIME below, then run this file.
 * Returns { check, timeline: {yearly, quarterly}, regions, related } — an INDEX (0-100), not volumes.
 *
 * Reading rules: very low volume shows as empty related queries and odd top regions — say so.
 * A one-quarter spike is not a trend. For absolute volumes use rung 5 (Keyword Planner CSV).
 * Calls Trends' own widget endpoints from inside the page, 2.5 s apart. Read-only.
 * Logic verified in a run on 2026-11-10; packaged afterwards — re-verify on first use.
 */
(async () => {
  const KEYWORDS = ['woocommerce product video'];   // up to 5
  const GEO = '';                                    // e.g. 'US'; '' = worldwide
  const TIME = 'today 5-y';
  const HL = 'en-US', TZ = new Date().getTimezoneOffset();
  const PAUSE = 2500;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const parse = t => JSON.parse(t.replace(/^\)\]\}',?\s*/, ''));
  const get = async (path, params) => {
    const url = `${path}?${new URLSearchParams(params)}`;
    const res = await fetch(url, { credentials: 'include' });
    await sleep(PAUSE);
    if (!res.ok) throw new Error(`${res.status} on ${path}`);
    return parse(await res.text());
  };
  const check = { keywords: KEYWORDS, geo: GEO || 'worldwide', time: TIME, errors: [] };

  const req = { comparisonItem: KEYWORDS.slice(0, 5).map(k => ({ keyword: k, geo: GEO, time: TIME })), category: 0, property: '' };
  let widgets;
  try {
    widgets = (await get('/trends/api/explore', { hl: HL, tz: TZ, req: JSON.stringify(req) })).widgets;
  } catch (e) {
    check.errors.push(`explore: ${e.message} — open the Trends home page first, then explore, then retry`);
    return { check };
  }
  const W = id => widgets.filter(w => w.id.startsWith(id));
  const out = { check, timeline: {}, regions: {}, related: {} };

  // Timeline → yearly and quarterly averages per keyword
  try {
    const ts = W('TIMESERIES')[0];
    const d = await get('/trends/api/widgetdata/multiline', { hl: HL, tz: TZ, req: JSON.stringify(ts.request), token: ts.token });
    const pts = d.default.timelineData.map(p => ({ t: new Date(Number(p.time) * 1000), v: p.value }));
    KEYWORDS.forEach((k, i) => {
      const yearly = {}, quarterly = {};
      for (const p of pts) {
        const y = p.t.getUTCFullYear(), q = `${y}-Q${Math.floor(p.t.getUTCMonth() / 3) + 1}`;
        (yearly[y] ||= []).push(p.v[i]); (quarterly[q] ||= []).push(p.v[i]);
      }
      const avg = o => Object.fromEntries(Object.entries(o).map(([k2, a]) => [k2, Math.round(a.reduce((s, x) => s + x, 0) / a.length)]));
      out.timeline[k] = { yearly: avg(yearly), quarterly: avg(quarterly) };
    });
    check.points = pts.length;
  } catch (e) { check.errors.push(`timeline: ${e.message}`); }

  // Regions (top 10 per keyword). With several keywords Trends returns ONE comparison
  // map whose value[] has one entry per keyword; with one keyword, one map.
  for (const [i, w] of W('GEO_MAP').entries()) {
    try {
      const d = await get('/trends/api/widgetdata/comparedgeo', { hl: HL, tz: TZ, req: JSON.stringify(w.request), token: w.token });
      const geo = d.default.geoMapData || [];
      const n = Math.max(1, ...geo.map(g => (g.value || []).length));
      for (let j = 0; j < n; j++) {
        const k = n > 1 ? (KEYWORDS[j] || `kw${j}`) : (KEYWORDS[i] || `kw${i}`);
        out.regions[k] = geo
          .filter(g => g.hasData?.[j] !== false && (g.value?.[j] || 0) > 0)
          .sort((a, b) => b.value[j] - a.value[j]).slice(0, 10)
          .map(g => ({ region: g.geoName, index: g.value[j] }));
      }
    } catch (e) { check.errors.push(`regions ${i}: ${e.message}`); }
  }

  // Related queries (top + rising)
  for (const [i, w] of W('RELATED_QUERIES').entries()) {
    try {
      const d = await get('/trends/api/widgetdata/relatedsearches', { hl: HL, tz: TZ, req: JSON.stringify(w.request), token: w.token });
      const lists = d.default.rankedList || [];
      out.related[KEYWORDS[i] || `kw${i}`] = {
        top: (lists[0]?.rankedKeyword || []).slice(0, 15).map(r => ({ query: r.query, value: r.value })),
        rising: (lists[1]?.rankedKeyword || []).slice(0, 15).map(r => ({ query: r.query, value: r.formattedValue })),
      };
    } catch (e) { check.errors.push(`related ${i}: ${e.message}`); }
  }
  check.lowVolumeHint = Object.values(out.related).every(r => !r.top.length) ? 'No related queries — volume is probably very low' : '';
  return out;
})();
