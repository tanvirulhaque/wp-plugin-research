/*
 * WooCommerce Marketplace review collector — AGENT VERSION (returns JSON, no downloads)
 * Rung 3 of the collection ladder (references/collectors.md).
 *
 * Use: in the agent's browser, open https://woocommerce.com/products/<slug>/,
 * then run this file with the browser's "execute script" tool. The last
 * expression is a Promise that resolves to:
 *   { check: {pages, total, reviews, replies, hasNav, stoppedBy}, rows: [...] }
 * Save rows to raw/rev/<slug>-reviews.json. If check.hasNav is false or
 * pages === 1 with many reviews on the listing, re-inspect the selectors.
 *
 * Read-only. Uses the page's own pagination, ~1 s between pages.
 * Selectors last verified: 2026-11-10.
 */
(async () => {
  const SEL = {
    list: 'ul.wccom-reviews-comments',
    item: 'li.wccom-reviews-comment',
    next: 'nav.woo-pagination a.page-numbers.next',
    nav: 'nav.woo-pagination',
    current: 'nav.woo-pagination .page-numbers.current',
    first: 'nav.woo-pagination a[data-tracks-page="1"]',
    rating: '.wccom-reviews-comment__rating-wrapper .screen-reader-text',
    bodyFull: '.wccom-read-more__measurement--full',
    bodyAlt: '.wccom-read-more__content > span',
    bodyMain: '.wccom-reviews-comment__main',
    user: '.wccom-reviews-comment__username',
    country: '.wccom-reviews-comment__country',
    date: '.wccom-reviews-comment__date',
  };
  const PAGE_DELAY = 1000, TIMEOUT = 20000, MAX_PAGES = 200;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const own = (li, sel) => [...li.querySelectorAll(sel)].find(el => el.closest(SEL.item) === li) || null;
  const ownTxt = (li, sel) => own(li, sel)?.textContent.trim() || '';
  const fullText = el => {
    if (!el) return '';
    const c = el.cloneNode(true);
    c.querySelectorAll('br').forEach(br => br.replaceWith('\n'));
    return c.textContent.replace(/[ \t]+/g, ' ').replace(/\n\s+/g, '\n').trim();
  };
  const signature = () => [...document.querySelectorAll(SEL.item)].map(li => li.id).join(',');
  const waitForNewPage = async prev => {
    const start = Date.now();
    while (Date.now() - start < TIMEOUT) {
      await sleep(250);
      if (document.querySelector(SEL.list)?.getAttribute('aria-busy') === 'true') continue;
      const s = signature();
      if (s && s !== prev) return true;
    }
    return false;
  };
  const rows = new Map();
  const grab = () => document.querySelectorAll(SEL.item).forEach(li => {
    const m = ownTxt(li, SEL.rating).match(/Rated\s+([\d.]+)/i);
    const body = own(li, SEL.bodyFull) || own(li, SEL.bodyAlt) || own(li, SEL.bodyMain);
    const parent = li.parentElement?.closest(SEL.item);
    const id = (li.id || '').replace('comment-', '') || `noid-${rows.size}`;
    if (!rows.has(id)) rows.set(id, {
      id, replyTo: parent ? parent.id.replace('comment-', '') : '',
      rating: m ? Number(m[1]) : null, username: ownTxt(li, SEL.user),
      country: ownTxt(li, SEL.country), date: ownTxt(li, SEL.date), review: fullText(body),
    });
  });

  const hasNav = !!document.querySelector(SEL.nav);
  const cur = () => document.querySelector(SEL.current)?.textContent.trim() || '?';
  if (hasNav && cur() !== '1') {
    const f = document.querySelector(SEL.first);
    if (f) { const s = signature(); f.click(); await waitForNewPage(s); await sleep(PAGE_DELAY); }
  }
  let pages = 0, stoppedBy = 'no next link';
  for (; pages < MAX_PAGES; ) {
    grab(); pages++;
    const next = document.querySelector(SEL.next);
    if (!next || next.classList.contains('disabled') || next.getAttribute('aria-disabled') === 'true') break;
    const s = signature();
    next.scrollIntoView({ block: 'center' }); next.click();
    if (!(await waitForNewPage(s))) { stoppedBy = 'timeout'; break; }
    await sleep(PAGE_DELAY);
  }
  if (pages >= MAX_PAGES) stoppedBy = 'max pages';
  const out = [...rows.values()];
  window.__wooReviews = out;
  return {
    check: { pages, total: out.length, reviews: out.filter(r => !r.replyTo).length,
             replies: out.filter(r => r.replyTo).length, hasNav, stoppedBy,
             slug: location.pathname.split('/').filter(Boolean).pop() },
    rows: out,
  };
})();
