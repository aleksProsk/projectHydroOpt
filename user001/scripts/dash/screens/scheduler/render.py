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
if int(hydroptModel.Scheduler.ReservoirInputType) == 1:
    typ = 'End Level'
elif int(hydroptModel.Scheduler.ReservoirInputType) == 2:
    typ = 'Level Difference'
else:
    typ = 'Water Value'
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
tval = CSafeList()
if hydroptModel.Scheduler.UseSpills == 1:
    tval.append('Spills')
if hydroptModel.Scheduler.UseConstraints == 1:
    tval.append('Min. Hours')
if hydroptModel.Scheduler.UseCosts == 1:
    tval.append('SU/SD Costs')
if hydroptModel.Scheduler.UseMinRunningFlow == 1:
    tval.append('Min RunPower')
if hydroptModel.Scheduler.UseInfiltrationLosses == 1:
    tval.append('Infil. Losses')
if hydroptModel.Scheduler.UseProductionReserves == 1:
    tval.append('Prod. reserves')
if hydroptModel.Scheduler.UseConsumptionReserves == 1:
    tval.append('Cons. reserves')
if hydroptModel.Scheduler.UseSpinningProductionReserves == 1:
    tval.append('Sp. prod. reserves')
if hydroptModel.Scheduler.UseSpinningConsumptionReserves == 1:
    tval.append('Sp. cons. reserves')
if hydroptModel.Scheduler.UseEngineAlternatives == 1:
    tval.append('Engine alternatives')
if hydroptModel.Scheduler.UseDynFlowCalc == 1:
    tval.append('Dyn flow calc')
if hydroptModel.Scheduler.UseFullNewton == 1:
    tval.append('Full newton')
StartYear = int(hydroptModel.Scheduler.StartYear)
StartMonth = int(hydroptModel.Scheduler.StartMonth)
StartDay = int(hydroptModel.Scheduler.StartDay)
EndYear = int(hydroptModel.Scheduler.EndYear)
EndMonth = int(hydroptModel.Scheduler.EndMonth)
EndDay =  int(hydroptModel.Scheduler.EndDay)

optimizingHorizonFrame = CFrame('Optimizing Horizon', width=0.4, height=0.2)

datePicker = Create(CDatePickerRange, {'name': 'datePicker', 'minDate': (1995, 1, 1), 'maxDate': (2050, 12, 31), 'startDate': (StartYear, StartMonth, StartDay), 'endDate': (EndYear, EndMonth, EndDay)})

optimizingHorizonFrame.aChild(datePicker)

performanceSettingsFrame = CFrame('Performance Settings', width=0.3, height=0.2)

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
                                        'style': {'width': '100%'},
                                        'placeholder': 'Choose performance settings'
                                    })

performanceSettingsFrame.aChild(performanceSettingsDropdown)

priceFrame = CFrame('Price', width=0.3, height=0.2)

priceButton = Create(CButton, {'name': 'priceButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Choose file'})

priceFrame.aChild(priceButton)

reservoirInputTypeFrame = CFrame('Reservoir Input Type', width=0.5, height=0.1)

reservoirInputTypeDropdown = Create(CDropdown, {'name': 'reservoirInputTypeDropdown',
                                        'options': [{'label': 'End Level', 'value': 'End Level',},
                                                    {'label': 'Level Difference', 'value': 'Level Difference',},
                                                    {'label': 'Water Value', 'value': 'Water Value',},
                                                    ],
                                        'value': typ,
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

reservoirInputTypeFrame.aChild(reservoirInputTypeDropdown)

importFrame = CFrame('Import Reservoir Parameters', width=0.5, height=0.1, style={'display': 'flex', 'flexDirection': 'column'})

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

myScreen = CPage('Scheduler')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

myScreen.aChild(optimizingHorizonFrame)
myScreen.aChild(performanceSettingsFrame)
myScreen.aChild(priceFrame)
myScreen.aChild(reservoirInputTypeFrame)
myScreen.aChild(importFrame)
myScreen.aChild(reservoirParametersFrame)
myScreen.aChild(buttonsContainer)

return myScreen


