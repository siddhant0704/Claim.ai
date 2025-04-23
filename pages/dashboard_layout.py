
import dash_bootstrap_components as dbc
from dash import html, dcc

landing_page_layout = dbc.Container([
    html.H1("📋 Patient Claims Dashboard", className="dashboard-title"),

    html.P(
        "Efficiently manage patient claims. Use the dashboard to view details, upload documents, and track claim status.",
        className="dashboard-subtitle"
    ),

    dbc.Row([
        dbc.Col(
            dbc.Button("➕ Add Patient", id="add-patient-btn", color="primary", className="add-patient-btn"),
            width="auto",
            className="ms-auto"
        )
    ]),

    dcc.Loading(
        id="loading-table",
        type="circle",
        children=[
            dbc.Table([
                html.Thead(
                    html.Tr([
                        html.Th("Patient Name", className="table-header"),
                        html.Th("Claim Status", className="table-header"),
                        html.Th("Actions", className="table-header")
                    ])
                ),
                html.Tbody([], id="patient-table-body")
            ],
                bordered=True,
                hover=True,
                responsive=True,
                striped=True,
                className="patient-table"
            )
        ]
    )
], fluid=True, className="dashboard-container")