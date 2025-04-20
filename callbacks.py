import os
import base64
import tempfile
from dash import Input, Output, State, html
from claim_processor import process_claim_case

def register_callbacks(app):
    @app.callback(
        [Output('file-list', 'children'),
         Output('output-info', 'value'),
         Output('output-summary', 'value'),
         Output('output-missing', 'value')],
        [Input('upload-docs', 'contents')],
        [State('upload-docs', 'filename')],
        prevent_initial_call=True
    )
    def run_claim_processing(contents, filenames):
        if contents is None:
            return ["No files uploaded."], "", "", ""

        file_info = []
        document_list = []

        for content, name in zip(contents, filenames):
            file_path = save_file(name, content)
            file_ext = name.lower().split('.')[-1]

            if file_ext in ["pdf"]:
                file_type = "pdf"
            elif file_ext in ["png", "jpg", "jpeg"]:
                file_type = "image"
            elif file_ext in ["mp3", "wav", "m4a"]:
                file_type = "audio"
            else:
                file_info.append(html.Li(f"{name} ❌ Unsupported file type"))
                continue

            document_list.append((file_path, file_type))
            file_info.append(html.Li(f"{name} ✅"))

        result = process_claim_case(document_list)

        return (
            html.Ul(file_info),
            result.get('combined_info', ''),
            result.get('claim_summary', ''),
            result.get('missing_documents', '')
        )

def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]
    suffix = os.path.splitext(name)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as fp:
        fp.write(base64.b64decode(data))
        return fp.name
