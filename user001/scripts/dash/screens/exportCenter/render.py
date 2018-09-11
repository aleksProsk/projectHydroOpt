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
curValuesList = CSafeList()
while (i < assets.len()):
    tDict = CSafeDict({'label': str(i) + ' - ' + assets.get(i).Name, 'value': assets.get(i).Shortname})
    curList.append(tDict.getDict())
    if assets.get(i).Export.Check == 1:
        curValuesList.append(assets.get(i).Shortname)
    i = i + 1
timeSeriesList = CSafeList()
if hydroptModel.Export.ReservoirLevel == 1:
    timeSeriesList.append('Reservoir Level')
if hydroptModel.Export.Inflow == 1:
    timeSeriesList.append('Inflow')
if hydroptModel.Export.Spill == 1:
    timeSeriesList.append('Spill')
if hydroptModel.Export.Flow == 1:
    timeSeriesList.append('Flow')
if hydroptModel.Export.InfiltrationLoss == 1:
    timeSeriesList.append('Infiltration Loss')
if hydroptModel.Export.Turbine == 1:
    timeSeriesList.append('Turbine Operation')
if hydroptModel.Export.Pump == 1:
    timeSeriesList.append('Pump Operation')
if hydroptModel.Export.Price == 1:
    timeSeriesList.append('Market Price')
if hydroptModel.Export.MarginPriceTS == 1:
    timeSeriesList.append('Margin Price')
if hydroptModel.Export.WaterValueTS == 1:
    timeSeriesList.append('Water Value')
if hydroptModel.Export.ReservoirConstraints == 1:
    timeSeriesList.append('Reservoir constraints')
if hydroptModel.Export.EngineConstraints == 1:
    timeSeriesList.append('Engine constraints')
resultsPerScenarioList = CSafeList()
if hydroptModel.Export.MarginPrices == 1:
    resultsPerScenarioList.append('Margin Prices')
if hydroptModel.Export.WaterValues == 1:
    resultsPerScenarioList.append('Water Values')
if hydroptModel.Export.Revenues == 1:
    resultsPerScenarioList.append('Revenue/Energy')
if hydroptModel.Export.RevenuesMonthly == 1:
    resultsPerScenarioList.append('Revenue/Energy monthly')
if hydroptModel.Export.RevenuesEngine == 1:
    resultsPerScenarioList.append('Revenue/Energy per Engine')
if hydroptModel.Export.RevenuesEngineMonthly == 1:
    resultsPerScenarioList.append('Revenue/Energy full detail')
if hydroptModel.Export.ReservoirUsage == 1:
    resultsPerScenarioList.append('Reservoir Usage')
if hydroptModel.Export.ReserveRevenues == 1:
    resultsPerScenarioList.append('Reserve Revenue')

