#!/usr/bin/env python3
"""
Static inventory of a WordPress/WooCommerce plugin codebase.

Usage:
  python analyze_plugin.py <plugin_dir_or_zip> [--json out.json] [--quiet]

Produces a quick map so you know WHERE to read: structure, size, hooks used and
offered, data storage, REST/AJAX/cron entry points, WooCommerce compatibility
declarations, Free/Pro & licensing signals, security & performance signals,
dependencies, tests. It does not judge quality alone - read the flagged files.
"""
import json, os, re, sys, zipfile, tempfile
from collections import Counter, defaultdict

SKIP_DIRS = {".git", "tests/_output"}
# Third-party code bundled inside plugins: counted separately, not analyzed as the plugin's own code
BUNDLED_DIRS = {"node_modules", "vendor", "vendor_prefixed", "freemius",
                "plugin-update-checker", "action-scheduler"}
# Often third-party, but sometimes the plugin's own code: still analyzed, listed for a human check
MAYBE_BUNDLED_DIRS = {"lib", "libs", "libraries", "sdk", "third-party", "packages"}
# Hooks that run on (almost) every request: heavy work here slows every page
HOT_HOOKS = {"init", "wp", "wp_loaded", "plugins_loaded", "template_redirect", "wp_head",
             "woocommerce_cart_loaded_from_session", "woocommerce_before_mini_cart",
             "woocommerce_init", "woocommerce_loaded"}
HEAVY_IN_HOT = r"calculate_totals\(|new\s+WP_Query\(|get_posts\(|wc_get_products\(|wc_get_orders\(|\$wpdb->(?:get_results|query|get_col)\(|foreach\s*\(\s*WC\(\)->cart->get_cart\("

def unpack(path):
    if zipfile.is_zipfile(path):
        d = tempfile.mkdtemp(prefix="plugin_")
        with zipfile.ZipFile(path) as z:
            z.extractall(d)
        return d
    return path

