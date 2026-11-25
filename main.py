"""Unified CLI entry point for running Sentinel AI backend, dashboard, or camera diagnostics."""

import argparse
import subprocess
import sys

import uvicorn

from config import settings
from detection.camera import CameraManager


def check_cameras() -> None:
    devices = CameraManager.detect_available_cameras(settings.MAX_CAMERA_PROBE_INDEX)
    if not devices:
        print("No physical cameras detected.")
        sys.exit(1)
    for dev in devices:
        print(f"Index {dev.index}: {dev.name} ({dev.width}x{dev.height})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sentinel AI Safety Monitoring Launcher")
    parser.add_argument(
        "command",
        choices=["backend", "dashboard", "check-cameras"],
        help="Component to run",
    )
    args = parser.parse_args()

    if args.command == "check-cameras":
        check_cameras()
    elif args.command == "backend":
        uvicorn.run(
            "backend.main:app",
            host=settings.API_HOST,
            port=settings.API_PORT,
            reload=False,
        )
    elif args.command == "dashboard":
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "dashboard/app.py"],
            check=True,
        )


if __name__ == "__main__":
    main()
