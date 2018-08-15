# start in linux via
# export FLASK_APP=filename.py
# flask run

# start in windows via
# set FLASK_APP=filename.py
# flask run

from flask import Flask
from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app)

colors = {
    'background': '#AB1111',
    'text': '#7FDBFF'
}

dash_app.layout = html.Div(id='page-content', style={'backgroundColor': colors['background']}, children=[
	dcc.Location(id='url', refresh=False)
])

@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	return dash_router(pathname)
	
def dash_router(pathname):
	children = [
		html.H1(
			children='Dash routing',
			style={
				'textAlign': 'center',
				'color': colors['text']
			}
		),
		html.H2(children=pathname)		
	]
	return children
	
