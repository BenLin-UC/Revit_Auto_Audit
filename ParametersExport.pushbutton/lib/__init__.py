import os
import logging

# Initialize the logger for the entire package
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'ParametersExport.log')

logging.basicConfig(
    filename=log_file,
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('ParameterExport')

# Import core functions for easier access
from .core_processing import (
    get_documents,
    get_model_categories,
    get_category_parameters,
    get_parameter_values,
    export_data_to_csv
)

from .warning import (
    display_warning,
    display_error
)

__all__ = [
    'get_documents',
    'get_model_categories',
    'get_category_parameters',
    'get_parameter_values',
    'export_data_to_csv',
    'load_xaml',
    'initialize_ui',
    'populate_list',
    'handle_confirm_click',
    'handle_cancel_click',
    'handle_search_text_changed',
    'handle_select_toggle_click',
    'highlight_search_box',
    'display_warning',
    'display_error'
]
