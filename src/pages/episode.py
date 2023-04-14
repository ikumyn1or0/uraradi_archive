import dash
import dash_bootstrap_components as dbc
import pandas as pd


from Class import Radio, Text, Time


PAGE_ID = "EPISODE"


radiolist = Radio.RadioList()

radio_selector = []
for date, radio in radiolist.get_radios(date_ascending=False):
    selector_text = radio.title.as_number() + " " + radio.title.as_shorten()
    radio_selector.append((date, selector_text))


transcriptlist = Text.TranscriptList()

transcript_df_columns = ["種類",
                         "再生時間",
                         "テキスト",
                         "seconds"]
transcript_dfs = {}


def load_transcript(date):
    if date not in transcript_dfs.keys():
        transcript = transcriptlist.get_transcript_in(date)
        radio = radiolist.get_radio_in(date)
        df_list = []
        for sentence in transcript.get_sentences():
            timestamp = sentence.get_timestamp_start()
            youtube_link = radio.get_url(timestamp=timestamp.as_second())
            row = [
                "🦉",
                f"[{timestamp.as_hms()}]({youtube_link})",
                sentence.get_text(),
                timestamp.as_second()]
            df_list.append(row)
        transcript_dfs[date] = pd.DataFrame(df_list, columns=transcript_df_columns)
    return transcript_dfs[date]


chatlist = Text.ChatList()

chat_df_columns = ["種類",
                   "再生時間",
                   "テキスト",
                   "seconds"]
chat_dfs = {}


def load_chat(date):
    if date not in chat_dfs.keys():
        chat = chatlist.get_chat_in(date)
        radio = radiolist.get_radio_in(date)
        df_list = []
        for comment in chat.get_comments():
            timestamp = comment.get_timestamp()
            youtube_link = radio.get_url(timestamp=timestamp.as_second())
            row = [
                "💬",
                f"[{timestamp.as_hms()}]({youtube_link})",
                comment.get_text(),
                timestamp.as_second()]
            df_list.append(row)
        chat_dfs[date] = pd.DataFrame(df_list, columns=chat_df_columns)
    return chat_dfs[date]


layout = dbc.Stack(
    [
        dash.html.Br(),
        dash.html.H3(
            "EPISODE",
            style={"textAlign": "center"}),
        dash.html.Div([
            dash.dcc.Markdown("表示する放送回を選択してください。"),
            dash.dcc.Dropdown(
                id=f"{PAGE_ID}_RADIO_SELECTOR",
                options=[
                    {
                        "label": dash.html.Span(l, style={"color": "#112137"}),
                        "value": v
                    } for v, l in radio_selector
                ],
                value=radio_selector[0][0],
                optionHeight=50,
                clearable=False
            ),
        ]),
        dbc.Card([
            dbc.CardHeader(
                dash.html.H4(
                    "放送情報",
                    style={"margin": 0})
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dash.html.P("サムネイル（リンク）"),
                        dash.html.H4(
                            id=f"{PAGE_ID}_RADIO_THUMBNAIL",
                            style={"fontSize": 25, "margin-top": -15})
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dash.html.P("タイトル"),
                        dash.html.P(
                            id=f"{PAGE_ID}_RADIO_TITLE",
                            style={"fontSize": 25, "margin-top": -15})
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dash.html.P("放送日付"),
                        dash.html.P(
                            id=f"{PAGE_ID}_RADIO_DATE",
                            style={"fontSize": 25, "margin-top": -15}),
                        dash.html.P(
                            "※金曜日の日付",
                            style={"fontSize": 10, "margin-top": -15})
                    ]),
                    dbc.Col([
                        dash.html.P("放送時間"),
                        dash.html.P(
                            id=f"{PAGE_ID}_RADIO_LENGTH",
                            style={"fontSize": 25, "margin-top": -15})
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dash.html.P("ナンバリング"),
                        dash.html.P(
                            id=f"{PAGE_ID}_RADIO_NUMBER",
                            style={"fontSize": 25, "margin-top": -15})
                    ]),
                    dbc.Col([
                        dash.html.P("ゲスト"),
                        dash.html.P(
                            id=f"{PAGE_ID}_RADIO_GUESTS",
                            style={"fontSize": 25, "margin-top": -15})
                    ])
                ])
            ],
            )
        ]),
        dbc.Card([
            dbc.CardHeader(
                dash.html.H4(
                    "テキスト情報",
                    style={"margin": 0})
            ),
            dbc.CardBody([
                dash.dcc.Markdown("表示するテキストを選択してください。"),
                dbc.Stack(
                    [
                        dash.dcc.Dropdown(
                            id=f"{PAGE_ID}_TEXT_SELECTOR",
                            options=[
                                {
                                    "label": dash.html.Span(v, style={"color": "#112137"}),
                                    "value": v
                                } for v in ["書き起こし", "チャット", "両方"]
                            ],
                            value="書き起こし",
                            optionHeight=50,
                            clearable=False),
                        dash.html.Div([
                            dash.dcc.Markdown("表示する形式を選択してください。"),
                            dbc.Tabs(
                                [
                                    dbc.Tab(
                                        label="再生時間指定",
                                        tab_id=f"{PAGE_ID}_text_tab_timestamp",
                                        children=[
                                            dash.html.Br(),
                                            dash.html.P(id=f"{PAGE_ID}_SLIDER_VALUE"),
                                            dash.dcc.Slider(
                                                id=f"{PAGE_ID}_TEXT_SLIDER",
                                                min=0,
                                                max=600,
                                                step=1,
                                                value=0)
                                        ]
                                    ),
                                    dbc.Tab(
                                        label="キーワード検索",
                                        tab_id=f"{PAGE_ID}_text_tab_keyword",
                                        children=[
                                            dash.html.Br(),
                                            dbc.Input(
                                                id=f"{PAGE_ID}_TEXT_INPUT",
                                                placeholder="キーワード",
                                                type="text"),
                                        ]
                                    )
                                ],
                                id=f"{PAGE_ID}_TEXT_TAB"
                            ),
                        ]),
                        dash.html.Div(id=f"{PAGE_ID}_TEXT_TABLE"),
                    ],
                    gap=3
                )
            ])
        ])
    ],
    gap=3
)


