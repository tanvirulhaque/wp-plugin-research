/*
 * Save the current page's loaded HTML — NO permissions needed (rung 4 alternative).
 * Works in any Chrome-based browser (Chrome, Edge, Brave, Arc) on macOS, Windows or Linux.
 *
 * Use: open the page (e.g. an old.reddit.com search), open DevTools → Console,
 * paste this file, press Enter. It downloads <site>-<path>.html to your Downloads
 * folder. Move the files into raw/<source>/ and run the parser on that folder.
 * Tip: Chrome may ask once "Download multiple files?" — allow it for that site.
 * Read-only: it only reads the page you are looking at.
 */
(() => {
  const name = (location.hostname + location.pathname + location.search)
    .replace(/^www\./, '').replace(/[^A-Za-z0-9._-]+/g, '_').slice(0, 120) + '.html';
  const html = '<!-- saved from ' + location.href + ' on ' + new Date().toISOString() + ' -->\n'
    + document.documentElement.outerHTML;
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
  a.download = name;
  document.body.appendChild(a); a.click(); a.remove();
  console.log('Saved', name, '(' + Math.round(html.length / 1024) + ' KB)');
  return name;
})();
