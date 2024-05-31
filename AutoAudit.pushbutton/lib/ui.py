import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (Application, Form, FolderBrowserDialog, Label, Button, TextBox, DialogResult,
                                  FormBorderStyle, FormStartPosition, TableLayoutPanel, FlowLayoutPanel, GroupBox,
                                  AutoSizeMode, Padding)
from System.Drawing import Point, Size, Color

from __init__ import logger  # Import the logger from __init__.py

class SimpleForm(Form):
    def __init__(self):
        self.initialize_components()

    def initialize_components(self):
        # Set form properties
        self.Text = "AutoAudit"
        self.ClientSize = Size(250, 250)
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.StartPosition = FormStartPosition.CenterScreen
        self.BackColor = Color.LightGray

        # Create a TableLayoutPanel to organize the controls
        layout_panel = TableLayoutPanel()
        layout_panel.RowCount = 5
        layout_panel.ColumnCount = 2
        layout_panel.AutoSize = True
        layout_panel.AutoSizeMode = AutoSizeMode.GrowAndShrink

        # Folder picker button
        browse_folder_button = Button()
        browse_folder_button.Text = 'Browse Folder'  # Shorter text for smaller button
        browse_folder_button.AutoSize = False  # Disable AutoSize
        browse_folder_button.Size = Size(120, 30)  # Set the desired size
        browse_folder_button.Click += self.browse_folder_button_click
        layout_panel.Controls.Add(browse_folder_button, 0, 0)

        # Label to display selected folder path
        self.folder_path_label = Label()
        self.folder_path_label.AutoSize = True
        layout_panel.Controls.Add(self.folder_path_label, 0, 1)

        # Warning file name label and input
        warning_label = Label()
        warning_label.Text = "Warning File:"
        layout_panel.Controls.Add(warning_label, 0, 2)

        self.warning_input = TextBox()
        self.warning_input.Text = "warning_info.csv"
        self.warning_input.AutoSize = False  # Disable AutoSize
        self.warning_input.Size = Size(150, 20)  # Set the desired size
        self.warning_input.TextChanged += self.input_text_changed
        layout_panel.Controls.Add(self.warning_input, 0, 3)

        # Audit file name label and input
        audit_label = Label()
        audit_label.Text = "Audit File:"
        layout_panel.Controls.Add(audit_label, 0, 4)

        self.audit_input = TextBox()
        self.audit_input.Text = "audit_info.csv"
        self.audit_input.AutoSize = False  # Disable AutoSize
        self.audit_input.Size = Size(150, 20)  # Set the desired size
        self.audit_input.TextChanged += self.input_text_changed
        layout_panel.Controls.Add(self.audit_input, 0, 5)

        # Action buttons
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
        layout_panel.SetColumnSpan(button_panel, 7)  # Span the button panel across both columns

        # Add the layout panel to the form
        self.Controls.Add(layout_panel)

    def browse_folder_button_click(self, sender, args):
        dialog = FolderBrowserDialog()
        if dialog.ShowDialog() == DialogResult.OK:
            self.folder_path_label.Text = dialog.SelectedPath
            self.input_text_changed(None, None)

    def submit_button_click(self, sender, args):
        self.DialogResult = DialogResult.OK
        self.Close()

    def input_text_changed(self, sender, args):
        # Enable the submit button only if all fields are filled
        self.submit_button.Enabled = (self.folder_path_label.Text != "" and
                                      self.warning_input.Text.strip() != "" and
                                      self.audit_input.Text.strip() != "")
        logger.debug(f"Submit button enabled: {self.submit_button.Enabled}")

def show_ui():
    Application.EnableVisualStyles()
    form = SimpleForm()
    result = form.ShowDialog()

    if result == DialogResult.OK:
        user_inputs = {
            'output_dir': form.folder_path_label.Text,
            'warning_file_name': form.warning_input.Text,
            'audit_file_name': form.audit_input.Text
        }
        logger.debug(f"User inputs: {user_inputs}")
        return user_inputs
    else:
        logger.warning("User cancelled the input.")
        return None