assetsFrame = CFrame('Assets', width=0.2, height=0.35, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

assetsChecklist = Create(CChecklist, {'name': 'assetsChecklist', 'options': curList.getList(), 'value': curValuesList.getList(),
                                      'labelStyle': {'margin-top': '5px', 'margin-bottom': '5px', 'margin-left': '40px'}})

aggregatedValue = 'Aggregated'
if hydroptModel.Export.Separated == 1:
    aggregatedValue = 'Separated'
aggregatedDropdown = Create(CDropdown, {'name': 'aggregatedDropdown',
                                        'options': [{'label': 'Aggregated', 'value': 'Aggregated',},
                                                    {'label': 'Separated', 'value': 'Separated',},
                                                    ],
                                        'value': aggregatedValue,
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

assetsFrame.aChild(assetsChecklist)
assetsFrame.aChild(aggregatedDropdown)

moduleSelectorFrame = CFrame('Module Selector', width = 0.2, height=0.08, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

moduleSelectorValue = 'Scenario Manager'
if hydroptModel.Export.Scheduler == 1:
    moduleSelectorValue = 'Scheduler'
moduleSelectorDropdown = Create(CDropdown, {'name': 'moduleSelectorDropdown',
                                        'options': [{'label': 'Scheduler', 'value': 'Scheduler',},
                                                    {'label': 'Scenario Manager', 'value': 'Scenario Manager',},
                                                    ],
                                        'value': moduleSelectorValue,
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

moduleSelectorFrame.aChild(moduleSelectorDropdown)

fileFormatFrame = CFrame('File Format', width = 0.2, height=0.08, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

fileFormatValue = 'Excel'
if hydroptModel.Export.CSV == 1:
    fileFormatValue = 'CSV'
if hydroptModel.Export.MAT == 1:
    fileFormatValue = 'MAT'
fileFormatDropdown = Create(CDropdown, {'name': 'fileFormatDropdown',
                                        'options': [{'label': 'Excel', 'value': 'Excel',},
                                                    {'label': 'MAT', 'value': 'MAT',},
                                                    {'label': 'CSV', 'value': 'CSV'},
                                                    ],
                                        'value': fileFormatValue,
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

fileFormatFrame.aChild(fileFormatDropdown)

timeSeriesFrame = CFrame('Time Series Mean', width = 0.2, height=0.14, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
timeSeriesDropdown = Create(CDropdown, {'name': 'timeSeriesDropdown',
                                        'options': [{'label': 'Reservoir Level', 'value': 'Reservoir Level',},
                                                    {'label': 'Inflow', 'value': 'Inflow',},
                                                    {'label': 'Spill', 'value': 'Spill',},
                                                    {'label': 'Flow', 'value': 'Flow',},
                                                    {'label': 'Infiltration Loss', 'value': 'Infiltration Loss',},
                                                    {'label': 'Turbine Operation', 'value': 'Turbine Operation',},
                                                    {'label': 'Pump Operation', 'value': 'Pump Operation',},
                                                    {'label': 'Market Price', 'value': 'Market Price',},
                                                    {'label': 'Margin Price', 'value': 'Margin Price',},
                                                    {'label': 'Water Value', 'value': 'Water Value',},
                                                    {'label': 'Reservoir constraints', 'value': 'Reservoir constraints',},
                                                    {'label': 'Engine constraints', 'value': 'Engine constraints',},
                                                    ],
                                        'value': timeSeriesList.getList(),
                                        'multi': True,
                                        'style': {'width': '100%'},
                            })

timeSeriesFrame.aChild(timeSeriesDropdown)

resultsPerScenarioFrame = CFrame('Results per Scenario', width = 0.2, height=0.14, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

resultsPerScenarioDropdown = Create(CDropdown, {'name': 'resultsPerScenarioDropdown',
                                        'options': [{'label': 'Margin Prices', 'value': 'Margin Prices',},
                                                    {'label': 'Water Values', 'value': 'Water Values',},
                                                    {'label': 'Revenue/Energy', 'value': 'Revenue/Energy',},
                                                    {'label': 'Revenue/Energy monthly', 'value': 'Revenue/Energy monthly',},
                                                    {'label': 'Revenue/Energy per Engine', 'value': 'Revenue/Energy per Engine',},
                                                    {'label': 'Revenue/Energy full detail', 'value': 'Revenue/Energy full detail',},
                                                    {'label': 'Reservoir Usage', 'value': 'Reservoir Usage',},
                                                    {'label': 'Reserve Revenue', 'value': 'Reserve Revenue',},
                                                    ],
                                        'value': resultsPerScenarioList.getList(),
                                        'multi': True,
                                        'style': {'width': '100%'},
                                    })

resultsPerScenarioFrame.aChild(resultsPerScenarioDropdown)

exportHorizonFrame = CFrame('Export Horizon', width=0.2, height=0.2)

StartYear = int(hydroptModel.Export.StartYear)
StartMonth = int(hydroptModel.Export.StartMonth)
StartDay = int(hydroptModel.Export.StartDay)
EndYear = int(hydroptModel.Export.EndYear)
EndMonth = int(hydroptModel.Export.EndMonth)
EndDay = int(hydroptModel.Export.EndDay)
datePicker = Create(CDatePickerRange, {'name': 'datePicker', 'minDate': (1995, 1, 1), 'maxDate': (2050, 12, 31), 'startDate': (StartYear, StartMonth, StartDay), 'endDate': (EndYear, EndMonth, EndDay)})

exportHorizonFrame.aChild(datePicker)

resolutionMeanResultsFrame = CFrame('Resolution Mean Results', width=0.15, height=0.1, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

resolutionMeanResultsValue = 'hourly'
if hydroptModel.Export.daily == 1:
    resolutionMeanResultsValue = 'daily'
if hydroptModel.Export.weekly == 1:
    resolutionMeanResultsValue = 'weekly'
if hydroptModel.Export.monthly == 1:
    resolutionMeanResultsValue = 'monthly'
resolutionMeanResultsDropdown = Create(CDropdown, {'name': 'resolutionMeanResultsDropdown',
                                        'options': [{'label': 'hourly', 'value': 'hourly',},
                                                    {'label': 'daily', 'value': 'daily',},
                                                    {'label': 'weekly', 'value': 'weekly'},
                                                    {'label': 'monthly', 'value': 'monthly'},
                                                    ],
                                        'value': resolutionMeanResultsValue,
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

resolutionMeanResultsFrame.aChild(resolutionMeanResultsDropdown)

unitFrame = CFrame('Unit', width=0.125, height=0.1)

unitValue = 'MWh'
if hydroptModel.Export.M3 == 1:
    unitValue = 'm3'
unitDropdown = Create(CDropdown, {'name': 'unitDropdown',
                                        'options': [{'label': 'MWh', 'value': 'MWh',},
                                                    {'label': 'm3', 'value': 'm3',},
                                                    ],
                                        'value': unitValue,
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

unitFrame.aChild(unitDropdown)

formatFrame = CFrame('Format', width=0.125, height=0.1)

formatValue = 'Autoformat'
if hydroptModel.Export.Round == 1:
    formatValue = 'Round'
formatDropdown = Create(CDropdown, {'name': 'formatDropdown',
                                        'options': [{'label': 'Autoformat', 'value': 'Autoformat',},
                                                    {'label': 'Round', 'value': 'Round',},
                                                    ],
                                        'value': formatValue,
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

formatFrame.aChild(formatDropdown)

folderFileSelectionFrame = CFrame('Folder/File Selection', width=0.15, height=0.1)

folderInput = Create(CInput, {'name': 'folderInput', 'value': 'exportResults', 'placeholder': 'Select folder', 'style': {'width': '100%'}})
fileInput = Create(CInput, {'name': 'fileInput', 'value': 'res', 'placeholder': 'Select file name', 'style': {'width': '100%'}})

folderFileSelectionFrame.aChild(folderInput)
folderFileSelectionFrame.aChild(fileInput)

buttonsContainer = Create(CContainer, {'name': 'buttonsContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '100%'}})

exportButton = Create(CButton, {'name': 'exportButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Export'})
backButton = Create(CButton, {'name': 'backButton', 'link': '/d/DisplayScreen@screen=index&asset=Alperia-VSM',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Back'})

buttonsContainer.aChild(exportButton)
buttonsContainer.aChild(backButton)

myScreen = CPage('Export Center')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

myScreen.aChild(assetsFrame)
myScreen.aChild(moduleSelectorFrame)
myScreen.aChild(fileFormatFrame)
myScreen.aChild(timeSeriesFrame)
myScreen.aChild(resultsPerScenarioFrame)
myScreen.aChild(exportHorizonFrame)
myScreen.aChild(resolutionMeanResultsFrame)
myScreen.aChild(unitFrame)
myScreen.aChild(formatFrame)
myScreen.aChild(folderFileSelectionFrame)
myScreen.aChild(buttonsContainer)

return myScreen


