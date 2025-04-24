from dash import Input, Output, State, callback, html
from urllib.parse import parse_qs

@callback(
    [
        Output("patient-name", "children"),
        Output("patient-info", "children"),
        Output("missing-docs", "children"),
    ],
    Input("url", "search"),  # Capture query parameters from the URL
    State("dashboard-data", "data"),  # Access the dashboard data
    prevent_initial_call=True,
)
def load_patient_profile(search, dashboard_data):
    # Debugging: Check if dashboard_data is empty
    if not dashboard_data:
        print("DEBUG: dashboard-data is empty.")
        return "N/A", "No information available", "No missing documents"

    # Parse query parameters from the URL
    query_params = parse_qs(search.lstrip("?"))  # Remove the leading "?" from the search string
    patient_name = query_params.get("patient", [None])[0]  # Extract the "patient" parameter

    # Debugging: Check if patient_name is extracted
    if not patient_name:
        print("DEBUG: Patient name not found in query parameters.")
        return "N/A", "No information available", "No missing documents"

    # Find the patient in the dashboard data
    for entry in dashboard_data:
        if entry["name"] == patient_name:
            # Format the stored_docs field as a string or Dash component
            stored_docs = entry.get("stored_docs", [])
            if isinstance(stored_docs, list):
                # Convert the list of documents into a readable string
                stored_docs = html.Ul([html.Li(f"{doc['name']}") for doc in stored_docs])

            # Debugging: Print the patient data
            print(f"DEBUG: Found patient data for {patient_name}: {entry}")

            return (
                entry["name"],  # Patient name
                stored_docs,  # Basic info (formatted as a list of document names)
                entry.get("missing_docs", "No missing documents"),  # Missing documents
            )

    # Debugging: Patient not found in dashboard_data
    print(f"DEBUG: Patient {patient_name} not found in dashboard-data.")
    return "N/A", "No information available", "No missing documents"