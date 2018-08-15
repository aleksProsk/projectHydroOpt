# start in linux via
# export FLASK_APP=filename.py
# flask run

# start in windows via
# set FLASK_APP=filename.py
# flask run
# oder
# flask run --host=0.0.0.0


print("imports...")
import inspect, os
from shutil import copyfile
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

import infix
import funcy

@infix.div_infix
def m(f,x): return list(map(f,x))

@infix.div_infix
def M(f,g): return lambda x: f /m/ g(x)

@infix.div_infix
def c(*f): return funcy.compose(*f)

# Beispiel: (math.sin /c/ math.cos /c/ math.tan) /m/ [1,2,3]

@infix.div_infix
def a(f,x): return f(x)

def split(s): return lambda x: x.split(s)

def transpose(v): return list(map(list, zip(*v)))

def flatten(lis):
	"""Given a list, possibly nested to any level, return it flattened."""
	new_lis = []
	for item in lis:
		if type(item) == type([]):
			new_lis.extend(flatten(item))
		else:
			new_lis.append(item)
	return new_lis
	
print("classdefs...")

def get_current_uid():
	return 0	#todo
	
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
	def to_str(self, d) : return d.strftime("%Y-%m-%d %H:%M")
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
	def __init__(self, sCaption, type = 'frame', isDynamic = True, width = 0.25, height = 0, smallScreenFactor = 2, tinyScreenFactor = 4, captionType = html.H2): 
		super().__init__()
		self._captionType = captionType
		self._caption = sCaption
		self._width = width
		self._height = height
		self._smallScreenFactor = smallScreenFactor
		self._tinyScreenFactor = tinyScreenFactor
		self._type = type
		if isDynamic: self._type = type + ' grid-item varsize' + '-' + str(round(width*100)) + '-' + str(round(height*100)) + '-' + str(round(smallScreenFactor)) + '-' + str(round(tinyScreenFactor))
		self.setCaption(sCaption)
	def getCaption(self): return self._caption
	def setCaption(self, sCaption): super().setDashRendering(html.Div(className = self._type, children = [self._captionType(sCaption, className = 'frame-caption')]))
	
class CPage(CFrame): #todo: eindeutiger id-parameter 
	def __init__(self, sCaption): 
		super().__init__(sCaption, type = 'content', isDynamic = False, captionType = html.H1)
		
		
class CText(CDashComponent):
	def __init__(self, text): 
		super().__init__()
		self.setText(text)
	def getText(self): return self.text
	def setText(self, text): 
		self.__text = text
		super().setDashRendering(html.P(str(text), className = 'text'))
	
class CNumber(CText):
	def __init__(self, value, unit):
		super().__init__(str(value) + " " + unit)
		self.__value = value
		self.__unit = unit
		self.setValue(value, unit)
	def getValue(self): return self.__value
	def setValue(self, value, unit=None): 
		if unit is None: unit=self.__unit
		super().setText(str(value) + " " + unit)
		self.__value = value
		self.__unit = unit
		
class CNumbers(CText):
	def __init__(self, keys_values_units, separator = '│'):
		self.__keys_values_units = keys_values_units
		self.__separator = separator
		super().__init__(self._getText())
	def _getText(self): return (' ' + self.__separator + ' ').join((lambda x: x[0] + ': ' + str(x[1]) + ' ' + x[2]) /m/ self.__keys_values_units)
	
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
	def _setDataVec(self): self._dataVec = (lambda x: [x[0].flatten(), x[1]]) /m/ transpose([self.__rows, self.__headers])  #list(map(lambda x: [x[0].flatten(), x[1]], transpose([self.__rows, self.__headers])))
	def _setData(self):	self._data = self._dataMap /m/ self._dataVec #list(map(self._dataMap, self._dataVec))
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
		'dateUtils' : CSafeDateUtils(),
		'CPage': CPage,
		'CText': CText,
		'CNumbers': CNumbers}
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
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/d/')

print("start dash...")

dash_app.layout = html.Div(id='page-content', children=[dcc.Location(id='url', refresh=False), dt0])

dash_app.css.config.serve_locally = False
dash_app.scripts.config.serve_locally = False

#copy css and js files to static folder
STATIC_FOLDER = os.path.join(os.getcwd(), 'static') #'/cygdrive/c/Users/SEC/Documents/MyDashFiles/static/' #todo temporäres verzeichnis ("with tempfile.TemporaryDirectory() as dirpath:")
STATIC_URL = '/static/'
CSS_PATHS = [
	'/cygdrive/c/Users/SEC/Documents/MyDashFiles/CSS/stylesheet-oil-and-gas.css',
	'/cygdrive/c/Users/SEC/Documents/MyDashFiles/CSS/jquery-ui-1.12.1/jquery-ui.css',
	'/cygdrive/c/Users/SEC/Documents/mynodefiles/myapp3/node_modules/jquery.mmenu/dist/css/jquery.mmenu.all.css',
	'/cygdrive/c/Users/SEC/Documents/mynodefiles/myapp3/node_modules/flickity/dist/flickity.css',
	'/cygdrive/c/Users/SEC/Documents/MyDashFiles/Beispiel-HTMLs/stylesheets/demo.css']
