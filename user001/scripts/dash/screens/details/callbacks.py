dataTable = CSafeDict()

def updateCalcParametersTable(value, assetName):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    hydroptModel = globalDict.get('hydroptModel')
    if hydroptModel.nAssets == 1:
        assets = CSafeList([hydroptModel.Asset])
    else:
        assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
    i = 0
    pos = -1
    while (i < assets.len()):
        if assets.get(i).Shortname == assetName:
            pos = i
            break
        i = i + 1
    if value == 'Scheduler':
        typ = 1
    else:
        typ = 2
    if typ == 1:
        Result = assets.get(pos).Scheduler.Result
        Input = assets.get(pos).Scheduler.Input
        octave.eval("Result = Data.Asset("+str(pos+1)+").Scheduler.Result;")
        octave.eval("Input = Data.Asset("+str(pos+1)+").Scheduler.Input;")
    else:
        Result = assets.get(pos).ScenarioWaterManager.Result
        Input = assets.get(pos).ScenarioWaterManager.Input
        octave.eval("Result = Data.Asset("+str(pos+1)+").ScenarioWaterManager.Result;")
        octave.eval("Input = Data.Asset("+str(pos+1)+").ScenarioWaterManager.Input;")
    octave.eval("RunTime = datestr(Result.RunTime,'dd-mmm-yyyy HH:MM');")
    RunTime = octave.pull("RunTime")
    octave.eval("Start = datestr(Result.DateNum(1),'dd-mmm-yyyy');")
    Start = octave.pull("Start")
    octave.eval("End = datestr(Result.DateNum(end),'dd-mmm-yyyy');")
    End = octave.pull("End")
    octave.eval("OptHorizon = [Start ' - ' End];")
    OptHorizon = octave.pull("OptHorizon")
    if Input.UseSpills == 1:
        US = 'on'
    else:
        US = 'off'
    if Input.UseConstraints == 1:
        UC = 'on'
    else:
        UC = 'off'
    if Input.UseCosts == 1:
        SC = 'on'
    else:
        SC = 'off'
    if Input.UseInfiltrationLosses == 1:
        IL = 'on'
    else:
        IL = 'off'
    octave.eval("PriceModDate = datestr(Result.PriceModificationDate,'dd-mmm-yyyy HH:MM');")
    PriceModDate = octave.pull("PriceModDate")
    octave.eval("DisplayType = " + str(typ) + ";")
    octave.eval("for i=1:length(Data.Asset("+str(pos+1)+").Reservoir) if DisplayType==1 IMDate(i)=Data.Asset("+str(pos+1)+").Reservoir(i).Scheduler.Result.InflowModificationDate; else IMDate(i)=Data.Asset("+str(pos+1)+").Reservoir(i).ScenarioWaterManager.Result.InflowModificationDate; end; end;")
    octave.eval("InflowModDate = datestr(max(IMDate),'dd-mmm-yyyy HH:MM');")
    InflowModDate = octave.pull("InflowModDate")
    col1 = CSafeList([['Calculation Finish'], ['Optimization Horizon'], ['Use Spills'], ['Use Minimum Hours'], ['Use Startup & Shutdown Costs'], ['Use Infiltration Losses'],
                      ['Last Modification of Price File'], ['Last Modification of Inflow File(s)']])
    col2 = CSafeList([[RunTime], [OptHorizon], [US], [UC], [SC], [IL], [PriceModDate], [InflowModDate]])
    rows = CSafeList()
    rows.append(col1.getList())
    rows.append(col2.getList())
    curTable = screenVariables.get('calcParametersTable')
    curTable.setTable(rows.getList(), ['Calculation Parameters', ' '], False, False, False, False, {'width': '70%', 'height': '50vh', 'marginTop': '1px'}, 320)
    return curTable.getData().to_dict('records')

