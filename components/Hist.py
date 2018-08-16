import dash_html_components as html
import dash_core_components as dcc

import copy

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

class CHist(CDashComponent):
    def __init__(self, x=[], names=[], title='', showlegend=True, hoverinfo='x+y', xAxis='', yAxis='', style={},
                 name = None, screenName = None):
        super().__init__(name, screenName)
        self.setHist(x, title, showlegend, hoverinfo, xAxis, yAxis, style)
    def __setData(self, x, hoverinfo):
        self.__data = []
        self.__data.append({})
        self.__data[0]['x'] = x
        self.__data[0]['type'] = 'histogram'
        self.__data[0]['hoverinfo'] = hoverinfo
        self.__data[0]['hoverlabel'] = dict()
        self.__data[0]['hoverlabel']['namelength'] = -1
    def __setLayout(self, x, title, showlegend, xAxis, yAxis, style):
        height = 'auto'
        if 'height' in style:
            height = style['height']
        width = 'auto'
        if 'width' in style:
            width = style['width']
        self.__layout = copy.deepcopy(BASIC_GRAPH_LAYOUT)
        self.__layout['title'] = title
        self.__layout['height'] = height
        self.__layout['width'] = width
        self.__layout['showlegend'] = showlegend
        tRange = []
        if len(x) > 0:
            tRange = [x[0] - 5, x[0] + 5]
        self.__layout['xaxis'] = dict(
            title=xAxis,
            range=tRange,
        )
        self.__layout['yaxis'] = dict(
            title=yAxis,
        )
    def __setFigure(self):
        self.__figure = {'data': self.__data, 'layout': self.__layout}
    def update(self, value):
        return
    def getValue(self): return self.__figure
    def setHist(self, x, title, showlegend, hoverinfo, xAxis, yAxis, style):
        self.__setData(x, hoverinfo)
        self.__setLayout(x, title, showlegend, xAxis, yAxis, style)
        self.__setFigure()
        chart = dcc.Graph(id=super().getID(), figure=self.__figure)
        super().setDashRendering(html.Div(chart, style=style))