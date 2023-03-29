import dash
import pandas as pd


playlist_path = "inputs/playlist_裏ラジオウルナイト.csv"
df = pd.read_csv(playlist_path)

app = dash.Dash(__name__)
app.title = "裏ラジアーカイブ"
server = app.server

app.layout = dash.html.Div([
    dash.html.H4("過去裏ラジ放送データ一覧"),
    dash.html.P("ページ作成中！"),
    dash.html.P(id="table_out"),
    dash.dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("Radio"),
        style_cell=dict(textAlign="left"),
        style_header=dict(backgroundColor="paleturquoise"),
        style_data=dict(backgroundColor="lavender")
    ),
])


@app.callback(
    dash.Output("table_out", "children"),
    dash.Input("table", "active_cell"))
def update_graphs(active_cell):
    if active_cell:
        cell_data = df.iloc[active_cell["row"]][active_cell["column_id"]]
        return f"Data: \"{cell_data}\" from table cell: {active_cell}"
    return "Click the table"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=False)
