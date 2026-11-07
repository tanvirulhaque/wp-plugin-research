#!/usr/bin/env python3
"""
Static inventory of a WordPress/WooCommerce plugin codebase.

Usage:
  python analyze_plugin.py <plugin_dir_or_zip> [--json out.json]

Produces a quick map so you know WHERE to read: structure, size, hooks used and
offered, data storage, REST/AJAX/cron entry points, WooCommerce compatibility
declarations, Free/Pro & licensing signals, security & performance signals,
dependencies, tests. It does not judge quality alone - read the flagged files.
"""
import json, os, re, sys, zipfile, tempfile
from collections import Counter, defaultdict

SKIP_DIRS = {"node_modules", ".git", "vendor_prefixed", "tests/_output"}

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
    "transients": r"(?:get|set|delete)_transient\(\s*['\"]([^'\"]+)",
}

SIGNALS = {
    # WooCommerce modern compatibility
    "hpos_declared": r"declare_compatibility\(\s*['\"]custom_order_tables['\"]",
    "blocks_declared": r"declare_compatibility\(\s*['\"]cart_checkout_blocks['\"]",
    "checkout_blocks_integration": r"IntegrationInterface|woocommerce_blocks_loaded|ExtendSchema|register_endpoint_data",
    "abilities_api": r"wp_register_ability\(|abilities_api_init",
    "store_api_usage": r"StoreApi|woocommerce_store_api_",
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
    # Code style / architecture
    "namespaces": r"^\s*namespace\s+[A-Za-z]",
    "classes": r"^\s*(?:final\s+|abstract\s+)?class\s+[A-Za-z_]",
    "rest_api_usage": r"register_rest_route",
    "wp_cli": r"WP_CLI::add_command",
    "i18n_calls": r"(?:__|_e|esc_html__|esc_html_e|_x|_n)\(\s*['\"]",
    "jquery_usage": r"jQuery|\$\(\s*document\s*\)",
    "react_usage": r"wp\.element|@wordpress/element|React\.|createElement\(",
}

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    root = unpack(sys.argv[1])
    out_json = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None

    ext_lines = Counter(); ext_files = Counter()
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
        if "/vendor/" in "/" + low and ext == ".php":
            ext_files["vendor_php"] += 1
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
        if name == "readme.txt":
            for key in ["Tested up to", "Stable tag", "Requires PHP"]:
                mm = re.search(re.escape(key) + r":\s*(.+)", txt)
                if mm: header["readme " + key] = mm.group(1).strip()
        if ext not in {".php", ".js", ".jsx", ".ts", ".tsx"}:
            continue
        for k, pat in PATTERNS.items():
            for m in re.finditer(pat, txt):
                val = ":".join(g for g in m.groups() if g) if m.groups() else "x"
                found[k][val] += 1
        for k, pat in SIGNALS.items():
            c = len(re.findall(pat, txt, flags=re.I | re.M))
            if c:
                signal_hits[k].append((rel, c))

    def total(k): return sum(c for _, c in signal_hits.get(k, []))
    def top_files(k, n=5):
        return sorted(signal_hits.get(k, []), key=lambda x: -x[1])[:n]

    wc_hooks = {h: c for h, c in found["hooks_used"].items() if h.startswith("woocommerce")}
    report = {
        "header": header,
        "size": {"lines_by_ext": dict(ext_lines), "files_by_ext": dict(ext_files),
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
        "free_pro_licensing": {k: {"count": total(k), "files": top_files(k)} for k in
            ["freemius", "edd_licensing", "custom_licensing", "pro_checks", "upsell_notices"]},
        "security": {k: total(k) for k in
            ["nonce_checks", "capability_checks", "sanitize_calls", "escape_calls",
             "prepared_sql", "raw_sql", "superglobals", "abspath_guard"]},
        "security_review_files": {"raw_sql": top_files("raw_sql"), "superglobals": top_files("superglobals")},
        "performance": {k: total(k) for k in
            ["enqueues", "global_enqueue_hint", "wc_get_orders_or_products",
             "posts_per_page_unlimited", "autoload_options"]},
        "performance_review_files": {"posts_per_page_unlimited": top_files("posts_per_page_unlimited")},
        "architecture": {k: total(k) for k in
            ["namespaces", "classes", "rest_api_usage", "wp_cli", "i18n_calls", "jquery_usage", "react_usage"]},
    }
    text = json.dumps(report, indent=2)
    if out_json:
        with open(out_json, "w") as fh: fh.write(text)
    print(text)

if __name__ == "__main__":
    main()
