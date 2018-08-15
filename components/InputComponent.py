import dash_core_components as dcc

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CInput(CDashComponent):
	def __init__(self, min = None, max = None, maxlength = -1, placeholder = 'Input field',
				 readonly = False, style = {}, type = 'text', value = None,
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setInput(min, max, maxlength, placeholder, readonly, style, type, value)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setInput(self, min, max, maxlength, placeholder, readonly, style, type, value):
		self.__min = min
		self.__max = max
		self.__type = type
		self.__value = value
		super().setDashRendering(dcc.Input(
			id=str(super().getID()),
			name=str(super().getID()),
			min=min,
			max=max,
			maxlength=maxlength,
			placeholder=placeholder,
			readonly=readonly,
			style=style,
			type=type,
			value=value,
		))