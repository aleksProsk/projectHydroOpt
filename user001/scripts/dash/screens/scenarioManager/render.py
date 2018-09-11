log.print("starting renderer")

if globalDict.contains('hydroptModel'):
    hydroptModel = globalDict.get('hydroptModel')
else:
    hydroptModel = hydropt.getData('model')
    globalDict.set('hydroptModel', hydroptModel)

data = CSafeList(globalDict.get('hydroptModel').Asset)
if globalDict.get('hydroptModel').nAssets == 1:
    assets = CSafeList([globalDict.get('hydroptModel').Asset])
else:
    assets = CSafeList(lst=data.get(0))
i = 0
curList = CSafeList()
res = CSafeList()
num = CSafeList()
rows = CSafeList()
col1 = CSafeList()
col2 = CSafeList()
col3 = CSafeList()
col4 = CSafeList()
labelClassName = ''
mx = 0
while (i < assets.len()):
    tDict = CSafeDict({'label': assets.get(i).Shortname, 'value': assets.get(i).Shortname})
    curList.append(tDict.getDict())
    mx = max(mx, assets.get(i).Topology.nRes)
    j = 0
    labelClassName = labelClassName + str(int(assets.get(i).Topology.nRes))
    if i != assets.len() - 1:
        labelClassName = labelClassName + '-'
    while (j < assets.get(i).Topology.nRes):
        if assets.get(i).Topology.nRes == 1:
            reservoirs = CSafeList([assets.get(i).Reservoir])
        else:
            reservoirs = CSafeList(CSafeList(assets.get(i).Reservoir).get(0))
        res.append(reservoirs.get(j).Name)
        num.append(i)
        if type(reservoirs.get(j).ScenarioWaterManager.StartLevel) == type([]):
            col1.append([''])
        else:
            col1.append([reservoirs.get(j).ScenarioWaterManager.StartLevel])
        if type(reservoirs.get(j).ScenarioWaterManager.EndLevel) == type([]):
            col2.append([''])
        else:
            col2.append([reservoirs.get(j).ScenarioWaterManager.EndLevel])
        if type(reservoirs.get(j).ScenarioWaterManager.Deviation) == type([]):
            col3.append([''])
        else:
            col3.append([reservoirs.get(j).ScenarioWaterManager.Deviation])
        if type(reservoirs.get(j).ScenarioWaterManager.HalfLife) == type([]):
            col4.append([''])
        else:
            col4.append([reservoirs.get(j).ScenarioWaterManager.HalfLife])
        j = j + 1
    i = i + 1
rows.append(col1.getList())
rows.append(col2.getList())
rows.append(col3.getList())
rows.append(col4.getList())

tval = CSafeList()
if hydroptModel.ScenarioWaterManager.UseSpills == 1:
    tval.append('Spills')
if hydroptModel.ScenarioWaterManager.UseConstraints == 1:
    tval.append('Min. Hours')
if hydroptModel.ScenarioWaterManager.UseCosts == 1:
    tval.append('SU/SD Costs')
if hydroptModel.ScenarioWaterManager.UseMinRunningFlow == 1:
    tval.append('Min RunPower')
if hydroptModel.ScenarioWaterManager.UseInfiltrationLosses == 1:
    tval.append('Infil. Losses')
if hydroptModel.ScenarioWaterManager.UseProductionReserves == 1:
    tval.append('Prod. reserves')
if hydroptModel.ScenarioWaterManager.UseConsumptionReserves == 1:
    tval.append('Cons. reserves')
if hydroptModel.ScenarioWaterManager.UseSpinningProductionReserves == 1:
    tval.append('Sp. prod. reserves')
if hydroptModel.ScenarioWaterManager.UseSpinningConsumptionReserves == 1:
    tval.append('Sp. cons. reserves')
if hydroptModel.ScenarioWaterManager.UseEngineAlternatives == 1:
    tval.append('Engine alternatives')
if hydroptModel.ScenarioWaterManager.UseDynFlowCalc == 1:
    tval.append('Dyn flow calc')
if hydroptModel.ScenarioWaterManager.UseFullNewton == 1:
    tval.append('Full newton')
