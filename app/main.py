from fastapi import FastAPI
from app.api import tasks, stats, metrics
from app.core.config import settings
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Task Processing Service",
    description="Microservice for asynchronous task processing",
    version="1.0.0"
)

# Include routers
app.include_router(tasks.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(metrics.router)

@app.on_event("startup")
async def startup():
    logger.info("Starting application")
    os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)

@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down application")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=settings.SERVER_PORT,
        log_config=None
    )