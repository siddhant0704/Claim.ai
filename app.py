from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_sqlalchemy import SQLAlchemy
import os

# Flask server for Dash
server = Flask(__name__)
server.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

# Configure Google OAuth
google_blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to="google_login"
)
server.register_blueprint(google_blueprint, url_prefix="/login")

# Configure SQLAlchemy for database
server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///claims.db"
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(server)

# Define a database model for storing processed claims
class ProcessedClaim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    combined_info = db.Column(db.Text, nullable=False)
    claim_summary = db.Column(db.Text, nullable=False)
    missing_documents = db.Column(db.Text, nullable=False)

# Initialize the database
with server.app_context():
    db.create_all()

# Dash app
app = Dash(__name__, server=server, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Claims Intake Platform"

# Import layouts
from pages.dashboard_layout import landing_page_layout
from pages.upload_docs_layout import upload_docs_page_layout

# Import callbacks
from callbacks.dashboard_callback import *
from callbacks.upload_callback import *

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
    if not google.authorized:
        return html.Div([
            html.H1("Please log in with Google"),
            html.A("Log in with Google", href=url_for("google.login"))
        ])
    if pathname == "/upload":
        return upload_docs_page_layout
    return landing_page_layout  # Default to dashboard

# Route to handle Google login
@server.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    user_info = resp.json()
    return redirect("/")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)