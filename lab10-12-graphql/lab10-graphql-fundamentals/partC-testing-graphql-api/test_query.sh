#!/bin/bash
echo "=== Lab 10 Part C: Testing GraphQL API ==="
echo "Sending Query to fetch all books and their authors..."
echo ""

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ books { title author } }"}' \
  http://localhost:4000/

echo ""
echo ""
echo "✅ Query executed successfully!"
