"""
__title__ = "AutoAudit"
__doc__ = """Version = 1.1
Date    = 06.06.2024
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to:
-> Click on the button
-> Change Settings(optional)
-> Make a change
_____________________________________________________________________
Last update:
- [24.04.2024] - 1.0 RELEASE
- [06.06.2024] - 1.1 UPDATE - ANNOTATION
_____________________________________________________________________
Author: Ben Lin - Preformance
"""

__author__ = "Preformance"
__min_revit_ver__ = 2021
__max_revit_ver = 2023
"""

import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (Application, Form, FolderBrowserDialog, Label, Button, TextBox, DialogResult,
                                  FormBorderStyle, FormStartPosition, TableLayoutPanel, FlowLayoutPanel, Padding)
from System.Drawing import Point, Size, Color
from __init__ import logger  # Import the logger from __init__.py


class SimpleForm(Form):
    def __init__(self):
        """Initialize the form components."""
        self.initialize_components()

    def initialize_components(self):
        """Set up the UI components for the form."""
        self.Text = "AutoAudit"
        self.ClientSize = Size(250, 250)
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.StartPosition = FormStartPosition.CenterScreen
        self.BackColor = Color.LightGray

        layout_panel = TableLayoutPanel()
        layout_panel.RowCount = 5
        layout_panel.ColumnCount = 2
        layout_panel.AutoSize = True
        layout_panel.AutoSizeMode = AutoSizeMode.GrowAndShrink

        browse_folder_button = Button()
        browse_folder_button.Text = 'Browse Folder'
        browse_folder_button.AutoSize = False
        browse_folder_button.Size = Size(120, 30)
        browse_folder_button.Click += self.browse_folder_button_click
        layout_panel.Controls.Add(browse_folder_button, 0, 0)

        self.folder_path_label = Label()
        self.folder_path_label.AutoSize = True
        layout_panel.Controls.Add(self.folder_path_label, 0, 1)

        warning_label = Label()
        warning_label.Text = "Warning File:"
        layout_panel.Controls.Add(warning_label, 0, 2)

        self.warning_input = TextBox()
        self.warning_input.Text = "warning_info.csv"
        self.warning_input.AutoSize = False
        self.warning_input.Size = Size(150, 20)
        self.warning_input.TextChanged += self.input_text_changed
        layout_panel.Controls.Add(self.warning_input, 0, 3)

        audit_label = Label()
        audit_label.Text = "Audit File:"
        layout_panel.Controls.Add(audit_label, 0, 4)

        self.audit_input = TextBox()
        self.audit_input.Text = "audit_info.csv"
        self.audit_input.AutoSize = False
        self.audit_input.Size = Size(150, 20)
        self.audit_input.TextChanged += self.input_text_changed
        layout_panel.Controls.Add(self.audit_input, 0, 5)

        button_panel = FlowLayoutPanel()
        button_panel.Padding = Padding(5)

        self.submit_button = Button()
        self.submit_button.Text = 'Submit'
        self.submit_button.Enabled = False
        self.submit_button.Click += self.submit_button_click
        button_panel.Controls.Add(self.submit_button)

        cancel_button = Button()
        cancel_button.Text = 'Cancel'
        cancel_button.Click += lambda sender, args: self.Close()
        button_panel.Controls.Add(cancel_button)

        layout_panel.Controls.Add(button_panel, 0, 7)
        layout_panel.SetColumnSpan(button_panel, 7)

        self.Controls.Add(layout_panel)

    def browse_folder_button_click(self, sender, args):
        """Handle the event when the browse folder button is clicked."""
        dialog = FolderBrowserDialog()
        if dialog.ShowDialog() == DialogResult.OK:
            self.folder_path_label.Text = dialog.SelectedPath
            self.input_text_changed(None, None)

    def submit_button_click(self, sender, args):
        """Handle the event when the submit button is clicked."""
        self.DialogResult = DialogResult.OK
        self.Close()

    def input_text_changed(self, sender, args):
        """Enable the submit button only if all fields are filled."""
        self.submit_button.Enabled = (self.folder_path_label.Text != "" and
                                      self.warning_input.Text.strip() != "" and
                                      self.audit_input.Text.strip() != "")
        logger.debug(f"Submit button enabled: