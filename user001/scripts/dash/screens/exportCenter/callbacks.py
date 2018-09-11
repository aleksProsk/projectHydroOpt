def updateAggregated(value):
    if value == 'Aggregated':
        octave.eval('Data.Export.Aggregated = 1.0;')
        octave.eval('Data.Export.Separated = 0.0;')
    else:
        octave.eval('Data.Export.Aggregated = 0.0;')
        octave.eval('Data.Export.Separated = 1.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select type'

def updateModuleSelector(value):
    if value == 'Scheduler':
        octave.eval('Data.Export.Scheduler = 1.0;')
        octave.eval('Data.Export.ScenarioWaterMgt = 0.0;')
    else:
        octave.eval('Data.Export.Scheduler = 0.0;')
        octave.eval('Data.Export.ScenarioWaterMgt = 1.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select module'

def updateFileFormat(value):
    if value == 'Excel':
        octave.eval('Data.Export.Excel = 1.0;')
        octave.eval('Data.Export.CSV = 0.0;')
        octave.eval('Data.Export.MAT = 0.0;')
    elif value == 'CSV':
        octave.eval('Data.Export.Excel = 0.0;')
        octave.eval('Data.Export.CSV = 1.0;')
        octave.eval('Data.Export.MAT = 0.0;')
    else:
        octave.eval('Data.Export.Excel = 0.0;')
        octave.eval('Data.Export.CSV = 0.0;')
        octave.eval('Data.Export.MAT = 1.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select file format'

def updateDatePicker(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    octave.eval('Data.Export.StartYear = '+str(start_date.year) + ';')
    octave.eval('Data.Export.StartMonth = '+str(start_date.month) + ';')
    octave.eval('Data.Export.StartDay = '+str(start_date.day) + ';')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    octave.eval('Data.Export.EndYear = '+str(end_date.year) + ';')
    octave.eval('Data.Export.EndMonth = '+str(end_date.month) + ';')
    octave.eval('Data.Export.EndDay = '+str(end_date.day) + ';')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return False

def updateResolutionMeanResults(value):
    if value == 'hourly':
        octave.eval('Data.Export.hourly = 1.0;')
        octave.eval('Data.Export.daily = 0.0;')
        octave.eval('Data.Export.weekly = 0.0;')
        octave.eval('Data.Export.monthly = 0.0;')
    elif value == 'daily':
        octave.eval('Data.Export.hourly = 0.0;')
        octave.eval('Data.Export.daily = 1.0;')
        octave.eval('Data.Export.weekly = 0.0;')
        octave.eval('Data.Export.monthly = 0.0;')
    elif value == 'weekly':
        octave.eval('Data.Export.hourly = 0.0;')
        octave.eval('Data.Export.daily = 0.0;')
        octave.eval('Data.Export.weekly = 1.0;')
        octave.eval('Data.Export.monthly = 0.0;')
    else:
        octave.eval('Data.Export.hourly = 0.0;')
        octave.eval('Data.Export.daily = 0.0;')
        octave.eval('Data.Export.weekly = 0.0;')
        octave.eval('Data.Export.monthly = 1.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select resolution'

def updateTimeSeries(value):
    if 'Reservoir Level' in value:
        octave.eval('Data.Export.ReservoirLevel = 1.0;')
    else:
        octave.eval('Data.Export.ReservoirLevel = 0.0;')
    if 'Inflow' in value:
        octave.eval('Data.Export.Inflow = 1.0;')
    else:
        octave.eval('Data.Export.Inflow = 0.0;')
    if 'Spill' in value:
        octave.eval('Data.Export.Spill = 1.0;')
    else:
        octave.eval('Data.Export.Spill = 0.0;')
    if 'Flow' in value:
        octave.eval('Data.Export.Flow = 1.0;')
    else:
        octave.eval('Data.Export.Flow = 0.0;')
    if 'Infiltration Loss' in value:
        octave.eval('Data.Export.InfiltrationLoss = 1.0;')
    else:
        octave.eval('Data.Export.InfiltrationLoss = 0.0;')
    if 'Turbine Operation' in value:
        octave.eval('Data.Export.Turbine = 1.0;')
    else:
        octave.eval('Data.Export.Turbine = 0.0;')
    if 'Pump Operation' in value:
        octave.eval('Data.Export.Pump = 1.0;')
    else:
        octave.eval('Data.Export.Pump = 0.0;')
    if 'Market Price' in value:
        octave.eval('Data.Export.Price = 1.0;')
    else:
        octave.eval('Data.Export.Price = 0.0;')
    if 'Margin Price' in value:
        octave.eval('Data.Export.MarginPriceTS = 1.0;')
    else:
        octave.eval('Data.Export.MarginPriceTS = 0.0;')
    if 'Water Value' in value:
        octave.eval('Data.Export.WaterValueTS = 1.0;')
    else:
        octave.eval('Data.Export.WaterValueTS = 0.0;')
    if 'Reservoir constraints' in value:
        octave.eval('Data.Export.ReservoirConstraints = 1.0;')
    else:
        octave.eval('Data.Export.ReservoirConstraints = 0.0;')
    if 'Engine constraints' in value:
        octave.eval('Data.Export.EngineConstraints = 1.0;')
    else:
        octave.eval('Data.Export.EngineConstraints = 0.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select'

def updateResultsPerScenario(value):
    if 'Margin Prices' in value:
        octave.eval('Data.Export.MarginPrices = 1.0;')
    else:
        octave.eval('Data.Export.MarginPrices = 0.0;')
    if 'Water Values' in value:
        octave.eval('Data.Export.WaterValues = 1.0;')
    else:
        octave.eval('Data.Export.WaterValues = 0.0;')
    if 'Revenue/Energy' in value:
        octave.eval('Data.Export.Revenues = 1.0;')
    else:
        octave.eval('Data.Export.Revenues = 0.0;')
    if 'Revenue/Energy monthly' in value:
        octave.eval('Data.Export.RevenuesMonthly = 1.0;')
    else:
        octave.eval('Data.Export.RevenuesMonthly = 0.0;')
    if 'Revenue/Energy per Engine' in value:
        octave.eval('Data.Export.RevenuesEngine = 1.0;')
    else:
        octave.eval('Data.Export.RevenuesEngine = 0.0;')
    if 'Revenue/Energy full detail' in value:
        octave.eval('Data.Export.RevenuesEngineMonthly = 1.0;')
    else:
        octave.eval('Data.Export.RevenuesEngineMonthly = 0.0;')
    if 'Reservoir Usage' in value:
        octave.eval('Data.Export.ReservoirUsage = 1.0;')
    else:
        octave.eval('Data.Export.ReservoirUsage = 0.0;')
    if 'Reserve Revenue' in value:
        octave.eval('Data.Export.ReserveRevenues = 1.0;')
    else:
        octave.eval('Data.Export.ReserveRevenues = 0.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select'

def updateTimeSeriesOptions(value1, value2):
    tempLst = CSafeList()
    tempLst.append({'label': 'Reservoir Level', 'value': 'Reservoir Level',})
    tempLst.append({'label': 'Inflow', 'value': 'Inflow',})
    tempLst.append({'label': 'Spill', 'value': 'Spill',})
    tempLst.append({'label': 'Flow', 'value': 'Flow',})
    tempLst.append({'label': 'Infiltration Loss', 'value': 'Infiltration Loss',})
    tempLst.append({'label': 'Turbine Operation', 'value': 'Turbine Operation',})
    tempLst.append({'label': 'Pump Operation', 'value': 'Pump Operation',})
    tempLst.append({'label': 'Market Price', 'value': 'Market Price',})
    if value1 == 'Separated':
        if value2 == 'Excel':
            tempLst.append({'label': 'Margin Price', 'value': 'Margin Price',})
            tempLst.append({'label': 'Water Value', 'value': 'Water Value',})
        elif value2 == 'MAT':
            tempLst.append({'label': 'Margin Price', 'value': 'Margin Price',})
            tempLst.append({'label': 'Water Value', 'value': 'Water Value',})
            tempLst.append({'label': 'Reservoir constraints', 'value': 'Reservoir constraints',})
            tempLst.append({'label': 'Engine constraints', 'value': 'Engine constraints',})
    return tempLst.getList()

def updateDropdownValue(options, value):
    options = CSafeList(options)
    optionValues = CSafeList()
    i = 0
    while (i < options.len()):
        tDict = CSafeDict(options.get(i))
        optionValues.append(tDict.get('value'))
        i = i + 1
    optionValues = optionValues.getList()
    value = CSafeList(value)
    newValue = CSafeList()
    i = 0
    while (i < value.len()):
        if value.get(i) in optionValues:
            newValue.append(value.get(i))
        i = i + 1
    return newValue.getList()

def updateResultsPerScenarioOptions(value1, value2):
    tempLst = CSafeList()
    if value1 == 'Separated':
        if value2 != 'CSV':
            tempLst.append({'label': 'Margin Prices', 'value': 'Margin Prices',})
            tempLst.append({'label': 'Water Values', 'value': 'Water Values',})
            tempLst.append({'label': 'Revenue/Energy', 'value': 'Revenue/Energy',})
            tempLst.append({'label': 'Revenue/Energy monthly', 'value': 'Revenue/Energy monthly',})
            tempLst.append({'label': 'Revenue/Energy per Engine', 'value': 'Revenue/Energy per Engine',})
            tempLst.append({'label': 'Revenue/Energy full detail', 'value': 'Revenue/Energy full detail',})
            tempLst.append({'label': 'Reservoir Usage', 'value': 'Reservoir Usage',})
    return tempLst.getList()

def updateUnit(value):
    if value == 'MWh':
        octave.eval('Data.Export.MWh = 1.0;')
    else:
        octave.eval('Data.Export.MWh = 0.0;')
    if value == 'm3':
        octave.eval('Data.Export.M3 = 1.0;')
    else:
        octave.eval('Data.Export.M3 = 0.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select unit type'

def updateFormat(value):
    if value == 'Autoformat':
        octave.eval('Data.Export.Autoformat = 1.0;')
    else:
        octave.eval('Data.Export.Autoformat = 0.0;')
    if value == 'Round':
        octave.eval('Data.Export.Round = 1.0;')
    else:
        octave.eval('Data.Export.Round = 0.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select format'

def updateExportCheck(values):
    data = CSafeList(globalDict.get('hydroptModel').Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    i = 0
    while (i < assets.len()):
        if assets.get(i).Shortname in values:
            octave.eval("Data.Asset("+str(i+1)+").Export.Check=1;")
        else:
            octave.eval("Data.Asset("+str(i+1)+").Export.Check=0;")
        i = i + 1
    globalDict.set('hydroptModel', octave.pull('Data'))
    return ''

def export(n_clicks):
    octave.eval("addpath('matlab/');")
    octave.eval('export(Data)')
    return ''

def updateFolderName(value):
    octave.eval("Data.Export.ExportFolder='"+value+"';")
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select folder'

def updateFileName(value):
    octave.eval("Data.Export.Filename='"+value+"';")
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select file name'