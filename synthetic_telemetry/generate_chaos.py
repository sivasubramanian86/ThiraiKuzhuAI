#!/usr/bin/env python3
"""Synthetic Studio Chaos Generator for Thirai Kuzhu AI.

Generates realistic Prometheus metrics, Loki log streams, and Tempo distributed traces
simulating real-world film production and streaming release disasters.
Used by evaluators and hackathon judges to verify multi-agent triage without live film hardware.
"""

import argparse
import json
import random
import time
from typing import Any


def scenario_ott_premiere_spike() -> dict[str, Any]:
    """Generates telemetry for midnight OTT blockbuster premiere CDN 504 overload."""
    return {
        "scenario": "ott_premiere_spike",
        "film_title": "Baahubali III: The Eternal Realm",
        "sequence": "Seq 14 - Royal Coronation Climax",
        "genre": "Epic Historical Warfare",
        "promql_metrics": [
            {
                "metric": "cdn_requests_total{status='504',region='ap-south-1'}",
                "value": round(random.uniform(7.8, 12.4), 2),
                "threshold": "> 5.0%",
                "status": "FIRING",
            },
            {
                "metric": "playback_stall_ratio{cdn_pop='chennai-01'}",
                "value": 0.042,
                "threshold": "> 0.01",
                "status": "FIRING",
            },
        ],
        "loki_logs": [
            "[origin-transcoder-01] Deadlock encountered while transcoding 4K AV1 master stream.",
            "[edge-proxy-chennai] 504 Gateway Timeout fetching segment seq14_4k_0142.m4s from origin.",
            "[drm-license-gateway] Token verification backlog: 14,200 pending consumer requests.",
        ],
        "tempo_trace": {
            "trace_id": "7b8f9e1204cba31d",
            "root_service": "cdn-edge-proxy",
            "total_duration_ms": 2480.0,
            "spans": [
                {"service": "cdn-edge-proxy", "operation": "handle_playback_req", "duration_ms": 12.0},
                {"service": "drm-license-validator", "operation": "validate_key", "duration_ms": 2410.0},
                {"service": "gcs-origin-pool", "operation": "read_manifest", "duration_ms": 58.0},
            ],
        },
        "box_office_at_risk_usd": 38500.00,
    }


def scenario_vfx_crash() -> dict[str, Any]:
    """Generates telemetry for 8K IMAX VFX render cluster CUDA Out of Memory crash."""
    return {
        "scenario": "vfx_crash",
        "film_title": "Avatar: The Deep Trenches",
        "sequence": "Seq 22 - Bioluminescent Trench Chase",
        "genre": "Action & Heavy Stunts",
        "promql_metrics": [
            {
                "metric": "vfx_gpu_memory_used_bytes{node='vfx-node-14'} / vfx_gpu_memory_total_bytes",
                "value": 0.994,
                "threshold": "> 0.95",
                "status": "CRITICAL_OOM",
            }
        ],
        "loki_logs": [
            "[vfx-node-14] CUDA out of memory allocating 34.2GB texture buffer for underwater reef render.",
            "[slurm-master] Job #84910 terminated with SIGSEGV (Out of GPU memory).",
            "[shot-scheduler] Shot 22-04 unrendered: 18 compositing tasks blocked downstream.",
        ],
        "tempo_trace": {
            "trace_id": "vfx-cuda-oom-9921",
            "root_service": "render-scheduler",
            "total_duration_ms": 12400.0,
            "spans": [
                {"service": "asset-fetcher", "operation": "pull_16k_mipmaps", "duration_ms": 4200.0},
                {"service": "cuda-kernel-renderer", "operation": "raytrace_volumetric", "duration_ms": 8200.0},
            ],
        },
        "box_office_at_risk_usd": 15000.00,
    }


