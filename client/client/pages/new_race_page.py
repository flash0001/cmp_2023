import requests
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from services import application as app
from services import dbservice as db
from components import race_form, competition_form


new_race_page = html.Div([
    html.H1("Панель управления"),
    html.Hr(),
    dbc.Row([
        dbc.Col(competition_form),
        dbc.Col(race_form),
    ]),
    dbc.Row([
        dbc.Col(width=4),
        dbc.Col(html.Div([dbc.Spinner(color="primary", type="grow")])),
        dbc.Col(html.Div([dbc.Spinner(color="primary", type="grow")])),
        dbc.Col(html.Div([dbc.Spinner(color="primary", type="grow")])),
        dbc.Col(width=4),
    ], style={"visibility": "hidden", "margin-top": "-40px", "padding-left": "40px"}),
    # html.Div([setting_race_params], className="py-2"),
    html.Div(id="container-button-basic-1"),
    html.Div(id="container-button-basic-2"),
])
