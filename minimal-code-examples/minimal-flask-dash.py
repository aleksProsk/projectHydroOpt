# start in linux via
# export FLASK_APP=minimal-flask-dash.py
# flask run

# start in windows via
# set FLASK_APP=minimal-flask-dash.py
# flask run

from flask import Flask, redirect
from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dashpath')

@flask_app.route('/')
def hello_world():
	return 'Index page'

@flask_app.route('/hello')
def hello():
    return 'Hello, World'	
	
@flask_app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@flask_app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
	
#statisches routing auf flask-basis
@flask_app.route('/dashboard') 
def render_dashboard():
    return redirect('/dashpath')	
	
colors = {
    'background': '#AB1111',
    'text': '#7FDBFF'
}

dash_app.layout = html.Div(id='page-content', style={'backgroundColor': colors['background']}, children=[
	dcc.Location(id='url', refresh=False),
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    )
])

#add-on: dynamisches routing auf dash-basis
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
	
