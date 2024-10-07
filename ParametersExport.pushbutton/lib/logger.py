import os
import logging

def setup_logger(name, log_file, level=logging.INFO):
    """
    Sets up a logger that writes logs to a specified file.

    Args:
        name (str): The name of the logger.
        log_file (str): The name of the log file where logs will be written.
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Get the user's AppData directory
    appdata_dir = os.getenv('APPDATA')

    # Create a log file path in the AppData directory
    log_file_path = os.path.join(appdata_dir, 'CustomRevitExtension\\Preformance.extension\\Preformance.tab\\Audit.panel\\TestButton_2.pushbutton\\logs\\ParametersExport.log')

    # Ensure the directory exists
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger('ParametersExportLogger')
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Adding handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Initialize the logger
logger = setup_logger('ParametersExportLogger', 'ParametersExport.log')