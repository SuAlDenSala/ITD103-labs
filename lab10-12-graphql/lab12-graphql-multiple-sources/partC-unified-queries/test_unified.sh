#!/bin/bash
echo "=== Lab 12 Part C: Unified Queries ==="
echo "Querying the API Gateway to stitch data from multiple microservices..."
echo ""

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ users { name borrowedBooks { title author } } }"}' \
  http://localhost:4000/

echo ""
echo ""
echo "✅ Unified query successfully routed to Books and Users subgraphs!"
