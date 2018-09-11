def updateNScenarios(value):
    if value == '':
        value = 0
    octave.eval('Data.ScenarioWaterManager.nScenarios = ' + str(value) + ';')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Number of scenarios'

def updateScenarioSettings(value):
    if 'Use HPFC Only' in value:
        octave.eval('Data.ScenarioWaterManager.UseHPFCOnly = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseHPFCOnly = 0.0;')
    if 'Export Excel' in value:
        octave.eval('Data.ScenarioWaterManager.ExportScenarios = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.ExportScenarios = 0.0;')
    if 'Export CSV' in value:
        octave.eval('Data.ScenarioWaterManager.ExportCSV = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.ExportCSV = 0.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Select scenario settings'

def updatePerformanceSettings(value):
    if 'Spills' in value:
        octave.eval('Data.ScenarioWaterManager.UseSpills = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseSpills = 0.0;')
    if 'Min. Hours' in value:
        octave.eval('Data.ScenarioWaterManager.UseConstraints = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseConstraints = 0.0;')
    if 'SU/SD Costs' in value:
        octave.eval('Data.ScenarioWaterManager.UseCosts = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseCosts = 0.0;')
    if 'Min RunPower' in value:
        octave.eval('Data.ScenarioWaterManager.UseMinRunningFlow = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseMinRunningFlow = 0.0;')
    if 'Infil. Losses' in value:
        octave.eval('Data.ScenarioWaterManager.UseInfiltrationLosses = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseInfiltrationLosses = 0.0;')
    if 'Prod. reserves' in value:
        octave.eval('Data.ScenarioWaterManager.UseProductionReserves = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseProductionReserves = 0.0;')
    if 'Cons. reserves' in value:
        octave.eval('Data.ScenarioWaterManager.UseConsumptionReserves = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseConsumptionReserves = 0.0;')
    if 'Sp. prod. reserves' in value:
        octave.eval('Data.ScenarioWaterManager.UseSpinningProductionReserves = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseSpinningProductionReserves = 0.0;')
    if 'Sp. cons. reserves' in value:
        octave.eval('Data.ScenarioWaterManager.UseSpinningConsumptionReserves = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseSpinningConsumptionReserves = 0.0;')
    if 'Engine alternatives' in value:
        octave.eval('Data.ScenarioWaterManager.UseEngineAlternatives = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseEngineAlternatives = 0.0;')
    if 'Dyn flow calc' in value:
        octave.eval('Data.ScenarioWaterManager.UseDynFlowCalc = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseDynFlowCalc = 0.0;')
    if 'Full newton' in value:
        octave.eval('Data.ScenarioWaterManager.UseFullNewton = 1.0;')
    else:
        octave.eval('Data.ScenarioWaterManager.UseFullNewton = 0.0;')
    globalDict.set('hydroptModel', octave.pull('Data'))
    return 'Choose performance settings'

def updateDatePicker(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    octave.eval('Data.ScenarioWaterManager.StartYear = ' + str(start_date.year) + ';')
    octave.eval('Data.ScenarioWaterManager.StartMonth = ' + str(start_date.month) + ';')
    octave.eval('Data.ScenarioWaterManager.StartDay = ' + str(start_date.day) + ';')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    octave.eval('Data.ScenarioWaterManager.EndYear = ' + str(end_date.year) + ';')
    octave.eval('Data.ScenarioWaterManager.EndMonth = ' + str(end_date.month) + ';')
    octave.eval('Data.ScenarioWaterManager.EndDay = ' + str(end_date.day) + ';')
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
                elif keys.get(k) == 'Inflow Deviation [%]':
                    name = 'Deviation'
                elif keys.get(k) == 'Half life [d]':
                    name = 'HalfLife'
                octave.eval('Data.Asset('+str(i + 1)+').Reservoir(' + str(j + 1) + ').ScenarioWaterManager.' + name + ' = ' + str(curValue) + ';')
                k = k + 1
            j = j + 1
        num = num + int(assets.get(i).Topology.nRes)
        i = i + 1
    globalDict.set('hydroptModel', octave.pull('Data'))
    return True