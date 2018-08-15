from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash()
a = 'aaa'
b = 'bbb'
app.layout = html.Div([
    dcc.Dropdown(
		id = a,
		options=[
			{'label': 'New York City', 'value': 'NYC'},
			{'label': 'Montreal', 'value': 'MTL'},
			{'label': 'San Francisco', 'value': 'SF'}
		],
		value='MTL',
	),
    dcc.Dropdown(
		id = b,
		options=[
			{'label': 'New York City', 'value': 'NYC'},
			{'label': 'Montreal', 'value': 'MTL'},
			{'label': 'San Francisco', 'value': 'SF'}
		],
		value='MTL',
	),
	html.Div(id='text'),
	html.Div(id='text1')
])


@app.callback(
    dash.dependencies.Output('text', 'children'),
    [dash.dependencies.Input(a, 'value')])
def update_output(value):
	print(1)
	return value
	
@app.callback(
    dash.dependencies.Output('text1', 'children'),
    [dash.dependencies.Input(b, 'value')])
def update_output(value):
	print(1)
	return value

if __name__ == '__main__':
    app.run_server(debug=True)
	