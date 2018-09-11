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

def loadModal1(n0, n1, n2, n3, n4, n5, n6, n7, oldStyle):
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
		N1 = n1
	if n2 != N2:
		fig = fig2
		N2 = n2
	if n3 != N3:
		fig = fig3
		N3 = n3
	if n4 != N4:
		fig = fig4
		N4 = n4
	if n5 != N5:
		fig = fig5
		N5 = n5
	if n6 != N6:
		fig = fig6
		N6 = n6
	newFig = CSafeFigure(figure=fig)
	newFig.scale(1.6)
	return newFig.getFigure()

N0t = 0
N1t = 0
N2t = 0
N3t = 0
N4t = 0
N5t = 0
N6t = 0
dataTables = CSafeDict({})

def buildModalTable(n0, n1, n2, n3, n4, n5, n6):
	global dataTables
	global N0t, N1t, N2t, N3t, N4t, N5t, N6t
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
	if n0 != N0t:
		N0t = n0
		if dataTables.contains('revenueAndRisk'):
			tempDF = CSafeDF()
			tempDF.define(CSafeDict(dataTables.get('revenueAndRisk')).get('rows'), CSafeDict(dataTables.get('revenueAndRisk')).get('headers'))
			return tempDF.to_dict('records')
	if n1 != N1t:
		N1t = n1
		if dataTables.contains('currentPower'):
			tempDF = CSafeDF()
			curDict = CSafeDict(dataTables.get('currentPower'))
			if curDict.contains('titles'):
				columnsList = CSafeList(curDict.get('rows'))
				dt = CSafeList()
				i = 0
				titles = CSafeList(curDict.get('titles'))
				while (i < titles.len()):
					dt.append(CSafeList([titles.get(i)]))
					i = i + 1
				i = 0
				while (i < columnsList.len()):
					column = CSafeList(columnsList.get(i))
					j = 0
					while (j < column.len()):
						tmp = dt.get(j)
						if i == columnsList.len() - 1:
							tmp.append(CSafeList(column.get(j)).get(0) + tmp.get(-1))
						else:
							tmp.append(CSafeList(column.get(j)).get(0))
						dt.set(j, tmp)
						j = j + 1
					i = i + 1
				i = 0
				while (i < dt.len()):
					tmp = dt.get(i)
					dt.set(i, tmp.getList())
					i = i + 1
				tempDF.define(dt.getList(), curDict.get('headers'))
			else:
				rows = CSafeList(curDict.get('rows'))
				i = 1
				while (i < CSafeList(curDict.get('headers')).len()):
					rows.append('')
					i = i + 1
				tempDF.define([rows.getList()], curDict.get('headers'))
			return tempDF.to_dict('records')
	if n2 != N2t:
		N2t = n2
		if dataTables.contains('powerPlanning'):
			tempDF = CSafeDF()
			curDict = CSafeDict(dataTables.get('powerPlanning'))
			if curDict.contains('titles'):
				columnsList = CSafeList(curDict.get('rows'))
				dt = CSafeList()
				i = 0
				titles = CSafeList(curDict.get('titles'))
				while (i < titles.len() - 1):
					dt.append(CSafeList([titles.get(i)]))
					i = i + 1
				i = 0
				while (i < columnsList.len()):
					column = CSafeList(columnsList.get(i))
					j = 0
					while (j < column.len()):
						tmp = dt.get(j)
						tmp.append(column.get(j))
						dt.set(j, tmp)
						j = j + 1
					i = i + 1
				i = 0
				while (i < dt.len()):
					tmp = dt.get(i)
					dt.set(i, tmp.getList())
					i = i + 1
				tempDF.define(dt.getList(), curDict.get('headers'))
			else:
				rows = CSafeList(curDict.get('rows'))
				i = 1
				while (i < CSafeList(curDict.get('headers')).len()):
					rows.append('')
					i = i + 1
				tempDF.define([rows.getList()], curDict.get('headers'))
			return tempDF.to_dict('records')
	if n3 != N3t:
		N3t = n3
		if dataTables.contains('currentReservoirLevel'):
			tempDF = CSafeDF()
			curDict = CSafeDict(dataTables.get('currentReservoirLevel'))
			if curDict.contains('titles'):
				columnsList = CSafeList(curDict.get('rows'))
				dt = CSafeList()
				i = 0
				titles = CSafeList(curDict.get('titles'))
				while (i < titles.len()):
					dt.append(CSafeList([titles.get(i)]))
					i = i + 1
				i = 0
				while (i < columnsList.len()):
					column = CSafeList(columnsList.get(i))
					j = 0
					while (j < column.len()):
						tmp = dt.get(j)
						if i == columnsList.len() - 1:
							tmp.append(CSafeList(column.get(j)).get(0) + tmp.get(-1))
						else:
							tmp.append(CSafeList(column.get(j)).get(0))
						dt.set(j, tmp)
						j = j + 1
					i = i + 1
				i = 0
				while (i < dt.len()):
					tmp = dt.get(i)
					dt.set(i, tmp.getList())
					i = i + 1
				tempDF.define(dt.getList(), curDict.get('headers'))
			else:
				rows = CSafeList(curDict.get('rows'))
				i = 1
				while (i < CSafeList(curDict.get('headers')).len()):
					rows.append('')
					i = i + 1
				tempDF.define([rows.getList()], curDict.get('headers'))
			return tempDF.to_dict('records')
	if n4 != N4t:
		N4t = n4
		if dataTables.contains('marginPrice'):
			tempDF = CSafeDF()
			curDict = CSafeDict(dataTables.get('marginPrice'))
			if curDict.contains('titles'):
				column = CSafeList(curDict.get('rows'))
				dt = CSafeList()
				i = 0
				titles = CSafeList(curDict.get('titles'))
				while (i < titles.len()):
					dt.append(CSafeList([titles.get(i)]))
					i = i + 1
				i = 0
				while (i < column.len()):
					tmp = dt.get(i)
					tmp.append(CSafeList(column.get(i)).get(0))
					dt.set(i, tmp)
					i = i + 1
				i = 0
				while (i < dt.len()):
					tmp = dt.get(i)
					dt.set(i, tmp.getList())
					i = i + 1
				tempDF.define(dt.getList(), curDict.get('headers'))
			else:
				rows = CSafeList(curDict.get('rows'))
				i = 1
				while (i < CSafeList(curDict.get('headers')).len()):
					rows.append('')
					i = i + 1
				tempDF.define([rows.getList()], curDict.get('headers'))
			return tempDF.to_dict('records')
	if n5 != N5t:
		N5t = n5
		if dataTables.contains('reservoirCycle'):
			tempDF = CSafeDF()
			curDict = CSafeDict(dataTables.get('reservoirCycle'))
			if curDict.contains('titles'):
				columnsList = CSafeList(curDict.get('rows'))
				dt = CSafeList()
				i = 0
				titles = CSafeList(curDict.get('titles'))
				while (i < titles.len() - 1):
					dt.append(CSafeList([titles.get(i)]))
					i = i + 1
				i = 0
				while (i < columnsList.len()):
					column = CSafeList(columnsList.get(i))
					j = 0
					while (j < column.len()):
						tmp = dt.get(j)
						if not isinstance(column.get(j), float):
							tmp.append(CSafeList(column.get(j)).get(0))
						else:
							tmp.append(column.get(j))
						dt.set(j, tmp)
						j = j + 1
					i = i + 1
				i = 0
				while (i < dt.len()):
					tmp = dt.get(i)
					dt.set(i, tmp.getList())
					i = i + 1
				tempDF.define(dt.getList(), curDict.get('headers'))
			else:
				rows = CSafeList(curDict.get('rows'))
				i = 1
				while (i < CSafeList(curDict.get('headers')).len()):
					rows.append('')
					i = i + 1
				tempDF.define([rows.getList()], curDict.get('headers'))
			return tempDF.to_dict('records')
	if n6 != N6t:
		N6t = n6
		if dataTables.contains('energyPlanningPeak'):
			tempDF = CSafeDF()
			curDict = CSafeDict(dataTables.get('energyPlanningPeak'))
			if curDict.contains('titles'):
				columnsList = CSafeList(curDict.get('rows'))
				dt = CSafeList()
				i = 0
				titles = CSafeList(curDict.get('titles'))
				while (i < titles.len()):
					dt.append(CSafeList([titles.get(i)]))
					i = i + 1
				i = 0
				while (i < columnsList.len()):
					column = CSafeList(columnsList.get(i))
					j = 0
					while (j < column.len()):
						tmp = dt.get(j)
						tmp.append(CSafeList(column.get(j)).get(0))
						dt.set(j, tmp)
						j = j + 1
					i = i + 1
				i = 0
				while (i < dt.len()):
					tmp = dt.get(i)
					dt.set(i, tmp.getList())
					i = i + 1
				tempDF.define(dt.getList(), curDict.get('headers'))
			else:
				rows = CSafeList(curDict.get('rows'))
				i = 1
				while (i < CSafeList(curDict.get('headers')).len()):
					rows.append('')
					i = i + 1
				tempDF.define([rows.getList()], curDict.get('headers'))
			return tempDF.to_dict('records')
	return []

