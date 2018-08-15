import dash_core_components as dcc
import plotly.graph_objs as go
map_box_token = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'
import numpy as np

from components import Map

CMap = Map.CMap

def getCenter(lat, lon):
	lat = np.hstack(lat)
	lon = np.hstack(lon)
	return {
		'lat': (np.max(lat) + np.min(lat)) / 2.0,
		'lon': (np.max(lon) + np.min(lon)) / 2.0,
	}

def getZoom(lat, lon):
	lat = np.hstack(lat)
	lon = np.hstack(lon)
	mlat = (np.max(lat) + np.min(lat)) / 2.0
	mlon = (np.max(lon) + np.min(lon)) / 2.0
	return 8 - (mlat - 46.2035375)

def buildGraph(lat, lon, edges):
	data = []
	for edge in edges:
		data.append(
			go.Scattermapbox(
				lat=[lat[edge[0]], lat[edge[1]]],
				lon=[lon[edge[0]], lon[edge[1]]],
				mode='lines',
				visible=True,
				line=dict(
					color='black',
					width=2,
				)
			)
		)
	return data

class CTopologyMap(CMap):
	def __init__(self, mode = 'light', center = {'lat': '46.864081', 'lon': '8.2187543'}, zoom = 6, showlegend = False, title = 'Map', style = {},
				 lat = [], lon = [], text = [], names = [], customdata = [], dataMode = [], hoverinfo = [], textposition = [], color=[], edges = [],
				 name = None, screenName = None):
		super().__init__(mode, center, zoom, showlegend, title, style, name, screenName)
		if (len(lat) > 0):
			center = getCenter(lat, lon)
			zoom = getZoom(lat, lon)
		self.__lat = lat
		self.__lon = lon
		self.__color = color
		self.__selected_points = set()
		self.__layout = self.setLayout(mode, center, zoom, showlegend, title)
		self.__clickData = None
		self.setData(lat, lon, text, names, customdata, dataMode, hoverinfo, textposition, color, edges)
		self.setTopologyMap(style)
	def setData(self, lat, lon, text, names, customdata, dataMode, hoverinfo, textposition, color, edges):
		self.__edges = edges
		self.__data = buildGraph(lat, lon, edges)
		for i in range(len(lat)):
			self.__data.append(go.Scattermapbox(
				lat=[lat[i]],
				lon=[lon[i]],
				mode=dataMode[i],
				marker=dict(
					size=16,
					color=color[i]
				),
				name=names[i],
				text=text[i],
				textposition=textposition[i],
				hoverinfo=hoverinfo[i],
				customdata=[customdata[i]],
				textfont=dict(
					color='black',
					size=14,
				),
				visible=True,
			))
	def getEdges(self):
		return self.__edges
	def update(self, value):
		self.__clickData = value
	def getValue(self):
		return self.__clickData
	def setTopologyMap(self, style):
		self.setDashRendering(dcc.Graph(id = super().getID(), figure = go.Figure(data = self.__data, layout = self.__layout), style=style))
	def setNewCoordinatesForPoint(self, setIndex, pointIndex, lat, lon):
		self.__lat[setIndex - len(self.__edges)] = float(lat)
		self.__lon[setIndex - len(self.__edges)] = float(lon)
		self.__data[setIndex]['lat'] = [float(lat)]
		self.__data[setIndex]['lon'] = [float(lon)]
		newEdges = buildGraph(self.__lat, self.__lon, self.__edges)
		for i in range(len(newEdges)):
			self.__data[i] = newEdges[i]
		return self.getFigure()
	def getFigure(self):
		return go.Figure(data = self.__data, layout = self.__layout)
	def highlight(self, setIndex, pointIndex):
		print(self.__data)
		if setIndex in self.__selected_points:
			self.__selected_points.remove(setIndex)
			self.__data[setIndex]['marker'] = dict(
				size=16,
				color=self.__color[setIndex - len(self.__edges)]
			)
			self.__data[setIndex]['textfont'] = dict(
				color='black',
				size=14,
			)
		else:
			self.__selected_points.add(setIndex)
			self.__data[setIndex]['marker'] = dict(
				size=20,
				color=self.__color[setIndex - len(self.__edges)],
			)
			self.__data[setIndex]['textfont'] = dict(
				color='white',
				size=16,
			)
		return self.getFigure()