N1 = 0
N2 = 0
N3 = 0
N4 = 0
N5 = 0
N6 = 0
N7 = 0
N8 = 0
def updateResultGraph(value, n1, n2, n3, n4, n5, n6, n7, n8, assetName):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    global N1, N2, N3, N4, N5, N6, N7, N8, FlushProfitScenarios, FlushPriceScenarios, FlushReservoirScenarios, FlushInflowScenarios, FlushEngine, FlushReservoir, FlushLosses, FlushFlow
    if n1 is None:
        n1 = 0
    if n2 is None:
        n2 = 0
    if n3 is None:
        n3 = 0
    if n4 is None:
        n4 = 0
    if n5 is None:
        n5 = 0
    if n6 is None:
        n6 = 0
    if n7 is None:
        n7 = 0
    if n8 is None:
        n8 = 0
    hydroptModel = globalDict.get('hydroptModel')
    if hydroptModel.nAssets == 1:
        assets = CSafeList([hydroptModel.Asset])
    else:
        assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
    i = 0
    pos = -1
    while (i < assets.len()):
        if assets.get(i).Shortname == assetName:
            pos = i
            break
        i = i + 1
    octave.eval("NoSchedulerResults = isempty(Data.Asset("+str(pos+1)+").Scheduler.Result) | isempty(Data.Asset("+str(pos+1)+").Reservoir(1).Scheduler.Result) | isempty(Data.Asset("+str(pos+1)+").Engine(1).Scheduler.Result);")
    octave.eval("NoScenarioWaterManagerResults = isempty(Data.Asset("+str(pos+1)+").ScenarioWaterManager.Result) | isempty(Data.Asset("+str(pos+1)+").Reservoir(1).ScenarioWaterManager.Result) | isempty(Data.Asset("+str(pos+1)+").Engine(1).ScenarioWaterManager.Result);")
    NoSchedulerResults = octave.pull("NoSchedulerResults")
    NoScenarioWaterManagerResults = octave.pull("NoScenarioWaterManagerResults")
    if NoSchedulerResults == 1 and NoScenarioWaterManagerResults == 1:
        curChart = screenVariables('resultGraphFigure')
        curChart.setChart(rows=[], headers=[], rowCaptions=[], title='No results for asset', type='bar', barmode='group',
						  style={'width': '550', 'height': '400'}, xAxis='', yAxis='', showLegend=False, hoverinfo='x+y', error={})
        return curChart.getValue()
    if value == 'Scheduler':
        typ = 1
    elif value == 'Engines':
        typ = 2
    else:
        typ = 3

    ###TODO: SENSITIVITY!!!!!!!!

    if typ == 3:
        if n6 != N6:
            N6 = n6
            if globalDict.contains('selectedType'):
                globalDict.erase('selectedType')
                globalDict.erase('selectedElement')
            return FlushPriceScenarios(pos)
        elif n3 != N3:
            N3 = n3
            if globalDict.contains('selectedType'):
                globalDict.erase('selectedType')
                globalDict.erase('selectedElement')
            return FlushReservoirScenarios(pos)
        elif n7 != N7:
            N7 = n7
            if globalDict.contains('selectedType'):
                globalDict.erase('selectedType')
                globalDict.erase('selectedElement')
            return FlushInflowScenarios(pos)
        else:
            N5 = n5
            if globalDict.contains('selectedType'):
                globalDict.erase('selectedType')
                globalDict.erase('selectedElement')
            return FlushProfitScenarios(pos)
    else:
        if n2 != N2:
            N2 = n2
            if globalDict.contains('selectedType'):
                globalDict.erase('selectedType')
                globalDict.erase('selectedElement')
            return FlushEngine(pos, [], 'Pump', typ)
        elif n3 != N3:
            N3 = n3
            if globalDict.contains('selectedType'):
                globalDict.erase('selectedType')
                globalDict.erase('selectedElement')
            return FlushReservoir(pos, [], typ)
        elif n4 != N4:
            N4 = n4
            if globalDict.contains('selectedType'):
                globalDict.erase('selectedType')
                globalDict.erase('selectedElement')
            return FlushLosses(pos, [], typ)
        elif n8 != N8:
            N8 = n8
            selectedType = globalDict.get('selectedType')
            name = globalDict.get('selectedElement')
            if selectedType == 'turbine':
                return FlushEngine(pos, [name], 'Turbine', typ)
            elif selectedType == 'flow':
                return FlushFlow(pos, [name], typ)
            elif selectedType == 'pump':
                return FlushEngine(pos, [name], 'Pump', typ)
            else:
                return FlushReservoir(pos, [name], typ)
        else:
            N1 = n1
            if globalDict.contains('selectedType'):
                globalDict.erase('selectedType')
                globalDict.erase('selectedElement')
            return FlushEngine(pos, [], 'Turbine', typ)

def FlushProfitScenarios(pos):
    global dataTable
    hydroptModel = globalDict.get('hydroptModel')
    if hydroptModel.nAssets == 1:
        assets = CSafeList([hydroptModel.Asset])
    else:
        assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
    R = assets.get(pos).ScenarioWaterManager.Result
    Rev = R.OverallRevenue / 1e6
    curChart = screenVariables.get('resultGraphFigure')
    ##TODO: fix this
    curChart.setChart(rows=[[1]], headers=[''], rowCaptions=[Rev], title='Revenue unhadged', type='bar', barmode='stack',
						  style={'width': '550', 'height': '400'}, xAxis='Revenue unhedged [Mio. EUR]', yAxis='Scenarios', showLegend=False, hoverinfo='x+y', error={})
    dataTable = CSafeDict({'headers': [' ', 'Revenue unhedged [Mio. EUR]'], 'rows': [[1], Rev]})
    return curChart.getValue()

