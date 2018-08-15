import dash_core_components as dcc

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CTabs(CDashComponent):
	def __init__(self, tabs = [], value = None, vertical = False, style = {},
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setTabs(tabs, value, vertical, style)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setTabs(self, tabs, value, vertical, style):
		self.__tabs = tabs
		self.__value = value
		super().setDashRendering(dcc.Tabs(
			id=str(super().getID()),
			tabs=tabs,
			value=value,
			vertical=vertical,
			style=style,
		))