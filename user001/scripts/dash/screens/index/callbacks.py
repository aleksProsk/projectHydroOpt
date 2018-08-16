def loadModal(n0, n1, n2, n3, n4, n5, n6, n7, oldStyle):
	if n0 is None:
		n0 = 0
	if n1 is None:
		n1 = 0
	if n2 is None:
		n2 = 0
	if n3 is None:
		n3 = 0
	if n4 is None:
		n4 = 0
	if n5 is None:
		n5 = 0
	if n6 is None:
		n6 = 0
	if n7 is None:
		n7 = 0
	style = CSafeDict(oldStyle)
	if n0 + n1 + n2 + n3 + n4 + n5 + n6 > n7:
		style.set('display', 'block')
	else:
		style.set('display', 'none')
	return style.getDict()

N0 = 0
N1 = 0
N2 = 0
N3 = 0
N4 = 0
N5 = 0
N6 = 0

def buildModalGraph(n0, n1, n2, n3, n4, n5, n6, fig0, fig1, fig2, fig3, fig4, fig5, fig6):
	global N0, N1, N2, N3, N4, N5, N6
	if n0 is None:
		n0 = 0
	if n1 is None:
		n1 = 0
	if n2 is None:
		n2 = 0
	if n3 is None:
		n3 = 0
	if n4 is None:
		n4 = 0
	if n5 is None:
		n5 = 0
	if n6 is None:
		n6 = 0
	fig = fig0
	if n1 != N1:
		fig = fig1
	if n2 != N1:
		fig = fig2
	if n3 != N1:
		fig = fig3
	if n4 != N1:
		fig = fig4
	if n5 != N1:
		fig = fig5
	if n6 != N1:
		fig = fig6
	log.print(fig)
	newFig = CSafeFigure(figure=fig)
	newFig.scale(1.6)
	return newFig.getFigure()

def renderRevenueAndRiskGraphFigure(value):
	curHist = screenVariables.get('revenueAndRiskGraphFigure')
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	assets = CSafeList(lst=data.get(0))
	i = 0
	was = False
	mi = 0
	ma = 0
	idx = -1
	while i < assets.len():
		if assets.get(i).Shortname in value:
			if was == False:
				ma = assets.get(i).ScenarioWaterManager.Result.RunTime
				mi = assets.get(i).ScenarioWaterManager.Result.RunTime
				idx = i
				was = True
			if assets.get(i).ScenarioWaterManager.Result.RunTime > ma:
				ma = assets.get(i).ScenarioWaterManager.Result.RunTime
			if assets.get(i).ScenarioWaterManager.Result.RunTime < mi:
				mi = assets.get(i).ScenarioWaterManager.Result.RunTime
		i = i + 1
	if idx != -1 and ma == mi and assets.get(0).ScenarioWaterManager.Input.HedgeType == 1:
		R = assets.get(0).ScenarioWaterManager.Result

		#TODO: add this feature
		#???????????????????????????????????????????
		#if isfield(R, 'skipped')
		#	if sum(R.skipped) > 0
		#		R.HedgeRevenue(R.skipped == 1) = [];
		#	end
		#end
		overall = CSafeNP.array(R.OverallRevenue)
		hedgeR = CSafeNP.array(R.HedgeRevenue)
		hedgeV = CSafeNP.array(R.HedgeValue)
		Rev = (overall - hedgeR + hedgeV) / 1e6
		i = idx + 1
		while i < assets.len():
			if assets.get(i).Shortname in value:
				R = assets.get(i).ScenarioWaterManager.Result
				overall = CSafeNP.array(R.OverallRevenue)
				hedgeR = CSafeNP.array(R.HedgeRevenue)
				hedgeV = CSafeNP.array(R.HedgeValue)
				Rev = Rev + (overall - hedgeR + hedgeV) / 1e6
			i = i + 1
		log.print('HERE!!!!!!!!!!!!!!!!!!!!!!!')
		log.print(CSafeNP.array(Rev))
		curHist.setHist(title='', style={'width': '400', 'height': '400'}, xAxis='Revenue Hedged [Mio. EUR]',
						  yAxis='Scenarios', showlegend='False', hoverinfo='x+y', x=Rev)
	else:
		curHist.setHist(title='No common data available', style={'width': '400', 'height': '400'}, xAxis='Revenue Hedged [Mio. EUR]',
						  yAxis='Scenarios', showlegend='False', hoverinfo='x+y', x=[])
	log.print(curHist.getValue())
	return curHist.getValue()
