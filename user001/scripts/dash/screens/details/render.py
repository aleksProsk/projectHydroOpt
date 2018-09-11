log.print("starting renderer")

if globalDict.contains('hydroptModel'):
    hydroptModel = globalDict.get('hydroptModel')
else:
    hydroptModel = hydropt.getData('model')
    globalDict.set('hydroptModel', hydroptModel)
if hydroptModel.nAssets == 1:
    assets = CSafeList([hydroptModel.Asset])
else:
    assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
assetName = args.get('asset')
i = 0
pos = -1
while (i < assets.len()):
    if assets.get(i).Shortname == args.get('asset'):
        pos = i
        break
    i = i + 1
octave.eval("NoSchedulerResults = isempty(Data.Asset("+str(pos+1)+").Scheduler.Result) | isempty(Data.Asset("+str(pos+1)+").Reservoir(1).Scheduler.Result) | isempty(Data.Asset("+str(pos+1)+").Engine(1).Scheduler.Result);")
octave.eval("NoScenarioWaterManagerResults = isempty(Data.Asset("+str(pos+1)+").ScenarioWaterManager.Result) | isempty(Data.Asset("+str(pos+1)+").Reservoir(1).ScenarioWaterManager.Result) | isempty(Data.Asset("+str(pos+1)+").Engine(1).ScenarioWaterManager.Result);")
NoSchedulerResults = octave.pull("NoSchedulerResults")
NoScenarioWaterManagerResults = octave.pull("NoScenarioWaterManagerResults")
resultsSelectionOptions = CSafeList()
if NoSchedulerResults == 0:
    resultsSelectionOptions.append({'label': 'Scheduler', 'value': 'Scheduler'})
if NoScenarioWaterManagerResults == 0:
    resultsSelectionOptions.append({'label': 'Scenario Manager - Engines', 'value': 'Engines'})
    resultsSelectionOptions.append({'label': 'Scenario Manager - Value & Risk', 'value': 'valueAndRisk'})
resultsSelectionValue = ''
if resultsSelectionOptions.len() > 0:
    resultsSelectionValue = resultsSelectionOptions.get(0)
types = CSafeList()
x = CSafeList()
y = CSafeList()
names_r = CSafeList()
names_t = CSafeList()
names_p = CSafeList()
names_f = CSafeList()
names = CSafeList()
if assets.get(pos).Topology.nRes != 0:
    if assets.get(pos).Topology.nRes == 1:
        reservoirs = CSafeList([assets.get(pos).Reservoir])
    else:
        reservoirs = CSafeList(CSafeList(assets.get(pos).Reservoir).get(0))
    j = 0
    while (j < reservoirs.len()):
        names_r.append(reservoirs.get(j).Shortname)
        names.append(reservoirs.get(j).Shortname)
        j = j + 1
if assets.get(pos).Topology.nFlows != 0:
    if assets.get(pos).Topology.nFlows == 1:
        flows = CSafeList([assets.get(pos).Flow])
    else:
        flows = CSafeList(CSafeList(assets.get(pos).Flow).get(0))
    j = 0
    while (j < flows.len()):
        names_f.append(flows.get(j).Shortname)
        names.append(flows.get(j).Shortname)
        j = j + 1
if assets.get(pos).Topology.nTurbines != 0:
    if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
        turbines = CSafeList([assets.get(pos).Engine])
    else:
        turbines = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
    j = 0
    while (j < int(assets.get(pos).Topology.nTurbines)):
        names_t.append(turbines.get(j).Shortname)
        names.append(turbines.get(j).Shortname)
        j = j + 1
if assets.get(pos).Topology.nPumps != 0:
    if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
        pumps = CSafeList([assets.get(pos).Engine])
    else:
        pumps = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
    j = int(assets.get(pos).Topology.nTurbines)
    while (j < pumps.len()):
        names_p.append(pumps.get(j).Shortname)
        names.append(pumps.get(j).Shortname)
        j = j + 1
operatesFrom = CSafeList()
operatesTo = CSafeList()
j = 0
if assets.get(pos).Topology.nRes != 0:
    if assets.get(pos).Topology.nRes == 1:
        reservoirs = CSafeList([assets.get(pos).Topology.Reservoir])
    else:
        reservoirs = CSafeList(CSafeList(assets.get(pos).Topology.Reservoir).get(0))
    while (j < assets.get(pos).Topology.nRes):
        types.append('reservoir')
        coords = CSafeList(CSafeList(reservoirs.get(j).Btn).get(0))
        x.append(coords.get(0))
        y.append(coords.get(1))
        if reservoirs.get(j).SpillsToRes == 0:
            operatesTo.append('null')
        else:
            operatesTo.append(names_r.get(int(reservoirs.get(j).SpillsToRes) - 1))
        operatesFrom.append('null')
        j = j + 1
