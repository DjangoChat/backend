import time
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import structlog

logger = structlog.get_logger(__name__)


def health_check(request):
    """Comprehensive health check endpoint."""
    health = {
        "status": "healthy",
        "timestamp": time.time(),
        "version": getattr(settings, "APP_VERSION", "unknown"),
        "checks": {},
    }

    # Database check
    try:
        start = time.time()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health["checks"]["database"] = {
            "status": "healthy",
            "latency_ms": round((time.time() - start) * 1000, 2),
        }
    except Exception as e:
        logger.error("health_check_database_failed", error=str(e))
        health["status"] = "unhealthy"
        health["checks"]["database"] = {"status": "unhealthy", "error": str(e)}

    # Cache check
    try:
        start = time.time()
        cache.set("health_check", "ok", 10)
        value = cache.get("health_check")
        if value != "ok":
            raise Exception("Cache read/write mismatch")
        health["checks"]["cache"] = {
            "status": "healthy",
            "latency_ms": round((time.time() - start) * 1000, 2),
        }
    except Exception as e:
        logger.error("health_check_cache_failed", error=str(e))
        health["status"] = "unhealthy"
        health["checks"]["cache"] = {"status": "unhealthy", "error": str(e)}

    # Celery check
    try:
        from config.celery import app

        inspect = app.control.inspect()
        stats = inspect.stats()
        if stats:
            health["checks"]["celery"] = {"status": "healthy", "workers": len(stats)}
        else:
            raise Exception("No workers responding")
    except Exception as e:
        logger.warning("health_check_celery_failed", error=str(e))
        health["checks"]["celery"] = {"status": "degraded", "error": str(e)}

    status_code = 200 if health["status"] == "healthy" else 503
    return JsonResponse(health, status=status_code)


def readiness_check(request):
    """Check if app is ready to receive traffic."""
    # Simpler check for load balancer
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ready"})
    except:
        return JsonResponse({"status": "not ready"}, status=503)


def liveness_check(request):
    """Check if app process is alive."""
    # Just return OK if the process is running
    return JsonResponse({"status": "alive"})
