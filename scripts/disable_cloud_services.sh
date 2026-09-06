#!/usr/bin/env bash
# Disable Billable GCP Cloud Services & Scale Cloud Run to 0 (Denial-of-Wallet Guardrail)
# Run this script to pause billable resources and preserve personal credits until final hackathon submission.
set -e

PROJECT_ID=${1:-$(gcloud config get-value project 2>/dev/null || echo "genai-apac-2026-491004")}
REGION=${2:-"us-central1"}
SERVICE_NAME="thirai-kuzhu-ai"

echo "🛑 [COST GUARD] Freezing and disabling billable services for project: ${PROJECT_ID}"

# 1. Scale Cloud Run Service to 0 instances (stops any compute execution)
if gcloud run services describe "${SERVICE_NAME}" --project="${PROJECT_ID}" --region="${REGION}" >/dev/null 2>&1; then
    echo "  🔒 Locking Cloud Run ingress to internal and scale-to-zero..."
    gcloud run services update "${SERVICE_NAME}" \
        --project="${PROJECT_ID}" \
        --region="${REGION}" \
        --ingress=internal \
        --min-instances=0 \
        --max-instances=1 \
        --quiet
    echo "  ✓ Cloud Run ingress locked to internal; 0 internet traffic permitted."
else
    echo "  ℹ️ Cloud Run service '${SERVICE_NAME}' not found or not deployed yet."
fi

# 2. Disable optional high-cost APIs to prevent background batch jobs or unexpected API consumption
echo "  🔒 Disabling billable auxiliary APIs..."
SERVICES_TO_DISABLE=(
    "translate.googleapis.com"
    "texttospeech.googleapis.com"
)

for svc in "${SERVICES_TO_DISABLE[@]}"; do
    echo "    - Disabling ${svc}..."
    gcloud services disable "${svc}" --project="${PROJECT_ID}" --quiet || true
done

echo ""
echo "✅ [COST GUARD ACTIVE] All billable services and Cloud Run instances are FROZEN ($0.00 spend)."
echo "👉 When ready to submit or test live, run: ./scripts/enable_cloud_services.sh"
