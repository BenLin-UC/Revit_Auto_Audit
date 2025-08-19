import clr
import os
import csv
from lib.warning import collect_warning_data
from lib.basic import collect_basic_data
from lib.workset import collect_workset_data
from lib.view import collect_view_data
from lib.preview import show_audit_preview
from lib.ui import show_ui
from pyrevit import script

from __init__ import logger  # Import the logger from __init__.py

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

doc = __revit__.ActiveUIDocument.Document

def validate_user_inputs(user_inputs):
    """Validate user inputs before processing."""
    if user_inputs is None:
        logger.warning("User cancelled the input.")
        return False, "User cancelled the input."

    # Check if output directory is specified
    if not user_inputs.get('output_dir'):
        logger.error("Error: Output directory is required.")
        return False, "Error: Output directory is required."
    
    # Check if at least one audit type is enabled
    if not any([user_inputs.get('enable_basic'), user_inputs.get('enable_workset'), user_inputs.get('enable_view')]):
        logger.error("Error: At least one audit type must be enabled.")
        return False, "Error: At least one audit type must be enabled."
    
    # Validate basic audit inputs
    if user_inputs.get('enable_basic'):
        if not all([user_inputs.get('warning_file_name'), user_inputs.get('audit_file_name')]):
            logger.error("Error: Warning and audit file names are required for basic audit.")
            return False, "Error: Warning and audit file names are required for basic audit."
    
    # Validate workset audit inputs
    if user_inputs.get('enable_workset'):
        if not all([user_inputs.get('workset_file_name'), user_inputs.get('view_keyword')]):
            logger.error("Error: Workset file name and view keyword are required for workset audit.")
            return False, "Error: Workset file name and view keyword are required for workset audit."
    
    # Validate view audit inputs
    if user_inputs.get('enable_view'):
        if not all([user_inputs.get('view_file_name'), user_inputs.get('view_patterns')]):
            logger.error("Error: View file name and patterns are required for view audit.")
            return False, "Error: View file name and patterns are required for view audit."
    
    return True, "Validation successful"

