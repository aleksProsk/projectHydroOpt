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
    shortname = hydroptModel.Asset.Shortname
    name = hydroptModel.Asset.Name
    pricePath = hydroptModel.Price.ExpectedSpotPriceFile
    assets = CSafeList([hydroptModel.Asset])
else:
    shortnames = CSafeList(CSafeList(lst=hydroptModel.Asset.Shortname).get(0))
    shortname = CSafeList(CSafeList(lst=hydroptModel.Asset.Shortname).get(0)).get(0)
    name = CSafeList(CSafeList(lst=hydroptModel.Asset.Name).get(0)).get(0)
    pricePath = hydroptModel.Price.ExpectedSpotPriceFile
    assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
dropdownList = CSafeList()
drag = CSafeList()
lat = CSafeList()
lon = CSafeList()
i = 0
i = 0
while i < shortnames.len():
    tDict = CSafeDict(dct={})
    tDict.set('label', str(i + 1) + ' ' + shortnames.get(i))
    tDict.set('value', shortnames.get(i))
    dropdownList.append(tDict.getDict())
    drag.append(True)
    pos = CSafeList(CSafeList(assets.get(i).Position).get(0))
    if pos.get(0) < 1.0:
        pos.set(0, latList.get(i))
    if pos.get(1) < 1.0:
        pos.set(1, lonList.get(i))
    lat.append(pos.get(0))
    lon.append(pos.get(1))
    i = i + 1

assetsFrame = CFrame('Assets', width=0.5, height=0.32)

mainMap = Create(CYMap, {'name': 'mainMap', 'style': {'width': '100%', 'height': '60vh'},
                         'names': shortnames.getList(), 'lat': lat.getList(), 'lon': lon.getList(), 'draggable': drag.getList()})

assetsFrame.aChild(mainMap)

assetFrame = CFrame('Asset', width=0.5, height=0.32)

assetContent = Create(CContainer, {'name': 'assetContent', 'style': {'display': 'flex', 'flexDirection': 'column', 'padding': '1vh 1vw 1vh 1vw'}})

