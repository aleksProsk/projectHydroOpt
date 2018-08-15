# start in linux via
# export FLASK_APP=filename.py
# flask run

# start in windows via
# set FLASK_APP=filename.py
# flask run

print("imports...")
import inspect, os
#os.environ["FLASK_APP"] = inspect.getfile(inspect.currentframe())
os.environ["OCTAVE_EXECUTABLE"] = "C:\\Octave\\Octave-4.2.2\\bin\\octave-cli.exe"

from oct2py import octave
from flask import Flask
from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import random

from pandas import DataFrame
import numpy as np

from RestrictedPython import compile_restricted_function, safe_builtins, limited_builtins, utility_builtins

from pathlib import Path # für inline-io
from functools import lru_cache # für memoization

print("classdefs...")

@lru_cache(maxsize=32)
def load_hydopt_data(filepath):
	print("load_hydopt_data")
	octave.eval("load('" + filepath + "', '-mat')") #todo: separate octave instanz für jeden user
	data = octave.pull('Data')
	return data

class CHydropt(object):
	def __init__(self, uid): self.__uid = uid
	def getData(self, filepath): return load_hydopt_data(filepath)
		
class CSafeNP(object):
	def __init__(self, uid): self.__uid = uid
	def min(self, v): return np.min(v)
	def max(self, v): return np.max(v)
	def hstack(self, v): return np.hstack(v)
	def vstack(self, v): return np.vstack(v)
	
class CSafeDF(object):
	def __init__(self, uid): self.__uid = uid
	def define(self, matrix, columns): self.__df = DataFrame(matrix, columns=columns)
	def to_dict(self, param): return self.__df.to_dict(param)
	def columns(self): return self.__df.columns

class CSafeLog(object):
	def __init__(self, uid): self.__uid = uid
	def print(self,s): print(s)
	
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
	return load_script(scriptpath, {'hydropt' : CHydropt(uid), 'html' : html, 'dt' : dt, 'np' : CSafeNP(uid), 'df' : CSafeDF(uid), 'log' : CSafeLog(uid)}, {}, name)
	
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
		self.render_pointer = load_script_uid(scriptpath, 'render', uid)
		CInits.__numOfInstances += 1
	def getNumOfInstances():
		return CInits.__numOfInstances
	getNumOfInstances = staticmethod(getNumOfInstances)

dt0 = dt.DataTable(
	rows=[{0: 0}],
	row_selectable=False,
	filterable=False,
	sortable=False,
	selected_row_indices=[],
	id='dt0'
)
	
print("start servers...")
flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app)

print("start dash...")
dash_app.layout = html.Div(id='page-content', children=[dcc.Location(id='url', refresh=False), dt0])

@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	print("display_page")
	uid = 1
	inits = CInits(uid, 'C:\\Users\\SEC\Documents\\MyDashFiles\\user001\\scripts\\dash\\table')
	print(inits.getNumOfInstances())
	return dash_router(pathname, inits)
	
def dash_router(url, inits):
	children = []
	if inits.render_pointer is not None:
		children = inits.render_pointer(*[], **{})
	else:
		print("render-pointer is none")
	return children

	
