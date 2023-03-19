import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from services import application as app
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from services import application as app
from services import database as db, HTTPClient


route_field = html.Div([
    dbc.Label("Список координат точек", html_for="route"),
    dbc.Input(id="route"),
], style={"margin-bottom": "20px"})

fields = [
    dbc.Row([dbc.Col(route_field)]),
]

form = dbc.Form([
    dbc.Row([
        dbc.Col(fields),
    ], style={"padding-left": "25px", "padding-right": "25px"}),
])

save_route = html.Div([
    dbc.Button(
        "Сохранить",
        id="save_route",
        size="md",
        color="primary",
        className="me-1",
        n_clicks=0,
        disabled=False,
    ),
], className="d-grid gap-2")

route_form = dbc.Card([
    dbc.CardHeader("Новый маршрут полёта"),
    dbc.CardBody([form]),
    dbc.CardFooter(
        dbc.Row([
            dbc.Col(save_route),
        ])
    ),
    html.Div(id="dummy_out-1", style={"visibility": "hidden"}),
])


route_page = html.Div([
    html.H1("Маршрут полёта"),
    html.Hr(),
    dbc.Row([
        dbc.Col(route_form),
    ]),
])


@app.callback(
    Output("dummy_out-1", "children"),
    [Input("save_route", "n_clicks")],
    State("route", "value"),
)
def on_click_star_race(n_click, value):
    if n_click:
        print(value)