def iter_files(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [x for x in dns if x not in SKIP_DIRS]
        for f in fns:
            yield os.path.join(dp, f)

def read(p):
    try:
        with open(p, encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except Exception:
        return ""

PATTERNS = {
    # hooks the plugin USES (integration points into WP/WC)
    "hooks_used": r"add_(?:action|filter)\(\s*['\"]([^'\"]+)['\"]",
    # hooks the plugin OFFERS (its own extension API)
    "hooks_offered": r"(?:do_action|apply_filters)(?:_ref_array|_deprecated)?\(\s*['\"]([^'\"]+)['\"]",
    "shortcodes": r"add_shortcode\(\s*['\"]([^'\"]+)['\"]",
    "rest_routes": r"register_rest_route\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]",
    "ajax_actions": r"['\"]wp_ajax_(?:nopriv_)?([a-zA-Z0-9_\-]+)['\"]",
    "cron_events": r"wp_schedule_(?:single_)?event\([^;]*?['\"]([a-zA-Z0-9_\-]+)['\"]",
    "action_scheduler": r"as_(?:schedule_single_action|schedule_recurring_action|enqueue_async_action)\(",
    "options": r"(?:get|update|add|delete)_option\(\s*['\"]([^'\"]+)['\"]",
    "post_meta_keys": r"(?:get|update|add|delete)_post_meta\([^,]+,\s*['\"]([^'\"]+)['\"]",
    "wc_meta_api": r"->(?:get|update|add|delete)_meta(?:_data)?\(\s*['\"]([^'\"]+)['\"]",
    "custom_tables": r"CREATE TABLE(?: IF NOT EXISTS)?\s+([^\s(]+)",
    "post_types": r"register_post_type\(\s*['\"]([^'\"]+)['\"]",
    "taxonomies": r"register_taxonomy\(\s*['\"]([^'\"]+)['\"]",
    "blocks": r"register_block_type(?:_from_metadata)?\(",
    "transients": r"(?:get|set|delete)_(?:site_)?transient\(\s*['\"]([^'\"]+)",
}

SIGNALS = {
    # WooCommerce modern compatibility
    "hpos_declared": r"declare_compatibility\(\s*['\"]custom_order_tables['\"]",
    "blocks_declared": r"declare_compatibility\(\s*['\"]cart_checkout_blocks['\"]",
    "checkout_blocks_integration": r"IntegrationInterface|woocommerce_blocks_loaded|ExtendSchema|register_endpoint_data|registerCheckoutFilters|woocommerce_blocks_[a-z_]+_block_registration|registerPaymentMethod",
    "abilities_api": r"wp_register_ability\(|abilities_api_init",
    "store_api_usage": r"StoreApi|woocommerce_store_api_|wc/store/v1|ExtendSchema",
    "legacy_order_postmeta": r"get_post_meta\(\s*\$order_id|get_post_meta\(\s*\$order->get_id",
    # Free / Pro / licensing
    "freemius": r"fs_dynamic_init|freemius|__premium_only|is__premium_only|can_use_premium_code",
    "edd_licensing": r"EDD_SL_Plugin_Updater|edd_action.*activate_license",
    "custom_licensing": r"license_key|activate_license|check_license",
    "pro_checks": r"class_exists\(\s*['\"][A-Za-z_\\\\]*Pro|defined\(\s*['\"][A-Z_]*PRO[A-Z_]*['\"]|is_pro\(|is_premium\(|has_pro\(",
    "upsell_notices": r"admin_notices|upgrade to pro|go pro|get pro|upgrade now",
    # Security
    "nonce_checks": r"wp_verify_nonce|check_admin_referer|check_ajax_referer",
    "capability_checks": r"current_user_can\(",
    "sanitize_calls": r"sanitize_[a-z_]+\(|absint\(|intval\(|wp_kses",
    "escape_calls": r"esc_(?:html|attr|url|js|textarea)(?:_e|__)?\(|wp_kses_post\(",
    "prepared_sql": r"\$wpdb->prepare\(",
    "raw_sql": r"\$wpdb->(?:query|get_results|get_var|get_row|get_col)\(\s*[\"'][^\"']*\$",
    "superglobals": r"\$_(?:GET|POST|REQUEST|COOKIE)\[",
    "abspath_guard": r"defined\(\s*['\"]ABSPATH['\"]\s*\)",
    # Performance
    "enqueues": r"wp_enqueue_(?:script|style)\(",
    "global_enqueue_hint": r"add_action\(\s*['\"]wp_enqueue_scripts['\"]",
    "wc_get_orders_or_products": r"wc_get_orders\(|wc_get_products\(|WP_Query\(",
    "posts_per_page_unlimited": r"['\"](?:posts_per_page|limit|numberposts)['\"]\s*=>\s*-1",
    "autoload_options": r"add_option\([^)]*,\s*(?:['\"]yes['\"]|true)\s*\)",
    "caching_calls": r"set_(?:site_)?transient\(|wp_cache_(?:get|set|add)\(",
    "remote_calls": r"wp_remote_(?:post|get|request)\(|wp_safe_remote_(?:post|get)\(",
    "delegated_wc_ajax": r"WC_AJAX::",
    # Code style / architecture
    "namespaces": r"^\s*namespace\s+[A-Za-z]",
    "classes": r"^\s*(?:final\s+|abstract\s+)?class\s+[A-Za-z_]",
    "rest_api_usage": r"register_rest_route",
    "wp_cli": r"WP_CLI::add_command",
    "i18n_calls": r"(?:__|_e|esc_html__|esc_html_e|_x|_n)\(\s*['\"]",
    "jquery_usage": r"jQuery|\$\(\s*document\s*\)",
    "react_usage": r"wp\.element|@wordpress/element|from\s+['\"]react['\"]|React\.|createElement\(|useState\(",
}

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    root = unpack(sys.argv[1])
    out_json = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None

    quiet = "--quiet" in sys.argv
    ext_lines = Counter(); ext_files = Counter()
    bundled_lines = Counter(); bundled_dirs = Counter(); maybe_bundled = Counter()
    php_texts = {}
    readme = {}
    found = defaultdict(Counter)
    signal_hits = defaultdict(list)
    header = {}
    big_files = []
    has = {"composer.json": False, "package.json": False, "tests": False,
           "phpunit": False, "uninstall.php": False, "readme.txt": False,
           "block.json": False, "languages": False}

    for p in iter_files(root):
        rel = os.path.relpath(p, root)
        name = os.path.basename(p)
        ext = os.path.splitext(p)[1].lower()
        low = rel.lower()
        if name in has: has[name] = True
        if "/tests/" in "/" + low or low.startswith("tests"): has["tests"] = True
        if "phpunit" in name: has["phpunit"] = True
        if "/languages/" in "/" + low: has["languages"] = True
        if ext not in {".php", ".js", ".jsx", ".ts", ".tsx", ".css", ".scss", ".json", ".txt"}:
            continue
        parts = low.replace("\\", "/").split("/")
        maybe = next((d for d in parts[:-1] if d in MAYBE_BUNDLED_DIRS), None)
        if maybe:
            maybe_bundled[maybe] += 1
        hit = next((d for d in parts[:-1] if d in BUNDLED_DIRS), None)
        if hit:
            bundled_dirs[hit] += 1
            if ext in {".php", ".js"}:
                bundled_lines[ext] += read(p).count("\n") + 1
            continue
        if ext == ".js" and (".min." in name or "/build/" in "/" + low or "/dist/" in "/" + low):
            ext_files["built_js"] += 1
            continue
        txt = read(p)
        n = txt.count("\n") + 1
        ext_lines[ext] += n; ext_files[ext] += 1
        if ext == ".php" and n > 1500:
            big_files.append((rel, n))
        if ext == ".php" and "Plugin Name" not in header:
            m = re.search(r"Plugin Name:\s*(.+)", txt)
            if m:
                header["file"] = rel
                for key in ["Plugin Name", "Version", "Requires at least", "Requires PHP",
                            "WC requires at least", "WC tested up to", "Text Domain",
                            "Requires Plugins", "Author"]:
                    mm = re.search(re.escape(key) + r":\s*(.+)", txt)
                    if mm: header[key] = mm.group(1).strip()
        if name.lower() == "readme.txt" and low.count("/") <= 1:
            for key in ["Requires at least", "Tested up to", "Stable tag", "Requires PHP",
                        "WC requires at least", "WC tested up to"]:
                mm = re.search(r"^\s*" + re.escape(key) + r":\s*(.+)$", txt, flags=re.I | re.M)
                if mm: readme[key] = mm.group(1).strip()
        if ext not in {".php", ".js", ".jsx", ".ts", ".tsx"}:
            continue
        if ext == ".php":
            php_texts[rel] = txt
        for k, pat in PATTERNS.items():
            for m in re.finditer(pat, txt):
                val = ":".join(g for g in m.groups() if g) if m.groups() else "x"
                found[k][val] += 1
        for k, pat in SIGNALS.items():
            c = len(re.findall(pat, txt, flags=re.I | re.M))
            if c:
                signal_hits[k].append((rel, c))

    # merge readme.txt values where the plugin header is silent
    for key, val in readme.items():
        header.setdefault(key, val)
        header["readme " + key] = val

    def is_admin(rel): return "admin" in rel.lower()

    # hot-path heuristic: callbacks on every-request hooks that do heavy cart/query work
    func_bodies = {}
    for rel, txt in php_texts.items():
        starts = [(m.start(), m.group(1)) for m in re.finditer(r"function\s+&?\s*([A-Za-z0-9_]+)\s*\(", txt)]
        for i, (pos, fname) in enumerate(starts):
            end = starts[i + 1][0] if i + 1 < len(starts) else min(len(txt), pos + 8000)
            func_bodies.setdefault(fname, []).append((rel, txt[pos:end]))
    hot_path = []
    hook_re = re.compile(r"add_(?:action|filter)\(\s*['\"]([a-z0-9_]+)['\"]\s*,(.{0,160}?)\)", re.S)
    for rel, txt in php_texts.items():
        for m in hook_re.finditer(txt):
            hook = m.group(1)
            if hook not in HOT_HOOKS:
                continue
            names = re.findall(r"['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]", m.group(2))
            if not names:
                continue
            cb = names[-1]
            for frel, body in func_bodies.get(cb, []):
                heavy = sorted(set(re.findall(HEAVY_IN_HOT, body)))
                if heavy:
                    hot_path.append({"hook": hook, "callback": cb, "registered_in": rel,
                                     "defined_in": frel, "heavy_calls": [f.strip("(") for f in heavy],
                                     "admin_path": is_admin(frel)})
    # telemetry: remote calls outside update/licensing code
    telemetry = [(rel, c) for rel, c in signal_hits.get("remote_calls", [])
                 if not re.search(r"updat|licen|sdk|api-client", rel, flags=re.I)]

    def split(k):
        hits = signal_hits.get(k, [])
        return {"front_end": sum(c for r, c in hits if not is_admin(r)),
                "admin": sum(c for r, c in hits if is_admin(r))}

    tsx_jsx = ext_files.get(".tsx", 0) + ext_files.get(".jsx", 0)

    def total(k): return sum(c for _, c in signal_hits.get(k, []))
    def top_files(k, n=5):
        return sorted(signal_hits.get(k, []), key=lambda x: -x[1])[:n]

    wc_hooks = {h: c for h, c in found["hooks_used"].items() if h.startswith("woocommerce")}
    report = {
        "header": header,
        "size": {"lines_by_ext": dict(ext_lines), "files_by_ext": dict(ext_files),
                 "bundled_lines_by_ext": dict(bundled_lines),
                 "bundled_dirs": dict(bundled_dirs),
                 "maybe_bundled_dirs_analyzed_as_own": dict(maybe_bundled),
                 "largest_php_files": sorted(big_files, key=lambda x: -x[1])[:10]},
        "project_files": has,
        "entry_points": {
            "rest_routes": list(found["rest_routes"]),
            "ajax_actions": list(found["ajax_actions"]),
            "cron_events": list(found["cron_events"]),
            "action_scheduler_calls": sum(found["action_scheduler"].values()),
            "shortcodes": list(found["shortcodes"]),
            "blocks_registered": sum(found["blocks"].values()),
            "post_types": list(found["post_types"]),
            "taxonomies": list(found["taxonomies"]),
        },
        "hooks": {
            "used_total": len(found["hooks_used"]),
            "woocommerce_hooks_used": dict(sorted(wc_hooks.items(), key=lambda x: -x[1])[:60]),
            "wp_hooks_used_top": dict(Counter({h: c for h, c in found["hooks_used"].items()
                                               if not h.startswith("woocommerce")}).most_common(30)),
            "offered_total": len(found["hooks_offered"]),
            "offered_sample": [h for h, _ in found["hooks_offered"].most_common(40)],
        },
        "data_storage": {
            "options": list(found["options"])[:60],
            "post_meta_keys": list(found["post_meta_keys"])[:60],
            "wc_crud_meta_keys": list(found["wc_meta_api"])[:60],
            "custom_tables": list(found["custom_tables"]),
            "transients": list(found["transients"])[:30],
        },
        "woocommerce_compat": {k: total(k) for k in
            ["hpos_declared", "blocks_declared", "checkout_blocks_integration", "store_api_usage", "abilities_api", "legacy_order_postmeta"]},
        "woocommerce_compat_note": "0 means 'not found in this code' - declarations can live in a Pro plugin or helper; confirm before calling it missing.",
        "free_pro_licensing": {k: {"count": total(k), "files": top_files(k)} for k in
            ["freemius", "edd_licensing", "custom_licensing", "pro_checks", "upsell_notices"]},
        "security": {k: total(k) for k in
            ["nonce_checks", "capability_checks", "sanitize_calls", "escape_calls",
             "prepared_sql", "raw_sql", "superglobals", "abspath_guard"]},
        "security_review_files": {"raw_sql": top_files("raw_sql"), "superglobals": top_files("superglobals")},
        "security_delegated": {"wc_ajax_calls": total("delegated_wc_ajax"),
            "note": "Handlers that call WC_AJAX:: methods delegate nonce/capability checks to WooCommerce core - label them 'delegated', not 'missing'."},
        "performance": {
            **{k: total(k) for k in ["enqueues", "global_enqueue_hint", "autoload_options", "caching_calls",
                                     "wc_get_orders_or_products", "posts_per_page_unlimited"]},
            "queries": split("wc_get_orders_or_products"),
            "unlimited_queries": split("posts_per_page_unlimited"),
            "hot_path": hot_path[:25],
            "hot_path_front_end_count": sum(1 for h in hot_path if not h["admin_path"]),
        },
        "telemetry_review": {"files": sorted(telemetry, key=lambda x: -x[1])[:8],
            "note": "Remote calls outside update/licensing code - check whether they are opt-in."},
        "performance_review_files": {"posts_per_page_unlimited": top_files("posts_per_page_unlimited")},
        "architecture": {**{k: total(k) for k in
            ["namespaces", "classes", "rest_api_usage", "wp_cli", "i18n_calls", "jquery_usage", "react_usage"]},
            "tsx_jsx_files": tsx_jsx,
            "react_admin_likely": bool(tsx_jsx or total("react_usage"))},
    }
    text = json.dumps(report, indent=2)
    if out_json:
        with open(out_json, "w") as fh: fh.write(text)
    if quiet:
        print(f"Saved {out_json or '(no --json given)'}: {ext_lines.get('.php', 0):,} own PHP lines, "
              f"{bundled_lines.get('.php', 0):,} bundled, {len(hot_path)} hot-path findings")
        return
    try:
        print(text)
    except BrokenPipeError:
        try: sys.stdout.close()
        except Exception: pass

if __name__ == "__main__":
    main()
