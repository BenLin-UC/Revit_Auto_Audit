import clr
import csv
import os
from pyrevit import script
from _collections import deque

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

from __init__ import logger  # Import the logger from __init__.py

def generate_table_html(data, fieldnames, max_rows=10):
    """
    Generate an HTML table string from the given data.

    Args:
        data (list): A list of dictionaries containing the data.
        fieldnames (list): A list of fieldnames for the table headers.
        max_rows (int): The maximum number of rows to include in the table.

    Returns:
        str: An HTML string representing the table.
    """
    table_html = "<table>"
    table_html += "<tr><th>{}</th><th>{}</th><th>{}</th></tr>".format(*fieldnames)
    for row in deque(data, maxlen=max_rows):
        table_html += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(row['Document Title'], row['Warning Descriptions'], row['Related Elements'])
    table_html += "</table>"
    return table_html

def collect_warning_data(docs, output_dir, file_name):
    """
    Collect warning data from a list of Revit documents and export to a CSV file.

    Args:
        docs (list): A list of Revit document objects.
        output_dir (str): The directory path where the CSV file will be saved.
        file_name (str): The name of the CSV file.

    Returns:
        str: A success message if the CSV export is successful, or an error message if an exception occurs.
    """
    output_path = os.path.join(output_dir, file_name)
    fieldnames = ['Document Title', 'Warning Descriptions', 'Related Elements']
    data = []

    for doc in docs:
        if doc:
            try:
                warnings = doc.GetWarnings()
                workset_table = doc.GetWorksetTable()  # Get the workset table from the document

                for warning in warnings:
                    description = warning.GetDescriptionText()
                    failing_elements = warning.GetFailingElements()
                    elements_detail = []

                    for elem_id in failing_elements:
                        elem = doc.GetElement(elem_id)
                        if elem:
                            category = elem.Category.Name if elem.Category else "No Category"
                            try:
                                name = elem.Name  # Try to access the Name property directly
                            except TypeError:  # Handles cases where elem.Name is not accessible
                                name = elem.LookupParameter("Name").AsString() if elem.LookupParameter("Name") else "Not a Name"
                                if not name:  # Fallback if parameter is None or empty
                                    name = "Not a Name"

                            # Retrieve workset information
                            workset_id = elem.WorksetId
                            workset = workset_table.GetWorkset(workset_id)
                            workset_name = workset.Name if workset else "No Workset"

                            elements_detail.append(f"{workset_name}: <{category}> {name}: [{elem_id}]")

                    related_elements = '; \n '.join(elements_detail)
                    data.append({
                        'Document Title': doc.Title,
                        'Warning Descriptions': description,
                        'Related Elements': related_elements
                    })
            except Exception as e:
                logger.error(f"Error processing document {doc.Title}: {str(e)}")
        else:
            logger.warning("Encountered a null document; skipping.")

    # Write data to CSV
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except PermissionError:
        logger.error(f"Error: You don't have permission to write to {output_path}")
        return
    except Exception as e:
        logger.error(f"Error: Failed to export CSV. {str(e)}")
        return

    table_html = generate_table_html(data, fieldnames)
    heading = "<h3>Top Entries</h3>" if table_html else ""
    result_message = "CSV export successful.\n" + heading + table_html

    return result_message