def FlushPriceScenarios(pos):
    global dataTable
    hydroptModel = globalDict.get('hydroptModel')
    if hydroptModel.nAssets == 1:
        assets = CSafeList([hydroptModel.Asset])
    else:
        assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
    Price = assets.get(pos).ScenarioWaterManager.Result.PCoarse
    t = CSafeList(CSafeList(assets.get(pos).ScenarioWaterManager.Result.CoarseTime).get(0))
    i = 0
    while (i < t.len()):
        t.set(i, dateUtils.from_matlab(t.get(i)))
        i = i + 1
    curChart = screenVariables.get('resultGraphFigure')
    ##TODO: add more lines on chart
    curChart.setChart(rows=[Price], headers=[''], rowCaptions=pd.DatetimeIndex(t.getList()), title='Price scenarios', type='line', barmode='stack',
						  style={'width': '550', 'height': '400'}, xAxis='', yAxis='Weekly Average [EUR/MWh]', showLegend=False, hoverinfo='x+y', error={})
    dataTable = CSafeDict({'headers': ['Time', 'Weekly Average [EUR/MWh]'], 'rows': [Price], 'titles': pd.DatetimeIndex(t.getList())})
    return curChart.getValue()

def FlushReservoirScenarios(pos):
    global dataTable
    hydroptModel = globalDict.get('hydroptModel')
    if hydroptModel.nAssets == 1:
        assets = CSafeList([hydroptModel.Asset])
    else:
        assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
    octave.eval("HP=Data.Asset("+str(pos+1)+"); R=HP.Reservoir(1).ScenarioWaterManager.Result.RCoarse; R1=HP.Reservoir(1).ScenarioWaterManager.Result.Level(1); Rend=HP.Reservoir(1).ScenarioWaterManager.Result.Level(end);")
    octave.eval("for i=2:HP.Topology.nRes R=R+HP.Reservoir(i).ScenarioWaterManager.Result.RCoarse; R1=R1+HP.Reservoir(i).ScenarioWaterManager.Result.Level(1); Rend=Rend+HP.Reservoir(i).ScenarioWaterManager.Result.Level(end); end;")
    octave.eval("R=[R1*ones(1,size(R,2)); R ; Rend*ones(1,size(R,2))]/1000; CoarseTime=HP.ScenarioWaterManager.Result.CoarseTime; DateNum=HP.ScenarioWaterManager.Result.DateNum; t=[DateNum(1) CoarseTime DateNum(end)];")
    R = octave.pull("R")
    t = CSafeList(CSafeList(octave.pull("t")).get(0))
    i = 0
    while (i < t.len()):
        t.set(i, dateUtils.from_matlab(t.get(i)))
        i = i + 1
    curChart = screenVariables.get('resultGraphFigure')
    ##TODO: add more lines on chart
    curChart.setChart(rows=[R], headers=[''], rowCaptions=pd.DatetimeIndex(t.getList()), title='Reservoirs scenarios', type='line', barmode='stack',
						  style={'width': '550', 'height': '400'}, xAxis='', yAxis='Reservoir Level [GWh]', showLegend=False, hoverinfo='x+y', error={})
    dataTable = CSafeDict({'headers': ['Time', 'Reservoir Level [GWh]'], 'rows': [R], 'titles': pd.DatetimeIndex(t.getList())})
    return curChart.getValue()

def FlushInflowScenarios(pos):
    global dataTable
    hydroptModel = globalDict.get('hydroptModel')
    if hydroptModel.nAssets == 1:
        assets = CSafeList([hydroptModel.Asset])
    else:
        assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
    octave.eval("HP=Data.Asset("+str(pos+1)+"); I=HP.Reservoir(1).ScenarioWaterManager.Result.ICoarse;")
    octave.eval("for i=2:HP.Topology.nRes I=I+HP.Reservoir(i).ScenarioWaterManager.Result.ICoarse; end; t=HP.ScenarioWaterManager.Result.CoarseTime;")
    I = octave.pull("I")
    t = CSafeList(CSafeList(octave.pull("t")).get(0))
    i = 0
    while (i < t.len()):
        t.set(i, dateUtils.from_matlab(t.get(i)))
        i = i + 1
    curChart = screenVariables.get('resultGraphFigure')
    ##TODO: add more lines on chart
    curChart.setChart(rows=[I], headers=[''], rowCaptions=pd.DatetimeIndex(t.getList()), title='Inflow scenarios', type='line', barmode='stack',
                      style={'width': '550', 'height': '400'}, xAxis='', yAxis='Inflow [MWh]', showLegend=False, hoverinfo='x+y', error={})
    dataTable = CSafeDict({'headers': ['Time', 'Inflow [MWh]'], 'rows': [I], 'titles': pd.DatetimeIndex(t.getList())})
    return curChart.getValue()

