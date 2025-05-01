import dash_bootstrap_components as dbc
from dash import html, dcc

landing_page_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("📋 Welcome to ClaimPal Dashboard!", className="fw-bold mb-2"),
            html.P(
                "Easily manage, upload, and track patient claim documents. Streamline your claims processing workflow.",
                className="text-muted"
            )
        ], md=8),
        dbc.Col(
            dbc.Button("Add Patient", id="add-patient-btn", color="secondary", className="mt-3 mt-md-0 float-md-end"),
            md=4
        )
    ], className="align-items-center mb-4"),

    # Metrics Row
    dbc.Row([
        dbc.Col(html.Div([
            html.H5("Total Patients", className="metric-label"),
            html.H3(id="metric-total", className="metric-value")
        ], className="metric-card text-center"), md=4),
        dbc.Col(html.Div([
            html.H5("Under Review", className="metric-label"),
            html.H3(id="metric-under-approval", className="metric-value text-success")
        ], className="metric-card text-center"), md=4),
        dbc.Col(html.Div([
            html.H5("Pending", className="metric-label"),
            html.H3(id="metric-pending", className="metric-value text-warning")
        ], className="metric-card text-center"), md=4),
    ], className="mb-4"),

    html.Hr(style={"margin": "2rem 0"}), 

    dcc.Loading(
        id="loading-table",
        type="circle",
        children=[
            dbc.Table([
                html.Thead(
                    html.Tr([
                        html.Th("👤 Patient Name", className="fw-bold mb-2"),
                        html.Th("📝 Summary", className="fw-bold mb-2"), 
                        html.Th("📄 Claim Status", className="fw-bold mb-2")

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
        ], 
    )
], fluid=True, className="dashboard-container")