from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

# Import layouts
from pages.dashboard_layout import landing_page_layout
from pages.upload_docs_layout import upload_docs_page_layout

# Import callbacks
from callbacks.dashboard_callback import dashboard_callback
from callbacks.upload_callback import upload_callback

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Claims Intake Platform"
server = app.server  # for deployment (e.g. Heroku, Render)

# App layout with location and page content
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="navigation-store"),  # Store for navigation
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

# Navigation callback
@app.callback(
    Output("url", "pathname"),
    Input("navigation-store", "data"),
    prevent_initial_call=True
)
def navigate(data):
    return data

# Run the app
if __name__ == "__main__":
    app.run(debug=True)