# start in linux via
# export FLASK_APP=filename.py
# flask run

# start in windows via
# set FLASK_APP=filename.py
# flask run
# oder
# flask run --host=0.0.0.0 --port=4000


print("imports...")
import inspect, os, math, scipy, urllib
from shutil import copyfile
#os.environ["FLASK_APP"] = inspect.getfile(inspect.currentframe())
os.environ["OCTAVE_EXECUTABLE"] = "C:\\Octave\\Octave-4.4.0\\bin\\octave-cli.exe"
import copy
from oct2py import octave
from flask import Flask
from flask import send_from_directory
from flask import request
from dash import Dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import random
import simplejson as json

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
CSafeMatlab = Restricted.CSafeMatlab
CSafeStr = Restricted.CSafeStr

globalDict = CSafeDict()

from components import DashComponent, Chart, Text, Container, StopWaitingForGraphics, DataTable, DatePickerRange, DatePickerSingle, Dropdown, Slider, RangeSlider, InputComponent
from components import TextArea, Checklist, RadioItems, Button, Upload, Map, TopologyMap, Frame, Page, Tabs, NavigationPane, Interval, PieChart, Image, Modal, SelectList, Hist, YMap
from components import Topology, TopologyRedactor
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
CYMap = YMap.CYMap
CTopology = Topology.CTopology
CTopologyRedactor = TopologyRedactor.CTopologyRedactor

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
			#'model': 'models\\engl.mod'}
			#'model': 'models\\BER_.mod'}
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
		'CSafeMatlab': CSafeMatlab(),
		'globalDict': globalDict,
		'CSafeStr': CSafeStr,
		'CYMap': CYMap,
		'CTopology': CTopology,
		'CTopologyRedactor': CTopologyRedactor,
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
	'initialize-isotope.js',
	'scripts.js',
	'ymapsAPI.js',
	'ymap.js',
	'fabric.js',
	'topology.js']

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

tempMatlab = CSafeMatlab()
@flask_app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
	shortname = request.form['shortname']
	lat = request.form['lat']
	lon = request.form['lon']
	print(shortname, lat, lon)
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	for i in range(assets.len()):
		if assets.get(i).Shortname == shortname:
			#print(assets.get(i).Position)
			octave.eval('Data.Asset('+str(i+1)+').Position = [' + lat + ', ' + lon + ', 0, 0];')
			#tempMatlab.setField(assets.get(i), 'Position', [[float(lat), float(lon), 0, 0]])
			#print(assets.get(i).Position)
	globalDict.set('hydroptModel', octave.pull('Data'))
	return shortname

@flask_app.route('/selectElement', methods = ['POST'])
def get_post_javascript_asset_selection():
	name = request.form['name']
	typ = request.form['type']
	globalDict.set('selectedElement', name)
	globalDict.set('selectedType', typ)
	return name

