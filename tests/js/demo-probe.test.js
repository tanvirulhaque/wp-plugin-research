const { JSDOM } = require('jsdom'); const fs = require('fs');
const dom = new JSDOM(`<body><div class="woocommerce-product-gallery woocommerce-product-gallery--with-images"><div class="woocommerce-product-gallery__wrapper"><div class="swiper-slide"><iframe src="https://www.youtube-nocookie.com/embed/x"></iframe></div></div></div><script type="application/ld+json">{"@type":"VideoObject"}</script></body>`, { runScripts: 'outside-only', url: 'https://demo.example.com/product/x/' });
dom.window.performance.getEntriesByType = () => [{ name: 'https://demo.example.com/wp-content/plugins/pv-pro/assets/swiper.min.js', initiatorType: 'script', transferSize: 40960 }];
const r = dom.window.eval(fs.readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify({ g: r.gallery.nativeClassicGallery, iframes: r.video.iframesLoaded.length, nocookie: r.video.nocookie, schema: r.video.videoObjectSchema, libs: r.weight.libraries, by: r.weight.byPlugin }));
