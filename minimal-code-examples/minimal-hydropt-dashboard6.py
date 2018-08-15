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
import copy
from oct2py import octave
from flask import Flask
from flask import send_from_directory
from dash import Dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import random

from pandas import DataFrame, DatetimeIndex
import pandas as pd
import numpy as np
from datetime import date, timedelta

import plotly.graph_objs as go

from RestrictedPython import compile_restricted_function, safe_builtins, limited_builtins, utility_builtins

from pathlib import Path # für inline-io
from functools import lru_cache # für memoization

print("classdefs...")

def get_current_uid():
	return 0	#todo

def transpose(v): return list(map(list, zip(*v)))
	
@lru_cache(maxsize=32)
def load_hydropt_data(filepath):
	print("load_hydopt_data")
	octave.eval("load('" + filepath + "', '-mat')") #todo: separate octave instanz für jeden user
	data = octave.pull('Data')
	return data
	
class CUser(object):
	def __init__(self, uid=None):
		if uid is None:
			self.__uid = get_current_uid()
		else:
			self.__uid = uid
	def getRights(self):return 0
	def getUID(self): return self.__uid

class CRestricted(object):
	__id = 0
	def getID(): return str(CRestricted.__id)
	getID = staticmethod(getID)
	def __init__(self, user): 
		self.__user = user
		CRestricted.__id += 1
	def getUser(self): return self.__user

class CHydropt(CRestricted):
	def __init__(self, user): super().__init__(user)
	def getData(self, filepath): return load_hydropt_data(filepath)
		
class CSafeNP(CRestricted):
	def __init__(self, user=CUser()): super().__init__(user)
	def min(self, v): return np.min(v)
	def max(self, v): return np.max(v)
	def hstack(self, v): return np.hstack(v)
	def vstack(self, v): return np.vstack(v)
	def arange(self, stop, start=0, step=1, dtype=None): return np.arange(start=start, stop=stop, step=step, dtype=dtype)
	def size(self, v) : return v.size
	
	
class CSafeDateUtils(CRestricted):
	def __init__(self, user=CUser()): super().__init__(user)
	def to_datetime(self,v): return pd.to_datetime(v)
	def from_matlab(self,v): return date.fromordinal(int(v)) + timedelta(days=v%1) - timedelta(days = 366) #date.fromordinal(int(v-366))
	def date_range(self, start, end, freq='D', tz=None) : return pd.date_range(start=start, end=end, freq=freq, tz=tz)
	def date_range_from_matlab(self, start, end, freq='H', tz=None) : return self.date_range(start=self.from_matlab(start), end=self.from_matlab(end), freq=freq, tz=tz)
	def months_from_matlab(self, start, end) : return self.date_range_from_matlab(start=start, end=end, freq='MS')
	#df['python_datetime'] = df['matlab_datenum'].apply(lambda x: self.from_matlab(x))
	
class CSafeDF(CRestricted):
	def __init__(self, user=CUser()): super().__init__(user)
	def define(self, matrix, columns): self.__df = DataFrame(matrix, columns=columns)
	def to_dict(self, param): return self.__df.to_dict(param)
	def columns(self): return self.__df.columns

class CSafeLog(CRestricted):
	def __init__(self, user): super().__init__(user)
	def print(self,s): print(s)
	
class CGUIComponent(CRestricted):
	def __init__(self): 
		super().__init__(CUser())
		self.__children = []
	def getChildren(self): return self.__children
	def appendChild(self, c): self.__children.append(c)
	
class CDashComponent(CGUIComponent):
	def setDashRendering(self, r): self.__dashRendering = r
	def getDashRendering(self): return self.__dashRendering
	def appendChild(self,c): 
		super().appendChild(c)
		self.__dashRendering.children.append(c.getDashRendering())
	def aChild(self,c): self.appendChild(c)
	
