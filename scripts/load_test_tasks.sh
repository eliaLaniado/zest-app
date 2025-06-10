#!/bin/bash

NUM_REQUESTS=100
API_URL="http://localhost:8000/api/tasks"
MESSAGE="Hello from load test"

for i in $(seq 1 $NUM_REQUESTS); do
  curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"$MESSAGE #$i\"}" &
done

wait
echo "Sent $NUM_REQUESTS requests to $API_URL"