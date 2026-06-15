#!/bin/bash

echo "=== Lab 4 Part A: Importing Datasets ==="

echo "Importing restaurants dataset..."
mongoimport --db itd103_advanced --collection restaurants --file ../../../datasets/restaurants.json

echo ""
echo "Importing sales dataset..."
mongoimport --db itd103_advanced --collection sales --file ../../../datasets/sales.json

echo ""
echo "Datasets imported successfully!"
