#!/usr/bin/env python3
"""
Download a plugin's FREE code when wordpress.org is blocked.

Usage:
  python fetch_code.py SLUG [--out DIR] [--expect-version X.Y.Z]

Tries, in order:
  1. https://downloads.wordpress.org/plugin/SLUG.zip
  2. GitHub mirrors on codeload.github.com:
     WordPressBugBounty/plugins-SLUG and common-repository/SLUG,
     branches master, main, trunk
Saves DIR/SLUG.zip (default DIR = ./code) and prints the source and the plugin
header Version. Compare it with the stable version on wordpress.org: mirrors
can lag behind. Never use this for paid (Pro) code - that comes from the user.
"""
import io, re, sys, time, urllib.request, zipfile, os

def candidates(slug):
    yield "wordpress.org", f"https://downloads.wordpress.org/plugin/{slug}.zip"
    for repo in (f"WordPressBugBounty/plugins-{slug}", f"common-repository/{slug}"):
        for br in ("master", "main", "trunk"):
            yield f"github:{repo}@{br}", f"https://codeload.github.com/{repo}/zip/refs/heads/{br}"

def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "wp-plugin-research/1.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def header_version(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for n in z.namelist():
            if n.endswith(".php") and n.count("/") <= 2:
                head = z.read(n)[:8192].decode("utf-8", "ignore")
                if "Plugin Name:" in head:
                    m = re.search(r"Version:\s*([^\s*]+)", head)
                    return n, (m.group(1) if m else "?")
    return None, "?"

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    slug = sys.argv[1]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "code"
    expect = sys.argv[sys.argv.index("--expect-version") + 1] if "--expect-version" in sys.argv else None
    os.makedirs(out, exist_ok=True)
    for label, url in candidates(slug):
        try:
            data = get(url)
            if not zipfile.is_zipfile(io.BytesIO(data)):
                raise ValueError("not a zip")
            main_file, ver = header_version(data)
            if not main_file:
                raise ValueError("no plugin header found")
        except Exception as e:
            print(f"  ✗ {label}: {str(e)[:60]}")
            time.sleep(0.5)
            continue
        path = os.path.join(out, f"{slug}.zip")
        with open(path, "wb") as fh:
            fh.write(data)
        note = ""
        if expect and ver != expect:
            note = f"  ⚠️ version {ver} differs from expected {expect} - mirror may lag"
        print(f"✓ {slug}: {label} → {path} (Version {ver}){note}")
        return 0
    print(f"✗ {slug}: no source worked. Add it to the user's code request.")
    return 2

if __name__ == "__main__":
    sys.exit(main())
