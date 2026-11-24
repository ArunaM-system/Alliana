#!/usr/bin/env bash
# ALLINA Database Migration Script
set -euo pipefail

echo "Running Alembic database migrations..."
cd backend
alembic upgrade head
echo "Database migrations applied successfully."
