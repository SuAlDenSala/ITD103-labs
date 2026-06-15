#!/bin/bash
echo "=== Lab 11 Part B: Authentication ==="
echo "1. Attempting to fetch secret data WITHOUT a token (Should Fail):"
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ secretData }"}' \
  http://localhost:4001/

echo ""
echo ""
echo "2. Attempting to fetch secret data WITH a valid token (Should Succeed):"
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer my-secret-token" \
  -d '{"query":"{ secretData }"}' \
  http://localhost:4001/

echo ""
echo ""
echo "✅ Authentication test complete!"
