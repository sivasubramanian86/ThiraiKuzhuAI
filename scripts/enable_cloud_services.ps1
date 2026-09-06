# PowerShell script to enable GCP services and restore Cloud Run capacity
param (
    [string]$ProjectId = "genai-apac-2026-491004",
    [string]$Region = "us-central1",
    [string]$ServiceName = "thirai-kuzhu-ai"
)

Write-Host "[ACTIVATION] Enabling services and unfreezing Cloud Run for project: $ProjectId" -ForegroundColor Cyan

# 1. Enable required APIs
Write-Host "  [API] Enabling Cloud Run, Vertex AI, Translation, TTS, and Secret Manager APIs..." -ForegroundColor Yellow
$servicesToEnable = @(
    "run.googleapis.com",
    "aiplatform.googleapis.com",
    "secretmanager.googleapis.com",
    "translate.googleapis.com",
    "texttospeech.googleapis.com"
)

foreach ($svc in $servicesToEnable) {
    Write-Host "    + Enabling $svc..." -ForegroundColor Green
    gcloud services enable $svc --project=$ProjectId --quiet 2>$null
}

# 2. Restore Cloud Run service capacity
try {
    $serviceCheck = gcloud run services describe $ServiceName --project=$ProjectId --region=$Region 2>$null
    if ($serviceCheck) {
        Write-Host "  [DEPLOY] Restoring Cloud Run capacity for '$ServiceName' (scale-to-zero active)..." -ForegroundColor Green
        gcloud run services update $ServiceName `
            --project=$ProjectId `
            --region=$Region `
            --min-instances=0 `
            --max-instances=3 `
            --quiet
        $serviceUrl = gcloud run services describe $ServiceName --project=$ProjectId --region=$Region --format="value(status.url)"
        Write-Host "  [READY] Cloud Run service live at: $serviceUrl" -ForegroundColor Cyan
    } else {
        Write-Host "  [INFO] Cloud Run service not deployed yet. Run: .\scripts\deploy_cloudrun.ps1" -ForegroundColor Gray
    }
} catch {
    Write-Host "  [WARNING] Error checking Cloud Run service: $_" -ForegroundColor Yellow
}

Write-Host "`n[SYSTEM READY] Thirai Kuzhu AI is activated for live hackathon evaluation!" -ForegroundColor Green
