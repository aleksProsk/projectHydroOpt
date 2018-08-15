log.print("starting renderer")

optimizingHorizonFrame = CFrame('Optimizing Horizon', width=0.4, height=0.2)

datePicker = Create(CDatePickerRange, {'name': 'datePicker', 'minDate': (1995, 1, 1), 'maxDate': (2050, 12, 31), 'startDate': (2025, 10, 1), 'endDate': (2031, 10, 1)})

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
                                        'value': ['Spills',],
                                        'multi': True,
                                        'style': {'width': '100%'},
                                    })

performanceSettingsFrame.aChild(performanceSettingsDropdown)

priceFrame = CFrame('Price', width=0.3, height=0.2)

priceButton = Create(CButton, {'name': 'priceButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Choose file'})

priceFrame.aChild(priceButton)

reservoirInputTypeFrame = CFrame('Reservoir Input Type', width=0.5, height=0.2)

reservoirInputTypeDropdown = Create(CDropdown, {'name': 'reservoirInputTypeDropdown',
                                        'options': [{'label': 'End Level', 'value': 'End Level',},
                                                    {'label': 'Level Difference', 'value': 'Level Difference',},
                                                    {'label': 'Water Value', 'value': 'Water Value',},
                                                    ],
                                        'value': ['End level',],
                                        'multi': True,
                                        'clearable': False,
                                        'style': {'width': '100%'},
                                    })

reservoirInputTypeFrame.aChild(reservoirInputTypeDropdown)

importFrame = CFrame('Import Reservoir Parameters', width=0.5, height=0.2, style={'display': 'flex', 'flexDirection': 'column'})

importButton = Create(CButton, {'name': 'importButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '1vmax', 'marginTop': '1vh', 'marginLeft': '1vw', 'marginRight': '1vw', 'width': '16vw'},
                            'text': 'Choose file'})
sheetInput = Create(CInput, {'name': 'sheetInput', 'placeholder': 'Sheet'})
rangeInput = Create(CInput, {'name': 'rangeInput', 'placeholder': 'Range'})

importFrame.aChild(importButton)
importFrame.aChild(sheetInput)
importFrame.aChild(rangeInput)

reservoirParametersFrame = CFrame('Reservoir Parameters', width=1.0, height=1.0)

reservoirParametersContainer = Create(CContainer, {'name': 'reservoirParametersContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'}})

hydroplantSelectList = Create(CSelectList, {'name': 'hydroplantSelectList', 'labels': ['KWO', 'All'],
                                    'containerStyle': {'display': 'flex', 'flexDirection': 'column', 'width': '20%', 'background': 'rgb(245, 245, 245)', 'marginTop': '1%', 'padding-left': '5%'},
                                    'labelStyle': {'background': 'rgb(245, 245, 245)', 'width': '100%', 'border': '1px solid black', 'color': 'black', 'padding': '5px 0 5px 5px',
                                                   'marginBottom': '70%'},
                                    'selectedLabelStyle': {'background': '#AAA', 'width': '100%', 'border': '1px solid black', 'color': 'white', 'padding': '5px 0 5px 5px',
                                                   'marginBottom': '70%'}
                            })

tableContainer = Create(CContainer, {'name': 'tableContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'width': '70%'}})

rowNames = Create(CContainer, {'name': 'rowNames', 'style': {'width': '15%', 'marginTop': '4.5%'}})

text1 = Create(CText, {'name': 'text1', 'text': 'Oberaarsee', 'style': {'marginBottom': '9%'}})
text2 = Create(CText, {'name': 'text2', 'text': 'Grimselsee', 'style': {'marginBottom': '9%'}})
text3 = Create(CText, {'name': 'text3', 'text': 'Gelmersee', 'style': {'marginBottom': '9%'}})
text4 = Create(CText, {'name': 'text4', 'text': 'Räterichsbodensee', 'style': {'marginBottom': '9%'}})
text5 = Create(CText, {'name': 'text5', 'text': 'AB Handeck', 'style': {'marginBottom': '9%'}})

rowNames.aChild(text1)
rowNames.aChild(text2)
rowNames.aChild(text3)
rowNames.aChild(text4)
rowNames.aChild(text5)

hydroplantTable = Create(CDataTable, {'name': 'hzdroplantTable', 'editable' : True, 'row_selectable': False, 'sortable': False, 'filterable': False,
                                      'rows': [[[''], [''], [''], [''], ['']], [[''], [''], [''], [''], ['']], [[''], [''], [''], [''], ['']], [[''], [''], [''], [''], ['']]],
                                      'headers': ['Start level [m3]', 'End level [m3]', 'Inflow Deviation [%]', 'Half life [d]'],
                                   'style': {'width': '65%', 'height': '50%', 'marginLeft': '1%', 'marginRight': '1%', 'marginTop': '1%'}})

tableContainer.aChild(rowNames)
tableContainer.aChild(hydroplantTable)

reservoirParametersContainer.aChild(hydroplantSelectList)
reservoirParametersContainer.aChild(tableContainer)

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


