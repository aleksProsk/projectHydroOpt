log.print("starting renderer")

latList = CSafeList([46.563371, 46.183447, 46.067888, 46.623189, 46.080639, 46.137034, 46.481873, 46.461194, 46.371179, 46.070118, 46.145847, 46.169434, 46.5782776, 47.229296, 47.369007])
lonList = CSafeList([8.9612593, 7.2491351, 6.9303941, 10.1909703, 7.4023168, 7.5696649, 9.4516843, 8.3680963, 8.0014061, 6.8762443, 6.9671043, 8.1199813, 9.1179484, 7.5880925, 7.9783607])

if globalDict.contains('hydroptModel'):
    hydroptModel = globalDict.get('hydroptModel')
else:
    hydroptModel = hydropt.getData('model')
    globalDict.set('hydroptModel', hydroptModel)
if hydroptModel.nAssets == 1:
    shortnames = CSafeList([hydroptModel.Asset.Shortname])
    assets = CSafeList([hydroptModel.Asset])
else:
    shortnames = CSafeList(CSafeList(lst=hydroptModel.Asset.Shortname).get(0))
    assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
dropdownList = CSafeList()
drag = CSafeList()
lat = CSafeList()
lon = CSafeList()
dropdownValue = CSafeList();
i = 0
i = 0
while i < shortnames.len():
    tDict = CSafeDict(dct={})
    tDict.set('label', shortnames.get(i))
    tDict.set('value', shortnames.get(i))
    dropdownList.append(tDict.getDict())
    drag.append(False)
    pos = CSafeList(CSafeList(assets.get(i).Position).get(0))
    if assets.get(i).MainFig.Check == 1.0:
        dropdownValue.append(shortnames.get(i))
    if pos.get(0) < 1.0:
        pos.set(0, latList.get(i))
    if pos.get(1) < 1.0:
        pos.set(1, lonList.get(i))
    lat.append(pos.get(0))
    lon.append(pos.get(1))
    i = i + 1

assetsFrame = CFrame('Assets', width=0.4, height=0.25)

#mainMap = Create(CMap, {'name': 'mainMap', 'style': {'width': '37%', 'marginLeft': '0.75vw'}})
mainMap = Create(CYMap, {'name': 'mainMap', 'style': {'width': '100%', 'height': '45vh'},
                         'names': shortnames.getList(), 'lat': lat.getList(), 'lon': lon.getList(), 'draggable': drag.getList()})

assetsFrame.aChild(mainMap)

controlFrame = CFrame('Control', width=0.2, height=0.25, style={'display': 'flex', 'flexDirection': 'column'})

