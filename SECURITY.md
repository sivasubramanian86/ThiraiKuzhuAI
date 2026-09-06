# Security Policy

## Supported Versions

Only the latest active release branch of **Thirai Kuzhu AI (திரை குழு AI)** receives security updates and vulnerability patches.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

---

## Security Architecture & Posture

Thirai Kuzhu AI enforces an APAC 2026 Enterprise Studio Hardening standard:
1. **Zero Static Credentials**: All Vertex AI Gemini models execute under the **Gemini Enterprise Agent Platform** with Application Default Credentials (ADC) and Workload Identity Federation (WIF).
2. **Secret Manager Encryption**: Grafana Cloud Service Account tokens are fetched dynamically via Google Cloud Secret Manager with Customer-Managed Encryption Keys (CMEK) via Cloud KMS.
3. **Telemetry Sanitization**: All Grafana Loki logs and Prometheus metrics pass through the `sanitize_telemetry_for_prompt` pipeline to neutralize prompt injection, credential leaks, and actor PII exposure.
4. **Denial-of-Wallet Defense**: Hard-capped circuit breakers limit investigations to 8 MCP tool invocations and 16,000 tokens per incident.
5. **Continuous Code Scanning**: Bandit AST security auditing and Gitleaks secrets scanning run on every GitHub pull request.

---

## Reporting a Vulnerability

If you discover a security vulnerability within Thirai Kuzhu AI, please **do not open a public GitHub issue**.

Instead, follow this responsible disclosure process:
1. Email your findings directly to the maintainers at `security@thiraikuzhu.ai`.
2. Include the following details:
   - Type of issue (e.g., prompt injection, credential exposure, SSRF, IAM privilege escalation).
   - Component affected (`backend/src/governance/`, `infra/terraform/`, or `src/tools/`).
   - Detailed proof-of-concept (PoC) or reproduction steps.
   - Potential impact on studio confidentiality and IP sovereignty.
3. You will receive an initial response within **24 hours**.
4. If accepted, a coordinated security advisory and patch will be released within **7 business days**.