class CFrame(CDashComponent): #todo: eindeutiger id-parameter 
	def __init__(self, sCaption, type = 'row'): 
		super().__init__()
		self.__caption = sCaption
		self.setCaption(sCaption, type)
	def getCaption(self): return self.__caption
	def setCaption(self, sCaption, type): super().setDashRendering(html.Div(className = type, children = [html.H2(sCaption, className = 'frame-caption')]))
	
class CNumber(CDashComponent):
	def __init__(self, value, unit): 
		super().__init__()
		self.__value = value
		self.__unit = unit
		self.setValue(value)
	def getValue(self): return self.value
	def setValue(self, value): super().setDashRendering(html.P(str(value) + " " + self.__unit, className = 'value'))
	
class CDataTable(CDashComponent):
	def __init__(self, rows, headers): 
		super().__init__()
		self.__np = CSafeNP(super().getUser())
		self.__df = CSafeDF(super().getUser())
		self.setTable(rows, headers)
	def getRows(self): return self.__rows
	def getHeaders(self): return self.__headers
	def __setValues(self, rows): self.__values = self.__np.hstack(rows)
	def setTable(self, rows, headers):
		self.__setValues(rows)
		self.__df.define(self.__values, columns=headers)
		self.__dt = dt.DataTable(
			rows=self.__df.to_dict('records'),
			#optional - sets the order of columns
			#columns=sorted(self.__df.columns()),
			row_selectable=True,
			filterable=True,
			sortable=True,
			selected_row_indices=[]#,
			#id='datatable-gapminder' todo
		)
		self.__rows = rows
		self.__headers = headers
		super().setDashRendering(self.__dt)
		
BASIC_GRAPH_LAYOUT = dict(
	autosize=True,
	height=500,
	#font=dict(color='#CCCCCC'),
	#titlefont=dict(color='#CCCCCC', size='14'),
	margin=dict(l=35, r=35, b=35, t=45),
	hovermode="closest",
	plot_bgcolor="#F9FAFA",
	paper_bgcolor="#F2F2F2",
	legend=dict(font=dict(size=10), orientation='h'),
	title='Satellite Overview'#,
	#mapbox=dict(
	#	accesstoken=mapbox_access_token,
	#	style="dark",
	#	center=dict(
	#		lon=-78.05,
	#		lat=42.54
	#	),
	#	zoom=7,
	#)
)

class CChart(CDashComponent):
	def __init__(self, rows, headers, rowCaptions, title, type='bar', barmode='group'): 
		super().__init__()
		self.setChart(rows, headers, rowCaptions, title, type, barmode)
	def getRows(self): return self.__rows
	def getHeaders(self): return self.__headers
	def getRowCaptions(self): return self._rowCaptions
	def _setParams(self, rows, headers, rowCaptions, title, type='bar', barmode='group'):
		self.__rows = rows
		self.__headers = headers
		self._isTimeSeries = isinstance(rowCaptions, DatetimeIndex)
		self._rowCaptions = rowCaptions if self._isTimeSeries else rowCaptions.flatten()
		self.__title = title
		self.__type = type
		self.__barmode = barmode
	def _setDataMap(self): self._dataMap = lambda x: {'x': self._rowCaptions, 'y': x[0], 'name': x[1], 'type': self.__type}
	def _setDataVec(self): self._dataVec = list(map(lambda x: [x[0].flatten(), x[1]], transpose([self.__rows, self.__headers])))
	def _setData(self):	self._data = list(map(self._dataMap, self._dataVec))
	def _setLayout(self):
		self.__layout = copy.deepcopy(BASIC_GRAPH_LAYOUT)
		self.__layout['title'] = self.__title
		self.__layout['barmode'] = self.__barmode
		if self._isTimeSeries: 
			self.__layout['xaxis'] = dict(rangeselector=dict(
				buttons=list([
					dict(count=1, label='1d', step='day', stepmode='backward'),
					dict(count=7, label='1w', step='day', stepmode='backward'),
					dict(count=1, label='1m', step='month', stepmode='backward'),
					dict(count=6, label='6m', step='month', stepmode='backward'),
					dict(count=12, label='1y', step='month', stepmode='backward'),
					dict(step='all')])),
				rangeslider=dict(), type='date')
	def _setFigure(self): self.__figure = {'data': self._data, 'layout': self.__layout}
	def _getFigure(self): return self.__figure
	def setChart(self, rows, headers, rowCaptions, title, type='bar', barmode='group'):
		self._setParams(rows, headers, rowCaptions, title, type, barmode)
		self._setDataMap()
		self._setDataVec()
		self._setData()
		self._setLayout()
		self._setFigure()
		chart = dcc.Graph(id=super().getID(), figure=self._getFigure())
		super().setDashRendering(chart)
		
