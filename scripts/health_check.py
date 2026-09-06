#!/usr/bin/env python3
"""Local and remote health-check utility for Thirai Kuzhu AI.

Pings the FastAPI backend service and validates telemetry and indices readiness.
Follows PEP 257 Google-style docstrings.
"""

import json
import sys
import urllib.error
import urllib.request

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def check_health(base_url: str = "http://localhost:8080") -> bool:
    """Verifies that the backend liveness probe and indices endpoints are responding.

    Args:
        base_url: Base HTTP address of the Thirai Kuzhu AI service.

    Returns:
        bool: True if healthy, False if probe failed.
    """
    endpoints = [
        "/api/health",
        "/api/projects",
        "/api/personas",
        "/api/evaluation/indices",
    ]

    print(f"🎬 Performing health probe on Thirai Kuzhu AI at {base_url}...")

    all_passed = True
    for ep in endpoints:
        target = f"{base_url}{ep}"
        try:
            req = urllib.request.Request(target, headers={"User-Agent": "ThiraiKuzhuHealthCheck/1.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                status_code = response.getcode()
                data = json.loads(response.read().decode("utf-8"))
                if status_code == 200:
                    print(f"  ✅ [200 OK] {ep}")
                else:
                    print(f"  ❌ [{status_code}] {ep}")
                    all_passed = False
        except Exception as err:
            print(f"  ❌ [FAILED] {ep}: {err}")
            all_passed = False

    if all_passed:
        print("🚀 All Thirai Kuzhu AI subsystems healthy and operational.")
    else:
        print("⚠️ One or more subsystem health probes failed.")
    return all_passed


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    success = check_health(url)
    sys.exit(0 if success else 1)
