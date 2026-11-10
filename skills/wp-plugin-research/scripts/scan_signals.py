#!/usr/bin/env python3
"""
Niche code-signal scan across MANY plugins (all free plugins found, plus local copies).

Usage:
  python scan_signals.py --dirs code/ [more dirs or plugin folders...] [--signals signals.json] \
      [--out raw/scan/signals] [--libs "slick|swiper|plyr"]

--dirs     plugin folders, or parent folders whose subfolders are plugins (e.g. code/ or wp-content/plugins/)
--signals  JSON {"name": "regex", ...} for THIS niche (gallery replacement, facade, schema, ...).
           Without it, a generic WooCommerce set is used. Write one per run in Phase 4/9.
Output: <out>.csv and <out>.json — one row per plugin: files matching each signal,
own PHP lines, JS+CSS KB, front-end libraries found.

Rules this enforces (from a real run):
  * Any "nobody does X" claim must come from this all-plugin scan and say "of N scanned".
  * vendor/, node_modules/ and minified files are skipped; files > 600 KB are skipped.
  * Loops are in Python (no shell word-splitting or unquoted globs).
"""
import argparse, csv, json, os, re

GENERIC = {
    "replaces_template": r"remove_action\(\s*'woocommerce_before_single_product_summary'|woocommerce_locate_template|wc_get_template",
    "native_gallery_hooks": r"woocommerce_single_product_image_thumbnail_html|'woocommerce_product_thumbnails'",
    "block_filters": r"render_block_woocommerce/|register_block_type",
    "store_api": r"woocommerce_store_api_|ExtendSchema",
    "hpos": r"custom_order_tables",
    "checkout_blocks": r"cart_checkout_blocks",
    "csv_import_export": r"woocommerce_product_import|product_export_column|woocommerce_csv_product",
    "rest": r"register_rest_(route|field)",
    "wpcli": r"WP_CLI::add_command",
    "elementor": r"elementor",
    "divi": r"et_builder|et_pb_",
    "theme_adapters": r"flatsome|astra|blocksy|kadence|woodmart|porto|avada|oceanwp",
    "wpml_polylang": r"wpml|polylang",
    "abilities_api": r"wp_register_ability",
    "tests": r"WP_UnitTestCase|PHPUnit",
}
LIBS = r"slick|swiper|flexslider|fancybox|video-?js|plyr|magnific|photoswipe|venobox|owl|lightgallery|glightbox|splide|fontawesome|font-awesome|html5lightbox|elevatezoom|lite-youtube"
SKIP = {"vendor", "node_modules", ".git"}

def plugin_dirs(paths):
    out = {}
    for p in paths:
        p = os.path.expanduser(p)
        if not os.path.isdir(p):
            print("skip (not a folder):", p); continue
        has_php = any(f.endswith(".php") for f in os.listdir(p))
        if has_php:
            out[os.path.basename(p.rstrip("/"))] = p
        else:
            for d in sorted(os.listdir(p)):
                full = os.path.join(p, d)
                if os.path.isdir(full) and any(f.endswith(".php") for _, _, fs in os.walk(full) for f in fs):
                    inner = [os.path.join(full, x) for x in os.listdir(full)]
                    # unzip layouts like code/<slug>/src/ or code/<slug>/<slug>/
                    sub = next((x for x in inner if os.path.isdir(x) and any(f.endswith(".php") for f in os.listdir(x))), None)
                    out[d] = full if any(f.endswith(".php") for f in os.listdir(full)) else (sub or full)
    return out

def scan(d, sig, libs_rx):
    txt = {}
    kb, libs = 0, set()
    for r, dirs, fs in os.walk(d):
        dirs[:] = [x for x in dirs if x not in SKIP]
        for f in fs:
            p = os.path.join(r, f)
            if f.endswith((".js", ".css")):
                kb += os.path.getsize(p) // 1024
                m = libs_rx.search(f)
                if m: libs.add(m.group(0).lower())
            if f.endswith((".php", ".js")) and not f.endswith(".min.js") and os.path.getsize(p) < 600_000:
                try: txt[p] = open(p, encoding="utf-8", errors="ignore").read()
                except OSError: pass
    row = {k: sum(1 for t in txt.values() if re.search(rx, t, re.I)) for k, rx in sig.items()}
    row["php_lines"] = sum(t.count("\n") for f, t in txt.items() if f.endswith(".php"))
    row["js_css_kb"] = kb
    row["libs"] = ",".join(sorted(libs))
    return row

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--signals", default="")
    ap.add_argument("--libs", default=LIBS)
    ap.add_argument("--out", default="raw/scan/signals")
    a = ap.parse_args()
    sig = json.load(open(a.signals)) if a.signals else GENERIC
    libs_rx = re.compile(a.libs, re.I)
    dirs = plugin_dirs(a.dirs)
    if not dirs:
        raise SystemExit("No plugin folders found.")
    out = {}
    for name, d in dirs.items():
        out[name] = scan(d, sig, libs_rx)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    cols = ["plugin"] + list(sig) + ["php_lines", "js_css_kb", "libs"]
    with open(a.out + ".csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for n, r in out.items(): w.writerow([n] + [r[c] for c in cols[1:]])
    json.dump({"scanned": len(out), "signals": sig, "plugins": out}, open(a.out + ".json", "w"), indent=1)
    print(f"Scanned {len(out)} plugins → {a.out}.csv / .json")
    for k in sig:
        n = sum(1 for r in out.values() if r[k])
        print(f"  {k}: {n} of {len(out)} scanned")

if __name__ == "__main__":
    main()
