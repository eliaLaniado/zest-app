import time
import logging
from app.core.factories import logger_factory, metrics_factory, queue_factory
from app.worker.manager import WorkerManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting worker service")
    
    # Initialize dependencies
    queue = queue_factory()
    logger_component = logger_factory()
    metrics = metrics_factory()
    
    # Create and start worker manager
    manager = WorkerManager(queue, logger_component, metrics)
    manager.start()
    
    try:
        # Main monitoring loop
        while True:
            # Update metrics
            queue_length = queue.get_queue_length()
            metrics.set_queue_length(queue_length)
            metrics.set_worker_counts(
                active=manager.active_workers,
                idle=manager.idle_workers
            )
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down worker service")
        manager.stop()
    except Exception as e:
        logger.exception(f"Critical error in worker: {str(e)}")
        manager.stop()

if __name__ == "__main__":
    main()