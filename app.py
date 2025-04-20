import dash
from dash import Dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])  # A cleaner theme (LUX)
server = app.server
app.title = "Insurance Claim Assistant"

# Set layout
app.layout = layout

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
