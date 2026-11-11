"""
IBM Applied Data Science Capstone — SpaceX Falcon 9 Interactive Dashboard
Execute the notebook first to generate outputs/spacex_launch_dash.csv.
Run: pip install -r requirements.txt && python app.py
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

DATA_PATH = Path("outputs/spacex_launch_dash.csv")
if not DATA_PATH.exists():
    raise FileNotFoundError(
        "Run notebooks/SpaceX_Capstone_End_to_End.ipynb first. "
        "It creates outputs/spacex_launch_dash.csv."
    )

data = pd.read_csv(DATA_PATH)
app = Dash(__name__)
app.title = "SpaceX Falcon 9 Landing Analytics"
sites = sorted(data["LaunchSite"].dropna().unique())

app.layout = html.Div([
    html.H1("SpaceX Falcon 9 — Landing Analytics",
            style={"textAlign": "center", "color": "#12304A"}),
    html.Div([
        html.Label("Select launch site"),
        dcc.Dropdown(
            id="launch-site",
            options=[{"label": site, "value": site} for site in sites],
            value=sites[0] if sites else None,
            clearable=False
        ),
        html.Label("Payload mass range (kg)", style={"marginTop": "18px"}),
        dcc.RangeSlider(
            id="payload-range",
            min=float(data["PayloadMass"].min()),
            max=float(data["PayloadMass"].max()),
            value=[float(data["PayloadMass"].min()), float(data["PayloadMass"].max())],
            step=100,
            tooltip={"placement": "bottom", "always_visible": False}
        )
    ], style={"maxWidth": "850px", "margin": "auto", "padding": "20px"}),
    html.Div(id="dashboard-output",
             style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px"})
], style={"fontFamily": "Arial", "padding": "24px", "backgroundColor": "#F4F7FB"})

@app.callback(
    Output("dashboard-output", "children"),
    Input("launch-site", "value"),
    Input("payload-range", "value")
)
def update_dashboard(site, payload_range):
    filtered = data[
        (data["LaunchSite"] == site) &
        (data["PayloadMass"].between(payload_range[0], payload_range[1]))
    ].copy()

    if filtered.empty:
        return html.Div("No records match the selected filters.")

    counts = (
        filtered["Class"].map({0: "Unsuccessful landing", 1: "Successful landing"})
        .value_counts().rename_axis("Landing outcome").reset_index(name="Launch count")
    )
    pie = px.pie(counts, names="Landing outcome", values="Launch count",
                 title=f"Landing outcomes — {site}")

    scatter = px.scatter(
        filtered, x="PayloadMass", y="Class", color="Class",
        hover_data=[c for c in ["Orbit", "BoosterVersion", "FlightNumber"] if c in filtered],
        title="Payload mass versus landing outcome",
        labels={"PayloadMass": "Payload mass (kg)", "Class": "Landing class (0/1)"}
    )

    orbit = filtered.groupby("Orbit", as_index=False)["Class"].mean()
    orbit_fig = px.bar(orbit, x="Orbit", y="Class",
                       title="Landing success rate by orbit",
                       labels={"Class": "Success rate"})

    if "BoosterVersion" in filtered.columns:
        booster = filtered.groupby("BoosterVersion", as_index=False)["Class"].mean()
        booster_fig = px.bar(booster, x="BoosterVersion", y="Class",
                             title="Landing success rate by booster",
                             labels={"Class": "Success rate"})
    else:
        booster_fig = px.histogram(filtered, x="Class", title="Landing class distribution")

    return [
        dcc.Graph(figure=pie),
        dcc.Graph(figure=scatter),
        dcc.Graph(figure=orbit_fig),
        dcc.Graph(figure=booster_fig)
    ]

if __name__ == "__main__":
    app.run(debug=True)
