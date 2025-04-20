# Revit Document Audit Tool

A lite version tool for auditing and comparing Revit documents, analysing grids, levels, and survey points across host and linked models to ensure coordination and identify discrepancies.

## Description

The Revit Document Audit Tool extracts and compares critical positioning data across multiple Revit files, helping teams identify coordination issues between linked models. It analyses:

- Grid positions and naming conventions
- Level elevations and names
- Survey and project base points
- True North angles

The tool generates comprehensive reports to help ensure all linked models properly align in 3D space, preventing costly errors during construction.

## Installation Instructions

This tool is designed as a PyRevit extension. To install:

1. Ensure you have [PyRevit](https://github.com/eirannejad/pyrevit) installed (version 4.7 or higher recommended)
2. Download or clone this repository
3. Place the contents in your PyRevit extensions folder:
   ```
   %appdata%\CustomRevitExtension\Preformance.extension\Preformance.tab\Audit.panel
   ```
4. Organize files as follows:
   ```
   RevitDocumentAudit.extension/
   ├── lib/
   │   ├── __init__.py
   │   ├── audit_processor.py
   │   ├── grid_analyzer.py
   │   ├── level_analyzer.py
   │   ├── link_analyzer.py
   │   ├── logger.py
   │   ├── survey_analyzer.py
   │   ├── ui.py
   │   └── unit_utils.py
   └── script.py
   ```
5. Restart Revit or reload PyRevit

## Usage

1. Open your Revit project
2. Run the Document Audit Tool from the PyRevit tab
3. Review the preview showing grid, level, and survey point data
4. If the data looks correct, click "Yes" to export to CSV
5. Select a directory for the output file
6. The tool will generate a comprehensive CSV report named `document_audit_data.csv`

## Features

- **Comprehensive Analysis**: Analyzes grids, levels, survey points, and project base points across host and linked models
- **Coordinate Transformation**: Properly transforms coordinates from linked models to the host model for accurate comparison
- **Interactive Preview**: View data in formatted tables before exporting
- **Unit Conversion**: Automatically converts Revit's internal units (feet) to millimeters for standardized reporting
- **Error Handling**: Robust error handling with detailed logging
- **CSV Export**: Exports all data to a structured CSV file for further analysis

## Dependencies

- Revit 2019 or newer
- PyRevit 4.7 or newer
- IronPython 2.7 (included with PyRevit)

## Configuration

The tool works out of the box without additional configuration. If needed, logs are stored in the `logs` directory within the extension folder, with rotating log files of up to 5MB.

## Data Format

The tool exports data in the following format:

- **Grid Data**: `GridName: x1,y1,z1---x2,y2,z2` (coordinates in mm)
- **Level Data**: `LevelName: Elevation` (elevation in mm)
- **Survey Points**: `(x,y,z)` (coordinates in mm)
- **True North**: Angle in degrees

## Contributing Guidelines

Contributions to improve the Revit Document Audit Tool are welcome:

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
- All contributors who have helped improve this tool