def collect_audit_data(linked_docs, user_inputs):
    """Collect all audit data without exporting to files"""
    audit_results = {
        'warning_data': [],
        'basic_data': [],
        'workset_data': [],
        'view_data': []
    }
    
    try:
        # Collect basic audit data (warnings and model health)
        if user_inputs.get('enable_basic', False):
            logger.info("Collecting basic audit data...")
            
            # Collect warnings
            for doc_obj in linked_docs:
                if doc_obj:
                    try:
                        warnings = doc_obj.GetWarnings()
                        workset_table = doc_obj.GetWorksetTable() if doc_obj.IsWorkshared else None
                        
                        for warning in warnings:
                            description = warning.GetDescriptionText()
                            failing_elements = warning.GetFailingElements()
                            elements_detail = []
                            
                            for elem_id in failing_elements:
                                elem = doc_obj.GetElement(elem_id)
                                if elem:
                                    category = elem.Category.Name if elem.Category else "No Category"
                                    try:
                                        name = elem.Name
                                    except:
                                        name = elem.LookupParameter("Name").AsString() if elem.LookupParameter("Name") else "Not a Name"
                                        if not name:
                                            name = "Not a Name"
                                    
                                    workset_name = "No Workset"
                                    if workset_table:
                                        try:
                                            workset_id = elem.WorksetId
                                            workset = workset_table.GetWorkset(workset_id)
                                            workset_name = workset.Name if workset else "No Workset"
                                        except:
                                            pass
                                    
                                    elements_detail.append(f"{workset_name}: <{category}> {name}: [{elem_id}]")
                            
                            audit_results['warning_data'].append({
                                'Document Name': doc_obj.Title,
                                'Warning Descriptions': description,
                                'Related Elements': '; '.join(elements_detail)
                            })
                    except Exception as e:
                        logger.error(f"Error collecting warnings from {doc_obj.Title}: {str(e)}")
            
            # Collect basic model health data
            for doc_obj in linked_docs:
                if doc_obj:
                    try:
                        # Collect in-place families
                        collector = FilteredElementCollector(doc_obj).OfClass(FamilyInstance)
                        model_in_place_elements = [elem for elem in collector if elem.Symbol.Family.IsInPlace]
                        in_place_count = len(model_in_place_elements)
                        
                        # Collect other metrics
                        unused_elements_count = sum(
                            1 for elem in FilteredElementCollector(doc_obj).OfClass(Family)
                            if not FilteredElementCollector(doc_obj).OfClass(FamilyInstance).OfCategoryId(elem.FamilyCategory.Id).ToElements())
                        
                        detail_groups = len(
                            set(g.Name for g in FilteredElementCollector(doc_obj).OfClass(Group)
                                if g.GroupType.FamilyName == "Detail Group"))
                        
                        detail_group_instances = len(
                            [g for g in FilteredElementCollector(doc_obj).OfClass(Group)
                             if g.GroupType.FamilyName == "Detail Group"])
                        
                        audit_results['basic_data'].append({
                            'Document Name': doc_obj.Title,
                            'Purgeable Elements': unused_elements_count,
                            'Detail Groups': detail_groups,
                            'Detail Group Instances': detail_group_instances,
                            'In-Place Families': in_place_count
                        })
                    except Exception as e:
                        logger.error(f"Error collecting basic data from {doc_obj.Title}: {str(e)}")
        
        # Collect workset data
        if user_inputs.get('enable_workset', False):
            logger.info("Collecting workset audit data...")
            # Import the collection functions from workset module
            from lib.workset import get_3d_views_with_keyword, get_worksets_by_visibility_in_view, get_all_worksets_simple
            
            for doc_obj in linked_docs:
                if doc_obj and doc_obj.IsWorkshared:
                    try:
                        doc_name = doc_obj.Title
                        matching_views = get_3d_views_with_keyword(doc_obj, doc_name, user_inputs.get('view_keyword', 'Revizto'))
                        
                        if matching_views:
                            for view_info in matching_views:
                                try:
                                    view = doc_obj.GetElement(ElementId(view_info['view_id']))
                                    if view:
                                        visible, hidden = get_worksets_by_visibility_in_view(doc_obj, view, doc_name)
                                        
                                        for workset in visible + hidden:
                                            audit_results['workset_data'].append({
                                                'Document Name': workset['document'],
                                                'View Name': workset['view_name'],
                                                'View ID': workset['view_id'],
                                                'Workset Name': workset['workset_name'],
                                                'Workset ID': workset['workset_id'],
                                                'Visibility Setting': workset['visibility_setting'],
                                                'Actually Visible': workset['is_actually_visible'],
                                                'Is Open': workset['is_open'],
                                                'Owner': workset['owner']
                                            })
                                except Exception as e:
                                    logger.error(f"Error processing view {view_info['view_name']}: {str(e)}")
                        else:
                            # Fallback: collect all worksets
                            all_worksets = get_all_worksets_simple(doc_obj, doc_name)
                            for workset in all_worksets:
                                audit_results['workset_data'].append({
                                    'Document Name': workset['document'],
                                    'View Name': 'N/A (No matching views)',
                                    'View ID': 'N/A',
                                    'Workset Name': workset['workset_name'],
                                    'Workset ID': workset['workset_id'],
                                    'Visibility Setting': 'N/A',
                                    'Actually Visible': 'N/A',
                                    'Is Open': workset['is_open'],
                                    'Owner': workset['owner']
                                })
                    except Exception as e:
                        logger.error(f"Error collecting workset data from {doc_obj.Title}: {str(e)}")
        
        # Collect view data
        if user_inputs.get('enable_view', False):
            logger.info("Collecting view audit data...")
            # Import the collection functions from view module
            from lib.view import get_all_views_by_type, check_view_name_compliance, get_view_details
            
            for doc_obj in linked_docs:
                if doc_obj:
                    try:
                        doc_name = doc_obj.Title
                        all_views = get_all_views_by_type(doc_obj, user_inputs.get('view_types'))
                        
                        for view in all_views:
                            try:
                                view_details = get_view_details(view, doc_obj)
                                compliance = check_view_name_compliance(view.Name, user_inputs.get('view_patterns', []))
                                
                                audit_results['view_data'].append({
                                    'Document Name': doc_name,
                                    'View Name': view_details['name'],
                                    'View ID': view_details['id'],
                                    'View Type': view_details['view_type'],
                                    'Scale': view_details['scale'],
                                    'Is Compliant': compliance['is_compliant'],
                                    'Matched Patterns': '; '.join(compliance['matched_patterns']),
                                    'Failed Patterns': '; '.join(compliance['failed_patterns']),
                                    'Exclusion Violations': '; '.join(compliance['exclusion_violations']),
                                    'Detail Level': view_details['detail_level'],
                                    'Phase': view_details['phase'],
                                    'Is On Sheet': view_details['is_on_sheet'],
                                    'Sheet Count': view_details['sheet_count']
                                })
                            except Exception as e:
                                logger.error(f"Error processing view {view.Name}: {str(e)}")
                    except Exception as e:
                        logger.error(f"Error collecting view data from {doc_obj.Title}: {str(e)}")
        
    except Exception as e:
        logger.error(f"Error in data collection: {str(e)}")
    
    return audit_results

