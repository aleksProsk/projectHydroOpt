import numpy as np
import copy

import dash_html_components as html
import dash_core_components as dcc

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

class CPieChart(CDashComponent):
    def __init__(self, labels = [], values = [], title = 'Pie Chart', hoverinfo = 'label+percent', hole = 0, showlegend = False, style={},
                 name = None, screenName = None):
        super().__init__(name, screenName)
        self.setPieChart(labels, values, title, hoverinfo, hole, showlegend, style)
    def __setParams(self, labels, values, title, hoverinfo, hole, showlegend, style):
        self.__labels = labels
        self.__values = values
    def __setData(self, labels, values, hoverinfo, hole):
        self.__data = [{'values': values, 'labels': labels, 'hoverinfo': hoverinfo, 'hole': hole, 'type': 'pie'}]
    def __setLayout(self, title, showlegend):
        self.__layout = copy.deepcopy(BASIC_GRAPH_LAYOUT)
        self.__layout['title'] = title
        self.__layout['showlegend'] = showlegend
    def __setFigure(self):
        self.__figure = {'data': self.__data, 'layout': self.__layout}
    def update(self, value):
        return
        #self.__figure = value
    def getValue(self): return self.__figure
    def setPieChart(self, labels, values, title, hoverinfo, hole, showlegend, style):
        self.__setParams(labels, values, title, hoverinfo, hole, showlegend, style)
        self.__setData(labels, values, hoverinfo, hole)
        self.__setLayout(title, showlegend)
        self.__setFigure()
        chart = dcc.Graph(id=super().getID(), figure=self.__figure)
        super().setDashRendering(html.Div(chart, style=style))
        print(self.__figure)