StartYear = int(hydroptModel.ScenarioWaterManager.StartYear)
StartMonth = int(hydroptModel.ScenarioWaterManager.StartMonth)
StartDay = int(hydroptModel.ScenarioWaterManager.StartDay)
EndYear = int(hydroptModel.ScenarioWaterManager.EndYear)
EndMonth = int(hydroptModel.ScenarioWaterManager.EndMonth)
EndDay =  int(hydroptModel.ScenarioWaterManager.EndDay)

optimizingHorizonFrame = CFrame('Optimizing Horizon', width=0.2, height=0.2)

datePicker = Create(CDatePickerRange, {'name': 'datePicker', 'minDate': (1995, 1, 1), 'maxDate': (2050, 12, 31), 'startDate': (StartYear, StartMonth, StartDay), 'endDate': (EndYear, EndMonth, EndDay)})

optimizingHorizonFrame.aChild(datePicker)

timeGranularityFrame = CFrame('Time Granularity', width=0.2, height=0.2)

timeGranularityDropdown = Create(CDropdown, {'name': 'timeGranularityDropdown',
                                             'options': [{'label': '15 minutes', 'value': '15min'},
                                                         {'label': 'hourly', 'value': 'hourly'}],
                                             'value': 'hourly',
                                             'multi': False,
                                             'clearable': False,
                                             'style': {'width': '100%'}})

timeGranularityFrame.aChild(timeGranularityDropdown)

performanceSettingsFrame = CFrame('Performance Settings', width=0.2, height=0.2)

performanceSettingsDropdown = Create(CDropdown, {'name': 'performanceSettingsDropdown',
                                        'options': [{'label': 'Spills', 'value': 'Spills',},
                                                    {'label': 'Min. Hours', 'value': 'Min. Hours',},
                                                    {'label': 'SU/SD Costs', 'value': 'SU/SD Costs',},
                                                    {'label': 'Min RunPower', 'value': 'Min RunPower',},
                                                    {'label': 'Infil. Losses', 'value': 'Infil. Losses',},
                                                    {'label': 'Dyn flow calc', 'value': 'Dyn flow calc',},
                                                    {'label': 'Prod. reserves', 'value': 'Prod. reserves',},
                                                    {'label': 'Cons. reserves', 'value': 'Cons. reserves',},
                                                    {'label': 'Sp. prod. reserves', 'value': 'Sp. prod. reserves',},
                                                    {'label': 'Sp. cons. reserves', 'value': 'Sp. cons. reserves',},
                                                    {'label': 'Engine alternatives', 'value': 'Engine alternatives',},
                                                    {'label': 'Full newton', 'value': 'Full newton',},
                                                    ],
                                        'value': tval.getList(),
                                        'multi': True,
                                        'clearable': True,
                                        'placeholder': 'Select performance settings',
                                        'style': {'width': '100%'},
                                    })

performanceSettingsFrame.aChild(performanceSettingsDropdown)

scenarioSettingsFrame = CFrame('Scenario Settings', width=0.2, height=0.2, style={'display': 'flex', 'flexDirection': 'column'})

scenarioSettingsDropdown = Create(CDropdown, {'name': 'scenarioSettingsDropdown',
                                        'options': [{'label': 'Rotate', 'value': 'Rotate',},
                                                    {'label': 'Shuffle', 'value': 'Shuffle',},
                                                    ],
                                        'value': 'Rotate',
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })
scenarioSettingsInput = Create(CInput, {'name': 'scenarioSettingsInput', 'value': hydroptModel.ScenarioWaterManager.nScenarios, 'placeholder': 'nScenarios', 'style': {'width': '100%'}})

tval = CSafeList()
if hydroptModel.ScenarioWaterManager.UseHPFCOnly == 1:
    tval.append('Use HPFC Only')
if hydroptModel.ScenarioWaterManager.ExportScenarios == 1:
    tval.append('Export Excel')
if hydroptModel.ScenarioWaterManager.ExportCSV == 1:
    tval.append('Export CSV')
