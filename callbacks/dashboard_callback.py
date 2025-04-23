from dash import Input, Output, State, callback, ctx, dash, html
import dash_bootstrap_components as dbc
from dash import dcc

@callback(
    Output("patient-table-body", "children"),  # Update patient table
    Input("dashboard-data", "data"),  # Retrieve current dashboard data
    prevent_initial_call=True,
)
def populate_table(dashboard_data):
    if not dashboard_data:
        return []

    # Populate the table rows
    table_rows = []
    for entry in dashboard_data:
        # Ensure missing_docs is a properly formatted string
        missing_docs = entry.get("missing_docs", "None")
        if isinstance(missing_docs, list):
            missing_docs = ", ".join(missing_docs)  # Join list into a single string

        table_rows.append(html.Tr([
            html.Td(entry["name"]),
            html.Td(entry["status"]),
            html.Td(missing_docs)  # Display missing documents as a single string
        ]))

    return table_rows

@callback(
    Output("url", "pathname"),  # Directly update the URL
    Input("add-patient-btn", "n_clicks"),  # Button click to add a new patient
    prevent_initial_call=True,
)
def navigate_to_upload(add_patient_clicks):
    triggered_id = ctx.triggered_id

    # If "Add Patient" button is clicked, navigate to the upload page
    if triggered_id == "add-patient-btn" and add_patient_clicks:
        return "/upload"

    return dash.no_update