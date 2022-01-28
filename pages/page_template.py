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
# TODO: connect data


# PREWORK
fig = make_subplots(
    specs=[[{"secondary_y": True}]],
    )
fig.update_layout(
    showlegend=True,
    plot_bgcolor="#FFFFFF",
    hovermode="x",
    hoverdistance=100, # Distance to show hover label of data point
    spikedistance=1000, # Distance to show spike
    xaxis=dict(
        title='x axis title',
        linecolor="#BCCCDC",
        showspikes=True, # Show spike line for X-axis
        spikethickness=2,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
    yaxis=dict(
        linecolor="#BCCCDC",
        title='y axis title',
    )
)
# fig.add_trace(go.Scatter(x=df['utc'], y=df['c'], mode='lines', name='close', line_color='orange', line_dash='solid'), secondary_y=False)    # price    
fig.update_yaxes(title_text='yaxis 1', secondary_y=False)
fig.update_yaxes(title_text='yaxis 2', secondary_y=True)


# LAYOUT
layout = [
    dbc.Row(
        children=[
            html.H3(className='page-content-title', children='Page Title'),
        ]
    ),
    dbc.Row(
        children=[
            html.P(className='page-content-description', children='Page description.'),
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
    )
]
