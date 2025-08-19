import clr
import csv
import os
from pyrevit import script, forms

from __init__ import logger  # Import the logger from __init__.py

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import System

from RevitServices.Persistence import DocumentManager

def collect_in_place_families(revit_doc):
    """
    Count the number of in-place families in a Revit document.

    Args:
        revit_doc (Autodesk.Revit.DB.Document): The Revit document object.

    Returns:
        int: The number of in-place families in the document.
    """
    try:
        collector = FilteredElementCollector(revit_doc).OfClass(FamilyInstance)
        model_in_place_elements = [elem for elem in collector if elem.Symbol.Family.IsInPlace]
        return len(model_in_place_elements)
    except Exception as e:
        logger.error(f"Error collecting in-place families for {revit_doc.Title}: {str(e)}")
        return 0

def get_non_builtin_categories_count(revit_doc):
    """
    Count the number of invalid built-in categories in the document using BuiltInCategory.INVALID.
    
    Args:
        revit_doc (Autodesk.Revit.DB.Document): The Revit document object.
        
    Returns:
        int: The number of invalid built-in categories.
    """
    try:
        all_categories = revit_doc.Settings.Categories
        non_builtin = []

        for category in all_categories:
            # Check if the category is not a built-in category
            if category.Id.IntegerValue < 0:  # Built-in categories have negative IDs
                continue
            non_builtin.append(category)
            
        count = len(non_builtin)
        return count
    except Exception as e:
        logger.error(f"Error counting invalid built-in categories in {revit_doc.Title}: {str(e)}")
        return 0
    
def get_hidden_views_info(revit_doc):
    """
    Get information about views on sheets that are set to "Do not Display" mode.
    
    Args:
        revit_doc (Autodesk.Revit.DB.Document): The Revit document object.
        
    Returns:
        tuple: (count of hidden views, formatted string of view and sheet names)
    """
    try:
        # Define target view types
        target_view_types = [
            ViewType.FloorPlan,
            ViewType.CeilingPlan,
            ViewType.Elevation,
            ViewType.ThreeD,
            ViewType.EngineeringPlan,
            ViewType.AreaPlan,
            ViewType.Section,
            ViewType.Detail
        ]
        
        # Get all sheets
        sheet_collector = FilteredElementCollector(revit_doc).OfClass(ViewSheet)
        hidden_views_count = 0
        hidden_views_info = []
        
        for sheet in sheet_collector:
            # Get viewport ids on this sheet
            viewport_ids = sheet.GetAllViewports()
            
            for viewport_id in viewport_ids:
                viewport = revit_doc.GetElement(viewport_id)
                if not viewport:
                    continue
                    
                view_id = viewport.ViewId
                view = revit_doc.GetElement(view_id)
                
                # Check if view type is in our target list
                if view and view.ViewType in target_view_types:
                    display_mode_param = view.get_Parameter(
                        BuiltInParameter.VIEW_MODEL_DISPLAY_MODE
                    )
                    if display_mode_param and display_mode_param.AsInteger() == 2:  # 2 = Do not display
                        hidden_views_count += 1
                        # Format: ViewName_SheetNumber
                        view_info = f"{sheet.SheetNumber}: {view.Name}"
                        hidden_views_info.append(view_info)
        
        # Join all view infos with semicolon
        formatted_info = ";".join(hidden_views_info) if hidden_views_info else ""
        
        return hidden_views_count, formatted_info
    
    except Exception as e:
        logger.error(f"Error analyzing hidden views in {revit_doc.Title}: {str(e)}")
        return 0, ""

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
    fieldnames = ['Document Name', 
                  'Document Type',
                  'Purgeable Elements', 
                  'Detail Groups', 
                  'Detail Group Instances', 
                  'In-Place Families',
                  'Non-Builtin Categories',
                  'Hidden Views on Sheets',
                  'View Names & Sheet Names']
    data = []
    errors = []
    
    if not docs:
        errors.append("No documents provided for processing.")
        logger.error("No documents provided for processing.")
        return "No documents provided for processing."

    # Log how many documents we're processing
    logger.info(f"Processing {len(docs)} documents for basic data collection")
    
    # Get the host document (first in the list)
    host_doc = docs[0] if docs else None
    
    for i, doc in enumerate(docs):
        if doc:  # Check if document is not null
            try:
                # Determine document type (host or linked)
                doc_type = "Host" if i == 0 else "Linked"
                
                # Log which document we're currently processing
                logger.info(f"Processing {doc_type}: {doc.Title}")
                
                unused_elements_count = sum(1 for elem in FilteredElementCollector(doc).OfClass(Family) 
                                           if not FilteredElementCollector(doc).OfClass(FamilyInstance).OfCategoryId(elem.FamilyCategory.Id).ToElements())
                
                detail_groups = len(set(g.Name for g in FilteredElementCollector(doc).OfClass(Group) 
                                       if g.GroupType and g.GroupType.FamilyName == "Detail Group"))
                
                detail_group_instances = len([g for g in FilteredElementCollector(doc).OfClass(Group) 
                                           if g.GroupType and g.GroupType.FamilyName == "Detail Group"])
                
                in_place_count = collect_in_place_families(doc)
                non_builtin_count = get_non_builtin_categories_count(doc)
                hidden_views_count, hidden_views_info = get_hidden_views_info(doc)
                
                data.append({
                    'Document Name': doc.Title,
                    'Document Type': doc_type,
                    'Purgeable Elements': unused_elements_count,
                    'Detail Groups': detail_groups,
                    'Detail Group Instances': detail_group_instances,
                    'In-Place Families': in_place_count,
                    'Non-Builtin Categories': non_builtin_count,
                    'Hidden Views on Sheets': hidden_views_count,
                    'View Names & Sheet Names': hidden_views_info
                    })
                
                logger.info(f"Successfully processed {doc.Title}")
                
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
            table_html += "<tr>" + "".join(f"<th>{field}</th>" for field in fieldnames[:5]) + "</tr>"
            for row in data[:10]:
                table_html += "<tr>" + "".join(f"<td>{row[field]}</td>" for field in fieldnames[:5]) + "</tr>"
            table_html += "</table>"

            result_message = f"CSV export successful. Exported data for {len(data)} documents.\n\n" + table_html

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