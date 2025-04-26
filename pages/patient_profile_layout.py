import dash_bootstrap_components as dbc
from dash import html, dcc

patient_profile_layout = dbc.Container([
    # Back Button
    dbc.Row([
        dbc.Col(
            dbc.Button("⬅ Back to Dashboard", id="back-to-dashboard-btn", color="secondary", className="mb-4", href="/"),
            width="auto"
        )
    ]),

    # Header Section
    dbc.Row([
        dbc.Col([
            html.H2("👤 Patient Profile", className="fw-bold mb-4 text-center"),
        ])
    ]),

    # Patient Info Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Span("📝 ", style={"fontSize": "1.5rem"}),
                    html.Span("Patient Details", className="card-header text-center")
                ]),
                dbc.CardBody([
                    html.Div([
                        html.H4([html.Span("🙍‍♂️ "), "Name:"], className="fw-bold"),
                        html.P(id="patient-name", className="text-muted mb-3"),
                    ], className="mb-3"),

                    html.H4([html.Span("📋 "), "Basic Info:"], className="fw-bold mt-4"),
                    html.Div(id="patient-info", className="mb-3 patient-info-table"),  # Table will be styled

                    html.H4([html.Span("📎 "), "Uploaded Documents:"], className="fw-bold mt-4"),
                    html.Div(id="uploaded-docs-preview", className="mb-3 uploaded-docs-grid"),

                    html.H4([html.Span("❌ "), "Missing Documents:"], className="fw-bold mt-4"),
                    html.Div(id="missing-docs", className="text-muted"),
                ])
            ], className="shadow-sm")
        ], md=8, className="offset-md-2"),
    ], className="mb-4"),

    # Action Buttons
    dbc.Row([
        dbc.Col(dbc.Button("Reach Out to Patient", id="reach-out-btn", color="primary", className="me-2"), width="auto"),
        dbc.Col(dbc.Button("Submit to Insurance Agency", id="submit-btn", color="success"), width="auto"),
    ], justify="center"),

    # Modal for submission confirmation
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Submission Successful!")),
            dbc.ModalBody([
                html.Div(
                    [
                        html.Div("✅", style={"fontSize": "3rem", "color": "#28a745", "textAlign": "center", "marginBottom": "1rem"}),
                        html.Div(
                            "This patient's claim report is submitted to insurance company for approval.",
                            style={"textAlign": "center"}
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
], fluid=True, className="patient-profile-container")