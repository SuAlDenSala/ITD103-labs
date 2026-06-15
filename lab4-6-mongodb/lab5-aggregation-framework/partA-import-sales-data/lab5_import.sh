#!/bin/bash

echo "=== Lab 5 Part A: Importing Sales Data ==="
echo "Importing sales dataset for Aggregation framework..."

mongoimport --db itd103_advanced --collection sales --drop --file ../../../datasets/sales.json

echo ""
echo "Sales dataset imported successfully!"
