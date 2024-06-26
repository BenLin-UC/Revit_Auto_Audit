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
import csv
import os
from pyrevit import script
from __init__ import logger  # Import the logger from __init__.py

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager


def collect_in_place_families(revit_doc):
    """
    Count the number of in-place families in a Revit document.

    Args:
        revit_doc (Autodesk.Revit.DB.Document): The Revit document object.

    Returns:
        int: The number of in-place families in the document.
    """
    collector = FilteredElementCollector(revit_doc).OfClass(FamilyInstance)
    model_in_place_elements = [elem for elem in collector if elem.Symbol.Family.IsInPlace]
    return len(model_in_place_elements)


def collect_basic_data(docs, output_dir, file_name):
    """
    Collect basic audit data from a list of Revit documents and export to a CSV file.

    Args:
        docs (list): A list of Revit document objects.
        output_dir (str): The directory path where the CSV file will be saved.
        file_name (str): The name of the CSV file.

    Returns:
        str: A success message if the CSV export is successful, or an error message if an exception occurs.
    """
    output_path = os.path.join(output_dir, file_name)  # Ensure path is correct
    fieldnames = ['Document Title', 'Purgeable Elements', 'Detail Groups', 'Detail Group Instances', 'In-Place Families']
    data = []
    errors = []

    for doc in docs:
        if doc:  # Check if document is not null
            try:
                # Collect purgeable elements, detail groups, and in-place families
                unused_elements_count = sum(
                    1 for elem in FilteredElementCollector(doc).OfClass(Family)
                    if not FilteredElementCollector(doc).OfClass(FamilyInstance).OfCategoryId(elem.FamilyCategory.Id).ToElements())
                detail_groups = len(
                    set(g.Name for g in FilteredElementCollector(doc).OfClass(Group)
                        if g.GroupType.FamilyName == "Detail Group"))
                detail_group_instances = len(
                    [g for g in FilteredElementCollector(doc).OfClass(Group)
                     if g.GroupType.FamilyName == "Detail Group"])
                in_place_count = collect_in_place_families(doc)
                data.append({
                    'Document Title': doc.Title,
                    'Purgeable Elements': unused_elements_count,
                    'Detail Groups': detail_groups,
                    'Detail Group Instances': detail_group_instances,
                    'In-Place Families': in_place_count
                })
            except Exception as e:
                errors.append(f"Error processing document {doc.Title}: {str(e)}")
                logger.error(f"Error processing document {doc.Title}: {str(e)}")
        else:
            errors.append("Encountered a null document; skipping.")
            logger.warning("Encountered a null document; skipping.")

    # Write data to CSV if data was collected
    if data:
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            table_html = "<table>"
            table_html += "<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>".format(*fieldnames)
            for row in data[:10]:
                table_html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                    row['Document Title'], row['Purgeable Elements'], row['Detail Groups'], row['Detail Group Instances'], row['In-Place Families'])
            table_html += "</table>"

            result_message = "CSV export successful.\n\n" + table_html

        except Exception as e:
            result_message = f"Failed to export CSV. Error: {str(e)}"
            logger.error(f"Failed to export CSV. Error: {str(e)}")
    else:
        result_message = "No data to export."
        logger.warning("No data to export.")

    # Combine result message with any errors
    if errors:
        result_message += "\n" + "\n".join(errors)

    return result_message