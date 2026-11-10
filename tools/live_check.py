#!/usr/bin/env python3
"""
Live check for the network collectors — run on YOUR computer (not a sandbox).

Usage (from the repo root):
  python3 tools/live_check.py            # ~1-2 minutes, about 15 polite requests
  python3 tools/live_check.py --slug woocommerce-pdf-invoices-packing-slips --keyword "pdf invoice"

Runs each script once on a small, real target and prints PASS / FAIL with the
reason. Results are saved to live-check-report.md — paste that file back into
the chat that maintains the skill, so selectors and notes can be updated.

Read-only and rate-limited (about 1 s between requests). Browser-based
collectors (Marketplace reviews, Google Trends, demo probe, Chrome tab saver)
need a browser: see tools/LIVE-CHECK.md for their 2-minute manual checks.
"""
import argparse, datetime, json, os, platform, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "skills", "wp-plugin-research", "scripts")

def run(args, timeout=240):
    try:
        p = subprocess.run([sys.executable] + args, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        return 1, "timed out"

def load(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return {"__error__": str(e)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", default="woocommerce-pdf-invoices-packing-slips", help="a wordpress.org plugin with reviews and forum threads")
    ap.add_argument("--keyword", default="pdf invoice")
    ap.add_argument("--tag", default="invoice")
    a = ap.parse_args()
    tmp = tempfile.mkdtemp(prefix="wpr-live-")
    results = []

    def check(name, args, out, test, why):
        code, log = run(args + ["--out", out] if out else args)
        data = load(out) if out and os.path.exists(out) else {}
        try:
            ok, detail = test(data, log)
        except Exception as e:
            ok, detail = False, f"unexpected output: {e}"
        results.append((name, "PASS" if ok and code == 0 else "FAIL", detail if ok else f"{detail} | exit {code} | {log[-300:]}"))
        print(f"{'PASS' if ok and code == 0 else 'FAIL'}  {name}: {detail}")

    print(f"Live check — {datetime.date.today()} — {platform.system()} — target: {a.slug}\n")
    # SSL pre-flight: the #1 cause of "everything fails" on macOS python.org installs
    sys.path.insert(0, S)
    import _http
    try:
        import certifi; store = "certifi"
    except ImportError:
        store = "system bundle" if _http.CTX.get_ca_certs() else "Python default"
    try:
        _http.open_url("https://api.wordpress.org/core/version-check/1.7/", 20).read(200)
        results.append(("SSL / network pre-flight", "PASS", f"HTTPS works (certificates: {store})"))
        print(f"PASS  SSL / network pre-flight: HTTPS works (certificates: {store})")
    except Exception as e:
        msg = str(getattr(e, "reason", e))[:160]
        hint = _http.SSL_HINT if _http.is_ssl_error(getattr(e, "reason", e)) or _http.is_ssl_error(e) else "Check your internet connection, VPN or firewall."
        results.append(("SSL / network pre-flight", "FAIL", f"{msg} — {hint}"))
        print(f"FAIL  SSL / network pre-flight: {msg}\n      {hint}\n      Fix this first, then re-run; the other checks depend on it.\n")

    check("wporg_discover.py (API, keyword + tag)",
          [os.path.join(S, "wporg_discover.py"), "--keywords", a.keyword, "--tags", a.tag, "--pages", "1"],
          os.path.join(tmp, "discover.json"),
          lambda d, l: (d.get("screened", 0) > 0 and any(p.get("downloaded") is not None for p in d.get("plugins", {}).values()),
                        f"screened {d.get('screened')}, matched {d.get('matched')}, newcomers {d.get('newcomers', {}).get('count')}" + (", downloaded field present" if d.get("screened") else "; errors: " + "; ".join(d.get("errors", [])[:2]))),
          "API reachable and fields present")

    check("wporg_threads.py (forum titles)",
          [os.path.join(S, "wporg_threads.py"), a.slug, "--pages", "1"],
          os.path.join(tmp, "threads.json"),
          lambda d, l: (d.get("titles", 0) >= 5, f"{d.get('titles')} titles; top themes {list(d.get('theme_counts', {}).items())[:3]}"),
          "forum markup")

    check("wporg_reviews.py (1-star + newest 5-star)",
          [os.path.join(S, "wporg_reviews.py"), a.slug, "--stars", "1", "--newest5", "2", "--pages", "1"],
          os.path.join(tmp, "reviews.json"),
          lambda d, l: (isinstance(d, list) and len(d) >= 2 and sum(1 for r in d if r.get("text")) >= 2
                        and all(r.get("stars") for r in d)
                        and all(r.get("date") and any(ch.isdigit() for ch in r["date"][-4:]) for r in d),
                        f"{len(d) if isinstance(d, list) else 0} reviews, text in {sum(1 for r in d if r.get('text')) if isinstance(d, list) else 0}, "
                        f"stars in {sum(1 for r in d if r.get('stars')) if isinstance(d, list) else 0} (from page: {sum(1 for r in d if r.get('stars_source') == 'page') if isinstance(d, list) else 0}), sample date '{(d[0].get('date') if isinstance(d, list) and d else '')}'"),
          "review markup + full dates")

    check("autocomplete.py",
          [os.path.join(S, "autocomplete.py"), "woocommerce " + a.keyword],
          os.path.join(tmp, "ac.json"),
          lambda d, l: (sum(len(v) for v in d.values()) > 0, f"{sum(len(v) for v in d.values())} suggestions: {sum(d.values(), [])[:3]}"),
          "suggest endpoint")

    out = os.path.join(tmp, "code")
    code, log = run([os.path.join(S, "fetch_code.py"), a.slug, "--out", out])
    ok = code == 0 and os.path.exists(os.path.join(out, f"{a.slug}.zip"))
    src = next((ln for ln in log.splitlines() if ln.startswith("✓")), log[-200:])
    results.append(("fetch_code.py", "PASS" if ok else "FAIL", src))
    print(f"{'PASS' if ok else 'FAIL'}  fetch_code.py: {src}")

    if ok:
        j = os.path.join(tmp, "scan.json")
        code, log = run([os.path.join(S, "analyze_plugin.py"), os.path.join(out, f"{a.slug}.zip"), "--json", j, "--quiet"])
        results.append(("analyze_plugin.py on the download", "PASS" if code == 0 else "FAIL", log[-200:]))
        print(f"{'PASS' if code == 0 else 'FAIL'}  analyze_plugin.py: {log[-200:]}")

    passed = sum(1 for r in results if r[1] == "PASS")
    report = os.path.join(os.getcwd(), "live-check-report.md")
    with open(report, "w", encoding="utf-8") as fh:
        fh.write(f"# Live check report\n\n- Date: {datetime.date.today()}\n- OS: {platform.platform()}\n- Python: {platform.python_version()}\n- Target: {a.slug} / '{a.keyword}' / tag '{a.tag}'\n- Result: {passed} of {len(results)} passed\n\n")
        fh.write("| Script | Result | Detail |\n|---|---|---|\n")
        for n, r, d in results:
            fh.write(f"| {n} | {r} | {d.replace('|', '/').replace(chr(10), ' ')[:400]} |\n")
        fh.write("\n## Browser checks (fill in from tools/LIVE-CHECK.md)\n\n| Check | Result | Notes |\n|---|---|---|\n"
                 "| Marketplace reviews (woo-reviews-return.js) | | |\n| Google Trends (google-trends.js) | | |\n"
                 "| Demo probe (demo-probe.js) | | |\n| Chrome tab saver + Reddit parser | | |\n| Reddit API (optional, needs your keys) | | |\n")
    print(f"\n{passed} of {len(results)} passed. Report: {report}")
    print("Raw outputs kept in:", tmp)

if __name__ == "__main__":
    main()
