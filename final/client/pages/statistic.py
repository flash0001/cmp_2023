import dash_bootstrap_components as dbc
from dash import html


table_header = [
    html.Thead(
        html.Tr([
            html.Th("Номер"),
            html.Th("Тип гонки"),
            html.Th("Пилоты"),
            html.Th("Начала гонки"),
            html.Th("Конец гонки"),
        ]),
    ),
]

rows = []

for i in range(10):
    row = html.Tr([
        html.Td("Arthur"),
        html.Td("Dent"),
        html.Td("Arthur"),
        html.Td("Dent"),
        html.Td("Dent")],
        id=f"row_{1}",
        style={"cursor": "pointer"}
    )
    rows.append(row)


table_body = [html.Tbody(rows)]

table = dbc.Table(table_header + table_body, bordered=True)

statistic_page = html.Div([
    html.H1("Статистика"),
    html.Hr(),
    html.Div([
        table
    ])
])