#class CTimeSeriesChart(CChart):
#	def _setDataMap(self):
#		super()._dataMap = lambda v:
#			go.Scatter(
#			x=df.Date,
#			y=df['AAPL.High'],
#			name = "AAPL High",
#			line = dict(color = '#17BECF'),
#			opacity = 0.8)




def load_script(scriptpath, additional_globals, safe_locals, name):
	myscript = Path(scriptpath).read_text()
	cr = compile_restricted_function(p = '', body = myscript, name = name, filename = '<inline code>')
	safe_globals = safe_builtins
	safe_globals.update(additional_globals)
	exec(cr.code, safe_globals, safe_locals)
	return safe_locals[name]
		
@lru_cache(maxsize=32)
def load_script_uid(scriptpath, name, uid):
	user = CUser(uid)
	globals = {
		'hydropt' : CHydropt(user), 
		'html' : html, 
		'dt' : dt, 
		'np' : CSafeNP(user), 
		'df' : CSafeDF(user), 
		'log' : CSafeLog(user), 
		'CFrame' : CFrame, 
		'CNumber' : CNumber,
		'CDataTable' : CDataTable,
		'CChart' : CChart,
		'dateUtils' : CSafeDateUtils()}
	return load_script(scriptpath, globals, {}, name)
	
def getSubdirs(path):
	return next(os.walk(path))[1]

class CInits(object):
	__numOfInstances = 0
	def __init__(self, user, path):
		#Kompilieren der Hauptfunktion
		print("init")
		scriptpath = path + '\\render.py'
		self.hydropt = CHydropt(user)
		self.__user = user
		self.render_pointer = load_script_uid(scriptpath, 'render', user.getUID())
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
	id=str(hash('dt0'))
)

print("start servers...")
flask_app = Flask(__name__)
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/d')

print("start dash...")

#dash_app.css.append_css({'external_url': './CSS/stylesheet-oil-and-gas.css'})  # noqa: E501
dash_app.css.config.serve_locally = True
dash_app.layout = html.Div(id='page-content', children=[dcc.Location(id='url', refresh=False), dt0])

@flask_app.route('/')
def hello_world():
	return 'Index page'

#@dash_app.server.route('/static/<path:path>')
@flask_app.route('/static/<path>')
def static_file(path):
	print('LOAD STATIC FILE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
	static_folder = os.path.join(os.getcwd(), 'CSS')
	return send_from_directory(static_folder, path)
	
@flask_app.route('/user/<username>')
def show_user_profile(username):
	# show the user profile for that user
	return 'User %s' % username

@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	print("display_page")
	uid = 1
	user = CUser(uid)
	inits = CInits(user, 'C:\\Users\\SEC\Documents\\MyDashFiles\\user001\\scripts\\dash\\screens\\ResultOverview')
	return dash_router(pathname, inits)

def dash_router(url, inits):
	children = []
	if inits.render_pointer is not None:
		screenComponents = inits.render_pointer(*[], **{})
		if screenComponents is not None:
			#children = screenComponents.getDashRendering()
			children = [html.Link(rel='stylesheet', href='/static/stylesheet-oil-and-gas.css'), screenComponents.getDashRendering()]
		else:
			print("error rendering screen " + url)
	else:
		print("render-pointer is none")
	return children

	
