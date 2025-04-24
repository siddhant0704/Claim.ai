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
                dbc.CardHeader("Patient Details", className="card-header text-center"),
                dbc.CardBody([
                    html.H4("Name:", className="fw-bold"),
                    html.P(id="patient-name", className="text-muted mb-3"),  # Patient name will be dynamically populated

                    html.H4("Basic Info:", className="fw-bold mt-4"),
                    html.Div(id="patient-info", className="text-muted mb-3"),  # Parsed info will be dynamically populated

                    html.H4("Missing Documents:", className="fw-bold mt-4"),
                    html.Div(id="missing-docs", className="text-muted"),  # Missing documents will be dynamically populated
                ])
            ], className="shadow-sm")
        ], md=8, className="offset-md-2"),  # Center the card
    ], className="mb-4"),

    # Action Buttons
    dbc.Row([
        dbc.Col(dbc.Button("Reach Out to Patient", id="reach-out-btn", color="primary", className="me-2"), width="auto"),
        dbc.Col(dbc.Button("Submit to Insurance Agency", id="submit-btn", color="success"), width="auto"),
    ], justify="center"),
], fluid=True, className="patient-profile-container")