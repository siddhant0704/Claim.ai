from dash import Input, Output, State, callback, html
from urllib.parse import parse_qs
from utils import format_combined_info

@callback(
    [
        Output("patient-name", "children"),
        Output("patient-info", "children"),
        Output("uploaded-docs-preview", "children"),  # <-- Add this output
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
        return "N/A", "No information available", [], "No missing documents"

    query_params = parse_qs(search.lstrip("?"))
    patient_name = query_params.get("patient", [None])[0]

    if not patient_name:
        print("DEBUG: Patient name not found in query parameters.")
        return "N/A", "No information available", [], "No missing documents"

    for entry in dashboard_data:
        if entry["name"] == patient_name:
            print(f"DEBUG: Found patient data for {patient_name}: {entry}")

            # Generate document previews
            previews = []
            for doc in entry.get("stored_docs", []):
                name = doc.get("name", "Unknown")
                content = doc.get("content", "")
                ext = name.split(".")[-1].lower()
                doc_type = doc.get("parsed_data", {}).get("doc_type", "Unknown")

                if ext in ["jpg", "jpeg", "png"]:
                    previews.append(html.Div([
                        html.P(f"{doc_type}"),
                        html.Img(src=f"data:image/{ext};base64,{content}", style={"height": "100px"})
                    ]))
                elif ext == "pdf":
                    previews.append(html.Div([
                        html.P(f"{doc_type} (PDF preview not supported)")
                    ]))
                else:
                    previews.append(html.Div([
                        html.P(f"{doc_type} (No preview)")
                    ]))
            
            combined_info_html = format_combined_info(entry.get("stored_docs", [{}])[0].get("parsed_data", {}).get("combined_info", ""))

            return (
                entry["name"],
                combined_info_html,
                previews,  # <-- Uploaded docs preview
                entry.get("missing_docs", "No missing documents"),
            )

    print(f"DEBUG: Patient {patient_name} not found in dashboard-data.")
    return "N/A", "No information available", [], "No missing documents"

@callback(
    Output("submit-modal", "is_open"),
    [Input("submit-btn", "n_clicks"), Input("close-submit-modal", "n_clicks")],
    [State("submit-modal", "is_open")],
    prevent_initial_call=True,
)
def toggle_submit_modal(submit_clicks, close_clicks, is_open):
    if submit_clicks or close_clicks:
        return not is_open
    return is_open