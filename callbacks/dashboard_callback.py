from dash import Input, Output, State, callback, ctx, dash, html
import dash_bootstrap_components as dbc
from dash import dcc

@callback(
    Output("patient-table-body", "children"),
    Input("dashboard-data", "data"),
    prevent_initial_call=False,
)
def populate_table(dashboard_data):
    if not dashboard_data:
        return []

    table_rows = []
    for entry in dashboard_data:
        patient_name = entry["name"]
        patient_url = f"/profile?patient={patient_name}"
        print(f"DEBUG: Generating URL for patient {patient_name}: {patient_url}")

        summary = entry.get("summary", "No summary available")

        table_rows.append(html.Tr([
            html.Td(dcc.Link(patient_name, href=patient_url)),
            html.Td(summary),
            html.Td(entry["status"]),
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