import dash
import dash_bootstrap_components as dbc


from Class import Radio


PAGE_ID = "EPISODE"


radiolist = Radio.RadioList()

radio_selector = []
for date, radio in radiolist.get_radios(date_ascending=False):
    selector_text = radio.title.as_number() + " " + radio.title.as_shorten()
    radio_selector.append((date, selector_text))


layout = dbc.Stack(
    [
        dash.html.Br(),
        dash.html.H3("EPISODE",
                     style={"textAlign": "center"}),
        dash.html.Div([
            dash.dcc.Markdown("表示する放送回を選択してください。"),
            dash.dcc.Dropdown(
                id=f"{PAGE_ID}_RADIO_SELECTOR",
                options=[
                    {"label": dash.html.Span(l, style={"color": "#112137"}),
                     "value": v}
                    for v, l in radio_selector
                ],
                value=radio_selector[0][0],
                optionHeight=50,
                clearable=False
            ),
        ]),
        dbc.Card([
            dbc.CardHeader(dash.html.H3("放送情報",
                                        style={"margin": 0})),
            dbc.CardBody(dbc.Stack(
                [
                    dbc.Col([
                        dash.html.P("タイトル",
                                    className="card-text"),
                        dash.html.H4(id=f"{PAGE_ID}_RADIO_TITLE",
                                     className="card-text")
                    ]),
                    dbc.Col([
                        dash.html.P("サムネイル（リンク）", className="card-text"),
                        dash.html.H4(id=f"{PAGE_ID}_RADIO_THUMBNAIL",
                                     className="card-text")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dash.html.P("放送日付",
                                        className="card-text"),
                            dash.html.H4(id=f"{PAGE_ID}_RADIO_DATE",
                                         className="card-text"),
                            dash.html.P("※金曜日の日付を表示",
                                        className="card-text",
                                        style={"font-size": 10})
                        ]),
                        dbc.Col([
                            dash.html.P("放送時間",
                                        className="card-text"),
                            dash.html.H4(id=f"{PAGE_ID}_RADIO_LENGTH",
                                         className="card-text")
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dash.html.P("ナンバリング",
                                        className="card-text"),
                            dash.html.H4(id=f"{PAGE_ID}_RADIO_NUMBER",
                                         className="card-text")
                        ]),
                        dbc.Col([
                            dash.html.P("ゲスト",
                                        className="card-text"),
                            dash.html.H4(id=f"{PAGE_ID}_RADIO_GUESTS",
                                         className="card-text")
                        ])
                    ])
                ],
                gap=5
            ))
        ]),
        # dbc.Card([
        #     dbc.CardHeader(dash.html.H3("テキスト情報",
        #                                 style={"margin": 0})),
        #     dbc.CardBody([
        #         dash.dcc.Markdown("表示するテキストを選択してください。"),
        #         dbc.Stack(
        #             [
        #                 dash.dcc.Dropdown(
        #                     id=f"{PAGE_ID}_TEXT_SELECTOR",
        #                     options=[
        #                         {"label": dash.html.Span(v, style={"color": "#112137"}),
        #                          "value": v}
        #                         for v in ["書き起こし", "チャット", "両方"]
        #                     ],
        #                     value="書き起こし",
        #                     optionHeight=50,
        #                     clearable=False),
        #                 # dash.dcc.Markdown("WordCloudを表示するオプション"),
        #                 dash.html.Div([
        #                     dash.dcc.Markdown("表示する形式を選択してください。"),
        #                     dbc.Tabs([
        #                         dbc.Tab(
        #                             label="再生時間指定",
        #                             children=[
        #                                 dash.html.Br(),
        #                                 dash.html.Div(
        #                                     dbc.ButtonGroup(
        #                                         [
        #                                             dbc.Button("<< 10m"),
        #                                             dbc.Button("<< 1m"),
        #                                             dbc.Button("<< 10s"),
        #                                             dbc.Button(">> 10s"),
        #                                             dbc.Button(">> 1m"),
        #                                             dbc.Button(">> 10m"),
        #                                         ],
        #                                         size="sm",
        #                                     ),
        #                                     className="d-grid"
        #                                 ),
        #                                 dash.html.Br(),
        #                                 dash.dcc.Slider(0, 600, value=0)
        #                             ]
        #                         ),
        #                         dbc.Tab(
        #                             label="キーワード検索",
        #                             children=[
        #                                 dash.html.Br(),
        #                                 dbc.Input(placeholder="キーワード", type="text"),
        #                                 dash.html.Br(),
        #                                 dbc.Button("検索"),
        #                             ]
        #                         )
        #                     ]),
        #                 ]),
        #                 dash.dcc.Markdown("ここに書き起こしテキストを表示する"),
        #             ],
        #             gap=3
        #         )
        #     ])
        # ])
    ],
    gap=3
)


@dash.callback(
    dash.Output(f"{PAGE_ID}_RADIO_TITLE", "children"),
    dash.Input(f"{PAGE_ID}_RADIO_SELECTOR", "value")
)
def show_radio_title(date_value):
    radio = radiolist.get_radio_in(date_value)
    title = radio.title.as_full()
    return title


@dash.callback(
    dash.Output(f"{PAGE_ID}_RADIO_THUMBNAIL", "children"),
    dash.Input(f"{PAGE_ID}_RADIO_SELECTOR", "value")
)
def show_radio_thumbnail(date_value):
    radio = radiolist.get_radio_in(date_value)
    thumbnail_url = radio.get_thumbnail_url(quality="maxresdefault")
    youtube_url = radio.get_url()
    return dash.html.A(
        dash.html.Img(src=thumbnail_url,
                      width="60%"),
        href=youtube_url,
        target="_blank")


@dash.callback(
    dash.Output(f"{PAGE_ID}_RADIO_DATE", "children"),
    dash.Input(f"{PAGE_ID}_RADIO_SELECTOR", "value")
)
def show_radio_date(date_value):
    return date_value


@dash.callback(
    dash.Output(f"{PAGE_ID}_RADIO_LENGTH", "children"),
    dash.Input(f"{PAGE_ID}_RADIO_SELECTOR", "value")
)
def show_radio_length(date_value):
    radio = radiolist.get_radio_in(date_value)
    return radio.length.as_hms(ja_style=True)


@dash.callback(
    dash.Output(f"{PAGE_ID}_RADIO_NUMBER", "children"),
    dash.Input(f"{PAGE_ID}_RADIO_SELECTOR", "value")
)
def show_radio_number(date_value):
    radio = radiolist.get_radio_in(date_value)
    datelist = radiolist.get_dates(ascending=True)
    return f"{radio.title.as_number()}（放送{datelist.index(date_value)+1}回目）"


@dash.callback(
    dash.Output(f"{PAGE_ID}_RADIO_GUESTS", "children"),
    dash.Input(f"{PAGE_ID}_RADIO_SELECTOR", "value")
)
def show_radio_guests(date_value):
    radio = radiolist.get_radio_in(date_value)
    guests = radio.get_guests()
    if len(guests) == 0:
        return "なし"
    else:
        return "・".join(guests)
