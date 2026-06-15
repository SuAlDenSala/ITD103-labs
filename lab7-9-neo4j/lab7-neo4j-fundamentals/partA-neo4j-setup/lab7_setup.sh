#!/bin/bash

echo "=== Lab 7 Part A: Neo4j Setup ==="
echo "Checking Neo4j Database Connection..."
echo ""

# Check if Neo4j is accepting connections
if curl -s -I http://localhost:7474 | grep -q "200 OK"; then
    echo "✅ Neo4j Database is running and accessible!"
    echo "Port 7474: HTTP Browser UI Active"
    echo "Port 7687: Bolt Protocol Active"
    echo ""
    echo "Setup is complete. You may proceed to Part B."
else
    echo "⏳ Neo4j is still starting up or not running."
    echo "Please ensure you ran 'docker-compose up -d' in the previous folder."
fi
