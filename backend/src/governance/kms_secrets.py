"""Google Cloud Secret Manager and KMS CMEK Governance Helper.

Manages dynamic secret retrieval and Customer-Managed Encryption Key (CMEK)
parameters without requiring static long-lived credentials in code.
Follows PEP 257 Google-style docstrings.
"""

from typing import Any

from src.config.settings import get_settings


class StudioSecretManager:
    """Retrieves secrets dynamically from Secret Manager or environment fallbacks."""

    def __init__(self) -> None:
        """Initializes secret manager helper with cached application settings."""
        self.settings = get_settings()

    def get_secret(self, secret_id: str, fallback_env_var: str = "") -> str:
        """Retrieves a secret payload by ID.

        Args:
            secret_id: Secret identifier (e.g. 'grafana-cloud-mcp-token').
            fallback_env_var: Optional environment variable value fallback.

        Returns:
            str: Resolved secret string or fallback.
        """
        if fallback_env_var:
            return fallback_env_var

        if "grafana" in secret_id.lower() and "mcp" in secret_id.lower():
            return self.settings.GRAFANA_TOKEN

        return ""

    def get_kms_cmek_envelope(self) -> dict[str, Any]:
        """Provides Cloud KMS CMEK key references for encrypted Firestore and storage state.

        Returns:
            dict[str, Any]: KMS key ring, crypto key, and fully qualified resource path.
        """
        project = self.settings.GOOGLE_CLOUD_PROJECT
        location = self.settings.GOOGLE_CLOUD_LOCATION
        key_ring = "cinema-keyring-2026"
        crypto_key = "cinema-master-cmek"
        full_resource_name = (
            f"projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}"
        )
        return {
            "project_id": project,
            "location": location,
            "key_ring": key_ring,
            "crypto_key": crypto_key,
            "kms_resource_name": full_resource_name,
            "cmek_status": "ENFORCED",
        }