def FlushEngine(pos, Tag, Type, DisplayType):
    global dataTable
    octave.push("Tag", Tag)
    octave.push("Type", Type)
    octave.push("DisplayType", DisplayType)
    octave.eval("HP=Data.Asset("+str(pos+1)+");")
    Tag = CSafeList(Tag)
    octave.eval("""function [r,I,J] = uniquex(x,varargin)
                    v = ver();
                    d = v.Date;
                    y = str2num(d(end-3:end));
                    if y < 2013
                        [r,I,J] = unique(x,varargin{:});
                    else
                        [r,I,J] = unique(x,varargin{:},'legacy');
                    end""")
    if Tag.len() == 0:
        octave.eval(""" nTurbines = HP.Topology.nTurbines;
                        if DisplayType == 1  % Scheduler
                            t = HP.Scheduler.Result.DateNum;
                            F = HP.Scheduler.Result.ExpectedSpotPrice;
                            if isequal(Type,'Turbine')
                                O = HP.Engine(1).Scheduler.Result.Operation;
                                for j=2:nTurbines
                                    O = O + HP.Engine(j).Scheduler.Result.Operation;
                                end
                            elseif HP.Topology.nPumps > 0
                                O = HP.Engine(nTurbines + 1).Scheduler.Result.Operation;
                                for j=2:HP.Topology.nPumps
                                    O = O + HP.Engine(nTurbines + j).Scheduler.Result.Operation;
                                end
                            end
                        elseif DisplayType == 2  % ScenarioWaterManager
                            t = HP.ScenarioWaterManager.Result.DateNum;
                            F = HP.ScenarioWaterManager.Result.ExpectedSpotPrice;
                            if isequal(Type,'Turbine')
                                O = HP.Engine(1).ScenarioWaterManager.Result.Operation;
                                for j=2:nTurbines
                                    O = O + HP.Engine(j).ScenarioWaterManager.Result.Operation;
                                end
                            elseif HP.Topology.nPumps > 0
                                O = HP.Engine(nTurbines + 1).ScenarioWaterManager.Result.Operation;
                                for j=2:HP.Topology.nPumps
                                    O = O + HP.Engine(nTurbines + 1).ScenarioWaterManager.Result.Operation;
                                end
                            end
                        end""")
    else:
        hydroptModel = globalDict.get('hydroptModel')
        if hydroptModel.nAssets == 1:
            assets = CSafeList([hydroptModel.Asset])
        else:
            assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
        if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
            engines = CSafeList([assets.get(pos).Engine])
        else:
            engines = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
        i = 0
        num = -1
        while (i < engines.len()):
            if engines.get(i).Shortname == Tag.get(0):
                num = i
                break
            i = i + 1
        octave.eval(""" Engine = HP.Engine("""+str(num+1)+""");  
                        if DisplayType == 1
                            t = HP.Scheduler.Result.DateNum;
                            F = HP.Scheduler.Result.ExpectedSpotPrice;
                            O = Engine.Scheduler.Result.Operation;
                        elseif DisplayType == 2
                            t = HP.ScenarioWaterManager.Result.DateNum;
                            F = HP.ScenarioWaterManager.Result.ExpectedSpotPrice;
                            O = Engine.ScenarioWaterManager.Result.Operation;
                        end;""")
    octave.eval("O = abs(O); [tdistinct,idx] = uniquex(t'); O=O(idx);")
    t = CSafeList(octave.pull("tdistinct"))
    i = 0
    while (i < t.len()):
        t.set(i, dateUtils.from_matlab(CSafeList(t.get(i)).get(0)))
        i = i + 1
    data = octave.pull("O")
    curChart = screenVariables.get('resultGraphFigure')
    curChart.setChart(rows=[[data]], headers=[''], rowCaptions=pd.DatetimeIndex(t.getList()), title='Engine Operation [MW] and Market Price [scaled]', type='bar', barmode='group',
						  style={'width': '550', 'height': '400'}, xAxis='', yAxis='[MW]', showLegend=False, hoverinfo='x+y', error={})
    octave.eval("FScaled = F(idx)/max(F) * max(abs(O));")
    FScaled = CSafeList(octave.pull("FScaled"))
    i = 0
    while (i < FScaled.len()):
        FScaled.set(i, CSafeList(FScaled.get(i)).get(0))
        i = i + 1
    curChart.addTrace(x=pd.DatetimeIndex(t.getList()), y=FScaled.getList(), type='line', hoverinfo='x+y', yaxis=None)
    dataTable = CSafeDict({'headers': ['Time', 'Market Price [scaled]', 'Engine Operation [MW]'], 'rows': [FScaled.getList(), data], 'titles': pd.DatetimeIndex(t.getList())})
    return curChart.getValue()

