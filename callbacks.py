import os
import base64
import tempfile
import dash
from dash import Input, Output, State, html, ctx, dcc
from claim_processor import process_claim_case


def register_callbacks(app):
    @app.callback(
        Output("stored-docs", "data"),
        Output("file-preview", "children"),
        Output("output-info", "value"),
        Output("output-summary", "value"),
        Output("output-missing", "value"),
        Output("action-buttons", "style"),
        Input("upload-docs", "contents"),
        Input("submit-btn", "n_clicks"),
        Input("reset-btn", "n_clicks"),
        State("upload-docs", "filename"),
        State("stored-docs", "data"),
        prevent_initial_call=True
    )
    def handle_all_actions(contents, submit_clicks, reset_clicks, filenames, stored):
        triggered_id = ctx.triggered_id

        # RESET
        if triggered_id == "reset-btn":
            return [], [], "", "", "", {"display": "none"}

        # UPLOAD
        if triggered_id == "upload-docs":
            if not contents:
                return stored, [], "", "", "", {"display": "none"}

            previews = []
            new_data = stored.copy()
            for content, filename in zip(contents, filenames):
                ext = filename.split('.')[-1].lower()
                label = "📄 PDF" if ext == "pdf" else "🖼 Image" if ext in ["jpg", "jpeg", "png"] else "🔊 Audio"
                previews.append(
                    html.Div([
                        html.Img(src=content, style={"maxHeight": "120px"}) if "image" in content else html.P(f"{filename} ({label})"),
                        html.P(f"{filename} - {label}", className="text-muted text-center", style={"fontSize": "0.9rem"})
                    ], style={"margin": "10px"}, className="d-inline-block")
                )
                new_data.append({"filename": filename, "content": content})

            return new_data, previews, "", "", "", {"display": "flex"}

        # SUBMIT
        if triggered_id == "submit-btn":
            if not stored:
                return dash.no_update, [], "", "", "", {"display": "none"}

            file_list = []
            previews = []

            for doc in stored:
                path = save_file(doc["filename"], doc["content"])
                ext = doc["filename"].split('.')[-1].lower()
                doc_type = "pdf" if ext == "pdf" else "image" if ext in ["jpg", "jpeg", "png"] else "audio"
                file_list.append((path, doc_type))

            result = process_claim_case(file_list)

            for doc in stored:
                label = result.get("labels", {}).get(doc["filename"], "Processed")
                previews.append(
                    html.Div([
                        html.Img(src=doc["content"], style={"maxHeight": "120px"}) if "image" in doc["content"] else html.P(doc["filename"]),
                        html.P(label, className="text-success text-center", style={"fontSize": "0.9rem", "fontWeight": "bold"})
                    ], style={"margin": "10px"}, className="d-inline-block")
                )

            return (
                stored,
                previews,
                result.get("combined_info", ""),
                result.get("claim_summary", ""),
                result.get("missing_documents", ""),
                {"display": "flex"}
            )

        # Fallback
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]
    suffix = os.path.splitext(name)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as fp:
        fp.write(base64.b64decode(data))
        return fp.name
