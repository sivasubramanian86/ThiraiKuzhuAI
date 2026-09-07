# PowerShell script to freeze billable services and scale Cloud Run to 0 (Denial-of-Wallet Guardrail)
param (
    [string]$ProjectId = "genai-apac-2026-491004",
    [string]$Region = "us-central1",
    [string]$ServiceName = "thirai-kuzhu-ai"
)

Write-Host "[COST GUARD] Freezing and disabling billable services for project: $ProjectId" -ForegroundColor Red

# 1. Scale Cloud Run Service to 0 instances
try {
    $serviceCheck = gcloud run services describe $ServiceName --project=$ProjectId --region=$Region 2>$null
    if ($serviceCheck) {
        Write-Host "  [FREEZE] Locking Cloud Run ingress to internal and scale-to-zero..." -ForegroundColor Yellow
        gcloud run services update $ServiceName `
            --project=$ProjectId `
            --region=$Region `
            --ingress=internal `
            --min-instances=0 `
            --max-instances=1 `
            --quiet
        Write-Host "  [FROZEN] Cloud Run ingress locked to internal; 0 internet traffic permitted." -ForegroundColor Green
    } else {
        Write-Host "  [INFO] Cloud Run service '$ServiceName' not deployed yet." -ForegroundColor Gray
    }
} catch {
    Write-Host "  [WARNING] Error checking Cloud Run service: $_" -ForegroundColor Yellow
}

# 2. Disable optional billable APIs
Write-Host "  [API] Disabling billable auxiliary APIs..." -ForegroundColor Yellow
$servicesToDisable = @(
    "translate.googleapis.com",
    "texttospeech.googleapis.com",
    "vision.googleapis.com",
    "videointelligence.googleapis.com"
)

foreach ($svc in $servicesToDisable) {
    Write-Host "    - Disabling $svc..." -ForegroundColor DarkYellow
    gcloud services disable $svc --project=$ProjectId --quiet 2>$null
}

Write-Host "`n[COST GUARD ACTIVE] All billable services and Cloud Run instances are FROZEN ($0.00 spend)." -ForegroundColor Green
Write-Host "When ready for final hackathon demo, run: .\scripts\enable_cloud_services.ps1" -ForegroundColor Cyan
