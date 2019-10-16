import json
import os

import dash
import dash_bio as dashbio
import dash_canvas
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_daq as daq
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import skimage
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_canvas.components import image_upload_zone
from dash_canvas.utils import (
    array_to_data_url,
    image_string_to_PILImage,
    image_with_contour,
    parse_jsonstring,
    superpixel_color_segmentation,
)

# data read
citydata = pd.read_csv("assets/citydata.csv", index_col=0)

# image read
filepath = "assets/me.jpg"
filename = array_to_data_url(skimage.io.imread(filepath))

# mapbox
px.set_mapbox_access_token(
    "pk.eyJ1IjoibWF6YXJpbW9ubyIsImEiOiJjanA5Y3I\
xaWsxeGtmM3dweDh5bjgydGFxIn0.3vrfsqZ_kGPGhi4_npruGg"
)

# markdownのスタイル

mkstyle_ins = {
    "fontSize": 30,
    "width": "80%",
    "margin": "auto",
    "backgroundColor": "white",
    "padding": "3%",
    "borderRadius": 10,
}

mkstyle_ous = {
    "width": "80%",
    "margin": "auto",
    "backgroundColor": "#cbe86e",
    "padding": "3%",
    "margin": "3% auto ",
    "borderRadius": 15,
}

# タイトル用の関数
def head_title(word):
    return html.Div(
        [html.H1(word, style={"textAlign": "center"})],
        style={"backgroundColor": "#fbffb9"},
    )


app_dash = dash.Dash(__name__)

app = app_dash.server

app_dash.config.suppress_callback_exceptions = True


# layout
# -------------------------------------------------------------------------------------

app_dash.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="assets/pyconchina.png",
                            style={"width": "90%", "marginTop": "5%"},
                        )
                    ]
                ),
                html.P("用Dash的可视化", style={"fontSize": 30}),
                html.Div(
                    [
                        html.Div([dcc.Link("TiTle", href="/")]),
                        html.Div([dcc.Link("Link_to_web_app", href="/web-app")]),
                        html.Div([dcc.Link("自我介绍", href="/self-introduce")]),
                        html.Div([dcc.Link("为什么我来这里", href="/reasons")]),
                        html.Div([dcc.Link("Today's Menu", href="/menu")]),
                        html.Div([dcc.Link("Merit of Interactive", href="/merit")]),
                        html.Div([dcc.Link("数据可视化", href="/datavisualization")]),
                        html.Div([dcc.Link("数据可视化2", href="/datavisualization_human")]),
                        html.Div(
                            [dcc.Link("数据可视化3", href="/interactive_visualization")]
                        ),
                        html.Div([dcc.Link("数据可视化4", href="/visualization_tools")]),
                        html.Div([dcc.Link("about_dash", href="/about_dash")]),
                        html.Div([dcc.Link("dash_basic", href="/dash_basic")]),
                        html.Div([dcc.Link("dash_graphs", href="/dash_graphs")]),
                        html.Div(
                            [dcc.Link("dash_components", href="/dash_components")]
                        ),
                        html.Div([dcc.Link("deploy", href="/deploy")]),
                        html.Div([dcc.Link("matome", href="/matome")]),
                        html.Div(
                            [
                                html.Img(
                                    src="assets/logo-simple.png", style={"width": "70%"}
                                )
                            ]
                        ),
                    ]
                ),
            ],
            id="title",
            style={
                "width": "20%",
                "height": 900,
                "backgroundColor": "#C5E99B",
                "textAlign": "center",
                "float": "left",
                "borderRadius": "10px",
            },
        ),
        html.Div(
            [dcc.Location(id="url", refresh=False), html.Div(id="contents")],
            style={
                "width": "80%",
                "backgroundColor": "#D7FFF1",
                "display": "inline-block",
                "borderRadius": "10px",
            },
        ),
    ],
    style={"width": "95%", "margin": "auto"},
)

title = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src="assets/python.png",
                    style={"width": "20%", "marginLeft": "5%", "float": "left"},
                ),
                html.Img(
                    src="assets/chomoku-logo.png",
                    style={
                        "marginTop": "5%",
                        "width": "20%",
                        "float": "right",
                        "marginRight": "5%",
                    },
                ),
            ],
            style={"marginTop": "5%", "display": "inline-block"},
        ),
        html.P(
            "用 Dash 实现交互式数据可视化",
            style={"textAlign": "center", "marginTop": "5%", "fontSize": 60},
        ),
        html.P(
            "PyCon China 北京 2019/10/19",
            style={
                "marginTop": "10%",
                "textAlign": "right",
                "marginRight": "5%",
                "fontSize": 30,
            },
        ),
        html.P(
            "长目 CEO 小川 英幸",
            style={"textAlign": "right", "marginRight": "5%", "fontSize": 30},
        ),
        html.Div(
            [dcc.Link("Next: link_to_web_app", href="/web-app")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ],
    style={"height": 900},
)