def FlushReservoir(pos, Tag, DisplayType):
    global dataTable
    octave.push("Tag", Tag)
    octave.push("DisplayType", DisplayType)
    octave.eval("HP=Data.Asset("+str(pos+1)+");")
    Tag = CSafeList(Tag)
    octave.eval("if DisplayType == 1 Result = HP.Scheduler.Result; elseif DisplayType == 2 Result = HP.ScenarioWaterManager.Result; end; t = Result.DateNum;")
    if Tag.len() == 0:
        if DisplayType == 1:
            octave.eval("R=HP.Reservoir(1).Scheduler.Result.Level; for j=2:length(HP.Reservoir) R = R + HP.Reservoir(j).Scheduler.Result.Level; end;")
        else:
            octave.eval("R=HP.Reservoir(1).ScenarioWaterManager.Result.Level; for j=2:length(HP.Reservoir) R = R + HP.Reservoir(j).ScenarioWaterManager.Result.Level; end;")
    else:
        hydroptModel = globalDict.get('hydroptModel')
        if hydroptModel.nAssets == 1:
            assets = CSafeList([hydroptModel.Asset])
        else:
            assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
        if assets.get(pos).Topology.nReservoirs == 1:
            reservoirs = CSafeList([assets.get(pos).Reservoir])
        else:
            reservoirs = CSafeList(CSafeList(assets.get(pos).Reservoir).get(0))
        i = 0
        num = -1
        while (i < reservoirs.len()):
            if reservoirs.get(i).Shortname == Tag.get(0):
                num = i
                break
            i = i + 1
        if DisplayType == 1:
            octave.eval(""" R = HP.Reservoir("""+str(num+1)+""").Scheduler.Result.Level;
                            S = HP.Reservoir("""+str(num+1)+""").Scheduler.Result.Spill;
                            if isempty(S)
                                S = zeros(size(R));
                            end
                            ILoss = HP.Reservoir("""+str(num+1)+""").Scheduler.Result.InfiltrationLoss;
                            if isempty(ILoss)
                                ILoss = zeros(size(R));
                            end    
                            Loss = S + ILoss;""")
        else:
            octave.eval(""" R = HP.Reservoir("""+str(num+1)+""").ScenarioWaterManager.Result.Level;
                            S = HP.Reservoir("""+str(num+1)+""").ScenarioWaterManager.Result.Spill;
                            if isempty(S)
                                S = zeros(size(R));
                            end
                            ILoss = HP.Reservoir("""+str(num+1)+""").ScenarioWaterManager.Result.InfiltrationLoss;
                            if isempty(ILoss)
                                ILoss = zeros(size(R));
                            end     
                            Loss = S + ILoss;""")
    octave.eval("R = R/1000;")
    t = CSafeList(CSafeList(octave.pull("t")).get(0))
    i = 0
    while (i < t.len()):
        t.set(i, dateUtils.from_matlab(t.get(i)))
        i = i + 1
    data = CSafeList(octave.pull("R"))
    curChart = screenVariables.get('resultGraphFigure')
    i = 0
    while (i < data.len()):
        data.set(i, CSafeList(data.get(i)).get(0))
        i = i + 1
    if Tag.len() == 0:
        curChart.setChart(rows=[data.getList()], headers=[''], rowCaptions=pd.DatetimeIndex(t.getList()), title='Reservoir Level [GWh]', type='line', barmode='group',
                          style={'width': '550', 'height': '400'}, xAxis='', yAxis='[GWh]', showLegend=False, hoverinfo='x+y', error={})
        dataTable = CSafeDict({'headers': ['Time', 'Reservoir Level [GWh]'], 'rows': [data.getList()], 'titles': pd.DatetimeIndex(t.getList())})
    else:
        curChart.setChart(rows=[data.getList()], headers=[''], rowCaptions=pd.DatetimeIndex(t.getList()), title='Reservoir Level [GWh] and Losses [GWh]', type='line', barmode='group',
                          style={'width': '550', 'height': '400'}, xAxis='', yAxis='[GWh]', showLegend=False, hoverinfo='x+y', error={})
        Loss = CSafeList(octave.pull("Loss"))
        curChart = screenVariables.get('resultGraphFigure')
        i = 0
        while (i < Loss.len()):
            Loss.set(i, CSafeList(Loss.get(i)).get(0))
            i = i + 1
        curChart.addTrace(x=pd.DatetimeIndex(t.getList()), y=Loss.getList(), type='line', hoverinfo='x+y', yaxis={'title': '[MWh]', 'side': 'right', 'overlaying': 'y'})
        dataTable = CSafeDict({'headers': ['Time', 'Reservoir Level [GWh]', 'Losses [MWh]'], 'rows': [data.getList(), Loss.getList()], 'titles': pd.DatetimeIndex(t.getList())})
    return curChart.getValue()

