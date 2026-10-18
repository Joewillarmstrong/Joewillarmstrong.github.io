#!/bin/sh
# Local preview at http://localhost:8000 (validates first).
cd "$(dirname "$0")/.." && python3 scripts/validate.py && python3 -m http.server 8000
