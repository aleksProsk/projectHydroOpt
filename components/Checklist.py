import dash_core_components as dcc

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CChecklist(CDashComponent):
	def __init__(self, inputStyle = {}, labelStyle = {}, options = [], style = {}, value = [],
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setChecklist(inputStyle, labelStyle, options, style, value)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setChecklist(self, inputStyle, labelStyle, options, style, value):
		self.__options = options
		self.__value = value
		super().setDashRendering(dcc.Checklist(
			id=str(super().getID()),
			inputStyle=inputStyle,
			labelStyle=labelStyle,
			options=options,
			style=style,
			values=value,
		))