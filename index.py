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
                dbc.Col(),    # company name
                dbc.Col(),    # page links
                dbc.Col(),    # company logo (right justified)
            ]
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
# Create navbar
# Add performance page
# Add coin comparison page
# Add revenue / interest page
# Add other pages...
# Link to website...
