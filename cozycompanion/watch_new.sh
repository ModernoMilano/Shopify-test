#!/bin/bash
# Poll CozyCompanion every 5 minutes and print one line per newly imported product (no cc-ready tag).
cd "$(dirname "$0")"
SEEN=/tmp/claude-0/-home-user-Shopify-test/7ae2a11e-4ae5-5a99-ac75-b7957d6a039d/scratchpad/seen_products.txt
touch "$SEEN"
while true; do
  curl -sf --retry 3 -X POST "https://$COZY_SHOPIFY_DOMAIN/admin/oauth/access_token" \
    -H "Content-Type: application/x-www-form-urlencoded" -o tok.new \
    -d "grant_type=client_credentials&client_id=$COZY_SHOPIFY_CLIENT_ID&client_secret=$COZY_SHOPIFY_CLIENT_SECRET" && mv tok.new tok.json
  python3 -I -c "
import sys; sys.path.insert(0,'.')
from lib import gql
seen=set(open('$SEEN').read().split())
for p in gql('{products(first:100, query:\"-status:archived -tag:cc-ready\"){nodes{id title status}}}')['products']['nodes']:
    if p['id'] not in seen:
        print('NEW PRODUCT:', p['status'], p['title'], p['id'], flush=True)
        open('$SEEN','a').write(p['id']+'\n')
" 2>&1 | grep --line-buffered -E "NEW PRODUCT|Error|error" || true
  sleep 300
done
