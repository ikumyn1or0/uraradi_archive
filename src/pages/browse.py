import dash
import dash_bootstrap_components as dbc


PAGE_ID = "BROWSE"


layout = dbc.Container([
    dash.html.Br(),
    dash.html.H2("BROWSE", style={"textAlign": "center"}),
    dash.html.Br(),
    dash.dcc.Markdown("詳細なデータを可視化したページです。"),
    dash.dcc.Markdown("まだ見ないでよ。"),
    dbc.Button("HOMEに戻る", color="dark", href="/")
])
