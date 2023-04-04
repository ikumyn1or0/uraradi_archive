import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go


from Class import Radio


PAGE_ID = "HOME"


radiolist = Radio.RadioList()


radio_total_num = radiolist.get_total_num()
radio_total_length = radiolist.get_total_length()
radio_average_length = radiolist.get_average_length()
radio_total_guests = radiolist.get_total_guests_num()


radio_df_columns = ["日付", "リンク", "タイトル"]
radio_df_list = []
for radio in radiolist.radios.values():
    date = radio.date
    image_link = f"http://img.youtube.com/vi/{radio.youtube_id}/default.jpg"
    youtube_link = radio.get_url()
    title = radio.title.as_number() + "\n" + radio.title.as_shorten()
    row = [date, f"[![{title}]({image_link})]({youtube_link})", title]
    radio_df_list.append(row)
radio_df = pd.DataFrame(radio_df_list, columns=radio_df_columns)
radio_df = radio_df.sort_values(by="日付", ascending=False)
RADIO_PAGE_SIZE = 5
RADIO_PAGES = np.ceil(len(radio_df) / 5)


fig_df_columns = ["日付", "放送時間", "hover_text"]
fig_df_list = []
for radio in radiolist.radios.values():
    if radio.is_clip or radio.is_recording:
        continue
    date = radio.date
    length = pd.to_datetime(radio.length.as_hms(), format="%H:%M:%S")
    hover_text = radio.title.as_number() + "(" + radio.date + ")<br>" + radio.length.as_hms(ja_style=True)
    fig_df_list.append([date, length, hover_text])
fig_df = pd.DataFrame(fig_df_list, columns=fig_df_columns)

fig_df_list = []
fig = go.Figure()
fig.add_trace(go.Scatter(x=fig_df["日付"],
                         y=fig_df["放送時間"],
                         mode="lines+markers",
                         marker_color="#62B8E3",
                         hovertemplate="%{text}<extra></extra>",
                         text=fig_df["hover_text"],
                         showlegend=False
                         ))
# fig.add_hline(y=fig_df["放送時間"].mean(),
#               line_dash="dot",
#               line_color="green",
#               annotation_text=f"平均:{radio_average_length.as_hms(ja_style=True)}",
#               annotation_position="top left")
fig.update_layout(
    paper_bgcolor="#243542",
    plot_bgcolor="#0C2031",
    font_color="#ebebeb",
    margin={
        "l": 30,
        "r": 30,
        "b": 30,
        "t": 30
    }
)
fig.update_xaxes(
    title="日付",
    gridcolor="#808080",
    tickformat="%Y-%m"
)
fig.update_yaxes(
    title="時間",
    gridcolor="#808080",
    tickformat="%H:%M:00"
)


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
                                dash.html.H4(f"{radio_total_num}回", className="card-text")
                            ]),
                            dbc.Col([
                                dash.html.P("ゲスト", className="card-text"),
                                dash.html.H4(f"{radio_total_guests}人", className="card-text")
                            ]),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dash.html.P("合計時間", className="card-text"),
                                dash.html.H4(radio_total_length.as_hms(ja_style=True), className="card-text")
                            ]),
                            dbc.Col([
                                dash.html.P("平均時間", className="card-text"),
                                dash.html.H4(radio_average_length.as_hms(ja_style=True), className="card-text"),
                                dash.html.P("※総集編・収録放送は除外", className="card-text", style={"font-size": 10}),
                            ]),
                        ])
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
                        dbc.Container(
                            id="HOME_RADIO_CONTENT"
                        ),
                        dbc.Pagination(
                            id="HOME_RADIO_PAGINATION",
                            active_page=1,
                            max_value=RADIO_PAGES,
                            previous_next=True,
                            fully_expanded=False,
                        )
                    ],
                    gap=3
                )
            ])
        ]),
        dbc.Card([
            dbc.CardHeader(dash.html.H3("放送時間", style={"margin": 0})),
            dbc.CardBody([
                dash.dcc.Graph(figure=fig)
            ])
        ])
    ],
    gap=3
)


@dash.callback(
    dash.Output("HOME_RADIO_CONTENT", "children"),
    dash.Input("HOME_RADIO_PAGINATION", "active_page"),
    suppress_callback_exceptions=True
)
def change_page(page):
    index_start = (page - 1) * RADIO_PAGE_SIZE
    index_end = page * RADIO_PAGE_SIZE
    df = radio_df.iloc[index_start: index_end]
    radio_datatable = dash.dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[
            {"id": "日付", "name": "日付"},
            {"id": "リンク", "name": "リンク", "presentation": "markdown"},
            {"id": "タイトル", "name": "タイトル"}],
        css=[
            {"selector": "p",
             "rule": "margin: 0"}],
        style_cell={
            "color": "white",
            "border": "1px solid gray",
            "font-family": "sans-serif"},
        style_cell_conditional=[
            {"if": {"column_id": "日付"},
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
        style_header={
            "textAlign": "center",
            "backgroundColor": "#19508B"},
        style_data={
            "backgroundColor": "#0C2031"},
        page_current=0,
        page_size=5,
        page_action="native",
        cell_selectable=False
    )
    return radio_datatable
