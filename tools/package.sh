#!/usr/bin/env bash
# Build release files into dist/:
#   wp-plugin-research.skill  (Claude: folder at top)
#   wp-plugin-research.zip    (ChatGPT / Gemini: SKILL.md at top)
set -eu
cd "$(dirname "$0")/.."
rm -rf dist && mkdir dist
(cd skills && zip -qr ../dist/wp-plugin-research.skill wp-plugin-research -x "*/__pycache__/*")
(cd skills/wp-plugin-research && zip -qr ../../dist/wp-plugin-research.zip . -x "*/__pycache__/*")
echo "Built: dist/wp-plugin-research.skill and dist/wp-plugin-research.zip"
