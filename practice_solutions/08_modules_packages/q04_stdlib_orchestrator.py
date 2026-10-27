"""
Topic 08 - Modules and Packages: Question 4
Problem: Telemetry Bundle Orchestrator coordinating math, random, os, sys, shutil, and json.
"""

import json
import math
import os
import random
import shutil
import sys
from typing import Any, Dict, List


class TelemetryBundleOrchestrator:
    """Coordinates core Standard Library modules for synthetic telemetry generation and packaging."""

    def generate_sensor_readings(self, sample_size: int, seed: int = 101) -> List[Dict[str, Any]]:
        """Generates Gaussian sensor readings transformed via sigmoid normalization."""
        if sample_size <= 0:
            raise ValueError("Sample size must be strictly positive")

        random.seed(seed)
        sensor_pool = ["TEMP-01", "TEMP-02", "PRESSURE-01", "VIBRATION-01"]
        readings = []

        for _ in range(sample_size):
            sid = random.choice(sensor_pool)
            raw = round(random.gauss(mu=50.0, sigma=12.0), 2)
            # Sigmoid transformation
            norm_score = round(1.0 / (1.0 + math.exp(-raw / 25.0)), 4)
            is_alert = raw > 75.0 or raw < 25.0

            readings.append({
                "sensor_id": sid,
                "raw_reading": raw,
                "normalized_score": norm_score,
                "is_alert": is_alert
            })

        return readings

    def export_dataset(self, records: List[Dict[str, Any]], output_directory: str, filename: str = "telemetry.json") -> str:
        """Serializes records to formatted JSON on disk."""
        os.makedirs(output_directory, exist_ok=True)
        dest_path = os.path.abspath(os.path.join(output_directory, filename))
        with open(dest_path, mode="w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
        return dest_path

    def compress_bundle(self, directory_to_zip: str, archive_base_name: str, format: str = "zip") -> Dict[str, Any]:
        """Creates compressed zip archive of directory tree and measures file size."""
        archive_path = shutil.make_archive(archive_base_name, format, directory_to_zip)
        size_bytes = os.path.getsize(archive_path)
        return {
            "archive_path": archive_path,
            "size_bytes": size_bytes
        }

    def get_runtime_diagnostics(self) -> Dict[str, Any]:
        """Collects runtime Python engine and OS process metadata."""
        return {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": sys.platform,
            "process_id": os.getpid(),
            "working_dir": os.getcwd()
        }


# Verification & Execution
staging_dir = "./telemetry_staging"
archive_base = "./telemetry_backup"

try:
    orchestrator = TelemetryBundleOrchestrator()
    readings = orchestrator.generate_sensor_readings(sample_size=5, seed=42)

    print(f"Generated {len(readings)} sensor readings. Sample item 1:")
    print(json.dumps(readings[0], indent=2))

    filepath = orchestrator.export_dataset(readings, staging_dir, "metrics.json")
    print(f"\nExported file: {filepath.replace(os.sep, '/')}")

    archive_meta = orchestrator.compress_bundle(staging_dir, archive_base, "zip")
    print(f"Archive Created: {archive_meta['archive_path'].replace(os.sep, '/')} (Size: ~{archive_meta['size_bytes']} bytes)")

    env_info = orchestrator.get_runtime_diagnostics()
    print("\nEnvironment Diagnostics:")
    print(f"- Python Version: {env_info['python_version']}")
    print(f"- Platform: {env_info['platform']}")
    print(f"- Process ID: {env_info['process_id']}")

finally:
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir, ignore_errors=True)
    zip_path = f"{archive_base}.zip"
    if os.path.exists(zip_path):
        os.remove(zip_path)
