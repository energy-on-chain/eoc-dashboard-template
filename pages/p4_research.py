import os
import datetime
import pandas as pd
from google.cloud import storage
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from app import app


# CREDENTIALS
# TODO: link creds


# CONFIG
# TODO: add config settings


# DATA
data_dict = {
    'btc': 'gs://eoc-template-dashboard/api_data/glassnode_btc_price_usd_ohlc_24h.csv',
    'eth': 'gs://eoc-template-dashboard/api_data/glassnode_eth_price_usd_ohlc_24h.csv',
    'aave': 'gs://eoc-template-dashboard/api_data/glassnode_aave_price_usd_ohlc_24h.csv',
    'ltc': 'gs://eoc-template-dashboard/api_data/glassnode_ltc_price_usd_ohlc_24h.csv',
    'matic': 'gs://eoc-template-dashboard/api_data/glassnode_matic_price_usd_ohlc_24h.csv',
    'sushi': 'gs://eoc-template-dashboard/api_data/glassnode_sushi_price_usd_ohlc_24h.csv',
}


# PREWORK
# TODO: add default graphs, figs, tables here


# LAYOUT
layout = [
    dbc.Row(
        children=[
            html.H3(className='page-content-title', children='Coin Research ...'),
        ]
    ),
    dbc.Row(
        children=[
            html.P(className='page-content-description', children='Select a coin from the dropdown menu to compare its performance to BTC or ETH over time.'),
        ]
    ),
    dbc.Row(
        children=[
            dbc.Col(
                dcc.Graph(
                    id='page-content-graph',
                    figure=go.Figure()
                ),
                width={'size': 10, 'offset': 1}
            )
        ]
    ),
    html.Br(),
    dbc.Row(
        children=[
            dbc.Col(
                dcc.RadioItems(
                    id='main-coin-radio-button',
                    options=[
                        {'label': 'BTC', 'value': 'btc'},
                        {'label': 'ETH', 'value': 'eth'},
                        {'label': 'None', 'value': None},
                    ],
                    value='btc'
                ),
                width=6,
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='alt-coin-dropdown',
                    options=[
                        {'label': 'AAVE', 'value': 'aave'},
                        {'label': 'LITECOIN', 'value': 'ltc'},
                        {'label': 'MATIC', 'value': 'matic'},
                        {'label': 'SUSHI', 'value': 'sushi'},
                        {'label': 'None', 'value': None},
                    ],
                    value='aave'
                ),
                width=6,
            ) 
        ]
    ),
]

@app.callback(
    Output('page-content-graph', 'figure'), 
    Input('main-coin-radio-button', 'value'),
    Input('alt-coin-dropdown', 'value'),
    )
def update_page(coin_main, coin_alt):

    fig = make_subplots(specs=[[{"secondary_y": True}]])    # create graph
    fig.update_layout(
        showlegend=True,
        plot_bgcolor="#FFFFFF",
        hovermode="x",
        hoverdistance=100, # Distance to show hover label of data point
        spikedistance=1000, # Distance to show spike
        xaxis=dict(
            title='Time (UTC)',
            linecolor="#BCCCDC",
            showspikes=True, # Show spike line for X-axis
            spikethickness=2,
            spikedash="dot",
            spikecolor="#999999",
            spikemode="across",
        ),
        yaxis=dict(
            linecolor="#BCCCDC",
            title='Price (USD)',
        )
    )

    print(data_dict[coin_main])
    print(pd.read_csv(data_dict[coin_main]))
    # if coin_main is not None:    # add main coin if selected
    #     main_df = pd.read_csv(data_dict[coin_main])
    #     fig.add_trace(go.Scatter(x=main_df['utc'], y=main_df['c'], mode='lines', name=coin_main, line_color='orange', line_dash='solid'), secondary_y=False)  
    #     fig.update_yaxes(title_text=coin_main + ' price (usd)', secondary_y=False)

    #     if coin_alt is not None:    # add alt coin if selected
    #         alt_df = pd.read_csv(data_dict[coin_alt])  
    #         fig.add_trace(go.Scatter(x=alt_df['utc'], y=alt_df['c'], mode='lines', name=coin_alt, line_color='blue', line_dash='solid'), secondary_y=True)  
    #         fig.update_yaxes(title_text=coin_alt + ' price (usd)', secondary_y=True)

    return fig
