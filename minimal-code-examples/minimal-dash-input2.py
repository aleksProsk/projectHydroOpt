from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash()
app.layout = html.Div([
	dcc.DatePickerRange(
		id='my-date-picker-range-1',
		min_date_allowed=dt(1995, 8, 5),
		max_date_allowed=dt(2017, 9, 19),
		initial_visible_month=dt(2017, 8, 5),
		end_date=dt(2017, 8, 25)
	),
	dcc.DatePickerRange(
		id='my-date-picker-range-2',
		min_date_allowed=dt(2000, 8, 5),
		max_date_allowed=dt(2020, 9, 19),
		initial_visible_month=dt(2017, 8, 5),
		end_date=dt(2017, 8, 25)
	),
	html.Div(id='output-container-date-picker-range-1'),
	html.Div(id='output-container-date-picker-range-2')
])

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

app.callback(
	dash.dependencies.Output('output-container-date-picker-range-1', 'children'),
	[dash.dependencies.Input('my-date-picker-range-1', 'start_date'),
	 dash.dependencies.Input('my-date-picker-range-1', 'end_date')])(update_output_A)
	 
app.callback(
	dash.dependencies.Output('output-container-date-picker-range-2', 'children'),
	[dash.dependencies.Input('my-date-picker-range-2', 'start_date'),
	 dash.dependencies.Input('my-date-picker-range-2', 'end_date')])(update_output_B)



if __name__ == '__main__':
	app.run_server(debug=True, port=5001)