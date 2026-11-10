const fs = require('fs');
let src = fs.readFileSync(process.argv[2], 'utf8')
  .replace("const KEYWORDS = ['woocommerce product video'];", "const KEYWORDS = ['a','b'];")
  .replace("const PAUSE = 2500;", "const PAUSE = 0;");
const P = ")]}',\n";
global.fetch = async (url) => {
  const body = url.startsWith('/trends/api/explore') ? P + JSON.stringify({ widgets: [
      { id: 'TIMESERIES', request: {}, token: 't' }, { id: 'GEO_MAP', request: {}, token: 'g' },
      { id: 'RELATED_QUERIES', request: {}, token: 'r0' }, { id: 'RELATED_QUERIES_1', request: {}, token: 'r1' }] })
    : url.includes('multiline') ? P + JSON.stringify({ default: { timelineData: [
      { time: '1609459200', value: [10, 20] }, { time: '1640995200', value: [30, 0] }] } })
    : url.includes('comparedgeo') ? P + JSON.stringify({ default: { geoMapData: [
      { geoName: 'US', value: [80, 10], hasData: [true, true] }, { geoName: 'IN', value: [20, 90], hasData: [true, true] }] } })
    : P + JSON.stringify({ default: { rankedList: [{ rankedKeyword: [{ query: 'x', value: 100 }] }, { rankedKeyword: [] }] } });
  return { ok: true, text: async () => body };
};
global.window = {};
eval(src).then(r => console.log(JSON.stringify({ timeline: r.timeline, regions: r.regions, related: Object.keys(r.related), errors: r.check.errors })));
