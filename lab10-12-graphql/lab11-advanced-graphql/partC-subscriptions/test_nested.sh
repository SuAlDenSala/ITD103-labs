#!/bin/bash
echo "=== Lab 11 Part C: Nested Queries ==="
echo "Fetching authors and their nested books array:"
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ authors { name books { title } } }"}' \
  http://localhost:4001/

echo ""
echo ""
echo "✅ Nested queries test complete!"
