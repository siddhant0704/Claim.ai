import dash_bootstrap_components as dbc
from dash import html, dcc

landing_page_layout = dbc.Container([
    html.H1("Patient Claims Overview", className="text-center my-5 text-dark font-weight-bold"),

    html.P(
        "View and manage patient claims here. You can add a new patient, upload their documents, and get the claim status.",
        className="text-center mb-5 text-muted",
        style={"fontSize": "1.1rem", "maxWidth": "800px", "margin": "0 auto"}
    ),

    dbc.Table(
        [
            html.Thead(
                html.Tr([html.Th("Patient Name"), html.Th("Claim Summary"), html.Th("Claim Status"), html.Th("Actions")])
            ),
            html.Tbody([], id="patient-table-body")
        ],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
    ),

    dbc.Row([
        dbc.Col(
            dbc.Button("Add Patient", id="add-patient-btn", color="primary", className="mb-4 w-100"),
            md=4
        ),
    ], justify="center"),
], fluid=True)
