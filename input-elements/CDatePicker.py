from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc
import random

class CDatePicker(object):
	#Initialising function
	#TODO: create an opportunity to define the output object. Now it is only simple div "output-container-date-picker-range"
	def __init__(self, callb, outputId, outputParam='children', minDate=(1995, 8, 5), maxDate=(2017, 9, 19), startDate=(2017, 8, 5), endDate=(2017, 8, 25)): 
		self.__id = random.randint(0,1e6)
		self.__cb = callb
		self.__start_date = dt(*startDate).date()
		self.__end_date = dt(*endDate).date()
		self.__outputId = outputId
		self.__outputParam = outputParam
		self.__rendering = [dcc.DatePickerRange(
			id='my-date-picker-range-' + str(self.__id),
			min_date_allowed=dt(*minDate),
			max_date_allowed=dt(*maxDate),
			initial_visible_month=dt(*startDate),
			end_date=dt(*endDate).date(),
			start_date=dt(*startDate).date()),
			#html.Div(id='output-container-date-picker-range-' + str(self.__id)),
			html.Div(id='fake-container-' + str(self.__id), style={'display':'none'})]
	#Updating function. It is called every time user changes the time range to store current information about date range
	def update(self):
		def changeData(start_date, end_date):
			if start_date is not None:
				self.__start_date = start_date
			if end_date is not None:
				self.__end_date = end_date
			#debug output
			print('internal data of DatePicker ' + str(self.__id) + ' changed to' + str(self.__start_date) + ' ' + str(self.__end_date))
			return ''
		return changeData
	#Wrapper to get the layout of object
	def getRendering(self): return self.__rendering
	#These are the functions to get decorators for callbacks
	def getCallbDecorator(self): return (
		dash.dependencies.Output(self.__outputId, self.__outputParam),
		[dash.dependencies.Input('my-date-picker-range-' + str(self.__id), 'start_date'),
		 dash.dependencies.Input('my-date-picker-range-' + str(self.__id), 'end_date')])
	def getFakeCallbDecorator(self):
		return (
		dash.dependencies.Output('fake-container-' + str(self.__id), 'children'),
		[dash.dependencies.Input('my-date-picker-range-' + str(self.__id), 'start_date'),
		 dash.dependencies.Input('my-date-picker-range-' + str(self.__id), 'end_date')])
	#Wrapper for a callback function
	def getCallback(self): return self.__cb
	#Creating callbacks for object
	def registerCallb(self, app): 
		app.callback(*self.getFakeCallbDecorator())(self.update())
		app.callback(*self.getCallbDecorator())(self.getCallback())
	#Function to receive the date range
	def getSelectedRange(self):
		return 'Current date range is: ' + str(self.__start_date) + ' ' + str(self.__end_date)