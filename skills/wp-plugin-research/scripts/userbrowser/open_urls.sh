#!/usr/bin/env bash
# Open a list of URLs in the USER'S browser (rung 4 of the collection ladder).
# Usage: bash open_urls.sh urls.txt [pause_seconds]
#   urls.txt: one URL per line (lines starting with # are skipped).
# macOS opens Google Chrome; Linux uses xdg-open; Windows (Git Bash) uses start.
# Read-only: it only opens pages. Pauses between URLs to stay polite (default 3 s).
set -u
LIST="${1:?usage: open_urls.sh urls.txt [pause_seconds]}"
PAUSE="${2:-3}"
while IFS= read -r url || [ -n "$url" ]; do
  case "$url" in ''|'#'*) continue ;; esac
  case "$(uname -s)" in
    Darwin) open -a "Google Chrome" "$url" ;;
    Linux)  xdg-open "$url" >/dev/null 2>&1 ;;
    MINGW*|MSYS*|CYGWIN*) start "" "$url" ;;
    *) echo "Open manually: $url" ;;
  esac
  echo "opened: $url"
  sleep "$PAUSE"
done < "$LIST"
