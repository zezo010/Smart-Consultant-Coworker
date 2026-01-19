"""FastAPI application main module."""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..common.config import settings
from ..common.logging import get_logger
from ..common.schemas import HealthCheck
from .routes import router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting HexaGen GRC Engine...")
    logger.info(f"Ollama URL: {settings.ollama_base_url}")
    logger.info(f"Chroma Path: {settings.chroma_path}")

    # Ensure directories exist
    settings.ensure_directories()
    logger.info("Directories initialized")

    # Initialize services (KB, agents, etc.)
    # TODO: Initialize vector DB, load models, etc.

    logger.info("HexaGen GRC Engine started successfully")

    yield

    # Shutdown
    logger.info("Shutting down HexaGen GRC Engine...")
    # TODO: Cleanup resources
    logger.info("HexaGen GRC Engine shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="HexaGen GRC Engine",
    description="Offline Multi-Agent GRC Security Consultant",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An error occurred"
        }
    )


# Health check endpoint
@app.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check() -> HealthCheck:
    """
    Health check endpoint.

    Returns the health status of the service and its dependencies.
    """
    # TODO: Check Ollama availability
    # TODO: Check Chroma availability

    return HealthCheck(
        status="healthy",
        version="0.1.0",
        ollama_available=False,  # TODO: Implement check
        chroma_available=False,  # TODO: Implement check
    )


# Include routers
app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root() -> dict:
    """Root endpoint."""
    return {
        "message": "HexaGen GRC Engine",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "hexagen_grc.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )
