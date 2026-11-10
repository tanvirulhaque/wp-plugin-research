"""Shared polite HTTP helper for the collector scripts (standard library only).

SSL on macOS: Python from python.org ships without trusted root certificates,
so HTTPS fails with CERTIFICATE_VERIFY_FAILED. This helper fixes that without
turning verification off: Python's default store if it has certificates, else
the OS bundle (/etc/ssl/cert.pem on macOS), else `certifi`.
Verification is never disabled.
"""
import json, os, ssl, sys, time, urllib.error, urllib.request

UA = "Mozilla/5.0 (plugin-market-research; read-only)"
SSL_HINT = ("SSL certificates are missing for this Python. Fix once with ONE of:\n"
            "  pip3 install certifi\n"
            "  open \"/Applications/Python 3.$(python3 -c 'import sys;print(sys.version_info[1])')/Install Certificates.command\"")
_warned = False

def ssl_context():
    """Default store first (keeps company proxy certificates working); if it is empty
    (python.org macOS), the OS bundle; then certifi. Never disables verification."""
    ctx = ssl.create_default_context()
    if ctx.get_ca_certs():
        return ctx
    for bundle in ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt", "/etc/pki/tls/certs/ca-bundle.crt"):
        if os.path.exists(bundle):
            return ssl.create_default_context(cafile=bundle)
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ctx

CTX = ssl_context()

def is_ssl_error(e):
    return isinstance(e, ssl.SSLError) or "CERTIFICATE_VERIFY_FAILED" in str(e)

def open_url(url, timeout=30, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en", **(headers or {})})
    return urllib.request.urlopen(req, timeout=timeout, context=CTX)

def get(url, pause=1.0, timeout=30, as_json=False, retries=3):
    """GET with a pause after every call and simple retry on 429/5xx. Returns text, parsed JSON, or None."""
    global _warned
    for attempt in range(retries):
        try:
            with open_url(url, timeout) as r:
                body = r.read().decode("utf-8", "ignore")
            time.sleep(pause)
            return json.loads(body) if as_json else body
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                time.sleep(10 * (attempt + 1)); continue
            print(f"  HTTP {e.code}: {url}"); time.sleep(pause); return None
        except Exception as e:
            reason = getattr(e, "reason", e)
            if is_ssl_error(reason) or is_ssl_error(e):
                if not _warned:
                    print("  SSL error: " + SSL_HINT, file=sys.stderr); _warned = True
                return None
            print(f"  retry ({e.__class__.__name__}: {str(reason)[:80]}): {url}"); time.sleep(3)
    return None
