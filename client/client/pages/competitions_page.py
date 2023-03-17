import dash_bootstrap_components as dbc
from dash import Input, Output, State, html


class Competition:
    def __init__(self):
        pass


class CompetitionCollection(dict):
    def __init__(self):
        pass


table_header = [
    html.Thead(
        html.Tr([
            html.Th("Наименование соревнования"),
            html.Th("Дата"),
            html.Th("Наименование организатора"),
            html.Th("Место проведения"),
        ]),
    ),
]

rows = []

for i in range(10):
    row = html.Tr([
        html.Td("Arthur"),
        html.Td("Dent"),
        html.Td("Arthur"),
        html.Td("Dent")],
        id=f"row_{1}",
    )
    rows.append(row)


table_body = [html.Tbody(rows)]

table = dbc.Table(table_header + table_body, bordered=True)

competition_page = html.Div([
    html.H1("Соревнования"),
    html.Hr(),
    html.Div([
        table
    ])
])