def scenario_wuxia_foley_lag() -> dict[str, Any]:
    """Generates telemetry for Martial Arts / Wuxia wirework and combat Foley transient sync lag."""
    return {
        "scenario": "wuxia_foley_lag",
        "film_title": "Shadow of the Crane (鶴影之劍)",
        "sequence": "Seq 07 - Bamboo Forest Swordfight",
        "genre": "Martial Arts & Wuxia",
        "promql_metrics": [
            {
                "metric": "foley_strike_transient_sync_offset_ms{channel='stem-foley-combat'}",
                "value": 14.8,
                "threshold": "< 5.0ms",
                "status": "DESYNC_DETECTED",
            }
        ],
        "loki_logs": [
            "[foley-sync-engine] Transient spike on blade collision detected at frame 840 (offset +14.8ms).",
            "[wire-removal-ai] Alpha matte edge jitter flagged on vertical ascent wire 02.",
        ],
        "tempo_trace": {
            "trace_id": "wuxia-foley-trace-01",
            "root_service": "foley-sync-engine",
            "total_duration_ms": 18.2,
            "spans": [
                {"service": "video-frame-clock", "operation": "24fps_timecode_sync", "duration_ms": 3.4},
                {"service": "stem-foley-combat", "operation": "transient_alignment", "duration_ms": 14.8},
            ],
        },
        "box_office_at_risk_usd": 8500.00,
    }


def scenario_anime_sakuga_stall() -> dict[str, Any]:
    """Generates telemetry for Anime / Sakuga stepped framerate render buffer stalls."""
    return {
        "scenario": "anime_sakuga_stall",
        "film_title": "Neo-Tokyo Valkyrie: Infinite Resonance",
        "sequence": "Seq 09 - Mecha Aerial Re-entry Sakuga",
        "genre": "Animation & Anime Sakuga",
        "promql_metrics": [
            {
                "metric": "sakuga_frame_stepped_rate_deviation{render_tier='h265-60fps'}",
                "value": -4.2,
                "threshold": "== 0.0",
                "status": "STEP_MISMATCH",
            }
        ],
        "loki_logs": [
            "[sakuga-render-worker] Stepped cadence mismatch: Expected animated on 1s; received 2s keyframe.",
            "[clip-studio-pipe] Dropped 6 drawing interpolation sub-frames in re-entry trail burst.",
        ],
        "tempo_trace": {
            "trace_id": "anime-sakuga-trace-77",
            "root_service": "sakuga-compositor",
            "total_duration_ms": 340.0,
            "spans": [
                {"service": "cel-shader", "operation": "vector_line_cleanup", "duration_ms": 120.0},
                {"service": "h265-encoder", "operation": "frame_rate_conform", "duration_ms": 220.0},
            ],
        },
        "box_office_at_risk_usd": 12000.00,
    }


def main() -> None:
    """CLI entrypoint for generating synthetic chaos scenarios."""
    parser = argparse.ArgumentParser(
        description="Thirai Kuzhu AI — Synthetic Studio Chaos Telemetry Generator"
    )
    parser.add_argument(
        "--scenario",
        type=str,
        choices=["ott_premiere_spike", "vfx_crash", "wuxia_foley_lag", "anime_sakuga_stall"],
        default="ott_premiere_spike",
        help="Cinema incident scenario to generate",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Optional path to output generated telemetry JSON",
    )
    args = parser.parse_args()

    scenarios = {
        "ott_premiere_spike": scenario_ott_premiere_spike,
        "vfx_crash": scenario_vfx_crash,
        "wuxia_foley_lag": scenario_wuxia_foley_lag,
        "anime_sakuga_stall": scenario_anime_sakuga_stall,
    }

    print(f"\n[Thirai Kuzhu AI] Injecting Studio Chaos: '{args.scenario}'...")
    time.sleep(0.3)
    data = scenarios[args.scenario]()

    formatted = json.dumps(data, indent=2)
    print(formatted)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(formatted)
        print(f"\n[INFO] Telemetry written to {args.output}")

    print("\n[SUCCESS] Synthetic chaos scenario generated successfully!")


if __name__ == "__main__":
    main()
