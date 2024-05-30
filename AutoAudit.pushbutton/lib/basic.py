import clr
import csv
import os
from pyrevit import script

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

def collect_in_place_families(revit_doc):
    collector = FilteredElementCollector(revit_doc).OfClass(FamilyInstance)
    model_in_place_elements = [elem for elem in collector if elem.Symbol.Family.IsInPlace]
    return len(model_in_place_elements)

def collect_basic_data(docs, output_dir, file_name):
    output_path = os.path.join(output_dir, file_name)  # Ensure path is correct
    fieldnames = ['Document Title', 'Purgeable Elements', 'Detail Groups', 'Detail Group Instances', 'In-Place Families']
    data = []
    errors = []

    for doc in docs:
        if doc:  # Check if document is not null
            try:
                unused_elements_count = sum(1 for elem in FilteredElementCollector(doc).OfClass(Family) if not FilteredElementCollector(doc).OfClass(FamilyInstance).OfCategoryId(elem.FamilyCategory.Id).ToElements())
                detail_groups = len(set(g.Name for g in FilteredElementCollector(doc).OfClass(Group) if g.GroupType.FamilyName == "Detail Group"))
                detail_group_instances = len([g for g in FilteredElementCollector(doc).OfClass(Group) if g.GroupType.FamilyName == "Detail Group"])
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
        else:
            errors.append("Encountered a null document; skipping.")

    # Write data to CSV if data was collected
    if data:
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

                    
            table_html = "<table>"
            table_html += "<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>".format(*fieldnames)
            for row in data[:10]:
                table_html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(row['Document Title'], row['Purgeable Elements'], row['Detail Groups'], row['Detail Group Instances'], row['In-Place Families'])
            table_html += "</table>"

            result_message = "CSV export successful.\n\n" + table_html
            
        except Exception as e:
            result_message = f"Failed to export CSV. Error: {str(e)}"
    else:
        result_message = "No data to export."

    # Combine result message with any errors
    if errors:
        result_message += "\n" + "\n".join(errors)

    return result_message