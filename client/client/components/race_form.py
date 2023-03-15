import requests
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
from services import application as app
from services import dbservice as db


# it loads data from the database
with db.Session() as session:
    race_type_collection = session.scalars(db.select(db.RaceType))
    race_collection = session.scalars(db.select(db.Race))
    driver_collection = session.scalars(db.select(db.Driver))

    race_types = [*map(lambda o: o.name, race_type_collection)]
    is_disabled = not bool([*map(lambda _: _, race_collection)])
    drivers = [*map(lambda o: o.id, driver_collection)]


# the race types
select_race_type = html.Div([
    dbc.Label("Тип гонки", html_for="race_type"),
    dbc.Select(race_types, race_types[0], id="race_type"),
], style={"margin-bottom": "20px"})


# the first driver
select_driver_1 = html.Div([
    dbc.Label("Гонщик 1", html_for="sponsor"),
    dbc.Select(drivers, drivers[0], id="driver_1"),
], style={"margin-bottom": "20px"})

# the second driver
select_driver_2 = html.Div([
    dbc.Label("Гонщик 2", html_for="sponsor"),
    dbc.Select(drivers, drivers[0], id="driver_2", disabled=True),
], style={"margin-bottom": "20px"})


# this checkbox activates the second driver
select_pair_race = html.Div([
    dbc.Label("Парная гонка"),
    dbc.Checklist(
        options=[{"label": "", "value": 1}],
        switch=True,
        value=[],
        id="select_pair_race",
    )],
    style={"margin-bottom": "35px"}
)

# fields of the form
fields = [
    dbc.Row([dbc.Col(select_race_type)]),
    dbc.Row([dbc.Col(select_pair_race)]),
    dbc.Row([dbc.Col(select_driver_1), dbc.Col(select_driver_2)]),
]

# the form
form = dbc.Form([
    dbc.Row([
        dbc.Col(fields),
    ], style={"padding-left": "25px", "padding-right": "25px"}),
])


run_button = html.Div([
    dbc.Button(
        "Запуск",
        id="run_race",
        # outline=True,
        size="md",
        color="primary",
        className="me-1",
        n_clicks=0,
        disabled=is_disabled,
    ),
], className="d-grid gap-2")

stop_button = html.Div([
    dbc.Button(
        "Остановка",
        id="stop_race",
        # outline=True,
        size="md",
        color="secondary",
        className="me-1",
        n_clicks=0,
        disabled=is_disabled,
    ),
], className="d-grid gap-2")

# the component
race_form = dbc.Card([
    dbc.CardHeader("Заезд"),
    dbc.CardBody([form]),
    dbc.CardFooter(
        dbc.Row([
            dbc.Col(stop_button),
            dbc.Col(run_button),
        ])
    ),
    html.Div(id="race_form_dummy_out", style={"visibility": "hidden"})
])


@app.callback(
    Output("driver_2", "disabled"),
    [Input("select_pair_race", "value")],
)
def on_checkbox(values):
    if len(values):
        return False
    return True


@app.callback(
    Output("run_race", "disabled"),
    [Input("add_competition", "n_clicks")],
)
def disable_btn(*value):
    if value[0]:
        return False
    return True


@app.callback(
    Output("race_form_dummy_out", "children"),
    [Input("run_race", "n_clicks")],
    State("race_type", "value"),
    State("driver_1", "value"),
    State("driver_2", "value"),
    State("select_pair_race", "value"),
)
def cb_render(*values):
    data = [v for v in values if v]
    if isinstance(data[0], int):
        data.append([0])
        data = data[1:6]
        data[-1] = bool(data[-1][0])
        print(">>>> ", data)
    return ""