scenarioSettingsUseDropdown = Create(CDropdown, {'name': 'scenarioSettingsUseDropdown',
                                        'options': [{'label': 'Use HPFC Only', 'value': 'Use HPFC Only',},
                                                    {'label': 'Export Excel', 'value': 'Export Excel',},
                                                    {'label': 'Export CSV', 'value': 'Export CSV',},
                                                    ],
                                        'value': tval.getList(),
                                        'multi': True,
                                        'clearable': True,
                                        'style': {'width': '100%'},
                                        'placeholder': 'Select scenario settings'
                                    })

scenarioSettingsFrame.aChild(scenarioSettingsDropdown)
scenarioSettingsFrame.aChild(scenarioSettingsInput)
scenarioSettingsFrame.aChild(scenarioSettingsUseDropdown)

importFrame = CFrame('Import Reservoir Parameters', width=0.2, height=0.2, style={'display': 'flex', 'flexDirection': 'column'})

importButton = Create(CButton, {'name': 'importButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Choose file'})
sheetInput = Create(CInput, {'name': 'sheetInput', 'placeholder': 'Sheet'})
rangeInput = Create(CInput, {'name': 'rangeInput', 'placeholder': 'Range'})

importFrame.aChild(importButton)
importFrame.aChild(sheetInput)
importFrame.aChild(rangeInput)

reservoirParametersFrame = CFrame('Reservoir Parameters', width=1.0, height=0.02 * (res.len() + 2))

reservoirParametersContainer = Create(CContainer, {'name': 'reservoirParametersContainer', 'style': {'display': 'flex', 'flexDirection': 'row'}})

assetsContainer = Create(CContainer, {'name': 'assetsContainer', 'style': {'width': '15%', 'display': 'flex', 'flexDirection': 'column'}})

assetsTitle = Create(CText, {'name': 'assetsTitle', 'text': 'Asset'})

assetsContainer.aChild(assetsTitle)

assetsChecklist = Create(CChecklist, {'name': 'assetsChecklist', 'options': curList.getList(), 'labelClassName': labelClassName,
                                      'labelStyle': {'marginBottom': str((mx - 1) * 22) + 'px', 'margin-left': '40px'}})

assetsContainer.aChild(assetsChecklist)

reservoirsContainer = Create(CContainer, {'name': 'reservoirContainer', 'style': {'width': '15%', 'display': 'flex', 'flexDirection': 'column'}})

reservoirsTitle = Create(CText, {'name': 'reservoirsTitle', 'text': 'Reservoir'})

reservoirsContainer.aChild(reservoirsTitle)

i = 0
while (i < res.len()):
    margin = 0
    tmp = Create(CText, {'name': 'tmp-' + str(i), 'text': res.get(i), 'style': {'marginTop': '0px', 'marginBottom': '13px'}})
    reservoirsContainer.aChild(tmp)
    i = i + 1

hydroplantTable = Create(CDataTable, {'name': 'hydroplantTable', 'editable' : True, 'row_selectable': False, 'sortable': False, 'filterable': False,
                                      'headers': ['Start level [m3]', 'End level [m3]', 'Inflow Deviation [%]', 'Half life [d]'], 'min_height': 35 * (res.len() + 1) + 10,
                                      'style': {'width': '70%', 'height': '50vh', 'marginTop': '1px'},
                                      'rows': rows.getList(),})

reservoirParametersContainer.aChild(assetsContainer)
reservoirParametersContainer.aChild(reservoirsContainer)
reservoirParametersContainer.aChild(hydroplantTable)

reservoirParametersFrame.aChild(reservoirParametersContainer)

buttonsContainer = Create(CContainer, {'name': 'buttonscontainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '100%'}})

importButton = Create(CButton, {'name': 'importButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Import'})
backButton = Create(CButton, {'name': 'backButton', 'link': '/d/DisplayScreen@screen=index&asset=Alperia-VSM',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Back'})

buttonsContainer.aChild(importButton)
buttonsContainer.aChild(backButton)

myScreen = CPage('Scenario Manager')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

myScreen.aChild(optimizingHorizonFrame)
myScreen.aChild(timeGranularityFrame)
myScreen.aChild(performanceSettingsFrame)
myScreen.aChild(scenarioSettingsFrame)
myScreen.aChild(importFrame)
myScreen.aChild(reservoirParametersFrame)
myScreen.aChild(buttonsContainer)

return myScreen


