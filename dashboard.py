# start in linux via
# export FLASK_APP=filename.py
# flask run

# start in windows via
# set FLASK_APP=filename.py
# flask run
# oder
# flask run --host=0.0.0.0 --port=4000


print("imports...")
import inspect, os
from shutil import copyfile
#os.environ["FLASK_APP"] = inspect.getfile(inspect.currentframe())
os.environ["OCTAVE_EXECUTABLE"] = "C:\\Octave\\Octave-4.4.0\\bin\\octave-cli.exe"
import copy
from oct2py import octave
from flask import Flask
from flask import send_from_directory
from dash import Dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import random

from pandas import DataFrame, DatetimeIndex
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime

import plotly.graph_objs as go
map_box_token = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'

from RestrictedPython import compile_restricted_function, safe_builtins, limited_builtins, utility_builtins, compile_restricted

from pathlib import Path # für inline-io
from functools import lru_cache # für memoization

from parser import parse
from compile_callbacks import compile_callbacks
from readObjects import readObjects
import infix
import funcy
import base64
import io
import time

from baseObjects import Restricted
dictionaryOfAllScreenVariables = Restricted.dictionaryOfAllScreenVariables
CSafeDict = Restricted.CSafeDict
CUser = Restricted.CUser
generateId = Restricted.generateId
CRestricted = Restricted.CRestricted
CSafeNP = Restricted.CSafeNP
CSafeFigure = Restricted.CSafeFigure
CSafePoint = Restricted.CSafePoint
CSafeDateUtils = Restricted.CSafeDateUtils
CSafeDF = Restricted.CSafeDF
CSafeLog = Restricted.CSafeLog
safeSplit = Restricted.safeSplit
CSafeMenu = Restricted.CSafeMenu
CSafeList = Restricted.CSafeList

globalDict = CSafeDict()

from components import DashComponent, Chart, Text, Container, StopWaitingForGraphics, DataTable, DatePickerRange, DatePickerSingle, Dropdown, Slider, RangeSlider, InputComponent
from components import TextArea, Checklist, RadioItems, Button, Upload, Map, TopologyMap, Frame, Page, Tabs, NavigationPane, Interval, PieChart, Image, Modal, SelectList, Hist
CDashComponent = DashComponent.CDashComponent
CChart = Chart.CChart
CText = Text.CText
CNumber = Text.CNumber
CNumbers = Text.CNumbers
CContainer = Container.CContainer
CStopWaitingForGraphics = StopWaitingForGraphics.CStopWaitingForGraphics
CDataTable = DataTable.CDataTable
CDatePickerRange = DatePickerRange.CDatePickerRange
CDatePickerSingle = DatePickerSingle.CDatePickerSingle
CDropdown = Dropdown.CDropdown
CSlider = Slider.CSlider
CRangeSlider = RangeSlider.CRangeSlider
CInput = InputComponent.CInput
CTextArea = TextArea.CTextArea
CChecklist = Checklist.CChecklist
CRadioItems = RadioItems.CRadioItems
CButton = Button.CButton
CUpload = Upload.CUpload
CMap = Map.CMap
CTopologyMap = TopologyMap.CTopologyMap
CFrame = Frame.CFrame
CPage = Page.CPage
CTabs = Tabs.CTabs
CNavigationPane = NavigationPane.CNavigationPane
CInterval = Interval.CInterval
CPieChart = PieChart.CPieChart
CImage = Image.CImage
CModal = Modal.CModal
CSelectList = SelectList.CSelectList
CHist = Hist.CHist

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

def getScreenNames(uid):
	path = "user" + uid + "/scripts/dash/screens/"
	screenNames = []
	for root, dirs, files in os.walk(path, topdown=False):
		for name in dirs:
			screenNames.append(os.path.join(name))
	return screenNames

def getNameFromId(id):
	name, type, screen = id.split('-')
	return name

def getTypeFromId(id):
	name, type, screen = id.split('-')
	return type

print("classdefs...")

@lru_cache(maxsize=32) #todo: bei dateiänderungen nicht memoisieren, ggf änderungsdatum mitschicken als argument
def load_hydropt_data(filepath):
	print("load_hydopt_data")
	octave.eval("load('" + filepath + "', '-mat')") #todo: separate octave instanz für jeden user
	data = octave.pull('Data')
	return data

class CHydropt(CRestricted):
	def __init__(self, user):
		super().__init__(user)
	def getData(self, filepath): 
		#todo: dynamsieren
		pathLookup = {
			'model': 'models\\AllInOneTestMOPS8Hydropt110607eIP3.mod'}
		return load_hydropt_data(pathLookup[filepath])
	def getAssetName(self, asset): return self.__assetNames[asset]