def export_audit_data(audit_results, user_inputs):
    """Export audit data to CSV files"""
    export_status = []
    
    try:
        # Export basic audit data
        if user_inputs.get('enable_basic', False) and (audit_results['warning_data'] or audit_results['basic_data']):
            warning_status = collect_warning_data([], user_inputs['output_dir'], user_inputs['warning_file_name'])
            basic_status = collect_basic_data([], user_inputs['output_dir'], user_inputs['audit_file_name'])
            
            # Since we're bypassing the original functions, write the data directly
            import csv
            
            # Export warning data
            if audit_results['warning_data']:
                warning_path = os.path.join(user_inputs['output_dir'], user_inputs['warning_file_name'])
                try:
                    with open(warning_path, 'w', newline='', encoding='utf-8') as csvfile:
                        fieldnames = ['Document Name', 'Warning Descriptions', 'Related Elements']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(audit_results['warning_data'])
                    export_status.append(f"[SUCCESS] Warning data exported: {len(audit_results['warning_data'])} entries")
                except Exception as e:
                    export_status.append(f"[ERROR] Warning export failed: {str(e)}")
            
            # Export basic audit data
            if audit_results['basic_data']:
                basic_path = os.path.join(user_inputs['output_dir'], user_inputs['audit_file_name'])
                try:
                    with open(basic_path, 'w', newline='', encoding='utf-8') as csvfile:
                        fieldnames = ['Document Name', 'Purgeable Elements', 'Detail Groups', 'Detail Group Instances', 'In-Place Families']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(audit_results['basic_data'])
                    export_status.append(f"[SUCCESS] Basic audit data exported: {len(audit_results['basic_data'])} entries")
                except Exception as e:
                    export_status.append(f"[ERROR] Basic audit export failed: {str(e)}")
        
        # Export workset data
        if user_inputs.get('enable_workset', False) and audit_results['workset_data']:
            workset_path = os.path.join(user_inputs['output_dir'], user_inputs['workset_file_name'])
            try:
                with open(workset_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Document Name', 'View Name', 'View ID', 'Workset Name', 'Workset ID', 
                                'Visibility Setting', 'Actually Visible', 'Is Open', 'Owner']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(audit_results['workset_data'])
                export_status.append(f"[SUCCESS] Workset data exported: {len(audit_results['workset_data'])} entries")
            except Exception as e:
                export_status.append(f"[ERROR] Workset export failed: {str(e)}")
        
        # Export view data
        if user_inputs.get('enable_view', False) and audit_results['view_data']:
            view_path = os.path.join(user_inputs['output_dir'], user_inputs['view_file_name'])
            try:
                with open(view_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Document Name', 'View Name', 'View ID', 'View Type', 'Scale', 
                                'Is Compliant', 'Matched Patterns', 'Failed Patterns', 'Exclusion Violations',
                                'Detail Level', 'Phase', 'Is On Sheet', 'Sheet Count']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(audit_results['view_data'])
                export_status.append(f"[SUCCESS] View data exported: {len(audit_results['view_data'])} entries")
            except Exception as e:
                export_status.append(f"[ERROR] View export failed: {str(e)}")
                
    except Exception as e:
        export_status.append(f"[ERROR] Export error: {str(e)}")
    
    return export_status

def validate_user_inputs(user_inputs):
    """Validate user inputs before processing."""
    if user_inputs is None:
        logger.warning("User cancelled the input.")
        return False, "User cancelled the input."

    # Check if output directory is specified
    if not user_inputs.get('output_dir'):
        logger.error("Error: Output directory is required.")
        return False, "Error: Output directory is required."
    
    # Check if at least one audit type is enabled
    if not any([user_inputs.get('enable_basic'), user_inputs.get('enable_workset'), user_inputs.get('enable_view')]):
        logger.error("Error: At least one audit type must be enabled.")
        return False, "Error: At least one audit type must be enabled."
    
    # Validate basic audit inputs
    if user_inputs.get('enable_basic'):
        if not all([user_inputs.get('warning_file_name'), user_inputs.get('audit_file_name')]):
            logger.error("Error: Warning and audit file names are required for basic audit.")
            return False, "Error: Warning and audit file names are required for basic audit."
    
    # Validate workset audit inputs
    if user_inputs.get('enable_workset'):
        if not all([user_inputs.get('workset_file_name'), user_inputs.get('view_keyword')]):
            logger.error("Error: Workset file name and view keyword are required for workset audit.")
            return False, "Error: Workset file name and view keyword are required for workset audit."
    
    # Validate view audit inputs
    if user_inputs.get('enable_view'):
        if not all([user_inputs.get('view_file_name'), user_inputs.get('view_patterns')]):
            logger.error("Error: View file name and patterns are required for view audit.")
            return False, "Error: View file name and patterns are required for view audit."
    
    return True, "Validation successful"

