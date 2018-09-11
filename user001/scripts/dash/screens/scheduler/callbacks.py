def updateSecondColumn(value):
    data = CSafeList(globalDict.get('hydroptModel').Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    i = 0
    rows = CSafeList()
    col1 = CSafeList()
    col2 = CSafeList()
    col3 = CSafeList()
    col4 = CSafeList()
    names = CSafeList()
    names.append('Start level [m3]')
    if value == 'End Level':
        names.append('End level [m3]')
        typ = 'End Level'
    elif value == 'Level Difference':
        names.append('Level Difference [m3]')
        typ = 'Level Difference'
    else:
        names.append('Water Value [Eur/m3]')
        typ = 'Water Value'
    names.append('Inflow Deviation [%]')
    names.append('Half life [d]')
    sum = 0
    while (i < assets.len()):
        j = 0
        sum = sum + assets.get(i).Topology.nRes
        while (j < assets.get(i).Topology.nRes):
            if assets.get(i).Topology.nRes == 1:
                reservoirs = CSafeList([assets.get(i).Reservoir])
            else:
                reservoirs = CSafeList(CSafeList(assets.get(i).Reservoir).get(0))
            if type(reservoirs.get(j).Scheduler.StartLevel) == type([]):
                col1.append([''])
            else:
                col1.append([reservoirs.get(j).Scheduler.StartLevel])
            if typ == 'End Level':
                if type(reservoirs.get(j).Scheduler.EndLevel) == type([]):
                    col2.append([''])
                else:
                    col2.append([reservoirs.get(j).Scheduler.EndLevel])
            elif typ == 'Level Difference':
                if type(reservoirs.get(j).Scheduler.LevelDiff) == type([]):
                    col2.append([''])
                else:
                    col2.append([reservoirs.get(j).Scheduler.LevelDiff])
            else:
                if type(reservoirs.get(j).Scheduler.WaterValue) == type([]):
                    col2.append([''])
                else:
                    col2.append([reservoirs.get(j).Scheduler.WaterValue])
            if type(reservoirs.get(j).Scheduler.Deviation) == type([]):
                col3.append([''])
            else:
                col3.append([reservoirs.get(j).Scheduler.Deviation])
            if type(reservoirs.get(j).Scheduler.HalfLife) == type([]):
                col4.append([''])
            else:
                col4.append([reservoirs.get(j).Scheduler.HalfLife])
            j = j + 1
        i = i + 1
    rows.append(col1.getList())
    rows.append(col2.getList())
    rows.append(col3.getList())
    rows.append(col4.getList())
    curTable = screenVariables.get('hydroplantTable')
    curTable.setTable(rows.getList(), names.getList(), False, False, False, True, {'width': '70%', 'height': '50vh', 'marginTop': '1px'}, 35 * (sum + 1))
    return curTable.getData().to_dict('records')

def updatePerformanceSettings(value):
    if 'Spills' in value:
        octave.eval('Data.Scheduler.UseSpills = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseSpills = 0.0;')
    if 'Min. Hours' in value:
        octave.eval('Data.Scheduler.UseConstraints = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseConstraints = 0.0;')
    if 'SU/SD Costs' in value:
        octave.eval('Data.Scheduler.UseCosts = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseCosts = 0.0;')
    if 'Min RunPower' in value:
        octave.eval('Data.Scheduler.UseMinRunningFlow = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseMinRunningFlow = 0.0;')
    if 'Infil. Losses' in value:
        octave.eval('Data.Scheduler.UseInfiltrationLosses = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseInfiltrationLosses = 0.0;')
    if 'Prod. reserves' in value:
        octave.eval('Data.Scheduler.UseProductionReserves = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseProductionReserves = 0.0;')
    if 'Cons. reserves' in value:
        octave.eval('Data.Scheduler.UseConsumptionReserves = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseConsumptionReserves = 0.0;')
    if 'Sp. prod. reserves' in value:
        octave.eval('Data.Scheduler.UseSpinningProductionReserves = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseSpinningProductionReserves = 0.0;')
    if 'Sp. cons. reserves' in value:
        octave.eval('Data.Scheduler.UseSpinningConsumptionReserves = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseSpinningConsumptionReserves = 0.0;')
    if 'Engine alternatives' in value:
        octave.eval('Data.Scheduler.UseEngineAlternatives = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseEngineAlternatives = 0.0;')
    if 'Dyn flow calc' in value:
        octave.eval('Data.Scheduler.UseDynFlowCalc = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseDynFlowCalc = 0.0;')
    if 'Full newton' in value:
        octave.eval('Data.Scheduler.UseFullNewton = 1.0;')
    else:
        octave.eval('Data.Scheduler.UseFullNewton = 0.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Choose performance settings'

def updateInputType(value):
    if value == 'End Level':
        octave.eval('Data.Scheduler.ReservoirInputType = 1.0;')
    elif value == 'Level Difference':
        octave.eval('Data.Scheduler.ReservoirInputType = 2.0;')
    else:
        octave.eval('Data.Scheduler.ReservoirInputType = 3.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return ''

def updateDatePicker(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    octave.eval('Data.Scheduler.StartYear = ' + str(start_date.year) + ';')
    octave.eval('Data.Scheduler.StartMonth = ' + str(start_date.month) + ';')
    octave.eval('Data.Scheduler.StartDay = ' + str(start_date.day) + ';')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    octave.eval('Data.Scheduler.EndYear = ' + str(end_date.year) + ';')
    octave.eval('Data.Scheduler.EndMonth = ' + str(end_date.month) + ';')
    octave.eval('Data.Scheduler.EndDay = ' + str(end_date.day) + ';')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return False

def updateReservoirParameters(rows):
    hydroptModel = globalDict.get('hydroptModel')
    data = CSafeList(hydroptModel.Asset)
    if globalDict.get('hydroptModel').nAssets == 1:
        assets = CSafeList([globalDict.get('hydroptModel').Asset])
    else:
        assets = CSafeList(lst=data.get(0))
    i = 0
    rows = CSafeList(rows)
    num = 0
    while (i < assets.len()):
        j = 0
        while (j < assets.get(i).Topology.nRes):
            tDict = CSafeDict(rows.get(num + j))
            keys = CSafeList(tDict.getKeys())
            values = CSafeList(tDict.getValues())
            k = 0
            while (k < keys.len()):
                curValue = []
                if CSafeStr(values.get(k)).len() != 0:
                    curValue = float(values.get(k))
                if keys.get(k) == 'Start level [m3]':
                    name = 'StartLevel'
                elif keys.get(k) == 'End level [m3]':
                    name = 'EndLevel'
                elif keys.get(k) == 'Level Difference [m3]':
                    name = 'LevelDiff'
                elif keys.get(k) == 'Water Value [Eur/m3]':
                    name = 'WaterValue'
                elif keys.get(k) == 'Inflow Deviation [%]':
                    name = 'Deviation'
                elif keys.get(k) == 'Half life [d]':
                    name = 'HalfLife'
                octave.eval('Data.Asset(' + str(i + 1) + ').Reservoir(' + str(j + 1) + ').Scheduler.' + name + '=' + str(curValue) + ';')
                k = k + 1
            j = j + 1
        num = num + int(assets.get(i).Topology.nRes)
        i = i + 1
    globalDict.set('hydroptModel', octave.pull('Data'))
    return True