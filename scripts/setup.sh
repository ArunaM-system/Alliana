#!/usr/bin/env bash
# ALLINA Development Environment Setup
set -euo pipefail

echo "Setting up ALLINA development environment..."
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

echo "Environment file created. Ensure PostgreSQL and Redis are accessible."
