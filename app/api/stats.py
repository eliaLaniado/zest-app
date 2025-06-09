from fastapi import APIRouter, Depends
from prometheus_client import generate_latest
from fastapi.responses import Response
from app.api.dependencies import get_metrics
from app.core.metrics import BaseMetrics

router = APIRouter()

@router.get("/statistics")
async def get_statistics(
    metrics: BaseMetrics = Depends(get_metrics)
) -> dict:
    #return metrics.get_statistics()
    return Response(generate_latest(), media_type="text/plain")