modellerButton = Create(CButton, {'name': 'modellerButton', 'link': '/d/DisplayScreen@screen=modeller',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Modeller'})
scenarioManagerButton = Create(CButton, {'name': 'scenarioManagerButton', 'link': '/d/DisplayScreen@screen=scenarioManager',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Scenario Manager'})
schedulerButton = Create(CButton, {'name': 'schedulerButton', 'link': '/d/DisplayScreen@screen=scheduler',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Scheduler'})
exportCenterButton = Create(CButton, {'name': 'exportCenterButton', 'link': '/d/DisplayScreen@screen=exportCenter',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Export Center'})
batchManagerButton = Create(CButton, {'name': 'batchManagerButton', 'link': '/d/DisplayScreen@screen=batchManager',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Batch Manager'})
partnerButton = Create(CButton, {'name': 'partnerButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Partnerwerk manager'})
liveUpdatesButton = Create(CButton, {'name': 'liveUpdatesButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Live updates'})
greeksButton = Create(CButton, {'name': 'greeksButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Greeks'})

controlFrame.aChild(modellerButton)
controlFrame.aChild(scenarioManagerButton)
controlFrame.aChild(schedulerButton)
controlFrame.aChild(exportCenterButton)
controlFrame.aChild(batchManagerButton)
controlFrame.aChild(partnerButton)
controlFrame.aChild(liveUpdatesButton)
controlFrame.aChild(greeksButton)

revenueAndRiskFrame = CFrame('Revenue and Risk', width=0.4, height=0.25)

revenueAndRiskContent = Create(CContainer, {'name': 'revenueAndRiskContent', 'style': {'display': 'flex', 'flexDirection': 'row'}})

revenueAndRiskText = Create(CContainer, {'name': 'revenueAndRiskText', 'style': {'display': 'flex', 'flexDirection': 'column', 'marginLeft': '1vw', 'flexBasis': '30%'}})

startDateTitle = Create(CText, {'name': 'startDateTitle', 'text': 'Start Date', 'style': {'margin-left': '0', 'margin-bottom': '0'}})
startDate = Create(CText, {'name': 'startDate', 'text': '', 'style': {'margin-left': '0', 'margin-top': '0'}})

endDateTitle = Create(CText, {'name': 'endDateTitle', 'text': 'End Date', 'style': {'margin-left': '0', 'margin-bottom': '0'}})
endDate = Create(CText, {'name': 'endDate', 'text': '', 'style': {'margin-left': '0', 'margin-top': '0'}})

averageRevenueTitle = Create(CText, {'name': 'averageRevenueTitle', 'text': 'Average Revenue', 'style': {'margin-left': '0', 'margin-bottom': '0'}})
averageRevenue = Create(CText, {'name': 'averageRevenue', 'text': '697.93 Mio. EUR', 'style': {'margin-left': '0', 'margin-top': '0'}})

minimumRevenueTitle = Create(CText, {'name': 'minimumRevenueTitle', 'text': 'Minimum Revenue (95%)', 'style': {'margin-left': '0', 'margin-bottom': '0'}})
minimumRevenue = Create(CText, {'name': 'minimumRevenue', 'text': '697.93 Mio. EUR', 'style': {'margin-left': '0', 'margin-top': '0'}})

revenueAndRiskText.aChild(startDateTitle)
revenueAndRiskText.aChild(startDate)
revenueAndRiskText.aChild(endDateTitle)
revenueAndRiskText.aChild(endDate)
revenueAndRiskText.aChild(averageRevenueTitle)
revenueAndRiskText.aChild(averageRevenue)
revenueAndRiskText.aChild(minimumRevenueTitle)
revenueAndRiskText.aChild(minimumRevenue)

revenueAndRiskContent.aChild(revenueAndRiskText)

revenueAndRiskGraph = Create(CContainer, {'name': 'revenueAndRiskGraph', 'style': {'display': 'flex', 'flexDirection': 'column', 'flexBasis': '70%', 'justifyContent': 'center', 'alignItems': 'center'}})

revenueAndRiskGraphFigure = Create(CHist, {'name': 'revenueAndRiskGraphFigure', 'title': '', 'style': {'width': '400', 'height': '400'},
                          'x': [], 'xAxis': 'Revenue Hedged [Mio. EUR]', 'yAxis': 'Scenarios', 'showlegend': 'False'})

revenueAndRiskGraphButtons = Create(CContainer, {'name': 'revenueAndRiskGraphButtons', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%'}})

revenueAndRiskOpen = Create(CButton, {'name': 'revenueAndRiskOpen',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Graph'})
revenueAndRiskTable = Create(CButton, {'name': 'revenueAndRiskTable',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Data Table'})

revenueAndRiskGraphButtons.aChild(revenueAndRiskOpen)
revenueAndRiskGraphButtons.aChild(revenueAndRiskTable)

revenueAndRiskGraph.aChild(revenueAndRiskGraphFigure)
revenueAndRiskGraph.aChild(revenueAndRiskGraphButtons)

revenueAndRiskContent.aChild(revenueAndRiskGraph)

revenueAndRiskFrame.aChild(revenueAndRiskContent)

displayFrame = CFrame('Display', width=0.1, height=0.41)

displayDropdown = Create(CDropdown, {'name': 'displayDropdown',
                                        'options': dropdownList.getList(),
                                        'value': dropdownValue.getList(),
                                        'multi': True,
                                        'clearable': True,
                                        'placeholder': 'Select assets',
                                        'style': {'width': '100%'},
                                    })

displayFrame.aChild(displayDropdown)

currentPowerFrame = CFrame('Current Power [MW]', width=0.3, height=0.2)

currentPowerGraph = Create(CContainer, {'name': 'currentPowerGraph', 'style': {'display': 'flex', 'flexDirection': 'column', 'flexBasis': '70%', 'justifyContent': 'center', 'alignItems': 'center'}})

currentPowerGraphFigure = Create(CChart, {'name': 'currentPowerGraphFigure', 'title': '', 'style': {'width': '450', 'height': '300'},
                          'rows': [], 'headers': [], 'rowCaptions': [], 'showLegend': 'False'})

currentPowerGraphButtons = Create(CContainer, {'name': 'currentPowerGraphButtons', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%'}})

currentPowerOpen = Create(CButton, {'name': 'currentPowerOpen',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Graph'})
currentPowerTable = Create(CButton, {'name': 'currentPowerTable',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Data Table'})

currentPowerGraphButtons.aChild(currentPowerOpen)
currentPowerGraphButtons.aChild(currentPowerTable)

currentPowerGraph.aChild(currentPowerGraphFigure)
currentPowerGraph.aChild(currentPowerGraphButtons)

currentPowerFrame.aChild(currentPowerGraph)

powerPlanningFrame = CFrame('Power Planning [MW]', width=0.3, height=0.2)

powerPlanningGraph = Create(CContainer, {'name': 'powerPlanningGraph', 'style': {'display': 'flex', 'flexDirection': 'column', 'flexBasis': '70%', 'justifyContent': 'center', 'alignItems': 'center'}})

powerPlanningGraphFigure = Create(CChart, {'name': 'powerPlanningGraphFigure', 'title': '', 'style': {'width': '450', 'height': '300'},
                          'rows': [], 'headers': [], 'rowCaptions': [], 'type': 'line','showLegend': 'False'})

powerPlanningGraphButtons = Create(CContainer, {'name': 'powerPlanningGraphButtons', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%'}})

powerPlanningOpen = Create(CButton, {'name': 'powerPlanningOpen',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Graph'})
powerPlanningTable = Create(CButton, {'name': 'powerPlanningTable',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Data Table'})

powerPlanningGraphButtons.aChild(powerPlanningOpen)
powerPlanningGraphButtons.aChild(powerPlanningTable)

powerPlanningGraph.aChild(powerPlanningGraphFigure)
powerPlanningGraph.aChild(powerPlanningGraphButtons)

powerPlanningFrame.aChild(powerPlanningGraph)

currentReservoirLevelFrame = CFrame('Current Reservoir Level [GVh]', width=0.3, height=0.2)

currentReservoirLevelGraph = Create(CContainer, {'name': 'currentReservoirLevelGraph', 'style': {'display': 'flex', 'flexDirection': 'column', 'flexBasis': '70%', 'justifyContent': 'center', 'alignItems': 'center'}})

currentReservoirLevelGraphFigure = Create(CChart, {'name': 'currentReservoirLevelGraphFigure', 'title': '', 'style': {'width': '450', 'height': '300'},
                          'rows': [], 'headers': [], 'rowCaptions': [], 'barmode': 'stack', 'showLegend': 'True'})

currentReservoirLevelGraphButtons = Create(CContainer, {'name': 'currentReservoirLevelGraphButtons', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%'}})

currentReservoirLevelOpen = Create(CButton, {'name': 'currentReservoirLevelOpen',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Graph'})
currentReservoirLevelTable = Create(CButton, {'name': 'currentReservoirLevelTable',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Data Table'})

currentReservoirLevelGraphButtons.aChild(currentReservoirLevelOpen)
currentReservoirLevelGraphButtons.aChild(currentReservoirLevelTable)

currentReservoirLevelGraph.aChild(currentReservoirLevelGraphFigure)
currentReservoirLevelGraph.aChild(currentReservoirLevelGraphButtons)

currentReservoirLevelFrame.aChild(currentReservoirLevelGraph)

marginPriceFrame = CFrame('Margin Price [EUR/MWh]', width=0.3, height=0.2)

marginPriceGraph = Create(CContainer, {'name': 'marginPriceGraph', 'style': {'display': 'flex', 'flexDirection': 'column', 'flexBasis': '70%', 'justifyContent': 'center', 'alignItems': 'center'}})

marginPriceGraphFigure = Create(CChart, {'name': 'marginPriceGraphFigure', 'title': '', 'style': {'width': '450', 'height': '300'},
                          'rows': [], 'headers': [], 'rowCaptions': [], 'showLegend': False})

marginPriceGraphButtons = Create(CContainer, {'name': 'marginPriceGraphButtons', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%'}})

marginPriceOpen = Create(CButton, {'name': 'marginPriceOpen',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Graph'})
marginPriceTable = Create(CButton, {'name': 'marginPriceTable',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Data Table'})

marginPriceGraphButtons.aChild(marginPriceOpen)
marginPriceGraphButtons.aChild(marginPriceTable)

marginPriceGraph.aChild(marginPriceGraphFigure)
marginPriceGraph.aChild(marginPriceGraphButtons)

marginPriceFrame.aChild(marginPriceGraph)

reservoirCycleFrame = CFrame('Reservoir Cycle [GWh]', width=0.3, height=0.2)

reservoirCycleGraph = Create(CContainer, {'name': 'reservoirCycleGraph', 'style': {'display': 'flex', 'flexDirection': 'column', 'flexBasis': '70%', 'justifyContent': 'center', 'alignItems': 'center'}})

reservoirCycleGraphFigure = Create(CChart, {'name': 'reservoirCycleGraphFigure', 'title': '', 'style': {'width': '450', 'height': '300'},
                          'rows': [], 'headers': [], 'rowCaptions': [], 'type': 'line',
                                                   'showLegend': False})

reservoirCycleGraphButtons = Create(CContainer, {'name': 'reservoirCycleGraphButtons', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%'}})

reservoirCycleOpen = Create(CButton, {'name': 'reservoirCycleOpen',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Graph'})
reservoirCycleTable = Create(CButton, {'name': 'reservoirCycleTable',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Data Table'})

reservoirCycleGraphButtons.aChild(reservoirCycleOpen)
reservoirCycleGraphButtons.aChild(reservoirCycleTable)

reservoirCycleGraph.aChild(reservoirCycleGraphFigure)
reservoirCycleGraph.aChild(reservoirCycleGraphButtons)

reservoirCycleFrame.aChild(reservoirCycleGraph)

energyPlanningPeakFrame = CFrame('Energy Planning Peak/Off-Peak [GWh]', width=0.3, height=0.2)

energyPlanningPeakGraph = Create(CContainer, {'name': 'reservoirCycleGraph', 'style': {'display': 'flex', 'flexDirection': 'column', 'flexBasis': '70%', 'justifyContent': 'center', 'alignItems': 'center'}})

energyPlanningPeakGraphFigure = Create(CChart, {'name': 'energyPlanningPeakGraphFigure', 'title': '', 'style': {'width': '450', 'height': '300'},
                          'rows': [], 'headers': [], 'rowCaptions': [], 'type': 'line', 'showLegend': False})

energyPlanningPeakGraphButtons = Create(CContainer, {'name': 'energyPlanningPeakGraphButtons', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%'}})

energyPlanningPeakOpen = Create(CButton, {'name': 'energyPlanningPeakOpen',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Graph'})
energyPlanningPeakTable = Create(CButton, {'name': 'energyPlanningPeakTable',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Data Table'})

energyPlanningPeakGraphButtons.aChild(energyPlanningPeakOpen)
energyPlanningPeakGraphButtons.aChild(energyPlanningPeakTable)

energyPlanningPeakGraph.aChild(energyPlanningPeakGraphFigure)
energyPlanningPeakGraph.aChild(energyPlanningPeakGraphButtons)

energyPlanningPeakFrame.aChild(energyPlanningPeakGraph)

myScreen = CPage('Overview')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

myGraphModal = Create(CModal, {'name': 'myGraphModal'})

modalCloser = Create(CText, {'name': 'modalCloser', 'text': 'Close', 'style': {'font-size': '28px', 'color': '#F2F2F2', 'margin-bottom': '1vh', 'font-weight': 'bold', 'left': '67%',
                                                                                'position': 'fixed', 'top': '15%'}})
myGraphModal.aChild(modalCloser)

modalContent = Create(CContainer, {'name': 'modalContent', 'style': {'background-color': '#F2F2F2', 'padding': '20px', 'border': '1px solid #888', 'width': '40%', 'position': 'fixed',
                                                                     'left': '30%', 'top': '20%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}})

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

myScreen.aChild(assetsFrame)
myScreen.aChild(controlFrame)
myScreen.aChild(revenueAndRiskFrame)
myScreen.aChild(displayFrame)
myScreen.aChild(currentPowerFrame)
myScreen.aChild(powerPlanningFrame)
myScreen.aChild(currentReservoirLevelFrame)
myScreen.aChild(marginPriceFrame)
myScreen.aChild(reservoirCycleFrame)
myScreen.aChild(energyPlanningPeakFrame)
myScreen.aChild(myGraphModal)
myScreen.aChild(myTableModal)

return myScreen


