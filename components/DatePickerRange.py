from datetime import date, timedelta, datetime
import dash_core_components as dcc
import dash_html_components as html

from components import DashComponent
CDashComponent = DashComponent.CDashComponent

class CDatePickerRange(CDashComponent):
	#Initialising function
	def __init__(self, minDate = (1995, 8, 5), maxDate = (2017, 9, 19), startDate = (2017, 8, 5), endDate = (2017, 8, 25), style = {},
				 name = None, screenName = None):
		super().__init__(name, screenName)
		self.setDatePickerRange(minDate, maxDate, startDate, endDate, style)
	def update(self, start_date = None, end_date = None):
		if start_date is not None:
			self.__start_date = start_date
		if end_date is not None:
			self.__end_date = end_date
	def getSelectedRange(self):
		return [self.__start_date, self.__end_date]
	def setDatePickerRange(self, minDate, maxDate, startDate, endDate, style):
		self.__start_date = datetime(*startDate).date()
		self.__end_date = datetime(*endDate).date()
		super().setDashRendering(html.Div([dcc.DatePickerRange(
			id=str(super().getID()),
			min_date_allowed=datetime(*minDate),
			max_date_allowed=datetime(*maxDate),
			end_date=datetime(*endDate).date(),
			start_date=datetime(*startDate).date(),
			initial_visible_month=datetime(*startDate).date())],
			style=style
		))