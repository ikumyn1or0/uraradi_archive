import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


from pages import overview, episode, browse, about


PAGE_TITLE = "裏ラジアーカイブ(仮)"
LAST_UPDATE = "2023-04-14"


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = PAGE_TITLE
server = app.server


navbar = dbc.Navbar(
    dbc.Container([
        dbc.Stack(
            [
                dmc.ActionIcon(
                    DashIconify(icon="streamline:interface-setting-menu-parallel-hamburger-square-navigation-parallel-hamburger-buttonmenu-square",
                                width=30),
                    variant="filled",
                    color="gray",
                    id="NAVBAR_HAMBURGER_BUTTON",
                    size=30),
                dash.html.A(
                    dbc.NavbarBrand(
                        dash.html.Img(
                            src=r"assets/logo/middle.png",
                            height="50px")
                    ),
                    href="/",)
            ],
            direction="horizontal",
            gap=3
        ),
        dbc.DropdownMenu(
            label="LINK",
            children=[
                dbc.DropdownMenuItem(
                    "裏ラジオウルナイト",
                    disabled=True),
                dbc.DropdownMenuItem(
                    "YouTube",
                    href="https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL",
                    target="_blank"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem(
                    "大浦るかこ",
                    disabled=True),
                dbc.DropdownMenuItem(
                    "YouTube",
                    href="https://www.youtube.com/@Rukako_Oura",
                    target="_blank"),
                dbc.DropdownMenuItem(
                    "Twitter",
                    href="https://twitter.com/Rukako_Oura",
                    target="_blank"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem(
                    PAGE_TITLE,
                    disabled=True),
                dbc.DropdownMenuItem(
                    "Github",
                    href="https://github.com/ikumyn1or0/uraradi_archive",
                    target="_blank"),
                dbc.DropdownMenuItem(
                    "Contact",
                    href="https://twitter.com/mega_ebi",
                    target="_blank"),
                dbc.DropdownMenuItem(
                    f"最終更新：{LAST_UPDATE}",
                    disabled=True)],
            nav=True,
            in_navbar=True,
            menu_variant="dark",
            align_end=True
        )
    ]),
    color="primary",
    dark=True,
    expand="lg",
    sticky="top"
)


sidebar = dbc.Offcanvas(
    title="Menu",
    is_open=False,
    id="SIDEBAR",
    children=[
        dbc.Nav(
            [
                dbc.NavItem(
                    dbc.NavLink(
                        "OVERVIEW",
                        href="/",
                        active="exact",
                        id="SIDEBAR_OVERVIEW_BUTTON")
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "EPISODE",
                        href="/episode",
                        active="exact",
                        id="SIDEBAR_EPISODE_BUTTON")
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "BROWSE",
                        href="/browse",
                        active="exact",
                        id="SIDEBAR_BROWSE_BUTTON")
                ),
                dbc.NavItem(
                    dbc.NavLink(
                        "ABOUT",
                        href="/about",
                        active="exact",
                        id="SIDEBAR_ABOUT_BUTTON")
                )
            ],
            justified=True,
            vertical=True,
            pills=True,
        )
    ],
    style={
        "width": "300px",
        "backgroundColor": "#1B3A50"}
)


content = dbc.Container(id="PAGE_CONTAINER_CONTENT")


app.layout = dash.html.Div([
    dash.dcc.Location(id="URL",
                      refresh=False),
    sidebar,
    navbar,
    content
])


@app.callback(
    dash.Output("SIDEBAR", "is_open"),
    [
        dash.Input("NAVBAR_HAMBURGER_BUTTON", "n_clicks"),
        dash.Input("SIDEBAR_OVERVIEW_BUTTON", "n_clicks"),
        dash.Input("SIDEBAR_EPISODE_BUTTON", "n_clicks"),
        dash.Input("SIDEBAR_BROWSE_BUTTON", "n_clicks"),
        dash.Input("SIDEBAR_ABOUT_BUTTON", "n_clicks"),
    ],
    dash.State("SIDEBAR", "is_open"),
    prevent_initial_call=True
)
def show_sidebar(n_clicks_hamburger, n_clicks_overview, n_clicks_episode, n_clicks_browse, n_clicks_about, is_open):
    if is_open:
        return False
    else:
        return True


@app.callback(
    dash.Output("PAGE_CONTAINER_CONTENT", "children"),
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
    # app.run_server(host="0.0.0.0", port=8080, debug=True)
