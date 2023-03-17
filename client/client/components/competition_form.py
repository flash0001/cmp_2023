import requests
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from services import application as app
from services import database as db, HTTPClient
from time import sleep

class RaceContext:
    def __init__(self):
        self.http_client = HTTPClient()
        res = self.http_client.get_race_status()

        if res.error:
            sys.stderr.write(res.ok)
            sys.exit(1)
        self.is_finished_race = res.ok == "finished"
        self.competition = db.get_current_competition()
        self.is_disabled = db.does_competition_exist()
        self.race_types = db.get_race_type_names()
        self.drivers = db.get_drivers_id()

    @property
    def is_comp_form_disabled(self) -> bool:
        return db.does_competition_exist()

    @property
    def is_race_form_disabled(self) -> bool:
        return not db.does_competition_exist()

    @property
    def name(self):
        return self.competition.name if self.competition else ""

    @property
    def sponsor(self):
        return self.competition.sponsor if self.competition else ""

    @property
    def date(self):
        return self.competition.date if self.competition else ""

    @property
    def location(self):
        return self.competition.location if self.competition else ""


ctx = RaceContext()

competition_name_input = html.Div([
    dbc.Label("Наименование соревнования", html_for="competition_name"),
    dbc.Input(
        id="com_name",
        placeholder="",
        type="text",
        value=ctx.name
    ),
], style={"margin-bottom": "20px"})

sponsor_name_input = html.Div([
    dbc.Label("Наименование организатора", html_for="sponsor_name"),
    dbc.Input(
        id="sponsor_name",
        placeholder="",
        type="text",
        value=ctx.sponsor
    ),
], style={"margin-bottom": "20px"})

date_input = html.Div([
    dbc.Label("Дата", html_for="date"),
    dbc.Input(
        placeholder="",
        type="date",
        id="date",
        value=ctx.date
    ),
], style={"margin-bottom": "20px"})

location_input = html.Div([
    dbc.Label("Место проведения", html_for="location"),
    dbc.Input(
        id="location",
        placeholder="",
        type="text",
        value=ctx.location
    ),
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


create_comp_btn = html.Div([
    dbc.Button(
        "Запуск",
        id="add_competition",
        # outline=True,
        size="md",
        color="primary",
        className="me-1",
        n_clicks=0,
        disabled=ctx.is_comp_form_disabled,
    ),
], className="d-grid gap-2")


make_archive_btn = html.Div([
    dbc.Button(
        "Архивация",
        id="make_archive",
        # outline=True,
        size="md",
        color="secondary",
        className="me-1",
        n_clicks=0,
        disabled=not ctx.is_comp_form_disabled,
    ),
], className="d-grid gap-2")

# the component
competition_form = dbc.Card([
    dbc.CardHeader("Соревнование"),
    dbc.CardBody([form]),
    dbc.CardFooter(
        dbc.Row([
            dbc.Col(create_comp_btn),
            dbc.Col(make_archive_btn),
        ]),
    ),
    html.Div(id="com_form_dummy_out", style={"visibility": "hidden"})
])


@app.callback(
    Output("com_form_dummy_out", "children"),
    [Input("add_competition", "n_clicks")],
    State("com_name", "value"),
    State("sponsor_name", "value"),
    State("date", "value"),
    State("location", "value"),
)
def on_save_competition(*values):
    data = [v for v in values if v]
    if isinstance(data[0], int):
        print("create a new competition from ", data)
        try:
            name, sponsor, date, location = data[1:]
            db.save_competition(
                name=name,
                sponsor=sponsor,
                date=date,
                location=location
            )
        except Exception as err:
            print(err)
    return ""

@app.callback(
    Output("add_competition", "disabled"),
    [Input("add_competition", "n_clicks")],
)
def disable_btn(n_clicks):
    print(">>>> ", ctx.is_comp_form_disabled)
    sleep(0.8)
    return ctx.is_comp_form_disabled