def renderRevenueAndRiskGraphFigure(value):
	global dataTables
	curHist = screenVariables.get('revenueAndRiskGraphFigure')
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	i = 0
	was = False
	mi = 0
	ma = 0
	idx = -1
	try:
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
	except:
		curHist.setHist(title='No common data available', style={'width': '400', 'height': '400'}, xAxis='Revenue Hedged [Mio. EUR]',
						yAxis='Scenarios', showlegend='False', hoverinfo='x+y', x=[])
		dataTables.set('revenueAndRisk', {'headers': ['Revenue Hedged [Mio. EUR]'], 'rows': ['No common data available']})
		return curHist.getValue()
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
		curHist.setHist(title='', style={'width': '400', 'height': '400'}, xAxis='Revenue Hedged [Mio. EUR]',
						  yAxis='Scenarios', showlegend='False', hoverinfo='x+y', x=Rev)
		dataTables.set('revenueAndRisk', {'headers': ['Revenue Hedged [Mio. EUR]'], 'rows': Rev})
	else:
		curHist.setHist(title='No common data available', style={'width': '400', 'height': '400'}, xAxis='Revenue Hedged [Mio. EUR]',
						  yAxis='Scenarios', showlegend='False', hoverinfo='x+y', x=[])
		dataTables.set('revenueAndRisk', {'headers': ['Revenue Hedged [Mio. EUR]'], 'rows': ['No common data available']})
	return curHist.getValue()

def getAvenisOptionTypes():
	j = 0
	OT = CSafeList()
	OT.append({})
	OT.append({})
	OT.append({})
	OT.append({})
	OT.append({})
	OT.append({})
	OT.append({})
	OT.append({})
	OT.append({})
	OT.append({})
	tDict = CSafeDict()
	tDict.set('ID', 1001)
	tDict.set('Name', 'Daily Base Swing')
	tDict.set('ParameterName', ['Max Power [MW]', 'Max Draws'])
	tDict.set('ParameterDefault', [50, 21])
	tDict.set('nParameters', 2)
	tDict.set('UsePut', 0)
	tTempDict = CSafeDict()
	tTempDict.set('CurrentPower', 1)
	tTempDict.set('PowerPlanning', 1)
	tTempDict.set('CurrentReservoirLevel', 1)
	tTempDict.set('ReservoirCycle', 1)
	tTempDict.set('WaterValue', 0)
	tTempDict.set('EnergyPlanning', 1)
	tDict.set('Show', tTempDict.getDict())
	tDict.set('Description', ['DAILY BASE SWING', '', 'The Buyer has the right to buy base load power called on a day ahead basis from the Seller.', '',
							  'Buyer can call a maximum of <MaxDraws> days and must pay an option premium for <MaxDraws> days worth of calls whether they are used or not'])
	OT.set(j, tDict.getDict())

	j = j + 1;
	tDict = CSafeDict()
	tDict.set('ID', 1002)
	tDict.set('Name', 'Daily Peak Swing')
	tDict.set('ParameterName', ['Max Power [MW]', 'Max Draws'])
	tDict.set('ParameterDefault', [50, 21])
	tDict.set('nParameters', 2)
	tDict.set('UsePut', 0)
	tTempDict = CSafeDict()
	tTempDict.set('CurrentPower', 1)
	tTempDict.set('PowerPlanning', 1)
	tTempDict.set('CurrentReservoirLevel', 1)
	tTempDict.set('ReservoirCycle', 1)
	tTempDict.set('WaterValue', 0)
	tTempDict.set('EnergyPlanning', 1)
	tDict.set('Show', tTempDict.getDict())
	tDict.set('Description', ['DAILY PEAK SWING', '', 'The Buyer has the right to buy peak load power called on a day ahead basis from the Seller.', '',
							  'Buyer can call a maximum of <MaxDraws> days and must pay an option premium for <MaxDraws> days worth of calls whether they are used or not'])
	OT.set(j, tDict.getDict())

	j = j + 1;
	tDict = CSafeDict()
	tDict.set('ID', 1003)
	tDict.set('Name', 'Hourly Swing')
	tDict.set('ParameterName', ['Max Power [MW]', 'Max Hours', 'Min # of Op. Hours'])
	tDict.set('ParameterDefault', [50, 1000, 4])
	tDict.set('nParameters', 3)
	tDict.set('UsePut', 0)
	tTempDict = CSafeDict()
	tTempDict.set('CurrentPower', 1)
	tTempDict.set('PowerPlanning', 1)
	tTempDict.set('CurrentReservoirLevel', 1)
	tTempDict.set('ReservoirCycle', 1)
	tTempDict.set('WaterValue', 1)
	tTempDict.set('EnergyPlanning', 1)
	tDict.set('Show', tTempDict.getDict())
	tDict.set('Description', ['HOURLY SWING', '', 'The Buyer has the right to buy power called on a day ahead basis from the Seller.', '',
							  'Buyer can call a maximum of <Max Hours> hours and must pay an option premium for <Max Hours> hours worth of calls whether they are used or not', '',
							  'When calling, buyer must call at least <Min # of Op. Hours> consecutive hours.'])
	OT.set(j, tDict.getDict())

	j = j + 1;
	tDict = CSafeDict()
	tDict.set('ID', 1007)
	tDict.set('Name', 'Hourly Strike Swing')
	tDict.set('ParameterName', ['Max Power [MW]', 'Strike Price [€/MWh]', 'Max Hours', 'Min # of Op. Hours'])
	tDict.set('ParameterDefault', [50, 100, 100, 4])
	tDict.set('nParameters', 4)
	tDict.set('UsePut', 0)
	tTempDict = CSafeDict()
	tTempDict.set('CurrentPower', 1)
	tTempDict.set('PowerPlanning', 1)
	tTempDict.set('CurrentReservoirLevel', 1)
	tTempDict.set('ReservoirCycle', 1)
	tTempDict.set('WaterValue', 0)
	tTempDict.set('EnergyPlanning', 1)
	tDict.set('Show', tTempDict.getDict())
	tDict.set('Description', ['HOURLY STRIKE SWING', '', 'The option resembles a string of hourly call options at a certain strike price.', '',
			   'The overall number of drawn hours is restricted by <Max Hours>', '', 'When calling, buyer must call at least <Min # of Op. Hours> consecutive hours..', '', ''])
	OT.set(j, tDict.getDict())

	j = j + 1;
	tDict = CSafeDict()
	tDict.set('ID', 1008)
	tDict.set('Name', 'MinMax Strike Swing')
	tDict.set('ParameterName', ['Max Power [MW]', 'Strike Price [€/MWh]', 'Min Hours', 'Max Hours'])
	tDict.set('ParameterDefault', [25, 66, 1750, 2000])
	tDict.set('nParameters', 4)
	tDict.set('UsePut', 0)
	tTempDict = CSafeDict()
	tTempDict.set('CurrentPower', 1)
	tTempDict.set('PowerPlanning', 1)
	tTempDict.set('CurrentReservoirLevel', 1)
	tTempDict.set('ReservoirCycle', 1)
	tTempDict.set('WaterValue', 0)
	tTempDict.set('EnergyPlanning', 1)
	tDict.set('Show', tTempDict.getDict())
	tDict.set('Description', ['MINMAX STRIKE SWING', '', 'The option resembles a string of hourly call options at a certain strike price.', '',
			   'The overall number of drawn hours must be at least <Min Hours> and at most <Max Hours>', '', ''])
	OT.set(j, tDict.getDict())

	j = j + 1;
	tDict = CSafeDict()
	tDict.set('ID', 1004)
	tDict.set('Name', 'Synthetic Storage')
	tDict.set('ParameterName', ['Turbine Power [MW]', 'Pump Power [MW]', 'Pump Efficiency [1]', 'Max Level [GWh]', 'Start Level [GWh]', 'End Level [GWh]', 'Min # of Op. Hours'])
	tDict.set('ParameterDefault', [25, 30, 0.7, 100, 0, 0, 1])
	tDict.set('nParameters', 7)
	tDict.set('UsePut', 0)
	tTempDict = CSafeDict()
	tTempDict.set('CurrentPower', 1)
	tTempDict.set('PowerPlanning', 1)
	tTempDict.set('CurrentReservoirLevel', 1)
	tTempDict.set('ReservoirCycle', 1)
	tTempDict.set('WaterValue', 1)
	tTempDict.set('EnergyPlanning', 1)
	tDict.set('Show', tTempDict.getDict())
	tDict.set('Description', ['SYNTHETIC STORAGE', '', 'The option resembles a pump storage hydro plant with one reservoir, one turbine and one pump.', '',
							  'The Buyer has the right to draw and deliver energy which is accounted for in a virtual reservoir.', '',
							  'Delivered (pumped) energy is multiplied by <Pump Efficiency> before added to the reservoir.', '',
							  'Start and End Level of the reservoir as well as the minimum number of consecutive production/pump hours can be defined.', '', ''])
	OT.set(j, tDict.getDict())

	j = j + 1;
	tDict = CSafeDict()
	tDict.set('ID', 1005)
	tDict.set('Name', 'EdF Virtual Power Plant')
	tDict.set('ParameterName', ['Max Power [MW]', 'Strike Price [€/MWh]', 'Min # of Op. Hours', 'Min # of Idle Hours'])
	tDict.set('ParameterDefault', [50, 23.18, 1, 1])
	tDict.set('nParameters', 4)
	tDict.set('UsePut', 0)
	tTempDict = CSafeDict()
	tTempDict.set('CurrentPower', 1)
	tTempDict.set('PowerPlanning', 1)
	tTempDict.set('CurrentReservoirLevel', 0)
	tTempDict.set('ReservoirCycle', 0)
	tTempDict.set('WaterValue', 0)
	tTempDict.set('EnergyPlanning', 1)
	tDict.set('Show', tTempDict.getDict())
	tDict.set('Description', ['EDF VIRTUAL POWER PLANT', '', 'The option resembles a string of hourly call options at a certain strike price.', '',
							  'When calling, buyer must call at least <Min # of Op. Hours> consecutive hours.', '<Min # of Idle Hours> can also be specified'])
	OT.set(j, tDict.getDict())

	j = j + 1;
	tDict = CSafeDict()
	tDict.set('ID', 1006)
	tDict.set('Name', 'UK Virtual Power Plant')
	tDict.set('ParameterName', ['Max Power [MW]', 'Strike Price [€/MWh]', 'From Hour', 'To Hour', 'Startup Cost [€]'])
	tDict.set('ParameterDefault', [50, 23.18, 7, 21, 300])
	tDict.set('nParameters', 5)
	tDict.set('UsePut', 0)
	tTempDict = CSafeDict()
	tTempDict.set('CurrentPower', 1)
	tTempDict.set('PowerPlanning', 1)
	tTempDict.set('CurrentReservoirLevel', 0)
	tTempDict.set('ReservoirCycle', 0)
	tTempDict.set('WaterValue', 0)
	tTempDict.set('EnergyPlanning', 1)
	tDict.set('Show', tTempDict.getDict())
	tDict.set('Description', ['UK VIRTUAL POWER PLANT', '', 'The option resembles a string of hourly call options at a certain strike price.', '',
							  'The power may be called on week days and weekends between <From Hour> and <To Hour> in hourly blocks.', '',
							  'The Buyer will pay the Seller <Startup Cost> per start.', '', ''])
	OT.set(j, tDict.getDict())

	###    % return % < -- für ALPIQ auskommentieren    ###

	j = j + 1;
	tDict = CSafeDict()
	tDict.set('ID', 1009)
	tDict.set('Name', 'Reduction Option')
	tDict.set('ParameterName', ['Max Power [MW]', 'Max Starts', 'Max Nr. of op. Hours'])
	tDict.set('ParameterDefault', [50, 22, 12])
	tDict.set('nParameters', 3)
	tDict.set('UsePut', 0)
	tTempDict = CSafeDict()
	tTempDict.set('CurrentPower', 1)
	tTempDict.set('PowerPlanning', 1)
	tTempDict.set('CurrentReservoirLevel', 0)
	tTempDict.set('ReservoirCycle', 0)
	tTempDict.set('WaterValue', 0)
	tTempDict.set('EnergyPlanning', 1)
	tDict.set('Show', tTempDict.getDict())
	tDict.set('Description', ['REDUCTION OPTION', '', 'The holder of the option is allowed to draw energy at a certain power b times (e.g. 22) within a specified time interval.',
							  '', 'The number of subsequently drawn hours must not exceed the number c.', '', ''])
	OT.set(j, tDict.getDict())

	j = j + 1;
	tDict = CSafeDict()
	tDict.set('ID', 1010)
	tDict.set('Name', 'Special Reduction Option')
	tDict.set('ParameterName', ['Max Power [MW]', 'Max Starts', 'Max Starts last month', 'Min # of Op. Hours', 'Max # of Op. Hours', 'Max Energy [MWh]'])
	tDict.set('ParameterDefault', [50, 22, 5, 4, 12, 13200])
	tDict.set('nParameters', 6)
	tDict.set('UsePut', 0)
	tTempDict = CSafeDict()
	tTempDict.set('CurrentPower', 1)
	tTempDict.set('PowerPlanning', 1)
	tTempDict.set('CurrentReservoirLevel', 0)
	tTempDict.set('ReservoirCycle', 0)
	tTempDict.set('WaterValue', 0)
	tTempDict.set('EnergyPlanning', 1)
	tDict.set('Show', tTempDict.getDict())
	tDict.set('Description', ['SPECIAL REDUCTION OPTION', '',
							  'The holder of the option is allowed to draw energy at a certain power b times (e.g. 22) within a specified time interval, however only m times (e.g. 5) within the last month of this time interval.',
							  '', 'The overall amount of drawn energy must not exceed a given value. The minimum and maximum number of subsequently drawn hours can be specified.', '', ''])
	OT.set(j, tDict.getDict())
	return OT

