"""
The modal window provides results of a race
"""
from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
from services import application as app
from services import database
import plotly.graph_objs as go


class DataTableModel(list):
    def __init__(self):
        pass


class GraphBuilder:
    def __init__(self, data_table):
        self.__data_table = data_table

    def build(self, row: int):
        try:
            data = self.__data_table[row]
        except IndexError:
            return None


# df = px.data.iris()  # iris is a pandas DataFrame
# fig = px.scatter(df, x="sepal_width", y="sepal_length")
fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

graph = dcc.Graph(figure=fig)

mw_body = dbc.ModalBody(
    [
        html.Div(id="table_out"),
        graph,
        graph,
    ]
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