@flask_app.route('/postTopology', methods = ['POST'])
def get_post_javascript_topology_data():
	#TODO: TimeLags
	names = request.form.getlist('names[]')
	types = request.form.getlist('types[]')
	x = request.form.getlist('x[]')
	y = request.form.getlist('y[]')
	operatesFrom = request.form.getlist('operatesFrom[]')
	operatesTo = request.form.getlist('operatesTo[]')
	assetName = request.form['assetName']
	print(names)
	print(types)
	print(x)
	print(y)
	print(operatesFrom)
	print(operatesTo)
	print(assetName)
	pos = -1
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	for i in range(assets.len()):
		if assets.get(i).Shortname == assetName:
			pos = i
			break
	if pos == -1:
		return names[0]
	#DELETE
	#Reservoirs
	while (True):
		was = False
		data = CSafeList(globalDict.get('hydroptModel').Asset)
		if globalDict.get('hydroptModel').nAssets == 1:
			assets = CSafeList([globalDict.get('hydroptModel').Asset])
		else:
			assets = CSafeList(lst=data.get(0))
		if assets.get(pos).Topology.nRes == 1:
			reservoirs = CSafeList([assets.get(pos).Reservoir])
		else:
			reservoirs = CSafeList(CSafeList(assets.get(pos).Reservoir).get(0))
		for i in range(reservoirs.len()):
			if reservoirs.get(i).Shortname not in names:
				octave.eval('Top=Data.Asset('+str(pos+1)+').Topology; Top.nRes=Top.nRes-1; Top.Reservoir('+str(i+1)+')=[]; Data.Asset('+str(pos+1)+').Reservoir('+str(i+1)+')=[];')
				octave.eval('Idx=find([Top.Engine.OperatesFrom]=='+str(i+1)+'); for i=Idx Top.Engine(i).OperatesFrom=0; end; Idx=find([Top.Engine.OperatesTo]=='+str(i+1)+');')
				octave.eval('for i=Idx Top.Engine(i).OperatesTo=0; end; Idx=find([Top.Engine.OperatesFrom]>'+str(i+1)+');  for i=Idx Top.Engine(i).OperatesFrom=Top.Engine(i).OperatesFrom-1; end')
				octave.eval('Idx=find([Top.Engine.OperatesTo]>'+str(i+1)+'); for i=Idx Top.Engine(i).OperatesTo=Top.Engine(i).OperatesTo-1; end ')
				octave.eval('if Top.nFlows>0 Idx=find([Top.Flow.OperatesFrom]=='+str(i+1)+'); for i=Idx Top.Flow(i).OperatesFrom=0; end; Idx=find([Top.Flow.OperatesTo]=='+str(i+1)+'); for i=Idx Top.Flow(i).OperatesTo = 0; end; end')
				octave.eval('if Top.nFlows>0 Idx=find([Top.Flow.OperatesFrom]>'+str(i+1)+'); for i=Idx Top.Flow(i).OperatesFrom=Top.Flow(i).OperatesFrom-1; end; Idx = find([Top.Flow.OperatesTo]>'+str(i+1)+'); for i=Idx Top.Flow(i).OperatesTo=Top.Flow(i).OperatesTo-1; end; end')
				octave.eval('Idx=find([Top.Reservoir.SpillsToRes]=='+str(i+1)+'); for i=Idx Top.Reservoir(i).SpillsToRes=0; end; Idx=find([Top.Reservoir.SpillsToRes]>'+str(i+1)+'); for i=Idx Top.Reservoir(i).SpillsToRes=Top.Reservoir(i).SpillsToRes-1; end')
				octave.eval('Data.Asset('+str(pos+1)+').Topology=Top;')
				globalDict.set('hydroptModel', octave.pull('Data'))
				was = True
				break
		if was == False:
			break
	#Flows
	if assets.get(pos).Topology.nFlows > 0:
		while (True):
			was = False
			data = CSafeList(globalDict.get('hydroptModel').Asset)
			if globalDict.get('hydroptModel').nAssets == 1:
				assets = CSafeList([globalDict.get('hydroptModel').Asset])
			else:
				assets = CSafeList(lst=data.get(0))
			if assets.get(pos).Topology.nFlows == 1:
				flows = CSafeList([assets.get(pos).Flow])
			else:
				flows = CSafeList(CSafeList(assets.get(pos).Flow).get(0))
			for i in range(flows.len()):
				if flows.get(i).Shortname not in names:
					octave.eval('Top=Data.Asset('+str(pos+1)+').Topology; Top.nFlows=Top.nFlows-1; Top.Flow('+str(i+1)+')=[]; Data.Asset('+str(pos+1)+').Flow('+str(i+1)+')=[]; Data.Asset('+str(pos+1)+').Topology=Top;')
					globalDict.set('hydroptModel', octave.pull('Data'))
					was = True
					break
			if was == False:
				break
	#Turbines and pumps
	while (True):
		was = False
		data = CSafeList(globalDict.get('hydroptModel').Asset)
		if globalDict.get('hydroptModel').nAssets == 1:
			assets = CSafeList([globalDict.get('hydroptModel').Asset])
		else:
			assets = CSafeList(lst=data.get(0))
		if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
			engines = CSafeList([assets.get(pos).Engine])
		else:
			engines = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
		for i in range(engines.len()):
			if engines.get(i).Shortname not in names:
				if i < assets.get(pos).Topology.nTurbines:
					octave.eval('Top=Data.Asset('+str(pos+1)+').Topology; Top.nTurbines=Top.nTurbines-1; Top.Engine('+str(i+1)+')=[]; Data.Asset('+str(pos+1)+').Engine('+str(i+1)+')=[];')
					octave.eval('if ~isempty(Data.Asset('+str(pos+1)+').EngineAlternatives) Data.Asset('+str(pos+1)+').EngineAlternatives('+str(i+1)+',:) = []; Data.Asset('+str(pos)+').EngineAlternatives(:,'+str(i+1)+') = []; end')
				else:
					octave.eval('Top=Data.Asset('+str(pos+1)+').Topology; Top.nPumps=Top.nPumps-1; Top.Engine('+str(i+1)+')=[]; Data.Asset('+str(pos+1)+').Engine('+str(i+1)+')=[];')
					octave.eval('if ~isempty(Data.Asset('+str(pos+1)+').EngineAlternatives) Data.Asset('+str(pos+1)+').EngineAlternatives('+str(i+1)+',:) = []; Data.Asset('+str(pos+1)+').EngineAlternatives(:,'+str(i+1)+') = []; end;')
				octave.eval('Data.Asset(' + str(pos + 1) + ').Topology=Top;')
				globalDict.set('hydroptModel', octave.pull('Data'))
				was = True
				break
		if was == False:
			break
	#ADD
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	names_r = []
	names_t = []
	names_p = []
	names_f = []
	for i in range(len(names)):
		if types[i] == 'reservoir':
			names_r.append(names[i])
		elif types[i] == 'pump':
			names_p.append(names[i])
		elif types[i] == 'turbine':
			names_t.append(names[i])
		else:
			names_f.append(names[i])
	#Reservoirs
	if assets.get(pos).Topology.nRes == 1:
		reservoirs = CSafeList([assets.get(pos).Reservoir])
	else:
		reservoirs = CSafeList(CSafeList(assets.get(pos).Reservoir).get(0))
	for i in range(len(names_r)):
		was = False
		for j in range(reservoirs.len()):
			if reservoirs.get(j).Shortname == names_r[i]:
				was = True
				break
		if was == True:
			continue
		#Fix reading problems
		if assets.get(pos).Topology.nRes > 1:
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Reservoir(1), 'ExpectedInflow')==0 Expected=[]; Expected.Val=[]; Expected.Start=0; Expected.End=0; [Data.Asset("+str(pos+1)+").Reservoir(:).ExpectedInflow]=deal(Expected); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Reservoir(1), 'MaxLevel')==0 Mx=[]; Mx.Val=[]; Mx.Start=0; Mx.End=0; [Data.Asset("+str(pos+1)+").Reservoir(:).MaxLevel]=deal(Mx); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Reservoir(1), 'MinLevel')==0 Mn=[]; Mn.Val=[]; Mn.Start=0; Mn.End=0; [Data.Asset("+str(pos+1)+").Reservoir(:).MinLevel]=deal(Mn); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Reservoir(1), 'M3_to_MWh')==0 M3=[]; M3.X=[]; M3.Y=[]; [Data.Asset("+str(pos+1)+").Reservoir(:).M3_to_MWh]=deal(M3); end;")
			octave.eval("Data.Asset("+str(pos+1)+").Reservoir=orderfields(Data.Asset("+str(pos+1)+").Reservoir, {'ID', 'Name', 'Shortname', 'IsStochastic', 'MaxLevelFile', 'MinLevelFile', 'MWh2CubicMetresFile', 'InfiltrationLossesFile', 'Inflow', 'ExpectedInflow', 'Spill', 'Scheduler', 'StochasticWaterManager', 'ScenarioWaterManager', 'MaxLevel', 'MinLevel', 'M3_to_MWh'});")
		else:
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Reservoir(1), 'ExpectedInflow')==0 Expected=[]; Expected.Val=[]; Expected.Start=0; Expected.End=0; [Data.Asset("+str(pos+1)+").Reservoir(1).ExpectedInflow]=deal(Expected); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Reservoir(1), 'MaxLevel')==0 Mx=[]; Mx.Val=[]; Mx.Start=0; Mx.End=0; [Data.Asset("+str(pos+1)+").Reservoir(1).MaxLevel]=Mx; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Reservoir(1), 'MinLevel')==0 Mn=[]; Mn.Val=[]; Mn.Start=0; Mn.End=0; [Data.Asset("+str(pos + 1)+").Reservoir(1).MinLevel]=Mn; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Reservoir(1), 'M3_to_MWh')==0 M3=[]; M3.X=[]; M3.Y=[]; [Data.Asset("+str(pos+1)+").Reservoir(1).M3_to_MWh]=M3; end;")
			octave.eval("Data.Asset("+str(pos+1)+").Reservoir=orderfields(Data.Asset("+str(pos+1)+").Reservoir, {'ID', 'Name', 'Shortname', 'IsStochastic', 'MaxLevelFile', 'MinLevelFile', 'MWh2CubicMetresFile', 'InfiltrationLossesFile', 'Inflow', 'ExpectedInflow', 'Spill', 'Scheduler', 'StochasticWaterManager', 'ScenarioWaterManager', 'MaxLevel', 'MinLevel', 'M3_to_MWh'});")
		#adding
		octave.eval('Top=Data.Asset('+str(pos+1)+').Topology; nRes=Top.nRes+1; Data.Asset('+str(pos+1)+').Topology.nRes=nRes; Data.Asset('+str(pos+1)+').Topology.Reservoir(nRes).Btn=[0.2+0.02*nRes 0.8+0.02*nRes];')
		octave.eval("Data.Asset("+str(pos+1)+").Topology.Reservoir(nRes).SpillsToRes = 0; Res=[]; Res.ID=datenum(clock); Res.Name=''; Res.Shortname='"+names_r[i]+"'; Res.IsStochastic=1; Res.MaxLevelFile='';")
		octave.eval("Res.MinLevelFile='0'; Res.MWh2CubicMetresFile='%AutoCalc'; Res.InfiltrationLossesFile=''; Res.Inflow.MinimumInflowFile='0'; Res.Inflow.MaximumInflowFile='0';")
		octave.eval("Res.Inflow.ExpectedInflowFile='0'; Res.ExpectedInflow.Val=[]; Res.ExpectedInflow.Start=0; Res.ExpectedInflow.End=0; Res.Inflow.DayPatternFile = '';")
		octave.eval("Res.Inflow.InflowScenarioFolder=''; Res.Inflow.TransitionProbabilityFile=''; Res.Spill.Capacity=1000; Res.Spill.Efficiency=100; Res.Scheduler.StartLevel=[]; Res.Scheduler.EndLevel=[];")
		octave.eval("Res.Scheduler.LevelDiff=[]; Res.Scheduler.WaterValue=[]; Res.Scheduler.Deviation=[]; Res.Scheduler.HalfLife=[]; Res.Scheduler.Result=[]; Res.StochasticWaterManager.nStatesReservoir=101;")
		octave.eval("Res.StochasticWaterManager.DMin=-10; Res.StochasticWaterManager.DMax=0; Res.StochasticWaterManager.StartLevel=[]; Res.StochasticWaterManager.Result=[];")
		octave.eval("Res.ScenarioWaterManager.StartLevel=[]; Res.ScenarioWaterManager.EndLevel=[]; Res.ScenarioWaterManager.Deviation=[]; Res.ScenarioWaterManager.HalfLife=[];")
		octave.eval("Res.ScenarioWaterManager.Result=[]; Res.MaxLevel.Val=[]; Res.MaxLevel.Start=0; Res.MaxLevel.End=0; Res.MinLevel.Val=[]; Res.MinLevel.Start=0; Res.MinLevel.End=0;")
		octave.eval("Res.M3_to_MWh.X=[]; Res.M3_to_MWh.Y=[]; Data.Asset("+str(pos+1)+").Reservoir(nRes)=Res;")
	globalDict.set('hydroptModel', octave.pull('Data'))
	#Flows
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	if assets.get(pos).Topology.nFlows == 0:
		flows = CSafeList([])
	elif assets.get(pos).Topology.nFlows == 1:
		flows = CSafeList([assets.get(pos).Flow])
	else:
		flows = CSafeList(CSafeList(assets.get(pos).Flow).get(0))
	for i in range(len(names_f)):
		was = False
		for j in range(flows.len()):
			if flows.get(j).Shortname == names_f[i]:
				was = True
				break
		if was == True:
			continue
		octave.eval("Top=Data.Asset("+str(pos+1)+").Topology; nFlows=Top.nFlows+1; Data.Asset("+str(pos+1)+").Topology.nFlows=nFlows; Data.Asset("+str(pos+1)+").Topology.Flow(nFlows).Btn=[0.2+0.02*nFlows 0.2+0.02*nFlows];")
		octave.eval("Data.Asset("+str(pos+1)+").Topology.Flow(nFlows).OperatesFrom=0; Data.Asset("+str(pos+1)+").Topology.Flow(nFlows).OperatesTo=0; ")
		octave.eval("for idxFlow=1:(nFlows-1) if ~isfield(Data.Asset("+str(pos+1)+").Flow(idxFlow), 'MaxFlow') Data.Asset("+str(pos+1)+").Flow(idxFlow).MaxFlow.Val=[]; Data.Asset("+str(pos+1)+").Flow(idxFlow).MaxFlow.Start=0; Data.Asset("+str(pos+1)+").Flow(idxFlow).MaxFlow.End=0; Data.Asset("+str(pos+1)+").Flow(idxFlow).MinFlow.Val=[]; Data.Asset("+str(pos+1)+").Flow(idxFlow).MinFlow.Start=0; Data.Asset("+str(pos+1)+").Flow(idxFlow).MinFlow.End=0; end; end;")
		octave.eval("Flow=[]; Flow.ID=datenum(clock); Flow.Name=''; Flow.Shortname='"+names_f[i]+"'; Flow.MaxFlowFile=''; Flow.MinFlowFile='0'; Flow.Scheduler.Result=[]; Flow.ScenarioWaterManager.Result=[];")
		octave.eval("Flow.MaxFlow.Val=[]; Flow.MaxFlow.Start=0; Flow.MaxFlow.End=0; Flow.MinFlow.Val=[]; Flow.MinFlow.Start=0; Flow.MinFlow.End=0;")
		octave.eval("if nFlows==1 Data.Asset("+str(pos+1)+").Flow=Flow; else Data.Asset("+str(pos+1)+").Flow(nFlows)=Flow; end;")
	globalDict.set('hydroptModel', octave.pull('Data'))
	#Turbines
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
		engines = CSafeList([assets.get(pos).Engine])
	else:
		engines = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
	for i in range(len(names_t)):
		was = False
		for j in range(int(assets.get(pos).Topology.nTurbines)):
			if engines.get(j).Shortname == names_t[i]:
				was = True
				break
		if was == True:
			continue
		#fix reading problems
		if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps > 1:
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MaxFlow')==0 Mx=[]; Mx.Val=[]; Mx.Start=0; Mx.End=0; [Data.Asset("+str(pos+1)+").Engine(:).MaxFlow]=deal(Mx); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MinRunFlow')==0 Mn=[]; Mn.Val=[]; Mn.Start=0; Mn.End=0; [Data.Asset("+str(pos+1)+").Engine(:).MinRunFlow]=deal(Mn); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MinFlow')==0 Mn=[]; Mn.Val=[]; Mn.Start=0; Mn.End=0; [Data.Asset("+str(pos+1)+").Engine(:).MinFlow]=deal(Mn); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'Characteristic')==0 Ch=[]; Ch.X=[]; Ch.Y=0; [Data.Asset("+str(pos+1)+").Engine(:).Characteristic]=deal(Ch); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PowerCharacteristic')==0 PCh=[]; PCh.X=[]; PCh.Y=0; [Data.Asset("+str(pos+1)+").Engine(:).PowerCharacteristic]=deal(PCh); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PowerCharacteristicIsAbsolute')==0 [Data.Asset("+str(pos+1)+").Engine(:).PowerCharacteristicIsAbsolute]=deal(0); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'bUseReservoirAbove')==0 [Data.Asset("+str(pos+1)+").Engine(:).bUseReservoirAbove]=deal(true); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PriceFile')==0 [Data.Asset("+str(pos+1)+").Engine(:).PriceFile]=deal([]); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'Price')==0 Pr=[]; Pr.Val=[]; Pr.Start=0; Pr.End=0; [Data.Asset("+str(pos+1)+").Engine(:).Price]=deal(Pr); end;")
			octave.eval("Data.Asset("+str(pos+1)+").Engine=orderfields(Data.Asset("+str(pos+1)+").Engine, {'ID', 'Name', 'Shortname', 'Type', 'MaxFlowFile', 'MaxFlow', 'MinRunningFlowFile', 'MinRunFlow', 'MinFlowFile', 'MinFlow', 'StartupFile', 'ShutdownFile', 'EngineCharacteristicFile', 'Characteristic', 'EnginePowerCharacteristicFile', 'PowerCharacteristic', 'PowerCharacteristicIsAbsolute', 'bUseReservoirAbove', 'OperatingCosts', 'StartupCosts', 'ShutdownCosts', 'MaxNofOperatingHours', 'MinNofOperatingHours', 'MinNofIdleHours', 'MinProductionHoursValue', 'MaxProductionHoursValue', 'MaxProductionHoursPeriod', 'MinStartsValue', 'MaxStartsValue', 'MaxStartsPeriod', 'PriceFile', 'Price', 'MaxNofProductionHours', 'MaxNofStarts', 'ProductionReserve', 'ConsumptionReserve', 'IncludeInReserve', 'Scheduler', 'ScenarioWaterManager'});")
		else:
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MaxFlow')==0 Mx=[]; Mx.Val=[]; Mx.Start=0; Mx.End=0; [Data.Asset("+str(pos+1)+").Engine(1).MaxFlow]=Mx; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MinRunFlow')==0 Mn=[]; Mn.Val=[]; Mn.Start=0; Mn.End=0; [Data.Asset("+str(pos+1)+").Engine(1).MinRunFlow]=Mn; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MinFlow')==0 Mn=[]; Mn.Val=[]; Mn.Start=0; Mn.End=0; [Data.Asset("+str(pos+1)+").Engine(1).MinFlow]=Mn; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'Characteristic')==0 Ch=[]; Ch.X=[]; Ch.Y=0; [Data.Asset("+str(pos+1)+").Engine(1).Characteristic]=Ch; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PowerCharacteristic')==0 PCh=[]; PCh.X=[]; PCh.Y=0; [Data.Asset("+str(pos+1)+").Engine(1).PowerCharacteristic]=PCh; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PowerCharacteristicIsAbsolute')==0 [Data.Asset("+str(pos+1)+").Engine(1).PowerCharacteristicIsAbsolute]=0; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'bUseReservoirAbove')==0 [Data.Asset("+str(pos+1)+").Engine(1).bUseReservoirAbove]=true; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PriceFile')==0 [Data.Asset("+str(pos+1)+").Engine(1).PriceFile]=[]; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'Price')==0 Pr=[]; Pr.Val=[]; Pr.Start=0; Pr.End=0; [Data.Asset("+str(pos+1)+").Engine(1).Price]=Pr; end;")
			octave.eval("Data.Asset("+str(pos+1)+").Engine=orderfields(Data.Asset("+str(pos+1)+").Engine, {'ID', 'Name', 'Shortname', 'Type', 'MaxFlowFile', 'MaxFlow', 'MinRunningFlowFile', 'MinRunFlow', 'MinFlowFile', 'MinFlow', 'StartupFile', 'ShutdownFile', 'EngineCharacteristicFile', 'Characteristic', 'EnginePowerCharacteristicFile', 'PowerCharacteristic', 'PowerCharacteristicIsAbsolute', 'bUseReservoirAbove', 'OperatingCosts', 'StartupCosts', 'ShutdownCosts', 'MaxNofOperatingHours', 'MinNofOperatingHours', 'MinNofIdleHours', 'MinProductionHoursValue', 'MaxProductionHoursValue', 'MaxProductionHoursPeriod', 'MinStartsValue', 'MaxStartsValue', 'MaxStartsPeriod', 'PriceFile', 'Price', 'MaxNofProductionHours', 'MaxNofStarts', 'ProductionReserve', 'ConsumptionReserve', 'IncludeInReserve', 'Scheduler', 'ScenarioWaterManager'});")
		#adding
		octave.eval("Top=Data.Asset("+str(pos+1)+").Topology; nTurbines=Top.nTurbines+1; Data.Asset("+str(pos+1)+").Topology.nTurbines=nTurbines;")
		octave.eval("Data.Asset("+str(pos+1)+").Topology.Engine(nTurbines+1 : nTurbines+Top.nPumps)=Data.Asset("+str(pos+1)+").Topology.Engine(Top.nTurbines+1 : Top.nTurbines+Top.nPumps);")
		octave.eval("Data.Asset("+str(pos+1)+").Engine(nTurbines+1 : nTurbines+Top.nPumps)=Data.Asset("+str(pos+1)+").Engine(Top.nTurbines+1 : Top.nTurbines+Top.nPumps);")
		octave.eval("Data.Asset("+str(pos+1)+").Topology.Engine(nTurbines).Btn=[0.2+0.02*nTurbines 0.6+0.02*nTurbines]; Data.Asset("+str(pos+1)+").Topology.Engine(nTurbines).OperatesFrom = 0;")
		octave.eval("Engine=[]; Engine.ID=datenum(clock); Engine.Name=''; Engine.Shortname='"+names_t[i]+"'; Engine.Type = 1; Engine.MaxFlowFile=''; Engine.MaxFlow.Val=[]; Engine.MaxFlow.Start=0;")
		octave.eval("Engine.MaxFlow.End=0; Engine.MinRunningFlowFile='0'; Engine.MinRunFlow.Val=[]; Engine.MinRunFlow.Start=0; Engine.MinRunFlow.End=0; Engine.MinFlowFile='0';")
		octave.eval("Engine.MinFlow.Val=[]; Engine.MinFlow.Start=0; Engine.MinFlow.End=0; Engine.StartupFile='1'; Engine.ShutdownFile='1'; Engine.EngineCharacteristicFile='';")
		octave.eval("Engine.Characteristic.X=[]; Engine.Characteristic.Y=[]; Engine.EnginePowerCharacteristicFile='%Constant'; Engine.PowerCharacteristic.X=[]; Engine.PowerCharacteristic.Y = [];")
		octave.eval("Engine.PowerCharacteristicIsAbsolute=false; Engine.bUseReservoirAbove=true; Engine.OperatingCosts=0; Engine.StartupCosts=0; Engine.ShutdownCosts=0; Engine.MaxNofOperatingHours = Inf;")
		octave.eval("Engine.MinNofOperatingHours=1; Engine.MinNofIdleHours=1; Engine.MinProductionHoursValue=[]; Engine.MaxProductionHoursValue=[]; Engine.MaxProductionHoursPeriod='Day';")
		octave.eval("Engine.MinStartsValue=[]; Engine.MaxStartsValue=[]; Engine.MaxStartsPeriod='Day'; Eng.AlphaPower=[]; Eng.AlphaPrime=[]; Eng.LastFlow=[]; Eng.MaxPower=[]; Eng.MinPower = [];")
		octave.eval("Eng.MinRunningPower=[]; Eng.MaxPowerPrime=[]; Eng.MaxFlow=[]; Eng.MinRunningFlow=[]; Eng.MinFlow=[]; Eng.MaxPossibleFlow=[]; Eng.MinPossibleRunningFlow=[]; Eng.MinPossibleFlow=[];")
		octave.eval("Eng.MaxFlowPrime=[]; Eng.RM3Lin=[]; Engine.PriceFile=''; Engine.Price.Val=[]; Engine.Price.Start=0; Engine.Price.End=0; Engine.MaxNofProductionHours=[]; Engine.MaxNofStarts=[];")
		octave.eval("Engine.ProductionReserve=0; Engine.ConsumptionReserve=0; Engine.IncludeInReserve=0; Engine.Scheduler.Result=[]; Engine.ScenarioWaterManager.Result=[];")
		octave.eval("Data.Asset("+str(pos+1)+").Topology.Engine(nTurbines).OperatesTo=0; Data.Asset("+str(pos+1)+").Engine(nTurbines)=Engine;")
		octave.eval("if ~isempty(Data.Asset("+str(pos+1)+").EngineAlternatives) Old=Data.Asset("+str(pos+1)+").EngineAlternatives; New=zeros(nTurbines+Top.nPumps); New(1:Top.nTurbines,1:Top.nTurbines)=Old(1:Top.nTurbines,1:Top.nTurbines); New(1:Top.nTurbines,nTurbines+1:end)=Old(1:Top.nTurbines,Top.nTurbines+1:end); New(nTurbines+1:end,1:Top.nTurbines)=Old(Top.nTurbines+1:end,1:Top.nTurbines); New(nTurbines+1:end,nTurbines+1:end)=Old(Top.nTurbines+1:end,Top.nTurbines+1:end); Data.Asset("+str(pos+1)+").EngineAlternatives = New; end;")
		octave.eval("Data.Asset("+str(pos+1)+").Engine(nTurbines).IncludeInReserve=zeros(1,length(Data.Asset("+str(pos+1)+").Reserve));")
	globalDict.set('hydroptModel', octave.pull('Data'))
	#Pumps
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
		engines = CSafeList([assets.get(pos).Engine])
	else:
		engines = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
	for i in range(len(names_p)):
		was = False
		for j in range(int(assets.get(pos).Topology.nTurbines), engines.len()):
			if engines.get(j).Shortname == names_p[i]:
				was = True
				break
		if was == True:
			continue
		#fix reading problems
		if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps > 1:
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MaxFlow')==0 Mx=[]; Mx.Val=[]; Mx.Start=0; Mx.End=0; [Data.Asset("+str(pos+1)+").Engine(:).MaxFlow]=deal(Mx); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MinRunFlow')==0 Mn=[]; Mn.Val=[]; Mn.Start=0; Mn.End=0; [Data.Asset("+str(pos+1)+").Engine(:).MinRunFlow]=deal(Mn); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MinFlow')==0 Mn=[]; Mn.Val=[]; Mn.Start=0; Mn.End=0; [Data.Asset("+str(pos+1)+").Engine(:).MinFlow]=deal(Mn); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'Characteristic')==0 Ch=[]; Ch.X=[]; Ch.Y=0; [Data.Asset("+str(pos+1)+").Engine(:).Characteristic]=deal(Ch); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PowerCharacteristic')==0 PCh=[]; PCh.X=[]; PCh.Y=0; [Data.Asset("+str(pos+1)+").Engine(:).PowerCharacteristic]=deal(PCh); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PowerCharacteristicIsAbsolute')==0 [Data.Asset("+str(pos+1)+").Engine(:).PowerCharacteristicIsAbsolute]=deal(0); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'bUseReservoirAbove')==0 [Data.Asset("+str(pos+1)+").Engine(:).bUseReservoirAbove]=deal(true); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PriceFile')==0 [Data.Asset("+str(pos+1)+").Engine(:).PriceFile]=deal([]); end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'Price')==0 Pr=[]; Pr.Val=[]; Pr.Start=0; Pr.End=0; [Data.Asset("+str(pos+1)+").Engine(:).Price]=deal(Pr); end;")
			octave.eval("Data.Asset("+str(pos+1)+").Engine=orderfields(Data.Asset("+str(pos+1)+").Engine, {'ID', 'Name', 'Shortname', 'Type', 'MaxFlowFile', 'MaxFlow', 'MinRunningFlowFile', 'MinRunFlow', 'MinFlowFile', 'MinFlow', 'StartupFile', 'ShutdownFile', 'EngineCharacteristicFile', 'Characteristic', 'EnginePowerCharacteristicFile', 'PowerCharacteristic', 'PowerCharacteristicIsAbsolute', 'bUseReservoirAbove', 'OperatingCosts', 'StartupCosts', 'ShutdownCosts', 'MaxNofOperatingHours', 'MinNofOperatingHours', 'MinNofIdleHours', 'MinProductionHoursValue', 'MaxProductionHoursValue', 'MaxProductionHoursPeriod', 'MinStartsValue', 'MaxStartsValue', 'MaxStartsPeriod', 'PriceFile', 'Price', 'MaxNofProductionHours', 'MaxNofStarts', 'ProductionReserve', 'ConsumptionReserve', 'IncludeInReserve', 'Scheduler', 'ScenarioWaterManager'});")
		else:
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MaxFlow')==0 Mx=[]; Mx.Val=[]; Mx.Start=0; Mx.End=0; [Data.Asset("+str(pos+1)+").Engine(1).MaxFlow]=Mx; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MinRunFlow')==0 Mn=[]; Mn.Val=[]; Mn.Start=0; Mn.End=0; [Data.Asset("+str(pos+1)+").Engine(1).MinRunFlow]=Mn; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'MinFlow')==0 Mn=[]; Mn.Val=[]; Mn.Start=0; Mn.End=0; [Data.Asset("+str(pos+1)+").Engine(1).MinFlow]=Mn; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'Characteristic')==0 Ch=[]; Ch.X=[]; Ch.Y=0; [Data.Asset("+str(pos+1)+").Engine(1).Characteristic]=Ch; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PowerCharacteristic')==0 PCh=[]; PCh.X=[]; PCh.Y=0; [Data.Asset("+str(pos+1)+").Engine(1).PowerCharacteristic]=PCh; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PowerCharacteristicIsAbsolute')==0 [Data.Asset("+str(pos+1)+").Engine(1).PowerCharacteristicIsAbsolute]=0; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'bUseReservoirAbove')==0 [Data.Asset("+str(pos+1)+").Engine(1).bUseReservoirAbove]=true; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'PriceFile')==0 [Data.Asset("+str(pos+1)+").Engine(1).PriceFile]=[]; end;")
			octave.eval("if isfield(Data.Asset("+str(pos+1)+").Engine(1), 'Price')==0 Pr=[]; Pr.Val=[]; Pr.Start=0; Pr.End=0; [Data.Asset("+str(pos+1)+").Engine(1).Price]=Pr; end;")
			octave.eval("Data.Asset("+str(pos+1)+").Engine=orderfields(Data.Asset("+str(pos+1)+").Engine, {'ID', 'Name', 'Shortname', 'Type', 'MaxFlowFile', 'MaxFlow', 'MinRunningFlowFile', 'MinRunFlow', 'MinFlowFile', 'MinFlow', 'StartupFile', 'ShutdownFile', 'EngineCharacteristicFile', 'Characteristic', 'EnginePowerCharacteristicFile', 'PowerCharacteristic', 'PowerCharacteristicIsAbsolute', 'bUseReservoirAbove', 'OperatingCosts', 'StartupCosts', 'ShutdownCosts', 'MaxNofOperatingHours', 'MinNofOperatingHours', 'MinNofIdleHours', 'MinProductionHoursValue', 'MaxProductionHoursValue', 'MaxProductionHoursPeriod', 'MinStartsValue', 'MaxStartsValue', 'MaxStartsPeriod', 'PriceFile', 'Price', 'MaxNofProductionHours', 'MaxNofStarts', 'ProductionReserve', 'ConsumptionReserve', 'IncludeInReserve', 'Scheduler', 'ScenarioWaterManager'});")
		#adding
		octave.eval("Top=Data.Asset("+str(pos+1)+").Topology; nPumps=Top.nPumps+1; Data.Asset("+str(pos+1)+").Topology.nPumps=nPumps; Data.Asset("+str(pos+1)+").Topology.Engine(Top.nTurbines+nPumps).Btn=[0.2+0.02*nPumps 0.4+0.02*nPumps];")
		octave.eval("Data.Asset("+str(pos+1)+").Topology.Engine(Top.nTurbines+nPumps).OperatesFrom=0; Data.Asset("+str(pos+1)+").Topology.Engine(Top.nTurbines+nPumps).OperatesTo=0;")
		octave.eval("Engine=[]; Engine.ID=datenum(clock); Engine.Name=''; Engine.Shortname='"+names_p[i]+"'; Engine.Type = 1; Engine.MaxFlowFile=''; Engine.MaxFlow.Val=[]; Engine.MaxFlow.Start=0;")
		octave.eval("Engine.MaxFlow.End=0; Engine.MinRunningFlowFile='0'; Engine.MinRunFlow.Val=[]; Engine.MinRunFlow.Start=0; Engine.MinRunFlow.End=0; Engine.MinFlowFile='0';")
		octave.eval("Engine.MinFlow.Val=[]; Engine.MinFlow.Start=0; Engine.MinFlow.End=0; Engine.StartupFile='1'; Engine.ShutdownFile='1'; Engine.EngineCharacteristicFile='';")
		octave.eval("Engine.Characteristic.X=[]; Engine.Characteristic.Y=[]; Engine.EnginePowerCharacteristicFile='%Constant'; Engine.PowerCharacteristic.X=[]; Engine.PowerCharacteristic.Y = [];")
		octave.eval("Engine.PowerCharacteristicIsAbsolute=false; Engine.bUseReservoirAbove=true; Engine.OperatingCosts=0; Engine.StartupCosts=0; Engine.ShutdownCosts=0; Engine.MaxNofOperatingHours = Inf;")
		octave.eval("Engine.MinNofOperatingHours=1; Engine.MinNofIdleHours=1; Engine.MinProductionHoursValue=[]; Engine.MaxProductionHoursValue=[]; Engine.MaxProductionHoursPeriod='Day';")
		octave.eval("Engine.MinStartsValue=[]; Engine.MaxStartsValue=[]; Engine.MaxStartsPeriod='Day'; Eng.AlphaPower=[]; Eng.AlphaPrime=[]; Eng.LastFlow=[]; Eng.MaxPower=[]; Eng.MinPower = [];")
		octave.eval("Eng.MinRunningPower=[]; Eng.MaxPowerPrime=[]; Eng.MaxFlow=[]; Eng.MinRunningFlow=[]; Eng.MinFlow=[]; Eng.MaxPossibleFlow=[]; Eng.MinPossibleRunningFlow=[]; Eng.MinPossibleFlow=[];")
		octave.eval("Eng.MaxFlowPrime=[]; Eng.RM3Lin=[]; Engine.PriceFile=''; Engine.Price.Val=[]; Engine.Price.Start=0; Engine.Price.End=0; Engine.MaxNofProductionHours=[]; Engine.MaxNofStarts=[];")
		octave.eval("Engine.ProductionReserve=0; Engine.ConsumptionReserve=0; Engine.IncludeInReserve=0; Engine.Scheduler.Result=[]; Engine.ScenarioWaterManager.Result=[];")
		octave.eval("Data.Asset("+str(pos+1)+").Engine(Top.nTurbines+nPumps)=Engine; ")
		octave.eval("if ~isempty(Data.Asset("+str(pos+1)+").EngineAlternatives) Old=Data.Asset("+str(pos+1)+").EngineAlternatives; New=zeros(Top.nTurbines+nPumps); New(1:Top.nTurbines+Top.nPumps,1:Top.nTurbines+Top.nPumps)=Old; Data.Asset("+str(pos+1)+").EngineAlternatives=New; end;")
		octave.eval("Data.Asset("+str(pos+1)+").Engine(Top.nTurbines+nPumps).IncludeInReserve=zeros(1,length(Data.Asset("+str(pos+1)+").Reserve));")
	globalDict.set('hydroptModel', octave.pull('Data'))
	#Connections and Coordinates
	resPos = {}
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	if assets.get(pos).Topology.nRes == 1:
		reservoirs = CSafeList([assets.get(pos).Reservoir])
	else:
		reservoirs = CSafeList(CSafeList(assets.get(pos).Reservoir).get(0))
	if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
		engines = CSafeList([assets.get(pos).Engine])
	else:
		engines = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
	for i in range(reservoirs.len()):
		resPos[reservoirs.get(i).Shortname] = i + 1
	if assets.get(pos).Topology.nFlows == 0:
		flows = CSafeList([])
	elif assets.get(pos).Topology.nFlows == 1:
		flows = CSafeList([assets.get(pos).Flow])
	else:
		flows = CSafeList(CSafeList(assets.get(pos).Flow).get(0))
	for i in range(len(names)):
		#Reservoirs
		if types[i] == 'reservoir':
			if operatesTo[i] != 'null':
				octave.eval("Data.Asset("+str(pos+1)+").Topology.Reservoir("+str(resPos[names[i]])+").SpillsToRes="+str(resPos[operatesTo[i]])+";")
			octave.eval("Data.Asset("+str(pos+1)+").Topology.Reservoir("+str(resPos[names[i]])+").Btn=["+str(x[i])+" "+str(y[i])+"];")
		#Turbines and Pumps
		for j in range(engines.len()):
			if engines.get(j).Shortname == names[i]:
				if operatesFrom[i] != 'null':
					octave.eval("Data.Asset("+str(pos+1)+").Topology.Engine("+str(j+1)+").OperatesFrom="+str(resPos[operatesFrom[i]])+";")
				if operatesTo[i] != 'null':
					octave.eval("Data.Asset("+str(pos+1)+").Topology.Engine("+str(j+1)+").OperatesTo="+str(resPos[operatesTo[i]])+";")
				octave.eval("Data.Asset("+str(pos+1)+").Topology.Engine("+str(j+1)+").Btn=["+str(x[i])+" "+str(y[i])+"];")
		#Flows
		for j in range(flows.len()):
			if flows.get(j).Shortname == names[i]:
				if operatesFrom[i] != 'null':
					octave.eval("Data.Asset("+str(pos+1)+").Topology.Flow("+str(j+1)+").OperatesFrom="+str(resPos[operatesFrom[i]])+";")
				if operatesTo[i] != 'null':
					octave.eval("Data.Asset("+str(pos+1)+").Topology.Flow("+str(j+1)+").OperatesTo="+str(resPos[operatesTo[i]])+";")
				octave.eval("Data.Asset("+str(pos+1)+").Topology.Flow("+str(j+1)+").Btn=["+str(x[i])+" "+str(y[i])+"];")
	globalDict.set('hydroptModel', octave.pull('Data'))
	return names[0]

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
	'date': date, 'timedelta': timedelta, 'datetime': datetime, 'log': CSafeLog(None), 'globalDict': globalDict, 'CSafeNP': CSafeNP(), 'dateUtils': CSafeDateUtils(), 'math': math,
	'decodeFile': base64.b64decode, 'split': safeSplit, 'pd': pd, 'io': io, 'CSafeFigure': CSafeFigure, 'CSafeDict': CSafeDict, 'CSafePoint': CSafePoint, 'CSafeMatlab': CSafeMatlab(),
	'CSafeStr': CSafeStr, 'scipy': scipy, 'CSafeDF': CSafeDF, 'urllib': urllib, 'octave': octave,
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
		'getNameFromId' : getNameFromId, 'CSafeList': CSafeList, 'globalDict': globalDict, 'CSafeNP': CSafeNP(), 'dateUtils': CSafeDateUtils(), 'CSafeMatlab': CSafeMatlab(),
		'math': math, 'CSafeStr': CSafeStr, 'scipy': scipy, 'CSafeDF': CSafeDF, 'urllib': urllib, 'octave': octave,
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
	stateLst = []
	if 'state' in interaction:
		for state in interaction['state']:
			stateId = generateId(state['object'], state['type'], interaction['screen'])
			stateLst.append(State(stateId, state['param']))
	outputId = generateId(interaction['output']['object'], interaction['output']['type'], interaction['screen'])
	print(interaction['screen'], interaction['callback'])
	dash_app.callback(
		Output(outputId, interaction['output']['param']),
		inputLst,
		stateLst,
	)(callbackFunctions[interaction['screen']][interaction['callback']] if interaction['callback'] in callbackFunctions[interaction['screen']] else globalCallbacks[interaction['callback']])