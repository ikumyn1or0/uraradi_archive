import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


from pages import overview, episode, browse, about


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "裏ラジアーカイブ(仮)"
server = app.server


navbar = dbc.Navbar(
    dbc.Container([
        dbc.Stack(
            [
                dmc.ActionIcon(
                    DashIconify(icon="ci:hamburger-md", width=30),
                    variant="filled",
                    color="gray",
                    id="SIDEBAR_BUTTON"
                ),
                dash.html.A(
                    dbc.Row([
                        dbc.NavbarBrand("裏ラジアーカイブ(仮)")
                    ]),
                    href="/",
                )
            ],
            direction="horizontal",
            gap=3
        )
    ]),
    color="dark",
    dark=True,
    expand="lg"
)


sidebar = dbc.Offcanvas(
    title="Menu",
    is_open=False,
    id="SIDEBAR",
    children=[
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("OVERVIEW", href="/", active="exact", id="temp")),
                dbc.NavItem(dbc.NavLink("EPISODE", href="/episode", active="exact")),
                dbc.NavItem(dbc.NavLink("BROWSE", href="/browse", active="exact")),
                dbc.NavItem(dbc.NavLink("ABOUT", href="/about", active="exact")),
            ],
            justified=True,
            vertical=True,
            pills=True,
        )
    ],
    style={
        "width": "300px"
    }
)


content = dash.html.Div(
    id="PAGE_CONTENT",
)


app.layout = dash.html.Div(
    [
        dash.dcc.Location(id="URL", refresh=False),
        sidebar,
        navbar,
        content
    ]
)


@app.callback(
    dash.Output("SIDEBAR", "is_open"),
    dash.Input("SIDEBAR_BUTTON", "n_clicks"),
    prevent_initial_call=True
)
def show_sidebar(n_clicks):
    return True


@app.callback(
    dash.Output("PAGE_CONTENT", "children"),
    dash.Input("URL", "pathname")
)
def set_sidebar(pathname):
    if pathname == "/":
        return overview.layout
    elif pathname == "/episode":
        return episode.layout
    elif pathname == "/browse":
        return browse.layout
    elif pathname == "/about":
        return about.layout
    else:
        return "404 not found"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=False)
