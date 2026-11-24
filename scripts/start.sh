#!/usr/bin/env bash
# ALLINA Platform Start Script
set -euo pipefail

echo "Starting ALLINA platform services via Docker Compose..."
docker compose up -d
echo "Services started. Backend: http://localhost:8000, Frontend: http://localhost:5173"
