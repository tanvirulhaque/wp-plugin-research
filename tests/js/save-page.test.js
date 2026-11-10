const { JSDOM } = require('jsdom'); const fs = require('fs');
const dom = new JSDOM('<body><p>hi</p></body>', { runScripts: 'outside-only', url: 'https://old.reddit.com/r/woocommerce/search?q=product+video' });
let clicked = null;
dom.window.URL.createObjectURL = () => 'blob:x';
dom.window.HTMLAnchorElement.prototype.click = function () { clicked = this.download; };
const r = dom.window.eval(fs.readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify({ returned: r, downloaded: clicked }));
