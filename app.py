import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
from flask import Flask, redirect, url_for, session, request
from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
REDIRECT_URI = "http://localhost:8050/login/callback"
SCOPE = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]

server = Flask(__name__)
server.secret_key = "Hiral_love" 
# Dash app
app = Dash(__name__, server=server, url_base_pathname='/', suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Claims Intake Platform"

# Import layouts
from pages.dashboard_layout import landing_page_layout
from pages.upload_docs_layout import upload_docs_page_layout
from pages.patient_profile_layout import patient_profile_layout
from pages.landing_layout import landing_layout

# Import callbacks
from callbacks.dashboard_callback import *
from callbacks.upload_callback import *
from callbacks.patient_profile_callback import *

# App layout with location and page content
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="dashboard-data", data=[]),
    html.Div(id="page-content"),
    html.Div([
        landing_page_layout,
        upload_docs_page_layout,
        patient_profile_layout,
        landing_layout,  # Add this
    ], style={"display": "none"})
])

# Flask routes for Google OAuth
@server.route("/login")
def login():
    google = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = google.authorization_url(AUTHORIZATION_BASE_URL, access_type="offline", prompt="select_account")
    session["oauth_state"] = state
    return redirect(authorization_url)

@server.route("/login/callback")
def callback():
    if "oauth_state" not in session:
        return redirect("/login")
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=session["oauth_state"])
    token = google.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)
    session["oauth_token"] = token
    print("User logged in successfully!") 
    return redirect("/")

@server.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@server.before_request
def require_login():
    # Allow landing page ("/"), login, callback, static, and favicon without auth
    if request.path in ["/", "/login", "/login/callback", "/favicon.ico"] or \
       request.path.startswith("/static") or request.path.startswith("/_dash"):
        return
    if "oauth_token" not in session:
        return redirect("/login")

# Callback to dynamically load pages
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    State("dashboard-data", "data")
)
def display_page(pathname, dashboard_data):
    if "oauth_token" not in session:
        return landing_layout
    if pathname == "/upload":
        return upload_docs_page_layout
    elif pathname.startswith("/profile"):
        return patient_profile_layout
    elif pathname == "/":
        return landing_page_layout
    return landing_page_layout

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)
