import dash
import dash_bootstrap_components as dbc


PAGE_ID = "BROWSE"


layout = dbc.Col([
    dash.html.Br(),
    dash.html.H3("BROWSE", style={"textAlign": "center"}),
    dash.html.Br(),
    dash.dcc.Markdown("詳細なデータを可視化したページです。"),
    dash.dcc.Markdown("まだ見ないでよ。"),
    dbc.Button("HOMEに戻る", color="dark", href="/")
])
