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

    # RESET: Clear all components
    if triggered_id == "reset-btn":
        return None, [], "", "", "", {"display": "none"}, dash.no_update

    # BACK: Restore dashboard table using stored parsed data
    if triggered_id == "back-btn":
        if stored_data:
            if not dashboard_data:
                dashboard_data = []

            for file in stored_data:
                parsed_data = file.get("parsed_data", {})

                # Attempt to extract patient name from combined_info
                combined_info = parsed_data.get("combined_info", "")
                match = re.search(r"(?:Name|Patient)\s*[:\-]?\s*([A-Za-z\s]+)", combined_info)
                patient_name = match.group(1).strip() if match else file["name"]

                claim_status = "Processed" if parsed_data.get("summary", "").strip() == "Yes" else "Pending"

                # Avoid duplicate rows
                if not any(entry["name"] == patient_name for entry in dashboard_data):
                    dashboard_data.append({
                        "name": patient_name,
                        "status": claim_status,
                        "missing_docs": (
                            ", ".join(result["missing_documents"])
                            if isinstance(result.get("missing_documents"), list)
                            else result.get("missing_documents", "None")
                        )
                    })

            return stored_data, [], "", "", "", {"display": "none"}, dashboard_data

        return stored_data, [], "", "", "", {"display": "none"}, dashboard_data

    # FILE UPLOAD
    elif triggered_id == "upload-docs":
        if contents is None:
            return stored_data, [], "", "", "", {"display": "none"}, dash.no_update

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

        return updated_stored, file_previews, "", "", "", {"display": "flex"}, dash.no_update

    # SUBMIT: Process and extract data
    elif triggered_id == "submit-btn":
        if not stored_data:
            return stored_data, [], "", "", "", {"display": "flex"}, dash.no_update

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

            # Attempt to extract patient name from combined_info
            combined_info = result.get("combined_info", "")
            match = re.search(r"(?:Name|Patient)\s*[:\-]?\s*([A-Za-z\s]+)", combined_info)
            patient_name = match.group(1).strip() if match else name

            claim_status = "Processed" if result.get("claim_summary", "").strip() == "Yes" else "Pending"

            # Avoid duplicate rows
            if not any(entry["name"] == patient_name for entry in dashboard_data):
                dashboard_data.append({
                    "name": patient_name,
                    "status": claim_status,
                    "missing_docs": ", ".join(result.get("missing_documents", [])) or "None"
                })

            # Store everything needed for back button
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
            dashboard_data  # Pass updated dashboard data
        )

    return stored_data, [], "", "", "", {"display": "none"}, dash.no_update