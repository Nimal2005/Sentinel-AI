"""FastAPI application entry point for Sentinel AI."""

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import health, incidents, monitoring
from backend.services.monitoring_service import MonitoringService
from config import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def create_app(monitoring_service: Optional[MonitoringService] = None) -> FastAPI:
    """Application factory for Sentinel AI backend."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not hasattr(app.state, "monitoring_service") or app.state.monitoring_service is None:
            app.state.monitoring_service = monitoring_service or MonitoringService()
        logger.info("Sentinel AI backend started.")
        try:
            yield
        finally:
            app.state.monitoring_service.stop_monitoring()
            logger.info("Sentinel AI backend shut down cleanly.")

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-Powered Real-Time Worker Safety Monitoring System REST API",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if monitoring_service is not None:
        app.state.monitoring_service = monitoring_service

    app.include_router(health.router)
    app.include_router(monitoring.router)
    app.include_router(incidents.router)

    return app


app = create_app()
