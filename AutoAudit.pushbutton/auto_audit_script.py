import clr
import os
from lib.warning import collect_warning_data
from lib.basic import collect_basic_data
from lib.ui import show_ui
from pyrevit import script

from __init__ import logger  # Import the logger from __init__.py

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

doc = __revit__.ActiveUIDocument.Document

def main():
    output = script.get_output()
    user_inputs = show_ui()

    if user_inputs is None:
        logger.warning("User cancelled the input.")
        return

    # Make sure all fields have values
    if not all([user_inputs.get('output_dir'), user_inputs.get('warning_file_name'), user_inputs.get('audit_file_name')]):
        logger.error("Error: All input fields are required.")
        return

    try:
        if not doc:
            logger.error("Error: No active document found.")
            return  # Exit the function if there's no active document

        # Gather documents safely
        linked_docs = [doc]  # Start with the main document

        # Check if the doc is not null before creating FilteredElementCollector
        if doc:
            link_instances = FilteredElementCollector(doc).OfClass(RevitLinkInstance)
            for link in link_instances:
                linked_doc = link.GetLinkDocument()
                if linked_doc:  # Check if the linked document is loaded
                    linked_docs.append(linked_doc)
                else:
                    logger.warning("Warning: One or more linked documents could not be loaded.")

        # Process warnings and basic data
        warning_status = collect_warning_data(linked_docs, user_inputs['output_dir'], user_inputs['warning_file_name'])
        basic_status = collect_basic_data(linked_docs, user_inputs['output_dir'], user_inputs['audit_file_name'])

        logger.info("Warning Processing Result: {}".format(warning_status.split('\n')[0]))
        output.print_html(warning_status[warning_status.find('\n')+1:])
        logger.info("Basic Audit Processing Result: {}".format(basic_status.split('\n')[0]))
        output.print_html(basic_status[basic_status.find('\n')+1:])

    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()