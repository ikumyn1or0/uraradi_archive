import dash
import dash_bootstrap_components as dbc
import pandas as pd


from Class import Radio


playlist = Radio.Playlist()
df_columns = ["日付", "リンク", "＃", "タイトル", "ゲスト"]
df_list = []
for radio in playlist.radios.values():
    thumbnail_url = f"http://img.youtube.com/vi/{radio.youtube_id}/default.jpg"
    youtube_url = radio.get_url()
    row = [radio.date, f"[![{youtube_url}]({thumbnail_url})]({youtube_url})", radio.title.as_number(), radio.title.as_shorten(), "・".join(radio.guests)]
    df_list.append(row)
df = pd.DataFrame(df_list, columns=df_columns)


font = {"font-family": 'Noto Sans JP'}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "裏ラジアーカイブ"
server = app.server


app.layout = dash.html.Div([
    dash.html.H4("過去裏ラジ放送データ一覧", style=font),
    dash.html.P("ページ作成中！", style=font),
    dash.html.P(id="table_out", style=font),
    dash.dash_table.DataTable(
        id="table",
        columns=[{"id": x, "name": x, "presentation": "markdown"} if x == "リンク" else {"id": x, "name": x} for x in df.columns],
        data=df.to_dict("records"),
        style_header={"textAlign": "center"},
        style_data={"textAlign": "left",
                    "whiteSpace": "normal",
                    "height": "auto"},
        style_cell=font,
        fill_width=False,
        style_as_list_view=True
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