if assets.get(pos).Topology.nFlows != 0:
    if assets.get(pos).Topology.nFlows == 1:
        flows = CSafeList([assets.get(pos).Topology.Flow])
    else:
        flows = CSafeList(CSafeList(assets.get(pos).Topology.Flow).get(0))
    j = 0
    while (j < flows.len()):
        types.append('flow')
        coords = CSafeList(CSafeList(flows.get(j).Btn).get(0))
        x.append(coords.get(0))
        y.append(coords.get(1))
        if flows.get(j).OperatesFrom == 0:
            operatesFrom.append('null')
        else:
            operatesFrom.append(names_r.get(int(flows.get(j).OperatesFrom) - 1))
        if flows.get(j).OperatesTo == 0:
            operatesTo.append('null')
        else:
            operatesTo.append(names_r.get(int(flows.get(j).OperatesTo) - 1))
        j = j + 1
if assets.get(pos).Topology.nTurbines != 0:
    if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
        turbines = CSafeList([assets.get(pos).Topology.Engine])
    else:
        turbines = CSafeList(CSafeList(assets.get(pos).Topology.Engine).get(0))
    j = 0
    while (j < int(assets.get(pos).Topology.nTurbines)):
        types.append('turbine')
        coords = CSafeList(CSafeList(turbines.get(j).Btn).get(0))
        x.append(coords.get(0))
        y.append(coords.get(1))
        if turbines.get(j).OperatesFrom == 0:
            operatesFrom.append('null')
        else:
            operatesFrom.append(names_r.get(int(turbines.get(j).OperatesFrom) - 1))
        if turbines.get(j).OperatesTo == 0:
            operatesTo.append('null')
        else:
            operatesTo.append(names_r.get(int(turbines.get(j).OperatesTo) - 1))
        j = j + 1
if assets.get(pos).Topology.nPumps != 0:
    if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
        pumps = CSafeList([assets.get(pos).Topology.Engine])
    else:
        pumps = CSafeList(CSafeList(assets.get(pos).Topology.Engine).get(0))
    j = int(assets.get(pos).Topology.nTurbines)
    while (j < pumps.len()):
        types.append('pump')
        coords = CSafeList(CSafeList(pumps.get(j).Btn).get(0))
        x.append(coords.get(0))
        y.append(coords.get(1))
        if pumps.get(j).OperatesFrom == 0:
            operatesFrom.append('null')
        else:
            operatesFrom.append(names_r.get(int(pumps.get(j).OperatesFrom) - 1))
        if pumps.get(j).OperatesTo == 0:
            operatesTo.append('null')
        else:
            operatesTo.append(names_r.get(int(pumps.get(j).OperatesTo) - 1))
        j = j + 1

resultSelectionFrame = CFrame('Result Selection', width=0.25, height=0.18)

resultsSelectionDropdown = Create(CDropdown, {'name': 'resultsSelectionDropdown',
                                        'options': resultsSelectionOptions.getList(),
                                        'value': resultsSelectionValue,
                                        'multi': False,
                                        'clearable': False,
                                        'placeholder': 'No results for asset',
                                        'style': {'width': '100%'},
                                    })

resultSelectionFrame.aChild(resultsSelectionDropdown)

summaryFrame = CFrame('Summary', width=0.25, height=0.18)

