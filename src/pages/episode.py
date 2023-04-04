import dash
import dash_bootstrap_components as dbc


PAGE_ID = "EPISODE"


layout = dbc.Col([
    dash.html.Br(),
    dash.html.H3("EPISODE", style={"textAlign": "center"}),
    dash.html.Br(),
    dash.dcc.Markdown("放送回ごとの分析をするページです。"),
    dash.dcc.Markdown("まだ見ないでね。"),
    dbc.Button("HOMEに戻る", color="dark", href="/")
])
