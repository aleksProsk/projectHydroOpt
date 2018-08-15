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

data = hydropt.getData('C:\\Users\\SEC\\Documents\\Alperia\\HydroptModel\\vsm.mod')
children = render_OverallReturn(data)
return children