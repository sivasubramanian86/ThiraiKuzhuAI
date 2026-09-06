#!/usr/bin/env bash
# Enable Billable GCP Cloud Services & Restore Cloud Run Service (Pre-Submission Activation)
# Run this script on the final day of hackathon submission or live judging.
set -e

PROJECT_ID=${1:-$(gcloud config get-value project 2>/dev/null || echo "genai-apac-2026-491004")}
REGION=${2:-"us-central1"}
SERVICE_NAME="thirai-kuzhu-ai"

echo "⚡ [ACTIVATION] Enabling services and unfreezing Cloud Run for project: ${PROJECT_ID}"

# 1. Enable required APIs
echo "  🔓 Enabling Cloud Run, Vertex AI, Translation, TTS, and Secret Manager APIs..."
SERVICES_TO_ENABLE=(
    "run.googleapis.com"
    "aiplatform.googleapis.com"
    "secretmanager.googleapis.com"
    "translate.googleapis.com"
    "texttospeech.googleapis.com"
)

for svc in "${SERVICES_TO_ENABLE[@]}"; do
    echo "    + Enabling ${svc}..."
    gcloud services enable "${svc}" --project="${PROJECT_ID}" --quiet
done

# 2. Restore Cloud Run service capacity (min-instances=0 scale-to-zero, max-instances=3)
if gcloud run services describe "${SERVICE_NAME}" --project="${PROJECT_ID}" --region="${REGION}" >/dev/null 2>&1; then
    echo "  🚀 Restoring Cloud Run capacity for '${SERVICE_NAME}' (scale-to-zero active)..."
    gcloud run services update "${SERVICE_NAME}" \
        --project="${PROJECT_ID}" \
        --region="${REGION}" \
        --ingress=all \
        --min-instances=0 \
        --max-instances=3 \
        --quiet
    SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --project="${PROJECT_ID}" --region="${REGION}" --format="value(status.url)")
    echo "  ✓ Cloud Run service live at: ${SERVICE_URL}"
else
    echo "  ℹ️ Cloud Run service not deployed yet. Run: ./scripts/deploy_cloudrun.sh"
fi

echo ""
echo "🎉 [SYSTEM READY] Thirai Kuzhu AI is activated for live hackathon evaluation!"
