import dash_bootstrap_components as dbc
from dash import html, dcc

landing_page_layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H2("Claims Dashboard", className="fw-bold mb-1", style={"letterSpacing": "1px", "color": "#1a3c60"}),
            html.P(
                "Monitor, manage, and process patient insurance claims efficiently.",
                className="text-muted",
                style={"fontSize": "1.1rem", "marginBottom": "0"}
            ),
        ], md=8),
    ], className="align-items-center mb-3"),

    # Metrics Row as Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Total Patients", className="metric-label mb-2", style={"color": "#6c757d"}),
                html.H2(id="metric-total", className="metric-value mb-0", style={"fontWeight": "700", "color": "#1a3c60"})
            ])
        ], className="shadow-sm metric-card", style={"border": "none"}), md=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Under Review", className="metric-label mb-2", style={"color": "#6c757d"}),
                html.H2(id="metric-under-approval", className="metric-value mb-0", style={"fontWeight": "700", "color": "#198754"})
            ])
        ], className="shadow-sm metric-card", style={"border": "none"}), md=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Pending", className="metric-label mb-2", style={"color": "#6c757d"}),
                html.H2(id="metric-pending", className="metric-value mb-0", style={"fontWeight": "700", "color": "#ffc107"})
            ])
        ], className="shadow-sm metric-card", style={"border": "none"}), md=4),
    ], className="mb-4 g-3"),

    # Action Buttons (right-aligned)
    dbc.Row([
        dbc.Col(width=6),  # Spacer
        dbc.Col([
            dbc.Button("Add Patient", id="add-patient-btn", color="primary", className="me-2", n_clicks=0, style={"minWidth": "130px", "fontWeight": "600"}),
            dbc.Button("Edit", id="edit-table-btn", color="secondary", className="me-2", n_clicks=0, style={"minWidth": "100px", "fontWeight": "600"}),
            dbc.Button("Delete Selected", id="delete-selected-btn", color="danger", style={"display": "none", "minWidth": "160px", "fontWeight": "600"}),
        ], width="auto", style={"textAlign": "right"})
    ], className="mb-3 justify-content-end"),

    # Table Section in Card
    dbc.Card([
        dbc.CardHeader([
            html.H5("Patient Claims", className="mb-0", style={"fontWeight": "600", "color": "#1a3c60"}),
        ], className="bg-white border-bottom-0"),
        dbc.CardBody([
            dcc.Loading(
                id="loading-table",
                type="circle",
                children=[
                    dbc.Table([
                        html.Thead(
                            html.Tr([
                                html.Th("", id="select-all-header"),
                                html.Th("Patient Name", className="fw-bold mb-2 text-start", style={"color": "#495057"}),
                                html.Th("Summary", className="fw-bold mb-2 text-start", style={"color": "#495057"}),
                                html.Th("Claim Status", className="fw-bold mb-2 text-center", style={"color": "#495057"})
                            ], className="table-header sticky-top")
                        ),
                        html.Tbody([], id="patient-table-body")
                    ],
                        bordered=False,
                        hover=True,
                        responsive=True,
                        striped=True,
                        className="patient-table shadow-sm",
                        style={"borderRadius": "12px", "overflow": "hidden"}
                    )
                ]
            ),
        ], style={"padding": "0.5rem 0.5rem 0.5rem 0.5rem"})
    ], className="mb-4 shadow-sm"),

    # Delete Confirmation Modal
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
    dcc.Store(id="edit-mode", data=False),
    dcc.Store(id="selected-rows", data=[]),
], fluid=True, className="dashboard-container")