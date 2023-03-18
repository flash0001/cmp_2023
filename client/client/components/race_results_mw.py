"""
The modal window provides results of a race
"""
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
from services import application as app
from services import database
import plotly.graph_objs as go
import numpy as np


class GraphBuilder:
    def __init__(self, duration, data):
        self.duration = duration
        self.driver_id = data["driver_id"]
        self.y = data["telemetry"]
        self.x = list(np.linspace(0, duration, len(self.y)))

    def build(self):
        return dbc.Row([
            dbc.Col([
                html.H4(f"Пилот {self.driver_id}"),
                go.Figure(data=[go.Scatter(x=self.x, y=self.y)])
            ])
        ])


# df = px.data.iris()  # iris is a pandas DataFrame
# fig = px.scatter(df, x="sepal_width", y="sepal_length")
fig = go.Figure(data=[go.Scatter(x=[23, 4, 5], y=[4, 1, 2])])

graph = dcc.Graph(figure=fig)

mw_body = dbc.ModalBody(
    id="modal_body",
)

modal_window = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Результаты заезда")),
        mw_body,
    ],
    id="race_results_window",
    fullscreen=True,
)

__all__ = ["modal_window"]
