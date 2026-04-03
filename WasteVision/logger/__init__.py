import os
import sys
import logging
from datetime import datetime

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Create logs directory
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Create unique log file per run
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filepath = os.path.join(log_dir, f"run_{timestamp}.log")

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("WasteVisionLogger")

logger.info("Logging initialized")