def getStandardOptionTypes(*arglst):
	global getAvenisOptionTypes
	arglst = CSafeList(arglst)
	OT = getAvenisOptionTypes()
	if arglst.len() == 1:
		if arglst.get(0) <= 1000:
			num = arglst.get(0)
		else:
			i = 0
			while (i < OT.len()):
				if OT.get(i).ID == arglst.get(0):
					num = i
				i = i + 1
		return OT.get(num)

def isStochastic(asset, resIdx):
	if asset.Topology.nRes == 1:
		return int(asset.Reservoir.IsStochastic)
	else:
		reservoirs = CSafeList(CSafeList(asset.Reservoir).get(0))
		return int(reservoirs.get(int(resIdx) - 1).IsStochastic)

def renderMarginPriceGraphFigure(value):
	global dataTables
	global isStochastic, getStandardOptionTypes
	curChart = screenVariables.get('marginPriceGraphFigure')
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	MP = CSafeList()
	MP5 = CSafeList()
	MP95 = CSafeList()
	TurbName = CSafeList()
	TurbShortname = CSafeList()
	AssetTurbNumber = CSafeList()
	i = 0
	try:
		while (i < assets.len()):
			if assets.get(i).Shortname in value:
				if assets.get(i).Type == 2:
					OT = getStandardOptionTypes(assets.get(i).Option.TypeID)
					if not OT.Show.WaterValue:
						i = i + 1
						continue
				j = 0
				if assets.get(i).Topology.nTurbines + assets.get(i).Topology.nPumps == 1:
					topologyEngines = CSafeList([assets.get(i).Topology.Engine])
				else:
					topologyEngines = CSafeList(CSafeList(assets.get(i).Topology.Engine).get(0))
				while (j < assets.get(i).Topology.nTurbines):
					OperatesFrom = topologyEngines.get(j).OperatesFrom
					if OperatesFrom <= assets.get(i).Topology.nRes:
						if assets.get(i).Topology.nTurbines + assets.get(i).Topology.nPumps == 1:
							engines = CSafeList([assets.get(i).Engine])
						else:
							engines = CSafeList(CSafeList(assets.get(i).Engine).get(0))
						if isStochastic(assets.get(i), OperatesFrom) == 1:
							MarginPrice = CSafeList(CSafeNP.array(engines.get(j).ScenarioWaterManager.Result.MarginPrice))
							MarginPrice.sort()
							MP.append(CSafeNP.mean(MarginPrice.getList()))
							quantile = 1
							if (int(round(MarginPrice.len() * 0.05)) > quantile):
								quantile = int(round(MarginPrice.len() * 0.05))
							MP5.append(MarginPrice.get(quantile - 1))
							MP95.append(MarginPrice.get(-quantile))
							TurbName.append(engines.get(j).Shortname)
							TurbShortname.append(assets.get(i).Shortname + '-' + engines.get(j).Shortname)
							AssetTurbNumber.append([i, j])
							if len(engines.get(j).Shortname) == 0:
								TurbName.set(TurbName.len() - 1, assets.get(i).Shortname + '-' + str(j))
								TurbShortname.set(TurbShortname.len() - 1, assets.get(i).Shortname)
					j = j + 1
			i = i + 1
	except:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('marginPrice', {'headers': ['Margin Price [EUR/MWh]'], 'rows': ['No common data available']})
		return curChart.getValue()
	MPsort = CSafeList()
	i = 0
	while (i < MP.len()):
		MPsort.append([MP.get(i), i])
		i = i + 1
	MPsort.sortKey(0, desc=True)
	permutation = CSafeList()
	i = 0
	MPs = CSafeList()
	MPss = CSafeList()
	MP5s = CSafeList()
	MP95s = CSafeList()
	TurbNames = CSafeList()
	TurbShortnames = CSafeList()
	AssetTurbNumbers = CSafeList()
	while (i < MPsort.len()):
		permutation.append(CSafeList(MPsort.get(i)).get(1))
		MPs.append([CSafeList(MPsort.get(i)).get(0)])
		MPss.append(CSafeList(MPsort.get(i)).get(0))
		i = i + 1
	i = 0
	while (i < MP5.len()):
		MP5s.append(MP5.get(permutation.get(i)))
		MP95s.append(MP95.get(permutation.get(i)))
		TurbNames.append(TurbName.get(permutation.get(i)))
		TurbShortnames.append(TurbShortname.get(permutation.get(i)))
		AssetTurbNumbers.append(AssetTurbNumber.get(permutation.get(i)))
		i = i + 1
	errorBar = CSafeDict({})
	errorBar.set('type', 'data')
	errorBar.set('visible', True)
	errorBar.set('array', CSafeNP.array(MP95s.getList()) - CSafeNP.array(MPss.getList()))
	errorBar.set('arrayminus', CSafeNP.array(MP5s.getList()) - CSafeNP.array(MPss.getList()))
	if MPs.len() > 0:
		curChart.setChart(rows=[MPs.getList()], headers=TurbShortnames.getList(), rowCaptions=TurbShortnames.getList(), title='', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error=errorBar.getDict())
		dataTables.set('marginPrice', {'headers': ['Turbine', 'Margin Price [EUR/MWh]'], 'rows': MPs.getList(), 'titles': TurbShortnames.getList()})
	else:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('marginPrice', {'headers': ['Margin Price [EUR/MWh]'], 'rows': ['No common data available']})
	return curChart.getValue()

