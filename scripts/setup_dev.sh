#!/usr/bin/env bash
set -e

echo "=== Initializing DFU-XAI Development Environment ==="

# Check environment
python3 scripts/check_environment.py

# Ensure uploads and synthetic directory exist
mkdir -p data/uploads data/sample_synthetic ml/weights

# Copy .env if not exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

echo "Development environment initialized successfully."
