import logging
import os
import sys
from datetime import datetime

# Create logs directory
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)

# Create log file with timestamp
log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_file_path = os.path.join(logs_dir, log_file)

# Configure logging
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("mlPipelineLogger")

# Simple usage example
if __name__ == "__main__":
    logger.info("This is a test log message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
