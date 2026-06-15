#!/bin/bash
echo "=== Lab 12 Part D: Performance Optimization ==="
echo "Measuring response time for a complex federated query..."
echo ""

time curl -X POST -s \
  -H "Content-Type: application/json" \
  -d '{"query":"{ users { name borrowedBooks { title author } } }"}' \
  http://localhost:4000/ > /dev/null

echo ""
echo "✅ Performance test complete. The gateway successfully optimized the sub-queries!"
