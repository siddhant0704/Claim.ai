import dash_bootstrap_components as dbc
from dash import html

landing_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.Div([
                        html.Img(
                            src="https://img.icons8.com/ios-filled/100/4a90e2/medical-doctor.png",
                            style={"height": "70px", "marginBottom": "1.5rem"},
                            className="mx-auto d-block"
                        ),
                        html.H1(
                            "ClaimPal.ai",
                            className="display-3 fw-bold text-center mb-2",
                            style={"color": "#1a3c60", "letterSpacing": "1px"}
                        ),
                        html.P(
                            "AI-powered insurance claims for healthcare — built for speed, accuracy, and resilience in disaster zones.",
                            className="lead text-center mb-4",
                            style={"fontSize": "1.25rem", "color": "#495057"}
                        ),
                        dbc.Row([
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H5("Our Purpose", className="fw-bold", style={"color": "#007bff"}),
                                        html.P(
                                            "Accelerate patient care by eliminating paperwork bottlenecks and empowering hospitals to process claims in real time.",
                                            className="mb-0",
                                            style={"fontSize": "1.05rem"}
                                        ),
                                    ]),
                                    className="shadow-sm border-0",
                                    style={"backgroundColor": "#f8f9fa"}
                                ),
                                md=6
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H5("Our Goal", className="fw-bold", style={"color": "#007bff"}),
                                        html.P(
                                            "Deliver a seamless, intuitive platform that transforms insurance claims into a fast, reliable, and stress-free experience — even in the toughest situations.",
                                            className="mb-0",
                                            style={"fontSize": "1.05rem"}
                                        ),
                                    ]),
                                    className="shadow-sm border-0",
                                    style={"backgroundColor": "#f8f9fa"}
                                ),
                                md=6
                            ),
                        ], className="mb-4 mt-2 g-3"),
                        html.Div(
                            html.A(
                                "Login with Google",
                                href="/login",
                                className="btn btn-primary btn-lg px-5 py-3 shadow d-block mx-auto",
                                style={"fontWeight": "600", "fontSize": "1.15rem", "letterSpacing": "0.5px"}
                            ),
                            className="text-center"
                        ),
                    ], className="mt-5 mb-5"),
                ],
                md=10,
                className="offset-md-1"
            )
        ),
    ],
    fluid=True,
    className="landing-page-container"
)