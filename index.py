import os
import json
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from app import server
from pages import p0_page_template, p1_holdings, p2_performance, p3_revenue, p4_spot, p5_derivatives
from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import secretmanager


# CREDENTIALS
project_id = "eoc-template"
storage_client = storage.Client()


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
                        html.A(className='navbar-link', children='Spot', href='/p4_spot'),
                        html.A(className='navbar-link', children='Derivatives', href='/p5_derivatives'),
                        html.A(className='navbar-link', children='Custom', href='/p0_page_template'),
                    ],
                    width='auto'
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
        return p1_holdings.layout
    elif pathname == '/p1_holdings':
        return p1_holdings.layout
    elif pathname == '/p2_performance':
        return p2_performance.layout
    elif pathname == '/p3_revenue':
        return p3_revenue.layout
    elif pathname == '/p4_spot':
        return p4_spot.layout
    elif pathname == '/p5_derivatives':
        return p5_derivatives.layout
    elif pathname == '/p0_page_template':
        return p0_page_template.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)


# TODO
# Deploy as app instance
# Add to portfolio website "lightweight", "fully customized", "notificaitons of level alerts, etc"
# Relaunch EOC website on host gator
# Move on to DApps
# Pitch energy / financial services clientssd
# Make revenue table editable / dynamic updates
# Make holdings table editable / dynamic updates
# Add example notification levels (even if it's not connected fully)
