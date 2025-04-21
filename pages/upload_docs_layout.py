import dash_bootstrap_components as dbc
from dash import html, dcc

# Layout for the Upload Docs Page (Processing Claims)
upload_docs_page_layout = dbc.Container([
    html.H1("📝 Insurance Claim Processor", className="text-center my-5 text-dark font-weight-bold"),

    html.P(
        "This web app helps you process insurance claims by extracting relevant information from various document types. Upload your claim documents and get a comprehensive report within seconds.",
        className="text-center mb-5 text-muted",
        style={"fontSize": "1.1rem", "maxWidth": "800px", "margin": "0 auto"}
    ),

    # The same upload interface as in your original UI
    dcc.Upload(
        id='upload-docs',
        children=html.Div([
            "📂 Drag and drop or ",
            html.A("select files", className="text-primary fw-bold")
        ]),
        style={
            'width': '100%',
            'height': '150px',
            'lineHeight': '150px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            'backgroundColor': '#e9ecef',
            'cursor': 'pointer',
            'marginBottom': '30px',
            'boxShadow': '0 0 15px rgba(0,0,0,0.1)'
        },
        multiple=True,
        accept=".pdf,.png,.jpg,.jpeg,.mp3,.wav,.m4a"
    ),

    # Buttons (Process and Reset)
    dbc.Row([
        dbc.Col(dbc.Button("🚀 Process Claim", id="submit-btn", color="primary", className="mb-2 w-100"), md=4),
        dbc.Col(dbc.Button("🔄 Start From Beginning", id="reset-btn", color="danger", className="mb-2 w-100"), md=4),
    ], justify="center", className="mb-4", style={"display": "none"}, id="action-buttons"),

    html.Div(id="file-preview", className="mb-4"),

    # Output with spinner
    dcc.Loading(
        id="loading-output",
        type="circle",
        children=[
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader("📋 Combined Info", className="bg-light text-dark font-weight-bold"),
                    dbc.CardBody(dcc.Textarea(id="output-info", style={"width": "100%", "height": "150px", "resize": "none", "border": "none", "fontSize": "1rem"}))
                ]), md=4, className="mb-4"),

                dbc.Col(dbc.Card([
                    dbc.CardHeader("📑 Summary", className="bg-light text-dark font-weight-bold"),
                    dbc.CardBody(dcc.Textarea(id="output-summary", style={"width": "100%", "height": "150px", "resize": "none", "border": "none", "fontSize": "1rem"}))
                ]), md=4, className="mb-4"),

                dbc.Col(dbc.Card([
                    dbc.CardHeader("❌ Missing Documents", className="bg-light text-dark font-weight-bold"),
                    dbc.CardBody(dcc.Textarea(id="output-missing", style={"width": "100%", "height": "150px", "resize": "none", "border": "none", "fontSize": "1rem"}))
                ]), md=4, className="mb-4"),
            ])
        ]
    ),

    # Store uploaded files
    dcc.Store(id="stored-docs", data=[]),

    # Back Button
    dbc.Row([
        dbc.Col(dbc.Button("🔙 Back to Claims", id="back-btn", color="secondary", className="w-100 mb-4", href="/"), md=4),
    ], justify="center"),

], fluid=True)
