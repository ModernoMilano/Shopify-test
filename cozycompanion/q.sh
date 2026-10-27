#!/bin/bash
# usage: q.sh '<graphql>' [variables-json]
S="$(cd "$(dirname "$0")" && pwd)"
T=$(python3 -c "import json;print(json.load(open('$S/tok.json'))['access_token'])")
python3 -c "import json,sys;print(json.dumps({'query':sys.argv[1],'variables':json.loads(sys.argv[2] if len(sys.argv)>2 else '{}')}))" "$1" "${2:-{\}}" > $S/.body.json
curl -s -X POST "https://$COZY_SHOPIFY_DOMAIN/admin/api/2026-10/graphql.json" -H "Content-Type: application/json" -H "X-Shopify-Access-Token: $T" --data @$S/.body.json
