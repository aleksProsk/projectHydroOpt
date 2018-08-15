log.print("starting renderer")

batchesFrame = CFrame('Batches', width=0.6, height=0.25, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

chooseBatchContainer = Create(CContainer, {'name': 'chooseNatchContainer', 'style': {'display': ' flex', 'flexDirection': 'row', 'margin': '3% 0 1% 0', 'justifyContent': 'space-between',
                                                                                     'padding': '0 3% 0 3%', 'width': '80%'}})

chooseBatchText = Create(CText, {'name': 'chooseBatchText', 'text': 'Choose Batch'})
chooseBatchDropdown = Create(CDropdown, {'name': 'chooseBatchDropdown',
                                         'options': [{'label': 'first', 'value': 'first',},
                                                     {'label': 'second', 'value': 'second',},
                                                     {'label': 'third', 'value': 'third',},
                                                     ],
                                         'value': '',
                                         'multi':False,
                                         'placeholder':'Choose Batch',
                                         'style': {'width': '50%'}})

chooseBatchContainer.aChild(chooseBatchText)
chooseBatchContainer.aChild(chooseBatchDropdown)

batchesFrame.aChild(chooseBatchContainer)

nameContainer = Create(CContainer, {'name': 'nameContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'margin-bottom': '1%', 'justifyContent': 'space-between', 'width': '80%'}})

nameText = Create(CText, {'name': 'nameText', 'text': 'Name'})
nameInput = Create(CInput, {'name': 'nameInput', 'style': {'width': '50%'}})

nameContainer.aChild(nameText)
nameContainer.aChild(nameInput)

batchesFrame.aChild(nameContainer)

openModel = Create(CButton, {'name': 'openModel', 'text': 'Choose Model',
                             'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '30vw'}})

batchesFrame.aChild(openModel)

mySelectList = Create(CSelectList, {'name': 'mySelectList', 'labels': ['Import Reservoir Levels', 'Export Results', 'Overwrite existing files', 'Skip infeasible solutions',
                                                                       'Disable Export if warnings occur in optimization'],
                                    'containerStyle': {'display': 'flex', 'flexDirection': 'column', 'width': '93%', 'background': 'rgb(245, 245, 245)', 'margin-top': '5%'},
                                    'labelStyle': {'background': 'rgb(245, 245, 245)', 'width': '100%', 'border': '1px solid black', 'color': 'black', 'padding': '5px 0 5px 5px'},
                                    'selectedLabelStyle': {'background': '#AAA', 'width': '100%', 'border': '1px solid black', 'color': 'white', 'padding': '5px 0 5px 5px'}})

batchesFrame.aChild(mySelectList)

batchSequenceFrame = CFrame('Batch Sequence', width=0.4, height=0.25, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})

mySelectList1 = Create(CSelectList, {'name': 'mySelectList1', 'labels': ['1', '2', '3'],
                                    'containerStyle': {'display': 'flex', 'flexDirection': 'column', 'width': '93%', 'background': 'rgb(245, 245, 245)', 'margin-top': '5%'},
                                    'labelStyle': {'background': 'rgb(245, 245, 245)', 'width': '100%', 'border': '1px solid black', 'color': 'black', 'padding': '5px 0 5px 5px'},
                                    'selectedLabelStyle': {'background': '#AAA', 'width': '100%', 'border': '1px solid black', 'color': 'white', 'padding': '5px 0 5px 5px'}})

batchSequenceFrame.aChild(mySelectList1)

activateButton = Create(CButton, {'name': 'activateButton', 'text': 'Activate Batch Sequence',
                                  'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '35vw'}})

batchSequenceFrame.aChild(activateButton)

buttonsContainer = Create(CContainer, {'name': 'buttonsContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'flex-end', 'width': '100%'}})

backButton = Create(CButton, {'name': 'backButton', 'text': 'Back', 'link': '/d/DisplayScreen@screen=index&asset=Alperia-VSM',
                              'style': {'backgroundColor': 'white',
                                        'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                        'fontSize': '0.7vmax', 'margin': '1vh 0 1vh 0', 'width': '35vw'}})

buttonsContainer.aChild(backButton)

myScreen = CPage('Batch Manager')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

myScreen.aChild(batchesFrame)
myScreen.aChild(batchSequenceFrame)
myScreen.aChild(buttonsContainer)

return myScreen


