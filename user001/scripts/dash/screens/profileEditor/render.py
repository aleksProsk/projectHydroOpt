log.print("starting renderer")

hedgeProfileEditorFrame = CFrame('Hedge Profile', width=1.0, height=0.3)

content = Create(CContainer, {'name': 'content', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'padding': '0 10% 0 10%'}})

left = Create(CContainer, {'name': 'left', 'style': {'display': 'flex', 'flexDirection': 'column', 'width': '40%'}})

profileContainer = Create(CContainer, {'name': 'profileContainer', 'style': {'display': 'flex', 'flex-direction': 'row', 'justifyContent': 'space-between'}})

profileText = Create(CText, {'name': 'profileText', 'text': 'Profile'})
profileDropdown = Create(CDropdown, {'name': 'profileDropdown',
                                        'options': [{'label': '1 Base Y', 'value': '1 Base Y',},
                                                    {'label': '2 Peak Y', 'value': '2 Peak Y',},
                                                    ],
                                        'value': '1 Base Y',
                                        'multi': False,
                                        'clearable': True,
                                        'placeholder': 'Select profile',
                                        'style': {'width': '50%'},
                            })

profileContainer.aChild(profileText)
profileContainer.aChild(profileDropdown)

nameContainer = Create(CContainer, {'name': 'nameContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'}})

nameText = Create(CText, {'name': 'nameText', 'text': 'Name'})
nameInput = Create(CInput, {'name': 'nameInput', 'placeholder': 'Name', 'style': {'width': '40%'}})

nameContainer.aChild(nameText)
nameContainer.aChild(nameInput)

controlsContainer = Create(CContainer, {'name': 'controlscontainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'}})

newButton = Create(CButton, {'name': 'newButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '8vw'},
                            'text': 'New'})
copyButton = Create(CButton, {'name': 'copyButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '8vw'},
                            'text': 'Copy'})
removeButton = Create(CButton, {'name': 'removeButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '8vw'},
                            'text': 'Remove'})

controlsContainer.aChild(newButton)
controlsContainer.aChild(copyButton)
controlsContainer.aChild(removeButton)

left.aChild(profileContainer)
left.aChild(nameContainer)
left.aChild(controlsContainer)

right = Create(CContainer, {'name': 'right', 'style': {'display': 'flex', 'flexDirection': 'column', 'width': '40%'}})

deliveryPeriodContainer = Create(CContainer, {'name': 'deliveryPeriodContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'}})

deliveryPeriodText = Create(CText, {'name': 'deliveryPeriodText', 'text': 'Delivery Period'})
deliveryPeriodDropdown = Create(CDropdown, {'name': 'deliveryPeriodDropdown',
                                        'options': [{'label': 'Year', 'value': 'Year',},
                                                    {'label': 'Quarter', 'value': 'Quarter',},
                                                    {'label': 'Month', 'value': 'Month',},
                                                    {'label': 'Week', 'value': 'Week',},
                                                    {'label': 'Day', 'value': 'Day',},
                                                    ],
                                        'value': 'Year',
                                        'multi': False,
                                        'clearable': False,
                                        'style': {'width': '50%'},
                            })

deliveryPeriodContainer.aChild(deliveryPeriodText)
deliveryPeriodContainer.aChild(deliveryPeriodDropdown)

tradingHorizonContainer = Create(CContainer, {'name': 'tradingHorizonContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'}})

tradingHorizonText = Create(CText, {'name': 'tradingHorizonText', 'text': 'Trading horizon [days]'})
tradingHorizonInput = Create(CInput, {'name': 'tradingHorizonInput', 'placeholder': 'Trading horizon', 'style': {'width': '40%'}})

tradingHorizonContainer.aChild(tradingHorizonText)
tradingHorizonContainer.aChild(tradingHorizonInput)

useInHedgingSelect = Create(CSelectList, {'name': 'useInHedgingSelect', 'labels': ['Use in Hedging'],
                                    'containerStyle': {'display': 'flex', 'flexDirection': 'column', 'width': '20%', 'background': 'rgb(245, 245, 245)', 'padding-left': '5%'},
                                    'labelStyle': {'background': 'rgb(245, 245, 245)', 'width': '100%', 'border': '1px solid black', 'color': 'black', 'padding': '5px 0 5px 5px'},
                                    'selectedLabelStyle': {'background': '#AAA', 'width': '100%', 'border': '1px solid black', 'color': 'white', 'padding': '5px 0 5px 5px'}
                            })

right.aChild(deliveryPeriodContainer)
right.aChild(tradingHorizonContainer)
right.aChild(useInHedgingSelect)

content.aChild(left)
content.aChild(right)

workDayContainer = Create(CContainer, {'name': 'workDaycontainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%', 'marginLeft': '10%'}})