@lru_cache(maxsize=32)
def crf_mem(body, name): return compile_restricted_function(p = '', body = body, name = name, filename = '<inline code>')
		
def load_script(scriptpath, additional_globals, safe_locals, name):
	myscript = Path(scriptpath).read_text()
	cr = crf_mem(myscript, name)#compile_restricted_function(p = '', body = myscript, name = name, filename = '<inline code>')
	safe_globals = safe_builtins
	safe_globals.update(additional_globals)
	exec(cr.code, safe_globals, safe_locals)
	return safe_locals[name]

class HDict(dict):
	def __hash__(self): return hash(str(self))#hash(frozenset(self.items()))  #hashable dictionary

def CreateObjectWithScreenName(o, scName, **args):
	return o(**args['args'][0], screenName=scName)

#@lru_cache(maxsize=32) todo führt dazu, dass seite nicht neu geladen wird
def load_script_uid(scriptpath, name, uid, args):
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
		'CStopWaitingForGraphics': CStopWaitingForGraphics,
		'CNumbers': CNumbers,
		'CDatePickerRange': CDatePickerRange,
		'CDatePickerSingle': CDatePickerSingle,
		'CDropdown': CDropdown,
		'CSlider': CSlider,
		'CRangeSlider': CRangeSlider,
		'CInput': CInput,
		'CTextArea': CTextArea,
		'CChecklist': CChecklist,
		'CRadioItems': CRadioItems,
		'CButton': CButton,
		'CUpload': CUpload,
		'CTabs': CTabs,
		'CContainer': CContainer,
		'CMap': CMap,
		'CTopologyMap': CTopologyMap,
		'CInterval': CInterval,
		'CPieChart': CPieChart,
		'CImage': CImage,
		'CSafeList': CSafeList,
		'Create': lambda o, *a: CreateObjectWithScreenName(o=o, scName=args['screen'], args=a),
		'CSafeMenu': CSafeMenu,
		'CModal': CModal,
		'CSelectList': CSelectList,
		'CHist': CHist,
		'globalDict': globalDict,
		'args': CSafeDict(args, user=user)}
	return load_script(scriptpath, globals, {}, name)
	
def getSubdirs(path):
	return next(os.walk(path))[1]

class CInits(object):
	__numOfInstances = 0
	def __init__(self, user, args):
		#Kompilieren der Hauptfunktion
		print("init")
		scriptpath = 'user001\\scripts\\dash\\screens\\' + args['screen'] + '\\render.py'
		menupath = 'user001\\scripts\\dash\\menu\\menu.py'
		self.__user = user
		self.__args = args
		self.render_pointer = load_script_uid(scriptpath, 'render', user.getUID(), HDict(args))
		self.render_menu = load_script_uid(menupath, 'menu', user.getUID(), HDict(args))
		CInits.__numOfInstances += 1
	def getArgs(self): return self.__args
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

dash_app.title = 'HydroOpt2.0'
dash_app.layout = html.Div(id='page-content', children=[dcc.Location(id='url', refresh=False), dt0])

dash_app.css.config.serve_locally = False
dash_app.scripts.config.serve_locally = False
dash_app.config.supress_callback_exceptions = True

#copy css and js files to static folder
STATIC_FOLDER = os.path.join(os.getcwd(), 'static') #'/cygdrive/c/Users/Aleksandr Proskurin/Documents/work/MyDashFiles/static/' #todo temporäres verzeichnis ("with tempfile.TemporaryDirectory() as dirpath:")
STATIC_URL = '/static/'
CSS_PATHS = [
	'CSS/stylesheet-oil-and-gas.css',
	'CSS/jquery-ui-1.12.1/jquery-ui.css',
	'mynodefiles/myapp3/node_modules/jquery.mmenu/dist/css/jquery.mmenu.all.css',
	'mynodefiles/myapp3/node_modules/flickity/dist/flickity.css',
	'Beispiel-HTMLs/stylesheets/demo.css',
	'CSS/loading.css']
JS_PATHS = [
	'mynodefiles/jquery-zeug/node_modules/jquery/dist/jquery.js',
	'CSS/jquery-ui-1.12.1/jquery-ui.js',
	'mynodefiles/myapp3/node_modules/jquery.mmenu/dist/js/jquery.mmenu.min.js',
	'mynodefiles/myapp3/node_modules/jquery.mmenu/dist/js/jquery.mmenu.all.min.js',
	'mynodefiles/myapp3/node_modules/flickity/dist/flickity.pkgd.min.js',
	'mynodefiles/isotope-zeug/node_modules/isotope-layout/dist/isotope.pkgd.min.js',
	'initialize-isotope.js']

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

