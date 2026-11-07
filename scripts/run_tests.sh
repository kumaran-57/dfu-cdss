#!/usr/bin/env bash
set -e

echo "=== Running DFU-XAI Verification Tests ==="

export ENVIRONMENT=testing
export DATABASE_URL="sqlite:///:memory:"
export SECRET_KEY="test-secret-key-for-automated-verification-only"

pytest backend/tests ml/tests -v --durations=10

echo "=== All Tests Passed Successfully ==="