def getProperTime(Start, End):
	### TODO: delete LastSunMar LastSunOct as in matlab ???
	t = CSafeList()
	i = Start
	while (i <= End):
		t.append(i)
		i = i + 1.0 / 24.0
	dt = 1.0 / 24.0 / 60.0 / 10.0

	return t

def getHydroptTime(*arglst):
	global getProperTime
	arglst = CSafeList(arglst)
	if arglst.len() == 0:
		delta = datetime.now() - datetime(1, 1, 1)
		tStart = math.floor(math.floor(float(delta.days) + (float(delta.seconds) / 86400) + 367))
		tEnd = tStart + 365
	elif arglst.len() == 1:
		return CSafeLst([arglst.get(0)])
	else:
		tStart = arglst.get(0)
		tEnd = arglst.get(1)
	Time = getProperTime(tStart, tEnd)
	return Time

def fileparts(FileName):
	tans = CSafeList(CSafeStr(FileName).split('.'))
	path = tans.get(0)
	ext = tans.get(1)
	tans = CSafeList(CSafeStr(path).rsplit('\\'))
	path = tans.get(0)
	name = tans.get(1)
	ans = CSafeList([path, name, ext])
	return ans

def getCustomFormat(FileName):
	global fileparts
	Msg = ''
	Dat = []
	Val = []
	ans = CSafeList()
	tans = fileparts(FileName)
	Dummy = tans.get(0)
	Name = tans.get(1)
	Ext = tans.get(2)
	try:
		sep = globalDict.get('hydroptModel').Status.Import.ColumnSeparator
		dt = CSafeList(pd.read_csv(FileName).values)
		i = 0
		### TODO: pd.values doesn't read the first line with comment!
		while (i < int(globalDict.get('hydroptModel').Status.Import.StartDate.Row)):
			line = CSafeList(dt.get(i)).get(0)
			i = i + 1
		SepPos = CSafeStr(line).find(sep)
		if SepPos != -1:
			DateString = CSafeStr(CSafeStr(line).slice(0, SepPos))
		else:
			DateString = CSafeStr(line)
		DateFormat = CSafeStr(globalDict.get('hydroptModel').Status.Import.DateFormat)
		DateFormat.replace('dd', '%d')
		DateFormat.replace('mm', '%m')
		DateFormat.replace('yyyy', '%Y')
		DateFormat.replace('HH', '%H')
		DateFormat.replace('MM', '%M')
		if abs(DateFormat.len() - DateString.len()) < 3:
			Dat = datetime.strptime(DateString.getStr(), DateFormat.getStr())
		elif DateFormat.len() > DateString.len():
			Dat = datetime.strptime(DateString.getStr(), '%d.%m.%Y')
		elif DateFormat.len() < DateString.len():
			Dat = datetime.strptime(DateString.getStr(), '%d.%m.%Y %H:%M')
		Dat = Dat.toordinal() + 366
		Val = CSafeList(CSafeNP.getColumn(pd.read_csv(FileName, sep=sep).values, 1))
	except:
		Msg = 'File not found'
	ans.append(Msg)
	ans.append(Dat)
	ans.append(Val)
	return ans

def getHydroptFormat(FileName):
	Msg = ''
	Dat = []
	Val = []
	ans = CSafeList()
	try:
		tans = fileparts(FileName)
		Dummy = tans.get(0)
		Name = tans.get(1)
		Ext = tans.get(2)
		dt = CSafeList(pd.read_csv(FileName).values)
		DateString = dt.get(0)
		DateFormat = CSafeStr(globalDict.get('hydroptModel').Status.Import.HydroptDateFormat)
		DateFormat.replace('dd', '%d')
		DateFormat.replace('mm', '%m')
		DateFormat.replace('yyyy', '%Y')
		DateFormat.replace('HH', '%H')
		DateFormat.replace('MM', '%M')
		Dat = datetime.strptime(DateString, DateFormat)
		Val = CSafeList(CSafeNP.getColumn(pd.read_csv(FileName, sep=sep).values, 1))
	except:
		Msg = 'Error reading file'
	ans.append(Msg)
	ans.append(Dat)
	ans.append(Val)
	return ans

def getCSVFile(FileName):
	global getCustomFormat, getHydroptFormat
	Format = 'Custom'
	DateNum = []
	Values = []
	Msg = ''
	ans = CSafeList()
	tans = getCustomFormat(FileName)
	if tans.get(0) != '':
		tans = getHydroptFormat(FileName)
		Format = 'Hydropt'
		Msg = tans.get(0)
		Dat = tans.get(1)
		Val = tans.get(2)
	else:
		Dat = tans.get(1)
		Val = tans.get(2)
	if Msg != '':
		ans.append(Msg)
		ans.append(DateNum)
		ans.append(Values)
		ans.append(Format)
		return ans
	TimeShift = 0 if globalDict.get('hydroptModel').Status.Import.FromTime == 0 else 1.0 / 24.0
	t = getHydroptTime(Dat - TimeShift, Dat + Val.len() / 24.0 + 10)
	DateNum = CSafeList(t.slice(0, Val.len()))
	Values = Val
	ans.append(Msg)
	ans.append(DateNum)
	ans.append(Values)
	ans.append(Format)
	return ans

def getTSValues(*arglst):
	global getHydroptTime, getCSVFile
	arglst = CSafeList(arglst)
	FileName = arglst.get(0)
	Context = 'Silent'
	### TODO: add some filename building stuff with regexp
	Values = CSafeList()
	MinStart = CSafeList()
	MaxEnd = CSafeList()
	Msg = ''
	Format = CSafeList()
	i = 1
	nargs = arglst.len()
	while (i < nargs):
		if isinstance(arglst.get(i), str):
			Context = arglst.get(i)
			nargs = nargs - 1
		i = i + 1
	if nargs == 2:
		DateNumStart = arglst.get(1)
		DateNumEnd = arglst.get(1)
	elif nargs == 3:
		DateNumStart = arglst.get(1)
		DateNumEnd = arglst.get(2)
	if FileName is None or len(FileName) == 0:
		Msg = 'No file defined'
	else:
		### TODO: add interacting with files stuff
		if CSafeStr(FileName).get(0) == '.':
			FileName = r"\\TAH-HUT\Users\Aleksandr Proskurin\Documents\HydroOptStorage" + CSafeStr(FileName).slice(1, CSafeStr(FileName).len())
			tans = getCSVFile(FileName)
			Msg = tans.get(0)
			DateNum = tans.get(1)
			Values = tans.get(2)
			Format = tans.get(3)
			if Msg != '':
				return CSafeList([Values, MinStart, MaxEnd, Msg, Format])
			if nargs >= 2:
				MinStart = DateNum.get(0)
				MaxEnd = DateNum.get(-1)
				start_idx = CSafeNP.whereTime(DateNum.getList(), DateNumStart)
				end_idx = CSafeNP.whereTime(DateNum.getList(), DateNumEnd)
				if start_idx == -1 or end_idx == -1:
					Msg = 'Time interval is incorrect'
				else:
					Values = CSafeList(Values.slice(start_idx, end_idx))
			elif nargs == 1:
				MinStart = DateNum.get(0)
				MaxEnd = DateNum.get(-1)
		elif FileName.replace('.','',1).isdigit():
			if nargs > 1:
				t = getHydroptTime(DateNumStart,DateNumEnd)
			else:
				t = getHydroptTime()
			i = 0
			while (i < t.len()):
				Values.append(float(FileName))
				MinStart = -1000000007
				MaxEnd = 1000000007
				i = i + 1
		else:
			Msg = 'This case wasn\'t implemented so far'
	if Msg != '':
		###TODO: add this enormous disgusting list of lines which do something (I can't understand what at all)
		return CSafeList([Values, MinStart, MaxEnd, Msg, Format])
	return CSafeList([Values, MinStart, MaxEnd, Msg, Format])

