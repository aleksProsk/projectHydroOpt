import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash import Dash
from dash.dependencies import Input, Output
#import json
import pandas as pd
import numpy as np

dash_app = Dash(__name__)

DF_GAPMINDER = pd.read_csv(
	#'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
	'C:\\Users\\SEC\\Downloads\\gapminderDataFiveYear.csv'
)
DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['year'] == 2007]
DF_GAPMINDER.loc[0:20]

dt0 = dt.DataTable(
	rows=[{0: 0}],
	row_selectable=False,
	filterable=False,
	sortable=False,
	selected_row_indices=[],
	id='dt0'
)

mydt = dt.DataTable(
	rows=DF_GAPMINDER.to_dict('records'),
	# optional - sets the order of columns
	#columns=sorted(DF_GAPMINDER.columns),
	row_selectable=False,
	filterable=False,
	sortable=False,
	selected_row_indices=[],
	id='datatable-gapminder'
)


#dash_app.layout = html.Div(id='page-content', children=[dcc.Location(id='url', refresh=False)])
dash_app.layout = html.Div(id='page-content', children=[dcc.Location(id='url', refresh=False), dt0])

@dash_app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	return [html.H4('DataTable'), mydt]
	
if __name__ == '__main__':
	dash_app.run_server(debug=False)


