# Configure logs to retrieve INFO messages and higher
import os
import logging
from datetime import datetime



def setup_logging():
    os.makedirs("logs", exist_ok=True)

    log_filename = (f"logs/{__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_filename
    )

    return logging.getLogger(__name__) #this takes the name of the current module (file) as the logger name, which is a common practice in Python logging
