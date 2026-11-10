/*
 * WooCommerce Marketplace review collector — USER CONSOLE VERSION (downloads files)
 * Rung 3/4 of the collection ladder (references/collectors.md).
 *
 * Use: open a woocommerce.com/products/<slug>/ page, scroll to Reviews,
 * open DevTools → Console, paste this file, press Enter.
 * Output: <slug>-reviews.csv and <slug>-reviews.json downloads (+ JSON on the clipboard).
 * For agents with a browser script tool, use woo-reviews-return.js instead (returns JSON).
 *
 * Read-only. Clicks only the page's own "next" link, ~1 s between pages.
 * Selectors last verified: 2026-11-10 (54 + 7 replies on Addify; 43 / 9 pages on FmeAddons).
 * Original script by the skill's user; self-check summary added.
 */
(async () => {
  // ---- Settings ----
  const LIST_SEL = 'ul.wccom-reviews-comments';
  const ITEM_SEL = 'li.wccom-reviews-comment';
  const NEXT_SEL = 'nav.woo-pagination a.page-numbers.next';
  const PAGE_DELAY = 1000;  // pause between pages (ms)
  const TIMEOUT = 20000;    // max wait for a page to load (ms)
  const MAX_PAGES = 500;    // safety stop

  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const txt = (root, sel) => root?.querySelector(sel)?.textContent.trim() || '';

  // Find an element that belongs to THIS review item, not to a reply nested inside it
  const own = (li, sel) =>
    [...li.querySelectorAll(sel)].find(el => el.closest(ITEM_SEL) === li) || null;
  const ownTxt = (li, sel) => own(li, sel)?.textContent.trim() || '';

  // Get text with <br> kept as line breaks
  const fullText = el => {
    if (!el) return '';
    const c = el.cloneNode(true);
    c.querySelectorAll('br').forEach(br => br.replaceWith('\n'));
    return c.textContent.replace(/[ \t]+/g, ' ').replace(/\n\s+/g, '\n').trim();
  };

  const parseReview = li => {
    const ratingText = ownTxt(li, '.wccom-reviews-comment__rating-wrapper .screen-reader-text');
    const m = ratingText.match(/Rated\s+([\d.]+)/i);
    // The "--full" measurement span holds the untruncated review text
    const body =
      own(li, '.wccom-read-more__measurement--full') ||
      own(li, '.wccom-read-more__content > span') ||
      own(li, '.wccom-reviews-comment__main');
    const parent = li.parentElement?.closest(ITEM_SEL);
    return {
      id: (li.id || '').replace('comment-', '') || `noid-${collected.size}-${Date.now()}`,
      replyTo: parent ? parent.id.replace('comment-', '') : '',
      rating: m ? Number(m[1]) : null,
      username: ownTxt(li, '.wccom-reviews-comment__username'),
      country: ownTxt(li, '.wccom-reviews-comment__country'),
      date: ownTxt(li, '.wccom-reviews-comment__date'),
      review: fullText(body),
    };
  };

  const signature = () =>
    [...document.querySelectorAll(ITEM_SEL)].map(li => li.id).join(',');

  const currentPage = () =>
    txt(document, 'nav.woo-pagination .page-numbers.current') || '?';

  const waitForNewPage = async prevSig => {
    const start = Date.now();
    while (Date.now() - start < TIMEOUT) {
      await sleep(250);
      const list = document.querySelector(LIST_SEL);
      if (list?.getAttribute('aria-busy') === 'true') continue;
      const sig = signature();
      if (sig && sig !== prevSig) return true;
    }
    return false;
  };

  const collected = new Map();
  const grab = () => {
    let added = 0;
    document.querySelectorAll(ITEM_SEL).forEach(li => {
      try {
        const r = parseReview(li);
        if (!collected.has(r.id)) { collected.set(r.id, r); added++; }
      } catch (e) {
        console.warn('Skipped an item that could not be parsed:', li, e);
      }
    });
    return added;
  };

  // ---- Go to page 1 first if needed ----
  if (currentPage() !== '1') {
    const first = document.querySelector('nav.woo-pagination a[data-tracks-page="1"]');
    if (first) {
      const sig = signature();
      first.click();
      await waitForNewPage(sig);
      await sleep(PAGE_DELAY);
    }
  }

  // ---- Loop through all pages ----
  for (let i = 0; i < MAX_PAGES; i++) {
    const added = grab();
    window.__wooPagesSeen = i + 1;
    console.log(`Page ${currentPage()}: +${added} (total ${collected.size})`);

    const next = document.querySelector(NEXT_SEL);
    if (!next || next.classList.contains('disabled') || next.getAttribute('aria-disabled') === 'true') {
      console.log('No more pages.');
      break;
    }
    const sig = signature();
    next.scrollIntoView({ block: 'center' });
    next.click();
    const ok = await waitForNewPage(sig);
    if (!ok) { console.warn('Timed out waiting for next page. Stopping.'); break; }
    await sleep(PAGE_DELAY);
  }

  const reviews = [...collected.values()];
  window.__wooReviews = reviews;
  console.table(reviews);

  // ---- Export ----
  const json = JSON.stringify(reviews, null, 2);
  const esc = v => `"${String(v ?? '').replace(/"/g, '""')}"`;
  const cols = ['id', 'replyTo', 'rating', 'username', 'country', 'date', 'review'];
  const csv = '\uFEFF' + [cols.join(','), ...reviews.map(r => cols.map(c => esc(r[c])).join(','))].join('\n');

  const download = (content, name, type) => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([content], { type }));
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
  };
  const slug = location.pathname.split('/').filter(Boolean).pop() || 'reviews';
  download(csv, `${slug}-reviews.csv`, 'text/csv;charset=utf-8');
  download(json, `${slug}-reviews.json`, 'application/json');

  // Copy JSON to clipboard (DevTools copy() works without page focus)
  try {
    if (typeof copy === 'function') copy(json);
    else await navigator.clipboard.writeText(json);
    console.log('JSON copied to clipboard.');
  } catch (e) {
    console.warn('Clipboard copy failed — use the downloaded files or run: copy(window.__wooReviews)');
  }

  const pagesSeen = window.__wooPagesSeen || '?';
  console.log(`Done: ${reviews.length} items collected (${reviews.filter(r => !r.replyTo).length} reviews, ${reviews.filter(r => r.replyTo).length} vendor/user replies). Self-check: hasNav=${!!document.querySelector('nav.woo-pagination')}, pages=${pagesSeen}`);
})();
