from datetime import datetime as dt
import dash
import dash_html_components as html
from flask import Flask, redirect

from CDatePicker import CDatePicker

#Simple callback methods
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

#Initialising the Dash app
flask_app = Flask(__name__)
#app = dash.Dash()
app = dash.Dash(__name__, server=flask_app)

app.config.supress_callback_exceptions = True

#Build a layout of a webpage
myDatePicker1 = CDatePicker(update_output_A, 'output-1')
myDatePicker2 = CDatePicker(update_output_B, 'output-2')
myDatePicker1.registerCallb(app)
myDatePicker2.registerCallb(app)
app.layout = html.Div([
	html.Div(myDatePicker1.getRendering()),
	html.Div(id='output-1'),
	html.Div(myDatePicker2.getRendering()),
	html.Div(id='output-2'),
	html.Button('Show current date ranges', id='button'),
	html.Div(id='result')])

#Simple callback to respond to button clicks
@app.callback(
		dash.dependencies.Output('result', 'children'),
		[dash.dependencies.Input('button', 'n_clicks')])
def updateResult(n_clicks):
	if n_clicks is None:
		return ''
	start_date1 = myDatePicker1.getSelectedRange()
	start_date2 = myDatePicker2.getSelectedRange()
	return start_date1 + '\n' + start_date2
	
#if __name__ == '__main__':
#	app.run_server(debug=True, port=5001)