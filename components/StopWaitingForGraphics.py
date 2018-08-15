import dash_html_components as html

from components import DashComponent

CDashComponent = DashComponent.CDashComponent

class CStopWaitingForGraphics(CDashComponent):
	def __init__(self, name = None, screenName = None):
		super().__init__(name, screenName)
		super().setDashRendering(html.P("", className = 'CStopWaitingForGraphics'))