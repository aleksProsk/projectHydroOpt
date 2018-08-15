from pandas import DataFrame, DatetimeIndex
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import copy

import plotly.graph_objs as go

from baseObjects import User
CUser = User.CUser

dictionaryOfAllScreenVariables = {}

def generateId(name, type, screen):
	print(name, type, screen)
	return name + '-' + type + '-' + screen

class CRestricted(object):
	__id = 0
	def getID(self): return str(self.__localID) #str(CRestricted.__id)
	def getNumberOfInstances(): return str(CRestricted.__id)
	getNumberOfInstances = staticmethod(getNumberOfInstances)
	def __init__(self, user, name = None, screenName = None):
		self.__user = user
		CRestricted.__id += 1
		if name is None and screenName is None:
			self.__localID = CRestricted.__id
		else:
			self.__localID = generateId(name, self.__class__.__name__, screenName)
			cur_uid = str(self.getUser().getUID())
			if cur_uid not in dictionaryOfAllScreenVariables:
				dictionaryOfAllScreenVariables[cur_uid] = {}
			if screenName not in dictionaryOfAllScreenVariables[cur_uid]:
				dictionaryOfAllScreenVariables[cur_uid][screenName] = CSafeDict({})
			dictionaryOfAllScreenVariables[cur_uid][screenName].set(name, self)
			print('Added ', name, ' to dict with uid = ', cur_uid, ' screen = ', screenName)
		print('name: ', name)
		print('screenName: ', screenName)
		print('classname: ', self.__class__.__name__)
		print('id: ', self.__localID)
	def getUser(self): return self.__user

class CSafeDict(CRestricted):
    def __init__(self, dict, user=CUser()):
        super().__init__(user)
        self.__d = dict
    def get(self, s): return self.__d[s]
    def getDict(self): return self.__d
    def set(self, key, value): self.__d[key] = value

class CSafeNP(CRestricted):
	def __init__(self, user=CUser()): super().__init__(user)
	def min(self, v): return np.min(v)
	def max(self, v): return np.max(v)
	def hstack(self, v): return np.hstack(v)
	def vstack(self, v): return np.vstack(v)
	def arange(self, stop, start=0, step=1, dtype=None): return np.arange(start=start, stop=stop, step=step, dtype=dtype)
	def size(self, v): return v.size
	def array(self, v): return np.array(v)
	def reshape(self, v, x, y): return v.reshape(x, y)
	def transpose(self, v): return np.transpose(v)


class CSafeFigure(CRestricted):
	def __init__(self, user=CUser(), figure={}):
		super().__init__(user)
		self.__figure = copy.deepcopy(figure)
	def restrict(self, value):
		data = self.__figure['data'][0]
		nx = []
		ny = []
		for i in range(len(data['x'])):
			if data['y'][i] >= value[0] and data['y'][i] <= value[1]:
				nx.append(data['x'][i])
				ny.append(data['y'][i])
		self.__figure['data'][0]['x'] = nx
		self.__figure['data'][0]['y'] = ny
	def getFigure(self):
		return self.__figure
	def getZoom(self):
		if 'layout' in self.__figure and 'mapbox' in self.__figure['layout'] and 'zoom' in self.__figure['layout']['mapbox']:
			return self.__figure['layout']['mapbox']['zoom']
		return None
	def addPoint(self, x, y, num):
		try:
			x = int(x)
			y = int(y)
			self.__figure['data'][num]['x'] = np.append(self.__figure['data'][num]['x'], x)
			self.__figure['data'][num]['y'] = np.append(self.__figure['data'][num]['y'], y)
		except Exception as e:
			print('PLEASE ADD ONLY NUMBERS!!!')
	def setLineType(self, type = 'linear', num = 0, smoothing = 0.65, deg = 2):
		print(self.__figure)
		if type == 'polyfit':
			z = np.polyfit(self.__figure['data'][num]['x'], self.__figure['data'][num]['y'], deg)
			f = np.poly1d(z)
			x_new = np.linspace(np.min(self.__figure['data'][num]['x']), np.max(self.__figure['data'][num]['x']), 50)
			y_new = f(x_new)
			self.__figure['data'].append(go.Scatter(
				x=x_new,
				y=y_new,
				mode='lines',
			))
			self.__figure['data'][num]['mode'] = 'markers'
		else:
			self.__figure['data'][num]['line'] = dict(
				shape=type,
				smoothing=smoothing,
			)

class CSafePoint(CRestricted):
	def __init__(self, clickData, user=CUser()):
		super().__init__(user)
		self.__point = CSafeDict(clickData['points'][0])
	def getDict(self): return self.__point.getDict()
	def getPoint(self): return self.__point


class CSafeDateUtils(CRestricted):
	def __init__(self, user=CUser()): super().__init__(user)
	def to_datetime(self, v): return pd.to_datetime(v)
	def to_str(self, d): return d.strftime("%Y-%m-%d %H:%M")
	def from_matlab(self, v): return date.fromordinal(int(v)) + timedelta(days=v % 1) - timedelta(days=366)  # date.fromordinal(int(v-366))
	def date_range(self, start, end, freq='D', tz=None): return pd.date_range(start=start, end=end, freq=freq, tz=tz)
	def date_range_from_matlab(self, start, end, freq='H', tz=None): return self.date_range(start=self.from_matlab(start), end=self.from_matlab(end), freq=freq, tz=tz)
	def months_from_matlab(self, start, end): return self.date_range_from_matlab(start=start, end=end, freq='MS')

class CSafeDF(CRestricted):
	def __init__(self, user=CUser()): super().__init__(user)
	def define(self, matrix, columns): self.__df = DataFrame(matrix, columns=columns)
	def to_dict(self, param): return self.__df.to_dict(param)
	def columns(self): return self.__df.columns


class CSafeLog(CRestricted):
	def __init__(self, user): super().__init__(user)
	def print(self, s): print(s)

class CGUIComponent(CRestricted):
	def __init__(self, name, screenName):
		super().__init__(CUser(), name, screenName)
		self.__children = []
	def getChildren(self): return self.__children
	def appendChild(self, c): self.__children.append(c)

def safeSplit(separator, string, num):
	return string.split(separator)[num]

class CSafeMenu(CRestricted):
	def __init__(self, user = CUser(), menu = {}):
		super().__init__(user)
		self.__menu = menu
	def addSubmenu(self, submenu):
		self.__menu[submenu] = []
	def addItem(self, submenu, item):
		self.__menu[submenu].append(item)
	def getNestedList(self):
		nestedList = []
		for elem in self.__menu:
			nestedList.append([])
			nestedList[-1].append(elem)
			nestedList[-1].append(self.__menu[elem])
		return nestedList

class CSafeList(CRestricted):
	def __init__(self, user = CUser(), lst = []):
		super().__init__(user)
		self.__lst = list(lst)
	def set(self, position, value):
		self.__lst[position] = value
	def get(self, position):
		return self.__lst[position]
	def append(self, value):
		self.__lst.append(value)
	def getList(self):
		return self.__lst
	def len(self):
		return len(self.__lst)