web_app = html.Div(
    [
        head_title("Web App"),
        html.Div(
            [
                html.Img(
                    src="assets/qr.png",
                    style={"width": "30%", "marginTop": "5%", "marginBottom": "5%"},
                ),
                html.Br(),
                dcc.Link(
                    "https://pyconchina-dash.azurewebsites.net/",
                    href="https://pyconchina-dash.azurewebsites.net/",
                    style={"textAlign": "center", "fontSize": 40},
                ),
            ],
            style={"textAlign": "center", "padding": "5%"},
        ),
        html.Div(
            [dcc.Link("Next: 自我介绍", href="/self-introduce")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)

self_intro = html.Div(
    [
        head_title("你好，自我介绍"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="assets/me.jpg", style={"width": "60%", "margin": "20%"}
                        ),
                        html.Img(
                            src="assets/hannnari.png",
                            style={"width": "60%", "marginLeft": "20%"},
                        ),
                    ]
                )
            ],
            style={"width": "40%", "float": "left"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P("我叫 小川 英幸（wechat： hide_xiao）"),
                        html.Div(
                            [
                                html.P("我的事业"),
                                html.P(
                                    "· I worked as a trader and analyst at Financial Institute."
                                ),
                                html.P(
                                    "· I started using Python 5 years ago(for data analysis)."
                                ),
                                html.P("· I founded a company named Chomoku(长目)."),
                            ]
                        ),
                        html.P("我来自,日本京都（你知吗？）"),
                        dcc.Graph(
                            figure=px.scatter_mapbox(
                                citydata,
                                lat="lat",
                                lon="long",
                                text="city",
                                size="pop",
                                color="pop",
                                zoom=3,
                                color_continuous_scale=px.colors.sequential.Rainbow,
                            )
                        ),
                        html.Br(),
                        html.P("はんなり == 优雅(you1ya3)"),
                        html.P("优雅Python 在每个第三个星期五 "),
                    ],
                    style={"fontSize": 25, "margin": "5%"},
                )
            ],
            style={"width": "60%", "display": "inline-block"},
        ),
        html.Div(
            [dcc.Link("Next: 为什么我来 PyCon CHINA 北京？", href="/reasons")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)

reasons = html.Div(
    [
        head_title("为什么我来 PyCon CHINA 北京？"),
        html.Div(
            [
                # あとから手直しする Dashが面白いフレームワークなので紹介したかった。
                dcc.Markdown(
                    """
                1. I heve been interested in chinese culture.    
                    - I learn chinese for a year and half.(not good student...)       
                    - My company name "Chomoku" is from old chinese word ["长目飞耳"](https://baike.baidu.com/item/%E9%95%BF%E7%9B%AE%E9%A3%9E%E8%80%B3).
                1. Many People says "Chinese Programmer quiality is the best in the world."
                    - My friend who work at chinese company said so too!
                    - I want to meet.(I cannot speak Chinese and not good at English...)
                1. I read a book titled "Ant Financial".
                    - This book was very exiting for me.
                    - The most impressive scene was that Ant Financial people visited Square's office and they were disappointment of Square's buissiness model. Square earn from the expensive fee of the servise.   
                    - Ant Financial start to think their own buisiness model.
                1. I found PyCon China Beijing.
                    - I accidentally found this event in August.
                    - Then I was preparing for PyCon Japan talk.So I send proposal with same theme.(But contents is not same.)
                1. Dash is good framework.
                    - I am not contributor, I am user.
                    - I want to share.
            """,
                    style=mkstyle_ins,
                )
            ],
            style=mkstyle_ous,
        ),
        html.Div(
            [dcc.Link("Next: Today's Menu", href="/menu")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)

# -----------------  Today's Munu  ---------------------------------------------

menu = html.Div(
    [
        head_title("Today I will talk about"),
        html.Div(
            [
                dcc.Markdown(
                    """
        1. Merit of interactive data visualization.
        1. About Data Visualization.
        1. About Dash.         

    """,
                    style=mkstyle_ins,
                )
            ],
            style=mkstyle_ous,
        ),
        html.Div(
            [dcc.Link("Next: Merit of interactive", href="/merit")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)

# ----------------- Merit of Interactive ------------------------------------

# 訪日観光客データ　https://www.jnto.go.jp/jpn/statistics/visitor_trends/


jpvisit = pd.read_csv("assets/total_tourist_wocumsum.csv", index_col=0)
ex_area = ["総数", "アジア計", "北アメリカ計", "ヨーロッパ計", "オセアニア計", "南アメリカ計", "アフリカ計"]
jpvisit1 = jpvisit[~jpvisit["country"].isin(ex_area)]

df_kyoto_hotels_groupby = pd.read_csv("assets/kyoto_hotel_groupby.csv", index_col=0)
df_kyoto_hotels = pd.read_csv("assets/kyoto_hotel_comp.csv", index_col=0)
mapbox_accesstoken = "pk.eyJ1IjoibWF6YXJpbW9ubyIsImEiOiJjanA5Y3I\
xaWsxeGtmM3dweDh5bjgydGFxIn0.3vrfsqZ_kGPGhi4_npruGg"

merit = html.Div(
    [
        html.Div(
            [
                head_title("Merit of Interactive data visualization"),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            At first, Let's feel the merit of Interactive Data Visualization.    
            (Data: Number of Tourist in Japan, Number of permission of hotel in Kyoto)
            """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    "Number of Foreign tourists in Japan(by country Top10: yearly)",
                                    style={"textAlign": "center"},
                                )
                            ],
                            style={"backgroundColor": "#fbffb9"},
                        ),
                        dcc.Dropdown(
                            id="year_select_dd",
                            options=[
                                {"label": y, "value": y}
                                for y in jpvisit1["year"].unique()
                            ],
                            value=2019,
                            clearable=False,
                            style={
                                "height": 30,
                                "width": "40%",
                                "margin": "auto",
                                "fontSize": 25,
                                "textAlign": "center",
                            },
                        ),
                    ]
                ),
                html.Div(
                    id="year_tourist_rank",
                    style={"width": "50%", "margin": "5% auto 5%"},
                ),
            ]
        ),
        html.Div(
            [html.H2("Number of tourist in japan(monthly)", style={"textAlign": "center"})],
            style={"backgroundColor": "#fbffb9"},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="tourist_country_dd",
                    options=[
                        {"label": country, "value": country}
                        for country in jpvisit["country"].unique()
                    ],
                    value="中国",
                    clearable=False,
                    style={"fontSize": 25, "height": 30, "textAlign": "center"},
                )
            ],
            style={"width": "40%", "margin": "auto"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="tourist_graph")],
                            style={"float": "left", "width": "50%"},
                        ),
                        html.Div(
                            [dcc.Graph(id="all_tourist_graph")],
                            style={"display": "inline-block", "width": "50%"},
                        ),
                    ]
                ),
                dcc.Graph(id="country_tourist_ratio"),
            ],
            style={"margin": "3%"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            "What happens?: Lack of Hotels!",
                            style={"textAlign": "center"},
                        )
                    ],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
                There are not enough rooms to stay. So people rushed buying rooms! And I wanted too!!
            """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    "Increase of kyoto hotel.",
                                    style={"textAlign": "center"},
                                )
                            ],
                            style={"backgroundColor": "#fbffb9"},
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    figure={
                                        "data": [
                                            go.Bar(
                                                x=df_kyoto_hotels_groupby["year"],
                                                y=df_kyoto_hotels_groupby["count"],
                                            )
                                        ]
                                    }
                                )
                            ]
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
                            So I want information about real-estate.But no one give me.     
                            Graph like this is not for investment decision.    
                            So I make my interactive data visualization!     
                            """,
                                    style=mkstyle_ins,
                                )
                            ],
                            style=mkstyle_ous,
                        ),
                    ],
                    style={"width": "90%", "margin": "3% auto 3%"},
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H2("Interactive", style={"textAlign": "center"})],
                            style={"backgroundColor": "#fbffb9"},
                        ),
                        html.Div(
                            [
                                html.H4(
                                    id="year-number", style={"textAlign": "center"}
                                ),
                                dcc.Graph(
                                    id="kyoto-hotel-bar",
                                    figure={
                                        "data": [
                                            go.Bar(
                                                x=df_kyoto_hotels_groupby["year"],
                                                y=df_kyoto_hotels_groupby["count"],
                                            )
                                        ],
                                        "layout": go.Layout(height=300),
                                    },
                                    clickData={"points": [{"x": "all"}]},
                                ),
                                dcc.Graph(id="kyoto-hotelmap-yearcallback"),
                                dcc.Link(
                                    "Data from Kyoto City: I added geo data",
                                    href="https://data.city.kyoto.lg.jp/node/100228",
                                    style={"marginLeft": "60%"},
                                ),
                                html.Div(
                                    [
                                        dcc.Markdown(
                                            """
                                * The map shows where hotels are and where is popular or unpopular.     
                                * I think this sample shows merit of interactive data visualization.    
                                * Interactive data visualization gives us more information and helps us to understand circumstances.                     
                                  
                                """,
                                            style=mkstyle_ins,
                                        )
                                    ],
                                    style=mkstyle_ous,
                                ),
                                html.Div(
                                    [
                                        dcc.Markdown(
                                            """
                                ### How to Use Application.       
                                - Click 2010s legend near map, 2010s scatters turn off. Click one more, Turn on.
                                We can feel massive increase in 2010s.     
                                - Click the year on the upper Bar graph, points on the map shows only the year.     
                                - Click 1946 on the upper Bar graph, all data appears.   
                                    """,
                                            style=mkstyle_ins,
                                        )
                                    ],
                                    style=mkstyle_ous,
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Link(
                                                    "Next: 数据可视化",
                                                    href="/datavisualization",
                                                )
                                            ]
                                        )
                                    ],
                                    style={"textAlign": "right", "marginBottom": "5%"},
                                ),
                            ],
                            style={"width": "90%", "margin": "auto"},
                        ),
                    ]
                ),
            ]
        ),
    ]
)

# --------------------------- Tourist by country callback ---------------------------------------------


@app_dash.callback(
    Output("year_tourist_rank", "children"), [Input("year_select_dd", "value")]
)
def year_rank_update(year_select):
    df2 = jpvisit1[jpvisit1["year"] == year_select]
    pivR = pd.pivot_table(df2, index=["country"], values="value", aggfunc="sum")
    pivR = pivR.assign(year=year_select)
    pivR = pivR.assign(country=pivR.index)
    pivR = pivR[["country", "year", "value"]]
    pivR = pivR.sort_values(by="value", ascending=False)

    pivR = pivR[:10]
    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in pivR.columns],
        data=pivR.to_dict("records"),
        style_cell={
            "height": 30,
            "minWidth": 0,
            "maxWidth": 180,
            "whiteSpace": "normal",
            "fontSize": 30,
            "textAlign": "center",
        },
    )
    return table


# -------------------------------- tourist by country month callback ----------------------------------


@app_dash.callback(
    [
        Output("tourist_graph", "figure"),
        Output("all_tourist_graph", "figure"),
        Output("country_tourist_ratio", "figure"),
    ],
    [Input("tourist_country_dd", "value")],
)
def tourist_graph_update(tourist_country):
    dff = jpvisit[jpvisit["country"] == tourist_country]
    dff.index = [i for i in range(len(dff))]
    dfa = jpvisit[jpvisit["country"] == "総数"]
    dfa.index = [i for i in range(len(dfa))]

    firstG = {
        "data": [go.Bar(x=dff["date"], y=dff["value"])],
        "layout": go.Layout(title="Visit from {}".format(tourist_country), height=400),
    }

    secondG = {
        "data": [go.Bar(x=dfa["date"], y=dfa["value"])],
        "layout": go.Layout(title="Total Tourist(by month)", height=400),
    }

    thirdG = {
        "data": [go.Bar(x=dff["date"], y=dff["value"] / dfa["value"])],
        "layout": go.Layout(title="Tourist ratio({})".format(tourist_country)),
    }

    return firstG, secondG, thirdG


# -------------------------------


@app_dash.callback(
    [
        Output("kyoto-hotelmap-yearcallback", "figure"),
        Output("year-number", "children"),
    ],
    [Input("kyoto-hotel-bar", "clickData")],
)
def update_map(clickData):
    data_x = clickData["points"][0]["x"]
    dff = df_kyoto_hotels[df_kyoto_hotels["year"] == data_x]
    dff_amount = df_kyoto_hotels_groupby[df_kyoto_hotels_groupby["year"] == data_x]
    if data_x == "all":
        return (
            {
                "data": [
                    go.Scattermapbox(
                        lat=df_kyoto_hotels[df_kyoto_hotels["age"] == i]["ido"],
                        lon=df_kyoto_hotels[df_kyoto_hotels["age"] == i]["keido"],
                        mode="markers",
                        marker=dict(size=9),
                        text=df_kyoto_hotels[df_kyoto_hotels["age"] == i]["hotel_name"],
                        name=str(i),
                    )
                    for i in df_kyoto_hotels["age"].unique()
                ],
                "layout": go.Layout(
                    autosize=True,
                    hovermode="closest",
                    mapbox=dict(
                        accesstoken=mapbox_accesstoken,
                        center=dict(
                            lat=np.mean(df_kyoto_hotels["ido"]),
                            lon=np.mean(df_kyoto_hotels["keido"]),
                        ),
                        pitch=90,
                        zoom=12,
                    ),
                    height=600,
                ),
            },
            "Number of Kyoto hotels (2018/12)： {}".format(len(df_kyoto_hotels)),
        )
    elif data_x == 1946:
        return (
            {
                "data": [
                    go.Scattermapbox(
                        lat=df_kyoto_hotels[df_kyoto_hotels["age"] == i]["ido"],
                        lon=df_kyoto_hotels[df_kyoto_hotels["age"] == i]["keido"],
                        mode="markers",
                        marker=dict(size=9),
                        text=df_kyoto_hotels[df_kyoto_hotels["age"] == i]["hotel_name"],
                        name=str(i),
                    )
                    for i in df_kyoto_hotels["age"].unique()
                ],
                "layout": go.Layout(
                    autosize=True,
                    hovermode="closest",
                    mapbox=dict(
                        accesstoken=mapbox_accesstoken,
                        center=dict(
                            lat=np.mean(df_kyoto_hotels["ido"]),
                            lon=np.mean(df_kyoto_hotels["keido"]),
                        ),
                        pitch=90,
                        zoom=12,
                    ),
                    height=600,
                ),
            },
            "Number of Kyoto hotels (2018/12)： {}".format(len(df_kyoto_hotels)),
        )
    else:
        return (
            {
                "data": [
                    go.Scattermapbox(
                        lat=dff["ido"],
                        lon=dff["keido"],
                        mode="markers",
                        marker=dict(size=9),
                        text=dff["hotel_name"],
                    )
                ],
                "layout": go.Layout(
                    autosize=True,
                    hovermode="closest",
                    mapbox=dict(
                        accesstoken=mapbox_accesstoken,
                        center=dict(
                            lat=np.mean(df_kyoto_hotels["ido"]),
                            lon=np.mean(df_kyoto_hotels["keido"]),
                        ),
                        pitch=90,
                        zoom=12,
                    ),
                    height=600,
                ),
            },
            "Number of hotels built in {}: {}".format(
                data_x, dff_amount["count"].values[0]
            ),
        )


# ------------------- About Data Visualization -------------------------------------
# Dashについて話す前に、そもそものデータビジュアライゼーションについて話します。
# ここは頑張らずにサンプルデータを利用する。 iris, gapminder,
datavisualization = html.Div(
    [
        head_title("关于数据可视化"),
        # About Data visualization.
        # add some samples to understand what is data visualization.
        # ここでデータ分析において探索的な分析、特徴量の探索が必要であることに触れる。
        # この次に人間にとってわかりやすいという話を行う。
        html.Div(
            [html.Div(id="whywedata-v-child", style=mkstyle_ous)],
            id="whywedata-v",
            n_clicks=0,
        ),
        html.Div(
            [dcc.Link("数据可视化2", href="/datavisualization_human")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)

## 1 のところがずれるし直したい。
@app_dash.callback(
    Output("whywedata-v-child", "children"), [Input("whywedata-v", "n_clicks")]
)
def update_markdown(n_clicks):
    if n_clicks % 2 == 0:
        return dcc.Markdown(
            """
            - Why do we visualize data?     
                - When we analyze data, there are 5steps.     
                    - 1.Define your questions & goals.     
                    - 2.Collect data.      
                    - 3.Data Preprocessing.      
                    - 4.Exploratory data analysis.      
                    - 5.Evaluate Model and Algorithms.      
            """,
            style=mkstyle_ins,
        )
    else:
        return dcc.Markdown(
            """
            ## Exploratory data analysis     
                - Analyze data sets and summarize their main characters.
                - To know buissiness.     
            ## This step often use visual methods.Because in this step we human observe data.
            ## This step is important to make good model.
            """,
            style=mkstyle_ins,
        )


iris = plotly.data.iris()

datavisualization_human = html.Div(
    [
        head_title("关于数据可视化2"),
        # ここで可視化した方が人間にとってわかりやすいという話を行う。
        html.Div(
            [
                html.Button("change button", id="table_to_chart", n_clicks=0),
                html.Div(id="showdata_for_humans"),
            ],
            style={"margin": "5%"},
        ),
        html.Div(
            [dcc.Link("Next: 关于数据可视化3", href="/interactive_visualization")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)


@app_dash.callback(
    Output("showdata_for_humans", "children"), [Input("table_to_chart", "n_clicks")]
)
def change_table_to_chart(n_clicks):
    if n_clicks % 2 == 0:
        return html.Div(
            [
                html.H2(
                    "Table is difficult to understand.", style={"textAlign": "center"}
                ),
                dash_table.DataTable(
                    columns=[{"id": i, "name": i} for i in iris.columns],
                    data=iris.to_dict("records"),
                    style_cell={"textAlign": "center", "fontSize": 25},
                ),
            ]
        )
    else:
        return html.Div(
            [
                html.H2("Graph is easy to understand.", style={"textAlign": "center"}),
                dcc.Graph(
                    figure=px.scatter_matrix(
                        iris,
                        dimensions=[
                            "sepal_width",
                            "sepal_length",
                            "petal_width",
                            "petal_length",
                        ],
                        color="species",
                    )
                ),
            ]
        )


gapminder = plotly.data.gapminder()
gapminder5 = gapminder[
    gapminder["country"].isin(
        ["Canada", "Switzerland", "Denmark", "United States", "Australia"]
    )
]


interactive_visualization = html.Div(
    [
        head_title("关于数据可视化3"),
        html.Div(
            [
                html.H2(
                    "Normal Visualization(with using gapminder data)",
                    style={"textAlign": "center"},
                ),
                html.Button("change button", id="normal_button", n_clicks=0),
                html.Div(id="normal_visualization"),
                html.Div(
                    [
                        html.H2(
                            "Interactive Visualization", style={"textAlign": "center"}
                        ),
                        html.Button(
                            "change button", id="interactive_button", n_clicks=0
                        ),
                        html.Div(id="interactive_viz"),
                        dcc.Checklist(
                            id="interactive_checklist",
                            options=[
                                {"label": i, "value": i}
                                for i in gapminder.country.unique()
                            ],
                            labelStyle={"display": "inline-block"},
                            value=[
                                "Canada",
                                "Switzerland",
                                "Denmark",
                                "United States",
                                "Australia",
                            ],
                        ),
                    ]
                ),
            ],
            style={"margin": "5%"},
        ),
        html.Div(
            [dcc.Link("Next: 关于数据可视化4", href="/visualization_tools")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)


@app_dash.callback(
    Output("normal_visualization", "children"), [Input("normal_button", "n_clicks")]
)
def update_to_normal(n_clicks):
    if n_clicks % 2 == 0:
        return dcc.Graph(
            figure=px.line(
                gapminder5,
                x="year",
                y="gdpPercap",
                color="country",
                title="Normal Visualization",
            )
        )
    elif n_clicks % 2 == 1:
        return dcc.Graph(
            figure=px.line(
                gapminder,
                x="year",
                y="gdpPercap",
                color="country",
                title="Normal Visualization(with more data)",
            )
        )


# 全部の国が選べるボタンも欲しい。


@app_dash.callback(
    Output("interactive_viz", "children"),
    [Input("interactive_button", "n_clicks"), Input("interactive_checklist", "value")],
)
def update_interactive(n_clicks, country_list):
    gapp = gapminder[gapminder["country"].isin(country_list)]
    if n_clicks % 2 == 0:
        return dcc.Graph(
            figure=px.line(
                gapp,
                x="year",
                y="gdpPercap",
                color="country",
                title="Interactive Visualization",
            )
        )
    else:
        return dcc.Graph(
            figure=px.scatter(
                gapminder,
                x="gdpPercap",
                y="lifeExp",
                size="pop",
                color="continent",
                hover_name="country",
                animation_frame="year",
                size_max=45,
                range_x=[100, 100000],
                range_y=[30, 90],
                log_x=True,
            )
        )


visualization_tools = html.Div(
    [
        head_title("关于数据可视化4"),
        html.Div(
            [
                html.H2("Visualization Tools", style={"textAlign": "center"}),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            ## There are many data visualization tools
            ### BI Tools:(1)
            #### Tableau, Microsoft Power BI, Qlik, SAP BI, Google Data Studio
            ### Libraries
            #### D3, Highcharts, Matplotlib, Bokeh, etc....
            ### Interactive Web Framework
            #### Shiny(R), Dash(Python & R), Panel(Python)
            ### All of these are good tools and we can use whatever we like. It helps to understand data.
        """,
                            style=mkstyle_ins,
                        ),
                        html.Div(
                            [
                                html.A(
                                    "(1) from garter report",
                                    href="https://www.gartner.com/reviews/market/analytics-business-intelligence-platforms",
                                )
                            ],
                            style={"textAlign": "right"},
                        ),
                    ],
                    style=mkstyle_ous,
                ),
            ],
            style={"margin": "5%"},
        ),
        html.Div(
            [dcc.Link("Next: About Dash", href="/about_dash")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)

about_dash = html.Div(
    [
        head_title("About Dash"),
        html.Div(
            [
                dcc.Markdown(
                    """
            - Dash is Open Source Python library(MIT License).
                - Analytical web framework.
                - Made by [plotly](https://plot.ly/).
                - Write code with only Python.
                - Made by Flask、plotly.js、react.js.
                - [Document](https://dash.plot.ly/)
            - With Dash it is easy to build Interactive data visualization, and easy to share.
                - Data Visualozation with Plotly.
                - A lot of data can observe.
                - Easy to share on the web.
            - There are many other components besides graphs.
                - Dash_Cytoscape、Dash-Bio and so on.
                - [You can build your own components!](https://dash.plot.ly/plugins)
        """,
                    style=mkstyle_ins,
                )
            ],
            style=mkstyle_ous,
        ),
        html.Div(
            [dcc.Link("Next: dash_basic", href="/dash_basic")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)

dash_basic = html.Div(
    [
        head_title("how to build dash application."),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="hello-graph",
                            figure={
                                "data": [
                                    {
                                        "x": [1, 2, 3],
                                        "y": [2, 3, 4],
                                        "type": "bar",
                                        "name": "Kyoto",
                                    },
                                    {
                                        "x": [1, 2, 3],
                                        "y": [4, 2, 4],
                                        "type": "bar",
                                        "name": "Tokyo",
                                    },
                                    {
                                        "x": [1, 2, 3],
                                        "y": [3, 1, 4],
                                        "type": "bar",
                                        "name": "Osaka",
                                    },
                                ],
                                "layout": {"title": "Dash DataViz", "height": 400},
                            },
                        ),
                        html.Div(id="hello-graph-callback", style={"fontSize": 30}),
                    ],
                    style={"width": "70%", "margin": "auto"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    "Dash application is made by layout and callbacks.",
                                    style={"textAlign": "center"},
                                )
                            ],
                            style={"backgroundColor": "#fbffb9"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
                            - Layout
                                - make what looks like.
                                - build with components.
                            - callbacks
                                - Keys to make applications interactive.
                                - Use Input State Output
                        """,
                                    style=mkstyle_ins,
                                )
                            ],
                            style=mkstyle_ous,
                        ),
                    ]
                ),
                # コードのマークダウンを直す。
                html.Div(
                    [
                        html.P("Code ", style={"fontSize": 30}),
                        dcc.Markdown(
                            """
            ```python

            import dash     
            import dash_core_components as dcc     
            import dash_html_components as html     
                 
            app = dash.Dash(__name__)      
                     
           # Create a layout     
                  
            app.layout = html.Div(     
                    children=[    
                    dcc.Graph(    
                        id="hello-graph",    
                        figure={    
                            "data": [    
                                {"x": [1, 2, 3], "y": [2, 3, 4],    
                                  "type": "bar", "name": "Kyoto"},    
                                {"x": [1, 2, 3], "y": [4, 2, 4],    
                                  "type": "bar", "name": "Tokyo"},    
                                {"x": [1, 2, 3], "y": [3, 1, 4],    
                                  "type": "bar", "name": "Osaka"},    
                                ],    
                            "layout": {"title": "Dash DataViz", "height": 800},    
                        },    
                    ),    
                    html.Div(id="hello-graph-callback", style={"fontSize":30}),    
                ]    
            )     
                  
            # Create a callback    
            @app.callback(Output("hello-graph-callback", "children"),         
                        [Input("hello-graph", "hoverData")])             
            def hello_graph_callback(hoverData):         
                return json.dumps(hoverData)         

            if __name__ == "__main__"
                app.run_server(debug=True)  
            
            ```

            """,
                            style=mkstyle_ins,
                        ),
                    ],
                    style=mkstyle_ous,
                ),
                html.Div([
                    dcc.Markdown("""
                        - This app was written in just only 38 lines!(including comments!! formatted with black!!!)     
                        - With Dash we can build complex application easily.
                    """, style=mkstyle_ins)
                ], style=mkstyle_ous),
            ]
        ),
        html.Div(
            [dcc.Link("Next: dash_graphs", href="/dash_graphs")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)


@app_dash.callback(
    Output("hello-graph-callback", "children"), [Input("hello-graph", "hoverData")]
)
def hello_graph_callback(hoverData):
    return json.dumps(hoverData)


# dash_graphs
### Think about graphs to show sample.
graphModuleList = ["dash", "plotly.graph_objects", "plotly.express"]
go_graphTypes = []
px_graphTypes = []

dash_graphs = html.Div(
    [
        head_title("Graphs"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            """
                Difference between normal web framework and dash is dash can use the interactive graphs.
     
                Dash can create graphs with Plotly.     
                And plotly has wrapper names plotly.express like maplotlib's seaborn.     
                Let's look difference of module!
                        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    "Graph by Modules", style={"textAlign": "center"}
                                )
                            ],
                            style={"backgroundColor": "#fbffb9"},
                        ),
                        dcc.RadioItems(
                            id="graphs_radio",
                            options=[{"label": i, "value": i} for i in graphModuleList],
                            value="dash",
                            labelStyle={"display": "inline-block", "margin": "1%"},
                        ),
                    ],
                    style={"fontSize": 30},
                ),
                html.Div(id="graph_by_module"),
                # html.Div(
                #     [html.H2("Graph Types", style={"textAlign": "center"})],
                #     style={"backgroundColor": "#fbffb9"},
                # ),
                # html.Div(
                #     [
                #         dcc.Markdown(
                #             """
                #     [Plotly.py](https://plot.ly/python/) library supports over 40 chart types.
                #     Here shows some exmples.
                #     """,
                #             style=mkstyle_ins,
                #         )
                #     ],
                #     style=mkstyle_ous,
                # ),
                # dcc.RadioItems(
                #     id="graphModule",
                #     options=[
                #         {"label": i, "value": i}
                #         for i in ["plotly.graph_objects", "plotly.express"]
                #     ],
                #     value="plotly.graph_objects",
                #     labelStyle={
                #         "display": "inline-block",
                #         "margin": "2%",
                #         "fontSize": 30,
                #     },
                # ),
                # html.Div(id="graphType"),
            ],
            style={"margin": "5%"},
        ),
        html.Div(
            [dcc.Link("Next: dash_components", href="/dash_components")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)

# マークダウン内のコメントアウトの処理

# グラフモジュールによる違いを見せるコールバック
@app_dash.callback(
    Output("graph_by_module", "children"), [Input("graphs_radio", "value")]
)
def update_by_graph_module(module_name):
    gapminder2007 = gapminder[gapminder["year"] == 2007]
    if module_name == "dash":
        return html.Div(
            [
                dcc.Graph(
                    figure={
                        "data": [
                            {
                                "x": gapminder2007["gdpPercap"],
                                "y": gapminder2007["lifeExp"],
                                "mode": "markers",
                            }
                        ],
                        "layout": {
                            "height": 400,
                            "xaxis": {"title": "gdpPercap(log)", "type": "log"},
                            "yaxis": {"title": "lifeExp"},
                            "title": "Graph by Dash",
                        },
                    }
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """

            ```
            dcc.Graph(figure={"data": [{"x": gapminder2007["gdpPercap"], 
            "y":gapminder2007["lifeExp"],"mode":"markers"}], 
            "layout": {"height": 400, "xaxis": {"title": "gdpPercap(log)",
             "type": "log"}, "yaxis":{"title": "lifeExp"}, 
             "title":"Graph by Dash"}})
            ```

            """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
            ]
        )

    elif module_name == "plotly.graph_objects":
        return html.Div(
            [
                dcc.Graph(
                    figure={
                        "data": [
                            go.Scatter(
                                x=gapminder2007["gdpPercap"],
                                y=gapminder2007["lifeExp"],
                                mode="markers",
                            )
                        ],
                        "layout": go.Layout(
                            height=400,
                            xaxis={"title": "gdpPercap(log)", "type": "log"},
                            yaxis={"title": "lifeExp"},
                            title="Graph by plotly.graph_objects",
                        ),
                    }
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """

            ```
            dcc.Graph(figure={"data": [go.Scatter(x=gapminder2007["gdpPercap"],
             y=gapminder2007["lifeExp"], mode="markers")],
            "layout":go.Layout(height=400, xaxis={"title": "gdpPercap(log)", 
            "type":"log"}, yaxis={"title":"lifeExp"}, 
            title= "Graph by plotly.graph_objects")})
            ```
            
            """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
            ]
        )

    else:
        return html.Div(
            [
                dcc.Graph(
                    figure=px.scatter(
                        gapminder2007,
                        x="gdpPercap",
                        y="lifeExp",
                        height=400,
                        log_x=True,
                        title="Graph by plotly.express",
                    )
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            dcc.Graph(figure=px.scatter(gapminder2007, x="gdpPercap", 
            y="lifeExp", height=400, log_x=True, title="Graph by plotly.express"))
            """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
            ]
        )


# グラフサンプルを表示するコールバック
# 時間があれば作りこみたい。今はとりあえずいくつか作りたい。

# Components
params = ["Weight", "Torque", "Width", "Height"]

# ####Cytoscape Data Preprocessing

with open("assets/cyto_sample.txt", "r") as f:
    network_data = f.read().split("\n")

edges = network_data[:750]
nodes = set()

following_node_di = {}  # user id -> list of users they are following
following_edges_di = {}  # user id -> list of cy edges starting from user id

followers_node_di = {}  # user id -> list of followers (cy_node format)
followers_edges_di = {}  # user id -> list of cy edges ending at user id

cy_edges = []
cy_nodes = []

for edge in edges:
    if " " not in edge:
        continue

    source, target = edge.split(" ")

    cy_edge = {"data": {"id": source + target, "source": source, "target": target}}
    cy_target = {"data": {"id": target, "label": "User #" + str(target[-5:])}}
    cy_source = {"data": {"id": source, "label": "User #" + str(source[-5:])}}

    if source not in nodes:
        nodes.add(source)
        cy_nodes.append(cy_source)
    if target not in nodes:
        nodes.add(target)
        cy_nodes.append(cy_target)

    # Process dictionary of following
    if not following_node_di.get(source):
        following_node_di[source] = []
    if not following_edges_di.get(source):
        following_edges_di[source] = []

    following_node_di[source].append(cy_target)
    following_edges_di[source].append(cy_edge)

    # Process dictionary of followers
    if not followers_node_di.get(target):
        followers_node_di[target] = []
    if not followers_edges_di.get(target):
        followers_edges_di[target] = []

    followers_node_di[target].append(cy_source)
    followers_edges_di[target].append(cy_edge)

genesis_node = cy_nodes[0]
genesis_node["classes"] = "genesis"
default_elements = [genesis_node]

default_stylesheet = [
    {"selector": "node", "style": {"opacity": 0.65, "z-index": 9999}},
    {
        "selector": "edge",
        "style": {"curve-style": "bezier", "opacity": 0.45, "z-index": 5000},
    },
    {"selector": ".followerNode", "style": {"background-color": "#0074D9"}},
    {
        "selector": ".followerEdge",
        "style": {
            "mid-target-arrow-color": "blue",
            "mid-target-arrow-shape": "vee",
            "line-color": "#0074D9",
        },
    },
    {"selector": ".followingNode", "style": {"background-color": "#FF4136"}},
    {
        "selector": ".followingEdge",
        "style": {
            "mid-target-arrow-color": "red",
            "mid-target-arrow-shape": "vee",
            "line-color": "#FF4136",
        },
    },
    {
        "selector": ".genesis",
        "style": {
            "background-color": "#B10DC9",
            "border-width": 2,
            "border-color": "purple",
            "border-opacity": 1,
            "opacity": 1,
            "label": "data(label)",
            "color": "#B10DC9",
            "text-opacity": 1,
            "font-size": 12,
            "z-index": 9999,
        },
    },
    {
        "selector": ":selected",
        "style": {
            "border-width": 2,
            "border-color": "black",
            "border-opacity": 1,
            "opacity": 1,
            "label": "data(label)",
            "color": "black",
            "font-size": 12,
            "z-index": 9999,
        },
    },
]


def NamedDropdown(name, **kwargs):
    return html.Div(
        style={"margin": "10px 0px"},
        children=[
            html.P(children=f"{name}:", style={"margin-left": "3px"}),
            dcc.Dropdown(**kwargs),
        ],
    )


def DropdownOptionsList(*args):
    return [{"label": val.capitalize(), "value": val} for val in args]


def NamedRadioItems(name, **kwargs):
    return html.Div(
        style={"padding": "20px 10px 25px 4px"},
        children=[html.P(children=f"{name}:"), dcc.RadioItems(**kwargs)],
    )


styles = {
    "json-output": {
        "overflow-y": "scroll",
        "height": "calc(50% - 25px)",
        "border": "thin lightgrey solid",
    },
    "tab": {"height": "calc(98vh - 80px)"},
}

fjson = open("assets/mol2d.json", "r")
moljson = json.load(fjson)
fjson.close()

# ########dash_components Layout

dash_components = html.Div(
    [
        head_title("Components"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            """
            Dash's layout must be made by components.Dash has 7 components ready to use.
            Today I will show you some of these.
        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [html.H2("dash_html_components", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            Dash_html_components provide HTML Tags as Python Classes.     
                 
            if you want to write       
                  
            ```
            <h1>Hello China!</h1>
            ```
                   
            with Dash_html_components module      
                   
            ```
            import dash_html_components as html
            html.H1("Hello China!")
            ```

            Dash_components_components has 131 classes. Covers all HTML tags? I have no idea.

        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        html.A(
                            "Dash HTML Components Document",
                            href="https://dash.plot.ly/dash-html-components",
                        )
                    ],
                    style={"textAlign": "center"},
                ),
                html.Div(
                    [html.H2("Dash_Core_Components", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            Dash_Core_Components provides components like sliders, dropdowns, graphs and more.
            Many conponents fires callback. And application gets interactive.
        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("X axis value: ", style={"fontSize": 25}),
                                dcc.Dropdown(
                                    id="dcc_dd_x",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in gapminder.columns[3:6]
                                    ],
                                    value="lifeExp",
                                ),
                            ],
                            style={"width": "49%", "float": "left"},
                        ),
                        html.Div(
                            [
                                html.P("Y axis value: ", style={"fontSize": 25}),
                                dcc.Dropdown(
                                    id="dcc_dd_y",
                                    options=[
                                        {"label": i, "value": i}
                                        for i in gapminder.columns[3:6]
                                    ],
                                    value="pop",
                                ),
                            ],
                            style={"width": "49%", "display": "inline-block"},
                        ),
                        html.Div(id="show_dccs_graph"),
                        html.Div(
                            [
                                html.A(
                                    "Dash Core Components Document",
                                    href="https://dash.plot.ly/dash-core-components",
                                )
                            ],
                            style={"textAlign": "center"},
                        ),
                        # The reason is not clear but cannot be displayed...(RangeSlider)
                        # Try to add RangeSlider Later///
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H2("Dash Table", style={"textAlign": "center"})],
                            style={"backgroundColor": "#fbffb9"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
                - Dash Datatable is interactive table. This can be use like Excel.
                - I will show you how the graph changes as I enter numbers in the table.   
            """,
                                    style=mkstyle_ins,
                                )
                            ],
                            style=mkstyle_ous,
                        ),
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id="table-editing-simple",
                                    columns=(
                                        [{"id": "Model", "name": "Model"}]
                                        + [{"id": p, "name": p} for p in params]
                                    ),
                                    data=[
                                        dict(Model=i, **{param: 0 for param in params})
                                        for i in range(1, 5)
                                    ],
                                    style_cell={"fontSize": 25, "textAlign": "center"},
                                    editable=True,
                                ),
                                dcc.Graph(id="table-editing-simple-output"),
                            ]
                        ),
                        html.Div(
                            [
                                html.A(
                                    "Dash DataTable Document",
                                    href="https://dash.plot.ly/datatable",
                                )
                            ],
                            style={"textAlign": "center"},
                        ),
                    ]
                ),
                # dash_daq
                html.Div(
                    [html.H2("Dash Daq", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            Dash Daq is for Data aquisition. It can make beautiful UIs.Tools for Measuring 
            such as voltage,temperature, pressure and more. 
        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        dcc.Interval(
                            id="daq-interval",
                            interval=1000,
                            n_intervals=0,
                            disabled=True,
                        ),
                        daq.PowerButton(
                            id="daq-powerbutton", on=False, size=100, color="green"
                        ),
                        html.Div(id="daq-realtime"),
                        html.Div(
                            [
                                html.A(
                                    "Dash Daq Document",
                                    href="https://dash.plot.ly/dash-daq",
                                )
                            ],
                            style={"textAlign": "center"},
                        ),
                    ]
                ),
                # dash_canvas
                html.Div(
                    [html.H2("Dash Canvas", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
            Dash Canvas is drawing and annotation for image processing. Annotation for 
            Machine Learning training set and more.
        """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dash_canvas.DashCanvas(
                                    id="canvas-bg",
                                    width=500,
                                    filename=filename,
                                    lineWidth=8,
                                    goButtonTitle="Remove background",
                                    hide_buttons=["line", "zoom", "pan"],
                                )
                            ],
                            style={"display": "inline-block", "marginRight": "5%"},
                        ),
                        html.Div(
                            [html.Img(id="seg-image", width=500)],
                            style={"display": "inline-block"},
                        ),
                        html.Div(
                            [
                                html.A(
                                    "Dash Canvas Document",
                                    href="https://dash.plot.ly/canvas",
                                )
                            ],
                            style={"margin": "5%", "textAlign": "center"},
                        ),
                    ]
                ),
                # ---------------------Cytoscape ----------------------------------------------
                html.Div(
                    [html.H2("Dash Cytoscape", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9"},
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
                        [Dash Cytoscape](https://github.com/plotly/dash-cytoscape) is a network visualization components. Using Cytoscape.js.
                        
                    """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
                html.Div(
                    [
                        html.Div(
                            children=[
                                cyto.Cytoscape(
                                    id="cytoscape",
                                    elements=default_elements,
                                    stylesheet=default_stylesheet,
                                    style={"height": "60vh"},
                                )
                            ],
                            style={"width": "70%", "float": "left"},
                        ),
                        html.Div(
                            children=[
                                dcc.Tabs(
                                    id="tabs",
                                    children=[
                                        dcc.Tab(
                                            label="Control Panel",
                                            children=[
                                                NamedDropdown(
                                                    name="Layout",
                                                    id="dropdown-layout",
                                                    options=DropdownOptionsList(
                                                        "random",
                                                        "grid",
                                                        "circle",
                                                        "concentric",
                                                        "breadthfirst",
                                                        "cose",
                                                    ),
                                                    value="grid",
                                                    clearable=False,
                                                ),
                                                NamedRadioItems(
                                                    name="Expand",
                                                    id="radio-expand",
                                                    options=DropdownOptionsList(
                                                        "followers", "following"
                                                    ),
                                                    value="followers",
                                                ),
                                            ],
                                        ),
                                        dcc.Tab(
                                            label="JSON",
                                            children=[
                                                html.Div(
                                                    style=styles["tab"],
                                                    children=[
                                                        html.P("Node Object JSON:"),
                                                        html.Pre(
                                                            id="tap-node-json-output",
                                                            style=styles["json-output"],
                                                        ),
                                                        html.P("Edge Object JSON:"),
                                                        html.Pre(
                                                            id="tap-edge-json-output",
                                                            style=styles["json-output"],
                                                        ),
                                                    ],
                                                )
                                            ],
                                        ),
                                    ],
                                )
                            ],
                            style={"width": "30%", "display": "inline-block"},
                        ),
                    ],
                    style={"height": "63vh"},
                ),
                # ----------------------- Dash Bio -----------------------------------------------
                html.Div(
                    [
                        html.Div(
                            [html.H2("Dash Bio", style={"textAlign": "center"})],
                            style={"backgroundColor": "#fbffb9"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    """
                        [Dash Bio](https://dash.plot.ly/dash-bio) is Bioinformatics components.This component is for Bio informatics,
                        But some graphs can be used normally.
                        """,
                                    style=mkstyle_ins,
                                )
                            ],
                            style=mkstyle_ous,
                        ),
                        html.Div(
                            [dashbio.Molecule2dViewer(modelData=moljson, width=1500)],
                            style={"width": "80%", "margin": "auto"},
                        ),
                    ]
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
                    Sample of these components are on [dash-gallaly](https://dash-gallery.plotly.host/Portal/).
                    Please check it out!
                    """,
                            style=mkstyle_ins,
                        )
                    ],
                    style=mkstyle_ous,
                ),
            ],
            style={"margin": "5%"},
        ),
        html.Div(
            [dcc.Link("Next: deploy", href="/deploy")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)

# dcc sample callback
@app_dash.callback(
    Output("show_dccs_graph", "children"),
    [Input("dcc_dd_x", "value"), Input("dcc_dd_y", "value")],
)
def update_xy_data_graph(x_value, y_value):
    return dcc.Graph(
        figure=px.scatter(
            gapminder,
            x=x_value,
            y=y_value,
            color="year",
            hover_name="country",
            log_x=True,
            log_y=True,
            title="Gapminder Chart X: {}, Y: {}".format(x_value, y_value),
        )
    )


# dash_table sample callback


@app_dash.callback(
    Output("table-editing-simple-output", "figure"),
    [Input("table-editing-simple", "data"), Input("table-editing-simple", "columns")],
)
def display_output(rows, columns):
    df = pd.DataFrame(rows, columns=[c["name"] for c in columns])
    return {
        "data": [
            {
                "type": "parcoords",
                "dimensions": [
                    {"label": col["name"], "values": df[col["id"]]} for col in columns
                ],
            }
        ]
    }


# dash_daq sample callback
@app_dash.callback(Output("daq-interval", "disabled"), [Input("daq-powerbutton", "on")])
def wakeupCall(switch):
    if switch == 1:
        return False
    else:
        return True


@app_dash.callback(
    Output("daq-realtime", "children"), [Input("daq-interval", "n_intervals")]
)
def wakeupDaq(n_intervals):
    if n_intervals:
        n1 = np.random.random() * 10
        n2 = np.random.random() * 10
        n3 = np.random.random() * 10
        n4 = np.random.random() * 10
        n5 = np.random.random() * 10
        n6 = np.random.random() * 10
        n7 = np.random.random() * 10
        n_sum = n1 + n2 + n3 + n4 + n5 + n6 + n7

        return html.Div(
            [
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n1,
                    size=400,
                    style={"display": "inline-block"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n2,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n3,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n4,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n5,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n6,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.GraduatedBar(
                    color={
                        "gradient": True,
                        "ranges": {"green": [0, 4], "yellow": [4, 7], "red": [7, 10]},
                    },
                    showCurrentValue=True,
                    vertical=True,
                    value=n7,
                    size=400,
                    style={"display": "inline-block", "marginLeft": "5%"},
                ),
                daq.LEDDisplay(value=n_sum),
            ],
            style={"textAlign": "center", "margin": "5%"},
        )


# dash canvas callback
# -------------------------------------------------------------------------------------------


@app_dash.callback(
    Output("seg-image", "src"),
    [Input("canvas-bg", "json_data"), Input("canvas-bg", "image_content")],
)
def update_figure(string, image):
    if string:
        if image is None:
            im = skimage.io.imread(filepath)
        else:
            im = image_string_to_PILImage(image)
            im = np.asarray(im)
        shape = im.shape[:2]
        try:
            mask = parse_jsonstring(string, shape=shape)
        except IndexError:
            raise PreventUpdate
        if mask.sum() > 0:
            seg = superpixel_color_segmentation(im, mask)
        else:
            seg = np.ones(shape)
        fill_value = 255 * np.ones(3, dtype=np.uint8)
        dat = np.copy(im)
        dat[np.logical_not(seg)] = fill_value
        return array_to_data_url(dat)
    else:
        raise PreventUpdate


# Cytoscape Callback
# -----------------------------------------------------------------------
@app_dash.callback(
    Output("tap-node-json-output", "children"), [Input("cytoscape", "tapNode")]
)
def display_tap_node(data):
    return json.dumps(data, indent=2)


@app_dash.callback(
    Output("tap-edge-json-output", "children"), [Input("cytoscape", "tapEdge")]
)
def display_tap_edge(data):
    return json.dumps(data, indent=2)


@app_dash.callback(Output("cytoscape", "layout"), [Input("dropdown-layout", "value")])
def update_cytoscape_layout(layout):
    return {"name": layout}


@app_dash.callback(
    Output("cytoscape", "elements"),
    [Input("cytoscape", "tapNodeData")],
    [State("cytoscape", "elements"), State("radio-expand", "value")],
)
def generate_elements(nodeData, elements, expansion_mode):
    if not nodeData:
        return default_elements

    # If the node has already been expanded, we don't expand it again
    if nodeData.get("expanded"):
        return elements

    # This retrieves the currently selected element, and tag it as expanded
    for element in elements:
        if nodeData["id"] == element.get("data").get("id"):
            element["data"]["expanded"] = True
            break

    if expansion_mode == "followers":

        followers_nodes = followers_node_di.get(nodeData["id"])
        followers_edges = followers_edges_di.get(nodeData["id"])

        if followers_nodes:
            for node in followers_nodes:
                node["classes"] = "followerNode"
            elements.extend(followers_nodes)

        if followers_edges:
            for follower_edge in followers_edges:
                follower_edge["classes"] = "followerEdge"
            elements.extend(followers_edges)

    elif expansion_mode == "following":

        following_nodes = following_node_di.get(nodeData["id"])
        following_edges = following_edges_di.get(nodeData["id"])

        if following_nodes:
            for node in following_nodes:
                if node["data"]["id"] != genesis_node["data"]["id"]:
                    node["classes"] = "followingNode"
                    elements.append(node)

        if following_edges:
            for follower_edge in following_edges:
                follower_edge["classes"] = "followingEdge"
            elements.extend(following_edges)

    return elements


# ------------------ deploy ----------------------------------------------

deploy = html.Div(
    [
        head_title("deploy application"),
        html.Div(
            [
                dcc.Markdown(
                    """
    Sharing applications is easy with cloud. This time I use Azure first time, but it was very easy too.
    And I will show you how to deploy. [Here you can learn how to deploy Flask app.](https://docs.microsoft.com/en-us/azure/app-service/containers/how-to-configure-python#flask-app)
    """,
                    style=mkstyle_ins,
                )
            ],
            style=mkstyle_ous,
        ),
        html.Div(
            [
                dcc.Markdown(
                    """
    1. Make your account and get CLI
    2. Make Dash app file.
    
    ---  application.py ----

    ```python:application.py

    import dash
    import dash_html_components as html

    dash_app = dash.Dash(__name__)

    app = dash_app.server

    dash_app.layout = html.Div([
        html.H1("hello world")
    ])

    if __name__ == "__main__":
        dash_app.run_server(debug=True)

    ```

    ---  application.py ----

    3. Make requirements file. ()
    4. Deploy to azure with CLI.    

    ---- CLI -----   
    az login   
    az webapp up -n <your-app-name> -l <your-location>   
    ---- CLI -----   

    5. Here we are! [Website](http://dash-sample-beijing.azurewebsites.net/)     
    [files are on my github.](https://github.com/mazarimono/dash_beijing_deploy_sample)      

    """,
                    style=mkstyle_ins,
                )
            ],
            style=mkstyle_ous,
        ),
        html.Div(
            [
                dcc.Markdown(
                    """
        - Sharing Interactive data Visialization can be done easy with Dash and cloud.     
        - Collaborating with collegues and client will be eisier and there will be new discoveries.    
        - It will helps to create better services!     
        """,
                    style=mkstyle_ins,
                )
            ],
            style=mkstyle_ous,
        ),
        html.Div(
            [dcc.Link("Next: matome", href="/matome")],
            style={"textAlign": "right", "margin": "5%"},
        ),
    ]
)

# ----------------------- matome -----------------------------------

matome = html.Div(
    [head_title("conclusion"), html.Div([], id="conclusion-div", style=mkstyle_ous)],
    id="conclusion-outside",
    n_clicks=0,
)


@app_dash.callback(
    Output("conclusion-div", "children"), [Input("conclusion-outside", "n_clicks")]
)
def conlusion_update(n_clicks):
    if n_clicks % 3 == 0:
        return dcc.Markdown(
            """
        - Interactive data visualization gives us more information.
        - Sharing(apps) and collaborating will create new discoveries.
        - Good insights help to create better services!
        """,
            style=mkstyle_ins,
        )
    elif n_clicks % 3 == 1:
        return html.Div(
            [
                html.Div(
                    [html.H2("I think dash can help with this process!", style={"textAlign": "center"}),
                        html.H2("Let's Start with", style={"textAlign": "center"})],
                    style={"backgroundColor": "#fbffb9", "borderRadius": 20},
                ),
                html.Div(
                    [
                        html.H2(
                            "pip install dash",
                            style={"color": "white", "padding": "2.5%"},
                        )
                    ],
                    style={"backgroundColor": "black", "borderRadius": 20},
                ),
            ],
            style={"width": "90%", "margin": "auto"},
        )
    elif n_clicks % 3 == 2:
        return html.Div(
            [
                html.P(
                    "谢谢",
                    style={"textAlign": "center", "fontSize": 90, "marginTop": "5%"},
                ),
                html.Img(
                    src="assets/python.png",
                    style={"width": "30%", "textAlign": "center"},
                ),
                html.P(
                    "wechat: xiao_hide",
                    style={"textAlign": "center", "fontSize": 50},
                ),
            ],
            style={"backgroundColor": "white", "textAlign": "center"},
        )


# Page Lotation Callback
# ------------------------------------------------------------------------


@app_dash.callback(Output("contents", "children"), [Input("url", "pathname")])
def update_pages(pathname):
    if pathname == "/self-introduce":
        return self_intro
    elif pathname == "/web-app":
        return web_app
    elif pathname == "/reasons":
        return reasons
    elif pathname == "/menu":
        return menu
    elif pathname == "/merit":
        return merit
    elif pathname == "/datavisualization":
        return datavisualization
    elif pathname == "/datavisualization_human":
        return datavisualization_human
    elif pathname == "/interactive_visualization":
        return interactive_visualization
    elif pathname == "/visualization_tools":
        return visualization_tools
    elif pathname == "/about_dash":
        return about_dash
    elif pathname == "/dash_basic":
        return dash_basic
    elif pathname == "/dash_graphs":
        return dash_graphs
    elif pathname == "/dash_components":
        return dash_components
    elif pathname == "/deploy":
        return deploy
    elif pathname == "/matome":
        return matome
    else:
        return title


if __name__ == "__main__":
    app_dash.run_server(debug=True)
