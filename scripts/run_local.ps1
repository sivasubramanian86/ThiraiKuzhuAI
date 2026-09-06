# PowerShell script to run Thirai Kuzhu AI locally
$ErrorActionPreference = "Stop"

Write-Host "🎬 Starting Thirai Kuzhu AI Local Development Environment..." -ForegroundColor Cyan

# 1. Build frontend assets
Write-Host "📦 Building Frontend Console..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\..\frontend"
npm run build

# 2. Launch FastAPI with static frontend mount
Write-Host "🚀 Launching FastAPI Backend on http://localhost:8080..." -ForegroundColor Green
Set-Location -Path "$PSScriptRoot\..\backend"
python -m uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
