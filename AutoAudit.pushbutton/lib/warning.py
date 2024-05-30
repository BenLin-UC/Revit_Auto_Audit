import clr
import csv
import os
from pyrevit import script
from _collections import deque
#from itertools import zip_longest

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

def collect_warning_data(docs, output_dir, file_name):
    output_path = os.path.join(output_dir, file_name)  # Ensure path is correct
    fieldnames = ['Document Title', 'Warning Descriptions', 'Related Elements']
    data = []

    for doc in docs:
        if doc:  # Check if document is not null
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
                print(f"Error: {str(e)}")
                return
        else:
            print("Document is null. Skipping.")

    # Write data to CSV
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

        # Print top 10 entries in a table visualiSation
        output = script.get_output()
        table_html = "<table>"
        table_html += "<tr><th>{}</th><th>{}</th><th>{}</th></tr>".format(*fieldnames)
        for row in deque(data, maxlen=10):
            table_html += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(row['Document Title'], row['Warning Descriptions'], row['Related Elements'])
        table_html += "</table>"

        heading = "<h3>Top 10 Entries</h3>" or ""
        table = table_html or ""

        return "CSV export successful.\n" + heading + table
    except Exception as e:
        print(f"Error: {str(e)}")
        return