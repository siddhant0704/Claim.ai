import dash_bootstrap_components as dbc
from dash import html

landing_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H1("ClaimPal.ai", className="display-3 fw-bold mb-3 text-center"),
                    html.P(
                        "Smart Document Understanding and Reasoning Engine for Healthcare Claims.",
                        className="lead text-center mb-4"
                    ),
                    html.Div(
                        html.A(
                            "Login with Google",
                            href="/login",
                            className="btn btn-primary btn-lg d-block mx-auto",
                            style={"textDecoration": "none"}
                        ),
                        className="text-center"
                    ),
                ],
                md=8,
                className="offset-md-2 mt-5"
            )
        ),
    ],
    fluid=True,
    className="landing-page-container"
)