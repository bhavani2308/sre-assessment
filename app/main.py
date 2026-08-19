import asyncio
import logging
import os
import socket
import time
from datetime import datetime, UTC

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI(
    title="SRE Operations Dashboard",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")


# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("sre-app")


# --------------------------------------------------
# Application counters
# --------------------------------------------------

metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0
}


application_start_time = time.time()


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    logger.info("Dashboard accessed")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# --------------------------------------------------
# Health endpoint
# --------------------------------------------------

@app.get("/health")
async def health():

    logger.info("Health check passed")

    return {
    "status": "healthy",
    "timestamp": datetime.now(UTC).isoformat(),
    "hostname": socket.gethostname()
}


# --------------------------------------------------
# Readiness endpoint
# --------------------------------------------------

@app.get("/ready")
async def ready():

    return {
        "status": "ready"
    }


# --------------------------------------------------
# Application status
# --------------------------------------------------

@app.get("/api/status")
async def status():

    uptime = int(time.time() - application_start_time)

    return {
        "application": "SRE Operations Dashboard",
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "hostname": socket.gethostname(),
        "uptime_seconds": uptime,
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": metrics
    }


# --------------------------------------------------
# Generate normal request
# --------------------------------------------------

@app.post("/api/request")
async def generate_request():

    metrics["total_requests"] += 1
    metrics["successful_requests"] += 1

    logger.info(
        "Successful application request processed. Total=%s",
        metrics["total_requests"]
    )

    return {
        "message": "Request processed successfully",
        "timestamp": datetime.utcnow().isoformat()
    }


# --------------------------------------------------
# Simulate application error
# --------------------------------------------------

@app.post("/api/error")
async def generate_error():

    metrics["total_requests"] += 1
    metrics["failed_requests"] += 1

    logger.error(
        "Simulated application failure triggered"
    )

    raise HTTPException(
        status_code=500,
        detail="Simulated application failure"
    )


# --------------------------------------------------
# Simulate slow response
# --------------------------------------------------

@app.post("/api/slow")
async def slow_request():

    metrics["total_requests"] += 1

    logger.warning(
        "Slow request simulation started"
    )

    await asyncio.sleep(5)

    metrics["successful_requests"] += 1

    logger.info(
        "Slow request completed successfully"
    )

    return {
        "message": "Slow request completed",
        "duration_seconds": 5
    }