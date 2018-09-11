function result = export(Data)

Export = Data.Export;

A = [Data.Asset.Export];
As = find([A.Check]);

%%%TODO
%if batchmode discard assets with warnings (if option is activated)
%if handles.BatchMode
%    for i = As
%        if ~isempty(Data.Asset(i).ScenarioWaterManager.Warning)
%            if (Data.Asset(i).ScenarioWaterManager.Warning == 1) && (handles.Batch.disableExport == 1)
%                As(i) = [];
%            end
%        end
%    end
%end


% get time horizon
Dummy.Dummy = 1;
[Dummy, tStart, tEnd] = getDateSelectors(Dummy, Data);
tEnd = tEnd - 1/24;


%**************************************************************************
%******************* Input Checking ***************************************
%**************************************************************************

%%TODO
%check if assets are selected
if isempty(As)
    %if ~handles.BatchMode
    %    infodlgx(handles.BatchMode, 'An asset has to be selected.');
    %end
    result = ['An asset has to be selected.']
    return
end

%check if results are selected
ResultsSelection = [Export.ReservoirLevel; Export.Inflow; Export.Spill; Export.Flow ; Export.InfiltrationLoss; ...
   Export.Turbine; Export.Pump; Export.Price; Export.MarginPriceTS; Export.WaterValueTS ; Export.MarginPrices; ...
   Export.WaterValues; Export.Revenues; Export.RevenuesMonthly; Export.RevenuesEngine; ...
   Export.RevenuesEngineMonthly; Export.ReservoirUsage; Export.Log];

x = find(ResultsSelection);
if (Export.WaterValues == 1 && Export.ScenarioWaterMgt == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1))
   x=1;
end

if (Export.MarginPrices == 1 && Export.ScenarioWaterMgt == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1))
   x=1;
end

%%%TODO
if isempty(x)
    %if ~(Export.Revenues == 1 && Export.ScenarioWaterMgt == 1 && Export.Separated == 1 ...
    %     && (Export.Excel == 1 || Export.MAT == 1) && strcmp('on',get(handles.checkbox_Revenues,'enable')))
    %    infodlgx(handles.BatchMode, 'Please select results.');
    %    return
    %end
end

% Check if pumps are defined
if Export.Pump == 1
    for i = As
        Pumps(i) = Data.Asset(i).Topology.nPumps;
    end
    nPumps = length(find(Pumps));

    if nPumps == 0 % if no pumps at all are selected
       Export.Pump = 0;
    end
end


% Check if Flows are defined
if Export.Flow == 1
    for i = As
        Flows(i) = Data.Asset(i).Topology.nFlows;
    end
    nFlows = length(find(Flows));

    if nFlows == 0 % if no pumps at all are selected
       Export.Flow = 0;
    end
end

%%%%%TODO
if length(As) == 1 % Aggregate only if more than one asset
   Export.Aggregated = 0;

   Data.Export.Aggregated = 0;
   %set(gcf,'userdata',Data);
end


%%TODO
%Check Time and data availability
if Export.Scheduler == 1 %Scheduler % Module
   for i = As

      %data availability
     if isempty(Data.Asset(i).Scheduler.Result)
        %errordlgx(handles.BatchMode, ['No results for Asset ' num2str(i) '.']);
        result = ['No results for Asset ' num2str(i) '.']
        return
     end

     %Time
     t = Data.Asset(i).Scheduler.Result.DateNum;
     [StartIdx,EndIdx,t] = findT(t,tStart,tEnd);
     if isempty(StartIdx) | isempty(EndIdx)
         Name = Data.Asset(i).Name;
         %infodlgx(handles.BatchMode, [Name ': Time horizon for export does not match with optimization horzion.']);
         result = [Name ': Time horizon for export does not match with optimization horzion.']
          return
     end

   end
else
    for i = As
        %data availability
        if isempty(Data.Asset(i).ScenarioWaterManager.Result)
           %errordlgx(handles.BatchMode, ['No results for Asset ' num2str(i) '.']);
           result = ['No results for Asset ' num2str(i) '.']
          return
        end

        %Time
        t = Data.Asset(i).ScenarioWaterManager.Result.DateNum;
        [StartIdx,EndIdx,t] = findT(t,tStart,tEnd);

        if isempty(StartIdx) | isempty(EndIdx)
            Name = Data.Asset(i).Name;
            %infodlgx(handles.BatchMode, [Name ': Time horizon for export does not match with optimization horzion.']);
            result = [Name ': Time horizon for export does not match with optimization horzion.']
            return
        end
    end
end

%TODO
%Check if directory exists
%if exxist(Data.Export.ExportFolder) ~= 7 % is not a directory
%   if ~(Export.Aggregated | length(As)==1) % if more than one file is produced
%      errordlgx(handles.BatchMode, ['Error: Export folder not found (multiple files will be produced).'])
%      return
%   end

%   if Export.MAT | Export.CSV
%      errordlgx(handles.BatchMode, ['Error: Export folder not found.'])
%      return
%   end
%end

%Check if file is given
%if isempty(Data.Export.Filename)
%   if Export.MAT
%      errordlgx(handles.BatchMode, ['Error: Export file has to be defined.'])
%      return
%   end
%end

%Check if File Format is given
if ~Export.MAT & ~Export.CSV & ~Export.Excel
    %errordlgx(handles.BatchMode, ['Error: File format has to be defined.'])
    result = ['Error: File format has to be defined.']
    return
end




%**************************************************************************
%******************* Acquire Results **************************************
%**************************************************************************

Count = 0;
Asset(1).Res = [];
Asset(1).Inflow = [];
Asset(1).Spill = [];
Asset(1).Flow = [];
Asset(i).InfiltrationLoss = [];
Asset(1).Turbine = [];
Asset(1).Pump = [];
Asset(1).Rev = [];
Asset(1).MarginPrices = [];
Asset(1).WaterValues = [];
Asset(1).MarginPriceTS = [];
Asset(1).WaterValueTS = [];
Asset(1).ResUsageMin = [];
Asset(1).ResUsageMax = [];
Asset(1).Price = [];



