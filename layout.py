from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("📝 Insurance Claim Processor", className="text-center my-5 text-dark font-weight-bold"),

    html.P(
        "This web app helps you process insurance claims by extracting relevant information from various document types. Upload your claim documents and get a comprehensive report within seconds.",
        className="text-center mb-5 text-muted", style={"fontSize": "1.1rem", "maxWidth": "800px", "margin": "0 auto"}
    ),
    
    # Upload Section
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

    dbc.Button("🚀 Process Claim", id="submit-btn", color="primary", className="mx-auto d-block mb-4 py-2 px-4 font-weight-bold"),

    # Loading spinner and file processing output
    dcc.Loading(
        id="loading-output",
        type="circle",
        children=[
            html.Div(id="file-list", className="mb-4"),
            dbc.Row([
                # Cards for displaying processed output
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
], fluid=True)
