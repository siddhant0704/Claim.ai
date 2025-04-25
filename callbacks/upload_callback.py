import dash
from dash import Input, Output, State, callback, ctx, html
import base64
import os
import tempfile
import re  # For extracting patient name
from utils import process_claim_case, generate_patient_summary

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
        Input("upload-submit-btn", "n_clicks"),
        Input("upload-reset-btn", "n_clicks"),
        Input("upload-back-btn", "n_clicks"),
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
    if triggered_id == "upload-reset-btn":
        return None, [], "", "", "", {"display": "none"}, dashboard_data

    # BACK: Update or add a single row for the patient
    if triggered_id == "upload-back-btn":
        if stored_data:
            # Aggregate all docs for this patient
            # Try to extract patient name from the first doc with parsed data
            patient_name = None
            summary = ""
            claim_status = "Pending"
            missing_docs = ""
            for file in stored_data:
                parsed_data = file.get("parsed_data", {})
                combined_info = parsed_data.get("combined_info", "")
                match = re.search(r"Patient Name:\s*([A-Za-z\s]+)", combined_info)
                if match:
                    patient_name = match.group(1).strip()
                    summary = parsed_data.get("patient_summary", "")
                    claim_status = "Processed" if parsed_data.get("summary", "").strip() == "Yes" else "Pending"
                    missing_docs = parsed_data.get("missing_documents", "")
                    break
            if not patient_name:
                # Fallback to first file name if patient name not found
                patient_name = stored_data[0]["name"]

            # Check if patient already exists
            found = False
            for entry in dashboard_data:
                if entry["name"] == patient_name:
                    # Update the existing row: merge stored_docs
                    entry["status"] = claim_status
                    entry["missing_docs"] = missing_docs or "None"
                    entry["stored_docs"] = stored_data
                    entry["summary"] = summary
                    found = True
                    break
            if not found:
                # Add new row for patient
                dashboard_data.append({
                    "name": patient_name,
                    "status": claim_status,
                    "missing_docs": missing_docs or "None",
                    "stored_docs": stored_data,
                    "summary": summary,
                })

            print(f"DEBUG: Updated dashboard data: {dashboard_data}")
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
    elif triggered_id == "upload-submit-btn":
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

            # Generate a crisp summary
            summary = generate_patient_summary(result.get("combined_info", ""))

            previews.append(html.Div([html.P(f"{name} (Processed)")]))

            info_outputs.append(result.get("combined_info", ""))
            summary_outputs.append(result.get("claim_summary", ""))
            missing_outputs.append(result.get("missing_documents", ""))

            # Extract document type/category from combined_info
            combined_info = result.get("combined_info", "")
            doc_type_match = re.search(r"Category:\s*([^\n]+)", combined_info)
            doc_type = doc_type_match.group(1).strip() if doc_type_match else "Unknown"

            # Store parsed data for back button functionality
            file["parsed_data"] = {
                "summary": result.get("claim_summary", ""),
                "missing_documents": result.get("missing_documents", ""),
                "combined_info": result.get("combined_info", ""),
                "patient_summary": summary,  
                "doc_type": doc_type,  
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