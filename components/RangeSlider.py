import dash_core_components as dcc
import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CRangeSlider(CDashComponent):
	def __init__(self, allowCross = False, dots = False, marks = {}, min = 0, max = 100, step = 1, value = None, pushable = False, vertical = False, style = {},
				 name = None, screenName = None):
		if value is None:
			value = max
		super().__init__(name, screenName)
		self.setRangeSlider(allowCross, dots, marks, min, max, step, value, pushable, vertical, style)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def getMinMaxRange(self):
		return [self.__min, self.__max]
	def setRangeSlider(self, allowCross, dots, marks, min, max, step, value, pushable, vertical, style):
		self.__min = min
		self.__max = max
		self.__value = value
		super().setDashRendering(html.Div([dcc.RangeSlider(
			id=str(super().getID()),
			allowCross=allowCross,
			dots=dots,
			marks=marks,
			min=min,
			max=max,
			step=step,
			value=value,
			pushable=pushable,
			vertical=vertical,
		)], style=style))