numberContainer = Create(CContainer, {'name': 'numberContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'width': '100%'}})

numberText = Create(CText, {'name': 'numberText', 'text': 'Number', 'style': {'width': '30%'}})

numberDropdown = Create(CDropdown, {'name': 'numberDropdown',
                                        'options': dropdownList.getList(),
                                        'value': dropdownList.get(0).get('value'),
                                        'multi': False,
                                        'clearable': False,
                                        'placeholder': 'Select asset',
                                        'style': {'width': '60%'},
                                    })
updateNumberDropdownButton = Create(CButton, {'name': 'updateNumberDropdownButton',
                                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                                      'fontSize': '0.7vmax', 'width': '5vw'},
                                            'text': 'Update'})

numberContainer.aChild(numberText)
numberContainer.aChild(numberDropdown)
numberContainer.aChild(updateNumberDropdownButton)

nameContainer = Create(CContainer, {'name': 'nameContainer', 'style': {'display': 'flex', 'flexDirectipn': 'row', 'width': '100%'}})

nameText = Create(CText, {'name': 'nameText', 'text': 'Name', 'style': {'width': '30%'}})
nameInput = Create(CInput, {'name': 'nameInput', 'value': name, 'placeholder': 'Name', 'style': {'width': '70%'}})

nameContainer.aChild(nameText)
nameContainer.aChild(nameInput)

shortNameContainer = Create(CContainer, {'name': 'shortNameContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'width': '100%'}})

shortNameText = Create(CText, {'name': 'shortNameText', 'text': 'Short Name', 'style': {'width': '30%'}})
shortNameInput = Create(CInput, {'name': 'shortNameInput', 'value': shortname, 'placeholder': 'Short Name', 'style': {'width': '70%'}})

shortNameContainer.aChild(shortNameText)
shortNameContainer.aChild(shortNameInput)

assetTypeContainer = Create(CContainer, {'name': 'assetTypeContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'width': '100%'}})

assetTypeText = Create(CText, {'name': 'assetTypeText', 'text': 'Asset Type', 'style': {'width': '30%'}})
assetTypeDropdown = Create(CDropdown, {'name': 'assetTypeDropdown', 'value': 'Hydroplant', 'multi': False, 'clearable': False,
                                       'options': [{'label': 'Hydroplant', 'value': 'Hydroplant'},
                                                   {'label': 'Option', 'value': 'Option'}],
                                       'style': {'width': '70%'}})

assetTypeContainer.aChild(assetTypeText)
assetTypeContainer.aChild(assetTypeDropdown)

assetButtonsContainer = Create(CContainer, {'name': 'assetButtonscontainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '100%'}})

defineButton = Create(CButton, {'name': 'defineButton', 'link': '/d/DisplayScreen@screen=defineTopology',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '15vw'},
                            'text': 'Define Topology'})
optimizationParametersButton = Create(CButton, {'name': 'optimizationParametersButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '15vw'},
                            'text': 'Optimization Parameters'})

assetButtonsContainer.aChild(defineButton)
assetButtonsContainer.aChild(optimizationParametersButton)

assetPositionContainer = Create(CContainer, {'name': 'assetPositionContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'width': '100%'}})

tmpText = Create(CText, {'name': 'tmpText', 'text': 'HERE WOULD BE SOMETHING'})

assetPositionContainer.aChild(tmpText)

assetControlsContainer = Create(CContainer, {'name': 'assetControlsContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'width': '100%'}})

newButton = Create(CButton, {'name': 'newButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '7vw'},
                            'text': 'New'})
copyButton = Create(CButton, {'name': 'copyButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '7vw'},
                            'text': 'Copy'})
removeButton = Create(CButton, {'name': 'removeButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '7vw'},
                            'text': 'Remove'})

assetControlsContainer.aChild(newButton)
assetControlsContainer.aChild(copyButton)
assetControlsContainer.aChild(removeButton)

poolText = Create(CText, {'name': 'poolText', 'text': 'Pool of assets', 'style': {'fontSize': '24px', 'marginTop': '2%'}})

poolContainer = Create(CContainer, {'name': 'poolContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'width': '100%', 'justifyContent': 'space-between'}})

poolAssetsDropdown = Create(CDropdown, {'name': 'poolAssetsDropdown',
                                        'options': dropdownList.getList(),
                                        'value': [],
                                        'multi': True,
                                        'clearable': True,
                                        'placeholder': 'Select assets',
                                        'style': {'width': '60%'},})

poolButton = Create(CButton, {'name': 'poolButton',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'width': '10vw'},
                            'text': 'Define constraints'})

poolContainer.aChild(poolAssetsDropdown)
poolContainer.aChild(poolButton)

assetContent.aChild(numberContainer)
assetContent.aChild(nameContainer)
assetContent.aChild(shortNameContainer)
assetContent.aChild(assetTypeContainer)
assetContent.aChild(assetButtonsContainer)
assetContent.aChild(assetPositionContainer)
assetContent.aChild(assetControlsContainer)
assetContent.aChild(poolText)
assetContent.aChild(poolContainer)

assetFrame.aChild(assetContent)

priceFrame = CFrame('Price', width=1.0, height=0.3)

priceContent = Create(CContainer, {'name': 'priceContent', 'style': {'display': 'flex', 'flexDirection': 'row', 'padding': '1vh 1vw 1vh 1vw'}})

chartContainer = Create(CContainer, {'name': 'chartContainer', 'style': {'display': 'flex', 'flexDirection': 'column', 'width': '40%'}})

priceChart = Create(CChart, {'name': 'priceChart', 'title': '', 'style': {'width': '650', 'height': '500'},
                          'rows': [], 'headers': [], 'rowCaptions': [], 'type': 'line','showLegend': 'False'})
chartButtons = Create(CContainer, {'name': 'chartButtons', 'style': {'display': 'flex', 'flexDirection': 'row', 'width': '100%', 'justifyContent': 'space-between'}})

chartOpen = Create(CButton, {'name': 'chartOpen',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Graph'})
chartTable = Create(CButton, {'name': 'chartTable',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'width': '10vw'},
                            'text': 'Open Data Table'})

chartButtons.aChild(chartOpen)
chartButtons.aChild(chartTable)

chartContainer.aChild(priceChart)
chartContainer.aChild(chartButtons)

priceControls = Create(CContainer, {'name': 'priceControls', 'style': {'display': 'flex', 'flexDirection': 'column', 'width': '50%'}})

forwardCurveContainer = Create(CContainer, {'name': 'forwardCurveContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'width': '100%'}})

forwardCurveText = Create(CText, {'name': 'forwardCurveText', 'text': 'Forward Curve', 'style': {'width': '30%'}})
forwardCurveInput = Create(CInput, {'name': 'forwardCurveInput', 'value': pricePath, 'placeholder': 'Forward Curve path', 'style': {'width': '70%'}})

forwardCurveContainer.aChild(forwardCurveText)
forwardCurveContainer.aChild(forwardCurveInput)

priceScenariosContainer = Create(CContainer, {'name': 'priceScenariosContainer', 'style': {'display': 'flex', 'flexDirection': 'row', 'width': '100%'}})

priceScenariosText = Create(CText, {'name': 'priceScenariosText', 'text': 'Price Scenarios', 'style': {'width': '30%'}})
priceScenariosInput = Create(CInput, {'name': 'priceScenariosInput', 'placeholder': 'Price Scenarios path', 'style': {'width': '70%'}})

priceScenariosContainer.aChild(priceScenariosText)
priceScenariosContainer.aChild(priceScenariosInput)

generatePriceScenariosButton = Create(CButton, {'name': 'generatePriceScenariosButton', 'link': '/d/DisplayScreen@screen=generatePriceScenarios',
                            'style': {'backgroundColor': 'white', 'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
                                      'fontSize': '0.7vmax', 'marginTop': '1vh', 'marginLeft': '30%', 'width': '15vw'},
                            'text': 'Generate Price Scenarios'})

displayDatePicker = Create(CDatePickerRange, {'name': 'displayDatePicker', 'minDate': (1995, 1, 1), 'maxDate': (2050, 12, 31), 'startDate': (2017, 11, 1), 'endDate': (2023, 4, 1)})

priceControls.aChild(forwardCurveContainer)
priceControls.aChild(priceScenariosContainer)
priceControls.aChild(generatePriceScenariosButton)
priceControls.aChild(displayDatePicker)

priceContent.aChild(chartContainer)
priceContent.aChild(priceControls)

priceFrame.aChild(priceContent)

myScreen = CPage('Modeller')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)

myGraphModal = Create(CModal, {'name': 'myGraphModal'})

modalCloser = Create(CText, {'name': 'modalCloser', 'text': 'Close', 'style': {'font-size': '28px', 'color': '#F2F2F2', 'margin-bottom': '1vh', 'font-weight': 'bold', 'left': '73%',
                                                                                'position': 'fixed', 'top': '7%'}})
myGraphModal.aChild(modalCloser)

modalContent = Create(CContainer, {'name': 'modalContent', 'style': {'background-color': '#F2F2F2', 'padding': '20px', 'border': '1px solid #888', 'width': '50%', 'position': 'fixed',
                                                                     'left': '25%', 'top': '12%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}})

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
myScreen.aChild(assetFrame)
myScreen.aChild(priceFrame)
myScreen.aChild(myGraphModal)
myScreen.aChild(myTableModal)

return myScreen