def FlushLosses(pos, Tag, DisplayType):
    global dataTable
    octave.push("Tag", Tag)
    octave.push("DisplayType", DisplayType)
    octave.eval("HP=Data.Asset(" + str(pos + 1) + ");")
    Tag = CSafeList(Tag)
    octave.eval(""" if DisplayType == 1 
                    Result = HP.Scheduler.Result;
                    S = HP.Reservoir(1).Scheduler.Result.Spill;
                    if ~isempty(S);
                        for j=2:HP.Topology.nRes
                            S = S + HP.Reservoir(j).Scheduler.Result.Spill;
                        end
                    else
                        S = zeros(size(Result.DateNum));
                    end
                    ILoss = HP.Reservoir(1).Scheduler.Result.InfiltrationLoss;
                    if ~isempty(ILoss);
                        for j=2:HP.Topology.nRes
                            ILoss = ILoss + HP.Reservoir(j).Scheduler.Result.InfiltrationLoss;
                        end
                    else
                        ILoss = zeros(size(Result.DateNum));
                    end 
                    Loss = max(S,ILoss);
                    elseif DisplayType == 2
                    Result = HP.ScenarioWaterManager.Result;
                    S = HP.Reservoir(1).ScenarioWaterManager.Result.Spill;
                    if ~isempty(S);
                        for j=2:HP.Topology.nRes
                            S = S + HP.Reservoir(j).ScenarioWaterManager.Result.Spill;
                        end
                    else
                        S = zeros(size(Result.DateNum))';
                    end
                    ILoss = HP.Reservoir(1).ScenarioWaterManager.Result.InfiltrationLoss;
                    if ~isempty(ILoss);
                        for j=2:HP.Topology.nRes
                            ILoss = ILoss + HP.Reservoir(j).ScenarioWaterManager.Result.InfiltrationLoss;
                      end
                    else
                        ILoss = zeros(size(Result.DateNum))';
                    end 
                    Loss = max(S,ILoss);
                    end
                    t = Result.DateNum;""")
    t = CSafeList(CSafeList(octave.pull("t")).get(0))
    i = 0
    while (i < t.len()):
        t.set(i, dateUtils.from_matlab(t.get(i)))
        i = i + 1
    S = CSafeList(octave.pull("S"))
    ILoss = CSafeList(octave.pull("ILoss"))
    curChart = screenVariables.get('resultGraphFigure')
    i = 0
    while (i < S.len()):
        S.set(i, CSafeList(S.get(i)).get(0))
        i = i + 1
    i = 0
    while (i < ILoss.len()):
        ILoss.set(i, CSafeList(ILoss.get(i)).get(0))
        i = i + 1
    curChart.setChart(rows=[S.getList()], headers=[''], rowCaptions=pd.DatetimeIndex(t.getList()), title='Infiltration Loss and Spill [MWh]', type='line', barmode='group',
                      style={'width': '550', 'height': '400'}, xAxis='', yAxis='[MWh]', showLegend=False, hoverinfo='x+y', error={})
    curChart.addTrace(x=pd.DatetimeIndex(t.getList()), y=ILoss.getList(), type='line', hoverinfo='x+y', yaxis=None)
    dataTable = CSafeDict({'headers': ['Time', 'Infiltration Loss [MWh]', 'Spill [MWh]'], 'rows': [ILoss.getList(), S.getList()], 'titles': pd.DatetimeIndex(t.getList())})
    return curChart.getValue()

