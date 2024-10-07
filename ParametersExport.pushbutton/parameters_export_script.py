import os
import logging
import traceback
from pyrevit import forms

from lib.ui import (
    select_models, 
    select_categories, 
    select_parameters, 
    display_data_table
)
from lib.core_processing import (
#    get_documents,
#    get_model_categories, 
#    get_category_parameters, 
    get_parameter_values, 
#    export_data_to_csv
)
from lib.warning import (
    display_warning, 
#    display_error,
    handle_exception
)

from lib.logger import setup_logger

def main():
    doc = __revit__.ActiveUIDocument.Document
    appdata_dir = os.getenv('APPDATA')
    log_file_path = os.path.join(appdata_dir, 'CustomRevitExtension', 'Preformance.extension', 'Preformance.tab', 'Audit.panel', 'TestButton_2.pushbutton', 'logs', 'ParametersExport.log')
    logger = setup_logger(log_file_path, logging.DEBUG)

    try:
        # Step 1: Select Models
        selected_documents = select_models(doc)
        if not selected_documents:
            display_warning("No models selected. Operation cancelled.")
            return

        # Step 2: Select Categories
        selected_categories = select_categories(selected_documents)
        if not selected_categories:
            display_warning("No categories selected. Operation cancelled.")
            return

        # Step 3: Select Parameters
        selected_parameters = select_parameters(selected_categories)
        if not selected_parameters:
            display_warning("No parameters selected. Operation cancelled.")
            return

        # Process the data with progress bar
        data_by_document = {doc.Title: [] for doc in selected_documents}
        total_items = sum(len(doc_category_pairs) for doc_category_pairs in selected_categories.values())
        
        with forms.ProgressBar(title='Processing Data', cancellable=True, step=1) as pb:
            current_item = 0
            for category_name, doc_category_pairs in selected_categories.items():
                for doc, category in doc_category_pairs:
                    get_parameter_values(doc, category, selected_parameters, data_by_document)
                    current_item += 1
                    percentage = (current_item / total_items) * 100
                    pb.update_progress(current_item, total_items)
                    pb.title = f'Processing Data: {percentage:.2f}%'

                    if pb.cancelled:
                        forms.alert('Operation cancelled by user.', title='Cancelled')
                        return

        # Display data and export
        display_data_table(data_by_document, selected_parameters)

    except Exception as ex:
        handle_exception(ex)

if __name__ == "__main__":
    main()