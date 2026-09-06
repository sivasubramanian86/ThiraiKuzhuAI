# PowerShell script to deploy Thirai Kuzhu AI to Google Cloud Run
param (
    [string]$ProjectId = "genai-apac-2026-491004",
    [string]$Region = "us-central1",
    [string]$ServiceName = "thirai-kuzhu-ai"
)

$ErrorActionPreference = "Stop"
$ImageTag = "gcr.io/$ProjectId/${ServiceName}:latest"

Write-Host "[DEPLOY] Deploying Thirai Kuzhu AI to Google Cloud Run (Cost Guard: SCALE-TO-ZERO)..." -ForegroundColor Cyan
Write-Host "  Project ID:     $ProjectId"
Write-Host "  Region:         $Region"
Write-Host "  Service Name:   $ServiceName"
Write-Host "  Container Tag:  $ImageTag"

# 1. Build frontend distribution bundle
Write-Host "[BUILD] Building Frontend Console..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\..\frontend"
npm run build
Set-Location -Path "$PSScriptRoot\.."
if (Test-Path "backend/frontend_dist") { Remove-Item -Path "backend/frontend_dist" -Recurse -Force }
Copy-Item -Path "frontend/dist" -Destination "backend/frontend_dist" -Recurse -Force

# 2. Build Container Image via Cloud Build
Write-Host "[BUILD] Submitting Container Build to Cloud Build..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\.."
gcloud builds submit --project=$ProjectId --tag=$ImageTag backend/

# 3. Deploy to Cloud Run with scale-to-zero ($0 idle cost)
Write-Host "[DEPLOY] Deploying to Cloud Run with scale-to-zero..." -ForegroundColor Green
$saEmail = "thirai-kuzhu-orchestrator-sa@$ProjectId.iam.gserviceaccount.com"
$envVars = "ENV=production,GOOGLE_CLOUD_PROJECT=$ProjectId,GOOGLE_CLOUD_LOCATION=$Region,PRIMARY_MODEL=gemini-3.8-flash-001,DIRECTOR_MODEL=gemini-3.8-pro-001"
$secretVar = "GRAFANA_TOKEN=grafana-cloud-mcp-token:latest"

gcloud run deploy $ServiceName `
  --project=$ProjectId `
  --region=$Region `
  --image=$ImageTag `
  --platform=managed `
  --allow-unauthenticated `
  --service-account=$saEmail `
  --set-env-vars=$envVars `
  --set-secrets=$secretVar `
  --memory=1Gi `
  --cpu=1 `
  --min-instances=0 `
  --max-instances=3

Write-Host "[SUCCESS] Deployment completed successfully with zero idle cost!" -ForegroundColor Green
