import dash_core_components as dcc
import plotly.graph_objs as go
map_box_token = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CMap(CDashComponent):
	def __init__(self, mode = 'light', center = {'lat': '46.864081', 'lon': '8.2187543'}, zoom = 6, showlegend = False, title = 'Map', style = {},
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setLayout(mode, center, zoom, showlegend, title)
		self.setMap(style)
	def setLayout(self, mode, center, zoom, showlegend, title):
		self.__data = [go.Scattermapbox()]
		self.__layout = go.Layout(
			title = title,
			autosize = True,
			hovermode = 'closest',
			showlegend = showlegend,
			margin = dict(
				l=0,
				r=0,
				b=0,
				t=45,
			),
			mapbox = dict(
				accesstoken=map_box_token,
				bearing=0,
				center=center,
				pitch=0,
				zoom=zoom,
				style=mode,
			),
		)
		return self.__layout
	def update(self, value):
		return
	def setMap(self, style):
		self.setDashRendering(dcc.Graph(id = super().getID(), figure = go.Figure(data = self.__data, layout = self.__layout), style=style))