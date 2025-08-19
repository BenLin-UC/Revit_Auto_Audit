import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (Application, Form, FolderBrowserDialog, Label, Button, TextBox, DialogResult,
                                  FormBorderStyle, FormStartPosition, TableLayoutPanel, FlowLayoutPanel, 
                                  Padding, CheckBox, GroupBox, ComboBox, ComboBoxStyle, AutoSizeMode, DockStyle, 
                                  ScrollBars, FlowDirection)
from System.Drawing import Point, Size, Color, Font
from __init__ import logger


class ExtendedAuditForm(Form):
    def __init__(self):
        """Initialize the extended form components."""
        self.initialize_components()

    def initialize_components(self):
        """Set up the UI components for the extended form."""
        self.Text = "AutoAudit - Extended"
        self.ClientSize = Size(400, 700)
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.StartPosition = FormStartPosition.CenterScreen
        self.BackColor = Color.LightGray

        # Main layout panel
        main_layout = TableLayoutPanel()
        main_layout.RowCount = 6
        main_layout.ColumnCount = 1
        main_layout.AutoSize = True
        main_layout.AutoSizeMode = AutoSizeMode.GrowAndShrink
        main_layout.Dock = DockStyle.Fill

        # Output folder section
        folder_group = self.create_folder_section()
        main_layout.Controls.Add(folder_group, 0, 0)

        # Basic audit section
        basic_group = self.create_basic_audit_section()
        main_layout.Controls.Add(basic_group, 0, 1)

        # Workset audit section
        workset_group = self.create_workset_section()
        main_layout.Controls.Add(workset_group, 0, 2)

        # View audit section
        view_group = self.create_view_section()
        main_layout.Controls.Add(view_group, 0, 3)

        # Buttons section
        button_panel = self.create_button_section()
        main_layout.Controls.Add(button_panel, 0, 4)

        self.Controls.Add(main_layout)
        self.update_submit_button_state()

    def create_folder_section(self):
        """Create the output folder selection section."""
        group = GroupBox()
        group.Text = "Output Settings"
        group.AutoSize = True
        group.AutoSizeMode = AutoSizeMode.GrowAndShrink

        layout = TableLayoutPanel()
        layout.RowCount = 2
        layout.ColumnCount = 2
        layout.AutoSize = True

        browse_button = Button()
        browse_button.Text = 'Browse Folder'
        browse_button.Size = Size(100, 22)  # Reduced height from default to 22
        browse_button.Click += self.browse_folder_button_click
        layout.Controls.Add(browse_button, 0, 0)

        self.folder_path_label = Label()
        self.folder_path_label.AutoSize = True
        self.folder_path_label.Text = "No folder selected"
        layout.Controls.Add(self.folder_path_label, 0, 1)

        group.Controls.Add(layout)
        return group

    def create_basic_audit_section(self):
        """Create the basic audit settings section."""
        group = GroupBox()
        group.Text = "Basic Audit (Warnings & Model Health)"
        group.AutoSize = True
        group.AutoSizeMode = AutoSizeMode.GrowAndShrink

        layout = TableLayoutPanel()
        layout.RowCount = 5
        layout.ColumnCount = 2
        layout.AutoSize = True

        self.enable_basic_checkbox = CheckBox()
        self.enable_basic_checkbox.Text = "Enable Basic Audit"
        self.enable_basic_checkbox.Checked = True
        self.enable_basic_checkbox.CheckedChanged += self.checkbox_changed
        layout.Controls.Add(self.enable_basic_checkbox, 0, 0)

        warning_label = Label()
        warning_label.Text = "Warning File:"
        layout.Controls.Add(warning_label, 0, 1)

        self.warning_input = TextBox()
        self.warning_input.Text = "warning_info.csv"
        self.warning_input.Size = Size(200, 20)
        self.warning_input.TextChanged += self.input_text_changed
        layout.Controls.Add(self.warning_input, 1, 1)

        audit_label = Label()
        audit_label.Text = "Audit File:"
        layout.Controls.Add(audit_label, 0, 2)

        self.audit_input = TextBox()
        self.audit_input.Text = "audit_info.csv"
        self.audit_input.Size = Size(200, 20)
        self.audit_input.TextChanged += self.input_text_changed
        layout.Controls.Add(self.audit_input, 1, 2)

        group.Controls.Add(layout)
        return group

    def create_workset_section(self):
        """Create the workset audit settings section."""
        group = GroupBox()
        group.Text = "Workset Audit"
        group.AutoSize = True
        group.AutoSizeMode = AutoSizeMode.GrowAndShrink

        layout = TableLayoutPanel()
        layout.RowCount = 4
        layout.ColumnCount = 2
        layout.AutoSize = True

        self.enable_workset_checkbox = CheckBox()
        self.enable_workset_checkbox.Text = "Enable Workset Audit"
        self.enable_workset_checkbox.Checked = False
        self.enable_workset_checkbox.CheckedChanged += self.checkbox_changed
        layout.Controls.Add(self.enable_workset_checkbox, 0, 0)

        workset_file_label = Label()
        workset_file_label.Text = "Workset File:"
        layout.Controls.Add(workset_file_label, 0, 1)

        self.workset_file_input = TextBox()
        self.workset_file_input.Text = "workset_info.csv"
        self.workset_file_input.Size = Size(200, 20)
        self.workset_file_input.TextChanged += self.input_text_changed
        layout.Controls.Add(self.workset_file_input, 1, 1)

        view_keyword_label = Label()
        view_keyword_label.Text = "3D View Keyword:"
        layout.Controls.Add(view_keyword_label, 0, 2)

        self.view_keyword_input = TextBox()
        self.view_keyword_input.Text = "Revizto"
        self.view_keyword_input.Size = Size(200, 20)
        self.view_keyword_input.TextChanged += self.input_text_changed
        layout.Controls.Add(self.view_keyword_input, 1, 2)

        group.Controls.Add(layout)
        return group

    def create_view_section(self):
        """Create the view audit settings section."""
        group = GroupBox()
        group.Text = "View Audit"
        group.AutoSize = True
        group.AutoSizeMode = AutoSizeMode.GrowAndShrink

        layout = TableLayoutPanel()
        layout.RowCount = 5
        layout.ColumnCount = 2
        layout.AutoSize = True

        self.enable_view_checkbox = CheckBox()
        self.enable_view_checkbox.Text = "Enable View Audit"
        self.enable_view_checkbox.Checked = False
        self.enable_view_checkbox.CheckedChanged += self.checkbox_changed
        layout.Controls.Add(self.enable_view_checkbox, 0, 0)

        view_file_label = Label()
        view_file_label.Text = "View File:"
        layout.Controls.Add(view_file_label, 0, 1)

        self.view_file_input = TextBox()
        self.view_file_input.Text = "view_compliance.csv"
        self.view_file_input.Size = Size(200, 20)
        self.view_file_input.TextChanged += self.input_text_changed
        layout.Controls.Add(self.view_file_input, 1, 1)

        view_types_label = Label()
        view_types_label.Text = "View Types:"
        layout.Controls.Add(view_types_label, 0, 2)

        self.view_types_combo = ComboBox()
        self.view_types_combo.DropDownStyle = ComboBoxStyle.DropDownList
        # Add items individually to avoid Array conversion issues
        view_type_options = ["All Views", "3D Views Only", "Plan Views Only", "Section Views Only", "Custom Selection"]
        for option in view_type_options:
            self.view_types_combo.Items.Add(option)
        self.view_types_combo.SelectedIndex = 0
        self.view_types_combo.Size = Size(200, 20)
        layout.Controls.Add(self.view_types_combo, 1, 2)

        patterns_label = Label()
        patterns_label.Text = "View Patterns:"
        layout.Controls.Add(patterns_label, 0, 3)

        self.view_patterns_input = TextBox()
        self.view_patterns_input.Text = "discipline:STR,ARC,MEP,ELE; not:temp; not:test; not:copy"
        self.view_patterns_input.Size = Size(200, 60)
        self.view_patterns_input.Multiline = True
        self.view_patterns_input.ScrollBars = ScrollBars.Vertical
        self.view_patterns_input.TextChanged += self.input_text_changed
        layout.Controls.Add(self.view_patterns_input, 1, 3)

        help_label = Label()
        help_label.Text = "Pattern Help:\n• Discipline: 'discipline:STR,ARC,MEP' matches '_STR_', '_ARC_', '_MEP_'\n• Simple text: 'Linked View' matches views containing that text\n• Exclusions: 'not:temp' excludes views with 'temp'\n• Regex: 'regex:^Linked View_\\w{3}_' for advanced patterns\n• Separate multiple patterns with semicolons"
        help_label.Size = Size(380, 70)  # Reduced height from 80 to 70
        help_label.Font = Font("Arial", 7)
        layout.Controls.Add(help_label, 0, 4)
        layout.SetColumnSpan(help_label, 2)

        group.Controls.Add(layout)
        return group

    def create_button_section(self):
        """Create the button section."""
        button_panel = FlowLayoutPanel()
        button_panel.FlowDirection = FlowDirection.LeftToRight
        button_panel.AutoSize = True
        button_panel.Padding = Padding(10)

        self.submit_button = Button()
        self.submit_button.Text = 'Submit'
        self.submit_button.Size = Size(80, 30)
        self.submit_button.Enabled = False
        self.submit_button.Click += self.submit_button_click
        button_panel.Controls.Add(self.submit_button)

        cancel_button = Button()
        cancel_button.Text = 'Cancel'
        cancel_button.Size = Size(80, 30)
        cancel_button.Click += lambda sender, args: self.Close()
        button_panel.Controls.Add(cancel_button)

        return button_panel

    def browse_folder_button_click(self, sender, args):
        """Handle the event when the browse folder button is clicked."""
        dialog = FolderBrowserDialog()
        if dialog.ShowDialog() == DialogResult.OK:
            self.folder_path_label.Text = dialog.SelectedPath
            self.update_submit_button_state()

    def submit_button_click(self, sender, args):
        """Handle the event when the submit button is clicked."""
        self.DialogResult = DialogResult.OK
        self.Close()

    def checkbox_changed(self, sender, args):
        """Handle checkbox state changes."""
        self.update_submit_button_state()

    def input_text_changed(self, sender, args):
        """Handle text input changes."""
        self.update_submit_button_state()

    def update_submit_button_state(self):
        """Enable the submit button only if required fields are filled."""
        has_folder = self.folder_path_label.Text != "No folder selected" and self.folder_path_label.Text != ""
        
        # Check if at least one audit type is enabled
        has_enabled_audit = (self.enable_basic_checkbox.Checked or 
                           self.enable_workset_checkbox.Checked or 
                           self.enable_view_checkbox.Checked)
        
        # Check required fields for enabled audits
        basic_valid = True
        if self.enable_basic_checkbox.Checked:
            basic_valid = (self.warning_input.Text.strip() != "" and 
                          self.audit_input.Text.strip() != "")
        
        workset_valid = True
        if self.enable_workset_checkbox.Checked:
            workset_valid = (self.workset_file_input.Text.strip() != "" and
                           self.view_keyword_input.Text.strip() != "")
        
        view_valid = True
        if self.enable_view_checkbox.Checked:
            view_valid = (self.view_file_input.Text.strip() != "" and
                         self.view_patterns_input.Text.strip() != "")
        
        self.submit_button.Enabled = (has_folder and has_enabled_audit and 
                                    basic_valid and workset_valid and view_valid)
        
        logger.debug(f"Submit button enabled: {self.submit_button.Enabled}")

    def get_user_inputs(self):
        """Get all user inputs from the form."""
        # Parse view patterns
        view_patterns = []
        if self.view_patterns_input.Text.strip():
            patterns = [p.strip() for p in self.view_patterns_input.Text.split(';')]
            view_patterns = [p for p in patterns if p]  # Remove empty patterns
        
        # Parse view types
        view_types_selection = self.view_types_combo.SelectedItem
        if view_types_selection == "All Views":
            view_types = None
        elif view_types_selection == "3D Views Only":
            view_types = ["View3D"]
        elif view_types_selection == "Plan Views Only":
            view_types = ["ViewPlan"]
        elif view_types_selection == "Section Views Only":
            view_types = ["ViewSection"]
        else:
            view_types = None  # Default to all for custom selection
        
        return {
            'output_dir': self.folder_path_label.Text,
            
            # Basic audit settings
            'enable_basic': self.enable_basic_checkbox.Checked,
            'warning_file_name': self.warning_input.Text.strip(),
            'audit_file_name': self.audit_input.Text.strip(),
            
            # Workset audit settings
            'enable_workset': self.enable_workset_checkbox.Checked,
            'workset_file_name': self.workset_file_input.Text.strip(),
            'view_keyword': self.view_keyword_input.Text.strip(),
            
            # View audit settings
            'enable_view': self.enable_view_checkbox.Checked,
            'view_file_name': self.view_file_input.Text.strip(),
            'view_patterns': view_patterns,
            'view_types': view_types
        }


def show_ui():
    """Show the extended UI and return user inputs."""
    try:
        form = ExtendedAuditForm()
        
        if form.ShowDialog() == DialogResult.OK:
            user_inputs = form.get_user_inputs()
            logger.info("User inputs collected successfully")
            return user_inputs
        else:
            logger.info("User cancelled the input dialog")
            return None
            
    except Exception as e:
        logger.error(f"Error showing UI: {str(e)}")
        return None