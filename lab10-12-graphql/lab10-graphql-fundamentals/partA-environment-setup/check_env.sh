#!/bin/bash
echo "=== Lab 10 Part A: Environment Setup ==="
echo "Checking Node.js and NPM..."

if command -v node >/dev/null 2>&1; then
    echo "✅ Node.js is installed: $(node -v)"
else
    echo "❌ Node.js is not installed."
    exit 1
fi

if command -v npm >/dev/null 2>&1; then
    echo "✅ NPM is installed: $(npm -v)"
else
    echo "❌ NPM is not installed."
    exit 1
fi

echo "Environment is perfectly set up for GraphQL!"
