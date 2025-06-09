from fastapi import APIRouter, Depends
from prometheus_client import Gauge, generate_latest, CollectorRegistry
from fastapi.responses import Response
from app.api.dependencies import get_metrics
from app.core.metrics import BaseMetrics

router = APIRouter()

@router.get("/statistics")
async def get_statistics(
    metrics: BaseMetrics = Depends(get_metrics)
) -> dict:
    stats = metrics.get_statistics()

    registry = CollectorRegistry()
    g_processed = Gauge('tasks_processed', 'Total tasks processed', registry=registry)
    g_retried = Gauge('tasks_retried', 'Total task retries', registry=registry)
    g_succeeded = Gauge('tasks_succeeded', 'Successful tasks', registry=registry)
    g_failed = Gauge('tasks_failed', 'Failed tasks', registry=registry)
    g_queue_length = Gauge('queue_length', 'Current queue size', registry=registry)
    g_idle_workers = Gauge('idle_workers', 'Idle workers count', registry=registry)
    g_active_workers = Gauge('active_workers', 'Active workers count', registry=registry)

    g_processed.set(stats["tasks_processed"])
    g_retried.set(stats["tasks_retried"])
    g_succeeded.set(stats["tasks_succeeded"])
    g_failed.set(stats["tasks_failed"])
    g_queue_length.set(stats["queue_length"])
    g_idle_workers.set(stats["idle_workers"])
    g_active_workers.set(stats["active_workers"])

    return Response(generate_latest(registry), media_type="text/plain")