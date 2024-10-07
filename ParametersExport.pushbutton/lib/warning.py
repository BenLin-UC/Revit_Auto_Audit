import logging
import sys
import traceback
from pyrevit import forms

logger = logging.getLogger('ParametersExport')

def log_warning(message):
    """
    Log a warning message.
    
    Args:
        message (str): The warning message to log.
    """
    logger.warning(message)

def log_error(message):
    """
    Log an error message.
    
    Args:
        message (str): The error message to log.
    """
    logger.error(message)

def display_warning(message):
    """
    Display a warning to the user and log it.
    
    Args:
        message (str): The warning message to display and log.
    """
    log_warning(message)
    forms.alert(message, title='Warning')

def display_error(message, exception=None):
    """
    Display an error to the user and log it with detailed information.

    Args:
        message (str): The error message to display and log.
        exception (Exception, optional): The exception to include more context.
    """
    detailed_message = message
    if exception:
        detailed_message += f": {str(exception)}"
    log_error(detailed_message)
    forms.alert(detailed_message, title='Error')
    
def handle_exception(exception):
    """
    Handle an exception by logging and displaying an error message.
    
    Args:
        exception (Exception): The exception to handle.
    """
    display_error("An unexpected error occurred", exception)