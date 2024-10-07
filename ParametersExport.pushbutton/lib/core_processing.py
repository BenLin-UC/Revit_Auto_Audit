import clr, os, csv, re
from pyrevit import forms

clr.AddReference('RevitAPI')
clr.AddReference('System.Windows.Forms')
from Autodesk.Revit.DB import FilteredElementCollector, RevitLinkInstance, CategoryType, BuiltInCategory
from System.Windows.Forms import FolderBrowserDialog, DialogResult

def get_documents(doc):
    """
    Retrieve the current document and linked documents.
    
    Args:
        doc: The current Revit document.
        
    Returns:
        list: A list containing the current document and linked RevitLinkInstances documents.
    """
    linked_docs = []
    linked_instances = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
    linked_docs.append(doc)
    for link_instance in linked_instances:
        linked_docs.append(link_instance.GetLinkDocument())
    return linked_docs

def get_model_categories(documents):
    """
    Retrieve all categories of type Model from the given documents.
    
    Args:
        documents (list): A list of Revit documents.
        
    Returns:
        dict: A dictionary mapping category names to (document, Category) tuples.
    """
    desired_categories = {
    "Air Systems",
    "Air Terminals",
    "Bearings",
    "Bridge Cables",
    "Bridge Decks",
    "Bridge Framing",
    "Cable Tray Fittings",
    "Cable Tray Runs",
    "Cable Trays",
    "Casework",
    "Ceilings",
    "Columns",
    "Communication Devices",
    "Conduit Fittings",
    "Conduit Runs",
    "Conduits",
    "Coordination Model",
    "Curtain Grids",
    "Curtain Panels",
    "Curtain Wall Mullions",
    "Data Devices",
    "Doors",
    "Duct Accessories",
    "Duct Fittings",
    "Duct Insulations",
    "Duct Linings",
    "Duct Placeholders",
    "Ducts",
    "Electrical Circuits",
    "Electrical Equipment",
    "Electrical Fixtures",
    "Electrical Spare/Space Circuits",
    "Entourage",
    "Fire Alarm Devices",
    "Flex Ducts",
    "Flex Pipes",
    "Floors",
    "Furniture",
    "Furniture Systems",
    "Generic Models",
    "HVAC Zones",
    "Lighting Devices",
    "Lighting Fixtures",
    "MEP Fabrication Containment",
    "MEP Fabrication Ductwork",
    "MEP Fabrication Hangers",
    "MEP Fabrication Pipework",
    "Mechanical Equipment",
    "Nurse Call Devices",
    "Parking",
    "Piers",
    "Pipe Accessories",
    "Pipe Fittings",
    "Pipe Insulations",
    "Pipe Placeholders",
    "Pipe Segments",
    "Pipes",
    "Piping Systems",
    "Planting",
    "Plumbing Fixtures",
    "Railings",
    "Ramps",
    "Roads",
    "Roofs",
    "Rooms",
    "Routing Preferences",
    "Security Devices",
    "Shaft Openings",
    "Site",
    "Spaces",
    "Specialty Equipment",
    "Sprinklers",
    "Stairs",
    "Structural Area Reinforcement",
    "Structural Beam Systems",
    "Structural Columns",
    "Structural Connections",
    "Structural Fabric Areas",
    "Structural Fabric Reinforcement",
    "Structural Foundations",
    "Structural Framing",
    "Structural Path Reinforcement",
    "Structural Rebar",
    "Structural Rebar Couplers",
    "Structural Stiffeners",
    "Structural Tendons",
    "Structural Trusses",
    "Switch System",
    "Telephone Devices",
    "Topography",
    "Vibration Management",
    "Walls",
    "Water Loops",
    "Windows"
    }
    categories = {}
    for doc in documents:
        for category in doc.Settings.Categories:
            if category.CategoryType == CategoryType.Model and category.Name in desired_categories:
                if category.Name not in categories:
                    categories[category.Name] = []
                categories[category.Name].append((doc, category))
    return categories

def get_category_parameters(doc, category):
    """
    Retrieve all parameters from elements in the specified category.
    
    Args:
        doc: The Revit document.
        category: The Category object.

    Returns:
        set: A set of parameter names found within the elements of the specified category.
    """
    parameters = set()
    collector = FilteredElementCollector(doc).OfCategoryId(category.Id)
    elements = collector.ToElements()
    for elem in elements:
        for param in elem.Parameters:
            parameters.add(param.Definition.Name)
    return parameters