JS_PATHS = [
	'/cygdrive/c/Users/SEC/Documents/mynodefiles/jquery-zeug/node_modules/jquery/dist/jquery.js',
	'/cygdrive/c/Users/SEC/Documents/MyDashFiles/CSS/jquery-ui-1.12.1/jquery-ui.js',
	'/cygdrive/c/Users/SEC/Documents/mynodefiles/myapp3/node_modules/jquery.mmenu/dist/js/jquery.mmenu.min.js',
	'/cygdrive/c/Users/SEC/Documents/mynodefiles/myapp3/node_modules/jquery.mmenu/dist/js/jquery.mmenu.all.min.js',
	'/cygdrive/c/Users/SEC/Documents/mynodefiles/myapp3/node_modules/flickity/dist/flickity.pkgd.min.js',
	'/cygdrive/c/Users/SEC/Documents/mynodefiles/isotope-zeug/node_modules/isotope-layout/dist/isotope.pkgd.min.js',
	'/cygdrive/c/Users/SEC/Documents/MyDashFiles/initialize-isotope.js']

(lambda x: copyfile(x, os.path.join(STATIC_FOLDER, os.path.basename(x)))) /m/ (CSS_PATHS + JS_PATHS)
(lambda x: dash_app.css.append_css			({"external_url": STATIC_URL + x})) /m/ (os.path.basename /m/ CSS_PATHS)
(lambda x: dash_app.scripts.append_script	({"external_url": STATIC_URL + x})) /m/ (os.path.basename /m/ JS_PATHS)

@flask_app.route('/')
def hello_world():
	return 'Index page'

#@dash_app.server.route('/static/<path:path>')
@flask_app.route(STATIC_URL + '<path>')
def static_file(path): return send_from_directory(STATIC_FOLDER, path)
	
@flask_app.route('/user/<username>')
def show_user_profile(username):
	# show the user profile for that user
	return 'User %s' % username

class CUrlProcessor(CRestricted):
#bsp. path: http://localhost:5000/d/DisplayScreen@screen=ResultOverview&theme=grey/CalcFourier@data=data
	def __init__(self, sUrl, sBasePath, sFuncSplitter='/', sHeadSplitter='@', sArgsSplitter='&', sKeyValueSplitter='=', user=CUser()):
		super().__init__(user)
		
		self.hasFunctionCalls = False
		self.callStringList = []
		self.numberOfFunctionCalls = 0
		self.nestedCallList = []
		self.argList = []
		self.funcList = []
		self.results = None
		self.dashResult = None
		
		baseSplit = sUrl.split(sBasePath)
		self.hasFunctionCalls = len(baseSplit) > 1
		if self.hasFunctionCalls:
			callString = ''.join(baseSplit[1:])
			self.callStringList = callString.split(sFuncSplitter)
			self.numberOfFunctionCalls = len(self.callStringList)
			if self.numberOfFunctionCalls > 0:
				self.nestedCallList = (lambda x: [flatten(x[0]), dict(x[1])]) /m/ (split(sKeyValueSplitter) /M/ split(sArgsSplitter) /M/ split(sHeadSplitter) /M/ split(sFuncSplitter))(callString)
				self.funcList = transpose(self.nestedCallList)[0]
				self.argList = transpose(self.nestedCallList)[1]
				#callString='f&g?a=x&b=y/h?c=z/d?u=ux' -> [[['f', 'g'], {'a': 'x', 'b': 'y'}], [['h'], {'c': 'z'}], [['d'], {'u': 'ux'}]]
				
				#callString = 'f&g?a=x&b=y/h?c=z/d?x'
				#self.nestedCallList = list(map(lambda x: list(map(lambda y: list(map(lambda z: z.split('='), y.split('&'))), x.split('?'))), callString.split('/')))
				# -> [[[['f'], ['g']], [['a', 'x'], ['b', 'y']]], [[['h']], [['c', 'z']]], [[['d']], [['x']]]]
		
		self.sDashFunction = 'DisplayScreen'
		self.hasDashFunction = [self.sDashFunction] in self.funcList
		self.idxDashFunction = self.funcList.index([self.sDashFunction]) if self.hasDashFunction else None
		self.fDash = dash_router /c/ (lambda x: CInits(user, 'C:\\Users\\SEC\Documents\\MyDashFiles\\user001\\scripts\\dash\\screens\\' + x['screen']))
		
		self.funcLookup = {}
		self.funcLookup[self.sDashFunction] = self.fDash
		
	def run(self): 
		if self.hasFunctionCalls: 
			print((lambda x: x[0]) /m/ self.nestedCallList)
			def buildFuncComposition(fstrings): return funcy.compose(*(lambda fstring: self.funcLookup[fstring]) /m/ fstrings)
			self.result = (lambda x: buildFuncComposition(x[0])(x[1])) /m/ self.nestedCallList #bildet (fi1@*fi2@*...)(xi1, xi2, ...) für alle i = 1, ..., numberOfFunctionCalls
			self.dashResult = self.result[self.idxDashFunction]



				
@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	print("display_page ")
	uid = 1
	user = CUser(uid)
	urlProcessor = CUrlProcessor(pathname, dash_app.url_base_pathname, user = user)
	#inits = CInits(user, 'C:\\Users\\SEC\Documents\\MyDashFiles\\user001\\scripts\\dash\\screens\\'+pathname.split("/")[-1])
	#return dash_router(inits, pathname)
	urlProcessor.run()
	return urlProcessor.dashResult

def dash_router(inits, url=''):
	children = []
	if inits.render_pointer is not None:
		screenComponents = inits.render_pointer(*[], **{})
		if screenComponents is not None:
			children = screenComponents.getDashRendering()
		else:
			print("error rendering screen " + url)
	else:
		print("render-pointer is none")
	return children

	
