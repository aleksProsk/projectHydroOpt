from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc
import random

app = dash.Dash()

class CDatePicker(object):
	def __init__(self, callb, minDate=(1995, 8, 5), maxDate=(2017, 9, 19), initDate=(2017, 8, 5), endDate=(2017, 8, 25)): 
		self.__id = random.randint(0,1e6)
		self.__cb = callb
		self.__start_date = dt(*initDate)
		self.__end_date = dt(*endDate)
		self.__rendering = [dcc.DatePickerRange(
			id='my-date-picker-range-' + str(self.__id),
			min_date_allowed=dt(*minDate),
			max_date_allowed=dt(*maxDate),
			initial_visible_month=dt(*initDate),
			end_date=dt(*endDate),
			start_date=dt(*initDate)),
			html.Div(id='output-container-date-picker-range-' + str(self.__id)),
			html.Div(id='fake-container-' + str(self.__id), style={'display':'none'})]
	def update(self):
		def changeData(start_date, end_date):
			if start_date is not None:
				self.__start_date = start_date
			if end_date is not None:
				self.__end_date = end_date
			print('internal data of DatePicker ' + str(self.__id) + ' changed to' + str(self.__start_date) + ' ' + str(self.__end_date))
			return ''
		return changeData
	def getRendering(self): return self.__rendering
	def getCallbDecorator(self): return (
		dash.dependencies.Output('output-container-date-picker-range-' + str(self.__id), 'children'),
		[dash.dependencies.Input('my-date-picker-range-' + str(self.__id), 'start_date'),
		 dash.dependencies.Input('my-date-picker-range-' + str(self.__id), 'end_date')])
	def getFakeCallbDecorator(self):
		return (
		dash.dependencies.Output('fake-container-' + str(self.__id), 'children'),
		[dash.dependencies.Input('my-date-picker-range-' + str(self.__id), 'start_date'),
		 dash.dependencies.Input('my-date-picker-range-' + str(self.__id), 'end_date')])
	def getCallback(self): return self.__cb
	def registerCallb(self, app): 
		app.callback(*self.getFakeCallbDecorator())(self.update())
		app.callback(*self.getCallbDecorator())(self.getCallback())
	#def getSelectedRange(self)	... todo: callb als private methode, die einen sinnvollen output für diese methode (getSelectedRange) bereitstellt


def update_output_A(start_date, end_date):
	string_prefix = 'You have selected: '
	if start_date is not None:
		start_date = dt.strptime(start_date, '%Y-%m-%d')
		start_date_string = start_date.strftime('%B %d, %Y')
		string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
	if end_date is not None:
		end_date = dt.strptime(end_date, '%Y-%m-%d')
		end_date_string = end_date.strftime('%B %d, %Y')
		string_prefix = string_prefix + 'End Date: ' + end_date_string
	if len(string_prefix) == len('You have selected: '):
		return 'Select a date to see it displayed here'
	else:
		return string_prefix
		
def update_output_B(start_date, end_date):
	string_prefix = 'XXXXX: '
	if start_date is not None:
		start_date = dt.strptime(start_date, '%Y-%m-%d')
		start_date_string = start_date.strftime('%B %d, %Y')
		string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
	if end_date is not None:
		end_date = dt.strptime(end_date, '%Y-%m-%d')
		end_date_string = end_date.strftime('%B %d, %Y')
		string_prefix = string_prefix + 'End Date: ' + end_date_string
	if len(string_prefix) == len('You have selected: '):
		return 'Select a date to see it displayed here'
	else:
		return string_prefix


app.config.supress_callback_exceptions = True

myDatePicker1 = CDatePicker(update_output_A)
myDatePicker2 = CDatePicker(update_output_B)
app.layout = html.Div([
	html.Div(myDatePicker1.getRendering()),
	html.Div(myDatePicker2.getRendering())])
myDatePicker1.registerCallb(app)
myDatePicker2.registerCallb(app)



if __name__ == '__main__':
	app.run_server(debug=True, port=5001)