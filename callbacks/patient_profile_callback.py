from dash import Input, Output, State, callback, html
from urllib.parse import parse_qs

from dash import Input, Output, State, callback, html
from urllib.parse import parse_qs

@callback(
    [
        Output("patient-name", "children"),
        Output("patient-info", "children"),
        Output("missing-docs", "children"),
    ],
    Input("url", "search"),
    State("dashboard-data", "data"),
    prevent_initial_call=False,
)
def load_patient_profile(search, dashboard_data):
    print(f"DEBUG: URL search parameter: {search}")

    if not dashboard_data:
        print("DEBUG: dashboard-data is empty.")
        return "N/A", "No information available", "No missing documents"

    query_params = parse_qs(search.lstrip("?"))
    patient_name = query_params.get("patient", [None])[0]

    if not patient_name:
        print("DEBUG: Patient name not found in query parameters.")
        return "N/A", "No information available", "No missing documents"

    for entry in dashboard_data:
        if entry["name"] == patient_name:
            print(f"DEBUG: Found patient data for {patient_name}: {entry}")
            return (
                entry["name"],  # Patient name
                html.Div([
                    html.P(f"Claim Status: {entry.get('status', 'N/A')}"),
                    html.P(entry.get("summary", "No summary available"))
                ]),
                entry.get("missing_docs", "No missing documents"),
            )

    print(f"DEBUG: Patient {patient_name} not found in dashboard-data.")
    return "N/A", "No information available", "No missing documents"