summaryTurbines = Create(CButton, {'name': 'summaryTurbines',
                                   'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                                   'text': 'Turbines'})
summaryRevenues = Create(CButton, {'name': 'summaryRevenues',
                                   'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                                   'text': 'Revenues'})
summaryPumps = Create(CButton, {'name': 'summaryPumps',
                                   'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                                   'text': 'Pumps'})
summaryPrices = Create(CButton, {'name': 'summaryPrices',
                                   'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                                   'text': 'Prices'})
summaryReservoirs = Create(CButton, {'name': 'summaryReservoirs',
                                   'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                                   'text': 'Reservoirs'})
summaryLosses = Create(CButton, {'name': 'summaryLosses',
                                   'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                                   'text': 'Losses'})
summaryInflows = Create(CButton, {'name': 'summaryInflows',
                                   'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                                   'text': 'Inflows'})

summaryFrame.aChild(summaryTurbines)
summaryFrame.aChild(summaryRevenues)
summaryFrame.aChild(summaryPumps)
summaryFrame.aChild(summaryPrices)
summaryFrame.aChild(summaryReservoirs)
summaryFrame.aChild(summaryLosses)
summaryFrame.aChild(summaryInflows)

calcParametersFrame = CFrame('Calculation Parameters', width=0.5, height=0.18)

calcParametersTable = Create(CDataTable, {'name': 'calcParametersTable', 'editable' : False, 'row_selectable': False, 'sortable': False, 'filterable': False,
                                      'headers': [''], 'min_height': 320, 'style': {'width': '70%', 'height': '50vh', 'marginTop': '1px'}, 'rows': [['']],})

calcParametersFrame.aChild(calcParametersTable)

topologyFrame = CFrame('Topology', width=0.5, height=0.4)

topology = Create(CTopology, {'name': 'topology', 'style': {'width': '800px', 'height': '450px'},
                              'types': types.getList(),
                              'names': names.getList(),
                              'x': x.getList(),
                              'y': y.getList(),
                              'operatesFrom': operatesFrom.getList(),
                              'operatesTo': operatesTo.getList()})

topologyFrame.aChild(topology)

resultsFrame = CFrame('Results', width=0.5, height=0.3)

resultGraph = Create(CContainer, {'name': 'resultGraph', 'style': {'display': 'flex', 'flexDirection': 'column', 'flexBasis': '70%', 'justifyContent': 'center', 'alignItems': 'center'}})

resultGraphFigure = Create(CChart, {'name': 'resultGraphFigure', 'title': '', 'style': {'width': '550', 'height': '400'},
                          'rows': [], 'headers': [], 'rowCaptions': [], 'showLegend': 'False'})

text1 = Create(CText, {'name': 'text1', 'text': '', 'style': {'display': 'none', 'marginTop': '2%'}})
text2 = Create(CText, {'name': 'text2', 'text': '', 'style': {'display': 'none', 'marginTop': '0'}})

resultGraphButtons = Create(CContainer, {'name': 'resultGraphButtons', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%'}})

resultOpen = Create(CButton, {'name': 'resultOpen',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Graph'})
resultTable = Create(CButton, {'name': 'resultTable',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Data Table'})

resultGraphButtons.aChild(resultOpen)
resultGraphButtons.aChild(resultTable)

resultGraph.aChild(resultGraphFigure)
resultGraph.aChild(text1)
resultGraph.aChild(text2)
resultGraph.aChild(resultGraphButtons)

resultsFrame.aChild(resultGraph)

myScreen = CPage('Results')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

myGraphModal = Create(CModal, {'name': 'myGraphModal'})

modalCloser = Create(CText, {'name': 'modalCloser', 'text': 'Close', 'style': {'font-size': '28px', 'color': '#F2F2F2', 'margin-bottom': '1vh', 'font-weight': 'bold', 'left': '70%',
                                                                                'position': 'fixed', 'top': '15%'}})
myGraphModal.aChild(modalCloser)

modalContent = Create(CContainer, {'name': 'modalContent', 'style': {'background-color': '#F2F2F2', 'padding': '20px', 'border': '1px solid #888', 'width': '45%', 'position': 'fixed',
                                                                     'left': '27.5%', 'top': '20%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}})

modalGraph = Create(CChart, {'name': 'modalGraph'})

modalContent.aChild(modalGraph)

myGraphModal.aChild(modalContent)

myTableModal = Create(CModal, {'name': 'myTableModal'})

modalCloser1 = Create(CText, {'name': 'modalCloser1', 'text': 'Close', 'style': {'font-size': '28px', 'color': '#F2F2F2', 'margin-bottom': '1vh', 'font-weight': 'bold', 'left': '67%',
                                                                                'position': 'fixed', 'top': '15%'}})
myTableModal.aChild(modalCloser1)

modalContent1 = Create(CContainer, {'name': 'modalContent1', 'style': {'background-color': '#F2F2F2', 'padding': '20px', 'border': '1px solid #888', 'width': '40%', 'position': 'fixed',
                                                                     'left': '30%', 'top': '20%', 'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'justify-content': 'center'}})

modalTable = Create(CDataTable, {'name': 'modalTable', 'row_selectable': False, 'style': {'width': '100%', 'height': '100%'}})

saveButton = Create(CButton, {'name': 'saveButton', 'download': 'table.csv',
                              'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                              'text': 'Save Table'})

modalContent1.aChild(modalTable)
modalContent1.aChild(saveButton)

myTableModal.aChild(modalContent1)

hiddenText = Create(CText, {'name': 'hiddenText', 'text': args.get('asset'), 'style': {'display': 'none'}})
myScreen.aChild(hiddenText)

hiddenButton = Create(CButton, {'name': 'hiddenButton', 'style': {'display': 'none'}})
myScreen.aChild(hiddenButton)

myScreen.aChild(resultSelectionFrame)
myScreen.aChild(summaryFrame)
myScreen.aChild(calcParametersFrame)
myScreen.aChild(topologyFrame)
myScreen.aChild(resultsFrame)
myScreen.aChild(myGraphModal)
myScreen.aChild(myTableModal)

return myScreen


