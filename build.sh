#!/usr/bin/env bash
# Builds dist/manictime-tracker-<version>.xpi from the add-on files.
set -euo pipefail
cd "$(dirname "$0")"

version=$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' manifest.json | head -n1)
[ -n "$version" ] || { echo "Version not found in manifest.json" >&2; exit 1; }

out="dist/manictime-tracker-${version}.xpi"
mkdir -p dist
rm -f "$out"
zip -r -X "$out" manifest.json background.js options.html options.css options.js manictime.png _locales
echo "Created $out"
