import dash_bootstrap_components as dbc
from dash import html, dcc

upload_docs_page_layout = dbc.Container([
    # Back Button (top left)
    dbc.Row([
        dbc.Col(
            dbc.Button(
                "Back to Dashboard",
                id="upload-back-btn",
                color="secondary",
                className="mb-4",
                href="/",
                style={"fontWeight": "500"}
            ),
            width="auto"
        )
    ], className="mb-2"),

    # Header Section
    dbc.Row([
        dbc.Col([
            html.H2("Upload Documents", className="fw-bold mb-1", style={"letterSpacing": "1px", "color": "#1a3c60"}),
            html.P(
                "Upload patient documents for claim processing. Supported formats: PDF, JPG, PNG.",
                className="text-muted",
                style={"fontSize": "1.1rem", "marginBottom": "0"}
            ),
        ], md=8),
    ], className="align-items-center mb-4"),

    # Upload Section (Card 1) with Action Buttons
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Upload Files", className="fw-bold mb-3", style={"color": "#1a3c60"}),
                    dcc.Upload(
                        id="upload-docs",
                        children=html.Div([
                            "Drag and drop files here, or ",
                            html.A("browse", style={"color": "#007bff", "textDecoration": "underline"})
                        ]),
                        style={
                            "width": "100%",
                            "height": "180px",
                            "lineHeight": "180px",
                            "borderWidth": "2px",
                            "borderStyle": "dashed",
                            "borderRadius": "10px",
                            "textAlign": "center",
                            "backgroundColor": "#f8f9fa",
                            "color": "#6c757d",
                        },
                        multiple=True
                    ),
                    html.Div(id="file-preview", className="mt-3", style={"fontSize": "0.9rem", "color": "#495057"}),
                    html.Div(
                        [
                            dbc.Button("Submit", id="upload-submit-btn", color="primary", className="me-2", n_clicks=0, style={"minWidth": "120px", "fontWeight": "600"}),
                            dbc.Button("Reset", id="upload-reset-btn", color="secondary", n_clicks=0, style={"minWidth": "120px", "fontWeight": "600"}),
                        ],
                        id="action-buttons",
                        className="d-flex justify-content-center gap-3 mt-4"
                    ),
                ])
            ], className="shadow-sm mb-4"),
            md=12, className="mx-auto"
        )
    ]),

    # Output Section (Card 2)
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Processing Results", className="fw-bold mb-3", style={"color": "#1a3c60"}),
                    dcc.Loading(
                        id="loading-output",
                        type="circle",
                        children=[
                            dbc.Row([
                                dbc.Col([
                                    html.P("Patient Info:", className="fw-bold mb-1", style={"color": "#495057"}),
                                    dcc.Textarea(
                                        id="output-info",
                                        className="form-control mb-3",
                                        style={"height": "180px", "resize": "none"},
                                        readOnly=True
                                    ),
                                ], md=4),
                                dbc.Col([
                                    html.P("Summary:", className="fw-bold mb-1", style={"color": "#495057"}),
                                    dcc.Textarea(
                                        id="output-summary",
                                        className="form-control mb-3",
                                        style={"height": "180px", "resize": "none"},
                                        readOnly=True
                                    ),
                                ], md=4),
                                dbc.Col([
                                    html.P("Missing Documents:", className="fw-bold mb-1", style={"color": "#495057"}),
                                    dcc.Textarea(
                                        id="output-missing",
                                        className="form-control",
                                        style={"height": "180px", "resize": "none"},
                                        readOnly=True
                                    ),
                                ], md=4),
                            ], className="g-3"),
                        ]
                    ),
                ]),
            ], className="shadow-sm"),
            md=12, className="mx-auto"
        )
    ]),

    dcc.Store(id="stored-docs", data=[]),
], fluid=True, className="upload-container")