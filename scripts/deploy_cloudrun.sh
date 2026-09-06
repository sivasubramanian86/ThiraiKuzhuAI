#!/usr/bin/env bash
# Deploy Thirai Kuzhu AI to Google Cloud Run with Gemini Enterprise Agent Platform
set -e

PROJECT_ID=${1:-$(gcloud config get-value project 2>/dev/null || echo "genai-apac-2026-491004")}
REGION=${2:-"us-central1"}
SERVICE_NAME="thirai-kuzhu-ai"
IMAGE_TAG="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"

echo "🎬 Deploying Thirai Kuzhu AI to Google Cloud Run (Cost Guard: SCALE-TO-ZERO)..."
echo "  Project ID:     ${PROJECT_ID}"
echo "  Region:         ${REGION}"
echo "  Service Name:   ${SERVICE_NAME}"
echo "  Container Tag:  ${IMAGE_TAG}"

# 1. Build frontend distribution bundle
echo "📦 Building Frontend Console..."
cd frontend
npm run build
cd ..

# 2. Build Container Image via Cloud Build
echo "☁️ Submitting Container Build to Cloud Build..."
gcloud builds submit --project="${PROJECT_ID}" --tag="${IMAGE_TAG}" backend/

# 3. Deploy to Cloud Run with scale-to-zero ($0 idle cost)
echo "🚀 Deploying to Cloud Run with scale-to-zero protection..."
gcloud run deploy "${SERVICE_NAME}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --image="${IMAGE_TAG}" \
  --platform=managed \
  --allow-unauthenticated \
  --service-account="thirai-kuzhu-orchestrator-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --set-env-vars="ENV=production,GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=${REGION},PRIMARY_MODEL=gemini-3.8-flash-001,DIRECTOR_MODEL=gemini-3.8-pro-001" \
  --set-secrets="GRAFANA_TOKEN=projects/${PROJECT_ID}/secrets/grafana-cloud-mcp-token:latest" \
  --memory=1Gi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=3

echo "✅ Deployment completed successfully with zero idle billing!"
