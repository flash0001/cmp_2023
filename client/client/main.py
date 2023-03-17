#! /usr/bin/env python3
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from pages import new_race_page, statistic_page, competition_page, new_competition_page
from services import config, application as app


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background": "#444" if config.dark else "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.P("Электронная система судейства", className="lead"),
        html.Hr(),
        dbc.Nav(
            [
                # html.P("Заезды"),
                dbc.NavLink("Панель управления",
                            href="/", active="exact"),
                dbc.NavLink("Статистика", href="/statistic",
                            active="exact"),
                # html.Hr(),
                # html.P("Соревнования"),
                # dbc.NavLink(
                #    "Обзор",
                #    href="/competition",
                #    active="exact"),
                # dbc.NavLink("Добавить",
                #            href="/competition/new", active="exact"),
            ],
            vertical=True,
            # pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/statistic":
        return statistic_page
    elif pathname == "/race/new" or pathname == "/":
        return new_race_page
    elif pathname == "/competition":
        return competition_page
    elif pathname == "/competition/new":
        return new_competition_page
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Page Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(port=config.server.port, threaded=True, debug=config.server.debug)
