const { JSDOM } = require('jsdom'); const fs = require('fs');
const pages = [[1,2,3],[4,5,6],[7]];
const item = (id, reply) => `<li class="wccom-reviews-comment" id="comment-${id}"><div class="wccom-reviews-comment__rating-wrapper"><span class="screen-reader-text">Rated ${id%5+1} out of 5</span></div><span class="wccom-reviews-comment__username">u${id}</span><span class="wccom-reviews-comment__date">2026-01-0${id%9+1}</span><div class="wccom-read-more__measurement--full">Review ${id}<br>line2</div>${reply?`<ul><li class="wccom-reviews-comment" id="comment-${id}00"><span class="wccom-reviews-comment__username">vendor</span><div class="wccom-read-more__measurement--full">Reply to ${id}</div></li></ul>`:''}</li>`;
const render = (doc, p) => {
  doc.querySelector('ul.wccom-reviews-comments').innerHTML = pages[p].map(i => item(i, i===2)).join('');
  doc.querySelector('nav').innerHTML = `<span class="page-numbers current">${p+1}</span>` + (p < pages.length-1 ? `<a class="page-numbers next" href="#">Next</a>` : '');
  const n = doc.querySelector('a.next'); if (n) n.addEventListener('click', e => { e.preventDefault(); setTimeout(() => render(doc, p+1), 300); });
};
const dom = new JSDOM(`<body><ul class="wccom-reviews-comments"></ul><nav class="woo-pagination"></nav></body>`, { runScripts: 'outside-only', pretendToBeVisual: true });
dom.window.HTMLElement.prototype.scrollIntoView = () => {};
render(dom.window.document, 0);
dom.window.eval(`window.__p = ${fs.readFileSync(process.argv[2],'utf8')}`);
dom.window.__p.then(r => { console.log(JSON.stringify(r.check)); console.log(r.rows.map(x=>x.id+':'+(x.replyTo||'-')+':'+x.rating).join(' ')); });
