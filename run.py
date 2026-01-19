"""Multi-process server runner."""
import uvicorn
import multiprocessing
from src.config import settings


def run_main_server():
    """Run main application server."""
    uvicorn.run(
        "src.main:app",
        host=settings.server_host,
        port=settings.server_port,
        workers=settings.server_workers,
        log_level=settings.log_level.lower(),
        reload=False
    )


def run_metrics_server():
    """Run metrics exporter server."""
    if not settings.metrics_enabled:
        return
    
    # TODO: Implement metrics exporter
    print(f"Metrics server would run on port {settings.metrics_port}")


if __name__ == "__main__":
    # Start main server
    main_process = multiprocessing.Process(target=run_main_server)
    main_process.start()
    
    # Start metrics server if enabled
    if settings.metrics_enabled:
        metrics_process = multiprocessing.Process(target=run_metrics_server)
        metrics_process.start()
    
    # Wait for processes
    main_process.join()
