from fastapi import APIRouter, Depends

from app.api.dependencies import get_metrics
from app.core.metrics import BaseMetrics

router = APIRouter()

@router.get("/statistics")
async def get_statistics(
    metrics: BaseMetrics = Depends(get_metrics)
) -> dict:
    return metrics.get_statistics()

@router.post("/statistics/reset")
async def reset_statistics(
    metrics: BaseMetrics = Depends(get_metrics)
) -> dict:
    metrics.reset()
    return {"status": "ok", "message": "Statistics reset."}