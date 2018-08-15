log.print("starting renderer")

hedgeSettingsFrame = CFrame('Hedge Settings', width=0.5, height=0.5)

hedgeSettingsDropdown = Create(CDropdown, {'name': 'hedgeSettingsDropdown',
                                        'options': [{'label': 'Zero Hedge', 'value': 'Zero Hedge',},
                                                    {'label': '100% of Energy', 'value': '100% of Energy',},
                                                    {'label': '90% of Energy', 'value': '90% of Energy',},
                                                    {'label': '50% of Energy', 'value': '50% of Energy',},
                                                    ],
                                        'value': '100% of Energy',
                                        'multi': False,
                                        'clearable': True,
                                        'style': {'width': '100%'},
                                    })
currentHedgeButton = Create(CButton, {'name': 'currentHedgeButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Choose current hedge file'})
datePicker = Create(CDatePickerRange, {'name': 'datePicker', 'minDate': (1995, 1, 1), 'maxDate': (2050, 12, 31), 'startDate': (2025, 10, 1), 'endDate': (2031, 10, 1)})

hedgeSettingsFrame.aChild(hedgeSettingsDropdown)
hedgeSettingsFrame.aChild(currentHedgeButton)
hedgeSettingsFrame.aChild(datePicker)

assetFrame = CFrame('Asset', width=0.5, height=0.5)

assetsList = Create(CSelectList, {'name': 'assetsList', 'labels': ['KWO', 'KWO2'],
                                    'containerStyle': {'display': 'flex', 'flexDirection': 'column', 'width': '20%', 'background': 'rgb(245, 245, 245)', 'padding-left': '5%'},
                                    'labelStyle': {'background': 'rgb(245, 245, 245)', 'width': '100%', 'border': '1px solid black', 'color': 'black', 'padding': '5px 0 5px 5px'},
                                    'selectedLabelStyle': {'background': '#AAA', 'width': '100%', 'border': '1px solid black', 'color': 'white', 'padding': '5px 0 5px 5px'}
                            })

assetFrame.aChild(assetsList)

buttonsContainer = Create(CContainer, {'name': 'buttonscontainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '100%'}})

startButton = Create(CButton, {'name': 'startButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Import'})
backButton = Create(CButton, {'name': 'backButton', 'link': '/d/DisplayScreen@screen=index&asset=Alperia-VSM',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Back'})

buttonsContainer.aChild(startButton)
buttonsContainer.aChild(backButton)

myScreen = CPage('Hedge Decomposer')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

myScreen.aChild(hedgeSettingsFrame)
myScreen.aChild(assetFrame)
myScreen.aChild(buttonsContainer)

return myScreen


