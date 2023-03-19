import requests
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from services import application as app


sponsors = ["Sponsor 1", "Sponsor 2", "Sponsor 3", "Sponsor 4"]
race_type = [
    "qualifying",
    "top 32",
    "top 16",
    "top 8",
    "semifinal",
    "battle for 3rd place",
    "final"
]
drivers = [*range(1, 100)]

competitions = ["TEST", "BEST"]

select_sponsor = html.Div([
    dbc.Label("Организатор", html_for="sponsor"),
    dbc.Select(sponsors, sponsors[0], id="sponsor"),
], style={"margin-bottom": "20px"})


select_competition = html.Div([
    dbc.Label("Соревнование", html_for="competition"),
    dbc.Select(competitions, competitions[0], id="competition"),
], style={"margin-bottom": "20px"})

select_race_type = html.Div([
    dbc.Label("Тип гонки", html_for="race_type"),
    dbc.Select(race_type, race_type[0], id="race_type"),
], style={"margin-bottom": "20px"})


select_driver_1 = html.Div([
    dbc.Label("Гонщик 1", html_for="sponsor"),
    dbc.Select(drivers, drivers[0], id="driver_1"),
], style={"margin-bottom": "20px"})


driver_2 = dbc.Select(drivers, drivers[0], id="driver_2", disabled=True)
select_driver_2 = html.Div([
    dbc.Label("Гонщик 2", html_for="sponsor"),
    driver_2,
], style={"margin-bottom": "20px"})


select_pair_race = html.Div([
    # dbc.Label("Парная гонка"),
    dbc.Checklist(
        options=[{"label": "Парная гонка", "value": 1}],
        switch=True,
        value=[],
        id="select_pair_race",
    )],
    style={"margin-bottom": "20px"}
)


fields = [
    dbc.Row([dbc.Col(select_sponsor)]),
    dbc.Row([dbc.Col(select_race_type)]),
    dbc.Row([dbc.Col(select_pair_race)]),
    dbc.Row([dbc.Col(select_driver_1), dbc.Col(select_driver_2)]),
]


form = dbc.Form([
    dbc.Row([
        dbc.Col(fields),
    ], style={"padding-left": "25px", "padding-right": "25px"}),
])


button_block = html.Div([
    dbc.Button(
        "Запуск",
        id="submit_btn",
        outline=True,
        size="md",
        color="primary",
        className="me-1",
        n_clicks=0,
    ),
], className="d-grid gap-2"),


setting_race_params = dbc.Card([
    dbc.CardHeader("Параметры гонки"),
    dbc.CardBody([form]),
    dbc.CardFooter(button_block),
])


new_competition_page = html.Div([
    html.H1("Новое соревнование"),
    html.Hr(),
])
