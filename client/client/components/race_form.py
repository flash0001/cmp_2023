import sys
import requests
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from services import application as app
from services import database as db, HTTPClient

class RaceContext:
    def __init__(self):
        self.http_client = HTTPClient()
        res = self.http_client.get_race_status()

        if res.error:
            sys.stderr.write(res.ok)
            sys.exit(1)
        self.is_finished_race = res.ok == "finished"
        self.race_types = db.get_race_type_names()
        self.drivers = db.get_drivers_id()
        self.is_disabled = not db.does_competition_exist()

ctx = RaceContext()

# the race types
select_race_type = html.Div([
    dbc.Label("Тип гонки", html_for="race_type"),
    dbc.Select(ctx.race_types, ctx.race_types[0], id="race_type"),
], style={"margin-bottom": "20px"})


# the first driver
select_driver_1 = html.Div([
    dbc.Label("Гонщик 1", html_for="sponsor"),
    dbc.Select(ctx.drivers, ctx.drivers[0], id="driver_1"),
], style={"margin-bottom": "20px"})

# the second driver
select_driver_2 = html.Div([
    dbc.Label("Гонщик 2", html_for="sponsor"),
    dbc.Select(ctx.drivers, ctx.drivers[0], id="driver_2", disabled=True),
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
        "Старт",
        id="start_race",
        # outline=True,
        size="md",
        color="primary",
        className="me-1",
        n_clicks=0,
        disabled=ctx.is_disabled,
    ),
], className="d-grid gap-2")

stop_button = html.Div([
    dbc.Button(
        "Финиш",
        id="finish_race",
        # outline=True,
        size="md",
        color="secondary",
        className="me-1",
        n_clicks=0,
        disabled=ctx.is_disabled,
    ),
], className="d-grid gap-2")

# the component
race_form = dbc.Card([
    dbc.CardHeader("Заезд"),
    dbc.CardBody([form]),
    dbc.CardFooter(
        dbc.Row([
            dbc.Col(run_button),
            dbc.Col(stop_button),
        ])
    ),
    html.Div(id="race_form_dummy_out-1", style={"visibility": "hidden"}),
    html.Div(id="race_form_dummy_out-2", style={"visibility": "hidden"}),
])


@app.callback(
    Output("driver_2", "disabled"),
    [Input("select_pair_race", "value")],
)
def on_checkbox(values):
    return not len(values)

@app.callback(
    Output("start_race", "disabled"),
    [Input("start_race", "n_clicks")],
)
def disable_btn(*value):
    return ctx.is_disabled

@app.callback(
    Output("finish_race", "disabled"),
    [Input("finish_race", "n_clicks")],
)
def disable_btn(*value):
    return ctx.is_disabled

@app.callback(
    Output("race_form_dummy_out-1", "children"),
    [Input("start_race", "n_clicks")],
    State("race_type", "value"),
    State("driver_1", "value"),
    State("driver_2", "value"),
    State("select_pair_race", "value"),
)
def on_click_star_race(*values):
    data = [v for v in values if v]
    if isinstance(data[0], int):
        data.append([0])
        data = data[1:6]
        data[-1] = bool(data[-1][0])
        drivers = data[1:3] if data[-1] else data[1:2]
        print("[INFO] trying to start a race with these params: ", {"race_type": data[0], "drivers": drivers})
        race_type = "_".join(data[0].split(" "))
        res = ctx.http_client.start_race(race_type=race_type, drivers=drivers)
        data = res.ok
        print(f"[{data and 'OK' or 'ERROR'}] response has been received from server: ", res)
        if data:
            ctx.is_finished_race = True
            self.notifications.append(res.ok)
    return ""


@app.callback(
    Output("race_form_dummy_out-2", "children"),
    [Input("finish_race", "n_clicks")],
)
def on_click_finish_race(n_click):
    if n_click:
        print("[INFO] trying to finish a race")
        res = ctx.http_client.stop_race()
        print(f"[{res.ok and 'OK' or 'ERROR'}] response has been received from server: ", res)
        if res.ok:
            db.save_race_results(res)
            ctx.is_finished_race = False
    return ""

