import clr
clr.AddReference('System.Windows')

from pyrevit import forms
from System.Windows.Controls import WebBrowser, Grid

from .core_processing import get_documents, get_model_categories, get_category_parameters, get_parameter_values, generate_table_html, export_data_to_csv
from .warning import display_warning, display_error, handle_exception, log_warning


def select_models(doc):
    docs = get_documents(doc)
    options = [f"Current Model: {doc.Title}"] + [f"Linked Model: {d.Title}" for d in docs[1:]]
    selected = forms.SelectFromList.show(
        options,
        title='Select Models',
        multiselect=True,
        button_name='Next'
    )
    if not selected:
        return None
    return [d for d in docs if d.Title in [s.split(": ", 1)[1] for s in selected]]

def select_categories(documents):
    all_categories = get_model_categories(documents)
    options = sorted(all_categories.keys())
    selected = forms.SelectFromList.show(
        options,
        title='Select Categories',
        multiselect=True,
        button_name='Next'
    )
    if not selected:
        return None
    return {cat: all_categories[cat] for cat in selected}

def select_parameters(selected_categories):
    all_parameters = set()
    for category_name, doc_category_pairs in selected_categories.items():
        for doc, category in doc_category_pairs:
            all_parameters.update(get_category_parameters(doc, category))
    
    options = sorted(all_parameters)
    selected = forms.SelectFromList.show(
        options,
        title='Select Parameters',
        multiselect=True,
        button_name='Finish'
    )
    if not selected:
        return None
    return selected

class HTMLTableWindow(forms.WPFWindow):
    def __init__(self, title, width, height):
#        forms.WPFWindow.__init__(self, title)
        self.Width = width
        self.Height = height

        # Create a WebBrowser control
        self.web_browser = WebBrowser()

        # Create a Grid to hold the WebBrowser
        grid = Grid()
        grid.Children.Add(self.web_browser)

        # Set the window content
        self.Content = grid

    def set_html_content(self, html_content):
        self.web_browser.NavigateToString(html_content)

def display_data_table(data_by_document, selected_parameters):
    html_content = ""
    for doc_title, data in data_by_document.items():
        html_content += f"<h2>{doc_title}</h2>"
        html_content += generate_table_html(data, selected_parameters)

    window = HTMLTableWindow("Data Preview", 800, 600)
    window.set_html_content(html_content)
    window.ShowDialog()

    # After displaying the data, ask if the user wants to export
    if forms.alert("Do you want to export this data to CSV?", yes=True, no=True):
        from lib.core_processing import export_data_to_csv
        export_data_to_csv(data_by_document, selected_parameters)