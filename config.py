"""Centralized configuration for Sentinel AI loaded from environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _get_bool(key: str, default: bool = False) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    """Application settings loaded from environment variables."""

    APP_NAME: str = "Sentinel AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # FastAPI server
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # Camera & Detection
    DEFAULT_CAMERA_INDEX: int = int(os.getenv("DEFAULT_CAMERA_INDEX", "0"))
    MAX_CAMERA_PROBE_INDEX: int = int(os.getenv("MAX_CAMERA_PROBE_INDEX", "5"))
    YOLO_MODEL_PATH: str = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.50"))
    FRAME_PROCESS_INTERVAL: float = float(os.getenv("FRAME_PROCESS_INTERVAL", "0.15"))
    INCIDENT_COOLDOWN_SECONDS: int = int(os.getenv("INCIDENT_COOLDOWN_SECONDS", "30"))

    # PPE Requirements
    REQUIRE_HELMET: bool = _get_bool("REQUIRE_HELMET", True)
    REQUIRE_VEST: bool = _get_bool("REQUIRE_VEST", True)

    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = os.getenv(
        "FIREBASE_CREDENTIALS_PATH", "secrets/firebase-service-account.json"
    )
    FIRESTORE_COLLECTION: str = os.getenv("FIRESTORE_COLLECTION", "safety_incidents")

    # Twilio
    TWILIO_MOCK_MODE: bool = _get_bool("TWILIO_MOCK_MODE", True)
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_FROM_NUMBER: str = os.getenv("TWILIO_FROM_NUMBER", "")
    TWILIO_TO_NUMBER: str = os.getenv("TWILIO_TO_NUMBER", "")
    TWILIO_ALERT_COOLDOWN_SECONDS: int = int(
        os.getenv("TWILIO_ALERT_COOLDOWN_SECONDS", "120")
    )
    TWILIO_MIN_CONFIDENCE: float = float(os.getenv("TWILIO_MIN_CONFIDENCE", "0.55"))


settings = Settings()
