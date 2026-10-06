#!/usr/bin/env bash
# Render -> contrast check -> 1:1 crops + previews -> final verification. Stops at the first failure.
set -e
NODE_PATH=${NODE_PATH:-/usr/local/lib/node_modules} node render.js "$@"
python3 contrast.py
python3 post.py $(python3 -c "import json;print(' '.join(str(a['id']) for a in json.load(open('ads.json'))))")
python3 verify.py
