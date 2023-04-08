import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go


from Class import Radio, Time


PAGE_ID = "HOME"


radiolist = Radio.RadioList()


radio_total_num = radiolist.get_total_num()
radio_total_length = radiolist.get_total_length()
radio_average_length = radiolist.get_average_length()
radio_total_guests = radiolist.get_total_guests_num()


radio_df_columns = ["日付",
                    "リンク",
                    "タイトル"]
radio_df_list = []
for radio in radiolist.radios.values():
    image_link = f"http://img.youtube.com/vi/{radio.youtube_id}/default.jpg"
    youtube_link = radio.get_url()
    title = radio.title.as_number() + "\n" + radio.title.as_shorten()
    row = [radio.date,
           f"[![{title}]({image_link})]({youtube_link})",
           title]
    radio_df_list.append(row)
radio_df = pd.DataFrame(radio_df_list, columns=radio_df_columns)
radio_df = radio_df.sort_values(by="日付", ascending=False)
RADIO_PAGE_SIZE = 5
RADIO_PAGES = np.ceil(len(radio_df) / 5)


radiolength_df_columns = ["日付",
                          "放送時間",
                          "テキスト",
                          "length"]
radiolength_df_list = []
for radio in radiolist.radios.values():
    if radio.is_clip or radio.is_recording:
        continue
    date = radio.date
    row = [date,
           radio.length.as_datetime(),
           radio.title.as_number() + "<br>" + radio.date + "<br>" + radio.length.as_hms(),
           radio.length]
    radiolength_df_list.append(row)
