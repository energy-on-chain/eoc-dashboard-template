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
    'BTC Funding Rate (Deribit)': 'gs://eoc-template-dashboard/api_data/deribit_funding_rate_1h.csv',
    'BTC Historical Volatility (Deribit)': 'gs://eoc-template-dashboard/api_data/deribit_historical_volatility_1h.csv',
}


# PREWORK
# TODO: add default graphs, figs, tables here


# LAYOUT
layout = [
    dbc.Row(
        children=[
            html.H3(className='page-content-title', children='Derivatives Market Data'),
        ]
    ),
    dbc.Row(
        children=[
            html.P(className='page-content-description', children='Display your preferred set of derivatives market data and insights from any number of sources (e.g. Deribit, Glassnode, Binance, etc.)'),
        ]
    ),
    dbc.Row(
        children=[
            dbc.Col(
                dcc.Graph(
                    id='derivatives-page-content-graph',
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
                dcc.Checklist(
                    id='derivatives-checklist',
                    options=[
                        {'label': 'Plot BTC Funding Rate (Deribit)', 'value': 'BTC Funding Rate (Deribit)'},
                        {'label': 'Plot BTC Historical Volatility (Deribit)', 'value': 'BTC Historical Volatility (Deribit)'},
                    ],
                    value=['BTC Funding Rate (Deribit)'],
                    # labelStyle={'display': 'inline-block'}
                ),
                width={'size': 10, 'offset': 1}
            ),
        ]
    ),
]

@app.callback(
    Output('derivatives-page-content-graph', 'figure'), 
    Input('derivatives-checklist', 'value'),
    )
def update_page(checklist1):
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

    for item in checklist1:
        df = pd.read_csv(data_dict[item]) 
        df.sort_values(by=['utc'], inplace=True)
        if item == 'BTC Funding Rate (Deribit)':
            fig.add_trace(go.Scatter(x=df['utc'], y=df['interest_1h'], mode='lines', name=item, line_color='orange', line_dash='solid'), secondary_y=False) 
            fig.update_yaxes(title_text=item, secondary_y=False) 
        elif item == 'BTC Historical Volatility (Deribit)':
            fig.add_trace(go.Scatter(x=df['utc'], y=df['historical_volatility'], mode='lines', name=item, line_color='blue', line_dash='solid'), secondary_y=True) 
            fig.update_yaxes(title_text=item, secondary_y=True) 

    return fig


# TODO
