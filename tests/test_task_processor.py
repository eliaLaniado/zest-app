from app.worker.processor import TaskProcessor

def test_successful_task_processing(mock_logger, mock_metrics, sample_task):
    processor = TaskProcessor(mock_logger, mock_metrics)
    # Force success
    import app.core.config as config
    config.settings.TASK_SIMULATED_ERROR_PERCENTAGE = 0
    success, processing_time = processor.process(sample_task)
    assert success is True
    assert processing_time > 0
    mock_metrics.task_started.assert_called_once()
    mock_metrics.task_succeeded.assert_called_once()
    mock_logger.log.assert_called_once()

def test_failed_task_processing(mock_logger, mock_metrics, sample_task):
    processor = TaskProcessor(mock_logger, mock_metrics)
    # Force failure
    import app.core.config as config
    config.settings.TASK_SIMULATED_ERROR_PERCENTAGE = 1
    success, processing_time = processor.process(sample_task)
    assert success is False
    assert processing_time > 0
    mock_metrics.task_failed.assert_called_once()
    mock_logger.error.assert_called_once()