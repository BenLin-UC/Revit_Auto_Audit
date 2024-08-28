import os
import sys
import clr
import logging

from lib.ui import (
    load_xaml,
    initialize_ui,
    handle_confirm_click,
    handle_cancel_click,
    handle_search_text_changed,
    handle_select_toggle_click,
    highlight_search_box,
    populate_list
)
from lib.core_processing import (
    get_documents,
    get_model_categories, 
    get_category_parameters, 
    get_parameter_values, 
    export_data_to_csv
)
from lib.warning import (
    display_warning, 
    display_error,
    handle_exception
)

from lib.logger import setup_logger

def main():
    doc = __revit__.ActiveUIDocument.Document
    appdata_dir = os.getenv('APPDATA')
    log_file_path = os.path.join(appdata_dir, 'CustomRevitExtension', 'Preformance.extension', 'Preformance.tab', 'Audit.panel', 'ParametersExport.pushbutton', 'logs', 'ParametersExport.log')
    logger = setup_logger(log_file_path, logging.DEBUG)
    # Set the path to the XAML file
    xaml_file_path = os.path.join(appdata_dir, 'CustomRevitExtension', 'Preformance.extension', 'Preformance.tab', 'Audit.panel', 'ParametersExport.pushbutton', 'lib','SimpleUI.xaml')

    try:
        # Initialize state
        state = {
            "doc": doc,  # This should be set with the current document at some point
            "step": "models",
            "selected_documents": None,
            "selected_categories": None,
            "selected_parameters": None
        }
        # Load the UI
        window = load_xaml(xaml_file_path)

        # Populate the list with document names immediately
        docs = get_documents(doc)
        model_names = [f"Current Model: {doc.Title}"] + [f"Linked Model: {link.Title}" for link in docs[1:]]  # Skip the first one as it's the current document
        ui_elements = {
            'ItemList': window.FindName('ItemList'),
            'ConfirmButton': window.FindName('ConfirmButton'),
            'CancelButton': window.FindName('CancelButton'),
            'SearchBox': window.FindName('SearchBox'),
            'SelectToggleButton': window.FindName('SelectToggleButton'),
        }
        populate_list(ui_elements['ItemList'], model_names)

        # Initialize the UI
        initialize_ui(
            window,
            lambda s, e, st: handle_confirm_click(window, ui_elements['ItemList'], state),
            lambda s: handle_cancel_click(window),  # Pass window to handle_cancel_click
            lambda s, e: handle_search_text_changed(ui_elements['ItemList'], ui_elements['SearchBox']),
            lambda s, e: handle_select_toggle_click(ui_elements['ItemList'], ui_elements['SelectToggleButton']),
            initial_items=model_names,
            state=state
        )
        window.ShowDialog()

    except Exception as ex:
        handle_exception(ex)

if __name__ == "__main__":
    main()