def gather_documents():
    """Safely gather main document and linked documents."""
    linked_docs = []
    
    # Add main document if available
    if doc:
        linked_docs.append(doc)
        logger.info(f"Added main document: {doc.Title}")
    else:
        logger.error("Error: No active document found.")
        return []

    # Gather linked documents
    try:
        link_instances = FilteredElementCollector(doc).OfClass(RevitLinkInstance)
        linked_count = 0
        
        for link in link_instances:
            linked_doc = link.GetLinkDocument()
            if linked_doc:  # Check if the linked document is loaded
                linked_docs.append(linked_doc)
                linked_count += 1
                logger.info(f"Added linked document: {linked_doc.Title}")
            else:
                logger.warning(f"Warning: Linked document could not be loaded: {link.Name}")
        
        logger.info(f"Total documents gathered: {len(linked_docs)} (1 main + {linked_count} linked)")
        
    except Exception as e:
        logger.error(f"Error gathering linked documents: {str(e)}")
    
    return linked_docs

def main():
    """Main execution function with enhanced preview and export workflow."""
    output = script.get_output()
    
    # Show extended UI
    user_inputs = show_ui()
    
    # Validate inputs
    is_valid, validation_message = validate_user_inputs(user_inputs)
    if not is_valid:
        output.print_html(f"<p style='color: red;'>{validation_message}</p>")
        return

    try:
        # Gather documents
        linked_docs = gather_documents()
        if not linked_docs:
            output.print_html("<p style='color: red;'>Error: No documents available for processing.</p>")
            return

        # Display initial processing info
        output.print_html("<h2>AutoAudit Processing</h2>")
        output.print_html(f"<p><strong>Documents to process:</strong> {len(linked_docs)}</p>")
        output.print_html(f"<p><strong>Output directory:</strong> {user_inputs['output_dir']}</p>")
        
        enabled_audits = []
        if user_inputs.get('enable_basic'): enabled_audits.append("Basic Audit")
        if user_inputs.get('enable_workset'): enabled_audits.append("Workset Audit")
        if user_inputs.get('enable_view'): enabled_audits.append("View Audit")
        
        output.print_html(f"<p><strong>Enabled audits:</strong> {', '.join(enabled_audits)}</p>")
        output.print_html("<p>Collecting audit data...</p>")

        # Collect all audit data
        audit_results = collect_audit_data(linked_docs, user_inputs)
        
        # Show data counts
        data_summary = []
        if audit_results['warning_data']: 
            data_summary.append(f"{len(audit_results['warning_data'])} warnings")
        if audit_results['basic_data']: 
            data_summary.append(f"{len(audit_results['basic_data'])} documents analyzed")
        if audit_results['workset_data']: 
            data_summary.append(f"{len(audit_results['workset_data'])} workset entries")
        if audit_results['view_data']: 
            data_summary.append(f"{len(audit_results['view_data'])} views analyzed")
        
        output.print_html(f"<p><strong>Data collected:</strong> {', '.join(data_summary)}</p>")
        output.print_html("<p>Opening preview window...</p>")
        
        # Show preview and get user confirmation
        user_wants_export = show_audit_preview(
            warning_data=audit_results['warning_data'],
            basic_data=audit_results['basic_data'],
            workset_data=audit_results['workset_data'],
            view_data=audit_results['view_data']
        )
        
        if user_wants_export:
            output.print_html("<p>Exporting data to CSV files...</p>")
            
            # Export data to CSV files
            export_status = export_audit_data(audit_results, user_inputs)
            
            # Show export results
            output.print_html("<h3>Export Results:</h3>")
            for status in export_status:
                if status.startswith("[SUCCESS]"):
                    output.print_html(f"<p style='color: green;'>{status}</p>")
                else:
                    output.print_html(f"<p style='color: red;'>{status}</p>")
            
            output.print_html("<hr>")
            output.print_html("<h3>Processing Complete!</h3>")
            output.print_html(f"<p>Check the output directory: <strong>{user_inputs['output_dir']}</strong></p>")
            
        else:
            output.print_html("<p>Export cancelled by user.</p>")
            output.print_html("<p>Data was collected successfully but not exported to files.</p>")
        
        logger.info("AutoAudit processing completed")

    except Exception as e:
        error_msg = f"Unexpected error during processing: {str(e)}"
        logger.error(error_msg)
        output.print_html(f"<p style='color: red;'>{error_msg}</p>")

if __name__ == "__main__":
    main()