import dash_bootstrap_components as dbc
from dash import html, dcc

upload_docs_page_layout = dbc.Container([

    # Header section
    dbc.Row([
        dbc.Col([
            html.H2("📝 Insurance Claim Processor", className="fw-bold mb-2"),
            html.P(
                "Upload your claim documents and extract insights instantly. Supported formats include PDFs, images, and audio files.",
                className="text-muted"
            )
        ], md=8),
    ], className="align-items-center mb-4"),

    dcc.Upload(
        id='upload-docs',
        children=html.Div([
            "📂 Drag and drop or ",
            html.A("select files", className="upload-link")
        ]),
        className="upload-box",
        multiple=True,
        accept=".pdf,.png,.jpg,.jpeg,.mp3,.wav,.m4a"
    ),

    dbc.Row([
        dbc.Col(dbc.Button("🚀 Process Claim", id="submit-btn", color="primary", className="action-btn"), md=4),
        dbc.Col(dbc.Button("🔄 Start Over", id="reset-btn", color="danger", className="action-btn"), md=4),
    ], justify="center", id="action-buttons", className="hidden"),

    html.Div(id="file-preview", className="mb-4"),

    dcc.Loading(
        id="loading-output",
        type="circle",
        children=[
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader("📋 Combined Info", className="card-header"),
                    dbc.CardBody(
                        dcc.Textarea(id="output-info", className="output-textarea")
                    )
                ]), md=4, className="mb-4"),

                dbc.Col(dbc.Card([
                    dbc.CardHeader("📑 Summary", className="card-header"),
                    dbc.CardBody(
                        dcc.Textarea(id="output-summary", className="output-textarea")
                    )
                ]), md=4, className="mb-4"),

                dbc.Col(dbc.Card([
                    dbc.CardHeader("❌ Missing Documents", className="card-header"),
                    dbc.CardBody(
                        dcc.Textarea(id="output-missing", className="output-textarea")
                    )
                ]), md=4, className="mb-4"),
            ])
        ]
    ),

    dcc.Store(id="stored-docs", data=[]),

    dbc.Row([
        dbc.Col(dbc.Button("⬅️ Upload to Dashboard", id="back-btn", color="secondary", className="back-btn", href="/")),
    ], justify="center"),

], fluid=True, className="upload-page-container")
