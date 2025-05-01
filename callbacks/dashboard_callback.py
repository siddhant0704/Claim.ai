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
    
    def status_badge(status):
        color = "secondary"
        if status.lower() == "pending":
            color = "warning"
        elif status.lower() == "submitted for approval":
            color = "success"
        elif status.lower() == "requested additional info":
            color = "danger"
        return dbc.Badge(status, color=color, className="fw-bold", pill=True)

    table_rows = []
    for entry in dashboard_data:
        patient_name = entry["name"]
        patient_url = f"/profile?patient={patient_name}"
        summary = entry.get("summary", "No summary available")
        status = entry.get("status", "Pending")

        table_rows.append(html.Tr([
            html.Td(dcc.Link(patient_name, href=patient_url)),
            html.Td(summary, className="summary-left-align"),
            html.Td(status_badge(status)),
        ]))

    return table_rows

@callback(
    Output("url", "pathname"),  # Directly update the URL
    Input("add-patient-btn", "n_clicks"),  # Button click to add a new patient
    prevent_initial_call=True,
)
def navigate_to_upload(add_patient_clicks):
    triggered_id = ctx.triggered_id

    if triggered_id == "add-patient-btn" and add_patient_clicks:
        return "/upload"

    return dash.no_update

@callback(
    [
        Output("metric-total", "children"),
        Output("metric-under-approval", "children"),
        Output("metric-pending", "children"),
    ],
    Input("dashboard-data", "data"),
    prevent_initial_call=False,
)
def update_metrics(dashboard_data):
    if not dashboard_data:
        return 0, 0, 0

    total = len(dashboard_data)
    under_approval = sum(1 for entry in dashboard_data if entry.get("status", "").lower() == "submitted for approval")
    pending = sum(1 for entry in dashboard_data if entry.get("status", "").lower() == "pending")
    return total, under_approval, pending