def renderCurrentPowerGraphFigure(value):
	global dataTables
	global getStandardOptionTypes, getTSValues
	curChart = screenVariables.get('currentPowerGraphFigure')
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	MaxPower = CSafeList()
	CurrentPower = CSafeList()
	name = CSafeList()
	i = 0
	while (i < assets.len()):
		if assets.get(i).Shortname in value:
			if assets.get(i).Type == 2:
				OT = getStandardOptionTypes(assets.get(i).Option.TypeID)
				if not OT.Show.CurrentPower:
					i = i + 1
					continue
			CurP = 0
			MaxP = 0
			j = 0
			while (j < assets.get(i).Topology.nTurbines):
				if assets.get(i).Topology.nTurbines + assets.get(i).Topology.nPumps == 1:
					engines = CSafeList([assets.get(i).Engine])
				else:
					engines = CSafeList(CSafeList(assets.get(i).Engine).get(0))
				tmp = getTSValues(engines.get(j).MaxFlowFile, 'Silent')
				ThisPower = tmp.get(0)
				MinStart = tmp.get(1)
				MaxEnd = tmp.get(2)
				Msg = tmp.get(3)
				if Msg != '':
					curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
					dataTables.set('currentPower', {'headers': ['Current Power [MW]', 'Maximum Power [MW]'], 'rows': ['No common data available']})
					return curChart.getValue()
				if MinStart > -1000000007:
					#### TODO: solve the case of real time series
					t = 1
					NowIdx = 0
				else:
					NowIdx = 0
				ThisCurPower = ThisPower.get(NowIdx)
				ThisMaxPower = CSafeNP.max(ThisPower.getList())
				CurP = CurP + ThisCurPower
				MaxP = MaxP + ThisMaxPower
				j = j + 1
			MaxPower.append(MaxP)
			CurrentPower.append(CurP)
			name.append(assets.get(i).Shortname)
		i = i + 1
	CurrentPowerSort = CSafeList()
	CurrentPowers = CSafeList()
	MaxPowers = CSafeList()
	names = CSafeList()
	i = 0
	while (i < CurrentPower.len()):
		CurrentPowerSort.append([CurrentPower.get(i), i])
		i = i + 1
	CurrentPowerSort.sortKey(0, desc=True)
	i = 0
	while (i < CurrentPower.len()):
		CurrentPowers.append(CSafeList(CurrentPowerSort.get(i)).get(0))
		MaxPowers.append(MaxPower.get(CSafeList(CurrentPowerSort.get(i)).get(1)))
		names.append(name.get(CSafeList(CurrentPowerSort.get(i)).get(1)))
		i = i + 1
	if MaxPowers.len() == 0:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('currentPower', {'headers': ['Current Power [MW]', 'Maximum Power [MW]'], 'rows': ['No common data available']})
	else:
		MaxPowerDelta = CSafeList(CSafeNP.array(MaxPowers.getList()) - CSafeNP.array(CurrentPowers.getList()))
		MaxPowerG = CSafeList()
		CurrentPowerG = CSafeList()
		i = 0
		while (i < CurrentPowers.len()):
			MaxPowerG.append([MaxPowerDelta.get(i)])
			CurrentPowerG.append([CurrentPowers.get(i)])
			i = i + 1
		curChart.setChart(rows=[CurrentPowerG.getList(), MaxPowerG.getList()], headers=['Current Power', 'Max Power'], rowCaptions=names.getList(), title='',
						  type='bar', barmode='stack', style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('currentPower', {'headers': ['Asset', 'Current Power [MW]', 'Maximum Power [MW]'], 'rows': [CurrentPowerG.getList(), MaxPowerG.getList()], 'titles': names.getList()})
	return curChart.getValue()

def getChars(*arglst):
	arglst = CSafeList(arglst)
	nargs = arglst.len()
	FileName = arglst.get(0)
	Context = 'Silent'
	i = 1
	while (i < arglst.len()):
		if isinstance(arglst.get(i), str):
			Context = arglst.get(i)
			nargs = nargs - 1
		i = i + 1
	M3 = CSafeList()
	MWsPerM3 = CSafeList()
	Msg = ''
	tans = CSafeDict({})
	if FileName == None or FileName == '':
		Msg = 'No file defined.'
	else:
		### TODO: add interactions with files
		if FileName.replace('.','',1).isdigit():
			M3 = CSafeList([0, 1e10])
			MWsPerM3 = CSafeList([float(FileName), float(FileName)])
			tans.set('Reservoir_Level_M3', M3)
			tans.set('MWs_per_CubicMetre', MWsPerM3)
		else:
			Msg = 'Error with FileName.'
	return CSafeList([tans, Msg])

def getMWh2M3(*arglst):
	global getChars
	arglst = CSafeList(arglst)
	nargs = arglst.len()
	FileName = arglst.get(0)
	Context = 'Silent'
	i = 1
	while (i < arglst.len()):
		if isinstance(arglst.get(i), str):
			Context = arglst.get(i)
			nargs = nargs - 1
		i = i + 1
	M3 = CSafeList()
	MWh = CSafeList()
	Msg = ''
	A = CSafeDict({})
	if FileName == None or FileName == '':
		Msg = 'No file defined.'
	else:
		FileName = CSafeStr(FileName)
		### TODO: relative paths are given
		### TODO: add working with files???
		if FileName.get(0) == '%':
			asset = arglst.get(1)
			ResIdx = arglst.get(2)
			Top = asset.Topology
			ComponentType = 1
			i = 0
			Idx = CSafeList()
			if Top.nTurbines + Top.nPumps == 1:
				enginesTop = CSafeList([asset.Topology.Engine])
				engines = CSafeList([asset.Engine])
			else:
				enginesTop = CSafeList(CSafeList(asset.Topology.Engine).get(0))
				engines = CSafeList(CSafeList(asset.Engine).get(0))
			while (i < Top.nTurbines):
				if enginesTop.get(i).OperatesFrom == ResIdx + 1:
					Idx.append(i)
				i = i + 1
			if Idx.len() == 0 and Top.nFlows > 0:
				componentType = 2
				if Top.nFlows == 1:
					flows = CSafeList([asset.Topology.Flow])
				else:
					flows = CSafeList(CSafeList(asset.Topology.Flow).get(0))
				i = 0
				while (i < Top.nFlows):
					if flows.get(i).OperatesFrom == ResIdx + 1:
						Idx.append(i)
					i = i + 1
			if Idx.len() == 0:
				Msg = 'There is a reservoir without a turbine below. AutoCalc not possible.'
				NextResIdx = 0
			elif Idx.len() >= 2:
				Msg = 'There is a reservoir with more than one turbine/flow below. AutoCalc not possible.'
				NextResIdx = 0
			elif ComponentType == 1:
				tans = getChars(engines.get(Idx.get(0)).EngineCharacteristicFile)
				if tans.get(1) != '':
					Msg = tans.get(1)
					NextResIdx = 0
				else:
					M30 = tans.get(0).get('Reservoir_Level_M3')
					MWsPerM3 = tans.get(0).get('MWs_per_CubicMetre')
					NextResIdx = enginesTop.get(Idx.get(0)).OperatesTo
			else:
				M30 = CSafeList([0, 1e10])
				MWsPerM3 = CSafeList([0, 0])
				NextResIdx = flows.get(Idx.get(0)).OperatesTo
			while (NextResIdx > 0):
				Idx = CSafeList()
				i = 0
				while (i < Top.nTurbines):
					if enginesTop.get(i).OperatesFrom == NextResIdx:
						Idx.append(i)
					i = i + 1
				ComponentType = 1
				if Idx.len() == 0 and Top.nFlows > 0:
					componentType = 2
					i = 0
					while (i < Top.nFlows):
						if flows.get(i).OperatesFrom == NextResIdx:
							Idx.append(i)
						i = i + 1
				if Idx.len() == 0:
					Msg = 'There is a reservoir without a turbine below. AutoCalc not possible.'
					NextResIdx = 0
				elif Idx.len() >= 2:
					Msg = 'There is a reservoir with more than one turbine/flow below. AutoCalc not possible.'
					NextResIdx = 0
				elif ComponentType == 1:
					tans = getChars(engines.get(Idx.get(0)).EngineCharacteristicFile)
					if tans.get(1) != '':
						Msg = tans.get(1)
						NextResIdx = 0
					else:
						M3 = tans.get(0).get('Reservoir_Level_M3')
						MWs = tans.get(0).get('MWs_per_CubicMetre')
						if CSafeList(CSafeNP.unique(MWs.getList())).len() > 1:
							Msg = 'A turbine below has variable efficiency. AutoCalc not possible.'
							NextResIdx = 0
						else:
							MWsPerM3 = CSafeList(CSafeNP.array(MWsPerM3.getList()) + MWs.get(0))
							NextResIdx = enginesTop.get(Idx.get(0)).OperatesTo
				else:
					NextResIdx = flows.get(Idx.get(0)).OperatesTo
		else:
			Msg = 'This case didn\'t created for now'
		if Msg == '':
			MWh = CSafeList()
			i = 0
			while (i < M30.len()):
				MWh.append(0)
				i = i + 1
			i = 1
			while (i < MWh.len()):
				MWh.set(i, MWh.get(i - 1) + (M30.get(i) - M30.get(i - 1)) * (MWsPerM3.get(i - 1) + MWsPerM3.get(i)) / 2 / 3600)
				i = i + 1
			A.set('CubicMetres', M30)
			A.set('MWh', MWh)
	ans = CSafeList()
	ans.append(A)
	ans.append(Msg)
	return ans

def interpolate(xx, yy, x, method='spline'):
	method = 'linear'
	return scipy.interpolate.interp1d(xx.getList(), yy.getList(), kind=method, fill_value='extrapolate')(x)

def renderCurrentReservoirLevelGraphFigure(value):
	global dataTables
	global getStandardOptionTypes, getTSValues, getMWh2M3, interpolate
	curChart = screenVariables.get('currentReservoirLevelGraphFigure')
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	MaxLevel = CSafeList()
	CurrentLevel = CSafeList()
	name = CSafeList()
	i = 0
	while (i < assets.len()):
		if assets.get(i).Shortname in value:
			if assets.get(i).Type == 2:
				OT = getStandardOptionTypes(assets.get(i).Option.TypeID)
				if not OT.Show.CurrentReservoirLevel:
					i = i + 1
					continue
			MaxLMWh = 0
			CurLMWh = 0
			j = 0
			while (j < assets.get(i).Topology.nRes):
				if assets.get(i).Topology.nRes == 1:
					reservoirs = CSafeList([assets.get(i).Reservoir])
				else:
					reservoirs = CSafeList(CSafeList(assets.get(i).Reservoir).get(0))
				tans = getTSValues(reservoirs.get(j).MaxLevelFile, 'Silent')
				if tans.get(3) != '':
					curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
									  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
					dataTables.set('currentReservoirLevel', {'headers': ['Current Level [GWh]', 'Maximum Level [GWh]'], 'rows': ['No common data available']})
					return curChart.getValue()
				MaxL = CSafeNP.max(tans.get(0).getList())
				Char = None
				if globalDict.get('hydroptModel').Status.Units == 2:
					Char = getMWh2M3(reservoirs.get(j).MWh2CubicMetresFile, assets.get(i), j, 'Silent')
					if Char.get(1) != '':
						curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
										  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
						dataTables.set('currentReservoirLevel', {'headers': ['Current Level [GWh]', 'Maximum Level [GWh]'], 'rows': ['No common data available']})
						return curChart.getValue()
					MaxLMWh = MaxLMWh + interpolate(Char.get(0).getDict().get('CubicMetres'), Char.get(0).getDict().get('MWh'), MaxL)
				else:
					MaxLMWh = MaxLMWh + MaxL
				if globalDict.get('hydroptModel').Status.UnitsOptimization == 2:
					if Char == None:
						Char = getMWh2M3(reservoirs.get(j).MWh2CubicMetresFile, assets.get(i), j, 'Silent')
						if Char.get(1) != '':
							curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
											  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
							dataTables.set('currentReservoirLevel', {'headers': ['Current Level [GWh]', 'Maximum Level [GWh]'], 'rows': ['No common data available']})
							return curChart.getValue()
					CurLMWh = CurLMWh + interpolate(Char.get(0).getDict().get('CubicMetres'), Char.get(0).getDict().get('MWh'), reservoirs.get(j).ScenarioWaterManager.StartLevel)
				else:
					CurLMWh = CurLMWh + reservoirs.get(j).ScenarioWaterManager.StartLevel
				j = j + 1
			MaxLevel.append(MaxLMWh)
			CurrentLevel.append(CurLMWh)
			name.append(assets.get(i).Shortname)
		i = i + 1
	CurrentLevelSort = CSafeList()
	i = 0
	while (i < CurrentLevel.len()):
		CurrentLevelSort.append([CurrentLevel.get(i), i])
		i = i + 1
	CurrentLevelSort.sortKey(0, desc=True)
	CurrentLevels = CSafeList()
	MaxLevels = CSafeList()
	names = CSafeList()
	i = 0
	while (i < CurrentLevel.len()):
		CurrentLevels.append(CurrentLevel.get(CSafeList(CurrentLevelSort.get(i)).get(1)) / 1000.0)
		MaxLevels.append(MaxLevel.get(CSafeList(CurrentLevelSort.get(i)).get(1)) / 1000.0)
		names.append(name.get(CSafeList(CurrentLevelSort.get(i)).get(1)))
		i = i + 1
	if MaxLevels.len() == 0:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('currentReservoirLevel', {'headers': ['Current Level [GWh]', 'Maximum Level [GWh]'], 'rows': ['No common data available']})
	else:
		MaxLevelDelta = CSafeList(CSafeNP.array(MaxLevels.getList()) - CSafeNP.array(CurrentLevels.getList()))
		MaxLevelG = CSafeList()
		CurrentLevelG = CSafeList()
		i = 0
		while (i < CurrentLevels.len()):
			MaxLevelG.append([MaxLevelDelta.get(i)])
			CurrentLevelG.append([CurrentLevels.get(i)])
			i = i + 1
		curChart.setChart(rows=[CurrentLevelG.getList(), MaxLevelG.getList()], headers=['Current Level', 'Max Level'], rowCaptions=names.getList(), title='',
						  type='bar', barmode='stack', style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='name', error={})
		dataTables.set('currentReservoirLevel', {'headers': ['Asset', 'Current Level [GWh]', 'Maximum Level [GWh]'], 'rows': [CurrentLevelG.getList(), MaxLevelG.getList()], 'titles': names.getList()})
	return curChart.getValue()

def renderEnergyPlanningPeakGraphFigure(value):
	global dataTables
	global getStandardOptionTypes, getTSValues, getMWh2M3, interpolate
	curChart = screenVariables.get('energyPlanningPeakGraphFigure')
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	TMax = 1000000007
	TMin = -1000000007
	ShowErr = 1
	RunTime = CSafeList()
	Show = CSafeList()
	i = 0
	try:
		while (i < assets.len()):
			if assets.get(i).Shortname in value:
				RunTime.append(assets.get(i).ScenarioWaterManager.Result.RunTime)
				Show.append(1)
			i = i + 1
	except:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('energyPlanningPeak', {'headers': ['Off Peak [GWh]', 'Peak [GWh]'], 'rows': ['No common data available']})
		return curChart.getValue()
	if Show.len() == 0:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('energyPlanningPeak', {'headers': ['Off Peak [GWh]', 'Peak [GWh]'], 'rows': ['No common data available']})
		return curChart.getValue()
	if CSafeList(CSafeNP.unique(RunTime)).len() > 1:
		ShowErr = 0
	else:
		MonthlyEnergyPeak = 0
		MonthlyEnergyOffPeak = 0
	i = 0
	it = 0
	try:
		while (i < assets.len()):
			if assets.get(i).Shortname in value:
				if assets.get(i).Type == 2:
					OT = getStandardOptionTypes(assets.get(i).Option.TypeID)
					if not OT.Show.EnergyPlanning:
						i = i + 1
						Show.set(it, 0)
						continue
				T = CSafeList(CSafeList(assets.get(i).ScenarioWaterManager.Result.DateNum).get(0))
				if T.get(-1) < TMax:
					TMax = T.get(-1)
				if T.get(0) > TMin:
					TMin = T.get(0)
				it = it + 1
			i = i + 1
	except:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('energyPlanningPeak', {'headers': ['Off Peak [GWh]', 'Peak [GWh]'], 'rows': ['No common data available']})
		return curChart.getValue()
	TMWSum = CSafeList()
	i = 0
	it = 0
	pos = -1
	try:
		while (i < assets.len()):
			if assets.get(i).Shortname in value:
				pos = i
				if Show.get(it) == 1:
					T = CSafeList(CSafeList(assets.get(i).ScenarioWaterManager.Result.DateNum).get(0))
					TMinIdx = CSafeNP.whereTime(T.getList(), TMin)
					TMaxIdx = CSafeNP.whereTime(T.getList(), TMax)
					TMW = CSafeList()
					if assets.get(i).Topology.nTurbines + assets.get(i).Topology.nPumps == 1:
						engines = CSafeList([assets.get(i).Engine])
					else:
						engines = CSafeList(CSafeList(assets.get(i).Engine).get(0))
					j = 0
					while (j < assets.get(i).Topology.nTurbines + assets.get(i).Topology.nPumps):
						operation = CSafeNP.transpose(engines.get(j).ScenarioWaterManager.Result.Operation)
						TMW.append(CSafeNP.array(CSafeList(operation).slice(TMinIdx, TMaxIdx + 1)))
						j = j + 1
					TMWSum.append(CSafeNP.sum(CSafeNP.array(TMW.getList()), axis=0))
					if ShowErr == 1:
						MonthlyEnergyPeak = CSafeNP.array(MonthlyEnergyPeak) + CSafeNP.array(assets.get(i).ScenarioWaterManager.Result.MonthlyEnergyPeak)
						MonthlyEnergyOffPeak = CSafeNP.array(MonthlyEnergyOffPeak) + CSafeNP.array(assets.get(i).ScenarioWaterManager.Result.MonthlyEnergyOffPeak)
				it = it + 1
			i = i + 1
	except:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('energyPlanningPeak', {'headers': ['Off Peak [GWh]', 'Peak [GWh]'], 'rows': ['No common data available']})
		return curChart.getValue()
	E = CSafeList(CSafeList(CSafeNP.sum(CSafeNP.array(TMWSum.getList()), axis=0)).get(0))
	t = CSafeList(CSafeList(CSafeList(assets.get(pos).ScenarioWaterManager.Result.DateNum).get(0)).slice(TMinIdx, TMaxIdx + 1))
	i = 0
	PeakProfile = CSafeList()
	while (i < t.len()):
		date = datetime.fromordinal(int(t.get(i)) - 366)
		if t.get(i) % 1 > 8.0 / 24.0 and t.get(i) % 1 < 20.0 / 24.0 and date.weekday() != 5 and date.weekday() != 6:
			PeakProfile.append(1)
		else:
			PeakProfile.append(0)
		i = i + 1
	EPeak = CSafeList(CSafeNP.array(E.getList()) * CSafeNP.array(PeakProfile.getList()))
	EOffPeak = CSafeList(CSafeNP.array(E.getList()) - CSafeNP.array(EPeak.getList()))
	i = 0
	it = 0
	EP = CSafeList()
	EO = CSafeList()
	tDisp = CSafeList()
	i = 0
	tDisp.append(t.get(0))
	EP.append(0)
	EO.append(0)
	while (i < EPeak.len()):
		if i > 0 and not (datetime.fromordinal(int(t.get(i)) - 366).year == datetime.fromordinal(int(t.get(i - 1)) - 366).year and datetime.fromordinal(int(t.get(i)) - 366).month == datetime.fromordinal(int(t.get(i - 1)) - 366).month):
			it = it + 1
			tDisp.append(t.get(i))
			EP.append(0)
			EO.append(0)
		EP.set(it, EP.get(it) + EPeak.get(i))
		EO.set(it, EO.get(it) + EOffPeak.get(i))
		i = i + 1
	if ShowErr == 1:
		n = CSafeList(CSafeNP.shape(CSafeNP.array(MonthlyEnergyPeak))).get(1)
		MonthlyEnergyPeak = CSafeNP.sort(MonthlyEnergyPeak, axis=1)
		MonthlyEnergyOffPeak = CSafeNP.sort(MonthlyEnergyOffPeak, axis=1)
		quantile = max(1, int(round(n * 0.05)))
		i = 0
		EBLowPeak = CSafeNP.array(EP.getList())
		EBUpPeak = -1 * CSafeNP.array(EP.getList())
		EBLowOffPeak = CSafeNP.array(EO.getList())
		EBUpOffPeak = -CSafeNP.array(EO.getList())
		while (i < quantile):
			EBLowPeak = EBLowPeak - CSafeNP.transpose(CSafeNP.getColumn(MonthlyEnergyPeak, i))
			EBUpPeak = EBUpPeak + CSafeNP.transpose(CSafeNP.getColumn(MonthlyEnergyPeak, -i - 1))
			EBLowOffPeak = EBLowOffPeak - CSafeNP.transpose(CSafeNP.getColumn(MonthlyEnergyOffPeak, i))
			EBUpOffPeak = EBUpOffPeak + CSafeNP.transpose(CSafeNP.getColumn(MonthlyEnergyOffPeak, -i - 1))
			i = i + 1
		EBLowPeak = EBLowPeak / 1000.0
		EBUpPeak = EBUpPeak / 1000.0
		EBLowOffPeak = EBLowOffPeak / 1000.0
		EBUpOffPeak = EBUpOffPeak / 1000.0
	EP = CSafeList(CSafeNP.array(EP.getList()) / 1000)
	EO = CSafeList(CSafeNP.array(EO.getList()) / 1000)
	if tDisp.len() == 1:
		ShowErr = 0
		XDataPeak = CSafeList(tDisp.get(0))
		tListY1 = CSafeList()
		tListY2 = CSafeList()
		i = 0
		while (i < EP.len()):
			tListY1.append([EP.get(i)])
			i = i + 1
		i = 0
		while (i < EO.len()):
			tListY2.append([EO.get(i)])
			i = i + 1
		times = CSafeList()
		i = 0
		while (i < XDataPeak.len()):
			times.append(datetime.fromordinal(int(round(XDataPeak.get(i))) - 366).strftime("%Y-%m-%d %H:%M:%S"))
			i = i + 1
		times = pd.to_datetime(times.getList())
		curChart.setChart(rows=[tListY1.getList(), tListY2.getList()], headers=['Peak', 'Off Peak'], rowCaptions=times, title='',
						  type='bar', barmode='group', style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='name', error={})
		dataTables.set('energyPlanningPeak', {'headers': ['Time', 'Off Peak [GWh]', 'Peak [GWh]'], 'rows': [tListY2.getList(), tListY1.getList()], 'titles': times})
	else:
		XDataPeak = CSafeList(tDisp.getList())
		tListY1 = CSafeList()
		tListY2 = CSafeList()
		i = 0
		while (i < EP.len()):
			tListY1.append([EP.get(i)])
			i = i + 1
		i = 0
		while (i < EO.len()):
			tListY2.append([EO.get(i)])
			i = i + 1
		errorbar = CSafeDict({})
		if ShowErr == 1:
			tListMinus = CSafeNP.concatenate(EBLowPeak, EBLowOffPeak)
			tListPlus = CSafeNP.concatenate(EBUpPeak, EBUpOffPeak)
			errorbar.set('type', 'data')
			errorbar.set('visible', True)
			errorbar.set('array', tListPlus)
			errorbar.set('arrayminus', tListMinus)
		times = CSafeList()
		i = 0
		while (i < XDataPeak.len()):
			times.append(datetime.fromordinal(int(round(XDataPeak.get(i))) - 366).strftime("%Y-%m-%d %H:%M:%S"))
			i = i + 1
		times = pd.to_datetime(times.getList())
		curChart.setChart(rows=[tListY1.getList(), tListY2.getList()], headers=['Peak', 'Off Peak'], rowCaptions=times, title='',
						  type='bar', barmode='group', style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='name', error=errorbar.getDict())
		dataTables.set('energyPlanningPeak', {'headers': ['Time', 'Off Peak [GWh]', 'Peak [GWh]'], 'rows': [tListY2.getList(), tListY1.getList()], 'titles': times})
	return curChart.getValue()

def renderPowerPlanningGraphFigure(value):
	global dataTables
	global getHydroptTime, getStandardOptionTypes, getTSValues
	curChart = screenVariables.get('powerPlanningGraphFigure')
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	TMax = 1000000007
	TMin = -1000000007
	delta = datetime.now() - datetime(1, 1, 1)
	ShowStart = math.floor(math.floor(float(delta.days) + (float(delta.seconds) / 86400) + 367))
	ShowEnd = ShowStart + 365 - 1.0 / 24.0
	t = getHydroptTime(ShowStart, ShowEnd)
	B = CSafeList()
	i = 0
	Count = 1
	i = 0
	while (i < assets.len()):
		if assets.get(i).Shortname in value:
			if assets.get(i).Type == 2:
				OT = getStandardOptionTypes(assets.get(i).Option.TypeID)
				if not OT.Show.PowerPlanning:
					i = i + 1
					continue
			j = 0
			if assets.get(i).Topology.nTurbines + assets.get(i).Topology.nPumps == 1:
				engines = CSafeList([assets.get(i).Engine])
			else:
				engines = CSafeList(CSafeList(assets.get(i).Engine).get(0))
			while (j < assets.get(i).Topology.nTurbines):
				tans = getTSValues(engines.get(j).MaxFlowFile, ShowStart, ShowEnd, 'Silent')
				RevPlan = tans.get(0)
				Dummy = tans.get(1)
				MaxEnd = tans.get(2)
				if tans.get(3) != '':
					curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
									  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
					dataTables.set('powerPlanning', {'headers': ['Power Planning [MW]'], 'rows': ['No common data available']})
					return curChart.getValue()
				if RevPlan.len() == 0:
					ShowEnd = MaxEnd
					tans = getTSValues(engines.get(j).MaxFlowFile, ShowStart, ShowEnd, 'Silent')
					RevPlan = tans.get(0)
					if tans.get(3) != '':
						curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
										  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
						dataTables.set('powerPlanning', {'headers': ['Power Planning [MW]'], 'rows': ['No common data available']})
						return curChart.getValue()
					if B.len() > 0:
						B = CSafeList(CSafeNP.getColumns(B.getList(), 0, RevPlan.len()))
					t = t.slice(0, RevPlan.len())
				B.append(CSafeNP.array(RevPlan.getList()))
				if assets.get(i).Type == 2:
					Opt = assets.get(i).Option
					ContractStart = datetime.toordinal(datetime(year=Opt.StartYear, month=Opt.StartMonth, day=Opt.StartDay)) + 366
					ContractEnd = datetime.toordinal(datetime(year=Opt.EndYear, month=Opt.EndMonth, day=Opt.EndDay)) + 366
					ContractStartIdx = CSafeNP.whereTime(t.getList(), ContractStart)
					ContractEndIdx = CSafeNP.whereTime(t.getList(), ContractEnd)
					temp = CSafeList(B.get(-1))
					if ContractStartIdx != -1:
						k = 0
						while (k < ContractStartIdx):
							temp.set(k, 0)
							k = k + 1
					if ContractEndIdx != -1:
						k = ContractEndIdx + 1
						while (k < temp.len()):
							temp.set(k, 0)
							k = k + 1
					if ContractStart > t.get(-1) or ContractEnd < t.get(0):
						k = 0
						while (k < temp.len()):
							temp.set(k, 0)
							k = k + 1
					B.set(-1, CSafeNP.array(temp.getList()))
				Count = Count + 1
				j = j + 1
		i = i + 1
	if B.len() == 0:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('powerPlanning', {'headers': ['Power Planning [MW]'], 'rows': ['No common data available']})
		return curChart.getValue()
	B = CSafeNP.sum(CSafeNP.array(B.getList()), axis=0)
	times = dateUtils.date_range_from_matlab(t.get(0), t.get(-1) + 1)
	curChart.setChart(rows=[B], headers=['Power Planning'], rowCaptions=times, title='', type='line', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='y+name', error={})
	dataTables.set('powerPlanning', {'headers': ['Time', 'Power Planning [MW]'], 'rows': [B], 'titles': times})
	return curChart.getValue()

def renderReservoirCycleGraphFigure(value):
	global dataTables
	global getHydroptTime, getStandardOptionTypes
	curChart = screenVariables.get('powerPlanningGraphFigure')
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	TMax = 1000000007
	TMin = -1000000007
	ShowEnv = 1
	RunTime = CSafeList()
	Show = CSafeList()
	i = 0
	try:
		while (i < assets.len()):
			if assets.get(i).Shortname in value:
				RunTime.append(assets.get(i).ScenarioWaterManager.Result.RunTime)
				Show.append(1)
			i = i + 1
	except:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('reservoirCycle', {'headers': ['Reservoir Cycle [GWh]', '95% envelope[GWh]', '5% envelope [GWh]'],
						'rows': ['No common data available']})
		return curChart.getValue()
	if RunTime.len() == 0:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('reservoirCycle', {'headers': ['Reservoir Cycle [GWh]', '95% envelope[GWh]', '5% envelope [GWh]'], 'rows': ['No common data available']})
		return curChart.getValue()
	if CSafeList(CSafeNP.unique(RunTime.len())).len() != 1:
		ShowEnv = 0
	i = 0
	it = 0
	try:
		while (i < assets.len()):
			if assets.get(i).Shortname in value:
				if assets.get(i).Type == 2:
					OT = getStandardOptionTypes(assets.get(i).Option.TypeID)
					if not OT.Show.ReservoirCycle:
						i = i + 1
						Show.set(it, 0)
						continue
				T = CSafeList(CSafeList(lst=assets.get(i).ScenarioWaterManager.Result.DateNum).get(0))
				if T.get(-1) < TMax:
					TMax = T.get(-1)
				if T.get(0) > TMin:
					TMin = T.get(0)
				it = it + 1
			i = i + 1
	except:
		curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No common data available', type='bar', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
		dataTables.set('reservoirCycle', {'headers': ['Reservoir Cycle [GWh]', '95% envelope[GWh]', '5% envelope [GWh]'], 'rows': ['No common data available']})
		return curChart.getValue()
	EnvRes = 0
	Count = 1
	i = 0
	it = 0
	R = CSafeList()
	lst = 0
	while (i < assets.len()):
		if assets.get(i).Shortname in value:
			lst = i
			if Show.get(it) == 1:
				T = CSafeList(CSafeList(lst=assets.get(i).ScenarioWaterManager.Result.DateNum).get(0))
				TMinIdx = CSafeNP.whereTime(T.getList(), TMin)
				TMaxIdx = CSafeNP.whereTime(T.getList(), TMax)
				if assets.get(i).Topology.nRes == 1:
					reservoirs = CSafeList([assets.get(i).Reservoir])
				else:
					reservoirs = CSafeList(CSafeList(assets.get(i).Reservoir).get(0))
				j = 0
				RLev = CSafeList()
				while (j < reservoirs.len()):
					levels = CSafeList(reservoirs.get(j).ScenarioWaterManager.Result.Level)
					RLev.append(CSafeNP.array(levels.slice(TMinIdx, TMaxIdx + 1)))
					if ShowEnv == 1:
						EnvRes = EnvRes + CSafeNP.array(reservoirs.get(j).ScenarioWaterManager.Result.RCoarse)
					j = j + 1
				R.append(CSafeNP.sum(RLev.getList(), axis=0))
				Count = Count + 1
			it = it + 1
		i = i + 1
	R = CSafeList(CSafeNP.sum(R.getList(), axis=0) / 1000.0)
	t = getHydroptTime(TMin, TMax)
	if ShowEnv == 1:
		CoarseTime = assets.get(lst).ScenarioWaterManager.Result.CoarseTime
		CoarseTime = CSafeNP.concatenate(CSafeNP.array(t.get(0)), CSafeNP.array(CoarseTime))
		CoarseTime = CSafeList(CSafeNP.concatenate(CSafeNP.array(CoarseTime), CSafeNP.array(t.get(-1))))
		n = CSafeList(CSafeNP.shape(EnvRes)).get(1)
		EnvRes = CSafeNP.sort(EnvRes, axis=1) / 1000.0
		quantile = max(1, int(round(n * 0.05)))
		EnvResFive = CSafeNP.concatenate(CSafeNP.array(R.get(0)), CSafeNP.getColumn(EnvRes, quantile - 1))
		EnvResFive = CSafeList(CSafeNP.concatenate(EnvResFive, CSafeNP.array(R.get(-1))))
		EnvResNinetyFive = CSafeNP.concatenate(CSafeNP.array(R.get(0)), CSafeNP.getColumn(EnvRes, n - quantile))
		EnvResNinetyFive = CSafeList(CSafeNP.concatenate(EnvResNinetyFive, CSafeNP.array(R.get(-1))))
		EnvResFive = scipy.interpolate.interp1d(CoarseTime.getList(), EnvResFive.getList(), 'cubic')(t.getList())
		EnvResNinetyFive = scipy.interpolate.interp1d(CoarseTime.getList(), EnvResNinetyFive.getList(), 'cubic')(t.getList())
		### TODO: add two more graphs!
	times = dateUtils.date_range_from_matlab(TMin, TMax + 1)
	curChart.setChart(rows=[R.getList()], headers=['Reservoir Cycle'], rowCaptions=times, title='', type='line', barmode='group',
						  style={'width': '450', 'height': '300'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
	dataTables.set('reservoirCycle', {'headers': ['Time', 'Reservoir Cycle [GWh]', '95% envelope[GWh]', '5% envelope [GWh]'], 'rows': [R.getList(), EnvResFive, EnvResNinetyFive], 'titles': times})
	return curChart.getValue()

def renderStartDate(value):
	i = 0
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	lst = -1
	mi = 0
	ma = 0
	was = False
	try:
		while i < assets.len():
			if assets.get(i).Shortname in value:
				lst = i
				if was == False:
					ma = assets.get(i).ScenarioWaterManager.Result.RunTime
					mi = assets.get(i).ScenarioWaterManager.Result.RunTime
					was = True
				if assets.get(i).ScenarioWaterManager.Result.RunTime > ma:
					ma = assets.get(i).ScenarioWaterManager.Result.RunTime
				if assets.get(i).ScenarioWaterManager.Result.RunTime < mi:
					mi = assets.get(i).ScenarioWaterManager.Result.RunTime
			i = i + 1
	except:
		return ''
	if ma != mi or lst == -1:
		return ''
	dates = CSafeList(CSafeList(lst=assets.get(lst).ScenarioWaterManager.Result.DateNum).get(0))
	return dateUtils.to_str(dateUtils.from_matlab(dates.get(0)))

def renderEndDate(value):
	i = 0
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	lst = -1
	mi = 0
	ma = 0
	was = False
	try:
		while i < assets.len():
			if assets.get(i).Shortname in value:
				lst = i
				if was == False:
					ma = assets.get(i).ScenarioWaterManager.Result.RunTime
					mi = assets.get(i).ScenarioWaterManager.Result.RunTime
					was = True
				if assets.get(i).ScenarioWaterManager.Result.RunTime > ma:
					ma = assets.get(i).ScenarioWaterManager.Result.RunTime
				if assets.get(i).ScenarioWaterManager.Result.RunTime < mi:
					mi = assets.get(i).ScenarioWaterManager.Result.RunTime
			i = i + 1
	except:
		return ''
	if ma != mi or lst == -1:
		return ''
	dates = CSafeList(CSafeList(lst=assets.get(lst).ScenarioWaterManager.Result.DateNum).get(0))
	return dateUtils.to_str(dateUtils.from_matlab(dates.get(dates.len() - 1)))

def renderAverageRevenue(value):
	i = 0
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	idx = -1
	mi = 0
	ma = 0
	was = False
	Rev = CSafeList()
	try:
		while i < assets.len():
			if assets.get(i).Shortname in value:
				if was == False:
					ma = assets.get(i).ScenarioWaterManager.Result.RunTime
					mi = assets.get(i).ScenarioWaterManager.Result.RunTime
					was = True
					idx = i
				if assets.get(i).ScenarioWaterManager.Result.RunTime > ma:
					ma = assets.get(i).ScenarioWaterManager.Result.RunTime
				if assets.get(i).ScenarioWaterManager.Result.RunTime < mi:
					mi = assets.get(i).ScenarioWaterManager.Result.RunTime
			i = i + 1
	except:
		return ''
	if ma != mi or was == False:
		return ''
	R = assets.get(idx).ScenarioWaterManager.Result
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
	return CSafeNP.format(CSafeNP.mean(Rev), '{:.2f} Mio. EUR')

def renderMinimumRevenue(value):
	i = 0
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	idx = -1
	mi = 0
	ma = 0
	was = False
	Rev = CSafeList()
	try:
		while i < assets.len():
			if assets.get(i).Shortname in value:
				if was == False:
					ma = assets.get(i).ScenarioWaterManager.Result.RunTime
					mi = assets.get(i).ScenarioWaterManager.Result.RunTime
					was = True
					idx = i
				if assets.get(i).ScenarioWaterManager.Result.RunTime > ma:
					ma = assets.get(i).ScenarioWaterManager.Result.RunTime
				if assets.get(i).ScenarioWaterManager.Result.RunTime < mi:
					mi = assets.get(i).ScenarioWaterManager.Result.RunTime
			i = i + 1
	except:
		return ''
	if ma != mi or was == False:
		return ''
	R = assets.get(idx).ScenarioWaterManager.Result
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
	###TODO: ask Christoph what is happening here
	return CSafeNP.format(CSafeNP.min(Rev), '{:.2f} Mio. EUR')

def updateChecked(value, style):
	i = 0
	data = CSafeList(globalDict.get('hydroptModel').Asset)
	if globalDict.get('hydroptModel').nAssets == 1:
		assets = CSafeList([globalDict.get('hydroptModel').Asset])
	else:
		assets = CSafeList(lst=data.get(0))
	while i < assets.len():
		if assets.get(i).Shortname in value:
			octave.eval('Data.Asset('+str(i+1)+').MainFig.Check = 1;')
		else:
			octave.eval('Data.Asset('+str(i+1)+').MainFig.Check = 0;')
		i = i + 1
	globalDict.set('hydroptModel', octave.pull('Data'))
	return style

def buildLink(rows):
	df = pd.DataFrame.from_dict(rows)
	csv_string = df.to_csv(index=False, encoding='utf-8')
	csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
	return csv_string