@flask_app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(flask_app.root_path, 'static'),
							   'favicon.ico')

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
		self.fDash = dash_router /c/ (lambda x: CInits(user, x))
		
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
	if pathname is None: return None
	urlProcessor = CUrlProcessor(pathname, dash_app.url_base_pathname, user = user)
	#inits = CInits(user, 'C:\\Users\\Aleksandr Proskurin\Documents\\work\\MyDashFiles\\user001\\scripts\\dash\\screens\\'+pathname.split("/")[-1])
	#return dash_router(inits, pathname)
	urlProcessor.run()
	return urlProcessor.dashResult

def dash_router(inits, url=''):
	children = []
	if inits.render_pointer is not None:
		screenComponents = inits.render_pointer(*[], **{})
		menu = inits.render_menu(*[], **{})
		navPane = CNavigationPane(menu)
		if screenComponents is not None:
			children = [navPane.getDashRendering(), screenComponents.getDashRendering()]
		else:
			print("error rendering screen " + url)
	else:
		print("render-pointer is none")
	return children
#http://localhost:5000/d/DisplayScreen@screen=ResultOverview&asset=Alperia-VSM
#http://localhost:5000/d/DisplayScreen@screen=test&asset=Alperia-VSM
#http://localhost:5000/d/DisplayScreen@screen=secondTest&asset=Alperia-VSM

