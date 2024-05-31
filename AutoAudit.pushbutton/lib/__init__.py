# Import the logging module
import logging
import os
from logging.handlers import RotatingFileHandler

# Get the user's AppData directory
appdata_dir = os.getenv('APPDATA')

# Create a log file path in the AppData directory
log_file_path = os.path.join(appdata_dir, 'CustomRevitExtension\\Preformance.extension\\Preformance.tab\\Audit.panel\\AutoAudit.pushbutton\\AutoAudit.log')

# Create a logger instance
logger = logging.getLogger(__name__)

# Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.setLevel(logging.DEBUG)

# Create a rotating file handler
file_handler = RotatingFileHandler(log_file_path, maxBytes=1024*1024, backupCount=5)  # 1 MB file size, keep 5 backup files
file_handler.setLevel(logging.INFO)

# Create a console handler to print logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter to specify the log message format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Set the formatter for the file and console handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)