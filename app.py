from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import os

# Dash app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Claims Intake Platform"

from pages.dashboard_layout import landing_page_layout
from pages.upload_docs_layout import upload_docs_page_layout
from pages.patient_profile_layout import patient_profile_layout  # Import the new layout

# Import callbacks
from callbacks.dashboard_callback import *
from callbacks.upload_callback import *
from callbacks.patient_profile_callback import *  # Import the new callback

# App layout with location and page content
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # Define it here only once
    dcc.Store(id="dashboard-data", data=[]),  # Global store for dashboard data
    html.Div(id="page-content"),

    # Hidden container to register all components referenced in callbacks
    html.Div([
        landing_page_layout,
        upload_docs_page_layout,
        patient_profile_layout  # Include the new layout
    ], style={"display": "none"})
])

# Callback to dynamically load pages
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    State("dashboard-data", "data")  # Pass the dashboard data to repopulate the table
)
def display_page(pathname, dashboard_data):
    if pathname == "/upload":
        return upload_docs_page_layout
    elif pathname.startswith("/profile"):
        return patient_profile_layout  # Route to the patient profile page for any /profile?...
    elif pathname == "/":
        populate_table(dashboard_data)
        return landing_page_layout
    return landing_page_layout

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)