def FlushFlow(pos, Tag, DisplayType):
    global dataTable
    octave.push("Tag", Tag)
    octave.push("DisplayType", DisplayType)
    octave.eval("HP=Data.Asset(" + str(pos + 1) + ");")
    Tag = CSafeList(Tag)
    hydroptModel = globalDict.get('hydroptModel')
    if hydroptModel.nAssets == 1:
        assets = CSafeList([hydroptModel.Asset])
    else:
        assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
    if assets.get(pos).Topology.nFlows == 1:
        flows = CSafeList([assets.get(pos).Flow])
    else:
        flows = CSafeList(CSafeList(assets.get(pos).Flow).get(0))
    i = 0
    num = -1
    while (i < flows.len()):
        if flows.get(i).Shortname == Tag.get(0):
            num = i
            break
        i = i + 1
    octave.eval(""" Flow = HP.Flow("""+str(num+1)+""");  
                    if DisplayType == 1
                        t = HP.Scheduler.Result.DateNum;
                        O = Flow.Scheduler.Result.Operation;
                    elseif DisplayType == 2
                        t = HP.ScenarioWaterManager.Result.DateNum;
                        F = HP.ScenarioWaterManager.Result.ExpectedSpotPrice;
                        O = Flow.ScenarioWaterManager.Result.Operation;          
                    end;
                    [tdistinct,idx] = uniquex(t);
                    O = O(idx);""")
    t = CSafeList(CSafeList(octave.pull("t")).get(0))
    i = 0
    while (i < t.len()):
        t.set(i, dateUtils.from_matlab(t.get(i)))
        i = i + 1
    O = CSafeList(octave.pull("O"))
    curChart = screenVariables.get('resultGraphFigure')
    i = 0
    while (i < O.len()):
        O.set(i, CSafeList(O.get(i)).get(0))
        i = i + 1
    curChart.setChart(rows=[O.getList()], headers=[''], rowCaptions=pd.DatetimeIndex(t.getList()), title='Flow [MWh]', type='bar', barmode='group',
                      style={'width': '550', 'height': '400'}, xAxis='', yAxis='[MWh]', showLegend=False, hoverinfo='x+y', error={})
    dataTable = CSafeDict({'headers': ['Time', 'Flow [MWh]'], 'rows': [O.getList()], 'titles': pd.DatetimeIndex(t.getList())})
    return curChart.getValue()

def turbinesButton(value):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    style = CSafeDict({})
    if value == 'Engines':
        style.set('display', 'block')
    else:
        style.set('display', 'none')
    return style.getDict()

def revenuesButton(value):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    style = CSafeDict({})
    if value == 'Engines':
        style.set('display', 'none')
    else:
        style.set('display', 'block')
    return style.getDict()

def pumpsButton(value):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    style = CSafeDict({})
    if value == 'Engines':
        style.set('display', 'block')
    else:
        style.set('display', 'none')
    return style.getDict()

def pricesButton(value):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    style = CSafeDict({})
    if value == 'Engines':
        style.set('display', 'none')
    else:
        style.set('display', 'block')
    return style.getDict()

def lossesButton(value):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    style = CSafeDict({})
    if value == 'Engines':
        style.set('display', 'block')
    else:
        style.set('display', 'none')
    return style.getDict()

def inflowsButton(value):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    style = CSafeDict({})
    if value == 'Engines':
        style.set('display', 'none')
    else:
        style.set('display', 'block')
    return style.getDict()

def loadModal(n0, n1, oldStyle):
	if n0 is None:
		n0 = 0
	if n1 is None:
		n1 = 0
	style = CSafeDict(oldStyle)
	if n0 > n1:
		style.set('display', 'block')
	else:
		style.set('display', 'none')
	return style.getDict()

def loadModal1(n0, n1, oldStyle):
	if n0 is None:
		n0 = 0
	if n1 is None:
		n1 = 0
	style = CSafeDict(oldStyle)
	if n0 > n1:
		style.set('display', 'block')
	else:
		style.set('display', 'none')
	return style.getDict()

def buildModalGraph(n0, fig0):
    newFig = CSafeFigure(figure=fig0)
    newFig.scale(1.6)
    return newFig.getFigure()

def drawText1(fig, value):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    if value == 'valueAndRisk' or (globalDict.contains('selectedType') and (globalDict.get('selectedType') == 'turbine' or globalDict.get('selectedType') == 'pump')):
        return {'display': 'block', 'marginTop': '2%'}
    else:
        return {'display': 'none', 'marginTop': '2%'}

def buildText1(fig, value, assetName):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    if value == 'valueAndRisk':
        hydroptModel = globalDict.get('hydroptModel')
        if hydroptModel.nAssets == 1:
            assets = CSafeList([hydroptModel.Asset])
        else:
            assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
        i = 0
        pos = -1
        while (i < assets.len()):
            if assets.get(i).Shortname == assetName:
                pos = i
                break
            i = i + 1
        octave.eval(""" HP = Data.Asset("""+str(pos+1)+""");
                        R = HP.ScenarioWaterManager.Result;
                        Rev = R.OverallRevenue / 1e6;
                        mu = sprintf('%.2f Mio. EUR',mean(Rev));
                        """)
        return 'Average Revenue: ' + octave.pull("mu")
    else:
        if globalDict.contains('selectedType') and (globalDict.get('selectedType') == 'turbine' or globalDict.get('selectedType') == 'pump'):
            hydroptModel = globalDict.get('hydroptModel')
            if hydroptModel.nAssets == 1:
                assets = CSafeList([hydroptModel.Asset])
            else:
                assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
            i = 0
            pos = -1
            while (i < assets.len()):
                if assets.get(i).Shortname == assetName:
                    pos = i
                    break
                i = i + 1
            if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
                engines = CSafeList([assets.get(pos).Engine])
            else:
                engines = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
            i = 0
            num = -1
            while (i < engines.len()):
                if engines.get(i).Shortname == globalDict.get("selectedElement"):
                    num = i
                    break
                i = i + 1
            octave.eval("HP = Data.Asset("+str(pos+1)+"); Engine = HP.Engine("+str(num+1)+");")
            if value == 'Engines':
                octave.eval("result = sprintf(' %.1f EUR/MWh', Engine.ScenarioWaterManager.Result.MarginPrice);")
            else:
                octave.eval("result = sprintf(' %.1f EUR/MWh', Engine.Scheduler.Result.MarginPrice);")
            return 'Margin Price: ' + octave.pull("result")
        return ''

