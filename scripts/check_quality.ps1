# PowerShell script for quality and security checks
$ErrorActionPreference = "Stop"

Write-Host "🛡️ Running Thirai Kuzhu AI Quality & Security Gates..." -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot\..\backend"

Write-Host "1. Ruff Linter..." -ForegroundColor Yellow
python -m ruff check src tests
python -m ruff format --check src tests

Write-Host "2. Bandit Security Audit..." -ForegroundColor Yellow
python -m bandit -r src/ -c pyproject.toml

Write-Host "3. Pytest with 100% Statement Coverage Gate..." -ForegroundColor Yellow
python -m pytest tests -v --cov=src --cov-fail-under=100

Write-Host "4. Frontend Build Check..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\..\frontend"
npm run build

Write-Host "✅ All Quality & Security Gates Passed Successfully!" -ForegroundColor Green
