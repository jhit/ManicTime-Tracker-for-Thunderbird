#!/usr/bin/env bash
# Builds dist/manictime-tracker-<version>.xpi from the add-on files in src/.
set -euo pipefail
cd "$(dirname "$0")"

version=$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' src/manifest.json | head -n1)
[ -n "$version" ] || { echo "Version not found in src/manifest.json" >&2; exit 1; }

python3 doc/readme2html.py

out="$PWD/dist/manictime-tracker-${version}.xpi"
mkdir -p dist
rm -f "$out"
(cd src && zip -r -X "$out" manifest.json background.js options.html options.css options.js manictime-48.png manictime-96.png _locales)
zip -X "$out" LICENSE
echo "Created dist/manictime-tracker-${version}.xpi"
