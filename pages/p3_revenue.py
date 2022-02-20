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
def build_table_data():
    
    portfolio_df = pd.read_csv('data/01_holdings.csv')    # get private portfolio data from csv (option to store on cloud)
    coingecko_df = coingecko_api()    # get current market data to calculate metrics
    df = pd.merge(portfolio_df, coingecko_df, on='Coin')

    df['# of Coins'] = pd.to_numeric(df['# of Coins'])    # add performance metrics
    df['Price ($)'] = pd.to_numeric(df['Price ($)'])
    df['APY%'] = pd.to_numeric(df['APY%'])
    df['Yearly (coins)'] = df['# of Coins'] * (df['APY%'] / 100)
    df['Yearly ($)'] = df['Yearly (coins)'] * df['Price ($)']
    df['Monthly (coins)'] = df['Yearly (coins)'] / 12
    df['Monthly ($)'] = df['Yearly ($)'] / 12
    df['Daily (coins)'] = df['Yearly (coins)'] / 365
    df['Daily ($)'] = df['Yearly (coins)'] / 365

    df['Price ($)'] = df['Price ($)'].apply(lambda x: round(x, 2)) 
    df['Yearly (coins)'] = df['Yearly (coins)'].apply(lambda x: round(x, 4))
    df['Yearly ($)'] = df['Yearly ($)'].apply(lambda x: round(x, 2))
    df['Monthly (coins)'] = df['Monthly (coins)'].apply(lambda x: round(x, 4))
    df['Monthly ($)'] = df['Monthly ($)'].apply(lambda x: round(x, 2))
    df['Daily (coins)'] = df['Daily (coins)'].apply(lambda x: round(x, 4))
    df['Daily ($)'] = df['Daily ($)'].apply(lambda x: round(x, 2))

    df = df[['Coin', 'Symbol', '# of Coins', 'APY%', 'Custodian', 'Price ($)', 'Yearly (coins)', 'Monthly (coins)', 'Daily (coins)', 'Yearly ($)', 'Monthly ($)', 'Daily ($)', 'Last Updated (UTC)']]

    return df


def build_figure(df):
    revenue_df = df.copy()
    label_list = []
    for x in range(0, 13):
        label = 'Month ' + str(x)
        revenue_df[label] = x * revenue_df['Monthly ($)']
        label_list.append(label)

    sub_df = revenue_df[['Coin'] + label_list].set_index('Coin').transpose()
    sub_df['Total'] = sub_df[sub_df.columns].sum(axis=1)
    sub_df.reset_index(inplace=True)
    sub_df.rename(columns={'index':'Month'}, inplace=True)
    sub_df['Month'] = sub_df['Month'].apply(lambda x: int(x.replace('Month ', '')))

    fig = make_subplots(specs=[[{"secondary_y": True}]])    # create graph
    fig.update_layout(
        showlegend=True,
        plot_bgcolor="#FFFFFF",
        hovermode="x",
        hoverdistance=100, # Distance to show hover label of data point
        spikedistance=1000, # Distance to show spike
        xaxis=dict(
            title='Months Elapsed',
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
    
    for col in sub_df.columns[1:]:
        fig.add_trace(go.Scatter(x=sub_df['Month'], y=sub_df[col], mode='lines', name=col, line_dash='solid'), secondary_y=False) 
    fig.update_yaxes(title_text='Cumulative Revenue ($)', secondary_y=False) 

    return fig

data = build_table_data()
figure = build_figure(data)
col_list = []
for col in data.columns:
    col_list.append({'name': str(col), 'id': str(col)})


# LAYOUT
layout = [
    dbc.Row(
        children=[
            html.H3(className='page-content-title', children='Revenue Projection'),
        ]
    ),
    dbc.Row(
        children=[
            html.P(className='page-content-description', children='Get a forecast of the passive income you will be earning from your investments (*** at current price levels ***).'),
        ]
    ),
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    dcc.Graph(
                        id='revenue-graph',
                        figure=figure
                    ),
                ],
                width={'size': 10, 'offset': 1}
            )
        ]
    ),
    html.Br(),
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    dash_table.DataTable(
                        id='revenue-table',
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
                id='yearly-total',
                children=[html.H6(children='Yearly Income ($): ' + str(round(data['Yearly ($)'].sum(), 2)))],
                width={'size': 3, 'offset': 1}
            ),
            dbc.Col(
                id='monthly-total',
                children=[html.H6(children='Monthly Income ($): ' + str(round(data['Monthly ($)'].sum(), 2)))],
                width={'size': 3, 'offset': 0}
            ),
            dbc.Col(
                id='daily-total',
                children=[html.H6(children='Daily Income ($): ' + str(round(data['Daily ($)'].sum().sum(), 2)))],
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
                    dbc.Button('Update Display', className='btn-primary', id='revenue-button'),
                ],
                width={'size': 1, 'offset': 1}
            ),
            dbc.Col(
                children=[
                    html.Button("Download .CSV", className='btn-primary', id="revenue-download-button"),
                    dcc.Download(id="revenue-download")
                ],
                width={'size': 1, 'offset': 0}
            ),
        ],
        justify='evenly'
    ),
    html.Br(),
]

@app.callback(
    Output('revenue-graph', 'figure'), 
    Output('revenue-table', 'data'), 
    Output('yearly-total', 'children'), 
    Output('monthly-total', 'children'), 
    Output('daily-total', 'children'), 
    Input('revenue-button', 'n_clicks'),
    )
def update_revenue(n_clicks):
    if n_clicks == 0:
        return go.Figure()
    
    else:
        data = build_table_data()
        figure = build_figure(data)

        yearly = html.H6(children='Yearly Income ($): ' + str(round(data['Yearly ($)'].sum(), 2)))    # calc summary metrics
        monthly = html.H6(children='Monthly Income ($): ' + str(round(data['Monthly ($)'].sum(), 2)))
        daily = html.H6(children='Daily Income: ' + str(round(data['Daily ($)'].sum().sum(), 2)))

        return figure, data.to_dict('records'), yearly, monthly, daily

@app.callback(
    Output("revenue-download", "data"),
    Input("revenue-download-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_revenue_csv(n_clicks):
    df = build_table_data()
    return dcc.send_data_frame(df.to_csv, "revenue_table.csv")


# TODO
