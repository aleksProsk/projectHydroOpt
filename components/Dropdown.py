import dash_core_components as dcc
import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CDropdown(CDashComponent):
	def __init__(self, options = [], placeholder = 'Select', value = '', multi = False, clearable = True, style = {},
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setDropdown(options, placeholder, value, multi, clearable, style)
	def getValue(self):
		return self.__value
	def update(self, value):
		self.__value = value
	def setDropdown(self, options, placeholder, value, multi, clearable, style):
		self.__options = options
		self.__value = value
		super().setDashRendering(html.Div([dcc.Dropdown(
			id=str(super().getID()),
			options=options,
			placeholder=placeholder,
			multi=multi,
			value=value,
			clearable=clearable,
		)], style=style))