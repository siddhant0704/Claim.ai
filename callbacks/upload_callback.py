import dash
from dash import Input, Output, State, callback, ctx, html
import base64
import os
import tempfile
from utils import process_claim_case

@callback(
    [
        Output("stored-docs", "data"),  # Stores uploaded files
        Output("file-preview", "children"),  # Previews files
        Output("output-info", "value"),  # Display extracted info
        Output("output-summary", "value"),  # Display claim summary
        Output("output-missing", "value"),  # Display missing documents
        Output("action-buttons", "style"),  # Show/Hide action buttons
        Output("dashboard-data", "data"),  # Populate dashboard table with parsed data
    ],
    [
        Input("upload-docs", "contents"),  # File upload input
        Input("submit-btn", "n_clicks"),  # Submit button
        Input("reset-btn", "n_clicks"),  # Reset button
        Input("back-btn", "n_clicks"),  # Back button
    ],
    [
        State("upload-docs", "filename"),  # Get the uploaded file names
        State("upload-docs", "last_modified"),  # Get the last modified time of the files
        State("stored-docs", "data"),  # Get the stored data of previously uploaded files
        State("dashboard-data", "data"),  # Get the current dashboard data
    ],
    prevent_initial_call=True,
)
def upload_callback(contents, submit_clicks, reset_clicks, back_clicks, filenames, last_modified, stored_data, dashboard_data):
    triggered_id = ctx.triggered_id

    # If reset button is clicked, clear everything
    if triggered_id == "reset-btn":
        return None, [], "", "", "", {"display": "none"}, dash.no_update

    # Handle back button logic
    if triggered_id == "back-btn":
        if stored_data:
            # Add a new entry to the dashboard data
            if not dashboard_data:
                dashboard_data = []

            for file in stored_data:
                name = file["name"]
                parsed_data = file.get("parsed_data", {})
                dashboard_data.append({
                    "name": name,
                    "summary": parsed_data.get("summary", "N/A"),
                    "status": "Processed",
                    "missing_docs": parsed_data.get("missing_documents", "N/A")
                })

            return stored_data, [], "", "", "", {"display": "none"}, dashboard_data

        return stored_data, [], "", "", "", {"display": "none"}, dashboard_data

    # Handle file upload logic
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

    # Handle file submission and processing logic
    elif triggered_id == "submit-btn":
        if not stored_data:
            return stored_data, [], "", "", "", {"display": "flex"}, dash.no_update

        previews = []
        info_outputs, summary_outputs, missing_outputs = [], [], []

        # Process each uploaded file
        for file in stored_data:
            name, encoded = file["name"], file["content"]
            decoded = base64.b64decode(encoded)
            suffix = os.path.splitext(name)[-1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(decoded)
                temp_path = temp_file.name

            # Determine file type and process the claim accordingly
            filetype = suffix.lower().strip(".")
            result = process_claim_case([(temp_path, filetype)])

            # Previews for processed files
            previews.append(html.Div([html.P(f"{name} (Processed)")]))

            # Gather the results
            info_outputs.append(result.get("combined_info", ""))
            summary_outputs.append(result.get("claim_summary", ""))
            missing_outputs.append(result.get("missing_documents", ""))

            # Store parsed data for back button functionality
            file["parsed_data"] = {
                "summary": result.get("claim_summary", ""),
                "missing_documents": result.get("missing_documents", "")
            }

        # Return the processed results and updated UI components
        return (
            stored_data,
            previews,
            "\n".join(info_outputs),
            "\n".join(summary_outputs),
            "\n".join(missing_outputs),
            {"display": "flex"},
            dash.no_update
        )

    return stored_data, [], "", "", "", {"display": "none"}, dash.no_update