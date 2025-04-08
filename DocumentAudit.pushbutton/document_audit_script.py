"""Document Audit Script - Main execution script"""

import clr
import os
import csv
import re

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

from lib import (
    GridAnalyzer,
    LevelAnalyzer,
    SurveyAnalyzer,
    logger
)
from lib.ui import show_dialog, show_data_preview
from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document

def sanitize_filename(filename):
    """Sanitize filename for Windows compatibility"""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return filename.strip('. ')

def combine_data_for_csv(grid_data, level_data, survey_data):
    """Combine all data into a single structured format"""
    combined_data = []
    
    # Process host document
    if grid_data and 'host_doc' in grid_data:
        host_doc = grid_data['host_doc']
        host_name = host_doc['name']
        
        # Find corresponding level and survey data
        host_levels = next((data for data in level_data if data['Document Name'] == host_name), None)
        host_survey = next((data for data in survey_data if data['Document Name'] == host_name), None)
        
        combined_data.append({
            'Document Type': 'Host',
            'Document Name': host_name,
            'True North': host_doc.get('true_north', 'No Data'),
            'Grid Data': host_doc.get('grid_data', 'No Data'),
            'Level Data': host_levels['Level Data'] if host_levels else 'No Data',
            'Survey Point': host_survey['Survey Coordinate'] if host_survey else 'No Data',
            'Project Base Point': host_survey['Project Base Coordinate'] if host_survey else 'No Data',
        })
    
    # Process linked documents
    if grid_data and 'linked_docs' in grid_data:
        for doc_name, link_data in grid_data['linked_docs'].items():
            # Find corresponding level and survey data
            link_levels = next((data for data in level_data if data['Document Name'] == doc_name), None)
            link_survey = next((data for data in survey_data if data['Document Name'] == doc_name), None)
            
            combined_data.append({
                'Document Type': 'Linked',
                'Document Name': doc_name,
                'True North': link_data.get('true_north', 'No Data'),
                'Grid Data': link_data.get('grid_data', 'No Data'),
                'Level Data': link_levels['Level Data'] if link_levels else 'No Data',
                'Survey Point': link_survey['Survey Coordinate'] if link_survey else 'No Data',
                'Project Base Point': link_survey['Project Base Coordinate'] if link_survey else 'No Data',
            })
    
    return combined_data

def write_csv_data(data, filepath):
    """Write data to CSV file"""
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            csvfile.write('\ufeff')  # UTF-8 BOM for Excel
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        logger.error(f"Error writing CSV file {filepath}: {str(e)}")
        return False

def process_document():
    """Process the active document and its linked documents"""
    try:
        # Initialize analyzers
        grid_analyzer = GridAnalyzer(doc)
        level_analyzer = LevelAnalyzer(doc)
        survey_analyzer = SurveyAnalyzer(doc)

        # Collect data
        grid_data = grid_analyzer.collect_all_grid_data()
        level_data = level_analyzer.collect_all_level_data()
        survey_data = survey_analyzer.collect_all_survey_data()

        # Format data for preview
        grid_csv_data = grid_analyzer.format_for_csv(grid_data)
        level_csv_data = level_analyzer.format_for_csv(level_data)
        survey_csv_data = survey_analyzer.format_for_csv(survey_data)

        # Show preview
        preview_result = show_data_preview(grid_csv_data, level_csv_data, survey_csv_data)
        if not preview_result:
            logger.info("Operation cancelled after preview")
            return False

        # Show UI and get user inputs
        user_inputs = show_dialog()
        if not user_inputs:
            logger.info("Operation cancelled by user")
            return False

        # Create output directory if it doesn't exist
        output_dir = user_inputs['output_dir']
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Combine and write data
        combined_data = combine_data_for_csv(grid_data, level_csv_data, survey_csv_data)
        combined_path = os.path.join(output_dir, 'document_audit_data.csv')
        
        if write_csv_data(combined_data, combined_path):
            forms.alert(
                'Document audit completed successfully.',
                title='Success',
                sub_msg='Data has been exported to the selected directory.'
            )
            logger.info("Document audit completed successfully")
            return True
        else:
            forms.alert(
                'Failed to export audit data.',
                title='Error',
                sub_msg='Check the log file for details.'
            )
            logger.error("Failed to export audit data")
            return False

    except Exception as e:
        logger.error(f"Error in document audit: {str(e)}")
        forms.alert(
            'An error occurred during document audit.',
            title='Error',
            sub_msg=str(e)
        )
        return False

if __name__ == '__main__':
    process_document()