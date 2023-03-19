import json
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dash_table
from services import application as app, database as db, shared_context as ctx
from collections import OrderedDict
from components import modal_window, GraphBuilder
from datetime import datetime


graph_page = html.Div([
    html.H1("График"),
    html.Hr(),
    html.Div(id="test-1"),
    dbc.Button("eeee", id="t"),
])


@app.callback(
    # [Output("driver-1-result", "children"),
    # Output("driver-2-result", "children")],
    Output("test-1", "children"),
    [Input("t", "n_clicks")],
)
def display_click_data():
    print("TTE")
    row = 1
    data = ctx.races_table_data[row]
    data["telemetry"] = json.loads(data["telemetry"])

    start = datetime.fromisoformat(data["started_at"])
    finish = datetime.fromisoformat(data["finished_at"])
    duration = finish - start
    acc = []
    for t in data["telemetry"]:
        acc.append(GraphBuilder(duration.seconds, t).build())
    # html.Div(acc)
    el = html.Div(acc)
    return e1
