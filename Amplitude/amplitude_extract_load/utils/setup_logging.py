# Configure logs to retrieve INFO messages and higher
import os
import logging
from datetime import datetime

def setup_logging(logs_dir):
    # log_dir = 'logs'
    # os.makedirs(log_dir, exist_ok=True)
    # log_dir = os.path.join(log_dir)

    os.makedirs(logs_dir, exist_ok=True)
    log_filepath = os.path.join(logs_dir, (f"{__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"))

    log_filename = (f"{logs_dir}/{__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_filepath
    )

    return logging.getLogger(__name__) #this takes the name of the current module (file) as the logger name, which is a common practice in Python logging
