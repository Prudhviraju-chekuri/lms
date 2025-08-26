# app/routers/health_checks.py
from fastapi import APIRouter

router = APIRouter()

@router.get("", tags=["health"])
def health_root():
    """
    GET /health
    Basic health check endpoint.
    """
    return {"status": "ok"}

@router.get("/ready", tags=["health"])
def health_ready():
    """
    GET /health/ready
    Readiness probe — can later be extended to check DB, cache, etc.
    """
    return {"status": "ready"}

@router.get("/live", tags=["health"])
def health_live():
    """
    GET /health/live
    Liveness probe.
    """
    return {"status": "live"}
