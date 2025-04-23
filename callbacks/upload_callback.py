import dash
from dash import Input, Output, State, callback, ctx, html
import base64
import os
import tempfile
import re  # For extracting patient name
from utils import process_claim_case

@callback(
    [
        Output("stored-docs", "data"),
        Output("file-preview", "children"),
        Output("output-info", "value"),
        Output("output-summary", "value"),
        Output("output-missing", "value"),
        Output("action-buttons", "style"),
        Output("dashboard-data", "data"),
    ],
    [
        Input("upload-docs", "contents"),
        Input("submit-btn", "n_clicks"),
        Input("reset-btn", "n_clicks"),
        Input("back-btn", "n_clicks"),
    ],
    [
        State("upload-docs", "filename"),
        State("upload-docs", "last_modified"),
        State("stored-docs", "data"),
        State("dashboard-data", "data"),
    ],
    prevent_initial_call=True,
)
def upload_callback(contents, submit_clicks, reset_clicks, back_clicks, filenames, last_modified, stored_data, dashboard_data):
    triggered_id = ctx.triggered_id

    # Initialize dashboard_data if None
    if dashboard_data is None:
        dashboard_data = []

    # RESET: Clear all components
    if triggered_id == "reset-btn":
        return None, [], "", "", "", {"display": "none"}, dashboard_data

    # BACK: Add a new row to the dashboard table
    if triggered_id == "back-btn":
        if stored_data:
            for file in stored_data:
                parsed_data = file.get("parsed_data", {})

                # Extract patient name or fallback to file name
                combined_info = parsed_data.get("combined_info", "")
                match = re.search(r"(?:Name|Patient)\s*[:\-]?\s*([A-Za-z\s]+)", combined_info)
                patient_name = match.group(1).strip() if match else file["name"]

                # Determine claim status
                claim_status = "Processed" if parsed_data.get("summary", "").strip() == "Yes" else "Pending"

                # Format missing_docs as a single string
                missing_docs = parsed_data.get("missing_documents", [])
                if isinstance(missing_docs, list):
                    missing_docs = ", ".join(missing_docs)  # Join list into a single string

                # Add a new row to the dashboard data
                dashboard_data.append({
                    "name": patient_name,
                    "status": claim_status,
                    "missing_docs": missing_docs or "None"  # Ensure it's a string
                })

            return stored_data, [], "", "", "", {"display": "none"}, dashboard_data

        return stored_data, [], "", "", "", {"display": "none"}, dashboard_data

    # FILE UPLOAD
    elif triggered_id == "upload-docs":
        if contents is None:
            return stored_data, [], "", "", "", {"display": "none"}, dashboard_data

        file_previews = []
        updated_stored = []

        for content, name in zip(contents, filenames):
            filetype = name.split(".")[-1].lower()
            encoded = content.split(",")[1]

            if filetype in ["jpg", "jpeg", "png"]:
                preview = html.Div([
                    html.Img(src=content, style={"height": "100px"}),
                    html.P(name)
                ])
            elif filetype in ["pdf", "mp3", "wav"]:
                preview = html.Div([
                    html.P(f"{name} (Uploaded)")
                ])
            else:
                preview = html.Div([html.P(f"{name} (Unsupported)")])

            file_previews.append(preview)
            updated_stored.append({"name": name, "content": encoded})

        return updated_stored, file_previews, "", "", "", {"display": "flex"}, dashboard_data

    # SUBMIT: Process and extract data
    elif triggered_id == "submit-btn":
        if not stored_data:
            return stored_data, [], "", "", "", {"display": "flex"}, dashboard_data

        previews = []
        info_outputs, summary_outputs, missing_outputs = [], [], []

        for file in stored_data:
            name, encoded = file["name"], file["content"]
            decoded = base64.b64decode(encoded)
            suffix = os.path.splitext(name)[-1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(decoded)
                temp_path = temp_file.name

            filetype = suffix.lower().strip(".")
            result = process_claim_case([(temp_path, filetype)])

            previews.append(html.Div([html.P(f"{name} (Processed)")]))

            info_outputs.append(result.get("combined_info", ""))
            summary_outputs.append(result.get("claim_summary", ""))
            missing_outputs.append(result.get("missing_documents", ""))

            # Store parsed data for back button functionality
            file["parsed_data"] = {
                "summary": result.get("claim_summary", ""),
                "missing_documents": result.get("missing_documents", ""),
                "combined_info": result.get("combined_info", "")
            }

        return (
            stored_data,
            previews,
            "\n".join(info_outputs),
            "\n".join(summary_outputs),
            "\n".join(missing_outputs),
            {"display": "flex"},
            dashboard_data
        )

    return stored_data, [], "", "", "", {"display": "none"}, dashboard_data