@dash.callback(
    dash.Output(f"{PAGE_ID}_TEXT_TABLE", "children"),
    [
        dash.Input(f"{PAGE_ID}_TEXT_TAB", "active_tab"),
        dash.Input(f"{PAGE_ID}_TEXT_SLIDER", "value"),
        dash.Input(f"{PAGE_ID}_TEXT_INPUT", "value"),
        dash.Input(f"{PAGE_ID}_TEXT_SELECTOR", "value"),
        dash.Input(f"{PAGE_ID}_RADIO_SELECTOR", "value")
    ],
)
def show_text_table(active_tab, timestamp_value, input_value, select_type, date_value):
    if select_type in ["書き起こし", "両方"]:
        if date_value not in transcriptlist.get_dates():
            return dash.dcc.Markdown("書き起こしテキスト追加までお待ちください。")
    if select_type in ["チャット", "両方"]:
        if date_value not in chatlist.get_dates():
            return dash.dcc.Markdown("チャットテキスト追加までお待ちください。")

    if select_type == "書き起こし":
        table_data = load_transcript(date_value)
    elif select_type == "チャット":
        table_data = load_chat(date_value)
    else:
        table_data = pd.concat(
            [
                load_transcript(date_value),
                load_chat(date_value)
            ],
            axis=0,
            ignore_index=True
        )

    if active_tab == f"{PAGE_ID}_text_tab_timestamp":
        table_data = table_data[table_data["seconds"] >= timestamp_value]
    elif active_tab == f"{PAGE_ID}_text_tab_keyword":
        if input_value is not None:
            table_data = table_data[table_data["テキスト"].str.contains(input_value)]
    table_data = table_data.sort_values(by="seconds")

    text_datatable = dash.dash_table.DataTable(
        data=table_data.to_dict("records"),
        columns=[
            {"id": "種類", "name": "種類"},
            {"id": "再生時間", "name": "再生時間", "presentation": "markdown"},
            {"id": "テキスト", "name": "テキスト"},
        ],
        css=[
            {"selector": "p", "rule": "margin: 0"}],
        style_cell={
            "color": "white",
            "border": "1px solid gray",
            "font-family": "sans-serif"},
        style_cell_conditional=[
            {
                "if": {"column_id": "種類"},
                "textAlign": "center",
                "width": "5%"},
            {
                "if": {"column_id": "再生時間"},
                "width": "10%"},
            {
                "if": {"column_id": "テキスト"},
                "textAlign": "left",
                "Height": "auto",
                "whiteSpace": "normal",
                "maxWidth": 0}
        ],
        fixed_rows={"headers": True},
        style_header={"textAlign": "center",
                      "backgroundColor": "#2C637A"},
        style_data={"backgroundColor": "#112137"},
        cell_selectable=False
    )
    return text_datatable


@dash.callback(
    [
        dash.Output(f"{PAGE_ID}_TEXT_SLIDER", "max"),
        dash.Output(f"{PAGE_ID}_TEXT_SLIDER", "marks"),
    ],
    dash.Input(f"{PAGE_ID}_RADIO_SELECTOR", "value")
)
def update_slider_length(date_value):
    radio = radiolist.get_radio_in(date_value)
    max_value = radio.length.as_second()
    marks = {}
    for value in range(0, radio.length.as_second(), 30 * 60):
        marks[value] = Time.Time(value).as_hms()
    return max_value, marks


@dash.callback(
    dash.Output(f"{PAGE_ID}_SLIDER_VALUE", "children"),
    dash.Input(f"{PAGE_ID}_TEXT_SLIDER", "value")
)
def show_slider_value(value):
    return Time.Time(value).as_hms()


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
        dash.html.Img(
            src=thumbnail_url,
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
