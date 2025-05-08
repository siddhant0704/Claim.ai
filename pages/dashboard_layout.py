import dash_bootstrap_components as dbc
from dash import html, dcc

landing_page_layout = dbc.Container([
    # Header section
    dbc.Row([
        dbc.Col([
            html.H2("📋 Welcome to ClaimPal Dashboard!", className="fw-bold mb-2"),
            html.P(
                "Easily manage, upload, and track patient claim documents. Streamline your claims processing workflow.",
                className="text-muted"
            )
        ], md=12),
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

    # Move Edit/Add Patient buttons here
    dbc.Row([
        dbc.Col(
            dbc.Button("Delete Selected", id="delete-selected-btn", color="danger", style={"display": "none"}),
            width="auto"
        ),
        dbc.Col(
            dbc.Button("Add Patient", id="add-patient-btn", color="secondary"),
            width="auto"
        ),
        dbc.Col(
            dbc.Button("Edit", id="edit-table-btn", color="warning"),
            width="auto"
        ),
    ], className="align-items-center mb-2 justify-content-end", justify="end"),

    html.Hr(style={"margin": "2rem 0"}), 

    dcc.Store(id="edit-mode", data=False),
    dcc.Store(id="selected-rows", data=[]),

    dcc.Loading(
        id="loading-table",
        type="circle",
        children=[
            dbc.Table([
                html.Thead(
                    html.Tr([
                        html.Th("", id="select-all-header"),  # For checkboxes
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
    ),

    dbc.Modal(
        [
            dbc.ModalHeader("Confirm Deletion"),
            dbc.ModalBody("Are you sure you want to delete the selected entries?"),
            dbc.ModalFooter([
                dbc.Button("Cancel", id="cancel-delete-btn", color="secondary", className="me-2"),
                dbc.Button("Delete", id="confirm-delete-btn", color="danger"),
            ]),
        ],
        id="delete-confirm-modal",
        is_open=False,
        centered=True,
    ),
], fluid=True, className="dashboard-container")