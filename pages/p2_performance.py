import os
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from google.cloud import storage
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from app import app
from apis.coingecko.coingecko_api import coingecko_api


# CREDENTIALS
# TODO: link creds


# CONFIG
# TODO: add config settings


# DATA
portfolio_df = pd.read_csv('data/01_holdings.csv')    # get private portfolio data from csv (option to store on cloud)
coingecko_df = coingecko_api()    # get current market data to calculate metrics
df = pd.merge(portfolio_df, coingecko_df, on='Coin')
df['current_value'] = df['# of Coins'] * df['Price ($)']
df['asset_allocation'] = df['current_value'] / df['current_value'].sum()
print(df)
df2 = df.groupby('Custodian').sum()
print(df2)


# PREWORK
def build_sector_plot():
    
    df2 = df.groupby('Custodian').sum()
    labels = df2.index.to_list()
    values = df2['asset_allocation']

    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0, 0, 0.2, 0])])
    fig.update_layout(
        font={
            'size': 18,
            'color': 'rgb(2,21,70)'
        },
        margin={
            't': 0,
            'b': 0,
            'r': 0,
            'l': 0,
            'pad': 0,
        },
        title={
            'text': 'Custodian Risk',
            'y': 0.975,
            'x': 0.375,
            'xanchor': 'center',
            'yanchor': 'top', 
        },
        titlefont={
            'size': 20,
            'color': 'rgb(2,21,70)'
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig

def build_sunburst_plot():
    fig=px.sunburst(df, path=['Network', 'Symbol'], values='current_value')
    fig.update_layout(
        font={
            'size': 18,
            'color': 'rgb(2,21,70)'
        },
        margin={
            't': 0,
            'b': 0,
            'r': 0,
            'l': 0,
            'pad': 0,
        },
        title={
            'text': 'Asset Allocation',
            'y': 0.975,
            'x': 0.25,
            'xanchor': 'center',
            'yanchor': 'top', 
        },
        titlefont={
            'size': 20,
            'color': 'rgb(2,21,70)'
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig


# LAYOUT
layout = [
    dbc.Row(
        children=[
            html.H3(className='page-content-title', children='Performance Metrics'),
        ]
    ),
    dbc.Row(
        children=[
            html.P(className='page-content-description', children='Analyze your portfolio performance and identify risk levels with graphs and other insights.'),
        ]
    ),
    dbc.Row(
        children=[
            dbc.Col(
                className='pie-chart',
                children=[
                    dcc.Graph(
                        id='performance-graph1',
                        figure=build_sector_plot()
                    ),
                ],
                width=6,
            ),
            dbc.Col(
                className='pie-chart',
                children=[
                    dcc.Graph(
                        id='performance-graph2',
                        figure=build_sunburst_plot()
                    ),
                ],
                width=6,
            )
        ]
    ),
    html.Br(),
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                ],
                width={'size': 6, 'offset': 0}
            ),
                        dbc.Col(
                children=[
                ],
                width={'size': 6, 'offset': 0}
            )
        ]
    ),
    html.Br(),
]


# TODO
