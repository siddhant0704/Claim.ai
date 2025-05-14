import dash_bootstrap_components as dbc
from dash import html, dcc

patient_profile_layout = dbc.Container([
    # Back Button
    dbc.Row([
        dbc.Col(
            dbc.Button("Back to Dashboard", id="back-to-dashboard-btn", color="secondary", className="mb-4", href="/", style={"fontWeight": "500"}),
            width="auto"
        )
    ]),

    # Header Section
    dbc.Row([
        dbc.Col([
            html.H2("Patient Profile", className="fw-bold mb-2", style={"letterSpacing": "1px", "color": "#1a3c60"}),
            html.P(
                "Detailed view of patient claim, uploaded documents, and extracted information.",
                className="text-muted",
                style={"fontSize": "1.1rem", "marginBottom": "0"}
            ),
        ], md=8),
    ], className="align-items-center mb-4"),

    # Patient Info Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Patient Details", className="card-header"),
                dbc.CardBody([
                    html.Div([
                        html.H5("Name", className="fw-bold mb-1", style={"color": "#1a3c60"}),
                        html.P(id="patient-name", className="text-muted mb-3", style={"fontSize": "1.1rem"}),
                    ], className="mb-3"),

                    html.H5("Basic Info", className="fw-bold mt-4 mb-2", style={"color": "#1a3c60"}),
                    html.Div(id="patient-info", className="mb-3 patient-info-table"),

                    html.H5("Uploaded Documents", className="fw-bold mt-4 mb-2", style={"color": "#1a3c60"}),
                    html.Div(id="uploaded-docs-preview", className="mb-3 uploaded-docs-grid"),

                    html.H5("Missing Documents", className="fw-bold mt-4 mb-2", style={"color": "#1a3c60"}),
                    html.Div(id="missing-docs", className="text-muted"),
                ])
            ], className="shadow-sm")
        ], md=8, className="offset-md-2"),
    ], className="mb-4"),

    # Action Buttons
    dbc.Row([
        dbc.Col(dbc.Button("Reach Out to Patient", id="reach-out-btn", color="primary", className="me-2 action-btn"), width="auto"),
        dbc.Col(dbc.Button("Submit to Insurance Agency", id="submit-btn", color="success", className="action-btn"), width="auto"),
    ], justify="center", className="mb-4"),

    # Modal for submission confirmation
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Submission Successful!")),
            dbc.ModalBody([
                html.Div(
                    [
                        html.Div(
                            "This patient's claim report is submitted to insurance company for approval.",
                            style={"textAlign": "center", "fontWeight": "500", "color": "#198754"}
                        )
                    ]
                )
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-submit-modal", className="ms-auto", n_clicks=0)
            ),
        ],
        id="submit-modal",
        is_open=False,
        centered=True,
    ),
    dbc.Modal(
        [
            dbc.ModalHeader("Clarification Request Template"),
            dbc.ModalBody([
                html.Div([
                    dbc.Label("Recipient Email", html_for="clarification-email"),
                    dbc.Input(type="email", id="clarification-email", placeholder="Enter recipient email", className="mb-2"),
                ]),
                html.Pre(id="clarification-message", style={"whiteSpace": "pre-wrap"}),
            ]),
            dbc.ModalFooter([
                dbc.Button("Send Email", id="send-clarification-email-btn", color="primary", className="me-2"),
                dbc.Button("Close", id="close-clarification-modal", className="ms-auto")
            ]),
        ],
        id="clarification-modal",
        is_open=False,
        centered=True,
    ),
], fluid=True, className="patient-profile-container")