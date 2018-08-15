import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
#import json
import pandas as pd
import numpy as np

app = dash.Dash()

#app.scripts.config.serve_locally=True

DF_GAPMINDER = pd.read_csv(
	#'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
	'C:\\Users\\SEC\\Downloads\\gapminderDataFiveYear.csv'
)
DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['year'] == 2007]
DF_GAPMINDER.loc[0:20]

app.layout = html.Div([
	html.H4('DataTable'),
	dt.DataTable(
		rows=DF_GAPMINDER.to_dict('records'),
		# optional - sets the order of columns
		columns=sorted(DF_GAPMINDER.columns),
		row_selectable=True,
		filterable=True,
		sortable=True,
		selected_row_indices=[],
		id='datatable-gapminder'
	)
])

if __name__ == '__main__':
	app.run_server(debug=False)