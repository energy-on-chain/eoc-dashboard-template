from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from app import server
from pages import p0_page_template, p1_holdings, p2_performance, p3_revenue, p4_research


# LAYOUT
app.layout = dbc.Container(
    className='page-container',
    fluid=True,
    children=[
        # URL
        dcc.Location(id='url', refresh=False),

        # NAVBAR
        dbc.Row(
            className='navbar',
            children=[
                dbc.Col(
                    children=[
                        html.H2(html.A(className='navbar-title-link', children='Energy On Chain |', href='/')),
                    ],
                    width='auto'
                ),
                dbc.Col(
                    children=[
                        html.A(className='navbar-first-link', children='Holdings', href='/p1_holdings'),
                        html.A(className='navbar-link', children='Performance', href='/p2_performance'),
                        html.A(className='navbar-link', children='Revenue', href='/p3_revenue'),
                        html.A(className='navbar-link', children='Research', href='/p4_research'),
                        html.A(className='navbar-link', children='Customize', href='/p0_page_template'),
                    ]
                ), 
                dbc.Col(
                    children=[
                        html.Img(className='navbar-logo', src=app.get_asset_url('full_eoc_logo.jpg'), height=50)
                    ],
                )   
            ],
            align='center'
        ),

        # PAGE CONTENT
        html.Br(),
        html.Div(
            id='page-content',
            className='page-content',
            children=[]
        )
    ]
)

# CALLBACKS
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def update_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/p1_holdings':
        return p1_holdings.layout
    elif pathname == '/p2_performance':
        return p2_performance.layout
    elif pathname == '/p3_revenue':
        return p3_revenue.layout
    elif pathname == '/p4_research':
        return p4_research.layout
    elif pathname == '/p0_page_template':
        return p0_page_template.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)


# TODO
# Page 1 - Holdings
#   Table showing the coins you hold
#   Connect coingecko
#   Populate table... bag size, cost basis, gains, losses, ROI, ath drawdown
#   Refresh button
#   Pulldown csv button
# Page 2 - Performance
#   Recreate the 7 metrics from my excel sheet here
# Page 3 - Revenue
#   Show annualized interest being earned for each coin
# Page 4 - Research
#   Coingecko api -> get market cap, volume, etc.
#   Deribit api -> get derivatives dat
#   Glassnode api -> get OHLC for BTC, ETH, other example coins
#   Implement as cloud functions
#   Put on cloud scheduler, run automatically at 1 day intervals
#   Create plot to compare any coins
#
# Connect github
# Connect to portfolio website, relaunch on host gator
