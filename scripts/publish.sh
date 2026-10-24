#!/usr/bin/env bash
# Valideert data, bouwt feed.xml en pusht naar main als er wijzigingen zijn.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_feed.py
git add -A data feed.xml SCHEMA.md README.md rapporten scripts
if git diff --cached --quiet; then
  echo "Geen wijzigingen; niets te publiceren."
  exit 0
fi
git commit -m "Radar-update $(TZ=Europe/Amsterdam date +%Y-%m-%d)"
git push origin main
echo "Gepubliceerd."
