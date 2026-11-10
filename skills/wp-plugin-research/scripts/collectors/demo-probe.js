/*
 * Vendor demo probe — AGENT VERSION (returns JSON)
 * Rung 3. A "Pro without the zip" probe (label findings "not code-verified").
 *
 * Use: open a competitor's PUBLIC demo product page in the agent's browser,
 * wait for it to load (and click the video thumbnail once if you want to see
 * what loads on play), then run this file. Returns how the plugin renders:
 * gallery markup, whether the native WooCommerce gallery / zoom / lightbox
 * survive, video embeds and facades, and the scripts/styles the page loads.
 *
 * Read-only: reads the DOM and the browser's resource timing list.
 * Written 2026-11-10 from the run's checklist — verify on first use.
 */
(() => {
  const q = s => document.querySelectorAll(s);
  const has = s => q(s).length > 0;
  const kb = n => Math.round((n || 0) / 1024);
  const res = performance.getEntriesByType('resource');
  const scripts = res.filter(r => r.initiatorType === 'script' || /\.js(\?|$)/.test(r.name));
  const styles = res.filter(r => r.initiatorType === 'link' && /\.css(\?|$)/.test(r.name) || /\.css(\?|$)/.test(r.name));
  const size = r => r.transferSize || r.encodedBodySize || 0;
  const pluginOf = url => (url.match(/wp-content\/(plugins|themes)\/([^/]+)/) || [])[0]?.replace('wp-content/', '') || new URL(url).hostname;
  const byPlugin = {};
  for (const r of [...scripts, ...styles]) {
    const p = pluginOf(r.name);
    byPlugin[p] = byPlugin[p] || { files: 0, kb: 0 };
    byPlugin[p].files++; byPlugin[p].kb += kb(size(r));
  }
  const LIBS = /(slick|swiper|flexslider|fancybox|video-?js|plyr|magnific|photoswipe|venobox|owl|lightgallery|glightbox|splide|font-?awesome|lite-youtube|lite-vimeo|mediaelement)/i;
  const libs = [...new Set(res.map(r => (r.name.match(LIBS) || [])[1]?.toLowerCase()).filter(Boolean))];
  const iframes = [...q('iframe')].map(f => f.src || f.dataset.src || '').filter(s => /youtube|vimeo|wistia|loom/i.test(s));
  const galleryHtml = (document.querySelector('.woocommerce-product-gallery, .wp-block-woocommerce-product-gallery, [class*="product-gallery"], [class*="gallery"]')?.outerHTML || '').slice(0, 1500);
  return {
    check: { url: location.href, resources: res.length, note: 'Front-end only. Label findings "not code-verified".' },
    gallery: {
      nativeClassicGallery: has('.woocommerce-product-gallery'),
      nativeGalleryWrapper: has('.woocommerce-product-gallery__wrapper'),
      productGalleryBlock: has('.wp-block-woocommerce-product-gallery'),
      flexsliderViewport: has('.flex-viewport'),
      zoom: has('.zoomImg') || has('.woocommerce-product-gallery__trigger'),
      photoswipe: has('.pswp'),
      galleryClassNames: [...new Set([...q('[class*="gallery"]')].flatMap(e => [...e.classList]).filter(c => /gallery|slider|swiper|slick/i.test(c)))].slice(0, 25),
      galleryHtmlSample: galleryHtml,
    },
    video: {
      iframesLoaded: iframes,
      videoTags: [...q('video')].map(v => ({ src: v.currentSrc || v.src || v.querySelector('source')?.src || '', poster: v.poster || '', autoplay: v.autoplay, muted: v.muted, playsinline: v.playsInline, preload: v.preload })),
      facadeLikely: has('lite-youtube, lite-vimeo, [data-src*="youtube"], [data-video-id], [class*="facade"], [class*="video-placeholder"]') && iframes.length === 0,
      nocookie: iframes.some(s => /youtube-nocookie/.test(s)),
      videoObjectSchema: [...q('script[type="application/ld+json"]')].some(s => /VideoObject/.test(s.textContent)),
    },
    weight: {
      scripts: scripts.length, scriptKB: scripts.reduce((s, r) => s + kb(size(r)), 0),
      styles: styles.length, styleKB: styles.reduce((s, r) => s + kb(size(r)), 0),
      byPlugin: Object.entries(byPlugin).sort((a, b) => b[1].kb - a[1].kb).slice(0, 15).map(([p, v]) => ({ source: p, ...v })),
      libraries: libs,
      note: 'Sizes are transfer sizes from this page load; cached files can show 0 — reload with cache disabled for exact numbers.',
    },
  };
})();
