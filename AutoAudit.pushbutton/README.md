# Revit AutoAudit Tool

A first generation Revit model auditing tool developed by Preformance that analyses both the active document and linked models, collecting warnings and model health metrics to help identify potential issues and improve model performance.

## Description

The Revit AutoAudit Tool automatically collects and exports critical data about your Revit models, including warnings, in-place families, detail groups, non-standard categories, and more. This extension helps BIM managers, Revit power users, and project teams:

- Identify and track Revit warnings across host and linked models
- Detect performance-impacting elements such as in-place families and excessive detail groups
- Spot potential coordination issues like hidden views on sheets
- Generate standardised reports for project health assessments

## Installation Instructions

This tool is designed as a PyRevit extension. To install:

1. Ensure you have [PyRevit](https://github.com/eirannejad/pyrevit) installed (version 4.7 or higher recommended)
2. Download or clone this repository
3. Place the contents in your PyRevit extensions folder:
   ```
   %appdata%\pyRevit\extensions\Preformance.extension\Preformance.tab\Audit.panel\AutoAudit.pushbutton\
   ```
4. Organize files as follows:
   ```
   AutoAudit.pushbutton/
   ├── __init__.py
   ├── auto_audit_script.py 
   └── lib/
       ├── __init__.py
       ├── basic.py
       ├── ui.py
       └── warning.py
   ```
5. Restart Revit or reload PyRevit

## Usage

1. Open your Revit project 
2. From the Preformance tab, navigate to the Audit panel and click AutoAudit
3. In the dialog that appears:
   - Click "Browse Folder" to select an output directory
   - Verify or modify the default filenames ("warning_info.csv" and "audit_info.csv")
   - Click "Submit" to run the audit
4. Review the generated reports in your selected output folder

## Features

- **Warning Analysis**: Collects all warnings from host and linked models with detailed information on related elements
- **Model Health Metrics**:
  - Counts purgeable/unused elements
  - Identifies detail groups and instances
  - Measures in-place family usage
  - Counts non-standard categories
  - Detects hidden views on sheets
- **Multi-Document Support**: Analyzes both host and linked models in a single operation
- **Workset Tracking**: Includes workset information for enhanced troubleshooting
- **CSV Export**: Generates standardized reports for documentation and tracking
- **Visual Preview**: Shows highlights of the audit results directly in the PyRevit interface

## Dependencies

- Revit 2019 or newer
- PyRevit 4.7 or newer
- .NET Framework 4.5+

## Configuration

Logs are automatically stored in:
```
%appdata%\CustomRevitExtension\Preformance.extension\Preformance.tab\Audit.panel\AutoAudit.pushbutton\AutoAudit.log
```

Log files rotate when they reach 1MB, with up to 5 backup files maintained.

## Data Format

The tool generates two CSV files:

### warning_info.csv
- Document Title
- Document Type (Host/Linked)
- Warning Descriptions 
- Related Elements (with Workset, Category, Name, and ID information)

### audit_info.csv
- Document Title
- Document Type (Host/Linked)
- Purgeable Elements Count
- Detail Groups Count
- Detail Group Instances Count
- In-Place Families Count
- Non-Builtin Categories Count
- Hidden Views on Sheets Count
- View Names & Sheet Names

## Contributing Guidelines

Contributions to improve the Revit AutoAudit Tool are welcome:

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

## Contact Information

For questions, feature requests, or bug reports:
- Create an issue on the repository
- Contact the maintainer at: [your-email@example.com]

## Acknowledgments

- The PyRevit team for creating the framework that makes Revit extensions easier to develop
- Autodesk for providing the Revit API
- All contributors who have helped improve this tool
