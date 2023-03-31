import dash
import dash_bootstrap_components as dbc
import pandas as pd


from Class import Radio


font = {"font-family": 'Noto Sans JP'}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "裏ラジアーカイブ(仮)"
server = app.server


radiolist = Radio.RadioList()
df_columns = ["日付", "リンク", "＃", "再生時間", "タイトル", "ゲスト"]
df_list = []
for radio in radiolist.radios.values():
    thumbnail_url = f"http://img.youtube.com/vi/{radio.youtube_id}/default.jpg"
    youtube_url = radio.get_url()
    row = [radio.date, f"[![{youtube_url}]({thumbnail_url})]({youtube_url})", radio.title.as_number(), radio.length.as_hms(), radio.title.as_shorten(), "・".join(radio.guests)]
    df_list.append(row)
df_radio = pd.DataFrame(df_list, columns=df_columns)

radio_table = dash.html.Div([
    dash.html.H4("過去裏ラジ放送データ一覧", style=font),
    # dash.html.P(id="table_out", style=font),
    dash.dash_table.DataTable(
        id="table",
        columns=[{"id": x, "name": x, "presentation": "markdown"} if x == "リンク" else {"id": x, "name": x} for x in df_radio.columns],
        data=df_radio.to_dict("records"),
        style_header={"textAlign": "center"},
        style_data={"textAlign": "left",
                    "whiteSpace": "normal",
                    "height": "auto"},
        style_cell_conditional=[
            {"if": {"column_id": "日付"},
             "width": "10%"},
            {"if": {"column_id": "リンク"},
             "width": "10%"},
            {"if": {"column_id": "＃"},
             "width": "5%"},
            {"if": {"column_id": "再生時間"},
             "width": "10%"},
            {"if": {"column_id": "タイトル"},
             "width": "40%"},
            {"if": {"column_id": "ゲスト"},
             "width": "25%"},
        ],
        page_size=5,
        style_cell=font,
        style_as_list_view=True
    ),
])


transcript_table = dash.html.Div([
    dash.html.H4("書き起こしテキスト一覧")
])


navbar = dbc.NavbarSimple(brand="裏ラジアーカイブ(仮)")


# content = dbc.Row([radio_table, transcript_table])
content = dbc.Container([dbc.Row([
    dash.dcc.Markdown("こちらのサイトはまだ開発中です！\n現在運用中の裏ラジアーカイブスは[こちら](https://uraradi-archives.streamlit.app/)。", style=font),
    radio_table])])


# app.layout = dbc.Container([content])
app.layout = dash.html.Div([
    navbar,
    content
])


@app.callback(
    dash.Output("table_out", "children"),
    dash.Input("table", "active_cell"))
def update_graphs(active_cell):
    if active_cell:
        cell_data = df_radio.iloc[active_cell["row"]][active_cell["column_id"]]
        return f"Data: \"{cell_data}\" from table cell: {active_cell}"
    return "Click the table"


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=False)
