log.print("starting renderer")
data = hydropt.getData('C:\\Users\\SEC\\Documents\\Alperia\\HydroptModel\\vsm.mod')
result = data.Asset.ScenarioWaterManager.Result

tinterval = [np.min(result.DateNum), np.max(result.DateNum)]

values = np.hstack((
	result.MonthlyEnergyPeak, 
	result.MonthlyEnergyOffPeak,
	result.MonthlyEnergyPeak+result.MonthlyEnergyOffPeak
))

df.define(values, columns=['Peak [MWh]', 'Offpeak [MWh]', 'Total [MWh]'])
log.print(df.columns())
log.print("html stuff")
mydt = dt.DataTable(
	rows=df.to_dict('records'),
	#optional - sets the order of columns
	columns=sorted(df.columns()),
	row_selectable=True,
	filterable=True,
	sortable=True,
	selected_row_indices=[],
	id='datatable-gapminder'
)
log.print("done")

def render_OverallReturn(data):
	fPnl = data.Asset.ScenarioWaterManager.Result.OverallRevenue
	sUnit = 'CHF'
	frame = render_frame('Overall PnL')
	frame.children.append(render_kpi(fPnl, sUnit))
	return frame
		
def render_frame(sCaption):
	return html.Div(className = 'frame', children = [html.H2(sCaption, className = 'frame-caption')])
	
def render_kpi(fKPI, sUnit):
	sKPI = str(fKPI) + " " + sUnit
	return html.P(sKPI, className = 'KPI')

frame = render_frame('Monthly results')
frame.children.append(mydt)
return frame