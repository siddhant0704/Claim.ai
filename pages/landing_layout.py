import dash_bootstrap_components as dbc
from dash import html

landing_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.Div([
                        # Modern text-based logo with gradient
                        html.Div([
                            html.H1(
                                [
                                    html.Span("Claim", style={
                                        "fontWeight": "700",
                                        "color": "#1a3c60",
                                        "fontFamily": "'Inter', sans-serif"
                                    }),
                                    html.Span("Pal", style={
                                        "fontWeight": "700",
                                        "background": "linear-gradient(90deg, #007bff 0%, #00c6ff 100%)",
                                        "WebkitBackgroundClip": "text",
                                        "WebkitTextFillColor": "transparent",
                                        "fontFamily": "'Inter', sans-serif"
                                    }),
                                ],
                                className="display-3 fw-bold text-center mb-2",
                                style={"letterSpacing": "1px", "marginTop": "2.5rem"}
                            ),
                            html.P(
                                "AI-driven insurance claims for disaster zones — accelerating patient care, reducing paperwork, and saving lives.",
                                className="lead text-center mb-4",
                                style={"fontSize": "1.2rem", "color": "#495057", "fontWeight": "500"}
                            ),
                        ]),
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
                                [
                                    html.Img(
                                        src="https://img.icons8.com/color/24/000000/google-logo.png",
                                        style={"marginRight": "8px", "marginBottom": "3px"}
                                    ),
                                    "Login with Google"
                                ],
                                href="/login",
                                className="btn btn-outline-primary btn-md px-4 py-2 shadow-sm d-inline-flex align-items-center",
                                style={
                                    "fontWeight": "500",
                                    "fontSize": "1rem",
                                    "letterSpacing": "0.5px",
                                    "marginTop": "1.5rem"
                                }
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