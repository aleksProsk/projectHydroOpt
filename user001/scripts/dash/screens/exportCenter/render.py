log.print("starting renderer")

assetsFrame = CFrame('Assets', width=0.2, height=0.35, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

assetsSelectList = Create(CSelectList, {'name': 'assetsSelectList', 'labels': ['1', '2'],
                                    'containerStyle': {'display': 'flex', 'flexDirection': 'column', 'width': '93%', 'background': 'rgb(245, 245, 245)', 'margin-top': '5%'},
                                    'labelStyle': {'background': 'rgb(245, 245, 245)', 'width': '100%', 'border': '1px solid black', 'color': 'black', 'padding': '5px 0 5px 5px'},
                                    'selectedLabelStyle': {'background': '#AAA', 'width': '100%', 'border': '1px solid black', 'color': 'white', 'padding': '5px 0 5px 5px'}})
aggregatedDropdown = Create(CDropdown, {'name': 'aggregatedDropdown',
                                        'options': [{'label': 'Aggregated', 'value': 'Aggregated',},
                                                    {'label': 'Separated', 'value': 'Separated',},
                                                    ],
                                        'value': 'Separated',
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

assetsFrame.aChild(assetsSelectList)
assetsFrame.aChild(aggregatedDropdown)

moduleSelectorFrame = CFrame('Module Selector', width = 0.4, height=0.05, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

moduleSelectorDropdown = Create(CDropdown, {'name': 'moduleSelectorDropdown',
                                        'options': [{'label': 'Scheduler', 'value': 'Scheduler',},
                                                    {'label': 'Scenario Manager', 'value': 'Scenario Manager',},
                                                    ],
                                        'value': 'Scenario Manager',
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

moduleSelectorFrame.aChild(moduleSelectorDropdown)

fileFormatFrame = CFrame('File Format', width = 0.4, height=0.05, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

fileFormatDropdown = Create(CDropdown, {'name': 'fileFormatDropdown',
                                        'options': [{'label': 'Excel', 'value': 'Excel',},
                                                    {'label': 'MAT', 'value': 'MAT',},
                                                    {'label': 'CSV', 'value': 'CSV'},
                                                    ],
                                        'value': 'Excel',
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

fileFormatFrame.aChild(fileFormatDropdown)

timeSeriesFrame = CFrame('Time Series Mean', width = 0.4, height=0.3, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
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
                                        'value': ['Reservoir Level', 'Inflow', 'Spill', 'Flow', 'Turbine Operation', 'Pump Operation', 'Market Price',],
                                        'multi': True,
                                        'style': {'width': '100%'},
                            })

timeSeriesFrame.aChild(timeSeriesDropdown)

resultsPerScenarioFrame = CFrame('Results per Scenario', width = 0.4, height=0.3, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

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
                                        'value': ['Revenue/Energy', 'Revenue/Energy monthly'],
                                        'multi': True,
                                        'style': {'width': '100%'},
                                    })
logInformationSelectList = Create(CSelectList, {'name': 'logInformationSelectList',
                                            'labels': ['Log Information'],
                                    'containerStyle': {'display': 'flex', 'flexDirection': 'column', 'width': '93%', 'background': 'rgb(245, 245, 245)', 'margin-top': '5%'},
                                    'labelStyle': {'background': 'rgb(245, 245, 245)', 'width': '100%', 'border': '1px solid black', 'color': 'black', 'padding': '5px 0 5px 5px'},
                                    'selectedLabelStyle': {'background': '#AAA', 'width': '100%', 'border': '1px solid black', 'color': 'white', 'padding': '5px 0 5px 5px'}})

resultsPerScenarioFrame.aChild(resultsPerScenarioDropdown)
resultsPerScenarioFrame.aChild(logInformationSelectList)

exportHorizonFrame = CFrame('exportHorizonFrame', width=0.2, height=0.1)

datePicker = Create(CDatePickerRange, {'name': 'datePicker', 'minDate': (1995, 1, 1), 'maxDate': (2050, 12, 31), 'startDate': (2025, 10, 1), 'endDate': (2031, 10, 1)})

exportHorizonFrame.aChild(datePicker)

resolutionMeanResultsFrame = CFrame('Resolution Mean Results', width=0.2, height=0.1, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

resolutionMeanResultsDropdown = Create(CDropdown, {'name': 'resolutionMeanResultsDropdown',
                                        'options': [{'label': 'hourly', 'value': 'hourly',},
                                                    {'label': 'daily', 'value': 'daily',},
                                                    {'label': 'weekly', 'value': 'weekly'},
                                                    {'label': 'monthly', 'value': 'monthly'},
                                                    ],
                                        'value': 'hourly',
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

resolutionMeanResultsFrame.aChild(resolutionMeanResultsDropdown)

unitFrame = CFrame('Unit', width=0.125, height=0.1)

unitDropdown = Create(CDropdown, {'name': 'unitDropdown',
                                        'options': [{'label': 'MWh', 'value': 'MWh',},
                                                    {'label': 'm3', 'value': 'm3',},
                                                    ],
                                        'value': 'MWh',
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

unitFrame.aChild(unitDropdown)

formatFrame = CFrame('Format', width=0.125, height=0.1)

formatDropdown = Create(CDropdown, {'name': 'formatDropdown',
                                        'options': [{'label': 'Autoformat', 'value': 'Autoformat',},
                                                    {'label': 'Round', 'value': 'Autoformat',},
                                                    ],
                                        'value': 'Autoformat',
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

formatFrame.aChild(formatDropdown)

fileSelectionFrame = CFrame('Folder / File Selection')

tempText = Create(CText, {'name': 'tempText', 'text': '???'})

fileSelectionFrame.aChild(tempText)

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
myScreen.aChild(fileSelectionFrame)
myScreen.aChild(buttonsContainer)

return myScreen


