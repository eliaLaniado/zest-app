from app.worker.manager import WorkerManager
import time

def test_worker_manager_lifecycle(mock_queue, mock_logger, mock_metrics, sample_task):
    """Test WorkerManager starts, processes a task, and stops cleanly."""
    mock_queue.dequeue.side_effect = [sample_task, None]
    manager = WorkerManager(mock_queue, mock_logger, mock_metrics, max_workers=1)
    try:
        manager.start()
        time.sleep(0.3)  # Slightly longer for reliability
        assert manager.active is True
    finally:
        manager.stop()
    assert manager.active is False
    mock_metrics.task_processed.assert_called()