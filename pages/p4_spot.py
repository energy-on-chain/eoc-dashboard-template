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
            html.H3(className='page-content-title', children='Spot Market Data'),
        ]
    ),
    dbc.Row(
        children=[
            html.P(className='page-content-description', children='Display your preferred set of spot market data and insights from any number of sources (e.g. Glassnode, exchanges, etc.)'),
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
                dcc.Dropdown(
                    id='coin1-dropdown',
                    placeholder='Select first coin to plot...',
                    options=[
                        {'label': 'AAVE', 'value': 'aave'},
                        {'label': 'BTC', 'value': 'btc'},
                        {'label': 'ETH', 'value': 'eth'},
                        {'label': 'LTC', 'value': 'ltc'},
                        {'label': 'MATIC', 'value': 'matic'},
                        {'label': 'SUSHI', 'value': 'sushi'},
                        {'label': 'None', 'value': None},
                    ],
                    value=None
                ),
                width=4,
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='coin2-dropdown',
                    placeholder='Select second coin to plot...',
                    options=[
                        {'label': 'AAVE', 'value': 'aave'},
                        {'label': 'BTC', 'value': 'btc'},
                        {'label': 'ETH', 'value': 'eth'},
                        {'label': 'LTC', 'value': 'ltc'},
                        {'label': 'MATIC', 'value': 'matic'},
                        {'label': 'SUSHI', 'value': 'sushi'},
                        {'label': 'None', 'value': None},
                    ],
                    value=None
                ),
                width=4,
            ),
            dbc.Col(
                dbc.Button('Update Display', className='btn-primary', id='spot-button'),
                width=2
            )
            
        ],
        justify='center'
    ),
]

@app.callback(
    Output('page-content-graph', 'figure'), 
    Input('spot-button', 'n_clicks'),
    State('coin1-dropdown', 'value'),
    State('coin2-dropdown', 'value'),
    )
def update_page(n_clicks, coin1, coin2):
    if n_clicks == 0:
        return go.Figure()
    
    else:
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
        if coin1 is not None:
            coin1_df = pd.read_csv(data_dict[coin1])   
            fig.add_trace(go.Scatter(x=coin1_df['utc'], y=coin1_df['c'], mode='lines', name=coin1, line_color='orange', line_dash='solid'), secondary_y=False) 
            fig.update_yaxes(title_text=coin1 + ' price (usd)', secondary_y=False) 

        if coin2 is not None:
            coin2_df = pd.read_csv(data_dict[coin2])
            fig.add_trace(go.Scatter(x=coin2_df['utc'], y=coin2_df['c'], mode='lines', name=coin2, line_color='blue', line_dash='solid'), secondary_y=True)  
            fig.update_yaxes(title_text=coin2 + ' price (usd)', secondary_y=True)

        return fig
