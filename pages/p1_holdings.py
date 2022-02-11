import os
import datetime
import pandas as pd
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
# TODO: connect data


# HELPERS
def build_table_data():
    
    portfolio_df = pd.read_csv('data/01_holdings.csv')    # get private portfolio data from csv (option to store on cloud)
    coingecko_df = coingecko_api()    # get current market data to calculate metrics
    df = pd.merge(portfolio_df, coingecko_df, on='Coin')

    df['# of Coins'] = pd.to_numeric(df['# of Coins'])    # add performance metrics
    df['Price ($)'] = pd.to_numeric(df['Price ($)'])
    df['All-in # ($)'] = pd.to_numeric(df['All-in # ($)'])
    df['Current Value ($)'] = df['# of Coins'] * df['Price ($)']
    df['Net Profits ($)'] = df['Current Value ($)'] - df['All-in # ($)']
    df['ROI'] = df['Current Value ($)'] / df['All-in # ($)']

    df['All-in # ($)'] = df['All-in # ($)'].apply(lambda x: round(x, 2))  # rounding
    df['Cost Basis ($)'] = df['Cost Basis ($)'].apply(lambda x: round(x, 2))
    df['Price ($)'] = df['Price ($)'].apply(lambda x: round(x, 2)) 
    df['Current Value ($)'] = df['Current Value ($)'].apply(lambda x: round(x, 2))
    df['Net Profits ($)'] = df['Net Profits ($)'].apply(lambda x: round(x, 2))
    df['ROI'] = df['ROI'].apply(lambda x: round(x, 2))

    df = df[['Coin', 'Symbol', '# of Coins', 'All-in # ($)', 'Cost Basis ($)', 'APY%', 'Custodian', 'Price ($)', 'Current Value ($)', 'Net Profits ($)', 'ROI', 'Last Updated (UTC)']]

    return df

# Get col list for table
data = build_table_data()
col_list = []
for col in data.columns:
    col_list.append({'name': str(col), 'id': str(col)})


# LAYOUT
layout = [
    dbc.Row(
        children=[
            html.H3(className='page-content-title', children='Portfolio Holdings Summary'),
        ]
    ),
    dbc.Row(
        children=[
            html.P(className='page-content-description', children='Get a real-time summary of your investment holdings all in one place.'),
        ]
    ),
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    dash_table.DataTable(
                        id='holdings-table',
                        editable=False,
                        style_header={
                            'backgroundColor': 'rgb(2,21,70)',
                            'fontWeight': 'bold',
                            'color': 'white',
                            'textAlign': 'center'
                        },
                        style_cell={
                            'textAlign': 'center'
                        },
                        columns=col_list,
                        data=data.to_dict('records'),
                    )
                ],
                width={'size': 10, 'offset': 1}
            )
        ]
    ),
    html.Br(),
    dbc.Row(
        children=[
            dbc.Col(
                id='profits-total',
                children=[html.H6(children='Total Profits ($): ' + str(round(data['Net Profits ($)'].sum(), 2)))],
                width={'size': 3, 'offset': 1}
            ),
            dbc.Col(
                id='holdings-total',
                children=[html.H6(children='Total Holdings ($): ' + str(round(data['Current Value ($)'].sum(), 2)))],
                width={'size': 3, 'offset': 0}
            ),
            dbc.Col(
                id='roi-total',
                children=[html.H6(children='Total ROI: ' + str(round(data['Current Value ($)'].sum() / data['All-in # ($)'].sum(), 2)))],
                width={'size': 3, 'offset': 0}
            )
        ],
        justify='center'
    ),
    html.Br(),
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    dbc.Button('Update Display', className='btn-primary', id='holdings-button'),
                ],
                width={'size': 1, 'offset': 1}
            ),
            dbc.Col(
                children=[
                    html.Button("Download .CSV", className='btn-primary', id="holdings-download-button"),
                    dcc.Download(id="holdings-download")
                ],
                width={'size': 1, 'offset': 0}
            ),
        ],
        justify='evenly'
    ),
]

@app.callback(
    Output('holdings-table', 'data'), 
    Output('holdings-total', 'children'), 
    Output('profits-total', 'children'), 
    Output('roi-total', 'children'), 
    Input('holdings-button', 'n_clicks'),
    )
def update_holdings_table(n_clicks):
    if n_clicks == 0:
        return go.Figure()
    
    else:
        data = build_table_data()

        holdings = html.H6(children='Total Holdings ($): ' + str(round(data['Current Value ($)'].sum(), 2)))    # calc summary metrics
        profits = html.H6(children='Total Profits ($): ' + str(round(data['Net Profits ($)'].sum(), 2)))
        roi = html.H6(children='Total ROI: ' + str(round(data['Current Value ($)'].sum() / data['All-in # ($)'].sum(), 2)))

        return data.to_dict('records'), holdings, profits, roi

@app.callback(
    Output("holdings-download", "data"),
    Input("holdings-download-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_holdings_csv(n_clicks):
    df = build_table_data()
    return dcc.send_data_frame(df.to_csv(index=False), "holdings_table.csv")

# TODO
# display as currency
# Column order
# make editable... which cols, how will save / refresh work, add permissions
# add email notification feature for level alerts
