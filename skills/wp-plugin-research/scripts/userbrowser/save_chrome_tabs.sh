#!/usr/bin/env bash
# Save the loaded HTML of open Chrome tabs whose URL contains PATTERN (rung 4).
# macOS + Google Chrome only.
#
# Needs TWO one-time permissions, both granted BY THE USER (the agent must ask, never change them):
#   1. Chrome → View → Developer → "Allow JavaScript from Apple Events"
#   2. macOS asks "Terminal wants to control Google Chrome" the first time → click OK
#      (later: System Settings → Privacy & Security → Automation → your terminal → Google Chrome)
# This script checks both BEFORE saving and stops with instructions if one is missing.
#
# No permissions wanted? Use save-page.js instead (paste in the DevTools console on each page),
# or Cmd+S → "Webpage, HTML only". The parsers read all three the same way.
#
# Usage: bash save_chrome_tabs.sh PATTERN OUT_DIR
#   e.g. bash save_chrome_tabs.sh old.reddit.com raw/reddit/search
# Writes OUT_DIR/<n>-<sanitised-url>.html for each matching tab. Read-only.
set -u
PATTERN="${1:?usage: save_chrome_tabs.sh PATTERN OUT_DIR}"
OUT="${2:?usage: save_chrome_tabs.sh PATTERN OUT_DIR}"
[ "$(uname -s)" = "Darwin" ] || { echo "macOS only. Use save-page.js in the console, or Ctrl+S → 'Webpage, HTML only'."; exit 1; }
mkdir -p "$OUT"

# --- Pre-flight: can we control Chrome, and is JavaScript from Apple Events on? ---
probe=$(osascript -e 'tell application "Google Chrome"
  if (count of windows) = 0 then return "NO_WINDOWS"
  return execute active tab of front window javascript "1+1"
end tell' 2>&1)
case "$probe" in
  2|2.0) ;;  # all good
  NO_WINDOWS) echo "Chrome has no open windows. Open the pages first (open_urls.sh), then re-run."; exit 1 ;;
  *"turned off"*|*"Apple Events"*|*"JavaScript"*)
    cat << 'MSG'
Chrome is blocking scripts from Apple Events (a Chrome security setting).
To allow it — you do this, once:
  Chrome menu bar → View → Developer → "Allow JavaScript from Apple Events" (tick it)
Then re-run this command. You can untick it again when you're done.
No-permission alternative: paste scripts/userbrowser/save-page.js into the DevTools console on each page.
MSG
    exit 2 ;;
  *"Not authorized"*|*"-1743"*|*"not allowed"*)
    cat << 'MSG'
macOS hasn't allowed this terminal to control Google Chrome.
To allow it — you do this, once:
  System Settings → Privacy & Security → Automation → [your terminal app] → turn on "Google Chrome"
Then re-run this command.
MSG
    exit 3 ;;
  *) echo "Could not talk to Chrome: $probe"; exit 4 ;;
esac

# --- Save every matching tab ---
n=0
for w in $(osascript -e 'tell application "Google Chrome" to get id of every window' | tr ',' ' '); do
  tabs=$(osascript -e "tell application \"Google Chrome\" to count tabs of window id $w")
  for ((t=1; t<=tabs; t++)); do
    url=$(osascript -e "tell application \"Google Chrome\" to get URL of tab $t of window id $w")
    case "$url" in *"$PATTERN"*) ;; *) continue ;; esac
    n=$((n+1))
    safe=$(printf '%s' "$url" | sed -E 's#^https?://##; s#[^A-Za-z0-9._-]+#_#g' | cut -c1-120)
    file="$OUT/$(printf '%03d' "$n")-$safe.html"
    if ! osascript -e "tell application \"Google Chrome\" to execute tab $t of window id $w javascript \"document.documentElement.outerHTML\"" > "$file" 2>/dev/null; then
      echo "Could not read tab: $url"; rm -f "$file"; continue
    fi
    echo "saved: $file"
  done
done
if [ "$n" -eq 0 ]; then echo "No open Chrome tabs match '$PATTERN'."; exit 1; fi
echo "Done: $n tab(s) matched '$PATTERN'."
