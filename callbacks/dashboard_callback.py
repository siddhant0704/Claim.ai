from dash import Input, Output, State, callback, ctx, dash
import dash_bootstrap_components as dbc
from dash import dcc


@callback(
    Output("patient-table-body", "children"),  # Update patient table
    Input("add-patient-btn", "n_clicks"),  # Button click to add a new patient
    State("dashboard-data", "data"),  # Retrieve current dashboard data
    prevent_initial_call=True
)
def dashboard_callback(add_patient_clicks, current_dashboard_data):
    triggered_id = ctx.triggered_id

    # If "Add Patient" button is clicked, no need to update URL here
    if triggered_id == "add-patient-btn" and add_patient_clicks:
        return dash.no_update  # Keep the table unchanged for now

    return dash.no_update