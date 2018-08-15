from pandas import DataFrame, DatetimeIndex
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import infix
import copy

import dash_html_components as html
import dash_core_components as dcc

@infix.div_infix
def m(f,x): return list(map(f,x))

def transpose(v): return list(map(list, zip(*v)))

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

BASIC_GRAPH_LAYOUT = dict(
	autosize=True,
	height=500,
	margin=dict(l=35, r=35, b=35, t=45),
	hovermode="closest",
	plot_bgcolor="#F9FAFA",
	paper_bgcolor="#F2F2F2",
	legend=dict(font=dict(size=10), orientation='h'),
	title='Satellite Overview'
)

class CChart(CDashComponent):
	def __init__(self, rows=[], headers=[], rowCaptions=[], title='', type='bar', barmode='group', style={}, xAxis='', yAxis='', showLegend=True, hoverinfo='x+y',
                 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setChart(rows, headers, rowCaptions, title, type, barmode, style, xAxis, yAxis, showLegend, hoverinfo)
	def getRows(self): return self.__rows
	def getHeaders(self): return self.__headers
	def getRowCaptions(self): return self.__rowCaptions
	def __setParams(self, rows, headers, rowCaptions, title, type='bar', barmode='group'):
		self.__rows = rows
		self.__headers = headers
		self.__isTimeSeries = isinstance(rowCaptions, DatetimeIndex)
		self.__rowCaptions = rowCaptions if self.__isTimeSeries else np.array(rowCaptions).flatten()
		self.__title = title
		self.__type = type
		self.__barmode = barmode
	def __setDataMap(self): self.__dataMap = lambda x: {'x': self.__rowCaptions, 'y': x[0], 'name': x[1], 'type': self.__type}
	def __setDataVec(self): self.__dataVec = (lambda x: [np.array(x[0]).flatten(), x[1]]) /m/ transpose([self.__rows, self.__headers])  #list(map(lambda x: [x[0].flatten(), x[1]], transpose([self.__rows, self.__headers])))
	def __setData(self, hoverinfo):
		self.__data = self.__dataMap /m/ self.__dataVec #list(map(self._dataMap, self._dataVec))
		for i in range(len(self.__data)):
			self.__data[i]['hoverinfo'] = hoverinfo
			self.__data[i]['hoverlabel'] = dict()
			self.__data[i]['hoverlabel']['namelength'] = -1
	def __setLayout(self, style, xAxis, yAxis, showLegend):
		height = 'auto'
		if 'height' in style:
			height = style['height']
		width = 'auto'
		if 'width' in style:
			width = style['width']
		self.__layout = copy.deepcopy(BASIC_GRAPH_LAYOUT)
		self.__layout['title'] = self.__title
		self.__layout['barmode'] = self.__barmode
		self.__layout['height'] = height
		self.__layout['width'] = width
		self.__layout['showlegend'] = showLegend
		if self.__isTimeSeries:
			self.__layout['xaxis'] = dict(rangeselector=dict(
				buttons=list([
					dict(count=1, label='1d', step='day', stepmode='backward'),
					dict(count=7, label='1w', step='day', stepmode='backward'),
					dict(count=1, label='1m', step='month', stepmode='backward'),
					dict(count=6, label='6m', step='month', stepmode='backward'),
					dict(count=12, label='1y', step='month', stepmode='backward'),
					dict(step='all')])),
				rangeslider=dict(), type='date', title=xAxis)
		else:
			self.__layout['xaxis'] = dict(
				title=xAxis,
			)
		self.__layout['yaxis'] = dict(
			title=yAxis,
		)
	def __setFigure(self):
		print(self.__data)
		self.__figure = {'data': self.__data, 'layout': self.__layout}
	def update(self, value):
		return
		#self.__figure = value
	def getValue(self): return self.__figure
	def setChart(self, rows, headers, rowCaptions, title, type, barmode, style, xAxis, yAxis, showLegend, hoverinfo):
		self.__setParams(rows, headers, rowCaptions, title, type, barmode)
		self.__setDataMap()
		self.__setDataVec()
		self.__setData(hoverinfo)
		self.__setLayout(style, xAxis, yAxis, showLegend)
		self.__setFigure()
		chart = dcc.Graph(id=super().getID(), figure=self.__figure)
		super().setDashRendering(html.Div(chart, style=style))