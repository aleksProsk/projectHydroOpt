import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CModal(CDashComponent):
	def __init__(self, style={}, name = None, screenName = None):
		super().__init__(name, screenName)
		self.setModal(style)
	def setModal(self, style):
		style['display'] = 'none'
		style['position'] = 'fixed'
		style['zIndex'] = 10001
		style['padding-top'] = '10%'
		style['left'] = 0
		style['top'] = 0
		style['width'] = '100%'
		style['height'] = '100%'
		style['overflow'] = 'auto'
		if 'background-color' not in style:
			style['background-color'] = 'rgba(0, 0, 0, 0.4)'
		self.setDashRendering(html.Div([],
			id=str(super().getID()),
			style=style,
		))