#    try:
#        category = doc.Settings.Categories.get_Item(category_name)
#        if category:
#            collector = FilteredElementCollector(doc).OfCategoryId(category.Id)
#            elements = collector.ToElements()
#            for elem in elements:
#                for param in elem.Parameters:
#                    parameters.add(param.Definition.Name)
#            return parameters
#    except:
#        if category_name=="Structural Trusses":
#            collector = FilteredElementCollector(doc).OfCategoryId(category.Id)
#            elements = collector.ToElements()
#            for elem in elements:
#                for param in elem.Parameters:
#                    parameters.add(param.Definition.Name)
#            return parameters

def get_parameter_values(doc, category, parameter_names, data_by_document):
    """
    Retrieve the values of specified parameters for elements in the given category.
    
    Args:
        doc: The Revit document.
        category_name: The name of the category to filter elements by.
        parameter_names (list): A list of parameter names to retrieve values for.
        
    Returns:
        list: A list of dictionaries containing element IDs and parameter values.
    """
    collector = FilteredElementCollector(doc).OfCategoryId(category.Id)
    elements = collector.ToElements()
    for elem in elements:
        if elem.LookupParameter('Family and Type') is not None:
            element_data = {
                "GUID": elem.UniqueId,
                "ElementId": elem.Id.IntegerValue
            }
            for param_name in parameter_names:
                param_value = next((param.AsValueString() for param in elem.Parameters if param.Definition.Name == param_name), "N/A")
                element_data[param_name] = param_value
            data_by_document[doc.Title].append(element_data)

def export_data_to_csv(data_by_document, selected_parameters):
    """
    Exports the data for each document into a CSV file, using the document title as the filename.
    
    Args:
        data_by_document (dict): The dictionary containing all documents' data.
        selected_parameters (list): The list of selected parameters.
    """
    # Open a directory selection dialog
    dialog = FolderBrowserDialog()
    dialog.Description = "Select the folder where CSV files will be saved."
    
    if dialog.ShowDialog() == DialogResult.OK:
        selected_directory = dialog.SelectedPath
        
        # Iterate over each document's data and export to CSV
        for doc_title, data in data_by_document.items():
            # Generate a sanitized filename
            sanitized_title = sanitise_filename(doc_title)
            csv_filename = os.path.join(selected_directory, f"{sanitized_title}.csv")
            
            # Write data to CSV
            try:
                with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=['GUID', 'ElementId'] + selected_parameters)
                    writer.writeheader()
                    writer.writerows(data)
                forms.alert(f"Data for {doc_title} exported successfully!", title='Export Complete')
            except Exception as e:
                forms.alert(f"Failed to export data for {doc_title}: {e}", title='Export Error')

def sanitise_filename(filename):
    """
    Sanitizes a string to make it safe to use as a filename.
    
    Args:
        filename (str): The filename to sanitize.
        
    Returns:
        str: The sanitized filename.
    """
    # Replace any character that is not alphanumeric, a space, or a period
    sanitized = re.sub(r'[^a-zA-Z0-9\s\._-]', '_', filename)
    return sanitized.strip()

def generate_table_html(data, selected_parameters, max_rows=10):
    """
    Generate an HTML table preview of the data with an Export button.
    
    Args:
        data (list): The data to be displayed.
        selected_parameters (list): The list of selected parameters.
        
    Returns:
        str: The generated HTML content.
    """
    fieldnames = ['ElementId'] + selected_parameters
    table_html = "<table border='1'>"
    table_html += "<tr>" + "".join(f"<th>{header}</th>" for header in fieldnames) + "</tr>"

    for row in data[:max_rows]:
        table_html += "<tr>" + "".join(f"<td>{row.get(field, 'N/A')}</td>" for field in fieldnames) + "</tr>"

    table_html += "</table>"

    return table_html

def sanitise_filename(filename):
    """
    Sanitizes a string to make it safe to use as a filename.
    
    Args:
        filename (str): The filename to sanitize.
        
    Returns:
        str: The sanitized filename.
    """
    # Replace any character that is not alphanumeric, a space, or a period
    sanitized = re.sub(r'[^a-zA-Z0-9\s\._-]', '_', filename)
    return sanitized.strip()