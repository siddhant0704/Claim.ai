import dash
import os
import smtplib
from email.mime.text import MIMEText
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

from dash import Input, Output, State, callback, html, ctx
from urllib.parse import parse_qs

@callback(
    Output("dashboard-data", "data", allow_duplicate=True),  # <-- Add allow_duplicate=True
    [
        Input("submit-btn", "n_clicks"),
        Input("reach-out-btn", "n_clicks"),
    ],
    [
        State("url", "search"),
        State("dashboard-data", "data"),
    ],
    prevent_initial_call=True,
)
def update_claim_status(submit_clicks, reach_out_clicks, search, dashboard_data):
    if not dashboard_data:
        return dash.no_update

    query_params = parse_qs(search.lstrip("?"))
    patient_name = query_params.get("patient", [None])[0]
    if not patient_name:
        return dash.no_update

    triggered_id = ctx.triggered_id
    new_status = None
    if triggered_id == "submit-btn":
        new_status = "Submitted for Approval"
    elif triggered_id == "reach-out-btn":
        new_status = "Requested Additional Info"

    if new_status:
        for entry in dashboard_data:
            if entry["name"] == patient_name:
                entry["status"] = new_status
                break
        return dashboard_data

    return dash.no_update

from utils import generate_clarification_message

@callback(
    Output("clarification-modal", "is_open"),
    Output("clarification-message", "children"),
    Input("reach-out-btn", "n_clicks"),
    State("patient-name", "children"),
    State("missing-docs", "children"),
    State("clarification-modal", "is_open"),
    prevent_initial_call=True,
)
def show_clarification_modal(n_clicks, patient_name, missing_docs, is_open):
    if n_clicks:
        message = generate_clarification_message(patient_name, missing_docs)
        return True, message
    return is_open, dash.no_update

@callback(
    Output("clarification-message", "children", allow_duplicate=True),
    Input("send-clarification-email-btn", "n_clicks"),
    State("clarification-email", "value"),
    State("clarification-message", "children"),
    prevent_initial_call=True,
)
def send_clarification_email(n_clicks, recipient_email, message):
    if n_clicks and recipient_email and message:
        # --- Simple SMTP Example (for demo only, not production) ---
        # For production, use Gmail API with OAuth2 for security!
        try:
            sender_email = os.getenv("GMAIL_SENDER_EMAIL")
            sender_password = os.getenv("GMAIL_APP_PASSWORD")
            msg = MIMEText(message)
            msg["Subject"] = "Clarification Needed for Insurance Claim"
            msg["From"] = sender_email
            msg["To"] = recipient_email

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
            return message + "\n\n✅ Email sent successfully!"
        except Exception as e:
            return message + f"\n\n❌ Failed to send email: {e}"
    return message