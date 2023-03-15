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
    is_disabled = bool([*map(lambda _: _, race_collection)])
    drivers = [*map(lambda o: o.id, driver_collection)]


competition_name_input = html.Div([
    dbc.Label("Наименование соревнования", html_for="competition_name"),
    dbc.Input(placeholder="", type="text", id="com_name"),
], style={"margin-bottom": "20px"})

sponsor_name_input = html.Div([
    dbc.Label("Наименование организатора", html_for="sponsor_name"),
    dbc.Input(placeholder="", type="text", id="sponsor_name"),
], style={"margin-bottom": "20px"})

date_input = html.Div([
    dbc.Label("Дата", html_for="date"),
    dbc.Input(placeholder="", type="date", id="date"),
], style={"margin-bottom": "20px"})

location_input = html.Div([
    dbc.Label("Место проведения", html_for="location"),
    dbc.Input(placeholder="", type="text", id="location"),
], style={"margin-bottom": "20px"})

# fields of the form
fields = [
    dbc.Row([dbc.Col(competition_name_input)]),
    dbc.Row([dbc.Col(sponsor_name_input)]),
    dbc.Row([dbc.Col(date_input), dbc.Col(location_input)]),
]

# the form
form = dbc.Form([
    dbc.Row([
        dbc.Col(fields),
    ], style={"padding-left": "25px", "padding-right": "25px"}),
])


button_block = html.Div([
    dbc.Button(
        "Запуск",
        id="add_competition",
        # outline=True,
        size="md",
        color="primary",
        className="me-1",
        n_clicks=0,
        disabled=is_disabled,
    ),
], className="d-grid gap-2")

# the component
competition_form = dbc.Card([
    dbc.CardHeader("Соревнование"),
    dbc.CardBody([form]),
    dbc.CardFooter(button_block),
    html.Div(id="com_form_dummy_out", style={"visibility": "hidden"})
])


@app.callback(
    Output("add_competition", "disabled"),
    [Input("add_competition", "n_clicks")],
)
def disable_btn(*value):
    if value[0]:
        return True
    return False


@app.callback(
    Output("com_form_dummy_out", "children"),
    [Input("add_competition", "n_clicks")],
    State("com_name", "value"),
    State("sponsor_name", "value"),
    State("date", "value"),
    State("location", "value"),
)
def cb_render(*values):
    data = [v for v in values if v]
    if isinstance(data[0], int):
        print(">>>> ", data)
    return ""
