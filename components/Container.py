import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CContainer(CDashComponent):
	def __init__(self, style = {}, name = None, screenName = None):
		super().__init__(name, screenName)
		super().setDashRendering(html.Div([], style = style))