def createUpdateCallback(uid, screen):
	objects = readObjects(uid, screen)
	inputLst = []
	stateLst = []
	for obj in objects:
		id = generateId(obj['object'], obj['type'], screen)
		num = 1
		if obj['type'] == 'CDatePickerRange':
			num = 2
			inputLst.append(Input(id, 'start_date'))
			inputLst.append(Input(id, 'end_date'))
		elif obj['type'] ==  'CDatePickerSingle':
			inputLst.append(Input(id, 'date'))
		elif obj['type'] == 'CText':
			inputLst.append(Input(id, 'children'))
		elif obj['type'] == 'CDropdown':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CSlider':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CRangeSlider':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CInput':
			inputLst.append(Input(id,'value'))
		elif obj['type'] == 'CTextArea':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CChecklist':
			inputLst.append(Input(id, 'values'))
		elif obj['type'] == 'CRadioItems':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CButton':
			inputLst.append(Input(id, 'n_clicks'))
		elif obj['type'] == 'CUpload':
			num = 2
			inputLst.append(Input(id, 'contents'))
			inputLst.append(Input(id, 'filename'))
		elif obj['type'] == 'CTabs':
			inputLst.append(Input(id, 'value'))
		elif obj['type'] == 'CDataTable':
			num = 2
			inputLst.append(Input(id, 'selected_row_indices'))
			inputLst.append(Input(id, 'rows'))
		elif obj['type'] == 'CChart':
			inputLst.append(Input(id, 'figure'))
		elif obj['type'] == 'CMap':
			inputLst.append(Input(id, 'figure'))
		elif obj['type'] == 'CTopologyMap':
			inputLst.append(Input(id, 'clickData'))
		elif obj['type'] == 'CInterval':
			inputLst.append(Input(id, 'n_intervals'))
		elif obj['type'] == 'CPieChart':
			inputLst.append(Input(id, 'figure'))
		elif obj['type'] == 'CImage':
			inputLst.append(Input(id, 'children'))
		elif obj['type'] == 'CHist':
			inputLst.append(Input(id, 'figure'))
		else:
			num = 0
		for i in range(num):
			stateLst.append(State(id, 'id'))
	if len(objects) > 0:
		outputId = generateId(objects[0]['object'], objects[0]['type'], screen)
		@dash_app.callback(
			Output(outputId, 'id'),
			inputLst,
			stateLst,
		)
		def update(*args):
			for i in range(len(args) // 2):
				if args[i] is None:
					continue
				id = args[i + len(args) // 2]
				type = getTypeFromId(id)
				name = getNameFromId(id)
				#### TODO:User Id 0 is hardcoded!!!
				object = dictionaryOfAllScreenVariables["0"][screen].get(name)
				if type == 'CDatePickerRange':
					if i + len(args) // 2 + 1 < len(args) and args[i + len(args) // 2 + 1] == args[i + len(args) // 2]:
						object.update(start_date = args[i])
					else:
						object.update(end_date = args[i])
				elif type == 'CDatePickerSingle':
					object.update(args[i])
				elif type == 'CText':
					object.update(args[i])
				elif type == 'CDropdown':
					object.update(args[i])
				elif type == 'CSlider':
					object.update(args[i])
				elif type == 'CRangeSlider':
					object.update(args[i])
				elif type == 'CInput':
					object.update(args[i])
				elif type == 'CTextArea':
					object.update(args[i])
				elif type == 'CChecklist':
					object.update(args[i])
				elif type == 'CRadioItems':
					object.update(args[i])
				elif type == 'CButton':
					object.update(args[i])
				elif type == 'CUpload':
					if i + len(args) // 2 + 1 < len(args) and args[i + len(args) // 2 + 1] == args[i + len(args) // 2]:
						object.update(contents = args[i])
					else:
						object.update(filename = args[i])
				elif type == 'CTabs':
					object.update(args[i])
				elif type == 'CDataTable':
					if i + len(args) // 2 + 1 < len(args) and args[i + len(args) // 2 + 1] == args[i + len(args) // 2]:
						object.update(selected_rows = args[i])
					else:
						object.update(rows = args[i])
				elif type == 'CChart':
					object.update(args[i])
				elif type == 'CMap':
					object.update(args[i])
				elif type == 'CTopologyMap':
					object.update(args[i])
				elif type == 'CInterval':
					object.update(args[i])
				elif type == 'CPieChart':
					object.update(args[i])
				elif type == 'CImage':
					object.update(args[i])
				elif type == 'CHist':
					object.update(args[i])
			return outputId

# find out all the screen names
screenNames = getScreenNames("001")

#Create callbacks for live updates of objects
for screen in screenNames:
	createUpdateCallback("001", screen)

globalCallbacks = {}
f = open("globals/callbacks.py", "r")
source_code = f.read()
locals = {}
byte_code = compile_restricted(
	source = source_code,
	filename = '<inline>',
	mode = 'exec'
)
additional_globals = {
	'date': date, 'timedelta': timedelta, 'datetime': datetime, 'log': CSafeLog(None), 'globalDict': globalDict, 'CSafeNP': CSafeNP(),
	'decodeFile': base64.b64decode, 'split': safeSplit, 'pd': pd, 'io': io, 'CSafeFigure': CSafeFigure, 'CSafeDict': CSafeDict, 'CSafePoint': CSafePoint
}
safe_globals = safe_builtins
safe_globals.update(additional_globals)
exec(byte_code, dict(safe_globals), locals)
globalCallbacks = locals

callbackFunctions = {}
for screen in screenNames:
	path = "user" + "001" + "/scripts/dash/screens/"
	f = open(path + screen + "/callbacks.py", "r")
	source_code = f.read()
	locals = {}
	byte_code = compile_restricted(
		source = source_code,
		filename = '<inline>',
		mode = 'exec'
	)
	#TODO: User Id 0 is hardcoded
	uid = "0"
	if uid not in dictionaryOfAllScreenVariables:
		dictionaryOfAllScreenVariables[uid] = {}
	if screen not in dictionaryOfAllScreenVariables[uid]:
		dictionaryOfAllScreenVariables[uid][screen] = CSafeDict({})
	additional_globals = {
		'date': date, 'timedelta': timedelta, 'datetime': datetime, 'screenVariables': dictionaryOfAllScreenVariables["0"][screen], 'log': CSafeLog(None), 'screen': screen,
		'decodeFile': base64.b64decode, 'split': safeSplit, 'pd': pd, 'io': io, 'CSafeFigure': CSafeFigure, 'CSafeDict': CSafeDict, 'CSafePoint': CSafePoint, 'time': time,
		'getNameFromId' : getNameFromId, 'CSafeList': CSafeList, 'globalDict': globalDict, 'CSafeNP': CSafeNP(),
	}
	safe_globals = safe_builtins
	safe_globals.update(additional_globals)
	exec(byte_code, dict(safe_globals), locals)
	callbackFunctions[screen] = locals

#Extract all the interactions
interactionsDict = parse("001")

for interaction in interactionsDict:
	inputLst = []
	for input in interaction['input']:
		if len(input['type']) < 19 or input['type'][0:19] != 'CSelectList-labels-':
			inputId = generateId(input['object'], input['type'], interaction['screen'])
			inputLst.append(Input(inputId, input['param']))
		else:
			tType, tmp, cnt = input['type'].split('-')
			for i in range(int(cnt)):
				inputId = generateId(input['object'], tType, interaction['screen']) + '-label-' + str(i)
				inputLst.append(Input(inputId, input['param']))
				print(inputId)
	stateLst = []
	if 'state' in interaction:
		for state in interaction['state']:
			stateId = generateId(state['object'], state['type'], interaction['screen'])
			stateLst.append(State(stateId, state['param']))
	outputId = generateId(interaction['output']['object'], interaction['output']['type'], interaction['screen'])
	dash_app.callback(
		Output(outputId, interaction['output']['param']),
		inputLst,
		stateLst,
	)(callbackFunctions[interaction['screen']][interaction['callback']] if interaction['callback'] in callbackFunctions[interaction['screen']] else globalCallbacks[interaction['callback']])