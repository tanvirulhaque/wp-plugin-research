#!/usr/bin/env python3
"""
Reddit thread collector using Reddit's official API (read-only, app-only login).

Why this instead of the console script: Reddit now answers 403 to the old
".json" page addresses, even in a logged-in browser. The official API is the
supported way to read public threads.

One-time setup (2 minutes, done by you):
  1. Go to https://www.reddit.com/prefs/apps  ->  "create another app..."
  2. Type: "script". Name: anything. Redirect URI: http://localhost:8080
  3. Copy the id (under the app name) and the secret.

Run (in your own terminal, so the keys never pass through chat):
  export REDDIT_CLIENT_ID=your_id
  export REDDIT_CLIENT_SECRET=your_secret
  python3 reddit_collector.py

  python3 reddit_collector.py --subs "woocommerce,Wordpress,ecommerce" \
      --queries "product video,video product gallery" --relevant video --out raw/reddit/api.json

Rung 5 of the collection ladder (references/collectors.md). Status: written, UNTESTED.
Output: JSON with threads + top comments. Read-only; nothing is posted or changed.
Skip site-wide searches sorted by "new" unless needed - they returned noise in testing.
"""
import argparse, base64, json, os, re, sys, time, urllib.parse, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _http import CTX

AP = argparse.ArgumentParser()
AP.add_argument("--subs", default="woocommerce,Wordpress,ProWordPress,ecommerce")
AP.add_argument("--queries", required=False, default="", help="comma list of phrases from the Phase 1 keyword list")
AP.add_argument("--sitewide", default="", help="optional comma list of site-wide searches")
AP.add_argument("--relevant", default="", help="regex a title/body must match (e.g. the core word)")
AP.add_argument("--out", default="raw/reddit/api.json")
ARGS = AP.parse_args()
SUBS = [s.strip() for s in ARGS.subs.split(",") if s.strip()]
QUERIES = [q.strip() for q in ARGS.queries.split(",") if q.strip()]
SITEWIDE = [q.strip() for q in ARGS.sitewide.split(",") if q.strip()]
MAX_PAGES = 5       # 5 x 100 results per search
MAX_COMMENTS = 25   # top comments kept per thread
PAUSE = 1.1         # seconds between calls (API allows about 100 per minute)
RELEVANT = re.compile(ARGS.relevant or ".", re.I)
UA = os.environ.get("REDDIT_USER_AGENT", "script:plugin-market-research:1.0")
OUT = ARGS.out


def token():
    cid, sec = os.environ.get("REDDIT_CLIENT_ID"), os.environ.get("REDDIT_CLIENT_SECRET")
    if not cid or not sec:
        sys.exit("Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET first (see the top of this file).")
    req = urllib.request.Request(
        "https://www.reddit.com/api/v1/access_token",
        data=b"grant_type=client_credentials",
        headers={"Authorization": "Basic " + base64.b64encode(f"{cid}:{sec}".encode()).decode(), "User-Agent": UA},
    )
    try:
        return json.load(urllib.request.urlopen(req, timeout=30, context=CTX))["access_token"]
    except urllib.error.HTTPError as e:
        sys.exit(f"Login failed ({e.code}). Check the id and secret, and that the app type is 'script'.")


def get(path, tok, params):
    url = "https://oauth.reddit.com" + path + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok, "User-Agent": UA})
            data = json.load(urllib.request.urlopen(req, timeout=30, context=CTX))
            time.sleep(PAUSE)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("  rate limited, waiting 60s"); time.sleep(60); continue
            print(f"  {e.code} for {path} {params.get('q', '')}"); time.sleep(PAUSE); return None
        except Exception as e:  # network hiccup
            print("  retry:", e); time.sleep(5)
    return None


def main():
    if not QUERIES:
        sys.exit("Give --queries (phrases from the keyword list).")
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    tok = token()
    threads = {}

    def collect(path, q, label, restrict):
        after = None
        for _ in range(MAX_PAGES):
            p = {"q": q, "limit": 100, "sort": "new", "t": "all", "raw_json": 1, "type": "link"}
            if restrict: p["restrict_sr"] = 1
            if after: p["after"] = after
            j = get(path, tok, p)
            if not j or "data" not in j: break
            for c in j["data"]["children"]:
                d = c["data"]
                if not RELEVANT.search(d.get("title", "") + " " + d.get("selftext", "")): continue
                t = threads.setdefault(d["id"], {
                    "id": d["id"], "sub": d["subreddit"],
                    "date": time.strftime("%Y-%m-%d", time.gmtime(d["created_utc"])),
                    "score": d["score"], "num_comments": d["num_comments"], "title": d["title"],
                    "url": "https://www.reddit.com" + d["permalink"], "permalink": d["permalink"],
                    "text": d.get("selftext", "")[:3000], "found_by": [], "comments": [],
                })
                if label not in t["found_by"]: t["found_by"].append(label)
            after = j["data"].get("after")
            if not after: break
        print(f"{label} -> {len(threads)} threads so far")

    for s in SUBS:
        for q in QUERIES:
            collect(f"/r/{s}/search", q, f"r/{s}: {q}", True)
    for q in SITEWIDE:
        collect("/search", q, f"all: {q}", False)

    todo = [t for t in threads.values() if t["num_comments"]]
    for i, t in enumerate(todo, 1):
        j = get(t["permalink"].rstrip("/"), tok, {"limit": MAX_COMMENTS, "sort": "top", "raw_json": 1})
        if j and len(j) > 1:
            t["comments"] = [{"score": c["data"].get("score"), "text": c["data"].get("body", "")[:1500]}
                             for c in j[1]["data"]["children"] if c["kind"] == "t1"][:MAX_COMMENTS]
        if i % 20 == 0: print(f"comments: {i}/{len(todo)}")

    for t in threads.values(): t.pop("permalink", None)
    json.dump({"collected": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "subs": SUBS, "queries": QUERIES,
               "count": len(threads), "threads": sorted(threads.values(), key=lambda x: x["date"], reverse=True)},
              open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"Done: {len(threads)} threads saved to {OUT}")


if __name__ == "__main__":
    main()
