log.print("starting renderer")

hydroptModel = globalDict.get('hydroptModel')

assetsFrame = CFrame('Assets', width=0.5, height=0.25)



myScreen = CPage('Modeller')

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

myScreen.aChild(myGraphModal)
myScreen.aChild(myTableModal)

return myScreen


