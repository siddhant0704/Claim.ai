from dash import Input, Output, State, callback, ctx, dash, html, MATCH
import dash_bootstrap_components as dbc
from dash import dcc
from dash import Input, Output, State, callback, ctx, dash, html, dcc, ALL
import dash_bootstrap_components as dbc

@callback(
    Output("patient-table-body", "children"),
    Input("dashboard-data", "data"),
    Input("edit-mode", "data"),
    Input("selected-rows", "data"),
    prevent_initial_call=False,
)
def populate_table(dashboard_data, edit_mode, selected_rows):
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
    for idx, entry in enumerate(dashboard_data):
        patient_name = entry["name"]
        patient_url = f"/profile?patient={patient_name}"
        summary = entry.get("summary", "No summary available")
        status = entry.get("status", "Pending")
        checked = idx in (selected_rows or [])

        row = []
        if edit_mode:
            row.append(
                html.Td(
                    dcc.Checklist(
                        options=[{"label": "", "value": idx}],
                        value=[idx] if checked else [],
                        id={"type": "row-select", "index": idx},
                        inline=True,
                        style={"margin": "0"}
                    ),
                    style={"width": "40px"}
                )
            )
        else:
            row.append(html.Td(""))

        row += [
            html.Td(dcc.Link(patient_name, href=patient_url)),
            html.Td(summary, className="summary-left-align"),
            html.Td(status_badge(status)),
        ]
        table_rows.append(html.Tr(row))

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


# ...existing code...

from dash import ALL

# Toggle edit mode
@callback(
    Output("edit-mode", "data"),
    Input("edit-table-btn", "n_clicks"),
    State("edit-mode", "data"),
    prevent_initial_call=True,
)
def toggle_edit_mode(n, edit_mode):
    return not edit_mode if n else edit_mode

# Show/hide Delete Selected button
@callback(
    Output("delete-selected-btn", "style"),
    Input("edit-mode", "data"),
    Input("selected-rows", "data"),
    prevent_initial_call=False,
)
def show_delete_btn(edit_mode, selected_rows):
    if edit_mode and selected_rows:
        return {"display": "inline-block"}
    return {"display": "none"}

# Handle row selection
@callback(
    Output("selected-rows", "data"),
    Input({"type": "row-select", "index": ALL}, "value"),
    State("edit-mode", "data"),
    prevent_initial_call=True,
)
def update_selected_rows(values, edit_mode):
    if not edit_mode:
        return []
    selected = []
    for idx, val in enumerate(values):
        if val:
            selected.append(val[0])
    return selected

# Open/close delete confirmation modal
@callback(
    Output("delete-confirm-modal", "is_open"),
    [Input("delete-selected-btn", "n_clicks"), Input("cancel-delete-btn", "n_clicks"), Input("confirm-delete-btn", "n_clicks")],
    [State("delete-confirm-modal", "is_open")],
    prevent_initial_call=True,
)
def toggle_delete_modal(open_click, cancel_click, confirm_click, is_open):
    triggered = ctx.triggered_id
    if triggered == "delete-selected-btn":
        return True
    elif triggered in ["cancel-delete-btn", "confirm-delete-btn"]:
        return False
    return is_open

# Delete selected rows
@callback(
    Output("dashboard-data", "data", allow_duplicate=True),
    Output("selected-rows", "data", allow_duplicate=True),
    Input("confirm-delete-btn", "n_clicks"),
    State("selected-rows", "data"),
    State("dashboard-data", "data"),
    prevent_initial_call=True,
)
def delete_selected_rows(n, selected_rows, dashboard_data):
    if not n or not selected_rows or not dashboard_data:
        return dash.no_update, dash.no_update
    # Remove entries by index
    new_data = [row for idx, row in enumerate(dashboard_data) if idx not in selected_rows]
    return new_data, []

