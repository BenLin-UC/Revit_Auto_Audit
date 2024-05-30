import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (Application, Form, FolderBrowserDialog, Label, Button, TextBox, DialogResult,
                                  FormBorderStyle, FormStartPosition)
from System.Drawing import Point, Size

class SimpleForm(Form):
    def __init__(self):
        self.initialize_components()

    def initialize_components(self):
        self.Text = "Test UI Form"
        self.ClientSize = Size(280, 240)
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.StartPosition = FormStartPosition.CenterScreen

        # Folder picker button
        self.folderButton = Button()
        self.folderButton.Text = 'Pick Folder'
        self.folderButton.Location = Point(10, 10)
        self.folderButton.Click += self.folder_button_click
        self.Controls.Add(self.folderButton)

        # Label to display selected folder path
        self.folderPathLabel = Label()
        self.folderPathLabel.Location = Point(10, 40)
        self.folderPathLabel.Size = Size(260, 40)
        self.Controls.Add(self.folderPathLabel)

        # Entry for the warning file name
        self.warning_label = Label()
        self.warning_label.Text = "Enter warning file name:"
        self.warning_label.Location = Point(10, 90)
        self.warning_label.AutoSize = True
        self.Controls.Add(self.warning_label)

        self.warningInput = TextBox()
        self.warningInput.Text = "warning_info.csv"
        self.warningInput.Location = Point(10, 110)
        self.warningInput.Width = 260
        self.warningInput.TextChanged += self.input_text_changed
        self.Controls.Add(self.warningInput)

        # Entry for the basic file name
        self.basic_label = Label()
        self.basic_label.Text = "Enter audit info file name:"
        self.basic_label.Location = Point(10, 140)
        self.basic_label.AutoSize = True
        self.Controls.Add(self.basic_label)

        self.basicInput = TextBox()
        self.basicInput.Text = "audit_info.csv"
        self.basicInput.Location = Point(10, 160)
        self.basicInput.Width = 260
        self.basicInput.TextChanged += self.input_text_changed
        self.Controls.Add(self.basicInput)

        # Submit button
        self.submitButton = Button()
        self.submitButton.Text = 'Submit'
        self.submitButton.Location = Point(10, 190)
        self.submitButton.Enabled = False  # Initially disabled
        self.submitButton.Click += self.submit_button_click
        self.Controls.Add(self.submitButton)

        # Cancel button
        self.cancelButton = Button()
        self.cancelButton.Text = 'Cancel'
        self.cancelButton.Location = Point(180, 190)
        self.cancelButton.Click += lambda sender, args: self.Close()
        self.Controls.Add(self.cancelButton)

    def folder_button_click(self, sender, args):
        dialog = FolderBrowserDialog()
        if dialog.ShowDialog() == DialogResult.OK:
            self.folderPathLabel.Text = dialog.SelectedPath
            self.input_text_changed(None, None)

    def submit_button_click(self, sender, args):
        self.DialogResult = DialogResult.OK
        self.Close()

    def input_text_changed(self, sender, args):
        # Enable the submit button only if all fields are filled
        self.submitButton.Enabled = (self.folderPathLabel.Text != "" and
                                     self.warningInput.Text.strip() != "" and
                                     self.basicInput.Text.strip() != "")
        
    def CancelButton_Click(self, sender, event):
        self.DialogResult = DialogResult.Cancel
        self.Close()

def show_ui():
    Application.EnableVisualStyles()
    form = SimpleForm()
    result = form.ShowDialog()

    if result == DialogResult.OK:
        return {
            'output_dir': form.folderPathLabel.Text,
            'warning_file_name': form.warningInput.Text,
            'basic_file_name': form.basicInput.Text
        }
    return None