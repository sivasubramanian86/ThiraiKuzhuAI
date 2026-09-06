# PowerShell script to deploy Thirai Kuzhu AI to Google Cloud Run
param (
    [string]$ProjectId = $(gcloud config get-value project 2>$null; if (-not $?) { "genai-apac-2026-491004" }),
    [string]$Region = "us-central1",
    [string]$ServiceName = "thirai-kuzhu-ai"
)

$ErrorActionPreference = "Stop"
$ImageTag = "gcr.io/$ProjectId/${ServiceName}:latest"

Write-Host "🎬 Deploying Thirai Kuzhu AI to Google Cloud Run (Cost Guard: SCALE-TO-ZERO)..." -ForegroundColor Cyan
Write-Host "  Project ID:     $ProjectId"
Write-Host "  Region:         $Region"
Write-Host "  Service Name:   $ServiceName"
Write-Host "  Container Tag:  $ImageTag"

# 1. Build frontend distribution bundle
Write-Host "📦 Building Frontend Console..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\..\frontend"
npm run build

# 2. Build Container Image via Cloud Build
Write-Host "☁️ Submitting Container Build to Cloud Build..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\.."
gcloud builds submit --project="$ProjectId" --tag="$ImageTag" backend/

# 3. Deploy to Cloud Run with scale-to-zero ($0 idle cost)
Write-Host "🚀 Deploying to Cloud Run with scale-to-zero..." -ForegroundColor Green
gcloud run deploy "$ServiceName" `
  --project="$ProjectId" `
  --region="$Region" `
  --image="$ImageTag" `
  --platform=managed `
  --allow-unauthenticated `
  --service-account="thirai-kuzhu-orchestrator-sa@${ProjectId}.iam.gserviceaccount.com" `
  --set-env-vars="ENV=production,GOOGLE_CLOUD_PROJECT=$ProjectId,GOOGLE_CLOUD_LOCATION=$Region,PRIMARY_MODEL=gemini-3.8-flash-001,DIRECTOR_MODEL=gemini-3.8-pro-001" `
  --set-secrets="GRAFANA_TOKEN=projects/${ProjectId}/secrets/grafana-cloud-mcp-token:latest" `
  --memory=1Gi `
  --cpu=1 `
  --min-instances=0 `
  --max-instances=3

Write-Host "✅ Deployment completed successfully with zero idle cost!" -ForegroundColor Green
