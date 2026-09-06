# Terraform IAM Configurations for Thirai Kuzhu AI (Enterprise Studio Hardening)
# Enforces APAC 2026 Zero-Trust Least-Privilege Architecture for Google Cloud Platform

terraform {
  required_version = ">= 1.8.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30"
    }
  }
}

variable "project_id" {
  type        = string
  description = "Google Cloud Project ID for Thirai Kuzhu AI"
  default     = "genai-blockbuster-2026"
}

# 1. Orchestrator Master Director Service Account
resource "google_service_account" "orchestrator_sa" {
  account_id   = "thirai-kuzhu-orchestrator-sa"
  display_name = "Thirai Kuzhu AI Orchestrator Service Account"
  description  = "Executes multi-agent synthesis, Vertex AI reasoning, and Cloud Run dispatch"
  project      = var.project_id
}

resource "google_project_iam_member" "orchestrator_aiplatform" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.orchestrator_sa.email}"
}

resource "google_project_iam_member" "orchestrator_secrets" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.orchestrator_sa.email}"
}

resource "google_project_iam_member" "orchestrator_run" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.orchestrator_sa.email}"
}

# 2. VFXOps Dedicated Department Service Account
resource "google_service_account" "vfx_sa" {
  account_id   = "thirai-kuzhu-dept-vfx-sa"
  display_name = "Thirai Kuzhu AI VFXOps Service Account"
  description  = "Monitors distributed GPU render farm metrics and CUDA error logs"
  project      = var.project_id
}

resource "google_project_iam_member" "vfx_aiplatform" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.vfx_sa.email}"
}

resource "google_project_iam_member" "vfx_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.vfx_sa.email}"
}

# 3. OTTOps Dedicated Department Service Account
resource "google_service_account" "ott_sa" {
  account_id   = "thirai-kuzhu-dept-ott-sa"
  display_name = "Thirai Kuzhu AI OTTOps Service Account"
  description  = "Performs CDN edge telemetry analysis and streaming health metrics ingestion"
  project      = var.project_id
}

resource "google_project_iam_member" "ott_aiplatform" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.ott_sa.email}"
}

resource "google_project_iam_member" "ott_monitoring" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.ott_sa.email}"
}

# 4. Grafana MCP Adapter Service Account
resource "google_service_account" "grafana_mcp_sa" {
  account_id   = "thirai-kuzhu-grafana-mcp-sa"
  display_name = "Thirai Kuzhu AI Grafana MCP Bridge Service Account"
  description  = "Accesses Grafana Cloud MCP credentials via Secret Manager with strict egress"
  project      = var.project_id
}

resource "google_project_iam_member" "grafana_mcp_secrets" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.grafana_mcp_sa.email}"
}
