# Revit Model Coordination Toolkit

A  suite of PyRevit extensions for auditing, analysing, and managing Revit project coordination across multiple disciplines.

## Overview

The Revit Model Coordination Toolkit provides a collection of specialised tools designed to help BIM teams maintain consistency, accuracy, and coordination in complex Revit projects. These tools address common challenges in multi-discipline environments where ensuring alignment between host and linked models is critical.

## Tools Included

### 1. Document Audit Tool

Analyses and compares critical positioning data across host and linked models:
- Grid positions and naming conventions
- Level elevations and names
- Survey and project base points
- True North angles

Perfect for identifying coordination issues before they cause problems in construction.

### 2. Parameters Export Tool

Extracts and analyses parameter values from multiple Revit documents:
- Multi-model support (host and linked models)
- Category filtering
- Flexible parameter selection
- Instance and type parameter extraction
- Data previewing and CSV export

Ideal for data analysis, compliance checking, and documentation.

## Installation

### Requirements
- Revit 2019 or newer
- PyRevit 4.7 or newer

### Installation Steps

1. Ensure you have [PyRevit](https://github.com/eirannejad/pyrevit) installed
2. Download or clone this repository
3. Place the contents in your PyRevit extensions folder:
   ```
   %appdata%\pyRevit\extensions\RevitCoordinationToolkit.extension\
   ```
4. Restart Revit or reload PyRevit
5. Find the tools in the PyRevit tab of your Revit ribbon

## Repository Structure

```
RevitCoordinationToolkit.extension/
├── README.md                        # This file
├── icon.png                         # Extension icon
├── DocumentAudit.pushbutton/        # Document Audit Tool
│   ├── icon.png                     # Tool icon
│   ├── README.md                    # Tool documentation
│   ├── document_audit_script.py     # Main script
│   └── lib/                         # Tool libraries
│       ├── __init__.py
│       ├── grid_analyzer.py
│       ├── level_analyzer.py
│       ├── survey_analyzer.py
│       └── ...
├── ParametersExport.pushbutton/     # Parameters Export Tool
│   ├── icon.png                     # Tool icon
│   ├── README.md                    # Tool documentation
│   ├── parameters_export_script.py  # Main script
│   ├── SimpleUI.xaml                # UI definition
│   └── lib/                         # Tool libraries
│       ├── __init__.py
│       ├── core_processing.py
│       ├── ui.py
│       └── ...
└── ...                              # Future tools
```

## Features

- **Multi-Model Analysis**: Work with both host and linked models simultaneously
- **Comprehensive Reporting**: Generate detailed reports in CSV format
- **Interactive Previews**: Review data before exporting
- **Robust Error Handling**: Detailed logging for troubleshooting
- **User-Friendly Interfaces**: Simple selection dialogs and progress tracking

## Dependencies

- Revit API
- PyRevit Framework
- IronPython 2.7 (included with PyRevit)

## Documentation

Each tool includes its own detailed README with specific usage instructions, data formats, and examples. See the individual tool directories for more information:

- [Document Audit Tool Documentation](./DocumentAudit.pushbutton/README.md)
- [Parameters Export Tool Documentation](./ParametersExport.pushbutton/README.md)

## Usage Tips

- Run these tools early in your coordination process to identify issues before they propagate
- Use the Document Audit Tool before starting work to ensure proper alignment
- Export parameters periodically to track changes and verify consistency
- Analyse exported data in Excel or other data analysis tools for deeper insights

## Contributing

Contributions to improve these tools are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please follow the existing code style and include proper error handling and logging.

## License

This project is distributed under the MIT License. See the LICENSE file for more information.

## Acknowledgments

- The PyRevit team for creating the framework that makes Revit extensions easier to develop
- Autodesk for providing the Revit API
- All contributors who have helped improve these tools

## Future Development

Planned future additions to the toolkit include:
- Model Health Checker
- Coordination Issue Tracker
- BIM Standards Validator
- Change Management Tool

Stay tuned for updates!
