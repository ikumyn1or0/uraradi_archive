import dash
import dash_bootstrap_components as dbc


from Class import Radio


PAGE_ID = "HOME"


radiolist = Radio.RadioList()
table_header = dash.html.Tr(
    [
        dash.html.Th("日付"),
        dash.html.Th("リンク"),
        dash.html.Th("タイトル")
    ],
    style={"text-align": "center",
           "vertical-align": "middle"}
)
table_body_list = []
for radio in radiolist.radios.values():
    date = radio.date
    image_link = f"http://img.youtube.com/vi/{radio.youtube_id}/default.jpg"
    youtube_link = radio.get_url()
    title = radio.title.as_number() + "：" + radio.title.as_shorten()
    row = [
        dash.html.Td(date),
        dash.html.Td(dash.html.A(dash.html.Img(src=image_link, style={"height": "80px"}),
                     href=youtube_link,
                     target="_blank"),
                     style={"text-align": "center"}),
        dash.html.Td(title),
    ]
    table_body_list.append(dash.html.Tr(row,
                                        style={"vertical-align": "middle"}))
table = dbc.Card(
    children=[
        dash.html.H3("裏ラジ過去放送回一覧"),
        dash.html.Div(
            dbc.Table(
                [dash.html.Thead(table_header), dash.html.Tbody(table_body_list)],
                bordered=True,
                hover=True,
                striped=True
            ),
            style={"maxHeight": "600px", "overflow": "scroll"}
        )
    ],
    body=True
)

layout = dbc.Container([
    dash.html.Br(),
    dash.html.H2("OVERVIEW", style={"textAlign": "center"}),
    dash.html.Br(),
    dash.dcc.Markdown("こちらのサイトはまだ開発中です！"),
    dash.dcc.Markdown("現在運用中の裏ラジアーカイブスは[こちら](https://uraradi-archives.streamlit.app/)。"),
    table
])
