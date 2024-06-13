"""
__title__ = "AutoAudit"
__doc__ = """Version = 1.1
Date    = 06.06.2024
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> Change Settings(optional)
-> Make a change
_____________________________________________________________________
Last update:
- [24.04.2024] - 1.0 RELEASE
- [06.06.2024] - 1.1 UPDATE - ANNOTATION
_____________________________________________________________________
Author: Ben Lin - Preformance
"""

__author__ = "Preformance"
__min_revit_ver__ = 2021
__max_revit_ver = 2023
"""

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

# Get the active Revit document
doc = __revit__.ActiveUIDocument.Document


def main():
    """Main function to collect and process Revit document data."""
    output = script.get_output()
    user_inputs = show_ui()

    if user_inputs is None:
        logger.warning("User cancelled the input.")
        return

    # Ensure all necessary inputs are provided
    if not all([user_inputs.get('output_dir'), user_inputs.get('warning_file_name'), user_inputs.get('audit_file_name')]):
        logger.error("Error: All input fields are required.")
        return

    try:
        if not doc:
            logger.error("Error: No active document found.")
            return

        # List to store the main document and linked documents
        linked_docs = [doc]

        # Collect linked documents
        link_instances = FilteredElementCollector(doc).OfClass(RevitLinkInstance)
        for link in link_instances:
            linked_doc = link.GetLinkDocument()
            if linked_doc:
                linked_docs.append(linked_doc)
            else:
                logger.warning("Warning: One or more linked documents could not be loaded.")

        # Collect and process warning data
        warning_status = collect_warning_data(
            linked_docs, user_inputs['output_dir'], user_inputs['warning_file_name'])
        # Collect and process basic audit data
        basic_status = collect_basic_data(
            linked_docs, user_inputs['output_dir'], user_inputs['audit_file_name'])

        # Log and display the results
        logger.info("Warning Processing Result: {}".format(
            warning_status.split('\n')[0]))
        output.print_html(warning_status[warning_status.find('\n')+1:])
        logger.info("Basic Audit Processing Result: {}".format(
            basic_status.split('\n')[0]))
        output.print_html(basic_status[basic_status.find('\n')+1:])

    except Exception as e:
        logger.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()