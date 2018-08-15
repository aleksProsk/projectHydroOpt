from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc
from InputElements import Dropdown
from InputElements import Input
from InputElements import Slider
from InputElements import RangeSlider
from InputElements import Textarea
from InputElements import Checklist
from InputElements import Radioitems
from InputElements import DatePickerSingle
from InputElements import DatePickerRange

app = dash.Dash()

#Initialize classes
myDropdown = Dropdown('1', '1', [
			{'label': 'New York City', 'value': 'NYC'},
			{'label': 'Montreal', 'value': 'MTL'},
			{'label': 'San Francisco', 'value': 'SF'}
		],
		False,
		'please select')
		

myInput = Input(uid='1', id='2', placeholder='please write')	

mySlider = Slider('1', '3', 100, 0, 5)

myRangeSlider = RangeSlider('1', '4', 100, 0, 5)
max
myTextarea = Textarea('1', '5', 5, 5, 100)

myChecklist = Checklist('1', '6', [
			{'label': 'New York City', 'value': 'NYC'},
			{'label': 'Montreal', 'value': 'MTL'},
			{'label': 'San Francisco', 'value': 'SF'}
		])

myRadioitems = Radioitems('1', '7', [
			{'label': 'New York City', 'value': 'NYC'},
			{'label': 'Montreal', 'value': 'MTL'},
			{'label': 'San Francisco', 'value': 'SF'}
		])
		
myDatePickerSingle = DatePickerSingle('1', '8', dt(2017, 9, 19), dt(1995, 8, 5))

myDatePickerRange = DatePickerRange('1', '9', dt(2017, 9, 19), dt(1995, 8, 5))
		
#Now create Dash objects from the class items

a = dcc.Dropdown(id = myDropdown.id,
	options = myDropdown.options,
	multi = myDropdown.multi,
	placeholder = myDropdown.placeholder)
	
a1 = html.Div(id = 'a')
		
b = dcc.Input(id = myInput.id,
	placeholder = myInput.placeholder)

b1 = html.Div(id = 'b')

c = dcc.Slider(id = mySlider.id,
	max = mySlider.max,
	min = mySlider.min,
	step = mySlider.step,
	marks = mySlider.marks)
	
c1 = html.Div(id = 'c')

d = dcc.RangeSlider(id = myRangeSlider.id,
	max = myRangeSlider.max,
	min = myRangeSlider.min,
	step = myRangeSlider.step,
	allowCross = myRangeSlider.allowCross,
	marks = myRangeSlider.marks)
	
d1 = html.Div(id = 'd')

e = dcc.Textarea(id = myTextarea.id,
	cols = myTextarea.cols,
	rows = myTextarea.rows,
	maxLength = myTextarea.maxLength,
	placeholder = myTextarea.placeholder,
	title = myTextarea.title)
	
e1 = html.Div(id = 'e')

f = dcc.Checklist(id = myChecklist.id,
	options = myChecklist.options,
	values = [])
	
f1 = html.Div(id = 'f')

g = dcc.RadioItems(id = myRadioitems.id,
	options = myRadioitems.options)
	
g1 = html.Div(id = 'g')

h = dcc.DatePickerSingle(id = myDatePickerSingle.id,
	max_date_allowed = myDatePickerSingle.max_date_allowed,
	min_date_allowed = myDatePickerSingle.min_date_allowed,
    initial_visible_month=dt(2017, 8, 5),)
	
h1 = html.Div(id = 'h')

i = dcc.DatePickerRange(id = myDatePickerRange.id,
	max_date_allowed = myDatePickerSingle.max_date_allowed,
	min_date_allowed = myDatePickerSingle.min_date_allowed,
    initial_visible_month=dt(2017, 8, 5),)
	
i1 = html.Div(id = 'i')

#Store them to make a webpage
lst = []

lst.append(html.Div([a, a1]))
lst.append(html.Div([b, b1]))
lst.append(html.Div([c, c1]))
lst.append(html.Div([d, d1]))
lst.append(html.Div([e, e1]))
lst.append(html.Div([f, f1]))
lst.append(html.Div([g, g1]))
lst.append(html.Div([h, h1]))
lst.append(html.Div([i, i1]))
		
#Make layout
app.layout = html.Div(
	lst
)

#Callbacks for input elements

def f

@app.callback(
	dash.dependencies.Output('a', 'children'),
    [dash.dependencies.Input('1', 'value')])
def update_output(value):
	print('Dropdown changed to ' + value)
	value = f(id,value(
	return value
	
@app.callback(
	dash.dependencies.Output('b', 'children'),
    [dash.dependencies.Input('2', 'value')])
def update_output(value):
	print('Input changed to ' + value)
	return value
	
@app.callback(
	dash.dependencies.Output('c', 'children'),
    [dash.dependencies.Input('3', 'value')])
def update_output(value):
	print('Slider changed to ' + str(value))
	return value
	
@app.callback(
	dash.dependencies.Output('d', 'children'),
    [dash.dependencies.Input('4', 'value')])
def update_output(value):
	print('RangeSlider changed to ' + str(value))
	return value
	
@app.callback(
	dash.dependencies.Output('e', 'children'),
    [dash.dependencies.Input('5', 'value')])
def update_output(value):
	print('Textarea changed to ' + str(value))
	return value
	
@app.callback(
	dash.dependencies.Output('f', 'children'),
    [dash.dependencies.Input('6', 'values')])
def update_output(values):
	print('Checklist changed to ' + str(values))
	return str(values)
	
@app.callback(
	dash.dependencies.Output('g', 'children'),
    [dash.dependencies.Input('7', 'value')])
def update_output(value):
	print('Radioitems changed to ' + str(value))
	return value
	
@app.callback(
	dash.dependencies.Output('h', 'children'),
    [dash.dependencies.Input('8', 'date')])
def update_output(date):
	print('DatePickerSingle changed to ' + str(value))
	return str(date)
	
@app.callback(
	dash.dependencies.Output('i', 'children'),
    [dash.dependencies.Input('9', 'start_date'),
	dash.dependencies.Input('9', 'end_date')])
def update_output(start_date, end_date):
	print('DatePickerRange changed to ' + str(start_date) + ' ' + str(end_date))
	return str(start_date) + str(end_date)
	
'''
for value1, value2 in itertools.product(
        ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']):
    app.callback(
        Output(value2, 'children'),
        [Input(value1, 'value')])(
        print 
    )
	'''
#Run application
if __name__ == '__main__':
	app.run_server(debug=True)
		

