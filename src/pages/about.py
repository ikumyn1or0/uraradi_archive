import dash
import dash_bootstrap_components as dbc


PAGE_ID = "ABOUT"


layout = dbc.Col([
    dash.html.Br(),
    dash.html.H3("ABOUT", style={"textAlign": "center"}),
    dash.html.Br(),
    dash.dcc.Markdown("ラジオやAIについて記載したページです。"),
    dash.dcc.Markdown("まだ見ないでってば。"),
    dbc.Button("HOMEに戻る", color="dark", href="/")
])
