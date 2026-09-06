#!/usr/bin/env bash
# Run Thirai Kuzhu AI locally (FastAPI + Vite Console)
set -e

echo "🎬 Starting Thirai Kuzhu AI Local Development Environment..."

# 1. Build frontend assets
echo "📦 Building Frontend Console..."
cd frontend
npm run build
cd ..

# 2. Launch FastAPI with static frontend mount
echo "🚀 Launching FastAPI Backend on http://localhost:8080..."
cd backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
