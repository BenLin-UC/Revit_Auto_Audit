# Revit Document Coordination Tools

A comprehensive suite of PyRevit tools for auditing, comparing, and exporting data from Revit documents to ensure proper coordination and data management across projects.

## Description

This package includes two powerful tools designed to help BIM teams maintain consistency and accuracy in their Revit projects:

1. **Document Audit Tool**: Analyzes and compares critical positioning data (grids, levels, survey points) across host and linked models to identify coordination issues.

2. **Parameters Export Tool**: Extracts parameter values from multiple Revit documents and categories, allowing for comprehensive data analysis and coordination.

## Installation Instructions

These tools are designed as PyRevit extensions. To install:

1. Ensure you have [PyRevit](https://github.com/eirannejad/pyrevit) installed (version 4.7 or higher recommended)
2. Download or clone this repository
3. Place the contents in your PyRevit extensions folder:
   ```
   %appdata%\CustomRevitExtension\Preformance.extension\Preformance.tab\Audit.panel\ParametersExport.pushbutton
   ```
4. Organize files as follows:
   ```
   RevitCoordinationTools.extension/
   ├── DocumentAudit.pushbutton/
   │   ├── lib/
   │   │   ├── __init__.py
   │   │   ├── grid_analyzer.py
   │   │   ├── level_analyzer.py
   │   │   ├── link_analyzer.py
   │   │   ├── logger.py
   │   │   ├── survey_analyzer.py
   │   │   ├── ui.py
   │   │   └── unit_utils.py
   │   └── document_audit_script.py
   ├── ParametersExport.pushbutton/
   │   ├── lib/
   │   │   ├── __init__.py
   │   │   ├── core_processing.py
   │   │   ├── logger.py
   │   │   ├── ui.py
   │   │   └── warning.py
   │   ├── parameters_export_script.py
   │   └── SimpleUI.xaml
   └── icon.png
   ```
5. Restart Revit or reload PyRevit

## Usage

### Document Audit Tool

1. Open your Revit project
2. Run the Document Audit Tool from the PyRevit tab
3. Review the preview showing grid, level, and survey point data
4. If the data looks correct, click "Yes" to export to CSV
5. Select a directory for the output file
6. The tool will generate a comprehensive CSV report named `document_audit_data.csv`

### Parameters Export Tool

1. Open your Revit project
2. Run the Parameters Export Tool from the PyRevit tab
3. Select models to analyze (current and/or linked models)
4. Choose categories to extract data from (Walls, Doors, Windows, etc.)
5. Select specific parameters to export
6. Review the data preview
7. Click "Yes" to export to CSV files (one per document)
8. Choose the export directory

## Features

### Document Audit Tool

- **Comprehensive Analysis**: Analyzes grids, levels, survey points, and project base points across host and linked models
- **Coordinate Transformation**: Properly transforms coordinates from linked models to the host model for accurate comparison
- **Interactive Preview**: View data in formatted tables before exporting
- **Unit Conversion**: Automatically converts Revit's internal units (feet) to millimeters for standardized reporting
- **Error Handling**: Robust error handling with detailed logging

### Parameters Export Tool

- **Multi-Model Support**: Extract data from both host and linked models
- **Category Filtering**: Target specific element categories
- **Parameter Selection**: Choose which parameters to extract
- **Instance & Type Parameters**: Export both instance and type parameter values
- **Data Preview**: Review extracted data before exporting
- **CSV Export**: Generate organized CSV files for further analysis

## Dependencies

- Revit 2019 or newer
- PyRevit 4.7 or newer
- IronPython 2.7 (included with PyRevit)

## Configuration

Both tools work out of the box without additional configuration. Logs are stored in the following locations:

- Document Audit Tool: `logs/document_audit.log` within the extension folder
- Parameters Export Tool: `%appdata%\CustomRevitExtension\Preformance.extension\Preformance.tab\Audit.panel\ParametersExport.pushbutton\logs\ParametersExport.log`

## Data Format

### Document Audit Tool

- **Grid Data**: `GridName: x1,y1,z1---x2,y2,z2` (coordinates in mm)
- **Level Data**: `LevelName: Elevation` (elevation in mm)
- **Survey Points**: `(x,y,z)` (coordinates in mm)
- **True North**: Angle in degrees

### Parameters Export Tool

- CSV files contain both instance and type parameters
- Headers include: GUID, ElementId, Family and Type, and all selected parameters
- Values are displayed in their native format with units where applicable

## Contributing Guidelines

Contributions to improve these tools are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes proper error handling and logging.

## License

This project is distributed under the MIT License. See the LICENSE file for more information.    

## Documentation

For more detailed documentation on:
- PyRevit: [PyRevit Documentation](https://www.notion.so/pyRevit-bd907d6292ed4ce997c46e84b6ef67a0)
- Revit API: [Revit API Documentation](https://www.revitapidocs.com/)

## Acknowledgments

- The PyRevit team for creating the framework that makes Revit extensions easier to develop
- Autodesk for providing the Revit API
- All contributors who have helped improve these tools
