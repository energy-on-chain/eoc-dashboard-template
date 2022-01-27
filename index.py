from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from app import server


# LAYOUT
app.layout = html.Div(
    children=[
        # URL
        dcc.Location(id='url', refresh=False),

        # NAVBAR
        dbc.Row(
            className='navbar',
            children=[
                dbc.Col(
                    children=[
                        # html.H2(className='navbar-title-link', children='Energy On Chain   |'),
                        html.H2(html.A(className='navbar-title-link', children='Energy On Chain   |', href='https://www.google.com')),
                    ],
                    width='auto'
                ),
                dbc.Col(
                    children=[
                        html.A(className='navbar-first-link', children='Page 1', href='https://www.google.com'),
                        html.A(className='navbar-link', children='Page 2', href='https://www.google.com'),
                        html.A(className='navbar-link', children='Page 3', href='https://www.google.com'),
                    ]
                ), 
                dbc.Col(
                    children=[
                        html.Img(className='navbar-logo', src=app.get_asset_url("full_eoc_logo.jpg"), height=50)
                    ],
                )   
            ],
            align='center'
        ),

        # PAGE CONTENT
        dbc.Row(
            className='page-content',
            children=[]
        ),
    ]
)


# CALLBACKS
# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def update_page(pathname):
#     if pathname == '/':
#         return index.layout
#     else:
#         return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)


# TODO
# Page 1 - Summary
#   Table showing the coins you hold
#   Create csv file that holds all this info that can be plugged in
#   Populate table... bag size, cost basis, gains, losses, ROI, ath drawdown
# Page 2 - Metrics
#   Recreate the 7 metrics from my excel sheet here
# Page 3 - Revenue
#   Show annualized interest being earned for each coin
# Page 4 - Coin Comparator
#   Select any coin you are holding and toggle on BTC / ETH price action
# Page 5 - Any other custom page you want...
# Post this on EOC site 
# Relaunch the EOC site
