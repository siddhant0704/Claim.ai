from dash import Input, Output, State, callback, ctx, dash
import dash_bootstrap_components as dbc

# Store for keeping track of data between pages
from dash import dcc

# This is where the table data gets stored
dcc.Store(id="dashboard-data", data=[])

@callback(
    [
        Output("url", "pathname"),  # Redirect to the correct page
        Output("patient-table-body", "children"),  # Update patient table
        Output("back-btn", "style"),  # Ensure the back button appears
    ],
    [
        Input("add-patient-btn", "n_clicks"),  # Button click to add a new patient
        Input("back-btn", "n_clicks"),  # Button click to go back from Upload to Dashboard
    ],
    [
        State("dashboard-data", "data"),  # Retrieve current dashboard data
    ],
)
def dashboard_callback(add_patient_clicks, back_clicks, current_dashboard_data):
    triggered_id = ctx.triggered_id

    # If "Add Patient" button is clicked, redirect to Upload page
    if triggered_id == "add-patient-btn" and add_patient_clicks:
        return "/upload", current_dashboard_data, {"display": "none"}  # Hide the button on the upload page

    # If "Back" button is clicked, return to the dashboard and update data
    elif triggered_id == "back-btn" and back_clicks:
        # Return the updated data (or whatever you want to pass to the table)
        return "/dashboard", current_dashboard_data, {"display": "block"}  # Show the back button again

    return dash.no_update, dash.no_update, dash.no_update
