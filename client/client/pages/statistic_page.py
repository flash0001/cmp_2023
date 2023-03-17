import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dash_table
from services import application as app
from collections import OrderedDict
from components import modal_window


table2 = dash_table.DataTable(
    id="table",
    columns=[
        {"name": "Тип заезда", "id": "type_race"},
        {"name": "Номер(а) Пилота(ов)", "id": "driver"},
        {"name": "Время начала заезда", "id": "started_at"},
        {"name": "Время окончания заезда", "id": "finished_at"},
        {"name": "Данные телеметрии", "id": "telemetry"},
    ],
    data=[{
        "type_race": i * 10, "driver": i * 100,
        "started_at": i * -1, "finished_at": i * -100,
        "telemetry": ",".join([*map(lambda x: str(x), range(60))])[:60] + "...",
    } for i in range(10)],
    merge_duplicate_headers=True,


    style_header={
        # 'textDecoration': 'underline',
        # 'textDecorationStyle': 'dotted',
        "textAlign": "center",
    },
    style_cell={
        "textAlign": "center",
    },
    tooltip_delay=0,
    tooltip_duration=None,
)

table_header = [
    html.Thead(
        html.Tr([
            html.Th("Номер"),
            html.Th("Тип гонки"),
            html.Th("Пилоты"),
            html.Th("Время начала гонки"),
            html.Th("Время окончания гонки"),
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

table = dbc.Table(table_header + table_body, bordered=True, id="table")

statistic_page = html.Div([
    html.H1("Статистика"),
    html.Hr(),
    html.Div([
        table2
    ]),
    modal_window,
])


@app.callback(
    Output("table_out", "children"),
    [Input('table', 'active_cell')],
    [State('table', 'data')]
)
def display_click_data(active_cell, table_data):
    if active_cell is not None:
        # print(">>>> HELLO, ", active_cell)
        # cell = json.dumps(active_cell, indent=2)
        row = active_cell['row']
        col = active_cell['column_id']
        value = table_data[row][col]
        out = f"{row}:{col}:{value}"
    else:
        out = ''
    return out


@app.callback(
    Output("race_results_window", "is_open"),
    [Input("table", "active_cell")],
    State("race_results_window", "is_open"),
)
def open_modal(*values):
    print(">>>> ", values)
    data, is_open = values
    return False if data is None else True
    #return values[1] if values[0] else not values[1]