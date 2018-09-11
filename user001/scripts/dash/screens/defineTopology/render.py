log.print("starting renderer")

if globalDict.contains('hydroptModel'):
    hydroptModel = globalDict.get('hydroptModel')
else:
    hydroptModel = hydropt.getData('model')
    globalDict.set('hydroptModel', hydroptModel)
if hydroptModel.nAssets == 1:
    assets = CSafeList([hydroptModel.Asset])
else:
    assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
assetName = args.get('asset')
i = 0
pos = -1
while (i < assets.len()):
    if assets.get(i).Shortname == assetName:
        pos = i
        break
    i = i + 1
types = CSafeList()
x = CSafeList()
y = CSafeList()
names_r = CSafeList()
names_t = CSafeList()
names_p = CSafeList()
names_f = CSafeList()
names = CSafeList()
if assets.get(pos).Topology.nRes != 0:
    if assets.get(pos).Topology.nRes == 1:
        reservoirs = CSafeList([assets.get(pos).Reservoir])
    else:
        reservoirs = CSafeList(CSafeList(assets.get(pos).Reservoir).get(0))
    j = 0
    while (j < reservoirs.len()):
        names_r.append(reservoirs.get(j).Shortname)
        names.append(reservoirs.get(j).Shortname)
        j = j + 1
if assets.get(pos).Topology.nFlows != 0:
    if assets.get(pos).Topology.nFlows == 1:
        flows = CSafeList([assets.get(pos).Flow])
    else:
        flows = CSafeList(CSafeList(assets.get(pos).Flow).get(0))
    j = 0
    while (j < flows.len()):
        names_f.append(flows.get(j).Shortname)
        names.append(flows.get(j).Shortname)
        j = j + 1
if assets.get(pos).Topology.nTurbines != 0:
    if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
        turbines = CSafeList([assets.get(pos).Engine])
    else:
        turbines = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
    j = 0
    while (j < int(assets.get(pos).Topology.nTurbines)):
        names_t.append(turbines.get(j).Shortname)
        names.append(turbines.get(j).Shortname)
        j = j + 1
if assets.get(pos).Topology.nPumps != 0:
    if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
        pumps = CSafeList([assets.get(pos).Engine])
    else:
        pumps = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
    j = int(assets.get(pos).Topology.nTurbines)
    while (j < pumps.len()):
        names_p.append(pumps.get(j).Shortname)
        names.append(pumps.get(j).Shortname)
        j = j + 1
operatesFrom = CSafeList()
operatesTo = CSafeList()
j = 0
if assets.get(pos).Topology.nRes != 0:
    if assets.get(pos).Topology.nRes == 1:
        reservoirs = CSafeList([assets.get(pos).Topology.Reservoir])
    else:
        reservoirs = CSafeList(CSafeList(assets.get(pos).Topology.Reservoir).get(0))
    while (j < assets.get(pos).Topology.nRes):
        types.append('reservoir')
        coords = CSafeList(CSafeList(reservoirs.get(j).Btn).get(0))
        x.append(coords.get(0))
        y.append(coords.get(1))
        if reservoirs.get(j).SpillsToRes == 0:
            operatesTo.append('null')
        else:
            operatesTo.append(names_r.get(int(reservoirs.get(j).SpillsToRes) - 1))
        operatesFrom.append('null')
        j = j + 1
if assets.get(pos).Topology.nFlows != 0:
    if assets.get(pos).Topology.nFlows == 1:
        flows = CSafeList([assets.get(pos).Topology.Flow])
    else:
        flows = CSafeList(CSafeList(assets.get(pos).Topology.Flow).get(0))
    j = 0
    while (j < flows.len()):
        types.append('flow')
        coords = CSafeList(CSafeList(flows.get(j).Btn).get(0))
        x.append(coords.get(0))
        y.append(coords.get(1))
        if flows.get(j).OperatesFrom == 0:
            operatesFrom.append('null')
        else:
            operatesFrom.append(names_r.get(int(flows.get(j).OperatesFrom) - 1))
        if flows.get(j).OperatesTo == 0:
            operatesTo.append('null')
        else:
            operatesTo.append(names_r.get(int(flows.get(j).OperatesTo) - 1))
        j = j + 1
if assets.get(pos).Topology.nTurbines != 0:
    if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
        turbines = CSafeList([assets.get(pos).Topology.Engine])
    else:
        turbines = CSafeList(CSafeList(assets.get(pos).Topology.Engine).get(0))
    j = 0
    while (j < int(assets.get(pos).Topology.nTurbines)):
        types.append('turbine')
        coords = CSafeList(CSafeList(turbines.get(j).Btn).get(0))
        x.append(coords.get(0))
        y.append(coords.get(1))
        if turbines.get(j).OperatesFrom == 0:
            operatesFrom.append('null')
        else:
            operatesFrom.append(names_r.get(int(turbines.get(j).OperatesFrom) - 1))
        if turbines.get(j).OperatesTo == 0:
            operatesTo.append('null')
        else:
            operatesTo.append(names_r.get(int(turbines.get(j).OperatesTo) - 1))
        j = j + 1
if assets.get(pos).Topology.nPumps != 0:
    if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
        pumps = CSafeList([assets.get(pos).Topology.Engine])
    else:
        pumps = CSafeList(CSafeList(assets.get(pos).Topology.Engine).get(0))
    j = int(assets.get(pos).Topology.nTurbines)
    while (j < pumps.len()):
        types.append('pump')
        coords = CSafeList(CSafeList(pumps.get(j).Btn).get(0))
        x.append(coords.get(0))
        y.append(coords.get(1))
        if pumps.get(j).OperatesFrom == 0:
            operatesFrom.append('null')
        else:
            operatesFrom.append(names_r.get(int(pumps.get(j).OperatesFrom) - 1))
        if pumps.get(j).OperatesTo == 0:
            operatesTo.append('null')
        else:
            operatesTo.append(names_r.get(int(pumps.get(j).OperatesTo) - 1))
        j = j + 1

redactorFrame = CFrame('Define Topology', width=1.0, height=0.5)

redactor = Create(CTopologyRedactor, {'name': 'redactor', 'style': {'width': '800px', 'height': '450px'},
                              'types': types.getList(),
                              'names': names.getList(),
                              'x': x.getList(),
                              'y': y.getList(),
                              'operatesFrom': operatesFrom.getList(),
                              'operatesTo': operatesTo.getList()})

redactorFrame.aChild(redactor)

myScreen = CPage('Define Topology')

myWaitStopper = CStopWaitingForGraphics()
myScreen.aChild(myWaitStopper)


myScreen.aChild(redactorFrame)

return myScreen


