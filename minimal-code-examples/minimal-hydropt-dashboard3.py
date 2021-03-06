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
import random

from RestrictedPython import compile_restricted_function, safe_builtins, limited_builtins, utility_builtins

from pathlib import Path # für inline-io

class CHydropt(object):
	def __init__(self, uid):
		self.__uid = uid
	def getData(self, filepath):
		octave.eval("load('" + filepath + "', '-mat')") #todo: separate octave instanz für jeden user
		data = octave.pull('Data')
		#todo: fehler check + memoisierung
		return data
		
class CInits(object):
	__numOfInstances = 0
	def __init__(self, uid):
		#Kompilieren der Hauptfunktion
		print("init")
		scriptpath = '.\\user001\\scripts\\render_cockpit.py'
		myscript = Path(scriptpath).read_text()
		render_cockpit_name = 'render_cockpit'
		render_cockpit = compile_restricted_function(p = '', body = myscript, name = render_cockpit_name, filename = '<inline code>')
		safe_globals = safe_builtins
		safe_locals = {}
		hydropt = CHydropt(uid)
		additional_globals = {'hydropt' : hydropt, 'html' : html}
		safe_globals.update(additional_globals)
		exec(render_cockpit.code, safe_globals, safe_locals)
		render_cockpit_pointer = safe_locals[render_cockpit_name]
		
		self.__uid = uid
		self.render_cockpit_pointer = render_cockpit_pointer
		self.hydropt = CHydropt(uid)
		self.safe_globals = safe_globals
		self.safe_locals = safe_locals
		
		CInits.__numOfInstances += 1
	
	def getNumOfInstances():
		return CInits.__numOfInstances
	getNumOfInstances = staticmethod(getNumOfInstances)
		
flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app)

dash_app.layout = html.Div(id='page-content', children=[
	dcc.Location(id='url', refresh=False)
])



@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	uid = 1
	inits = CInits(uid)
	print(inits.getNumOfInstances())
	return dash_router(pathname, inits)
	
def dash_router(url, inits):
	children = []
	if inits.render_cockpit_pointer is not None:
		children = inits.render_cockpit_pointer(*[], **{})
	return children

	
