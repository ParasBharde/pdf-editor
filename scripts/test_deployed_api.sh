#!/bin/bash

# Script to test deployed API
# Usage: ./test_deployed_api.sh https://your-api-url.com

if [ -z "$1" ]; then
    echo "Usage: ./test_deployed_api.sh <API_URL>"
    echo "Example: ./test_deployed_api.sh https://pdf-redaction.onrender.com"
    exit 1
fi

API_URL=$1
echo "Testing API at: $API_URL"
echo "================================"
echo ""

# Remove trailing slash if present
API_URL=${API_URL%/}

# Test 1: Health Check
echo "1. Testing Health Check..."
response=$(curl -s -w "\n%{http_code}" "${API_URL}/health")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | head -n -1)

if [ "$http_code" = "200" ]; then
    echo "✅ Health check passed"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
else
    echo "❌ Health check failed (HTTP $http_code)"
    echo "$body"
fi
echo ""

# Test 2: Get Supported Types
echo "2. Testing Supported Types..."
response=$(curl -s -w "\n%{http_code}" "${API_URL}/api/supported-types")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | head -n -1)

if [ "$http_code" = "200" ]; then
    echo "✅ Supported types endpoint working"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
else
    echo "❌ Supported types failed (HTTP $http_code)"
    echo "$body"
fi
echo ""

# Test 3: Test with sample PDF (if available)
if [ -f "sample.pdf" ]; then
    echo "3. Testing Preview Endpoint with sample.pdf..."
    response=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}/api/preview" \
        -F "file=@sample.pdf" \
        -F "redaction_types=[\"email\",\"phone\"]")
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        echo "✅ Preview endpoint working"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        echo "❌ Preview failed (HTTP $http_code)"
        echo "$body"
    fi
    echo ""
else
    echo "3. ⚠️  Skipping preview test (sample.pdf not found)"
    echo "   Create a sample.pdf to test the preview endpoint"
    echo ""
fi

echo "================================"
echo "API Testing Complete!"
echo ""
echo "Your API is ready to use at: $API_URL"
echo ""
echo "Example usage:"
echo "curl -X POST ${API_URL}/api/redact \\"
echo "  -F \"file=@resume.pdf\" \\"
echo "  -F \"redaction_types=[\\\"email\\\",\\\"phone\\\"]\" \\"
echo "  -o redacted.pdf"
