# start in linux via
# export FLASK_APP=filename.py
# flask run

# start in windows via
# set FLASK_APP=filename.py
# flask run

import inspect, os
#os.environ["FLASK_APP"] = inspect.getfile(inspect.currentframe())
os.environ["OCTAVE_EXECUTABLE"] = "C:\\Octave\\Octave-4.2.2\\bin\\octave-cli.exe"

from oct2py import octave
from flask import Flask
from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from RestrictedPython import compile_restricted_function, safe_builtins, limited_builtins, utility_builtins

from pathlib import Path # für inline-io

class CHydropt(object):
	def __init__(self, uid):
		self.uid = uid
	def getData(self, filepath):
		octave.eval("load('" + filepath + "', '-mat')") #todo: separate octave instanz für jeden user
		data = octave.pull('Data')
		#todo: fehler check + memoisierung
		return data
		
flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app)

#Kompilieren der Hauptfunktion
scriptpath = '.\\user001\\scripts\\render_cockpit.py'
myscript = Path(scriptpath).read_text()
render_cockpit_name = 'render_cockpit'
render_cockpit = compile_restricted_function(p = '', body = myscript, name = render_cockpit_name, filename = '<inline code>')
safe_globals = safe_builtins
safe_locals = {}
additional_globals = {'hydropt' : CHydropt(uid = 1), 'html' : html}
safe_globals.update(additional_globals)
exec(render_cockpit.code, safe_globals, safe_locals)
render_cockpit_pointer = safe_locals[render_cockpit_name]

dash_app.layout = html.Div(id='page-content', children=[
	dcc.Location(id='url', refresh=False)
])

@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	return dash_router(pathname)
	
def dash_router(url):
	children = render_cockpit_pointer(*[], **{})
	return children

	
