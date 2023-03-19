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
