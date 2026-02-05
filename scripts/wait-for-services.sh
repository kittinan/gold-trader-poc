#!/bin/bash

# Wait for services to be healthy before running E2E tests
# Timeout: 120 seconds

set -e

echo "🔍 Waiting for services to be ready..."

# Timeout in seconds
TIMEOUT=120
START_TIME=$(date +%s)

# Function to check if service is healthy
check_service_health() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Checking $service_name health at $url"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            echo "✅ $service_name is healthy!"
            return 0
        fi
        
        echo "⏳ Waiting for $service_name... (attempt $attempt/$max_attempts)"
        sleep 4
        attempt=$((attempt + 1))
    done
    
    echo "❌ $service_name failed to become healthy within $((max_attempts * 4)) seconds"
    return 1
}

# Check backend health
check_service_health "Backend" "http://localhost:8000/health/"

# Check frontend health
check_service_health "Frontend" "http://localhost:5173/"

# Check if we've exceeded the total timeout
CURRENT_TIME=$(date +%s)
ELAPSED_TIME=$((CURRENT_TIME - START_TIME))

if [ $ELAPSED_TIME -gt $TIMEOUT ]; then
    echo "❌ Total wait time exceeded $TIMEOUT seconds"
    exit 1
fi

echo "🎉 All services are ready! Total wait time: ${ELAPSED_TIME}s"
exit 0