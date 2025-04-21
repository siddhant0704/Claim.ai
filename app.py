from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc

# Import layouts
from pages.dashboard_layout import landing_page_layout
from pages.upload_docs_layout import upload_docs_page_layout

# Import callbacks
from callbacks.dashboard_callback import *
from callbacks.upload_callback import *

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Claims Intake Platform"
server = app.server  # for deployment (e.g. Heroku, Render)

# App layout with location and page content
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="dashboard-data", data=[]),  # Global store for dashboard data
    html.Div(id="page-content"),

    # Hidden container to register all components referenced in callbacks
    html.Div([
        landing_page_layout,
        upload_docs_page_layout
    ], style={"display": "none"})
])

# Callback to dynamically load pages
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/upload":
        return upload_docs_page_layout
    return landing_page_layout  # Default to dashboard

# Run the app
if __name__ == "__main__":
    app.run(debug=True)