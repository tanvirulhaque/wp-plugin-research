#!/usr/bin/env python3
"""
Compare analyze_plugin.py outputs side by side (technical analytics table).

Usage:
  python compare_code.py "Name A=a.json" "Name B=b.json" ... > code-compare.md

Prints a Markdown table: size, requirements, WooCommerce readiness,
Free/Pro & licensing signals, extensibility, security and performance signals.
Signals are counts from static scanning - read the flagged files before judging.
"""
import json, sys

def load(arg):
    name, path = arg.split("=", 1)
    with open(path) as fh:
        return name, json.load(fh)

def yn(n): return "✅" if n else "❌"

ROWS = [
    ("Version", lambda r: r["header"].get("Version", "?")),
    ("Requires PHP", lambda r: r["header"].get("Requires PHP", r["header"].get("readme Requires PHP", "?"))),
    ("WC tested up to", lambda r: r["header"].get("WC tested up to", "?")),
    ("PHP lines (own code)", lambda r: f'{r["size"]["lines_by_ext"].get(".php", 0):,}'),
    ("Files > 1,500 lines", lambda r: len(r["size"]["largest_php_files"])),
    ("HPOS declared", lambda r: yn(r["woocommerce_compat"]["hpos_declared"])),
    ("Checkout Blocks declared", lambda r: yn(r["woocommerce_compat"]["blocks_declared"])),
    ("Store API / Blocks integration", lambda r: yn(r["woocommerce_compat"].get("store_api_usage", 0) + r["woocommerce_compat"]["checkout_blocks_integration"])),
    ("Abilities API (AI-agent ready)", lambda r: yn(r["woocommerce_compat"].get("abilities_api", 0))),
    ("Legacy order post-meta calls", lambda r: r["woocommerce_compat"]["legacy_order_postmeta"]),
    ("Action Scheduler used", lambda r: yn(r["entry_points"]["action_scheduler_calls"])),
    ("Licensing", lambda r: ", ".join(k for k in ["freemius", "edd_licensing", "custom_licensing"] if r["free_pro_licensing"][k]["count"]) or "none found"),
    ("Pro checks in code", lambda r: r["free_pro_licensing"]["pro_checks"]["count"]),
    ("Upsell / notice signals", lambda r: r["free_pro_licensing"]["upsell_notices"]["count"]),
    ("Hooks offered to developers", lambda r: r["hooks"]["offered_total"]),
    ("WooCommerce hooks used", lambda r: len(r["hooks"]["woocommerce_hooks_used"])),
    ("REST routes / AJAX actions", lambda r: f'{len(r["entry_points"]["rest_routes"])} / {len(r["entry_points"]["ajax_actions"])}'),
    ("Custom tables", lambda r: len(r["data_storage"]["custom_tables"])),
    ("Nonce checks", lambda r: r["security"]["nonce_checks"]),
    ("Capability checks", lambda r: r["security"]["capability_checks"]),
    ("Prepared SQL / raw SQL", lambda r: f'{r["security"]["prepared_sql"]} / {r["security"]["raw_sql"]}'),
    ("Superglobal reads (review)", lambda r: r["security"]["superglobals"]),
    ("Unlimited queries (-1)", lambda r: r["performance"]["posts_per_page_unlimited"]),
    ("Namespaced / React admin", lambda r: f'{yn(r["architecture"]["namespaces"])} / {yn(r["architecture"]["react_usage"])}'),
    ("Tests present", lambda r: yn(r["project_files"]["tests"] or r["project_files"]["phpunit"])),
]

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    plugins = [load(a) for a in sys.argv[1:]]
    print("| Signal | " + " | ".join(n for n, _ in plugins) + " |")
    print("|---|" + "---|" * len(plugins))
    for label, fn in ROWS:
        vals = []
        for _, r in plugins:
            try: vals.append(str(fn(r)))
            except Exception: vals.append("?")
        print(f"| {label} | " + " | ".join(vals) + " |")

if __name__ == "__main__":
    main()