workDayText = Create(CText, {'name': 'workDayText', 'text': 'Work Day'})
workDayDropdown = Create(CDropdown, {'name': 'workDayDropdown',
                                        'options': [{'label': '1', 'value': '1',}, {'label': '2', 'value': '2',}, {'label': '3', 'value': '3',}, {'label': '4', 'value': '4',},
                                                    {'label': '5', 'value': '5',}, {'label': '6', 'value': '6',}, {'label': '7', 'value': '7',}, {'label': '8', 'value': '8',},
                                                    {'label': '9', 'value': '9',}, {'label': '10', 'value': '10',}, {'label': '11', 'value': '11',}, {'label': '12', 'value': '12',},
                                                    {'label': '13', 'value': '13',}, {'label': '14', 'value': '14',}, {'label': '15', 'value': '15',}, {'label': '16', 'value': '16',},
                                                    {'label': '17', 'value': '17',}, {'label': '18', 'value': '18',}, {'label': '19', 'value': '19',}, {'label': '20', 'value': '20',},
                                                    {'label': '21', 'value': '21',}, {'label': '22', 'value': '22',}, {'label': '23', 'value': '23',}, {'label': '24', 'value': '24',},
                                                    ],
                                        'value': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
                                        'multi': True,
                                        'clearable': True,
                                        'placeholder': 'Hourly power pattern',
                                        'style': {'width': '90%'},
                            })

workDayContainer.aChild(workDayText)
workDayContainer.aChild(workDayDropdown)

saturdayContainer = Create(CContainer, {'name': 'saturdayContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%', 'marginLeft': '10%'}})

saturdayText = Create(CText, {'name': 'saturdayText', 'text': 'Saturday'})
saturdayDropdown = Create(CDropdown, {'name': 'saturdayDropdown',
                                        'options': [{'label': '1', 'value': '1',}, {'label': '2', 'value': '2',}, {'label': '3', 'value': '3',}, {'label': '4', 'value': '4',},
                                                    {'label': '5', 'value': '5',}, {'label': '6', 'value': '6',}, {'label': '7', 'value': '7',}, {'label': '8', 'value': '8',},
                                                    {'label': '9', 'value': '9',}, {'label': '10', 'value': '10',}, {'label': '11', 'value': '11',}, {'label': '12', 'value': '12',},
                                                    {'label': '13', 'value': '13',}, {'label': '14', 'value': '14',}, {'label': '15', 'value': '15',}, {'label': '16', 'value': '16',},
                                                    {'label': '17', 'value': '17',}, {'label': '18', 'value': '18',}, {'label': '19', 'value': '19',}, {'label': '20', 'value': '20',},
                                                    {'label': '21', 'value': '21',}, {'label': '22', 'value': '22',}, {'label': '23', 'value': '23',}, {'label': '24', 'value': '24',},
                                                    ],
                                        'value': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
                                        'multi': True,
                                        'clearable': True,
                                        'placeholder': 'Hourly power pattern',
                                        'style': {'width': '90%'},
                            })

saturdayContainer.aChild(saturdayText)
saturdayContainer.aChild(saturdayDropdown)

sundayContainer = Create(CContainer, {'name': 'sundayContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '80%', 'marginLeft': '10%'}})

sundayText = Create(CText, {'name': 'sundayText', 'text': 'Sunday'})
sundayDropdown = Create(CDropdown, {'name': 'sundayDropdown',
                                        'options': [{'label': '1', 'value': '1',}, {'label': '2', 'value': '2',}, {'label': '3', 'value': '3',}, {'label': '4', 'value': '4',},
                                                    {'label': '5', 'value': '5',}, {'label': '6', 'value': '6',}, {'label': '7', 'value': '7',}, {'label': '8', 'value': '8',},
                                                    {'label': '9', 'value': '9',}, {'label': '10', 'value': '10',}, {'label': '11', 'value': '11',}, {'label': '12', 'value': '12',},
                                                    {'label': '13', 'value': '13',}, {'label': '14', 'value': '14',}, {'label': '15', 'value': '15',}, {'label': '16', 'value': '16',},
                                                    {'label': '17', 'value': '17',}, {'label': '18', 'value': '18',}, {'label': '19', 'value': '19',}, {'label': '20', 'value': '20',},
                                                    {'label': '21', 'value': '21',}, {'label': '22', 'value': '22',}, {'label': '23', 'value': '23',}, {'label': '24', 'value': '24',},
                                                    ],
                                        'value': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
                                        'multi': True,
                                        'clearable': True,
                                        'placeholder': 'Hourly power pattern',
                                        'style': {'width': '90%'},
                            })

sundayContainer.aChild(sundayText)
sundayContainer.aChild(sundayDropdown)

hedgeProfileEditorFrame.aChild(content)
hedgeProfileEditorFrame.aChild(workDayContainer)
hedgeProfileEditorFrame.aChild(saturdayContainer)
hedgeProfileEditorFrame.aChild(sundayContainer)

buttonsContainer = Create(CContainer, {'name': 'buttonscontainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '100%'}})

okButton = Create(CButton, {'name': 'okButton', 'link': '/d/DisplayScreen@screen=index&asset=Alperia-VSM',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'OK'})
backButton = Create(CButton, {'name': 'backButton', 'link': '/d/DisplayScreen@screen=index&asset=Alperia-VSM',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Back'})

buttonsContainer.aChild(okButton)
buttonsContainer.aChild(backButton)

myScreen = CPage('Hedge Profile Editor')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

myScreen.aChild(hedgeProfileEditorFrame)
myScreen.aChild(buttonsContainer)

return myScreen