radiolength_df = pd.DataFrame(radiolength_df_list, columns=radiolength_df_columns)
radiolength_df["月別"] = radiolength_df["日付"].apply(lambda x: x[:7])
radiolength_df["3ヶ月別"] = radiolength_df["日付"].apply(lambda x: x[:5] + str(((int(x[5:7]) - 1) // 3) * 3 + 1).zfill(2))
radiolength_df["年別"] = radiolength_df["日付"].apply(lambda x: x[:5] + "01")

radiolength_agg_dfs = {}
radiolength_agg_dfs["月別"] = radiolength_df.groupby("月別", as_index=False)["length"].agg(lambda s: Time.average_time(s.values.tolist()).as_datetime()).rename(columns={"length": "平均放送時間"})
radiolength_agg_dfs["3ヶ月別"] = radiolength_df.groupby("3ヶ月別", as_index=False)["length"].agg(lambda s: Time.average_time(s.values.tolist()).as_datetime()).rename(columns={"length": "平均放送時間"})
radiolength_agg_dfs["年別"] = radiolength_df.groupby("年別", as_index=False)["length"].agg(lambda s: Time.average_time(s.values.tolist()).as_datetime()).rename(columns={"length": "平均放送時間"})


layout = dbc.Stack(
    [
        dash.html.Br(),
        dash.html.H3("OVERVIEW", style={"textAlign": "center"}),
        dash.dcc.Markdown("こちらのサイトはまだ開発中です！\n現在運用中の裏ラジアーカイブスは[こちら](https://uraradi-archives.streamlit.app/)。", style={"white-space": "pre"}),
        dbc.Card([
            dbc.CardBody([
                dbc.Stack(
                    [
                        dbc.Row([
                            dbc.Col([
                                dash.html.P("放送", className="card-text"),
                                dash.html.H4(f"{radio_total_num}回", className="card-text")]),
                            dbc.Col([
                                dash.html.P("ゲスト", className="card-text"),
                                dash.html.H4(f"{radio_total_guests}人", className="card-text")])]),
                        dbc.Row([
                            dbc.Col([
                                dash.html.P("合計時間", className="card-text"),
                                dash.html.H4(radio_total_length.as_hms(ja_style=True), className="card-text")]),
                            dbc.Col([
                                dash.html.P("平均時間", className="card-text"),
                                dash.html.H4(radio_average_length.as_hms(ja_style=True), className="card-text"),
                                dash.html.P("※総集編・収録放送は除外", className="card-text", style={"font-size": 10})])])
                    ],
                    gap=5
                )
            ])
        ]),
        dbc.Card([
            dbc.CardHeader(dash.html.H3("放送回一覧", style={"margin": 0})),
            dbc.CardBody([
                dbc.Stack(
                    [
                        dbc.Pagination(
                            id=f"{PAGE_ID}_RADIO_PAGINATION",
                            active_page=1,
                            max_value=RADIO_PAGES,
                            fully_expanded=False,
                            className="ms-auto"),
                        dbc.Container(
                            id=f"{PAGE_ID}_RADIO_CONTENT"),
                    ],
                    gap=3
                )
            ])
        ]),
        dbc.Card([
            dbc.CardHeader(dash.html.H3("放送時間", style={"margin": 0})),
            dbc.CardBody([
                dbc.Stack(
                    [
                        dash.dcc.Dropdown(
                            id=f"{PAGE_ID}_RADIOLENGTH_SELECTOR",
                            options=[{"label": dash.html.Span(v, style={"color": "#112137"}),
                                      "value": v}
                                     for v in ["集計なし", "放送回別", "月別", "3ヶ月別", "年別"]],
                            value="集計なし",
                            placeholder="表示方法を選択してください。",
                            clearable=False),
                        dash.dcc.Graph(id=f"{PAGE_ID}_RADIOLENGTH_CONTENT")
                    ],
                    gap=3
                )
            ])
        ])
    ],
    gap=3
)


@dash.callback(
    dash.Output(f"{PAGE_ID}_RADIOLENGTH_CONTENT", "figure"),
    dash.Input(f"{PAGE_ID}_RADIOLENGTH_SELECTOR", "value")
)
def update_radiolength_graph(value):
    fig = go.Figure()

    if value == "放送回別":
        fig.add_trace(go.Scatter(x=radiolength_df["日付"],
                                 y=radiolength_df["放送時間"],
                                 mode="lines+markers",
                                 marker_color="#0caaec",
                                 hovertemplate="%{text}<extra></extra>",
                                 text=radiolength_df["テキスト"],
                                 showlegend=False
                                 ))
        fig.update_xaxes(title="日付",
                         tickformat="%Y-%m")
    elif value in ["月別", "3ヶ月別", "年別"]:
        fig.add_trace(go.Scatter(x=radiolength_df[value],
                                 y=radiolength_df["放送時間"],
                                 mode="markers",
                                 marker_color="#0caaec",
                                 hovertemplate="%{text}<extra></extra>",
                                 text=radiolength_df["テキスト"],
                                 showlegend=False
                                 ))
        radiolength_agg_df = radiolength_agg_dfs[value]
        fig.add_trace(go.Scatter(x=radiolength_agg_df[value],
                                 y=radiolength_agg_df["平均放送時間"],
                                 mode="lines",
                                 marker_color="#0caaec",
                                 showlegend=False,
                                 hoverinfo="skip"
                                 ))
        fig.update_xaxes(title="日付",
                         tickformat="%Y-%m")
    else:
        fig.add_trace(go.Histogram(y=radiolength_df["放送時間"],
                                   marker_color="#0caaec",
                                   hovertemplate="%{y}<br>%{x}回<extra></extra>"
                                   ))
        fig.update_xaxes(title="回数")
    # fig.add_hline(y=radio_average_length.as_datetime().timestamp() * 1000,
    #               line_dash="dot",
    #               line_color="#e8da18",
    #               annotation_text=f"平均 {radio_average_length.as_hms()}",
    #               )
    fig.update_xaxes(title="日付",
                     gridcolor="#808080")
    fig.update_yaxes(title="時間",
                     tickformat="%H:%M:00",
                     gridcolor="#808080")
    fig.update_layout(
        paper_bgcolor="#1B3A50",
        plot_bgcolor="#112137",
        font_color="#E3F4FB",
        margin={"l": 30,
                "r": 30,
                "b": 30,
                "t": 30}
    )
    return fig


@dash.callback(
    dash.Output(f"{PAGE_ID}_RADIO_CONTENT", "children"),
    dash.Input(f"{PAGE_ID}_RADIO_PAGINATION", "active_page"),
    suppress_callback_exceptions=True
)
def change_page(page):
    index_start = (page - 1) * RADIO_PAGE_SIZE
    index_end = page * RADIO_PAGE_SIZE
    df = radio_df.iloc[index_start: index_end]
    radio_datatable = dash.dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"id": "日付", "name": "日付"},
                 {"id": "リンク", "name": "リンク", "presentation": "markdown"},
                 {"id": "タイトル", "name": "タイトル"}],
        css=[{"selector": "p",
              "rule": "margin: 0"}],
        style_cell={"color": "white",
                    "border": "1px solid gray",
                    "font-family": "sans-serif"},
        style_cell_conditional=[{"if": {"column_id": "日付"},
                                 "textAlign": "center",
                                 "width": "10%"},
                                {"if": {"column_id": "リンク"},
                                 "width": "120px"},
                                {"if": {"column_id": "タイトル"},
                                 "textAlign": "left",
                                 "whiteSpace": "pre-line",
                                 "overflow": "hidden",
                                 "textOverflow": "ellipsis",
                                 "maxWidth": 0}],
        style_header={"textAlign": "center",
                      "backgroundColor": "#2C637A"},
        style_data={"backgroundColor": "#112137"},
        page_current=0,
        page_size=5,
        page_action="native",
        cell_selectable=False
    )
    return radio_datatable
