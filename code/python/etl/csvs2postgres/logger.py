import os
from datetime import datetime
from loguru import logger

def setup_logging(log_dir="/home/jovyan/code/logs", prefix="log"):
    """Configures Loguru logger to write to a timestamped log file."""

    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"{prefix}_{timestamp}.log"
    log_path = os.path.join(log_dir, log_filename)

    # Remove any default handlers to avoid duplicates
    logger.remove()

    # File handler
    logger.add(
        log_path,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        rotation="10 MB",
        enqueue=True
    )

    # Console handler
    logger.add(
        sink=lambda msg: print(msg),
        level="DEBUG",
        format="<cyan>{level}</cyan> - {message}"
    )

    logger.info(f"Logging to file: {log_path}")