for i = As
    try
        Count = Count+1;

        nPumps = Data.Asset(i).Topology.nPumps;
        nTurb = Data.Asset(i).Topology.nTurbines;
        nFlows = Data.Asset(i).Topology.nFlows;
        nRes = Data.Asset(i).Topology.nRes;
        nEngines = nTurb + nPumps;

        if Data.Export.Scheduler
           nScenarios = 1;
           DateNum = Data.Asset(i).Scheduler.Result.DateNum;
        else
           nScenarios = Data.Asset(i).ScenarioWaterManager.Input.nScenarios;
           DateNum = Data.Asset(i).ScenarioWaterManager.Result.DateNum;
        end
        %Reservoir Level
        if Export.ReservoirLevel == 1
            if Export.Scheduler == 1 %Scheduler
               for j = 1:nRes
                  Resu = Data.Asset(i).Reservoir(j).Scheduler.Result;
                  Asset(Count).R(:,j) = AdaptUnitMWh(Resu.Level(StartIdx:EndIdx),Resu.Level(StartIdx:EndIdx),...
                                                  Resu.MWh,...
                                                  Resu.CubicMetres,Export.MWh,'Res');
               end
            else
               for j = 1:nRes
                  Resu = Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result;
                  Asset(Count).R(:,j) = AdaptUnitMWh(Resu.Level(StartIdx:EndIdx),Resu.Level(StartIdx:EndIdx),...
                                                     Resu.MWh,...
                                                     Resu.CubicMetres,Export.MWh,'Res');
               end
            end
            Asset(Count).Res = getResolutedValues(Asset(Count).R, t, tStart, tEnd,'mean','auto', Data);
        end
        % Spill
        if Export.Spill == 1
            if Export.Scheduler == 1 %Scheduler
                if isempty(Data.Asset(i).Reservoir(1).Scheduler.Result.Spill) % no Spill calculated
                   Asset(Count).Spill = zeros(length(t),nRes);
                else
                   for j = 1:nRes
                      Asset(Count).Spill(:,j) = AdaptUnitMWh(Data.Asset(i).Reservoir(j).Scheduler.Result.Spill(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(j).Scheduler.Result.Level(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(j).Scheduler.Result.MWh,...
                                                  Data.Asset(i).Reservoir(j).Scheduler.Result.CubicMetres,Export.MWh,'Spill');
                   end
                end
            else
               if isempty(Data.Asset(i).Reservoir(1).ScenarioWaterManager.Result.Spill) % no Spill calculated
                  Asset(Count).Spill = zeros(length(t),nRes);
               else
                  for j = 1:nRes
                      Asset(Count).Spill(:,j) = AdaptUnitMWh(Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result.Spill(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result.Level(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result.MWh,...
                                                  Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result.CubicMetres,Export.MWh,'Spill');
                  end
               end
            end
            Asset(Count).Spill = getResolutedValues(Asset(Count).Spill, t, tStart, tEnd,iff(Export.MWh,'sum','mean'),'auto', Data);
        end
        % InfiltrationLoss
        if Export.InfiltrationLoss == 1
            if Export.Scheduler == 1 %Scheduler
               if isempty(Data.Asset(i).Reservoir(1).Scheduler.Result.InfiltrationLoss) % no InfiltrationLoss calculated
                  Asset(Count).InfiltrationLoss = zeros(length(t),nRes);
               else
                   for j = 1:nRes
                      Asset(Count).InfiltrationLoss(:,j) = AdaptUnitMWh(Data.Asset(i).Reservoir(j).Scheduler.Result.InfiltrationLoss(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(j).Scheduler.Result.Level(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(j).Scheduler.Result.MWh,...
                                                  Data.Asset(i).Reservoir(j).Scheduler.Result.CubicMetres,Export.MWh,'InfiltrationLoss');
                   end
               end
            else
               if isempty(Data.Asset(i).Reservoir(1).ScenarioWaterManager.Result.InfiltrationLoss) % no InfiltrationLoss calculated
                  Asset(Count).InfiltrationLoss = zeros(length(t),nRes);
               else
                  for j = 1:nRes
                     Asset(Count).InfiltrationLoss(:,j) = AdaptUnitMWh(Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result.InfiltrationLoss(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result.Level(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result.MWh,...
                                                  Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result.CubicMetres,Export.MWh,'InfiltrationLoss');
                  end
               end
            end
            Asset(Count).InfiltrationLoss = getResolutedValues(Asset(Count).InfiltrationLoss, t, tStart, tEnd,iff(Export.MWh,'sum','mean'),'auto', Data);
        end
    catch
      %%%TODO
       %Log{Count} = ['Asset ' num2str(i) ' - ' Data.Asset(i).Name ' - Error: ' lasterr];
       %Data.Scheduler.Result.LogText = WriteLogFile(Data.Status.Optimization.LogFolder,Log,now,now,'Export');
        %if ~handles.BatchMode
         %  errordlgx(handles.BatchMode, ['Error in aquiring Reservoir results: ' lasterr]);
         %  beep
        %end
        result = ['Error in aquiring Reservoir results: ']
       return
    end


    try
        % Flow
        if (Export.Flow == 1) && (nFlows > 0)
            if Export.Scheduler == 1 %Scheduler
               for j = 1:nFlows
                   FromRes = Data.Asset(i).Topology.Flow(j).OperatesFrom;
                   Asset(Count).Flow(:,j) = AdaptUnitMWh(Data.Asset(i).Flow(j).Scheduler.Result.Operation(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(FromRes).Scheduler.Result.Level(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(FromRes).Scheduler.Result.MWh,...
                                                  Data.Asset(i).Reservoir(FromRes).Scheduler.Result.CubicMetres,Export.MWh,'Flow');
                end
            else
               for j = 1:nFlows
                   FromRes = Data.Asset(i).Topology.Flow(j).OperatesFrom;
                   Asset(Count).Flow(:,j) = AdaptUnitMWh(Data.Asset(i).Flow(j).ScenarioWaterManager.Result.Operation(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(FromRes).ScenarioWaterManager.Result.Level(StartIdx:EndIdx),...
                                                  Data.Asset(i).Reservoir(FromRes).ScenarioWaterManager.Result.MWh,...
                                                  Data.Asset(i).Reservoir(FromRes).ScenarioWaterManager.Result.CubicMetres,Export.MWh,'Flow');
               end
            end
            Asset(Count).Flow = getResolutedValues(Asset(Count).Flow, t, tStart, tEnd,iff(Export.MWh,'sum','mean'),'auto', Data);
        end


        %Inflow
        if Export.Inflow == 1
            if Export.Scheduler == 1 %Scheduler
               for j = 1:nRes
                  Resu = Data.Asset(i).Reservoir(j).Scheduler.Result;
                  Asset(Count).Inflow(:,j) = AdaptUnitMWh(Resu.Inflow(StartIdx:EndIdx),Resu.Level(StartIdx:EndIdx),...
                                                  Resu.MWh,Resu.CubicMetres,Export.MWh,'Inflow');
               end
            else
               for j = 1:nRes
                  Resu = Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result;
                  Asset(Count).Inflow(:,j) = AdaptUnitMWh(Resu.Inflow(StartIdx:EndIdx),Resu.Level(StartIdx:EndIdx),...
                                                          Resu.MWh,Resu.CubicMetres,Export.MWh,'Inflow');
               end
            end
            Asset(Count).Inflow = getResolutedValues(Asset(Count).Inflow, t, tStart, tEnd,iff(Export.MWh,'sum','mean'),'auto', Data);
        end

    catch
      %%%TODO
       %Log{Count} = ['Asset ' num2str(i) ' - ' Data.Asset(i).Name ' - Error: ' lasterr];
       %Data.Scheduler.Result.LogText = WriteLogFile(Data.Status.Optimization.LogFolder,Log,now,now,'Export');

       %if ~handles.BatchMode
       %    errordlgx(handles.BatchMode, ['Error in aquiring Flow/Inflow results: ' lasterr]);
       %    beep
       %end
        result = ['Error in aquiring Flow/Inflow results: ']
       return
    end


    try
        %Turbine operation
        if Export.Turbine == 1
           if Export.Scheduler == 1 %Scheduler
              for j = 1:nTurb
                 Asset(Count).Turbine(:,j) = AdaptUnitMW(Data.Asset(i).Engine(j).Scheduler.Result.Operation(StartIdx:EndIdx)',...
                                                         Data.Asset(i).Engine(j).Scheduler.Result.AlphaPower,Export.MWh);

              end
           else %Scenario Water Management
              for j = 1:nTurb
                 Asset(Count).Turbine(:,j) = AdaptUnitMW(Data.Asset(i).Engine(j).ScenarioWaterManager.Result.Operation(StartIdx:EndIdx)',...
                                                         Data.Asset(i).Engine(j).ScenarioWaterManager.Result.AlphaPower,Export.MWh);
              end
           end
           Asset(Count).Turbine = getResolutedValues(Asset(Count).Turbine, t, tStart, tEnd,iff(Export.MWh,'sum','mean'),'auto', Data);
        end

        %Pump
        if Export.Pump == 1 && nPumps > 0
             if Export.Scheduler == 1 %Scheduler
                 for j = 1:nPumps
                    Asset(Count).Pump(:,j) = AdaptUnitMW(Data.Asset(i).Engine(nTurb+j).Scheduler.Result.Operation(StartIdx:EndIdx)',...
                                                      Data.Asset(i).Engine(nTurb+j).Scheduler.Result.AlphaPower,Export.MWh);
                 end
             else %Scenario Water Management
                 for j = 1:nPumps
                    Asset(Count).Pump(:,j) = AdaptUnitMW(Data.Asset(i).Engine(nTurb+j).ScenarioWaterManager.Result.Operation(StartIdx:EndIdx)',...
                                                      Data.Asset(i).Engine(nTurb+j).ScenarioWaterManager.Result.AlphaPower,Export.MWh);
                 end
             end
            Asset(Count).Pump = getResolutedValues(Asset(Count).Pump, t, tStart, tEnd,iff(Export.MWh,'sum','mean'),'auto', Data);
        end
     catch
      %%%TODO
       %Log{Count} = ['Asset ' num2str(i) ' - ' Data.Asset(i).Name ' - Error: ' lasterr];
       %Data.Scheduler.Result.LogText = WriteLogFile(Data.Status.Optimization.LogFolder,Log,now,now,'Export');
       % if ~handles.BatchMode
       %    errordlgx(handles.BatchMode, ['Error in aquiring Engine results: ' lasterr]);
       %    beep
       % end
        result = ['Error in aquiring Engine results: ']
       return
    end

    try
        %Price
        if Export.Price==1
            if Export.Scheduler == 1 %Scheduler
                Asset(Count).Price = Data.Asset(i).Scheduler.Result.ExpectedSpotPrice(StartIdx:EndIdx);
            else %Scenario Water Management
                Asset(Count).Price = Data.Asset(i).ScenarioWaterManager.Result.ExpectedSpotPrice(StartIdx:EndIdx);
            end
            Asset(Count).Price = getResolutedValues(Asset(Count).Price, t, tStart, tEnd,'mean',2, Data);
        end

        %Margin Prices
        if Export.MarginPrices == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1)
            for j = 1:nEngines
               if Export.Scheduler == 1 %Scheduler
                  MP = Data.Asset(i).Engine(j).Scheduler.Result.MarginPrice;
               else
                  MP = Data.Asset(i).Engine(j).ScenarioWaterManager.Result.MarginPrice;
               end
               Asset(Count).MarginPrices = RoundValues([Asset(Count).MarginPrices MP(:)],'auto', Data);
            end
        end

        %Margin Price Time Series
        if Export.MarginPriceTS == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1)
            clear MP
            for j = 1:nEngines
               if Export.Scheduler == 1 %Scheduler
                  MP(:,j) = Data.Asset(i).Engine(j).Scheduler.Result.MarginPriceTS;
               else
                  MP(:,j) = Data.Asset(i).Engine(j).ScenarioWaterManager.Result.MarginPriceTS;
               end
            end
            Asset(Count).MarginPriceTS = getResolutedValues(MP, t, tStart, tEnd,'mean','auto', Data);
        end


        %Water Values
        if Export.WaterValues == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1)
            for j = 1:nRes
                if Data.Asset(i).Reservoir(j).IsStochastic

                   if Export.Scheduler == 1 %Scheduler
                      Resu = Data.Asset(i).Reservoir(j).Scheduler.Result;
                      WV = AdaptUnitMWh(Resu.WaterValue,Resu.Level(StartIdx),Resu.MWh,Resu.CubicMetres,Export.MWh,'WaterValue');
                   else
                      Resu = Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result;
                      WV = AdaptUnitMWh(Resu.WaterValue,Resu.Level(StartIdx),Resu.MWh,Resu.CubicMetres,Export.MWh,'WaterValue');
                   end
                   Asset(Count).WaterValues = RoundValues([Asset(Count).WaterValues WV(:)],'auto', Data);
                end
            end
        end


        %Water Value Time Series
        if Export.WaterValueTS == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1)
            WV = [];
            for j = 1:nRes
                if Data.Asset(i).Reservoir(j).IsStochastic
                   if Export.Scheduler == 1 %Scheduler
                      Resu = Data.Asset(i).Reservoir(j).Scheduler.Result;
                      WV(:,end+1) = AdaptUnitMWh(Resu.WaterValueTS,Resu.Level(StartIdx),Resu.MWh,Resu.CubicMetres,Export.MWh,'WaterValue');
                   else
                      Resu = Data.Asset(i).Reservoir(j).ScenarioWaterManager.Result;
                      WV(:,end+1) = AdaptUnitMWh(Resu.WaterValueTS,Resu.Level(StartIdx),Resu.MWh,Resu.CubicMetres,Export.MWh,'WaterValue');
                   end
                end
            end
            Asset(Count).WaterValueTS = getResolutedValues(WV, t, tStart, tEnd,'mean','auto', Data);
        end

    catch
      %%%TODO
       %Log{Count} = ['Asset ' num2str(i) ' - ' Data.Asset(i).Name ' - Error: ' lasterr];
       %Data.Scheduler.Result.LogText = WriteLogFile(Data.Status.Optimization.LogFolder,Log,now,now,'Export');

       %if ~handles.BatchMode
       %    errordlgx(handles.BatchMode, ['Error in aquiring Price/MarginPrice / Watervalue results: ' lasterr]);
       %    beep
       %end
        result = ['Error in aquiring Price/MarginPrice / Watervalue results: ']
       return
    end


    try
        %Reservoir Usage
        if Export.ReservoirUsage == 1 && (Export.Excel == 1 || Export.MAT == 1)
           if Export.ScenarioWaterMgt
              Asset(Count).ResUsageMin = Data.Asset(i).ScenarioWaterManager.Result.ReservoirUsageMin;
              Asset(Count).ResUsageMax = Data.Asset(i).ScenarioWaterManager.Result.ReservoirUsageMax;
           else
              Asset(Count).ResUsageMin = Data.Asset(i).Scheduler.Result.ReservoirUsageMin;
              Asset(Count).ResUsageMax = Data.Asset(i).Scheduler.Result.ReservoirUsageMax;
           end
        end

    catch
        %%TODO
       %Log{Count} = ['Asset ' num2str(i) ' - ' Data.Asset(i).Name ' - Error: ' lasterr];
       %Data.Scheduler.Result.LogText = WriteLogFile(Data.Status.Optimization.LogFolder,Log,now,now,'Export');

       %if ~handles.BatchMode
       %    errordlgx(handles.BatchMode, ['Error in aquiring Reservoirlevel results: ' lasterr]);
       %    beep
       %end
        result = ['Error in aquiring Reservoirlevel results: ']
       return
    end



    try
        %Revenues
        %%%TODO
        if Export.Revenues == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1) %&& strcmp('on',get(handles.checkbox_Revenues,'enable'))

           if Export.ScenarioWaterMgt
              Result = Data.Asset(i).ScenarioWaterManager.Result;
           else
              Result = Data.Asset(i).Scheduler.Result;
           end

           Asset(Count).Rev = RoundValues(Result.OverallRevenue','auto', Data);
           if isfield(Result, 'OverallReserveRevenue')
               Asset(Count).ResRev = RoundValues(Result.OverallReserveRevenue', 'auto', Data);
           else
               Asset(Count).ResRev = 0;
           end
           Asset(Count).HRev = RoundValues(Result.HedgeRevenue','auto', Data);
           Asset(Count).HVal = RoundValues(Result.HedgeValue * ones(size(Asset(Count).HRev)),'auto', Data);
           Asset(Count).TurbRev = RoundValues(Result.TurbineRevenue','auto', Data);

           Asset(Count).PumpCost = RoundValues(Result.PumpCost','auto', Data);
           Asset(Count).VarOpCost = RoundValues(Result.VariableOperatingCost','auto', Data);
           Asset(Count).StartUpCost = RoundValues(Result.StartUpCost','auto', Data);
           Asset(Count).ShutDownCost = RoundValues(Result.ShutDownCost','auto', Data);

           try
            Asset(Count).Production = RoundValues(Result.Production','auto', Data);
            Asset(Count).Consumption = RoundValues(Result.Consumption','auto', Data);
           catch err
           end
        end

        %Reserve Revenues
        %%%TODO
        if Export.ReserveRevenues == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1) && Export.ScenarioWaterMgt %&& strcmp('on',get(handles.checkbox_Revenues,'enable'))

            Result = Data.Asset(i).ScenarioWaterManager.Result;
            Asset(Count).ReserveRevenues = RoundValues(Result.ReserveRevenues', 'auto', Data);
            Asset(Count).ReserveNames = Result.ReserveNames;

        end




        %Revenues/Energy monthly
        %TODO
        if Export.RevenuesMonthly == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1) %&& strcmp('on',get(handles.checkbox_Revenues,'enable'))

           if Export.ScenarioWaterMgt
             Result = Data.Asset(i).ScenarioWaterManager.Result;
           else
             Result = Data.Asset(i).Scheduler.Result;
           end

           Asset(Count).ProductionM = RoundValues(reshape(sum(Result.MEnergy(:,1:nTurb,:),2),[],1),'auto', Data);
           Asset(Count).ConsumptionM = RoundValues(reshape(sum(Result.MEnergy(:,nTurb+1:nEngines,:),2),[],1),'auto', Data);

           Asset(Count).TurbRevM = RoundValues(reshape(sum(Result.MTurnover(:,1:nTurb,:),2),[],1),'auto', Data);
           Asset(Count).PumpCostM = RoundValues(reshape(sum(Result.MTurnover(:,nTurb+1:nEngines,:),2),[],1),'auto', Data);

           Asset(Count).VarOpCostM = RoundValues(reshape(sum(Result.MVariableOpCost,2),[],1),'auto', Data);
           Asset(Count).StartUpCostM = RoundValues(reshape(sum(Result.MStartupCost,2),[],1),'auto', Data);
           Asset(Count).ShutDownCostM = RoundValues(reshape(sum(Result.MShutdownCost,2),[],1),'auto', Data);

           Asset(Count).RevM = Asset(Count).TurbRevM + Asset(Count).PumpCostM + Asset(Count).VarOpCostM + ...
                              Asset(Count).StartUpCostM + Asset(Count).ShutDownCostM;

        end

        %Revenues/Energy per engine
        %%TODO
        if Export.RevenuesEngine == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1) %&& strcmp('on',get(handles.checkbox_Revenues,'enable'))

           if Export.ScenarioWaterMgt
             Result = Data.Asset(i).ScenarioWaterManager.Result;
           else
             Result = Data.Asset(i).Scheduler.Result;
           end

           Asset(Count).EnergyE = RoundValues(reshape(sum(Result.MEnergy,1),nEngines,nScenarios)','auto', Data);
           Asset(Count).TurnoverE = RoundValues(reshape(sum(Result.MTurnover,1),nEngines,nScenarios)','auto', Data);
           Asset(Count).VarOpCostE = RoundValues(reshape(sum(Result.MVariableOpCost,1),nEngines,nScenarios)','auto', Data);
           Asset(Count).StartUpCostE = RoundValues(reshape(sum(Result.MStartupCost,1),nEngines,nScenarios)','auto', Data);
           Asset(Count).ShutDownCostE = RoundValues(reshape(sum(Result.MShutdownCost,1),nEngines,nScenarios)','auto', Data);
           Asset(Count).StartupE = RoundValues(reshape(sum(Result.MStartups,1),nEngines,nScenarios)','auto', Data);

        end

        %TODO
        if Export.RevenuesEngineMonthly == 1 && Export.Separated == 1 && (Export.Excel == 1 || Export.MAT == 1) %&& strcmp('on',get(handles.checkbox_Revenues,'enable'))

           if Export.ScenarioWaterMgt
             Result = Data.Asset(i).ScenarioWaterManager.Result;
           else
             Result = Data.Asset(i).Scheduler.Result;
           end

           Asset(Count).EnergyEM = RoundValues(Result.MEnergy,'auto', Data);
           Asset(Count).TurnoverEM = RoundValues(Result.MTurnover,'auto', Data);
           Asset(Count).VarOpCostEM = RoundValues(Result.MVariableOpCost,'auto', Data);
           Asset(Count).StartUpCostEM = RoundValues(Result.MStartupCost,'auto', Data);
           Asset(Count).ShutDownCostEM = RoundValues(Result.MShutdownCost,'auto', Data);
           Asset(Count).StartupEM = RoundValues(Result.MStartups,'auto', Data);
        end

    catch
      %%TODO
       %Log{Count} = ['Asset ' num2str(i) ' - ' Data.Asset(i).Name ' - Error: ' lasterr];
       %Data.Scheduler.Result.LogText = WriteLogFile(Data.Status.Optimization.LogFolder,Log,now,now,'Export');

       %if ~handles.BatchMode
       %    errordlgx(handles.BatchMode, ['Error in aquiring Revenue results: ' lasterr]);
       %    beep
       %end
        result = ['Error in aquiring Revenue results: ']
       return
    end
end

        s = 'HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERE'
%adapt t
if Export.hourly == 1
    t = AdaptTime(t,'hourly', Data);
elseif Export.daily == 1
    t = AdaptTime(t,'daily', Data);
elseif Export.weekly == 1
    t = AdaptTime(t,'weekly', Data);
elseif Export.monthly == 1
    t = AdaptTime(t,'monthly', Data);
end
        s = 'HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERE'

%Aggregated or separated
if Export.Aggregated
    Res = 0;
    Inflow = 0;
    Spill = 0;
    Flow = 0;
    InfiltrationLoss = 0;
    Turbine = 0;
    Pump = 0;

    for i = 1:length(As)
        Res = Res + sum(Asset(i).Res,2);
        Inflow = Inflow + sum(Asset(i).Inflow,2);
        Spill = Spill + sum(Asset(i).Spill,2);
        InfiltrationLoss = InfiltrationLoss + sum(Asset(i).InfiltrationLoss,2);
        Turbine = Turbine + sum(Asset(i).Turbine,2);
        Price = Asset(i).Price;

        if Data.Asset(As(i)).Topology.nPumps % add pumps only if there are any
           Pump = Pump + sum(Asset(i).Pump,2);
        end

        if Data.Asset(As(i)).Topology.nFlows % add flows only if there are any
           Flow = Flow + sum(Asset(i).Flow,2);
        end
    end

    Asset = [];
    Asset.Price = RoundValues(Price,2, Data);
    Asset.Res = RoundValues(Res,'auto', Data);
    Asset.Inflow = RoundValues(Inflow,'auto', Data);
    Asset.Spill = RoundValues(Spill,'auto', Data);
    Asset.Flow = RoundValues(Flow,'auto', Data);
    Asset.InfiltrationLoss = RoundValues(InfiltrationLoss,'auto', Data);
    Asset.Turbine = RoundValues(Turbine,'auto', Data);
    Asset.Pump = RoundValues(Pump,'auto', Data);
end

%**************************************************************************
%******************* Write files: Excel or Csv ****************************
%**************************************************************************

Status = 0;

%TODO
try
   % repl = @(s,s1,s2,r) regexprep(s,strcat('(?=',s1,').*(?<=',s2,')'),r(regexp(s,strcat('(?<=',s1,').*(?=',s2,')'),'match')));
   % i = Data.Status.BatchManager.Current;
   % n = Data.Status.BatchManager.nSteps;
   % Export.Filename = repl(Export.Filename,'{','}',@(x) num2str(eval(x{1})));
%    disp '-----------------------------------';
%    disp(i);
%    disp(Export.Filename);
catch
end


%TODO
if Export.Excel == 1
   Status = writeExcel(Asset,As,t,Export, Data);
elseif Export.CSV == 1
   Status = writeCSV(Asset,As,t,Export, Data);
elseif Export.MAT == 1
   Status = writeMAT(Asset,As,t,Export, Data);
end

result = ['OK']

%%TODO
%if Status == 1 && (~handles.BatchMode)  % Dialogue only if not in BatchMode
%   infodlgx(handles.BatchMode, 'Export finished.');
%elseif Status ~= 1 && (~handles.BatchMode)
%   errordlgx(handles.BatchMode, 'Export didn''t finish.');
%end

function [FigData,Start,End] = getDateSelectors(FigData, Data);

StartYearString = num2str(Data.Export.StartYear);

% FigData might be one of Scheduler, WaterMgr, RiskMgr.
FigData.StartDay = Data.Export.StartDay;
FigData.StartMonth = Data.Export.StartMonth;

% StartYearVal = get(handles.popupmenu_StartYear,'value');
% FigData.StartYear = str2num(StartYearString{StartYearVal});
FigData.StartYear =  Data.Export.StartYear;

StartMonthString = num2str(FigData.StartMonth);

EndYearString = num2str(Data.Export.EndYear);

FigData.EndDay = Data.Export.EndDay;
FigData.EndMonth = Data.Export.EndMonth;
% EndYearVal = get(handles.popupmenu_EndYear,'value');
% FigData.EndYear = str2num(EndYearString{EndYearVal});
FigData.EndYear =  Data.Export.EndYear;

EndMonthString = num2str(FigData.EndMonth);

Start = datenum(FigData.StartYear, FigData.StartMonth, FigData.StartDay);
End = datenum(FigData.EndYear, FigData.EndMonth, FigData.EndDay);

function [Idx1,Idx2,t] = findT(t,t1,t2)
% entspricht der Funktion Idx = find(t == t2), aber ohne Rundungsissues

Idx1 = find(abs(t-t1)<1e-8);

if nargin == 3 && nargout > 1
   Idx2 = find(abs(t-t2)<1e-8);
   t = t(min(Idx1,Idx2):max(Idx1,Idx2));
end





%**************************************************************************
function t = AdaptTime(t,resolution, Data)
%adapt time vector t to the desired time resolution

%%TODO
%hourly resolution
if isequal(resolution,'hourly')

    %Data = get(gcf,'userdata');
    if Data.Status.Import.FromTime == 0
       t=datestr(t','dd.mm.yyyy HH:MM:SS');
    else % time shift by one hour
       t=datestr(t'+1/24,'dd.mm.yyyy HH:MM:SS');
    end

%daily resolution
elseif isequal(resolution,'daily')
    [Y,M,D] = datevec(t);
    U = uniquex([Y' M' D'],'rows');
    U = datenum(U);
    t = datestr(U,'dd.mm.yyyy');

%weekly resolution (always Mondays)
elseif isequal(resolution,'weekly')
    time(1) = t(1);
    i = 1;
    a = 1;
    while a==1
        i=i+1;
        if weekday(time(i-1)) == 2
            x = time(i-1)+1;
        else
            x = time(i-1);
        end
        NextMon = getNextMonday(x);
        NextMon = findT(t,NextMon);
        if ~isempty(NextMon)
            time(i) = t(NextMon);
        else
            a=2;
            break
        end
    end
    t = datestr(time,'dd.mm.yyyy');

%monthly resolution
elseif isequal(resolution,'monthly')
        [Y,M] = datevec(t);
        U = uniquex([Y' M'],'rows');
        U = datenum([U ones(size(U,1),1)]);
        t = datestr(U,'mm/yyyy');
end

function dateout = getNextMonday(datein)

day = weekday(datein);

if day < 3 %*** Sunday or Monday
    dateout = datein+2-day;
else
    dateout = datein+2+7-day;
end

%**************************************************************************
function TS = AdaptUnitMWh(TSMWh,Level,MWh,M3,UnitMWh,Type)
% Transforms the Unit of the output to the desired format

if UnitMWh % Unit = MWh -> export as is
   TS = TSMWh;
elseif isequal(Type,'Res')    % Unit = M3 -> transform MWh to M3 // Ist die Std. Einheit für R MWh ?
   TS = interpolate(MWh,M3,TSMWh,'cubic');
elseif isequal(Type,'WaterValue')
   LevelM3 = interpolate(MWh,M3,Level,'cubic');
   alpha = (interpolate(M3,MWh,LevelM3+1000,'cubic') - interpolate(M3,MWh, LevelM3,'cubic'))/1000;
   TS = TSMWh * alpha;
else                          % Unit = M3/s -> transform MWh to M3/s
   % Berechne Tangente an Umrechnungsgerade --> für Umrechnung von Zufluss, Spill, etc.
   LevelM3 = interpolate(MWh,M3,Level,'spline');
   alpha = (interpolate(M3,MWh,LevelM3+1000,'spline') - interpolate(M3,MWh, LevelM3,'spline'))/1000;
   TS = TSMWh(:) ./ alpha(:) / 3600;
   % TS = interpolate(MWh,M3,TSMWh)/3600;
end
TS = TS(:);


%**************************************************************************
function [Values,Msg] = getResolutedValues(Values, t, tStart, tEnd, calc, digits, Data)

n = size(Values,2);

[StartIdx,EndIdx,t] = findT(t,tStart,tEnd);
Values = Values(StartIdx:EndIdx,:);
Msg = [];

if Data.Export.hourly % nothing to be done
   % do nothing
end


%daily resolution
if Data.Export.daily

  [Y,M,D] = datevec(t);
  U = uniquex([Y' M' D'],'rows');

  ValuesModified = zeros(size(U,1),n);

  for i=1:size(U,1)
      Idx = find( (Y == U(i,1)) & (M == U(i,2)) &  (D == U(i,3)));
      if isequal(calc,'mean')
          ValuesModified(i,:) = mean(Values(Idx,:));
      elseif isequal (calc, 'sum')
          ValuesModified(i,:) = sum(Values(Idx,:));
      end
  end
  Values = ValuesModified;
end


%weekly resolution
if Data.Export.weekly

  [Y,M,D] = datevec(t);
  dD = [0 diff(D)];
  WD = weekday(t);

  WeekBreak = find(WD==2 & (dD~=0));
  Break = [1 WeekBreak length(t)];

  ValuesModified = zeros(length(Break)-1,n);

  for i=1:length(Break)-1

      Idx = [Break(i):Break(i+1)-1];
      if isequal(calc,'mean')
          ValuesModified(i,:) = mean(Values(Idx,:));
      elseif isequal (calc, 'sum')
          ValuesModified(i,:) = sum(Values(Idx,:));
      end
  end
  Values = ValuesModified;
end


%monthly resolution
if Data.Export.monthly

  [Y,M] = datevec(t);
  U = uniquex([Y' M'],'rows');
  ValuesModified = zeros(size(U,1),n);

  for i=1:size(U,1)
      Idx = find( (Y == U(i,1)) & (M == U(i,2)) );
      if isequal(calc,'mean')
          ValuesModified(i,:) = mean(Values(Idx,:));
      elseif isequal (calc, 'sum')
          ValuesModified(i,:) = sum(Values(Idx,:));
      end
  end
  Values = ValuesModified;
end


if Data.Export.Round & (~Data.Export.Aggregated)
   Values = RoundValues(Values,digits, Data);
end






%**************************************************************************
function [r,I,J] = uniquex(x,varargin)
%Behebt Kompatbilitätsprobleme
v = ver();
d = v.Date;
y = str2num(d(end-3:end));
if y < 2013
    [r,I,J] = unique(x,varargin{:});
else
    [r,I,J] = unique(x,varargin{:},'legacy');
end

function y = interpolate(xx,yy,x, method)

if ~exist('method')
    method = 'spline';
end

method = 'linear';


try
   y = interp1(xx,yy,x,method, 'extrap');
catch
   error(lasterr);
end

if isnan(y(end))
    y(end) = y(end-1);
end
if any(isnan(y))
   Msg = 'Interpolation failed. Result contains NaNs.';
   error(Msg);
end


%**************************************************************************
function Values = RoundValues(Values,digits, Data)
% Round Values if desired
if Data.Export.Round % if aggregated, round on aggregated level
   Values = double(Values); % otherwise problems with roundings

   for j=1:size(Values,3)  % Revenue Engine monthly is a 3-dim array
      for i=1:size(Values,2)
         MaxVal = max(abs(Values(:,i,j)));

         if isequal(digits,'auto') % if round should be determined automatically
            if MaxVal >= 10 % at least two significant digits
               Values(:,i,j) = round(Values(:,i,j));
            elseif MaxVal > 1
               Values(:,i,j) = round(Values(:,i,j)*10)/10; % round with one digit after the comma
            else
               Values(:,i,j) = round(Values(:,i,j)*100)/100; % round with one digit after the comma
            end
         else
            Scale = 10^digits;
            Values(:,i,j) = round(Values(:,i,j)*Scale)/Scale;
         end
      end
   end
end


%***********************************************************************
function Status = writeCSV(Asset,As,t,Export, Data)
%writes Csv Files


Status = 0;
%%TODO
%if handles.BatchMode == 0
%   overwrite = '?';
%elseif handles.Batch.OverwriteFiles == 1
%   overwrite = 'OK';
%else
   overwrite = '?';
%end

for i=1:length(As)

    nPumps = Data.Asset(As(i)).Topology.nPumps;
    nTurb = Data.Asset(As(i)).Topology.nTurbines;
    nFlows = Data.Asset(As(i)).Topology.nFlows;
    nRes = Data.Asset(As(i)).Topology.nRes;
    AssetName = Data.Asset(As(i)).Name;

    ResultsSelection = [Export.ReservoirLevel; Export.Inflow; Export.Turbine;...
    Export.Pump; Export.Price];
    numberExport = sum(ResultsSelection);

    %%TODO
    %Reseroir Level
    if Export.ReservoirLevel == 1
       if Export.Aggregated
           FileName = [Export.ExportFolder '/' Export.Filename ' Reservoir Level.csv'];
           %overwrite = CheckFileName(FileName,overwrite);
           %if isequal(overwrite,'Cancel')
           %    return
           %end
          s = FileName
           writeCSVFile(FileName,Asset(1).Res,t);
       else
        for j=1:nRes
            if nRes == 1 & numberExport == 1
                FileName = [Export.ExportFolder '/' Export.Filename '.csv'];
            else
                if isempty(Data.Asset(As(i)).Reservoir(j).Shortname)
                    ResName = ['Res' num2str(j)];
                else
                    ResName = ['Res' num2str(j) ' - ' Data.Asset(As(i)).Reservoir(j).Shortname];
                end
                FileName = [Export.ExportFolder '/' Export.Filename ' ' num2str(As(i)) ' - ' AssetName ' ' ResName '.csv'];
            end
            %overwrite = CheckFileName(FileName,overwrite);
            %if isequal(overwrite,'Cancel')
            %    return
            %end
          s = FileName
            writeCSVFile(FileName,Asset(i).Res(:,j),t);
        end
        end
    end

    %Inflow
    if Export.Inflow == 1
        if Export.Aggregated
           FileName = [Export.ExportFolder '/' Export.Filename ' Inflow.csv'];
           %overwrite = CheckFileName(FileName,overwrite);
           %if isequal(overwrite,'Cancel'), return, end
          s = FileName
           writeCSVFile(FileName,Asset(1).Inflow,t);
        else
            for j=1:nRes
                if nRes == 1 & numberExport == 1
                    FileName = [Export.ExportFolder '/' Export.Filename '.csv'];
                else
                    if isempty(Data.Asset(As(i)).Reservoir(j).Shortname)
                        Tag = ['Res' num2str(j)];
                    else
                        Tag = ['Res' num2str(j) ' - ' Data.Asset(As(i)).Reservoir(j).Shortname];
                    end
                    Name = ['Inflow ' Tag];
                    FileName = [Export.ExportFolder '/' Export.Filename ' ' num2str(As(i)) ' - ' AssetName ' ' Name '.csv'];
                end
                %overwrite = CheckFileName(FileName,overwrite);
                %if isequal(overwrite,'Cancel')
                %    return
                %end
          s = FileName
                writeCSVFile(FileName,Asset(i).Inflow(:,j),t);
            end
        end
    end

    %%TODO
    %Spill
    if Export.Spill == 1
        if Export.Aggregated
           FileName = [Export.ExportFolder '/' Export.Filename ' Spill.csv'];
           %overwrite = CheckFileName(FileName,overwrite);
           %if isequal(overwrite,'Cancel'), return, end
          s = FileName
           writeCSVFile(FileName,Asset(1).Spill,t);
        else
            for j=1:nRes
                if nRes == 1 & numberExport == 1
                    FileName = [Export.ExportFolder '/' Export.Filename '.csv'];
                else
                    if isempty(Data.Asset(As(i)).Reservoir(j).Shortname)
                        Tag = ['Res' num2str(j)];
                    else
                        Tag = ['Res' num2str(j) ' - ' Data.Asset(As(i)).Reservoir(j).Shortname];
                    end
                    Name = ['Spill ' Tag];
                    FileName = [Export.ExportFolder '/' Export.Filename ' ' num2str(As(i)) ' - ' AssetName ' ' Name '.csv'];
                end
                %overwrite = CheckFileName(FileName,overwrite);
                %if isequal(overwrite,'Cancel')
                %    return
                %end
          s = FileName
                writeCSVFile(FileName,Asset(i).Spill(:,j),t);
            end
        end
    end

    %TODO
    %Flow
    if Export.Flow == 1
        if Export.Aggregated
           FileName = [Export.ExportFolder '/' Export.Filename ' Flow.csv'];
           %overwrite = CheckFileName(FileName,overwrite);
           %if isequal(overwrite,'Cancel'), return, end
          s = FileName
           writeCSVFile(FileName,Asset(1).Flow,t);
        else
            for j=1:nFlows
                if nFlows == 1 & numberExport == 1
                    FileName = [Export.ExportFolder '/' Export.Filename '.csv'];
                else
                    if isempty(Data.Asset(As(i)).Flow(j).Shortname)
                        Name = ['Flow' num2str(j)];
                    else
                        Name = ['Flow' num2str(j) ' - ' Data.Asset(As(i)).Engine(j).Shortname];
                    end
                    FileName = [Export.ExportFolder '/' Export.Filename ' ' num2str(As(i)) ' - ' AssetName ' ' Name '.csv'];
                end
                %overwrite = CheckFileName(FileName,overwrite);
                %if isequal(overwrite,'Cancel')
                %    return
                %end
          s = FileName
                writeCSVFile(FileName,Asset(i).Flow(:,j),t);
            end
        end
    end

    %%TODO
    %InfiltrationLoss
    if Export.InfiltrationLoss == 1
        if Export.Aggregated
           FileName = [Export.ExportFolder '/' Export.Filename ' InfiltrationLoss.csv'];
           %overwrite = CheckFileName(FileName,overwrite);
           %if isequal(overwrite,'Cancel'), return, end
          s = FileName
           writeCSVFile(FileName,Asset(1).InfiltrationLoss,t);
        else
            for j=1:nRes
                if nRes == 1 & numberExport == 1
                    FileName = [Export.ExportFolder '/' Export.Filename '.csv'];
                else
                    if isempty(Data.Asset(As(i)).Reservoir(j).Shortname)
                        Tag = ['Res' num2str(j)];
                    else
                        Tag = ['Res' num2str(j) ' - ' Data.Asset(As(i)).Reservoir(j).Shortname];
                    end
                    Name = ['InfiltrationLoss ' Tag];
                    FileName = [Export.ExportFolder '/' Export.Filename ' ' num2str(As(i)) ' - ' AssetName ' ' Name '.csv'];
                end
                %overwrite = CheckFileName(FileName,overwrite);
                %if isequal(overwrite,'Cancel')
                %    return
                %end
          s = FileName
                writeCSVFile(FileName,Asset(i).InfiltrationLoss(:,j),t);
            end
        end
    end

    %%TODO
    %Turbine
    if Export.Turbine == 1
        if Export.Aggregated
           FileName = [Export.ExportFolder '/' Export.Filename ' Turbine.csv'];
           %overwrite = CheckFileName(FileName,overwrite);
           %if isequal(overwrite,'Cancel'), return, end
          s = FileName
           writeCSVFile(FileName,Asset(1).Turbine,t);
        else
            for j=1:nTurb
                if nTurb == 1 & numberExport == 1
                    FileName = [Export.ExportFolder '/' Export.Filename '.csv'];
                else
                    if isempty(Data.Asset(As(i)).Engine(j).Shortname)
                        Name = ['Turbine' num2str(j)];
                    else
                        Name = ['Turbine' num2str(j) ' - ' Data.Asset(As(i)).Engine(j).Shortname];
                    end
                    FileName = [Export.ExportFolder '/' Export.Filename ' ' num2str(As(i)) ' - ' AssetName ' ' Name '.csv'];
                end
                %overwrite = CheckFileName(FileName,overwrite);
                %if isequal(overwrite,'Cancel')
                %    return
                %end
          s = FileName
                writeCSVFile(FileName,Asset(i).Turbine(:,j),t);
            end
        end
    end

    %%TODO
    %Pump
    if Export.Pump == 1
        if Export.Aggregated
           FileName = [Export.ExportFolder '/' Export.Filename ' Pump.csv'];
           %overwrite = CheckFileName(FileName,overwrite);
           %if isequal(overwrite,'Cancel'), return, end
          s = FileName
           writeCSVFile(FileName,Asset(1).Pump,t);
        else
            for j=1:nPumps
                if nPumps == 1 & numberExport == 1
                    FileName = [Export.ExportFolder '/' Export.Filename '.csv'];
                else
                    if isempty(Data.Asset(As(i)).Engine(j+nTurb).Shortname)
                        Name = ['Pump ' num2str(j)];
                    else
                        Name = ['Pump ' num2str(j) ' - ' Data.Asset(As(i)).Engine(j+nTurb).Shortname];
                    end
                    FileName = [Export.ExportFolder '/' Export.Filename ' ' num2str(As(i)) ' - ' AssetName ' ' Name '.csv'];
                end
                %overwrite = CheckFileName(FileName,overwrite);
                %if isequal(overwrite,'Cancel')
                %    return
                %end
          s = FileName
                writeCSVFile(FileName,Asset(i).Pump(:,j),t);
            end
        end
    end

    %%TODO
    %Price
    if Export.Price == 1
        if Export.Aggregated
           FileName = [Export.ExportFolder '/' Export.Filename ' Price.csv'];
           %overwrite = CheckFileName(FileName,overwrite);
           %if isequal(overwrite,'Cancel'), return, end
          s = FileName
           writeCSVFile(FileName,Asset(1).Price,t);
        else
            if numberExport == 1
                FileName = [Export.ExportFolder '/' Export.Filename '.csv'];
            else
                FileName = [Export.ExportFolder '/' Export.Filename ' ' num2str(As(i)) ' - ' AssetName ' Price.csv'];
            end
            %overwrite = CheckFileName(FileName,overwrite);
            %if isequal(overwrite,'Cancel')
            %    return
            %end
          s = FileName
            writeCSVFile(FileName,Asset(i).Price,t);
        end
    end
end
Status = 1;


%**************************************************************************
function writeCSVFile(FileName,Values,t)

%%TODO
%ValStr = sprintf(';%8.2f\n',Values);
%ValStr = reshape(ValStr,[],size(t,1))';
%WriteStr = [t ValStr];
FileName = [pwd, '/', FileName];
fid = fopen(FileName,'w');
for j=1:size(t,1)
    %fprintf(fid,WriteStr(j,:));
    fprintf(fid, sprintf('%s;%8.2f\n',t(j,:),Values(j,:)));
    %printf(sprintf('%s;%8.2f\n',t(j,:),Values(j,:)));
end
fclose(fid);

%**************************************************************************
function Status = writeExcel(Asset,As,t,Export, Data)

Status = 0;
%get FileNames
FileName = {};
SameName = 0;

%%TODO
%Export.ExportFolder = expand(Export.ExportFolder);
Export.ExportFolder = [pwd, '/', Export.ExportFolder];
s = Export.ExportFolder

%TODO
excelVersion = 10;
% determine Excel version and set file extension
%X = actxserver('Excel.Application');
%excelVersion = str2double(X.Version);
%X.Quit
%X.delete
%clear X;

if excelVersion < 12
   excelExtension = '.xls';
else
   excelExtension = '.xlsx';
end


if length(Asset)>1
    for i=1:length(As)
        Name = Data.Asset(As(i)).Name;
        if isempty(Export.Filename)
           FileName{i}=[Export.ExportFolder '/' num2str(As(i)) ' - '  Name excelExtension];
        else
           FileName{i}=[Export.ExportFolder '/' Export.Filename ' ' num2str(As(i)) ' - '  Name excelExtension];
        end
    end
else
    FileName{1} = [Export.ExportFolder '/' Export.Filename excelExtension];
    As = 1; % only one asset
end

%%TODO
%if handles.BatchMode == 0
%   overwrite = '?';
%elseif handles.Batch.OverwriteFiles == 1
%   overwrite = 'OK';
%else
%   overwrite = '?';
%end

%%TODO
%for i=1:length(FileName)
%    overwrite = CheckFileName(FileName{i},overwrite);
%    if isequal(overwrite,'Cancel')
%        return
%    end
%end

%writes Excel Files
tcell = cellstr(t);

if Export.MWh
   ResUnit = '[MWh]';
   FlowUnit = '[MWh]';
else
   ResUnit = '[m3]';
   FlowUnit = '[m3/s]';
end

if Export.Round
   NumberFormat = ''; % no format
else
   NumberFormat = '0.00';
end


for i=1:length(As)

    nPumps = Data.Asset(As(i)).Topology.nPumps;
    nTurb = Data.Asset(As(i)).Topology.nTurbines;
    nFlows = Data.Asset(As(i)).Topology.nFlows;
    nRes = Data.Asset(As(i)).Topology.nRes;
    nEngines = nTurb + nPumps;

    if Data.Export.Scheduler
       nScenarios = 1;
       DateNum = Data.Asset(As(i)).Scheduler.Result.DateNum;
    else
       nScenarios = Data.Asset(As(i)).ScenarioWaterManager.Input.nScenarios;
       DateNum = Data.Asset(As(i)).ScenarioWaterManager.Result.DateNum;
    end

    [Excel ExcelWorkbook] = XLSOpen;
    nSheets = Excel.Sheets.Count;

    %Reseroir Level
    if Export.ReservoirLevel == 1
        ReservoirLevel = XLSAddSheets(Excel,'Reservoir Level');
        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Content Reservoirs'
           Name{end+1} = 'Sum';
           Unit{end+1} = ResUnit;
        else
           for j=1:nRes
              Tag{end+1}  = ['Content Reservoir ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Reservoir(j).Name;
              Unit{end+1} = ResUnit;
           end
        end
        xlswriteCR(Excel,{ReservoirLevel,ReservoirLevel, ReservoirLevel, ReservoirLevel, ReservoirLevel},{'A4','B1','B2','B3','B4'},...
        {tcell,cellstr(Tag),cellstr(Name),cellstr(Unit),Asset(i).Res},NumberFormat);

    end

    %Inflow
    if Export.Inflow == 1
        Inflow = XLSAddSheets(Excel,'Inflow');
        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Inflow Reservoirs';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;
        else
           for j=1:nRes
              Tag{end+1}  = ['Inflow Reservoir ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Reservoir(j).Name;
              Unit{end+1} = FlowUnit;
           end
        end
        xlswriteCR(Excel,{Inflow, Inflow, Inflow, Inflow, Inflow},{'A4','B1','B2','B3','B4'},...
        {tcell,cellstr(Tag),cellstr(Name),cellstr(Unit),Asset(i).Inflow},NumberFormat);

        % Add a Comment: Inflow validity Date, if export is not aggregated
        if ~Export.Aggregated
            for j=1:nRes

               Str = 'Inflow Scenario Path:\n';

               if Data.Export.Scheduler
                  Folder = Data.Asset(As(i)).Reservoir(j).Scheduler.Result.InflowScenarioFolder;
                  UsedInflowScenarios{1} = Data.Asset(As(i)).Reservoir(j).Scheduler.Result.InflowScenario;
               else % Scenario Manager
                  Folder = Data.Asset(As(i)).Reservoir(j).ScenarioWaterManager.Result.InflowScenarioFolder;
                  UsedInflowScenarios = Data.Asset(As(i)).Reservoir(j).ScenarioWaterManager.Result.UsedInflowScenarios';
               end

               Folder = strrep(Folder,'\','/');
               Str = [Str Folder '\n\n'];

               Str = [Str 'Used Inflow Files:\n'];
               for k=1:length(UsedInflowScenarios)
                  Str = [Str UsedInflowScenarios{k} '\n'];
               end


               if Data.Export.Scheduler == 1
                  IMDate(j) = Data.Asset(As(i)).Reservoir(j).Scheduler.Result.InflowModificationDate;
               else
                  IMDate(j) = Data.Asset(As(i)).Reservoir(j).ScenarioWaterManager.Result.InflowModificationDate;
               end

               InflowModDate = datestr(IMDate(j),'dd-mmm-yyyy HH:MM');
               Str = [Str '\nLast Modification of Inflow File(s):\n' InflowModDate];

               Comment = sprintf(Str);
               XLSAddComment(Excel,[char(double('A')+j) '1'],Comment);
            end
        end
    end

    % Spill
    if Export.Spill == 1
        Spill = XLSAddSheets(Excel,'Spill');
        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Spill Reservoirs';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;
        else
           for j=1:nRes
              Tag{end+1}  = ['Spill Reservoir ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Reservoir(j).Name;
              Unit{end+1} = FlowUnit;
           end
        end
        xlswriteCR(Excel,{Spill, Spill, Spill, Spill, Spill},{'A4','B1','B2','B3','B4'},...
        {tcell,cellstr(Tag),cellstr(Name),cellstr(Unit),Asset(i).Spill},NumberFormat);
    end

    % Flow
    if Export.Flow == 1
        Flow = XLSAddSheets(Excel,'Flow');
        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Flows';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;
        else
           for j=1:nFlows
              Tag{end+1}  = ['Flow ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Flow(j).Name;
              Unit{end+1} = FlowUnit;
           end
        end
        xlswriteCR(Excel,{Flow, Flow, Flow, Flow, Flow},{'A4','B1','B2','B3','B4'},...
        {tcell,cellstr(Tag),cellstr(Name),cellstr(Unit),Asset(i).Flow},NumberFormat);
    end

    % InfiltrationLoss
    if Export.InfiltrationLoss == 1
        InfiltrationLoss = XLSAddSheets(Excel,'InfiltrationLoss');
        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'InfiltrationLoss';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;

        else
           for j=1:nRes
              Tag{end+1}  = ['Reservoir ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Reservoir(j).Name;
              Unit{end+1} = FlowUnit;
           end
        end
        xlswriteCR(Excel,{InfiltrationLoss, InfiltrationLoss, InfiltrationLoss, InfiltrationLoss, InfiltrationLoss},...
         {'A4','B1','B2','B3','B4'},{tcell,cellstr(Tag),cellstr(Name),cellstr(Unit),Asset(i).InfiltrationLoss},NumberFormat);
    end


    %Turbine
    if Export.Turbine == 1
        Turbine = XLSAddSheets(Excel,'Turbine operation');
        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Turbine';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;
        else
           for j=1:nTurb
              Tag{end+1}  = ['Turbine ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Engine(j).Name;
              Unit{end+1} = FlowUnit;
           end
        end
        xlswriteCR(Excel,{Turbine, Turbine, Turbine, Turbine, Turbine},{'A4','B1','B2','B3','B4'},...
        {tcell,cellstr(Tag),cellstr(Name),cellstr(Unit),Asset(i).Turbine},NumberFormat);
    end

    %Pump
    if Export.Pump == 1 & (nPumps | Export.Aggregated)
        Pump = XLSAddSheets(Excel,'Pump operation');
        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Pump';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;
        else
           for j=1:nPumps
              Tag{end+1}  = ['Pump ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Engine(j+nTurb).Name;
              Unit{end+1} = FlowUnit;
           end
        end
        xlswriteCR(Excel,{Pump, Pump, Pump, Pump, Pump},{'A4','B1','B2','B3','B4'},...
        {tcell,cellstr(Tag),cellstr(Name),cellstr(Unit),Asset(i).Pump},NumberFormat);
    end

    %Market Price
    if Export.Price == 1
        Price = XLSAddSheets(Excel,'Market Price');

        if Data.Export.Scheduler
           Result = Data.Asset(As(i)).Scheduler.Result;
        else
           Result = Data.Asset(As(i)).ScenarioWaterManager.Result;
        end
        PriceModDate = datestr(Result.PriceModificationDate,'dd-mmm-yyyy HH:MM');

        Name ={'Price'};
        Unit ={'[€/MWh]'};
        xlswriteCR(Excel,{Price, Price, Price, Price, Price},{'A4','B1','B2','B3','B4'},...
        {tcell,Name,cellstr(PriceModDate),Unit,Asset(i).Price},NumberFormat);

        if ~Export.Aggregated
            Str = ['Price Scenario Path:\n'];

            if Data.Export.Scheduler
               Folder = Data.Asset(As(i)).Scheduler.Result.PriceScenarioFolder;
               UsedPriceScenarios = Data.Asset(As(i)).Scheduler.Result.UsedPriceScenarios;
            else % Scenario Manager
               Folder = Data.Asset(As(i)).ScenarioWaterManager.Result.PriceScenarioFolder;
               UsedPriceScenarios = Data.Asset(As(i)).ScenarioWaterManager.Result.UsedPriceScenarios;
            end

            Folder = strrep(Folder,'\','/');
            Str = [Str Folder '\n\n'];

            Str = [Str 'Used Price Files:\n'];
            for k=1:length(UsedPriceScenarios)
               Str = [Str UsedPriceScenarios{k} '\n'];
            end

            PriceModDate = datestr(Result.PriceModificationDate,'dd-mmm-yyyy HH:MM');
            Str = [Str '\nLast Modification of Price File(s):\n' PriceModDate];

            Comment = sprintf(Str);
            XLSAddComment(Excel,'B2',Comment);
        end
    end

     %Margin Prices
     if Export.MarginPrices == 1 && Export.Separated==1 && ~isempty(Asset(i).MarginPrices)
         MarginPrice = XLSAddSheets(Excel,'Margin Prices');
         Name ={'Scenario'};
         for j = 1:nTurb
             Name{end+1} = ['Turb' num2str(j) ' ' Data.Asset(As(i)).Engine(j).Shortname ' [EUR/MWh]'];
         end
         for j = nTurb+1:nEngines
             Name{end+1} = ['Pump' num2str(j-nTurb) ' ' Data.Asset(As(i)).Engine(j).Shortname ' [EUR/MWh]'];
         end

         xlswriteCR(Excel,{MarginPrice, MarginPrice, MarginPrice},{'A1','A2','B2'},...
             {Name,(1:size(Asset(i).MarginPrices,1))', Asset(i).MarginPrices},NumberFormat);
     end


    %Margin Price Time Series
    if Export.MarginPriceTS == 1 && Export.Separated==1 && ~isempty(Asset(i).MarginPriceTS)

        MPTS = XLSAddSheets(Excel,'Margin Price Time Series');

        Tag  = {};
        Name = {};
        Unit = {};

        for j=1:nEngines
           Tag{end+1}  = ['Engine ' num2str(j)];
           Name{end+1} = Data.Asset(As(i)).Engine(j).Name;
           Unit{end+1} = 'EUR/MWh';
        end

        xlswriteCR(Excel,{MPTS, MPTS, MPTS, MPTS, MPTS},{'A4','B1','B2','B3','B4'},...
        {tcell,cellstr(Tag),cellstr(Name),cellstr(Unit),Asset(i).MarginPriceTS},NumberFormat);
    end



    %WaterValues
     if Export.WaterValues == 1 && Export.Separated==1 && ~isempty(Asset(i).WaterValues)
         WaterValue = XLSAddSheets(Excel,'Water Values');
         Name ={'Scenario'};
         for j = 1:nRes
             if Data.Asset(As(i)).Reservoir(j).IsStochastic
                Name{end+1} = ['Res' num2str(j) ' ' Data.Asset(As(i)).Reservoir(j).Shortname ' [EUR/' ResUnit(2:end)];
             end
         end
         xlswriteCR(Excel,{WaterValue, WaterValue, WaterValue},{'A1','A2','B2'},...
             {Name,(1:nScenarios)', Asset(i).WaterValues},NumberFormat);
     end


     % WaterValue Time Series
     if Export.WaterValueTS == 1 && Export.Separated==1 && ~isempty(Asset(i).WaterValueTS)

        WVTS = XLSAddSheets(Excel,'Water Value Time Series');
        Tag  = {};
        Name = {};
        Unit = {};

        for j=1:nRes
           if Data.Asset(As(i)).Reservoir(j).IsStochastic
              Tag{end+1}  = ['Reservoir ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Reservoir(j).Name;
              Unit{end+1} = [' [EUR/' ResUnit(2:end)];
           end
        end

        xlswriteCR(Excel,{WVTS,WVTS, WVTS, WVTS, WVTS},{'A4','B1','B2','B3','B4'},...
        {tcell,cellstr(Tag),cellstr(Name),cellstr(Unit),Asset(i).WaterValueTS},NumberFormat);
     end


    %Reservoir Usage
     if Export.ReservoirUsage == 1 && Export.Separated==1
         ResUsage = XLSAddSheets(Excel,'Reservoir Usage');

         Name ={'Scenario'};
         MinName = {};
         MaxName = {};
         for j = 1:nRes
             Name{end+1} = ['Res' num2str(j) ' ' Data.Asset(As(i)).Reservoir(j).Shortname];
             MinName{end+1} = 'Minimum';
             MaxName{end+1} = 'Maximum';
         end
         Name = [Name Name(2:end)]; % Namen verdoppeln (Min/Max)

         xlswriteCR(Excel,{ResUsage, ResUsage, ResUsage, ResUsage},{'A2','A3','B1','B3'},...
             {Name,[1:nScenarios]',[MinName MaxName], ...
             [Asset(i).ResUsageMin' Asset(i).ResUsageMax']},NumberFormat);
     end


    %Revenue
    if Export.Revenues == 1 && Export.Separated==1 && strcmp('on',get(handles.checkbox_Revenues,'enable'))

         Revenue = XLSAddSheets(Excel,'Revenue-Energy');
         Name = {'Scenario','Overall Revenues [EUR]','Hedged Revenues [EUR]','Hedge Value [EUR]','',...
                 'Turbine Revenues [EUR]','Pump Costs [EUR]','','Variable Operating Costs [EUR]',...
                 'Startup Costs [EUR]','Shutdown Costs [EUR]','',...
                 'Overall Production [MWh]','Overall Consumption [MWh]','', ...,
                 'Reserve Revenue [EUR]'};

         try
         xlswriteCR(Excel,{Revenue,Revenue,Revenue,Revenue,Revenue,Revenue,Revenue,Revenue,Revenue,Revenue,Revenue,Revenue,Revenue},...
                {'A1','A2','B2','C2','D2','F2','G2','I2','J2','K2','M2','N2','P2'},...
             {Name,(1:nScenarios)', Asset(i).Rev, Asset(i).HRev, Asset(i).HVal ,...
              Asset(i).TurbRev,Asset(i).PumpCost,Asset(i).VarOpCost, Asset(i).StartUpCost,...
              Asset(i).ShutDownCost, Asset(i).Production, Asset(i).Consumption, Asset(i).ResRev} , NumberFormat);
         catch err
         end

    end

   %ReserveRevenue
   if Export.Revenues == 1 && Export.Separated==1 && strcmp('on',get(handles.checkbox_Revenues,'enable')) && isfield(Asset(i), 'ReserveRevenues')
       ReserveRevenue = XLSAddSheets(Excel,'Reserve-Revenues');

       ResName = {};
       ResName(1) = {'Scenario'};
       XlsWriteHeader = {};
       XlsWriteHeader(1) = {ReserveRevenue};
       XlsWriteHeader(2) = {ReserveRevenue};
       XlsWriteCells = {};
       XlsWriteCells(1) = {'A1'};
       XlsWriteCells(2) = {'A2'};
       XlsWriteValues = {};
       XlsWriteCaption = {};


       for j = 1:size(Asset(i).ReserveRevenues, 2)
         ResName(j+1) = strcat(Asset(i).ReserveNames(j), ' Revenue [EUR]');
         XlsWriteHeader(j+2) = {ReserveRevenue};
         XlsWriteCells(j+2) = strcat({char(65+j)}, {'2'});
         %XlsWriteValues(:,j) = Asset(i).ReserveRevenues(:,j);
       end

       XlsWriteCaption = {ResName, (1:nScenarios)', Asset(i).ReserveRevenues};%XlsWriteValues};

       xlswriteCR(Excel, XlsWriteHeader, XlsWriteCells, XlsWriteCaption, NumberFormat);


   end


   %Revenue monthly
   if Export.RevenuesMonthly == 1 && Export.Separated==1 && strcmp('on',get(handles.checkbox_Revenues,'enable'))

      % get time string
      tmonth = AdaptTime(DateNum,'monthly');
      nMonths = size(tmonth,1);

      Scenario = repmat([1:nScenarios],nMonths,1);
      Scenario = Scenario(:);

      tmonth = repmat(tmonth,nScenarios,1);
      tmonth = cellstr(tmonth);

      RevenueM = XLSAddSheets(Excel,'Revenue-Energy monthly');
      Name = {'Scenario','Month','Overall Revenues [EUR]','',...
              'Turbine Revenues [EUR]','Pump Costs [EUR]','','Variable Operating Costs [EUR]',...
              'Startup Costs [EUR]','Shutdown Costs [EUR]','',...
              'Overall Production [MWh]','Overall Consumption [MWh]'};
         try
         xlswriteCR(Excel,{RevenueM,RevenueM,RevenueM,RevenueM,RevenueM,RevenueM,RevenueM,RevenueM,RevenueM,RevenueM,RevenueM},...
                {'A1','A2','B2','C2','E2','F2','H2','I2','J2','L2','M2'},...
             {Name,Scenario,tmonth, Asset(i).RevM, Asset(i).TurbRevM,Asset(i).PumpCostM,...
              Asset(i).VarOpCostM, Asset(i).StartUpCostM,...
              Asset(i).ShutDownCostM, Asset(i).ProductionM, Asset(i).ConsumptionM} , NumberFormat);
         catch err
         end
     end

     %Revenue engine
     if Export.RevenuesEngine == 1 && Export.Separated==1 && strcmp('on',get(handles.checkbox_Revenues,'enable'))

         RevenueE = XLSAddSheets(Excel,'Revenue-Energy Engine');

         % get KPI string
         for j=1:nEngines
            KPIStr{j} = 'Engine Turnover [EUR]';
            KPIStr{j+nEngines} = 'Variable Operating Costs [EUR]';
            KPIStr{j+2*nEngines} = 'Startup Costs [EUR]';
            KPIStr{j+3*nEngines} = 'Shutdown Costs [EUR]';
            KPIStr{j+4*nEngines} = 'Startups';
            KPIStr{j+5*nEngines} = 'Energy [MWh]';
         end

         % get engine string
         for k=1:6
            for j=1:nTurb
               EngStr{(k-1)*nEngines+j} = ['Turb' num2str(j) ' ' Data.Asset(As(i)).Engine(j).Shortname];
            end
            for j=nTurb+1:nEngines
               EngStr{(k-1)*nEngines+j} = ['Pump' num2str(j-nTurb) ' ' Data.Asset(As(i)).Engine(j).Shortname];
            end
         end


         xlswriteCR(Excel,{RevenueE,RevenueE,RevenueE,RevenueE,RevenueE},...
                {'A2','A3','B1','B2','B3'},...
                {{'Scenario'},[1:nScenarios]',KPIStr,EngStr,...
                [Asset(i).TurnoverE Asset(i).VarOpCostE Asset(i).StartUpCostE ...
                 Asset(i).ShutDownCostE Asset(i).StartupE Asset(i).EnergyE]} , NumberFormat);
     end

     %Revenue engine monthly
     if Export.RevenuesEngineMonthly == 1 && Export.Separated==1 && strcmp('on',get(handles.checkbox_Revenues,'enable'))

         RevenueEM = XLSAddSheets(Excel,'Revenue-Energy Engine Monthly');

         % get KPI string
         for j=1:nEngines
            KPIStr{j} = 'Engine Turnover [EUR]';
            KPIStr{j+nEngines} = 'Variable Operating Costs [EUR]';
            KPIStr{j+2*nEngines} = 'Startup Costs [EUR]';
            KPIStr{j+3*nEngines} = 'Shutdown Costs [EUR]';
            KPIStr{j+4*nEngines} = 'Startups';
            KPIStr{j+5*nEngines} = 'Energy [MWh]';
         end

         % get engine string
         for k=1:6
            for j=1:nTurb
               EngStr{(k-1)*nEngines+j} = ['Turb' num2str(j) ' ' Data.Asset(As(i)).Engine(j).Shortname];
            end
            for j=nTurb+1:nEngines
               EngStr{(k-1)*nEngines+j} = ['Pump' num2str(j-nTurb) ' ' Data.Asset(As(i)).Engine(j).Shortname];
            end
         end

         % get time string
         tmonth = AdaptTime(DateNum,'monthly');
         nMonths = size(tmonth,1);

         Scenario = repmat([1:nScenarios],nMonths,1);
         Scenario = Scenario(:);

         tmonth = repmat(tmonth,nScenarios,1);
         tmonth = cellstr(tmonth);

         TurnoverEM = zeros(nMonths*nScenarios,nEngines);
         VarOpCostEM = TurnoverEM;
         StartUpCostEM = TurnoverEM;
         ShutDownCostEM = TurnoverEM;
         StartupEM = TurnoverEM;
         EnergyEM = TurnoverEM;

         for j=1:nScenarios
            Idx = [(j-1)*nMonths+1:j*nMonths];

            TurnoverEM(Idx,:) = Asset(i).TurnoverEM(:,:,j);
            VarOpCostEM(Idx,:) = Asset(i).VarOpCostEM(:,:,j);
            StartUpCostEM(Idx,:) = Asset(i).StartUpCostEM(:,:,j);
            ShutDownCostEM(Idx,:) = Asset(i).ShutDownCostEM(:,:,j);
            StartupEM(Idx,:) = Asset(i).StartupEM(:,:,j);
            EnergyEM(Idx,:) = Asset(i).EnergyEM(:,:,j);
         end

         xlswriteCR(Excel,{RevenueEM,RevenueEM,RevenueEM,RevenueEM,RevenueEM,RevenueEM},...
                {'A2','A3','B3','C1','C2','C3'},...
                {{'Scenario','Month'},Scenario,tmonth,KPIStr,EngStr,...
                [TurnoverEM VarOpCostEM StartUpCostEM ...
                 ShutDownCostEM StartupEM EnergyEM]} , NumberFormat);
     end







    %Log
    if Export.Log & (~Export.Aggregated)
         Log = XLSAddSheets(Excel,'Log');

         if Data.Export.Scheduler
            Input = Data.Asset(As(i)).Scheduler.Input;
            RunTime = Data.Asset(As(i)).Scheduler.Result.RunTime;

            %Folder = Data.Asset(As(i)).Scheduler.Result.PriceScenarioFolder;
            UsedPriceScenarios = Data.Asset(As(i)).Scheduler.Result.UsedPriceScenarios;

            for j=1:length(Data.Asset(As(i)).Reservoir)
               %Folder{j} = Data.Asset(As(i)).Reservoir(j).Scheduler.Result.InflowScenarioFolder;
               UsedInflowScenarios{1,j} = Data.Asset(As(i)).Reservoir(j).Scheduler.Result.InflowScenario;
            end

            nScenarios = 1;
         else
            Input = Data.Asset(As(i)).ScenarioWaterManager.Input;
            RunTime = Data.Asset(As(i)).ScenarioWaterManager.Result.RunTime;

            nScenarios = Data.Asset(As(i)).ScenarioWaterManager.Input.nScenarios;
            UPS = Data.Asset(As(i)).ScenarioWaterManager.Result.UsedPriceScenarios;

            UsedPriceScenarios = cell(nScenarios,1);

            for k=1:nScenarios
               if length(UPS) > 1 % many inflow scenarios used, not only expected inflow
                  UsedPriceScenarios{k} = UPS{k};
               else
                  UsedPriceScenarios{k} = UPS{1};
               end
            end

            for j=1:length(Data.Asset(As(i)).Reservoir)
               UIS = Data.Asset(As(i)).Reservoir(j).ScenarioWaterManager.Result.UsedInflowScenarios;
               for k=1:nScenarios
                  if length(UIS) > 1 % many inflow scenarios used, not only expected inflow
                     UsedInflowScenarios{k,j} = UIS{k};
                  else
                     UsedInflowScenarios{k,j} = UIS{1};
                  end
               end
            end
         end

         clear Str;
         Str{1} = 'LOG INFORMATION';
         Str{end+1} = '';
         Str{end+1} = 'Run Time:';
         Str{end+1} = '';
         Str{end+1} = 'Use Spills:';
         Str{end+1} = 'Use Minimum Number of operating/idle hours:';
         Str{end+1} = 'Use Variable/Startup/Shutdown Costs:';
         Str{end+1} = 'Use Minimum Running Power:';
         Str{end+1} = 'Use Infiltration Losses:';
         Str{end+1} = 'Use Production Reserves:';
         Str{end+1} = 'Use Consumption Reserves:';
         Str{end+1} = 'Use Spinning Production Reserves:';
         Str{end+1} = 'Use Spinning Consumption Reserves:';
         Str{end+1} = 'Use Engine Alternatives:';
         Str{end+1} = 'Use Variable Engine Efficiency:';
         Str = Str';

         clear Val;
         Val{1} = datestr(RunTime,'yyyy-mm-dd HH:MM:SS');
         Val{end+1} = '';
         Val{end+1} = iff(Input.UseSpills,'on','off');
         Val{end+1} = iff(Input.UseConstraints,'on','off');
         Val{end+1} = iff(Input.UseCosts,'on','off');
         Val{end+1} = iff(Input.UseMinRunningFlow,'on','off');
         Val{end+1} = iff(Input.UseInfiltrationLosses,'on','off');
         Val{end+1} = iff(Input.UseProductionReserves,'on','off');
         Val{end+1} = iff(Input.UseConsumptionReserves,'on','off');
         Val{end+1} = iff(Input.UseSpinningProductionReserves,'on','off');
         Val{end+1} = iff(Input.UseSpinningConsumptionReserves,'on','off');
         Val{end+1} = iff(Input.UseEngineAlternatives,'on','off');
         Val{end+1} = iff(Input.UseVariableEfficiency,'on','off');
         Val = Val';

         xlswriteCR(Excel,{Log,Log},{'B2','C4'},{Str,Val});

         Str = {'Scenario','Price'};
         for j=1:length(Data.Asset(As(i)).Reservoir)
            Str{end+1} = ['Inflow Res' num2str(j) ' ' Data.Asset(As(i)).Reservoir(j).Shortname];
         end

         xlswriteCR(Excel,{Log,Log,Log},{'A20','A21','B21'},{Str,[1:nScenarios]',[UsedPriceScenarios UsedInflowScenarios]});
    end

    %delete unnecessary sheets
    for j = 1:nSheets
        XLSDeleteSheets(Excel,1);
    end

    %save Workbooks or show workbooks
    if isempty(Export.Filename) && (length(FileName)==1) % if no filename and only one file
       set(Excel,'Visible',1);
    else
       ExcelWorkbook.SaveAs(FileName{i});
       %close Excel and Workbook
       XLSClose(Excel,ExcelWorkbook);
    end
end

Status = 1;

%**************************************************************************
function Status = writeMAT(Asset,As,t,Export, Data)

%Data = get(gcf,'userdata');
%handles = guidata(gcf);

Status = 0;
%get FileNames
FileName = {};
SameName = 0;

%Export.ExportFolder = expand(Export.ExportFolder);
Export.ExportFolder = [pwd, '/', Export.ExportFolder];

matExtension = '.mat';

if length(Asset)>1
    for i=1:length(As)
        Name = Data.Asset(As(i)).Name;
        if isempty(Export.Filename)
           FileName{i}=[Export.ExportFolder '/' Export.Filename matExtension];
        else
           FileName{i}=[Export.ExportFolder '/' Export.Filename matExtension];
        end
    end
else
    FileName{1} = [Export.ExportFolder '/' Export.Filename matExtension];
    As = 1; % only one asset
end

%%TODO
%if handles.BatchMode == 0
%   overwrite = '?';
%elseif handles.Batch.OverwriteFiles == 1
%   overwrite = 'OK';
%else
%   overwrite = '?';
%end

%%TODO
%for i=1:length(FileName)
%    overwrite = CheckFileName(FileName{i},overwrite);
%    if isequal(overwrite,'Cancel')
%        return
%    end
%end

%writes Excel Files
tcell = cellstr(t);

if Export.MWh
   ResUnit = 'MWh';
   FlowUnit = 'MWh';
else
   ResUnit = 'm3';
   FlowUnit = 'm3/s';
end

assetstruct = [];

for i=1:length(As)

    nPumps = Data.Asset(As(i)).Topology.nPumps;
    nTurb = Data.Asset(As(i)).Topology.nTurbines;
    nFlows = Data.Asset(As(i)).Topology.nFlows;
    nRes = Data.Asset(As(i)).Topology.nRes;
    nEngines = nTurb + nPumps;


    if Data.Export.Scheduler
       nScenarios = 1;
       DateNum = Data.Asset(As(i)).Scheduler.Result.DateNum;
    else
       nScenarios = Data.Asset(As(i)).ScenarioWaterManager.Input.nScenarios;
       DateNum = Data.Asset(As(i)).ScenarioWaterManager.Result.DateNum;
    end

    %Reseroir Level
    if Export.ReservoirLevel == 1
        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Content Reservoirs'
           Name{end+1} = 'Sum';
           Unit{end+1} = ResUnit;
        else
           for j=1:nRes
              Tag{end+1}  = ['Content Reservoir ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Reservoir(j).Name;
              Unit{end+1} = ResUnit;
           end
        end

        assetstruct(i).ReservoirLevel.Tag = Tag;
        assetstruct(i).ReservoirLevel.Name = Name;
        assetstruct(i).ReservoirLevel.Unit = Unit;
        assetstruct(i).ReservoirLevel.Values = Asset(i).Res;
    end

    %Inflow
    if Export.Inflow == 1

        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Inflow Reservoirs';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;
        else
           for j=1:nRes
              Tag{end+1}  = ['Inflow Reservoir ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Reservoir(j).Name;
              Unit{end+1} = FlowUnit;
           end
        end

        assetstruct(i).Inflow.Tag = Tag;
        assetstruct(i).Inflow.Name = Name;
        assetstruct(i).Inflow.Unit = Unit;
        assetstruct(i).Inflow.Values = Asset(i).Inflow;
    end

    % Spill
    if Export.Spill == 1

        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Spill Reservoirs';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;
        else
           for j=1:nRes
              Tag{end+1}  = ['Spill Reservoir ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Reservoir(j).Name;
              Unit{end+1} = FlowUnit;
           end
        end

        assetstruct(i).Spill.Tag = Tag;
        assetstruct(i).Spill.Name = Name;
        assetstruct(i).Spill.Unit = Unit;
        assetstruct(i).Spill.Values = Asset(i).Spill;

    end

    % Flow
    if Export.Flow == 1

        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Flows';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;
        else
           for j=1:nFlows
              Tag{end+1}  = ['Flow ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Flow(j).Name;
              Unit{end+1} = FlowUnit;
           end
        end

        assetstruct(i).Flow.Tag = Tag;
        assetstruct(i).Flow.Name = Name;
        assetstruct(i).Flow.Unit = Unit;
        assetstruct(i).Flow.Values = Asset(i).Flow;

    end

    % InfiltrationLoss
    if Export.InfiltrationLoss == 1

        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'InfiltrationLoss';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;

        else
           for j=1:nRes
              Tag{end+1}  = ['Reservoir ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Reservoir(j).Name;
              Unit{end+1} = FlowUnit;
           end
        end
        assetstruct(i).InfiltrationLoss.Tag = Tag;
        assetstruct(i).InfiltrationLoss.Name = Name;
        assetstruct(i).InfiltrationLoss.Unit = Unit;
        assetstruct(i).InfiltrationLoss.Values = Asset(i).InfiltrationLoss;
    end


    %Turbine
    if Export.Turbine == 1

        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Turbine';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;
        else
           for j=1:nTurb
              Tag{end+1}  = ['Turbine ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Engine(j).Name;
              Unit{end+1} = FlowUnit;
           end
        end

        assetstruct(i).TurbineOperation.Tag = Tag;
        assetstruct(i).TurbineOperation.Name = Name;
        assetstruct(i).TurbineOperation.Unit = Unit;
        assetstruct(i).TurbineOperation.Values = Asset(i).Turbine;

    end

    %Pump
    if Export.Pump == 1 & (nPumps | Export.Aggregated)
        Tag  = {};
        Name = {};
        Unit = {};

        if Export.Aggregated
           Tag{end+1}  = 'Pump';
           Name{end+1} = 'Sum';
           Unit{end+1} = FlowUnit;
        else
           for j=1:nPumps
              Tag{end+1}  = ['Pump ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Engine(j+nTurb).Name;
              Unit{end+1} = FlowUnit;
           end
        end

        assetstruct(i).PumpOperation.Tag = Tag;
        assetstruct(i).PumpOperation.Name = Name;
        assetstruct(i).PumpOperation.Unit = Unit;
        assetstruct(i).PumpOperation.Values = Asset(i).Pump;

    end

    %Market Price
    if Export.Price == 1
        if Data.Export.Scheduler
           Result = Data.Asset(As(i)).Scheduler.Result;
        else
           Result = Data.Asset(As(i)).ScenarioWaterManager.Result;
        end
        PriceModDate = datestr(Result.PriceModificationDate,'dd-mmm-yyyy HH:MM');


        assetstruct(i).MarketPrice.Tag = 'Market Price';
        assetstruct(i).MarketPrice.Name = 'Market Price';
        assetstruct(i).MarketPrice.Unit = 'EUR/MWh';
        assetstruct(i).MarketPrice.Values = Asset(i).Price;

    end

     %Margin Prices
     if Export.MarginPrices == 1 && Export.Separated==1 && ~isempty(Asset(i).MarginPrices)

         Name ={};
         for j = 1:nTurb
             Name{end+1} = ['Turb' num2str(j) ' ' Data.Asset(As(i)).Engine(j).Shortname];
         end
         for j = nTurb+1:nEngines
             Name{end+1} = ['Pump' num2str(j-nTurb) ' ' Data.Asset(As(i)).Engine(j).Shortname];
         end

         assetstruct(i).MarginPrice.Tag = 'Margin Prices';
         assetstruct(i).MarginPrice.Name = Name;
         assetstruct(i).MarginPrice.Unit = 'EUR/MWh';
         assetstruct(i).MarginPrice.Values = Asset(i).MarginPrices;
     end


    %Margin Price Time Series
    if Export.MarginPriceTS == 1 && Export.Separated==1 && ~isempty(Asset(i).MarginPriceTS)


        Tag  = {};
        Name = {};
        Unit = {};

        for j=1:nEngines
           Tag{end+1}  = ['Engine ' num2str(j)];
           Name{end+1} = Data.Asset(As(i)).Engine(j).Name;
           Unit{end+1} = 'EUR/MWh';
        end

         assetstruct(i).MarginPriceTimeSeries.Tag = Tag;
         assetstruct(i).MarginPriceTimeSeries.Name = Name;
         assetstruct(i).MarginPriceTimeSeries.Unit = Unit;
         assetstruct(i).MarginPriceTimeSeries.Values = Asset(i).MarginPriceTS;

    end



    %WaterValues
     if Export.WaterValues == 1 && Export.Separated==1 && ~isempty(Asset(i).WaterValues)
         %WaterValue = XLSAddSheets(Excel,'Water Values');
        Tag  = {};
        Name = {};
        Unit = {};
         for j = 1:nRes
             if Data.Asset(As(i)).Reservoir(j).IsStochastic
                Tag{end+1} = 'Water Value';
                Name{end+1} = ['Res' num2str(j) ' ' Data.Asset(As(i)).Reservoir(j).Shortname];
                Unit{end+1} = ['EUR/' ResUnit];
             end
         end

         assetstruct(i).WaterValue.Tag = Tag;
         assetstruct(i).WaterValue.Name = Name;
         assetstruct(i).WaterValue.Unit = Unit;
         assetstruct(i).WaterValue.Values = Asset(i).WaterValues;

     end


     % WaterValue Time Series
     if Export.WaterValueTS == 1 && Export.Separated==1 && ~isempty(Asset(i).WaterValueTS)

        Tag  = {};
        Name = {};
        Unit = {};

        for j=1:nRes
           if Data.Asset(As(i)).Reservoir(j).IsStochastic
              Tag{end+1}  = ['Reservoir ' num2str(j)];
              Name{end+1} = Data.Asset(As(i)).Reservoir(j).Name;
              Unit{end+1} = [' EUR/' ResUnit];
           end
        end

        assetstruct(i).WaterValueTimeSeries.Tag = Tag;
        assetstruct(i).WaterValueTimeSeries.Name = Name;
        assetstruct(i).WaterValueTimeSeries.Unit = Unit;
        assetstruct(i).WaterValueTimeSeries.Values = Asset(i).WaterValueTS;

     end


    %Reservoir Usage
     if Export.ReservoirUsage == 1 && Export.Separated==1
         %ResUsage = XLSAddSheets(Excel,'Reservoir Usage');

        Tag  = {};
        Name = {};
        Unit = {};
         MinName = {};
         MaxName = {};
         for j = 1:nRes
             Name{end+1} = ['Res' num2str(j) ' ' Data.Asset(As(i)).Reservoir(j).Shortname];
             MinName{end+1} = 'Minimum';
             MaxName{end+1} = 'Maximum';
             Unit{end+1} = ResUnit;
         end


         assetstruct(i).ReservoirUsageMin.Tag = MinName;
         assetstruct(i).ReservoirUsageMin.Name = Name;
         assetstruct(i).ReservoirUsageMin.Unit = Unit;
         assetstruct(i).ReservoirUsageMin.Values = Asset(i).ResUsageMin';

         assetstruct(i).ReservoirUsageMax.Tag = MaxName;
         assetstruct(i).ReservoirUsageMax.Name = Name;
         assetstruct(i).ReservoirUsageMax.Unit = Unit;
         assetstruct(i).ReservoirUsageMax.Values = Asset(i).ResUsageMax';
     end

    %%TODO
    %Revenue
    if Export.Revenues == 1 && Export.Separated==1 %&& strcmp('on',get(handles.checkbox_Revenues,'enable'))

         assetstruct(i).OverallReveneue.Tag = 'Overall Revenues';
         assetstruct(i).OverallReveneue.Name = 'Overall Revenue';
         assetstruct(i).OverallReveneue.Unit = 'EUR';
         assetstruct(i).OverallReveneue.Values = Asset(i).Rev;

         assetstruct(i).HedgeReveneue.Tag = 'Hedge Revenues';
         assetstruct(i).HedgeReveneue.Name = 'Hedge Revenues';
         assetstruct(i).HedgeReveneue.Unit = 'EUR';
         assetstruct(i).HedgeReveneue.Values = Asset(i).HRev;

         assetstruct(i).HedgeValue.Tag = 'Hedge Value';
         assetstruct(i).HedgeValue.Name = 'Hedge Values';
         assetstruct(i).HedgeValue.Unit = 'EUR';
         assetstruct(i).HedgeValue.Values = Asset(i).HVal;

         assetstruct(i).TurbineRevenue.Tag = 'Turbine Revenues';
         assetstruct(i).TurbineRevenue.Name = 'Hedge Values';
         assetstruct(i).TurbineRevenue.Unit = 'EUR';
         assetstruct(i).TurbineRevenue.Values = Asset(i).TurbRev;

         assetstruct(i).PumpCost.Tag = 'Pump Costs';
         assetstruct(i).PumpCost.Name = 'Pump Costs';
         assetstruct(i).PumpCost.Unit = 'EUR';
         assetstruct(i).PumpCost.Values = Asset(i).PumpCost;

         assetstruct(i).VarOpCost.Tag = 'Variable Operating Costs';
         assetstruct(i).VarOpCost.Name = 'Variable Operating Costs';
         assetstruct(i).VarOpCost.Unit = 'EUR';
         assetstruct(i).VarOpCost.Values = Asset(i).VarOpCost;

         assetstruct(i).StartUpCost.Tag = 'Startup Costs';
         assetstruct(i).StartUpCost.Name = 'Startup Costs';
         assetstruct(i).StartUpCost.Unit = 'EUR';
         assetstruct(i).StartUpCost.Values = Asset(i).StartUpCost;

         assetstruct(i).ShutDownCost.Tag = 'Shutdown Costs';
         assetstruct(i).ShutDownCost.Name = 'Shutdown Costs';
         assetstruct(i).ShutDownCost.Unit = 'EUR';
         assetstruct(i).ShutDownCost.Values = Asset(i).ShutDownCost;

         assetstruct(i).Production.Tag = 'Overall Production';
         assetstruct(i).Production.Name = 'Oveall Production';
         assetstruct(i).Production.Unit = 'MWh';
         assetstruct(i).Production.Values = Asset(i).Production;

         assetstruct(i).Consumption.Tag = 'Overall Consumption';
         assetstruct(i).Consumption.Name = 'Oveall Consumption';
         assetstruct(i).Consumption.Unit = 'MWh';
         assetstruct(i).Consumption.Values = Asset(i).Consumption;

         assetstruct(i).OverallReserveRevenue.Tag = 'Overall Reserve Revenue';
         assetstruct(i).OverallReserveRevenue.Name = 'Overall Reserve Revenue';
         assetstruct(i).OverallReserveRevenue.Unit = 'EUR';
         assetstruct(i).OverallReserveRevenue.Values = Asset(i).ResRev;

    end

    %%TODO
   %ReserveRevenue
   if Export.Revenues == 1 && Export.Separated==1 && isfield(Asset(i), 'ReserveRevenues') %&& strcmp('on',get(handles.checkbox_Revenues,'enable'))
       %ReserveRevenue = XLSAddSheets(Excel,'Reserve-Revenues');

        Tag  = {};
        Name = {};
        Unit = {};


       for j = 1:size(Asset(i).ReserveRevenues, 2)
         Name{end+1} = Asset(i).ReserveNames(j);
       end

       assetstruct(i).ReserveRevenue.Tag = 'Reserve Revenue per Scenario';
       assetstruct(i).ReserveRevenue.Name = Name;
       assetstruct(i).ReserveRevenue.Unit = 'EUR';
       assetstruct(i).ReserveRevenue.Values = Asset(i).ReserveRevenues;

   end


   %Revenue monthly
    %%TODO
   if Export.RevenuesMonthly == 1 && Export.Separated==1 %&& strcmp('on',get(handles.checkbox_Revenues,'enable'))


       assetstruct(i).RevenueM.Tag = 'Revenue per Month';
       assetstruct(i).RevenueM.Name = 'Revenue per Month';
       assetstruct(i).RevenueM.Unit = 'EUR';
       assetstruct(i).RevenueM.Values = Asset(i).RevM;

       assetstruct(i).TurbRevM.Tag = 'Turbine Revenues per Month';
       assetstruct(i).TurbRevM.Name = 'Turbine Revenues per Month';
       assetstruct(i).TurbRevM.Unit = 'EUR';
       assetstruct(i).TurbRevM.Values = Asset(i).TurbRevM;

       assetstruct(i).PumpCostM.Tag = 'Pump Costs per Month';
       assetstruct(i).PumpCostM.Name = 'Pump Costs per Month';
       assetstruct(i).PumpCostM.Unit = 'EUR';
       assetstruct(i).PumpCostM.Values = Asset(i).PumpCostM;


       assetstruct(i).VarOpCostM.Tag = 'Variable operation costs per Month';
       assetstruct(i).VarOpCostM.Name = 'Variable operation costs per Month';
       assetstruct(i).VarOpCostM.Unit = 'EUR';
       assetstruct(i).VarOpCostM.Values = Asset(i).VarOpCostM;

       assetstruct(i).StartUpCostM.Tag = 'Startup costs per Month';
       assetstruct(i).StartUpCostM.Name = 'Startup costs per Month';
       assetstruct(i).StartUpCostM.Unit = 'EUR';
       assetstruct(i).StartUpCostM.Values = Asset(i).StartUpCostM;

       assetstruct(i).ShutDownCostM.Tag = 'Shutdown costs per Month';
       assetstruct(i).ShutDownCostM.Name = 'Shutdown costs per Month';
       assetstruct(i).ShutDownCostM.Unit = 'EUR';
       assetstruct(i).ShutDownCostM.Values = Asset(i).ShutDownCostM;

       assetstruct(i).ProductionM.Tag = 'Overall Production per Month';
       assetstruct(i).ProductionM.Name = 'Overall Production per Month';
       assetstruct(i).ProductionM.Unit = 'MWh';
       assetstruct(i).ProductionM.Values = Asset(i).ProductionM;

       assetstruct(i).ConsumptionM.Tag = 'Overall Consumption per Month';
       assetstruct(i).ConsumptionM.Name = 'Overall Consumption per Month';
       assetstruct(i).ConsumptionM.Unit = 'MWh';
       assetstruct(i).ConsumptionM.Values = Asset(i).ConsumptionM;

     end

    %%TODO
     %Revenue engine
     if Export.RevenuesEngine == 1 && Export.Separated==1 %&& strcmp('on',get(handles.checkbox_Revenues,'enable'))

        Tag  = {};
        EngStr = {};
        Unit = {};

         % get engine string

            for j=1:nTurb
               EngStr{end+1} = ['Turb' num2str(j) ' ' Data.Asset(As(i)).Engine(j).Shortname];
            end
            for j=nTurb+1:nEngines
               EngStr{end+1} = ['Pump' num2str(j-nTurb) ' ' Data.Asset(As(i)).Engine(j).Shortname];
            end



        assetstruct(i).EngineTurnover.Tag = 'Engine Turnover per Scenario';
        assetstruct(i).EngineTurnover.Name = EngStr;
        assetstruct(i).EngineTurnover.Unit = 'EUR';
        assetstruct(i).EngineTurnover.Values = Asset(i).TurnoverE;

        assetstruct(i).EngineVariableOpCosts.Tag = 'Variable Operating Costs per Scenario';
        assetstruct(i).EngineVariableOpCosts.Name = EngStr;
        assetstruct(i).EngineVariableOpCosts.Unit = 'EUR';
        assetstruct(i).EngineVariableOpCosts.Values = Asset(i).VarOpCostE;

        assetstruct(i).EngineStartupCosts.Tag = 'Engine Startup Costs per Scenario';
        assetstruct(i).EngineStartupCosts.Name = EngStr;
        assetstruct(i).EngineStartupCosts.Unit = 'EUR';
        assetstruct(i).EngineStartupCosts.Values = Asset(i).StartUpCostE;

        assetstruct(i).EngineShutdownCosts.Tag = 'Engine Shutdown Costs per Scenario';
        assetstruct(i).EngineShutdownCosts.Name = EngStr;
        assetstruct(i).EngineShutdownCosts.Unit = 'EUR';
        assetstruct(i).EngineShutdownCosts.Values = Asset(i).ShutDownCostE;

        assetstruct(i).EngineStartups.Tag = 'Engine # of Startups per Scenario';
        assetstruct(i).EngineStartups.Name = EngStr;
        assetstruct(i).EngineStartups.Unit = 'EUR';
        assetstruct(i).EngineStartups.Values = Asset(i).StartupE;

        assetstruct(i).EngineEnergy.Tag = 'Engine Energy per Scenario';
        assetstruct(i).EngineEnergy.Name = EngStr;
        assetstruct(i).EngineEnergy.Unit = 'MWh';
        assetstruct(i).EngineEnergy.Values = Asset(i).EnergyE;

     end

    %%TODO
     %Revenue engine monthly
     if Export.RevenuesEngineMonthly == 1 && Export.Separated==1 %&& strcmp('on',get(handles.checkbox_Revenues,'enable'))

         EngStr = {};

         % get engine string

            for j=1:nTurb
               EngStr{end+1} = ['Turb' num2str(j) ' ' Data.Asset(As(i)).Engine(j).Shortname];
            end
            for j=nTurb+1:nEngines
               EngStr{end+1} = ['Pump' num2str(j-nTurb) ' ' Data.Asset(As(i)).Engine(j).Shortname];
            end


         % get time string
         tmonth = AdaptTime(DateNum,'monthly');
         nMonths = size(tmonth,1);

         Scenario = repmat([1:nScenarios],nMonths,1);
         Scenario = Scenario(:);

         tmonth = repmat(tmonth,nScenarios,1);
         tmonth = cellstr(tmonth);

         TurnoverEM = zeros(nMonths*nScenarios,nEngines);
         VarOpCostEM = TurnoverEM;
         StartUpCostEM = TurnoverEM;
         ShutDownCostEM = TurnoverEM;
         StartupEM = TurnoverEM;
         EnergyEM = TurnoverEM;

         for j=1:nScenarios
            Idx = [(j-1)*nMonths+1:j*nMonths];

            TurnoverEM(Idx,:) = Asset(i).TurnoverEM(:,:,j);
            VarOpCostEM(Idx,:) = Asset(i).VarOpCostEM(:,:,j);
            StartUpCostEM(Idx,:) = Asset(i).StartUpCostEM(:,:,j);
            ShutDownCostEM(Idx,:) = Asset(i).ShutDownCostEM(:,:,j);
            StartupEM(Idx,:) = Asset(i).StartupEM(:,:,j);
            EnergyEM(Idx,:) = Asset(i).EnergyEM(:,:,j);
         end


        assetstruct(i).EngineTurnoverM.Tag = 'Engine Turnover per Month';
        assetstruct(i).EngineTurnoverM.Name = EngStr;
        assetstruct(i).EngineTurnoverM.Unit = 'EUR';
        assetstruct(i).EngineTurnoverM.Values = Asset(i).TurnoverEM;

        assetstruct(i).EngineVariableOpCostsM.Tag = 'Variable Operating Costs per Month';
        assetstruct(i).EngineVariableOpCostsM.Name = EngStr;
        assetstruct(i).EngineVariableOpCostsM.Unit = 'EUR';
        assetstruct(i).EngineVariableOpCostsM.Values = Asset(i).VarOpCostEM;

        assetstruct(i).EngineStartupCostsM.Tag = 'Engine Startup Costs per Month';
        assetstruct(i).EngineStartupCostsM.Name = EngStr;
        assetstruct(i).EngineStartupCostsM.Unit = 'EUR';
        assetstruct(i).EngineStartupCostsM.Values = Asset(i).StartUpCostEM;

        assetstruct(i).EngineShutdownCostsM.Tag = 'Engine Shutdown Costs per Month';
        assetstruct(i).EngineShutdownCostsM.Name = EngStr;
        assetstruct(i).EngineShutdownCostsM.Unit = 'EUR';
        assetstruct(i).EngineShutdownCostsM.Values = Asset(i).ShutDownCostEM;

        assetstruct(i).EngineStartupsM.Tag = 'Engine # of Startups per Month';
        assetstruct(i).EngineStartupsM.Name = EngStr;
        assetstruct(i).EngineStartupsM.Unit = 'EUR';
        assetstruct(i).EngineStartupsM.Values = Asset(i).StartupEM;

        assetstruct(i).EngineEnergyM.Tag = 'Engine Energy per Month';
        assetstruct(i).EngineEnergyM.Name = EngStr;
        assetstruct(i).EngineEnergyM.Unit = 'MWh';
        assetstruct(i).EngineEnergyM.Values = Asset(i).EnergyEM;

     end

    %xxx
    if Export.EngineConstraints

         EngStr = {};

         % get engine string
            for j=1:nTurb
               EngStr{end+1} = ['Turb' num2str(j) ' ' Data.Asset(As(i)).Engine(j).Shortname];
            end
            for j=nTurb+1:nEngines
               EngStr{end+1} = ['Pump' num2str(j-nTurb) ' ' Data.Asset(As(i)).Engine(j).Shortname];
            end

        for j = 1:nEngines


            Eng = Data.Asset(As(i)).Engine(j);
            % Revisionsplan holen
            %if Input.Asset.Type == 1 %nicht für Optionen, nur für HPs
            MaxPower = getTSValues(Eng.MaxFlowFile,DateNum(1),DateNum(end),'Silent', Data);
            MinPower = getTSValues(Eng.MinFlowFile,DateNum(1),DateNum(end),'Silent', Data);
            MinRunningPower = getTSValues(Eng.MinRunningFlowFile,DateNum(1),DateNum(end),'Silent', Data);

            assetstruct(i).MaxPower.Values(:,j) = MaxPower;
            assetstruct(i).MinPower.Values(:,j) = MinPower;
            assetstruct(i).MinRunningPower.Values(:,j) = MinRunningPower;


        end

        assetstruct(i).MaxPower.Tag = 'Engine Max Power';
        assetstruct(i).MaxPower.Name = EngStr;
        assetstruct(i).MaxPower.Unit = 'MW';

        assetstruct(i).MaxPower.Tag = 'Engine Min Power';
        assetstruct(i).MinPower.Name = EngStr;
        assetstruct(i).MinPower.Unit = 'MW';

        assetstruct(i).MinRunningPower.Tag = 'Engine Min Running Power';
        assetstruct(i).MinRunningPower.Name = EngStr;
        assetstruct(i).MinRunningPower.Unit = 'MW';

    end

    if Export.ReservoirConstraints

         ResStr = {};

         % get engine string

            for j=1:nRes
               ResStr{end+1} = ['Res' num2str(j) ' ' Data.Asset(As(i)).Reservoir(j).Shortname];
            end


        for j = 1:nRes


            Res = Data.Asset(As(i)).Reservoir(j);
            % Revisionsplan holen
            %if Input.Asset.Type == 1 %nicht für Optionen, nur für HPs
            MaxLevel = getTSValues(Res.MaxLevelFile,DateNum(1),DateNum(end),'Silent', Data);
            MinLevel = getTSValues(Res.MinLevelFile,DateNum(1),DateNum(end),'Silent', Data);

            assetstruct(i).MaxLevel.Values(:,j) = MaxLevel;
            assetstruct(i).MinLevel.Values(:,j) = MinLevel;
        end

        assetstruct(i).MaxPower.Tag = 'Engine Max Power';
        assetstruct(i).MaxPower.Name = ResStr;
        assetstruct(i).MaxPower.Unit = 'MW';

        assetstruct(i).MinPower.Tag = 'Engine Min Power';
        assetstruct(i).MinPower.Name = ResStr;
        assetstruct(i).MinPower.Unit = 'MW';

    end

    assetstruct(i).Hour.Tag = 'Time Samples';
    assetstruct(i).Hour.Name = Data.Asset(As(i)).Name;
    assetstruct(i).Hour.Unit = 'h';
    assetstruct(i).Hour.Values = DateNum;

    tmonth = AdaptTime(DateNum,'monthly');
    nMonths = size(tmonth,1);

   %Scenario = repmat([1:nScenarios],nMonths,1);
    %Scenario = Scenario(:);

    Scenario = 1:nScenarios;

    tmonth = repmat(tmonth,nScenarios,1);

    assetstruct(i).Month.Tag = 'Months';
    assetstruct(i).Month.Name = Data.Asset(As(i)).Name;
    assetstruct(i).Month.Unit = 'Month';
    assetstruct(i).Month.Values = tmonth;

    assetstruct(i).Scenario.Tag = 'Scenarios';
    assetstruct(i).Scenario.Name = Data.Asset(As(i)).Name;
    assetstruct(i).Scenario.Unit = '';
    assetstruct(i).Scenario.Values = Scenario;

    if ~isempty(Export.Filename)
        save(FileName{1}, 'assetstruct');
    end

end

Status = 1;


%%********************************************************************************************
function [Values,MinStart,MaxEnd,Msg,Format] = getTSValues(varargin)
% Values = getValues(FileName,DateNumStart,DateNumEnd,Context)

basePath = Data.Reference.PathName;

nargs = nargin;
FileName = varargin{1};
Data = varargin{end};
Context = 'Silent';

%Lese Prefix- und Postfix-Anteil (Trennung durch "//")
FileNameSplit = strsplit(FileName,'//');
FileName = FileNameSplit{1};
PostfixOperations = '';
if length(FileNameSplit) > 1
    PostfixOperations = FileNameSplit(2:end);
end

try
    repl = @(s,s1,s2,r) regexprep(s,strcat('(?=',s1,').*(?<=',s2,')'),r(regexp(s,strcat('(?<=',s1,').*(?=',s2,')'),'match')));
    %Data = get(gcf,'userdata');
    i = Data.Status.BatchManager.Current;
    n = Data.Status.BatchManager.nSteps;
    FileName = repl(FileName,'{','}',@(x) num2str(eval(x{1})));
catch
end

Values = [];
MinStart = [];
MaxEnd = [];
Msg = [];
Format = [];

for i=2:nargin % Context is the only argument in string format (apart from filename)
  if isstr(varargin{i})
     Context = varargin{i};
     nargs  = nargs  -1;
  end
end

switch nargs
case 2
   DateNumStart = varargin{2};
   DateNumEnd = varargin{2};
case 3
   DateNumStart = varargin{2};
   DateNumEnd = varargin{3};
end



% return if file is empty
if isempty(FileName)
   Msg = 'No file defined.';
   return
end

% relative paths are given
if FileName(1) == '.' % CHANGES CHANGES
    %Data = get(gcf,'userdata');
   FileName = fullfile(basePath,FileName(2:end));
end

if exist(FileName)
   [Msg,A,Format] = getCSVFile(FileName);

   if isempty(Msg) % if no error has occured in reading the file
    if nargs  >= 2
      MinStart = A.DateNum(1);
      MaxEnd = A.DateNum(end);

      [start_idx,end_idx] = findT(A.DateNum , DateNumStart, DateNumEnd);

      Values = A.Values(start_idx:end_idx);
      if isempty(start_idx) || isempty(end_idx)
         [Path,Name,Ext] =  fileparts(FileName);
         Msg = ['File ''' Name Ext ''' : Definition interval does not match time horizon.'];
      end

    elseif nargs  == 1
      MinStart = A.DateNum(1);
      MaxEnd = A.DateNum(end);

      Values = A.Values;
    end

    Values = Values(:);
   end

elseif findstr(FileName,'>')  % Check whether a special option type is given

   if nargs > 1 % at least DateNumStart is given
      t = getHydroptTime(DateNumStart,DateNumEnd);
   else % user wants all data available
      t = getHydroptTime;
   end

   ColonIdx = findstr(FileName,'>');
   Val = str2num(FileName(1:ColonIdx-1));
   Rem = FileName(ColonIdx+1:end);

   if isequal(Rem,'Peak');  % Value>Peak, e.g. 50>Peak  % CHANGES CHANGES
      Values = Val * getPeak(t);
   elseif findstr(Rem,'<')  % Value1>Date<Value2, e.g. 2000>20060101<250
      Val1 = Val;
      Val2 = str2num(Rem(10:end));
      Values = Val1*ones(size(t));

      ChangeDate = datenum(Rem(1:8),'yyyymmdd');
      Idx = findT(t,ChangeDate);

      if ~isempty(Idx)
         Values(Idx:end) = Val2;
      elseif ChangeDate < t(1)
         Values = Val2;
      end % otherwise all the time is Value1

   else % Value>FromHour-ToHour , e.g. 50>7-21
      BarIdx = findstr(Rem,'-');
      FromHour = str2num(Rem(1:BarIdx-1));
      ToHour = str2num(Rem(BarIdx+1:end));

      Profile = zeros(24,3);
      Profile(FromHour:ToHour,:) = 1;

      Values = Val * getProfile(t,Profile);
   end

   Values = Values(:);
   MinStart = -Inf;
   MaxEnd = Inf;

elseif length(str2num(FileName))  % Check whether a number is given

   if nargs > 1 % at least DateNumStart is given
      t = getHydroptTime(DateNumStart,DateNumEnd);
   else % user wants all data available
      t = getHydroptTime;
   end

   Values = ones(size(t)) * str2num(FileName);
   Values = Values(:);
   MinStart = -Inf;
   MaxEnd = Inf;

else
   [Path,Name,Ext] =  fileparts(FileName);
   Msg = ['File ''' Name Ext ''' not found.'];
end

if ~isempty(Msg) && ~isequal(Context,'Silent')

   StrLength = max(length(Context),length(Msg));
   Str = char(zeros(2,StrLength));

   Str(1,1:length(Context)) = Context;
   Str(2,1:length(Msg)) = Msg;

   errordlg(Str);
%   error(Str);
end

try
    %Data = get(gcf,'Userdata');
    p = Data.ScenarioWaterManager.PostScript.Variables;
    v = Values;
    t0 = DateNumStart;
    t1 = DateNumEnd;
    t = getHydroptTime(t0, t1);
    nTimeSteps = length(t);
    Range = @(a,n) (a:(a+n-1))';
    fxx = @(f,x) f(x,x);

    Period = @(v) [repmat(v, floor(nTimeSteps/length(v)), 1); v(1:mod(nTimeSteps,length(v)))];
    Rep = @(v, n) repmat(v, n, 1);
    Rep2 = @(v, n) repmat(v, 1, n);

    STRIPLEADINGZEROSPROXY = @(out,in) out(find(in,1):end);
    STRIPLEADINGZEROS = @(v) STRIPLEADINGZEROSPROXY(v,v);

    FULLPATH = @(path) fullfile(basePath(1:length(basePath)*(path(1)=='.')), path((path(1)=='.')+1:end));
    CSV = @(path) AlignTimeSeries(t, getCSVFileDateNum(FULLPATH(path)), getCSVFileValues(FULLPATH(path)), 0);
    CSVp = @(path) AlignTimeSeries(t, getCSVFileDateNum(FULLPATH(path)), Period(getCSVFileValues(FULLPATH(path))), 0);
    CSVn = @(path,n) AlignTimeSeries(t, getCSVFileDateNum(FULLPATH(path)), Rep2(getCSVFileValues(FULLPATH(path)),n), 0);
    %periodischer CSV-Import, wobei führende Nullen gelöscht werden
    CSVp0 = @(path) AlignTimeSeries(t, STRIPLEADINGZEROSPROXY(getCSVFileDateNum(FULLPATH(path)),getCSVFileValues(FULLPATH(path))), Period(STRIPLEADINGZEROS(getCSVFileValues(FULLPATH(path)))), 0);
    %TS = @(Y,M,D,H, v) AlignTimeSeries(t, Range(fxx(@getProperTime,datenum(Y,M,D,H,0,0)),length(v)), v, 0);
    TS = @(Y,M,D,H, v) AlignTimeSeries(t, fxx(@getProperTime,datenum(Y,M,D,H,0,0)), v, 0);
    D2H = @(v) reshape(kron(v,ones(24,1)),1,[]);
    XLS = @(Y,M,D,H, path, sheet, range) AlignTimeSeries(t, getProperTime(datenum(Y,M,D,H,0,0)), xlsread(FULLPATH(path), sheet, range), 0); %xls hourly
    XLSdaily = @(Y,M,D, path, sheet, range) TS(Y,M,D,1, D2H(xlsread(FULLPATH(path), sheet, range)));

    Base = @(Y1, M1, D1, Y2, M2, D2) TS(Y1, M1, D1, 1, sign(        getProperTime(datenum(Y1,M1,D1,1,0,0),datenum(Y2,M2,D2,1,0,0))));
    Peak = @(Y1, M1, D1, Y2, M2, D2) TS(Y1, M1, D1, 1, sign(getPeak(getProperTime(datenum(Y1,M1,D1,1,0,0),datenum(Y2,M2,D2,1,0,0)))));
    Offp = @(Y1, M1, D1, Y2, M2, D2) 1 - Peak(Y1, M1, D1, Y2, M2, D2);

    BaseY = @(Y) Base(Y,1,1,Y+1,1,1);
    PeakY = @(Y) Peak(Y,1,1,Y+1,1,1);
    OffpY = @(Y) Offp(Y,1,1,Y+1,1,1);

    BaseQ = @(Y,Q) Base(Y,3*(Q-1)+1,1,Y,3*Q+1,1);
    PeakQ = @(Y,Q) Peak(Y,3*(Q-1)+1,1,Y,3*Q+1,1);
    OffpQ = @(Y,Q) Offp(Y,3*(Q-1)+1,1,Y,3*Q+1,1);

    BaseM = @(Y,M) Base(Y,M,1,Y,M+1,1);
    PeakM = @(Y,M) Peak(Y,M,1,Y,M+1,1);
    OffpM = @(Y,M) Offp(Y,M,1,Y,M+1,1);

    BaseD = @(Y,M,D) Base(Y,M,D,Y,M,D+1);
    PeakD = @(Y,M,D) Peak(Y,M,D,Y,M,D+1);
    OffpD = @(Y,M,D) Offp(Y,M,D,Y,M,D+1);

    Constant = @(v) v*ones(nTimeSteps, 1); %konstante Vektoren
    %Stretch = @(v, n) Prokrustes(kron(v, ones(n,1)), nTimeSteps); %Dehnen von Vektoren
    Avg = @(v, n) moving(v, n); %Moving average

    TwoStates = @(v1, n1, v2, n2) Period([Rep(v1, n1); Rep(v2, n2)]);
    ThreeStates = @(v1, n1, v2, n2, v3, n3) Period([Rep(v1, n1); Rep(v2, n2); Rep(v3, n3)]);
    HTNT = @(ht, nt) ThreeStates(nt, 6, ht, 16, nt, 2); %Hochtarif/Niedertarif
    Normalize = @(v) v/sum(v);
    MonthlyProfile = @(m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12) ... %Jahresprofil mit minatlicher Granularität geglättet und normalisiert auf Jahresproduktion von 1
        8760/nTimeSteps*Normalize(Avg(Period([...
        Rep(m1, 31*24); ...
        Rep(m2, 28*24); ...
        Rep(m3, 31*24); ...
        Rep(m4, 30*24); ...
        Rep(m5, 31*24); ...
        Rep(m6, 30*24); ...
        Rep(m7, 31*24); ...
        Rep(m8, 31*24); ...
        Rep(m9, 30*24); ...
        Rep(m10, 31*24); ...
        Rep(m11, 30*24); ...
        Rep(m12, 31*24)]), 30*24));
    DeltaFun = @(i) circshift(eye(nTimeSteps,1), [i+1, 0]);

    for operations = PostfixOperations
       op = operations{1};
       if length(strfind(op, '"')) == 2
           try
            op = regexp(op,'((?<=").*(?="))','match');
            op = fileread(op{1});
            eval(op);
           catch
               disp(['Inline function: error reading file ' op]);
           end
       else
            v = eval(op);
       end
       dimv = size(v);
       if dimv(1) < dimv(2)
         v = v';
       end
    end

catch
end
Values = v;

function [Msg,A,Format] = getCSVFile(FileName)
% reads timeseries from csvfile

Msg = '';
A = [];
Format = 'Custom';

[Msg, Dat, Val] = getCustomFormat(FileName);
if ~isempty(Msg)
   [Msg, Dat, Val] = getHydroptFormat(FileName);
   Format = 'Hydropt';
end

if ~isempty(Msg)
    return
end

Data = get(gcf,'userdata');
TimeShift = iff(Data.Status.Import.FromTime == 0,0,1/24);

t = getHydroptTime(Dat-TimeShift,Dat+length(Val)/24 + 10);  % get timeframe larger than that of file

A.DateNum = t(1:length(Val));
A.Values = Val;








function [Msg, Dat, Val] = getCustomFormat(FileName)

Data = get(gcf,'Userdata');

Msg = [];
Dat = [];
Val = [];

% get full file name
[Dummy,Name,Ext] = fileparts(FileName);
NameExt = [Name Ext];

fclose('all');
% if strcmp(Data.Status.Import.DecimalSeparator,',')
%    eval(['dos(''alter ' NameExt ' "," "."'')']);
% end

% open file
f=fopen(FileName);

for l = 1:Data.Status.Import.StartDate.Row
    line = fgetl(f);
end

SepPos = find(line == Data.Status.Import.ColumnSeparator);
if ~isempty(SepPos)  % Wenn line separator vorliegt, zweispaltiges Format
   DateString = line(1:SepPos-1);
else
   DateString = line;  % Einspaltiges Format
end

try
   %versuche Fehler im Datumsformat zu korrigieren
   if abs(length(Data.Status.Import.DateFormat) - length(DateString)) < 3
       Dat = datenum(DateString,Data.Status.Import.DateFormat);
   elseif length(Data.Status.Import.DateFormat) > length(DateString)
       Dat = datenum(DateString,'dd.mm.yyyy');
   elseif length(Data.Status.Import.DateFormat) < length(DateString)
       Dat = datenum(DateString,'dd.mm.yyyy HH:MM');
   end
catch
  fclose(f);
  Msg = ['File ''' NameExt ''': Date format does not match specified format.'];
  return
end


try
   Val = dlmread(FileName,Data.Status.Import.ColumnSeparator,Data.Status.Import.FirstValue.Row-1,Data.Status.Import.FirstValue.Column-1);
catch
   fclose(f);
   Msg = ['File ''' NameExt ''': Value format not recognized. First line should be date, all other lines numeric values.'];
   return
end

if isempty(Val)
    fclose(f);
    Msg = ['File''' NameExt ''': Could not read values. Check File format'];
    return
end

fclose(f);





function [Msg, Dat, Val] = getHydroptFormat(FileName)

Data = get(gcf,'Userdata');

Msg = [];
Dat = [];
Val = [];

% get full file name
[Dummy,Name,Ext] = fileparts(FileName);
NameExt = [Name Ext];

fclose('all');

% open file
f=fopen(FileName);

DateString = fgetl(f);

try
   Dat = datenum(DateString,Data.Status.Import.HydroptDateFormat);
catch
  fclose(f);
  Msg = ['File ''' NameExt ''': Date format does not match specified format.'];
  return
end


try
   Val = dlmread(FileName,';',1,0);
catch
   fclose(f);
   Msg = ['File ''' NameExt ''': File format not recognized.'];
   return
end


fclose(f);

function d = getCSVFileDateNum(FileName)
[~,A,~] = getCSVFile(FileName);
d = A.DateNum;

function v = getCSVFileValues(FileName)
[~,A,~] = getCSVFile(FileName);
v = A.Values;



%**************************************************************************
function TS = AdaptUnitMW(TSMW,AlphaPower,UnitMW)
% Transforms the Unit of the output to the desired format

if UnitMW % Unit = MWh -> export as is
   TS = TSMW;
else       % Unit = M3 -> transform to M3
   TS = TSMW(:)./AlphaPower(:);
end
TS = TS(:);



%%****************************************************************************
function out=iff(a,b,c)

if a
   out = b;
else
   out = c;
end








