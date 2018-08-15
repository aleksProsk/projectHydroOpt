from datetime import date, timedelta, datetime
import dash_core_components as dcc
import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CDatePickerSingle(CDashComponent):
	def __init__(self, minDate=(1995, 8, 5), maxDate = (2017, 9, 19), date = (2017, 8, 5), style = {},
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setDatePickerSingle(minDate, maxDate, date, style)
	def getValue(self):
		return self.__date
	def update(self, date = None):
		if date is not None:
			self.__date = date
	def setDatePickerSingle(self, minDate, maxDate, date, style):
		self.__minDate = datetime(*minDate).date()
		self.__maxDate = datetime(*maxDate).date()
		self.__date = datetime(*date).date()
		super().setDashRendering(html.Div([dcc.DatePickerSingle(
			id=str(super().getID()),
			min_date_allowed=datetime(*minDate),
			max_date_allowed=datetime(*maxDate),
			initial_visible_month=datetime(*date),
			date=datetime(*date).date())],
			style=style
		))