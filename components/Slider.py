import dash_core_components as dcc
import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CSlider(CDashComponent):
	def __init__(self, dots = False, marks = {}, min = 0, max = 100, step = 1, value = None, vertical = False, style = {},
				 name = None, screenName = None):
		if value is None:
			value = max
		super().__init__(name, screenName)
		self.setSlider(dots, marks, min, max, step, value, vertical, style)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setSlider(self, dots, marks, min, max, step, value, vertical, style):
		self.__min = min
		self.__max = max
		self.__value = value
		super().setDashRendering(html.Div([dcc.Slider(
			id=str(super().getID()),
			dots=dots,
			marks=marks,
			min=min,
			max=max,
			step=step,
			value=value,
			vertical=vertical,
		)], style=style))