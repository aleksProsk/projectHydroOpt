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
from functools import lru_cache # für memoization

@lru_cache(maxsize=32)
def load_hydopt_data(filepath):
	print("load_hydopt_data")
	octave.eval("load('" + filepath + "', '-mat')") #todo: separate octave instanz für jeden user
	data = octave.pull('Data')
	return data

class CHydropt(object):
	def __init__(self, uid):
		self.__uid = uid
	def getData(self, filepath):
		return load_hydopt_data(filepath)
	
def load_script(scriptpath, additional_globals, safe_locals, name):
	myscript = Path(scriptpath).read_text()
	cr = compile_restricted_function(p = '', body = myscript, name = name, filename = '<inline code>')
	safe_globals = safe_builtins
	safe_globals.update(additional_globals)
	exec(cr.code, safe_globals, safe_locals)
	return safe_locals[name]
	
@lru_cache(maxsize=32)
def load_script_uid(scriptpath, name, uid):
	print("load_script_uid")
	return load_script(scriptpath, {'hydropt' : CHydropt(uid), 'html' : html}, {}, name)
	
def getSubdirs(path):
	return next(os.walk(path))[1]

class CInits(object):
	__numOfInstances = 0
	def __init__(self, uid, path):
		#Kompilieren der Hauptfunktion
		print("init")
		scriptpath = path + '\\render.py'
		self.hydropt = CHydropt(uid)
		self.__uid = uid
		self.render_cockpit_pointer = load_script_uid(scriptpath, 'render_cockpit', uid)
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
	inits = CInits(uid, 'C:\\Users\\SEC\Documents\\MyDashFiles\\user001\\scripts\\dash\\cockpit')
	print(inits.getNumOfInstances())
	return dash_router(pathname, inits)
	
def dash_router(url, inits):
	children = []
	if inits.render_cockpit_pointer is not None:
		children = inits.render_cockpit_pointer(*[], **{})
	return children

	
