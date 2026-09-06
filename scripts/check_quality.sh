#!/usr/bin/env bash
# Execute all local quality gates: Ruff, Bandit, Pytest 100% coverage, and Frontend build
set -e

echo "🛡️ Running Thirai Kuzhu AI Quality & Security Gates..."

echo "1. Ruff Linter..."
cd backend
python -m ruff check src tests
python -m ruff format --check src tests

echo "2. Bandit Security Audit..."
python -m bandit -r src/ -c pyproject.toml

echo "3. Pytest with 100% Statement Coverage Gate..."
python -m pytest tests -v --cov=src --cov-fail-under=100

echo "4. Frontend Build Check..."
cd ../frontend
npm run build

echo "✅ All Quality & Security Gates Passed Successfully!"
