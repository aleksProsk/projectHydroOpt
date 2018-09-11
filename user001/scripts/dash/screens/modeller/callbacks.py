def loadModal(n0, n1, oldStyle):
    if n0 is None:
        n0 = 0
    if n1 is None:
        n1= 0
    style = CSafeDict(oldStyle)
    if n0 > n1:
        style.set('display', 'block')
    else:
        style.set('display', 'none')
    return style.getDict()

def loadModal1(n0, n1, oldStyle):
    if n0 is None:
        n0 = 0
    if n1 is None:
        n1 = 0
    style = CSafeDict(oldStyle)
    if n0 > n1:
        style.set('display', 'block')
    else:
        style.set('display', 'none')
    return style.getDict()

def buildModalGraph(n0, fig):
	newFig = CSafeFigure(figure=fig)
	newFig.scale(1.4)
	return newFig.getFigure()

dataTables = CSafeDict({})

def buildModalTable(n0):
    global dataTables
    if dataTables.contains('chart'):
        tempDF = CSafeDF()
        curDict = CSafeDict(dataTables.get('chart'))
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
    return []

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

lst = [-1, -1, -1]

def renderPriceChart(value, start_date, end_date):
    cur = [value, start_date, end_date]
    global getDateSelectors, getTSValues, lst
    #CSafeMatlab.setField(globalDict.get('hydroptModel').Price, 'ExpectedSpotPriceFile', value)
    octave.eval('Data.Price.ExpectedSpotPriceFile = "' + value + '";')
    globalDict.set('hydroptModel', octave.pull('Data'))
    curChart = screenVariables.get('priceChart')
    if lst == cur:
        lst = cur
        return curChart.getValue()
    lst = cur
    data = CSafeList(globalDict.get('hydroptModel').Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    val = CSafeList()
    ### TODO: add actual data to val
    val.append(1)
    val.append(0)
    InputType = CSafeNP.where(val.getList(), 1) + 1
    Start = datetime.toordinal(datetime.strptime(start_date, '%Y-%m-%d')) + 366
    End = datetime.toordinal(datetime.strptime(end_date, '%Y-%m-%d')) + 366
    End = End - 1.0 / 24.0
    if InputType == 1:
        tans = getTSValues(globalDict.get('hydroptModel').Price.ExpectedSpotPriceFile, Start, End, 'Silent')
    elif InputType == 2:
        tans = getTSValues(globalDict.get('hydroptModel').Price.PriceShiftsFile, Start, End, 'Silent')
    else:
        curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No data available', type='bar', barmode='group',
                          style={'width': '650', 'height': '500'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
        dataTables.set('chart', {'headers': ['Date', 'Price'], 'rows': ['No data available']})
        return curChart.getValue()
    Plot = tans.get(0)
    MinStart = tans.get(1)
    MaxEnd = tans.get(2)
    Msg = tans.get(3)
    ### TODO: add FlushTSDefinitionInterval
    if Msg != '':
        curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No data available', type='bar', barmode='group',
                          style={'width': '650', 'height': '500'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
        dataTables.set('chart', {'headers': ['Date', 'Price'], 'rows': ['No data available']})
        return curChart.getValue()
    if Plot.len() > 0:
        t = getHydroptTime(Start, End)
        times = dateUtils.date_range_from_matlab(Start, End + 1)
        curChart.setChart(rows=[Plot.getList()], headers=[''], rowCaptions=times, title='', type='line', barmode='group',
                          style={'width': '650', 'height': '500'}, xAxis='', yAxis='[EUR/MWh]', showLegend=False, hoverinfo='x+y', error={})
        dataTables.set('chart', {'headers': ['Date', 'Price'], 'rows': [Plot.getList()], 'titles': times})
    else:
        ### TODO: add FlushTSDefinitionInterval
        curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No data available', type='bar', barmode='group',
                          style={'width': '650', 'height': '500'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
        dataTables.set('chart', {'headers': ['Date', 'Price'], 'rows': ['No data available']})
        return curChart.getValue()
    return curChart.getValue()

N_CLICKS1 = 0
N_CLICKS2 = 0
N_CLICKS3 = 0
N_CLICKS4 = 0
def addNewAsset(n_clicks1, n_clicks2, n_clicks3, n_clicks4, options, value):
    global N_CLICKS1, N_CLICKS2, N_CLICKS3, N_CLICKS4
    cnt = 0
    if n_clicks1 is None:
        cnt = cnt + 1
        n_clicks1 = 0
    if n_clicks2 is None:
        cnt = cnt + 1
        n_clicks2 = 0
    if n_clicks3 is None:
        cnt = cnt + 1
        n_clicks3 = 0
    if n_clicks4 is None:
        cnt = cnt + 1
        n_clicks4 = 0
    if cnt == 3:
        N_CLICKS1 = 0
        N_CLICKS2 = 0
        N_CLICKS3 = 0
        N_CLICKS4 = 0
    if N_CLICKS2 != n_clicks2:
        data = CSafeList(globalDict.get('hydroptModel').Asset)
        if globalDict.get('hydroptModel').nAssets == 1:
            assets = CSafeList([globalDict.get('hydroptModel').Asset])
        else:
            assets = CSafeList(lst=data.get(0))
        i = 0
        dropdownList = CSafeList()
        while (i < assets.len()):
            tDict = CSafeDict(dct={})
            tDict.set('label', str(i + 1) + ' ' + assets.get(i).Shortname)
            tDict.set('value', assets.get(i).Shortname)
            dropdownList.append(tDict.getDict())
            i = i + 1
        N_CLICKS2 = n_clicks2
        return dropdownList.getList()
    if N_CLICKS3 != n_clicks3:
        data = CSafeList(globalDict.get('hydroptModel').Asset)
        if globalDict.get('hydroptModel').nAssets == 1:
            assets = CSafeList([globalDict.get('hydroptModel').Asset])
        else:
            assets = CSafeList(lst=data.get(0))
        i = 0
        pos = -1
        while (i < assets.len()):
            if assets.get(i).Shortname == value:
                pos = i + 1
            i = i + 1
        #data = globalDict.get('hydroptModel')
        #octave.push('data', data)
        ### Interacting with octave
        octave.push('pos', pos)
        octave.eval('Data.nAssets = Data.nAssets + 1;')
        octave.eval('Data.Asset(end + 1) = Data.Asset(pos);')
        #octave.eval('Pos = data.Asset(pos).Position;')
        #octave.eval('data.Asset(end).Position = [min(1,Pos(1)+0.02) max(0,Pos(2)-0.02) 0 0];')
        octave.eval('Data.Asset(end).Shortname = strcat(Data.Asset(end).Shortname, "Copy");')
        ###
        #data = octave.pull('data')
        #globalDict.set('hydroptModel', data)
        globalDict.set('hydroptModel', octave.pull('Data'))
        data = CSafeList(globalDict.get('hydroptModel').Asset)
        if globalDict.get('hydroptModel').nAssets == 1:
            assets = CSafeList([globalDict.get('hydroptModel').Asset])
        else:
            assets = CSafeList(lst=data.get(0))
        i = 0
        dropdownList = CSafeList()
        while (i < assets.len()):
            tDict = CSafeDict(dct={})
            tDict.set('label', str(i + 1) + ' ' + assets.get(i).Shortname)
            tDict.set('value', assets.get(i).Shortname)
            dropdownList.append(tDict.getDict())
            i = i + 1
        N_CLICKS3 = n_clicks3
        return dropdownList.getList()
    if N_CLICKS4 != n_clicks4:
        N_CLICKS4 = n_clicks4
        data = CSafeList(globalDict.get('hydroptModel').Asset)
        if globalDict.get('hydroptModel').nAssets == 1:
            assets = CSafeList([globalDict.get('hydroptModel').Asset])
        else:
            assets = CSafeList(lst=data.get(0))
        if assets.len() == 1:
            return options
        i = 0
        pos = -1
        while (i < assets.len()):
            if assets.get(i).Shortname == value:
                pos = i + 1
            i = i + 1
        #data = globalDict.get('hydroptModel')
        #octave.push('data', data)
        ### Interacting with octave
        octave.push('pos', pos)
        octave.eval('Data.nAssets = Data.nAssets - 1;')
        octave.eval('Data.Asset(pos) = [];')
        ###
        #data = octave.pull('data')
        #globalDict.set('hydroptModel', data)
        globalDict.set('hydroptModel', octave.pull('Data'))
        data = CSafeList(globalDict.get('hydroptModel').Asset)
        if globalDict.get('hydroptModel').nAssets == 1:
            assets = CSafeList([globalDict.get('hydroptModel').Asset])
        else:
            assets = CSafeList(lst=data.get(0))
        i = 0
        dropdownList = CSafeList()
        while (i < assets.len()):
            tDict = CSafeDict(dct={})
            tDict.set('label', str(i + 1) + ' ' + assets.get(i).Shortname)
            tDict.set('value', assets.get(i).Shortname)
            dropdownList.append(tDict.getDict())
            i = i + 1
        return dropdownList.getList()
    N_CLICKS1 = n_clicks1
    #data = globalDict.get('hydroptModel')
    #octave.push('data', data)
    ### Interacting with octave
    octave.eval("Asset.ID = datenum(clock); Asset.Name = ''; Asset.Shortname = 'new" + str(n_clicks1)+"'; Asset.Position = [0.5 0.5 0 0]; Asset.Type = 1; Asset.MainFig.Check = 0; Asset.Export.Check = 0; Asset.Decomposer.Check = 0;")
    octave.eval("Asset.Scheduler.Check = 0; Asset.Scheduler.Settings = []; Asset.Scheduler.Result = []; Asset.Scheduler.Input = []; Asset.ScenarioWaterManager.Check = 0;")
    octave.eval("Asset.ScenarioWaterManager.Settings = []; Asset.ScenarioWaterManager.Result = []; Asset.ScenarioWaterManager.Warning = 0; Asset.ScenarioWaterManager.Input = [];")
    octave.eval("Asset.StochasticWaterManagerCheck = 0; Asset.StochasticWaterManager.Settings = []; Asset.StochasticWaterManager.Result = []; Asset.ProductionReservePowerFile = [];")
    octave.eval("Asset.ConsumptionReservePowerFile = []; R.Name = ''; R.PCType = 1; R.RType = 1; R.PowerType = 1; R.PowerFile = ''; R.StartYear = 2000; R.StartMonth = 1;")
    octave.eval("R.StartDay = 1; R.EndYear = 2050; R.EndMonth = 1; R.EndDay = 1; R.Bonus = 0.0; R.ScenarioFolder = ''; Asset.Reserve(1) = R; Asset.StackReserves = 1;")
    octave.eval("Asset.EngineAlternatives = []; Sens.ID = datenum(clock); Sens.Name = ''; Sens.Shortname = ''; Sens.InputType = 1; Sens.Reservoir = 1; Sens.Variation = 10; Sens.Unit = 1;")
    octave.eval("Sens.Duration = 7; Sens.Offset = 0; Sens.Result = []; Asset.Sensitivity = Sens; Top.nRes = 1; Top.nTimeLags = 0; Top.nTurbines = 1; Top.nPumps = 0; Top.nFlows = 0;")
    octave.eval("Top.Reservoir(1).Btn = [0.5 0.75]; Top.Reservoir(1).SpillsToRes = 0; Top.TimeLag = []; Top.Flow = []; Top.Engine(1).Btn = [0.5 0.25]; Top.Engine(1).OperatesFrom = 1;")
    octave.eval("Top.Engine(1).OperatesTo = 0; Asset.Topology = Top; Res.ID = datenum(clock); Res.Name = ''; Res.Shortname = ''; Res.IsStochastic = 1; Res.MaxLevelFile = ''; Res.MinLevelFile = '0';")
    octave.eval("Res.MWh2CubicMetresFile = '%AutoCalc'; Res.InfiltrationLossesFile = ''; Res.Inflow.MinimumInflowFile = '0'; Res.Inflow.MaximumInflowFile = '0';")
    octave.eval("Res.Inflow.ExpectedInflowFile = '0'; Res.ExpectedInflow.Val = []; Res.ExpectedInflow.Start = 0; Res.ExpectedInflow.End = 0; Res.Inflow.DayPatternFile = '';")
    octave.eval("Res.Inflow.InflowScenarioFolder = ''; Res.Inflow.TransitionProbabilityFile = ''; Res.Spill.Capacity = 1000; Res.Spill.Efficiency = 100; Res.Scheduler.StartLevel = [];")
    octave.eval("Res.Scheduler.EndLevel = []; Res.Scheduler.LevelDiff = []; Res.Scheduler.WaterValue = []; Res.Scheduler.Deviation = []; Res.Scheduler.HalfLife = [];")
    octave.eval("Res.Scheduler.Result = []; Res.StochasticWaterManager.nStatesReservoir = 101; Res.StochasticWaterManager.DMin = -10; Res.StochasticWaterManager.DMax = 0;")
    octave.eval("Res.StochasticWaterManager.StartLevel = []; Res.StochasticWaterManager.Result = []; Res.ScenarioWaterManager.StartLevel = []; Res.ScenarioWaterManager.EndLevel = [];")
    octave.eval("Res.ScenarioWaterManager.Deviation = []; Res.ScenarioWaterManager.HalfLife = []; Res.ScenarioWaterManager.Result = []; Res.MaxLevel.Val = []; Res.MaxLevel.Start = 0;")
    octave.eval("Res.MaxLevel.End = 0; Res.MinLevel.Val = []; Res.MinLevel.Start = 0; Res.MinLevel.End = 0; Res.M3_to_MWh.X = []; Res.M3_to_MWh.Y = []; Asset.Reservoir = Res;")
    octave.eval("Asset.Flow = []; Engine.ID = datenum(clock); Engine.Name = ''; Engine.Shortname = ''; Engine.Type = 1; Engine.MaxFlowFile = ''; Engine.MaxFlow.Val = [];")
    octave.eval("Engine.MaxFlow.Start = 0; Engine.MaxFlow.End = 0; Engine.MinRunningFlowFile = '0'; Engine.MinRunFlow.Val = []; Engine.MinRunFlow.Start = 0; Engine.MinRunFlow.End = 0;")
    octave.eval("Engine.MinFlowFile = '0'; Engine.MinFlow.Val = []; Engine.MinFlow.Start = 0; Engine.MinFlow.End = 0; Engine.StartupFile = '1'; Engine.ShutdownFile = '1';")
    octave.eval("Engine.EngineCharacteristicFile = ''; Engine.Characteristic.X = []; Engine.Characteristic.Y = []; Engine.EnginePowerCharacteristicFile = '%Constant';")
    octave.eval("Engine.PowerCharacteristic.X = []; Engine.PowerCharacteristic.Y = []; Engine.PowerCharacteristicIsAbsolute = false; Engine.bUseReservoirAbove = true;")
    octave.eval("Engine.OperatingCosts = 0; Engine.StartupCosts = 0; Engine.ShutdownCosts = 0; Engine.MaxNofOperatingHours = Inf;  Engine.MinNofOperatingHours = 1; Engine.MinNofIdleHours = 1;")
    octave.eval("Engine.MinProductionHoursValue = []; Engine.MaxProductionHoursValue = []; Engine.MaxProductionHoursPeriod = 'Day'; Engine.MinStartsValue = [];")
    octave.eval("Engine.MaxStartsValue = []; Engine.MaxStartsPeriod = 'Day'; Eng.AlphaPower = []; Eng.AlphaPrime = []; Eng.LastFlow = []; Eng.MaxPower = []; Eng.MinPower = [];")
    octave.eval("Eng.MinRunningPower = []; Eng.MaxPowerPrime = []; Eng.MaxFlow = []; Eng.MinRunningFlow = []; Eng.MinFlow = []; Eng.MaxPossibleFlow = []; Eng.MinPossibleRunningFlow = [];")
    octave.eval("Eng.MinPossibleFlow = []; Eng.MaxFlowPrime = []; Eng.RM3Lin = []; Engine.PriceFile = ''; Engine.Price.Val = []; Engine.Price.Start = 0; Engine.Price.End = 0;")
    octave.eval("Engine.MaxNofProductionHours = []; Engine.MaxNofStarts = []; Engine.ProductionReserve = 0; Engine.ConsumptionReserve = 0; Engine.IncludeInReserve = 0;")
    octave.eval("Engine.Scheduler.Result = []; Engine.ScenarioWaterManager.Result = []; Asset.Engine = Engine; Stoch.ID = datenum(clock); Stoch.Name = ''; Stoch.nRes = 1; Stoch.nInflows = 1;")
    octave.eval("Stoch.StochRes(1).Reservoir = 1; Stoch.StochInflow(1).Inflow = 1; Stoch.StochInflow(1).Autocorrelation = 1; Asset.StochasticModel = Stoch; Asset.Optimization.MaxIter = [];")
    octave.eval("Asset.Optimization.Accuracy = []; Asset.Optimization.LogFolder = []; Asset.Optimization.SolverParametersMILP = []; Asset.Optimization.SolverParametersLP = [];")
    octave.eval("[Y,M,D] = datevec(datenum(clock)); Asset.Option.StartYear = Y; Asset.Option.StartDay = D; Asset.Option.StartMonth = M; Asset.Option.EndYear = Y+1; Asset.Option.EndDay = D;")
    octave.eval("Asset.Option.EndMonth = M; Asset.Option.BuySell = 1; Asset.Option.CallPut = 1; Asset.Option.Premium = ''; Asset.Option.TypeID = 1001;")
    octave.eval("j=0; j=j+1; OT(j).ID = 1001; OT(j).Name = 'Daily Base Swing'; OT(j).ParameterName = {'Max Power [MW]', 'Max Draws'}; OT(j).ParameterDefault = {50 21};")
    octave.eval("OT(j).nParameters = length(OT(j).ParameterName); OT(j).UsePut = 0; OT(j).Show.CurrentPower = 1; OT(j).Show.PowerPlanning = 1; OT(j).Show.CurrentReservoirLevel = 1;")
    octave.eval("OT(j).Show.ReservoirCycle = 1; OT(j).Show.WaterValue = 0; OT(j).Show.EnergyPlanning = 1;")
    octave.eval("OT(j).Description = {'DAILY BASE SWING', '', 'The Buyer has the right to buy base load power called on a day ahead basis from the Seller.', '', 'Buyer can call a maximum of <MaxDraws> days and must pay an option premium for <MaxDraws> days worth of calls whether they are used or not'};")
    octave.eval("Number = find([OT.ID] == Asset.Option.TypeID); OT = OT(Number); Asset.Option.Parameter = OT.ParameterDefault;")
    octave.eval("Data.nAssets = Data.nAssets + 1; Data.Asset(end + 1) = Asset; Topo.nRes = 1; Topo.nTimeLags = 0; Topo.nTurbines = 1; Topo.nPumps = 0; Topo.nFlows = 0;")
    octave.eval("Topo.Reservoir(1).Btn = [0.5 0.75]; Topo.Reservoir(1).SpillsToRes = 0; Topo.TimeLag = []; Topo.Flow = []; Topo.Engine(1).Btn = [0.5 0.25]; Topo.Engine(1).OperatesFrom = 1;")
    octave.eval("Topo.Engine(1).OperatesTo = 0; Data.Asset(end).Topology = Topo; Res.ID = datenum(clock); Res.Name = ''; Res.Shortname = ''; Res.IsStochastic = 1;")
    octave.eval("Res.MaxLevelFile = ''; Res.MinLevelFile = '0'; Res.MWh2CubicMetresFile = '%AutoCalc'; Res.InfiltrationLossesFile = '';Res.Inflow.MinimumInflowFile = '0';")
    octave.eval("Res.Inflow.MaximumInflowFile = '0'; Res.Inflow.ExpectedInflowFile = '0'; Res.ExpectedInflow.Val = []; Res.ExpectedInflow.Start = 0; Res.ExpectedInflow.End = 0;")
    octave.eval("Res.Inflow.DayPatternFile = ''; Res.Inflow.InflowScenarioFolder = ''; Res.Inflow.TransitionProbabilityFile = ''; Res.Spill.Capacity = 1000; Res.Spill.Efficiency = 100;")
    octave.eval("Res.Scheduler.StartLevel = []; Res.Scheduler.EndLevel = []; Res.Scheduler.LevelDiff = []; Res.Scheduler.WaterValue = []; Res.Scheduler.Deviation = [];")
    octave.eval("Res.Scheduler.HalfLife = []; Res.Scheduler.Result = []; Res.StochasticWaterManager.nStatesReservoir = 101; Res.StochasticWaterManager.DMin = -10; ")
    octave.eval("Res.StochasticWaterManager.DMax = 0; Res.StochasticWaterManager.StartLevel = []; Res.StochasticWaterManager.Result = []; Res.ScenarioWaterManager.StartLevel = [];")
    octave.eval("Res.ScenarioWaterManager.EndLevel = []; Res.ScenarioWaterManager.Deviation = []; Res.ScenarioWaterManager.HalfLife = []; Res.ScenarioWaterManager.Result = [];")
    octave.eval("Res.MaxLevel.Val = []; Res.MaxLevel.Start = 0; Res.MaxLevel.End = 0; Res.MinLevel.Val = []; Res.MinLevel.Start = 0; Res.MinLevel.End = 0; Res.M3_to_MWh.X = [];")
    octave.eval("Res.M3_to_MWh.Y = []; for i=1:Topo.nRes; Data.Asset(end).Reservoir(i) = Res; end; Engine.ID = datenum(clock); Engine.Name = ''; Engine.Shortname = ''; Engine.Type = 1;")
    octave.eval("Engine.MaxFlowFile = ''; Engine.MaxFlow.Val = []; Engine.MaxFlow.Start = 0; Engine.MaxFlow.End = 0; Engine.MinRunningFlowFile = '0'; Engine.MinRunFlow.Val = [];")
    octave.eval("Engine.MinRunFlow.Start = 0; Engine.MinRunFlow.End = 0; Engine.MinFlowFile = '0'; Engine.MinFlow.Val = []; Engine.MinFlow.Start = 0; Engine.MinFlow.End = 0;")
    octave.eval("Engine.StartupFile = '1'; Engine.ShutdownFile = '1'; Engine.EngineCharacteristicFile = ''; Engine.Characteristic.X = []; Engine.Characteristic.Y = [];")
    octave.eval("Engine.EnginePowerCharacteristicFile = '%Constant'; Engine.PowerCharacteristic.X = []; Engine.PowerCharacteristic.Y = []; Engine.PowerCharacteristicIsAbsolute = false;")
    octave.eval("Engine.bUseReservoirAbove = true; Engine.OperatingCosts = 0; Engine.StartupCosts = 0; Engine.ShutdownCosts = 0; Engine.MaxNofOperatingHours = Inf;")
    octave.eval("Engine.MinNofOperatingHours = 1; Engine.MinNofIdleHours = 1; Engine.MinProductionHoursValue = []; Engine.MaxProductionHoursValue = []; Engine.MaxProductionHoursPeriod = 'Day';")
    octave.eval("Engine.MinStartsValue = []; Engine.MaxStartsValue = []; Engine.MaxStartsPeriod = 'Day'; Eng.AlphaPower = []; Eng.AlphaPrime = []; Eng.LastFlow = []; Eng.MaxPower = [];")
    octave.eval("Eng.MinPower = []; Eng.MinRunningPower = []; Eng.MaxPowerPrime = []; Eng.MaxFlow = []; Eng.MinRunningFlow = []; Eng.MinFlow = []; Eng.MaxPossibleFlow = [];")
    octave.eval("Eng.MinPossibleRunningFlow = []; Eng.MinPossibleFlow = []; Eng.MaxFlowPrime = []; Eng.RM3Lin = []; Engine.PriceFile = ''; Engine.Price.Val = []; Engine.Price.Start = 0;")
    octave.eval("Engine.Price.End = 0; Engine.MaxNofProductionHours = []; Engine.MaxNofStarts = []; Engine.ProductionReserve = 0; Engine.ConsumptionReserve = 0; Engine.IncludeInReserve = 0;")
    octave.eval("Engine.Scheduler.Result = []; Engine.ScenarioWaterManager.Result = []; for i=1:Topo.nTurbines; Data.Asset(end).Engine(i) = Engine; end; Engine.Type = 2;")
    octave.eval("for i=1:Topo.nPumps; Data.Asset(end).Engine(Topo.nTurbines + i) = Engine; end; Data.Asset(end).Optimization = Data.Status.Optimization; Data.nAssets = Data.nAssets + 1;")
    ###
    #data = octave.pull('data')
    #globalDict.set('hydroptModel', data)
    globalDict.set('hydroptModel', octave.pull('Data'))
    data = CSafeList(globalDict.get('hydroptModel').Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    i = 0
    dropdownList = CSafeList()
    while (i < assets.len()):
        tDict = CSafeDict(dct={})
        tDict.set('label', str(i + 1) + ' ' + assets.get(i).Shortname)
        tDict.set('value', assets.get(i).Shortname)
        dropdownList.append(tDict.getDict())
        i = i + 1
    return dropdownList.getList()

N_CLICKS_ = 0
def changeDropdownValue(options, n_clicks):
    global N_CLICKS_
    if n_clicks is None:
        n_clicks = 0
        N_CLICKS_ = 0
    if N_CLICKS_ != n_clicks:
        N_CLICKS_ = n_clicks
        data = CSafeList(globalDict.get('hydroptModel').Asset)
        if globalDict.get('hydroptModel').nAssets == 1:
            assets = CSafeList([globalDict.get('hydroptModel').Asset])
        else:
            assets = CSafeList(lst=data.get(0))
        i = 0
        return assets.get(0).Shortname
    cur = CSafeList(options).get(-1)
    return CSafeDict(cur).get('value')

def changeName(value):
    data = CSafeList(globalDict.get('hydroptModel').Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    i = 0
    while (i < assets.len()):
        if assets.get(i).Shortname == value:
            return assets.get(i).Name
        i = i + 1
    return ''

def changeShortName(value):
    return value

def changeAssetType(value):
    data = CSafeList(globalDict.get('hydroptModel').Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    i = 0
    while (i < assets.len()):
        if assets.get(i).Shortname == value:
            if assets.get(i).Type == 1:
                return 'Hydroplant'
            else:
                return 'Option'
        i = i + 1
    return ''

def updateName(value, name, options):
    data = CSafeList(globalDict.get('hydroptModel').Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    i = 0
    options = CSafeList(options)
    while (i < options.len()):
        if CSafeDict(options.get(i)).get('value') == name:
            octave.eval('Data.Asset(' + str(i + 1) + ').Name = "' + value + '";')
            #CSafeMatlab.setField(assets.get(i), 'Name', value)
        i = i + 1
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Name'

def updateShortName(value, name, options):
    data = CSafeList(globalDict.get('hydroptModel').Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    i = 0
    options = CSafeList(options)
    while (i < options.len()):
        if CSafeDict(options.get(i)).get('value') == name:
            octave.eval('Data.Asset(' + str(i + 1) + ').Shortname = "' + value + '";')
            #CSafeMatlab.setField(assets.get(i), 'Shortname', value)
            break
        i = i + 1
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Short Name'

def updateAssetType(value, name, options):
    data = CSafeList(globalDict.get('hydroptModel').Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    i = 0
    options = CSafeList(options)
    while (i < options.len()):
        if CSafeDict(options.get(i)).get('value') == name:
            if value == 'Hydroplant':
                octave.eval('Data.Asset(' + str(i + 1) + ').Type = 1;')
                #CSafeMatlab.setField(assets.get(i), 'Type', 1)
            else:
                octave.eval('Data.Asset(' + str(i + 1) + ').Type = 2;')
                #CSafeMatlab.setField(assets.get(i), 'Type', 2)
        i = i + 1
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Asset Type'

cnt = 0
def updateMap(options):
    global cnt
    cnt = cnt + 1
    latList = CSafeList([46.563371, 46.183447, 46.067888, 46.623189, 46.080639, 46.137034, 46.481873, 46.461194, 46.371179, 46.070118, 46.145847, 46.169434, 46.5782776, 47.229296, 47.369007])
    lonList = CSafeList([8.9612593, 7.2491351, 6.9303941, 10.1909703, 7.4023168, 7.5696649, 9.4516843, 8.3680963, 8.0014061, 6.8762443, 6.9671043, 8.1199813, 9.1179484, 7.5880925, 7.9783607])
    curMap = screenVariables.get('mainMap')
    data = CSafeList(globalDict.get('hydroptModel').Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    i = 0
    shortnames = CSafeList()
    lat = CSafeList()
    lon = CSafeList()
    drag = CSafeList()
    while (i < assets.len()):
        shortnames.append(assets.get(i).Shortname)
        drag.append(True)
        pos = CSafeList(CSafeList(assets.get(i).Position).get(0))
        if pos.get(0) < 1.0:
            pos.set(0, latList.get(i))
        if pos.get(1) < 1.0:
            pos.set(1, lonList.get(i))
        lat.append(pos.get(0))
        lon.append(pos.get(1))
        i = i + 1
    curMap.setYMap(shortnames.getList(), lat.getList(), lon.getList(), drag.getList(), {'width': '100%', 'height': '60vh'}, cnt)
    return curMap.getContent()

def updateTopologyLink(value):
    return '/d/DisplayScreen@screen=defineTopology&asset='+value
