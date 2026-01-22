#!/bin/bash

# Test script for PDF Redaction Service
# This script tests the service endpoints

echo "Testing PDF Redaction Service"
echo "=============================="
echo ""

BASE_URL="http://localhost:5000"

# Test 1: Health Check
echo "1. Testing Health Check..."
curl -s "${BASE_URL}/health" | python3 -m json.tool
echo ""
echo ""

# Test 2: Get Supported Types
echo "2. Testing Supported Types..."
curl -s "${BASE_URL}/api/supported-types" | python3 -m json.tool
echo ""
echo ""

# Test 3: Preview (requires a PDF file)
if [ -f "sample.pdf" ]; then
    echo "3. Testing Preview Endpoint..."
    curl -s -X POST "${BASE_URL}/api/preview" \
        -F "file=@sample.pdf" \
        -F "redaction_types=[\"email\",\"phone\"]" | python3 -m json.tool
    echo ""
    echo ""

    echo "4. Testing Redact Endpoint..."
    curl -X POST "${BASE_URL}/api/redact" \
        -F "file=@sample.pdf" \
        -F "redaction_types=[\"email\",\"phone\",\"linkedin\"]" \
        -F "output_format=pdf" \
        -o "redacted_output.pdf"

    if [ -f "redacted_output.pdf" ]; then
        echo "✓ Redacted PDF saved as redacted_output.pdf"
        ls -lh redacted_output.pdf
    else
        echo "✗ Failed to create redacted PDF"
    fi
    echo ""
else
    echo "⚠ sample.pdf not found. Skipping preview and redact tests."
    echo "Create a sample.pdf file to test these endpoints."
    echo ""
fi

echo "=============================="
echo "Testing Complete!"
