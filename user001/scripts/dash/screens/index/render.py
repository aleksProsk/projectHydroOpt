log.print("starting renderer")

assetsFrame = CFrame('Assets', width=0.4, height=0.25)

mainMap = Create(CMap, {'name': 'mainMap', 'style': {'width': '37%', 'marginLeft': '0.75vw'}})

assetsFrame.aChild(mainMap)

controlFrame = CFrame('Control', width=0.2, height=0.25, style={'display': 'flex', 'flexDirection': 'column'})

modellerButton = Create(CButton, {'name': 'modellerButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Modeller'})
scenarioManagerButton = Create(CButton, {'name': 'scenarioManagerButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Scenario Manager'})
schedulerButton = Create(CButton, {'name': 'schedulerButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Scheduler'})
exportCenterButton = Create(CButton, {'name': 'exportCenterButton', 'link': '/d/DisplayScreen@screen=exportCenter&asset=Alperia-VSM',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Export Center'})
batchManagerButton = Create(CButton, {'name': 'batchManagerButton', 'link': '/d/DisplayScreen@screen=batchManager&asset=Alperia-VSM',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Batch Manager'})

controlFrame.aChild(modellerButton)
controlFrame.aChild(scenarioManagerButton)
controlFrame.aChild(schedulerButton)
controlFrame.aChild(exportCenterButton)
controlFrame.aChild(batchManagerButton)

revenueAndRiskFrame = CFrame('Revenue and Risk', width=0.4, height=0.25)

revenueAndRiskContent = Create(CContainer, {'name': 'revenueAndRiskContent', 'style': {'display': 'flex', 'flexDirection': 'row'}})

revenueAndRiskText = Create(CContainer, {'name': 'revenueAndRiskText', 'style': {'display': 'flex', 'flexDirection': 'column', 'marginLeft': '1vw', 'flexBasis': '30%'}})

startDateTitle = Create(CText, {'name': 'startDateTitle', 'text': 'Start Date', 'style': {'margin-left': '0', 'margin-bottom': '0'}})
startDate = Create(CText, {'name': 'startDate', 'text': '01-Oct-2025', 'style': {'margin-left': '0', 'margin-top': '0'}})

endDateTitle = Create(CText, {'name': 'endDateTitle', 'text': 'End Date', 'style': {'margin-left': '0', 'margin-bottom': '0'}})
endDate = Create(CText, {'name': 'endDate', 'text': '01-Oct-2031', 'style': {'margin-left': '0', 'margin-top': '0'}})

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

revenueAndRiskGraphFigure = Create(CChart, {'name': 'revenueAndRiskGraphFigure', 'title': '', 'style': {'width': '400', 'height': '400'},
                          'rows': [ [[1]] ], 'headers': ['Revenue And Risk'], 'rowCaptions': ['697.93'], 'xAxis': 'Revenue Hedged [Mio. EUR]', 'yAxis': 'Scenarios',
                                            'showLegend': 'False'})

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

mySelectList = Create(CSelectList, {'name': 'mySelectList', 'labels': ['All', '1', '2', '3'],
                                    'containerStyle': {'display': 'flex', 'flexDirection': 'column', 'width': '93%', 'background': 'rgb(245, 245, 245)', 'margin-top': '5%'},
                                    'labelStyle': {'background': 'rgb(245, 245, 245)', 'width': '100%', 'border': '1px solid black', 'color': 'black', 'padding': '5px 0 5px 5px'},
                                    'selectedLabelStyle': {'background': '#AAA', 'width': '100%', 'border': '1px solid black', 'color': 'white', 'padding': '5px 0 5px 5px'}})

displayFrame.aChild(mySelectList)

currentPowerFrame = CFrame('Current Power [MW]', width=0.3, height=0.2)

currentPowerGraph = Create(CContainer, {'name': 'currentPowerGraph', 'style': {'display': 'flex', 'flexDirection': 'column', 'flexBasis': '70%', 'justifyContent': 'center', 'alignItems': 'center'}})

currentPowerGraphFigure = Create(CChart, {'name': 'currentPowerGraphFigure', 'title': '', 'style': {'width': '450', 'height': '300'},
                          'rows': [ [[1000]] ], 'headers': ['Current Power'], 'rowCaptions': ['KWO'],
                                            'showLegend': 'False'})

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
                          'rows': [ [[1000, 1000]] ], 'headers': ['Current Power'], 'rowCaptions': [1, 10], 'type': 'line',
                                            'showLegend': 'False'})

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
                          'rows': [ [[560]], [[30]] ], 'headers': ['Current Reservoir Level', 'Maximum Reservoir Level'], 'rowCaptions': ['KWO'], 'barmode': 'stack',
                                                   'showLegend': 'True'})

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
                          'rows': [ [[160], [70], [65], [60], [55], [50]] ], 'headers': ['Gri2', 'H3H', 'Gri1Gri', 'H2', 'I1', 'Han1'], 'rowCaptions': ['Gri2', 'H3H', 'Gri1Gri', 'H2', 'I1', 'Han1'],
                                                   'showLegend': False})

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
                          'rows': [ [[1], [10]] ], 'headers': [''], 'rowCaptions': [2, 5], 'type': 'line',
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
                          'rows': [ [[1], [10]] ], 'headers': [''], 'rowCaptions': [2, 5], 'type': 'line',
                                                   'showLegend': False})

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

return myScreen