def drawText2(fig, value):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    if value == 'valueAndRisk' or (globalDict.contains('selectedType') and (globalDict.get('selectedType') == 'turbine' or globalDict.get('selectedType') == 'pump')):
        return {'display': 'block', 'marginTop': '0'}
    else:
        return {'display': 'none', 'marginTop': '0'}

def buildText2(fig, value, assetName):
    if type(value) != type('abc'):
        value = CSafeDict(value).get('value')
    if value == 'valueAndRisk':
        hydroptModel = globalDict.get('hydroptModel')
        if hydroptModel.nAssets == 1:
            assets = CSafeList([hydroptModel.Asset])
        else:
            assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
        i = 0
        pos = -1
        while (i < assets.len()):
            if assets.get(i).Shortname == assetName:
                pos = i
                break
            i = i + 1
        octave.eval(""" HP = Data.Asset("""+str(pos+1)+""");
                        R = HP.ScenarioWaterManager.Result;
                        Rev = R.OverallRevenue / 1e6;
                        S = sort(Rev);
                        EaR95 = S(max(1,round(length(S)/20)));
                        EaR95 = sprintf('%.2f Mio. EUR',EaR95);""")
        return 'Minimum Revenue (95%): ' + octave.pull("EaR95")
    else:
        if globalDict.contains('selectedType') and (globalDict.get('selectedType') == 'turbine' or globalDict.get('selectedType') == 'pump'):
            hydroptModel = globalDict.get('hydroptModel')
            if hydroptModel.nAssets == 1:
                assets = CSafeList([hydroptModel.Asset])
            else:
                assets = CSafeList(CSafeList(lst=hydroptModel.Asset).get(0))
            i = 0
            pos = -1
            while (i < assets.len()):
                if assets.get(i).Shortname == assetName:
                    pos = i
                    break
                i = i + 1
            if assets.get(pos).Topology.nTurbines + assets.get(pos).Topology.nPumps == 1:
                engines = CSafeList([assets.get(pos).Engine])
            else:
                engines = CSafeList(CSafeList(assets.get(pos).Engine).get(0))
            i = 0
            num = -1
            while (i < engines.len()):
                if engines.get(i).Shortname == globalDict.get("selectedElement"):
                    num = i
                    break
                i = i + 1
            octave.eval("HP = Data.Asset("+str(pos+1)+"); Engine = HP.Engine("+str(num+1)+");")
            if value == 'Engines':
                octave.eval("result = sprintf(' %.1f EUR/MWh', std(Engine.ScenarioWaterManager.Result.MarginPrice));")
                return 'Standard Dev.: ' + octave.pull("result")
            else:
                return ''
        return ''

def buildLink(rows):
	df = pd.DataFrame.from_dict(rows)
	csv_string = df.to_csv(index=False, encoding='utf-8')
	csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
	return csv_string

def buildModalTable(n_clicks):
    tempDF = CSafeDF()
    if dataTable.contains('titles'):
        columnsList = CSafeList(dataTable.get('rows'))
        dt = CSafeList()
        i = 0
        titles = CSafeList(dataTable.get('titles'))
        while (i < titles.len()):
            dt.append(CSafeList([titles.get(i)]))
            i = i + 1
        i = 0
        while (i < columnsList.len()):
            column = CSafeList(columnsList.get(i))
            j = 0
            while (j < column.len()):
                tmp = dt.get(j)
                tmp.append(column.get(j))
                dt.set(j, tmp)
                j = j + 1
            i = i + 1
        i = 0
        while (i < dt.len()):
            tmp = dt.get(i)
            dt.set(i, tmp.getList())
            i = i + 1
        tempDF.define(dt.getList(), dataTable.get('headers'))
    else:
        rows = CSafeList(dataTable.get('rows'))
        tempDF.define([rows.getList()], dataTable.get('headers'))
    return tempDF.to_dict('records')